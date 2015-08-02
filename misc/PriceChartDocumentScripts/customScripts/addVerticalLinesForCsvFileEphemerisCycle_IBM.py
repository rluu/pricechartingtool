#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for drawing veritcal lines at cycle turn dates.  These turn
#   dates are determined based various input parameters and an input
#   Ephemeris CSV file that contains composite calculated planetary
#   combinations.
#
#   In this script's current state, it is a custom script that reads
#   in an Ephemeris file made for the IBM trading system given by TAC,
#   and generates the hit points that should be the expected 2-planet
#   or 3-planet cycle pivots in this system.  (See global variables
#   below that can be tweaked to allow it to work with other trading
#   entities).  This input file is the output from running the
#   following scripts:
#
#     /home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/createLongitudeSpreadsheetFile_forTacSystem.py
#
#     /home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/readCsvFileAndAddFields.py
#   
#   See the documentation for these scripts for how to use them to
#   generate the required input to this script.
#
# Usage:
#
#   First make sure the global variables are set according to what you want.
#
#   Then run the following:
#
#     ./modifyPriceChartDocument.py --pcd-file=/home/rluu/programming/pricechartingtool/data/PriceChartDocumentFiles/IBM.pcd --script-file=./customScripts/addVerticalLinesForCsvFileEphemerisCycle_IBM.py
#
#
# WARNING:
#
#   This script makes very specific use of data from certain columns
#   of the input CSV file, and makes no attempt to verify that the
#   data from the planet that it thinks it is from.  If the scripts
#   that generate these inputs changes, then the column numbers
#   referenced in this script need to change too.
#
# Note:
# 
#   This script in its current state uses algorithms in this module
#   only work for Heliocentric cycle calculations.  Additional
#   modifications will be needed to get it to work with geocentric
#   cycles.
#
##############################################################################

import os
import sys
import errno

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Include some PriceChartingTool modules.
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene

# Holds functions for adding artifacts for various aspects.
from planetaryCombinationsLibrary import PlanetaryCombinationsLibrary

##############################################################################
# Global variables
##############################################################################

# For logging.
logLevel = logging.DEBUG
#logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)


# Column number that has the planetary data we seek to analyze.  This
# value is 0-based (column 0 is the first column).
# 
# This is the column number in the CSV file from which to read values
# from.  The values in this column will have a modulus operation done
# on them.
#
# For 2-planet cycle used in IBM.
#columnNumber = 12
# For 3-planet cycle used in IBM.
columnNumber = 15

# Modulus amount.
#
# For 2-planet cycle used in IBM.
#modulusAmt = 12
# For 3-planet cycle used in IBM.
modulusAmt = 10      

# moddedHitValue.
# After doing the modulus operation, we look for the value closest to
# this value to yield dates.
# 
# For 2-planet cycle used in IBM, based on November 1, 2005.
#moddedHitValue = 1.152887198
# For 3-planet cycle used in IBM, based on November 3, 2005.
#moddedHitValue = 9.604528504
moddedHitValue = 9.0


# Color to use when drawing the vertical lines.

# For 2-planet cycle used in IBM.
#color = QColor(Qt.cyan)
# For 3-planet cycle used in IBM.
color = QColor(Qt.yellow)



# Input CSV Ephemeris filename.
inputCsvFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/ephemerisForTacSystem/TacEphemeris2.csv"

# Timezone used for the data in the CSV spreadsheet.
inputCsvTimezone = pytz.timezone("US/Eastern")

# Column number for the date or timestamp.
timestampColumnNumber = 0

# Flag to save the added vertical lines to PCD file or not.
modifyPcddFlag = True

# Flag to print out the cycle hit points to log.debug().
printCycleTurnPointsFlag = False

