#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for adding various PriceBarChartArtifacts to a
#   PriceChartDocumentData object that are relevant to a Silver
#   chart.
#
##############################################################################

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
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene

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
#startDt = datetime.datetime(year=1508, month=1, day=1,n
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=1704, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=1968, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=2001, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
startDt = datetime.datetime(year=1970, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)

#endDt   = datetime.datetime(year=2008, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=2012, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
endDt   = datetime.datetime(year=2014, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=2020, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
highPrice = 5000.0
lowPrice = 300.0

##############################################################################

def processPCDD(pcdd, tag):
    """Module for adding various PriceBarChartArtifacts that are
    relevant to the Wheat chart.  The tag str used for the created
    artifacts is based the name of the function that is being called,
    without the 'add' string at the beginning.
    
    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.
           This implementation does not use this value.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    global highPrice
    global lowPrice
    
    # Return value.
    rv = 0

    # Works very well.  I will need to apply a filter, but this works
    # very nicely.
    if True:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Uranus", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # I think the 90-step works better than the 45-step.
    if True:
        step = 45
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Uranus", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This works nicely too.  Worth investigating further.
    if True:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Uranus", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This works pretty well.  Worth investigating further.
    if True:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Uranus", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    ############################################################################

    
    if success == True:
        log.debug("Success!")
        rv = 0
    else:
        log.debug("Failure!")
        rv = 1

    return rv

##############################################################################
