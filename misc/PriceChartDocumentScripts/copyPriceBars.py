#!/usr/bin/env python3
##############################################################################
# Script:  copyPriceBars.py
#
# Description:

#   This script takes the following fields related to PriceBars and
#   copies it from the input PriceChartDocument (.pcd) file to the
#   output PriceChartDocument (.pcd) file, overwriting values.
#
#   The PriceChartDocumentData object fields that will be copied are:
#     self.priceBars
#     self.locationTimezone
#     self.priceBarsFileFilename
#     self.priceBarsFileNumLinesToSkip
# 
#   Both the input and output PriceChartDocument files specified must
#   be existing files.
#
# Dependencies:
#   src/ephemeris.py
#   src/data_objects.py
#
# Usage:
# 
#   ./copyPriceBars.py --help
#   ./copyPriceBars.py --version
#
#   ./copyPriceBars.py --input-file=/tmp/input.pcd \
#                      --output-file=/tmp/output.pcd
#
##############################################################################

import sys
import os
import copy
import pickle

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

# For PyQt UI classes.
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# PriceChartDocument (.pcd) file that we are reading from.
# This value is specified via command-line option.
inputPcdFile = ""

# PriceChartDocument (.pcd) file that we are writing to.
# This value is specified via command-line option.
outputPcdFile = ""

# For logging.
#logLevel = logging.DEBUG
logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    Ephemeris.closeEphemeris()
    logging.shutdown()
    sys.exit(rc)

def picklePriceChartDocumentDataToFile(pcdd, filename):
    """Pickles the given PriceChartDocumentData object to the given
    filename.

    Arguments:
    pcdd     - PriceChartDocumentData object to save.
    filename - str holding the full path of the PriceChartDocument (.pcd) file.
    
    Returns:
    True if the write operation succeeded without problems, False otherwise.
    """

    log.debug("Entered picklePriceChartDocumentDataToFile()")

    # Return value.
    rv = True

    priceChartDocumentData = pcdd

    # Pickle to file.
    with open(filename, "wb") as fh:
        try:
            pickle.dump(priceChartDocumentData, fh) 
            rv = True
        except pickle.PickleError as pe:
            log.error("Error while pickling a " +
                      "PriceChartDocumentData to file " + 
                      filename + 
                      ".  Error is: {}".format(pe) +
                      ".  PriceChartDocumentData object " + 
                      "has the following info: " + 
                      priceChartDocumentData.toString())
            rv = False

    log.debug("Exiting picklePriceChartDocumentDataToFile(), " + \
              "rv == {}".format(rv))
    return rv

def unpicklePriceChartDocumentDataFromFile(filename):
    """Un-Pickles a PriceChartDocumentData object from file.

    Arguments:
    filename - str holding the full path of the PriceChartDocument (.pcd) file.
    
    Returns:
    Upon success: PriceChartDocumentData obtained is then returned
    Upon failure: None is returned.
    """

    log.debug("Entered unpicklePriceChartDocumentDataFromFile()")

    # Return value.
    rv = None

    # Get the PriceChartDocumentData from filename.
    try:
        with open(filename, "rb") as fh:
            try:
                priceChartDocumentData = pickle.load(fh)

                # Verify it is a PriceChartDocumentData object.
                if isinstance(priceChartDocumentData, 
                              PriceChartDocumentData) == True:
                    rv = priceChartDocumentData
                else:
                    # Print error message.
                    log.error("Cannot load this object.  " + 
                              "The object unpickled from file " + 
                              filename + " is not a " + 
                              "PriceChartDocumentData.")
                    rv = None
            except pickle.UnpicklingError as upe:
                log.error("Error while unpickling a " +
                          "PriceChartDocumentData from file " + 
                          filename + 
                          ".  Error is: {}".format(upe))
                rv = None
    except IOError as e:
        log.error("IOError while trying to open a file: {}".\
                  format(e))

        rv = None

    #log.debug("rv == {}".format(rv))
    log.debug("Exiting unpicklePriceChartDocumentDataFromFile()")
    
    return rv


##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--input-file",
                  action="store",
                  type="str",
                  dest="inputPcdFile",
                  default=None,
                  help="Specify the PriceChartDocument (.pcd) file " + \
                       "to read PriceBars from.",
                  metavar="<FILE>")

parser.add_option("--output-file",
                  action="store",
                  type="str",
                  dest="outputPcdFile",
                  default=None,
                  help="Specify the PriceChartDocument (.pcd) file " + \
                       "to write PriceBars to.",
                  metavar="<FILE>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

# Get the input pcd filename.
if (options.inputPcdFile == None):
    log.error("Please specify a PriceChartDocument (.pcd) file with " +
              "the --input-file option.")
    shutdown(1)
else:
    log.debug("options.inputPcdFile == {}".format(options.inputPcdFile))
    inputPcdFile = os.path.abspath(options.inputPcdFile)
    log.debug("inputPcdFile == {}".format(inputPcdFile))

    if os.path.exists(inputPcdFile) and os.path.isfile(inputPcdFile):
        log.debug("The inputPcdFile path exists, and it is a file.")
    else:
        log.error("The input PCD file either does not exist or is not a file.")
        shutdown(1)
        
# Get the output pcd filename.
if (options.outputPcdFile == None):
    log.error("Please specify a PriceChartDocument (.pcd) file with " +
              "the --output-file option.")
    shutdown(1)
else:
    log.debug("options.outputPcdFile == {}".format(options.outputPcdFile))
    outputPcdFile = os.path.abspath(options.outputPcdFile)
    log.debug("outputPcdFile == {}".format(outputPcdFile))

    if os.path.exists(outputPcdFile) and os.path.isfile(outputPcdFile):
        log.debug("The outputPcdFile path exists, and it is a file.")
    else:
        log.error("The output PCD file either does not exist or is not a file.")
        shutdown(1)
        
##############################################################################

# Initialize Ephemeris (required).
Ephemeris.initialize()

# Set application details so the we can use QSettings default
# constructor later.
appAuthor = "Ryan Luu"
appName = "PriceChartingTool"
QCoreApplication.setOrganizationName(appAuthor)
QCoreApplication.setApplicationName(appName)

# Create the Qt application.
app = QApplication(sys.argv)
app.setApplicationName(appName)

# Open the input PriceChartDocument file.
log.info("Loading input  PriceChartDocument '{}' ...".format(inputPcdFile))
inputPcdd = unpicklePriceChartDocumentDataFromFile(inputPcdFile)
if inputPcdd == None:
    # Retrieval failed.  An error message should have been logged.
    shutdown(1)

# Open the output PriceChartDocument file.
log.info("Loading output PriceChartDocument '{}' ...".format(outputPcdFile))
outputPcdd = unpicklePriceChartDocumentDataFromFile(outputPcdFile)
if outputPcdd == None:
    # Retrieval failed.  An error message should have been logged.
    shutdown(1)

# Change the fields of outputPcdd.
outputPcdd.priceBars = inputPcdd.priceBars
outputPcdd.locationTimezone = inputPcdd.locationTimezone
outputPcdd.priceBarsFileFilename = inputPcdd.priceBarsFileFilename
outputPcdd.priceBarsFileNumLinesToSkip = inputPcdd.priceBarsFileNumLinesToSkip

# Write to the output file.
log.info("Saving  output PriceChartDocument '{}' ...".format(outputPcdFile))
success = picklePriceChartDocumentDataToFile(outputPcdd, outputPcdFile)

if success == True:
    # Execution completed.
    log.info("Done.")
    shutdown(0)
else:
    # Write failed; the error should have been logged.
    shutdown(1)

##############################################################################
