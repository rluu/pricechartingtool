#!/usr/bin/env python3
##############################################################################
# Script:  createSwingFileFromPcdFile.py
#
# Description:
#   Takes a PriceChartDocument (.pcd) file and extracts the high and
#   low swings from it, based on some given parameters.
#   The results can then either be printed to the screen or written to file.
#
# Dependencies:
#   src/ephemeris.py
#   src/data_objects.py
#
# Usage:
# 
#   ./createSwingFileFromPcdFile.py --help
#   ./createSwingFileFromPcdFile.py --version
#
#   ./createSwingFileFromPcdFile.py --pcd-file=/tmp/soybeans.pcd \
#                                   --output-file=outputSwingFile.swg
#
#   ./createSwingFileFromPcdFile.py --pcd-file=/tmp/soybeans.pcd \
#                                   --print
#
#   ./createSwingFileFromPcdFile.py --pcd-file=/tmp/soybeans.pcd \
#                                   --output-file=outputSwingFile.swg \
#                                   --print
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

from swing import SwingFileData

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# PriceChartDocument (.pcd) file that we are reading from.
# This value is specified via command-line option.
pcdFile = ""

# Flag that indicates that we should output to stdout.
# This value is specified via command-line option.
printFlag = False

# Output file that is the swing file.
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

