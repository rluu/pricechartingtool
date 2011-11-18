#!/usr/bin/env python3
##############################################################################
# Script to convert BeansDMay_1949_2004.txt to the CSV format we want.
##############################################################################

import sys
import os
import copy

# For logging.
import logging

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""
linesToSkip = 1

inputFile = "/home/rluu/study/BeansDMay_1949_2004.txt"

outputFile = "/tmp/BeansDMay_1949_to_2004.txt"

# Use Windows newlines.
newline = "\r\n"

# For logging.
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    logging.shutdown()
    sys.exit(rc)

##############################################################################

# Lines in the destination file.
convertedLines = []

# Read input file.
with open(inputFile) as f:
    i = 0
    for line in f:
        if i >= linesToSkip:

            # Check the number of fields.
            fields = line.split(",")
            numFieldsExpected = 10
            if len(fields) != numFieldsExpected:
                log.error("Line does not have {} data fields".\
                      format(numFieldsExpected))
                shutdown(1)
                    
            dateStr = fields[0].strip()
            openStr = fields[2].strip()
            highStr = fields[3].strip()
            lowStr = fields[4].strip()
            closeStr = fields[5].strip()
            volumeStr = fields[6].strip()
            openIntStr = fields[7].strip()
            
            # Make sure date is the right length.
            if len(dateStr) != 8:
                log.error("dateStr is not the expected number " +
                      "of characters: " + dateStr)
                shutdown(1)
                
            log.debug("dateStr == {}".format(dateStr))

            monthStr = dateStr[4:6]
            dayStr = dateStr[6:8]
            yearStr = dateStr[0:4]
            
            convertedLine = ""
            
            convertedLine += monthStr + "/" + dayStr + "/" + yearStr
            convertedLine += ","
            
            convertedLine += openStr
            convertedLine += ","

            convertedLine += highStr
            convertedLine += ","

            convertedLine += lowStr
            convertedLine += ","

            convertedLine += closeStr
            convertedLine += ","

            convertedLine += volumeStr
            convertedLine += ","

            convertedLine += openIntStr

                        
            convertedLines.append(convertedLine)
            
        i += 1


# Insert header line.
convertedLines.insert(0, headerLine)

# Write to file, truncating if it already exists.
with open(outputFile, "w") as f:
    for line in convertedLines:
        f.write(line.rstrip() + newline)
        
log.info("Done.")
shutdown(0)

