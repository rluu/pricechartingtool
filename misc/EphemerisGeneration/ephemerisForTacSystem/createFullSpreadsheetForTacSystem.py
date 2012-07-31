#!/usr/bin/env python3
##############################################################################
# Description:
#
#  Script for creating a spreadsheet with all the information that
#  would be needed in the IBM system given by TAC in WITS post #61757
#  and #61777.
#
# The resulting spreadsheet will have the following fields:
# 
#   1) IBM OHLC data.
#
#   2) IBM cycle hit points from the TAC system:
#        - Hit points on the 2P cycle ("X" in a column)
#        - Hit points on the 3P cycle ("X" in a column)
#
#   4) TAC ephemeris fields.  These are:
#        1) MARS - SATURN           (absolute) (mod 360) (mod 12)
#        1) MARS - SATURN + EARTH   (absolute) (mod 360) (mod 10)
#
#   3) Ephemeris of other planets:
#        - Geocentric
#        - Heliocentric
#        - Declination
#
# Usage:
#   1) Make sure the input files have been created or generated.
#   
#   2) Edit the global variables below, making sure the paths to the input and
#   output files are set appropriately.
#
#   3) Run this script:
#
#          python3 ./createFullSpreadsheetForTacSystem.py
#  
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For copy.deepcopy()
import copy

# For dates.
import datetime

# For logging.
import logging

# For math.floor()
import math

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
thisScriptDir = os.path.dirname(thisScriptDir)
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from ephemeris import Ephemeris
from data_objects import *

##############################################################################

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Location information to use with the Ephemeris.
locationName = "New York City"
locationLongitude = 40.783
locationLatitude = 73.97
locationElevation = 0

# Timezone information to use with the Ephemeris.
timezone = pytz.timezone("US/Eastern")

# Default str used for time in a PriceBar data CSV file line.
defaultTimeStr = "12:00"
defaultHourOfDay = 12
defaultMinuteOfHour = 0

# Time of the day to use to whem getting ephemeris measurements.
hourOfDay = 12
minuteOfHour = 0

# Planet names to do calculations for.
geocentricPlanetNames = [\
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    #"Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "TrueNorthNode",
    "Chiron",
    "Isis"
    ]

# Planet names to do calculations for.
heliocentricPlanetNames = [\
    #"Sun",
    #"Moon",
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    #"TrueNorthNode",
    "Chiron",
    "Isis"
    ]

# Planet names to do calculations for.
declinationPlanetNames = [\
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    #"Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "TrueNorthNode",
    "Chiron",
    "Isis"
    ]


# Input file:
#  - IBM.txt (IBM pricebar data CSV file).
priceBarDataCsvFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/IBM_TAC_system_full.csv"
priceBarDataCsvFileLinesToSkip = 1

# Input file:
#  - TacEphemeris2.csv
tacEphemerisCsvFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/TacEphemeris2.csv"
tacEphemerisCsvFileLinesToSkip = 1

# Input file:
#  - cycleHitDates2P.csv
cycleHitDates2PlanetCsvFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/cycleHitDates2P.csv"
cycleHitDates2PlanetCsvFileLinesToSkip = 1

# Input file:
#  - cycleHitDates3P.csv
cycleHitDates3PlanetCsvFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/cycleHitDates3P.csv"
cycleHitDates3PlanetCsvFileLinesToSkip = 1

# Destination output CSV file.
outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/IBM_TAC_system_full.csv"

# For logging.
#logging.basicConfig(level=logging.DEBUG,
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    # Close the Ephemeris so it can do necessary cleanups.
    Ephemeris.closeEphemeris()
    
    logging.shutdown()
    
    sys.exit(rc)

##############################################################################

def isNumber(numStr):
    """Returns True if the string is a number."""

    rv = True
    
    for letter in numStr:
        if not (letter.isdigit() or letter == "."):
            rv = False
            break

    return rv

