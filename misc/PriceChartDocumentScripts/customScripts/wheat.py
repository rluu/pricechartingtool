#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for adding various PriceBarChartArtifacts to a
#   PriceChartDocumentData object that are relevant to a Wheat
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
#logLevel = logging.DEBUG
logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

# Start and ending timestamps for drawing.
#startDt = datetime.datetime(year=1508, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
startDt = datetime.datetime(year=1968, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=2010, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=2011, month=12, day=18,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
endDt   = datetime.datetime(year=2012, month=4, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=2012, month=4, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=2020, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
highPrice = 1200.0
lowPrice = 100.0

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

    #success = PlanetaryCombinationsLibrary.\
    #    addHelioSaturnUranus15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoSaturnUranus15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoVenusMars15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    success = PlanetaryCombinationsLibrary.\
        addHelioVenusMars15xVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice)
    
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioVenusJupiter120xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioMars150NeptuneVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioNeptune150MarsVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioVenus150NeptuneVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioNeptune150VenusVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoVenusSaturn120xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoMarsJupiter30xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoMarsSaturn120xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoMercuryJupiter90xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)

    stepSizeTd = datetime.timedelta(days=1)
    #highPrice = 800.0
    highPrice = 600.0
    #lowPrice = 600.0
    lowPrice = 300.0

    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Moon", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mercury", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mars", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Jupiter", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Saturn", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Uranus", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Neptune", 
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Pluto", 
    #    color=None, stepSizeTd=stepSizeTd)

    
    relativeDeclValue = -1.8
    #success = PlanetaryCombinationsLibrary.addDeclinationDiffLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mercury", relativeDeclValue=relativeDeclValue,
    #    color=None, stepSizeTd=stepSizeTd)
    
    p = 1000
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H1")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H2")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H3")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H4")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H5")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H6")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H7")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H8")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H9")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H10")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H11")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H12")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Sun")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Moon")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Mercury")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Venus")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Mars")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Jupiter")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Saturn")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Uranus")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Neptune")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Pluto")
    #p += 200
    
    if success == True:
        log.debug("Success!")
        rv = 0
    else:
        log.debug("Failure!")
        rv = 1

    return rv

