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
from astrologychart import AstrologyUtils
from ephemeris import Ephemeris
from ephemeris_utils import EphemerisUtils
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
timezone = pytz.timezone("US/Eastern")

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
maxErrorTd = datetime.timedelta(minutes=1)

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

def getNisan1DatesStandard():
    """
    Returns a list of the datetimes of the Nisan 1 dates, according to the
    standard method of calculating, astronomically.

    Nisan 1 is the first new moon before the G.Sun crosses the spring
    equinox.
    """
    getNisan1DatesRelativeToBeforeSpringEquinox()

def getNisan1DatesRelativeToBeforeSpringEquinox():
    """
    Returns a list of the datetimes of the Nisan 1 dates, according to the
    standard method of calculating, astronomically.

    Nisan 1 is the first new moon before the G.Sun crosses the spring
    equinox.
    """

    resultDts = []

    dts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            startDt,
            endDt,
            "geocentric",
            "tropical",
            "Sun",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

    if log.isDebugEnabled():
        log.debug("Got the following timestamps for G.Sun crossing 0 degrees: ")
        for dt in dts:
            log.debug("  " + Ephemeris.datetimeToDayStr(dt))

    for dt in dts:
        newMoonSearchStartDt = dt - datetime.timedelta(days=30)
        newMoonSearchEndDt = dt
        log.debug("Searching for new moons between " +
                Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                Ephemeris.datetimeToStr(newMoonSearchEndDt))
        newMoonsDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            newMoonSearchStartDt,
            newMoonSearchEndDt,
            "geocentric",
            "tropical",
            "MoSu",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

        if log.isDebugEnabled():
            log.debug("Got the following timestamps for G.MoSu crossing "
                + "0 degrees between the given start and end timestamps for "
                + "this year: ")
            for newMoonsDt in newMoonsDts:
                log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

        if len(newMoonDts) == 0:
            log.error("Did not find any new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        elif len(newMoonDts) > 2:
            log.error("Found too many new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        else:
            # Append the latest timestamp.
            newMoonDt = newMoonDts[-1]
            resultDts.append(newMoonDt)

    return resultDts

def getNisan1DatesRelativeToAfterSpringEquinox():
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
            "geocentric",
            "tropical",
            "Sun",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

    if log.isDebugEnabled():
        log.debug("Got the following timestamps for G.Sun crossing 0 degrees: ")
        for dt in dts:
            log.debug("  " + Ephemeris.datetimeToDayStr(dt))

    for dt in dts:
        newMoonSearchStartDt = dt
        newMoonSearchEndDt = dt + datetime.timedelta(days=30)
        log.debug("Searching for new moons between " +
                Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                Ephemeris.datetimeToStr(newMoonSearchEndDt))
        newMoonsDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            newMoonSearchStartDt,
            newMoonSearchEndDt,
            "geocentric",
            "tropical",
            "MoSu",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

        if log.isDebugEnabled():
            log.debug("Got the following timestamps for G.MoSu crossing "
                + "0 degrees between the given start and end timestamps for "
                + "this year: ")
            for newMoonsDt in newMoonsDts:
                log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

        if len(newMoonDts) == 0:
            log.error("Did not find any new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        elif len(newMoonDts) > 2:
            log.error("Found too many new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        else:
            # Append the earliest timestamp.
            newMoonDt = newMoonDts[0]
            resultDts.append(newMoonDt)

    return resultDts

def getNisan1DatesRelativeToBeforeTrueNorthNode():
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
            "geocentric",
            "tropical",
            "SunTrueNorthNode",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

    if log.isDebugEnabled():
        log.debug("Got the following timestamps for G.SunTrueNorthNode crossing 0 degrees: ")
        for dt in dts:
            log.debug("  " + Ephemeris.datetimeToDayStr(dt))

    for dt in dts:
        newMoonSearchStartDt = dt - datetime.timedelta(days=30)
        newMoonSearchEndDt = dt
        log.debug("Searching for new moons between " +
                Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                Ephemeris.datetimeToStr(newMoonSearchEndDt))
        newMoonsDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            newMoonSearchStartDt,
            newMoonSearchEndDt,
            "geocentric",
            "tropical",
            "MoSu",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

        if log.isDebugEnabled():
            log.debug("Got the following timestamps for G.MoSu crossing "
                + "0 degrees between the given start and end timestamps for "
                + "this year: ")
            for newMoonsDt in newMoonsDts:
                log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

        if len(newMoonDts) == 0:
            log.error("Did not find any new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        elif len(newMoonDts) > 2:
            log.error("Found too many new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        else:
            # Append the latest timestamp.
            newMoonDt = newMoonDts[-1]
            resultDts.append(newMoonDt)

    return resultDts

def getNisan1DatesRelativeToAfterTrueNorthNode():
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
            "geocentric",
            "tropical",
            "SunTrueNorthNode",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

    if log.isDebugEnabled():
        log.debug("Got the following timestamps for G.SunTrueNorthNode crossing 0 degrees: ")
        for dt in dts:
            log.debug("  " + Ephemeris.datetimeToDayStr(dt))

    for dt in dts:
        newMoonSearchStartDt = dt
        newMoonSearchEndDt = dt + datetime.timedelta(days=30)
        log.debug("Searching for new moons between " +
                Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                Ephemeris.datetimeToStr(newMoonSearchEndDt))
        newMoonsDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
            newMoonSearchStartDt,
            newMoonSearchEndDt,
            "geocentric",
            "tropical",
            "MoSu",
            0,
            maxErrorTd=datetime.timedelta(seconds=1))

        if log.isDebugEnabled():
            log.debug("Got the following timestamps for G.MoSu crossing "
                + "0 degrees between the given start and end timestamps for "
                + "this year: ")
            for newMoonsDt in newMoonsDts:
                log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

        if len(newMoonDts) == 0:
            log.error("Did not find any new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        elif len(newMoonDts) > 2:
            log.error("Found too many new moons in the time period specified: " +
                "newMoonSearchStartDt=" + newMoonSearchStartDt,
                ", newMoonSearchEndDt="+ newMoonSearchEndDt)
        else:
            # Append the earliest timestamp.
            newMoonDt = newMoonDts[0]
            resultDts.append(newMoonDt)

    return resultDts


##############################################################################

if __name__ == "__main__":
    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    # Set the Location (required).
    Ephemeris.setGeographicPosition(locationLongitude,
                                    locationLatitude,
                                    locationElevation)

    # Dictionary of results computed.
    results = {}

    # Angle that we want to obtain for the aspect.
    desiredAspectDegree = 0
    
    numPlanets = len(geocentricPlanetNames)

    for i in range(numPlanets):
        for j in range(numPlanets):
            if i >= j:
                continue
            else:
                planetName1 = geocentricPlanetNames[i]
                planetName2 = geocentricPlanetNames[j]

                comboPlanetName = planetName1 + "/" + planetName2
                log.info("Obtaining planet geocentric conjunction " + \
                         "information for '{}' ...".\
                         format(comboPlanetName))

                # Get list of conjunction timestamps.
                conjunctionTimestamps = \
                    EphemerisUtils.getLongitudeAspectTimestamps(\
                    startDt, endDt,
                    [(planetName1, "geocentric", "tropical")],
                    [(planetName2, "geocentric", "tropical")],
                    desiredAspectDegree,
                    True,
                    datetime.timedelta(seconds=30))

                # List of results.  Each item in this list is a tuple
                # containing:
                # - planetComboName
                # - julianDay
                # - datetime
                # - degreeDifference
                # - planetName1TropicalLongitude_Degrees
                # - planetName2TropicalLongitude_Degrees
                # - planetName1TropicalLongitude_ZodiacSignFormat
                # - planetName2TropicalLongitude_ZodiacSignFormat
                # - planetName1TropicalLongitudeLongitudeSpeed
                # - planetName2TropicalLongitudeLongitudeSpeed
                # - planetName1SiderealLongitude_Degrees
                # - planetName2SiderealLongitude_Degrees
                # - planetName1SiderealLongitude_ZodiacSignFormat
                # - planetName2SiderealLongitude_ZodiacSignFormat
                # - planetName1SiderealLongitudeLongitudeSpeed
                # - planetName2SiderealLongitudeLongitudeSpeed
                resultList = []

                # Create a tuple for each timestamp that was found
                # that was a conjunction.
                for dt in conjunctionTimestamps:
                    pi1 = Ephemeris.getPlanetaryInfo(planetName1, dt)
                    pi2 = Ephemeris.getPlanetaryInfo(planetName2, dt)
                    
                    tup = (comboPlanetName,
                           Ephemeris.datetimeToJulianDay(dt),
                           dt,
                           desiredAspectDegree,
                           pi1.geocentric["tropical"]["longitude"],
                           pi2.geocentric["tropical"]["longitude"],
                           pi1.geocentric["tropical"]["longitude_speed"],
                           pi2.geocentric["tropical"]["longitude_speed"],
                           pi1.geocentric["sidereal"]["longitude"],
                           pi2.geocentric["sidereal"]["longitude"],
                           pi1.geocentric["sidereal"]["longitude_speed"],
                           pi2.geocentric["sidereal"]["longitude_speed"])

                    resultList.append(tup)
                    
                results[comboPlanetName] = resultList
                
    # Print out results.
    headerLine = \
        "PlanetComboName," + \
        "JulianDay," + \
        "Datetime," + \
        "AspectAngle," + \
        "Planet1_GeoTropLongitude," + \
        "Planet2_GeoTropLongitude," + \
        "Planet1_GeoTropLongitude," + \
        "Planet2_GeoTropLongitude," + \
        "Planet1_GeoTropLongitudeSpeed," + \
        "Planet2_GeoTropLongitudeSpeed," + \
        "Planet1_GeoSidLongitude," + \
        "Planet2_GeoSidLongitude," + \
        "Planet1_GeoSidLongitude," + \
        "Planet2_GeoSidLongitude," + \
        "Planet1_GeoSidLongitudeSpeed," + \
        "Planet2_GeoSidLongitudeSpeed,"
    
    # Remove trailing comma.
    headerLine = headerLine[:-1]

    
    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)
    
    numPlanets = len(geocentricPlanetNames)
    
    for i in range(numPlanets):
        for j in range(numPlanets):
            if i >= j:
                continue
            else:
                planetName1 = geocentricPlanetNames[i]
                planetName2 = geocentricPlanetNames[j]
                
                comboPlanetName = planetName1 + "/" + planetName2

                for tup in results[comboPlanetName]:
                    
                    planetComboName = tup[0]
                    jd = tup[1]
                    dt = tup[2]
                    aspectAngle = tup[3]
                    planet1GeoTropLongitudeDegrees = tup[4]
                    planet2GeoTropLongitudeDegrees = tup[5]
                    planet1GeoTropLongitudeSpeed = tup[6]
                    planet2GeoTropLongitudeSpeed = tup[7]
                    planet1GeoSidLongitudeDegrees = tup[8]
                    planet2GeoSidLongitudeDegrees = tup[9]
                    planet1GeoSidLongitudeSpeed = tup[10]
                    planet2GeoSidLongitudeSpeed = tup[11]
                    
                    # Assemble the line that will go into the CSV file.
                    line = ""
                    line += "{}".format(planetComboName) + ","
                    line += "{}".format(jd) + ","
                    line += "{}".format(Ephemeris.datetimeToStr(dt)) + ","
                    line += "{}".format(aspectAngle) + ","
                    line += "{}".format(planet1GeoTropLongitudeDegrees) + ","
                    line += "{}".format(planet2GeoTropLongitudeDegrees) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet1GeoTropLongitudeDegrees)) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet2GeoTropLongitudeDegrees)) + ","
                    line += "{}".format(planet1GeoTropLongitudeSpeed) + ","
                    line += "{}".format(planet2GeoTropLongitudeSpeed) + ","
                    line += "{}".format(planet1GeoSidLongitudeDegrees) + ","
                    line += "{}".format(planet2GeoSidLongitudeDegrees) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet1GeoSidLongitudeDegrees)) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet2GeoSidLongitudeDegrees)) + ","
                    line += "{}".format(planet1GeoSidLongitudeSpeed) + ","
                    line += "{}".format(planet2GeoSidLongitudeSpeed) + ","
                    
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
