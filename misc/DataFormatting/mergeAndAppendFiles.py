#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script creates/writes a single CSV file of pricebar data,
#   from two or more input CSV data files.  The first file is used,
#   then when there is no more data, the new data from the second file
#   is used.  What is meant here by 'new data' is that the timestamp
#   for each pricebar of data is unique (timestamp hasn't been
#   utilized in all the previously read input files).  Hence, the data
#   from the files read earlier in the process have precedence over
#   the data read later.
#
#   This script assumes that the input CSV files have the following format:
#   "Date","Open","High","Low","Close","Volume","OpenInt"
#   and the date is in the format "MM/DD/YYYY".
# 
# Usage:
#
#   ./mergeAndAppendFiles.py --help
#   ./mergeAndAppendFiles.py --version
#
#   ./mergeAndAppendFiles.py --output-file="/tmp/SB_N_consolidated.txt" --input-file="/tmp/SB_N1.txt" --input-file="/tmp/SB_N2.txt"
#
#   ./mergeAndAppendFiles.py --output-file="/tmp/SB_N_consolidated.txt" --input-file="/tmp/SB_N1.txt" --input-file="/tmp/SB_N2.txt" --input-file="/tmp/SB_N3.txt"
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

# List of filenames of CSV data files, in priority usage order.
# This value is set via command-line parameters.
sourceDataFiles = []

# Destination output CSV text file.
# This value is set via command-line parameters.
destinationFilename = ""

# Number of lines of text to skip in the CSV data files.  This is
# usually a header line that just displays what the columns are.
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
    
parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file.",
                  metavar="<FILE>")

parser.add_option("--input-file",
                  action="append",
                  type="str",
                  dest="inputFile",
                  default=None,
                  help="Append an input CSV file to the list of " + \
                       "files to read.  Format of the date field " + \
                       "in the CSV file is expected to be: \"MM/DD/YYYY\".",
                  metavar="<FILE>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

if (options.outputFile == None):
    log.error("Please specify an output file to the " + \
          "--output-file option.")
    shutdown(1)
else:
    # Save the value.
    destinationFilename = options.outputFile

if (options.inputFile == None or len(options.inputFile) == 0):
    log.error("Please specify input file(s) to the " + \
          "--input-file option.")
    shutdown(1)
else:
    for f in options.inputFile:
        sourceDataFiles.append(f)
    
##############################################################################

def lineToComparableNumber(line):
    """Converts a line of text in the CSV file, to an int number by
    using the timestamp date value.  This function is used to do
    comparisons between lines, by timestamp.

    Arguments:
    line - str value holding a line of text of the CSV file.
           This value must have the date as the first field
           in format "MM/DD/YYYY".

    Returns:
    int value that represents the date.  This number can be used in
    date comparisons.
    """
    
    # Check the number of fields.
    fields = line.split(",")
    numFieldsExpected = 7
    if len(fields) != numFieldsExpected:
        return (False, "Line does not have {} data fields".\
                format(numFieldsExpected))

    dateStr = fields[0] 
    openStr = fields[1]
    highStr = fields[2]
    lowStr = fields[3]
    closeStr = fields[4]
    volumeStr = fields[5]
    openIntStr = fields[6]

    dateStrSplit = dateStr.split("/")
    if len(dateStrSplit) != 3:
        log.error("Format of the date was not 'MM/DD/YYYY'.  Line was: {}".\
              format(line))
        shutdown(1)

    monthStr = dateStrSplit[0]
    dayStr = dateStrSplit[1]
    yearStr = dateStrSplit[2]

    if len(monthStr) != 2:
        log.error("Month in the date is not two characters long")
        shutdown(1)
    if len(dayStr) != 2:
        log.error("Day in the date is not two characters long")
        shutdown(1)
    if len(yearStr) != 4:
        log.error("Year in the date is not four characters long")
        shutdown(1)

    try:
        monthInt = int(monthStr)
        if monthInt < 1 or monthInt > 12:
            log.error("Month in the date is not between 1 and 12")
            shutdown(1)
    except ValueError as e:
        log.error("Month in the date is not a number")
        shutdown(1)

    try:
        dayInt = int(dayStr)
        if dayInt < 1 or dayInt > 31:
            log.error("Day in the date is not between 1 and 31")
            shutdown(1)
    except ValueError as e:
        log.error("Day in the date is not a number")
        shutdown(1)

    try:
        yearInt = int(yearStr)
    except ValueError as e:
        log.error("Year in the date is not a number")
        shutdown(1)

    numericalValue = int(yearStr + monthStr + dayStr)

    log.debug("Convert line '{}' to numericalValue: '{}'".\
          format(line, numericalValue))
    
    return numericalValue

def compLines(line1, line2):
    """Comparison function for a line of text in the CSV files.
    This analyzes the timestamp date value, which is the first field
    on a line.
    """
    if lineToComparableNumber(line1) < lineToComparableNumber(line2):
        return -1
    elif lineToComparableNumber(line1) > lineToComparableNumber(line2):
        return 1
    else:
        return 0

def cmp_to_key(mycmp):
    """Converts a cmp= function into a key= function."""
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


##############################################################################
        
consolidatedDataLines = []

for filename in sourceDataFiles:
    # Make sure the source data path is good.
    if not os.path.exists(filename):
        log.error("Path does not exist: {}".format(filename))
        shutdown(1)
        
    log.info("Analyzing file '{}' ...".format(filename))
    with open(filename) as f:
        i = 0
        for line in f:
            if i < linesToSkip:
                log.debug("Skipping this line (i={}) ...".format(i))
                pass
            else:
                log.debug("Checking this line (i={}) ...".format(i))
                
                # Check the number of fields.
                fields = line.split(",")
                numFieldsExpected = 7
                if len(fields) != numFieldsExpected:
                    log.error("Line does not have {} data fields".\
                          format(numFieldsExpected))
                    shutdown(1)
                    
                dateStr = fields[0] 
                #openStr = fields[1]
                #highStr = fields[2]
                #lowStr = fields[3]
                #closeStr = fields[4]
                #volumeStr = fields[5]
                #openIntStr = fields[6]

                log.debug("dateStr == {}".format(dateStr))
                
                dateExistsAlready = False
                for l in consolidatedDataLines:
                    if l.startswith(dateStr):
                        log.debug("dateStr '{}' is old.".\
                              format(dateStr))
                        dateExistsAlready = True
                        break
                if dateExistsAlready == False:
                    log.debug("dateStr '{}' is new.  Adding to list.".\
                          format(dateStr))
                    consolidatedDataLines.append(line)
            i += 1

log.debug("Done reading all the files.")

# Sort the consolidatedDataLines by the timestamp field.
log.info("Sorting all lines by timestamp ...")
consolidatedDataLines.sort(key=cmp_to_key(compLines))

# Prepend header line.
consolidatedDataLines.insert(0, headerLine)

log.info("Writing to destination file '{}' ...".format(destinationFilename))

# Write to file, truncating if it already exists.
with open(destinationFilename, "w") as f:
    for line in consolidatedDataLines:
        f.write(line.rstrip() + newline)
        
log.info("Done.")
shutdown(0)
