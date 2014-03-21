#!/usr/bin/env python3
##############################################################################
# Description:
#
# Script for creating a generic spreadsheet containing an daily ephemeris of
# the main planets:
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
# This assumes that the relative directory from this script is: ../../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
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


#startDt = datetime.datetime(year=1969, month=1, day=1,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
#startDt = datetime.datetime(year=1894, month=1, day=1,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
startDt = datetime.datetime(year=2016, month=12, day=1,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)


endDt   = datetime.datetime(year=2016, month=12, day=31,
                            hour=hourOfDay, minute=minuteOfHour,
                            tzinfo=timezone)
#endDt   = datetime.datetime(year=1940, month=12, day=31,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)
#endDt   = datetime.datetime(year=1979, month=12, day=31,
#                            hour=hourOfDay, minute=minuteOfHour,
#                            tzinfo=timezone)


# Destination output CSV file.
outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleHuntingGeneric/generic_daily_ephemeris_nyc_noon.csv"


# Planet names to do calculations for.
geocentricPlanetNames = [\
    "Sun",
    "Moon",
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
    "Chiron",
    "Isis"
    ]

# Planet names to do calculations for.
heliocentricPlanetNames = [\
    #"Sun",
    #"Moon",
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    #"TrueNorthNode",
    "Chiron",
    "Isis"
    ]

# Planet names to do calculations for.
declinationPlanetNames = [\
    "Sun",
    "Moon",
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
    "Chiron",
    "Isis"
    ]

# Planet names to do calculations for.
geocentricLatitudePlanetNames = [\
    "Sun",
    "Moon",
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
    "Chiron",
    "Isis"
    ]

# Planet names to do calculations for.
heliocentricLatitudePlanetNames = [\
    #"Sun",
    #"Moon",
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    #"TrueNorthNode",
    "Chiron",
    "Isis"
    ]


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

while currDt.date() < endDt.date():
    line = ""

    # Get date and time str.
    line += formatToDateAndTimeStr(currDt) + ","

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
    
    # Increment the currDt by the step size for the next iteration.
    # Also, make sure the time is set.
    currDt = currDt + stepSizeTd
    currDt = currDt.replace(hour=hourOfDay, minute=minuteOfHour)
    
    
# Write outputLines to output file.
try:
    with open(outputFilename, "w", encoding="utf-8") as f:
        log.info("Writing to output file '{}' ...".format(outputFilename))
        
        endl = "\n"
        
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
