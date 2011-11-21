#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for adding various PriceBarChartArtifacts to a
#   PriceChartDocumentData object that are relevant to a Soybeans
#   chart.
#
##############################################################################

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
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene

# Holds functions for adding artifacts for various aspects.
from planetaryCombinationsLibrary import PlanetaryCombinationsLibrary

##############################################################################
# Global variables
##############################################################################

# For logging.
logLevel = logging.DEBUG
#logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

# Start and ending timestamps for drawing.
startDt = datetime.datetime(year=1970, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
endDt   = datetime.datetime(year=2020, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
highPrice = 2000.0
lowPrice = 0.0

##############################################################################

def processPCDD(pcdd, tag):
    """Module for adding various PriceBarChartArtifacts that are
    relevant to the Soybeans chart.  The tag str used for the created
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

    # Return value.
    rv = 0

    success = PlanetaryCombinationsLibrary.\
        addHelioVenusConjunctOrTrineJupiterVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioSaturnUranus15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoSaturnUranus15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    
    if success == True:
        log.debug("Success!")
        rv = 0
    else:
        log.debug("Failure!")
        rv = 1

    return rv

