#!/usr/bin/env python3
##############################################################################
# Description:
#   Obtains stock pricebar data from Google Finance.
#
# Usage:
#
#     ./getStockDataFromGoogle.py --help
#     ./getStockDataFromGoogle.py --version
#
#     ./getStockDataFromGoogle.py --stock-symbol=FSLR --start-timestamp=20091001 --end-timestamp=20111014 --output-file=/tmp/testing.txt
#
#    ./getStockDataFromGoogle.py --stock-symbol=NASDAQ:FSLR --start-timestamp=20091001 --end-timestamp=20111014 --output-file=/tmp/testing.txt
#
#
# Note:
# 
#    If possible, prefer to use the Yahoo equivalent of this script
#    (getStockDataFromGoogle.py).  This is because there are some
#    caveats the user should be aware of while using this script,
#    whereas the Yahoo version of this script works without problems.
#
#    The Google servers only return a maximum of 4000 price bars at a
#    time.  This works out to about 15.3 years.  That means if you
#    want to gather data for a stock with a long history, you need to
#    run this script several times and then combine the data.
#
#    Also, getting the stock indexes from Google doesn't appear to be
#    working.  Is there a way to do this, or is their service broken
#    for stock indexes?  If we go to:
#    http://www.google.com/finance/historical?q=INDEXNASDAQ:.IXIC
#    It works and it shows the data in a table, but there is no link to
#    "Download to spreadsheet" like when we access charts.
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

# For connecting to the server via HTTP
import http.cookiejar
import urllib
from urllib import *

##############################################################################

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Stock symbol to obtain data for.
# This value is obtained via command-line parameter.
stockSymbol = ""

# Starting timestamp.
# Format is "YYYYMMDD".
# This value is obtained via command-line parameter.
startTimestampStr = ""

# Ending timestamp.
# Format is "YYYYMMDD".
# This value is obtained via command-line parameter.
endTimestampStr = ""

# Destination output CSV text file.
# This value is obtained via command-line parameter.
outputFile = ""

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""

# Use Windows newlines in the output file.
newline = "\r\n"

