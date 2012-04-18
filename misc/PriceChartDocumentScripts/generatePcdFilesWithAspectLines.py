#!/usr/bin/env python3
##############################################################################
# Script:  generatePcdFilesWithAspectLines.py
#
# Description:
#
#   This script reads a PriceChartDocument (.pcd) file, and from that
#   data, generates PriceChartDocument files with aspect lines
#   (PriceBarChart graphics items) in them.  The files are placed in
#   the directory provided on the command-line, and each file contains
#   aspect lines for a certain set of aspects.
#
# Dependencies:
#   src/astrologychart.py
#   src/data_objects.py
#   src/ephemeris.py
#
# Usage:
# 
#   ./generatePcdFilesWithAspectLines.py --help
#   ./generatePcdFilesWithAspectLines.py --version
#
#   ./generatePcdFilesWithAspectLines.py \
#                         --input-file=/tmp/soybeans.pcd \
#                         --output-directory=/tmp/soybeans_aspect_pcd_files
#
##############################################################################

import sys
import os
import copy
import pickle

# For parsing command-line options
from optparse import OptionParser  

# For Process, Queue, current_process, freeze_support
import  multiprocessing

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
customScriptsDir = thisScriptDir + os.sep + "customScripts"
if customScriptsDir not in sys.path:
    sys.path.insert(0, customScriptsDir)
    
from astrologychart import AstrologyUtils
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene

# Holds functions for adding artifacts for various aspects.
from planetaryCombinationsLibrary import PlanetaryCombinationsLibrary

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# Number of processes to use to do the processing.
# This value is specified via command-line option.
numProcesses = 1

# PriceChartDocument (.pcd) input file that is used as the
# template for the newly created PriceChartDocument files with aspects.
# This value is specified via command-line option.
inputFile = ""

# Output directory that will contain the generated CSV files.
# This value is specified via command-line option.
outputDirectory = ""

# Queues.
taskQueue = multiprocessing.Queue()
resultQueue = multiprocessing.Queue()

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

    global taskQueue
    global numProcesses
    
    Ephemeris.closeEphemeris()

    # Tell spawned processes to end.
    for i in numProcesses:
        taskQueue.put("STOP")
    
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

def ensureDirectoryExists(dirPath):
    """Ensures that the given path is a directory exists.
    If the path does not exist, then a directory for it is created.
    If the path exists but is not a directory, an error is reported and
    shutdown(1) is called.
    """
    
    # Check to see if the outputDirectory exists already.
    if os.path.exists(outputDirectory):
        # Directory outputDirectory exists.
        
        # See if it is a directory.
        if os.path.isdir(outputDirectory):
            log.debug("outputDirectory exists, and is a directory.")
        else:
            log.debug("outputDirectory exists, but is not a directory.")
            log.error("The output directory specified exists " + \
                      "but is not a directory.  " + \
                      "Please specify a path that is not an existing file.")
            shutdown(1)
    else:
        # Create the outputDirectory since it does not exist yet.
        log.debug("outputDirectory does not exist.  Creating it ...")
        
        try:
            os.makedirs(outputDirectory)
        except OSError as e:
            # EEXIST can happen if a directory is created between the
            # time we do the first check for it and when we try to
            # create the directory.  If it is not errno.EEXIST, then
            # we want to report the error.
            if e.errno != errno.EEXIST:
                log.error("Caught an OSError exception " + \
                          "while trying to create the output directory: {}".\
                          format(e))
                shutdown(1)


def worker(taskQueue, resultQueue):
    """Function run by worker processes.  This basically calls
    functions in the taskQueue, and puts the result in resultQueue.
    If the str 'STOP' is encountered in teh taskQueue, then the worker
    stops processing tasks in the taskQueue.
    
    Arguments:
    
    taskQueue - multiprocessing.Queue object holding a queue of
                tuples, which are: (function, (args)).  The queue can
                also have the str 'STOP', which will cause the worker
                to halt processing anymore tasks in the taskQueue.

    resultQueue - multiprocessing.Queue object holding a queue of results.
                  Each result is a tuple with the following values:
                  (PriceChartDocumentData, int, str)
    """
    
    for func, args in iter(taskQueue.get, 'STOP'):
        result = func(*args)
        resultQueue.put(result)
    
