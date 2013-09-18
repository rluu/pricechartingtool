#!/usr/bin/python3
##############################################################################
# Description:
#
#   This script takes as input a certain number and returns the angle
#   of that number on the square-of-9 spiral chart.
#   An option is available to specify a custom base-number, which is the
#   number at the center of the spiral.
#
# Note:
#
#   The angle of 0 degrees (+360 degree multiples) is along the odd
#   squares, which is the diagonal where 1, 9, 25, 49, etc. are at.
#   If that is not what is desired, then after the function call,
#   simply add or subtract an offset angle.
#
#   Examples:
#      For a base number of 1:
#         - Number  1 would be at 0 degrees.
#         - Number  9 would be at 360 degrees
#         - Number 25 would be at 720 degrees.
#         - etc.
#
# Usage:
#
#   # This would give result: 1305 degrees (or 3 circles + 225 degrees).
#   ./SqOf9_NumberToAngleConversion.py --number=69
#
#   # This would give result: 2295 degrees (or 6 circles + 135 degrees).
#   ./SqOf9_NumberToAngleConversion.py --number=190
#
#   # This would give result: 675 degrees (or 1 circles + 315 degrees).
#   ./SqOf9_NumberToAngleConversion.py --base-number=44 --number=66
#
##############################################################################

import sys

# For math.floor().
import math

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

##############################################################################

# Global variables.

# Version string.
VERSION = "0.1"

# Base number that is in the center of the square of 9 spiral chart.
# Default value is 1.  Custom values may be set via command-line options.
baseNumber = 1

# Number to obtain the angle of on the square of 9 spiral chart.
# This value is obtained via command-line parameter.
inputNumber = None

# For logging.
logging.basicConfig(level=logging.INFO,
#logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    logging.shutdown()
    sys.exit(rc)


def getAngleForNumberOnSpiral(inputNumber, baseNumber=1):
    """Obtains the angle on the square-of-9 spiral for the given
    'inputNumber' for the spiral starting at 'baseNumber'.

    The angle of 360-degree circles is started along the odd squares,
    which is the diagonal where 1, 9, 25, 49, etc. are at.  If that is
    not what is desired, then after the function call, simply add or
    subtract an offset angle.

    Examples:
      getAngleForNumberOnSpiral(1, 1) would return 0.
      getAngleForNumberOnSpiral(25, 1) would return 720.
      getAngleForNumberOnSpiral(53, 1) would return 1125.
      getAngleForNumberOnSpiral(58, 44) would return 495.

    Input parameters:
      inputNumber - float value for the number to obtain the angle of.
      baseNumber - int value for the number in the center of the spiral.

    Returns:
      float for the angle on the spiral where the number is found.
      The angle of 0 degrees is along the odd squares, which is the diagonal
      where 1, 9, 25, 49, etc. are at.  
    """
    
    # Make a modified input number to account for the offset of the base number.
    modifiedInputNumber = inputNumber - (baseNumber - 1)
    log.debug("modifiedInputNumber == {}".format(modifiedInputNumber))
    
    # First find out what square it is in, and what the first and last
    # numbers of the squares before and after it are.

    # Initialize variables.
    currSquare = 1
    prevSquareLargestNumber = ((1 + (currSquare - 2) * 2) ** 2)
    currSquareLargestNumber = ((1 + (currSquare - 1) * 2) ** 2)
    
    while modifiedInputNumber > currSquareLargestNumber:
        currSquare += 1
    
        prevSquareLargestNumber = ((1 + (currSquare - 2) * 2) ** 2)
        currSquareLargestNumber = ((1 + (currSquare - 1) * 2) ** 2)
    
    # Decrement because we want 1 circle to be 360 degrees from the
    # base number.
    circleNumber = currSquare - 1
    
    # We should have our relevant values for the previous largest square
    # number and the current one.
    
    log.debug("prevSquareLargestNumber (raw) is: {}".\
              format(prevSquareLargestNumber))
    log.debug("currSquareLargestNumber (raw) is: {}".\
             format(currSquareLargestNumber))
    
    log.debug("prevSquareLargestNumber is:       {}".\
          format(prevSquareLargestNumber + baseNumber - 1))
    log.debug("currSquareLargestNumber is:       {}".\
          format(currSquareLargestNumber + baseNumber - 1))
    
    
    diffSquareToSquare = currSquareLargestNumber - prevSquareLargestNumber
    log.debug("diffSquareToSquare == {}".format(diffSquareToSquare))
    
    
    diffInputNumberToPrevSquareLargestNumber = \
        modifiedInputNumber - prevSquareLargestNumber
    log.debug("diffInputNumberToPrevSquareLargestNumber == {}".\
              format(diffInputNumberToPrevSquareLargestNumber))
    
    percentageOfCircle = None
    # Avoiding the divide-by-zero error.
    if diffSquareToSquare != 0:
        if diffInputNumberToPrevSquareLargestNumber == diffSquareToSquare:
            # If these two values are equal, then we have an even
            # multiple of circles, so the left-over is 0.
            percentageOfCircle = 0.0
            circleNumber += 1
        else:
            percentageOfCircle = \
                diffInputNumberToPrevSquareLargestNumber / diffSquareToSquare
    else:
        # This case means that it is number 1 on the first square.
        percentageOfCircle = 0.0
        circleNumber += 1
    
    log.debug("percentageOfCircle == {}".format(percentageOfCircle))

    totalCircles = (circleNumber - 1) + percentageOfCircle
    log.debug("totalCircles == {}".format(totalCircles))

    angleOfNumber = (totalCircles * 360)
    
    log.debug("angleOfNumber == {}".format(angleOfNumber))
    log.debug("angleOfNumber % 360 == {}".format(angleOfNumber % 360))
    
    return angleOfNumber

    
##############################################################################


##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--base-number",
                  action="store",
                  type="int",
                  dest="baseNumber",
                  default=1,
                  help="Specify base number in the center of the Square-of-9 spiral chart.  This is an optional field.  Default value: 1",
                  metavar="<BASE_NUMBER>")

