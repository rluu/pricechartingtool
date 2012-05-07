#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script creates a yearly CSV file of pricebar data,
#   from a monthly CSV file of pricebar data.
#
# Usage:
#
#   ./convertMonthlyToYearly.py --help
#   ./convertMonthlyToYearly.py --version
#
#   ./convertMonthlyToYearly.py --input-file="/tmp/soybeans_monthly.txt" --output-file="/tmp/soybeans_yearly.txt"
#   
##############################################################################

import sys
import os
import copy

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

import datetime


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
                  help="Specify input pricebar CSV data file.  This file should have daily pricebars, and it is assumed that the file has pricebars ordered from oldest to newest.",
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

currentWeekHasValues = False
currentWeekDateStr = ""
currentWeekOpen = -1
currentWeekHigh = -1
currentWeekLow = -1
currentWeekClose = -1
currentWeekVolume = -1
currentWeekOpenInt = -1

currentWeekIsoYearNumber = -1
currentWeekIsoWeekNumber = -1

# Read input file.
log.info("Analyzing file '{}' ...".format(inputFile))
with open(inputFile) as f:
    i = 0
    for line in f:
        if i >= linesToSkip and line.strip() != "":

            # Check the number of fields.
            fields = line.split(",")
            numFieldsExpected = 7
            if len(fields) != numFieldsExpected:
                log.error("Line does not have {} data fields".\
                          format(numFieldsExpected))
                shutdown(1)
            
            dateStr = fields[0].strip()
            openStr = fields[1].strip()
            highStr = fields[2].strip()
            lowStr = fields[3].strip()
            closeStr = fields[4].strip()
            volumeStr = fields[5].strip()
            openIntStr = fields[6].strip()
            
            # Make sure date is the right length.
            if len(dateStr) != 10:
                log.error("dateStr is not the expected number " +
                          "of characters: " + dateStr)
                shutdown(1)
                
            log.debug("dateStr == {}".format(dateStr))
            monthStr = dateStr[0:2]
            dayStr = dateStr[3:5]
            yearStr = dateStr[6:10]

            month = int(monthStr)
            day = int(dayStr)
            year = int(yearStr)

            d = datetime.date(year, month, day)

            isoWeekNumber = -1
            isoYearNumber = -1
            isoWeekdayNumber = -1
            (isoYearNumber, isoWeekNumber, isoWeekdayNumber) = d.isocalendar()
            isoYearNumber = year
            
            log.debug(\
                  "isoYearNumber={}, isoWeekNumber={}, isoWeekdayNumber={}".\
                  format(isoYearNumber, isoWeekNumber, isoWeekdayNumber))
            
            if currentWeekHasValues == False:
                log.debug("currentWeekHasValues == {}".\
                          format(currentWeekHasValues))
                
                currentWeekDateStr = dateStr
                currentWeekOpen = float(openStr)
                currentWeekHigh = float(highStr)
                currentWeekLow = float(lowStr)
                currentWeekClose = float(closeStr)
                currentWeekVolume = int(volumeStr)
                currentWeekOpenInt = int(openIntStr)

                #currentWeekIsoYearNumber = isoYearNumber
                currentWeekIsoYearNumber = year
                currentWeekIsoWeekNumber = isoWeekNumber
                currentWeekHasValues = True
                continue
            else:
                
                log.debug("isoYearNumber={}, currentWeekIsoYearNumber={}".\
                          format(isoYearNumber, currentWeekIsoYearNumber))
                log.debug("isoWeekNumber={}, currentWeekIsoWeekNumber={}".\
                          format(isoWeekNumber, currentWeekIsoWeekNumber))

                if isoYearNumber < currentWeekIsoYearNumber:
                    log.error("The input file is supposed to be " + \
                          "in chronological order!  Failed at line: {}".\
                          format(line))
                    shutdown(1)
                    
                elif isoYearNumber == currentWeekIsoYearNumber:
                    # Update the values as required.
                    log.debug("Date {} is within SAME week.".\
                          format(d.isoformat()))
                    
                    priceValues = []
                    priceValues.append(float(openStr))
                    priceValues.append(float(highStr))
                    priceValues.append(float(lowStr))
                    priceValues.append(float(closeStr))
                    priceValues.sort()

                    smallestValue = priceValues[0]
                    largestValue = priceValues[-1]

                    if smallestValue < currentWeekLow:
                        currentWeekLow = smallestValue
                    if largestValue > currentWeekHigh:
                        currentWeekHigh = largestValue
                    currentWeekClose = float(closeStr)
                    currentWeekVolume += int(volumeStr)
                    currentWeekOpenInt = int(openIntStr)
                    
                elif isoYearNumber > currentWeekIsoYearNumber:
                    
                    log.debug("Date {} is in a NEW week.".\
                          format(d.isoformat()))

                    # The new date is in a week that is later than the
                    # what the 'currentWeek' is.  This means the week
                    # has completed and we need to create and add a
                    # line of text for that week.
                    convertedLine = \
                        "{},{},{},{},{},{},{}".format(currentWeekDateStr,
                                                      currentWeekOpen,
                                                      currentWeekHigh,
                                                      currentWeekLow,
                                                      currentWeekClose,
                                                      currentWeekVolume,
                                                      currentWeekOpenInt)
                    convertedLines.append(convertedLine)
                    
                    # Set new values for the 'currentWeek'.
                    currentWeekDateStr = dateStr
                    currentWeekOpen = float(openStr)
                    currentWeekHigh = float(highStr)
                    currentWeekLow = float(lowStr)
                    currentWeekClose = float(closeStr)
                    currentWeekVolume = int(volumeStr)
                    currentWeekOpenInt = int(openIntStr)

                    currentWeekIsoYearNumber = isoYearNumber
                    currentWeekIsoWeekNumber = isoWeekNumber
                    currentWeekHasValues = True
                    
                else:
                    log.debug("Should never get here.")
                    
                    
        i += 1
        
    # Now done with going through all the lines.  Close out the last
    # week as a line.
    if currentWeekHasValues == True:
        convertedLine = \
            "{},{},{},{},{},{},{}".format(currentWeekDateStr,
                                          currentWeekOpen,
                                          currentWeekHigh,
                                          currentWeekLow,
                                          currentWeekClose,
                                          currentWeekVolume,
                                          currentWeekOpenInt)
        convertedLines.append(convertedLine)


log.debug("Total number of weeks in output file is: {}".\
      format(len(convertedLines)))

# Insert header line.
convertedLines.insert(0, headerLine)

# Write to file, truncating if it already exists.
log.info("Writing to destination file '{}' ...".format(outputFile))
with open(outputFile, "w") as f:
    for line in convertedLines:
        f.write(line + newline)

        
log.info("Done.")
shutdown(0)
