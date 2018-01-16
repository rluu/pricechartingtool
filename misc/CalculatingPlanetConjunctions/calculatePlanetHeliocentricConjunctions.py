#!/usr/bin/env python3
##############################################################################
# Description:
#
# This script calculates the timestamp and longitude location of
# conjunctions of heliocentric planets.  The timestamp and planet
# longitude at this moment in time is saved and later written to
# output text CSV file.
#
# The output filename can be modified by changing the setting of the
# 'outputFilename' global variable in the code below.
# 
# 
# Usage:
#
#   1) Run the script:
#
#           python3 calculatePlanetHeliocentricConjunctions.py
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
from lunar_calendar_utils import LunarDate
from lunar_calendar_utils import LunarCalendarUtils
from data_objects import *
from cache import Cache

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Location information to use with the Ephemeris.
#locationName = "New York City"
#locationLongitude = -74.0064
#locationLatitude = 40.7142

locationName = "AlexandriaVirginiaApartment"
locationLongitude = -77.0677
locationLatitude = 38.8012

locationElevation = 0

# Timezone information to use with the Ephemeris.
#timezone = pytz.timezone("US/Eastern")
timezone = pytz.utc

# Time of the day to use to whem getting ephemeris measurements.
hourOfDay = 12
minuteOfHour = 0


startDt = datetime.datetime(year=1906, month=1, day=1,
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
outputFilename = thisScriptDir + os.sep + "planetHeliocentricConjunctions.csv"

# Planet names to do calculations for.
heliocentricPlanetNames = [\
    #"Moon",
    "Mercury",
    "Venus",
    #"Sun",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    #"Pluto",
    #"TrueNorthNode",
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

    # Angle that we want to obtain for the aspect.
    desiredAspectDegree = 0
    
    numPlanets = len(heliocentricPlanetNames)

    for i in range(numPlanets):
        for j in range(numPlanets):
            if i >= j:
                continue
            else:
                planetName1 = heliocentricPlanetNames[i]
                planetName2 = heliocentricPlanetNames[j]

                comboPlanetName = planetName1 + "/" + planetName2
                log.info("Obtaining planet heliocentric " + \
                        "aspect-of-{}-degrees ".\
                        format(desiredAspectDegree) + \
                         "information for '{}' ...".\
                         format(comboPlanetName))

                # Get list of conjunction timestamps.
                conjunctionTimestamps = \
                    EphemerisUtils.getLongitudeAspectTimestamps(\
                    startDt, endDt,
                    [(planetName1, "heliocentric", "tropical")],
                    [(planetName2, "heliocentric", "tropical")],
                    desiredAspectDegree,
                    True,
                    datetime.timedelta(seconds=1))

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
                           pi1.heliocentric["tropical"]["longitude"],
                           pi2.heliocentric["tropical"]["longitude"],
                           pi1.heliocentric["tropical"]["longitude_speed"],
                           pi2.heliocentric["tropical"]["longitude_speed"],
                           pi1.heliocentric["sidereal"]["longitude"],
                           pi2.heliocentric["sidereal"]["longitude"],
                           pi1.heliocentric["sidereal"]["longitude_speed"],
                           pi2.heliocentric["sidereal"]["longitude_speed"])

                    resultList.append(tup)
                    
                results[comboPlanetName] = resultList
                
    # Print out results.
    headerLine = \
        "PlanetComboName," + \
        "JulianDay," + \
        "Datetime," + \
        "LunarDate," + \
        "AspectAngle," + \
        "Planet1_HelioTropLongitude," + \
        "Planet2_HelioTropLongitude," + \
        "Planet1_HelioTropLongitude," + \
        "Planet2_HelioTropLongitude," + \
        "Planet1_HelioTropLongitudeSpeed," + \
        "Planet2_HelioTropLongitudeSpeed," + \
        "Planet1_HelioSidLongitude," + \
        "Planet2_HelioSidLongitude," + \
        "Planet1_HelioSidLongitude," + \
        "Planet2_HelioSidLongitude," + \
        "Planet1_HelioSidLongitudeSpeed," + \
        "Planet2_HelioSidLongitudeSpeed,"
    
    # Remove trailing comma.
    headerLine = headerLine[:-1]

    
    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)
    
    numPlanets = len(heliocentricPlanetNames)
    
    for i in range(numPlanets):
        for j in range(numPlanets):
            if i >= j:
                continue
            else:
                planetName1 = heliocentricPlanetNames[i]
                planetName2 = heliocentricPlanetNames[j]

                if planetName1 != "Venus" and planetName2 != "Venus":
                    continue

                comboPlanetName = planetName1 + "/" + planetName2

                for tup in results[comboPlanetName]:
                    
                    planetComboName = tup[0]
                    jd = tup[1]
                    dt = tup[2]
                    ld = LunarCalendarUtils.datetimeToLunarDate(dt)
                    aspectAngle = tup[3]
                    planet1HelioTropLongitudeDegrees = tup[4]
                    planet2HelioTropLongitudeDegrees = tup[5]
                    planet1HelioTropLongitudeSpeed = tup[6]
                    planet2HelioTropLongitudeSpeed = tup[7]
                    planet1HelioSidLongitudeDegrees = tup[8]
                    planet2HelioSidLongitudeDegrees = tup[9]
                    planet1HelioSidLongitudeSpeed = tup[10]
                    planet2HelioSidLongitudeSpeed = tup[11]
                    
                    dtStr = Ephemeris.datetimeToStrWithoutMicroseconds(dt)
                    lunarDateStr = \
                        "LD(" + ld.toConciseStringWithoutCommas() + ")"
                        
                    # Assemble the line that will go into the CSV file.
                    line = ""
                    line += "{}".format(planetComboName) + ","
                    line += "{}".format(jd) + ","
                    line += "{}".format(dtStr) + ","
                    line += "{}".format(lunarDateStr) + ","
                    line += "{}".format(aspectAngle) + ","
                    line += "{}".format(planet1HelioTropLongitudeDegrees) + ","
                    line += "{}".format(planet2HelioTropLongitudeDegrees) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet1HelioTropLongitudeDegrees)) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet2HelioTropLongitudeDegrees)) + ","
                    line += "{}".format(planet1HelioTropLongitudeSpeed) + ","
                    line += "{}".format(planet2HelioTropLongitudeSpeed) + ","
                    line += "{}".format(planet1HelioSidLongitudeDegrees) + ","
                    line += "{}".format(planet2HelioSidLongitudeDegrees) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet1HelioSidLongitudeDegrees)) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiGlyph(\
                            planet2HelioSidLongitudeDegrees)) + ","
                    line += "{}".format(planet1HelioSidLongitudeSpeed) + ","
                    line += "{}".format(planet2HelioSidLongitudeSpeed) + ","
                    
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