def getHighestLowestEarliestLatestPriceBarPricesAndTimestamps(pcdd, self):
    """Goes through all the PriceBars, finding the highest price,
    lowest price, earliest timestamp, and latest timestamp of all the
    PriceBars.  These values are returned.
    
    Arguments:
    pcdd - PriceBarChartDocument that has all the pricebars to search through.
    
    Returns:

    Tuple of the highest price, lowest price, earliest timestamp and
    latest timestamp, among all the PriceBars:
    (float, float, datetime.datetime, datetime.datetime)
    """

    lowestPrice = None
    highestPrice = None
    earliestTimestamp = None
    latestTimestamp = None

    for pb in pcdd.priceBars:
        if lowestPrice == None:
            lowestPrice = pb.low
        elif pb.low < lowestPrice:
            lowestPrice = pb.low
            
        if highestPrice == None:
            highestPrice = pb.high
        elif pb.high > highestPrice:
            highestPrice = pb.high
            
        if earliestTimestamp == None:
            earliestTimestamp = pb.timestamp
        elif pb.timestamp < earliestTimestamp:
            earliestTimestamp = pb.timestamp

        if latestTimestamp == None:
            latestTimestamp = pb.timestamp
        elif pb.timestamp > latestTimestamp:
            latestTimestamp = pb.timestamp
        
        
    return (lowestPrice, highestPrice, earliestTimestamp, latestTimestamp)

def getColorForPlanetParamsList(planetParamsList):
    """Returns a QColor from the given planet params list."""

    # Return value.
    color = None
    
    if planetParamsList != None:
        planetName = planetParamsList[0]
        planetColor = \
            AstrologyUtils.getForegroundColorForPlanetName(planetName)
        color = planetColor
    
    return color
    
