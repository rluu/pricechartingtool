#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This takes a CSV file that is an ephemeris spreadsheet created by
#   script 'makeFilledMasterEphemeris_3p.py', and starting at a
#   certain column, adds more columns for mod 360 operation and divide
#   360 operation, these two for each original column of planetary data.  
#   The resulting data is then written to an output CSV file.
#
#  
# Usage steps:
#
#     1) Set the variable for the input file.
#
#     2) Set the variable for the output file.
#
#     5) Run the script.
#
#         python3 mod_360_and_div_360.py
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

thisScriptDir = os.path.dirname(os.path.abspath(__file__))

# Input filename for the CSV file created by
# 'makeCycleOfRepetitionSpreadsheet.py'.
#inputFilename = thisScriptDir + os.sep + "master_3p_ephemeris_nyc_noon.csv"
inputFilename = thisScriptDir + os.sep + "master_2p_ephemeris_nyc_noon.csv"

# Output filename for the output CSV file.
#outputFilename = thisScriptDir + os.sep + "master_3p_ephemeris_nyc_noon_with_mod_360_and_div_360.csv"
outputFilename = thisScriptDir + os.sep + "master_2p_ephemeris_nyc_noon_with_mod_360_and_div_360.csv"

# Lines to skip in the ephemeris input file.
#
# This is set to 1 because the first line contains the headers.  This
# is standard and shouldn't need to change.
linesToSkip = 1

# Column index from which to start doing mod 360 and div 360 operations.
startColumnIndexToDoMod360AndDiv360 = 113

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

##############################################################################

# Header line obtained from the input file and then modified.
headerLine = ""

# List holding each column header string.
headerRowDataValues = []

# List of lists.  The lists in this list are the data for each row of
# the ephemeris spreadsheet.
ephemerisRowsDataValues = []

# Read in the input file:
log.info("Reading from input file: '{}' ...".\
         format(inputFilename))
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
                headerRowDataValues = headerLine.split(",")
                i += 1
            else:
                # Normal data line.
                dataValues = line.split(",")

                # Append the list of data for this timestamp.
                ephemerisRowsDataValues.append(dataValues)
                i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)



log.debug("startColumnIndexToDoMod360AndDiv360 == {}".format(startColumnIndexToDoMod360AndDiv360))
#log.debug("headerRowDataValues == {}".format(headerRowDataValues))
log.debug("headerRowDataValues[{}] == {}".format(startColumnIndexToDoMod360AndDiv360, headerRowDataValues[startColumnIndexToDoMod360AndDiv360]))

i = startColumnIndexToDoMod360AndDiv360
while i < len(headerRowDataValues):
    
    columnNameStr = headerRowDataValues[i]

    columnNameMod360Str = columnNameStr + "%360"
    columnNameDiv360Str = columnNameStr + "/360"

    headerRowDataValues.insert(i+1, columnNameMod360Str)
    headerRowDataValues.insert(i+2, columnNameDiv360Str)
    
    for j in range(len(ephemerisRowsDataValues)):
        currFieldStr = ephemerisRowsDataValues[j][i]
        currFieldFloat = float(ephemerisRowsDataValues[j][i])
        
        mod360Value = currFieldFloat % 360
        div360Value = currFieldFloat / 360

        ephemerisRowsDataValues[j].insert(i+1, "{}".format(mod360Value))
        ephemerisRowsDataValues[j].insert(i+2, "{}".format(div360Value))
        
    # Increment to the next column after our inserted columns.
    i += 3


# Write to output file.
log.info("Writing to output file: '{}' ...".format(outputFilename))

try:
    with open(outputFilename, "w", encoding="utf-8") as f:
        endl = "\n"

        # Line to write to file.
        line = ""

        # Assemble the line for the column header.
        for headerField in headerRowDataValues:
            line += headerField + ","

        # Remove trailing comma.
        line = line[:-1]
        
        f.write(line + endl)
        
        # Assemble the lines for each row.
        for dataValueList in ephemerisRowsDataValues:
            line = ""
            for dataValue in dataValueList:
                line += dataValue + ","

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
