#!/usr/bin/env python3
##############################################################################
#
# Description:
#
#   Web scraper that obtains futures pricebar data from Barchart.com.
#
#   Barchart.com features:
#     - Historical data back to the year 1969.
#     - Cash commodity price data.
#     - Continuous futures data.
#     - Intraday   futures data.
#     - Daily      futures data.
#     - Weekly     futures data.
#     - Monthly    futures data.
#
# Usage:
#
#     ./getFuturesDataFromBarChart.py --help
#     ./getFuturesDataFromBarChart.py --version
#
#     # Update the intraday file, from the last pricebar in the output
#     # file, to the current moment in time.  If the output file is
#     # empty or doesn't exist, then intraday data is retrieved for
#     # the last week and written to the file.
#     ./getFuturesDataFromBarChart.py --update --futures-symbol=ZSK12 --interval=I --intraday-bar-size=1 --output-file=/tmp/testing.txt
#
#     # Update the output file, from the last pricebar in the output
#     # file, to the current moment in time.  If the output file is
#     # empty or doesn't exist, then data is retrieved for the last
#     # year and written to the file.
#     ./getFuturesDataFromBarChart.py --update --futures-symbol=ZSK12 --interval=DO --output-file=/tmp/testing.txt
#
#     # Write to the output file, retrieving pricebars starting from
#     # the given start timestamp to the given end timestamp.
#     ./getFuturesDataFromBarChart.py --futures-symbol=ZSK12 --interval=I --intraday-bar-size=1 --start-timestamp=20111101 --end-timestamp=20111114 --output-file=/tmp/testing.txt
#
#     # Write to the output file, retrieving pricebars starting from
#     # the given start timestamp to the given end timestamp.
#     ./getFuturesDataFromBarChart.py --futures-symbol=ZSK12 --interval=DO --start-timestamp=20091001 --end-timestamp=20111014 --output-file=/tmp/testing.txt
#
#     # Write to the output file, such that it holds pricebars
#     # starting from the earliest timestamp of data available to the
#     # latest timestamp of data availble.
#     ./getFuturesDataFromBarChart.py --futures-symbol=ZSK12 --interval=DO --output-file=/tmp/testing.txt
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

# Futures symbol to obtain data for.
# This value is obtained via command-line parameter.
futuresSymbol = ""

# Flag that says we should do an update of the output file.
updateFlag = False

# Interval (amount of time) for each pricebar.
# Valid values:
#   "I"  - Intraday chart
#   "DO" - Daily contract
#   "DN" - Daily nearest
#   "DC" - Daily continuous
#   "WO" - Weekly contract
#   "WN" - Weekly nearest
#   "WC" - Weekly continuous
#   "MO" - Monthly contract
#   "MN" - Monthly nearest
#   "MC" - Monthly continuous
# This value is obtained via command-line parameter.
interval = None

# Intraday bar time length, in minutes.
# Can be just about any number (1, 4, 5, 60, 120, etc.).
# This value must be specified if the interval specified
# is "I" (Intraday).
# This value is obtained via command-line parameter.
intradayBarSize = None

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

# Number of lines to skip in the file being read.
numLinesToSkip = 1

# Use Windows newlines in the output file.
newline = "\r\n"

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

