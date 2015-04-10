#!/usr/bin/env python3
##############################################################################
# Script to convert CSV files in the CSV format provided by
# quandl.com to the format that we use in PriceChartingTool.
#
# Usage:
#
#   ./reformatFuturesData_Quandl_CSV_File.py --help
#   ./reformatFuturesData_Quandl_CSV_File.py --version
#
#   ./reformatFuturesData_Quandl_CSV_File.py --input-file=/tmp/input.csv \
#                                            --output-file=/tmp/output.txt
#
##############################################################################

import sys
import os
import copy

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# Input CSV file obtained from Quandl.com.
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

# Use these types newlines in the output file.
newline = "\n"

# For logging.
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    logging.shutdown()
    sys.exit(rc)


def reformatQuandlDateField(dateStr):
    """Converts a date string in the format YYYY-MM-DD to MM/DD/YYYY.
    The converted string is returned.
    """
    
    dateFields = dateStr.split("-")
    if len(dateFields) != 3:
        log.error("Field for date is not in the expected format: {}".\
              format(dateStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)

    yearStr = dateFields[0]
    monthStr = dateFields[1]
    dayStr = dateFields[2]

    # Check inputs.
    if (len(monthStr) != 1 and len(monthStr) != 2) or \
           (not monthStr.isnumeric()):
        log.error("month in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)
    if (len(dayStr) != 1 and len(dayStr) != 2) or (not dayStr.isnumeric()):
        log.error("day in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)
    if len(yearStr) != 4 or (not yearStr.isnumeric()):
        log.error("year in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)

    # Make sure monthStr and dayStr is two characters.
    if len(monthStr) == 1:
        monthStr = "0" + monthStr
    if len(dayStr) == 1:
        dayStr = "0" + dayStr
    
    rv = "{}/{}/{}".format(monthStr, dayStr, yearStr)

    return rv

def reformatQuandlDataLine(line):
    """Converts the CSV line format to our desired format.

    Quandl.com gives us lines in the format:
        Date,Open,High,Low,Last,Change,Settle,Volume,Prev. Day Open Interest
        2004-11-17,316.0,319.0,314.0,,,318.5,28192.0,54451.0

    We want it in format:
        "Date","Open","High","Low","Close","Volume","OpenInt"
        07/23/1969,137,137,134.75,135,370,180

    Returns: the converted string
    """

    fields = line.split(",")
    
    if len(fields) != 9:
        log.error("Input line from Quandl isn't in the " + \
                  "expected format.  Line given is: {}".format(line))
        shutdown(1)

    dateStr = fields[0].strip()
    openStr = fields[1].strip()
    highStr = fields[2].strip()
    lowStr  = fields[3].strip()
    closeStr = fields[6].strip()
    volumeStr = fields[7].strip()
    openIntStr = fields[8].strip()

        
    # Check inputs.
    if not isNumber(openStr):
        log.error("Field for open price is not a valid number: {}".\
              format(openStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)
    if not isNumber(highStr):
        log.error("Field for high price is not a valid number: {}".\
              format(highStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)
    if not isNumber(lowStr):
        log.error("Field for low price is not a valid number: {}".\
              format(lowStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)
    if not isNumber(closeStr):
        log.error("Field for close price is not a valid number: {}".\
              format(closeStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)
    if not isNumber(volumeStr):
        log.error("Field for volume price is not a valid number: {}".\
              format(volumeStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)
    if not isNumber(openIntStr):
        log.error("Field for open interest is not a valid number: {}".\
                  format(openIntStr) + \
                  "  Line for this entry is: {}".format(line))
        shutdown(1)

    dateStr = reformatQuandlDateField(dateStr)

    rv = "{},{},{},{},{},{},{}".\
         format(dateStr,
                openStr,
                highStr,
                lowStr,
                closeStr,
                volumeStr,
                openIntStr)

    log.debug(" Converted line from '{}' to '{}'".format(line, rv))
    
    return rv

    
def isNumber(numStr):
    """Returns True if the string is a number."""

    rv = True
    
    for letter in numStr:
        if not (letter.isdigit() or letter == "."):
            rv = False
            break

    return rv

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
                  help="Specify input CSV file.  This file should have daily EOD pricebars, in the format as obtained from the quandl.com website.",
                  metavar="<FILE>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file that will be reformatted to the CSV format compatible with PriceChartingTool.",
                  metavar="<FILE>")


# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)


if (options.inputFile == None):
    log.error("Please specify an input file to the " + \
              "--input-file option.")
    shutdown(1)
else:
    # Make sure the input file path is good.
    if not os.path.exists(options.inputFile):
        log.error("The input file provided does not exist: {}".\
                  format(options.inputFile))
        shutdown(1)
        
    # Save the value.
    inputFile = options.inputFile

if (options.outputFile == None):
    log.error("Please specify an output filename to the " + \
              "--output-file option.")
    shutdown(1)
else:
    outputFile = options.outputFile

        
##############################################################################

# Lines in the destination file.
convertedLines = []

# Read input file.
with open(inputFile) as f:
    i = 0
    
    for line in f:
        if i >= linesToSkip:
            convertedLine = reformatQuandlDataLine(line)
            convertedLines.append(convertedLine)

        i += 1

# Reverse the lines, since Quandl gives us the dates in reverse-cronological
# order.
convertedLines.reverse()

# Insert header line.
convertedLines.insert(0, headerLine)

# Write to file, truncating if it already exists.
with open(outputFile, "w", encoding="utf-8") as f:
    for line in convertedLines:
        f.write(line.rstrip() + newline)
        
log.info("Done.")
shutdown(0)

##############################################################################
