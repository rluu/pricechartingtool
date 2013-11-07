#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script creates a single gann-style CSV file of pricebar data,
#   from multiple CSV data files, for a single contract month.
#
# Usage:
#
#   ./createGannStyleCsvFile.py --help
#   ./createGannStyleCsvFile.py --version
#
#   ./createGannStyleCsvFile.py --input-dir="/home/rluu/download/trading/data/futuresData_TradingCharts/EODFutures/Wheat_Pit_CBOT_reformatted" --output-file="/home/rluu/download/trading/data/futuresData_TradingCharts/EODFutures/Wheat_Pit_CBOT_reformatted/W_N_GannStyle.txt" --contract-month=N
#
#   ./createGannStyleCsvFile.py --input-dir="/home/rluu/download/trading/data/futuresData_TradingCharts/EODFutures/Wheat_Pit_CBOT_reformatted" --output-file="/home/rluu/download/trading/data/futuresData_TradingCharts/EODFutures/Wheat_Pit_CBOT_reformatted/W_N_GannStyle.txt" --contract-month=N --wrap-at-prev-month
#
#   
##############################################################################

import sys
import os
import copy
import datetime

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# Full path to the directory containing the contract CSV data files.
# This value is obtained via command-line parameter.
inputDir = ""

# Contract month.  
# This value is obtained via command-line parameter.
contractMonthLetter = ""
contractMonthInt = None

# Destination output CSV text file.
# This value is obtained via command-line parameter.
outputFile = ""

# Flag that indicates we should jump to the next year's pricebar data,
# the month before the actual contract month.  Thus, if the contract
# is 'N' for July, then this flag would jump to the next year's data
# after the end of June.  If this flag is set to False or not used,
# then the default behavior is to include the data for the year's
# contract month until there is no more data, and resume on the next
# year beginning where the previous year's contract month ended.
# This value is obtained via command-line parameter.
wrapAtPrevMonthFlag = False

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

