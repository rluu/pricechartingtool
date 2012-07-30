#!/usr/bin/env python3
##############################################################################
# File: planetPositionsForSwingDates.py
##############################################################################
#
# Description: This script takes a CSV file with dates and prices of
# major swings dates/prices, and outputs a CSV file with the same info, plus
# the geocentric positions of various planets.
#
# This script makes assumtions for the location and timezone.
#   Location: New York City, NY, USA.
#   Timezone: US/Eastern
# 
# Change the global variables below to modify these settings.
#
# Usage:
# 
#   ./planetPositionsForSwingDates.py --help
#   ./planetPositionsForSwingDates.py --version
#
#   ./planetPositionsForSwingDates.py \
#                           --input-file=/tmp/swingDates.txt \
#                           --description="IBM swings, from date X to Y."
#                           --output-file=swingsAndPlanetPositions.csv
#
##############################################################################
#
# Input file format:
#
#
# The input CSV file should be in the following format:
#
# First line is ignored.
# Subsequent lines are in one of the following formats:
#
#    <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
#    <MM/DD/YYYY HH:MM>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
#
# Where HH are values between 00 and 23, inclusive.
#
# For example, the following are valid:
#  
#    01/24/1962,547.00,550.00,544.25,550.00,408000,0
#
#    12/15/2011 23:21,580.5000000,580.5000000,580.5000000,580.5000000,0.0000000,0
#
##############################################################################
#   
# Dependencies:
#   src/astrologychart.py
#   src/ephemeris.py
#   src/data_objects.py
#
##############################################################################

import sys
import os
import copy
import pickle

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene
from astrologychart import AstrologyUtils

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# CSV input file.
# See description text at the top of this script for the format this
# should be in.
# THis valud is specified via command-line option. 
inputFilename = ""

# Output file that is a CSV file.
# This value is specified via command-line option.
outputFilename = ""


# Timezone information to use with the Ephemeris for the given timestamps.
timezone = pytz.timezone("US/Eastern")

# Location information to use with the Ephemeris.
locationName = "New York City"
locationLongitude = 40.783
locationLatitude = 73.97
locationElevation = 0

# Description string.
# This value is specified via command-line option.  
descriptionStr = ""

# Time of day used for timestamps given without a time.
defaultTimeStr = "12:00"

# For logging.
#logLevel = logging.DEBUG
logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    Ephemeris.closeEphemeris()
    logging.shutdown()
    sys.exit(rc)

