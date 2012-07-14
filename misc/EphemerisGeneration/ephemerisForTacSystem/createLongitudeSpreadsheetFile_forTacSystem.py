#!/usr/bin/env python3
##############################################################################
# Description:
#
# Run the following to create the Ephemeris for the system described
# by TAC in WITS post #61757 and #61777.  
#
#
#  ./createLongitudeSpreadsheetFile_forTacSystem.py --centricity=heliocentric --zodiac=tropical --calculate-midpoints=false --start-timestamp=199001 --end-timestamp=201312 --output-file=TacEphemeris.csv
#
#
# Then run this:
#
#   python3 readCsvFileAndAddFields.py
#
#
# The resulting file produced should be "TacEphemeris2.csv".
# 
##############################################################################
#
#   Below is the description of this script from the original 'createLongitudeSpreadsheetFile.py' script.  This file (for the TAC system) is a modification of that original script file.
#
###############################################################################
#
#   Script to create the a CSV file containing longitude positions of
#   the planets.  The longitude of the planets are not mod-ed by 360,
#   so the longitudes continue to increase upwards as the circles get
#   completed.  This is so the spreadsheet can be used to create a
#   midpoint longitude ephemeris.
# 
#   Before using this script, make sure the global variables below are
#   set as desired.  Global variable parameters that may be set are:
#     - Location (City, Latitude, Longitude).
#     - Timezone ("US/Eastern", etc.)
#     - Time of day.
#     - fieldName (longitude)
#     - calculateMidpointsFlag (True or False)
#     - planetName (List of planet names to include)
#
# Usage:
#
#     ./createLongitudeSpreadsheetFile.py --help
#     ./createLongitudeSpreadsheetFile.py --version
#
#     # Generate the planet positions from January 1900 to December 1930,
#     # and write the output to a file.
#     ./createLongitudeSpreadsheetFile.py --start-timestamp=190001 --end-timestamp=193012 --output-file=/tmp/geocentric_planets.csv
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

# For regular expressions.
import re

# For parsing command-line options
from optparse import OptionParser  

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
from ephemeris import Ephemeris
from data_objects import *

##############################################################################

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Location information to use with the Ephemeris.
locationName = "New York City"
locationLongitude = 40.783
locationLatitude = 73.97
locationElevation = 0

# Timezone information to use with the Ephemeris.
timezone = pytz.timezone("US/Eastern")

# Time of the day to take measurements.
hourOfDay = 12
minuteOfHour = 0

# Centricity type (str).  Value is obtained via command-line options.
# This is one of "geocentric", "heliocentric", or "topocentric".
centricityType = None

# Zodiac type (str).  Value is obtained via command-line options.
# This is one of "tropical" or "sidereal".
zodiacType = None

# Field name.
fieldName = "longitude"

# Flag to also calculate midpoints (bool).
# Value is obtained via command-line options.
calculateMidpointsFlag = True

# Planet names to do calculations for.
planetNames = [\
#    "Sun",
#    "Moon",
#    "Mercury",
#    "Venus",
    "Earth",
    "Mars",
#    "Jupiter",
    "Saturn",
#    "Uranus",
#    "Neptune",
#    "Pluto",
#    "TrueNorthNode",
#    "Chiron",
#    "Isis"
    ]

# Starting timestamp.
# Format is "YYYYMM".
# This value is obtained via command-line parameter.
startTimestampStr = ""

# Ending timestamp.
# Format is "YYYYMM".
# This value is obtained via command-line parameter.
endTimestampStr = ""

# Destination output CSV file.
# This value is obtained via command-line parameter.
outputFile = ""

# For logging.
#logging.basicConfig(level=logging.DEBUG,
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    # Close the Ephemeris so it can do necessary cleanups.
    Ephemeris.closeEphemeris()
    
    logging.shutdown()
    
    sys.exit(rc)

##############################################################################

