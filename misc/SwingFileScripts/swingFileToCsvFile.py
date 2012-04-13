#!/usr/bin/env python3
##############################################################################
# Script:  swingFileToCsvFile.py
#
# Description:
#   Takes a SwingFile (.swg) and outputs most of the fields to a CSV file.
#
# Dependencies:
#   src/ephemeris.py
#   src/data_objects.py
#
# Usage:
# 
#   ./swingFileToCsvFile.py --help
#   ./swingFileToCsvFile.py --version
#
#   ./swingFileToCsvFile.py --swing-file=/tmp/inputSwingFile.swg \
#                           --output-file=swings.csv
#
#   ./swingFileToCsvFile.py --swing-file=/tmp/inputSwingFile.swg \
#                           --print
#
#   ./swingFileToCsvFile.py --swing-file=/tmp/inputSwingFile.swg \
#                           --output-file=swings.csv
#                           --print
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

# For timestamps and timezone information.
import datetime
import pytz

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

from swing import SwingFileData

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# SwingFile (.swg) file that we are reading from.
# This value is specified via command-line option.
swingFile = ""

# Flag that indicates that we should output to stdout.
# This value is specified via command-line option.
printFlag = False

# Output file that is the CSV file.
# This value is specified via command-line option.
outputFile = ""

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

def unpickleSwingFileDataFromFile(filename):
    """Un-Pickles a SwingFileData object from file.

    Arguments:
    filename - str holding the full path of the SwingFile (.swg) file.
    
    Returns:
    Upon success: SwingFileData obtained is then returned
    Upon failure: None is returned.
    """

    log.debug("Entered unpickleSwingFileDataFromFile()")

    # Return value.
    rv = None

    # Get the SwingFileData from filename.
    try:
        with open(filename, "rb") as fh:
            try:
                swingFileData = pickle.load(fh)

                # Verify it is a SwingFileData object.
                if isinstance(swingFileData, 
                              SwingFileData) == True:
                    rv = swingFileData
                else:
                    # Print error message.
                    log.error("Cannot load this object.  " + 
                              "The object unpickled from file " + 
                              filename + " is not a " + 
                              "SwingFileData.")
                    rv = None
            except pickle.UnpicklingError as upe:
                log.error("Error while unpickling a " +
                          "SwingFileData from file " + 
                          filename + 
                          ".  Error is: {}".format(upe))
                rv = None
    except IOError as e:
        log.error("IOError while trying to open a file: {}".\
                  format(e))

        rv = None

    #log.debug("rv == {}".format(rv))
    log.debug("Exiting unpickleSwingFileDataFromFile()")
    
    return rv

def convertSwingFileDataToCsvStr(swingFileData):
    """Takes a SwingFileData and generates a CSV str containing most
    of the swing file data.
    """

    endl = "\r\n"
    
    rv = ""

    rv += "Trading Entity Description: {}".\
          format(swingFileData.tradingEntityDescription) + endl
    #rv += "Swing File Description: {}".\
    #      format(swingFileData.swingFileDescription) + endl
    #rv += "User notes: {}".\
    #      format(swingFileData.userNotes) + endl
    rv += "Source Swing File: {}".\
          format(swingFile) + endl
    #rv += "Source PCD filename: {}".\
    #      format(swingFileData.sourcePcdFilename) + endl
    #rv += "Source PriceBar data filename: {}".\
    #      format(swingFileData.sourcePriceBarDataFilename) + endl

    rv += "jd,day,date,time,timezone,tags,open,high,low,close,volume,oi" + endl

    for pb in swingFileData.priceBars:
        # Field: jd
        rv += "{}".format(Ephemeris.datetimeToJulianDay(pb.timestamp))
        rv += ","

        # Timezone name string, extracted from datetime.tzname().
        # This accounts for the fact that datetime.tzname() can return None.
        datetimeObj = pb.timestamp
        tznameStr = datetimeObj.tzname()
        if tznameStr == None:
            tznameStr = ""
        dayOfWeekStr = datetimeObj.ctime()[0:3]
        offsetStr = \
            Ephemeris.getTimezoneOffsetFromDatetime(datetimeObj)

        # Field: day
        rv += dayOfWeekStr
        rv += ","

        # Field: date
        rv += "{}-{:02}-{:02}".\
              format(datetimeObj.year,
                     datetimeObj.month,
                     datetimeObj.day)
        #rv += "{:02}/{:02}/{}".\
        #      format(datetimeObj.month,
        #             datetimeObj.day,
        #             datetimeObj.year)
        rv += ","

        # Field: time
        rv += "{:02}:{:02}:{:02}".\
              format(datetimeObj.hour,
                     datetimeObj.minute,
                     datetimeObj.second)
        rv += ","

        # Field: timezone.
        rv += "{}{}".format(tznameStr, offsetStr)
        rv += ","

        # Field: tags
        for tag in pb.tags:
            rv += tag + " "
        rv = rv[:-1]
        rv += ","

        # Field: open
        rv += "{}".format(pb.open)
        rv += ","
        
        # Field: high
        rv += "{}".format(pb.high)
        rv += ","
        
        # Field: low
        rv += "{}".format(pb.low)
        rv += ","
        
        # Field: close
        rv += "{}".format(pb.close)
        rv += ","
        
        # Field: volume
        rv += "{}".format(pb.vol)
        rv += ","
        
        # Field: oi
        rv += "{}".format(pb.oi)
        rv += ","


        rv = rv[:-1]
        rv += endl
        
    return rv
    
