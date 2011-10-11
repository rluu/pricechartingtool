#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script creates/writes a single CSV file of pricebar data,
#   from two or more input CSV data files.  The first file is used,
#   then when there is no more data, the new data from the second file
#   is used.  What is meant here by 'new data' is that the timestamp
#   for each pricebar of data is unique (timestamp hasn't been
#   utilized in all the previously read input files).
#
# Usage:
#
#   ./mergeAndAppendFiles.py --help
#   ./mergeAndAppendFiles.py --version
#
#   ./mergeAndAppendFiles.py --output-file="/tmp/SB_N_consolidated.txt" --input-file="/tmp/SB_N1.txt" --input-file="/tmp/SB_N2.txt"
#
#   ./mergeAndAppendFiles.py --output-file="/tmp/SB_N_consolidated.txt" --input-file="/tmp/SB_N1.txt" --input-file="/tmp/SB_N2.txt" --input-file="/tmp/SB_N3.txt"
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

# List of filenames of CSV data files, in priority usage order.
# This value is set via command-line parameters.
sourceDataFiles = []

# Destination output CSV text file.
# This value is set via command-line parameters.
destinationFilename = ""

# Number of lines of text to skip in the CSV data files.  This is
# usually a header line that just displays what the columns are.
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
    
parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputFile",
                  default=None,
                  help="Specify output CSV file.",
                  metavar="<FILE>")

parser.add_option("--input-file",
                  action="append",
                  type="str",
                  dest="inputFile",
                  default=None,
                  help="Append an input CSV file to the list of files to read.",
                  metavar="<FILE>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    sys.exit(0)

if (options.outputFile == None):
    print("Error: Please specify an output file to the " + \
          "--output-file option.")
    sys.exit(1)
else:
    # Save the value.
    destinationFilename = options.outputFile

if (options.inputFile == None or len(options.inputFile) == 0):
    print("Error: Please specify input file(s) to the " + \
          "--input-file option.")
    sys.exit(1)
else:
    for f in options.inputFile:
        sourceDataFiles.append(f)
    
##############################################################################


# Converts a line of text in the CSV file, to a int number by using
# the timestamp date value.  This function is used to do comparisons
# between lines, by timestamp.
def lineToComparableNumber(line):
    # Check the number of fields.
    fields = line.split(",")
    numFieldsExpected = 7
    if len(fields) != numFieldsExpected:
        return (False, "Line does not have {} data fields".\
                format(numFieldsExpected))

    dateStr = fields[0] 
    openStr = fields[1]
    highStr = fields[2]
    lowStr = fields[3]
    closeStr = fields[4]
    volumeStr = fields[5]
    openIntStr = fields[6]

    dateStrSplit = dateStr.split("/")
    if len(dateStrSplit) != 3:
        print("ERROR: Format of the date was not 'MM/DD/YYYY'.  Line was: {}".\
              format(line))
        sys.exit(1)

    monthStr = dateStrSplit[0]
    dayStr = dateStrSplit[1]
    yearStr = dateStrSplit[2]

    if len(monthStr) != 2:
        print("Month in the date is not two characters long")
        sys.exit(1)
    if len(dayStr) != 2:
        print("Day in the date is not two characters long")
        sys.exit(1)
    if len(yearStr) != 4:
        print("Year in the date is not four characters long")
        sys.exit(1)

    try:
        monthInt = int(monthStr)
        if monthInt < 1 or monthInt > 12:
            print("Month in the date is not between 1 and 12")
            sys.exit(1)
    except ValueError as e:
        print("Month in the date is not a number")
        sys.exit(1)

    try:
        dayInt = int(dayStr)
        if dayInt < 1 or dayInt > 31:
            print("Day in the date is not between 1 and 31")
            sys.exit(1)
    except ValueError as e:
        print("Day in the date is not a number")
        sys.exit(1)

    try:
        yearInt = int(yearStr)
    except ValueError as e:
        print("Year in the date is not a number")
        sys.exit(1)

    numericalValue = int(yearStr + monthStr + dayStr)

    #print("DEBUG: Convert line '{}' to numericalValue: '{}'".\
    #      format(line, numericalValue))
    
    return numericalValue


# Comparison function for a line of text in the CSV files.
# This analyzes the timestamp date value, which is the first field on a line.
def compLines(line1, line2):
    if lineToComparableNumber(line1) < lineToComparableNumber(line2):
        return -1
    elif lineToComparableNumber(line1) > lineToComparableNumber(line2):
        return 1
    else:
        return 0

    
# Converts a cmp= function into a key= function.
def cmp_to_key(mycmp):
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


##############################################################################
        
consolidatedDataLines = []

for filename in sourceDataFiles:
    # Make sure the source data path is good.
    if not os.path.exists(filename):
        print("Error: Path does not exist: {}".format(filename))
        sys.exit(1)
        
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
                        print("DEBUG: dateStr '{}' is old.".\
                              format(dateStr))
                        dateExistsAlready = True
                        break
                if dateExistsAlready == False:
                    print("DEBUG: dateStr '{}' is new.  Adding to list.".\
                          format(dateStr))
                    consolidatedDataLines.append(line)
            i += 1

print("Done reading all the files.")

# Sort the consolidatedDataLines by the timestamp field.
print("Sorting all lines by timestamp...")
consolidatedDataLines.sort(key=cmp_to_key(compLines))

# Prepend header line.
consolidatedDataLines.insert(0, headerLine)

print("Writing to destination file '{}' ...".format(destinationFilename))

# Write to file, truncating if it already exists.
with open(destinationFilename, "w") as f:
    for line in consolidatedDataLines:
        f.write(line.rstrip() + newline)
        
print("Done.")