def convertDateStrToUrlVariableStr(timestampStr):
    """Converts input str of a date timestamp from format YYYYMMDD to
    the format required in the URL for a HTTP GET to Barchart
    for the start or end date of the data series.
    The resulting equivalent string is returned.
    """
    
    # Check input.
    if len(timestampStr) != 8 or timestampStr.isnumeric() == False:
        log.error("Timestamp string must be in the format 'YYYYYMMDD'.  " + \
              "Timestamp string given was: {}".format(timestampStr))
        shutdown(1)
    
    yearStr = timestampStr[0:4]
    monthStr = timestampStr[4:6]
    dayStr = timestampStr[6:8]
    
    log.debug("yearStr={}, monthStr={}, dayStr={}".\
              format(yearStr, monthStr, dayStr))

    rv = "{}%2F{}%2F{}".format(monthStr, dayStr, yearStr)
    
    log.debug(" returning: {}".format(rv))
    
    return rv

def getHeaderText():
    """Returns the text that will be outputted as the first line in
    the file.
    """

    headerText = ""
    headerText += "Date,"
    headerText += "Day,"
    
    # Each planet has it's own column.
    for planetName in planetNames:
        headerText += planetName + ","

    if calculateMidpointsFlag == True:
        # Each combination of midpoints has it's own column.
        for i in range(len(planetNames)):
            for j in range(i + 1, len(planetNames)):
                headerText += planetNames[i] + "-" + planetNames[j] + ","

    # Chop off the the trailing comma, and add a newline.
    if len(headerText) > 0 and headerText[-1] == ",":
        headerText = headerText[:-1] + os.linesep
        
    return headerText

def getFooterText():
    """Returns the text that will be outputted to the end of the file.
    """

    rv = ""
    return rv

