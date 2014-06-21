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
from astrologychart import AstrologyUtils
from ephemeris import Ephemeris
from data_objects import *


# For variables set to TTTA dates.
from ttta_dates import *

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
eastern = pytz.timezone("US/Eastern")

# Time of the day to use to whem getting ephemeris measurements.
#hourOfDay = 12
#minuteOfHour = 0


#startDt
tz1 = pytz.timezone("US/Eastern")
#dt1 = datetime.datetime(year=1930, month=5, day=15,
#                        hour=12, minute=0,
#                        tzinfo=tz1)
dt1 = wallStreet69
loc1Name = "New York City"
loc1Longitude = -74.0064
loc1Latitude = 40.7142
loc1Elevation = 0

#endDt
tz2 = pytz.timezone("US/Eastern")
dt2 = datetime.datetime(year=1928, month=6, day=15,
                        hour=12, minute=0,
                        tzinfo=tz2)
#dt2 = 
loc2Name = "New York City"
loc2Longitude = -74.0064
loc2Latitude = 40.7142
loc2Elevation = 0


# Step size used when incrementing through all the timestamps between
# startDt and endDt.
stepSizeTd = datetime.timedelta(days=1)

# Error threshold for calculating timestamps.
maxErrorTd = datetime.timedelta(minutes=1)

# Destination output CSV file.
outputFilename = "/home/rluu/programming/pricechartingtool/misc/CalculatingPlanetConjunctions/planetGeocentricConjunctions.csv"

# Planet names to do calculations for.
geocentricPlanetNames = [\
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
    #"Neptune",
    #"Pluto",
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
    #"Neptune",
    #"Pluto",
    #"TrueNorthNode",
    #"Chiron",
    #"Isis"
    ]

# Line separator.
endl = os.linesep

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


def getPlanetsForDatetimeAndTimezone(dt, locName, locLongitude, locLatitude, locElevation):
    """Returns a string with the planet longitude position for the given
    datetime and timezone.
    """

    # Set the Location (required).
    Ephemeris.setGeographicPosition(locLongitude,
                                    locLatitude,
                                    locElevation)

    longitudeType = "tropical"
    fieldName = "longitude"

    rv = "For datetime: " + Ephemeris.datetimeToDayStr(dt) + \
         ", location: " + locName + endl

    
    for planetName in geocentricPlanetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, dt)

        rv += "  {: <14}".format("G." + planetName + ": ") + \
              "{:>.3f}".format(pi.geocentric[longitudeType][fieldName]) + \
              endl

    rv += endl
        
    for planetName in heliocentricPlanetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, dt)

        rv += "  {: <14}".format("H." + planetName + ": ") + \
              "{:>.3f}".format(pi.heliocentric[longitudeType][fieldName]) + \
              endl
        
    return rv


