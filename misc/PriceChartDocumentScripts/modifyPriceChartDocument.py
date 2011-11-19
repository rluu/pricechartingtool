#!/usr/bin/env python3
##############################################################################
# Script:  modifyPriceChartDocument.py
#
# Description:
#   Modifies a PriceChartDocument (.pcd) file in various ways.
#
# Dependencies:
#   src/ephemeris.py
#   src/data_objects.py
#
# Usage:
# 
#   ./modifyPriceChartDocument.py --help
#   ./modifyPriceChartDocument.py --version
#
#   ./modifyPriceChartDocument.py --pcd-file=/tmp/soybeans.pcd --print
#
#   ./modifyPriceChartDocument.py --pcd-file=/tmp/soybeans.pcd \
#                                 --tag=TAGNAME \
#                                 --script-file=/tmp/add_trine_aspects.py
#
#   ./modifyPriceChartDocument.py --pcd-file=/tmp/soybeans.pcd \
#                                 --tag=TAGNAME \
#                                 --script-file=/tmp/remove.py
#
# Notes:
#
#    The specified script file should have a function called:
#
#    def processPCDD(pcdd, tag):
#        """Modifies the PriceChartDocumentData object's internal artifacts
#        with the given tag.
#
#        Arguments:
#        pcdd - PriceChartDocumentData object that will be modified.
#        tag  - str containing the tag.
#
#        Returns:
#        0 if the changes are to be saved to file.
#        1 if the changes are NOT to be saved to file.
#        """
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
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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

# PriceChartDocument (.pcd) file that we are modifying.
# This value is specified via command-line option.
pcdFile = ""

# Flag that indicates we should print the contents of the
# PriceChartDocument (.pcd) file.
# This value is specified via command-line option.
printFlag = False

# Tag for the artifacts that we are adding, removing, or modifying.
# This value is specified via command-line option.
tag = ""

# Script file to execute for taking action to the PriceChartDocument
# (.pcd) file.  This value is specified via command-line option.
scriptFile = ""

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
    
parser.add_option("--pcd-file",
                  action="store",
                  type="str",
                  dest="pcdFile",
                  default=None,
                  help="Specify the PriceChartDocument (.pcd) file " + \
                       "to modify.",
                  metavar="<FILE>")

parser.add_option("--print",
                  action="store_true",
                  dest="printFlag",
                  default=False,
                  help="Print the contents of the given " + \
                       "PriceChartDocument (.pcd) file.")

parser.add_option("--tag",
                  action="store",
                  type="str",
                  dest="tag",
                  default=None,
                  help="Specify tag str of the artifacts we plan " + \
                       "to manipulate.",
                  metavar="<STRING>")

parser.add_option("--script-file",
                  action="store",
                  type="str",
                  dest="scriptFile",
                  default=None,
                  help="Specify a python3 script file to run on " + \
                       "PriceChartDocument's data.  Note that the " + \
                       "directory where this script lives must have " + \
                       "a __init__.py file in it, so that the file " + \
                       "can be loaded as a module.",
                  metavar="<SCRIPT>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

# Get the pcd filename.
if (options.pcdFile == None):
    log.error("Please specify a PriceChartDocument (.pcd) file with " +
              "the --pcd-file option.")
    shutdown(1)
else:
    log.debug("options.pcdFile == {}".format(options.pcdFile))
    pcdFile = os.path.abspath(options.pcdFile)
    log.debug("pcdFile == {}".format(pcdFile))

# Get the print flag.
printFlag = options.printFlag
log.debug("printFlag == {}".format(printFlag))

# Get the tag.
if (options.tag != None):
    strippedTag = options.tag.strip()
    if strippedTag.find(" ") != -1:
        # Found a space in the tag.
        log.error("The tag should not have any spaces.")
        shutdown(1)
    else:
        # Good, no spaces in the tag.
        tag = strippedTag
        log.debug("tag == {}".format(tag))
        
# Get the script filename.
if (options.scriptFile != None):
    log.debug("options.scriptFile == {}".format(options.scriptFile))
    scriptFile = os.path.abspath(options.scriptFile)

    # Make sure the file exists.
    if not os.path.isfile(scriptFile):
        log.error("Python3 script file '{}'".format(scriptFile) + \
                  " does not exist or it is not a file.")
        shutdown(1)
    
    log.debug("scriptFile == {}".format(scriptFile))
    scriptFileDir = os.path.dirname(scriptFile)
    log.debug("scriptFileDir == {}".format(scriptFileDir))
              
    # Make sure the __init__.py file exists so that it can be loaded
    # as a module.  
    if not os.path.isfile(scriptFileDir + os.sep + "__init__.py"):
        log.error("Python3 script file specified does " + \
                  "not have file '__init__.py' in its directory.")
        shutdown(1)
        
    if scriptFileDir not in sys.path:
        log.debug("scriptFileDir was not in sys.path.  Adding it now...")
        sys.path.insert(0, scriptFileDir)
else:
    log.debug("scriptFile was not specified.")


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

# Open the PriceChartDocument file.
log.info("Loading PriceChartDocument '{}' ...".format(pcdFile))
priceChartDocumentData = unpicklePriceChartDocumentDataFromFile(pcdFile)
if priceChartDocumentData == None:
    # Retrieval failed.  An error message should have been logged.
    shutdown(1)

# Print the contents if the print flag is set.
if printFlag == True:
    log.info("Printing PriceChartDocument data ...")
    print(priceChartDocumentData.toString())

# Run the script file if one was specified.
if scriptFile != "":
    moduleName = os.path.basename(scriptFile)
    if moduleName.endswith(".py") == True and len(moduleName) > 3:
        moduleName = moduleName[:-3]
    log.debug("moduleName == {}".format(moduleName))
    
    # Run the external code module.
    log.info("Loading external code module '{}' ...".format(moduleName))
    importedModule = \
        __import__(moduleName, globals(), locals(), [], 0)
    
    log.info("Running external code module '{}' ...".format(moduleName))
    rc = importedModule.processPCDD(priceChartDocumentData, tag)
    
    log.info("Finished running external code module.")

    # Check the return code of the function from the external code module.
    if rc == 0:
        # Return code 0 means to save changes.
        log.info("Saving changes...")
    
        saveSuccess = \
            picklePriceChartDocumentDataToFile(priceChartDocumentData, pcdFile)

        if saveSuccess == True:
            log.info("Modifications have been saved.")
        else:
            log.error("Saving failed.  " + \
                      "Please see previous error messages for why.")
            shutdown(1)
    elif rc == 1:
        # Return code 1 means do not save changes.
        log.info("Not saving changes.")
    else:
        # Unknown return code.
        log.error("Unknown return code from loaded code module.")
        shutdown(1)

# Execution completed.
log.info("Done.")
shutdown(0)