##############################################################################

if __name__ == "__main__":
    
    # Create the parser
    parser = OptionParser()
    
    # Specify all valid options.
    parser.add_option("-v", "--version",
                      action="store_true",
                      dest="version",
                      default=False,
                      help="Display script version info and author contact.")
    
    parser.add_option("--swing-file",
                      action="store",
                      type="str",
                      dest="swingFile",
                      default=None,
                      help="Specify the SwingFile (.swg) file " + \
                           "to load.",
                      metavar="<FILE>")
    
    parser.add_option("--print",
                      action="store_true",
                      dest="printFlag",
                      default=False,
                      help="Print the swing file's contents as a CSV.")
    
    parser.add_option("--output-file",
                      action="store",
                      type="str",
                      dest="outputFile",
                      default=None,
                      help="Specify an output filename for the CSV file.",
                      metavar="<FILE>")
    
    # Parse the arguments into options.
    (options, args) = parser.parse_args()
    
    # Print version information if the flag was used.
    if (options.version == True):
        print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
        print("By Ryan Luu, ryanluu@gmail.com")
        shutdown(0)
    
    # Get the pcd filename.
    if (options.swingFile == None):
        log.error("Please specify a SwingFile (.swg) file with " +
                  "the --swing-file option.")
        shutdown(1)
    else:
        log.debug("options.swingFile == {}".format(options.swingFile))
        swingFile = os.path.abspath(options.swingFile)
        log.debug("swingFile == {}".format(swingFile))
    
    # Get the print flag.
    printFlag = options.printFlag
    log.debug("printFlag == {}".format(printFlag))
    
    # Get the output filename.
    if (options.outputFile != None):
        log.debug("options.outputFile == {}".format(options.outputFile))
        outputFile = os.path.abspath(options.outputFile)
    else:
        log.debug("outputFile was not specified.")
    
    # Check to make sure either --print or --pcd-file was specified.
    if outputFile == "" and printFlag == False:
        log.error("Please specify either the --print option or " +
                  "the --swing-file option.")
        shutdown(1)
    
    ######################################
    
    # Initialize Ephemeris (required).
    Ephemeris.initialize()
    
    # Open the SwingFile.
    log.info("Loading SwingFile '{}' ...".format(swingFile))
    swingFileData = unpickleSwingFileDataFromFile(swingFile)
    if swingFileData == None:
        # Retrieval failed.  An error message should have been logged.
        shutdown(1)
    
    log.info("Creating CSV str ...")
    
    csvStr = convertSwingFileDataToCsvStr(swingFileData)
    
    # Print the contents if the print flag is set.
    if printFlag == True:
        log.info("Printing CSV ...")
        print(csvStr)
    
    # Write to file.
    if outputFile != "":
        log.info("Writing to output file '{}' ...".format(outputFile))
        with open(outputFile, "w") as f:
            f.write(csvStr)
        log.info("File successfully written.")
    
    # Execution completed.
    log.info("Done.")
    shutdown(0)

##############################################################################
