#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This takes a generic ephemeris spreadsheet as produced by
#   createGenericEphemerisSpreadsheet.py and does the work to add
#   2-planet combinations, for both geocentric and heliocentric.
#
#   Formula used for both geocentric and heliocentric calculations of
#   2-planet cycles is:
# 
#       (faster planet) + 360 - (slower planet).
#
#   Adjustments are required periodically when there is a 'gap' in
#   the calculated value for the planet combination.
#
#   This script will also calculate the Moon synodic month phases.
#   The moon phases are values in the range: [1, 30].
#
# Usage:
#
#   1) As long as there have been no modifications to the script that
#   produces the input CSV file, then the Global Variables are correct
#   by default.  Otherwise, the variables will need to be tweaked so
#   that it corresponds correctly with the input CSV file, and the
#   columns in that file.
#
#   2) Simply run the script from the directory:
#
#      python3 makeFilledMasterEphemeris_2p_moon_synodic_30_phases.py
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For dates.
#import datetime

# For logging.
import logging

# For math.floor()
#import math

##############################################################################
# Global variables

thisScriptDir = os.path.dirname(os.path.abspath(__file__))

# Input CSV file.  
inputFilename = thisScriptDir + os.sep + "sun_moon_node_ephemeris_nyc.csv"

# Ouptut CSV file.  
outputFilename = thisScriptDir + os.sep + "moon_synodic_30_phases_ephemeris_nyc.csv"

# Number of moon phases.
numMoonPhases = 30

# Lines to skip in the input file.
linesToSkip = 1

# Dictionary for input column values for each planet.
# Cell values in these columns are in range [0, 360).
planetGeocentricLongitudeColumn = \
{
    "Sun"           : 8,
    "Moon"          : 9,
    "TrueNorthNode" : 10,
  }

# Dictionary for input column values for each planet.
# Cell values in these columns are in range [0, 360).
planetHeliocentricLongitudeColumn = \
{
}


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


def doCalculationsForColumn(listOfDataValues,
                            planetColumn):
    """Calculations for single-planet movement.  This method can work for
    both geocentric and heliocentric planet longitude.
    The data values computed are for a column of data in the spreadsheet.
    
    The data in this column is the planet longitude such that the
    values have a 360 degrees added each time the longitude crosses 0 from
    below to above, and 360 degrees removed each time the longitude crosses
    0 from above to below.  That way the formula can work for both
    geocentric and heliocentric longitudes.

    The calculated value is placed as text into 'listOfDataValues' in an
    appended column.

    Arguments:
    listOfDataValues - list of lists.  Each item in the list is a row of data.

    planetColumn - int value holding the column number (index value)
                   of the planet to do calculations for.  Input values are
                   read from this column.
    
    Returns:
    Reference to the modified 'listOfDataValues'.
    """
    
    # Holds the calculated value for the previous row.
    # This is needed so we can determine if we crossed 360 degrees,
    # and in what direction we crossed it.
    prevCalculatedValue = None
    
    # Values increasing or decreasing day to day, should not exceed this value.
    maximumIncrement = 330

    
    for i in range(len(listOfDataValues)):

        log.debug("Curr timestamp is: {}".format(listOfDataValues[i][0]))
        
        planetLongitude = float(listOfDataValues[i][planetColumn])
        
        log.debug("planetLongitude == {}".format(planetLongitude))
        
        currCalculatedValue = planetLongitude
        
        log.debug("prevCalculatedValue == {}".format(prevCalculatedValue))
        log.debug("currCalculatedValue == {}".format(currCalculatedValue))
        
        # See if we need to make any adjustments to the calculated value.
        if prevCalculatedValue == None:
            # No need for any adjustment.
            pass
            
        elif prevCalculatedValue < currCalculatedValue - maximumIncrement:
            # Adjustment required.
            while prevCalculatedValue < currCalculatedValue - maximumIncrement:
                currCalculatedValue -= 360.0
            
        elif prevCalculatedValue >= currCalculatedValue + maximumIncrement:
            # Adjustment required.
            while prevCalculatedValue >= currCalculatedValue + maximumIncrement:
                currCalculatedValue += 360.0

        else:
            # Adjustment not required.
            pass

        log.debug("After adj.: prevCalculatedValue == {}".\
                  format(prevCalculatedValue))
        log.debug("After adj.: currCalculatedValue == {}".\
                  format(currCalculatedValue))
        

        # Any required adjustments should have now been made.
        
        # Store the result as text.
        listOfDataValues[i].append("{:.3f}".format(currCalculatedValue))
        
        # Save the calculated value for the next iteration.
        prevCalculatedValue = currCalculatedValue
        currCalculatedValue = None
        
    return listOfDataValues

    
