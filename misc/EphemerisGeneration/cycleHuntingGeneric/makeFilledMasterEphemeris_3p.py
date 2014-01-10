#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This takes a generic ephemeris spreadsheet as produced by
#   makeFilledMasterEphemeris_2p.py and does the work to add certain
#   3-planet combinations, for both geocentric and heliocentric.
#
#   Formula used for both geocentric and heliocentric calculations of
#   3-planet cycles is:
# 
#       (2-planet combination longitude) + (3rd planet longitude).
#
#   Adjustments are required periodically when there is a 'gap' in the
#   calculated value for the planet combination.  These adjustments
#   remove the '360' degree gaps.
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
#      python3 makeFilledMasterEphemeris_3p.py
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

# Input CSV file.  See the BA ACCE5S lesson document for details.
inputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleHuntingGeneric/master_2p_ephemeris_nyc_noon.csv"

# Ouptut CSV file.  This is the CSV file with all the calculations completed, per the homework.  
outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleHuntingGeneric/master_3p_ephemeris_nyc_noon.csv"

# Lines to skip in the input file.
linesToSkip = 1

# Dictionary of planet glyphs.
planetGlyph = \
{
    "Sun"           : "\u2609",
    "Moon"          : "\u263d",
    "Mercury"       : "\u263f",
    "Venus"         : "\u2640",
    "Earth"         : "\u2d32",
    "Mars"          : "\u2642",
    "Jupiter"       : "\u2643",
    "Saturn"        : "\u2644",
    "Uranus"        : "\u2645",
    "Neptune"       : "\u2646",
    "Pluto"         : "\u2647",
    "TrueNorthNode" : "\u260a",
    "Chiron"        : "\u26b7",
    "Isis"          : "\u26b6",
}

# Dictionary for input column values for each planet.
# Cell values in these columns are in range [0, 360).
planetGeocentricLongitudeColumn = \
{
    "Sun"           : 18,
    "Moon"          : 19,
    "Mercury"       : 20,
    "Venus"         : 21,
    "Mars"          : 22,
    "Jupiter"       : 23,
    "Saturn"        : 24,
    "Uranus"        : 25,
    "Neptune"       : 26,
    "Pluto"         : 27,
    "TrueNorthNode" : 28,
    "Chiron"        : 29,
    "Isis"          : 30,
  }

# Dictionary for input column values for each planet.
# Cell values in these columns are in range [0, 360).
planetHeliocentricLongitudeColumn = \
{
    "Mercury" : 55,
    "Venus"   : 56,
    "Earth"   : 57,
    "Mars"    : 58,
    "Jupiter" : 59,
    "Saturn"  : 60,
    "Uranus"  : 61,
    "Neptune" : 62,
    "Pluto"   : 63,
    "Chiron"  : 64,
    "Isis"    : 65,
  }


