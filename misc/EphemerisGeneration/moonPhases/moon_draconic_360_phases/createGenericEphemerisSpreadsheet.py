#!/usr/bin/env python3
##############################################################################
# Description:
#
# Script for creating a generic spreadsheet of the Sun, Moon, and TrueNorthNode.
# The timestamp of each line entry is at the exact moment (within an error
# threshold of 1 minute) of each of 360 moon phases of a Draconic month.
#
# Data included is:
#
#        - Geocentric
#        - Heliocentric
#        - Declination
#        - Latitude
#
# Usage:
#
#   1) Ensure the global variables have been set appropriately:
#        - Start and end dates
#        - Location (coordinates)
#        - Time of day.
#        - Planets used in calculations
#        - Output CSV filename.
#
#    2) Run the script:
#
#        python3 createGenericEphemerisSpreadsheet.py
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
# This assumes that the relative directory from this script is: ../../../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
thisScriptDir = os.path.dirname(thisScriptDir)
thisScriptDir = os.path.dirname(thisScriptDir)
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


startDt = datetime.datetime(year=1906, month=1, day=1,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)
#startDt = datetime.datetime(year=1984, month=1, day=1,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
#startDt = datetime.datetime(year=2013, month=1, day=1,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)


endDt   = datetime.datetime(year=1906, month=5, day=31,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)
#endDt   = datetime.datetime(year=1936, month=12, day=31,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
#endDt   = datetime.datetime(year=2015, month=12, day=31,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
#endDt   = datetime.datetime(year=2013, month=4, day=1,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)


# Destination output CSV file.
outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/moonPhases/moon_draconic_360_phases/sun_moon_node_ephemeris_nyc.csv"

# Planet names to do calculations for.
geocentricPlanetNames = [\
    "Sun",
    "Moon",
    #"Mercury",
    #"Venus",
    #"Earth",
    #"Mars",
    #"Jupiter",
    #"Saturn",
    #"Uranus",
    #"Neptune",
    #"Pluto",
    "TrueNorthNode",
    #"Chiron",
    #"Isis"
    ]

# Planet names to do calculations for.
heliocentricPlanetNames = [\
    #"Sun",
    #"Moon",
    #"Mercury",
    #"Venus",
    #"Earth",
    #"Mars",
    #"Jupiter",
    #"Saturn",
    #"Uranus",
    #"Neptune",
    #"Pluto",
    #"TrueNorthNode",
    #"Chiron",
    #"Isis"
    ]

# Planet names to do calculations for.
declinationPlanetNames = [\
    "Sun",
    "Moon",
    #"Mercury",
    #"Venus",
    #"Earth",
    #"Mars",
    #"Jupiter",
    #"Saturn",
    #"Uranus",
    #"Neptune",
    #"Pluto",
    #"TrueNorthNode",
    #"Chiron",
    #"Isis"
    ]

# Planet names to do calculations for.
geocentricLatitudePlanetNames = [\
    #"Sun",
    "Moon",
    #"Mercury",
    #"Venus",
    #"Earth",
    #"Mars",
    #"Jupiter",
    #"Saturn",
    #"Uranus",
    #"Neptune",
    #"Pluto",
    #"TrueNorthNode",
    #"Chiron",
    #"Isis"
    ]