def doCalculationsForColumns(listOfDataValues,
                             fasterPlanetColumn,
                             slowerPlanetColumn):
    """Does a calculation for a 2-planet combination.  This function
    works for both geocentric and heliocentric.

    The generic formula used is:
    
      (faster planet) + 360 - (slower planet).

    The result is then placed as text into 'listOfDataValues' in an
    appended column.

    The data in this column is the 2-planet longitude calculation such
    that the values have a 360 degrees added each time the computed
    longitude value crosses 0 from below to above, and 360 degrees
    removed each time the computed longitude value crosses 0 from
    above to below.  That way the formula can work for both
    geocentric and heliocentric.

    Arguments:
    listOfDataValues - list of lists.  Each item in the list is a row of data.

    fasterPlanetColumn - int value holding the column number (index value)
                         of the faster-moving planet.  Input values are
                         read from this column.
    
    slowerPlanetColumn - int value holding the column number (index value)
                         of the faster-moving planet.  Input values are
                         read from this column.
    
    Returns:
    Reference to the modified 'listOfDataValues'.
    """
    
    # Holds the calculated value for the previous row.
    # This is needed so we can determine if we crossed 360 degrees,
    # and in what direction we crossed it.
    prevCalculatedValue = None
    
    # Values increasing or decreasing day to day, should not exceed this value.
    maximumIncrement = 330


    
    for i in range(len(listOfDataValues)):

        log.debug("Curr timestamp is: {}".format(listOfDataValues[i][0]))
        
        fasterPlanetLongitude = float(listOfDataValues[i][fasterPlanetColumn])
        slowerPlanetLongitude = float(listOfDataValues[i][slowerPlanetColumn])

        log.debug("fasterPlanetLongitude == {}".format(fasterPlanetLongitude))
        log.debug("slowerPlanetLongitude == {}".format(slowerPlanetLongitude))
        
        currCalculatedValue = \
            fasterPlanetLongitude + 360 - slowerPlanetLongitude
        
        log.debug("prevCalculatedValue == {}".format(prevCalculatedValue))
        log.debug("currCalculatedValue == {}".format(currCalculatedValue))
        
        # See if we need to make any adjustments to the calculated value.
        if prevCalculatedValue == None:
            # No need for any adjustment.
            pass
            
        elif prevCalculatedValue < currCalculatedValue - maximumIncrement:
            # Adjustment required.
            while prevCalculatedValue < currCalculatedValue - maximumIncrement:
                currCalculatedValue -= 360.0
            
        elif prevCalculatedValue >= currCalculatedValue + maximumIncrement:
            # Adjustment required.
            while prevCalculatedValue >= currCalculatedValue + maximumIncrement:
                currCalculatedValue += 360.0

        else:
            # Adjustment not required.
            pass

        log.debug("After adj.: prevCalculatedValue == {}".\
                  format(prevCalculatedValue))
        log.debug("After adj.: currCalculatedValue == {}".\
                  format(currCalculatedValue))
        

        # Any required adjustments should have now been made.
        
        # Store the result as text.
        listOfDataValues[i].append("{:.3f}".format(currCalculatedValue))
        
        # Save the calculated value for the next iteration.
        prevCalculatedValue = currCalculatedValue
        currCalculatedValue = None
        
    return listOfDataValues

def doMod360ForColumn(listOfDataValues,
                      planetColumn):
    """Applies a modulus 360 operation on the column provided as
    input, and places the calculated result as text into
    'listOfDataValues' in an appended column.

    Arguments:
    listOfDataValues - list of lists.  Each item in the list is a row of data.

    planetColumn - int value holding the column number (index value)
                   of the planet to do calculations for.  Input values are
                   read from this column.
    
    Returns:
    Reference to the modified 'listOfDataValues'.
    """
    
    for i in range(len(listOfDataValues)):

        log.debug("Curr timestamp is: {}".format(listOfDataValues[i][0]))
        
        planetLongitude = float(listOfDataValues[i][planetColumn])
        
        log.debug("planetLongitude == {}".format(planetLongitude))
        
        currCalculatedValue = planetLongitude % 360

        # Store the result as text.
        listOfDataValues[i].append("{:.3f}".format(currCalculatedValue))
        
    return listOfDataValues

    
