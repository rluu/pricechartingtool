#!/usr/bin/env python3
##############################################################################
# Description:
#
# This script calculates the timestamp and longitude location of
# geocentric planets when they go retrograde and when they go direct.
# The timestamp and planet longitude at this moment in time is saved
# and later written to output text CSV file.
#
# The output filename can be modified by changing the setting of the
# 'outputFilename' global variable in the code below.
# 
# 
# Usage:
#
#   1) Run the script:
#
#           python3 calculatePlanetDirectAndRetrograde.py
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


#startDt = datetime.datetime(year=1890, month=1, day=1,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
startDt = datetime.datetime(year=1969, month=1, day=1,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)

#endDt   = datetime.datetime(year=1940, month=12, day=31,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
endDt   = datetime.datetime(year=2016, month=12, day=31,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)

# Step size used when incrementing through all the timestamps between
# startDt and endDt.
stepSizeTd = datetime.timedelta(days=5)

# Error threshold for calculating timestamps of retrograde and direct planets.
maxErrorTd = datetime.timedelta(minutes=1)

# Strings used to indicate Retrograde and Direct.
retrogradeStr = "R"
directStr = "D"

# Destination output CSV file.
outputFilename = "/home/rluu/programming/pricechartingtool/misc/CalculatingPlanetDirectAndRetrograde/planetDirectAndRetrograde.csv"

