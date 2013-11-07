#!/usr/bin/env python3
##############################################################################
# Script to convert a directory of CSV files in the CSV format
# provided by TradingCharts.com to a directory of CSV files in the
# format that we use in PriceChartingTool.
#
#   ./reformatFuturesData_TradingCharts_Directory.py --help
#   ./reformatFuturesData_TradingCharts_Directory.py --version
#
#   ./reformatFuturesData_TradingCharts_Directory.py --input-dir="/home/rluu/download/trading/data/futuresData_TradingCharts/EODFutures/Wheat_Pit_CBOT" --output-dir="/home/rluu/download/trading/data/futuresData_TradingCharts/EODFutures/Wheat_Pit_CBOT_reformatted"
#
##############################################################################

import sys
import os
import copy
import errno

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# Input directory of CSV files obtained from TradingCharts.com.
# This value is obtained via command-line parameter.
inputDir = ""

# Output directory to place reformatted CSV text files.
# This value is obtained via command-line parameter.
outputDir = ""

# Number of lines of text to skip in the CSV data files.  This is
# usually a header line that just displays what the columns are.
# This value is obtained via command-line parameter.
linesToSkip = 1

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""

# Use Windows newlines.
newline = "\r\n"

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


def reformatTradingChartsDateField(dateStr):
    """Converts a date string in the format M/D/YYYY to MM/DD/YYYY.
    The converted string is returned.
    """
    
    dateFields = dateStr.split("/")
    if len(dateFields) != 3:
        log.error("Field for date is not in the expected format: {}".\
              format(dateStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)

    monthStr = dateFields[0]
    dayStr = dateFields[1]
    yearStr = dateFields[2]

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

def reformatTradingChartsDataLine(line):
    """Converts the CSV line format to our desired format.

    TradingCharts.com gives us lines in the format:
        "Symbol","Date","Open","High","Low","Close","Vol","OI"
        WN1970,7/23/1969,137,137,134.75,135,370,180

    We want it in format:
        "Date","Open","High","Low","Close","Volume","OpenInt"
        07/23/1969,137,137,134.75,135,370,180

    Returns: the converted string
    """

    fields = line.split(",")
    
    if len(fields) != 8:
        log.error("Input line from TradingCharts.com isn't in the " + \
                  "expected format.  Line given is: {}".format(line))
        shutdown(1)

    symbolStr = fields[0].strip()
    dateStr = fields[1].strip()
    openStr = fields[2].strip()
    highStr = fields[3].strip()
    lowStr  = fields[4].strip()
    closeStr = fields[5].strip()
    volumeStr = fields[6].strip()
    openIntStr = fields[7].strip()

        
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

    dateStr = reformatTradingChartsDateField(dateStr)

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
    
parser.add_option("--input-dir",
                  action="store",
                  type="str",
                  dest="inputDir",
                  default=None,
                  help="Specify input directory containing CSV files.  The files in this directory should be CSV files, in the format as obtained from the TradingCharts.com website.",
                  metavar="<DIRECTORY>")

parser.add_option("--output-dir",
                  action="store",
                  type="str",
                  dest="outputDir",
                  default=None,
                  help="Specify output directory where the reformatted CSV files will be placed.",
                  metavar="<DIRECTORY>")


# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)


if (options.inputDir == None):
    log.error("Please specify an input directory to the " + \
              "--input-dir option.")
    shutdown(1)
else:
    # Make sure the input directory path is good.
    if not os.path.isdir(options.inputDir):
        log.error("The input directory provided does not exist: {}".\
                  format(options.inputDir))
        shutdown(1)
        
    # Save the value.
    inputDir = options.inputDir

if (options.outputDir == None):
    log.error("Please specify an output directory to the " + \
              "--output-dir option.")
    shutdown(1)
else:
    outputDir = options.outputDir

        
##############################################################################


filesInDirectory = os.listdir(inputDir)



for inputFile in filesInDirectory:
    
    # Get the inputFile as an absolute path.
    inputFileAbsPath = os.path.join(inputDir, inputFile)
    
    # Lines in the destination file.
    convertedLines = []

    # Read input file.
    with open(inputFileAbsPath) as f:
        i = 0
    
        for line in f:
            if i >= linesToSkip:
                convertedLine = reformatTradingChartsDataLine(line)
                convertedLines.append(convertedLine)

            i += 1
    

    # Insert header line.
    convertedLines.insert(0, headerLine)


    # Try to make the output directory if it does not already exist.
    try:
        os.makedirs(outputDir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    if not os.path.isdir(options.outputDir):
        log.error("Please specify a valid output directory to the " + \
                  "--output-dir option.")
        shutdown(1)

    # Assemble what would be the output filename.
    outputFile = ""
    lastPeriodLocation = inputFile.rfind(".")
    if lastPeriodLocation == -1:
        outputFile = inputFile + ".txt"
    else:
        outputFile = inputFile[0:lastPeriodLocation] + ".txt"

    outputFileAbsPath = os.path.join(outputDir, outputFile)
    
    # Write to file, truncating if it already exists.
    with open(outputFileAbsPath, "w") as f:
        for line in convertedLines:
            f.write(line.rstrip() + newline)
        
log.info("Done.")
shutdown(0)

##############################################################################