# Start and ending timestamps for analyzing and drawing vertical lines.
#startDt = datetime.datetime(year=1962, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
startDt = datetime.datetime(year=1990, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
endDt   = datetime.datetime(year=2013, month=12, day=31,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
highPrice = 700.0
lowPrice = 10.0

# Number of lines to skip before reading the data in the CSV file.
linesToSkip = 1

# Delimiter in the CSV file.
delimiter = ","

# Defaults for hour and minute of day for the timestamp from the input
# file when only the date is given.
defaultHourOfDay = 12
defaultMinuteOfHour = 0

##############################################################################

def convertEphemerisTimestampStrToDatetime(timestampStr):
    """Converts a timestamp str given in the one of the two formats to
    a datetime.datetime object.  If no time of day is given in the
    str, then the default time and timezone will be used.  See global
    variables.

    Arguments:
    timestampStr - str in one of the following formats:
    
                   YYYY-MM-DD
                   YYYY-MM-DD HH:MM

                   Where HH is a value in range [00, 23].
                   
    Returns:
    datetime.datetime object representing the timestamp given in the str.
    If the format is invalid, then None is returned.
    """

    dateOnlyFormat = "YYYY-MM-DD"
    dateAndTimeFormat = "YYYY-MM-DD HH:MM"

    # Check input string for correct formatting.
    if len(timestampStr) != len(dateOnlyFormat) and \
           len(timestampStr) != len(dateAndTimeFormat):
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None

    elif len(timestampStr) == len(dateOnlyFormat):
        if timestampStr[4] != "-" or timestampStr[7] != "-":
            log.error("Read a timestamp from the CSV file that is " + \
                      "not in the correct format.  timestampStr == '{}'".\
                      format(timestampStr))
            return None
        
    elif len(timestampStr) == len(dateAndTimeFormat):
        if timestampStr[4] != "-" or timestampStr[7] != "-" or \
               timestampStr[10] != " " or timestampStr[13] != ":":
            
            log.error("Read a timestamp from the CSV file that is " + \
                      "not in the correct format.  timestampStr == '{}'".\
                      format(timestampStr))
            return None
        

    yearStr = timestampStr[0:4]
    monthStr = timestampStr[5:7]
    dayStr = timestampStr[8:10]

    hourStr = None
    minuteStr = None
    if len(timestampStr) == len(dateAndTimeFormat):
        hourStr = timestampStr[11:13]
        minuteStr = timestampStr[14:16]
    else:
        hourStr   = "{:02}".format(defaultHourOfDay)
        minuteStr = "{:02}".format(defaultMinuteOfHour)
    
    # Test to make sure all the str values are digits before
    # converting to int values.
    for letter in yearStr:
        if not letter.isdigit():
            log.error("There is a non-digit year value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in monthStr:
        if not letter.isdigit():
            log.error("There is a non-digit month value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in dayStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    for letter in hourStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    for letter in minuteStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    
    # Convert the substrings to int values for the parts of the date/time.
    year = int(yearStr)
    month = int(monthStr)
    day = int(dayStr)

    hour = int(hourStr)
    minute = int(minuteStr)
    
    rv = datetime.datetime(year, month, day, hour, minute, \
                           tzinfo=inputCsvTimezone)
    
    return rv

def processPCDD(pcdd, tag):
    """
    
    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.  
           This implementation does not use this value.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    global highPrice
    global lowPrice

    
    # Return value.
    rv = 0


    # Check global variable inputs.
    if moddedHitValue >= modulusAmt:
        log.error("Global input variable 'moddedHitValue' " + \
                  "cannot be greater than the value for 'modulusAmt'.")
        # Don't save pccd.
        rv = 1
        return rv

    if startDt > endDt:
        log.error("Global input variable 'startDt' cannot be after 'endDt'.")
        # Don't save pccd.
        rv = 1
        return rv
    

    # Ephemeris earliest timestamp.  
    ephemerisEarliestTimestamp = None
    
    # Ephemeris latest timestamp.
    ephemerisLatestTimestamp = None
    
    # Cycle hit timestamps.
    cycleHitTimestamps = []
    
    # Previous and current values held across iterations of the lines
    # of the CSV file.
    prevDt = None
    currDt = None
    prevUnmoddedValue = None
    currUnmoddedValue = None
    
    # Counter for the current line number.
    lineNum = 0

    # Column name.  This is obtained from the first line in the CSV file.
    columnName = ""


    try:
        with open(inputCsvFilename) as f:

            for line in f:
                line = line.strip()
                #log.debug("Looking at line [{}]: {}".format(lineNum, line))
                
                # First line has the column headers.
                if lineNum == 0:
                    line = line.strip()
                    fieldValues = line.split(delimiter)
                                    
                    # Make sure we have enough columns of data.
                    if columnNumber >= len(fieldValues):
                        log.error("The input CSV file does not have enough " + \
                                  "columns.  Could not read column {}".\
                                  format(columnNumber))
                        # Don't save pcdd.
                        rv = 1
                        return rv
    
                    # Get the column name.
                    columnName = fieldValues[columnNumber]
                    
                if lineNum >= linesToSkip:
                    line = line.strip()
                    fieldValues = line.split(delimiter)
    
                    # Make sure we have enough columns of data.
                    if columnNumber >= len(fieldValues):
                        log.error("The input CSV file does not have enough " + \
                                  "columns.  Could not read column {}".\
                                  format(columnNumber))
                        # Don't save pcdd.
                        rv = 1
                        return rv
        
                    # Get the date from this line of text and convert
                    # to a datetime.
                    timestampStr = fieldValues[0]
                    currDt = convertEphemerisTimestampStrToDatetime(\
                        timestampStr)
                    
                    # If conversion failed then don't save.
                    if currDt == None:
                        # Don't save pcdd.
                        rv = 1
                        return rv
    
                    # Store the earliest and latest timestamps of the
                    # Ephemeris from the CSV file, as read so far.
                    if ephemerisEarliestTimestamp == None:
                        ephemerisEarliestTimestamp = currDt
                    elif currDt < ephemerisEarliestTimestamp:
                        ephemerisEarliestTimestamp = currDt
    
                    if ephemerisLatestTimestamp == None:
                        ephemerisLatestTimestamp = currDt
                    elif currDt > ephemerisLatestTimestamp:
                        ephemerisLatestTimestamp = currDt
                    
                    # Continue only if the currDt is between the start and
                    # end timestamps.
                    if startDt < currDt < endDt:
                        
                        currUnmoddedValue = float(fieldValues[columnNumber])
                        currModdedValue = currUnmoddedValue % modulusAmt
                        
                        if prevDt != None and prevUnmoddedValue != None:
                            # Assuming heliocentric cycles, so values change
                            # in only one direction.
        
                            prevModdedValue = prevUnmoddedValue % modulusAmt
                            
                            if prevUnmoddedValue < currUnmoddedValue:
                                # Increasing values.
                                
                                if prevModdedValue < currModdedValue:
                                    # Curr value has not looped over the
                                    # modulus amount.  This is the normal case.
                                    
                                    if prevModdedValue < moddedHitValue and \
                                           moddedHitValue <= currModdedValue:
                                        # We crossed over the moddedHitValue.
                                        
                                        # Check to see whether the
                                        # previous or the current is
                                        # closer to the moddedHitValue.
    
                                        prevDiff = abs(moddedHitValue - \
                                                       prevModdedValue)
    
                                        currDiff = abs(currModdedValue - \
                                                       moddedHitValue)
    
                                        if prevDiff < currDiff:
                                            # Prev is closer.
                                            cycleHitTimestamps.append(prevDt)
                                        else:
                                            # Curr is closer.
                                            cycleHitTimestamps.append(currDt)
                                            
                                elif prevModdedValue > currModdedValue:
                                    # Curr value has looped over the modulus
                                    # amount.  We must make an adjustment when
                                    # doing calculations.
                                    
                                    if prevModdedValue < moddedHitValue:
                                        # We crossed over the moddedHitValue.
                                        
                                        # Check to see whether the
                                        # previous or the current is
                                        # closer to the moddedHitValue.
    
                                        prevDiff = abs(moddedHitValue - \
                                                       prevModdedValue)
    
                                        currDiff = abs(currModdedValue + \
                                                       modulusAmt - \
                                                       moddedHitValue)
                                        
                                        if prevDiff < currDiff:
                                            # Prev is closer.
                                            cycleHitTimestamps.append(prevDt)
                                        else:
                                            # Curr is closer.
                                            cycleHitTimestamps.append(currDt)
                                            
                                    elif moddedHitValue <= currModdedValue:
                                        # We crossed over the moddedHitValue.
                                        
                                        # Check to see whether the
                                        # previous or the current is
                                        # closer to the moddedHitValue.
    
                                        prevDiff = abs(moddedHitValue + \
                                                       modulusAmt - \
                                                       prevModdedValue)
    
                                        currDiff = abs(currModdedValue - \
                                                       moddedHitValue)
    
                                        if prevDiff < currDiff:
                                            # Prev is closer.
                                            cycleHitTimestamps.append(prevDt)
                                        else:
                                            # Curr is closer.
                                            cycleHitTimestamps.append(currDt)
                                            
                            elif prevUnmoddedValue > currUnmoddedValue:
                                # Decreasing values.
                                
                                if currModdedValue < prevModdedValue:
                                    # Curr value has not looped over 0.
                                    # This is the normal case.
                                    
                                    if currModdedValue <= moddedHitValue and \
                                           moddedHitValue < prevModdedValue:
                                        # We crossed over the moddedHitValue.
                                        
                                        # Check to see whether the
                                        # previous or the current is
                                        # closer to the moddedHitValue.
    
                                        currDiff = abs(moddedHitValue - \
                                                       currModdedValue)
    
                                        prevDiff = abs(prevModdedValue - \
                                                       moddedHitValue)
    
                                        if prevDiff < currDiff:
                                            # Prev is closer.
                                            cycleHitTimestamps.append(prevDt)
                                        else:
                                            # Curr is closer.
                                            cycleHitTimestamps.append(currDt)
                                            
                                elif currModdedValue > prevModdedValue:
                                    # Curr value has looped over 0.
                                    # We must make an adjustment when
                                    # doing calculations.
                                    
                                    if currModdedValue <= moddedHitValue:
                                        # We crossed over the moddedHitValue.
                                        
                                        # Check to see whether the
                                        # previous or the current is
                                        # closer to the moddedHitValue.
    
                                        currDiff = abs(moddedHitValue - \
                                                       currModdedValue)
    
                                        prevDiff = abs(prevModdedValue + \
                                                       modulusAmt - \
                                                       moddedHitValue)
                                        
                                        if prevDiff < currDiff:
                                            # Prev is closer.
                                            cycleHitTimestamps.append(prevDt)
                                        else:
                                            # Curr is closer.
                                            cycleHitTimestamps.append(currDt)
                                            
                                    elif moddedHitValue < prevModdedValue:
                                        # We crossed over the moddedHitValue.
                                        
                                        # Check to see whether the
                                        # previous or the current is
                                        # closer to the moddedHitValue.
    
                                        currDiff = abs(moddedHitValue + \
                                                       modulusAmt - \
                                                       currModdedValue)
    
                                        prevDiff = abs(prevModdedValue - \
                                                       moddedHitValue)
    
                                        if prevDiff < currDiff:
                                            # Prev is closer.
                                            cycleHitTimestamps.append(prevDt)
                                        else:
                                            # Curr is closer.
                                            cycleHitTimestamps.append(currDt)
                                            
                            else:
                                # Value is the same.  This is an error.
                                log.error("Found two values in column {} ".\
                                          format(columnNumber) + \
                                          "that are the same value.  " + \
                                          "See line {} in file '{}'".\
                                          format(lineNum, inputCsvFilename))
                
                # Update variables for reading the next line.
                prevDt = currDt
                currDt = None
                
                prevUnmoddedValue = currUnmoddedValue
                currUnmoddedValue = None

                lineNum += 1

    except IOError as e:
        log.error("Please check to make sure input CSV file '{}'".\
                  format(inputCsvFilename) + \
                  " is a file and exists.")
        
        # Don't save pcdd.
        rv = 1
        return rv

    
    
    # We now have all the cycle hit timestamps that are in the time
    # range desired.  All these timestamps should be in the list
    # 'cycleHitTimestamps'.

    # Replace spaces in the column name with underscores.
    columnName = columnName.replace(" ", "_")
    
    # Set the tag name that will be used for the vertical lines.
    tag = "{}_Mod_{}_HitTo_{}".\
          format(columnName, modulusAmt, moddedHitValue)

    # Add the vertical lines at these timestamps.
    for dt in cycleHitTimestamps:
        PlanetaryCombinationsLibrary.\
            addVerticalLine(pcdd, dt,
                            highPrice, lowPrice, tag, color)

    # Calculate the minimum, maximum and average length of time
    # between the cycle hit timestamps.
    prevDt = None
    currDt = None
    
    minimumDiffTd = None
    maximumDiffTd = None
    averageDiffTd = None
    totalDiffTd = datetime.timedelta(0)
    
    for i in range(len(cycleHitTimestamps)):
        currDt = cycleHitTimestamps[i]

        # We skip calculating the timedelta for the first point
        # because we need two timestamps to calcate the timedelta.
        
        if i != 0 and prevDt != None:
            diffTd = currDt - prevDt

            # Update values if a new minimum or maximum is seen.
            
            if minimumDiffTd == None:
                minimumDiffTd = diffTd
            elif diffTd < minimumDiffTd:
                minimumDiffTd = diffTd
                
            if maximumDiffTd == None:
                maximumDiffTd = diffTd
            elif diffTd > maximumDiffTd:
                maximumDiffTd = diffTd

            # Add the diffTd to the total for the average calculation later.
            totalDiffTd += diffTd
            
        # Update for next iteration.
        prevDt = currDt
        currDt = None

    # Calculate the average.
    if len(cycleHitTimestamps) > 1:

        # Convert the timedelta to seconds.
        totalDiffSecs = \
            (totalDiffTd.microseconds + \
             (totalDiffTd.seconds + (totalDiffTd.days * 24 * 3600)) * 10**6) \
             / 10**6

        # Compute the average.
        averageDiffSec = totalDiffSecs / (len(cycleHitTimestamps) - 1)
        
        log.debug("totalDiffSecs == {}".format(totalDiffSecs))
        log.debug("averageDiffSec == {}".format(averageDiffSec))

        # Turn the average number of seconds to a timedelta.
        averageDiffTd = datetime.timedelta(seconds=averageDiffSec)
    
    # Print information about parameters and cycle hit timestamps that
    # were found.
    log.info("----------------------------------------------------")
    log.info("Ephemeris CSV filename: '{}'".format(inputCsvFilename))
    log.info("Ephemeris CSV data column number:  {}".format(columnNumber))
    log.info("Ephemeris earliest timestamp: {}".\
             format(ephemerisEarliestTimestamp))
    log.info("Ephemeris latest   timestamp: {}".\
             format(ephemerisLatestTimestamp))
    log.info("Modulus amount:    {}".format(modulusAmt))
    log.info("Modded hit value:  {}".format(moddedHitValue))
    log.info("startDt parameter: {}".format(startDt))
    log.info("endDt   parameter: {}".format(endDt))
    log.info("modifyPcddFlag:    {}".format(modifyPcddFlag))
    #log.info("highPrice:        {}".format(highPrice))
    #log.info("lowPrice:         {}".format(lowPrice))
    log.info("Number of cycle hit points: {}".format(len(cycleHitTimestamps)))
    log.info("Smallest timedelta between cycle hit points: {}".\
             format(minimumDiffTd))
    log.info("Largest  timedelta between cycle hit points: {}".\
             format(maximumDiffTd))
    log.info("Average  timedelta between cycle hit points: {}".\
             format(averageDiffTd))
    
    # Print the cycle turn points to debug.
    if printCycleTurnPointsFlag == True:
        log.debug("----------------------------------------------------")
        log.debug("Cycle hit points:")
        log.debug("----------------------------------------------------")
        for dt in cycleHitTimestamps:
            log.debug("{}    {}".format(Ephemeris.datetimeToStr(dt), tag))
        log.debug("----------------------------------------------------")
    
    if modifyPcddFlag == True:
        # Save changes.
        rv = 0
    else:
        # Don't save changes.
        rv = 1

    return rv

##############################################################################
