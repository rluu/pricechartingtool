#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script is a helper script to help converting the column
#   letters to column index numbers, and vice versa, in various Excel
#   or LibreOffice spreadsheets.  The column index numbers are
#   0-based, i.e. the first column index is 0.
#
# Usage:
#
#   ./columnLettersToColumnIndex.py --column="A"
#   ./columnLettersToColumnIndex.py --column="AB"
#   ./columnLettersToColumnIndex.py --column="AAA"
#
#   ./columnLettersToColumnIndex.py --column="0"
#   ./columnLettersToColumnIndex.py --column="52"
#   ./columnLettersToColumnIndex.py --column="702"
#
##############################################################################

import sys

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# For logging.
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
#log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    logging.shutdown()
    
    sys.exit(rc)

def getNumberValueForLetter(letter):
    """Returns an int for the letter corresponding to the alphabetic order.
    These values are 1-based.
    
    Thus:

    A --> 1
    B --> 2
    ...
    Z --> 26
    """

    if len(letter) != 1 or letter.isalpha() != True:
        log.error("Invalid argument to getNumberValueForLetter().  " + \
                  "str given was: '{}'".format(letter))
        shutdown(1)

    # Note:
    # In the python3 shell, ord('a') == 97.
    
    value = int(ord(letter.lower()) - 96)

    log.debug("Value returned for letter '{}' is: {}".\
              format(letter.lower(), value))
    
    return value
    
def convertFromLettersToIndexNumber(letters):
    """Converts the given str of letters to a index number that
    corresponds to that column.
    "A" corresponds to "0", "B" corresponds to "1", etc.

    Arguments:
    letters - str value holding one or more letters.

    Returns:
    str value holding the equivalent in index number (0-based).
    If an invalid argument is given, then None is returned.
    """

    # Make sure the input variable 'letters' contains only alphabetic
    # characters and is non-empty.
    if not letters.isalpha():
        log.error("Invalid argument given to " + \
                  "convertFromLettersToIndexNumber().  " + \
                  "str given was: '{}'".format(letters))
        return None

    letters = letters.lower()

    numLettersInAlphabet = 26
    
    currPower = len(letters) - 1

    sumValue = 0

    log.debug("Full str is: {}".format(letters))
    
    for i in range(0, len(letters)):
        
        log.debug("letters[{}] == '{}'".format(i, letters[i]))
        currLetter = letters[i]
        
        valueForCurrLetter = getNumberValueForLetter(currLetter)
        log.debug("valueForCurrLetter == {}".format(valueForCurrLetter))
        
        multiplier = numLettersInAlphabet ** currPower
        log.debug("multiplier == {}".format(multiplier))

        valueToAdd = valueForCurrLetter * multiplier
        log.debug("valueToAdd == {}".format(valueToAdd))

        sumValue += valueToAdd
        log.debug("sumValue == {}".format(sumValue))

        # Update the currPower for the next letter.
        currPower -= 1
    
    # Subtract 1 from the final sum obtained to get the zero-based
    # index number that we want.
    indexValue = sumValue - 1
    
    log.debug("After completing the loop, the index number obtained is: {}".\
              format(indexValue))
    
    return indexValue
    
def convertFromIndexNumberToLetters(value):
    """Converts the given index number to a str containing letters
    that correspond to that index number.

    Arguments:
    value - int value that contains the index number (0-based).

    Returns:
    str - str value containing the letters that correspond to that index
          number.  The letters returned are in uppercase.
    """

    # Return value.  Initialized to empty string.
    letters = ""
    
    numLettersInAlphabet = 26

    if not isinstance(value, int):
        log.error("Invalid argument given to " + \
                  "convertFromIndexNumberToLetters().  " + \
                  "value given was: '{}'".format(value))
        return None
    
    # Add 1 to make it not 0-based, which helps us in our calculations.
    valueRemaining = value + 1
    
    currPower = 1

    
    log.debug("valueRemaining == {}".format(valueRemaining))
    log.debug("currPower == {}".format(currPower))
    
    while valueRemaining > 0:
        divisor = numLettersInAlphabet ** (currPower - 1)
        
        modValue = numLettersInAlphabet ** currPower
        log.debug("modValue == {}".format(modValue))
        
        
        modResult = valueRemaining % modValue
        log.debug("modResult == {}".format(modResult))

        letterValue = modResult // divisor
        log.debug("letterValue == {}".format(letterValue))
        
        # Note:
        # In the python3 shell, ord('a') == 97.
        letter = chr(96 + letterValue).upper()
        log.debug("letter == {}".format(letter))

        # Update our return value by prepending the letter.
        letters = letter + letters
        log.debug("letters == {}".format(letters))

        # Update the valueRemaining.
        valueRemaining -= modResult
        log.debug("valueRemaining == {}".format(valueRemaining))

        # Update the currPower.
        currPower += 1
        log.debug("currPower == {}".format(currPower))
    
    return letters

##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--column",
                  action="store",
                  type="str",
                  dest="columnStr",
                  default=None,
                  help=\
                  "Specify the column letter(s) or column index for " + \
                  "conversion.  Note: Column index numbers are 0-based, " + \
                  "i.e. 0 is the first index.  This argument is required.  ",
                  metavar="<Column letter(s) or column index number>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if options.version == True:
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

if options.columnStr != None:
    columnStr = options.columnStr
    
    # Make sure the input variable 'letters' contains only alphabetic
    # characters and is non-empty.
    if columnStr.isalpha():
        index = convertFromLettersToIndexNumber(columnStr)

        if index != None:
            log.info("Index value for column '{}' is: {}".\
                     format(columnStr, index))
        else:
            # An error message should have already been printed, so
            # just shutdown now.
            shutdown(1)

    elif columnStr.isnumeric():
        letters = convertFromIndexNumberToLetters(int(columnStr))

        if letters != None:
            log.info("Letters for column index number {} is: '{}'".\
                     format(columnStr, letters))
        else:
            # An error message should have already been printed, so
            # just shutdown now.
            shutdown(1)
            
    else:
        log.error("Invalid input given.  " + \
                  "The column str should be all letters, or all numbers.")
        shutdown(1)
else:
    log.error("Please specify an argument to the --column command-line option.")
    shutdown(1)


