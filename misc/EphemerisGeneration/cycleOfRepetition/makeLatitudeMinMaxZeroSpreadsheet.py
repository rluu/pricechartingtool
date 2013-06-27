#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This takes as input, an ephemeris spreadsheet CSV file as
#   produced by /home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleHuntingGeneric/makeFilledMasterEphemeris_3p.py,
#
#   and extracts the dates for various geocentric declination or
#   heliocentric latitude measurements of each planet.  The days when
#   the planet has a latitude at max negative, max positive, and 0,
#   the timestamps and measurements are extracted and dates placed in
#   an output CSV file.
#
#
# Usage steps:
#
#     1) Open the CSV file that contains the input ephemeris spreadsheet.
#
#     2) Determine which column number (0-based index) of latitude
#     data (for whatever planet) you want to utilize.  Set the global
#     variable for this.
#
#     3) Set other global variables, including outputFilename.
#
#     4) Set the desired output format.  
#
#     5) Run the script.
#
#         python3 makeLatitudeMinMaxZeroSpreadsheet.py
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For timestamps and dates.
import datetime
import pytz

# For logging.
import logging

# For math.floor()
#import math

##############################################################################
# Global variables

# Input ephemeris CSV file.
#
# This should be a CSV file similar to something output by the script
# 'makeFilledMasterEphemeris_3p.py'.
#
#ephemerisInputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleHuntingGeneric/master_3p_ephemeris_nyc_noon.csv"
ephemerisInputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/master_3p_ephemeris_nyc_noon.csv"

# Timezone used in input ephemeris CSV file.
defaultInputFileTimezone = pytz.timezone("US/Eastern")

# Lines to skip in the ephemeris input file.
#
# This is set to 1 because the first line contains the headers.  This
# is standard and shouldn't need to change.
linesToSkip = 1

# Column number for the timestamp, in the input CSV file, that has the
# timestamp in format "YYYY-MM-DD HH:MM" or "YYYY-MM-DD".
ephemerisInputFileTimestampColumn = 0

# Column number (0-based) for the latitudes of various planet(s),
# in the input CSV file.  
#
# Note: Helper script '/home/rluu/programming/pricechartingtool/misc/SpreadsheetColumnLetterNumberConversion/columnLettersToColumnIndex.py' can be used to convert between column letters and column index numbers, but note that this script returns values that are 1-based indexes, so you will need to subtract 1 to get the actual index that is 0-based used for the variable below.
#
ephemerisInputFileLatitudeColumns = []
ephemerisInputFileLatitudeColumns.append(77)  # G.D.Sun
ephemerisInputFileLatitudeColumns.append(78)  # G.D.Moon
ephemerisInputFileLatitudeColumns.append(91)  # G.L.Moon
ephemerisInputFileLatitudeColumns.append(102) # H.L.Mercury
ephemerisInputFileLatitudeColumns.append(103) # H.L.Venus
ephemerisInputFileLatitudeColumns.append(105) # H.L.Mars
ephemerisInputFileLatitudeColumns.append(106) # H.L.Jupiter
ephemerisInputFileLatitudeColumns.append(107) # H.L.Saturn
ephemerisInputFileLatitudeColumns.append(108) # H.L.Uranus
ephemerisInputFileLatitudeColumns.append(109) # H.L.Neptune


# Ouptut CSV file.  
outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/latitudeMinMaxZero.csv"


# Output format choice.  (Set to either 1 or 2).
outputFormat = 1
#outputFormat = 2


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
    #Ephemeris.closeEphemeris()
    
    logging.shutdown()
    
    sys.exit(rc)