def convertPlanetaryInfosToLine(currDt, prevPlanetaryInfosDict, currPlanetaryInfosDict):
    """Returns the text that will represent one line in the table.

    Arguments:
    currDt = datetime.datetime object for the timestamp connected to
             the data in currPlanetaryInfosDict.
             
    prevPlanetaryInfosDict = dictionary of PlanetName to PlanetaryInfo
                             objects for the previous timestamp iteration.
    
    currPlanetaryInfosDict = dictionary of PlanetName to PlanetaryInfo
                             objects for the current timestamp iteration.

    Note: The algorithm used below assumes that the step size is
    between prev and curr is small enough that none of the enabled
    planets move more than 120 degrees between steps.
    """
    
    # First make measurement adjustments so that the relevant degree
    # values in currPlanetaryInfosDict are cumulative degrees based on
    # the values in prevPlanetaryInfosDict.
    
    for planetName in planetNames:
        log.debug("calculation for planet: {}".format(planetName))
        
        if centricityType.lower() == "geocentric":

            # Get the previous value.  This value from the dictionary
            # has been modified so that it has the incremental amount
            # of circles traversed since the first timestamp of
            # planetary position obtained.
            prevValue = 0
            if prevPlanetaryInfosDict != None:
                prevValue = prevPlanetaryInfosDict[planetName].\
                            geocentric[zodiacType][fieldName]
            else:
                # If prevPlanetaryInfosDict is None, then it means
                # that this is the first data point taken, so just use
                # the current value as the previous value.
                prevValue = currPlanetaryInfosDict[planetName].\
                            geocentric[zodiacType][fieldName]
                
            # Get the normalized value and the number of circles traversed.
            prevValueNormalized = Util.toNormalizedAngle(prevValue)
            prevValueNumCircles = math.floor(prevValue / 360)

            # Get the current value.
            currValue = Util.toNormalizedAngle(\
                currPlanetaryInfosDict[planetName].\
                geocentric[zodiacType][fieldName])
            
            # Test if we crossed the 0 Aries point.
            if currValue < 120 and prevValueNormalized > 240:
                # Yes, we crossed the 0 Aries point from below to
                # above, so add a circle when computing the new
                # cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    geocentric[zodiacType][fieldName] = \
                    ((prevValueNumCircles + 1) * 360) + currValue
            elif currValue > 240 and prevValueNormalized < 120:
                # Yes, we crossed the 0 Aries point from above to 
                # below, so subtract a circle when computing the new
                # cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    geocentric[zodiacType][fieldName] = \
                    ((prevValueNumCircles - 1) * 360) + currValue
            else:
                # No, the 0 Aries point was not crossed.  Don't add a
                # circle to the cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    geocentric[zodiacType][fieldName] = \
                    (prevValueNumCircles * 360) + currValue
            
        elif centricityType.lower() == "heliocentric":

            # Get the previous value.  This value from the dictionary
            # has been modified so that it has the incremental amount
            # of circles traversed since the first timestamp of
            # planetary position obtained.
            prevValue = 0
            if prevPlanetaryInfosDict != None:
                prevValue = prevPlanetaryInfosDict[planetName].\
                            heliocentric[zodiacType][fieldName]
            else:
                # If prevPlanetaryInfosDict is None, then it means
                # that this is the first data point taken, so just use
                # the current value as the previous value.
                prevValue = currPlanetaryInfosDict[planetName].\
                            heliocentric[zodiacType][fieldName]

            # Get the normalized value and the number of circles traversed.
            prevValueNormalized = Util.toNormalizedAngle(prevValue)
            prevValueNumCircles = math.floor(prevValue / 360)

            # Get the current value.
            currValue = Util.toNormalizedAngle(\
                currPlanetaryInfosDict[planetName].\
                heliocentric[zodiacType][fieldName])
            
            # Test if we crossed the 0 Aries point.
            if currValue < 120 and prevValueNormalized > 240:
                # Yes, we crossed the 0 Aries point from below to
                # above, so add a circle when computing the new
                # cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    heliocentric[zodiacType][fieldName] = \
                    ((prevValueNumCircles + 1) * 360) + currValue
            elif currValue > 240 and prevValueNormalized < 120:
                # Yes, we crossed the 0 Aries point from above to 
                # below, so subtract a circle when computing the new
                # cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    heliocentric[zodiacType][fieldName] = \
                    ((prevValueNumCircles - 1) * 360) + currValue
            else:
                # No, the 0 Aries point was not crossed.  Don't add a
                # circle to the cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    heliocentric[zodiacType][fieldName] = \
                    (prevValueNumCircles * 360) + currValue
            
        elif centricityType.lower() == "topocentric":

            # Get the previous value.  This value from the dictionary
            # has been modified so that it has the incremental amount
            # of circles traversed since the first timestamp of
            # planetary position obtained.
            prevValue = 0
            if prevPlanetaryInfosDict != None:
                prevValue = prevPlanetaryInfosDict[planetName].\
                            topocentric[zodiacType][fieldName]
            else:
                # If prevPlanetaryInfosDict is None, then it means
                # that this is the first data point taken, so just use
                # the current value as the previous value.
                prevValue = currPlanetaryInfosDict[planetName].\
                            topocentric[zodiacType][fieldName]

            # Get the normalized value and the number of circles traversed.
            prevValueNormalized = Util.toNormalizedAngle(prevValue)
            prevValueNumCircles = math.floor(prevValue / 360)

            # Get the current value.
            currValue = Util.toNormalizedAngle(\
                currPlanetaryInfosDict[planetName].\
                topocentric[zodiacType][fieldName])
            
            # Test if we crossed the 0 Aries point.
            if currValue < 120 and prevValueNormalized > 240:
                # Yes, we crossed the 0 Aries point from below to
                # above, so add a circle when computing the new
                # cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    topocentric[zodiacType][fieldName] = \
                    ((prevValueNumCircles + 1) * 360) + currValue
            elif currValue > 240 and prevValueNormalized < 120:
                # Yes, we crossed the 0 Aries point from above to 
                # below, so subtract a circle when computing the new
                # cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    topocentric[zodiacType][fieldName] = \
                    ((prevValueNumCircles - 1) * 360) + currValue
            else:
                # No, the 0 Aries point was not crossed.  Don't add a
                # circle to the cumulative position data.
                currPlanetaryInfosDict[planetName].\
                    topocentric[zodiacType][fieldName] = \
                    (prevValueNumCircles * 360) + currValue
            
    # Actually gather and compute the text that is to be outputted.  
    text = ""

    # Date.
    dateStr = formatToDateStr(currDt)
    text += "{},".format(dateStr)

    # Day of week.
    dayOfWeekInt = currDt.weekday()
    dayOfWeekStr = None
    if dayOfWeekInt == 0:
        dayOfWeekStr = "Mon"
    elif dayOfWeekInt == 1:
        dayOfWeekStr = "Tue"
    elif dayOfWeekInt == 2:
        dayOfWeekStr = "Wed"
    elif dayOfWeekInt == 3:
        dayOfWeekStr = "Thu"
    elif dayOfWeekInt == 4:
        dayOfWeekStr = "Fri"
    elif dayOfWeekInt == 5:
        dayOfWeekStr = "Sat"
    elif dayOfWeekInt == 6:
        dayOfWeekStr = "Sun"
    text += "{}".format(dayOfWeekStr) + ","
    
    # Each planet has it's own column.
    for planetName in planetNames:
        if centricityType.lower() == "geocentric":
            text += "{},".format(currPlanetaryInfosDict[planetName].\
                                 geocentric[zodiacType][fieldName])
        elif centricityType.lower() == "heliocentric":
            text += "{},".format(currPlanetaryInfosDict[planetName].\
                                 heliocentric[zodiacType][fieldName])
        elif centricityType.lower() == "topocentric":
            text += "{},".format(currPlanetaryInfosDict[planetName].\
                                 topocentric[zodiacType][fieldName])
        
    if calculateMidpointsFlag == True:
        # Each combination of midpoints has it's own column.
        for i in range(len(planetNames)):
            for j in range(i + 1, len(planetNames)):
                planet1Value = None
                planet2Value = None

                if centricityType.lower() == "geocentric":
                    planet1Value = \
                        currPlanetaryInfosDict[planetNames[i]].\
                        geocentric[zodiacType][fieldName]
                    planet2Value = \
                        currPlanetaryInfosDict[planetNames[j]].\
                        geocentric[zodiacType][fieldName]
                elif centricityType.lower() == "heliocentric":
                    planet1Value = \
                        currPlanetaryInfosDict[planetNames[i]].\
                        heliocentric[zodiacType][fieldName]
                    planet2Value = \
                        currPlanetaryInfosDict[planetNames[j]].\
                        heliocentric[zodiacType][fieldName]
                elif centricityType.lower() == "topocentric":
                    planet1Value = \
                        currPlanetaryInfosDict[planetNames[i]].\
                        topocentric[zodiacType][fieldName]
                    planet2Value = \
                        currPlanetaryInfosDict[planetNames[j]].\
                        topocentric[zodiacType][fieldName]

                averageValue = (planet1Value + planet2Value) / 2.0
                text += "{},".format(averageValue)
                
    # Chop off the the trailing comma.
    if len(text) > 0 and text[-1] == ",":
        text = text[:-1] + os.linesep

    return text
            
