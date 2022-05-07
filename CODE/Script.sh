#!/bin/sh

#  Script.sh:
#  Generate an XML file to send to NEOS. Then send the optimization problem
#  (wrapped in the XML file) to NEOS by calling NeosClient.py.
#  Finally, generate a an svg image file by calling genArt.py
#  The script can be changed to allow for different file naming conventions and
#  a different filing system
#
#  Example:
#  > sh Script.sh Ruby_sun black 1.2
#
#  Requires:
#    1. IMAGES/Ruby_sun.pbm
#
#  Generates:
#    1. PYTHON_OUTPUT/Ruby_sun.txt
#    2. PYTHON_OUTPUT/Ruby_sun.pkl
#    3. NEOS_INPUT/Ruby_sun.xml
#    4. NEOS_OUTPUT/Ruby_sun_neos.txt
#    5. IMAGES/TSP_IMAGES/Ruby_sun.svg
#
#
#  Created by Kalyani Nagaraj on 26 March, 2022.


cd /Users/kalyani/0_FUN/TSPArt/PYTHON
python3 genCoordinates.py ../IMAGES/$1.pbm ../PYTHON_OUTPUT/$1.txt ../PYTHON_OUTPUT/$1.pkl
python3 genXML.py ../PYTHON_OUTPUT/$1.txt ../NEOS_INPUT/$1.xml
python NeosClient.py ../NEOS_INPUT/$1.xml --writetofile ../NEOS_OUTPUT/$1_neos.txt
python3 genArt.py ../NEOS_OUTPUT/$1_neos.txt ../IMAGES/TSP_IMAGES/$1.svg ../PYTHON_OUTPUT/$1.pkl $2 $3
