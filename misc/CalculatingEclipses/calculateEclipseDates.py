#!/usr/bin/env python3
##############################################################################
# Description:
#
# This script calculates the timestamp and longitude location of
# eclipse dates.  The timestamp and planet longitude at this moment in
# time is saved and later written to output text CSV file.
#
# The output filename can be modified by changing the setting of the
# 'outputFilename' global variable in the code below.
# 
# Usage:
#
#   1) Run the script:
#
#           python3 calculateEclipseDates.py
#
#   2) View the output CSV file.
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys
import errno

# For dates.
import datetime

# For logging.
import logging

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from ephemeris import Ephemeris
from ephemeris_utils import EphemerisUtils
from lunar_calendar_utils import LunarDate
from lunar_calendar_utils import LunarCalendarUtils
from util import Util
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

# Starting lunar year to do calculations, inclusive.
startLunarYear = 1905

# Ending lunar year to do calculations, inclusive.
endLunarYear = 1940
#endLunarYear = 1908

# Destination output CSV file.
outputFilename = thisScriptDir + os.sep + "eclipseDates.csv"

# Thresholds for determing whether a new or full moon is a solar or lunar
# eclipse.
#longitudeThresholdForSolarEclipse = 18.5166666
longitudeThresholdForSolarEclipse = 18.55
#longitudeThresholdForLunarEclipse = 12.25
#longitudeThresholdForLunarEclipse = 13.0
longitudeThresholdForLunarEclipse = 16.26

# Flags for enabling the calculations for particular eclipse types.
solarEclipsesEnabled = True
lunarEclipsesEnabled = True

