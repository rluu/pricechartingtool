#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for adding various PriceBarChartArtifacts to a
#   PriceChartDocumentData object that are relevant to a ABX stock
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

eastern = pytz.timezone('US/Eastern')

# Start and ending timestamps for drawing.
startDt = datetime.datetime(year=1985, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=eastern)

endDt   = datetime.datetime(year=2016, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=eastern)
# High and low price limits for drawing the vertical lines.
highPrice = 70.0
lowPrice = 0.0

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

    if True:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.blue))
    
    if True:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.red))

    # G.Mercury 30 degree increments from 15 Libra 04'.
    if False:
        # For obtaining a color for a given planet.
        from astrologychart import AstrologyUtils
        col = AstrologyUtils.getForegroundColorForPlanetName("Mercury")
        
        success = PlanetaryCombinationsLibrary.\
            addPlanetLongitudeTraversalIncrementsVerticalLines(
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury", "geocentric", "tropical", 
            planetEpocDt=datetime.datetime(year=2013, month=12, day=6,
                                           hour=10, minute=0, second=0,
                                           tzinfo=eastern),
#            planetEpocDt=datetime.datetime(year=1985, month=10, day=1,
#                                           hour=10, minute=0, second=0,
#                                           tzinfo=eastern),
            degreeIncrement=30,
            color=col)
    
    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury", color=QColor(Qt.red))

    if False:
        success = PlanetaryCombinationsLibrary.\
            addHelioLatitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury", color=QColor(Qt.blue))

    # G.Mars 9 degree increments from 88 degrees.
    if False:
        # For obtaining a color for a given planet.
        from astrologychart import AstrologyUtils
        col = AstrologyUtils.getForegroundColorForPlanetName("Mars")
        
        success = PlanetaryCombinationsLibrary.\
            addPlanetLongitudeTraversalIncrementsVerticalLines(
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mars", "geocentric", "tropical",
            planetEpocDt=datetime.datetime(year=2011, month=12, day=2,
                                           hour=12, minute=0, second=0,
                                           tzinfo=eastern),
            
#            planetEpocDt=datetime.datetime(year=1985, month=10, day=5,
#                                           hour=12, minute=0, second=0,
#                                           tzinfo=eastern),
            degreeIncrement=9,
            color=col)
        
    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mars", color=QColor(Qt.blue))

    if False:
        success = PlanetaryCombinationsLibrary.\
            addHelioLatitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mars", color=QColor(Qt.green))

    # G.Jupiter 5 degree increments from  degrees.
    if False:
        # For obtaining a color for a given planet.
        from astrologychart import AstrologyUtils
        col = AstrologyUtils.getForegroundColorForPlanetName("Jupiter")
        
        success = PlanetaryCombinationsLibrary.\
            addPlanetLongitudeTraversalIncrementsVerticalLines(
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Jupiter", "geocentric", "tropical",
            planetEpocDt=datetime.datetime(year=2011, month=7, day=25,
                                           hour=12, minute=0, second=0,
                                           tzinfo=eastern),
            
#            planetEpocDt=datetime.datetime(year=1985, month=10, day=5,
#                                           hour=12, minute=0, second=0,
#                                           tzinfo=eastern),
            degreeIncrement=5,
            color=col)
        
    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Jupiter", color=QColor(Qt.blue))

    if False:
        success = PlanetaryCombinationsLibrary.\
            addHelioLatitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Jupiter", color=QColor(Qt.green))

    
    ############################################################################

    # Silver responds to this combination very well.
    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoJupiterSaturn15xVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice)

    
    # Worth looking closer into, as it hits turns perfectly at some
    # places, and then it is a little off, and then it stops working,
    # then it starts working again.  There is porbably some other
    # factor I need to take into account.  Note that the 150-degree
    # aspect between these two seems to work pretty well.
    # 
    # I should try to filter by season, or perhaps filter by whether
    # it is positive declination or negative declination, whether it
    # is positive latitude or negative latitude, or perhaps see how it
    # needs to be relative to some other planet (Sun or Pluto?).  Also
    # check to see if there is a certain effect in a bull market
    # vs. bear market.
    # 
    #
    if False:
        step = 15
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Venus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
    
    # Did not work too well.
    #step = 40
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Venus", "geocentric", "sidereal",
    #        "Venus", "heliocentric", "sidereal",
    #        degreeDiff)
    #    degreeDiff += step

    # This is definitely worth looking at more closely.
    if False:
        step = 18
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Venus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Meh, some hits, some misses.
    if False:
        step = 12
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Venus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # It'll hit a turn perfectly 3 times or so, and then stop working
    # for a while, and then work again.  Overall, this mostly has
    # misses though.
    if False:
        step = 11.25
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Venus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Does not work so well.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Venus", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # This marks some turns, so come back and investigate a little
    # more closely.
    if False:
        step = 15
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "geocentric", "sidereal",
                "Venus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Probably not worth studying further.  
    # On this aspect, there are big moves sometimes (eyeballing it,
    # maybe about 10% of the time?).  It's not clear that this defines
    # a change in trend though.
    if False:
        step = 15
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "geocentric", "tropical",
                "Venus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Generally, this does not work so well.
    # 108-degree aspects did show up a few times at tops and bottoms,
    # so maybe that particular aspect should be looked at more
    # closely.
    if False:
        step = 18
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "geocentric", "tropical",
                "Venus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Works well during very active markets.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "geocentric", "tropical",
                "Venus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Works well during very active markets.
    if False:
        step = 360 / 14.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "geocentric", "tropical",
                "Venus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step


    # Doesn't work very well.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Saturn", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Good for some triggers.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Saturn", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # There are few turns that this coincides with, but overall, it
    # does not work that well.
    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Saturn", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This cycle works pretty well!!!  Worth investigating
    # further to add a trigger.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Saturn", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This didn't work so well.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Saturn", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # It does mark some turns, but it doesn't always work and the
    # turns are not very large.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Saturn", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Overall, this doesn't work very well.
    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Jupiter", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This marks some tops and bottoms.  Worth investigating.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Jupiter", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Meh... Not that strong.  Not worth investigating further.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Jupiter", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Worth investigating closer.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Jupiter", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This is a somewhat consistent cycle in Silver, but a trigger
    # needs to be added.  Investigate further.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Jupiter", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # You can see it's affects, but it has a good amount of misses too.
    # Investigate further.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Jupiter", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Works very well.  I will need to apply a filter, but this works
    # very nicely.
    if False:
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
    if False:
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
    if False:
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
    if False:
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

    # Works okay when active.  It would need a trigger added though.
    # Using geo-geo is probably better, but I would need to check that.
    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Uranus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Some tops and bottoms, but they are mostly few.
    # I think geocentric works better than helio to helio.
    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Uranus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step


    # This times some turns, but overall, not very consistent.
    if False:
        step = 360 / 7.0
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

    # Does not work that well.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "sidereal",
                "Uranus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Shows up at some tops and bottoms.  Probably worth investigating further.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Uranus", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step


    # This is a cycle in silver.  Works very nicely when active.
    # Trigger may need to be added.
    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Pluto", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # This works pretty well; just needs triggers defined for it.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Pluto", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # This works pretty well too.  Just needs triggers defined for it.
    # Need to determine which is better for this aspect set, Venus
    # aspecting Geo Pluto or Venus aspecting Helio Pluto?
    # rluu: Just plot both to be aware of each.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Pluto", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # This combination may just be a trigger and not an actual cycle.
    #step = 15
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Venus", "geocentric", "sidereal",
    #        "Neptune", "heliocentric", "sidereal",
    #        degreeDiff)
    #    degreeDiff += step


    #step = 15
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Venus", "geocentric", "sidereal",
    #        "Neptune", "heliocentric", "sidereal",
    #        degreeDiff)
    #    degreeDiff += step
    
    # Worth investigating further.  The trigger needs to be defined.
    #step = 15
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Mars", "geocentric", "sidereal",
    #        "Pluto", "geocentric", "sidereal",
    #        degreeDiff)
    #    degreeDiff += step


    # 
    #step = 15
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Pluto", "heliocentric", "sidereal",
    #        "Mars", "geocentric", "sidereal",
    #        degreeDiff)
    #    degreeDiff += step


    # Had no effect.
    #step = 15
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Uranus", "geocentric", "tropical",
    #        "Neptune", "geocentric", "tropical",
    #        degreeDiff)
    #    degreeDiff += step


    # This catches some large and medium turns nicely, but also has
    # some smaller turns and misses. Is this just a triggering
    # combination?  Investigate to see if an additional trigger could
    # be utilized.
    #step = 15
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Mars", "geocentric", "tropical",
    #        "Isis", "geocentric", "tropical",
    #        degreeDiff)
    #    degreeDiff += step
    

    # This catches some large and medium turns nicely, but also has
    # some smaller turns and misses. Is this just a triggering
    # combination?  Investigate to see if an additional trigger could
    # be utilized.
    #step = 15
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Mars", "geocentric", "tropical",
    #        "Isis", "heliocentric", "tropical",
    #        degreeDiff)
    #    degreeDiff += step


    # This works well from about mid 2003 to end of 2008 (making well
    # defined turns).  Before 2003, it is either really sloppy or
    # doesn't catch turns.  Intervals between each aspect ranges from about
    # 4 months to ~2.25 years.
    #step = 7.5
    #start = 0
    #stop = 180
    #degreeDiff = start
    #while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Neptune", "geocentric", "tropical",
    #        "Isis", "geocentric", "tropical",
    #        degreeDiff)
    #    degreeDiff += step


    # Works pretty decently.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "geocentric", "sidereal",
                "Pluto", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Doesn't work that well.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "geocentric", "sidereal",
                "Pluto", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Coincided with some turns, but overall, this is not so good.
    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "geocentric", "sidereal",
                "Pluto", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
    
    # Coincided with some turns, but overall, this is not so good.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "geocentric", "sidereal",
                "Pluto", "geocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
            
    # This might be a very short cycle in silver.
    # At times it works really well, and at other times, it is not so good.
    # Maybe this is just a triggering combination.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This might be a very short cycle in silver.
    # At times it works really well, and at other times, it is not so good.
    # Maybe this is just a triggering combination.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # There are a lot of aspects created with this set, but it may be
    # worth exploring as a trigger since some hit the highs and lows.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "heliocentric", "tropical",
                "Pluto", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # There are some hits that coincide with turns, but 
    # generally this does not work too well.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "geocentric", "tropical",
                "Pluto", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Generally, this does not work that well.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Investigate further.  This may be an important cycle for silver!
    # You can see that prices either accelerate into the 120 degree
    # aspect, or accelerate after the 120 degree aspect, whenever this
    # aspect (planet combination) is active.
    # For the steps of 120, sometimes they mark turns (if dasa is active?),
    # and other times, nothing.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This looks to be an important combination in silver, although only
    # when it is 'active'.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This looks to be an important combination in silver, although only
    # when it is 'active'.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This is definitely worth keeping an eye on.  Especially when
    # hits are dead on, like in the 1997 to 1999 period.  It marks
    # very good 'time' for when a move is up.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "tropical",
                "Pluto", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Does not work that well.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Overall it does not seem to work too consistently, but some of
    # these trines, when they do catch, it is a very big turns.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Generally doesn't work too well.  There were a few hits, but
    # overall a low percentage.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "tropical",
                "Pluto", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Does not coincide with any notable turns.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Does not coincide with any notable turns.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Does not coincide with any notable turns.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "heliocentric", "tropical",
                "Pluto", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Does not coincide with any notable turns.
    if False:
        step = 15
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Uranus", "heliocentric", "sidereal",
                "Pluto", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Definitely a trigger combination for large turns, when a cycle is due.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Isis", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
            
    # Definitely a trigger combination for large turns, when a cycle is due.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Isis", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This works as a cycle so-so.  It does mark turns and also
    # periods when 'time' is up.  The negative is that the time ranges
    # that it does not work is pretty wide.  Although this cycle does
    # not appear to be a very strong.  Worth looking at again.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Isis", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This marks some tops and bottoms, and also periods when 'time' is up.
    # Worth investigating further.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Isis", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # At times it looks like there is something to this, but then
    # again it is also quite sloppy... so much so that there may not
    # be something here at all.  The turns it catches are not really
    # major turns.  At times it does not mark any turns at all.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Isis", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # In this, there are places where it marks that 'time' is up, but
    # there are also a lot of misses.  Worth looking at again later.
    # I might ask, what is the longitude difference between
    # heliocentric and geocentric Transpluto?  
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "tropical",
                "Isis", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step
            
    # Important (trigger?) combination for silver.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "sidereal",
                "Isis", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This is a trigger combination that doesn't work very often, and
    # when it does it coincides with turns that are very weak.  It's
    # probably better not to utilize this one.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "sidereal",
                "Isis", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # This marks some spots when 'time' is up, but there are also
    # a lot of places where it did not clearly have a move afterwards.
    # Probably not worth investigating too much further.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "tropical",
                "Isis", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Worth keeping this on the radar.  This marks powerful energy
    # energy surges when the market is trending.  There are some misses though.
    # Worth investigating further. 
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Earth", "heliocentric", "tropical",
                "Isis", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step
            
    # Important trigger combination for silver.
    # Some big reversals are marked with this combination.
    # An additional trigger may be needed.
    if False:
        step = 90
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "sidereal",
                "Isis", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Eye-balling this one, about 25% occurances coincided with turns.
    # Of the ones that did coincide with a turn, about half were
    # close to exact, and about half probably need an additional trigger.
    if False:
        step = 120
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "sidereal",
                "Isis", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    # Eye-balling this one, maybe about 5% coincided with tops or
    # bottoms.  The action caused by this combination isn't very clear
    # at all; overall it is kind of weak.  Probably not worth
    # investigating into this one.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "tropical",
                "Isis", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # When the market is active and trending, this will coincide with
    # some tops and bottoms (eye-balling: maybe 20% of them while
    # trending), and maybe about 5% overall.  Probably not worth
    # investigating into this one further.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "tropical",
                "Isis", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Coincides with some nice tops and bottoms when silver is trending.
    # This is probably a trigger.  Worth investigating closer.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "geocentric", "tropical",
                "Isis", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step
            
    ############################################################################
    # Heliocentric synodic combinations with Earth.
    #
    # For these, count the number of iterations.  For Jupiter, I
    # noticed that 24 synodic iterations later, there is a major high
    # coinciding with it again.  Also, the synodic Mars with Earth hit
    # once at the same time as synodic Jupiter with Earth, and that
    # was a huge high.  There is probably value to looking at all
    # these at once to see if any light can be seen as to how these
    # synodics (or cycles) work with each other.
    #

    
    # If active, it coincides with sharp turns.  If not active, then
    # there will need to be an orb and another trigger, but you can
    # definitely seen the rhythm of Mercury.  Something that may be
    # helpful to watch to see patterns as they develop.
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Saturn", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Uranus", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Neptune", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Pluto", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Chiron", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step
        
    if False:
        step = 360
        start = 0
        stop = 0
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Isis", "heliocentric", "sidereal",
                "Earth", "heliocentric", "sidereal",
                degreeDiff)
            degreeDiff += step

    ############################################################################

    # Testing new functions for longitude aspect timestamps.
    if False:
        aspectGroup = []
        step = 180
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            aspectGroup.append(degreeDiff)
            degreeDiff += step

        planet1ParamsList = [("Venus", "geocentric", "sidereal")]
        planet2ParamsList = [("Uranus", "geocentric", "sidereal")]
        uniDirectionalAspectsFlag = True
        
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
    
    ############################################################################

    if success == True:
        log.debug("Success!")
        rv = 0
    else:
        log.debug("Failure!")
        rv = 1

    return rv

##############################################################################
