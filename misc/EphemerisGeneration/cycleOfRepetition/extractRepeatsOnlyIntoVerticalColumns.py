#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This takes as input, an CSV file created by
#   'makeCycleOfRepetitionSpreadsheet.py', and creates another CSV
#   with only the repeat dates and longitude degrees.
#
#   The output CSV file thus will have format as follows:
#
#     <Timestamp>,<Longitude>
#
# Usage steps:
#
#     1) Set the variable for the input file.
#
#     2) Set the variable for the output file.
#
#     5) Run the script.
#
#         python3 extractRepeatsOnlyIntoVerticalColumns.py
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

# Input filename for the CSV file created by
# 'makeCycleOfRepetitionSpreadsheet.py'.
#inputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/CountingWheelsFrom_19060609/H.Mars_180_deg_repeats.csv"
#inputFilename = "/home/rluu/programming/pricechartingtool/doc/research/stocks/TDW/H.Venus_H.Mars_360_deg_repeats.csv"
#inputFilename = "/home/rluu/programming/pricechartingtool/doc/G.Sun_49_degree_repeats_1906_to_1935.csv"
#inputFilename = "/home/rluu/programming/pricechartingtool/doc/G.Sun_49_degree_repeats_1776_to_1935.csv"
#inputFilename = "/home/rluu/programming/pricechartingtool/doc/G.Sun_7_degree_repeats_1776_to_1935.csv"
inputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Earth_49_degree_repeats_to_NYC_Battle.csv"

# Output filename for the output CSV file.
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/CountingWheelsFrom_19060609/H.Mars_180_deg_repeats_only.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/research/stocks/TDW/H.Venus_H.Mars_360_deg_repeats_only.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/G.Sun_49_degree_repeats_1906_to_1935_repeats_only.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/G.Sun_49_degree_repeats_1776_to_1935_repeats_only.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/G.Sun_7_degree_repeats_1776_to_1935_repeats_only.csv"
outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Earth_49_degree_repeats_to_NYC_Battle_repeats_only.csv"

# Lines to skip in the ephemeris input file.
#
# This is set to 1 because the first line contains the headers.  This
# is standard and shouldn't need to change.
linesToSkip = 1

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

# Data values from the first line.
dataValues = None

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
                i += 1
            else:
                # Normal data line.
                dataValues = line.split(",")

                # We only need the first normal data line.
                break
                i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             inputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)

# Format the header line.
headerLineColumns = headerLine.split(",")
if len(headerLineColumns) < 4:
    errStr = "Expected at least 4 columns in the input file.  " + \
             "Perhaps this is an invalid input file?"
    log.error(errStr)
    shutdown(1)
outputHeaderLine = headerLineColumns[0] + "," + headerLineColumns[1] + ","


timestampValues = []
longitudeValues = []

for i in range(len(dataValues)):
    if i % 4 == 0:
        timestampValues.append(dataValues[i])
    elif i % 4 == 1:
        longitudeValues.append(dataValues[i])

if len(timestampValues) != len(longitudeValues):
    errStr = "Mismatch in number of timestamps and number of longitude values."
    log.error(errStr)
    shutdown(1)

# Write to output file.
log.info("Writing to output file: '{}' ...".format(outputFilename))

# Strip off the trailing comma.
if len(outputHeaderLine) > 0:
    outputHeaderLine = outputHeaderLine[:-1]
    
try:
    with open(outputFilename, "w", encoding="utf-8") as f:
        endl = "\n"
        f.write(outputHeaderLine + endl)

        for i in range(len(timestampValues)):
            line = timestampValues[i] + "," + longitudeValues[i] + ","

            # Strip off trailing comma.
            line = line[:-1]
            
            # Write the line to file.
            f.write(line + endl)
            
except IOError as e:
    errStr = "I/O Error while trying to write file '" + \
             outputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)

log.info("Done.")
shutdown(0)

##############################################################################