def validateLine(line):
    """Validates a line of text is a valid CSV data line.
    
    Arguments:
    line - str in one of the following formats:
    
      <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
      
      <MM/DD/YYYY HH:MM>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
      
    Returns:
    
    tuple of (boolean, str) that represents if the line
    of text was parsed to be a valid CSV data line.
    If the line of text is valid, the boolean part of the tuple 
    returned is True and the string is returned is empty.
    If the line of text is found to be not valid, the tuple returns
    False and a string explaining why the validation failed.
    """
    
    log.debug("validateLine(line='{}')".format(line))
    
    # Check the number of fields.
    fields = line.split(",")
    numFieldsExpected = 7
    if len(fields) != numFieldsExpected:
        return (False, "Line does not have {} data fields".\
                format(numFieldsExpected))
    
    timestampStr = fields[0]
    openStr = fields[1]
    highStr = fields[2]
    lowStr = fields[3]
    closeStr = fields[4]
    volumeStr = fields[5]
    openIntStr = fields[6]
    
    dateStr = None
    timeStr = None
    
    if len(timestampStr) == 10:
        # Format of timestamp is 'MM/DD/YYYY'.
        dateStr = timestampStr
        timeStr = None
        
    elif len(timestampStr) == 16:
        # Format of timestamp is 'MM/DD/YYYY HH:MM'.
        timestampStrSplit = timestampStr.split(" ")
        
        if len(timestampStrSplit) != 2:
            return (False, "Format of the timestamp was not " + \
                    "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'.")
        
        dateStr = timestampStrSplit[0]
        timeStr = timestampStrSplit[1]
        
    else:
        # Invalid number of characters for the timestamp.
        return (False, "Format of the timestamp was not " + \
                "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'.")
    
    dateStrSplit = dateStr.split("/")
    if len(dateStrSplit) != 3:
        return (False, "Format of the timestamp was not " + \
                "'MM/DD/YYYY' or 'MM/DD/YYYY HH:MM'.")
    
    monthStr = dateStrSplit[0]
    dayStr = dateStrSplit[1]
    yearStr = dateStrSplit[2]
    
    if len(monthStr) != 2:
        return (False, "Month in the date is not two characters long")
    if len(dayStr) != 2:
        return (False, "Day in the date is not two characters long")
    if len(yearStr) != 4:
        return (False, "Year in the date is not four characters long")
    
    try:
        monthInt = int(monthStr)
        if monthInt < 1 or monthInt > 12:
            return (False, "Month in the date is not between 1 and 12")
    except ValueError as e:
        return (False, "Month in the date is not a number")
    
    try:
        dayInt = int(dayStr)
        if dayInt < 1 or dayInt > 31:
            return (False, "Day in the date is not between 1 and 31")
    except ValueError as e:
        return (False, "Day in the date is not a number")
    
    try:
        yearInt = int(yearStr)
    except ValueError as e:
        return (False, "Year in the date is not a number")
    
    
    hourStr = None
    minuteStr = None
    
    if timeStr != None:
        timeFields = timeStr.split(":")
        
        if len(timeFields) != 2:
            errStr = \
                "Format of the time was not 'HH:MM'." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        hourStr = timeFields[0]
        minuteStr = timeFields[1]
        
        if len(hourStr) != 2:
            errStr = \
                "Hour in the timestamp is not " + \
                "two characters long." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        if len(minuteStr) != 2:
            errStr = \
                "Minute in the timestamp is not " + \
                "two characters long." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        try:
            hourInt = int(hourStr)
            if hourInt < 0 or hourInt > 23:
                errStr = \
                    "Hour in the timestamp is not in range " + \
                    "[00, 23]." + \
                    "  timeStr == {}".format(timeStr)
                return (False, errStr)
        except ValueError as e:
            errStr = \
                "Hour in the timestamp is not a number." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        try:
            minuteInt = int(minuteStr)
            if minuteInt < 0 or minuteInt > 59:
                errStr = \
                    "Minute in the timestamp is not in " + \
                    "range [00, 59]." + \
                    "  timeStr == {}".format(timeStr)
                return (False, errStr)
        except ValueError as e:
            errStr = \
                "Minute in the timestamp is not a number." + \
                "  timeStr == {}".format(timeStr)
            return (False, errStr)
        
        
    try:
        openFloat = float(openStr)
    except ValueError as e:
        return (False, "OpenPrice is not a number")
    
    try:
        highFloat = float(highStr)
    except ValueError as e:
        return (False, "HighPrice is not a number")
    
    try:
        lowFloat = float(lowStr)
    except ValueError as e:
        return (False, "LowPrice is not a number")
    
    try:
        closeFloat = float(closeStr)
    except ValueError as e:
        return (False, "ClosePrice is not a number")
    
    try:
        volumeFloat = float(volumeStr)
    except ValueError as e:
        return (False, "Volume is not a number")
    
    try:
        openIntFloat = float(openIntStr)
    except ValueError as e:
        return (False, "OpenInterest is not a number")
    
    
    # If it got this far without returning, then everything 
    # checked out fine.
    return (True, "")


def convertLineToPriceBar(line):
    """Convert a line of text from a CSV file to a PriceBar.
    
    The expected format of 'line' one of the following:
    <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
    <MM/DD/YYYY HH:MM>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
        
    Returns:
    PriceBar object from the line of text.  If the text was incorrectly
    formatted, then None is returned.  
    """

    log.debug("convertLineToPriceBar(line='{}')".format(line))
    
    # Return value.
    retVal = None
    
    # Do validation on the line first.
    (validFlag, reasonStr) = validateLine(line)
    
    if validFlag == False:
        log.debug("Line conversion failed because: {}" + reasonStr)
        retVal = None
    else:
        # Although we already validated the line, we wrap the parsing 
        # here in a try block just in case something unexpected 
        # was thrown at us.
        try:
            fields = line.split(",")
            
            timestampStr = fields[0]
            openPrice = float(fields[1])
            highPrice = float(fields[2])
            lowPrice = float(fields[3])
            closePrice = float(fields[4])
            volume = float(fields[5])
            openInt = float(fields[6])
            
            dateStr = None
            timeStr = None
            
            if len(timestampStr) == 10:
                # Format of timestamp is 'MM/DD/YYYY'.
                dateStr = timestampStr

                # No time of day is given, so we will use the default.
                timeStr = defaultTimeStr
                
            elif len(timestampStr) == 16:
                # Format of timestamp is 'MM/DD/YYYY HH:MM'.
                timestampStrSplit = timestampStr.split(" ")
                
                dateStr = timestampStrSplit[0]
                timeStr = timestampStrSplit[1]
                
            else:
                reasonStr = \
                    "Invalid number of characters in timestampStr."
                log.debug("Line conversion failed because: {}" + \
                               reasonStr)
                retVal = None
                return retVal
            
            dateStrSplit = dateStr.split("/")
            month = int(dateStrSplit[0])
            day = int(dateStrSplit[1])
            year = int(dateStrSplit[2])
            
            timeStrSplit = timeStr.split(":")
            hour = int(timeStrSplit[0])
            minute = int(timeStrSplit[1])
            second = 0
            timestamp = \
                datetime.datetime(year,
                                  month, 
                                  day, 
                                  hour, 
                                  minute, 
                                  second,
                                  tzinfo=timezone)
            
            # Create the PriceBar with the parsed data.
            retVal = PriceBar(timestamp, 
                              open=openPrice,
                              high=highPrice,
                              low=lowPrice,
                              close=closePrice,
                              oi=openInt,
                              vol=volume)
            
        except IndexError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an IndexError: " + e)
        except UnicodeDecodeError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an UnicodeDecodeError: " + e)
        except ValueError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an ValueError: " + e)
        except TypeError as e:
            log.error("While converting line of text to " + \
                           "PriceBar, got an TypeError: " + e)
            
    # Return the PriceBar created (or None if an error occurred).
    return retVal

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
    planets.append(Ephemeris.getVertexPlanetaryInfo(dt, houseSystem))
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
    planets.append(Ephemeris.getMeanNorthNodePlanetaryInfo(dt))
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
    planets.append(Ephemeris.getMeanOfFivePlanetaryInfo(dt))
    planets.append(Ephemeris.getCycleOfEightPlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgJuSaUrNePlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgJuSaPlanetaryInfo(dt))

    return planets