def getLongitudeDiffBetweenDatetimes(planetName,
                                     centricityType,
                                     dt1,
                                     loc1Longitude,
                                     loc1Latitude,
                                     loc1Elevation,
                                     dt2,
                                     loc2Longitude,
                                     loc2Latitude,
                                     loc2Elevation):

    startTimestamp = dt1
    endTimestamp = dt2

    # maxErrorTd - datetime.timedelta object holding the maximum
    #              time difference between the exact planetary
    #              timestamp for the phenomena, and the one
    #              calculated.  This would define the accuracy of
    #              the calculations.
    #
    maxErrorTd = datetime.timedelta(seconds=4)

    # Size of a circle, in degrees.
    #
    # Here we define our own value instead of using the value in
    # AstrologyUtils.degreesInCircle because it is possible we may
    # want to test different sizes of a 'circle'.
    circleSizeInDegrees = 360.0
        
    # All references to longitude_speed need to
    # be from tropical zodiac measurements!  If I use
    # sidereal zodiac measurements for getting the
    # longitude_speed, then the measurements from the
    # Swiss Ephemeris do not yield the correct values.
    # I use the following variable in these locations.
    zodiacTypeForLongitudeSpeed = "tropical"

    tropicalZodiacFlag = True

    # Text to set in the text item.
    text = ""

    # Total number of degrees elapsed.
    totalDegrees = 0
    
    Ephemeris.setGeographicPosition(loc1Longitude,
                                    loc1Latitude,
                                    loc1Elevation)
    
    # List of PlanetaryInfo objects for this particular
    # planet, sorted by timestamp.
    planetData = []
                
    # Step size to use in populating the data list with
    # PlanetaryInfos.
    #
    # The step size should cause the planet to move less
    # than 120 degrees in all cases, and idealy much less
    # than this, that way we can easily narrow down when
    # the planet passes the 0 degree or 360 degree
    # threshold, and also so it is easier to narrow down
    # when retrograde periods happen.  If the step size is
    # too large, it is possible that we would miss a whole
    # time window of retrograde movement, so discretion
    # has to be used in determining what to use for this value.
    #
    # Here we will set it to 1 day for the default case,
    # but if the planet name is a house cusp then shrink
    # the step size so we will get the correct resolution.
    # Also, if the planet name is an outer planet with a
    # large period, we can increase the step size slightly
    # to improve performance.
    stepSizeTd = datetime.timedelta(days=1)

    
    if Ephemeris.isHouseCuspPlanetName(planetName) or \
           Ephemeris.isAscmcPlanetName(planetName):
                    
        stepSizeTd = datetime.timedelta(hours=1)
                    
    elif planetName == "Jupiter" or \
         planetName == "Saturn" or \
         planetName == "Neptune" or \
         planetName == "Uranus" or \
         planetName == "Pluto":
                    
        stepSizeTd = datetime.timedelta(days=5)
                
        log.debug("Stepping through from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startTimestamp),
                         Ephemeris.datetimeToStr(endTimestamp)))
                
    # Current datetime as we step through all the
    # timestamps between the start and end timestamp.
    currDt = copy.deepcopy(startTimestamp)
                
    # Step through the timestamps, calculating the planet positions.
    while currDt < endTimestamp:
        p = Ephemeris.getPlanetaryInfo(planetName, currDt)
        planetData.append(p)
                    
        # Increment step size.
        currDt += stepSizeTd
                    
    # We must also append the planet calculation for the end timestamp.
    Ephemeris.setGeographicPosition(loc2Longitude,
                                    loc2Latitude,
                                    loc2Elevation)
    p = Ephemeris.getPlanetaryInfo(planetName, endTimestamp)
    planetData.append(p)
                
    # Geocentric measurement.
    if centricityType == "geocentric":
                    
        # Get the PlanetaryInfos for the timestamps of the
        # planet at the moment right after the
        # longitude_speed polarity changes.
        additionalPlanetaryInfos = []
                    
        prevLongitudeSpeed = None
                    
        for i in range(len(planetData)):
            currLongitudeSpeed = \
                planetData[i].geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']
                        
            if prevLongitudeSpeed != None and \
               ((prevLongitudeSpeed < 0 and currLongitudeSpeed >= 0) or \
               (prevLongitudeSpeed >= 0 and currLongitudeSpeed < 0)):
                            
                # Polarity changed.
                # Try to narrow down the exact moment in
                # time when this occured.
                t1 = planetData[i-1].dt
                t2 = planetData[i].dt
                currErrorTd = t2 - t1
                            
                while currErrorTd > maxErrorTd:
                    if log.isEnabledFor(logging.DEBUG) == True:
                        log.debug("Refining between {} and {}".\
                                       format(Ephemeris.datetimeToStr(t1),
                                              Ephemeris.datetimeToStr(t2)))
                                
                    # Check the timestamp between.
                    diffTd = t2 - t1
                    halfDiffTd = \
                        datetime.\
                        timedelta(days=(diffTd.days / 2.0),
                                  seconds=(diffTd.seconds / 2.0),
                                  microseconds=(diffTd.\
                                                microseconds / 2.0))
                    testDt = t1 + halfDiffTd

                    p = Ephemeris.getPlanetaryInfo(planetName, testDt)
                    testLongitudeSpeed = \
                        p.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']

                    if ((prevLongitudeSpeed < 0 and \
                         testLongitudeSpeed >= 0) or \
                        (prevLongitudeSpeed >= 0 and \
                         testLongitudeSpeed < 0)):

                        # Polarity change at the test timestamp.
                        t2 = testDt

                    else:
                        # No polarity change yet.
                        t1 = testDt

                    # Update the currErrorTd.
                    currErrorTd = t2 - t1
                            
                log.debug("Broke out of loop to find " + \
                               "velocity polarity change.  " + \
                               "currErrorTd is: {}, ".\
                               format(currErrorTd))
                                           
                # Timestamp at t2 is now within the amount
                # of the time error threshold ('maxErrorTd')
                # following the polarity change.
                # Append this value to the list.
                p = Ephemeris.getPlanetaryInfo(planetName, t2)
                additionalPlanetaryInfos.append(p)

                t1pi = planetData[i-1]
                t2pi = Ephemeris.getPlanetaryInfo(planetName, t2)
                            
                if log.isEnabledFor(logging.DEBUG) == True:
                    log.debug("t1 == {}, ".\
                               format(Ephemeris.datetimeToStr(t1pi.dt)) + \
                               "longitude(tropical) == {}, ".\
                               format(t1pi.geocentric['tropical']['longitude']) + \
                               "longitude(sidereal) == {}, ".\
                               format(t1pi.geocentric['sidereal']['longitude']) + \
                               "longitude_speed == {}, ".\
                               format(t1pi.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']))
                                
                    log.debug("t2 == {}, ".\
                               format(Ephemeris.datetimeToStr(t2pi.dt)) + \
                               "longitude(tropical) == {}, ".\
                               format(t2pi.geocentric['tropical']['longitude']) + \
                               "longitude(sidereal) == {}, ".\
                               format(t2pi.geocentric['sidereal']['longitude']) + \
                               "longitude_speed == {}, ".\
                               format(t2pi.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']))
                            
                # There is no need to update
                # currLongitudeSpeed here, because the
                # longitude_speed for 'p' should be the
                # same polarity.
                            
            # Update prevLongitudeSpeed.
            prevLongitudeSpeed = currLongitudeSpeed
                        
        # Sort all the extra PlanetaryInfo objects by timestamp.
        additionalPlanetaryInfos = \
            sorted(additionalPlanetaryInfos, key=lambda c: c.dt)
                    
        # Insert PlanetaryInfos from
        # 'additionalPlanetaryInfos' into 'planetData' at
        # the timestamp-ordered location.
        currLoc = 0
        for i in range(len(additionalPlanetaryInfos)):
            pi = additionalPlanetaryInfos[i]

            insertedFlag = False
                        
            while currLoc < len(planetData):
                if pi.dt < planetData[currLoc].dt:
                    planetData.insert(currLoc, pi)
                    insertedFlag = True
                    currLoc += 1
                    break
                else:
                    currLoc += 1
                        
            if insertedFlag == False:
                # PlanetaryInfo 'pi' has a timestamp that
                # is later than the last PlanetaryInfo in
                # 'planetData', so just append it.
                planetData.append(pi)

                # Increment currLoc so that the rest of
                # the PlanetaryInfos in
                # 'additionalPlanetaryInfos' can be
                # appended without doing anymore timestamp tests.
                currLoc += 1

        # Do summations to determine the measurements.
        showGeocentricRetroAsNegativeTextFlag = True
        if showGeocentricRetroAsNegativeTextFlag == True:
            if tropicalZodiacFlag == True:
                totalDegrees = 0
                zodiacType = "tropical"
                            
                for i in range(len(planetData)):
                    if i != 0:
                        prevPi = planetData[i-1]
                        currPi = planetData[i]

                        if prevPi.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                            # Direct motion.
                            # Elapsed amount for this segment should be positive.
                                        
                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.geocentric[zodiacType]['longitude'] - \
                                prevPi.geocentric[zodiacType]['longitude']
                                        
                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            longitudeElapsed = \
                                Util.toNormalizedAngle(longitudeElapsed)

                            totalDegrees += longitudeElapsed
                        else:
                            # Retrograde motion.
                            # Elapsed amount for this segment should be negative.
                            
                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.geocentric[zodiacType]['longitude'] - \
                                prevPi.geocentric[zodiacType]['longitude']

                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            if longitudeElapsed > 0:
                                longitudeElapsed -= 360

                            totalDegrees += longitudeElapsed
                                    
                # Line of text.  We append measurements to
                # this line of text depending on what
                # measurements are enabled.
                line = "G T {} moves ".format(planetName)

                numCircles = totalDegrees / circleSizeInDegrees
                numBiblicalCircles = \
                    totalDegrees / AstrologyUtils.degreesInBiblicalCircle
                            
                line += "{:.2f} deg ".format(totalDegrees)

                # Append last part of the line.
                line += "(r as -)"
                            
                text += line + os.linesep
                            
    if centricityType == "heliocentric":

        if tropicalZodiacFlag == True:
            totalDegrees = 0
            zodiacType = "tropical"
                        
            for i in range(len(planetData)):
                if i != 0:
                    prevPi = planetData[i-1]
                    currPi = planetData[i]
                                
                    if prevPi.heliocentric[zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                        # Direct motion.
                        # Elapsed amount for this segment should be positive.
                                    
                        # Find the amount of longitude elasped.
                        longitudeElapsed = \
                            currPi.heliocentric[zodiacType]['longitude'] - \
                            prevPi.heliocentric[zodiacType]['longitude']
                                    
                        # See if there was a crossing of the
                        # 0 degree point or the 360 degree point.
                        # If so, make the necessary adjustments
                        # so that the longitude elapsed is
                        # correct.
                        longitudeElapsed = \
                            Util.toNormalizedAngle(longitudeElapsed)
                                    
                        totalDegrees += longitudeElapsed
                    else:
                        # Retrograde motion.
                        # Elapsed amount for this segment should be negative.
                                    
                        # Find the amount of longitude elasped.
                        longitudeElapsed = \
                            currPi.heliocentric[zodiacType]['longitude'] - \
                            prevPi.heliocentric[zodiacType]['longitude']
                                    
                        # See if there was a crossing of the
                        # 0 degree point or the 360 degree point.
                        # If so, make the necessary adjustments
                        # so that the longitude elapsed is
                        # correct.
                        if longitudeElapsed > 0:
                            longitudeElapsed -= 360
                                        
                        totalDegrees += longitudeElapsed
                                    
            # Line of text.  We append measurements to
            # this line of text depending on what
            # measurements are enabled.
            line = "H T {} moves ".format(planetName)
                            
            numCircles = totalDegrees / circleSizeInDegrees
            numBiblicalCircles = \
                totalDegrees / AstrologyUtils.degreesInBiblicalCircle
            
            line += "{:.2f} deg ".format(totalDegrees)

            text += line + os.linesep
                        
    text = text.rstrip()
    
    return totalDegrees

    
def getPlanetDiffsForDatetimes(dt1,
                               loc1Name,
                               loc1Longitude,
                               loc1Latitude,
                               loc1Elevation,
                               dt2,
                               loc2Name,
                               loc2Longitude,
                               loc2Latitude,
                               loc2Elevation):
    """Returns a string with the planet longitude differences between the given
    datetimes and location.
    """

    longitudeType = "tropical"
    fieldName = "longitude"

    rv = "Between datetime: " + Ephemeris.datetimeToDayStr(dt1) + \
         ", location: " + loc1Name + " and " + endl
    rv += "        datetime: " + Ephemeris.datetimeToDayStr(dt2) + \
         ", location: " + loc2Name + endl


    calendarDayDiff = dt2 - dt1
    rv += "  Diff calendar days: {}".format(calendarDayDiff) + endl
    
    for planetName in geocentricPlanetNames:

        longitudeDiff = getLongitudeDiffBetweenDatetimes(planetName,
                                                         "geocentric",
                                                         dt1,
                                                         loc1Longitude,
                                                         loc1Latitude,
                                                         loc1Elevation,
                                                         dt2,
                                                         loc2Longitude,
                                                         loc2Latitude,
                                                         loc2Elevation)
        longitudeDiffFullRevs = int(longitudeDiff // 360)
        longitudeDiffMod360 = longitudeDiff % 360
        
        rv += "  {: <16}".format("Diff G." + planetName + ": ") + \
              "{:>10.3f}".format(longitudeDiff) + \
              "    or  {:>4} rev + {:>7.3f} deg".format(longitudeDiffFullRevs,
                                                        longitudeDiffMod360) + \
              endl

    rv += endl
        
    for planetName in heliocentricPlanetNames:

        longitudeDiff = getLongitudeDiffBetweenDatetimes(planetName,
                                                         "heliocentric",
                                                         dt1,
                                                         loc1Longitude,
                                                         loc1Latitude,
                                                         loc1Elevation,
                                                         dt2,
                                                         loc2Longitude,
                                                         loc2Latitude,
                                                         loc2Elevation)
        longitudeDiffFullRevs = int(longitudeDiff // 360)
        longitudeDiffMod360 = longitudeDiff % 360
        
        rv += "  {: <16}".format("Diff H." + planetName + ": ") + \
              "{:>10.3f}".format(longitudeDiff) + \
              "    or  {:>4} rev + {:>7.3f} deg".format(longitudeDiffFullRevs,
                                                        longitudeDiffMod360) + \
              endl
        
    return rv




##############################################################################

if __name__ == "__main__":
    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    printDt1 = True
    #printDt1 = False
    
    printDt2 = True
    #printDt2 = False
    
    printDiff = True
    #printDiff = False

    if printDt1 == True:
        outputStr = getPlanetsForDatetimeAndTimezone(dt1,
                                                     loc1Name,
                                                     loc1Longitude,
                                                     loc1Latitude,
                                                     loc1Elevation)
        print(outputStr)


    if printDt2 == True:
        outputStr = getPlanetsForDatetimeAndTimezone(dt2,
                                                     loc2Name,
                                                     loc2Longitude,
                                                     loc2Latitude,
                                                     loc2Elevation)
        print(outputStr)


    if printDiff == True:
        outputStr = getPlanetDiffsForDatetimes(dt1,
                                               loc1Name,
                                               loc1Longitude,
                                               loc1Latitude,
                                               loc1Elevation,
                                               dt2,
                                               loc2Name,
                                               loc2Longitude,
                                               loc2Latitude,
                                               loc2Elevation)
        print(outputStr)


    #log.info("Done.")
    shutdown(0)

##############################################################################
