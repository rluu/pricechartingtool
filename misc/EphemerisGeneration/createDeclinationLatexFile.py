#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Script to create the a Latex file containing declination positions
#   of the planets.
#
# Usage:
#
#     ./createDeclinationLatexFile.py --help
#     ./createDeclinationLatexFile.py --version
#
#     # Generate the planet positions from January 1900 to December 1930,
#     # and write the output to a file.
#     ./getFuturesDataFromBarChart.py --start-timestamp=190001 --end-timestamp=193012 --output-file=/tmp/testing.tex
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
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
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

# Description string.
descriptionStr = "Geocentric Tropical Declination: US/Eastern @ 12:00"

# Zodiac type.
zodiacType = "tropical"

# Field name.
fieldName = "declination"

# Planet names to do calculations for.
planetNames = [\
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Pluto",
    "Chiron"]

# Starting timestamp.
# Format is "YYYYMM".
# This value is obtained via command-line parameter.
startTimestampStr = ""

# Ending timestamp.
# Format is "YYYYMM".
# This value is obtained via command-line parameter.
endTimestampStr = ""

# Destination output latex .tex file.
# This value is obtained via command-line parameter.
outputFile = ""

# For logging.
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
    """Returns the text that will be outputted to the beginning of the
    Latex file.
    """

    startTimestampYearStr = startTimestampStr[0:4]
    startTimestampMonth = int(startTimestampStr[4:6])
    startTimestampMonthStr = Util.monthNumberToAbbrev(startTimestampMonth)
    
    endTimestampYearStr = endTimestampStr[0:4]
    endTimestampMonth = int(endTimestampStr[4:6])
    endTimestampMonthStr = Util.monthNumberToAbbrev(endTimestampMonth)
    
    rv = ""
    rv += "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    rv += os.linesep
    rv += "% " + descriptionStr + os.linesep
    rv += "% " + os.linesep
    rv += "% " + "Time range: {} {} to {} {}".\
          format(startTimestampMonthStr, startTimestampYearStr,
                 endTimestampMonthStr, endTimestampYearStr) + os.linesep
    rv += "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    rv += os.linesep
    rv += os.linesep
    rv += "\\documentclass[letterpaper]{article}" + os.linesep
    rv += "\\author{Ryan Le Luu}" + os.linesep
    rv += os.linesep
    rv += "\\usepackage[" + \
          "hmargin=0.8in," + \
          "vmargin=0.8in," + \
          "marginparwidth=0.0in]" + \
          "{geometry}" + os.linesep
    #rv += "\\addtolength{\\topmargin}{0.2in}" + os.linesep
    rv += os.linesep
    rv += "\\usepackage{fancyhdr}" + os.linesep
    rv += os.linesep
    rv += "\\usepackage{comment}" + os.linesep
    rv += os.linesep
    rv += "% Font used for planet glyphs." + os.linesep
    rv += "\\usepackage{starfont}" + os.linesep
    rv += os.linesep
    rv += "% Allow use of '\\degree' command for degree symbol." + os.linesep
    rv += "\\newcommand{\\degree}{\\ensuremath{^\\circ}}" + os.linesep
    rv += os.linesep
    rv += "\\begin{document}" + os.linesep
    rv += os.linesep
    rv += "\\pagestyle{fancy}" + os.linesep
    rv += "\\fancyhead{}" + os.linesep
    rv += "\\fancyhead[C]{" + descriptionStr + "}"
    rv += os.linesep
    rv += "\\footnotesize" + os.linesep
    rv += os.linesep
    rv += os.linesep

    return rv

def getFooterText():
    """Returns the text that will be outputted to the beginning of the
    Latex file.
    """

    rv = "\\end{document}" + os.linesep

    return rv

