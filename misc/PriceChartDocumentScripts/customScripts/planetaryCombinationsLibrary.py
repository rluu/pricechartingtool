#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Adds various sets of artifacts to the Soybeans chart.
#
##############################################################################

import copy

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

# Default for the maximum time difference between the exact planetary
# combination timestamp, and the one calculated.  This would define
# the accuracy of the calculations.  This is a datetime.timedelta object.
#
#defaultMaxErrorJd = datetime.timedelta(hours=1)

##############################################################################
class PlanetaryCombinationsLibrary:
    """Class that holds several static functions to create
    PriceBarChartArtifacts that represent various planetary
    combinations.
    """
    
    @staticmethod
    def addSaturnUranus15xHelioVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Saturn and Uranus are multiples of 15
        degrees apart, heliocentrically.
        
        Note: Default tag used for the artifacts added is the name of this
        function, without the word 'add' at the beginning.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """


        log.debug("Entered addSaturnUranus15xHelioVerticalLines()")

        # Return value.
        rv = True

        # Make sure the inputs are valid.
        if endDt < startDt:
            log.error("Invalid input: 'endDt' must be after 'startDt'")
            rv = False
            return rv
        if lowPrice > highPrice:
            log.error("Invalid input: " +
                      "'lowPrice' is not less than or equal to 'highPrice'")
            rv = False
            return rv
        
        # Set the color if it is not already set to something.
        if color == None:
            color = QColor(Qt.red)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:]
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Create the PriceBarChartGraphicsScene for conversion functions.
        log.debug("Creating PriceBarChartGraphicsScene for conversions ...")
        scene = PriceBarChartGraphicsScene()

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        desiredDiffMultiple = 15.0

        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Iterate through, creating artfacts and adding them as we go.
        prevDt = copy.deepcopy(startDt)
        currDt = copy.deepcopy(startDt)

        prevDiff = None
        currDiff = None
        
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while currDt < endDt:
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getSaturnPlanetaryInfo(currDt)
            p2 = Ephemeris.getUranusPlanetaryInfo(currDt)

            log.debug("Saturn heliocentric longitude is: {}".\
                      format(p1.heliocentric['sidereal']['longitude']))
            log.debug("Uranus heliocentric longitude is: {}".\
                      format(p2.heliocentric['sidereal']['longitude']))
            
            diffDeg = \
                p1.heliocentric['sidereal']['longitude'] - \
                p2.heliocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0

            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg % desiredDiffMultiple

            if prevDiff == None:
                prevDiff = currDiff

            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            # If the currDiff modulus (remainder of the division) is
            # less the prevDiff modulus, that means between the
            # previous timestamp and the current one, we passed the
            # point of exact.  We need to now narrow the point down to
            # within the 'maxErrorTd' datetime.timedelta.
            if currDiff < prevDiff:
                log.debug("Crossed over!")
                
                # This is the upper-bound of the error timedelta.
                t1 = prevDt
                t2 = currDt
                currErrorTd = t2 - t1

                # Refine the timestamp until it is less than the threshold.
                while currErrorTd > maxErrorTd:
                    log.debug("Refining between {} and {}".\
                              format(Ephemeris.datetimeToStr(t1),
                                     Ephemeris.datetimeToStr(t2)))
                    
                    # Check the timestamp between.
                    diffTd = t2 - t1
                    halfDiffTd = \
                        datetime.\
                        timedelta(days=(diffTd.days / 2.0),
                                  seconds=(diffTd.seconds / 2.0),
                                  microseconds=(diffTd.microseconds / 2.0))
                    testDt = t1 + halfDiffTd
                    
                    p1 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    p2 = Ephemeris.getUranusPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    if diffDeg % desiredDiffMultiple > 0:
                        t2 = testDt
                    else:
                        t1 = testDt
                    
                    currErrorTd = t2 - t1
                
                # Set currDt as the t2, which is the one where
                # diffDeg % desiredDiffMultiple is greater than 0.
                currDt = t2
                
                # Create the artifact at the timestamp.
                log.debug("Creating line artifact at: {} ...".\
                          format(Ephemeris.datetimeToStr(currDt)))
                
                lineX = scene.datetimeToSceneXPos(currDt)
                lineLowY = scene.priceToSceneYPos(lowPrice)
                lineHighY = scene.priceToSceneYPos(highPrice)
                
                lineArtifact = PriceBarChartLineSegmentArtifact()
                lineArtifact.addTag(tag)
                lineArtifact.setTiltedTextFlag(False)
                lineArtifact.setAngleTextFlag(False)
                lineArtifact.setColor(color)
                lineArtifact.setStartPointF(QPointF(lineX, lineLowY))
                lineArtifact.setEndPointF(QPointF(lineX, lineHighY))

                # Append the artifact.
                log.info("Adding '{}' line artifact at: {} ...".\
                          format(tag, Ephemeris.datetimeToStr(currDt)))
                pcdd.priceBarChartArtifacts.append(lineArtifact)
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting addSaturnUranus15xHelioVerticalLines()")
        return rv