def convertEphemerisTimestampStrToDatetime(timestampStr):
    """Converts a timestamp str given in the one of the two formats to
    a datetime.datetime object.  If no time of day is given in the
    str, then the default time and timezone will be used.  See global
    variables.

    Arguments:
    timestampStr - str in one of the following formats:
    
                   YYYY-MM-DD
                   YYYY-MM-DD HH:MM

                   Where HH is a value in range [00, 23].
                   
    Returns:
    datetime.datetime object representing the timestamp given in the str.
    If the format is invalid, then None is returned.
    """
    
    dateOnlyFormat = "YYYY-MM-DD"
    dateAndTimeFormat = "YYYY-MM-DD HH:MM"

    # Check input string for correct formatting.
    if len(timestampStr) != len(dateOnlyFormat) and \
           len(timestampStr) != len(dateAndTimeFormat):
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None

    elif len(timestampStr) == len(dateOnlyFormat):
        if timestampStr[4] != "-" or timestampStr[7] != "-":
            log.error("Read a timestamp from the CSV file that is " + \
                      "not in the correct format.  timestampStr == '{}'".\
                      format(timestampStr))
            return None
        
    elif len(timestampStr) == len(dateAndTimeFormat):
        if timestampStr[4] != "-" or timestampStr[7] != "-" or \
               timestampStr[10] != " " or timestampStr[13] != ":":
            
            log.error("Read a timestamp from the CSV file that is " + \
                      "not in the correct format.  timestampStr == '{}'".\
                      format(timestampStr))
            return None
        

    yearStr = timestampStr[0:4]
    monthStr = timestampStr[5:7]
    dayStr = timestampStr[8:10]

    hourStr = None
    minuteStr = None
    if len(timestampStr) == len(dateAndTimeFormat):
        hourStr = timestampStr[11:13]
        minuteStr = timestampStr[14:16]
    else:
        hourStr   = "{:02}".format(defaultHourOfDay)
        minuteStr = "{:02}".format(defaultMinuteOfHour)
    
    # Test to make sure all the str values are digits before
    # converting to int values.
    for letter in yearStr:
        if not letter.isdigit():
            log.error("There is a non-digit year value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in monthStr:
        if not letter.isdigit():
            log.error("There is a non-digit month value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in dayStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    for letter in hourStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    for letter in minuteStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    
    # Convert the substrings to int values for the parts of the date/time.
    year = int(yearStr)
    month = int(monthStr)
    day = int(dayStr)

    hour = int(hourStr)
    minute = int(minuteStr)
    
    rv = datetime.datetime(year, month, day, hour, minute, \
                           tzinfo=timezone)
    
    return rv

def formatToDateStr(dt):
    """Returns a date string in the format: "YYYY-MM-DD".

    Arguments:
    dt - datetime.datetime object.

    Returns:
    str object holding the date in format "YYYY-MM-DD".
    """

    dateStr = ""
    
    if dt.year < 10:
        dateStr += "000{}".format(dt.year)
    elif dt.year < 100:
        dateStr += "00{}".format(dt.year)
    elif dt.year < 1000:
        dateStr += "0{}".format(dt.year)
    else:
        dateStr += "{}".format(dt.year)

    dateStr += "-"
    if dt.month < 10:
        dateStr += "0{}".format(dt.month)
    else:
        dateStr += "{}".format(dt.month)
    
    dateStr += "-"
    if dt.day < 10:
        dateStr += "0{}".format(dt.day)
    else:
        dateStr += "{}".format(dt.day)
    
    return dateStr

def validateLine(line):
    """Validates a line of text from the pricebar data CSV file is a valid line.
    
    Arguments:
    line - str in one of the following formats:
    
      <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
      
      <MM/DD/YYYY HH:MM>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
      
    Returns:
    
    tuple of (boolean, str) that represents if the line
    of text was parsed to be a valid CSV data line.
    If the line of text is valid, the boolean part of the tuple 
    returned is True and the string is returned is empty.
    If the line of text is found to be not valid, the tuple returns
    False and a string explaining why the validation failed.
    """
    
    #log.debug("validateLine(line='{}')".format(line))
    
    # Check the number of fields.
    fields = line.split(",")
    numFieldsExpected = 7
    if len(fields) != numFieldsExpected:
        return (False, "Line does not have {} data fields".\
                format(numFieldsExpected))
    
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
        timeStr = None
        
    elif len(timestampStr) == 16:
        # Format of timestamp is 'MM/DD/YYYY HH:MM'.
        timestampStrSplit = timestampStr.split(" ")
        
        if len(timestampStrSplit) != 2:
            return (False, "Format of the timestamp was not " + \
                    "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'.")
        
        dateStr = timestampStrSplit[0]
        timeStr = timestampStrSplit[1]
        
    else:
        # Invalid number of characters for the timestamp.
        return (False, "Format of the timestamp was not " + \
                "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'.")
    
    dateStrSplit = dateStr.split("/")
    if len(dateStrSplit) != 3:
        return (False, "Format of the timestamp was not " + \
                "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'.")
    
    monthStr = dateStrSplit[0]
    dayStr = dateStrSplit[1]
    yearStr = dateStrSplit[2]
    
    if len(monthStr) != 2:
        return (False, "Month in the date is not two characters long")
    if len(dayStr) != 2:
        return (False, "Day in the date is not two characters long")
    if len(yearStr) != 4:
        return (False, "Year in the date is not four characters long")
    
    try:
        monthInt = int(monthStr)
        if monthInt < 1 or monthInt > 12:
            return (False, "Month in the date is not between 1 and 12")
    except ValueError as e:
        return (False, "Month in the date is not a number")
    
    try:
        dayInt = int(dayStr)
        if dayInt < 1 or dayInt > 31:
            return (False, "Day in the date is not between 1 and 31")
    except ValueError as e:
        return (False, "Day in the date is not a number")
    
    try:
        yearInt = int(yearStr)
    except ValueError as e:
        return (False, "Year in the date is not a number")
    
    
    hourStr = None
    minuteStr = None
    
    if timeStr != None:
        timeFields = timeStr.split(":")
        
        if len(timeFields) != 2:
            errStr = \
                "Format of the time was not 'HH:MM'." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        hourStr = timeFields[0]
        minuteStr = timeFields[1]
        
        if len(hourStr) != 2:
            errStr = \
                "Hour in the timestamp is not " + \
                "two characters long." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        if len(minuteStr) != 2:
            errStr = \
                "Minute in the timestamp is not " + \
                "two characters long." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        try:
            hourInt = int(hourStr)
            if hourInt < 0 or hourInt > 23:
                errStr = \
                    "Hour in the timestamp is not in range " + \
                    "[00, 23]." + \
                    "  timeStr == {}".format(timeStr)
                return (False, errStr)
        except ValueError as e:
            errStr = \
                "Hour in the timestamp is not a number." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        try:
            minuteInt = int(minuteStr)
            if minuteInt < 0 or minuteInt > 59:
                errStr = \
                    "Minute in the timestamp is not in " + \
                    "range [00, 59]." + \
                    "  timeStr == {}".format(timeStr)
                return (False, errStr)
        except ValueError as e:
            errStr = \
                "Minute in the timestamp is not a number." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        
    try:
        openFloat = float(openStr)
    except ValueError as e:
        return (False, "OpenPrice is not a number")
    
    try:
        highFloat = float(highStr)
    except ValueError as e:
        return (False, "HighPrice is not a number")
    
    try:
        lowFloat = float(lowStr)
    except ValueError as e:
        return (False, "LowPrice is not a number")
    
    try:
        closeFloat = float(closeStr)
    except ValueError as e:
        return (False, "ClosePrice is not a number")
    
    try:
        volumeFloat = float(volumeStr)
    except ValueError as e:
        return (False, "Volume is not a number")
    
    try:
        openIntFloat = float(openIntStr)
    except ValueError as e:
        return (False, "OpenInterest is not a number")
    
    
    # If it got this far without returning, then everything 
    # checked out fine.
    return (True, "")


def convertLineToPriceBar(line):
    """Convert a line of text from pricebar data CSV file to a PriceBar.
    
    The expected format of 'line' one of the following:
    <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
    <MM/DD/YYYY HH:MM>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
        
    Returns:
    PriceBar object from the line of text.  If the text was incorrectly
    formatted, then None is returned.  
    """

    #log.debug("convertLineToPriceBar(line='{}')".format(line))
    
    # Return value.
    retVal = None
    
    # Do validation on the line first.
    (validFlag, reasonStr) = validateLine(line)
    
    if validFlag == False:
        log.error("Line conversion failed because: {}" + reasonStr)
        retVal = None
    else:
        # Although we already validated the line, we wrap the parsing 
        # here in a try block just in case something unexpected 
        # was thrown at us.
        try:
            fields = line.split(",")
            
            timestampStr = fields[0]
            openPrice = float(fields[1])
            highPrice = float(fields[2])
            lowPrice = float(fields[3])
            closePrice = float(fields[4])
            volume = float(fields[5])
            openInt = float(fields[6])
            
            dateStr = None
            timeStr = None
            
            if len(timestampStr) == 10:
                # Format of timestamp is 'MM/DD/YYYY'.
                dateStr = timestampStr

                # No time of day is given, so we will use the default.
                timeStr = defaultTimeStr
                
            elif len(timestampStr) == 16:
                # Format of timestamp is 'MM/DD/YYYY HH:MM'.
                timestampStrSplit = timestampStr.split(" ")
                
                dateStr = timestampStrSplit[0]
                timeStr = timestampStrSplit[1]
                
            else:
                reasonStr = \
                    "Invalid number of characters in timestampStr."
                log.error("Line conversion failed because: {}" + \
                         reasonStr)
                retVal = None
                return retVal
            
            dateStrSplit = dateStr.split("/")
            month = int(dateStrSplit[0])
            day = int(dateStrSplit[1])
            year = int(dateStrSplit[2])
            
            timeStrSplit = timeStr.split(":")
            hour = int(timeStrSplit[0])
            minute = int(timeStrSplit[1])
            second = 0
            timestamp = \
                datetime.datetime(year,
                                  month, 
                                  day, 
                                  hour, 
                                  minute, 
                                  second,
                                  tzinfo=timezone)
            
            # Create the PriceBar with the parsed data.
            retVal = PriceBar(timestamp, 
                              open=openPrice,
                              high=highPrice,
                              low=lowPrice,
                              close=closePrice,
                              oi=openInt,
                              vol=volume)
            
        except IndexError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an IndexError: " + e)
        except UnicodeDecodeError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an UnicodeDecodeError: " + e)
        except ValueError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an ValueError: " + e)
        except TypeError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an TypeError: " + e)
            
    # Return the PriceBar created (or None if an error occurred).
    return retVal

def getPlanetaryInfosForDatetime(dt):
    """Helper function for getting a list of PlanetaryInfo objects
    to display in the astrology chart.
    """

    # Set the location again (required).
    Ephemeris.setGeographicPosition(locationLongitude,
                                    locationLatitude,
                                    locationElevation)
    
    # Get planetary info for all the planets.
    planets = []
    
    # Astrological house system for getting the house cusps.
    houseSystem = Ephemeris.HouseSys['Porphyry']
    
    planets.append(Ephemeris.getH1PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH2PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH3PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH4PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH5PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH6PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH7PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH8PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH9PlanetaryInfo(dt, houseSystem))
    planets.append(Ephemeris.getH10PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH11PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH12PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getARMCPlanetaryInfo(dt, houseSystem))
    planets.append(Ephemeris.getVertexPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getEquatorialAscendantPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getCoAscendant1PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getCoAscendant2PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getPolarAscendantPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getHoraLagnaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getGhatiLagnaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMeanLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getOsculatingLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(dt))
    planets.append(Ephemeris.getSunPlanetaryInfo(dt))
    planets.append(Ephemeris.getMoonPlanetaryInfo(dt))
    planets.append(Ephemeris.getMercuryPlanetaryInfo(dt))
    planets.append(Ephemeris.getVenusPlanetaryInfo(dt))
    planets.append(Ephemeris.getEarthPlanetaryInfo(dt))
    planets.append(Ephemeris.getMarsPlanetaryInfo(dt))
    planets.append(Ephemeris.getJupiterPlanetaryInfo(dt))
    planets.append(Ephemeris.getSaturnPlanetaryInfo(dt))
    planets.append(Ephemeris.getUranusPlanetaryInfo(dt))
    planets.append(Ephemeris.getNeptunePlanetaryInfo(dt))
    planets.append(Ephemeris.getPlutoPlanetaryInfo(dt))
    planets.append(Ephemeris.getMeanNorthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
    planets.append(Ephemeris.getTrueNorthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getCeresPlanetaryInfo(dt))
    #planets.append(Ephemeris.getPallasPlanetaryInfo(dt))
    #planets.append(Ephemeris.getJunoPlanetaryInfo(dt))
    #planets.append(Ephemeris.getVestaPlanetaryInfo(dt))
    planets.append(Ephemeris.getIsisPlanetaryInfo(dt))
    #planets.append(Ephemeris.getNibiruPlanetaryInfo(dt))
    planets.append(Ephemeris.getChironPlanetaryInfo(dt))
    #planets.append(Ephemeris.getGulikaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMandiPlanetaryInfo(dt))
    planets.append(Ephemeris.getMeanOfFivePlanetaryInfo(dt))
    planets.append(Ephemeris.getCycleOfEightPlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgJuSaUrNePlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgJuSaPlanetaryInfo(dt))

    return planets


def getEarliestDateFromData(priceBars, tacEphemerisData, cycleHitDates2PlanetSystem, cycleHitDates3PlanetSystem):
    """Obtains the earliest date referenced from the various input
    arguments.  

    Arguments:
    
      priceBars - list of PriceBar objects.
    
      tacEphemerisData - list of tuples.
         Each item in this list is a tuple: (datetime.datetime, str)
         The first variable in the tuple is the timestamp for the line.
         The second variable in the tuple is the str of CSV text for
         this timestamp.

      cycleHitDates2PlanetSystem - list of datetime.datetime objects.
    
      cycleHitDates3PlanetSystem - list of datetime.datetime objects.
    
    Returns:
    datetime.datetime object that is the earliest timestamp.
    If no dates are in any of these objects, then None is returned.
    """
    
    earliestDatetime = None

    for pb in priceBars:
        dt = pb.timestamp
        
        if earliestDatetime == None:
            earliestDatetime = dt
        elif dt < earliestDatetime:
            earliestDatetime = dt

    for tacEphemerisDataTuple in tacEphemerisData:
        dt = tacEphemerisDataTuple[0]
        
        if earliestDatetime == None:
            earliestDatetime = dt
        elif dt < earliestDatetime:
            earliestDatetime = dt

    for dt in cycleHitDates2PlanetSystem:
        if earliestDatetime == None:
            earliestDatetime = dt
        elif dt < earliestDatetime:
            earliestDatetime = dt

    for dt in cycleHitDates3PlanetSystem:
        if earliestDatetime == None:
            earliestDatetime = dt
        elif dt < earliestDatetime:
            earliestDatetime = dt

    rv = copy.deepcopy(earliestDatetime)
    
    return rv


def getLatestDateFromData(priceBars, tacEphemerisData, cycleHitDates2PlanetSystem, cycleHitDates3PlanetSystem):
    """Obtains the latest date referenced from the various input
    arguments.  For efficiency's sake, this function assumes that the
    data in these input arguments is ordered from earliest timestamp
    to latest timestamp.

    Arguments:
    
      priceBars - list of PriceBar objects.
    
      tacEphemerisData - list of tuples.
         Each item in this list is a tuple: (datetime.datetime, str)
         The first variable in the tuple is the timestamp for the line.
         The second variable in the tuple is the str of CSV text for
         this timestamp.

      cycleHitDates2PlanetSystem - list of datetime.datetime objects.
    
      cycleHitDates3PlanetSystem - list of datetime.datetime objects.
    
    Returns:
    datetime.datetime object that is the earliest timestamp.
    If no dates are in any of these objects, then None is returned.
    """
    
    latestDatetime = None

    for pb in priceBars:
        dt = pb.timestamp
        
        if latestDatetime == None:
            latestDatetime = dt
        elif dt > latestDatetime:
            latestDatetime = dt

    for tacEphemerisDataTuple in tacEphemerisData:
        dt = tacEphemerisDataTuple[0]
        
        if latestDatetime == None:
            latestDatetime = dt
        elif dt > latestDatetime:
            latestDatetime = dt

    for dt in cycleHitDates2PlanetSystem:
        if latestDatetime == None:
            latestDatetime = dt
        elif dt > latestDatetime:
            latestDatetime = dt

    for dt in cycleHitDates3PlanetSystem:
        if latestDatetime == None:
            latestDatetime = dt
        elif dt > latestDatetime:
            latestDatetime = dt

    rv = copy.deepcopy(latestDatetime)
    
    return rv


def getTimestampInfoDataLine(dt):
    """Obtains the line of CSV text that describes this datetime.datetime
    time.

    Arguments:
    
    dt - datetime.datetime object holding the timestamp of which to
         get information on.

    Returns:
    str in CSV format, holding the information regarding this timestamp.
    The data in this string is:
    
        jd,day,date,time,timezone
        
    """

    
    # Field: jd
    rv += "{}".format(Ephemeris.datetimeToJulianDay(dt))
    rv += ","
    
    # Timezone name string, extracted from datetime.tzname().
    # This accounts for the fact that datetime.tzname() can return None.
    datetimeObj = dt
    tznameStr = datetimeObj.tzname()
    if tznameStr == None:
        tznameStr = ""
    dayOfWeekStr = datetimeObj.ctime()[0:3]
    offsetStr = \
        Ephemeris.getTimezoneOffsetFromDatetime(datetimeObj)
    
    # Field: day
    rv += dayOfWeekStr
    rv += ","
    
    # Field: date
    rv += "{:04}-{:02}-{:02}".\
          format(datetimeObj.year,
                 datetimeObj.month,
                 datetimeObj.day)
    #rv += "{:02}/{:02}/{:04}".\
    #      format(datetimeObj.month,
    #             datetimeObj.day,
    #             datetimeObj.year)
    rv += ","
    
    # Field: time
    rv += "{:02}:{:02}:{:02}".\
          format(datetimeObj.hour,
                 datetimeObj.minute,
                 datetimeObj.second)
    rv += ","
    
    # Field: timezone.
    rv += "{}{}".format(tznameStr, offsetStr)
    rv += ","

    # Remove trailing comma.
    rv = rv[:-1]

    return rv

    
def getPriceBarDataLineForDate(priceBars, dt):
    """Obtains the line of CSV text related to the PriceBar at the
    date given.  

    If there is no pricebar data for the date desired, then blanks
    will be returned for each of the fields related to the pricebar.
    (i.e. ",,,,," would be returned.)

    Arguments:
    priceBars - list of PriceBar objects.
    dt - datetime.datetime object with the timestamp seeked.  We only
         look at the date in this object.
    
    Returns:
    str in CSV format, holding the data for this PriceBar.
    The data in this string is:
    
       open,high,low,close,volume,oi
       
    """

    # Return value.
    rv = ""

    
    # Find the PriceBar object with the same timestamp date.
    pb = None
    for priceBar in priceBars:
        if priceBar.timestamp().date() == dt.date():
            pb = priceBar
            break

    # If no PriceBar objects had a timestamp with the same date, then
    # return blank values for the price data.
    if pb == None:
        rv = ",,,,,"
        return rv

    
    # Field: open
    rv += "{}".format(pb.open)
    rv += ","
    
    # Field: high
    rv += "{}".format(pb.high)
    rv += ","
    
    # Field: low
    rv += "{}".format(pb.low)
    rv += ","
    
    # Field: close
    rv += "{}".format(pb.close)
    rv += ","
    
    # Field: volume
    rv += "{}".format(pb.vol)
    rv += ","
    
    # Field: oi
    rv += "{}".format(pb.oi)
    rv += ","

    # Remove trailing comma.
    rv = rv[:-1]
    
    return rv


def getTacEphemerisDataLineForDate(tacEphemerisData, dt):
    """Obtains the line of CSV text related to the TAC ephemeris data
    at the date given.  

    Arguments:
      tacEphemerisData - list of tuples.
         Each item in this list is a tuple: (datetime.datetime, str)
         The first variable in the tuple is the timestamp for the line.
         The second variable in the tuple is the str of CSV text for
         this timestamp.

      dt - datetime.datetime object with the timestamp seeked.  We only
           look at the date in this object.
    
    Returns:
    str in CSV format.  If no values for the given date timestamp then
    blank CSV values are returned (set of commas).
    """

    # Return value.
    rv = None
    
    for tacEphemerisDataTuple in tacEphemerisData:
        tacEphemerisDt = tacEphemerisDataTuple[0]
        
        if tacEphemerisDt.date() == dt.date():
            rv = tacEphemerisDataTuple[1]
            break

    if rv == None:
        # No matching dates.

        # Return a set of commas, but to do that we need to know how
        # many fields there are for the tac ephemeris.  For that we'll
        # check the first tuple element in the list.  If the list is
        # empty, then we'll return an empty string.

        if len(tacEphemerisData) == 0:
            rv = ""
        else:
            csvText = tacEphemerisData[0][1]
            fieldValues = csvText.split(",")
            
            rv = ""
            for i in range(len(fieldValues)):
                rv += ","

            # Remove trailing comma.
            rv = rv[:-1]
            
    return rv
        

def getCycleHitDate2PlanetSystemDataLineForDate(cycleHitDates2PlanetSystem, dt):
    """Obtains the line of CSV text related to the cycle hit date
    at the date given.  This function assumes that the data in these
    input arguments is ordered from earliest timestamp to latest
    timestamp.

    Arguments:
    dt - datetime.datetime object with the timestamp seeked.  We only
         look at the date in this object.
    
    Returns:

    str in CSV format. If the date is in the list, then "X" is returned.
    Otherwise "" is returned.
    """

    # Return value.
    rv = ""
    
    for cycleHitDt in cycleHitDates2PlanetSystem:
        if cycleHitDt.date() == dt.date():
            rv = "X"
            break

    return rv

def getCycleHitDate3PlanetSystemDataLineForDate(cycleHitDates3PlanetSystem, dt):
    """Obtains the line of CSV text related to the cycle hit date
    at the date given.  This function assumes that the data in these
    input arguments is ordered from earliest timestamp to latest
    timestamp.

    Arguments:
    dt - datetime.datetime object with the timestamp seeked.  We only
         look at the date in this object.
    
    Returns:

    str in CSV format. If the date is in the list, then "X" is returned.
    Otherwise "" is returned.
    """

    
    # Return value.
    rv = ""
    
    for cycleHitDt in cycleHitDates3PlanetSystem:
        if cycleHitDt.date() == dt.date():
            rv = "X"
            break

    return rv
    
def getEphemerisDataLineForDatetime(dt):
    """Obtains the line of CSV text of planetary position data.

    Arguments:
    dt - datetime.datetime object with the timestamp seeked.  
    
    Returns:
    
    str in CSV format. Since there are a lot of fields, please See the
    section of code where we write the header info str for the format.
    """
    
    
    planetaryInfos = getPlanetaryInfosForDatetime(dt)

    # Planet geocentric longitude 15-degree axis points.
    for planetName in geocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.geocentric['tropical']['longitude']
                rv += "{:6.3f},".format(lon % 15.0)
                    
    # Planet geocentric longitude.
    for planetName in geocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.geocentric['tropical']['longitude']
                rv += "{:6.3f},".format(lon)
                    
    # Planet geocentric longitude in zodiac str format.
    for planetName in geocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.geocentric['tropical']['longitude']
                valueStr = \
                         AstrologyUtils.\
                         convertLongitudeToStrWithRasiAbbrev(lon)
                rv += valueStr + ","
                
    # Planet heliocentric longitude 15-degree axis points.
    for planetName in heliocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.heliocentric['tropical']['longitude']
                rv += "{:6.3f},".format(lon % 15.0)
                    
    # Planet heliocentric longitude.
    for planetName in heliocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.heliocentric['tropical']['longitude']
                rv += "{:6.3f},".format(lon)
                    
    # Planet heliocentric longitude in zodiac str format.
    for planetName in heliocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.heliocentric['tropical']['longitude']
                valueStr = \
                         AstrologyUtils.\
                         convertLongitudeToStrWithRasiAbbrev(lon)
                rv += valueStr + ","
                
    # Planet declination.
    for planetName in declinationPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                declination = pi.geocentric['tropical']['declination']
                rv += "{:6.3f},".format(declination)
    

    # Remove trailing comma.
    rv = rv[:-1]

    return rv


##############################################################################

#if __name__ == "__main__":
    
# Initialize Ephemeris (required).
Ephemeris.initialize()

# Set the Location (required).
Ephemeris.setGeographicPosition(locationLatitude,
                                locationLongitude,
                                locationElevation)

# Get the pricebar data as a list of PriceBar objects.

# List of PriceBar objects.
priceBars = []

inputFilename = priceBarDataCsvFilename
linesToSkip = priceBarDataCsvFileLinesToSkip
try: 
    with open(inputFilename, "r") as f:
        # Line number index.
        i = 0
        
        for line in f:
            if i < linesToSkip:
                # Skip this line.
                continue

            # Conver the str a PriceBar, and append it.
            pb = convertLineToPriceBar(line)
            if pb == None:
                log.error("Failed to convert a line of text from the " + \
                          "PriceBar data CSV file ('{}') to a PriceBar.  ".\
                          format(inputFilename) + \
                          "It failed on line {}.".format(i + 1))
                shutdown(1)
            else:
                priceBars.append(pb)

            # Increment the index for the next iteration.
            i += 1
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)
    
# TAC ephemeris header fields.  We will read this in from the file.
tacEphemerisHeaderFields = ""

# TAC ephemeris list of data.
#
# Each item in this list is a tuple: (datetime.datetime, str)
# The first variable in the tuple is the timestamp for the line.
# The second variable in the tuple is the str of text for this timestamp.
#
tacEphemerisData = []

inputFilename = tacEphemerisCsvFilename
linesToSkip = tacEphemerisCsvFileLinesToSkip
try:
    with open(inputFilename, "r") as f:
        # Line number index.
        i = 0
        
        for line in f:
            if i < linesToSkip:
                # This is a header line.
                tacEphemerisHeaderFields = line
                continue

            fieldValues = line.split(",")
            
            # It is assumed that the first field is the timestamp.
            timestampStr = fieldValues[0]
            
            dt = convertEphemerisTimestampStrToDatetime(timestampStr)

            if dt == None:
                # Could not convert because of invalid format.
                log.error("Failed to convert a timestamp str to datetime " + \
                          "on line {} of '{}'".\
                          format(i + 1, inputFilename))
                shutdown(1)
            else:
                tacEphemerisData.append((dt, line))

            # Increment hte index for the next iteration.
            i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)

    
# List of datetime.datetime objects.
cycleHitDates2PlanetSystem = []

# List of datetime.datetime objects.
cycleHitDates3PlanetSystem = []


inputFilename = cycleHitDates2PlanetCsvFilename
linesToSkip = cycleHitDates2PlanetCsvFileLinesToSkip
try:
    with open(inputFilename, "r") as f:
        # Line number index.
        i = 0
        
        for line in f:
            if i < linesToSkip:
                # Skip this line.
                continue

            fieldValues = line.split(",")
            
            # It is assumed that the first field is the timestamp.
            timestampStr = fieldValues[0]
            
            dt = convertEphemerisTimestampStrToDatetime(timestampStr)
            
            if dt == None:
                # Could not convert because of invalid format.
                log.error("Failed to convert a timestamp str to datetime " + \
                          "on line {} of '{}'".\
                          format(i + 1, inputFilename))
                shutdown(1)
            else:
                cycleHitDates2PlanetSystem.append(dt)

            # Increment hte index for the next iteration.
            i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)



