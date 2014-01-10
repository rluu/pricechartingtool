#!/usr/bin/env python3
##############################################################################
# Description:
#   Obtains stock pricebar data from Yahoo Finance.
#
# Note:
#   From reading through the Yahoo Finance page HTML code,
#   it appears that Yahoo gets its data from
#   Commodity Systems, Inc. (CSI) http://www.csidata.com/
#
# Note:
#   As of 20130423, it appears that gathering the pricebars for the
#   indexes doesn't work anymore through this script.  Yahoo appears
#   to have disabled getting CSV data for the indexes, but obtaining
#   CSV data for regular individual stocks still works.  To get data
#   for the indexes, use script "getStockDataFromBarChart.py", which
#   works for obtaining the pricebar data for the past year.
# 
# Usage:
#
#     ./getStockDataFromYahoo.py --help
#     ./getStockDataFromYahoo.py --version
#
#     ./getStockDataFromYahoo.py --update --stock-symbol=FSLR --output-file=/tmp/testing.txt
#
#     ./getStockDataFromYahoo.py --stock-symbol=FSLR --start-timestamp=20091001 --end-timestamp=20111014 --output-file=/tmp/testing.txt
#
#     ./getStockDataFromYahoo.py --stock-symbol=FSLR --output-file=/tmp/testing.txt
#
#     ./getStockDataFromYahoo.py --stock-symbol=^DJI --start-timestamp=20091001 --end-timestamp=20111014 --output-file=/tmp/testing.txt
#
#     ./getStockDataFromYahoo.py --stock-symbol=^IXIC --start-timestamp=20091001 --end-timestamp=20111014 --output-file=/tmp/testing.txt
#
#     ./getStockDataFromYahoo.py --stock-symbol=^NDX --start-timestamp=20091001 --end-timestamp=20111014 --output-file=/tmp/testing.txt
#
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For dates.
import datetime

# For regular expressions.
import re

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

# Flag that says we should do an update of the output file.
updateFlag = False

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

# Url argument string.
#   Daily:   g=d
#   Weekly:  g=w
#   Monthly: g=m
formattedTimeUnit = "g=d"

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""

# Number of lines to skip in the file being read.
numLinesToSkip = 1

# Use these types newlines in the output file.
newline = "\n"