# Planet names to do calculations for.
geocentricPlanetNames = [\
    #"Sun",
    #"Moon",
    "Mercury",
    "Venus",
    #"Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    #"TrueNorthNode",
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

    
def getGeocentricPlanetDirectRetrogradeInfo(planetName):
    """
    Returns a list of tuples, each tuple containing:
    (planetName,
    julianDay,
    datetime,
    "R" or "D",
    geoTropLongitudeOfPlanet,
    geoSidLongitudeOfPlanet)
    """

    # Return value.
    rv = []

    prevDt = None
    currDt = copy.deepcopy(startDt)

    prevTropLongitudeSpeed = None
    currTropLongitudeSpeed = None

    currTropLongitude = None
    currSidLongitude = None
    
    while currDt <= endDt:
        dt = currDt

        pi = Ephemeris.getPlanetaryInfo(planetName, dt)
        
        log.debug("Just obtained planetaryInfo for planet '{}', timestamp: {}".\
                  format(planetName, Ephemeris.datetimeToStr(dt)))

        # Get the geocentric longitude and geocentric longitude speed.
        tropLongitudeSpeed = pi.geocentric['tropical']['longitude_speed']
        tropLongitude = pi.geocentric['tropical']['longitude']
        sidLongitude = pi.geocentric['sidereal']['longitude']

        # Store new current planet values.
        currTropLongitudeSpeed = tropLongitudeSpeed
        currTropLongitude = tropLongitude
        currSidLongitude = sidLongitude

        log.debug("prevTropLongitudeSpeed={}, currTropLongitudeSpeed={}".\
                  format(prevTropLongitudeSpeed, currTropLongitudeSpeed))
        
        # We need two data points to proceed.
        if prevTropLongitudeSpeed != None and \
               currTropLongitudeSpeed != None and \
               prevDt != None:
            
            # Check to see if we passed over 0 degrees.
            
            if prevTropLongitudeSpeed < 0.0 and currTropLongitudeSpeed >= 0.0:
                # Crossed over from negative to positive!
                log.debug("Crossed over from negative to positive!")

                # This is the upper-bound of the error timedelta.
                t1 = prevDt
                t2 = currDt
                currErrorTd = t2 - t1
                
                # Refine the timestamp until it is less than the
                # desired threshold.
                while currErrorTd > maxErrorTd:
                    log.debug("Refining between {} and {}".\
                              format(Ephemeris.datetimeToStr(t1),
                                     Ephemeris.datetimeToStr(t2)))
                    
                    # Check the timestamp between.
                    diffTd = t2 - t1
                    halfDiffTd = \
                        datetime.\
                        timedelta(days=(diffTd.days / 2.0),
                                  seconds=(diffTd.seconds / 2.0),
                                  microseconds=(diffTd.microseconds / 2.0))
                    testDt = t1 + halfDiffTd
                    
                    pi = Ephemeris.getPlanetaryInfo(planetName, testDt)
                    
                    testTropLongitudeSpeed = \
                        pi.geocentric['tropical']['longitude_speed']
                    testTropLongitude = pi.geocentric['tropical']['longitude']
                    testSidLongitude = pi.geocentric['sidereal']['longitude']

                    if testTropLongitudeSpeed >= 0.0:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        currDt = t2
                        currTropLongitudeSpeed = testTropLongitudeSpeed
                        currTropLongitude = testTropLongitude
                        currSidLongitude = testSidLongitude
                    else:
                        t1 = testDt

                    currErrorTd = t2 - t1
                        
                # Broke out of while loop, meaning we have a timestamp
                # within our threshold.
                # Create a tuple to add to our list.
                tup = (planetName,
                       Ephemeris.datetimeToJulianDay(currDt),
                       currDt,
                       directStr,
                       currTropLongitude,
                       currSidLongitude)

                # Append to the list.
                rv.append(tup)
                
            elif prevTropLongitudeSpeed > 0.0 and currTropLongitudeSpeed <= 0.0:
                # Crossed over from positive to negative!
                log.debug("Crossed over from positive to negative!")
                
                # This is the upper-bound of the error timedelta.
                t1 = prevDt
                t2 = currDt
                currErrorTd = t2 - t1
                
                # Refine the timestamp until it is less than the
                # desired threshold.
                while currErrorTd > maxErrorTd:
                    log.debug("Refining between {} and {}".\
                              format(Ephemeris.datetimeToStr(t1),
                                     Ephemeris.datetimeToStr(t2)))
                    
                    # Check the timestamp between.
                    diffTd = t2 - t1
                    halfDiffTd = \
                        datetime.\
                        timedelta(days=(diffTd.days / 2.0),
                                  seconds=(diffTd.seconds / 2.0),
                                  microseconds=(diffTd.microseconds / 2.0))
                    testDt = t1 + halfDiffTd
                    
                    pi = Ephemeris.getPlanetaryInfo(planetName, testDt)
                    
                    testTropLongitudeSpeed = \
                        pi.geocentric['tropical']['longitude_speed']
                    testTropLongitude = pi.geocentric['tropical']['longitude']
                    testSidLongitude = pi.geocentric['sidereal']['longitude']

                    if testTropLongitudeSpeed <= 0.0:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        currDt = t2
                        currTropLongitudeSpeed = testTropLongitudeSpeed
                        currTropLongitude = testTropLongitude
                        currSidLongitude = testSidLongitude
                    else:
                        t1 = testDt

                    currErrorTd = t2 - t1
                    
                # Broke out of while loop, meaning we have a timestamp
                # within our threshold.
                # Create a tuple to add to our list.
                tup = (planetName,
                       Ephemeris.datetimeToJulianDay(currDt),
                       currDt,
                       retrogradeStr,
                       currTropLongitude,
                       currSidLongitude)

                # Append to the list.
                rv.append(tup)
                
            
        # Increment currDt timestamp.
        prevDt = currDt
        currDt = currDt + stepSizeTd
        
        # Move the previous currTropLongitudeSpeed to prevTropLongitudeSpeed.
        prevTropLongitudeSpeed = currTropLongitudeSpeed
        currTropLongitudeSpeed = None
        currTropLongitude = None
        currSidLongitude = None

        log.debug("prevTropLongitudeSpeed={}, currTropLongitudeSpeed={}".\
                  format(prevTropLongitudeSpeed, currTropLongitudeSpeed))
        
    return rv


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
    
    for planetName in geocentricPlanetNames:
        log.info("Obtaining planet retrograde and direct information for " + \
                 "'{}' ...".format(planetName))
        results[planetName] = \
            getGeocentricPlanetDirectRetrogradeInfo(planetName)

    # Print out results.
    headerLine = \
        "Planet Name," + \
        "Julian Day," + \
        "Datetime," + \
        "Retrograde or Direct," + \
        "GeoTropLongitude," + \
        "GeoSidLongitude,"
    
    # Remove trailing comma.
    headerLine = headerLine[:-1]

    
    # Text in the output file.
    outputLines = []
    outputLines.append(headerLine)
    
    for planetName in geocentricPlanetNames:
        listOfTuplesForPlanet = results[planetName]
        for tup in listOfTuplesForPlanet:
            planetName = tup[0]
            jd = tup[1]
            dt = tup[2]
            retroOrDirect = tup[3]
            geoTropLongitudeOfPlanet = tup[4]
            geoSidLongitudeOfPlanet = tup[5]
            
            # Assemble the line that will go into the CSV file.
            line = ""
            line += "{}".format(planetName) + ","
            line += "{}".format(jd) + ","
            line += "{}".format(Ephemeris.datetimeToStr(dt)) + ","
            line += "{}".format(retroOrDirect) + ","
            line += "{}".format(geoTropLongitudeOfPlanet) + ","
            line += "{}".format(geoSidLongitudeOfPlanet) + ","
            
            # Remove last trailing comma.
            line = line[:-1]
    
            # Append to the output lines.
            outputLines.append(line)
    
    
    # Write outputLines to output file.
    with open(outputFilename, "w") as f:
        log.info("Writing to output file '{}' ...".format(outputFilename))
    
        endl = "\r\n"
    
        for line in outputLines:
            f.write(line + endl)
    
    log.info("Done.")
    shutdown(0)

##############################################################################