inputFilename = cycleHitDates3PlanetCsvFilename
linesToSkip = cycleHitDates3PlanetCsvFileLinesToSkip
try:
    with open(inputFilename, "r") as f:
        # Line number index.
        i = 0
        
        for line in f:
            if i < linesToSkip:
                # Skip this line.
                continue

            fieldValues = line.split(",")
            
            # It is assumed that the first field is the timestamp.
            timestampStr = fieldValues[0]
            
            dt = convertEphemerisTimestampStrToDatetime(timestampStr)
            
            if dt == None:
                # Could not convert because of invalid format.
                log.error("Failed to convert a timestamp str to datetime " + \
                          "on line {} of '{}'".\
                          format(i + 1, inputFilename))
                shutdown(1)
            else:
                cycleHitDates3PlanetSystem.append(dt)

            # Increment hte index for the next iteration.
            i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)




# Compile the header line text.
headerLine = ""
headerLine += "jd,day,date,time,timezone,open,high,low,close,volumn,oi,"
headerLine += "CycleHit2P,CycleHit3P,"
headerLine += tacEphemerisHeaderFields + ","

# Planet geocentric longitude mod 15.
for planetName in geocentricPlanetNames:
    headerLine += "G." + planetName + ","

# Planet geocentric longitude.
for planetName in geocentricPlanetNames:
    headerLine += "G." + planetName + ","

