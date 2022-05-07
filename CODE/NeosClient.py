#!/usr/bin/env python

# Copyright (c) 2017 NEOS-Server
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Python XML-RPC client for NEOS Server
=====================================

The original Python code has been lightly modified.
This code, additionally, does the following:
1. saves the solver output to a file
2. prints more status messages to screen

To view the orginal source code, visit repository:
https://github.com/NEOS-Server/PythonClient

For more information on the XML-RPC API for NEOS, go to:
https://neos-server.org/neos/xml-rpc.html

To run code:
> python NeosClient.py Ruby_sun.xml --writetofile ../NEOS_OUTPUT/Ruby_sun_neos.txt
OR, to read queue
> python NeosClient.py queue

Code modifications by:
Kalyani Nagaraj
May 2021
"""

import argparse
import os
import sys
import time
import re
try:
  import xmlrpc.client as xmlrpclib
except ImportError:
  import xmlrpclib


parser = argparse.ArgumentParser()
parser.add_argument("action", help="specify XML file name or queue for action")
parser.add_argument("--server", default="https://neos-server.org:3333", help="URL to NEOS Server XML-RPC interface")
parser.add_argument("--username", default=os.environ.get("NEOS_USERNAME", None), help="username for NEOS Server user account")
parser.add_argument("--password", default=os.environ.get("NEOS_PASSWORD", None), help="password for NEOS Server user account")
parser.add_argument("--writetofile", default="../NEOS_OUTPUT/neos-output.txt", help="write optimization output to this file")

args = parser.parse_args()

neos = xmlrpclib.ServerProxy(args.server)

sys.stdout.write("Attempting to connect to NEOS Server ... \n")
alive = neos.ping()
if alive != "NeosServer is alive\n":
    sys.stderr.write("Could not make connection to NEOS Server\n")
    sys.exit(1)

sys.stdout.write("Connection successful!\n")
if args.action == "queue":
    msg = neos.printQueue()
    sys.stdout.write("Printing queue ... \n")
    sys.stdout.write(msg)
else:
    xml = ""
    try:
        xmlfile = open(args.action, "r")
        buffer = 1
        while buffer:
            buffer = xmlfile.read()
            xml += buffer
        xmlfile.close()
    except IOError as e:
        sys.stderr.write("I/O error(%d): %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    sys.stdout.write("Sending job to server ... \n")
    if args.username and args.password:
        (jobNumber, password) = neos.authenticatedSubmitJob(xml, args.username, args.password)
    else:
        (jobNumber, password) = neos.submitJob(xml)
    sys.stdout.write("Job number = %d\nJob password = %s\n" % (jobNumber, password))
    if jobNumber == 0:
        sys.stderr.write("NEOS Server error: %s\n" % password)
        sys.exit(1)
    else:
        offset = 0
        status = ""
        sys.stdout.write("Waiting for job to complete ... \n")
        while status != "Done":
            time.sleep(1)
            (msg, offset) = neos.getIntermediateResults(jobNumber, password, offset)
            sys.stdout.write(msg.data.decode())
            status = neos.getJobStatus(jobNumber, password)
        msg = neos.getFinalResults(jobNumber, password)
        sys.stdout.write(msg.data.decode())

        lines = iter(re.split('\n+', msg.data.decode()))  # list object is not an iterator and must be converted to one using the iter() function
        with open(args.writetofile, 'w') as f:
            while True:   # Ignore lines upto
            # "*** Cities are numbered 0..n-1 and each line shows a leg from one city to the next followed by the distance rounded to integers***"
                line = next(lines)
                if "distance rounded to integers***" in line:
                    break

            while True:  # Print all following lines to file
                line = next(lines)
                if not line:
                    break

                f.write(line)
                f.write("\n")
