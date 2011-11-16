#!/usr/bin/env python3
##############################################################################
# Script to convert /home/rluu/download/trading/data/data_CycleTrader/Wheat_ZIP/Cash/W1259_82.TXT to the CSV format we want.
##############################################################################

import sys
import os
import copy

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""
linesToSkip = 2

inputFile = "/home/rluu/download/trading/data/data_CycleTrader/Wheat_ZIP/Cash/W1259_82.TXT"

outputFile = "/tmp/Wheat_Annual_England_1259_1938.txt"

# Use Windows newlines.
newline = "\r\n"

##############################################################################

# Lines in the destination file.
convertedLines = []

# Read input file.
with open(inputFile) as f:
    i = 0
    prevPriceStr = "0"
    
    for line in f:
        if i >= linesToSkip:
            
            dateStr = line[0:10]
            priceStr = line[11:].strip()

            # Make sure date is the right length.
            if len(dateStr) != 10:
                print("Error: dateStr is not the expected number " +
                      "of characters: " + dateStr)
                sys.exit(1)
                
            print("DEBUG: dateStr == ***{}***".format(dateStr))
            print("DEBUG: priceStr == ***{}***".format(priceStr))

            monthStr = dateStr[0:2]
            dayStr   = dateStr[3:5]
            yearStr  = dateStr[6:]

            openStr = prevPriceStr
            
            highStr = None
            lowStr = None
            
            if float(priceStr) > float(prevPriceStr):
                lowStr = prevPriceStr
                highStr = priceStr
            else:
                lowStr = priceStr
                highStr = prevPriceStr
            
            closeStr = priceStr
            volumeStr = "0"
            openIntStr = "0"
            
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

            # Save the price for the next iteration.
            prevPriceStr = priceStr
            
        i += 1


# Insert header line.
convertedLines.insert(0, headerLine)

# Write to file, truncating if it already exists.
with open(outputFile, "w") as f:
    for line in convertedLines:
        f.write(line.rstrip() + newline)
        
print("Done.")