def isNumber(numStr):
    """Returns True if the string is a number."""

    rv = True
    
    for letter in numStr:
        if not (letter.isdigit() or letter == "."):
            rv = False
            break

    return rv
        
##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--centricity",
                  action="store",
                  type="str",
                  dest="centricityTypeStr",
                  default="geocentric",
                  help=\
                  "Specify the centricity type for calculations.  " + \
                  "Valid values are: 'geocentric', 'heliocentric', and " + \
                  "'topocentric'.  Default value is: 'geocentric'.",
                  metavar="<CENTRICITY_TYPE>")

parser.add_option("--zodiac",
                  action="store",
                  type="str",
                  dest="zodiacTypeStr",
                  default="tropical",
                  help=\
                  "Specify the zodiac type for calculations.  " + \
                  "Valid values are: 'tropical' and 'sidereal'. " + \
                  "Default value is: 'tropical'.",
                  metavar="<ZODIAC_TYPE>")

parser.add_option("--calculate-midpoints",
                  action="store",
                  type="str",
                  dest="calculateMidpointsFlagStr",
                  default="true",
                  help=\
                  "Flag that indicates we should calculate midpoints also. " + \
                  "Valid values are: 'true' and 'false'.  " + \
                  "Default value is: 'true'.")

parser.add_option("--start-timestamp",
                  action="store",
                  type="str",
                  dest="startTimestampStr",
                  default=None,
                  help=\
                  "Specify starting year and month of the data.  " + \
                  "Format of this string is 'YYYYMM'.",
                  metavar="<TIMESTAMP>")