def convertDateStrToUrlVariableStr(timestampStr):
    """Converts input str of a date timestamp from format YYYYMMDD to
    the format required in the URL for a HTTP GET to Barchart
    for the start or end date of the data series.
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

    rv = "{}%2F{}%2F{}".format(monthStr, dayStr, yearStr)
    
    log.debug(" returning: {}".format(rv))
    
    return rv

def reformatBarchartTimestampField(timestampStr):
    """Converts a date string in the format 
    "Tue. Dec 13, 2011" to "MM/DD/YYYY HH:MM".
    The converted string is returned.

    This function does error checking to make sure the input is in the
    correct expected format.
    """
    
    timestampFields = timestampStr.split(" ")
    
    if len(timestampFields) != 4:
        log.error("Timestamp from Barchart is not in the expected format.  " + \
                  "timestampStr == {}".format(timestampStr))
        shutdown(1)
        
    monthAbbrevStr = timestampFields[1]
    if len(monthAbbrevStr) != 3:
        log.error("Timestamp from Barchart is not in the expected format.  " + \
                  "monthAbbrevStr == {}, ".format(monthAbbrevStr) + \
                  "timestampStr == {}".format(timestampStr))
        shutdown(1)
        
    dayStr = timestampFields[2].rstrip(",")
    if not dayStr.isdigit():
        log.error("Timestamp from Barchart is not in the expected format.  " + \
                  "dayStr == {}, ".format(dayStr) + \
                  "timestampStr == {}".format(timestampStr))
        shutdown(1)
        
    yearStr = timestampFields[3]
    if not yearStr.isdigit():
        log.error("Timestamp from Barchart is not in the expected format.  " + \
                  "yearStr == {}, ".format(yearStr) + \
                  "timestampStr == {}".format(timestampStr))
        shutdown(1)
        
    timeStr = timestampFields[4]
    
    timeFields = timeStr.split(":")
    if len(timeFields) < 2:
        log.error("Timestamp from Barchart is not in the expected format.  " + \
                  "timeStr == {}, ".format(timeStr) + \
                  "timestampStr == {}".format(timestampStr))
        shutdown(1)
        
    hourStr = timeFields[0]
    if len(hourStr) != 2 or not hourStr.isdigit():
        log.error("Timestamp from Barchart is not in the expected format.  " + \
                  "hourStr == {}, ".format(hourStr) + \
                  "timestampStr == {}".format(timestampStr))
        shutdown(1)
        
    minuteStr = timeFields[1]
    if len(minuteStr) != 2 or not minuteStr.isdigit():
        log.error("Timestamp from Barchart is not in the expected format.  " + \
                  "minuteStr == {}, ".format(minuteStr) + \
                  "timestampStr == {}".format(timestampStr))
        shutdown(1)
        
    # Convert month abbreviation to a two character str holding
    # the month number.
    monthStr = None
    ma = monthAbbrevStr.lower()
    if ma == "jan":
        monthStr = "01"
    elif ma == "feb":
        monthStr = "02"
    elif ma == "mar":
        monthStr = "03"
    elif ma == "apr":
        monthStr = "04"
    elif ma == "may":
        monthStr = "05"
    elif ma == "jun":
        monthStr = "06"
    elif ma == "jul":
        monthStr = "07"
    elif ma == "aug":
        monthStr = "08"
    elif ma == "sep":
        monthStr = "09"
    elif ma == "oct":
        monthStr = "10"
    elif ma == "nov":
        monthStr = "11"
    elif ma == "dec":
        monthStr = "12"
    else:
        log.error("Unknown month abbreviation found '{}'".\
                  format(monthAbbrevStr) + \
                  ".  timestampStr == {}".\
                  format(timestampStr))
        shutdown(1)

    # int form of the str values.
    monthInt = None
    dayInt = None
    yearInt = None
    hourInt = None
    minuteInt = None

    # Do conversions and some error checking.
    try:
        monthInt = int(monthStr)
        if monthInt < 1 or monthInt > 12:
            log.error("Month in the date is not between 1 and 12." + \
                      "  monthStr == {}".format(monthStr))
            shutdown(1)
    except ValueError as e:
        log.error("Month in the date is not a number." + \
                  "  monthStr == {}".format(monthStr))
        shutdown(1)
        
    try:
        dayInt = int(dayStr)
        if dayInt < 1 or dayInt > 31:
            log.error("Day in the date is not between 1 and 31." + \
                      "  dayStr == {}".format(dayStr))
            shutdown(1)
    except ValueError as e:
        log.error("Day in the date is not a number." + \
                  "  dayStr == {}".format(dayStr))
        shutdown(1)
            
    try:
        yearInt = int(yearStr)
    except ValueError as e:
        log.error("Year in the date is not a number")
        shutdown(1)

    try:
        hourInt = int(hourStr)
        if hourInt < 0 or hourInt > 23:
            log.error("Hour in the timestamp is not in range [00, 23]." + \
                      "  hourStr == {}".format(hourStr))
            shutdown(1)
    except ValueError as e:
        log.error("Hour in the timestamp is not a number." + \
                  "  hourStr == {}".format(hourStr))
        shutdown(1)

    try:
        minuteInt = int(minuteStr)
        if minuteInt < 0 or minuteInt > 59:
            log.error("Minute in the timestamp is not in range [00, 59]." + \
                      "  minuteStr == {}".format(minuteStr))
            shutdown(1)
    except ValueError as e:
        log.error("Minute in the timestamp is not a number." + \
                  "  minuteStr == {}".format(minuteStr))
        shutdown(1)

    rv = \
       "{:02}/{:02}/{:04} {:02}:{:02}".\
       format(monthInt, dayInt, yearInt, hourInt, minuteInt)
    
    return rv

def getPriceBarDataLines():
    """Returns the price bar data lines of text for a CSV file.

    This function has inputs.  It expects the following global
    variables to be set:

        futuresSymbol
        interval
        intradayBarSize   (used if interval is set to "I")
        startTimestampStr (optional)
        endTimestampStr   (optional)


    Returns:
    list of str; each str holds a line containing the price bar data.

    Notes:
    
    Some miscellaneous notes on the format of the URL are below,
    as a reference in case I need it later for some reason.
    
    Full URL as seen when using the page in a browser:
    
      http://barchart.com/chart.php?sym=ZSK12&style=technical&p=I&d=X&x=19&y=15&im=1&sd=&ed=&size=M&log=0&t=BAR&v=2&g=1&evnt=1&late=1&o1=&o2=&o3=&sh=100&indicators=&addindicator=&submitted=1&fpage=&txtDate=12%2F17%2F2011#jump

    My understanding of the fields (not exhaustive, just some of them
    that I probably care about):
    
      sym   - Symbol, in the format ZSK12
      style - Type of chart style.  Either "technical" or "classic"
      p     - Bar time length (frequency).
              Valid values:
                "I"  - Intraday chart
                "DO" - Daily contract
                "DN" - Daily nearest
                "DC" - Daily continuous
                "WO" - Weekly contract
                "WN" - Weekly nearest
                "WC" - Weekly continuous
                "MO" - Monthly contract
                "MN" - Monthly nearest
                "MC" - Monthly continuous
      d     - Time period.  "X" appears to be a week for Intraday bars,
              and a year for Daily bars.
      x     - Unknown field.  Doesn't appear to be required field.
      y     - Unknown field.  Doesn't appear to be required field.
      im    - Number of minutes for each bar in the intraday chart.
              Only used for intraday.  Can be any number in range [1, 1440).
      sd    - Start date, in the format example "12%2F15%2F2011" for 12/15/2011.
              Doesn't appear to be required field.
      ed    - End date, in the format example "12%2F15%2F2011" for 12/15/2011.
              Doesn't appear to be required field.
      size  - Size of the chart for the technical chart.
              Doesn't appear to be required field.
              Valid values:
                "M" - Medium chart size
                "S" - Small chart size
                "L" - Large chart size
      log   - "0" for linear scale chart, "1" for logrithmic scale chart.
      t     - Bar type.  "BAR" for OHLC bars.  
      v     - Volume.
              Valid values:
                "0" - Volume off
                "1" - Total volume
                "2" - Contract volume
              I'm not sure what the difference is between total volume and
              contract volume.
      g     - Flag for grid lines on the chart.
              Doesn't appear to be required field.
              Valid values:
                "0" - Disabled
                "1" - Enabled

    Examples of URL format that I will be using:

      Without start and end timestamps:
      
        http://barchart.com/chart.php?sym=ZSK12&style=technical&p=I&d=X&im=1&log=0&t=BAR&v=2&g=1

        http://barchart.com/chart.php?sym=ZSK12&style=technical&p=DO&d=X&log=0&t=BAR&v=2&g=1

      With start and end timestamp:
        http://barchart.com/chart.php?sym=ZSK12&style=technical&p=I&d=X&sd=07%2F08%2F2011&ed=01%2F01%2F2011&im=1&log=0&t=BAR&v=2&g=1
    
    """

    log.debug("futuresSymbol == {}".fomrat(futuresSymbol))
    log.debug("interval == {}".fomrat(interval))
    log.debug("intradayBarSize == {}".fomrat(intradayBarSize))
    log.debug("startTimestampStr == {}".format(startTimestampStr))
    log.debug("endTimestampStr   == {}".format(endTimestampStr))

    formattedStartTimestamp = None
    if startTimestampStr != None and startTimestampStr != "":
        formattedStartTimestamp = \
            convertDateStrToUrlVariableStr(startTimestampStr)

    formattedEndTimestamp = None
    if endTimestampStr != None and endTimestampStr != "":
        formattedEndTimestamp = \
            convertDateStrToUrlVariableStr(endTimestampStr)

    url = "http://barchart.com/chart.php?" + \
          "sym={}".format(futuresSymbol) + \
          "&style=technical" + \
          "&p={}".format(interval) + \
          "&d=X"

    if formattedStartTimestamp != None:
        url += "&sd={}".format(formattedStartTimestamp)
        
    if formattedEndTimestamp != None:
        url += "&ed={}".format(formattedEndTimestamp)
        
    if interval == "I":
        url += "&im={}".format(intradayBarSize)

    url += "&log=0" + \
           "&t=BAR" + \
           "&v=2" + \
           "&g=1" + \
    
    log.info("Obtaining futures price data by accessing URL: {}".format(url))
    
    opener = urllib.request.build_opener()
    request = urllib.request.Request(url)
    opener.addheaders = defaultHttpHeaders
    
    log.info("Opening HTTP request.")
    response = opener.open(request)
    
    log.info("Reading HTTP response.")
    data = response.read().decode()
    
    log.info("Processing and reformatting the data ...")
    
    log.debug(" Data read from {} is: ***{}***".format(url, data))

    # The data is within the map tag.
    match = re.search(r"""<map.*?>(.*?)</map>""", data)
        
    if not match:
        log.error("Could not get the pricebar data because " + \
                  "the <map> tag could not be found in the HTML.  " + \
                  "Please investigate why.")
        shutdown(1)

    # Get the text between the map tag.
    mapText = match.groups()[0]
    
    # Class holding info related to a PriceBar as retrieved from
    # Barchart.  We need this because in the HTML/Javascript, the
    # OHLC data is separate from the volume.
    class PriceBar:
        def __init__(self):
            self.timestampStr = None
            self.symbolStr = None
            self.openStr = None
            self.highStr = None
            self.lowStr = None
            self.closeStr = None
            self.volumeStr = "0"
            self.openIntStr = "0"
            
    # PriceBars.  
    priceBars = []

    # Get the text between the parenthesis of the function
    # showOHLCTooltip() in the HTML/Javascript.
    # This will have the OHLC data we are seeking.
    matchesOHLC = re.findall(r"""showOHLCTooltip\((.*?)\)""", mapText)
    
    # Extract OHLC data and put it into PriceBar objects.
    for match in matchesOHLC:
        args = match.split(",")
        
        pb = PriceBar()
        pb.timestampStr = args[2].strip(" '[]")
        pb.symbolStr = args[3].strip(" '")
        pb.openStr = args[4].strip(" '")
        pb.highStr = args[5].strip(" '")
        pb.lowStr = args[6].strip(" '")
        pb.closeStr = args[7].strip(" '")

        priceBars.append(pb)

    # Get the text between the parenthesis of the function
    # showStudyTooltip() in the HTML/Javascript.  This will have
    # the either the volume data or the open interest data.
    matchesStudy = re.findall(r"""showStudyTooltip\((.*?)\)""", mapText)
    
    # Extract the volume data and add it to the PriceBar object
    # that has the same timestamp.
    for match in matchesStudy:
        args = match.split(",")
        
        timestampStr = args[2].strip(" '[]")
        studyNameStr = args[3].strip(" '")
        studyValueStr = args[3].strip(" '")

        log.debug("timestampStr == {}, studyNameStr == {}, studyValueStr == {}".\
                  format(timestampStr, studyNameStr, studyValueStr))
        
        if studyNameStr != "Volume" and studyNameStr != "Interest":
            continue
        elif studyNameStr == "Volume":
            # Flag that says we found the PriceBar that has a
            # matching timestamp and we stored the volume in it.
            storedVolumeFlag = False
            
            # Find the PriceBar with a matching timestampStr.
            for pb in priceBars:
                if pb.timestampStr == timestampStr:
                    # Found the matching PriceBar.
                    # Store the volumeStr.
                    pb.volumeStr = studyValueStr
                    
                    storedVolumeFlag = True
                    break
                
            if storedVolumeFlag == False:
                log.error("Couldn't find a matching timestamp to " + \
                          "store the volume.  Volume timestampStr == {}".\
                          format(timestampStr))
                shutdown(1)
                
        elif studyNameStr == "Interest":
            # Flag that says we found the PriceBar that has a
            # matching timestamp and we stored the open interest in it.
            storedOpenIntFlag = False
            
            # Find the PriceBar with a matching timestampStr.
            for pb in priceBars:
                if pb.timestampStr == timestampStr:
                    # Found the matching PriceBar.
                    # Store the openIntStr.
                    pb.openIntStr = studyValueStr
                    
                    storedOpenIntFlag = True
                    break
                
            if storedOpenIntFlag == False:
                log.error("Couldn't find a matching timestamp to " + \
                          "store the openInt.  " + \
                          "OpenInt timestampStr == {}".\
                          format(timestampStr))
                shutdown(1)
        
    # At this point, 'priceBars' now has a list of PriceBar
    # objects.  We need to convert these objects into the str
    # CSV lines we wanted originally.
    
    reformattedLines = []
    for pb in priceBars:
        
        # Do some checks on the data.
        try:
            openFloat = float(pb.openStr)
        except ValueError as e:
            log.error("Open price str is not a number." + \
                      "  pb.openStr == {}".format(pb.openStr))
            shutdown(1)
        
        try:
            highFloat = float(pb.highStr)
        except ValueError as e:
            log.error("High price str is not a number." + \
                      "  pb.highStr == {}".format(pb.highStr))
            shutdown(1)
        
        try:
            lowFloat = float(pb.lowStr)
        except ValueError as e:
            log.error("Low price str is not a number." + \
                      "  pb.lowStr == {}".format(pb.lowStr))
            shutdown(1)
        
        try:
            closeFloat = float(pb.closeStr)
        except ValueError as e:
            log.error("Close price str is not a number." + \
                      "  pb.closeStr == {}".format(pb.closeStr))
            shutdown(1)

        try:
            volumeFloat = float(pb.volumeStr)
        except ValueError as e:
            log.error("Volume str is not a number." + \
                      "  pb.volumeStr == {}".format(pb.volumeStr))
            shutdown(1)
            
        try:
            openIntFloat = float(pb.openIntStr)
        except ValueError as e:
            log.error("OpenInt str is not a number." + \
                      "  pb.openIntStr == {}".format(pb.openIntStr))
            shutdown(1)

        # Convert the timestamp str to the format we want it in.
        timestampStr = reformatBarchartTimestampField(pb.timestampStr)

        # Create the CSV line.
        line = "{},{},{},{},{},{},{}".\
               format(timestampStr,
                      pb.openStr,
                      pb.highStr,
                      pb.lowStr,
                      pb.closeStr,
                      pb.volumeStr,
                      pb.openIntStr)

        # Append the line.
        reformattedLines.append(line)
        
    # Sort the lines by the timestamp field.
    reformattedLines.sort(key=cmp_to_key(compLines))
    
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
        timestampFields = dateStr.split(" ")
        
        dateStr = timestampFields[0]
        timeStr = timestampFields[1]
    else:
        # Invalid number of characters for the timestamp.
        log.error("Invalid number of characters for the timestamp." + \
                  lineInfoStr)
        shutdown(1)
    
    dateFields = dateStr.split("/")
    if len(dateFields) != 3:
        log.error("Format of the date was not 'MM/DD/YYYY'." + \
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
    
parser.add_option("--futures-symbol",
                  action="store",
                  type="str",
                  dest="futuresSymbol",
                  default=None,
                  help="Specify futures symbol to obtain data for.  " + \
                       "Example: 'ZSK12'.  " + \
                       "This is a required field.",
                  metavar="<SYMBOL>")

parser.add_option("--interval",
                  action="store",
                  type="str",
                  dest="interval"
                  default=None,
                  help="Interval (amount of time) for each pricebar." + \
                       newline + \
"                        Valid values:" + newline + \
"                          'I'  - Intraday chart" + newline + \
"                          'DO' - Daily contract" + newline + \
"                          'DN' - Daily nearest" + newline + \
"                          'DC' - Daily continuous" + newline + \
"                          'WO' - Weekly contract" + newline + \
"                          'WN' - Weekly nearest" + newline + \
"                          'WC' - Weekly continuous" + newline + \
"                          'MO' - Monthly contract" + newline + \
"                          'MN' - Monthly nearest" + newline + \
"                          'MC' - Monthly continuous",
                  metavar="<INTERVAL>")
                  
parser.add_option("--intraday-bar-size",
                  action="store",
                  type="int",
                  dest="intradayBarSize"
                  default=None,
                  help="Intraday bar time length, in minutes.  " + \
                  "Examples: '1', '4', '5', '60', '120', etc.).  " + \
                  "This field is required if the value specified " + \
                  "to the --interval option is 'I' (Intraday).",
                  metavar="<NUM_MINUTES>")
                  
parser.add_option("--update",
                  action="store_true",
                  dest="updateFlag",
                  default=False,
                  help="Update the output file with futures price " + \
                  "data starting from the last timestamp in that file.  " + \
                  "If the output file doesn't exist, then the " + \
                  "output file is created and the data is saved.  " + \
                  "This option doesn't do a check of the existing data " + \
                  "to ensure data integrity of the previous pricebars.  " + \
                  "Note also that the --update option takes precedence " + \
                  "over --start-timestamp and --end-timestamp options.   " + \
                  "This is an optional command-line argument.")
                  
parser.add_option("--start-timestamp",
                  action="store",
                  type="str",
                  dest="startTimestampStr",
                  default=None,
                  help=\
                  "Specify starting date of the data.  " + \
                  "Format of this string is 'YYYYMMDD'." + \
                  "This is an optional field.  " + \
                  "If not specified, the barchart.com default value " + \
                  "is used.  " + \
                  "This barchart.com default timestamp is a certain " + \
                  "time amount before either " + \
                  "the end timestamp specified in --end-timestamp, or a " + \
                  "certain time amount before the end of the contract, or " + \
                  "a certain time amount before the current date.  " + \
                  "In this default case, the time amount beforehand " + \
                  "is dependent on the argument specified to the " + \
                  "--interval option.  " + \
                  "For intraday it is a week, for daily it is a year, " + \
                  "for weekly it is 5 years, and for monthly it is 25 years.",
                  metavar="<TIMESTAMP>")

parser.add_option("--end-timestamp",
                  action="store",
                  type="str",
                  dest="endTimestampStr",
                  default=None,
                  help=\
                  "Specify ending date of the data.  " + \
                  "Format of this string is 'YYYYMMDD'." + \
                  "This is an optional field.  " + \
                  "If not specified, the barchart.com default value " + \
                  "is used.  " + \
                  "This barchart.com default timestamp is either the " + \
                  "last date of available data or the current date, " + \
                  "whichever is later.",
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

if options.futuresymbol == None:
    log.error("Please specify a futures symbol to the " + \
              "--futures-symbol option.")
    shutdown(1)
else:
    # Set it to upper-case value.
    futuresSymbol = options.futuresSymbol.strip().upper()
    
if options.updateFlag == True:
    updateFlag = True
else:
    updateFlag = False
    
    if options.startTimestampStr == None:
        startTimestampStr = ""
        log.debug("Start timestamp was not specified.")
    else:
        startTimestampStr = options.startTimestampStr
        
    if options.endTimestampStr == None:
        endTimestampStr = ""
        log.info("End timestamp was not specified.")
    else:
        endTimestampStr = options.endTimestampStr

if options.interval == None:
    log.error("Please specify an interval to the " + \
              "--interval option.")
    shutdown(1)
else:
    interval = options.interval.strip().upper()

if interval == "I":
    # Interval has been specified as intraday data.
    # This means that the intraday bar size must be specified.
    if options.intradayBarSize == None:
        log.error("Please specify a value to the " + \
                  "--intraday-bar-size option.")
        shutdown(1)
    else:
        # Make sure the intradayBarSize is in a valid range. 
        if 1 <= options.intradayBarSize < 1440:
            intradayBarSize = options.intradayBarSize
        else:
            log.error("Intraday bar size specified must be >= 1 and < 1440.")
            shutdown(1)

if options.outputFile == None:
    log.error("Please specify an output filename to the " + \
          "--output-file option.")
    shutdown(1)
else:
    outputFile = options.outputFile

        
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

            timestampStr = fields[0]
            dateStr = None

            log.debug("timestampStr == {}".format(timestampStr))
            
            if len(timestampStr) == 10:
                # Format of timestamp is 'MM/DD/YYYY'.
                dateStr = timestampStr
                
            elif len(timestampStr) == 16:
                # Format of timestamp is 'MM/DD/YYYY HH:MM'.
                timestampFields = dateStr.split(" ")
                
                dateStr = timestampFields[0]
            else:
                # Invalid number of characters for the timestamp.
                log.error("Invalid number of characters for the timestamp." + \
                          "  Line given is: {}".format(line))
                shutdown(1)
                
            log.debug("dateStr == {}".format(dateStr))
            
            dateFields = dateStr.split("/")
            
            monthStr = dateFields[0]
            dayStr   = dateFields[1]
            yearStr  = dateFields[2]

            dt = datetime.datetime(year=int(yearStr),
                                   month=int(monthStr),
                                   day=int(dayStr))
            nowDt = datetime.datetime.now()
            
            # Convert the int values to the desired str values.
            startTimestampStr = "{:04}{:02}{:02}".format(dt.year, dt.month, dt.day)
            endTimestampStr = "{:04}{:02}{:02}".format(nowDt.year, nowDt.month, nowDt.day)

            reformattedLines = []
            try:
                # List of str holding all the lines of price bar data
                # text that was retrieved.
                reformattedLines = getPriceBarDataLines()
            except urllib.error.HTTPError as e:
                log.error("{}".format(e))
                shutdown(1)

            # Merge the data.
            log.info("Merging old data with new data.  " + \
                     "Old data lines with the same timestamp as " + \
                     "a new data line will be overwritten.")
            
            # List of merged lines.  Start with the contents of
            # 'oldLines'.
            mergedLines = copy.deepcopy(oldLines)

            # Go through 'reformattedLines' and either overwrite the
            # non-unique timestamp lines or if the timestamp is
            # unique, then simply append the line.
            for line in reformattedLines:
                timestampStr = line.split(",")[0]
                
                # Flag that indicates that a matching timestamp was
                # found in the old lines.
                foundMatchingTimestampFlag = False
                
                for i in range(len(mergedLines)):
                    t = mergedLines[i].split(",")[0]
                    if timestampStr == t:
                        # Timestamp already exists in the old lines.
                        # Overwrite this entry.
                        foundMatchingTimestampFlag = True
                        mergedLines[i] = line
                        break
                
                if foundMatchingTimestampFlag == False:
                    # This is a unique timestamp line.
                    # Append it to the mergedLines list.
                    mergedLines.append(line)
            
            # Sort the lines.
            mergedLines.sort(key=cmp_to_key(compLines))
            
            # Write to file, truncating.
            log.info("Writing to output file '{}' ...".format(outputFile))
            
            with open(outputFile, "w") as f:
                f.write(headerLine + newline)
                for line in mergedLines:
                    f.write(line + newline)
        else:
            # File doesn't have at least 2 lines.  (one for header and
            # one actual data line).  That means we should just query
            # for the data and use defaults.
            
            # List of str holding all the lines of price bar data text that was
            # retrieved. .
            reformattedLines = getPriceBarDataLines()
            
            # Write to file, truncating.
            log.info("Writing to output file '{}' ...".format(outputFile))
            
            with open(outputFile, "w") as f:
                f.write(headerLine + newline)
                for line in reformattedLines:
                    f.write(line + newline)
    else:
        # File doesn't exist already.
        # Query for the data and use defaults.

        # List of str holding all the lines of price bar data text that was
        # retrieved. .
        reformattedLines = getPriceBarDataLines()
        
        # Write to file, truncating.
        log.info("Writing to output file '{}' ...".format(outputFile))

        with open(outputFile, "w") as f:
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
    
    with open(outputFile, "w") as f:
        f.write(headerLine + newline)
        for line in reformattedLines:
            f.write(line + newline)

log.info("Done.")
shutdown(0)


