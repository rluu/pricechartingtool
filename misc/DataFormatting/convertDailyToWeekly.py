#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script creates a weekly CSV file of pricebar data,
#   from a daily CSV file of pricebar data.
#
# Usage:
#
#   ./convertDailyToWeekly.py --help
#   ./convertDailyToWeekly.py --version
#
#   ./convertDailyToWeekly.py --input-file="/tmp/soybeans_daily.txt" --output-file="/tmp/soybeans_weekly.txt"
#   
##############################################################################

import sys
import os
import copy

# For parsing command-line options
from optparse import OptionParser  

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# Input CSV text file.
# This value is obtained via command-line parameter.
inputFile = ""

# Output CSV text file.
# This value is obtained via command-line parameter.
outputFile = ""

# Number of lines of text to skip in the CSV data files.  This is
# usually a header line that just displays what the columns are.
# This value is obtained via command-line parameter.
linesToSkip = 1

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""

# Use Windows newlines.
newline = "\r\n"

##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--input-file",
                  action="store",
                  type="str",
                  dest="inputFile",
                  default=None,
                  help="Specify input pricebar CSV data file.  This file should have daily pricebars.",
                  metavar="<FILE>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file that will have weekly pricebars.",
                  metavar="<FILE>")


# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    sys.exit(0)


if (options.inputFile == None):
    print("Error: Please specify an input file to the " + \
          "--input-file option.")
    sys.exit(1)
else:
    # Make sure the input file path is good.
    if not os.path.exists(options.inputFile):
        print("Error: The input file provided does not exist: {}".\
              format(options.inputFile))
        sys.exit(1)
        
    # Save the value.
    inputFile = options.inputFile

if (options.outputFile == None):
    print("Error: Please specify an output filename to the " + \
          "--output-file option.")
    sys.exit(1)
else:
    outputFile = options.outputFile

        
##############################################################################

print("ERROR:  Program is not completely coded.  Please finish coding and testing this script to do what we want it to do.")
sys.exit(1)


# Lines in the destination file.
convertedLines = []

# Read input file.
with open(inputFile) as f:
    i = 0
    for line in f:
        if i >= linesToSkip:

            # Check the number of fields.
            fields = line.split(",")
            numFieldsExpected = 7
            if len(fields) != numFieldsExpected:
                print("Error: Line does not have {} data fields".\
                      format(numFieldsExpected))
                sys.exit(1)
            
            dateStr = fields[0].strip()
            openStr = fields[1].strip()
            highStr = fields[2].strip()
            lowStr = fields[3].strip()
            closeStr = fields[4].strip()
            volumeStr = fields[5].strip()
            openIntStr = fields[6].strip()
            
            # Make sure date is the right length.
            if len(dateStr) != 10:
                print("Error: dateStr is not the expected number " +
                      "of characters: " + dateStr)
                sys.exit(1)
                
            #print("DEBUG: dateStr == {}".format(dateStr))
            monthStr = dateStr[0:2]
            dayStr = dateStr[3:5]
            yearStr = dateStr[6:10]
            
            convertedLines.append(convertedLine)
            
        i += 1


# Insert header line.
convertedLines.insert(0, headerLine)

# Write to file, truncating if it already exists.
with open(outputFile, "w") as f:
    for line in convertedLines:
        f.write(line.rstrip() + newline)
        
print("Done.")

