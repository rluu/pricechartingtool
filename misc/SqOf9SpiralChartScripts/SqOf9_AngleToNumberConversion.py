#!/usr/bin/python3
##############################################################################
# Description:
#
#   This script takes as input a certain number of degrees (angle) to
#   increment from the base number, and returns the number at this
#   angle on the square-of-9 spiral chart.  An option is available to
#   specify a custom base-number, which is the number at the center of
#   the spiral.
#
# Note:
#   The angle of 0 degrees (+360 degree multiples) is along the odd
#   squares, which is the diagonal where 1, 9, 25, 49, etc. are at.
#   If that is not what is desired, then before the function call,
#   simply add or subtract an offset angle.
#   
# Usage examples:
#
#   # This will give result: 2
#   ./SqOf9_AngleToNumberConversion.py --degrees=45
#
#   # This will give result: 9
#   ./SqOf9_AngleToNumberConversion.py --degrees=360
#
#   # This will give result: 25
#   ./SqOf9_AngleToNumberConversion.py --degrees=720
#
#   # This will give result: 28
#   # This is the equivalent of 765 degrees from the base number.
#   ./SqOf9_AngleToNumberConversion.py --circles=2 --degrees=45
#
#   # This will give result: 65
#   # This is the equivalent of 1260 degrees (3.5 * 360) from the base number.
#   ./SqOf9_AngleToNumberConversion.py --circles=3.5
#
#   # This will give result: 68
#   ./SqOf9_AngleToNumberConversion.py --base-number=44 --circles=2
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
# This value is obtained via command-line parameter from the degrees
# sum of the values specified to --degrees and --circles options.
inputAngle = 0

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

def getNumberForAngleOnSpiral(inputAngle, baseNumber=1):
    """Obtains the number on the square-of-9 spiral for the given
    'inputAngle' for the spiral starting at 'baseNumber'.

    The angle of 360-degree circles is started along the odd squares,
    which is the diagonal where 1, 9, 25, 49, etc. are at.  If that is
    not what is desired, then before the function call, simply add or
    subtract an offset angle.
    
    Examples:
      getNumberForAngleOnSpiral(0, 1) would return 1.
      getNumberForAngleOnSpiral(720, 1) would return 25.
      getNumberForAngleOnSpiral(1125, 1) would return 53.
      getNumberForAngleOnSpiral(495, 44) would return 58.

    Input parameters:
      inputAngle - float value for the angle to obtain the number of.
      baseNumber - int value for the number in the center of the spiral.

    Returns:
      float for the number on the spiral at the desired angle.
    """

    # For now, we will assume base number of 1.  We will apply offsets
    # to it to use the actual base number at the end of this function.


    # Initialize variables.
    currSquare = 1
    prevSquareLargestNumber = ((1 + (currSquare - 2) * 2) ** 2)
    currSquareLargestNumber = ((1 + (currSquare - 1) * 2) ** 2)

    # Count complete circles up to the inputAngle.  The partial part
    # of the cirlce remaining we will utilize after this step.
    currAngle = 0
    
    while currAngle <= inputAngle:
        currSquare += 1
        
        prevSquareLargestNumber = ((1 + (currSquare - 2) * 2) ** 2)
        currSquareLargestNumber = ((1 + (currSquare - 1) * 2) ** 2)

        currAngle += 360

    # Subtract 360 degrees from the current angle to roll-back the
    # last loop iteration.
    currAngle -= 360
    currSquare -= 1
    
    log.debug("currSquare == {}".format(currSquare))
    log.debug("currAngle == {}".format(currAngle))
    
    # We should have our relevant values for the current largest square
    # number and the prev largest square number.
    
    log.debug("currSquareLargestNumber is: {}".\
              format(currSquareLargestNumber))
    log.debug("prevSquareLargestNumber is: {}".\
              format(prevSquareLargestNumber))
    
    # Decrement because we want 1 circle to be 360 degrees from the
    # base number.
    circleNumber = currSquare - 1
    log.debug("circleNumber == {}".format(circleNumber))
    
    diffSquareToSquare = currSquareLargestNumber - prevSquareLargestNumber
    log.debug("diffSquareToSquare == {}".format(diffSquareToSquare))

    remainingRatioOfCircle = (inputAngle - currAngle) / 360
    log.debug("remainingRatioOfCircle == {}".format(remainingRatioOfCircle))

    amountOverPrevSquare = remainingRatioOfCircle * diffSquareToSquare
    log.debug("amountOverPrevSquare == {}".format(amountOverPrevSquare))

    # Obtain the desired number at the angle.
    # This number is unadjusted for any customized base numbers.
    # We do the adjustments for customized base numbers after this.
    number = prevSquareLargestNumber + amountOverPrevSquare

    # Now we need to adjust the number for non-default base numbers.
    if baseNumber != 1:
        log.debug("Doing adjustments for baseNumber ...")
        log.debug("number (before adjustment) == {}".format(number))
        
        # We used base number of 1, so find the difference between
        # what we should have done and we actually did.
        baseNumberDiff = baseNumber - 1

        # Take this diff and add it to our number to get the actual
        # number that has been adjusted to the baseNumber.
        number += baseNumberDiff
        log.debug("number (after adjustment) == {}".format(number))
    
    log.debug("number == {}".format(number))
    
    return number

    
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

parser.add_option("--degrees",
                  action="store",
                  type="float",
                  dest="degrees",
                  default=0,
                  help="Specify angle to obtain the number of on the Square-of-9 spiral chart.  The value of this parameter is summed with the number of degrees of circles specified to the --circles option to obtain the angle actually desired.  This is an optional field.",
                  metavar="<NUM_DEGREES>")

parser.add_option("--circles",
                  action="store",
                  type="float",
                  dest="circles",
                  default=0,
                  help="Specify number of circles to obtain the number of on the Square-of-9 spiral chart.  The value of this parameter is summed with the number of degrees specified to the --angle option to obtain the angle actually desired.  This is an optional field.",
                  metavar="<NUM_CIRCLES>")


# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print("SqOf9_AngleToNumberConversion.py (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    sys.exit(0)

# Store the base number.
if (options.baseNumber != 1):
    log.info("Using customized base number: {}".format(options.baseNumber))
baseNumber = options.baseNumber
log.debug("baseNumber == {}".format(baseNumber))

# Make sure inputAngle is zero to start with, because we will be adding to it.
inputAngle = 0

# Store the degrees number by adding it to the inputAngle.
inputAngle += options.degrees
log.debug("options.degrees == {}".format(options.degrees))

# Store the circles number by adding it to the inputAngle.
inputAngle += (options.circles * 360)
log.debug("options.circles == {}".format(options.circles))

log.debug("inputAngle == {}".format(inputAngle))
    
# Do error-checking on the inputAngle.
if inputAngle < 0:
    log.error("Invalid input angle.  " + \
              "The angle cannot be less than 0.")
    shutdown(1)

##############################################################################

# Calculate the number for the desired angle.
number = getNumberForAngleOnSpiral(inputAngle, baseNumber)

# Calculate angle values for output purposes.
fullCircles = math.floor(inputAngle / 360)
angleMod360 = inputAngle % 360

# Print results.
log.info("Angle {} degrees (or {} circle(s) plus {} degrees)".\
         format(inputAngle, fullCircles, angleMod360) + \
         " in the spiral has number: {}".\
         format(number))


shutdown(0)

##############################################################################