def generateOutputFileCsvStr(priceBars, descriptionStr):
    """Takes a list of PriceBar objects and generates a CSV str
    containing the same data and planet location information.

    Arguments:
    priceBars - list of PriceBar objects.  Each of the PriceBar
                objects in this list have timestamp and timezone
                information set.
                
    descriptionStr - str containing text that describes the trading entity
                and other descriptive text for the data.  This str
                will be part of the outputted CSV str.

    Returns:
    str value for the output CSV text.
    """
    
    geocentricPlanetNameList = [\
        "Sun",
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
        "Pluto",
        "Chiron",
        "TrueNorthNode",
        #"Isis",
        ]

    endl = "\r\n"

    # Return value.
    rv = ""

    rv += "Description: {}".\
          format(descriptionStr) + endl

    # Column headers.
    rv += "jd,day,date,time,timezone,tags,open,high,low,close,volume,oi"

    # Add the columns headers for the Geocentric planets' longitude.
    # Here we do it twice because the first set is the 15-degree axis
    # reduction, and the second set is the actual planet positions.
    for planetName in geocentricPlanetNameList:
        rv += ",G." + planetName
    for planetName in geocentricPlanetNameList:
        rv += ",G." + planetName

    rv += endl

    
    for pb in priceBars:
        # Field: jd
        rv += "{}".format(Ephemeris.datetimeToJulianDay(pb.timestamp))
        rv += ","

        # Timezone name string, extracted from datetime.tzname().
        # This accounts for the fact that datetime.tzname() can return None.
        datetimeObj = pb.timestamp
        tznameStr = datetimeObj.tzname()
        if tznameStr == None:
            tznameStr = ""
        dayOfWeekStr = datetimeObj.ctime()[0:3]
        offsetStr = \
            Ephemeris.getTimezoneOffsetFromDatetime(datetimeObj)

        # Field: day
        rv += dayOfWeekStr
        rv += ","

        # Field: date
        rv += "{}-{:02}-{:02}".\
              format(datetimeObj.year,
                     datetimeObj.month,
                     datetimeObj.day)
        #rv += "{:02}/{:02}/{}".\
        #      format(datetimeObj.month,
        #             datetimeObj.day,
        #             datetimeObj.year)
        rv += ","

        # Field: time
        rv += "{:02}:{:02}:{:02}".\
              format(datetimeObj.hour,
                     datetimeObj.minute,
                     datetimeObj.second)
        rv += ","

        # Field: timezone.
        rv += "{}{}".format(tznameStr, offsetStr)
        rv += ","

        # Field: tags
        for tag in pb.tags:
            rv += tag + " "
        rv += ","

        # Field: open
        rv += "{}".format(pb.open)
        rv += ","
        
        # Field: high
        rv += "{}".format(pb.high)
        rv += ","
        
        # Field: low
        rv += "{}".format(pb.low)
        rv += ","
        
        # Field: close
        rv += "{}".format(pb.close)
        rv += ","
        
        # Field: volume
        rv += "{}".format(pb.vol)
        rv += ","
        
        # Field: oi
        rv += "{}".format(pb.oi)
        rv += ","

        # Get PlanetaryInfos for this timestamp.
        planetaryInfos = \
            getPlanetaryInfosForDatetime(pb.timestamp)
        
        # Fields of the geocentric planets' longitude 15-degree axis points.
        for planetName in geocentricPlanetNameList:
            for pi in planetaryInfos:
                if pi.name == planetName:
                    lon = pi.geocentric['tropical']['longitude']
                    rv += "{:6.3f},".format(lon % 15.0)
                    break
            
        # Fields of the geocentric planets' longitude.
        for planetName in geocentricPlanetNameList:
            for pi in planetaryInfos:
                if pi.name == planetName:
                    lon = pi.geocentric['tropical']['longitude']
                    valueStr = AstrologyUtils.\
                               convertLongitudeToStrWithRasiAbbrev(lon)
                    rv += "{},".format(valueStr)
                    break

        # Chop off the last trailing comma.
        rv = rv[:-1]
        rv += endl
        
    return rv
    
