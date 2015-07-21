#!/bin/bash
##############################################################################
#
# File:    generateResourceSourceFile.sh
#
# Description:
#    
#          This script uses PyQt command pyrcc5 to generate the .py source file
#          with the embedded binary data of resources.  
#
#          This script should be re-run if the resources file or resources
#          change.
#
# Usage:
# 
#          ./generateResourceSourceFile
#
##############################################################################


##############################################################################
# Variables
##############################################################################

# Get the directory where this script is running.
scriptDirectory=`dirname "$0"`

# Set the output filename.
outputFile=$scriptDirectory/../src/resources.py

# Set the input filename.
inputFile=$scriptDirectory/resources.qrc

##############################################################################


# Generate output file from input file resource listing.
cmdToRun="pyrcc5 -o $outputFile $inputFile"
echo "$cmdToRun"
$cmdToRun