parser.add_option("--number",
                  action="store",
                  type="float",
                  dest="inputNumber",
                  default=None,
                  help="Specify number to obtain the angle degree on the Square-of-9 spiral chart.  This is a required field.",
                  metavar="<VALUE>")


# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print("SqOf9_NumberToAngleConversion.py (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    sys.exit(0)

# Store the base number.
if (options.baseNumber != 1):
    log.info("Using customized base number: {}".format(options.baseNumber))
baseNumber = options.baseNumber
log.debug("baseNumber == {}".format(baseNumber))


# Store the input number.
if (options.inputNumber == None):
    log.error("Error: Please specify a number to the --number option.")
    sys.exit(1)
else:
    inputNumber = options.inputNumber
    log.debug("inputNumber == {}".format(inputNumber))

    
# Do error-checking on the inputNumber and the baseNumber.
if inputNumber < baseNumber:
    log.error("Invalid input number.  " + \
              "Number cannot be less than the base number.")
    shutdown(1)

##############################################################################

# Calculate the angle for the desired number.
angle = getAngleForNumberOnSpiral(inputNumber, baseNumber)

# Calculate angle values for output purposes.
totalCircles = angle / 360
fullCircles = math.floor(angle / 360)
angleMod360 = angle % 360

# Print results.
log.info("Number '{}' in the spiral has angle: {} degrees".\
         format(inputNumber, angle))
log.info("Number '{}' in the spiral has angle: {} circle(s) plus {} degrees".\
         format(inputNumber, fullCircles, angleMod360))
log.info("Number '{}' in the spiral has angle: {} circle(s)".\
         format(inputNumber, totalCircles))


shutdown(0)

##############################################################################