##############################################################################

if __name__ == "__main__":
    
    # Create the parser
    parser = OptionParser()
    
    # Specify all valid options.
    parser.add_option("-v", "--version",
                      action="store_true",
                      dest="version",
                      default=False,
                      help="Display script version info and author contact.")
    
    parser.add_option("--input-file",
                      action="store",
                      type="str",
                      dest="inputFilename",
                      default=None,
                      help="Specify an input CSV file to load.  " + \
                      "For the expected format, please see the " + \
                      "description text at the top of this " + \
                      "script's source code.",
                      metavar="<FILE>")
    
    parser.add_option("--output-file",
                      action="store",
                      type="str",
                      dest="outputFilename",
                      default=None,
                      help="Specify an output filename for the CSV file.",
                      metavar="<FILE>")
    
    parser.add_option("--description",
                      action="store",
                      type="str",
                      dest="descriptionStr",
                      default=None,
                      help="Specify text that will be used as the " + \
                      "description text in the output CSV file.",
                      metavar="<STRING>")
    
    # Parse the arguments into options.
    (options, args) = parser.parse_args()
    
    # Print version information if the flag was used.
    if (options.version == True):
        print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
        print("By Ryan Luu, ryanluu@gmail.com")
        shutdown(0)
    
    # Get the input CSV filename.
    if (options.inputFilename == None):
        log.error("Please specify an input CSV file with " +
                  "the --input-file option.")
        shutdown(1)
    else:
        log.debug("options.inputFilename == {}".format(options.inputFilename))
        inputFilename = os.path.abspath(options.inputFilename)
        log.debug("inputFilename == {}".format(inputFilename))

        # Check to make sure the path exists and it is a file.
        if not os.path.isfile(inputFilename):
            log.error("The input file specified does not exist, " + \
                      "or is not a file.")
            shutdown(1)
        
    # Get the output CSV filename.
    if (options.outputFilename == None):
        log.error("Please specify an output CSV file with " +
                  "the --output-file option.")
        shutdown(1)
    else:
        log.debug("options.outputFilename == {}".format(options.outputFilename))
        outputFilename = os.path.abspath(options.outputFilename)
        log.debug("outputFilename == {}".format(outputFilename))

    # Get the description text.
    if (options.descriptionStr == None):
        log.error("Please specify some description text for the " + \
                  "output CSV file using the --description option.")
        shutdown(1)
    else:
        descriptionStr = options.descriptionStr
    
    
    ######################################
    
    # Initialize Ephemeris (required).
    Ephemeris.initialize()


    # Number of lines to skip when reading from the input CSV file.
    numLinesToSkip = 1

    # List of PriceBar objects read in from the input CSV file.
    priceBars = []

    try:
        with open(inputFilename, "r") as f:
            # Go through each line of the file.
            i = 0
            for line in f:
                i += 1
                
                # Skip over empty lines and lines before 
                # line number 'numLinesToSkip'.
                if i > numLinesToSkip and line.strip() != "":
                    (lineValid, reason) = validateLine(line)
                    if lineValid == False:
                        # Invalid line in the file.
                        validationStr = \
                            "Validation failed on line " + \
                            "{} because: {}".format(i, reason)
                        log.error(validationStr)
                        break
                    else:
                        # Valid line in the file.
                        
                        # Create a PriceBar and append it to 
                        # the PriceBar list.
                        pb = convertLineToPriceBar(line)
                        priceBars.append(pb)
    except IOError as e:
        errStr = "I/O Error while trying to read file '" + \
            inputFilename + "':" + os.linesep + str(e)
        log.error(errStr)
    
    log.info("Creating CSV str ...")
    
    csvStr = generateOutputFileCsvStr(priceBars, descriptionStr)
    
    # Write to file.
    if outputFilename != "":
        log.info("Writing to output file '{}' ...".format(outputFilename))
        with open(outputFilename, "w") as f:
            f.write(csvStr)
        log.info("File successfully written.")
    
    # Execution completed.
    log.info("Done.")
    shutdown(0)

##############################################################################
