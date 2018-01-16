#!/usr/bin/env python3
##############################################################################
# Description:
#
# This script calculates the timestamps of lunar dates in each lunar year
# within the time range of startLunarYear and endLunarYear lunar years.
# The timestamp at this moment in time is saved in various formats
# and written to output text CSV file.
#
# The output filename can be modified by changing the setting of the
# 'outputFilename' global variable in the code below.
# 
# 
# Usage:
#
#   1) Run the script:
#
#           python3 calculatePlanetLunarDates.py
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
from astrologychart import AstrologyUtils
from ephemeris import Ephemeris
from lunar_calendar_utils import LunarDate
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

# Starting lunar year to get dates for.
startLunarYear = 1905

# Ending lunar year to get dates for.
endLunarYear = 1940

# List of lunar dates to get for each year.
#
# The items in this list are a tuple containing two values:
# - int for the lunar month in the range [1, 13]
# - float for the lunar day of the month in the range [0.0, 30).
lunarDatesDesired = [
    (1, 0.0),     # Nisan 1
    ]

# Error threshold for calculating timestamps of retrograde and direct planets.
maxErrorTd = datetime.timedelta(seconds=1)

# Destination output CSV file.
outputFilename = thisScriptDir + os.sep + "planetLunarDates.csv"

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

    # Dictionary of results computed.
    results = {}
    
    log.info("Obtaining planet lunar dates information ...")
    lunarDates = []
    for lunarYear in range(startLunarYear, endLunarYear + 1):
        for lunarDateTup in lunarDatesDesired:
            lunarMonth = lunarDateTup[0]
            lunarDay = lunarDateTup[1]

            # Skip dates that aren't in a valid month.
            # This is not necessarily an error in input.
            # For example, if we wanted to print all the
            # new moons which are on the 13th month.
            isValidMonth = False
            if 1 <= lunarMonth <= 12:
                isValidMonth = True
            elif lunarMonth == 13 and LunarCalendarUtils.isLunarLeapYear(lunarYear):
                isValidMonth = True
            else:
                isValidMonth = False

            if isValidMonth:
                ld = LunarDate(lunarYear, lunarMonth, lunarDay)
                lunarDates.append(ld)
    
    # Print out results.
    headerLine = \
        "Planet Name," + \
        "Julian Day," + \
        "Datetime," + \
        "LunarDate,"
    
    # Remove trailing comma.
    headerLine = headerLine[:-1]
    
    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)
    
    for lunarDate in lunarDates:
        planetName = "LD(" + lunarDate.toConciseStringWithoutCommas() + ")"
        dt = LunarCalendarUtils.lunarDateToDatetime(lunarDate, tzInfo=timezone)
        jd = Ephemeris.datetimeToJulianDay(dt)

        dtStr = Ephemeris.datetimeToStrWithoutMicroseconds(dt)
        lunarDateStr = "LD(" + lunarDate.toConciseStringWithoutCommas() + ")"
        
        # Assemble the line that will go into the CSV file.
        line = ""
        line += "{}".format(planetName) + ","
        line += "{}".format(jd) + ","
        line += "{}".format(dtStr) + ","
        line += "{}".format(lunarDateStr) + ","
        
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