# Planet names to do calculations for.
heliocentricLatitudePlanetNames = [\
    #"Sun",
    #"Moon",
    #"Mercury",
    #"Venus",
    #"Earth",
    #"Mars",
    #"Jupiter",
    #"Saturn",
    #"Uranus",
    #"Neptune",
    #"Pluto",
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


def formatToDateAndDetailedTimeStr(datetimeObj):
    """Returns a string representation of a datetime.datetime object.
    Normally we wouldn't need to do this, but the datetime.strftime()
    does not work on years less than 1900. 

    Arguments:
    datetimeObj - datetime.datetime object with a tzinfo defined.

    Returns:
    String holding the info about the datetime.datetime object, in 
    the datetime.strftime() format:  "%Y-%m-%d %H:%M:%S %Z%z"
    """

    # Timezone name string, extracted from datetime.tzname().
    # This accounts for the fact that datetime.tzname() can return None.
    tznameStr = datetimeObj.tzname()
    if tznameStr == None:
        tznameStr = ""

    # Return the formatted string.
    return "{:04}-{:02}-{:02} {:02}:{:02} {}{}".\
        format(datetimeObj.year,
               datetimeObj.month,
               datetimeObj.day,
               datetimeObj.hour,
               datetimeObj.minute,
               tznameStr,
               Ephemeris.getTimezoneOffsetFromDatetime(datetimeObj))

    
def getPlanetaryInfosForDatetime(dt):
    """Helper function for getting a list of PlanetaryInfo objects
    to display in the astrology chart.
    """

    # Set the location again (required).
    Ephemeris.setGeographicPosition(locationLongitude,
                                    locationLatitude,
                                    locationElevation)
    
    # Get planetary info for all the planets.
    planets = []
    
    # Astrological house system for getting the house cusps.
    houseSystem = Ephemeris.HouseSys['Porphyry']
    
    planets.append(Ephemeris.getH1PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH2PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH3PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH4PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH5PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH6PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH7PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH8PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH9PlanetaryInfo(dt, houseSystem))
    planets.append(Ephemeris.getH10PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH11PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH12PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getARMCPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getVertexPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getEquatorialAscendantPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getCoAscendant1PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getCoAscendant2PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getPolarAscendantPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getHoraLagnaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getGhatiLagnaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMeanLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getOsculatingLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(dt))
    planets.append(Ephemeris.getSunPlanetaryInfo(dt))
    planets.append(Ephemeris.getMoonPlanetaryInfo(dt))
    planets.append(Ephemeris.getMercuryPlanetaryInfo(dt))
    planets.append(Ephemeris.getVenusPlanetaryInfo(dt))
    planets.append(Ephemeris.getEarthPlanetaryInfo(dt))
    planets.append(Ephemeris.getMarsPlanetaryInfo(dt))
    planets.append(Ephemeris.getJupiterPlanetaryInfo(dt))
    planets.append(Ephemeris.getSaturnPlanetaryInfo(dt))
    planets.append(Ephemeris.getUranusPlanetaryInfo(dt))
    planets.append(Ephemeris.getNeptunePlanetaryInfo(dt))
    planets.append(Ephemeris.getPlutoPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMeanNorthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
    planets.append(Ephemeris.getTrueNorthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getCeresPlanetaryInfo(dt))
    #planets.append(Ephemeris.getPallasPlanetaryInfo(dt))
    #planets.append(Ephemeris.getJunoPlanetaryInfo(dt))
    #planets.append(Ephemeris.getVestaPlanetaryInfo(dt))
    planets.append(Ephemeris.getIsisPlanetaryInfo(dt))
    #planets.append(Ephemeris.getNibiruPlanetaryInfo(dt))
    planets.append(Ephemeris.getChironPlanetaryInfo(dt))
    #planets.append(Ephemeris.getGulikaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMandiPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMeanOfFivePlanetaryInfo(dt))
    #planets.append(Ephemeris.getCycleOfEightPlanetaryInfo(dt))
    #planets.append(Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(dt))
    #planets.append(Ephemeris.getAvgJuSaUrNePlanetaryInfo(dt))
    #planets.append(Ephemeris.getAvgJuSaPlanetaryInfo(dt))

    return planets


def getEphemerisDataLineForDatetime(dt):
    """Obtains the line of CSV text of planetary position data.

    Arguments:
    dt - datetime.datetime object with the timestamp seeked.  
    
    Returns:
    
    str in CSV format. Since there are a lot of fields, please See the
    section of code where we write the header info str for the format.
    """

    # Return value.
    rv = ""

    planetaryInfos = getPlanetaryInfosForDatetime(dt)

    log.debug("Just obtained planetaryInfos for timestamp: {}".\
              format(Ephemeris.datetimeToStr(dt)))
    
    # Planet geocentric longitude 15-degree axis points.
    for planetName in geocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.geocentric['tropical']['longitude']
                rv += "{:.3f},".format(lon % 15.0)
                    
    # Planet geocentric longitude.
    for planetName in geocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.geocentric['tropical']['longitude']
                rv += "{:.3f},".format(lon)
                    
    # Planet geocentric longitude in zodiac str format.
    for planetName in geocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.geocentric['tropical']['longitude']
                valueStr = \
                         AstrologyUtils.\
                         convertLongitudeToStrWithRasiAbbrev(lon)
                rv += valueStr + ","
                
    # Planet heliocentric longitude 15-degree axis points.
    for planetName in heliocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.heliocentric['tropical']['longitude']
                rv += "{:.3f},".format(lon % 15.0)
                    
    # Planet heliocentric longitude.
    for planetName in heliocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.heliocentric['tropical']['longitude']
                rv += "{:.3f},".format(lon)
                    
    # Planet heliocentric longitude in zodiac str format.
    for planetName in heliocentricPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                lon = pi.heliocentric['tropical']['longitude']
                valueStr = \
                         AstrologyUtils.\
                         convertLongitudeToStrWithRasiAbbrev(lon)
                rv += valueStr + ","
                
    # Planet declination.
    for planetName in declinationPlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                declination = pi.geocentric['tropical']['declination']
                rv += "{:.3f},".format(declination)
    
    # Planet geocentric latitude.
    for planetName in geocentricLatitudePlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                latitude = pi.geocentric['tropical']['latitude']
                rv += "{:.3f},".format(latitude)
    
    # Planet heliocentric latitude.
    for planetName in heliocentricLatitudePlanetNames:
        for pi in planetaryInfos:
            if pi.name == planetName:
                latitude = pi.heliocentric['tropical']['latitude']
                rv += "{:.3f},".format(latitude)
    
    
    # Remove trailing comma.
    rv = rv[:-1]

    return rv

##############################################################################

def getLongitudeAspectTimestamps(\
    startDt, endDt,
    planet1ParamsList,
    planet2ParamsList,
    degreeDifference,
    uniDirectionalAspectsFlag=True,
    maxErrorTd=datetime.timedelta(hours=1)):
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
    highPrice - float value for the high price to end the vertical line.
    lowPrice  - float value for the low price to end the vertical line.
        
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

            log.debug("Planet {} has geo sid longitude: {}".\
                      format(planetName,
                             pi.geocentric["sidereal"]["longitude"]))
            
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

    log.debug("Number of timestamps obtained: {}".\
              format(len(aspectTimestamps)))
        
    log.debug("Exiting " + inspect.stack()[0][3] + "()")
    return aspectTimestamps

        
##############################################################################

#if __name__ == "__main__":
    
# Initialize Ephemeris (required).
Ephemeris.initialize()

# Set the Location (required).
Ephemeris.setGeographicPosition(locationLongitude,
                                locationLatitude,
                                locationElevation)

# Log the parameters that are being used.
log.info("Location used is: {}  (lat={}, lon={})".\
         format(locationName, locationLatitude, locationLongitude))
log.info("Timezone used is: {}".format(timezone.zone))
log.info("Start timestamp:  {}".format(Ephemeris.datetimeToStr(startDt)))
log.info("End   timestamp:  {}".format(Ephemeris.datetimeToStr(endDt)))

# Compile the header line text.
headerLine = ""
headerLine += "Date" + ","
headerLine += "Day of week" + ","
headerLine += "Day count" + ","
headerLine += "Week count" + ","
headerLine += "Month count" + ","

# Planet geocentric longitude mod 15.
for planetName in geocentricPlanetNames:
    headerLine += "G." + planetName + "%15" + ","

# Planet geocentric longitude.
for planetName in geocentricPlanetNames:
    headerLine += "G." + planetName + ","

# Planet geocentric longitude in zodiac str format.
for planetName in geocentricPlanetNames:
    headerLine += "G." + planetName + ","


# Planet heliocentric longitude mod 15.
for planetName in heliocentricPlanetNames:
    headerLine += "H." + planetName + "%15" + ","

# Planet heliocentric longitude.
for planetName in heliocentricPlanetNames:
    headerLine += "H." + planetName + ","

# Planet heliocentric longitude in zodiac str form.
for planetName in heliocentricPlanetNames:
    headerLine += "H." + planetName + ","

# Planet declination.
for planetName in declinationPlanetNames:
    headerLine += "D." + planetName + ","

# Planet geocentric latitude.
for planetName in geocentricLatitudePlanetNames:
    headerLine += "G.L." + planetName + ","

# Planet heliocentric latitude.
for planetName in heliocentricLatitudePlanetNames:
    headerLine += "H.L." + planetName + ","

# Remove the trailing comma.
headerLine = headerLine[:-1]

# Initialize the currDt to the start date.  Manually set the hour and
# minute so we get the ephemeris at noon localized time.
currDt = copy.deepcopy(startDt)
currDt = currDt.replace(hour=hourOfDay, minute=minuteOfHour)

stepSizeTd = datetime.timedelta(days=1)

# Text in the output file.
outputLines = []
outputLines.append(headerLine)

prevDate = None
dayCount = 0
weekCount = 0
monthCount = 0

log.info("Doing ephemeris calculations ...")

# Here we are obtaining 360 phases of a Draconic month.
degreesInCircle = 360.0
numMoonPhases = 360
increment = degreesInCircle / numMoonPhases

# Planet parameters.
planet1ParamsList = [("Moon", "geocentric", "tropical")]
planet2ParamsList = [("TrueNorthNode",  "geocentric", "tropical")]

timestamps = []

aspectDegrees = []

for i in range(0, numMoonPhases):
    aspectDegrees.append(i * (degreesInCircle / numMoonPhases))
    
for degreeDifference in aspectDegrees:
    timestamps.extend(\
        getLongitudeAspectTimestamps(\
            startDt, endDt,
            planet1ParamsList,
            planet2ParamsList,
            degreeDifference,
            uniDirectionalAspectsFlag=True,
            maxErrorTd=datetime.timedelta(minutes=1)))

# Sort the timestamps.
timestamps.sort()


# Log debug information.
for i in range(len(timestamps)):
    timestamp = timestamps[i]
    log.debug("timestamps[{}] == {}".\
              format(i, Ephemeris.datetimeToStr(timestamp)))

    currDt = timestamp

    line = ""

    # Get date and time str.
    #line += formatToDateAndTimeStr(currDt) + ","
    line += formatToDateAndDetailedTimeStr(currDt) + ","
    
    #line += Ephemeris.datetimeToStr(currDt) + ","

    # Get day of the week str, as 3-letter str.
    line += currDt.date().ctime()[0:3] + ","

    # Get the day count, week count, and month count.
    if prevDate == None:
        # This is first iteration in this while loop.  All counts
        # should be zero.

        # Day count.
        line += "{}".format(dayCount) + ","

        # Week count.
        line += "{}".format(weekCount) + ","

        # Month count.
        line += "{}".format(monthCount) + ","
        
    else:
        # There is a previous date stored, so check to see if we are
        # on a new day now.
        if prevDate != currDt.date():
            # Date changed, increment the day count.
            dayCount += 1
            
            # Day count.
            line += "{}".format(dayCount) + ","

            # See if the week changed.  Weeks start with Sunday.
            if currDt.date().isoweekday() == 7:
                # It is a Sunday.  A new week has arrived, so increment.
                weekCount += 1

            # Week count.
            line += "{}".format(weekCount) + ","

            # See if the month changed.  Months start on the 1st of the month.
            if prevDate.month != currDt.date().month:
                # A new month has arrived, so increment.
                monthCount += 1

            # Month count.
            line += "{}".format(monthCount) + ","
            
        else:
            # Date did not change, so print out the same counts as the
            # last loop iteration.
    
            # Day count.
            line += "{}".format(dayCount) + ","

            # Week count.
            line += "{}".format(weekCount) + ","

            # Month count.
            line += "{}".format(monthCount) + ","
        
    line += getEphemerisDataLineForDatetime(currDt) + ","
    
    # Remove the last trailing comma. 
    line = line[:-1]
    
    # Append to the output lines.
    outputLines.append(line)

    # Save the date for the next iteration, so we can maintain our
    # time-keeping for day, week, and month counts.
    prevDate = currDt.date()
    
    
# Write outputLines to output file.
try:
    with open(outputFilename, "w") as f:
        log.info("Writing to output file '{}' ...".format(outputFilename))
        
        endl = "\r\n"
        
        for line in outputLines:
            f.write(line + endl)
        
except IOError as e:
    errStr = "I/O Error while trying to write file '" + \
             outputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)

log.info("Done.")
shutdown(0)


##############################################################################
