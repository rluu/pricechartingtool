#!/usr/bin/env python3
##############################################################################
# Description:
#
# 
# 
# Usage:
#
#   1) Run the script:
#
#           python3 
#
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
from util import Util
from ephemeris import PlanetaryInfo
from ephemeris import Ephemeris
from lunar_calendar_utils import LunarDate
from lunar_calendar_utils import LunarCalendarUtils
from data_objects import *
from cache import Cache

# For variables set to TTTA dates.
#from ttta_dates import *
#from dow_pivots import *
#from planetaryEvents import *

##############################################################################

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Location information to use with the Ephemeris.

loc1Name = "New York City"
loc1Longitude = -74.0064
loc1Latitude = 40.7142
loc1Elevation = 0
nycLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)

#loc1Name = "Sherman"
#loc1Longitude = -96.609
#loc1Latitude = 33.635
#loc1Elevation = 0
#shermanLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)
#
#loc1Name = "Texarkana"
#loc1Longitude = -94.048
#loc1Latitude = 33.045
#loc1Elevation = 0
#texarkanaLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)
#
#loc1Name = "Paris"
#loc1Longitude = 2.333
#loc1Latitude = 48.87
#loc1Elevation = 0
#parisLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)
#
#loc1Name = "Chicago"
#loc1Longitude = 87.65
#loc1Latitude = 41.85
#loc1Elevation = 0
#chicagoLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)



# Timezone information to use with the Ephemeris.
#timezone = pytz.timezone("US/Eastern")
#eastern = pytz.timezone("US/Eastern")
#central =pytz.timezone("US/Central")
#central =pytz.timezone("US/Central")
timezone = pytz.utc

#locTuple = shermanLoc
locTuple = nycLoc


#planetEpocDt = datetime.datetime(year=2004, month=12, day=4,
#                                hour=12, minute=0,
#                                tzinfo=timezone)


# Error threshold for calculating timestamps.
maxErrorTd = datetime.timedelta(seconds=1)

# BasePlanetName
basePlanetName = "Earth"
basePlanetCentricityType = "heliocentric"
basePlanetLongitudeType = "tropical"

# Planet names to do calculations for.
geocentricPlanetNames = [\
    #"H1",
    #"H2",
    #"H3",
    #"H4",
    #"H5",
    #"H6",
    #"H7",
    #"H8",
    #"H9",
    #"H10",
    #"H11",
    #"H12",
    "Moon",
    "MoSu",
    "Sun",
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
    #"Chiron",
    #"Isis"
    ]

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
    "Pluto",
    #"TrueNorthNode",
    #"Chiron",
    #"Isis",
    "AvgJuSa"
    ]

# Line separator.
endl = os.linesep

# Cache enabling.
cacheEnabled = True

# CSV output filename 
csvOutputEnabled = True
outputFilename = thisScriptDir + os.sep + "planetLocationAndDifferences.csv"

# For logging.
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logging.DEBUG)
#log.setLevel(logging.INFO)

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

def getPlanetsForDatetimeAndTimezone(dt):
    """Returns a map with the key as a str indicating the planet
    and the value as the PlanetaryInfo object.
    """

    longitudeType = "tropical"
    fieldName = "longitude"

    log.debug("------------------------------------")

    piMap = {}
    
    for planetName in geocentricPlanetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, dt)

        key = "G." + planetName
        piMap[key] = pi

    for planetName in heliocentricPlanetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, dt)

        key = "H." + planetName
        piMap[key] = pi

    return piMap


def convertPlanetaryInfoMapToListBySortedLongitude(piMap,
        basePlanetLongitude):

    piTupList = []
    for key, value in piMap.items():
        longitude = None
        pi = value
        if key.startswith("G."):
            longitude = pi.geocentric["tropical"]["longitude"]
        elif key.startswith("H."):
            longitude = pi.heliocentric["tropical"]["longitude"]
        elif key.startswith("T."):
            longitude = pi.topocentric["tropical"]["longitude"]

        if longitude is None:
            raise ValueError("longitude may not be None")

        tup = (key, longitude, pi)
        piTupList.append(tup)

    piTupListSorted = sorted(piTupList, key=lambda tup: Util.toNormalizedAngle(tup[1] - basePlanetLongitude))

    return piTupListSorted

##############################################################################

