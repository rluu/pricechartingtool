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
#   from the files read earlier in the process take precedence over
#   the data read later.
#
#   This script assumes that the input CSV files have the following format:
#   "Date","Open","High","Low","Close","Volume","OpenInt"
#   and the timestamp is in the format "MM/DD/YYYY" or "MM/DD/YYYY HH:MM".
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
                       "in the CSV file is expected to be: \"MM/DD/YYYY\"" + \
                       "or \"MM/DD/YYYY HH:MM\".",
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
    using the timestamp value.  This function is used to do
    comparisons between lines, by timestamp.

    Arguments:
    line - str value holding a line of text of the CSV file.
           This value must have the timestamp as the first field
           in format "MM/DD/YYYY" or "MM/DD/YYYY HH:MM".

    Returns:
    int value that represents the timestamp in the form YYYYMMDD0000
    or YYYYMMDDHHMM.  This number can be used in date comparisons.
    """
    
    # str used in reporting errors.
    lineInfoStr = "  Line was: {}".format(line)
    
    # Check the number of fields.
    fields = line.split(",")

    numFieldsExpected = 7
    if len(fields) != numFieldsExpected:
        log.error("Line does not have {} data fields.".\
                  format(numFieldsExpected) + \
                  lineInfoStr)
        shutdown(1)

    timestampStr = fields[0] 
    openStr = fields[1]
    highStr = fields[2]
    lowStr = fields[3]
    closeStr = fields[4]
    volumeStr = fields[5]
    openIntStr = fields[6]

    dateStr = None
    timeStr = None
    
    if len(timestampStr) == 10:
        # Format of timestamp is 'MM/DD/YYYY'.
        dateStr = timestampStr
        timeStr = "00:00"
    elif len(timestampStr) == 16:
        # Format of timestamp is 'MM/DD/YYYY HH:MM'.
        timestampFields = timestampStr.split(" ")
        
        if len(timestampStrSplit) != 2:
            log.error("Format of the timestamp was not " + \
                      "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'." + \
                      lineInfoStr)
            shutdown(1)
            
        dateStr = timestampFields[0]
        timeStr = timestampFields[1]
    else:
        # Invalid number of characters for the timestamp.
        log.error("Invalid number of characters for the timestamp." + \
                  lineInfoStr)
        shutdown(1)
    
    dateFields = dateStr.split("/")
    if len(dateFields) != 3:
        log.error("Format of the timestamp was not " + \
                  "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'." + \
                  lineInfoStr)
        shutdown(1)

    monthStr = dateFields[0]
    dayStr = dateFields[1]
    yearStr = dateFields[2]

    if len(monthStr) != 2:
        log.error("Month in the date is not two characters long." + \
                  lineInfoStr)
        shutdown(1)
    if len(dayStr) != 2:
        log.error("Day in the date is not two characters long." + \
                  lineInfoStr)
        shutdown(1)
    if len(yearStr) != 4:
        log.error("Year in the date is not four characters long." + \
                  lineInfoStr)
        shutdown(1)

    try:
        monthInt = int(monthStr)
        if monthInt < 1 or monthInt > 12:
            log.error("Month in the date is not between 1 and 12." + \
                      lineInfoStr)
            shutdown(1)
    except ValueError as e:
        log.error("Month in the date is not a number." + \
                  lineInfoStr)
        shutdown(1)

    try:
        dayInt = int(dayStr)
        if dayInt < 1 or dayInt > 31:
            log.error("Day in the date is not between 1 and 31." + \
                      lineInfoStr)
            shutdown(1)
    except ValueError as e:
        log.error("Day in the date is not a number")
        shutdown(1)

    try:
        yearInt = int(yearStr)
    except ValueError as e:
        log.error("Year in the date is not a number")
        shutdown(1)



    timeFields = timeStr.split(":")
    if len(timeFields) != 2:
        log.error("Format of the time was not 'HH:MM'." + \
                  lineInfoStr)
        shutdown(1)

    hourStr = timeFields[0]
    minuteStr = timeFields[1]

    if len(hourStr) != 2:
        log.error("Hour in the timestamp is not two characters long." + \
                  lineInfoStr)
        shutdown(1)
    if len(minuteStr) != 2:
        log.error("Minute in the timestamp is not two characters long." + \
                  lineInfoStr)
        shutdown(1)
    
    try:
        hourInt = int(hourStr)
        if hourInt < 0 or hourInt > 23:
            log.error("Hour in the timestamp is not in range [00, 23]." + \
                      lineInfoStr)
            shutdown(1)
    except ValueError as e:
        log.error("Hour in the timestamp is not a number." + \
                  lineInfoStr)
        shutdown(1)

    try:
        minuteInt = int(minuteStr)
        if minuteInt < 0 or minuteInt > 59:
            log.error("Minute in the timestamp is not in range [00, 59]." + \
                      lineInfoStr)
            shutdown(1)
    except ValueError as e:
        log.error("Minute in the timestamp is not a number." + \
                  lineInfoStr)
        shutdown(1)


    numericalValue = int(yearStr + monthStr + dayStr + hourStr + minuteStr)

    log.debug("Convert line '{}' to numericalValue: '{}'".\
          format(line, numericalValue))
    
    return numericalValue

def compLines(line1, line2):
    """Comparison function for a line of text in the CSV files.
    This analyzes the timestamp date value, which is the first field
    on a line.

    Arguments:
    line1 - str value holding a line of text of the CSV file.
            This value must have the date as the first field
            in format "MM/DD/YYYY" or "MM/DD/YYYY HH:MM".
    line2 - str value holding a line of text of the CSV file.
            This value must have the date as the first field
            in format "MM/DD/YYYY" or "MM/DD/YYYY HH:MM".

    Returns:
    int value: -1, 0, or 1 if the first line's timestamp is
    earlier than, equal to, or later than the second line,
    respectively.
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
                    
                timestampStr = fields[0] 
                #openStr = fields[1]
                #highStr = fields[2]
                #lowStr = fields[3]
                #closeStr = fields[4]
                #volumeStr = fields[5]
                #openIntStr = fields[6]

                log.debug("timestampStr == {}".format(timestampStr))
                
                timestampExistsAlready = False
                for l in consolidatedDataLines:
                    if l.startswith(timestampStr):
                        log.debug("timestampStr '{}' is old.".\
                              format(timestampStr))
                        timestampExistsAlready = True
                        break
                if timestampExistsAlready == False:
                    log.debug("timestampStr '{}' is new.  Adding to list.".\
                          format(timestampStr))
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