def lineToComparableNumber(line):
    """Converts a line of text in the CSV file, to an int number by
    using the timestamp date value.  This function is used to do
    comparisons between lines, by timestamp.

    Arguments:
    line - str value holding a line of text of the CSV file.
           This value must have the date as the first field
           in format "MM/DD/YYYY".

    Returns:
    int value that represents the date in the form YYYYMMDD.
    This number can be used in date comparisons.
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

    Arguments:
    line1 - str value holding a line of text of the CSV file.
            This value must have the date as the first field
            in format "MM/DD/YYYY".
    line2 - str value holding a line of text of the CSV file.
            This value must have the date as the first field
            in format "MM/DD/YYYY".

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
                  help="Specify source CSV data directory.  This directory should have only all the CSV files for the given trading entity within it, and only containing for the desired contract month.  CSV files for other contract months should not be in this directory.  This value should not have a trailing slash.",
                  metavar="<DIR>")

parser.add_option("--contract-month",
                  action="store",
                  type="str",
                  dest="contractMonth",
                  default=None,
                  help="Specify contract month letter or 1-based number.",
                  metavar="<LETTER or NUMBER [1,12]>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file.",
                  metavar="<FILE>")

parser.add_option("--wrap-at-prev-month",
                  action="store_true",
                  dest="wrapAtPrevMonthFlag",
                  default=False,
                  help="Flag that indicates we should jump to the next year's pricebar data, the month before the actual contract month.  Thus, if the contract is 'N' for July, then this flag would jump to the next year's data after the end of June.  If this flag is set to False or not used, then the default behavior is to include the data for the year's contract month until there is no more data, and resume on the next year beginning where the previous year's contract month ended.  This flag is optional.  Default value: False (not set).",
                  metavar="<BOOL>")



# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)


if (options.inputDir == None):
    log.error("Please specify a directory path to the " + \
          "--input-dir option.")
    shutdown(1)
else:
    # Make sure the source data path is good.
    if not os.path.exists(options.inputDir):
        log.error("Input data directory provided does not exist: {}".\
              format(options.sourceDataDir))
        shutdown(1)
    if not os.path.isdir(options.inputDir):
        log.error("Input data directory is not a directory: {}".\
              format(options.inputDir))
        shutdown(1)

    # Save the value.
    inputDir = options.inputDir

    
if (options.contractMonth == None):
    log.error("Please specify a contract month to the " + \
              "--contract-month option.")
    shutdown(1)
else:
    options.contractMonth = options.contractMonth.strip()
    
    if not options.contractMonth.isalpha():
        # Number was given.
        contractMonthInt = int(options.contractMonth)
        
        # Set the contractMonthLetter.
        if contractMonthInt == 1:
            contractMonthLetter = "F"
        elif contractMonthInt == 2:
            contractMonthLetter = "G"
        elif contractMonthInt == 3:
            contractMonthLetter = "H"
        elif contractMonthInt == 4:
            contractMonthLetter = "J"
        elif contractMonthInt == 5:
            contractMonthLetter = "K"
        elif contractMonthInt == 6:
            contractMonthLetter = "M"
        elif contractMonthInt == 7:
            contractMonthLetter = "N"
        elif contractMonthInt == 8:
            contractMonthLetter = "Q"
        elif contractMonthInt == 9:
            contractMonthLetter = "U"
        elif contractMonthInt == 10:
            contractMonthLetter = "V"
        elif contractMonthInt == 11:
            contractMonthLetter = "X"
        elif contractMonthInt == 12:
            contractMonthLetter = "Z"
        else:
            log.error("Contract month number given must be in " + \
                      "range [1, 12].  " + \
                      "The contract month specified was: {}".\
                      format(options.contractMonth))
            shutdown(1)
        
    else:
        # Letter(s) were given.

        if len(options.contractMonth) != 1:
            log.error("Contract month letter is too many characters.  " + \
                      "The contract month specified was: {}".\
                      format(options.contractMonth))
            shutdown(1)
            
        # Set it to upper-case value.
        contractMonthLetter = options.contractMonth.upper()

        # Set all the contractMonthInt.
        if contractMonthLetter == "F":
            contractMonthInt = 1
        elif contractMonthLetter == "G":
            contractMonthInt = 2
        elif contractMonthLetter == "H":
            contractMonthInt = 3
        elif contractMonthLetter == "J":
            contractMonthInt = 4
        elif contractMonthLetter == "K":
            contractMonthInt = 5
        elif contractMonthLetter == "M":
            contractMonthInt = 6
        elif contractMonthLetter == "N":
            contractMonthInt = 7
        elif contractMonthLetter == "Q":
            contractMonthInt = 8
        elif contractMonthLetter == "U":
            contractMonthInt = 9
        elif contractMonthLetter == "V":
            contractMonthInt = 10
        elif contractMonthLetter == "X":
            contractMonthInt = 11
        elif contractMonthLetter == "Z":
            contractMonthInt = 12
        else:
            log.error("Contract month letter given does not map to a month." + \
                      "  Contract month letter specified was: {}".\
                      format(contractMonthLetter))
            shutdown(1)
            
    
if (options.outputFile == None):
    log.error("Please specify an output filename to the " + \
              "--output-file option.")
    shutdown(1)
else:
    outputFile = options.outputFile

if options.wrapAtPrevMonthFlag != None and options.wrapAtPrevMonthFlag == True:
    wrapAtPrevMonthFlag = True
else:
    wrapAtPrevMonthFlag = False
    
        
##############################################################################


# Sorted list of files in the directory from oldest to newest contract.
sortedListOfFiles = []

for inputFile in os.listdir(inputDir):
    # Get the filename as an absolute path.
    inputFileAbsPath = os.path.join(inputDir, inputFile)

    # If the file is a sub-directory, then skip over it.
    # We want to only look at regular files.
    if os.path.isdir(inputFile):
        continue

    log.debug("Looking at file: {}".format(inputFileAbsPath))
    log.debug("Basename of file is: {}".format(inputFile))
    sortedListOfFiles.append(inputFileAbsPath)

log.debug("sorting list ...")
sortedListOfFiles.sort()

log.debug("sorted list is: ")
for f in sortedListOfFiles:
    log.debug("f is: {}".format(f))


# List 'sortedListOfFiles' now has all the filenames of the source CSV
# data files, in the order we should extract dates and price data.


log.debug("Using the following files in the following order: ")
for f in sortedListOfFiles:
    log.debug("f: {}".format(f))

# List of all the lines that will go into the destination file.
consolidatedDataLines = []

for filename in sortedListOfFiles:
    log.info("Analyzing file '{}' ...".format(filename))

    # Lines in the file total.  We need this as a hack to
    # determine if there is another year of data in the file from
    # where we currently are in the iteration of working through
    # it's lines.
    numLines = 0
    with open(filename) as f:
        for line in f:
            numLines += 1
    log.debug("Number of lines is: {}".format(numLines))

    # Now actually go through and process the lines.
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
                    log.error("Line {} does not have {} data fields.".\
                          format(i + 1, numFieldsExpected))
                    shutdown(1)
                    
                dateStr = fields[0] 
                #openStr = fields[1]
                #highStr = fields[2]
                #lowStr = fields[3]
                #closeStr = fields[4]
                #volumeStr = fields[5]
                #openIntStr = fields[6]

                log.debug("dateStr == {}".format(dateStr))

                # Get the other str components of the dateStr.
                dateStrSplit = dateStr.split("/")
                if len(dateStrSplit) != 3:
                    log.error("Format of the date was not 'MM/DD/YYYY'.  " + \
                              "Line was: {}".format(line))
                    shutdown(1)

                monthStr = dateStrSplit[0]
                dayStr = dateStrSplit[1]
                yearStr = dateStrSplit[2]

                month = int(monthStr)
                day = int(dayStr)
                year = int(yearStr)
                
                currDate = datetime.date(year, month, day)
                
                # Here we go through and see if the date already
                # exists in our list of 'consolidatedDataLines'.  We
                # don't add the line if we have pricebars for this
                # date already.
                dateExistsAlready = False
                for l in consolidatedDataLines:
                    if l.startswith(dateStr):
                        log.debug("dateStr '{}' is old.".\
                                  format(dateStr))
                        dateExistsAlready = True
                        break
                if dateExistsAlready == False:
                    log.debug("dateStr '{}' is new.".format(dateStr))

                    # Before adding it to the list, check to see if
                    # the wrapAtPrevMonthFlag is true, and if we need
                    # to do anything special if that flag is true.
                    if wrapAtPrevMonthFlag == True:
                        # Flag is true.

                        if currDate.month == contractMonthInt:
                            # The months match the contract month.
                            # Normally, this would be grounds to no
                            # longer append, and break out of working
                            # through this file, but we need to see if
                            # there is another year of data to work
                            # through before doing that.  This needs
                            # to be done because for a file of
                            # pricebars for a certain contract, there
                            # may be multiple years of data within
                            # that one file.  For example, for the
                            # contract, July, 2006, the data could
                            # start in 2004, and we need to account
                            # for when we reach the beginning of July
                            # 2005, to ensure that we don't stop
                            # there, but continue.
                            #
                            # Here we will do a hackish thing.  
                            # There are approximately 260 weekdays in a
                            # year.  First check to see if there is still
                            # more than 30 pricebars left to go in this
                            # file.
                            numLinesLeft = numLines - i
                            if numLinesLeft > 30:
                                # There is probably about another year
                                # worth of data to go through.
                                # No need to worry about wrapping yet.
                                consolidatedDataLines.append(line)

                                log.debug("Num lines left is: {}".\
                                          format(numLinesLeft))
                            else:
                                # We reached the data lines near the
                                # end of the file which match the
                                # contract expiration month.  Because
                                # the flag is set, we should break out
                                # of the loop working on this file.
                                log.debug("Reached date {} which is in the contract month {}.  We will not appending this line, but will move onto the next file.".format(currDate, contractMonthInt))
                                break
                    else:
                        # The wrapAtPrevMonthFlag is false, so always
                        # append since the date is new.
                        consolidatedDataLines.append(line)
                    
            i += 1

log.info("Done reading all the files for contract month {}.".\
         format(contractMonthLetter))

# Make sure all lines in consolidatedDataLines are sorted by timestamp.
log.info("Sorting all lines by timestamp ...")
consolidatedDataLines.sort(key=cmp_to_key(compLines))

# Write to file, truncating if it already exists.
log.info("Writing to output file '{}' ...".format(outputFile))
with open(outputFile, "w") as f:
    f.write(headerLine + newline)

    for line in consolidatedDataLines:
        f.write(line.rstrip() + newline)
        
log.info("Done.")
shutdown(0)