if __name__ == "__main__":
    if cacheEnabled:
        # Initialize the caches.
        Cache.loadCachesFromShelve()

    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    locName = locTuple[0]
    locLongitude = locTuple[1]
    locLatitude = locTuple[2]
    locElevation = locTuple[3]

    log.debug("locName: {}".format(locName))
    log.debug("locLongitude: {}".format(locLongitude))
    log.debug("locLatitude: {}".format(locLatitude))
    log.debug("locElevation: {}".format(locElevation))

    # Set the Location (required).
    Ephemeris.setGeographicPosition(locLongitude,
                                    locLatitude,
                                    locElevation)

    basePlanetPi = Ephemeris.getPlanetaryInfo(basePlanetName, planetEpocDt)
    basePlanetNameKey = ""
    basePlanetLongitude = None
    basePlanetDirectOrRetrograde = None

    if basePlanetCentricityType == "geocentric":
        basePlanetNameKey += "G." + basePlanetName
        basePlanetLongitude = basePlanetPi.geocentric[basePlanetLongitudeType]["longitude"]
        if basePlanetPi.geocentric[basePlanetLongitudeType]["longitude_speed"] >= 0:
            basePlanetDirectOrRetrograde = "D"
        else:
            basePlanetDirectOrRetrograde = "R"
            
    elif basePlanetCentricityType == "heliocentric":
        basePlanetNameKey += "H." + basePlanetName
        basePlanetLongitude = basePlanetPi.heliocentric[basePlanetLongitudeType]["longitude"]
        if basePlanetPi.heliocentric[basePlanetLongitudeType]["longitude_speed"] >= 0:
            basePlanetDirectOrRetrograde = "D"
        else:
            basePlanetDirectOrRetrograde = "R"
    elif basePlanetCentricityType == "topocentric":
        basePlanetNameKey += "T." + basePlanetName
        basePlanetLongitude = basePlanetPi.topocentric[basePlanetLongitudeType]["longitude"]
        if basePlanetPi.topocentric[basePlanetLongitudeType]["longitude_speed"] >= 0:
            basePlanetDirectOrRetrograde = "D"
        else:
            basePlanetDirectOrRetrograde = "R"
    else:
        raise ValueError("Unknown centricityType: " + basePlanetCentricityType)

    if basePlanetNameKey is None or basePlanetNameKey == "":
        raise ValueError("basePlanetNameKey may not be None or empty")
    if basePlanetLongitude is None:
        raise ValueError("basePlanetLongitude may not be None")
    if basePlanetDirectOrRetrograde is None:
        raise ValueError("basePlanetDirectOrRetrograde may not be None")

    log.debug("basePlanetNameKey: {}".format(basePlanetNameKey))
    log.debug("basePlanetLongitude: {}".format(basePlanetLongitude))
    log.debug("basePlanetDirectOrRetrograde: {}".format(basePlanetDirectOrRetrograde))

    jd = Ephemeris.datetimeToJulianDay(planetEpocDt)
    log.debug("jd: {}".format(jd))

    dtStr = Ephemeris.datetimeToStrWithoutMicroseconds(planetEpocDt)
    log.debug("dtStr: {}".format(dtStr))

    lunarDateStr = \
        "LD(" + \
        LunarCalendarUtils.datetimeToLunarDate(planetEpocDt)\
        .toConciseStringWithoutCommas() + \
        ")"
    log.debug("lunarDateStr: {}".format(lunarDateStr))

    piMap = getPlanetsForDatetimeAndTimezone(planetEpocDt)

    piTupListSorted = \
        convertPlanetaryInfoMapToListBySortedLongitude(piMap, basePlanetLongitude)

    headerLine = \
        "BasePlanetName," + \
        "BaseJulianDay," + \
        "BaseDatetime," + \
        "BaseLunarDate," + \
        "BasePlanetDirectOrRetrograde," + \
        "BasePlanetLongitude," + \
        "PlanetName," + \
        "PlanetDirectOrRetrograde," + \
        "PlanetLongitude," + \
        "Diff + (0 * 360)," + \
        "Diff + (1 * 360)," + \
        "Diff + (2 * 360)," + \
        "Diff + (3 * 360)," + \
        "Diff + (4 * 360)," + \
        "Diff + (5 * 360)," + \
        "Diff + (6 * 360)," + \
        "Diff + (7 * 360)," + \
        "Diff + (8 * 360)," + \
        "Diff + (9 * 360)," + \
        "Diff + (10 * 360),"
    
    # Remove trailing comma.
    headerLine = headerLine[:-1]

    
    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)
    
    for piTup in piTupListSorted:
        key = piTup[0]
        longitude = piTup[1]
        pi = piTup[2]

        diff = longitude - basePlanetLongitude
        if diff < 0:
            diff += 360

        directOrRetrograde = None
        if key.startswith("H."):
            directOrRetrograde = "D"
        elif key.startswith("G."):
            if pi.geocentric["tropical"]["longitude_speed"] >= 0:
                directOrRetrograde = "D"
            else:
                directOrRetrograde = "R"
        elif key.startswith("T."):
            if pi.topocentric["tropical"]["longitude_speed"] >= 0:
                directOrRetrograde = "D"
            else:
                directOrRetrograde = "R"

        log.debug("piTup[{} ({})]: Longitude is:{}, diff is: {}".\
                format(key, directOrRetrograde, longitude, diff))

        # Assemble the line that will go into the CSV file.
        line = ""
        line += "{}".format(basePlanetNameKey) + ","
        line += "{}".format(jd) + ","
        line += "{}".format(dtStr) + ","
        line += "{}".format(lunarDateStr) + ","
        line += "{}".format(basePlanetDirectOrRetrograde) + ","
        line += "{}".format(basePlanetLongitude) + ","
        line += "{}".format(key) + ","
        line += "{}".format(directOrRetrograde) + ","
        line += "{}".format(longitude) + ","
        for i in range(11):
            line += "{}".format(diff + (i * 360)) + ","

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
