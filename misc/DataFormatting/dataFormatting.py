#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script creates a single gann-style CSV file of pricebar data,
#   from multiple CSV data files, for a single contract month.
#
# Usage:
#
#   ./dataFormatting.py --help
#   ./dataFormatting.py --version
#
#   ./dataFormatting.py --source-data-dir="/Users/rluu/programming/pricechartingtool/misc/DataFormatting/SB" --contract-letter="N" --output-file="/tmp/SB_N.txt" --earliest-two-digit-year=28
#   
##############################################################################

import sys
import os
import copy

# For parsing command-line options
from optparse import OptionParser  

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# Full path to the directory containing the contract CSV data files.
# This value is obtained via command-line parameter.
sourceDataDirectory = ""

# Contract month.  This is assumed to be the letter in the filename
# that follows the numerical digits in the filename.  
# This value is obtained via command-line parameter.
contractMonth = ""

# Destination output CSV text file.
# This value is obtained via command-line parameter.
destinationFilename = ""

# 2-digit year number of which starts the beggining of time.  This is
# because the year 2000 is represented by 00, and this confuses the
# sort of time when looking at filenames.
# This value is obtained via command-line parameter.
defaultEarliestTwoDigitYear = 28
earliestTwoDigitYear = defaultEarliestTwoDigitYear

# Number of lines of text to skip in the CSV data files.  This is
# usually a header line that just displays what the columns are.
# This value is obtained via command-line parameter.
linesToSkip = 1

# Header line to put as the first line of text in the destination file.
headerLine = "\"Date\",\"Open\",\"High\",\"Low\",\"Close\",\"Volume\",\"OpenInt\""

# Use Windows newlines.
newline = "\r\n"

##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--source-data-dir",
                  action="store",
                  type="str",
                  dest="sourceDataDir",
                  default=None,
                  help="Specify source CSV data directory.  This value should not have a trailing slash.",
                  metavar="<DIR>")

parser.add_option("--contract-letter",
                  action="store",
                  type="str",
                  dest="contractMonth",
                  default=None,
                  help="Specify contract month letter.",
                  metavar="<LETTER>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file.",
                  metavar="<FILE>")

