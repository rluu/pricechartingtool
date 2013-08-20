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
outputFilename = "/home/rluu/programming/pricechartingtool/misc/CalculatingPlanetConjunctions/planetHeliocentricConjunctions.csv"

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


def getLongitudeAspectTimestamps(\
    startDt, endDt,
    planet1ParamsList,
    planet2ParamsList,
    degreeDifference,
    uniDirectionalAspectsFlag=False,
    maxErrorTd=datetime.timedelta(minutes=1)):
    """Obtains a list of datetime.datetime objects that contain
    the moments when the aspect specified is active.
        
    Warning on usage:
    When planet-longitude-averaging is utilized for the longitude
    of planet1 or planet2, the aspects returned by this function
    cannot be fully relied upon.
        
    This short-coming happens under these circumstances because it
    is possible that the longitude can abruptly 'jump' or hop a
    large distance when measurements are taken between timestamp
    steps.

    For example, this 'jumping' effect can occur if two planets A
    and B, are both around 355 degrees, and planet A crosses the 0
    degree mark.  Now the average goes from around 355 degrees
    (355 + 355 = 710 / 2 = 355), to about 180 degrees (355 + 0 =
    355 / 2 = about 180).

    While corrections for this can be made for the case of having
    only 2 planets involved, if more planets are involved then the
    adjustment required quickly becomes non-trivial.
        
    Arguments:
    startDt   - datetime.datetime object for the starting timestamp
                to do the calculations for artifacts.
    endDt     - datetime.datetime object for the ending timestamp
                to do the calculations for artifacts.

    planet1ParamsList - List of tuples that will be used as parameters
                  for planet1.  Each tuple contained in this list
                  represents parameters for each planet that will
                  get averaged to create what is known as planet1.

                  The contents of the tuple are:
                  (planetName, centricityType, longitudeType)

                  Where:
                  planetName - str holding the name of the second
                               planet to do the calculations for.
                  centricityType - str value holding either "geocentric",
                                   "topocentric", or "heliocentric".
                  longitudeType - str value holding either
                                  "tropical" or "sidereal".
                      
                  Example: So if someone wanted planet1 to be the
                  average location of of geocentric sidereal
                  Saturn and geocentric sidereal Uranus, the
                  'planet1ParamsList' parameter would be:

                  [("Saturn", "geocentric", "sidereal"),
                   ("Uranus", "geocentric", "sidereal")]

                  If the typical use-case is desired for the
                  longitude of just a single planet, pass a list
                  with only 1 tuple.  As an example, for Mercury
                  it would be:

                  [("Mercury", "heliocentric", "tropical")]
        
    planet2ParamsList - List of tuples that will be used as parameters
                  for planet2.  For additional details about the
                  format of this parameter field, please see the
                  description for parameter 'planet1ParamsList'
                      
    degreeDifference - float value for the number of degrees of
                       separation for this aspect.
                           
    uniDirectionalAspectsFlag - bool value for whether or not
                 uni-directional aspects are enabled or not.  By
                 default, aspects are bi-directional, so Saturn
                 square-aspect Jupiter would be the same as
                 Jupiter square-aspect Saturn.  If this flag is
                 set to True, then those two combinations would be
                 considered unique.  In the case where the flag is
                 set to True, for the aspect to be active,
                 planet2 would need to be 'degreeDifference'
                 degrees in front of planet1.
        
    maxErrorTd - datetime.timedelta object holding the maximum
                 time difference between the exact planetary
                 combination timestamp, and the one calculated.
                 This would define the accuracy of the
                 calculations.  
        
    Returns:
        
    List of datetime.datetime objects.  Each timestamp in the list
    is the moment where the aspect is active and satisfies the
    given parameters.  In the event of an error, the reference
    None is returned.

    """

    log.debug("Entered " + inspect.stack()[0][3] + "()")

    # List of timestamps of the aspects found.
    aspectTimestamps = []
        
    # Make sure the inputs are valid.
    if endDt < startDt:
        log.error("Invalid input: 'endDt' must be after 'startDt'")
        return None

    # Check to make sure planet lists were given.
    if len(planet1ParamsList) == 0:
        log.error("planet1ParamsList must contain at least 1 tuple.")
        return None
    if len(planet2ParamsList) == 0:
        log.error("planet2ParamsList must contain at least 1 tuple.")
        return None

    log.debug("planet1ParamsList passed in is: {}".\
              format(planet1ParamsList))
    log.debug("planet2ParamsList passed in is: {}".\
              format(planet2ParamsList))
        
    # Check for valid inputs in each of the planet parameter lists.
    for planetTuple in planet1ParamsList + planet2ParamsList:
        if len(planetTuple) != 3:
            log.error("Input error: " + \
                      "Not enough values given in planet tuple.")
            return None

        planetName = planetTuple[0]
        centricityType = planetTuple[1]
        longitudeType = planetTuple[2]
            
        loweredCentricityType = centricityType.lower()
        if loweredCentricityType != "geocentric" and \
            loweredCentricityType != "topocentric" and \
            loweredCentricityType != "heliocentric":

            log.error("Invalid input: Centricity type is invalid.  " + \
                  "Value given was: {}".format(centricityType))
            return None

        # Check inputs for longitude type.
        loweredLongitudeType = longitudeType.lower()
        if loweredLongitudeType != "tropical" and \
            loweredLongitudeType != "sidereal":

            log.error("Invalid input: Longitude type is invalid.  " + \
                  "Value given was: {}".format(longitudeType))
            return None
            
    # Field name we are getting.
    fieldName = "longitude"
        
    # Initialize the Ephemeris with the birth location.
    log.debug("Setting ephemeris location ...")
    Ephemeris.setGeographicPosition(locationLongitude,
                                    locationLatitude,
                                    locationElevation)

    # Set the step size.
    stepSizeTd = datetime.timedelta(days=1)
    for planetTuple in planet1ParamsList + planet2ParamsList:
        planetName = planetTuple[0]
            
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
           Ephemeris.isAscmcPlanetName(planetName):
                
            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
        elif planetName == "Moon":
            # Use a smaller step size for the moon so we can catch
            # smaller aspect sizes.
            stepSizeTd = datetime.timedelta(hours=3)
        
    log.debug("Step size is: {}".format(stepSizeTd))
        
    # Desired angles.  We need to check for planets at these angles.
    desiredAngleDegList = []

    desiredAngleDeg1 = Util.toNormalizedAngle(degreeDifference)
    desiredAngleDegList.append(desiredAngleDeg1)
    if Util.fuzzyIsEqual(desiredAngleDeg1, 0):
        desiredAngleDegList.append(360)
        
    if uniDirectionalAspectsFlag == False:
        desiredAngleDeg2 = \
            360 - Util.toNormalizedAngle(degreeDifference)
        if desiredAngleDeg2 not in desiredAngleDegList:
            desiredAngleDegList.append(desiredAngleDeg2)

    # Debug output.
    anglesStr = ""
    for angle in desiredAngleDegList:
        anglesStr += "{} ".format(angle)
    log.debug("Angles in desiredAngleDegList: " + anglesStr)

    # Iterate through, appending to aspectTimestamps list as we go.
    steps = []
    steps.append(copy.deepcopy(startDt))
    steps.append(copy.deepcopy(startDt))

    longitudesP1 = []
    longitudesP1.append(None)
    longitudesP1.append(None)
        
    longitudesP2 = []
    longitudesP2.append(None)
    longitudesP2.append(None)

    def getFieldValue(dt, planetParamsList, fieldName):
        """Creates the PlanetaryInfo object for the given
        planetParamsList and returns the value of the field
        desired.
        """
        
        log.debug("planetParamsList passed in is: {}".\
                  format(planetParamsList))
        
        unAveragedFieldValues = []
            
        for t in planetParamsList:
            planetName = t[0]
            centricityType = t[1]
            longitudeType = t[2]
                
            pi = Ephemeris.getPlanetaryInfo(planetName, dt)

            fieldValue = None
                
            if centricityType.lower() == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type: {}".\
                          format(centricityType))
                fieldValue = None

            unAveragedFieldValues.append(fieldValue)

        log.debug("unAveragedFieldValues is: {}".\
                  format(unAveragedFieldValues))
        
        # Average the field values.
        total = 0.0
        for v in unAveragedFieldValues:
            total += v
        averagedFieldValue = total / len(unAveragedFieldValues)
        
        log.debug("averagedFieldValue is: {}".\
                  format(averagedFieldValue))
    
        return averagedFieldValue
            
    log.debug("Stepping through timestamps from {} to {} ...".\
              format(Ephemeris.datetimeToStr(startDt),
                     Ephemeris.datetimeToStr(endDt)))

    currDiff = None
    prevDiff = None
        

    while steps[-1] < endDt:
        currDt = steps[-1]
        prevDt = steps[-2]
            
        log.debug("Looking at currDt == {} ...".\
                  format(Ephemeris.datetimeToStr(currDt)))
            
        longitudesP1[-1] = \
            Util.toNormalizedAngle(\
            getFieldValue(currDt, planet1ParamsList, fieldName))
        longitudesP2[-1] = \
            Util.toNormalizedAngle(\
            getFieldValue(currDt, planet2ParamsList, fieldName))

        log.debug("{} {} is: {}".\
                  format(planet1ParamsList, fieldName,
                         longitudesP1[-1]))
        log.debug("{} {} is: {}".\
                  format(planet2ParamsList, fieldName,
                         longitudesP2[-1]))
        
        currDiff = Util.toNormalizedAngle(\
            longitudesP1[-1] - longitudesP2[-1])
        
        log.debug("prevDiff == {}".format(prevDiff))
        log.debug("currDiff == {}".format(currDiff))
        
        if prevDiff != None and \
               longitudesP1[-2] != None and \
               longitudesP2[-2] != None:
            
            if abs(prevDiff - currDiff) > 180:
                # Probably crossed over 0.  Adjust the prevDiff so
                # that the rest of the algorithm can continue to
                # work.
                if prevDiff > currDiff:
                    prevDiff -= 360
                else:
                    prevDiff += 360
                    
                log.debug("After adjustment: prevDiff == {}".\
                          format(prevDiff))
                log.debug("After adjustment: currDiff == {}".\
                          format(currDiff))

            for desiredAngleDeg in desiredAngleDegList:
                log.debug("Looking at desiredAngleDeg: {}".\
                          format(desiredAngleDeg))
                    
                desiredDegree = desiredAngleDeg
                    
                if prevDiff < desiredDegree and currDiff >= desiredDegree:
                    log.debug("Crossed over {} from below to above!".\
                              format(desiredDegree))

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than
                    # the threshold.
                    while currErrorTd > maxErrorTd:
                        log.debug("Refining between {} and {}".\
                                  format(Ephemeris.datetimeToStr(t1),
                                         Ephemeris.datetimeToStr(t2)))

                        # Check the timestamp between.
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=\
                                      (timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        testValueP1 = \
                            Util.toNormalizedAngle(getFieldValue(\
                            testDt, planet1ParamsList, fieldName))
                        testValueP2 = \
                            Util.toNormalizedAngle(getFieldValue(\
                            testDt, planet2ParamsList, fieldName))

                        log.debug("testValueP1 == {}".format(testValueP1))
                        log.debug("testValueP2 == {}".format(testValueP2))
                        
                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        elif longitudesP1[-2] < 120 and testValueP1 > 240:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 -= 360
                            
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360
                        elif longitudesP2[-2] < 120 and testValueP2 > 240:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 -= 360
                        
                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        # Handle special cases of degrees 0 and 360.
                        # Here we adjust testDiff so that it is in the
                        # expected ranges.
                        if Util.fuzzyIsEqual(desiredDegree, 0):
                            if testDiff > 240:
                                testDiff -= 360
                        elif Util.fuzzyIsEqual(desiredDegree, 360):
                            if testDiff < 120:
                                testDiff += 360
                        
                        log.debug("testDiff == {}".format(testDiff))
                        
                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                            longitudesP1[-1] = testValueP1
                            longitudesP2[-1] = testValueP2
            
                        currErrorTd = t2 - t1
                            
                    # Update our lists.
                    steps[-1] = currDt

                    # Store the aspect timestamp.
                    aspectTimestamps.append(currDt)
                 
                elif prevDiff > desiredDegree and currDiff <= desiredDegree:
                    log.debug("Crossed over {} from above to below!".\
                              format(desiredDegree))

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than
                    # the threshold.
                    while currErrorTd > maxErrorTd:
                        log.debug("Refining between {} and {}".\
                                  format(Ephemeris.datetimeToStr(t1),
                                         Ephemeris.datetimeToStr(t2)))

                        # Check the timestamp between.
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=\
                                      (timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        testValueP1 = \
                            Util.toNormalizedAngle(getFieldValue(\
                            testDt, planet1ParamsList, fieldName))
                        testValueP2 = \
                            Util.toNormalizedAngle(getFieldValue(\
                            testDt, planet2ParamsList, fieldName))

                        log.debug("testValueP1 == {}".format(testValueP1))
                        log.debug("testValueP2 == {}".format(testValueP2))
                        
                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        elif longitudesP1[-2] < 120 and testValueP1 > 240:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 -= 360
                            
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360
                        elif longitudesP2[-2] < 120 and testValueP2 > 240:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 -= 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        # Handle special cases of degrees 0 and 360.
                        # Here we adjust testDiff so that it is in the
                        # expected ranges.
                        if Util.fuzzyIsEqual(desiredDegree, 0):
                            if testDiff > 240:
                                testDiff -= 360
                        elif Util.fuzzyIsEqual(desiredDegree, 360):
                            if testDiff < 120:
                                testDiff += 360
                        
                        log.debug("testDiff == {}".format(testDiff))
                        
                        if testDiff > desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                            longitudesP1[-1] = testValueP1
                            longitudesP2[-1] = testValueP2
                            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Store the aspect timestamp.
                    aspectTimestamps.append(currDt)
                 
        # Prepare for the next iteration.
        log.debug("steps[-1] is: {}".\
                  format(Ephemeris.datetimeToStr(steps[-1])))
        log.debug("stepSizeTd is: {}".format(stepSizeTd))
        
        steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
        del steps[0]
        longitudesP1.append(None)
        del longitudesP1[0]
        longitudesP2.append(None)
        del longitudesP2[0]
        
        # Update prevDiff as the currDiff.
        prevDiff = Util.toNormalizedAngle(currDiff)
        
    log.info("Number of timestamps obtained: {}".\
             format(len(aspectTimestamps)))
    
    log.debug("Exiting " + inspect.stack()[0][3] + "()")
    return aspectTimestamps
        
    
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
    
    numPlanets = len(heliocentricPlanetNames)

    for i in range(numPlanets):
        for j in range(numPlanets):
            if i >= j:
                continue
            else:
                planetName1 = heliocentricPlanetNames[i]
                planetName2 = heliocentricPlanetNames[j]
                
                comboPlanetName = planetName1 + "/" + planetName2
                log.info("Obtaining planet heliocentric conjunction " + \
                         "information for '{}' ...".\
                         format(comboPlanetName))

                # Get list of conjunction timestamps.
                conjunctionTimestamps = \
                    getLongitudeAspectTimestamps(\
                    startDt, endDt,
                    [(planetName1, "heliocentric", "tropical")],
                    [(planetName2, "heliocentric", "tropical")],
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
                
                comboPlanetName = planetName1 + "/" + planetName2

                for tup in results[comboPlanetName]:
                    
                    planetComboName = tup[0]
                    jd = tup[1]
                    dt = tup[2]
                    aspectAngle = tup[3]
                    planet1HelioTropLongitudeDegrees = tup[4]
                    planet2HelioTropLongitudeDegrees = tup[5]
                    planet1HelioTropLongitudeSpeed = tup[6]
                    planet2HelioTropLongitudeSpeed = tup[7]
                    planet1HelioSidLongitudeDegrees = tup[8]
                    planet2HelioSidLongitudeDegrees = tup[9]
                    planet1HelioSidLongitudeSpeed = tup[10]
                    planet2HelioSidLongitudeSpeed = tup[11]
                    
                    # Assemble the line that will go into the CSV file.
                    line = ""
                    line += "{}".format(planetComboName) + ","
                    line += "{}".format(jd) + ","
                    line += "{}".format(Ephemeris.datetimeToStr(dt)) + ","
                    line += "{}".format(aspectAngle) + ","
                    line += "{}".format(planet1HelioTropLongitudeDegrees) + ","
                    line += "{}".format(planet2HelioTropLongitudeDegrees) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiAbbrev(\
                            planet1HelioTropLongitudeDegrees)) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiAbbrev(\
                            planet2HelioTropLongitudeDegrees)) + ","
                    line += "{}".format(planet1HelioTropLongitudeSpeed) + ","
                    line += "{}".format(planet2HelioTropLongitudeSpeed) + ","
                    line += "{}".format(planet1HelioSidLongitudeDegrees) + ","
                    line += "{}".format(planet2HelioSidLongitudeDegrees) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiAbbrev(\
                            planet1HelioSidLongitudeDegrees)) + ","
                    line += "{}".format(\
                        AstrologyUtils.convertLongitudeToStrWithRasiAbbrev(\
                            planet2HelioSidLongitudeDegrees)) + ","
                    line += "{}".format(planet1HelioSidLongitudeSpeed) + ","
                    line += "{}".format(planet2HelioSidLongitudeSpeed) + ","
                    
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
