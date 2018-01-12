#!/usr/bin/env python3
##############################################################################
# Description:
#
# This script calculates the timestamps of a planet crossing certain
# longitude degrees within the time range of startDt and
# endDt.  The timestamps at this moment in time is
# saved in various formats and written to output text CSV file.
#
# The output filename can be modified by changing the setting of the
# 'outputFilename' global variable in the code below.
# 
# 
# Usage:
#
#   1) Run the script:
#
#           python3 calculatePlanetCrossingLongitudeDegrees.py
#
#   2) View the output CSV file.
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys
import errno

# For sorting by second key of a tuple.
import operator

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
from astrologychart import AstrologyUtils
from ephemeris import Ephemeris
from ephemeris_utils import EphemerisUtils
from lunar_calendar_utils import LunarDate
from lunar_calendar_utils import LunarCalendarUtils
from data_objects import *

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


startDt = datetime.datetime(year=1905, month=1, day=1,
                            hour=12, minute=0,
                            tzinfo=timezone)

endDt   = datetime.datetime(year=1940, month=12, day=31,
                            hour=12, minute=0,
                            tzinfo=timezone)

# Error threshold for calculating timestamps of retrograde and direct planets.
maxErrorTd = datetime.timedelta(seconds=1)

# Planet name.
planetName = "Venus"

# Centricity type.
centricityType = "heliocentric"

# Longitude type.
longitudeType = "tropical"

# List of longitude degrees to get timestamps for.
# Each longitude is a float.
longitudeDegreesDesired = [
    90.0,
    270.0,
    ]

# Error threshold for calculating timestamps of retrograde and direct planets.
maxErrorTd = datetime.timedelta(seconds=1)

# Destination output CSV file.
outputFilename = thisScriptDir + os.sep + "planetCrossingLongitudeDegrees.csv"

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

    
##############################################################################

if __name__ == "__main__":
    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    # Set the Location (required).
    Ephemeris.setGeographicPosition(locationLongitude,
                                    locationLatitude,
                                    locationElevation)

    results = []
    
    log.info("Obtaining planet crossing longitude degrees dates info ...")

    for degree in longitudeDegreesDesired:
        dts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            startDt,
            endDt,
            planetName,
            centricityType,
            longitudeType,
            degree,
            maxErrorTd=maxErrorTd)

        for dt in dts:
            tup = (degree, dt)
            results.append(tup)

    # Sort results by datetime.
    results.sort(key=operator.itemgetter(1))
    
    # Print out results.
    headerLine = \
        "Planet Name," + \
        "Julian Day," + \
        "Datetime," + \
        "LunarDate," + \
        "CentricityType," + \
        "LongitudeType," + \
        "Longitude,"
    
    # Remove trailing comma.
    headerLine = headerLine[:-1]
    
    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)

    for result in results:
        degree = result[0]
        dt = result[1]

        jd = Ephemeris.datetimeToJulianDay(dt)
        lunarDate = LunarCalendarUtils.datetimeToLunarDate(dt)

        dtStr = Ephemeris.datetimeToStr(dt)
        lunarDateStr = "LD(" + lunarDate.toConciseStringWithoutCommas() + ")"
        
        # Assemble the line that will go into the CSV file.
        line = ""
        line += "{}".format(planetName) + ","
        line += "{}".format(jd) + ","
        line += "{}".format(dtStr) + ","
        line += "{}".format(lunarDateStr) + ","
        line += "{}".format(centricityType) + ","
        line += "{}".format(longitudeType) + ","
        line += "{}".format(degree) + ","
        
        # Remove last trailing comma.
        line = line[:-1]
        
        # Append to the output lines.
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
