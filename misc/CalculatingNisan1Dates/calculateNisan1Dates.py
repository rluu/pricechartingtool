#!/usr/bin/env python3
##############################################################################
# Description:
#
# This script calculates the timestamp and longitude location of
# Nisan 1 dates.  The timestamp and planet longitude at this moment in
# time is saved and later written to output text CSV file.
#
# The calculation for Nisan 1 can be done in the standard way, or
# it can potentially be done in other non-standard ways if desired.  
# This can be modified by changing code/method being invoked in the code
# below.
#
# The output filename can be modified by changing the setting of the
# 'outputFilename' global variable in the code below.
# 
# Usage:
#
#   1) Run the script:
#
#           python3 calculateNisan1Dates.py
#
#   2) View the output CSV file.
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
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from ephemeris import Ephemeris
from ephemeris_utils import EphemerisUtils
from lunar_calendar_utils import LunarCalendarUtils
from data_objects import *
from cache import Cache

##############################################################################

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Location information to use with the Ephemeris.
locationName = "New York City"
locationLongitude = -74.0064
locationLatitude = 40.7142
locationElevation = 0

# Timezone information to use with the Ephemeris.
#timezone = pytz.timezone("US/Eastern")
timezone = pytz.utc

# Time of the day to use to whem getting ephemeris measurements.
hourOfDay = 12
minuteOfHour = 0


startDt = datetime.datetime(year=1890, month=1, day=1,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)

endDt   = datetime.datetime(year=1940, month=12, day=31,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)

# Step size used when incrementing through all the timestamps between
# startDt and endDt.
stepSizeTd = datetime.timedelta(days=1)

# Error threshold for calculating timestamps.
maxErrorTd = datetime.timedelta(seconds=1)

# Destination output CSV file.
outputFilename = thisScriptDir + os.sep + "nisan1Dates.csv"

# Planet names to do calculations for.
geocentricPlanetNames = [\
    "MoSu",
    "Moon",
    "Mercury",
    "Venus",
    "Sun",
    #"Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    #"Neptune",
    #"Pluto",
    "TrueNorthNode",
    "TrueSouthNode",
    #"Chiron",
    #"Isis"
    ]

# Cache enabling.
cacheEnabled = True

# For logging.
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
#log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    # Close the Ephemeris so it can do necessary cleanups.
    Ephemeris.closeEphemeris()
    
    if cacheEnabled:
        Cache.saveCachesToShelve()

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

def formatToDateStr(dt):
    """Returns a date string in the format: "YYYY-MM-DD".

    Arguments:
    dt - datetime.datetime object.

    Returns:
    str object holding the date in format "YYYY-MM-DD".
    """

    dateStr = "{:04}-{:02}-{:02}".\
              format(dt.year, dt.month, dt.day)
    
    return dateStr

def formatToDateAndTimeStr(dt):
    """Returns a timestamp string in the format: "YYYY-MM-DD HH:MM"
    
    Arguments:
    dt - datetime.datetime object.

    Returns:
    str object holding the date in format "YYYY-MM-DD HH:MM".
    """

    dateAndTimeStr = "{:04}-{:02}-{:02} {:02}:{:02}".\
              format(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    
    return dateAndTimeStr

def getNisan1DatesStandard():
    """
    Returns a list of the datetimes of the Nisan 1 dates, according to the
    standard method of calculating, astronomically.

    Nisan 1 is the timestamp of the moment of the first new moon before the
    first full moon that occurs after the solar Spring equinox.
    """

    startYear = startDt.year
    endYear = endDt.year

    nisan1Dts = []
    for year in range(startYear, endYear + 1):
        print("DEBUG: Doing year: {}".format(year))
        nisan1Dt = LunarCalendarUtils.getNisan1DatetimeForYear(year)
        if startDt <= nisan1Dt <= endDt:
            nisan1Dts.append(nisan1Dt)
        
    return nisan1Dts

def getNisan1DatesRelativeToAfterSunTrueNorthNodeConjunction():
    """
    Returns a list of the datetimes of the Nisan 1 dates, according to the
    following non-standard reference point:

    This method returns the new moon for Nisan 1 that is the first new
    moon after the G.Sun crosses the Moon's TrueNorthNode.
    """

    resultDts = []

    dts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            startDt,
            endDt,
            "SunTrueNorthNode",
            "geocentric",
            "tropical",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

    if log.isEnabledFor(logging.DEBUG):
        log.debug("Got the following timestamps for G.Sun crossing 0 degrees: ")
        for dt in dts:
            log.debug("  " + Ephemeris.datetimeToDayStr(dt))

    for dt in dts:
        newMoonSearchStartDt = dt
        newMoonSearchEndDt = dt + datetime.timedelta(days=35)
        log.debug("Searching for new moons between " +
                Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                Ephemeris.datetimeToStr(newMoonSearchEndDt))
        newMoonDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            newMoonSearchStartDt,
            newMoonSearchEndDt,
            "MoSu",
            "geocentric",
            "tropical",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

        if log.isEnabledFor(logging.DEBUG):
            log.debug("Got the following timestamps for G.MoSu crossing "
                + "0 degrees between the given start and end timestamps for "
                + "this year: ")
            for newMoonDt in newMoonDts:
                log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

        if len(newMoonDts) == 0:
            log.error("Did not find any new moons in the time period specified: " +
                "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) +
                ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt))
        elif len(newMoonDts) > 2:
            log.error("Found too many new moons in the time period specified: " +
                "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) +
                ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt))
        else:
            # Append the earliest timestamp.
            newMoonDt = newMoonDts[0]
            resultDts.append(newMoonDt)

    return resultDts

