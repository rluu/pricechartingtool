#!/usr/bin/env python3
##############################################################################
# Script to convert /home/rluu/download/trading/data/data_CycleTrader/Stocks_ZIP/Stocks/Stocks_Daily_Trading/DJIA_1928_2009_OHLCV.txt to the CSV format we want.
##############################################################################

import sys
import os
import copy

# For logging.
import logging

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""
linesToSkip = 2

inputFile = "/home/rluu/download/trading/data/data_CycleTrader/Wheat_ZIP/Cash/W1890_82.TXT"

outputFile = "/tmp/W1890_82_converted.txt"

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
            fields = line.split("\t")
            numFieldsExpected = 3
            if len(fields) != numFieldsExpected:
                log.error("Line does not have {} data fields".\
                      format(numFieldsExpected))
                shutdown(1)
            
            dateStr = fields[0].strip()
            highStr = fields[1].strip()
            lowStr = fields[2].strip()
            openStr = "{}".format((float(lowStr) + float(highStr)) / 2.0)
            closeStr = "{}".format((float(lowStr) + float(highStr)) / 2.0)
            volumeStr = "0"
            openIntStr = "0"
            
            # Make sure date is the right length.
            if len(dateStr) != 4:
                log.error("dateStr is not the expected number " +
                      "of characters: " + dateStr)
                shutdown(1)
                
            log.debug("dateStr == {}".format(dateStr))
            #monthStr = dateStr[4:6]
            #dayStr = dateStr[6:8]
            #yearStr = dateStr[0:4]
            monthStr = "01"
            dayStr = "01"
            yearStr = dateStr
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