def convertTimestampStrToDatetime(timestampStr):
    """Converts a timestamp str from the CSV file to a datetime, and
    returns that datetime object.  If an error occurs in the
    conversion process, then None is returned.
    
    The timestamp str format can be in "YYYY-MM-DD HH:MM" or "YYYY-MM-DD".  

    If the timestamp str is given in the format "YYYY-MM-DD", then this
    function assumes that for a date given, the timestamp will be
    at 12:00 pm (noon).

    Prerequisites:
    'defaultInputFileTimezone' global variable is set to the
    pytz.timezone object used for the timestamp str.
    
    Parameters:
    timestampStr - str input value in the format
                  of "YYYY-MM-DD HH:MM" or "YYYY-MM-DD".  
    
    Return value:
    datetime.datetime object containing the equivalent timestamp.
    None is returned if an error occured during hte conversion process.
    """
    
    # Check input string for correct formatting.
    if len(timestampStr) != len("YYYY-MM-DD") and \
       len(timestampStr) != len("YYYY-MM-DD HH:MM"):
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None
    
    elif timestampStr[4] != "-" or timestampStr[7] != "-":
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None


    yearStr = timestampStr[0:4]
    monthStr = timestampStr[5:7]
    dayStr = timestampStr[8:10]

    hourStr = None
    minuteStr = None

    if len(timestampStr) == len("YYYY-MM-DD HH:MM"):
        hourStr = timestampStr[11:13]
        minuteStr = timestampStr[14:16]
    else:
        hourStr = "12"
        minuteStr = "00"
    
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
            log.error("There is a non-digit hour value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in minuteStr:
        if not letter.isdigit():
            log.error("There is a non-digit minute value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    # Convert the substrings to int values for the parts of the date/time.
    year = int(yearStr)
    month = int(monthStr)
    day = int(dayStr)
    hour = int(hourStr)
    minute = int(minuteStr)
    
    rv = datetime.datetime(year, month, day, hour, minute, \
                           tzinfo=defaultInputFileTimezone)
    
    return rv


def convertTimestampStrToDatetime2(timestampStr):
    """Converts a timestamp str from the CSV file to a datetime, and
    returns that datetime object.  If an error occurs in the
    conversion process, then None is returned.
    
    The timestamp str format can be in "MM/DD/YYYY HH:MM" or "MM/DD/YYYY".  

    If the timestamp str is given in the format "MM/DD/YYYY", then this
    function assumes that for a date given, the timestamp will be
    at 12:00 pm (noon).

    Prerequisites:
    'defaultInputFileTimezone' global variable is set to the
    pytz.timezone object used for the timestamp str.
    
    Parameters:
    timestampStr - str input value in the format
                  of "MM/DD/YYYY HH:MM" or "MM/DD/YYYY".
    
    Return value:
    datetime.datetime object containing the equivalent timestamp.
    None is returned if an error occured during hte conversion process.
    """
    
    # Check input string for correct formatting.
    if len(timestampStr) != len("MM/DD/YYYY") and \
       len(timestampStr) != len("MM/DD/YYYY HH:MM"):
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None
    
    elif timestampStr[2] != "/" or timestampStr[5] != "/":
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None


    monthStr = timestampStr[0:2]
    dayStr = timestampStr[3:5]
    yearStr = timestampStr[6:10]

    hourStr = None
    minuteStr = None

    if len(timestampStr) == len("MM/DD/YYYY HH:MM"):
        hourStr = timestampStr[11:13]
        minuteStr = timestampStr[14:16]
    else:
        hourStr = "12"
        minuteStr = "00"
    
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
            log.error("There is a non-digit hour value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in minuteStr:
        if not letter.isdigit():
            log.error("There is a non-digit minute value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    # Convert the substrings to int values for the parts of the date/time.
    year = int(yearStr)
    month = int(monthStr)
    day = int(dayStr)
    hour = int(hourStr)
    minute = int(minuteStr)
    
    rv = datetime.datetime(year, month, day, hour, minute, \
                           tzinfo=defaultInputFileTimezone)
    
    return rv



##############################################################################

# Holds the header line of the ephemeris input file.  We will use this
# header line in the output file.
headerLine = ""

# List of lists.  Each item in this list is a list containing the
# fields of text of the input ephemeris CSV file.
listOfEphemerisDataValues = []


# Read in the ephemeris input file:
log.info("Reading from ephemeris input file: '{}' ...".\
         format(ephemerisInputFilename))
try:
    with open(ephemerisInputFilename, "r") as f:
        i = 0
        for line in f:
            line = line.strip()
            if line == "":
                # Empty line, do nothing for this line.
                # Go to next line.
                i += 1
            elif i < linesToSkip:
                # Header line.
                headerLine = line
                i += 1
            else:
                # Normal data line.
                dataValues = line.split(",")
                listOfEphemerisDataValues.append(dataValues)
                i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             ephemerisInputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)

# This is a list that contains a list of list of list.  Each item in
# this is the result obtained in the next FOR loop, and which is stored
# into 'resultsList' on each iteration.
resultsForAllPlanets = []


for column in ephemerisInputFileLatitudeColumns:
    # Extract from the headerLine, the header str for the measurement we
    # are obtaining.
    headerStrForPlanetMeasurement = headerLine.split(",")[column]

    # List of historical dates and values.
    # The most recent value is at index -1.
    # The next older value in the history is at index -2.
    # The next older value in the history is at index -3.
    historicalDates = []
    historicalDates.append(None)
    historicalDates.append(None)
    historicalDates.append(None)
    
    historicalValues = []
    historicalValues.append(None)
    historicalValues.append(None)
    historicalValues.append(None)
    
    # Results.  This is a list of list.
    # Each item in this list is a row of data containing the following fields:
    # <Timestamp>,<LatitudeDegree>
    resultsList = []

    headerRow = ["Timestamp", headerStrForPlanetMeasurement]
    resultsList.append(headerRow)

    # Variable holding whatever the previous and current movement was
    # for planet declination/latitude.
    #
    # Possible values:
    #    1 for planet moving from negative to positive declination/latitude.
    #   -1 for planet moving from positive to negative declination/latitude.
    prevDeclinationOrLatitudeMovement = None
    currDeclinationOrLatitudeMovement = None
    
    for i in range(len(listOfEphemerisDataValues)):

        # Row of data values, as a list.
        dataValues = listOfEphemerisDataValues[i]
        
        currDateStr = dataValues[ephemerisInputFileTimestampColumn]
        
        currValue = dataValues[column]
        historicalDates[-1] = currDateStr
        historicalValues[-1] = currValue

        if historicalValues[-2] != None and historicalValues[-3] != None:
            # We have three data points now, and we can do analysis on
            # the latitude.

            lat1 = None
            lat2 = None
            lat3 = None
            
            try:
                lat1 = float(historicalValues[-1])
                lat2 = float(historicalValues[-2])
                lat3 = float(historicalValues[-3])
                
                log.debug("lat3 = {}, lat2 = {}, lat1 = {}".\
                          format(lat3, lat2, lat1))
                
            except ValueError as e:
                errStr = "ValueError encountered while trying to convert " + \
                         "CSV values to float.  " + \
                         "We are on index {} of column {}.".\
                         format(i, column) + \
                         "  Exception: {}".format(str(e))
                log.error(errStr)
                shutdown(1)

            # Determine if the planet is increasing or decreasing in
            # declination/latitude.
            if lat3 <= lat2 <= lat1 and not lat3 == lat2 == lat1:
                # Increasing.
                currDeclinationOrLatitudeMovement = 1
            elif lat3 >= lat2 >= lat1 and not lat3 == lat2 == lat1:
                # Decreasing.
                currDeclinationOrLatitudeMovement = -1
            elif lat3 == lat2 == lat1:
                # Use whatever the previous determination was.  Note
                # that if the previous movement was not determined yet
                # (and thus is None), then the current value will be
                # None also (and that's okay: It just means we haven't
                # determined the direction of movement yet).
                currDeclinationOrLatitudeMovement = \
                    prevDeclinationOrLatitudeMovement

            # See if we changed directions in declination/latitude.
            if currDeclinationOrLatitudeMovement != None and \
                prevDeclinationOrLatitudeMovement != None:

                if currDeclinationOrLatitudeMovement == -1 and \
                    prevDeclinationOrLatitudeMovement == 1:
                    
                    # We just went from increasing to decreasing.
                    dataRow = [historicalDates[-2], historicalValues[-2]]
                    resultsList.append(dataRow)
                
                    log.debug(headerStrForPlanetMeasurement + \
                              " went from increasing to decreasing, at: " + \
                              historicalDates[-2])

                elif currDeclinationOrLatitudeMovement == 1 and \
                    prevDeclinationOrLatitudeMovement == -1:

                    # We just went from decreasing to increasing.
                    dataRow = [historicalDates[-2], historicalValues[-2]]
                    resultsList.append(dataRow)
                    
                    log.debug(headerStrForPlanetMeasurement + \
                              " went from decreasing to increasing, at: " + \
                              historicalDates[-2])

            # See if we passed zero declination/latitude.
            if lat3 < 0 and lat2 < 0 and lat1 >= 0:
                # Crossed from below 0 to above 0.
                dataRow = [historicalDates[-1], historicalValues[-1]]
                resultsList.append(dataRow)

                log.debug(headerStrForPlanetMeasurement + \
                          " crossed from below 0 to above 0, at: " + \
                          historicalDates[-1])

            elif lat3 > 0 and lat2 > 0 and lat1 <= 0:
                # Crossed from above 0 to below 0.
                dataRow = [historicalDates[-1], historicalValues[-1]]
                resultsList.append(dataRow)
                
                log.debug(headerStrForPlanetMeasurement + \
                          " crossed from above 0 to below 0, at: " + \
                          historicalDates[-1])
                
                
        # Update the historical values for the next iteration of the loop.

        # Remove the first item in the list, which is the oldest
        # historical data point.
        historicalDates.pop(-3)
        historicalDates.append(None)
        historicalValues.pop(-3)
        historicalValues.append(None)
    
        # Update the prevDeclinationOrLatitudeMovement for the next iteration.
        prevDeclinationOrLatitudeMovement = currDeclinationOrLatitudeMovement


    # Completed results for this planet.
    resultsForAllPlanets.append(resultsList)



if outputFormat == 1:
    # This is output method 1.
    # For this output method, the CSV file will have 2 columns for each planet,
    # the columns being timestamp and the planet latitude.
    
    
    # Write to output file.
    log.info("Writing to output file: '{}' ...".format(outputFilename))
        
    try:
        with open(outputFilename, "w") as f:
            endl = "\r\n"
    
            done = False
            i = 0
            while not done:
                # Line of text to write to the CSV file.
                line = ""
    
                wroteSomeDataFlag = False
                
                for resultsList in resultsForAllPlanets:
                    if i < len(resultsList):
                        # Still have data for this planet.
                        line += resultsList[i][0] + ", " + \
                                resultsList[i][1] + ","
    
                        wroteSomeDataFlag = True
                    else:
                        # No more data for this planet.  Insert blank fields.
                        line += ",,"
    
                # Strip off the trailing comma.
                line = line[:-1]
                
                f.write(line + endl)
    
                
                if wroteSomeDataFlag == False:
                    done = True
                
                i += 1
                
    except IOError as e:
        errStr = "I/O Error while trying to write file '" + \
                 outputFilename + "':" + os.linesep + str(e)
        log.error(errStr)
        shutdown(1)
    
elif outputFormat == 2:
    # This is output method 2.
    #
    # For this output method, the CSV file will have 3 columns for all
    # the planets.  The columns are:
    #
    # <Timestamp>,<PlanetNameAndMeasurement>,<Latitude>


    # List of list that contains all the planets' data.
    # 
    # Each item in this list is a list of 3 elements, of which holds
    # the information for the 3 columns.
    dataForAllPlanets = []

    # Retrieve data and put it into dataForAllPlanets.
    for resultsList in resultsForAllPlanets:
        planetName = None
        
        for i in range(len(resultsList)):
            timestamp = None
            latitude = None
            
            if i == 0:
                planetName = resultsList[i][1]
            else:
                timestamp = resultsList[i][0]
                latitude = resultsList[i][1]

                dataFields = [timestamp, planetName, latitude]
                dataForAllPlanets.append(dataFields)

    #for row in dataForAllPlanets:
    #    log.info("timestamp={},planet={},lat={}".\
    #              format(row[0], row[1], row[2]))
        
    # Sort the 'dataForAllPlanets' list by timestamp.
    dataForAllPlanets.sort(key=lambda dataList: dataList[0])

    #for row in dataForAllPlanets:
    #    log.info("timestamp={},planet={},lat={}".\
    #              format(row[0], row[1], row[2]))
        
    
    # Write to output file.
    log.info("Writing to output file: '{}' ...".format(outputFilename))
        
    try:
        with open(outputFilename, "w") as f:
            endl = "\r\n"

            headerLine = "<Timestamp>,<PlanetNameAndMeasurement>,<Latitude>,"

            # Remove trailing comma.
            headerLine = headerLine[:-1]

            # Write the first header line.
            f.write(headerLine + endl)

            # Write each row of data.
            for row in dataForAllPlanets:
                line = row[0] + "," + row[1] + "," + row[2] + ","

                # Remove trailing comma.
                line = line[:-1]

                

                f.write(line + endl)
    
    except IOError as e:
        errStr = "I/O Error while trying to write file '" + \
                 outputFilename + "':" + os.linesep + str(e)
        log.error(errStr)
        shutdown(1)
    
log.info("Done.")
shutdown(0)

##############################################################################