def getNisan1DatesRelativeToBeforeSunTrueNorthNodeConjunction():
    """
    Returns a list of the datetimes of the Nisan 1 dates, according to the
    following non-standard reference point:

    This method returns the new moon for Nisan 1 that is the first new
    moon before the G.Sun crosses the Moon's TrueNorthNode.
    """

    resultDts = []

    dts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            startDt,
            endDt,
            "SunTrueNorthNode",
            "geocentric",
            "tropical",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

    if log.isEnabledFor(logging.DEBUG):
        log.debug("Got the following timestamps for G.SunTrueNorthNode crossing 0 degrees: ")
        for dt in dts:
            log.debug("  " + Ephemeris.datetimeToDayStr(dt))

    for dt in dts:
        newMoonSearchStartDt = dt - datetime.timedelta(days=35)
        newMoonSearchEndDt = dt
        log.debug("Searching for new moons between " +
                Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                Ephemeris.datetimeToStr(newMoonSearchEndDt))
        newMoonDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            newMoonSearchStartDt,
            newMoonSearchEndDt,
            "MoSu",
            "geocentric",
            "tropical",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

        if log.isEnabledFor(logging.DEBUG):
            log.debug("Got the following timestamps for G.MoSu crossing "
                + "0 degrees between the given start and end timestamps for "
                + "this year: ")
            for newMoonDt in newMoonDts:
                log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

        if len(newMoonDts) == 0:
            log.error("Did not find any new moons in the time period specified: " +
                "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) +
                ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt))
        elif len(newMoonDts) > 2:
            log.error("Found too many new moons in the time period specified: " +
                "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) +
                ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt))
        else:
            # Append the latest timestamp.
            newMoonDt = newMoonDts[-1]
            resultDts.append(newMoonDt)

    return resultDts

##############################################################################

if __name__ == "__main__":
    if cacheEnabled:
        # Initialize the caches.
        Cache.loadCachesFromShelve()

    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    # Set the Location (required).
    Ephemeris.setGeographicPosition(locationLongitude,
                                    locationLatitude,
                                    locationElevation)

    if True:
        dts = getNisan1DatesStandard()
        headerLine = "Nisan1DatesStandard"
    if False:
        dts = getNisan1DatesRelativeToAfterSunTrueNorthNodeConjunction()
        headerLine = "Nisan1DatesRelativeToAfterSunTrueNorthNodeConjunction"
    if False:
        dts = getNisan1DatesRelativeToBeforeSunTrueNorthNodeConjunction()
        headerLine = "Nisan1DatesRelativeToBeforeSunTrueNorthNodeConjunction"
    
    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)

    for dt in dts:
        line = "{}".format(Ephemeris.datetimeToDayStr(dt))
        outputLines.append(line)
    
    # Write outputLines to output file.
    with open(outputFilename, "w", encoding="utf-8") as f:
        log.info("Writing to output file '{}' ...".format(outputFilename))
    
        endl = "\n"
    
        for line in outputLines:
            f.write(line + endl)
    
    log.info("Done.")
    shutdown(0)

##############################################################################