# Cookie preferences are required for the pricebar data to be returned.
defaultHttpHeaders = \
        [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10'),
         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
         ('Accept-Language', 'en-us,en;q=0.5'),
         ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')]

# 2-digit year number of which starts the beggining of time.  This is
# because Google gives us data in which the year 2000 is represented
# by 00.
# This value is obtained via command-line parameter.
defaultEarliestTwoDigitYear = 28
earliestTwoDigitYear = defaultEarliestTwoDigitYear

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

def convertStringToFormattedDate(timestampStr):
    """Converts input str of a date timestamp from format YYYYMMDD to
    the format required in the URL for a HTTP GET to Google Finance.
    The resulting equivalent string is returned.
    """

    # Check input.
    if len(timestampStr) != 8 or timestampStr.isnumeric() == False:
        log.error("Timestamp string must be in the format 'YYYYYMMDD'.  " + \
              "Timestamp string given was: {}".format(timestampStr))
        shutdown(1)

    yearStr = timestampStr[0:4]
    monthStr = timestampStr[4:6]
    dayStr = timestampStr[6:8]

    month = int(monthStr)
    if month == 1:
        monthStr = "Jan"
    elif month == 2:
        monthStr = "Feb"
    elif month == 3:
        monthStr = "Mar"
    elif month == 4:
        monthStr = "Apr"
    elif month == 5:
        monthStr = "May"
    elif month == 6:
        monthStr = "Jun"
    elif month == 7:
        monthStr = "Jul"
    elif month == 8:
        monthStr = "Aug"
    elif month == 9:
        monthStr = "Sep"
    elif month == 10:
        monthStr = "Oct"
    elif month == 11:
        monthStr = "Nov"
    elif month == 12:
        monthStr = "Dec"

    day = int(dayStr)
    dayStr = "{}".format(day)
    
    log.debug("yearStr={}, monthStr={}, dayStr={}".\
              format(yearStr, monthStr, dayStr))

    rv = "{}+{}%2C+{}".format(monthStr, dayStr, yearStr)

    log.debug(" returning: {}".format(rv))
    
    return rv

def reformatGoogleDateField(dateStr):
    """Converts a date string in the format 30-Sep-11 or 3-Sep-11 to
    09/30/2011 or 09/03/2011, respectively.  The converted string is
    returned.
    """
    
    dateFields = dateStr.split("-")
    if len(dateFields) != 3:
        log.error("Field for date is not in the expected format: {}".\
              format(dateStr) + "  Line for this entry is: {}".format(line))
        shutdown(1)

    dayStr = dateFields[0]
    monthStr = dateFields[1]
    yearStr = dateFields[2]

    # Check inputs.
    if (len(dayStr) != 1 and len(dayStr) != 2) or (not dayStr.isnumeric()):
        log.error("day in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)
    if len(monthStr) != 3:
        log.error("month in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)
    if len(yearStr) != 2 or (not yearStr.isnumeric()):
        log.error("year in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)

    # Make sure dayStr is two characters when we're done looking at it.
    if len(dayStr) == 1:
        dayStr = "0" + dayStr
    
    # Convert month string to a 2-digit string.
    monthStr = monthStr.lower()
    if monthStr == "jan":
        monthStr = "01"
    elif monthStr == "feb":
        monthStr = "02"
    elif monthStr == "mar":
        monthStr = "03"
    elif monthStr == "apr":
        monthStr = "04"
    elif monthStr == "may":
        monthStr = "05"
    elif monthStr == "jun":
        monthStr = "06"
    elif monthStr == "jul":
        monthStr = "07"
    elif monthStr == "aug":
        monthStr = "08"
    elif monthStr == "sep":
        monthStr = "09"
    elif monthStr == "oct":
        monthStr = "10"
    elif monthStr == "nov":
        monthStr = "11"
    elif monthStr == "dec":
        monthStr = "12"
    else:
        log.error("month in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)

    # Convert the two-digit year to a 4-digit one.
    twoDigitYearInt = int(yearStr)

    fourDigitYearStr = ""
    if twoDigitYearInt < earliestTwoDigitYear:
        # Year that is in the 2000s.
        fourDigitYearStr = "20" + yearStr
    else:
        # Year that is in the 1900s.
        fourDigitYearStr = "19" + yearStr
    yearStr = fourDigitYearStr

    
    rv = "{}/{}/{}".format(monthStr, dayStr, yearStr)

    return rv

def reformatGoogleFinanceDataLine(line):
    """Converts the Google Finance CSV line format to our desired format.

    Google gives us lines in the format:
        Date,Open,High,Low,Close,Volume
        30-Sep-11,63.57,66.64,62.08,63.21,4245863

    We want it in format:
        "Date","Open","High","Low","Close","Volume","OpenInt"
        09/30/2011,63.57,66.64,62.08,63.21,4245863,0

    Returns: the converted string
    """

    fields = line.split(",")
    
    if len(fields) != 6:
        log.error("Input line from Google isn't in the expected format.  " +\
              "Line given is: {}".format(line))
        shutdown(1)

    dateStr = fields[0]
    openStr = fields[1]
    highStr = fields[2]
    lowStr  = fields[3]
    closeStr = fields[4]
    volumeStr = fields[5]

        
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

    dateStr = reformatGoogleDateField(dateStr)
    openIntStr = "0"

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
    
parser.add_option("--stock-symbol",
                  action="store",
                  type="str",
                  dest="stockSymbol",
                  default=None,
                  help="Specify stock symbol to obtain data for.  " + \
                       "This is a required field.",
                  metavar="<SYMBOL>")

parser.add_option("--start-timestamp",
                  action="store",
                  type="str",
                  dest="startTimestamp",
                  default=None,
                  help="Specify starting date of the data.  " + \
                       "This is a required field.  " + \
                       "Format of this string is 'YYYYMMDD'.",
                  metavar="<TIMESTAMP>")

parser.add_option("--end-timestamp",
                  action="store",
                  type="str",
                  dest="endTimestamp",
                  default=None,
                  help="Specify ending date of the data.  " + \
                       "This is a required field.  " + \
                       "Format of this string is 'YYYYMMDD'.",
                  metavar="<TIMESTAMP>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file.  This is a required field.",
                  metavar="<FILE>")

parser.add_option("--earliest-two-digit-year",
                  action="store",
                  type="int",
                  dest="earliestTwoDigitYear",
                  default=defaultEarliestTwoDigitYear,
                  help="Specify the earliest 2-digit year of which starts the beginning of time.  This is needed because in the data given to us by Google, the year 2000 is represented by 00.  Default value: {}".format(defaultEarliestTwoDigitYear),
                  metavar="<VALUE>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if options.version == True:
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)


if options.stockSymbol == None:
    log.error("Please specify a stock symbol to the " + \
          "--stock-symbol option.")
    shutdown(1)
else:
    # Set it to upper-case value.
    stockSymbol = options.stockSymbol.strip().upper()

if options.startTimestamp == None:
    log.error("Please specify a starting timestamp to the " + \
          "--start-timestamp option.")
    shutdown(1)
else:
    startTimestamp = options.startTimestamp
          
if options.endTimestamp == None:
    log.error("Please specify a ending timestamp to the " + \
          "--end-timestamp option.")
    shutdown(1)
else:
    endTimestamp = options.endTimestamp
          
if options.outputFile == None:
    log.error("Please specify an output filename to the " + \
          "--output-file option.")
    shutdown(1)
else:
    outputFile = os.path.abspath(options.outputFile)

if options.earliestTwoDigitYear != None:
    if not (0 <= options.earliestTwoDigitYear < 100):
        log.error("Please specify a non-negative number " + \
              "less than 100 to the " + \
              "--earliest-two-digit-year option.")
        shutdown(1)
    else:
        earliestTwoDigitYear = options.earliestTwoDigitYear
        
##############################################################################

formattedStartTimestamp = convertStringToFormattedDate(startTimestamp)
formattedEndTimestamp = convertStringToFormattedDate(endTimestamp)

url = "http://www.google.com/finance/historical?q=" + stockSymbol + \
      "&startdate={}".format(formattedStartTimestamp) + \
      "&enddate={}".format(formattedEndTimestamp) + \
      "&output=csv"

log.info("Obtaining stock price data by accessing URL: {}".format(url))

opener = urllib.request.build_opener()
request = urllib.request.Request(url)
opener.addheaders = defaultHttpHeaders

log.info("Opening HTTP request.")
response = opener.open(request)

log.info("Reading HTTP response.")
data = response.read().decode()

log.info("Processing and reformatting the data ...")

log.debug(" Data read from {} is: ***{}***".format(url, data))
outputLines = data.split("\n")

# Get rid of header lines in the Google data file.
if len(outputLines) > 0:
    index = 0
    googleHeaderLine = "Date,Open,High,Low,Close,Volume"
    if outputLines[index].find(googleHeaderLine) != -1:
        log.debug("Found header line.")
        outputLines.pop(index)

# Reverse the order of the bars, since we want the lines in our file
# to be from oldest to newest.
outputLines.reverse()

reformattedLines = []
for line in outputLines:
    if line.strip() != "":
        reformattedLine = reformatGoogleFinanceDataLine(line.strip())
        reformattedLines.append(reformattedLine)

log.info("Obtained a total of {} price bars.".format(len(reformattedLines)))

if len(reformattedLines) > 0:
    log.info("Earliest PriceBar is: {}".format(reformattedLines[0]))
    log.info("Latest   PriceBar is: {}".format(reformattedLines[-1]))
      
# Write to file, truncating if it already exists.
log.info("Writing to output file '{}' ...".format(outputFile))

with open(outputFile, "w") as f:
    f.write(headerLine + newline)
    for line in reformattedLines:
        f.write(line + newline)
        
log.info("Done.")
shutdown(0)