def processSwingFileData(swingFileData):
    """Processes the given SwingFileData.
    
    What this means in detail is it will scan through the PriceBars in
    the given SwingFileData, looking for relative highs and lows
    within our parameters for a window size, and if the PriceBar is
    determined to be a high or low, then the PriceBar will be tagged
    appropriately.  When this function is complete, the SwingFileData
    will only contain PriceBars that are tagged and deemed to be a
    high or low.  This function will also set the field
    'swingFileDescription' within the given SwingFileData object with
    information about the parameters used to filter out the PriceBar
    highs and lows.
    """

    # TODO: Add a flag and the code needed to implement filtering out highs and lows if they are not sharp enough.  (i.e. Filter out roving turns).
    
    # Parameters used to process the swing file:
    scanVars = []

    # Dictionaries below have the following keys-value fields:
    #
    # "tag": Text string for the tag.  The character 'H' starting the
    #     string indicates a high is being seeked.  The character 'L'
    #     starting the string indicates a low is being seeked.
    #
    # "priceRangeRequired": Percentage required for the range of
    #     PriceBar prices in the scanning window to have in order for
    #     the PriceBar to be able to be tagged as a high or low.
    #     These are percentages with values in the range [0, 1].
    # 
    # "param": The parameter value for 'X' in the following
    #     explanation of how highs and lows are determined.
    # 
    #     A PriceBar is considered a high if the following are true:
    #
    #     1) It has X number of PriceBars with lower or equal prices to it,
    #        coming before the timestamp of the PriceBar.
    #     2) It has X number of PriceBars with lower or equal prices to it.
    #        coming after the timestamp of the PriceBar.
    #  
    #     In case of a tie between PriceBars that are next to each other,
    #     the later bar wins.
    #
    #     A PriceBar is considered a low if the following are true:
    #
    #     1) It has X number of PriceBars with higher or equal prices to it,
    #        coming before the timestamp of the PriceBar.
    #     2) It has X number of PriceBars with higher or equal prices to it.
    #        coming after the timestamp of the PriceBar.
    #  
    #     In case of a tie between PriceBars that are next to each other,
    #     the later bar wins.
    #
    # 'window': List of PriceBars, used as the window for our
    #     scanning.  The PriceBar being evaluated would be the one in
    #     the middle of this list.  The size of the list would thus be
    #     determined with the formula: (2 * param) + 1.
    #
    
    #scanVars.append(\
    #    { "tag" : "H",
    #      "priceRangeRequired" : 0.05,
    #      "param" : 5,
    #      "window" : [] })
    scanVars.append(\
        { "tag" : "HH",
          "priceRangeRequired" : 0.10,
          "param" : 20,
          "window" : [] })
    scanVars.append(\
        { "tag" : "HHH",
          "priceRangeRequired" : 0.20,
          "param" : 30,
          "window" : [] })
    scanVars.append(\
        { "tag" : "HHHH",
          "priceRangeRequired" : 0.25,
          "param" : 80,
          "window" : [] })
    scanVars.append(\
        { "tag" : "HHHHH",
          "priceRangeRequired" : 0.30,
          "param" : 160,
          "window" : [] })

    #scanVars.append(\
    #    { "tag" : "L",
    #      "priceRangeRequired" : 0.05,
    #      "param" : 5,
    #      "window" : [] })
    scanVars.append(\
        { "tag" : "LL",
          "priceRangeRequired" : 0.10,
          "param" : 20,
          "window" : [] })
    scanVars.append(\
        { "tag" : "LLL",
          "priceRangeRequired" : 0.20,
          "param" : 30,
          "window" : [] })
    scanVars.append(\
        { "tag" : "LLLL",
          "priceRangeRequired" : 0.25,
          "param" : 80,
          "window" : [] })
    scanVars.append(\
        { "tag" : "LLLLL",
          "priceRangeRequired" : 0.30,
          "param" : 160,
          "window" : [] })

    scanVarsStr = "["
    for i in range(len(scanVars)):
        scanVar = scanVars[i]
        scanVarsStr += "{}".format(scanVar)
        if i != len(scanVars) - 1:
            scanVarsStr += ","
    scanVarsStr += "]"
    
    # Get the timestamp of the earliest PriceBar.
    earliestPriceBarTimestamp = None
    latestPriceBarTimestamp = None
    if len(swingFileData.priceBars) > 0:
        earliestPriceBarTimestamp = swingFileData.priceBars[0].timestamp
        latestPriceBarTimestamp = swingFileData.priceBars[-1].timestamp
    
    # Before we start doing any tagging ourselves, count how many
    # PriceBars are already tagged.
    count = 0
    originalPriceBarsLen = len(swingFileData.priceBars)
    for pb in swingFileData.priceBars:
        if len(pb.tags) > 0:
            count += 1
        pb.clearTags()
    if count > 0:
        log.warn("Before scanning, tagging, and extracting, " + \
                 "{} out of {} PriceBars already have tags.".\
                 format(count, originalPriceBarsLen))

    log.info("Scanning for highs and lows among {} PriceBars ...".\
             format(originalPriceBarsLen))

    # Start scanning.
    for pb in swingFileData.priceBars:
        log.debug("=============================================")
        log.debug("Looking at PriceBar with timestamp: {}".\
                  format(Ephemeris.datetimeToStr(pb.timestamp)))
        
        for scanVar in scanVars:
            log.debug("---------------------------------------------")
            log.debug("Currently looking at tag: {}".format(scanVar['tag']))
            
            # Calculate the required window size for this scanVar.
            requiredWindowSize = (scanVar['param'] * 2) + 1
            log.debug("requiredWindowSize == {}".format(requiredWindowSize))

            # Alias for the window.
            window = scanVar['window']
            log.debug("Before appending PriceBar, len(window) == {}".\
                      format(len(window)))

            # Index into the window, pointing to the PriceBar
            # currently being inspected for a high or low.
            currIndex = scanVar['param']
            log.debug("currIndex == {}".format(currIndex))

            # Append the PriceBar.
            window.append(pb)
            
            # If the size of the window is now larger than the
            # required size, then shrink it appropriately.
            while len(window) > requiredWindowSize:
                # Drop the PriceBar at the beginning of the window.
                window = window[1:]
            
            # If the size of the window is not large enough, don't do
            # any checks for a high or low yet.
            if len(window) < requiredWindowSize:
                continue
            
            log.debug("For scanVar['tag'] == '{}', len(window) == {}".\
                      format(scanVar['tag'], len(window)))
                      
            # First make sure the price range of these PriceBars is
            # sufficient for this scanVar.
            highPrice = None
            lowPrice = None
            for i in range(len(window)):
                if highPrice == None:
                    highPrice = window[i].high
                if lowPrice == None:
                    lowPrice = window[i].low

                if highPrice <= window[i].high:
                    highPrice = window[i].high
                if lowPrice >= window[i].low:
                    lowPrice = window[i].low
            priceRange = highPrice - lowPrice
            percentage = priceRange / highPrice
            
            if percentage < scanVar['priceRangeRequired']:
                log.debug("Price range not wide enough to warrant " + \
                          "investigating this PriceBar.  " + \
                          "tag=\'{}\', percentage={}, percentageRequired={}".\
                          format(scanVar['tag'],
                                 percentage,
                                 scanVar['priceRangeRequired']))
                
                # Go on to the next scanVar.
                continue
            else:
                log.debug("Price range is wide enough.")
                #log.debug("Price range is wide enough.  " + \
                #          "tag=\'{}\', percentage={}, percentageRequired={}".\
                #          format(scanVar['tag'],
                #                 percentage,
                #                 scanVar['priceRangeRequired']))
                pass

            if scanVar['tag'].startswith("L"):
                # We are looking for a low.
                currIndexIsTheLowest = True
                for i in range(len(window)):
                    log.debug("i == {}, currIndex == {}".format(i, currIndex))
                    if i != currIndex:
                        log.debug("window[i].low         == {}".\
                                  format(window[i].low))
                        log.debug("window[currIndex].low == {}".\
                                  format(window[currIndex].low))
                        if window[i].low < window[currIndex].low:
                            currIndexIsTheLowest = False
                            log.debug("currIndexIsTheLowest == False")
                            break
                if currIndexIsTheLowest == True:
                    log.debug("Checking the next index after currIndex.")
                    # Check the PriceBar after currIndex, to see if it
                    # has a low equal to this one.  If it does, then
                    # currIndex is not a low for our definition.
                    if currIndex + 1 < len(window):
                        log.debug("window[{}].low == {}".\
                                  format(currIndex, window[currIndex].low))
                        log.debug("window[{}].low == {}".\
                                  format(currIndex+1, window[currIndex+1].low))
                        if window[currIndex+1].low <= window[currIndex].low:
                            currIndexIsTheLowest = False
                            log.debug("currIndexIsTheLowest == False")

                # If the PriceBar is still the lowest, then tag it.
                if currIndexIsTheLowest == True:
                    log.debug("Adding tag '{}' to PriceBar with timestamp: {}".\
                              format(scanVar['tag'],
                                     Ephemeris.datetimeToStr(\
                                         window[currIndex].timestamp)))
                    window[currIndex].addTag(scanVar['tag'])
                    log.debug("PriceBar is now: {}".\
                              format(window[currIndex].toString()))
                
            elif scanVar['tag'].startswith("H"):
                # We are looking for a high.
                currIndexIsTheHighest = True
                for i in range(len(window)):
                    log.debug("i == {}, currIndex == {}".format(i, currIndex))
                    if i != currIndex:
                        log.debug("window[i].high         == {}".\
                                  format(window[i].high))
                        log.debug("window[currIndex].high == {}".\
                                  format(window[currIndex].high))
                        if window[i].high > window[currIndex].high:
                            currIndexIsTheHighest = False
                            log.debug("currIndexIsTheHighest == False")
                            break
                if currIndexIsTheHighest == True:
                    log.debug("Checking the next index after currIndex.")
                    # Check the PriceBar after currIndex, to see if it
                    # has a high equal to this one.  If it does, then
                    # currIndex is not a high for our definition.
                    if currIndex + 1 < len(window):
                        log.debug("window[{}].high == {}".\
                                  format(currIndex, window[currIndex].high))
                        log.debug("window[{}].high == {}".\
                                  format(currIndex+1, window[currIndex+1].high))
                        if window[currIndex+1].high >= window[currIndex].high:
                            currIndexIsTheHighest = False
                            log.debug("currIndexIsTheHighest == False")

                # If the PriceBar is still the highest, then tag it.
                if currIndexIsTheHighest == True:
                    log.debug("Adding tag '{}' to PriceBar with timestamp: {}".\
                              format(scanVar['tag'],
                                     Ephemeris.datetimeToStr(\
                                         window[currIndex].timestamp)))
                    window[currIndex].addTag(scanVar['tag'])
                    log.debug("PriceBar is now: {}".\
                              format(window[currIndex].toString()))
                
            else:
                log.warn("Warning, this tag name is not supported.")

    log.debug("Done scanning.")
    
    # Grab all the PriceBars with tags.
    taggedPriceBars = []
    for pb in swingFileData.priceBars:
        if len(pb.tags) > 0:
            debugStr = "PriceBar at {} has the following tags: ".\
                       format(Ephemeris.datetimeToStr(pb.timestamp))
            debugStr += "["
            for i in range(len(pb.tags)):
                debugStr += pb.tags[i]
                if i != len(pb.tags) - 1:
                    debugStr += ","
            debugStr += "]"
            log.debug(debugStr)
            
            taggedPriceBars.append(pb)

    log.info("Scanning for highs and lows complete.")
    log.info("Out of {} PriceBars, {} were extracted and tagged.".\
             format(originalPriceBarsLen, len(taggedPriceBars)))
    
    # Replace swingFileData.priceBars with the list with only tagged PriceBars.
    swingFileData.priceBars = taggedPriceBars

    # Set the string holding the parameters that were used to scan and
    # filter for highs and lows.
    swingFileDescriptionText = \
        "Swing file creation timestamp: {}.  ".\
        format(datetime.datetime.now(tz=pytz.utc)) + \
        "The swings included in this file were extracted from " + \
        "{} PriceBars, starting from {} to {}.  ".\
        format(originalPriceBarsLen,
               Ephemeris.datetimeToStr(earliestPriceBarTimestamp),
               Ephemeris.datetimeToStr(latestPriceBarTimestamp)) + \
        "Total number of PriceBars tagged as highs and lows " + \
        "in this swing file is: {}.  ".\
        format(len(swingFileData.priceBars)) + \
        "The parameters used in scanning and tagging were: " + \
        scanVarsStr

    swingFileData.swingFileDescription = swingFileDescriptionText

    log.debug("swingFileData.swingFileDescription == {}".\
              format(swingFileData.swingFileDescription))
              
    log.debug("Done processing swing file data.")

