'''
Generate an XML file to send to the CPLEX MILP solver on NEOS

To run code:
> python genXML.py path/to/TSP_city_coordinates_file.txt path/to/output_XML_file.xml

For example:
> python3 genXML.py ../PYTHON_OUTPUT/HM.txt ../NEOS_INPUT/HM.xml

Requires:
Input in the form of a .txt file of city coordinates:
path/to/TSP_city_coordinates_file.txt (e.g., ../PYTHON_OUTPUT/HM.txt)

Generates:
An .xml file: path/to/output_XML_file.xml (e.g., ../NEOS_INPUT/HM.xml)

Author:
Kalyani Nagaraj
March 2022
'''
import argparse
import sys
from bs4 import BeautifulSoup
from bs4 import CData

parser = argparse.ArgumentParser()
parser.add_argument("action", help="specify data file for generating XML")
parser.add_argument("target", help="specify target XML file name")
parser.add_argument("--alg", help="specify algorithm for solving TSP", default="lk")

args = parser.parse_args()

try:
    city_coord = ""
    f = open(args.action, "r")
    buffer = 1
    while buffer:
        buffer = f.read()
        city_coord += buffer
    f.close()
except OSError as e:
    sys.stderr.write("I/O error(%d): %s : %s\n" % (e.errno, args.action, e.strerror))
    sys.exit(1)

myemail = input('Enter a valid email to submit the job on NEOS: ')

bs_data  = BeautifulSoup(
"<document><category>co</category><solver>concorde</solver>\
<inputMethod>TSP</inputMethod><email></email><priority></priority><dat2></dat2>\
<dat1></dat1><tsp></tsp><ALGTYPE></ALGTYPE><RDTYPE></RDTYPE><PLTYPE></PLTYPE>\
</document>", 'xml')

bs_data.dat2.insert(0, CData(city_coord))   # use dat2 if distances are measured in L2 norm, and dat1 if using L1 norm
bs_data.priority.insert(0, CData('long'))   # long priority = longer runtime
bs_data.email.insert(0, CData(myemail))     # valid email required by NEOS
bs_data.ALGTYPE.insert(0, CData(args.alg))  # cqs=QSopt, con=CPLEX, lk=Lin-Kernighan (default)
bs_data.RDTYPE.insert(0, CData('variable')) # random seed (fixed=99 [default], variable=random)
bs_data.PLTYPE.insert(0, CData('no'))       # Plot optimal tour? (no [default], cp=yes (to PDF), pf=w/o cities (to PDF))

try:
    with open(args.target, 'w') as f:
        f.write(str(bs_data))   # Don't prettify the xml by calling  f.write(bs_data.prettify())
except OSError as e:
    sys.stderr.write("I/O error(%d): %s: %s\n" % (e.errno, args.target, e.strerror))
    sys.exit(1)
