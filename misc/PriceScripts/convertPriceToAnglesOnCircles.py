#!/usr/bin/env python3
##############################################################################
# File: convertPriceToAnglesOnCircles.py
#
# Description:
#   This script takes a number and converts it to an angle on various circles.
#   The standard circle sizes supported are: 12, 24, 36, 52, 90, 144, and 360.
#   The various angles on the different circles are then printed to stdout.
#
# Usage:
#
#   # This will print the angle on all the default circle sizes.
#   ./convertPriceToAnglesOnCircles.py --price=80.64
#
#   # This will print the angle on a custom circle size(s).
#   ./convertPriceToAnglesOnCircles.py --price=80.64 --circle=3600
#   ./convertPriceToAnglesOnCircles.py --price=39 --circle=3600 --circle=20736
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

##############################################################################
# Global variables.
##############################################################################

# Input price value.
# This value is obtained from command-line arguments.
price = None


# Circle sizes by default.
circleSizes = [12, 24, 36, 52, 90, 144, 360]

# Custom circle sizes.
customCircleSizes = []

# For logging.
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logging.DEBUG)
#log.setLevel(logging.INFO)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    # Close the Ephemeris so it can do necessary cleanups.
    #Ephemeris.closeEphemeris()
    
    logging.shutdown()
    sys.exit(rc)

##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--price",
                  action="store",
                  type="float",
                  dest="price",
                  default=None,
                  help=\
                  "Specify the price for calculations.  " + \
                  "This argument is required.",
                  metavar="<PRICE>")

parser.add_option("--circle",
                  action="append",
                  type="int",
                  dest="customCircleSizes",
                  default=[],
                  help=\
                  "Specify a custom circle size for calculations.",
                  metavar="<INTEGER>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if options.version == True:
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

# Price.
if options.price == None:
    log.error("Please specify a price to the --price option.")
    shutdown(1)
else:
    price = options.price

# Custom circle sizes.
customCircleSizes = options.customCircleSizes


# Do computations.
print("Input price: {}".format(price))
print("")
for circleSize in circleSizes:
    angle = ((price % circleSize) / circleSize) * 360.0
    print("Angle on circle of {:>3}:   {:6.2f}".format(circleSize, angle))

if len(customCircleSizes) != 0:
    print("")
    for circleSize in customCircleSizes:
        angle = ((price % circleSize) / circleSize) * 360.0
        print("Angle on circle of {}:   {:6.2f}".format(circleSize, angle))

print("")

##############################################################################
