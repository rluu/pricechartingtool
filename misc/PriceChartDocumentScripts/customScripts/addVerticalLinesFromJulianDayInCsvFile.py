#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for drawing veritcal lines at julian days that are specified in
#   a CSV file.  
#
#   Format of the CSV file:
#   - Header line is the first line of the CSV file and is always skipped.
#   - The first column contains the tag value used in the vertical line.
#   - The second column contains the julian day value.
#
#   The processPCDD() method requires a third argument, which is a 
#   list of str, where each str is a filename of a CSV file to load.
#
##############################################################################

import sys

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

import csv
import random

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Include some PriceChartingTool modules.
from ephemeris import Ephemeris
from ephemeris_utils import EphemerisUtils
from color import Color
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene
from util import Util
from lunar_calendar_utils import LunarDate
from lunar_calendar_utils import LunarCalendarUtils

# Holds functions for adding artifacts for various aspects.
from planetaryCombinationsLibrary import PlanetaryCombinationsLibrary

##############################################################################
# Global variables
##############################################################################

# For logging.
#logLevel = logging.DEBUG
logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

# Start and ending timestamps for drawing.

startDt = datetime.datetime(year=1905, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=1995, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
endDt = datetime.datetime(year=1940, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)

#startDt = datetime.datetime(year=1905, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=1936, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=1941, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
#highPrice = 22000.0
#highPrice = 15000.0
#highPrice = 4500.0
highPrice = 400.0
#lowPrice = 240.0
lowPrice = 35.0
#lowPrice = 800.0
#lowPrice = 4500.0

useRandomColors = False

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    Ephemeris.closeEphemeris()
    logging.shutdown()
    sys.exit(rc)

def processPCDD(pcdd, tag, customArguments=None):
    """Module for adding various PriceBarChartArtifacts that are
    relevant to the chart.  The tag str used for the created
    artifacts is based the name of the function that is being called,
    without the 'add' string at the beginning.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.
           This implementation does not use this value.
    customArguments - list of str, where each str is a filename of a
           CSV file to load.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    if pcdd is None:
        raise TypeError("pcdd may not be None")

    if customArguments is None:
        errMsg = \
            "Missing required argument.  " + \
            "Please specify an input CSV filename using the --argument option."
        log.error(errMsg)
        shutdown(1)

    if not isinstance(customArguments, list):
        errMsg = "Expected a list of str for argument 'customArguments'.  " + \
                "Type encountered was: {}".\
                format(str(type(customArguments)))
        log.error(errMsg)
        shutdown(1)

    csvFiles = []
    for argument in customArguments:
        log.debug("argument == {}".format(argument))
        csvFile = os.path.abspath(argument)

        # Make sure the file exists.
        if not os.path.isfile(csvFile):
            log.error("Input CSV file '{}'".format(csvFile) + \
                    " does not exist or it is not a file.")
            shutdown(1)

        csvFiles.append(csvFile)

    global highPrice
    global lowPrice
    global useRandomColors

    # Return value.
    rv = 0

    colorsAvailable = []

    for key in Color.__dict__:
        if not key.startswith("__"):
            value = Color.__dict__[key]
            if isinstance(value, QColor):
                colorsAvailable.append(value)

    if len(colorsAvailable) == 0:
        log.error("Unable to find any QColors for use.")
        shutdown(1)

    log.debug("Number of colors available: {}".\
            format(len(colorsAvailable)))

    for csvFile in csvFiles:
        log.info("Inspecting CSV file: {}".format(csvFile))

        # Get a QColor to use for drawing the vertical lines for this CSV file.
        color = None
        if useRandomColors and len(colorsAvailable) > 0:
            randomIndexForColorsAvailable = \
                random.randrange(len(colorsAvailable))
            log.debug("randomIndexForColorsAvailable == {}".\
                format(randomIndexForColorsAvailable))
            color = colorsAvailable[randomIndexForColorsAvailable]
            del colorsAvailable[randomIndexForColorsAvailable]
        else:
            color = Color.veryDarkGray

        with open(csvFile, 'r') as f:
            i = -1
            isFirstRow = True
            for line in f:
                i += 1
                log.debug("line[{}] == {}".format(i, line))
                row = line.split(",")

                if isFirstRow:
                    isFirstRow = False
                    continue
    
                tag = None
                jd = None
                try:
                    tagColumn = 0
                    jdColumn = 1
                    tag = row[tagColumn]
                    jdStr = row[jdColumn]
                    try:
                        jd = float(jdStr)
                    except ValueError as ve:
                        warnMsg = "Column at row index {}".format(i) + \
                            ", column index {}".format(jdColumn) + \
                            " does not contain a parsable float.  " + \
                            "Value seen was: '{}'.".format(jdStr) + \
                            "  Skipping this row.  " + \
                            "CSV file is: {}".format(csvFile)
                        log.warn(warnMsg)
                        continue
                except IndexError as ie:
                    errMsg = "Row at index {}".format(i) + \
                        " does not contain at least 2 columns.  " + \
                        "CSV file is: {}".format(csvFile)
                    log.error(errMsg)
                    shutdown(1)
    
                log.debug("i == {}, tag == {}, jd == {}".format(i, tag, jd))
    
                if tag is None or len(tag) == 0:
                    errMsg = "Row at index {}".format(i) + \
                        " does not contain a valid tag value.  " + \
                        "The tag value may not be empty.  " + \
                        "CSV file is: {}".format(csvFile)
                    log.error(errMsg)
                    shutdown(1)
    
                # Replace any spaces in the tag with an underscore to make the
                # tag valid.
                if " " in tag:
                    tag = tag.replace(" ", "_")
                    log.debug("Tag updated to: tag == {}".format(tag))
    
                dt = Ephemeris.julianDayToDatetime(jd, tzInfo=pytz.utc)
                log.debug("dt == {}".format(Ephemeris.datetimeToStr(dt)))
    
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, dt,
                                    highPrice, lowPrice, tag, color)
    

            log.info("Processed {} timestamps from CSV file: {}".\
                    format(i, csvFile))

    log.info("Processed {} total CSV file(s).".format(len(csvFiles)))
    success = True

    ##########################################################################

    if success == True:
        log.debug("Success!")
        rv = 0
    else:
        log.debug("Failure!")
        rv = 1

    return rv

##############################################################################