##############################################################################

def main():
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
                      help="Print the swing file's contents.")
    
    parser.add_option("--output-file",
                      action="store",
                      type="str",
                      dest="outputFile",
                      default=None,
                      help="Specify an output filename for the swing file." + \
                           "  The swing file data is pickled to this file.",
                      metavar="<FILE>")
    
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
    
    # Get the output filename.
    if (options.outputFile != None):
        log.debug("options.outputFile == {}".format(options.outputFile))
        outputFile = os.path.abspath(options.outputFile)
    else:
        log.debug("outputFile was not specified.")
        outputFile = ""
    
    # Check to make sure either --print or --pcd-file was specified.
    if outputFile == "" and printFlag == False:
        log.error("Please specify either the --print option or " +
                  "the --pcd-file option.")
        shutdown(1)
    
    ######################################
    
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
    
    log.info("Creating a new SwingFileData object ...")
             
    # Create SwingFileData object.
    swingFileData = SwingFileData()
    
    log.info("Extracting data from PriceChartDocumentData ...")
             
    # Load the PriceChartDocumentData into it.
    swingFileData.loadPriceChartDocumentData(pcdFile, priceChartDocumentData)
    
    log.info("Processing SwingFileData object for highs and lows ...")
             
    # Process the PriceBars in the SwingFileData object, tagging the
    # highs and lows.
    processSwingFileData(swingFileData)
    
    log.info("Processing complete.")
    
    # Print the contents if the print flag is set.
    if printFlag == True:
        log.info("Printing SwingFileData ...")
        print("Python object toString() output: " + os.linesep)
        print(swingFileData.toString())
    
    # Write to file.
    if outputFile != "":
        log.info("Writing to output file '{}' ...".format(outputFile))
        with open(outputFile, "wb") as f:
            try:
                pickle.dump(swingFileData, f)
                log.info("File successfully written.")
            except pickle.PickleError as pe:
                log.error("Error while pickling a " +
                          "SwingFileData object to file " + 
                          outputFile + 
                          ".  Error is: {}".format(pe) +
                          ".  SwingFileData object " + 
                          "has the following info: " + 
                          swingFileData.toString())
                shutdown(1)
    
    # Execution completed.
    log.info("Done.")
    shutdown(0)

##############################################################################
    
if __name__ == "__main__":
    main()

##############################################################################