def doMoonPhaseCalculationForColumn(listOfDataValues,
                                    planetColumn):
    """Calculates the moon phase based on the value in the
    "G.Moon/G.Sun" column.  The calculated value is then placed as
    text into 'listOfDataValues' in an appended column.

    Arguments:
    listOfDataValues - list of lists.  Each item in the list is a row of data.

    planetColumn - int value holding the column number (index value)
                   of the planet to do calculations for.  Input values are
                   read from this column.
    
    Returns:
    Reference to the modified 'listOfDataValues'.
    """
    
    for i in range(len(listOfDataValues)):

        log.debug("Curr timestamp is: {}".format(listOfDataValues[i][0]))
        
        planetLongitude = float(listOfDataValues[i][planetColumn])
        
        log.debug("planetLongitude == {}".format(planetLongitude))

        # Number of degrees per G.Moon phase.
        numDegreesPerMoonPhase = 360 / numMoonPhases

        ## New moon is labeled "1":
        #currCalculatedValue = \
        #    round((planetLongitude % 360) / numDegreesPerMoonPhase) + 1

        # New moon is labeled 'numMoonPhases', and
        # full moon is labeled 'numMoonPhases / 2'.
        currCalculatedValue = \
            round((planetLongitude % 360) / numDegreesPerMoonPhase)
        if currCalculatedValue == 0:
            currCalculatedValue = numMoonPhases
        
        # Store the result as text.
        listOfDataValues[i].append("{}".format(currCalculatedValue))
        
    return listOfDataValues

    
##############################################################################

# Holds the header line of the input file.  We will use this header
# line in the output file.
headerLine = ""

# List of lists.  Each item in this list is a list containing the
# fields of text of the input CSV file.
listOfDataValues = []


# Read in the input file:
log.info("Reading from input file: '{}' ...".format(inputFilename))
try:
    with open(inputFilename, "r") as f:
        i = 0
        for line in f:
            line = line.strip()
            if line == "":
                # Empty line, do nothing for thi sline.
                # Go to next line.
                i += 1
            elif i < linesToSkip:
                # Header line.
                headerLine = line
                i += 1
            else:
                # Normal data line.
                dataValues = line.split(",")
                listOfDataValues.append(dataValues)
                i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)


# Do each planet combination.
log.info("Doing planet calculations...")

# G.Moon
columnName = "G.Moon"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetColumn = planetGeocentricLongitudeColumn["Moon"]
listOfDataValues = doCalculationsForColumn(listOfDataValues,
                                           planetColumn)

# G.Sun
columnName = "G.Sun"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetColumn = planetGeocentricLongitudeColumn["Sun"]
listOfDataValues = doCalculationsForColumn(listOfDataValues,
                                           planetColumn)

# G.TrueNorthNode
columnName = "G.TrueNorthNode"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetColumn = planetGeocentricLongitudeColumn["TrueNorthNode"]
listOfDataValues = doCalculationsForColumn(listOfDataValues,
                                           planetColumn)

# G.Moon/G.Sun
columnName = "G.Moon/G.Sun"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
fasterPlanetColumn = planetGeocentricLongitudeColumn["Moon"]
slowerPlanetColumn = planetGeocentricLongitudeColumn["Sun"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            fasterPlanetColumn,
                                            slowerPlanetColumn)

# G.Moon/G.Sun % 360.
columnName = "G.Moon/G.Sun % 360"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetColumn = len(headerLine.split(",")) - 2     # Previous column.
listOfDataValues = doMod360ForColumn(listOfDataValues,
                                     planetColumn)

# G.Moon_Synodic_Month_Phase
columnName = "G.Moon_Synodic_Month_Phase"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetColumn = len(headerLine.split(",")) - 2     # Previous column.
listOfDataValues = doMoonPhaseCalculationForColumn(listOfDataValues,
                                                   planetColumn)

# G.Moon/G.TrueNorthNode
columnName = "G.Moon/G.TrueNorthNode"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
fasterPlanetColumn = planetGeocentricLongitudeColumn["Moon"]
slowerPlanetColumn = planetGeocentricLongitudeColumn["TrueNorthNode"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            fasterPlanetColumn,
                                            slowerPlanetColumn)

# G.Moon/G.TrueNorthNode % 360.
columnName = "G.Moon/G.TrueNorthNode % 360"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetColumn = len(headerLine.split(",")) - 2     # Previous column.
listOfDataValues = doMod360ForColumn(listOfDataValues,
                                     planetColumn)

# G.Sun/G.TrueNorthNode
columnName = "G.Sun/G.TrueNorthNode"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
fasterPlanetColumn = planetGeocentricLongitudeColumn["Sun"]
slowerPlanetColumn = planetGeocentricLongitudeColumn["TrueNorthNode"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            fasterPlanetColumn,
                                            slowerPlanetColumn)

# G.Sun/G.TrueNorthNode % 360.
columnName = "G.Sun/G.TrueNorthNode % 360"
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetColumn = len(headerLine.split(",")) - 2     # Previous column.
listOfDataValues = doMod360ForColumn(listOfDataValues,
                                     planetColumn)


# Write to output file.
log.info("Writing to output file: '{}' ...".format(outputFilename))
try:
    with open(outputFilename, "w", encoding="utf-8") as f:
        endl = "\n"
        f.write(headerLine + endl)
        
        for rowData in listOfDataValues:
            line = ""
            for i in range(len(rowData)):
                line += rowData[i] + ","

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