# Constants for the eclipse type abbreviation.
solarEclipseTypeStr = "S"
lunarEclipseTypeStr = "L"

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

    newMoonPhase = 0.0
    fullMoonPhase = 15.0

    # List of tuples.  
    # Each tuple is: 
    #   (julian day,
    #    datetime.datetime, 
    #    LunarDate, 
    #    G.Sun longitude, 
    #    G.Moon longitude, 
    #    G.Moon latitude, 
    #    G.TrueNorthNode longitude, 
    #    G.TrueSouthNode longitude,
    #    EclipseTypeStr,              # "S" or "L" for solar or lunar.
    #    DistanceFromNode longitude
    #    )
    eclipseTuples = []

    if startLunarYear > endLunarYear:
        errMsg = \
            "startLunarYear must be less than or equal to endLunarYear." + \
            "  startLunarYear: {}".format(startLunarYear) + \
            "  endLunarYear: {}".format(endLunarYear)
        log.error(errMsg)
        shutdown(1)

    numSolarEclipsesFound = 0
    numLunarEclipsesFound = 0

    infoStr = "Calculating "
    if solarEclipsesEnabled and lunarEclipsesEnabled:
        infoStr += "solar and lunar "
    elif solarEclipsesEnabled and not lunarEclipsesEnabled:
        infoStr += "solar "
    elif not solarEclipsesEnabled and lunarEclipsesEnabled:
        infoStr += "lunar "
    infoStr += "eclipses between the lunar years " + \
        "{} and {}, inclusive ...".format(startLunarYear, endLunarYear)
    log.info(infoStr)

    for lunarYear in range(startLunarYear, endLunarYear + 1):
        startLunarMonth = 1
        endLunarMonth = 12

        if LunarCalendarUtils.isLunarLeapYear(lunarYear):
            endLunarMonth = 13

        for lunarMonth in range(startLunarMonth, endLunarMonth + 1):
            lunarDays = []
            if solarEclipsesEnabled:
                lunarDays.append(newMoonPhase)
            if lunarEclipsesEnabled:
                lunarDays.append(fullMoonPhase)

            for lunarDay in lunarDays:
                log.debug("---")

                lunarDate = LunarDate(lunarYear, lunarMonth, lunarDay)
                log.debug("lunarDate == {}".format(lunarDate))

                dt = LunarCalendarUtils.lunarDateToDatetime(lunarDate, tzInfo=timezone)
                log.debug("dt == {}".format(Ephemeris.datetimeToStrWithoutMicroseconds(dt)))

                jd = Ephemeris.datetimeToJulianDay(dt)
                sunPI = Ephemeris.getPlanetaryInfo("Sun", dt)
                moonPI = Ephemeris.getPlanetaryInfo("Moon", dt)
                trueNorthNodePI = Ephemeris.getPlanetaryInfo("TrueNorthNode", dt)
                trueSouthNodePI = Ephemeris.getPlanetaryInfo("TrueSouthNode", dt)

                sunLongitude = sunPI.geocentric['tropical']['longitude']
                moonLongitude = moonPI.geocentric['tropical']['longitude']
                moonLatitude = moonPI.geocentric['tropical']['latitude']
                trueNorthNodeLongitude = trueNorthNodePI.geocentric['tropical']['longitude']
                trueSouthNodeLongitude = trueSouthNodePI.geocentric['tropical']['longitude']

                log.debug("sunLongitude == {}".format(sunLongitude))
                log.debug("moonLongitude == {}".format(moonLongitude))
                log.debug("moonLatitude == {}".format(moonLatitude))
                log.debug("trueNorthNodeLongitude == {}".format(trueNorthNodeLongitude))
                log.debug("trueSouthNodeLongitude == {}".format(trueSouthNodeLongitude))

                sunTrueNorthNodeDiff = sunLongitude - trueNorthNodeLongitude
                log.debug("sunTrueNorthNodeDiff == {}".format(sunTrueNorthNodeDiff))

                distanceFromNode = None
                while sunTrueNorthNodeDiff > 90:
                    sunTrueNorthNodeDiff = sunTrueNorthNodeDiff - 180
                while sunTrueNorthNodeDiff <= -90:
                    sunTrueNorthNodeDiff = sunTrueNorthNodeDiff + 180
                distanceFromNode = abs(sunTrueNorthNodeDiff)

                log.debug("distanceFromNode == {}".format(distanceFromNode))

                eclipseTypeStr = None
                if lunarDay == newMoonPhase:
                    eclipseTypeStr = solarEclipseTypeStr

                    if (distanceFromNode <= longitudeThresholdForSolarEclipse):
                        log.debug("Within threshold for a solar eclipse: {}".\
                            format(lunarDate))

                        tup = (jd,
                               dt,
                               lunarDate,
                               sunLongitude,
                               moonLongitude,
                               moonLatitude,
                               trueNorthNodeLongitude,
                               trueSouthNodeLongitude,
                               eclipseTypeStr,
                               distanceFromNode)

                        eclipseTuples.append(tup)

                        numSolarEclipsesFound += 1

                elif lunarDay == fullMoonPhase:
                    eclipseTypeStr = lunarEclipseTypeStr

                    if (distanceFromNode <= longitudeThresholdForLunarEclipse):
                        log.debug("Within threshold for a lunar eclipse: {}".\
                            format(lunarDate))

                        tup = (jd,
                               dt,
                               lunarDate,
                               sunLongitude,
                               moonLongitude,
                               moonLatitude,
                               trueNorthNodeLongitude,
                               trueSouthNodeLongitude,
                               eclipseTypeStr,
                               distanceFromNode)

                        eclipseTuples.append(tup)

                        numLunarEclipsesFound += 1

    if solarEclipsesEnabled:
        log.info("Found {} solar eclipses.".format(numSolarEclipsesFound))

    if lunarEclipsesEnabled:
        log.info("Found {} lunar eclipses.".format(numLunarEclipsesFound))

    # Sort the eclipse tuples by timestamp.
    eclipseTuples = sorted(eclipseTuples, key=lambda tup: tup[0])

    # Print out results.
    headerLine = \
        "PlanetName," + \
        "JulianDay," + \
        "Datetime," + \
        "LunarDate," + \
        "G.Sun longitude," + \
        "G.Moon longitude," + \
        "G.Moon latitude," + \
        "G.TrueNorthNode longitude," + \
        "G.TrueSouthNode longitude," + \
        "EclipseType," + \
        "DistanceFromNode longitude,"
    
    # Remove trailing comma.
    headerLine = headerLine[:-1]

    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)

    for tup in eclipseTuples:
        i = 0

        jd = tup[i]
        i += 1
        dt = tup[i]
        i += 1
        lunarDate = tup[i]
        i += 1
        sunLongitude = tup[i]
        i += 1
        moonLongitude = tup[i]
        i += 1
        moonLatitude = tup[i]
        i += 1
        trueNorthNodeLongitude = tup[i]
        i += 1
        trueSouthNodeLongitude = tup[i]
        i += 1
        eclipseTypeStr = tup[i]
        i += 1
        distanceFromNodeLongitude = tup[i]
        i += 1

        planetName = ""
        if eclipseTypeStr == solarEclipseTypeStr:
            planetName = "Solar Eclipse"
        elif eclipseTypeStr == lunarEclipseTypeStr:
            planetName = "Lunar Eclipse"

        dtStr = Ephemeris.datetimeToStrWithoutMicroseconds(dt)
        lunarDateStr = \
            "LD(" + lunarDate.toConciseStringWithoutCommas() + ")"

        line = \
            "{},".format(planetName) + \
            "{},".format(jd) + \
            "{},".format(dtStr) + \
            "{},".format(lunarDateStr) + \
            "{},".format(sunLongitude) + \
            "{},".format(moonLongitude) + \
            "{},".format(moonLatitude) + \
            "{},".format(trueNorthNodeLongitude) + \
            "{},".format(trueSouthNodeLongitude) + \
            "{},".format(eclipseTypeStr) + \
            "{},".format(distanceFromNodeLongitude)

        # Remove trailing comma.
        line = line[:-1]

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
