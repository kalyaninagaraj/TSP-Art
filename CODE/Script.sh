#!/bin/sh

#  Script.sh:
#  Generate an XML file to send to NEOS. Then send the optimization problem
#  (wrapped inside an XML file) to NEOS by calling `NeosClient.py`.
#  Finally, generate a an SVG image file by calling `genArt.py`.
#  This script can be changed to allow for different file naming conventions
#  and a different filing system.
#
#  Example: Generate a continuous line drawing of Hank Marvin
#    > sh Script.sh HM black 1.3
#
#  Requires: A PBM file containing a stippled image of Hank
#    ../IMAGES/HM.pbm
#
#  Generates:
#    1. ../PYTHON_OUTPUT/HM.txt
#    2. ../PYTHON_OUTPUT/HM.pkl
#    3. ../NEOS_INPUT/HM.xml
#    4. ../NEOS_OUTPUT/HM_neos.txt
#    5. ../IMAGES/TSP_IMAGES/HM.svg     <--- file containing final line drawing
#
#  Created by Kalyani Nagaraj on March, 2022


python3 genCoordinates.py ../IMAGES/$1.pbm ../PYTHON_OUTPUT/$1.txt ../PYTHON_OUTPUT/$1.pkl
python3 genXML.py ../PYTHON_OUTPUT/$1.txt ../NEOS_INPUT/$1.xml
python NeosClient.py ../NEOS_INPUT/$1.xml --writetofile ../NEOS_OUTPUT/$1_neos.txt
python3 genArt.py ../NEOS_OUTPUT/$1_neos.txt ../IMAGES/TSP_IMAGES/$1.svg ../PYTHON_OUTPUT/$1.pkl $2 $3