def getTableHeaderText(dt):
    """Returns the text that will be outputted at the top of each table.
    """

    text = ""
    
    text += "\\textbf{" + Util.monthNumberToAbbrev(dt.month) + " " + \
            str(dt.year) + "}" + \
            os.linesep + os.linesep
    
    text += "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|}" + os.linesep

    text += "  \\hline" + os.linesep + " "
    
    for planetName in planetNames:
        text += " & \\textbf{\\" + planetName + "}"
    text += " \\\\" + os.linesep
    
    text += "  \\hline" + os.linesep
    
    return text

def getTableFooterText():
    """Returns the text that will be outputted at the bottom of each table.
    """

    text = ""
    text += "\\end{tabular}" + os.linesep
    text += os.linesep
    text += "\\vspace{0.2in}" + os.linesep
    text += os.linesep
    
    return text

def convertPlanetaryInfosToLine(dateStr, planetaryInfosDict):
    """Returns the text that will represent one line in the table.

    Arguments:
    planetaryInfosDict = dictionary of PlanetName to PlanetaryInfo objects.
    """

    text = ""
    text += "  {}".format(dateStr)

    def convertPiToValueStr(pi):
        polarityStr = ""
        if pi.geocentric[zodiacType][fieldName] < 0:
            polarityStr = "-"
        else:
            polarityStr = "+"
            
        degrees = math.floor(abs(pi.geocentric[zodiacType][fieldName]))
        degreesStr = str(degrees)
        if degrees < 10:
            degreesStr = "0" + degreesStr

        minutes = \
            math.floor(\
            (abs(pi.geocentric[zodiacType][fieldName]) - degrees) * 60)
        minutesStr = str(minutes)
        if minutes < 10:
            minutesStr = "0" + minutesStr
        
        strValue = " & {}{}\\degree{}'".\
                   format(polarityStr, degreesStr, minutesStr)
        
        return strValue
    
    for planetName in planetNames:
        pi = planetaryInfosDict[planetName]
        text += convertPiToValueStr(pi)

    text += " \\\\" + os.linesep
    text += "  \\hline" + os.linesep
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
                  "Format of this string is 'YYYYMMDD'.",
                  metavar="<TIMESTAMP>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output latex file.  This is a required field.",
                  metavar="<FILE>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if options.version == True:
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

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

    dateStr = Util.monthNumberToAbbrev(dt.month) + " "
    
    if dt.day < 10:
        dateStr += "0{} ".format(dt.day)
    else:
        dateStr += "{} ".format(dt.day)
    
    if dt.year < 10:
        dateStr += "000{}".format(dt.year)
    elif dt.year < 100:
        dateStr += "00{}".format(dt.year)
    elif dt.year < 1000:
        dateStr += "0{}".format(dt.year)
    else:
        dateStr += "{}".format(dt.year)
    
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

while currDt < endDt:
    # See if this is a new month.
    if prevDt == None or prevDt.month != currDt.month:
        log.info("Processing: {} {}".\
                 format(Util.monthNumberToAbbrev(currDt.month), currDt.year))
        
        # Add the text for a new table.
        text += getTableHeaderText(currDt)
    
    planetaryInfosDict = {}
    
    for planetName in planetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, currDt)
        planetaryInfosDict[planetName] = pi

    dateStr = formatToDateStr(currDt)

    # Add text for a row in the table.
    text += convertPlanetaryInfosToLine(dateStr, planetaryInfosDict)
    
    # Prepare currDt for the next iteration.
    prevDt = currDt
    currDt = copy.deepcopy(currDt) + datetime.timedelta(days=1)
    currDt = currDt.replace(hour=hourOfDay, minute=minuteOfHour)

    if prevDt.month != currDt.month:
        # Month passed.  Close the table.
        text += getTableFooterText()

        # Pagebreak if it is an even month.
        if prevDt.month % 2 == 0:
            text += "\\pagebreak" + os.linesep + os.linesep

text += getFooterText()
    
with open(outputFile, "w") as f:
    log.info("Writing to output file '{}' ...".format(outputFile))
    f.write(text)

log.info("Done.")
shutdown(0)