# Planet geocentric longitude in zodiac str format.
for planetName in geocentricPlanetNames:
    headerLine += "G." + planetName + ","


# Planet heliocentric longitude mod 15.
for planetName in heliocentricPlanetNames:
    headerLine += "H." + planetName + ","

# Planet heliocentric longitude.
for planetName in heliocentricPlanetNames:
    headerLine += "H." + planetName + ","

# Planet heliocentric longitude in zodiac str form.
for planetName in heliocentricPlanetNames:
    headerLine += "H." + planetName + ","

# Planet declination.
for planetName in declinationPlanetNames:
    headerLine += "D." + planetName + ","

# Remove the trailing comma.
headerLine = headerLine[:-1]

# Get the earliest date.
earliestDate = getEarliestDateFromData(priceBars,
                                       tacEphemerisData,
                                       cycleHitDates2PlanetSystem,
                                       cycleHitDates3PlanetSystem)

log.debug("Earliest timestamp in all the files is: {}".\
          format(Ephemeris.datetimeToStr(earliestDate))

latestDate = getEarliestDateFromData(priceBars,
                                     tacEphemerisData,
                                     cycleHitDates2PlanetSystem,
                                     cycleHitDates3PlanetSystem)

log.debug("Latest timestamp in all the files is: {}".\
          format(Ephemeris.datetimeToStr(earliestDate))


startDt = earliestDate
endDt = latestDate

# Initialize the currDt to the start date.  Manually set the hour and
# minute so we get the ephemeris at noon localized time.
currDt = copy.deepcopy(startDt)
currDt.hour = hourOfDay
currDt.minute = minuteOfHour

stepSizeTd = datetime.timedelta(days=1)

# Text in the output file.
outputLines = []
outputLines.append(headerLine)

while currDt.date() < endDt.date():
    line = ""
    
    line += getTimestampInfoDataLine(currDt) + ","
    line += getPriceBarDataLineForDate(priceBars, currDt) + ","
    line += getCycleHitDate2PlanetSystemDataLineForDate(\
        cycleHitDates2PlanetSystem, dt) + ","
    line += getCycleHitDate3PlanetSystemDataLineForDate(\
        cycleHitDates3PlanetSystem, dt) + ","
    line += getTacEphemerisDataLineForDate(tacEphemerisData, currDt) + ","
    line += getEphemerisDataLineForDatetime(dt) + ","
    
    # Remove the last trailing comma. 
    line = line[:-1]
    
    # Append to the output lines.
    outputLines.append(line)
    
    # Increment the currDt by the step size for the next iteration.
    # Also, make sure the time is set.
    currDt = currDt + stepSizeTd
    currDt.hour = hourOfDay
    currDt.minute = minuteOfHour
    
    
# Write outputLines to output file.
with open(outputFilename, "w") as f:
    log.info("Writing to output file '{}' ...".format(outputFilename))
    
    endl = "\r\n"
    
    for line in outputLines:
        f.write(line + endl)
    
log.info("Done.")
shutdown(0)


##############################################################################
