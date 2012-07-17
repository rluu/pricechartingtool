#!/usr/bin/env python3
##############################################################################
# Description:
#
# This is a script written for the specific purpose of manipulating
# the ephemeris CSV file used for the TAC System.
#
# This script reads in a CSV file, and then does various operations to
# add fields to the CSV file.  
#
##############################################################################

# Number of lines to skip before reading the data.
linesToSkip = 1

# Delimiter.
delimiter = ","

inputFilename = "TacEphemeris.csv"
outputFilename = "TacEphemeris2.csv"


##############################################################################

import os
import sys 
import errno

##############################################################################

# Lines of text that will go into the output file.
outputFileLines = []
outputFileLines.append("Date,Day,Earth,Mars,Saturn,Mars - Saturn + Earth,(Mars - Saturn + Earth) % 360")


print("Processing input file...")

# Counter for the current line number.
lineNum = 0

with open(inputFilename) as f:
    for line in f:
        if lineNum >= linesToSkip:
            line = line.strip()
            fieldValues = line.split(delimiter)

            # Make a special manual +360 adjustment for Mars, just so
            # the subtraction will come out positive.
            fieldValues[3] = str(float(fieldValues[3]) + 360.0)

            earthLongitude = float(fieldValues[2])
            marsLongitude = float(fieldValues[3])
            saturnLongitude = float(fieldValues[4])
                                
            diffMarsSaturnPlusEarth = \
                marsLongitude - saturnLongitude + earthLongitude
            
            diffMarsSaturnPlusEarthMod360 = diffMarsSaturnPlusEarth % 360
        
            outputLine = fieldValues[0] + "," + \
                         fieldValues[1] + "," + \
                         fieldValues[2] + "," + \
                         fieldValues[3] + "," + \
                         fieldValues[4] + "," + \
                         str(diffMarsSaturnPlusEarth) + "," + \
                         str(diffMarsSaturnPlusEarthMod360)
            
            outputFileLines.append(outputLine)

        # Increment the line number counter.
        lineNum += 1


# Write output file.
print("Writing to output file...")

with open(outputFilename, "wt") as f:
    for line in outputFileLines:
        f.write(line + os.linesep)

print("Done.")

##############################################################################