def processAspectsCalculationTask(pcdd,
                                  planet1ParamsList,
                                  planet2ParamsList,
                                  aspectGroup):
    """Processes the aspects, calculating where they are and adding
    chart artifacts to the PriceChartDocumentData 'pcdd' object.

    Returns:
    Tuple containing:
    (PriceChartDocumentData, int, str)

    Where:
    PriceChartDocumentData - The modified 'pcdd' object with artifacts added.
    int - The number of artifacts added.
    str - String containing the suggested filename basename when
          saving this PriceChartDocumentData object.
    """
    
    # Make a deep copy of the pcdd and the artifacts to ensure that
    # the modifications are to a unique object.
    pcddArtifacts = copy.deepcopy(pcdd.priceBarChartArtifacts)
    pcdd = copy.deepcopy(pcdd)
    pcdd.priceBarChartArtifacts = pcddArtifacts

    # Keep a count of number of artifacts added.
    numArtifactsAdded = 0

    # Determine what the lowest price, highest price, earliest
    # timestamp, and latest timestamp is, among all the PriceBars in
    # the pcdd.
    (lowestPrice, highestPrice, earliestTimestamp, latestTimestamp) = \
        getHighestLowestEarliestLatestPriceBarPricesAndTimestamps(pcdd)

    # Set the values to variables that we will use to call functions
    # when creating pricebarchart artifacts.
    lowPrice = lowestPrice
    highPrice = highestPrice + (highestPrice * 0.1)
    startDt = earliestTimestamp - datetime.timedelta(days=90)
    endDt = latestTimestamp + datetime.timedelta(days=2*365)
    
    for aspect in aspectGroup:
        degreeDifference = aspect

        # Get the timestamps of the aspect.
        timestamps = \
            PlanetaryCombinationsLibrary.getLongitudeAspectTimestamps(\
            pcdd, startDt, endDt,
            planet1ParamsList,
            planet2ParamsList,
            degreeDifference,
            uniDirectionalAspectsFlag)

        # Get the tag str for the aspect.
        tag = \
            PlanetaryCombinationsLibrary.getTagNameForLongitudeAspect(\
            planet1ParamsList,
            planet2ParamsList,
            degreeDifference,
            uniDirectionalAspectsFlag)

        # Get the color to apply.
        color = getColorForPlanetParamsList(planet1ParamsList)
        
        # Draw the aspects.
        for dt in timestamps:
            PlanetaryCombinationsLibrary.addVerticalLine(\
                pcdd, dt, highPrice, lowPrice, tag, color)
            numArtifactsAdded += 1

    # Create a str for the proposed filename basename of this modified
    # PriceChartDocumentData object.
    basename = ""
    if len(aspectGroup) == 1:
        tag = \
            PlanetaryCombinationsLibrary.getTagNameForLongitudeAspect(\
            planet1ParamsList,
            planet2ParamsList,
            degreeDifference,
            uniDirectionalAspectsFlag)

        basename = tag + ".pcd"

    elif len(aspectGroup) > 1:
        stepSize = aspectGroup[1] - aspectGroup[0]
        degreeDifference = stepSize
        
        # Get the tag str for the aspect step size.
        tag = \
            PlanetaryCombinationsLibrary.getTagNameForLongitudeAspect(\
            planet1ParamsList,
            planet2ParamsList,
            degreeDifference,
            uniDirectionalAspectsFlag)

        # Here to create the basename, we will use the tag, but with an 'x'
        # added after the degree aspect size number.
        searchStr = "_DegreeAspect_"
        degreeAspectStrPos = tag.find(searchStr)
        if degreeAspectStrPos != -1:
            # Find the position of the first "_" before the searchStr.
            underscorePos = tag.rfind("_", start=0, end=degreeAspectStrPos)

            if underscorePos != -1:
                # Finally, assemble what we want the basename to be,
                # from pieces of the tag.
                basename = tag[0:underscorePos] + \
                      "_{}x".format(degreeDifference) + \
                      tag[degreeAspectStrPos:] + \
                      ".pcd"
            else:
                log.warn("Couldn't find the str '_' before str " + \
                         "'{}' in the tag '{}'."
                         format(searchStr, tag))
                basename = tag + ".pcd"

        else:
            log.warn("Couldn't find the str '{}' in the tag '{}'.".\
                     format(searchStr, tag))
            basename = tag + ".pcd"
    else:
        log.warn("There are aspects are in this aspectGroup.")
        basename = "UNCHANGED.pcd"
        
    log.debug("Setting basename to str '{}'".format(basename))

    # All the values for the result has now been obtained.
    # Return the result tuple.
    return (pcdd, numArtifactsAdded, basename)
    

##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--num-processes",
                  action="store",
                  type="int",
                  dest="numProcesses",
                  default=None,
                  help="Set the number of processes used.  " + \
                  "Default value is the number of CPUs in the system.")

parser.add_option("--input-file",
                  action="store",
                  type="str",
                  dest="inputFile",
                  default=None,
                  help="Specify the input PriceChartDocument (.pcd) file " + \
                       "used as the template for generated files.",
                  metavar="<FILE>")