parser.add_option("--end-timestamp",
                  action="store",
                  type="str",
                  dest="endTimestampStr",
                  default=None,
                  help=\
                  "Specify ending year and month of the data.  " + \
                  "Format of this string is 'YYYYMM'.",
                  metavar="<TIMESTAMP>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file.  This is a required field.",
                  metavar="<FILE>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if options.version == True:
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

if options.centricityTypeStr.lower() != "geocentric" and \
   options.centricityTypeStr.lower() != "heliocentric" and \
   options.centricityTypeStr.lower() != "topocentric":

    log.error("Please specify a valid centricity type to the " + \
              "--centricity option.")
    shutdown(1)
else:
    centricityType = options.centricityTypeStr.lower()

# Remove planet names that don't make sense for the chosen centricity type.
if centricityType == "geocentric" or centricityType == "topocentric":
    if "Earth" in planetNames:
        planetNames.remove("Earth")
if centricityType == "heliocentric":
    if "Sun" in planetNames:
        planetNames.remove("Sun")
    if "TrueNorthNode" in planetNames:
        planetNames.remove("TrueNorthNode")

if options.zodiacTypeStr.lower() != "tropical" and \
   options.zodiacTypeStr.lower() != "sidereal":

    log.error("Please specify a valid zodiac type to the " + \
              "--zodiac option.")
    shutdown(1)
else:
    zodiacType = options.zodiacTypeStr.lower()


if options.calculateMidpointsFlagStr.lower() == "true":
    calculateMidpointsFlag = True
elif options.calculateMidpointsFlagStr.lower() == "false":
    calculateMidpointsFlag = False
else:
    log.error("Please specify a valid value to the " + \
              "--calculate-midpoints option.")
    shutdown(1)
    
    
   
if options.startTimestampStr == None:
    log.error("Please specify a start timestamp to the " + \
              "--start-timestamp option.")
    shutdown(1)
else:
    startTimestampStr = options.startTimestampStr
    
    if len(startTimestampStr) != 6:
        log.error("Start timestamp must be in format YYYYMM.")
        shutdown(1)
        
    if not isNumber(startTimestampStr):
        log.error("Start timestamp must be in format YYYYMM.")
        shutdown(1)
    
if options.endTimestampStr == None:
    log.error("Please specify an end timestamp to the " + \
              "--end-timestamp option.")
    shutdown(1)
else:
    endTimestampStr = options.endTimestampStr

    if len(endTimestampStr) != 6:
        log.error("End timestamp must be in format YYYYMM.")
        shutdown(1)
        
    if not isNumber(endTimestampStr):
        log.error("End timestamp must be in format YYYYMM.")
        shutdown(1)

# Make sure the end is after or equal to the beginning timestamp.
if int(startTimestampStr) > int(endTimestampStr):
    log.error("Start timestamp cannot be after the end timestamp.")
    shutdown(1)
    
if options.outputFile == None:
    log.error("Please specify an output filename to the " + \
          "--output-file option.")
    shutdown(1)
else:
    outputFile = options.outputFile


def getStartDatetime():
    """Returns the starting timestamp as a datetime.datetime of when
    to start calculating planetary positions.  This object has its
    timezone information set.  The information is gathered from the
    global variables.
    """
    
    # Get starting datetime information.
    startTimestampYear = int(startTimestampStr[0:4])
    startTimestampMonth = int(startTimestampStr[4:6])
    startTimestampDay = 1
    
    # Start timestamp.
    startTimestamp = datetime.datetime(year=startTimestampYear,
                                       month=startTimestampMonth,
                                       day=startTimestampDay,
                                       hour=hourOfDay,
                                       minute=minuteOfHour,
                                       tzinfo=timezone)
    
    return startTimestamp

def getEndDatetime():
    """Returns the ending timestamp as a datetime.datetime of when to
    stop calculating planetary positions (exclusive).  This object has
    its timezone information set.  The information is gathered from
    the global variables.
    """
    
    # Get ending year, month and day.
    endTimestampYear = int(endTimestampStr[0:4])
    endTimestampMonth = int(endTimestampStr[4:6])
    if endTimestampMonth == 12:
        # Cross-over from December to January.
        endTimestampYear += 1
        endTimestampMonth = 1
    else:
        # Some other month.  Just increment the month.
        endTimestampMonth += 1
    endTimestampDay = 1
        
    # End timestamp.
    endTimestamp = datetime.datetime(year=endTimestampYear,
                                     month=endTimestampMonth,
                                     day=endTimestampDay,
                                     hour=0,
                                     minute=0,
                                     tzinfo=timezone)

    return endTimestamp

def formatToDateStr(dt):
    """Returns a date string in the format that we want it in."""

    dateStr = ""
    
    if dt.year < 10:
        dateStr += "000{}".format(dt.year)
    elif dt.year < 100:
        dateStr += "00{}".format(dt.year)
    elif dt.year < 1000:
        dateStr += "0{}".format(dt.year)
    else:
        dateStr += "{}".format(dt.year)

    dateStr += "-"
    if dt.month < 10:
        dateStr += "0{}".format(dt.month)
    else:
        dateStr += "{}".format(dt.month)
    
    dateStr += "-"
    if dt.day < 10:
        dateStr += "0{}".format(dt.day)
    else:
        dateStr += "{}".format(dt.day)
    
    return dateStr

##############################################################################

# Initialize Ephemeris (required).
Ephemeris.initialize()

# Set the Location (required).
Ephemeris.setGeographicPosition(locationLatitude,
                                locationLongitude,
                                locationElevation)

text = ""
text += getHeaderText()

startDt = getStartDatetime()
endDt = getEndDatetime()
currDt = startDt
prevDt = None

# Note: The algorithm used in this program requires that the step size
# be such that no planet will move more than 120 degrees over the span
# of one step.
stepSizeTd = datetime.timedelta(days=1)

prevPlanetaryInfosDict = None
currPlanetaryInfosDict = None

tableDataDict = {}

while currDt < endDt:
    currPlanetaryInfosDict = {}
    
    for planetName in planetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, currDt)
        currPlanetaryInfosDict[planetName] = pi
    
    # Add text for a row in the table.
    text += convertPlanetaryInfosToLine(currDt, prevPlanetaryInfosDict, currPlanetaryInfosDict)
    
    # Prepare currDt for the next iteration.
    prevDt = currDt
    currDt = copy.deepcopy(currDt) + stepSizeTd
    currDt = currDt.replace(hour=hourOfDay, minute=minuteOfHour)

    prevPlanetaryInfosDict = currPlanetaryInfosDict

text += getFooterText()

with open(outputFile, "w") as f:
    log.info("Writing to output file '{}' ...".format(outputFile))
    f.write(text)

log.info("Done.")
shutdown(0)