# Cookie preferences are required for the pricebar data to be returned.
defaultHttpHeaders = \
        [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10'),
         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
         ('Accept-Language', 'en-us,en;q=0.5'),
         ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')]

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

def getTimestampStrForEarliestData(stockSymbol):
    """Obtains the date of the earliest data we can obtain for the
    given stock symbol.

    Arguments:
    stockSymbol - str value holding the stock symbol we want to get
                  the earliest timestamp of data for.
    
    Returns:
    str holding the date in the format "YYYYMMDD".
    """

    # Here what we are doing is loading the webpage for historical
    # prices of the stock symbol.  By default, this page loads with
    # the earliest available data date, as well as the latest
    # available data date.  We extract the info from the HTML of this
    # page.


    url = "http://finance.yahoo.com/q/hp?" + \
          "s={}".format(stockSymbol)
    
    log.debug("Obtaining earliest data timestamp by accessing URL: {}".\
              format(url))

    opener = urllib.request.build_opener()
    request = urllib.request.Request(url)
    opener.addheaders = defaultHttpHeaders

    log.debug("Opening HTTP request.")
    response = opener.open(request)

    log.debug("Reading HTTP response.")
    data = response.read().decode()

    log.debug("Processing HTML page ...")

    log.debug(" Data length is: {}".format(len(data)))
    log.debug(" Data read from {} is: ***{}***".format(url, data))

    # Get the location where the label 'Start Date:' is shown.
    startDateLabelLoc = data.find("Start Date:")
    log.debug("startDateLabelLoc == {}".format(startDateLabelLoc))
    log.debug("type(startDateLabelLoc) == {}".format(type(startDateLabelLoc)))
    if startDateLabelLoc == -1:
        log.error("Could not find earliest data timestamp because " + \
                  "'Start Date:' could not be found in the HTML.")
        shutdown(1)

    # Get the location where the label 'End Date:' is shown.
    endDateLabelLoc = data.find("End Date:")
    log.debug("endDateLabelLoc == {}".format(endDateLabelLoc))
    log.debug("type(endDateLabelLoc) == {}".format(type(endDateLabelLoc)))
    if endDateLabelLoc == -1:
        log.error("Could not find earliest data timestamp because " + \
                  "'End Date:' could not be found in the HTML.")
        shutdown(1)

    # Get the HTML between these two label locations.
    htmlStr = data[startDateLabelLoc:endDateLabelLoc]
    log.debug("htmlStr is: ***{}***".format(htmlStr))

    # Strings that hold the data obtained from the Yahoo HTML page.
    # Here the month is 0-based, (e.g. January is "00").
    yahooMonthStr = ""
    yahooDayStr = ""
    yahooYearStr = ""
    
    # Search through the HTML for the month.
    log.debug("Searching for the month ...")
    match = re.search(r"""<option selected value="(.*?)">""", htmlStr)
    if match:
        cellText = match.groups()[0]

        log.debug("Cell text is: " + cellText)

        if len(cellText) == 2:
            yahooMonthStr = cellText
        else:
            log.error("Cell text for the month number is not of length 2.")
            shutdown(1)
    else:
        log.error("Could not find earliest data timestamp because " + \
                  "the month value could not be found in the HTML.")
        shutdown(1)
    
    # Search through the HTML for the day.
    log.debug("Searching for the day ...")
    match = re.search(r"""id="startday".*?value="(.*?)".*?>""", htmlStr)
    if match:
        cellText = match.groups()[0]
        log.debug("Cell text is: " + cellText)

        if len(cellText) == 1 or len(cellText) == 2:
            yahooDayStr = cellText
        else:
            log.error("Cell text for the day number is not of length 1 or 2.")
            shutdown(1)
    else:
        log.error("Could not find earliest data timestamp because " + \
                  "the day value could not be found in the HTML.")
        shutdown(1)
    
    # Search through the HTML for the year.
    log.debug("Searching for the year ...")
    match = re.search(r"""id="startyear".*?value="(.*?)".*?>""", htmlStr)
    if match:
        cellText = match.groups()[0]
        log.debug("Cell text is: " + cellText)

        if len(cellText) == 4:
            yahooYearStr = cellText
        else:
            log.error("Cell text for the year number is not of length 4.")
            shutdown(1)
    else:
        log.error("Could not find earliest data timestamp because " + \
                  "the year value could not be found in the HTML.")
        shutdown(1)

    log.debug("yahooMonthStr == {}".format(yahooMonthStr))
    log.debug("yahooDayStr   == {}".format(yahooDayStr))
    log.debug("yahooYearStr  == {}".format(yahooYearStr))
    
    # Convert the obtained values to integers.
    monthInt = int(yahooMonthStr) + 1
    dayInt = int(yahooDayStr)
    yearInt = int(yahooYearStr)

    # Convert the int values to the desired str values.
    monthStr = "{:02}".format(monthInt)
    dayStr = "{:02}".format(dayInt)
    yearStr = "{:04}".format(yearInt)

    rv = "{}{}{}".format(yearStr, monthStr, dayStr)

    log.debug("Returning rv == {}".format(rv))
    
    return rv

def getTimestampStrForLatestData(stockSymbol):
    """Obtains the date of the latest data we can obtain for the given
    stock symbol.  This implementation always returns the current date.

    Returns:
    str holding the date in the format "YYYYMMDD".
    """
    
    # Here what we are doing is loading the webpage for historical
    # prices of the stock symbol.  By default, this page loads with
    # the earliest available data date, as well as the latest
    # available data date.  We extract the info from the HTML of this
    # page.


    url = "http://finance.yahoo.com/q/hp?" + \
          "s={}".format(stockSymbol)
    
    log.debug("Obtaining latest data timestamp by accessing URL: {}".\
              format(url))

    opener = urllib.request.build_opener()
    request = urllib.request.Request(url)
    opener.addheaders = defaultHttpHeaders

    log.debug("Opening HTTP request.")
    response = opener.open(request)

    log.debug("Reading HTTP response.")
    data = response.read().decode()

    log.debug("Processing HTML page ...")
    log.debug(" Data length is: {}".format(len(data)))
    log.debug(" Data read from {} is: ***{}***".format(url, data))

    # Get the location where the label 'End Date:' is shown.
    endDateLabelLoc = data.find("End Date:")
    if endDateLabelLoc == -1:
        log.error("Could not find latest data timestamp because " + \
                  "'End Date:' could not be found in the HTML.")
        shutdown(1)

    # Get the HTML between the label location and the end of the HTML.
    htmlStr = data[endDateLabelLoc:]
    log.debug("htmlStr is: ***{}***".format(htmlStr))

    # Strings that hold the data obtained from the Yahoo HTML page.
    # Here the month is 0-based, (e.g. January is "00").
    yahooMonthStr = ""
    yahooDayStr = ""
    yahooYearStr = ""
    
    # Search through the HTML for the month.
    log.debug("Searching for the month ...")
    match = re.search(r"""<option selected value="(.*?)">""", htmlStr)
    if match:
        cellText = match.groups()[0]

        log.debug("Cell text is: " + cellText)

        if len(cellText) == 2:
            yahooMonthStr = cellText
        else:
            log.error("Cell text for the month number is not of length 2.")
            shutdown(1)
    else:
        log.error("Could not find latest data timestamp because " + \
                  "the month value could not be found in the HTML.")
        shutdown(1)
    
    # Search through the HTML for the day.
    log.debug("Searching for the day ...")
    match = re.search(r"""id="endday".*?value="(.*?)".*?>""", htmlStr)
    if match:
        cellText = match.groups()[0]
        log.debug("Cell text is: " + cellText)

        if len(cellText) == 1 or len(cellText) == 2:
            yahooDayStr = cellText
        else:
            log.error("Cell text for the day number is not of length 1 or 2.")
            shutdown(1)
    else:
        log.error("Could not find latest data timestamp because " + \
                  "the day value could not be found in the HTML.")
        shutdown(1)
    
    # Search through the HTML for the year.
    log.debug("Searching for the year ...")
    match = re.search(r"""id="endyear".*?value="(.*?)".*?>""", htmlStr)
    if match:
        cellText = match.groups()[0]
        log.debug("Cell text is: " + cellText)

        if len(cellText) == 4:
            yahooYearStr = cellText
        else:
            log.error("Cell text for the year number is not of length 4.")
            shutdown(1)
    else:
        log.error("Could not find latest data timestamp because " + \
                  "the year value could not be found in the HTML.")
        shutdown(1)


    log.debug("yahooMonthStr == {}".format(yahooMonthStr))
    log.debug("yahooDayStr   == {}".format(yahooDayStr))
    log.debug("yahooYearStr  == {}".format(yahooYearStr))
    
    # Convert the obtained values to integers.
    monthInt = int(yahooMonthStr) + 1
    dayInt = int(yahooDayStr)
    yearInt = int(yahooYearStr)

    # Convert the int values to the desired str values.
    monthStr = "{:02}".format(monthInt)
    dayStr = "{:02}".format(dayInt)
    yearStr = "{:04}".format(yearInt)

    rv = "{}{}{}".format(yearStr, monthStr, dayStr)

    log.debug("Returning rv == {}".format(rv))

    return rv

def convertStartTimestampStrToUrlArgsStr(timestampStr):
    """Converts input str of a date timestamp from format YYYYMMDD to
    the format required in the URL for a HTTP GET to Yahoo Finance
    for the start date of the data series.
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

    log.debug("yearStr={}, monthStr={}, dayStr={}".\
              format(yearStr, monthStr, dayStr))

    # Convert yearStr to int.
    yearInt = int(yearStr)

    # Convert monthStr to int.  The month here is 0-based.
    monthInt = int(monthStr) - 1

    # Convert dayStr to int.
    dayInt = int(dayStr)

    log.debug("yearInt={}, monthInt={}, dayInt={}".\
              format(yearInt, monthInt, dayInt))

    rv = "a={}&b={}&c={}".format(monthInt, dayInt, yearInt)
    
    log.debug(" returning: {}".format(rv))
    
    return rv

def convertEndTimestampStrToUrlArgsStr(timestampStr):
    """Converts input str of a date timestamp from format YYYYMMDD to
    the format required in the URL for a HTTP GET to Yahoo Finance
    for the end date of the data series.
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

    log.debug("yearStr={}, monthStr={}, dayStr={}".\
              format(yearStr, monthStr, dayStr))

    # Convert yearStr to int.
    yearInt = int(yearStr)

    # Convert monthStr to int.  The month here is 0-based.
    monthInt = int(monthStr) - 1

    # Convert dayStr to int.
    dayInt = int(dayStr)

    log.debug("yearInt={}, monthInt={}, dayInt={}".\
              format(yearInt, monthInt, dayInt))

    rv = "d={}&e={}&f={}".format(monthInt, dayInt, yearInt)
    
    log.debug(" returning: {}".format(rv))
    
    return rv

def reformatYahooDateField(dateStr):
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
    if len(dayStr) != 2 or (not dayStr.isnumeric()):
        log.error("day in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)
    if len(monthStr) != 2 or (not monthStr.isnumeric()):
        log.error("month in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)
    if len(yearStr) != 4 or (not yearStr.isnumeric()):
        log.error("year in dateStr is not in the expected format.  " + \
              "dateStr given is: {}".format(dateStr))
        shutdown(1)

    rv = "{}/{}/{}".format(monthStr, dayStr, yearStr)

    return rv

def reformatYahooFinanceDataLine(line):
    """Converts the Yahoo Finance CSV line format to our desired format.

    Yahoo gives us lines in the format:
        Date,Open,High,Low,Close,Volume,Adj Close
        2011-05-27,12398.06,12519.35,12382.93,12441.58,3124560000,12441.58

    We want it in format:
        "Date","Open","High","Low","Close","Volume","OpenInt"
        05/27/2011,12398.06,12519.35,12382.93,12441.58,3124560000,0

    Returns: the converted string
    """

    fields = line.split(",")
    
    if len(fields) != 7:
        log.error("Input line from Yahoo isn't in the expected format.  " +\
              "Line given is: {}".format(line))
        shutdown(1)

    dateStr = fields[0]
    openStr = fields[1]
    highStr = fields[2]
    lowStr  = fields[3]
    closeStr = fields[4]
    volumeStr = fields[5]
    adjCloseStr = fields[6]
        
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

    dateStr = reformatYahooDateField(dateStr)
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


def getPriceBarDataLines():
    """Returns the price bar data lines of text for a CSV file.

    This function has inputs.  It expects the following global
    variables to be set:

        stockSymbol
        startTimestampStr
        endTimestampStr
        formattedTimeUnit
    
    Returns:
    list of str; each str holds a line containing the price bar data.
    """
    
    log.debug("startTimestampStr == {}".format(startTimestampStr))
    log.debug("endTimestampStr   == {}".format(endTimestampStr))
            
    formattedStartTimestamp = \
        convertStartTimestampStrToUrlArgsStr(startTimestampStr)
    formattedEndTimestamp = \
        convertEndTimestampStrToUrlArgsStr(endTimestampStr)
    
    url = "http://ichart.finance.yahoo.com/table.csv?" + \
          "s={}".format(stockSymbol) + \
          "&{}".format(formattedStartTimestamp) + \
          "&{}".format(formattedEndTimestamp) + \
          "&{}".format(formattedTimeUnit) + \
          "&ignore=.csv"
    
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
    
    # Get rid of header lines in the Yahoo data file.
    if len(outputLines) > 0:
        index = 0
        yahooHeaderLine = "Date,Open,High,Low,Close,Volume,Adj Close"
        if outputLines[index].find(yahooHeaderLine) != -1:
            log.debug("Found header line.")
            outputLines.pop(index)
    
    # Reverse the order of the bars, since we want the lines in our file
    # to be from oldest to newest.
    outputLines.reverse()
    
    reformattedLines = []
    for line in outputLines:
        if line.strip() != "":
            reformattedLine = reformatYahooFinanceDataLine(line.strip())
            reformattedLines.append(reformattedLine)
    
    log.info("Obtained a total of {} price bars.".format(len(reformattedLines)))
    
    if len(reformattedLines) > 0:
        log.info("Earliest PriceBar is: {}".format(reformattedLines[0]))
        log.info("Latest   PriceBar is: {}".format(reformattedLines[-1]))
    
    return reformattedLines

def isNumber(numStr):
    """Returns True if the string is a number."""

    rv = True
    
    for letter in numStr:
        if not (letter.isdigit() or letter == "."):
            rv = False
            break

    return rv
        
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
    
parser.add_option("--stock-symbol",
                  action="store",
                  type="str",
                  dest="stockSymbol",
                  default=None,
                  help="Specify stock symbol to obtain data for.  " + \
                       "This is a required field.",
                  metavar="<SYMBOL>")

parser.add_option("--update",
                  action="store_true",
                  dest="updateFlag",
                  default=False,
                  help="Update the output file with stock price data starting from the last date in that file.  If the output file doesn't exist, then the output file is created and all the available data is saved.  This option doesn't do a check of the existing data to ensure data integrity of the previous pricebars.  Note also that the --update option takes precedence over --start-timestamp and --end-timestamp options.   This is an optional command-line argument.")
                  
parser.add_option("--start-timestamp",
                  action="store",
                  type="str",
                  dest="startTimestampStr",
                  default=None,
                  help="Specify starting date of the data.  " + \
                       "This is an optional field.  " + \
                       "If not specified, the earliest " + \
                       "date of data available is used.  "
                       "Format of this string is 'YYYYMMDD'.",
                  metavar="<TIMESTAMP>")

parser.add_option("--end-timestamp",
                  action="store",
                  type="str",
                  dest="endTimestampStr",
                  default=None,
                  help="Specify ending date of the data.  " + \
                       "This is an optional field.  " + \
                       "If not specified, the latest " + \
                       "date of data is used.  "
                       "Format of this string is 'YYYYMMDD'.",
                  metavar="<TIMESTAMP>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file.  This is a required field.",
                  metavar="<FILE>")

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
    
if options.updateFlag == True:
    updateFlag = True
else:
    updateFlag = False
    
    if options.startTimestampStr == None:
        startTimestampStr = getTimestampStrForEarliestData(stockSymbol)
        log.info("Start timestamp was not specified.  " + \
                 "Using earliest available date for data ({}).".\
                 format(startTimestampStr))
    else:
        startTimestampStr = options.startTimestampStr
          
    if options.endTimestampStr == None:
        endTimestampStr = getTimestampStrForLatestData(stockSymbol)
        log.info("End timestamp was not specified.  " + \
                 "Using latest available date for data ({}).".\
                 format(endTimestampStr))
    else:
        endTimestampStr = options.endTimestampStr
          
if options.outputFile == None:
    log.error("Please specify an output filename to the " + \
          "--output-file option.")
    shutdown(1)
else:
    outputFile = os.path.abspath(options.outputFile)

##############################################################################


if updateFlag == True:
    # Do an update of the output file.
    log.debug("Attempting to do an update of the output file.")
                   
    # First see if the output file exists.
    if os.path.isfile(outputFile):
        log.debug("Output file '{}' exists.  Reading it to get old data.".\
                  format(outputFile))
        
        # Read the data that is already in outputFile.
        oldLines = []
        i = 0
        with open(outputFile, "r") as f:
            for line in f:
                if i >= numLinesToSkip:
                    strippedLine = line.rstrip()
                    if strippedLine != "":
                        oldLines.append(strippedLine)
                i += 1

        log.debug("Read {} data lines from the file.".format(len(oldLines)))
            
        # See if there is at least one data line.  We check for 2 or
        # more lines because the first line is the header line.
        if len(oldLines) >= 2:
            lastLine = oldLines[-1]
            log.debug("Last line is: {}".format(lastLine))
            
            fields = lastLine.split(",")
            
            if len(fields) != 7:
                log.error("Line that we read from the output file " + \
                          "isn't in the expected format.  " +\
                          "Line given is: {}".format(line))
                shutdown(1)

            dateStr = fields[0]
            
            dateFields = dateStr.split("/")
            
            monthStr = dateFields[0]
            dayStr   = dateFields[1]
            yearStr  = dateFields[2]

            dt = datetime.datetime(year=int(yearStr),
                                   month=int(monthStr),
                                   day=int(dayStr))
            nextDt = dt + datetime.timedelta(days=1)

            # Convert the int values to the desired str values.
            monthStr = "{:02}".format(nextDt.month)
            dayStr = "{:02}".format(nextDt.day)
            yearStr = "{:04}".format(nextDt.year)
            
            startTimestampStr = "{}{}{}".format(yearStr, monthStr, dayStr)
            endTimestampStr = getTimestampStrForLatestData(stockSymbol)

            if startTimestampStr > endTimestampStr:
                # Start timestamp is after the end timestamp.
                # This means that the file is already up to date
                # because we can't query data any later than this.
                log.info("File '{}' is already up to date.".\
                         format(outputFile))
                shutdown(0)

            try:
                # List of str holding all the lines of price bar data
                # text that was retrieved.
                reformattedLines = getPriceBarDataLines()
            except urllib.error.HTTPError as e:
                if e.code == 404 and startTimestampStr == endTimestampStr:
                    # This means that Yahoo doesn't have any more
                    # pricebars for this timeframe.
                    log.info("File '{}' is already up to date.".\
                             format(outputFile))
                    shutdown(0)
                else:
                    log.error("{}".format(e))
                    shutdown(1)
                    
            # Write to file, truncating.
            log.info("Writing to output file '{}' ...".format(outputFile))
    
            with open(outputFile, "w", encoding="utf-8") as f:
                f.write(headerLine + newline)
                for line in oldLines:
                    f.write(line + newline)
                for line in reformattedLines:
                    f.write(line + newline)
        else:
            # File doesn't have at least 2 lines.  (one for header and
            # one actual data line).  That means we should just query
            # for all data and overwrite the output file.
            startTimestampStr = getTimestampStrForEarliestData(stockSymbol)
            endTimestampStr = getTimestampStrForLatestData(stockSymbol)

            # List of str holding all the lines of price bar data text that was
            # retrieved. .
            reformattedLines = getPriceBarDataLines()
            
            # Write to file, truncating.
            log.info("Writing to output file '{}' ...".format(outputFile))
    
            with open(outputFile, "w", encoding="utf-8") as f:
                f.write(headerLine + newline)
                for line in reformattedLines:
                    f.write(line + newline)
    else:
        # File doesn't exist already.
        
        # Query for all data and overwrite the output file.
        startTimestampStr = getTimestampStrForEarliestData(stockSymbol)
        endTimestampStr = getTimestampStrForLatestData(stockSymbol)

        # List of str holding all the lines of price bar data text that was
        # retrieved. .
        reformattedLines = getPriceBarDataLines()
        
        # Write to file, truncating.
        log.info("Writing to output file '{}' ...".format(outputFile))

        with open(outputFile, "w", encoding="utf-8") as f:
            f.write(headerLine + newline)
            for line in reformattedLines:
                f.write(line + newline)
                
else:
    # Not doing an update.  Means we just use the start and end timestamps.
    log.debug("Getting data to create or overwrite output file.")

    # List of str holding all the lines of price bar data text that was
    # retrieved. .
    reformattedLines = getPriceBarDataLines()
    
    # Write to file, truncating if it already exists.
    log.info("Writing to output file '{}' ...".format(outputFile))
    
    with open(outputFile, "w", encoding="utf-8") as f:
        f.write(headerLine + newline)
        for line in reformattedLines:
            f.write(line + newline)

log.info("Done.")
shutdown(0)