parser.add_option("--earliest-two-digit-year",
                  action="store",
                  type="int",
                  dest="earliestTwoDigitYear",
                  default=defaultEarliestTwoDigitYear,
                  help="Specify the earliest 2-digit year of which starts the beginning of time.  This is needed because the year 2000 is represented by 00 in many filenames given by data providers.  Without this, sort algorithms will get confused.  Default value: {}".format(defaultEarliestTwoDigitYear),
                  metavar="<VALUE>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    sys.exit(0)


if (options.sourceDataDir == None):
    print("Error: Please specify a directory path to the " + \
          "--source-data-dir option.")
    sys.exit(1)
else:
    # Make sure the source data path is good.
    if not os.path.exists(options.sourceDataDir):
        print("Error: Source data directory provided does not exist: {}".\
              format(options.sourceDataDir))
        sys.exit(1)
    if not os.path.isdir(options.sourceDataDir):
        print("Error: Source data directory is not a directory: {}".\
              format(options.sourceDataDir))
        sys.exit(1)

    # Save the value.
    sourceDataDirectory = options.sourceDataDir

    
if (options.contractMonth == None):
    print("Error: Please specify a contract month letter to the " + \
          "--contract-letter option.")
    sys.exit(1)
else:
    if len(options.contractMonth) > 1:
        print("Error: Please specify only 1 letter for the contract month.")
        sys.exit(1)
    elif not options.contractMonth.isalpha():
        print("Error: Non-letter character was specified to contract month.")
        sys.exit(1)
    else:
        # Set it to upper-case value.
        contractMonth = options.contractMonth.upper()
    
if (options.outputFile == None):
    print("Error: Please specify an output filename to the " + \
          "--output-file option.")
    sys.exit(1)
else:
    destinationFilename = options.outputFile

if options.earliestTwoDigitYear != None:
    if not (0 <= options.earliestTwoDigitYear < 100):
        print("Error: Please specify a non-negative number " + \
              "less than 100 to the " + \
              "--earliest-two-digit-year option.")
        sys.exit(1)
    else:
        earliestTwoDigitYear = options.earliestTwoDigitYear

        
##############################################################################


# Sorted list of files in the directory from oldest to newest contract.
sortedListOfFiles = []

for f in os.listdir(sourceDataDirectory):
    fullFilename = sourceDataDirectory + os.sep + f
    #print("DEBUG: Looking at file: {}".format(fullFilename))
    #print("DEBUG: Basename of file is: {}".format(f))
    sortedListOfFiles.append(fullFilename)

#print("DEBUG: sorting list...")
sortedListOfFiles.sort()

#print("DEBUG: sorted list is: ")
#for f in sortedListOfFiles:
#    print("DEBUG: f is: {}".format(f))


# Handle special case where the 2-digit year wraps around 00.
tempList = copy.deepcopy(sortedListOfFiles)
sortedListOfFiles = []
# First put into 'sortedListOfFiles' all the files after the start year.
for f in tempList:
    basename = os.path.basename(f)
    numStr = ""
    for i in range(len(basename)):
        if basename[i].isdigit():
            numStr += basename[i]
    if numStr == "":
        print("Warning: numStr is empty for file: {}".format(f))
    else:
        num = int(numStr)
        #print("DEBUG: num is: {}".format(num))
        if num >= earliestTwoDigitYear:
            #print("DEBUG: appending: {}".format(f))
            sortedListOfFiles.append(f)
            
# Now put into 'sortedListOfFiles' all the files that wrapped around year 2000.
for f in tempList:
    basename = os.path.basename(f)
    numStr = ""
    for i in range(len(basename)):
        if basename[i].isdigit():
            numStr += basename[i]
    if numStr == "":
        print("Warning: numStr is empty for file: {}".format(f))
    else:
        num = int(numStr)
        #print("DEBUG: num is: {}".format(num))
        if num < earliestTwoDigitYear:
            #print("DEBUG: appending: {}".format(f))
            sortedListOfFiles.append(f)

# List 'sortedListOfFiles' now has all the filenames of the source CSV
# data files, in the order we should extract dates and price data.


#print("DEBUG: Before filtering contract month, the files are: ")
#for f in sortedListOfFiles:
#    print("DEBUG: f: {}".format(f))

# Go through the list and remove the ones that aren't in the desired
# contact month.
tempList = copy.deepcopy(sortedListOfFiles)
sortedListOfFiles = []
for f in tempList:
    basename = os.path.basename(f)
    numStr = ""
    foundDigit = False
    for i in range(len(basename)):
        #print("DEBUG: basename[{}]: {}".format(i, basename[i]))
        if basename[i].isdigit():
            foundDigit = True
            numStr += basename[i]
        else:
            if foundDigit == True:
                # This is first letter after finding the numerical
                # digits.  This character should be the contract month letter.
                if basename[i].isalpha() and \
                   basename[i].upper() == contractMonth:

                    #print("DEBUG: found matching contract month.")
                    sortedListOfFiles.append(f)

#print("DEBUG: Using the following files in the following order: ")
#for f in sortedListOfFiles:
#    print("DEBUG: f: {}".format(f))

# List of all the lines that will go into the destination file.
consolidatedDataLines = []
consolidatedDataLines.append(headerLine)

for filename in sortedListOfFiles:
    print("Analyzing file '{}' ...".format(filename))
    with open(filename) as f:
        i = 0
        for line in f:
            if i < linesToSkip:
                #print("DEBUG: Skipping this line (i={}) ...".format(i))
                pass
            else:
                #print("DEBUG: Checking this line (i={}) ...".format(i))
                
                # Check the number of fields.
                fields = line.split(",")
                numFieldsExpected = 7
                if len(fields) != numFieldsExpected:
                    print("Error: Line does not have {} data fields".\
                          format(numFieldsExpected))
                    sys.exit(1)
                    
                dateStr = fields[0] 
                #openStr = fields[1]
                #highStr = fields[2]
                #lowStr = fields[3]
                #closeStr = fields[4]
                #volumeStr = fields[5]
                #openIntStr = fields[6]

                #print("DEBUG: dateStr == {}".format(dateStr))
                
                dateExistsAlready = False
                for l in consolidatedDataLines:
                    if l.startswith(dateStr):
                        #print("DEBUG: dateStr '{}' is old.".\
                        #      format(dateStr))
                        dateExistsAlready = True
                        break
                if dateExistsAlready == False:
                    #print("DEBUG: dateStr '{}' is new.  Adding to list.".\
                    #      format(dateStr))
                    consolidatedDataLines.append(line)
            i += 1

print("Done reading all the files.")
print("Writing to destination file '{}' ...".format(destinationFilename))
                    
# Write to file, truncating if it already exists.
with open(destinationFilename, "w") as f:
    for line in consolidatedDataLines:
        f.write(line.rstrip() + newline)
        
print("Done.")

#    statinfo = os.lstat(fullFilename)
#    self.log.debug("Most recent access time is: {}".\
#                   format(statinfo.st_atime))
#    self.log.debug("Most recent mod time is:    {}".\
#                   format(statinfo.st_atime))
            