parser.add_option("--output-directory",
                  action="store",
                  type="str",
                  dest="outputDirectory",
                  default=None,
                  help="Specify a directory to place the output files " + \
                  "into.  This can be a directory that exists already " + \
                  "or one that does not yet exist.",
                  metavar="<DIRECTORY>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if (options.version == True):
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

# Get the number of processes to use.
if options.numProcesses != None and options.numProcesses <= 0:
    log.error("Invalid number of processes specified.  " + \
              "Please specificy an int value greater than 0.")
    shutdown(1)
elif options.numProcesses == None:
    # No value was specified, so use the default, which is the number
    # of CPUs on the system. 
    numProcesses = multiprocessing.cpu_count()
else:
    # Value was specified, so use that.
    numProcesses = options.numProcesses
log.debug("numProcesses == {}".format(numProcesses))

# Get the inputFile filename.
if (options.inputFile == None):
    log.error("Please specify a input PriceChartDocument (.pcd) file with " +
              "the --input-file option.")
    shutdown(1)
else:
    log.debug("options.inputFile == {}".format(options.inputFile))
    inputFile = os.path.abspath(options.inputFile)
    log.debug("inputFile == {}".format(inputFile))

# Get the output directory.
if (options.outputDirectory != None):
    log.debug("options.outputDirectory == {}".\
              format(options.outputDirectory))
    outputDirectory = os.path.abspath(options.outputDirectory)
    log.debug("outputDirectory == {}".\
              format(outputDirectory))
    log.debug("os.path.dirname(outputDirectory) == {}".\
              format(os.path.dirname(outputDirectory)))
else:
    log.error("Please specify an output directory to " +
              "the --output-directory option.")
    shutdown(1)
    

##############################################################################

# Add support for when a program which uses multiprocessing to be
# frozen to produce a Windows executable. (Supported for py2exe,
# PyInstaller and cx_Freeze.)
freeze_support()

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

log.info("Setting processing parameters ...")

# Astrological house system for getting the house cusps.
houseSystem = Ephemeris.HouseSys['Porphyry']

# List of planet names that are utilized in astrology aspect calculations.
planetNames = []
#planetNames.append("H1")
#planetNames.append("H2")
#planetNames.append("H3")
#planetNames.append("H4")
#planetNames.append("H5")
#planetNames.append("H6")
#planetNames.append("H7")
#planetNames.append("H8")
#planetNames.append("H9")
#planetNames.append("H10")
#planetNames.append("H11")
#planetNames.append("H12")
#planetNames.append("ARMC")
#planetNames.append("Vertex")
#planetNames.append("EquatorialAscendant")
#planetNames.append("CoAscendant1")
#planetNames.append("CoAscendant2")
#planetNames.append("PolarAscendant")
#planetNames.append("HoraLagna")
#planetNames.append("GhatiLagna")
#planetNames.append("MeanLunarApogee")
#planetNames.append("OsculatingLunarApogee")
#planetNames.append("InterpolatedLunarApogee")
#planetNames.append("InterpolatedLunarPerigee")
planetNames.append("Sun")
planetNames.append("Moon")
planetNames.append("Mercury")
planetNames.append("Venus")
planetNames.append("Earth")
planetNames.append("Mars")
planetNames.append("Jupiter")
planetNames.append("Saturn")
planetNames.append("Uranus")
planetNames.append("Neptune")
planetNames.append("Pluto")
#planetNames.append("MeanNorthNode")
#planetNames.append("TrueSouthNode")
planetNames.append("TrueNorthNode")
#planetNames.append("TrueSouthNode")
#planetNames.append("Ceres")
#planetNames.append("Pallas")
#planetNames.append("Juno")
#planetNames.append("Vesta")
planetNames.append("Isis")
#planetNames.append("Nibiru")
planetNames.append("Chiron")
#planetNames.append("Gulika")
#planetNames.append("Mandi")
#planetNames.append("MeanOfFive")
#planetNames.append("CycleOfEight")
#planetNames.append("AvgMaJuSaUrNePl")
#planetNames.append("AvgJuSaUrNe")
#planetNames.append("AvgJuSa")

# List of centricity types utilized.
centricityTypes = []
centricityTypes.append("geocentric")
#centricityTypes.append("topocentric")
centricityTypes.append("heliocentric")

# List of zodiac longitude types used.
longitudeType = []
longitudeType.append("tropical")
longitudeType.append("sidereal")

# Flag that indicates that aspects are unidirectional.
uniDirectionalAspectsFlag = False

# List of list of aspects.
aspectGroupLists = []

# Square group.
aspectGroup = []
step = 90
start = 0
stop = 180
degreeDiff = start
while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    aspectGroup.append(degreeDiff)
    degreeDiff += step
aspectGroupLists.append(aspectGroup)

# Semi-square group.
aspectGroup = []
step = 45
start = 0
stop = 180
degreeDiff = start
while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    aspectGroup.append(degreeDiff)
    degreeDiff += step
aspectGroupLists.append(aspectGroup)

# Trine group.
aspectGroup = []
step = 120
start = 0
stop = 180
degreeDiff = start
while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    aspectGroup.append(degreeDiff)
    degreeDiff += step
aspectGroupLists.append(aspectGroup)

# Quintile group.
aspectGroup = []
step = 360 / 5.0
start = 0
stop = 180
degreeDiff = start
while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    aspectGroup.append(degreeDiff)
    degreeDiff += step
aspectGroupLists.append(aspectGroup)

# Septile group.
aspectGroup = []
step = 360 / 7.0
start = 0
stop = 180
degreeDiff = start
while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    aspectGroup.append(degreeDiff)
    degreeDiff += step
aspectGroupLists.append(aspectGroup)

# Conjunctions and oppositions.
aspectGroup = []
step = 180
start = 0
stop = 180
degreeDiff = start
while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    aspectGroup.append(degreeDiff)
    degreeDiff += step
aspectGroupLists.append(aspectGroup)

# Conjunctions.
aspectGroup = []
step = 360
start = 0
stop = 180
degreeDiff = start
while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    aspectGroup.append(degreeDiff)
    degreeDiff += step
aspectGroupLists.append(aspectGroup)

# List of tasks
tasks = []

# Submit tasks to the task queue.
log.info("Submitting tasks to queues ...")

# Here a task is submitted for each possible combination of planets
# and aspects.
for i in range(len(planetNames)):
    for j in range(len(planetNames)):
        for k in range(len(centricityTypes)):
            for l in range(len(centricityTypes)):
                for m in range(len(longitudeTypes)):
                    for n in range(len(longitudeTypes)):
                        planet1Name = planetNames[i]
                        planet2Name = planetNames[j]
                        planet1CentricityType = centricityTypes[k]
                        planet2CentricityType = centricityTypes[l]
                        planet1LongitudeType = longitudeTypes[k]
                        planet2LongitudeType = longitudeTypes[l]

                        # If all three are the same between the two
                        # planets, then continue on, otherwise,
                        # process it.
                        if planet1Name == planet2Name and \
                           planet1CentricityType == planet2CentricityType and \
                           planet1LongitudeType == planet2LongitudeType:

                            continue

                        planet1ParamsList = \
                            [(planet1Name,
                              planet1CentricityType,
                              planet1LongitudeType)]
                        planet2ParamsList = \
                            [(planet2Name,
                              planet2CentricityType,
                              planet2LongitudeType)]

                        for aspectGroup in aspectGroupLists:
                            task = (processAspectsCalculationTask,
                                    (pcdd,
                                     planet1ParamsList,
                                     planet2ParamsList
                                     aspectGroup))
                            tasks.append(task)

# TODO: add task for adding vertical lines for when a geocentric planet moves from retrograde to direct and direct to retrograde.


# Start the worker processes.
log.info("Spawning {} processes to complete {} tasks.".\
         format(numProcesses, len(tasks)))
for task in tasks:
    taskQueue.put(task)
for i in range(numProcesses):
    multiprocessing.Process(target=worker,
                            args=(taskQueue, resultQueue)).start()

# Get results.
log.info("Waiting for proccessing to complete ...")
for i in range(len(tasks)):
    result = resultQueue.get()

    # Extract values from the result tuple.
    resultPcdd = result[0]
    resultNumArtifactsAdded = result[1]
    resultFilenameBasename = result[2]
    
    log.info("Result returned: {} artifacts added for '{}'.".\
             format(resultNumArtifactsAdded, resultFilenameBasename))

    # Make sure the output directory exists.
    ensureDirectoryExists(outputDirectory)

    # Assemble the absolute path of the output filename.
    outputFilename = outputDirectory + os.sep + resultFilenameBasename

    # Write the PriceChartDocumentData to the file.
    log.info("Writing results to file '{}' ...".\
             format(outputFilename))
    saveSuccess = \
        picklePriceChartDocumentDataToFile(resultPcdd, outputFilename)
    
    if saveSuccess == True:
        log.info("Results have been saved to file.")
    else:
        log.error("Writing to file '{}' failed.  ".\
                  format(outputFilename) + \
                  "Please see previous error messages for why.")
    
# Execution completed.
log.info("Done.")
shutdown(0)

##############################################################################
