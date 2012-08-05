#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for adding various PriceBarChartArtifacts to a
#   PriceChartDocumentData object that are relevant to AAPL.
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
#startDt = datetime.datetime(year=2007, month=8, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
startDt = datetime.datetime(year=1984, month=8, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)

#endDt   = datetime.datetime(year=2008, month=6, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)

endDt   = datetime.datetime(year=2014, month=12, day=31,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
highPrice = 600.0
lowPrice = 30.0

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

    stepSizeTd = datetime.timedelta(days=3)
    #highPrice = 800.0
    #highPrice = 600.0
    #lowPrice = 600.0
    #lowPrice = 300.0

    if False:
        step = 24
        start = 0
        stop = 360
        
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addPlanetCrossingLongitudeDegVerticalLines(
                pcdd, startDt, endDt, highPrice, lowPrice,
                "heliocentric", "tropical", "Mercury", degreeDiff)
            degreeDiff += step
        
    if False:
        step = 36
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "tropical",
                "Mercury", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury")
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus")
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mars")
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Jupiter")
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Saturn")

    if False:
        aspectGroup = []
        step = 9
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            aspectGroup.append(degreeDiff)
            degreeDiff += step

        # Mercury-Venus did not work very well for the geocentric
        # 5-degree step differences.

        # Mercury-Venus did not work very well for the geocentric
        # 7-degree step differences.

        # Mercury-Venus did not work very well for the geocentric
        # 7.2-degree step differences.

        # Mercury-Sun did not work very well for the geocentric
        # 6-degree step differences.  May need to try a larger separation.

        # Mercury-TrueNorthNode did not work very well for the geocentric
        # 5-degree step differences.  
        
        # Mercury-TrueNorthNode geocentric 7.2-degree steps makes it
        # seem like this combination of planets has promise.  May need
        # a different separation amount though.  I tried 14.4, but
        # that is too wide.

        # H Mercury-G TrueNorthNode 14.4-degree steps gives too many
        # lines, so it's probably not the cycle.
        
        # G Venus-G TrueNorthNode 5-degree steps gives too many
        # lines, so they may just be coincidence.  7.2 didn't work well either.
        
                
        
        planet1ParamsList = [("Venus", "geocentric", "tropical")]
        planet2ParamsList = [("TrueNorthNode", "geocentric", "tropical")]
        uniDirectionalAspectsFlag = False
        
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
            from astrologychart import AstrologyUtils
            color = AstrologyUtils.\
                    getForegroundColorForPlanetName(planet1ParamsList[0][0])
            
            # Draw the aspects.
            for dt in timestamps:
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)
    
            log.info("Added {} artifacts for aspect {} degrees.".\
                      format(len(timestamps), degreeDifference))
        success = True
    
    # DId not work very well.
    if False:
        step = 360 / 20 # 18 degree steps.
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "heliocentric", "tropical",
                "Venus", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step
    
    # Investigate further.
    if True:
        step = 360 / 72 # 5 deg steps.
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "tropical",
                "Earth", "heliocentric", "tropical",
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