# Dictionary for input column values for each 2-planet combination.
# Cell values in these columns are in range [0, infinity).
planet2PlanetLongitudeColumn = {}
i = 137
planet2PlanetLongitudeColumn["G.Moon/G.Mercury"] = i
i += 1
planet2PlanetLongitudeColumn["G.Moon/G.Venus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Moon/G.Sun"] = i
i += 1
planet2PlanetLongitudeColumn["G.Moon/G.Mars"] = i
i += 1
planet2PlanetLongitudeColumn["G.Moon/G.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["G.Moon/G.TrueNorthNode"] = i
i += 1
planet2PlanetLongitudeColumn["G.Moon/G.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["G.Moon/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Venus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Sun"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Mars"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.TrueNorthNode"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mercury/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Sun"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Mars"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.TrueNorthNode"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Venus/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.Mars"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.TrueNorthNode"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Sun/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mars/G.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mars/G.TrueNorthNode"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mars/G.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mars/G.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mars/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mars/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Mars/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Jupiter/G.TrueNorthNode"] = i
i += 1
planet2PlanetLongitudeColumn["G.Jupiter/G.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["G.Jupiter/G.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["G.Jupiter/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Jupiter/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Jupiter/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.TrueNorthNode/G.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["G.TrueNorthNode/G.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["G.TrueNorthNode/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.TrueNorthNode/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.TrueNorthNode/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Saturn/G.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["G.Saturn/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Saturn/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Saturn/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Chiron/G.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["G.Chiron/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Chiron/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Uranus/G.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["G.Uranus/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["G.Neptune/G.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Venus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Earth"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Mars"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mercury/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Earth"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Mars"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Venus/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Earth/H.Mars"] = i
i += 1
planet2PlanetLongitudeColumn["H.Earth/H.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["H.Earth/H.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["H.Earth/H.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["H.Earth/H.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Earth/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Earth/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mars/H.Jupiter"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mars/H.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mars/H.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mars/H.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mars/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Mars/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Jupiter/H.Chiron"] = i
i += 1
planet2PlanetLongitudeColumn["H.Jupiter/H.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["H.Jupiter/H.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Jupiter/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Jupiter/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Chiron/H.Saturn"] = i
i += 1
planet2PlanetLongitudeColumn["H.Chiron/H.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Chiron/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Chiron/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Saturn/H.Uranus"] = i
i += 1
planet2PlanetLongitudeColumn["H.Saturn/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Saturn/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Uranus/H.Neptune"] = i
i += 1
planet2PlanetLongitudeColumn["H.Uranus/H.Pluto"] = i
i += 1
planet2PlanetLongitudeColumn["H.Neptune/H.Pluto"] = i
i += 1


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


def doCalculationsForColumns(listOfDataValues,
                             planetCombinationColumn,
                             thirdPlanetColumn):
    """Does a calculation for a 3-planet combination.  This function
    works for both geocentric and heliocentric.

    The generic formula used is:
    
      (2-planet combination longitude) + (3rd planet longitude).

    The result is then placed as text into 'listOfDataValues' in an
    appended column.

    The data in this column is the 3-planet longitude calculation such
    that the values have a 360 degrees added each time the computed
    longitude value crosses 0 from below to above, and 360 degrees
    removed each time the computed longitude value crosses 0 from
    above to below.  That way the formula can work for both geocentric
    and heliocentric.  (i.e. The data values smoothly increase or
    decrease).

    Arguments:
    listOfDataValues - list of lists.  Each item in the list is a row of data.

    planetCombinationColumn - int value holding the column number (index value)
                         of the 2-planet combination.  Input values are
                         read from this column.
    
    thirdPlanetColumn - int value holding the column number (index value)
                         of the 3rd planet.  Input values are
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

        planetCombinationLongitude = \
            float(listOfDataValues[i][planetCombinationColumn])
        thirdPlanetLongitude = \
            float(listOfDataValues[i][thirdPlanetColumn])
        
        log.debug("planetCombinationLongitude == {}".\
                  format(planetCombinationLongitude))
        log.debug("thirdPlanetLongitude == {}".\
                  format(thirdPlanetLongitude))
        
        currCalculatedValue = \
            planetCombinationLongitude + thirdPlanetLongitude
        
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
        listOfDataValues[i].append("{}".format(currCalculatedValue))
        
        # Save the calculated value for the next iteration.
        prevCalculatedValue = currCalculatedValue
        currCalculatedValue = None
        
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
                listOfDataValues.append(dataValues)
                i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)


# Do various planet combinations.
log.info("Doing planet calculations...")



# G.Mercury/G.Venus + G.Sun
columnName = \
    "G." + planetGlyph["Mercury"] + "/" + \
    "G." + planetGlyph["Venus"] + " + " + \
    "G." + planetGlyph["Sun"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Mercury/G.Venus"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Sun"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Mercury/G.Venus + G.Mars
columnName = \
    "G." + planetGlyph["Mercury"] + "/" + \
    "G." + planetGlyph["Venus"] + " + " + \
    "G." + planetGlyph["Mars"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Mercury/G.Venus"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mars"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Venus/G.Sun + G.Mercury
columnName = \
    "G." + planetGlyph["Venus"] + "/" + \
    "G." + planetGlyph["Sun"] + " + " + \
    "G." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Venus/G.Sun"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Venus/G.Sun + G.Mars
columnName = \
    "G." + planetGlyph["Venus"] + "/" + \
    "G." + planetGlyph["Sun"] + " + " + \
    "G." + planetGlyph["Mars"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Venus/G.Sun"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mars"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Venus/G.Mars + G.Mercury
columnName = \
    "G." + planetGlyph["Venus"] + "/" + \
    "G." + planetGlyph["Mars"] + " + " + \
    "G." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Venus/G.Mars"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Sun/G.Mars + G.Mercury
columnName = \
    "G." + planetGlyph["Sun"] + "/" + \
    "G." + planetGlyph["Mars"] + " + " + \
    "G." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Sun/G.Mars"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Sun/G.Mars + G.Venus
columnName = \
    "G." + planetGlyph["Sun"] + "/" + \
    "G." + planetGlyph["Mars"] + " + " + \
    "G." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Sun/G.Mars"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Mars/G.Jupiter + G.Mercury
columnName = \
    "G." + planetGlyph["Mars"] + "/" + \
    "G." + planetGlyph["Jupiter"] + " + " + \
    "G." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Mars/G.Jupiter"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Mars/G.Jupiter + G.Venus
columnName = \
    "G." + planetGlyph["Mars"] + "/" + \
    "G." + planetGlyph["Jupiter"] + " + " + \
    "G." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Mars/G.Jupiter"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Mars/G.Jupiter + G.Sun
columnName = \
    "G." + planetGlyph["Mars"] + "/" + \
    "G." + planetGlyph["Jupiter"] + " + " + \
    "G." + planetGlyph["Sun"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Mars/G.Jupiter"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Sun"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Sun/G.Jupiter + G.Mercury
columnName = \
    "G." + planetGlyph["Sun"] + "/" + \
    "G." + planetGlyph["Jupiter"] + " + " + \
    "G." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Sun/G.Jupiter"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Sun/G.Jupiter + G.Venus
columnName = \
    "G." + planetGlyph["Sun"] + "/" + \
    "G." + planetGlyph["Jupiter"] + " + " + \
    "G." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Sun/G.Jupiter"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Sun/G.Saturn + G.Mercury
columnName = \
    "G." + planetGlyph["Sun"] + "/" + \
    "G." + planetGlyph["Saturn"] + " + " + \
    "G." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Sun/G.Saturn"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Sun/G.Saturn + G.Venus
columnName = \
    "G." + planetGlyph["Sun"] + "/" + \
    "G." + planetGlyph["Saturn"] + " + " + \
    "G." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Sun/G.Saturn"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# G.Sun/G.Saturn + G.Mars
columnName = \
    "G." + planetGlyph["Sun"] + "/" + \
    "G." + planetGlyph["Saturn"] + " + " + \
    "G." + planetGlyph["Mars"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["G.Sun/G.Saturn"]
thirdPlanetColumn = planetGeocentricLongitudeColumn["Mars"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Mercury/H.Venus + H.Earth
columnName = \
    "H." + planetGlyph["Mercury"] + "/" + \
    "H." + planetGlyph["Venus"] + " + " + \
    "H." + planetGlyph["Earth"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Mercury/H.Venus"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Earth"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Mercury/H.Venus + H.Mars
columnName = \
    "H." + planetGlyph["Mercury"] + "/" + \
    "H." + planetGlyph["Venus"] + " + " + \
    "H." + planetGlyph["Mars"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Mercury/H.Venus"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mars"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Venus/H.Earth + H.Mercury
columnName = \
    "H." + planetGlyph["Venus"] + "/" + \
    "H." + planetGlyph["Earth"] + " + " + \
    "H." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Venus/H.Earth"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Venus/H.Earth + H.Mars
columnName = \
    "H." + planetGlyph["Venus"] + "/" + \
    "H." + planetGlyph["Earth"] + " + " + \
    "H." + planetGlyph["Mars"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Venus/H.Earth"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mars"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Venus/H.Mars + H.Mercury
columnName = \
    "H." + planetGlyph["Venus"] + "/" + \
    "H." + planetGlyph["Mars"] + " + " + \
    "H." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Venus/H.Mars"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Venus/H.Mars + H.Earth
columnName = \
    "H." + planetGlyph["Venus"] + "/" + \
    "H." + planetGlyph["Mars"] + " + " + \
    "H." + planetGlyph["Earth"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Venus/H.Mars"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Earth"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Earth/H.Mars + H.Mercury
columnName = \
    "H." + planetGlyph["Earth"] + "/" + \
    "H." + planetGlyph["Mars"] + " + " + \
    "H." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Earth/H.Mars"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Earth/H.Mars + H.Venus
columnName = \
    "H." + planetGlyph["Earth"] + "/" + \
    "H." + planetGlyph["Mars"] + " + " + \
    "H." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Earth/H.Mars"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Mars/H.Jupiter + H.Mercury
columnName = \
    "H." + planetGlyph["Mars"] + "/" + \
    "H." + planetGlyph["Jupiter"] + " + " + \
    "H." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Mars/H.Jupiter"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Mars/H.Jupiter + H.Venus
columnName = \
    "H." + planetGlyph["Mars"] + "/" + \
    "H." + planetGlyph["Jupiter"] + " + " + \
    "H." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Mars/H.Jupiter"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Mars/H.Jupiter + H.Earth
columnName = \
    "H." + planetGlyph["Mars"] + "/" + \
    "H." + planetGlyph["Jupiter"] + " + " + \
    "H." + planetGlyph["Earth"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Mars/H.Jupiter"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Earth"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Earth/H.Jupiter + H.Mercury
columnName = \
    "H." + planetGlyph["Earth"] + "/" + \
    "H." + planetGlyph["Jupiter"] + " + " + \
    "H." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Earth/H.Jupiter"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Earth/H.Jupiter + H.Venus
columnName = \
    "H." + planetGlyph["Earth"] + "/" + \
    "H." + planetGlyph["Jupiter"] + " + " + \
    "H." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Earth/H.Jupiter"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Earth/H.Saturn + H.Mercury
columnName = \
    "H." + planetGlyph["Earth"] + "/" + \
    "H." + planetGlyph["Saturn"] + " + " + \
    "H." + planetGlyph["Mercury"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Earth/H.Saturn"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mercury"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Earth/H.Saturn + H.Venus
columnName = \
    "H." + planetGlyph["Earth"] + "/" + \
    "H." + planetGlyph["Saturn"] + " + " + \
    "H." + planetGlyph["Venus"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Earth/H.Saturn"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Venus"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)

# H.Earth/H.Saturn + H.Mars
columnName = \
    "H." + planetGlyph["Earth"] + "/" + \
    "H." + planetGlyph["Saturn"] + " + " + \
    "H." + planetGlyph["Mars"]
headerLine += "," + columnName
log.info("Calculating data for column: {}".format(columnName))
planetCombinationColumn = planet2PlanetLongitudeColumn["H.Earth/H.Saturn"]
thirdPlanetColumn = planetHeliocentricLongitudeColumn["Mars"]
listOfDataValues = doCalculationsForColumns(listOfDataValues,
                                            planetCombinationColumn,
                                            thirdPlanetColumn)



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
