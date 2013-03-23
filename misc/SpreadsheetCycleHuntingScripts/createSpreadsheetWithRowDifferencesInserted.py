#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This takes a CSV file as input, and inserts between each row,
#   another row containing the difference between the values in the
#   column of two consecutive rows.  The resulting CSV file is
#   outputted to a file.
#
# Algorithm used:
#
#   An attempt is made to convert the text in each column for each row
#   into a number.  If that is successful for two consecutive rows,
#   then the difference is calculated and a row inserted in between.
#   If the attempt to convert the text into a number fails, then no
#   difference calculation is made.  This would be the case if the
#   column contains zodiac coordinates using zodiac signs.
#   
# Usage:
#
#   ./createSpreadsheetWithRowDifferencesInserted.py --help
#   ./createSpreadsheetWithRowDifferencesInserted.py --version
#
#   ./createSpreadsheetWithRowDifferencesInserted.py \
#       --input-file=/tmp/TDW_cycle_hunting_turns.csv
#       --output-file=/tmp/TDW_cycle_hunting_turns_with_diffs.csv
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For parsing command-line options
from optparse import OptionParser  

# For dates.
#import datetime

# For logging.
import logging

# For math.floor()
#import math

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Input CSV file.
# The value for this field is obtained via command-line arguments.
inputFilename = ""

# Output CSV file.
# The value for this field is obtained via command-line arguments.
outputFilename = ""

# Lines to skip in the input file.
linesToSkip = 1

# For logging.
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
#log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    # Close the Ephemeris so it can do necessary cleanups.
    #Ephemeris.closeEphemeris()
    
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
                  dest="inputFilename",
                  default=None,
                  help="Specify input CSV file with the market turns only.",
                  metavar="<FILE>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFilename",
                  default=None,
                  help="Specify output CSV file.",
                  metavar="<FILE>")


# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)


if (options.inputFilename == None):
    log.error("Please specify an input CSV file to the " + \
              "--input-file option.")
    shutdown(1)
else:
    # Make sure the input file path is good.
    if not os.path.exists(options.inputFilename):
        log.error("The input file provided does not exist: {}".\
                  format(options.inputFilename))
        shutdown(1)
        
    # Save the value.
    inputFilename = options.inputFilename

    
if (options.outputFilename == None):
    log.error("Please specify an output filename to the " + \
              "--output-file option.")
    shutdown(1)
else:
    outputFilename = options.outputFilename

    
##############################################################################
    
# Holds the header line of the input file.  We will use this header
# line in the output file.
headerLine = ""

# List of lists.  Each item in this list is a list containing the
# fields of text of the input CSV file.
inputListOfDataValues = []

# List of lists.  Each item in this list is a list containing the
# fields of text to be placed in the output CSV file.
outputListOfDataValues = []

# Read in the input file:
log.info("Reading from input file: '{}' ...".format(inputFilename))
try:
    with open(inputFilename, "r") as f:
        i = 0
        for line in f:
            line = line.strip()
            if line == "":
                # Empty line, do nothing for thi sline.
                # Go to next line.
                i += 1
            elif i < linesToSkip:
                # Header line.
                headerLine = line
                i += 1
            else:
                # Normal data line.
                dataValues = line.split(",")
                inputListOfDataValues.append(dataValues)
                i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)


# Computer row differences.
log.info("Computing differences between each row's columns ...")

for i in range(len(inputListOfDataValues)):
    if i == 0:
        outputListOfDataValues.append(inputListOfDataValues[i])
        continue

    # Get the previous row and the current row so we can do diffs
    # between the values in each column.
    prevDataValuesRow = inputListOfDataValues[i-1]
    currDataValuesRow = inputListOfDataValues[i]

    # This is a list of lists.  Each item in this list is a row of
    # data which holds the differences.
    insertedDataValuesRow = []

    # Error checking, to make sure we have an equal number of columns
    # between the rows we are comparing.
    if len(prevDataValuesRow) != len(currDataValuesRow):
        log.error("Unequal number of columns between two rows " + \
                  "in the CSV file!  This is seen on line: (i={}).".format(i))
        shutdown(1)

    # Go through each column of the two rows and try to calculate the
    # difference between them.
    for j in range(len(prevDataValuesRow)):
        prevRowColumnStr = prevDataValuesRow[j]
        currRowColumnStr = currDataValuesRow[j]

        log.debug("prevRowColumnStr == {}".format(prevRowColumnStr))
        log.debug("currRowColumnStr == {}".format(currRowColumnStr))

        try:
            prevRowColumnValue = float(prevRowColumnStr)
            currRowColumnValue = float(currRowColumnStr)

            log.debug("prevRowColumnValue == {}".format(prevRowColumnValue))
            log.debug("currRowColumnValue == {}".format(currRowColumnValue))

            # If it got here, then the conversion worked successfully.
            diff = currRowColumnValue - prevRowColumnValue

            insertedDataValuesRow.append("{}".format(diff))
            
        except ValueError as e:
            # This isn't an error.  It just means we don't do an operation.
            #log.debug("Column {} does not have numerical text.".format(j))
            
            insertedDataValuesRow.append("")

    # Append the inserted row that has the differences and the current
    # row to the output list.
    outputListOfDataValues.append(insertedDataValuesRow)
    outputListOfDataValues.append(currDataValuesRow)
    
    

# Write to output file.
log.info("Writing to output file: '{}' ...".format(outputFilename))
try:
    with open(outputFilename, "w") as f:
        endl = "\r\n"
        f.write(headerLine + endl)
        
        for rowData in outputListOfDataValues:
            line = ""
            for i in range(len(rowData)):
                line += rowData[i] + ","

            # Remove trailing comma.
            line = line[:-1]

            f.write(line + endl)

except IOError as e:
    errStr = "I/O Error while trying to write file '" + \
             outputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)


log.info("Done.")
shutdown(0)

##############################################################################
