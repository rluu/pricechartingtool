#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Adds various sets of artifacts related to planetary combinations.
#
# Notes:
#
#   Methods I care most about as of (Sun Feb 21 02:48:31 EST 2016):
#
#     _getDatetimesOfElapsedLongitudeDegrees()
#     addGeoLongitudeVelocityPolarityChangeVerticalLines()
#     addPlanetCrossingLongitudeDegVerticalLines()
#     addVerticalLine()
#     addHorizontalLine()
#
#   Newly added (Wed Feb 24 20:49:41 EST 2016):
#
#     getGeoRetrogradeDirectTimestamps()
#     getGeoConjunctionsOfDirectRetrogradeMidpoints()
#     getGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpoints()
#     addGeoConjunctionsOfDirectRetrogradeMidpointsVerticalLines()
#     addGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpointsVerticalLines()
#
##############################################################################

import copy

# For logging.
import logging

# For math.floor()
import math

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

from pricebarchart import LineSegmentGraphicsItem
from pricebarchart import PriceBarChartGraphicsScene
from pricebarchart import TextGraphicsItem
from pricebarchart import TimeMeasurementGraphicsItem


from astrologychart import AstrologyUtils

##############################################################################
# Global variables
##############################################################################

# For logging.
#logLevel = logging.DEBUG
logLevel = logging.INFO
#logLevel = logging.ERROR
#logging.basicConfig(format='%(levelname)s: %(message)s')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

class PlanetaryCombinationsLibrary:
    """Class that holds several static functions to create
    PriceBarChartArtifacts that represent various planetary
    combinations.
    """

    scene = PriceBarChartGraphicsScene()
    
    @staticmethod
    def addHorizontalLine(pcdd, startDt, endDt, price, tag, color):
        """Adds a horizontal line at the given price, from startDt to
        endDt, with the given tag and color.

        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for starting timestamp
                    of the horizontal line.
        endDt     - datetime.datetime object for ending timestamp
                    of the horizontal line.
        price     - float value for the price to draw the horizontal line.
        tag       - str value for the tag to add to the horizontal line.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        """

        # Create the artifact at the timestamp.
        log.debug("Creating line artifact at price: {} ...".\
                  format(price))
        
        lineY = \
            PlanetaryCombinationsLibrary.scene.priceToSceneYPos(price)
        lineStartX = \
            PlanetaryCombinationsLibrary.scene.datetimeToSceneXPos(startDt)
        lineEndX = \
            PlanetaryCombinationsLibrary.scene.datetimeToSceneXPos(endDt)
        
        item = LineSegmentGraphicsItem()
        item.loadSettingsFromAppPreferences()
        item.loadSettingsFromPriceBarChartSettings(\
            pcdd.priceBarChartSettings)
        
        artifact = item.getArtifact()
        artifact = PriceBarChartLineSegmentArtifact()
        artifact.addTag(tag)
        artifact.setTiltedTextFlag(False)
        artifact.setAngleTextFlag(False)
        artifact.setColor(color)
        artifact.setStartPointF(QPointF(lineStartX, lineY))
        artifact.setEndPointF(QPointF(lineEndX, lineY))
        
        # Append the artifact.
        log.info("Adding '{}' line artifact at price: {} ...".\
                 format(tag, price))
        pcdd.priceBarChartArtifacts.append(artifact)

    @staticmethod
    def addVerticalLine(pcdd, dt, highPrice, lowPrice, tag, color):
        """Adds a vertical line at the given timestamp, from highPrice
        to lowPrice, with the given tag and color.

        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        dt        - datetime.datetime object for timestamp
                    of the vertical line.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.
        tag       - str value for the tag to add to the vertical line.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        """

        # Create the artifact at the timestamp.
        log.debug("Creating line artifact at datetime: {} ...".\
                  format(Ephemeris.datetimeToStr(dt)))
        
        lineX = \
            PlanetaryCombinationsLibrary.scene.datetimeToSceneXPos(dt)
        lineLowY = \
            PlanetaryCombinationsLibrary.scene.priceToSceneYPos(lowPrice)
        lineHighY = \
            PlanetaryCombinationsLibrary.scene.priceToSceneYPos(highPrice)
        
        item = LineSegmentGraphicsItem()
        item.loadSettingsFromAppPreferences()
        item.loadSettingsFromPriceBarChartSettings(\
            pcdd.priceBarChartSettings)
        
        artifact = item.getArtifact()
        artifact = PriceBarChartLineSegmentArtifact()
        artifact.addTag(tag)
        artifact.setTiltedTextFlag(False)
        artifact.setAngleTextFlag(False)
        artifact.setColor(color)
        artifact.setStartPointF(QPointF(lineX, lineLowY))
        artifact.setEndPointF(QPointF(lineX, lineHighY))
        
        # Append the artifact.
        log.info("Adding '{}' line artifact at: {} (jd == {}) ...".\
                 format(tag,
                        Ephemeris.datetimeToStr(dt),
                        Ephemeris.datetimeToJulianDay(dt)))
        pcdd.priceBarChartArtifacts.append(artifact)

        
    @staticmethod
    def addHelioVenusJupiter120xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Venus and Jupiter are multiples of 120
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of green will be used for 0 deg, 120 deg, and 240 deg.
        color1 = QColor(0x008020)
        color2 = QColor(0x00A040)
        color3 = QColor(0x00C060)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=4)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 120.0

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
            
            p1 = Ephemeris.getVenusPlanetaryInfo(currDt)
            p2 = Ephemeris.getJupiterPlanetaryInfo(currDt)

            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))

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
                    
                    p1 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    p2 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < currDiff:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 120:
                        color = color2
                    elif round(abs(diffDeg)) == 240:
                        color = color3
                    else:
                        color = color1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addHelioMars150NeptuneVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Mars aspects Neptune at 150 degrees,
        heliocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of green will be used for 0 deg, 120 deg, and 240 deg.
        if color == None:
            color = QColor(Qt.darkMagenta)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=4)

        # Desired differential.
        desiredDiff = 150

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
            
            p1 = Ephemeris.getNeptunePlanetaryInfo(currDt)
            p2 = Ephemeris.getMarsPlanetaryInfo(currDt)
            
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))
            
            diffDeg = \
                p1.heliocentric['sidereal']['longitude'] - \
                p2.heliocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0

            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg
            
            if prevDiff == None:
                prevDiff = currDiff
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff > desiredDiff and currDiff < desiredDiff:
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
                    
                    p1 = Ephemeris.getNeptunePlanetaryInfo(testDt)
                    p2 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    if diffDeg > desiredDiff:
                        t1 = testDt
                    else:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = diffDeg
                        
                    currErrorTd = t2 - t1

                log.debug("diffDeg == {}".format(diffDeg))
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addHelioNeptune150MarsVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Neptune aspects Mars at 150 degrees,
        heliocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of green will be used for 0 deg, 120 deg, and 240 deg.
        if color == None:
            color = QColor(Qt.magenta)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=4)

        # Desired differential.
        desiredDiff = 150

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
            
            p1 = Ephemeris.getMarsPlanetaryInfo(currDt)
            p2 = Ephemeris.getNeptunePlanetaryInfo(currDt)
            
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))
            
            diffDeg = \
                p1.heliocentric['sidereal']['longitude'] - \
                p2.heliocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0

            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg
            
            if prevDiff == None:
                prevDiff = currDiff
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff < desiredDiff and currDiff > desiredDiff:
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
                    
                    p1 = Ephemeris.getNeptunePlanetaryInfo(testDt)
                    p2 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    if diffDeg < desiredDiff:
                        t1 = testDt
                    else:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = diffDeg
                        
                    currErrorTd = t2 - t1

                log.debug("diffDeg == {}".format(diffDeg))
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addHelioVenus150NeptuneVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Venus aspects Neptune at 150 degrees,
        heliocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of green will be used for 0 deg, 120 deg, and 240 deg.
        if color == None:
            color = QColor(Qt.darkYellow)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=4)

        # Desired differential.
        desiredDiff = 150

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
            
            p1 = Ephemeris.getNeptunePlanetaryInfo(currDt)
            p2 = Ephemeris.getVenusPlanetaryInfo(currDt)
            
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))
            
            diffDeg = \
                p1.heliocentric['sidereal']['longitude'] - \
                p2.heliocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0

            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg
            
            if prevDiff == None:
                prevDiff = currDiff
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff > desiredDiff and currDiff < desiredDiff:
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
                    
                    p1 = Ephemeris.getNeptunePlanetaryInfo(testDt)
                    p2 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    if diffDeg > desiredDiff:
                        t1 = testDt
                    else:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = diffDeg
                        
                    currErrorTd = t2 - t1

                log.debug("diffDeg == {}".format(diffDeg))
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addHelioNeptune150VenusVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Neptune aspects Venus at 150 degrees,
        heliocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of green will be used for 0 deg, 120 deg, and 240 deg.
        if color == None:
            color = QColor(Qt.yellow)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=4)

        # Desired differential.
        desiredDiff = 150

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
            
            p1 = Ephemeris.getVenusPlanetaryInfo(currDt)
            p2 = Ephemeris.getNeptunePlanetaryInfo(currDt)
            
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))
            
            diffDeg = \
                p1.heliocentric['sidereal']['longitude'] - \
                p2.heliocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0

            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg
            
            if prevDiff == None:
                prevDiff = currDiff
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff < desiredDiff and currDiff > desiredDiff:
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
                    
                    p1 = Ephemeris.getNeptunePlanetaryInfo(testDt)
                    p2 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    if diffDeg < desiredDiff:
                        t1 = testDt
                    else:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = diffDeg
                        
                    currErrorTd = t2 - t1

                log.debug("diffDeg == {}".format(diffDeg))
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addGeoVenusSaturn120xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Venus and Saturn are multiples of 120
        degrees apart, geocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of red will be used for 0 deg, 120 deg, and 240 deg.
        color1 = QColor(0xFF0000)
        color2 = QColor(0xFC0000)
        color3 = QColor(0xFA0000)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 120.0
        
        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        
        diffs = []
        diffs.append(None)
        diffs.append(None)
        diffs.append(None)
        
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[2] < endDt:
            
            currDt = steps[2]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getVenusPlanetaryInfo(currDt)
            p2 = Ephemeris.getSaturnPlanetaryInfo(currDt)

            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.geocentric['sidereal']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p1.name,
            #                 p1.geocentric['tropical']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p2.name,
            #                 p2.geocentric['tropical']['longitude']))
            
            
            diffDeg = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0
                
            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg % desiredDiffMultiple
            
            if diffs[0] == None:
                diffs[0] = currDiff
            if diffs[1] == None:
                diffs[1] = currDiff
            diffs[2] = currDiff
            
            log.debug("steps[0] == {}".format(steps[0]))
            log.debug("steps[1] == {}".format(steps[1]))
            log.debug("steps[2] == {}".format(steps[2]))
            
            log.debug("diffs[0] == {}".format(diffs[0]))
            log.debug("diffs[1] == {}".format(diffs[1]))
            log.debug("diffs[2] == {}".format(diffs[2]))

            if diffs[2] < diffs[0] and \
                   diffs[2] < diffs[1] and \
                   (diffs[1] - diffs[2] > crossoverRequirement):
                
                # Crossed over to above 0 while increasing over
                # 'desiredDiffMultiple'.  This happens when planets
                # are moving in direct motion.
                log.debug("Crossed over to above 0 while increasing over {}".\
                          format(desiredDiffMultiple))

                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    p2 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[2]:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 120:
                        color = color2
                    elif round(abs(diffDeg)) == 240:
                        color = color3
                    else:
                        color = color1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            elif diffs[2] > diffs[1] and \
                     diffs[2] > diffs[0] and \
                     (diffs[2] - diffs[1] > crossoverRequirement):
                
                # Crossed over to under 'desiredDiffMultiple' while
                # decreasing under 0.  This can happen when planets
                # are moving in retrograde motion.
                log.debug("Crossed over to under {} while decreasing under 0".\
                          format(desiredDiffMultiple))
                
                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    p2 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[1]:
                        t1 = testDt
                    else:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                        
                    currErrorTd = t2 - t1
                    
                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 120:
                        color = color2
                    elif round(abs(diffDeg)) == 240:
                        color = color3
                    else:
                        color = color1
                        
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            diffs.append(diffs[-1])
            del diffs[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addGeoMarsJupiter30xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Mars and Jupiter are multiples of 30
        degrees apart, geocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of blue will be used.
        color1 = QColor(0x000080)
        color2 = QColor(0x00008F)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 30.0
        
        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        
        diffs = []
        diffs.append(None)
        diffs.append(None)
        diffs.append(None)
        
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[2] < endDt:
            
            currDt = steps[2]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getMarsPlanetaryInfo(currDt)
            p2 = Ephemeris.getJupiterPlanetaryInfo(currDt)

            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.geocentric['sidereal']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p1.name,
            #                 p1.geocentric['tropical']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p2.name,
            #                 p2.geocentric['tropical']['longitude']))
            
            
            diffDeg = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0
                
            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg % desiredDiffMultiple
            
            if diffs[0] == None:
                diffs[0] = currDiff
            if diffs[1] == None:
                diffs[1] = currDiff
            diffs[2] = currDiff
            
            log.debug("steps[0] == {}".format(steps[0]))
            log.debug("steps[1] == {}".format(steps[1]))
            log.debug("steps[2] == {}".format(steps[2]))
            
            log.debug("diffs[0] == {}".format(diffs[0]))
            log.debug("diffs[1] == {}".format(diffs[1]))
            log.debug("diffs[2] == {}".format(diffs[2]))

            if diffs[2] < diffs[0] and \
                   diffs[2] < diffs[1] and \
                   (diffs[1] - diffs[2] > crossoverRequirement):
                
                # Crossed over to above 0 while increasing over
                # 'desiredDiffMultiple'.  This happens when planets
                # are moving in direct motion.
                log.debug("Crossed over to above 0 while increasing over {}".\
                          format(desiredDiffMultiple))

                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    p2 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[2]:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 0 or round(abs(diffDeg)) == 360:
                        color = color1
                    else:
                        color = color2
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            elif diffs[2] > diffs[1] and \
                     diffs[2] > diffs[0] and \
                     (diffs[2] - diffs[1] > crossoverRequirement):
                
                # Crossed over to under 'desiredDiffMultiple' while
                # decreasing under 0.  This can happen when planets
                # are moving in retrograde motion.
                log.debug("Crossed over to under {} while decreasing under 0".\
                          format(desiredDiffMultiple))
                
                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    p2 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[1]:
                        t1 = testDt
                    else:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                        
                    currErrorTd = t2 - t1
                    
                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 0 or round(abs(diffDeg)) == 360:
                        color = color1
                    else:
                        color = color2
                        
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            diffs.append(diffs[-1])
            del diffs[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addGeoMarsSaturn120xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Mars and Saturn are multiples of 120
        degrees apart, geocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of gray will be used for 0 deg, 120 deg, and 240 deg.
        color1 = QColor(0x808080)
        color2 = QColor(0xA0A0A4)
        color3 = QColor(0xA0A0A4)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 120.0
        
        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        
        diffs = []
        diffs.append(None)
        diffs.append(None)
        diffs.append(None)
        
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[2] < endDt:
            
            currDt = steps[2]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getMarsPlanetaryInfo(currDt)
            p2 = Ephemeris.getSaturnPlanetaryInfo(currDt)

            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.geocentric['sidereal']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p1.name,
            #                 p1.geocentric['tropical']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p2.name,
            #                 p2.geocentric['tropical']['longitude']))
            
            
            diffDeg = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0
                
            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg % desiredDiffMultiple
            
            if diffs[0] == None:
                diffs[0] = currDiff
            if diffs[1] == None:
                diffs[1] = currDiff
            diffs[2] = currDiff
            
            log.debug("steps[0] == {}".format(steps[0]))
            log.debug("steps[1] == {}".format(steps[1]))
            log.debug("steps[2] == {}".format(steps[2]))
            
            log.debug("diffs[0] == {}".format(diffs[0]))
            log.debug("diffs[1] == {}".format(diffs[1]))
            log.debug("diffs[2] == {}".format(diffs[2]))

            if diffs[2] < diffs[0] and \
                   diffs[2] < diffs[1] and \
                   (diffs[1] - diffs[2] > crossoverRequirement):
                
                # Crossed over to above 0 while increasing over
                # 'desiredDiffMultiple'.  This happens when planets
                # are moving in direct motion.
                log.debug("Crossed over to above 0 while increasing over {}".\
                          format(desiredDiffMultiple))

                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    p2 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[2]:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 120:
                        color = color2
                    elif round(abs(diffDeg)) == 240:
                        color = color3
                    else:
                        color = color1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            elif diffs[2] > diffs[1] and \
                     diffs[2] > diffs[0] and \
                     (diffs[2] - diffs[1] > crossoverRequirement):
                
                # Crossed over to under 'desiredDiffMultiple' while
                # decreasing under 0.  This can happen when planets
                # are moving in retrograde motion.
                log.debug("Crossed over to under {} while decreasing under 0".\
                          format(desiredDiffMultiple))
                
                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    p2 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[1]:
                        t1 = testDt
                    else:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                        
                    currErrorTd = t2 - t1
                    
                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 120:
                        color = color2
                    elif round(abs(diffDeg)) == 240:
                        color = color3
                    else:
                        color = color1
                        
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            diffs.append(diffs[-1])
            del diffs[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addGeoMercuryJupiter90xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Mercury and Jupiter are multiples of 90
        degrees apart, geocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        
        # If color was not explicitly defined, then the following
        # shades of cyan will be used for 0, and 90, 180, 270 deg.
        color1 = QColor(0x008080)
        color2 = QColor(0x00A0A4)
        
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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 90.0
        
        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        
        diffs = []
        diffs.append(None)
        diffs.append(None)
        diffs.append(None)
        
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[2] < endDt:
            
            currDt = steps[2]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getMercuryPlanetaryInfo(currDt)
            p2 = Ephemeris.getJupiterPlanetaryInfo(currDt)

            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.geocentric['sidereal']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p1.name,
            #                 p1.geocentric['tropical']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p2.name,
            #                 p2.geocentric['tropical']['longitude']))
            
            
            diffDeg = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0
                
            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg % desiredDiffMultiple
            
            if diffs[0] == None:
                diffs[0] = currDiff
            if diffs[1] == None:
                diffs[1] = currDiff
            diffs[2] = currDiff
            
            log.debug("steps[0] == {}".format(steps[0]))
            log.debug("steps[1] == {}".format(steps[1]))
            log.debug("steps[2] == {}".format(steps[2]))
            
            log.debug("diffs[0] == {}".format(diffs[0]))
            log.debug("diffs[1] == {}".format(diffs[1]))
            log.debug("diffs[2] == {}".format(diffs[2]))

            if diffs[2] < diffs[0] and \
                   diffs[2] < diffs[1] and \
                   (diffs[1] - diffs[2] > crossoverRequirement):
                
                # Crossed over to above 0 while increasing over
                # 'desiredDiffMultiple'.  This happens when planets
                # are moving in direct motion.
                log.debug("Crossed over to above 0 while increasing over {}".\
                          format(desiredDiffMultiple))

                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getMercuryPlanetaryInfo(testDt)
                    p2 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[2]:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 0 or round(abs(diffDeg)) == 360:
                        color = color1
                    else:
                        color = color2
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            elif diffs[2] > diffs[1] and \
                     diffs[2] > diffs[0] and \
                     (diffs[2] - diffs[1] > crossoverRequirement):
                
                # Crossed over to under 'desiredDiffMultiple' while
                # decreasing under 0.  This can happen when planets
                # are moving in retrograde motion.
                log.debug("Crossed over to under {} while decreasing under 0".\
                          format(desiredDiffMultiple))
                
                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getMercuryPlanetaryInfo(testDt)
                    p2 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[1]:
                        t1 = testDt
                    else:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                        
                    currErrorTd = t2 - t1
                    
                currDt = steps[2]
                
                log.debug("diffDeg == {}".format(diffDeg))
                usingDefaultColors = False
                if color == None:
                    usingDefaultColors = True
                    if round(abs(diffDeg)) == 0 or round(abs(diffDeg)) == 360:
                        color = color1
                    else:
                        color = color2
                        
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                if usingDefaultColors == True:
                    color = None
                numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            diffs.append(diffs[-1])
            del diffs[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addHelioSaturnUranus15xVerticalLines(\
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=4)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
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

            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))

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

                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < currDiff:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addHelioJupiterSaturn15xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Jupiter and Saturn are multiples of 15
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=4)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
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
            
            p1 = Ephemeris.getJupiterPlanetaryInfo(currDt)
            p2 = Ephemeris.getSaturnPlanetaryInfo(currDt)

            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))

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
                    
                    p1 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    p2 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < currDiff:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addGeoSaturnUranus15xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Saturn and Uranus are multiples of 15
        degrees apart, geocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
            color = QColor(Qt.darkYellow)

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 15.0

        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        diffs = []
        diffs.append(None)
        diffs.append(None)
        diffs.append(None)
        
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[2] < endDt:
            
            currDt = steps[2]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getSaturnPlanetaryInfo(currDt)
            p2 = Ephemeris.getUranusPlanetaryInfo(currDt)

            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.geocentric['sidereal']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p1.name,
            #                 p1.geocentric['tropical']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p2.name,
            #                 p2.geocentric['tropical']['longitude']))
            
            
            diffDeg = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0
                
            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg % desiredDiffMultiple
            
            if diffs[0] == None:
                diffs[0] = currDiff
            if diffs[1] == None:
                diffs[1] = currDiff
            diffs[2] = currDiff
            
            log.debug("steps[0] == {}".format(steps[0]))
            log.debug("steps[1] == {}".format(steps[1]))
            log.debug("steps[2] == {}".format(steps[2]))
            
            log.debug("diffs[0] == {}".format(diffs[0]))
            log.debug("diffs[1] == {}".format(diffs[1]))
            log.debug("diffs[2] == {}".format(diffs[2]))

            if diffs[2] < diffs[0] and \
                   diffs[2] < diffs[1] and \
                   (diffs[1] - diffs[2] > crossoverRequirement):
                
                # Crossed over to above 0 while increasing over
                # 'desiredDiffMultiple'.  This happens when planets
                # are moving in direct motion.
                log.debug("Crossed over to above 0 while increasing over {}".\
                          format(desiredDiffMultiple))

                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[2]:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                currDt = steps[2]
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            elif diffs[2] > diffs[1] and \
                     diffs[2] > diffs[0] and \
                     (diffs[2] - diffs[1] > crossoverRequirement):
                
                # Crossed over to under 'desiredDiffMultiple' while
                # decreasing under 0.  This can happen when planets
                # are moving in retrograde motion.
                log.debug("Crossed over to under {} while decreasing under 0".\
                          format(desiredDiffMultiple))
                
                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[1]:
                        t1 = testDt
                    else:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                        
                    currErrorTd = t2 - t1
                    
                currDt = steps[2]
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            diffs.append(diffs[-1])
            del diffs[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addGeoJupiterSaturn15xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Jupiter and Saturn are multiples of 15
        degrees apart, geocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
            color = QColor(Qt.darkYellow)

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 15.0

        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        diffs = []
        diffs.append(None)
        diffs.append(None)
        diffs.append(None)
        
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[2] < endDt:
            
            currDt = steps[2]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getJupiterPlanetaryInfo(currDt)
            p2 = Ephemeris.getSaturnPlanetaryInfo(currDt)

            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.geocentric['sidereal']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p1.name,
            #                 p1.geocentric['tropical']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p2.name,
            #                 p2.geocentric['tropical']['longitude']))
            
            
            diffDeg = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0
                
            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg % desiredDiffMultiple
            
            if diffs[0] == None:
                diffs[0] = currDiff
            if diffs[1] == None:
                diffs[1] = currDiff
            diffs[2] = currDiff
            
            log.debug("steps[0] == {}".format(steps[0]))
            log.debug("steps[1] == {}".format(steps[1]))
            log.debug("steps[2] == {}".format(steps[2]))
            
            log.debug("diffs[0] == {}".format(diffs[0]))
            log.debug("diffs[1] == {}".format(diffs[1]))
            log.debug("diffs[2] == {}".format(diffs[2]))

            if diffs[2] < diffs[0] and \
                   diffs[2] < diffs[1] and \
                   (diffs[1] - diffs[2] > crossoverRequirement):
                
                # Crossed over to above 0 while increasing over
                # 'desiredDiffMultiple'.  This happens when planets
                # are moving in direct motion.
                log.debug("Crossed over to above 0 while increasing over {}".\
                          format(desiredDiffMultiple))

                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    p2 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[2]:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                currDt = steps[2]
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            elif diffs[2] > diffs[1] and \
                     diffs[2] > diffs[0] and \
                     (diffs[2] - diffs[1] > crossoverRequirement):
                
                # Crossed over to under 'desiredDiffMultiple' while
                # decreasing under 0.  This can happen when planets
                # are moving in retrograde motion.
                log.debug("Crossed over to under {} while decreasing under 0".\
                          format(desiredDiffMultiple))
                
                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getJupiterPlanetaryInfo(testDt)
                    p2 = Ephemeris.getSaturnPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[1]:
                        t1 = testDt
                    else:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                        
                    currErrorTd = t2 - t1
                    
                currDt = steps[2]
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            diffs.append(diffs[-1])
            del diffs[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addGeoVenusMars15xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Venus and Mars are multiples of 15
        degrees apart, geocentrically.
        
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = QColor(Qt.blue)

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 15.0

        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        diffs = []
        diffs.append(None)
        diffs.append(None)
        diffs.append(None)
        
        def getColorBasedOnDiffDeg(diffDeg):
            if colorWasSpecifiedFlag == False:
                color = None
                index = round(diffDeg / desiredDiffMultiple)
                if index == 0:
                    color = QColor(Qt.blue)
                elif index == 1:
                    color = QColor(Qt.gray)
                elif index == 2:
                    color = QColor(Qt.red)
                elif index == 3:
                    color = QColor(Qt.green)
                elif index == 4:
                    color = QColor(Qt.magenta)
                elif index == 5:
                    color = QColor(Qt.darkBlue)
                elif index == 6:
                    color = QColor(128, 62, 64)
                elif index == 7:
                    color = QColor(255, 170, 0)
                elif index == 8:
                    color = QColor(255, 0, 127)
                elif index == 9:
                    color = QColor(Qt.darkMagenta)
                elif index == 10:
                    color = QColor(35, 123, 128)
                elif index == 11:
                    color = QColor(99, 58, 128)
                elif index == 12:
                    color = QColor(84, 81, 64)
                elif index == 13:
                    color = QColor(128, 73, 71)
                elif index == 14:
                    color = QColor(108, 128, 97)
                elif index == 15:
                    color = QColor(Qt.darkGray)
                elif index == 16:
                    color = QColor(5, 85, 128)
                elif index == 17:
                    color = QColor(82, 101, 42)
                elif index == 18:
                    color = QColor(255, 170, 255)
                elif index == 19:
                    color = QColor(Qt.darkGreen)
                elif index == 20:
                    color = QColor(170, 85, 255)
                elif index == 21:
                    color = QColor(255, 170, 127)
                elif index == 22:
                    color = QColor(Qt.darkRed)
                elif index == 23:
                    color = QColor(170, 255, 0)
                else:
                    color = QColor(Qt.black)
                return color

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[2] < endDt:
            
            currDt = steps[2]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getVenusPlanetaryInfo(currDt)
            p2 = Ephemeris.getMarsPlanetaryInfo(currDt)

            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.geocentric['sidereal']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p1.name,
            #                 p1.geocentric['tropical']['longitude']))
            #log.debug("{} geocentric tropical longitude is: {}".\
            #          format(p2.name,
            #                 p2.geocentric['tropical']['longitude']))
            
            
            diffDeg = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0
                
            log.debug("diffDeg == {}".format(diffDeg))
            
            color = getColorBasedOnDiffDeg(diffDeg)
                    
            currDiff = diffDeg % desiredDiffMultiple
            
            if diffs[0] == None:
                diffs[0] = currDiff
            if diffs[1] == None:
                diffs[1] = currDiff
            diffs[2] = currDiff
            
            log.debug("steps[0] == {}".format(steps[0]))
            log.debug("steps[1] == {}".format(steps[1]))
            log.debug("steps[2] == {}".format(steps[2]))
            
            log.debug("diffs[0] == {}".format(diffs[0]))
            log.debug("diffs[1] == {}".format(diffs[1]))
            log.debug("diffs[2] == {}".format(diffs[2]))

            if diffs[2] < diffs[0] and \
                   diffs[2] < diffs[1] and \
                   (diffs[1] - diffs[2] > crossoverRequirement):
                
                # Crossed over to above 0 while increasing over
                # 'desiredDiffMultiple'.  This happens when planets
                # are moving in direct motion.
                log.debug("Crossed over to above 0 while increasing over {}".\
                          format(desiredDiffMultiple))

                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    p2 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
                    
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[2]:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                currDt = steps[2]

                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            elif diffs[2] > diffs[1] and \
                     diffs[2] > diffs[0] and \
                     (diffs[2] - diffs[1] > crossoverRequirement):
                
                # Crossed over to under 'desiredDiffMultiple' while
                # decreasing under 0.  This can happen when planets
                # are moving in retrograde motion.
                log.debug("Crossed over to under {} while decreasing under 0".\
                          format(desiredDiffMultiple))
                
                # Timestamp is between steps[2] and steps[1].
                
                # This is the upper-bound of the error timedelta.
                t1 = steps[1]
                t2 = steps[2]
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
                    
                    p1 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    p2 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.geocentric['sidereal']['longitude'] - \
                            p2.geocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0
            
                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < diffs[1]:
                        t1 = testDt
                    else:
                        t2 = testDt
                        
                        # Update the curr values as the later boundary.
                        steps[2] = t2
                        diffs[2] = testDiff
                        
                    currErrorTd = t2 - t1
                    
                currDt = steps[2]
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            diffs.append(diffs[-1])
            del diffs[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addHelioVenusMars15xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Venus and Mars are multiples of 15
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = QColor(Qt.blue)

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 15.0

        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Iterate through, creating artfacts and adding them as we go.
        prevDt = copy.deepcopy(startDt)
        currDt = copy.deepcopy(startDt)

        prevDiff = None
        currDiff = None
        
        def getColorBasedOnDiffDeg(diffDeg):
            if colorWasSpecifiedFlag == False:
                color = None
                index = round(diffDeg / desiredDiffMultiple)
                if index == 0:
                    color = QColor(Qt.blue)
                elif index == 1:
                    color = QColor(Qt.gray)
                elif index == 2:
                    color = QColor(Qt.red)
                elif index == 3:
                    color = QColor(Qt.green)
                elif index == 4:
                    color = QColor(Qt.magenta)
                elif index == 5:
                    color = QColor(Qt.darkBlue)
                elif index == 6:
                    color = QColor(128, 62, 64)
                elif index == 7:
                    color = QColor(255, 170, 0)
                elif index == 8:
                    color = QColor(255, 0, 127)
                elif index == 9:
                    color = QColor(Qt.darkMagenta)
                elif index == 10:
                    color = QColor(35, 123, 128)
                elif index == 11:
                    color = QColor(99, 58, 128)
                elif index == 12:
                    color = QColor(84, 81, 64)
                elif index == 13:
                    color = QColor(128, 73, 71)
                elif index == 14:
                    color = QColor(108, 128, 97)
                elif index == 15:
                    color = QColor(Qt.darkGray)
                elif index == 16:
                    color = QColor(5, 85, 128)
                elif index == 17:
                    color = QColor(82, 101, 42)
                elif index == 18:
                    color = QColor(255, 170, 255)
                elif index == 19:
                    color = QColor(Qt.darkGreen)
                elif index == 20:
                    color = QColor(170, 85, 255)
                elif index == 21:
                    color = QColor(255, 170, 127)
                elif index == 22:
                    color = QColor(Qt.darkRed)
                elif index == 23:
                    color = QColor(170, 255, 0)
                else:
                    color = QColor(Qt.black)
                return color

        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while currDt < endDt:
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getVenusPlanetaryInfo(currDt)
            p2 = Ephemeris.getMarsPlanetaryInfo(currDt)

            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))

            diffDeg = \
                p1.heliocentric['sidereal']['longitude'] - \
                p2.heliocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0

            log.debug("diffDeg == {}".format(diffDeg))
            
            color = getColorBasedOnDiffDeg(diffDeg)
                    
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
                    
                    p1 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    p2 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < currDiff:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addHelioVenusMars90xVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where Venus and Mars are multiples of 90
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


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = QColor(Qt.blue)

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 90.0

        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Iterate through, creating artfacts and adding them as we go.
        prevDt = copy.deepcopy(startDt)
        currDt = copy.deepcopy(startDt)

        prevDiff = None
        currDiff = None
        
        def getColorBasedOnDiffDeg(diffDeg):
            if colorWasSpecifiedFlag == False:
                color = None
                index = round(diffDeg / desiredDiffMultiple)
                if index == 0:
                    color = QColor(Qt.blue)
                elif index == 1:
                    color = QColor(Qt.gray)
                elif index == 2:
                    color = QColor(Qt.red)
                elif index == 3:
                    color = QColor(Qt.green)
                elif index == 4:
                    color = QColor(Qt.magenta)
                elif index == 5:
                    color = QColor(Qt.darkBlue)
                elif index == 6:
                    color = QColor(128, 62, 64)
                elif index == 7:
                    color = QColor(255, 170, 0)
                elif index == 8:
                    color = QColor(255, 0, 127)
                elif index == 9:
                    color = QColor(Qt.darkMagenta)
                elif index == 10:
                    color = QColor(35, 123, 128)
                elif index == 11:
                    color = QColor(99, 58, 128)
                elif index == 12:
                    color = QColor(84, 81, 64)
                elif index == 13:
                    color = QColor(128, 73, 71)
                elif index == 14:
                    color = QColor(108, 128, 97)
                elif index == 15:
                    color = QColor(Qt.darkGray)
                elif index == 16:
                    color = QColor(5, 85, 128)
                elif index == 17:
                    color = QColor(82, 101, 42)
                elif index == 18:
                    color = QColor(255, 170, 255)
                elif index == 19:
                    color = QColor(Qt.darkGreen)
                elif index == 20:
                    color = QColor(170, 85, 255)
                elif index == 21:
                    color = QColor(255, 170, 127)
                elif index == 22:
                    color = QColor(Qt.darkRed)
                elif index == 23:
                    color = QColor(170, 255, 0)
                else:
                    color = QColor(Qt.black)
                return color

        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while currDt < endDt:
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getVenusPlanetaryInfo(currDt)
            p2 = Ephemeris.getMarsPlanetaryInfo(currDt)

            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['sidereal']['longitude']))
            log.debug("{} heliocentric sidereal longitude is: {}".\
                      format(p2.name,
                             p2.heliocentric['sidereal']['longitude']))

            diffDeg = \
                p1.heliocentric['sidereal']['longitude'] - \
                p2.heliocentric['sidereal']['longitude']
            if diffDeg < 0:
                diffDeg += 360.0

            log.debug("diffDeg == {}".format(diffDeg))
            
            color = getColorBasedOnDiffDeg(diffDeg)
                    
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
                    
                    p1 = Ephemeris.getVenusPlanetaryInfo(testDt)
                    p2 = Ephemeris.getMarsPlanetaryInfo(testDt)
                    
                    diffDeg = \
                            p1.heliocentric['sidereal']['longitude'] - \
                            p2.heliocentric['sidereal']['longitude']
                    if diffDeg < 0:
                        diffDeg += 360.0

                    testDiff = diffDeg % desiredDiffMultiple
                    if testDiff < currDiff:
                        t2 = testDt

                        # Update the curr values as the later boundary.
                        currDt = t2
                        currDiff = testDiff
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addPlanetCrossingLongitudeDegVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        centricityType, longitudeType, planetName, degree,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where a certain planet crosses a certain degree
        of longitude.
        
        The algorithm used assumes that a step size won't move the
        planet more than 1/3 of a circle.
        
        Note: Default tag used for the artifacts added is the name of
        this function, without the word 'add' at the beginning, and with
        the type of line it is appended (geo/helio, trop/sid, planet name).
        
        Arguments:
        pcdd          - PriceChartDocumentData object that will be modified.
        startDt       - datetime.datetime object for the starting timestamp
                        to do the calculations for artifacts.
        endDt         - datetime.datetime object for the ending timestamp
                        to do the calculations for artifacts.
        highPrice     - float value for the high price to end the vertical line.
        lowPrice      - float value for the low price to end the vertical line.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        planetName    - str value holding the name fo the planet to do
                        the search for.
        degree        - float value for the degree of longitude that should be
                        crossed in order to trigger a vertical line being drawn.
        color         - QColor object for what color to draw the lines.
                        If this is set to None, then the default color
                        will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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


        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            log.error("Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig))
            rv = False
            return rv

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            log.error("Invalid input: longitudeType is invalid.  " + \
                      "Value given was: {}".format(longitudeTypeOrig))
            rv = False
            return rv

        # Field name we are getting.
        fieldName = "longitude"
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)


        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:]

            if centricityType.startswith("geo"):
                tag += "_Geo"
            elif centricityType.startswith("topo"):
                tag += "_Topo"
            elif centricityType.startswith("helio"):
                tag += "_Helio"

            if longitudeType.startswith("trop"):
                tag += "_Trop"
            elif longitudeType.startswith("sid"):
                tag += "_Sid"

            tag += "_{}_Deg_".format(degree) + planetName
            
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):
            
            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
            
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudes = []
        longitudes.append(None)
        longitudes.append(None)
        
        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
            
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            longitudes[-1] = getFieldValue(p1, fieldName)
            
            log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))
            
            if longitudes[-2] != None:
                
                currValue = None
                prevValue = None
                desiredDegree = None
                crossedOverZeroDegrees = None

                # This algorithm assumes that a step size won't move the
                # planet more than 1/3 of a circle.
                if longitudes[-2] > 240 and longitudes[-1] < 120:
                    # Hopped over 0 degrees from below to above.
                    prevValue = longitudes[-2]
                    currValue = longitudes[-1] + 360
                    desiredDegree = degree + 360
                    crossedOverZeroDegrees = True
                elif longitudes[-2] < 120 and longitudes[-1] > 240:
                    # Hopped over 0 degrees from above to below.
                    prevValue = longitudes[-2] + 360
                    currValue = longitudes[-1]
                    desiredDegree = degree
                    crossedOverZeroDegrees = True
                else:
                    # Did not cross 0 degrees.
                    prevValue = longitudes[-2]
                    currValue = longitudes[-1]
                    desiredDegree = degree
                    crossedOverZeroDegrees = False

                if prevValue < desiredDegree and currValue >= desiredDegree:
                    log.debug("Crossed over from below to above!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if longitudes[-2] > 240 and testValue < 120:
                            testValue += 360
                        
                        if testValue < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt
    
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    longitudes[-1] = Util.toNormalizedAngle(currValue)
                    
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
                elif prevValue >= desiredDegree and currValue < desiredDegree:
                    log.debug("Crossed over from above to below!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if longitudes[-2] > 240 and testValue < 120:
                            testValue += 360
                        
                        if testValue >= desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                            
                        currErrorTd = t2 - t1
                    
                    # Update our lists.
                    steps[-1] = currDt
                    longitudes[-1] = Util.toNormalizedAngle(currValue)
                    
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
            
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudes.append(None)
            del longitudes[0]

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addBayerTimeFactorsAstroVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where all planets (excluding the Moon) transit
        across the following places, geocentrically, in the tropical zodiac:

        13 deg 36' 12" Taurus (43.6033333333333 degrees longitude)
        16 deg 21' 48" Virgo  (166.3633333333333 degrees longitude)
        11 deg 04' 56" Capricorn (281.0822222222222 degrees longitude)
        19 deg 15' 24" Capricorn (289.2566666666666 degrees longitude)
        
        Note: Default tag used for the artifacts added is the name of
        this function, without the word 'add' at the beginning, and
        with the str for the relevant planet name appended.
        
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

        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = QColor(Qt.blue)

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

        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Differencial multiple we are looking for, in degrees.
        #
        # Note, the below algorithm assumes that 360 is evenly
        # divisible by 'desiredDiffMultiple'.  Otherwise it will
        # not catch all cases (e.g. if we are looking for 14
        # degree multiples, it will catch if the diffDeg is 14,
        # but not if the diffDeg is -14).
        desiredDiffMultiple = 360.0

        # Parameter for a test to show that it actually crossed over
        # the boundary of the degree differential multiple.
        crossoverRequirement = (2/3) * desiredDiffMultiple
        
        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Get planetary ids that we want to get info for.
        planetNames = []
        planetNames.append(Ephemeris.getSunPlanetaryInfo(now).name)
        #planetNames.append(Ephemeris.getMoonPlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getMercuryPlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getVenusPlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getMarsPlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getJupiterPlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getSaturnPlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getUranusPlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getNeptunePlanetaryInfo(now).name)
        planetNames.append(Ephemeris.getPlutoPlanetaryInfo(now).name)
        

        # Cross-over points.
        # 13 deg 36' 12" Taurus (43.6033333333333 degrees longitude)
        # 16 deg 21' 48" Virgo  (166.3633333333333 degrees longitude)
        # 11 deg 04' 56" Capricorn (281.0822222222222 degrees longitude)
        # 19 deg 15' 24" Capricorn (289.2566666666666 degrees longitude)
        crossOverPoints = [43.6033333333333,
                           166.3633333333333,
                           281.0822222222222,
                           289.2566666666666]

        copIndex = None
        
        for copIndex in range(len(crossOverPoints)):
            cop = crossOverPoints[copIndex]
            log.info("Working on cross-over-point {} ({})".\
                     format(AstrologyUtils.\
                            convertLongitudeToStrWithRasiAbbrev(cop),
                            cop))
                               
            if colorWasSpecifiedFlag == False:
                # Use custom colors for each index of the crossOverPoints.
                if copIndex == 0:
                    color = QColor(Qt.blue)
                elif copIndex == 1:
                    color = QColor(Qt.red)
                elif copIndex == 2:
                    color = QColor(Qt.green)
                elif copIndex == 3:
                    color = QColor(Qt.darkYellow)
            
            for planetName in planetNames:
                log.info(\
                    "Working on planet '{}' for cross-over-point {} ({})".\
                    format(planetName,
                           AstrologyUtils.\
                           convertLongitudeToStrWithRasiAbbrev(cop),
                           cop))
                               

                steps = []
                steps.append(copy.deepcopy(startDt))
                steps.append(copy.deepcopy(startDt))
                steps.append(copy.deepcopy(startDt))

                diffs = []
                diffs.append(None)
                diffs.append(None)
                diffs.append(None)
        
                # Iterate through, creating artfacts and adding them as we go.
                log.debug("Stepping through timestamps from {} to {} ...".\
                          format(Ephemeris.datetimeToStr(startDt),
                                 Ephemeris.datetimeToStr(endDt)))
        
                while steps[2] < endDt:
                    
                    currDt = steps[2]
                    log.debug("Looking at currDt == {} ...".\
                              format(Ephemeris.datetimeToStr(currDt)))
                    
                    p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
        
                    #log.debug("{} geocentric sidereal longitude is: {}".\
                    #          format(p1.name,
                    #                 p1.geocentric['sidereal']['longitude']))
                    #log.debug("{} geocentric sidereal longitude is: {}".\
                    #          format(p2.name,
                    #                 p2.geocentric['sidereal']['longitude']))
                    log.debug("{} geocentric tropical longitude is: {}".\
                              format(p1.name,
                                     p1.geocentric['tropical']['longitude']))
                    #log.debug("{} geocentric tropical longitude is: {}".\
                    #          format(p2.name,
                    #                 p2.geocentric['tropical']['longitude']))
                    
                    diffDeg = \
                        p1.geocentric['tropical']['longitude'] - cop
                    if diffDeg < 0:
                        diffDeg += 360.0
                        
                    log.debug("diffDeg == {}".format(diffDeg))
                    
                    currDiff = diffDeg % desiredDiffMultiple
                    
                    if diffs[0] == None:
                        diffs[0] = currDiff
                    if diffs[1] == None:
                        diffs[1] = currDiff
                    diffs[2] = currDiff
                    
                    log.debug("steps[0] == {}".format(steps[0]))
                    log.debug("steps[1] == {}".format(steps[1]))
                    log.debug("steps[2] == {}".format(steps[2]))
                    
                    log.debug("diffs[0] == {}".format(diffs[0]))
                    log.debug("diffs[1] == {}".format(diffs[1]))
                    log.debug("diffs[2] == {}".format(diffs[2]))

                    if diffs[2] < diffs[0] and \
                           diffs[2] < diffs[1] and \
                           (diffs[1] - diffs[2] > crossoverRequirement):
                        
                        # Crossed over to above 0 while increasing over
                        # 'desiredDiffMultiple'.  This happens when planets
                        # are moving in direct motion.
                        log.debug("Crossed over to above 0 " +
                                  "while increasing over {}".\
                                  format(desiredDiffMultiple))
        
                        # Timestamp is between steps[2] and steps[1].
                        
                        # This is the upper-bound of the error timedelta.
                        t1 = steps[1]
                        t2 = steps[2]
                        currErrorTd = t2 - t1
        
                        # Refine the timestamp until it is less than
                        # the threshold.
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
                                          microseconds=(diffTd.\
                                                        microseconds / 2.0))
                            testDt = t1 + halfDiffTd
                            
                            p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                            
                            diffDeg = \
                                    p1.geocentric['tropical']['longitude'] - cop
                            if diffDeg < 0:
                                diffDeg += 360.0
                    
                            testDiff = diffDeg % desiredDiffMultiple
                            if testDiff < diffs[2]:
                                t2 = testDt
        
                                # Update the curr values as the later boundary.
                                steps[2] = t2
                                diffs[2] = testDiff
                            else:
                                t1 = testDt
                                
                            currErrorTd = t2 - t1
        
                        currDt = steps[2]
                        
                        # Create the artifact at the timestamp.
                        PlanetaryCombinationsLibrary.\
                            addVerticalLine(pcdd, currDt,
                                            highPrice, lowPrice,
                                            tag + "_" + p1.name, color)
                        numArtifactsAdded += 1
                        
                    elif diffs[2] > diffs[1] and \
                             diffs[2] > diffs[0] and \
                             (diffs[2] - diffs[1] > crossoverRequirement):
                        
                        # Crossed over to under 'desiredDiffMultiple' while
                        # decreasing under 0.  This can happen when planets
                        # are moving in retrograde motion.
                        log.debug("Crossed over to under {} while ".\
                                  format(desiredDiffMultiple) + \
                                  "decreasing under 0")
                        
                        # Timestamp is between steps[2] and steps[1].
                        
                        # This is the upper-bound of the error timedelta.
                        t1 = steps[1]
                        t2 = steps[2]
                        currErrorTd = t2 - t1
        
                        # Refine the timestamp until it is less than
                        # the threshold.
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
                                          microseconds=(diffTd.\
                                                        microseconds / 2.0))
                            testDt = t1 + halfDiffTd
                            
                            p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                            
                            diffDeg = \
                                    p1.geocentric['tropical']['longitude'] - cop
                            if diffDeg < 0:
                                diffDeg += 360.0
                    
                            testDiff = diffDeg % desiredDiffMultiple
                            if testDiff < diffs[1]:
                                t1 = testDt
                            else:
                                t2 = testDt
                                
                                # Update the curr values as the later boundary.
                                steps[2] = t2
                                diffs[2] = testDiff
                                
                            currErrorTd = t2 - t1
                            
                        currDt = steps[2]
                        
                        # Create the artifact at the timestamp.
                        PlanetaryCombinationsLibrary.\
                            addVerticalLine(pcdd, currDt,
                                            highPrice, lowPrice,
                                            tag + "_" + p1.name, color)
                        numArtifactsAdded += 1
                        
                    # Prepare for the next iteration.
                    steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
                    del steps[0]
                    diffs.append(diffs[-1])
                    del diffs[0]
                    
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addTimeMeasurementAndTiltedTextForNakshatraTransits(\
        pcdd, startDt, endDt,
        price,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(minutes=1)):
        """Adds TimeMeasurementGraphicsItems and TiltedText to
        locations where a certain planet crosses over the Nakshatra
        boundaries.  The time measurement boundaries are where the
        planet is in a certain nakshatra in direct motion or in
        retrograde motion.  The TextGraphicsItem added will describe
        what kind of effects is being shown.

        Warning: This function has a flaw.  It doesn't account for the
        case where if a planet p at t1 is at nakshatra 1 going direct,
        and then at t2, planet p has entered nakshatra 2 and started
        to go retrograde.
        
        Note: Default tag used for the artifacts added is the name of
        this function, without the word 'add' at the beginning, and
        with the str for the relevant planet name appended.
        
        Arguments:
        pcdd       - PriceChartDocumentData object that will be modified.
        startDt    - datetime.datetime object for the starting timestamp
                     to do the calculations for artifacts.
        endDt      - datetime.datetime object for the ending timestamp
                     to do the calculations for artifacts.
        price      - float value for price location to drawn the
                     TimeMeasurementGraphicsItem.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color      - QColor object for what color to draw the lines.
                     If this is set to None, then the default color will
                     be used.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """

        log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = True

        # Make sure the inputs are valid.
        if endDt < startDt:
            log.error("Invalid input: 'endDt' must be after 'startDt'")
            rv = False
            return rv
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Set the step size.
        #stepSizeTd = datetime.timedelta(minutes=1)
        stepSizeTd = datetime.timedelta(hours=1)

        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Longitudes of the steps saved (list of float).
        longitudes = []
        longitudes.append(None)
        longitudes.append(None)

        # Direction of movement of the previous steps (direct or retrograde).
        directMotion = 1
        retrogradeMotion = -1
        unknownMotion = 0
        motions = []
        motions.append(unknownMotion)
        motions.append(unknownMotion)

        # Start and end timestamps used for the location of the
        # TimeMeasurementGraphicsItem.
        startTimeMeasurementDt = None
        endTimeMeasurementDt = None

        # Sub-function that does the adding of the artifacts for this
        # function, since this is a bit more verbose than usual.
        def addArtifacts(pcdd,
                         planetName,
                         startTimeMeasurementDt,
                         endTimeMeasurementDt,
                         tag,
                         color):
            
            startPI = Ephemeris.getPlanetaryInfo(planetName,
                                                 startTimeMeasurementDt)
            endPI = Ephemeris.getPlanetaryInfo(planetName,
                                               endTimeMeasurementDt)
            
            y = PlanetaryCombinationsLibrary.\
                scene.priceToSceneYPos(price)
            startPointX = PlanetaryCombinationsLibrary.\
                scene.datetimeToSceneXPos(startTimeMeasurementDt)
            endPointX = PlanetaryCombinationsLibrary.\
                scene.datetimeToSceneXPos(endTimeMeasurementDt)

            item = TimeMeasurementGraphicsItem()
            item.loadSettingsFromAppPreferences()
            item.loadSettingsFromPriceBarChartSettings(\
                pcdd.priceBarChartSettings)
            
            artifact1 = item.getArtifact()
            artifact1.addTag(tag)
            artifact1.setColor(color)
            artifact1.setShowBarsTextFlag(False)
            artifact1.setShowSqrtBarsTextFlag(False)
            artifact1.setShowSqrdBarsTextFlag(False)
            artifact1.setShowHoursTextFlag(False)
            artifact1.setShowSqrtHoursTextFlag(False)
            artifact1.setShowSqrdHoursTextFlag(False)
            artifact1.setShowDaysTextFlag(False)
            artifact1.setShowSqrtDaysTextFlag(False)
            artifact1.setShowSqrdDaysTextFlag(False)
            artifact1.setShowWeeksTextFlag(False)
            artifact1.setShowSqrtWeeksTextFlag(False)
            artifact1.setShowSqrdWeeksTextFlag(False)
            artifact1.setShowMonthsTextFlag(False)
            artifact1.setShowSqrtMonthsTextFlag(False)
            artifact1.setShowSqrdMonthsTextFlag(False)
            artifact1.setShowTimeRangeTextFlag(False)
            artifact1.setShowSqrtTimeRangeTextFlag(False)
            artifact1.setShowSqrdTimeRangeTextFlag(False)
            artifact1.setShowScaledValueRangeTextFlag(False)
            artifact1.setShowSqrtScaledValueRangeTextFlag(False)
            artifact1.setShowSqrdScaledValueRangeTextFlag(False)
            artifact1.setShowAyanaTextFlag(False)
            artifact1.setShowSqrtAyanaTextFlag(False)
            artifact1.setShowSqrdAyanaTextFlag(False)
            artifact1.setShowMuhurtaTextFlag(False)
            artifact1.setShowSqrtMuhurtaTextFlag(False)
            artifact1.setShowSqrdMuhurtaTextFlag(False)
            artifact1.setShowVaraTextFlag(False)
            artifact1.setShowSqrtVaraTextFlag(False)
            artifact1.setShowSqrdVaraTextFlag(False)
            artifact1.setShowRtuTextFlag(False)
            artifact1.setShowSqrtRtuTextFlag(False)
            artifact1.setShowSqrdRtuTextFlag(False)
            artifact1.setShowMasaTextFlag(False)
            artifact1.setShowSqrtMasaTextFlag(False)
            artifact1.setShowSqrdMasaTextFlag(False)
            artifact1.setShowPaksaTextFlag(False)
            artifact1.setShowSqrtPaksaTextFlag(False)
            artifact1.setShowSqrdPaksaTextFlag(False)
            artifact1.setShowSamaTextFlag(False)
            artifact1.setShowSqrtSamaTextFlag(False)
            artifact1.setShowSqrdSamaTextFlag(False)
            artifact1.setStartPointF(QPointF(startPointX, y))
            artifact1.setEndPointF(QPointF(endPointX, y))
            
            # Append the artifact.
            log.info("Adding '{}' ".format(tag) + \
                     "PriceBarChartTimeMeasurementArtifact at " + \
                     "({}, {}) to ({}, {}), or ({} to {}) ...".\
                     format(startPointX, y,
                            endPointX, y,
                            Ephemeris.\
                            datetimeToStr(startTimeMeasurementDt),
                            Ephemeris.\
                            datetimeToStr(endTimeMeasurementDt)))
            
            pcdd.priceBarChartArtifacts.append(artifact1)
            
            startNakshatraAbbrev = \
                AstrologyUtils.\
                convertLongitudeToNakshatraAbbrev(\
                startPI.geocentric['sidereal']['longitude'])
            
            endNakshatraAbbrev = \
                AstrologyUtils.\
                convertLongitudeToNakshatraAbbrev(\
                endPI.geocentric['sidereal']['longitude'])
            
            startMotionAbbrev = None
            if startPI.geocentric['tropical']['longitude_speed'] < 0:
                startMotionAbbrev = "R"
            else:
                startMotionAbbrev = "D"
            
            endMotionAbbrev = None
            if endPI.geocentric['tropical']['longitude_speed'] < 0:
                endMotionAbbrev = "R"
            else:
                endMotionAbbrev = "D"
                
            text = "{}: {} {} to {} {}".\
                    format(planetName,
                           startMotionAbbrev,
                           startNakshatraAbbrev,
                           endMotionAbbrev,
                           endNakshatraAbbrev)
            textRotationAngle = 90.0
            
            x = (startPointX + endPointX) / 2
            
            item = TextGraphicsItem()
            item.loadSettingsFromAppPreferences()
            item.loadSettingsFromPriceBarChartSettings(\
                pcdd.priceBarChartSettings)
            
            artifact2 = item.getArtifact()
            artifact2.addTag(tag)
            artifact2.setColor(color)
            artifact2.setText(text)
            artifact2.setTextRotationAngle(textRotationAngle)
            artifact2.setPos(QPointF(x, y))
            
            # Append the artifact.
            log.info("Adding '{}' PriceBarChartTextArtifact at ".\
                     format(tag) + \
                     "           ({}, {}) to ({}, {}), or ({} to {}) ...".\
                     format(startPointX, y,
                            endPointX, y,
                            Ephemeris.\
                            datetimeToStr(startTimeMeasurementDt),
                            Ephemeris.\
                            datetimeToStr(endTimeMeasurementDt)))
            pcdd.priceBarChartArtifacts.append(artifact2)
                    
        
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} geocentric sidereal longitude is: {}".\
                      format(p1.name,
                             p1.geocentric['sidereal']['longitude']))
            
            longitudes[-1] = p1.geocentric['sidereal']['longitude']
            
            speed = p1.geocentric['tropical']['longitude_speed']
            if speed < 0:
                motions[-1] = retrogradeMotion
            else:
                motions[-1] = directMotion
            
            # Get the nakshatras of the current and previous steps.
            # 0 is Aswini.
            currNakshatraIndex = \
                math.floor(longitudes[-1] / (360 / 27))
            prevNakshatraIndex = None
            if longitudes[-2] == None:
                prevNakshatraIndex = currNakshatraIndex
            else:
                prevNakshatraIndex = math.floor(longitudes[-2] / (360 / 27))
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".format(i, steps[i]))
            for i in range(len(longitudes)):
                log.debug("longitudes[{}] == {}".format(i, longitudes[i]))
            for i in range(len(motions)):
                log.debug("motions[{}] == {}".format(i, motions[i]))
            log.debug("prevNakshatraIndex == {}".format(prevNakshatraIndex))
            log.debug("currNakshatraIndex == {}".format(currNakshatraIndex))


            if currNakshatraIndex != prevNakshatraIndex:
                # Shifted over a nakshatra.  Now we need to
                # narrow down onto the timestamp when this happened,
                # within the maxErrorTd timedelta.

                # Timestamp is between steps[-2] and steps[-1].

                # This is the upper-bound of the error timedelta.
                t1 = steps[-2]
                t2 = steps[-1]
                currErrorTd = t2 - t1

                currLongitude = longitudes[-1]
                currMotion = motions[-1]
                
                # Refine the timestamp until it is less than
                # the threshold.
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
                                  microseconds=(diffTd.\
                                                microseconds / 2.0))
                    testDt = t1 + halfDiffTd
                    
                    p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                    longitude = p1.geocentric['sidereal']['longitude']
                    speed = p1.geocentric['tropical']['longitude_speed']
                    motion = None
                    if speed < 0:
                        motion = retrogradeMotion
                    else:
                        motion = directMotion
                    
                    if math.floor(longitude / (360 / 27)) == currNakshatraIndex:
                        t2 = testDt

                        # Update curr values.
                        currLongitude = longitude
                        currNakshatraIndex = math.floor(longitude / (360 / 27))
                        currMotion = motion
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                # t2 holds the cross-over timestamp that is within
                # maxErrorTd to the nakshatra cross-over longitude.
                currDt = t2

                # Make sure the stored values for the steps are saved.
                steps[-1] = currDt
                longitudes[-1] = currLongitude
                motions[-1] = currMotion

                # Check to see if we have a start and end point.  If
                # yes, then we will be creating a
                # TimeMeasurementGraphicsItem and a TextGraphicsItem.
                if startTimeMeasurementDt == None:
                    startTimeMeasurementDt = currDt
                else:
                    endTimeMeasurementDt = currDt

                    # Okay, now create the items since we have the
                    # start and end timestamps for them.
                    addArtifacts(pcdd,
                                 planetName,
                                 startTimeMeasurementDt,
                                 endTimeMeasurementDt,
                                 tag,
                                 color)

                    # Shift start and end timestamp.  The start is now
                    # the end, and the end is cleared.
                    startTimeMeasurementDt = endTimeMeasurementDt
                    endTimeMeasurementDt = None
                
                    numArtifactsAdded += 2
                
            elif motions[-1] != motions[-2]:
                # Just went from retrograde to direct, or direct to
                # retrograde.  Now we need to narrow down onto the
                # timestamp when this happened, within the maxErrorTd
                # timedelta.
                
                # Timestamp is between steps[-2] and steps[-1].

                # This is the upper-bound of the error timedelta.
                t1 = steps[-2]
                t2 = steps[-1]
                currErrorTd = t2 - t1

                currLongitude = longitudes[-1]
                currMotion = motions[-1]
                
                # Refine the timestamp until it is less than
                # the threshold.
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
                                  microseconds=(diffTd.\
                                                microseconds / 2.0))
                    testDt = t1 + halfDiffTd
                    
                    p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                    longitude = p1.geocentric['sidereal']['longitude']
                    speed = p1.geocentric['tropical']['longitude_speed']
                    motion = None
                    if speed < 0:
                        motion = retrogradeMotion
                    else:
                        motion = directMotion
                    
                    if motion == currMotion:
                        t2 = testDt

                        # Update curr values.
                        currLongitude = longitude
                        currNakshatraIndex = math.floor(longitude / (360 / 27))
                        currMotion = motion
                    else:
                        t1 = testDt
                        
                    currErrorTd = t2 - t1

                # t2 holds the cross-over timestamp that is within
                # maxErrorTd to the nakshatra cross-over longitude.
                currDt = t2

                # Make sure the stored values for the steps are saved.
                steps[-1] = currDt
                longitudes[-1] = currLongitude
                motions[-1] = currMotion

                # Check to see if we have a start and end point.  If
                # yes, then we will be creating a
                # TimeMeasurementGraphicsItem and a TextGraphicsItem.
                if startTimeMeasurementDt == None:
                    startTimeMeasurementDt = currDt
                else:
                    endTimeMeasurementDt = currDt

                    # Okay, now create the items since we have the
                    # start and end timestamps for them.
                    addArtifacts(pcdd,
                                 planetName,
                                 startTimeMeasurementDt,
                                 endTimeMeasurementDt,
                                 tag,
                                 color)
                    
                    numArtifactsAdded += 2
                
                    # Shift start and end timestamp.  The start is now
                    # the end, and the end is cleared.
                    startTimeMeasurementDt = endTimeMeasurementDt
                    endTimeMeasurementDt = None

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudes.append(None)
            del longitudes[0]
            motions.append(unknownMotion)
            del motions[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    
    @staticmethod
    def addGeoDeclinationLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        stepSizeTd=datetime.timedelta(days=1)):
        """Adds a bunch of line segments that represent a given
        planet's declination degrees.  The start and end points of
        each line segment is 'stepSizeTd' distance away.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for +25 degrees declination.
        lowPrice  - float value for the low price which represents
                    the location for +25 degrees declination.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees declination.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Value for the absolute value of the maximum/minimum declination.
        absoluteMaxDeclination = 25.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Declination of the steps saved (list of float).
        declinations = []
        declinations.append(None)
        declinations.append(None)

        # Start and end timestamps used for the location of the
        # LineSegmentGraphicsItem.
        startLineSegmentDt = None
        endLineSegmentDt = None

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} declination is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['declination']))
            
            declinations[-1] = p1.geocentric['tropical']['declination']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(declinations)):
                log.debug("declinations[{}] == {}".format(i, declinations[i]))


            if declinations[-2] != None:
                pricePerDeclinationDegree = \
                    (highPrice - avgPrice) / absoluteMaxDeclination

                
                startPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-2])
                endPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-1])
        
                startPointPrice = \
                    avgPrice + (declinations[-2] * pricePerDeclinationDegree)
                startPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(startPointPrice)
                
                endPointPrice = \
                    avgPrice + (declinations[-1] * pricePerDeclinationDegree)
                endPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(endPointPrice)
                
                item = LineSegmentGraphicsItem()
                item.loadSettingsFromAppPreferences()
                item.loadSettingsFromPriceBarChartSettings(\
                    pcdd.priceBarChartSettings)
                
                artifact = item.getArtifact()
                artifact.addTag(tag)
                artifact.setTiltedTextFlag(False)
                artifact.setAngleTextFlag(False)
                artifact.setColor(color)
                artifact.setStartPointF(QPointF(startPointX, startPointY))
                artifact.setEndPointF(QPointF(endPointX, endPointY))
                
                # Append the artifact.
                log.info("Adding '{}' {} at ".\
                         format(tag, artifact.__class__.__name__) + \
                         "({}, {}) to ({}, {}), or ({} to {}) ...".\
                         format(startPointX, startPointY,
                                endPointX, endPointY,
                                Ephemeris.datetimeToStr(steps[-2]),
                                Ephemeris.datetimeToStr(steps[-1])))
                
                pcdd.priceBarChartArtifacts.append(artifact)
                
                numArtifactsAdded += 1

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            declinations.append(None)
            del declinations[0]
            
        
        # Add a horizontal line for the zero velocity.
        PlanetaryCombinationsLibrary.\
            addHorizontalLine(pcdd, startDt, endDt, avgPrice,
                              tag="DeclinationZeroLine",
                              color=QColor(Qt.black))
        numArtifactsAdded += 1

        
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    

    @staticmethod
    def addZeroDeclinationVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's
        declination changes from increasing to decreasing or
        decreasing to increasing.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees declination.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Desired declination degree.
        desiredDegree = 0.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Declination of the steps saved (list of float).
        declinations = []
        declinations.append(None)
        declinations.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} declination is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['declination']))

            declinations[-1] = p1.geocentric['tropical']['declination']

            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(declinations)):
                log.debug("declinations[{}] == {}".format(i, declinations[i]))

            if declinations[-2] != None:
                
                if declinations[-2] < desiredDegree and \
                       declinations[-1] >= desiredDegree:
    
                    log.debug("Crossed over from below to above!")
                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1
    
                    # Refine the timestamp until it is less than the threshold.
                    currDiff = None
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
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
    
                        diffDeg = p1.geocentric['tropical']['declination']
                        
                        testDiff = diffDeg
                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt
    
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                            
                        currErrorTd = t2 - t1
    
                    if currDiff != None:
                        steps[-1] = currDt
                        declinations[-1] = currDiff
    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.green)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
                elif declinations[-2] > desiredDegree and \
                       declinations[-1] <= desiredDegree:

                    log.debug("Crossed over from above to below!")
                    
                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1
    
                    # Refine the timestamp until it is less than the threshold.
                    currDiff = None
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
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
    
                        diffDeg = p1.geocentric['tropical']['declination']
                        
                        testDiff = diffDeg
                        if testDiff > desiredDegree:
                            t1 = testDt
                            
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                            
                        currErrorTd = t2 - t1
    
                    if currDiff != None:
                        steps[-1] = currDt
                        declinations[-1] = currDiff
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.darkGreen)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            declinations.append(None)
            del declinations[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addDeclinationVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's
        declination changes from increasing to decreasing or
        decreasing to increasing.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees declination.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Declination of the steps saved (list of float).
        declinationVelocitys = []
        declinationVelocitys.append(None)
        declinationVelocitys.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} declination speed is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['declination_speed']))
            
            declinationVelocitys[-1] = \
                p1.geocentric['tropical']['declination_speed']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(declinationVelocitys)):
                log.debug("declinationVelocitys[{}] == {}".\
                          format(i, declinationVelocitys[i]))

            if declinationVelocitys[-2] != None:

                if declinationVelocitys[-2] > 0 > declinationVelocitys[-1]:
    
                    # Was increasing, but now decreasing.
                    log.debug("Started decreasing after previously increasing.")
    
                    lineDt = steps[-1]
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.red)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
    
                elif declinationVelocitys[-2] < 0 < declinationVelocitys[-1]:
    
                    # Was decreasing, but now increasing.
                    log.debug("Started increasing after previously decreasing.")
    
                    lineDt = steps[-1]
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.darkRed)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            declinationVelocitys.append(None)
            del declinationVelocitys[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addGeoLongitudeElongationVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's
        geocentric longitude elongation extremes are.  Lines are also
        added for the the superior and inferior conjunction moments in
        time.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Longitude of the steps saved (list of float).
        longitudeDiffs = []
        longitudeDiffs.append(None)
        longitudeDiffs.append(None)
        longitudeDiffs.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            p2 = Ephemeris.getPlanetaryInfo("Sun", currDt)
            
            longitudeDiffs[-1] = \
                p1.geocentric['sidereal']['longitude'] - \
                p2.geocentric['sidereal']['longitude']

            if longitudeDiffs[-1] > 180 or longitudeDiffs[-1] < -180:
                # These planets are straddling 0 degrees Aries.
                # Make adjustments so that the longitude difference is
                # correct.

                if longitudeDiffs[-1] > 180:
                    longitudeDiffs[-1] = \
                        p1.geocentric['sidereal']['longitude'] - \
                        (360.0 + p2.geocentric['sidereal']['longitude'])
                elif longitudeDiffs[-1] < -180:
                    longitudeDiffs[-1] = \
                        (360.0 + p1.geocentric['sidereal']['longitude']) - \
                        p2.geocentric['sidereal']['longitude']
                
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(longitudeDiffs)):
                log.debug("longitudeDiffs[{}] == {}".\
                          format(i, longitudeDiffs[i]))
            
            if longitudeDiffs[-2] != None and longitudeDiffs[-3] != None:

                if longitudeDiffs[-3] < longitudeDiffs[-2] and \
                   longitudeDiffs[-1] < longitudeDiffs[-2]:
    
                    # Was increasing, but now decreasing.
                    log.debug("Started decreasing after previously increasing.")
    
                    # Use the middle datetime in our history as the
                    # location, which will ensure it is within the desired
                    # error timedelta.
                    lineDt = steps[-2]
    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.blue)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
                elif longitudeDiffs[-3] > longitudeDiffs[-2] and \
                   longitudeDiffs[-1] > longitudeDiffs[-2]:
    
                    # Was decreasing, but now increasing.
                    log.debug("Started increasing after previously decreasing.")
    
                    # Use the middle datetime in our history as the
                    # location, which will ensure it is within the desired
                    # error timedelta.
                    lineDt = steps[-2]
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.darkBlue)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
    
                # Check for conjunctions.
                isConjunction = False
                if longitudeDiffs[-2] < 0.0 and longitudeDiffs[-1] > 0.0:
                    log.debug("Crossed sun's longitude from below.")
                    isConjunction = True
                elif longitudeDiffs[-2] > 0.0 and longitudeDiffs[-1] < 0.0:
                    log.debug("Crossed sun's longitude from above.")
                    isConjunction = True
    
                if isConjunction == True:
                    # See if it is a superior or inferior conjunction by
                    # checking the planet position relative to Earth.
                    p3 = Ephemeris.getPlanetaryInfo("Earth", currDt)
    
                    diff = p1.heliocentric['sidereal']['longitude'] - \
                           p3.heliocentric['sidereal']['longitude']
    
                    lineDt = currDt
                    
                    if abs(diff) < 90:
                        # Inferior conjunction.
                        log.debug("Inferior conjunction.")
    
                        if colorWasSpecifiedFlag == False:
                            color = QColor(Qt.magenta)
                        
                        # Create the artifact at the timestamp.
                        PlanetaryCombinationsLibrary.\
                            addVerticalLine(pcdd, lineDt,
                                            highPrice, lowPrice, tag, color)
                        numArtifactsAdded += 1
                    else:
                        # Superior conjunction.
                        log.debug("Superior conjunction.")
    
                        if colorWasSpecifiedFlag == False:
                            color = QColor(Qt.darkMagenta)
                        
                        # Create the artifact at the timestamp.
                        PlanetaryCombinationsLibrary.\
                            addVerticalLine(pcdd, lineDt,
                                            highPrice, lowPrice, tag, color)
                        numArtifactsAdded += 1
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudeDiffs.append(None)
            del longitudeDiffs[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addGeoLongitudeVelocityLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        stepSizeTd=datetime.timedelta(days=1)):
        """Adds a bunch of line segments that represent a given
        planet's longitude speed.  The start and end points of
        each line segment is 'stepSizeTd' distance away.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for highest velocity.
        lowPrice  - float value for the low price which represents
                    the location for lowest velocity.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 velocity.
        avgPrice = (lowPrice + highPrice) / 2.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            
        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Velocity of the steps saved (list of float).
        velocitys = []
        velocitys.append(None)
        velocitys.append(None)

        # Start and end timestamps used for the location of the
        # LineSegmentGraphicsItem.
        startLineSegmentDt = None
        endLineSegmentDt = None

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        
        maxAbsoluteSpeed = 0.0
        helioSpeed = 0.0
        if planetName == "Moon":
            maxValue = abs(15.3854340872)
            minValue = abs(0.0)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Mercury":
            maxValue = abs(2.20247915641)
            minValue = abs(-1.38648011915)
            helioSpeed = 4.092346062424192
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Venus":
            maxValue = abs(1.25885851698)
            minValue = abs(-0.631105994856)
            helioSpeed = 1.6021312618132146
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Mars":
            maxValue = abs(0.791337340289)
            minValue = abs(-0.400655987562)
            helioSpeed = 0.5240395882
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Jupiter":
            maxValue = abs(0.242476279714)
            minValue = abs(-0.13658191218)
            helioSpeed = 0.08311070438168867
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Saturn":
            maxValue = abs(0.130369662001)
            minValue = abs(-0.0828733240411)
            helioSpeed = 0.033459674586075946
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Uranus":
            maxValue = abs(0.063236066386)
            minValue = abs(-0.0439273105247)
            helioSpeed = 0.011688655137431798
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Neptune":
            maxValue = abs(0.0380502077148)
            minValue = abs(-0.0283865987199)
            helioSpeed = 0.005981059976740323
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Pluto":
            maxValue = abs(0.040535459208)
            minValue = abs(-0.0282905050242)
            helioSpeed = 0.003972926492417422
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Mean North Node":
            maxValue = abs(0)
            minValue = abs(-0.0529539539963)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "True North Node":
            maxValue = abs(0.0583335323306)
            minValue = abs(-0.25912214133)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Mean Lunar Apogee":
            maxValue = abs(0.112068469719)
            minValue = abs(0)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Osculating Lunar Apogee":
            maxValue = abs(6.34870367365)
            minValue = abs(-3.61864664224)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Interpolated Lunar Apogee":
            maxValue = abs(0.236734866594)
            minValue = abs(-0.148972388849)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Interpolated Lunar Perigee":
            maxValue = abs(0.577564192133)
            minValue = abs(-2.26866537946)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Earth":
            maxValue = abs(0)
            minValue = abs(0)
            helioSpeed = 365.256366
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Chiron":
            maxValue = abs(0.145963623727)
            minValue = abs(-0.0794572071859)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Pholus":
            maxValue = abs(0.0657475495548)
            minValue = abs(-0.0478856503721)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Ceres":
            maxValue = abs(0.460418804451)
            minValue = abs(-0.238025771402)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Pallas":
            maxValue = abs(0.598055034244)
            minValue = abs(-0.342833713135)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Juno":
            maxValue = abs(0.597557822666)
            minValue = abs(-0.260653543849)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Vesta":
            maxValue = abs(0.541960483784)
            minValue = abs(-0.265968505255)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Isis":
            maxValue = abs(0.0206735201795)
            minValue = abs(-0.0155312857467)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "Nibiru":
            maxValue = abs(0.0776441794168)
            minValue = abs(-0.489747301768)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "MeanOfFive":
            maxValue = abs(0.0907366503314)
            minValue = abs(-0.0486608813613)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        elif planetName == "CycleOfEight":
            maxValue = abs(0.562461969991)
            minValue = abs(-0.239189857922)
            helioSpeed = 0.0
            if maxValue > minValue:
                maxAbsoluteSpeed = maxValue
            else:
                maxAbsoluteSpeed = minValue
        else:
            maxAbsoluteSpeed = 1.0
            helioSpeed = 0.0

        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} velocity is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['longitude_speed']))
            
            velocitys[-1] = p1.geocentric['tropical']['longitude_speed']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(velocitys)):
                log.debug("velocitys[{}] == {}".format(i, velocitys[i]))


            if velocitys[-2] != None:

                pricePerSpeedDeg = (highPrice - avgPrice) / maxAbsoluteSpeed
                
                startPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-2])
                endPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-1])
        
                startPointPrice = \
                    avgPrice + (velocitys[-2] * pricePerSpeedDeg)
                startPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(startPointPrice)
                
                endPointPrice = \
                    avgPrice + (velocitys[-1] * pricePerSpeedDeg)
                endPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(endPointPrice)
                
                item = LineSegmentGraphicsItem()
                item.loadSettingsFromAppPreferences()
                item.loadSettingsFromPriceBarChartSettings(\
                    pcdd.priceBarChartSettings)
                
                artifact = item.getArtifact()
                artifact.addTag(tag)
                artifact.setTiltedTextFlag(False)
                artifact.setAngleTextFlag(False)
                artifact.setColor(color)
                artifact.setStartPointF(QPointF(startPointX, startPointY))
                artifact.setEndPointF(QPointF(endPointX, endPointY))
                
                # Append the artifact.
                log.info("Adding '{}' {} at ".\
                         format(tag, artifact.__class__.__name__) + \
                         "({}, {}) to ({}, {}), or ({} to {}) ...".\
                         format(startPointX, startPointY,
                                endPointX, endPointY,
                                Ephemeris.datetimeToStr(steps[-2]),
                                Ephemeris.datetimeToStr(steps[-1])))
                
                pcdd.priceBarChartArtifacts.append(artifact)
                
                numArtifactsAdded += 1

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            velocitys.append(None)
            del velocitys[0]


        # Add a horizontal line for the zero velocity.
        if True:
            PlanetaryCombinationsLibrary.\
                addHorizontalLine(pcdd, startDt, endDt, avgPrice,
                                  tag="VelocityZeroLine_{}".format(planetName),
                                  color=QColor(Qt.black))
            numArtifactsAdded += 1

        # Add a horizontal line for speed of:
        #   SunSpeed * -1,
        #   SunSpeed * 1,
        #   SunSpeed * 2,
        if True:
            sunSpeed = 1.014555555555555
            
            pricePerSpeedDeg = (highPrice - avgPrice) / maxAbsoluteSpeed
            #log.debug("avgPrice == {}".format(avgPrice))
            #log.debug("maxAbsoluteSpeed == {}".format(maxAbsoluteSpeed))
            #log.debug("pricePerSpeedDeg == {}".format(pricePerSpeedDeg))

            if planetName == "Mercury":
                for i in [-1, -0.5, 0.5, 1, 2]:
                    speedToDraw = sunSpeed * i
                    price = avgPrice + (pricePerSpeedDeg * speedToDraw)
                    #log.debug("speedToDraw == {}".format(speedToDraw))
                    #log.debug("price == {}".format(price))
                    PlanetaryCombinationsLibrary.\
                        addHorizontalLine(pcdd, startDt, endDt, price,
                            tag="SunSpeed_x_{}_for_{}".\
                                format(speedToDraw, planetName),
                            color=color)
                    numArtifactsAdded += 1

            elif planetName == "Venus":
                for i in [-1, -0.5, 0.5, 1]:
                    speedToDraw = sunSpeed * i
                    price = avgPrice + (pricePerSpeedDeg * speedToDraw)
                    #log.debug("speedToDraw == {}".format(speedToDraw))
                    #log.debug("price == {}".format(price))
                    PlanetaryCombinationsLibrary.\
                        addHorizontalLine(pcdd, startDt, endDt, price,
                            tag="SunSpeed_x_{}_for_{}".\
                                format(speedToDraw, planetName),
                            color=color)
                    numArtifactsAdded += 1
            
            elif planetName == "Mars":
                for i in [-0.5, 0.5, 1]:
                    speedToDraw = sunSpeed * i
                    price = avgPrice + (pricePerSpeedDeg * speedToDraw)
                    #log.debug("speedToDraw == {}".format(speedToDraw))
                    #log.debug("price == {}".format(price))
                    PlanetaryCombinationsLibrary.\
                        addHorizontalLine(pcdd, startDt, endDt, price,
                            tag="SunSpeed_x_{}_for_{}".\
                                format(speedToDraw, planetName),
                            color=color)
                    numArtifactsAdded += 1
            
        # Add a horizontal line for the planet's heliocentric speed,
        # if it is not zero.
        #if helioSpeed != 0.0:
            #pricePerSpeedDeg = (highPrice - avgPrice) / maxAbsoluteSpeed
            #log.debug("avgPrice == {}".format(avgPrice))
            #log.debug("maxAbsoluteSpeed == {}".format(maxAbsoluteSpeed))
            #log.debug("pricePerSpeedDeg == {}".format(pricePerSpeedDeg))
            #
            #price = avgPrice + (pricePerSpeedDeg * helioSpeed)
            #log.debug("helioSpeed == {}".format(helioSpeed))
            #log.debug("price == {}".format(price))
            #
            #PlanetaryCombinationsLibrary.\
            #    addHorizontalLine(pcdd, startDt, endDt, price,
            #        tag="HelioVelocityLine_{}".format(planetName),
            #        color=color)
            #numArtifactsAdded += 1
        
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
            
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    

    @staticmethod
    def addGeoLongitudeVelocityLinesNonScaled(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        stepSizeTd=datetime.timedelta(days=1)):
        """Adds a bunch of line segments that represent a given
        planet's longitude speed.  The start and end points of
        each line segment is 'stepSizeTd' distance away.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for highest velocity.
        lowPrice  - float value for the low price which represents
                    the location for lowest velocity.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 velocity.
        avgPrice = (lowPrice + highPrice) / 2.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            
        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Velocity of the steps saved (list of float).
        velocitys = []
        velocitys.append(None)
        velocitys.append(None)

        # Start and end timestamps used for the location of the
        # LineSegmentGraphicsItem.
        startLineSegmentDt = None
        endLineSegmentDt = None

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        # We will use Mercury's fastest speed as the upper and lower
        # bounds for all the other planets.
        mercuryMaxSpeed = abs(2.20247915641)
        maxAbsoluteSpeed = mercuryMaxSpeed
        
        if planetName == "Mercury":
            helioSpeed = 4.092346062424192
        elif planetName == "Venus":
            helioSpeed = 1.6021312618132146
        elif planetName == "Mars":
            helioSpeed = 0.5240395882
        elif planetName == "Jupiter":
            helioSpeed = 0.08311070438168867
        elif planetName == "Saturn":
            helioSpeed = 0.033459674586075946
        elif planetName == "Uranus":
            helioSpeed = 0.011688655137431798
        elif planetName == "Neptune":
            helioSpeed = 0.005981059976740323
        elif planetName == "Pluto":
            helioSpeed = 0.003972926492417422
        else:
            helioSpeed = 0.0
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} velocity is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['longitude_speed']))
            
            velocitys[-1] = p1.geocentric['tropical']['longitude_speed']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(velocitys)):
                log.debug("velocitys[{}] == {}".format(i, velocitys[i]))


            if velocitys[-2] != None:
                
                pricePerSpeedDeg = (highPrice - avgPrice) / maxAbsoluteSpeed
                
                startPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-2])
                endPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-1])
        
                startPointPrice = \
                    avgPrice + (velocitys[-2] * pricePerSpeedDeg)
                startPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(startPointPrice)
                
                endPointPrice = \
                    avgPrice + (velocitys[-1] * pricePerSpeedDeg)
                endPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(endPointPrice)
                
                item = LineSegmentGraphicsItem()
                item.loadSettingsFromAppPreferences()
                item.loadSettingsFromPriceBarChartSettings(\
                    pcdd.priceBarChartSettings)
                
                artifact = item.getArtifact()
                artifact.addTag(tag)
                artifact.setTiltedTextFlag(False)
                artifact.setAngleTextFlag(False)
                artifact.setColor(color)
                artifact.setStartPointF(QPointF(startPointX, startPointY))
                artifact.setEndPointF(QPointF(endPointX, endPointY))
                
                # Append the artifact.
                log.info("Adding '{}' {} at ".\
                         format(tag, artifact.__class__.__name__) + \
                         "({}, {}) to ({}, {}), or ({} to {}) ...".\
                         format(startPointX, startPointY,
                                endPointX, endPointY,
                                Ephemeris.datetimeToStr(steps[-2]),
                                Ephemeris.datetimeToStr(steps[-1])))
                
                pcdd.priceBarChartArtifacts.append(artifact)
                
                numArtifactsAdded += 1

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            velocitys.append(None)
            del velocitys[0]


        # Add a horizontal line for various fixed velocities.
        if True:
            sunSpeed = 1.014555555555555

            pricePerSpeedDeg = (highPrice - avgPrice) / maxAbsoluteSpeed
            
            for n in [-1.0, -0.5, 0.0, 0.5, 1.0, 2.0]:
                speedToDraw = sunSpeed * n
                price = avgPrice + (pricePerSpeedDeg * speedToDraw)
                log.debug("speedToDraw == {}".format(speedToDraw))
                log.debug("price == {}".format(price))
                PlanetaryCombinationsLibrary.\
                    addHorizontalLine(pcdd, startDt, endDt, price,
                        tag="AvgSunSpeed_times_{}".format(n),
                        color=QColor(Qt.black))
                numArtifactsAdded += 1
        
        # Add a horizontal line for the planet's heliocentric speed,
        # if it is not zero.
        if helioSpeed != 0.0:
            pricePerSpeedDeg = (highPrice - avgPrice) / maxAbsoluteSpeed
            log.debug("avgPrice == {}".format(avgPrice))
            log.debug("maxAbsoluteSpeed == {}".format(maxAbsoluteSpeed))
            log.debug("pricePerSpeedDeg == {}".format(pricePerSpeedDeg))
            
            price = avgPrice + (pricePerSpeedDeg * helioSpeed)
            log.debug("helioSpeed == {}".format(helioSpeed))
            log.debug("price == {}".format(price))
            
            PlanetaryCombinationsLibrary.\
                addHorizontalLine(pcdd, startDt, endDt, price,
                    tag="HelioVelocityLine_{}".format(planetName),
                    color=color)
            numArtifactsAdded += 1
        
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
            
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    

    @staticmethod
    def addGeoLongitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(minutes=4)):
        """Adds vertical line segments whenever the given planet goes
        from direct to retrograde or retrograde to direct.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for highest velocity.
        lowPrice  - float value for the low price which represents
                    the location for lowest velocity.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
        
        # Calculate the average of the low and high price.  This is
        # the price location of 0 velocity.
        avgPrice = (lowPrice + highPrice) / 2.0
        
        # Field name we are getting.
        fieldName = "longitude_speed"
        centricityType = "geocentric"
        longitudeType = "tropical"

        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        darkerColor = None
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            darkerColor = color.darker()
        else:
            darkerColor = color
        
        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        
        # Velocity of the steps saved (list of float).
        velocitys = []
        velocitys.append(None)
        velocitys.append(None)

        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            velocitys[-1] = getFieldValue(p1, fieldName)
            
            log.debug("{} velocity is: {}".\
                      format(p1.name, velocitys[-1]))
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(velocitys)):
                log.debug("velocitys[{}] == {}".format(i, velocitys[i]))
            
            
            if velocitys[-2] != None:

                prevValue = velocitys[-2]
                currValue = velocitys[-1]
                prevDt = steps[-2]
                currDt = steps[-1]
                desiredVelocity = 0
                
                if prevValue < desiredVelocity and currValue >= desiredVelocity:
                    log.debug("Went from Retrograde to Direct!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if testValue < desiredVelocity:
                            t1 = testDt
                        else:
                            t2 = testDt
    
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    velocitys[-1] = currValue
                    
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice,
                                        tag + "_Direct",
                                        darkerColor)
                    numArtifactsAdded += 1
                    
                elif prevValue >= desiredVelocity and currValue < desiredVelocity:
                    log.debug("Went from Direct to Retrograde!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if testValue >= desiredVelocity:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                        
                        currErrorTd = t2 - t1
                    
                    # Update our lists.
                    steps[-1] = currDt
                    velocitys[-1] = currValue
                    
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice,
                                        tag + "_Retrograde",
                                        color)
                    numArtifactsAdded += 1
            
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            velocitys.append(None)
            del velocitys[0]

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
            
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    

    @staticmethod
    def addContraparallelDeclinationAspectVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planet1Name,
        planet2Name,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever two planets
        are contraparallel with each other.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planet1Name - str holding the name of the first planet to do the
                      calculations for.
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
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
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            color = QColor(Qt.darkYellow)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planet1Name + "_" + planet2Name
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Field name.
        fieldName = "declination"
        
        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Declination of the steps saved (list of float).
        declinationsAvg = []
        declinationsAvg.append(None)
        declinationsAvg.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)

            declinationsAvg[-1] = \
                (p1.geocentric['tropical'][fieldName] + \
                 p2.geocentric['tropical'][fieldName]) / 2.0
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(declinationsAvg)):
                log.debug("declinationsAvg[{}] == {}".\
                          format(i, declinationsAvg[i]))

            if declinationsAvg[-2] != None:
                    
                if (declinationsAvg[-2] < 0 and declinationsAvg[-1] > 0) or \
                   (declinationsAvg[-2] > 0 and declinationsAvg[-1] < 0):
    
                    # Average crossed from above to below 0, or below to
                    # above 0.  This means these planets crossed over the
                    # contraparallel aspect location.
    
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            declinationsAvg.append(None)
            del declinationsAvg[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addParallelDeclinationAspectVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planet1Name,
        planet2Name,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever two planets
        are parallel with each other.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planet1Name - str holding the name of the first planet to do the
                      calculations for.
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
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
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            color = QColor(Qt.darkCyan)
        
        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planet1Name + "_" + planet2Name
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Field name.
        fieldName = "declination"
        
        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Declination of the steps saved (list of float).
        declinationsP1 = []
        declinationsP1.append(None)
        declinationsP1.append(None)

        declinationsP2 = []
        declinationsP2.append(None)
        declinationsP2.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)
            
            declinationsP1[-1] = p1.geocentric['tropical'][fieldName]
            declinationsP2[-1] = p2.geocentric['tropical'][fieldName]
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(declinationsP1)):
                log.debug("declinationsP1[{}] == {}".\
                          format(i, declinationsP1[i]))
            for i in range(len(declinationsP2)):
                log.debug("declinationsP2[{}] == {}".\
                          format(i, declinationsP2[i]))
                
            if declinationsP1[-2] != None and declinationsP2[-2] != None:
                
                if (declinationsP1[-1] < 0 and declinationsP2[-1] < 0) or \
                    (declinationsP1[-1] > 0 and declinationsP2[-1] > 0):

                    # Declinations are the same polarity.
    
                    # Get the differences as if they were both positive values.
                    prevAbsDiff = \
                        abs(declinationsP1[-2]) - abs(declinationsP2[-2])
                    currAbsDiff = \
                        abs(declinationsP1[-1]) - abs(declinationsP2[-1])
    
                    if (prevAbsDiff < 0 and currAbsDiff > 0) or \
                       (prevAbsDiff > 0 and currAbsDiff < 0):
    
                        # Crossed over the parallel aspect location.
    
                        # Create the artifact at the timestamp.
                        PlanetaryCombinationsLibrary.\
                            addVerticalLine(pcdd, currDt,
                                            highPrice, lowPrice, tag, color)
                        numArtifactsAdded += 1
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            declinationsP1.append(None)
            del declinationsP1[0]
            declinationsP2.append(None)
            del declinationsP2[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
        
    @staticmethod
    def addPlanetOOBVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        planetName, 
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where a certain planet crosses a certain degree
        of longitude.  This function only is valid for the year 300
        and beyond.
        
        Note: Default tag used for the artifacts added is the name of
        this function, without the word 'add' at the beginning, and with
        the type of line it is appended (geo/helio, trop/sid, planet name).
        
        Arguments:
        pcdd          - PriceChartDocumentData object that will be modified.
        startDt       - datetime.datetime object for the starting timestamp
                        to do the calculations for artifacts.
        endDt         - datetime.datetime object for the ending timestamp
                        to do the calculations for artifacts.
        highPrice     - float value for the high price to end the vertical line.
        lowPrice      - float value for the low price to end the vertical line.
        planetName    - str value holding the name fo the planet to do
                        the search for.
        color         - QColor object for what color to draw the lines.
                        If this is set to None, then the default color
                        will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """


        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        centricityType = "geocentric"
        longitudeType = "tropical"
        
        # Field name we are getting.
        fieldName = "declination"
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)


        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:]

            tag += "_" + planetName
            
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Function for getting the max declination for a given datetime.
        initialDt = datetime.datetime(year=430, month=6, day=1, tzinfo=pytz.utc)
        initialJd = Ephemeris.datetimeToJulianDay(initialDt)
        initialMaxSunDeclination = 23.3333333333333
        incrementPerDay = (1 / 60.0) / (365.25 * 130)
        def getMaxSunDeclinationForDatetime(dt):
            jd = Ephemeris.datetimeToJulianDay(dt)
            return initialMaxSunDeclination + \
                   ((jd - initialJd) * incrementPerDay)
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Iterate through, creating artfacts and adding them as we go.
        prevDt = copy.deepcopy(startDt)
        currDt = copy.deepcopy(startDt)

        prevDiff = None
        currDiff = None

        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
            
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while currDt < endDt:
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            diffDeg = getFieldValue(p1, fieldName)

            log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             diffDeg))

            currMaxSunDeclination = getMaxSunDeclinationForDatetime(currDt)
            currMinSunDeclination = -1 * currMaxSunDeclination
            
            log.debug("diffDeg == {}".format(diffDeg))
            
            currDiff = diffDeg

            if prevDiff == None:
                prevDiff = currDiff

            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))

            desiredDegree = currMaxSunDeclination
            if prevDiff < desiredDegree and currDiff >= desiredDegree:

                log.debug("Crossed over max from below to above!")
                
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
                    
                    p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                    diffDeg = getFieldValue(p1, fieldName)
                    
                    testDiff = diffDeg
                    if testDiff < desiredDegree:
                        t1 = testDt
                    else:
                        t2 = testDt

                        # Update the curr values.
                        currDt = t2
                        currDiff = testDiff
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            elif prevDiff > desiredDegree and currDiff <= desiredDegree:

                log.debug("Crossed over max from above to below!")
                
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
                    
                    p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                    diffDeg = getFieldValue(p1, fieldName)
                    
                    testDiff = diffDeg
                    if testDiff > desiredDegree:
                        t1 = testDt
                        
                    else:
                        t2 = testDt
                        
                        # Update the curr values.
                        currDt = t2
                        currDiff = testDiff
                        
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            desiredDegree = currMinSunDeclination
            if prevDiff < desiredDegree and currDiff >= desiredDegree:

                log.debug("Crossed over min from below to above!")
                
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
                    
                    p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                    diffDeg = getFieldValue(p1, fieldName)
                    
                    testDiff = diffDeg
                    if testDiff < desiredDegree:
                        t1 = testDt
                    else:
                        t2 = testDt

                        # Update the curr values.
                        currDt = t2
                        currDiff = testDiff
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            elif prevDiff > desiredDegree and currDiff <= desiredDegree:

                log.debug("Crossed over max from above to below!")
                
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
                    
                    p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                    diffDeg = getFieldValue(p1, fieldName)
                    
                    testDiff = diffDeg
                    if testDiff > desiredDegree:
                        t1 = testDt
                        
                    else:
                        t2 = testDt
                        
                        # Update the curr values.
                        currDt = t2
                        currDiff = testDiff
                        
                        
                    currErrorTd = t2 - t1
                
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, currDt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1
                
            # Update prevDiff as the currDiff.
            prevDiff = currDiff
                
            # Increment currDt.
            prevDt = copy.deepcopy(currDt)
            currDt += stepSizeTd

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addGeoLatitudeLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        stepSizeTd=datetime.timedelta(days=1)):
        """Adds a bunch of line segments that represent a given
        planet's geocentric latitude degrees.  The start and end points of
        each line segment is 'stepSizeTd' distance away.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for +15 degrees latitude.
        lowPrice  - float value for the low price which represents
                    the location for +15 degrees latitude.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees latitude.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Value for the absolute value of the maximum/minimum latitude.
        absoluteMaxLatitude = 15.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudes = []
        latitudes.append(None)
        latitudes.append(None)

        # Start and end timestamps used for the location of the
        # LineSegmentGraphicsItem.
        startLineSegmentDt = None
        endLineSegmentDt = None

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} latitude is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['latitude']))
            
            latitudes[-1] = p1.geocentric['tropical']['latitude']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudes)):
                log.debug("latitudes[{}] == {}".format(i, latitudes[i]))


            if latitudes[-2] != None:
                pricePerLatitudeDegree = \
                    (highPrice - avgPrice) / absoluteMaxLatitude

                
                startPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-2])
                endPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-1])
        
                startPointPrice = \
                    avgPrice + (latitudes[-2] * pricePerLatitudeDegree)
                startPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(startPointPrice)
                
                endPointPrice = \
                    avgPrice + (latitudes[-1] * pricePerLatitudeDegree)
                endPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(endPointPrice)
                
                item = LineSegmentGraphicsItem()
                item.loadSettingsFromAppPreferences()
                item.loadSettingsFromPriceBarChartSettings(\
                    pcdd.priceBarChartSettings)
                
                artifact = item.getArtifact()
                artifact.addTag(tag)
                artifact.setTiltedTextFlag(False)
                artifact.setAngleTextFlag(False)
                artifact.setColor(color)
                artifact.setStartPointF(QPointF(startPointX, startPointY))
                artifact.setEndPointF(QPointF(endPointX, endPointY))
                
                # Append the artifact.
                log.info("Adding '{}' {} at ".\
                         format(tag, artifact.__class__.__name__) + \
                         "({}, {}) to ({}, {}), or ({} to {}) ...".\
                         format(startPointX, startPointY,
                                endPointX, endPointY,
                                Ephemeris.datetimeToStr(steps[-2]),
                                Ephemeris.datetimeToStr(steps[-1])))
                
                pcdd.priceBarChartArtifacts.append(artifact)
                
                numArtifactsAdded += 1

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudes.append(None)
            del latitudes[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    

    @staticmethod
    def addZeroGeoLatitudeVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's
        geocentric latitude changes from increasing to decreasing or
        decreasing to increasing.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees latitude.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Desired latitude degree.
        desiredDegree = 0.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudes = []
        latitudes.append(None)
        latitudes.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} latitude is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['latitude']))

            latitudes[-1] = p1.geocentric['tropical']['latitude']

            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudes)):
                log.debug("latitudes[{}] == {}".format(i, latitudes[i]))

            if latitudes[-2] != None:
                
                if latitudes[-2] < desiredDegree and \
                       latitudes[-1] >= desiredDegree:
    
                    log.debug("Crossed over from below to above!")
                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1
    
                    # Refine the timestamp until it is less than the threshold.
                    currDiff = None
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
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
    
                        diffDeg = p1.geocentric['tropical']['latitude']
                        
                        testDiff = diffDeg
                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt
    
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                            
                        currErrorTd = t2 - t1
    
                    if currDiff != None:
                        steps[-1] = currDt
                        latitudes[-1] = currDiff
    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.green)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
                elif latitudes[-2] > desiredDegree and \
                       latitudes[-1] <= desiredDegree:

                    log.debug("Crossed over from above to below!")
                    
                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1
    
                    # Refine the timestamp until it is less than the threshold.
                    currDiff = None
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
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
    
                        diffDeg = p1.geocentric['tropical']['latitude']
                        
                        testDiff = diffDeg
                        if testDiff > desiredDegree:
                            t1 = testDt
                            
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                            
                        currErrorTd = t2 - t1
    
                    if currDiff != None:
                        steps[-1] = currDt
                        latitudes[-1] = currDiff
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.darkGreen)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudes.append(None)
            del latitudes[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addGeoLatitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's geocentric
        latitude changes from increasing to decreasing or
        decreasing to increasing.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees latitude.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudeVelocitys = []
        latitudeVelocitys.append(None)
        latitudeVelocitys.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} latitude speed is: {}".\
                      format(p1.name,
                             p1.geocentric['tropical']['latitude_speed']))
            
            latitudeVelocitys[-1] = \
                p1.geocentric['tropical']['latitude_speed']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudeVelocitys)):
                log.debug("latitudeVelocitys[{}] == {}".\
                          format(i, latitudeVelocitys[i]))

            if latitudeVelocitys[-2] != None:

                if latitudeVelocitys[-2] > 0 > latitudeVelocitys[-1]:
    
                    # Was increasing, but now decreasing.
                    log.debug("Started decreasing after previously increasing.")
    
                    lineDt = steps[-1]
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.red)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
    
                elif latitudeVelocitys[-2] < 0 < latitudeVelocitys[-1]:
    
                    # Was decreasing, but now increasing.
                    log.debug("Started increasing after previously decreasing.")
    
                    lineDt = steps[-1]
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.darkRed)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudeVelocitys.append(None)
            del latitudeVelocitys[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addContraparallelGeoLatitudeAspectVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planet1Name,
        planet2Name,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever two planets
        are contraparallel with each other in geocentric latitude.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planet1Name - str holding the name of the first planet to do the
                      calculations for.
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
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
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            color = QColor(Qt.darkYellow)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planet1Name + "_" + planet2Name
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Field name.
        fieldName = "latitude"
        
        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudesAvg = []
        latitudesAvg.append(None)
        latitudesAvg.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)

            latitudesAvg[-1] = \
                (p1.geocentric['tropical'][fieldName] + \
                 p2.geocentric['tropical'][fieldName]) / 2.0
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudesAvg)):
                log.debug("latitudesAvg[{}] == {}".\
                          format(i, latitudesAvg[i]))

            if latitudesAvg[-2] != None:
                    
                if (latitudesAvg[-2] < 0 and latitudesAvg[-1] > 0) or \
                   (latitudesAvg[-2] > 0 and latitudesAvg[-1] < 0):
    
                    # Average crossed from above to below 0, or below to
                    # above 0.  This means these planets crossed over the
                    # contraparallel aspect location.
    
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudesAvg.append(None)
            del latitudesAvg[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addParallelGeoLatitudeAspectVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planet1Name,
        planet2Name,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever two planets
        are parallel with each other in geocentric latitude.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planet1Name - str holding the name of the first planet to do the
                      calculations for.
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
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
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            color = QColor(Qt.darkCyan)
        
        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planet1Name + "_" + planet2Name
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Field name.
        fieldName = "latitude"
        
        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudesP1 = []
        latitudesP1.append(None)
        latitudesP1.append(None)

        latitudesP2 = []
        latitudesP2.append(None)
        latitudesP2.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)
            
            latitudesP1[-1] = p1.geocentric['tropical'][fieldName]
            latitudesP2[-1] = p2.geocentric['tropical'][fieldName]
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudesP1)):
                log.debug("latitudesP1[{}] == {}".\
                          format(i, latitudesP1[i]))
            for i in range(len(latitudesP2)):
                log.debug("latitudesP2[{}] == {}".\
                          format(i, latitudesP2[i]))
                
            if latitudesP1[-2] != None and latitudesP2[-2] != None:
                
                if (latitudesP1[-1] < 0 and latitudesP2[-1] < 0) or \
                    (latitudesP1[-1] > 0 and latitudesP2[-1] > 0):

                    # Latitudes are the same polarity.
    
                    # Get the differences as if they were both positive values.
                    prevAbsDiff = \
                        abs(latitudesP1[-2]) - abs(latitudesP2[-2])
                    currAbsDiff = \
                        abs(latitudesP1[-1]) - abs(latitudesP2[-1])
    
                    if (prevAbsDiff < 0 and currAbsDiff > 0) or \
                       (prevAbsDiff > 0 and currAbsDiff < 0):
    
                        # Crossed over the parallel aspect location.
    
                        # Create the artifact at the timestamp.
                        PlanetaryCombinationsLibrary.\
                            addVerticalLine(pcdd, currDt,
                                            highPrice, lowPrice, tag, color)
                        numArtifactsAdded += 1
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudesP1.append(None)
            del latitudesP1[0]
            latitudesP2.append(None)
            del latitudesP2[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addHelioLatitudeLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        stepSizeTd=datetime.timedelta(days=1)):
        """Adds a bunch of line segments that represent a given
        planet's heliocentric latitude degrees.  The start and end points of
        each line segment is 'stepSizeTd' distance away.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for +15 degrees latitude.
        lowPrice  - float value for the low price which represents
                    the location for +15 degrees latitude.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees latitude.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Value for the absolute value of the maximum/minimum latitude.
        absoluteMaxLatitude = 15.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudes = []
        latitudes.append(None)
        latitudes.append(None)

        # Start and end timestamps used for the location of the
        # LineSegmentGraphicsItem.
        startLineSegmentDt = None
        endLineSegmentDt = None

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} latitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['tropical']['latitude']))
            
            latitudes[-1] = p1.heliocentric['tropical']['latitude']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudes)):
                log.debug("latitudes[{}] == {}".format(i, latitudes[i]))


            if latitudes[-2] != None:
                pricePerLatitudeDegree = \
                    (highPrice - avgPrice) / absoluteMaxLatitude

                
                startPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-2])
                endPointX = \
                    PlanetaryCombinationsLibrary.scene.\
                    datetimeToSceneXPos(steps[-1])
        
                startPointPrice = \
                    avgPrice + (latitudes[-2] * pricePerLatitudeDegree)
                startPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(startPointPrice)
                
                endPointPrice = \
                    avgPrice + (latitudes[-1] * pricePerLatitudeDegree)
                endPointY = \
                    PlanetaryCombinationsLibrary.scene.\
                    priceToSceneYPos(endPointPrice)
                
                item = LineSegmentGraphicsItem()
                item.loadSettingsFromAppPreferences()
                item.loadSettingsFromPriceBarChartSettings(\
                    pcdd.priceBarChartSettings)
                
                artifact = item.getArtifact()
                artifact.addTag(tag)
                artifact.setTiltedTextFlag(False)
                artifact.setAngleTextFlag(False)
                artifact.setColor(color)
                artifact.setStartPointF(QPointF(startPointX, startPointY))
                artifact.setEndPointF(QPointF(endPointX, endPointY))
                
                # Append the artifact.
                log.info("Adding '{}' {} at ".\
                         format(tag, artifact.__class__.__name__) + \
                         "({}, {}) to ({}, {}), or ({} to {}) ...".\
                         format(startPointX, startPointY,
                                endPointX, endPointY,
                                Ephemeris.datetimeToStr(steps[-2]),
                                Ephemeris.datetimeToStr(steps[-1])))
                
                pcdd.priceBarChartArtifacts.append(artifact)
                
                numArtifactsAdded += 1

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudes.append(None)
            del latitudes[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    

    @staticmethod
    def addZeroHelioLatitudeVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's
        heliocentric latitude changes from increasing to decreasing or
        decreasing to increasing.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        stepSizeTd - datetime.timedelta object holding the time
                     distance between each data sample.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees latitude.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Desired latitude degree.
        desiredDegree = 0.0
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudes = []
        latitudes.append(None)
        latitudes.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} latitude is: {}".\
                      format(p1.name,
                             p1.heliocentric['tropical']['latitude']))

            latitudes[-1] = p1.heliocentric['tropical']['latitude']

            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudes)):
                log.debug("latitudes[{}] == {}".format(i, latitudes[i]))

            if latitudes[-2] != None:
                
                if latitudes[-2] < desiredDegree and \
                       latitudes[-1] >= desiredDegree:
    
                    log.debug("Crossed over from below to above!")
                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1
    
                    # Refine the timestamp until it is less than the threshold.
                    currDiff = None
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
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
    
                        diffDeg = p1.heliocentric['tropical']['latitude']
                        
                        testDiff = diffDeg
                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt
    
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                            
                        currErrorTd = t2 - t1
    
                    if currDiff != None:
                        steps[-1] = currDt
                        latitudes[-1] = currDiff
    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.green)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
                elif latitudes[-2] > desiredDegree and \
                       latitudes[-1] <= desiredDegree:

                    log.debug("Crossed over from above to below!")
                    
                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1
    
                    # Refine the timestamp until it is less than the threshold.
                    currDiff = None
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
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
    
                        diffDeg = p1.heliocentric['tropical']['latitude']
                        
                        testDiff = diffDeg
                        if testDiff > desiredDegree:
                            t1 = testDt
                            
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                            
                        currErrorTd = t2 - t1
    
                    if currDiff != None:
                        steps[-1] = currDt
                        latitudes[-1] = currDiff
                    
                    if colorWasSpecifiedFlag == False:
                        color = QColor(Qt.darkGreen)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudes.append(None)
            del latitudes[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addHelioLatitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's heliocentric
        latitude changes from increasing to decreasing or
        decreasing to increasing.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Calculate the average of the low and high price.  This is
        # the price location of 0 degrees latitude.
        avgPrice = (lowPrice + highPrice) / 2.0

        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudeVelocitys = []
        latitudeVelocitys.append(None)
        latitudeVelocitys.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            log.debug("{} latitude speed is: {}".\
                      format(p1.name,
                             p1.heliocentric['tropical']['latitude_speed']))
            
            latitudeVelocitys[-1] = \
                p1.heliocentric['tropical']['latitude_speed']
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudeVelocitys)):
                log.debug("latitudeVelocitys[{}] == {}".\
                          format(i, latitudeVelocitys[i]))

            if latitudeVelocitys[-2] != None:

                if latitudeVelocitys[-2] > 0 > latitudeVelocitys[-1]:
    
                    # Was increasing, but now decreasing.
                    log.debug("Started decreasing after previously increasing.")
    
                    lineDt = steps[-1]
                    
                    #if colorWasSpecifiedFlag == False:
                    #    color = QColor(Qt.red)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
    
                elif latitudeVelocitys[-2] < 0 < latitudeVelocitys[-1]:
    
                    # Was decreasing, but now increasing.
                    log.debug("Started increasing after previously decreasing.")
    
                    lineDt = steps[-1]
                    
                    #if colorWasSpecifiedFlag == False:
                    #    color = QColor(Qt.darkRed)
                        
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, lineDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudeVelocitys.append(None)
            del latitudeVelocitys[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def addContraparallelHelioLatitudeAspectVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planet1Name,
        planet2Name,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever two planets
        are contraparallel with each other in heliocentric latitude.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planet1Name - str holding the name of the first planet to do the
                      calculations for.
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
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
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            color = QColor(Qt.darkYellow)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planet1Name + "_" + planet2Name
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Field name.
        fieldName = "latitude"
        
        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudesAvg = []
        latitudesAvg.append(None)
        latitudesAvg.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)

            latitudesAvg[-1] = \
                (p1.heliocentric['tropical'][fieldName] + \
                 p2.heliocentric['tropical'][fieldName]) / 2.0
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudesAvg)):
                log.debug("latitudesAvg[{}] == {}".\
                          format(i, latitudesAvg[i]))

            if latitudesAvg[-2] != None:
                    
                if (latitudesAvg[-2] < 0 and latitudesAvg[-1] > 0) or \
                   (latitudesAvg[-2] > 0 and latitudesAvg[-1] < 0):
    
                    # Average crossed from above to below 0, or below to
                    # above 0.  This means these planets crossed over the
                    # contraparallel aspect location.
    
                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudesAvg.append(None)
            del latitudesAvg[0]
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addParallelHelioLatitudeAspectVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planet1Name,
        planet2Name,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever two planets
        are parallel with each other in heliocentric latitude.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the location for the top of the vertical line.
        lowPrice  - float value for the low price which represents
                    the location for the bottom of the vertical line.
        planet1Name - str holding the name of the first planet to do the
                      calculations for.
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
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
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            #color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            color = QColor(Qt.darkCyan)
        
        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planet1Name + "_" + planet2Name
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        # Use maxErrorTd as the step size because I'm lazy and this
        # won't require us to narrow down the transition point when we
        # find it.
        stepSizeTd = maxErrorTd

        # Field name.
        fieldName = "latitude"
        
        # Count of artifacts added.
        numArtifactsAdded = 0

        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Latitude of the steps saved (list of float).
        latitudesP1 = []
        latitudesP1.append(None)
        latitudesP1.append(None)

        latitudesP2 = []
        latitudesP2.append(None)
        latitudesP2.append(None)

        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)
            
            latitudesP1[-1] = p1.heliocentric['tropical'][fieldName]
            latitudesP2[-1] = p2.heliocentric['tropical'][fieldName]
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(latitudesP1)):
                log.debug("latitudesP1[{}] == {}".\
                          format(i, latitudesP1[i]))
            for i in range(len(latitudesP2)):
                log.debug("latitudesP2[{}] == {}".\
                          format(i, latitudesP2[i]))
                
            if latitudesP1[-2] != None and latitudesP2[-2] != None:
                
                if (latitudesP1[-1] < 0 and latitudesP2[-1] < 0) or \
                    (latitudesP1[-1] > 0 and latitudesP2[-1] > 0):

                    # Latitudes are the same polarity.
    
                    # Get the differences as if they were both positive values.
                    prevAbsDiff = \
                        abs(latitudesP1[-2]) - abs(latitudesP2[-2])
                    currAbsDiff = \
                        abs(latitudesP1[-1]) - abs(latitudesP2[-1])
    
                    if (prevAbsDiff < 0 and currAbsDiff > 0) or \
                       (prevAbsDiff > 0 and currAbsDiff < 0):
    
                        # Crossed over the parallel aspect location.
    
                        # Create the artifact at the timestamp.
                        PlanetaryCombinationsLibrary.\
                            addVerticalLine(pcdd, currDt,
                                            highPrice, lowPrice, tag, color)
                        numArtifactsAdded += 1
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            latitudesP1.append(None)
            del latitudesP1[0]
            latitudesP2.append(None)
            del latitudesP2[0]
            
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
                
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def getTagNameForLongitudeAspect(\
        planet1ParamsList, planet2ParamsList,
        degreeDifference,
        uniDirectionalAspectsFlag=False):
        """Returns a tag name for a longitude aspect between the
        described two planets.  This function is intended to be
        supplementary to getLongitudeAspectTimestamps().

        Parameters:
        See the parameter documentation of the function
        getLongitudeAspectTimestamps(), and look at the documentation for
        the fields with the same names.

        Returns:
        str for the tag name.  If the given function arguments are
        invalid, then None will be returned.
        """
        
        # Check to make sure planet lists were given.
        if len(planet1ParamsList) == 0:
            log.error("planet1ParamsList must contain at least 1 tuple.")
            return None
        if len(planet2ParamsList) == 0:
            log.error("planet2ParamsList must contain at least 1 tuple.")
            return None
        
        # Check for valid inputs in each of the planet parameter lists.
        for planetTuple in planet1ParamsList + planet2ParamsList:
            if len(planetTuple) != 3:
                log.error("Input error: " + \
                          "Not enough values given in planet tuple.")
                return None

            planetName = planetTuple[0]
            centricityType = planetTuple[1]
            longitudeType = planetTuple[2]
            
            loweredCentricityType = centricityType.lower()
            if loweredCentricityType != "geocentric" and \
                loweredCentricityType != "topocentric" and \
                loweredCentricityType != "heliocentric":

                log.error("Invalid input: Centricity type is invalid.  " + \
                      "Value given was: {}".format(centricityType))
                return None

            # Check inputs for longitude type.
            loweredLongitudeType = longitudeType.lower()
            if loweredLongitudeType != "tropical" and \
                loweredLongitudeType != "sidereal":

                log.error("Invalid input: Longitude type is invalid.  " + \
                      "Value given was: {}".format(longitudeType))
                return None
            
        # Set the tag str.
        tag = "Longitude"
        if uniDirectionalAspectsFlag == True:
            tag += "UniDirectionalAspect_"
        else:
            tag += "BiDirectionalAspect_"
        
        if len(planet1ParamsList) > 1:
            tag += "Avg("
        for i in range(len(planet1ParamsList)):
            t = planet1ParamsList[i]
            
            planetName = t[0]
            centricityType = t[1]
            longitudeType = t[2]
        
            # If it's not the first planet in the list, add an
            # underscore to separate the planets.
            if i != 0:
                tag += "_"
            
            if centricityType.startswith("geo"):
                tag += "Geo_"
            elif centricityType.startswith("topo"):
                tag += "Topo_"
            elif centricityType.startswith("helio"):
                tag += "Helio_"
            
            if longitudeType.startswith("trop"):
                tag += "Trop_"
            elif longitudeType.startswith("sid"):
                tag += "Sid_"
            
            tag += planetName
            
        if len(planet1ParamsList) > 1:
            tag += ")"
            
        tag += "_{}_DegreeAspect_".format(degreeDifference)

        if len(planet2ParamsList) > 1:
            tag += "Avg("
        for i in range(len(planet2ParamsList)):
            t = planet2ParamsList[i]
            
            planetName = t[0]
            centricityType = t[1]
            longitudeType = t[2]
            
            # If it's not the first planet in the list, add an
            # underscore to separate the planets.
            if i != 0:
                tag += "_"
            
            if centricityType.startswith("geo"):
                tag += "Geo_"
            elif centricityType.startswith("topo"):
                tag += "Topo_"
            elif centricityType.startswith("helio"):
                tag += "Helio_"
            
            if longitudeType.startswith("trop"):
                tag += "Trop_"
            elif longitudeType.startswith("sid"):
                tag += "Sid_"
                
            tag += planetName
        if len(planet2ParamsList) > 1:
            tag += ")"
            
        log.debug("tag == '{}'".format(tag))

        return tag

    @staticmethod
    def getLongitudeAspectTimestamps(\
        pcdd, startDt, endDt,
        planet1ParamsList,
        planet2ParamsList,
        degreeDifference,
        uniDirectionalAspectsFlag=False,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Obtains a list of datetime.datetime objects that contain
        the moments when the aspect specified is active.
        
        Warning on usage:
        When planet-longitude-averaging is utilized for the longitude
        of planet1 or planet2, the aspects returned by this function
        cannot be fully relied upon.
        
        This short-coming happens under these circumstances because it
        is possible that the longitude can abruptly 'jump' or hop a
        large distance when measurements are taken between timestamp
        steps.

        For example, this 'jumping' effect can occur if two planets A
        and B, are both around 355 degrees, and planet A crosses the 0
        degree mark.  Now the average goes from around 355 degrees
        (355 + 355 = 710 / 2 = 355), to about 180 degrees (355 + 0 =
        355 / 2 = about 180).

        While corrections for this can be made for the case of having
        only 2 planets involved, if more planets are involved then the
        adjustment required quickly becomes non-trivial.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.
        
        planet1ParamsList - List of tuples that will be used as parameters
                      for planet1.  Each tuple contained in this list
                      represents parameters for each planet that will
                      get averaged to create what is known as planet1.

                      The contents of the tuple are:
                      (planetName, centricityType, longitudeType)

                      Where:
                      planetName - str holding the name of the second
                                   planet to do the calculations for.
                      centricityType - str value holding either "geocentric",
                                       "topocentric", or "heliocentric".
                      longitudeType - str value holding either
                                      "tropical" or "sidereal".
                      
                      Example: So if someone wanted planet1 to be the
                      average location of of geocentric sidereal
                      Saturn and geocentric sidereal Uranus, the
                      'planet1ParamsList' parameter would be:

                      [("Saturn", "geocentric", "sidereal"),
                       ("Uranus", "geocentric", "sidereal")]

                      If the typical use-case is desired for the
                      longitude of just a single planet, pass a list
                      with only 1 tuple.  As an example, for Mercury
                      it would be:

                      [("Mercury", "heliocentric", "tropical")]
        
        planet2ParamsList - List of tuples that will be used as parameters
                      for planet2.  For additional details about the
                      format of this parameter field, please see the
                      description for parameter 'planet1ParamsList'
                      
        degreeDifference - float value for the number of degrees of
                           separation for this aspect.
                           
        uniDirectionalAspectsFlag - bool value for whether or not
                     uni-directional aspects are enabled or not.  By
                     default, aspects are bi-directional, so Saturn
                     square-aspect Jupiter would be the same as
                     Jupiter square-aspect Saturn.  If this flag is
                     set to True, then those two combinations would be
                     considered unique.  In the case where the flag is
                     set to True, for the aspect to be active,
                     planet2 would need to be 'degreeDifference'
                     degrees in front of planet1.
        
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        
        List of datetime.datetime objects.  Each timestamp in the list
        is the moment where the aspect is active and satisfies the
        given parameters.  In the event of an error, the reference
        None is returned.
        """

        log.debug("Entered " + inspect.stack()[0][3] + "()")

        # List of timestamps of the aspects found.
        aspectTimestamps = []
        
        # Make sure the inputs are valid.
        if endDt < startDt:
            log.error("Invalid input: 'endDt' must be after 'startDt'")
            return None

        # Check to make sure planet lists were given.
        if len(planet1ParamsList) == 0:
            log.error("planet1ParamsList must contain at least 1 tuple.")
            return None
        if len(planet2ParamsList) == 0:
            log.error("planet2ParamsList must contain at least 1 tuple.")
            return None

        log.debug("planet1ParamsList passed in is: {}".\
                  format(planet1ParamsList))
        log.debug("planet2ParamsList passed in is: {}".\
                  format(planet2ParamsList))
        
        # Check for valid inputs in each of the planet parameter lists.
        for planetTuple in planet1ParamsList + planet2ParamsList:
            if len(planetTuple) != 3:
                log.error("Input error: " + \
                          "Not enough values given in planet tuple.")
                return None

            planetName = planetTuple[0]
            centricityType = planetTuple[1]
            longitudeType = planetTuple[2]
            
            loweredCentricityType = centricityType.lower()
            if loweredCentricityType != "geocentric" and \
                loweredCentricityType != "topocentric" and \
                loweredCentricityType != "heliocentric":

                log.error("Invalid input: Centricity type is invalid.  " + \
                      "Value given was: {}".format(centricityType))
                return None

            # Check inputs for longitude type.
            loweredLongitudeType = longitudeType.lower()
            if loweredLongitudeType != "tropical" and \
                loweredLongitudeType != "sidereal":

                log.error("Invalid input: Longitude type is invalid.  " + \
                      "Value given was: {}".format(longitudeType))
                return None
            
        # Field name we are getting.
        fieldName = "longitude"
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        for planetTuple in planet1ParamsList + planet2ParamsList:
            planetName = planetTuple[0]
            
            if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):
                
                # House cusps and ascmc planets need a smaller step size.
                stepSizeTd = datetime.timedelta(hours=1)
            elif planetName == "Moon":
                # Use a smaller step size for the moon so we can catch
                # smaller aspect sizes.
                stepSizeTd = datetime.timedelta(hours=3)
        
        log.debug("Step size is: {}".format(stepSizeTd))
        
        # Desired angles.  We need to check for planets at these angles.
        desiredAngleDegList = []

        desiredAngleDeg1 = Util.toNormalizedAngle(degreeDifference)
        desiredAngleDegList.append(desiredAngleDeg1)
        if Util.fuzzyIsEqual(desiredAngleDeg1, 0):
            desiredAngleDegList.append(360)
        
        if uniDirectionalAspectsFlag == False:
            desiredAngleDeg2 = \
                360 - Util.toNormalizedAngle(degreeDifference)
            if desiredAngleDeg2 not in desiredAngleDegList:
                desiredAngleDegList.append(desiredAngleDeg2)

        # Debug output.
        anglesStr = ""
        for angle in desiredAngleDegList:
            anglesStr += "{} ".format(angle)
        log.debug("Angles in desiredAngleDegList: " + anglesStr)

        # Iterate through, appending to aspectTimestamps list as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudesP1 = []
        longitudesP1.append(None)
        longitudesP1.append(None)
        
        longitudesP2 = []
        longitudesP2.append(None)
        longitudesP2.append(None)

        def getFieldValue(dt, planetParamsList, fieldName):
            """Creates the PlanetaryInfo object for the given
            planetParamsList and returns the value of the field
            desired.
            """
        
            log.debug("planetParamsList passed in is: {}".\
                      format(planetParamsList))
        
            unAveragedFieldValues = []
            
            for t in planetParamsList:
                planetName = t[0]
                centricityType = t[1]
                longitudeType = t[2]
                
                pi = Ephemeris.getPlanetaryInfo(planetName, dt)

                log.debug("Planet {} has geo sid longitude: {}".\
                          format(planetName,
                                 pi.geocentric["sidereal"]["longitude"]))
            
                fieldValue = None
                
                if centricityType.lower() == "geocentric":
                    fieldValue = pi.geocentric[longitudeType][fieldName]
                elif centricityType.lower() == "topocentric":
                    fieldValue = pi.topocentric[longitudeType][fieldName]
                elif centricityType.lower() == "heliocentric":
                    fieldValue = pi.heliocentric[longitudeType][fieldName]
                else:
                    log.error("Unknown centricity type: {}".\
                              format(centricityType))
                    fieldValue = None

                unAveragedFieldValues.append(fieldValue)

            log.debug("unAveragedFieldValues is: {}".\
                      format(unAveragedFieldValues))
        
            # Average the field values.
            total = 0.0
            for v in unAveragedFieldValues:
                total += v
            averagedFieldValue = total / len(unAveragedFieldValues)
            
            log.debug("averagedFieldValue is: {}".\
                      format(averagedFieldValue))
        
            return averagedFieldValue
            
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        currDiff = None
        prevDiff = None
        

        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            longitudesP1[-1] = \
                Util.toNormalizedAngle(\
                getFieldValue(currDt, planet1ParamsList, fieldName))
            longitudesP2[-1] = \
                Util.toNormalizedAngle(\
                getFieldValue(currDt, planet2ParamsList, fieldName))

            log.debug("{} {} is: {}".\
                      format(planet1ParamsList, fieldName,
                             longitudesP1[-1]))
            log.debug("{} {} is: {}".\
                      format(planet2ParamsList, fieldName,
                             longitudesP2[-1]))
            
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - longitudesP2[-1])
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff != None and \
                   longitudesP1[-2] != None and \
                   longitudesP2[-2] != None:
                
                if abs(prevDiff - currDiff) > 180:
                    # Probably crossed over 0.  Adjust the prevDiff so
                    # that the rest of the algorithm can continue to
                    # work.
                    if prevDiff > currDiff:
                        prevDiff -= 360
                    else:
                        prevDiff += 360
                        
                    log.debug("After adjustment: prevDiff == {}".\
                              format(prevDiff))
                    log.debug("After adjustment: currDiff == {}".\
                              format(currDiff))

                for desiredAngleDeg in desiredAngleDegList:
                    log.debug("Looking at desiredAngleDeg: {}".\
                              format(desiredAngleDeg))
                    
                    desiredDegree = desiredAngleDeg
                    
                    if prevDiff < desiredDegree and currDiff >= desiredDegree:
                        log.debug("Crossed over {} from below to above!".\
                                  format(desiredDegree))
    
                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1
    
                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            log.debug("Refining between {} and {}".\
                                      format(Ephemeris.datetimeToStr(t1),
                                             Ephemeris.datetimeToStr(t2)))
    
                            # Check the timestamp between.
                            timeWindowTd = t2 - t1
                            halfTimeWindowTd = \
                                datetime.\
                                timedelta(days=(timeWindowTd.days / 2.0),
                                    seconds=(timeWindowTd.seconds / 2.0),
                                    microseconds=\
                                          (timeWindowTd.microseconds / 2.0))
                            testDt = t1 + halfTimeWindowTd
    
                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1ParamsList, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet2ParamsList, fieldName))
    
                            log.debug("testValueP1 == {}".format(testValueP1))
                            log.debug("testValueP2 == {}".format(testValueP2))
                            
                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360
                                
                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360
                            
                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)
    
                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360
                            
                            log.debug("testDiff == {}".format(testDiff))
                            
                            if testDiff < desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt
    
                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff
    
                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2
                
                            currErrorTd = t2 - t1
                                
                        # Update our lists.
                        steps[-1] = currDt
    
                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)
                     
                    elif prevDiff > desiredDegree and currDiff <= desiredDegree:
                        log.debug("Crossed over {} from above to below!".\
                                  format(desiredDegree))
    
                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1
    
                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            log.debug("Refining between {} and {}".\
                                      format(Ephemeris.datetimeToStr(t1),
                                             Ephemeris.datetimeToStr(t2)))
    
                            # Check the timestamp between.
                            timeWindowTd = t2 - t1
                            halfTimeWindowTd = \
                                datetime.\
                                timedelta(days=(timeWindowTd.days / 2.0),
                                    seconds=(timeWindowTd.seconds / 2.0),
                                    microseconds=\
                                          (timeWindowTd.microseconds / 2.0))
                            testDt = t1 + halfTimeWindowTd
    
                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1ParamsList, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet2ParamsList, fieldName))
    
                            log.debug("testValueP1 == {}".format(testValueP1))
                            log.debug("testValueP2 == {}".format(testValueP2))
                            
                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360
                                
                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360
    
                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)
    
                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360
                            
                            log.debug("testDiff == {}".format(testDiff))
                            
                            if testDiff > desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt
    
                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff
    
                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2
                                
                            currErrorTd = t2 - t1
    
                        # Update our lists.
                        steps[-1] = currDt
    
                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)
                     
            # Prepare for the next iteration.
            log.debug("steps[-1] is: {}".\
                      format(Ephemeris.datetimeToStr(steps[-1])))
            log.debug("stepSizeTd is: {}".format(stepSizeTd))
            
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]
            longitudesP2.append(None)
            del longitudesP2[0]

            # Update prevDiff as the currDiff.
            prevDiff = Util.toNormalizedAngle(currDiff)

        log.info("Number of timestamps obtained: {}".\
                 format(len(aspectTimestamps)))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return aspectTimestamps

        
    @staticmethod
    def getOnePlanetLongitudeAspectTimestamps(\
        pcdd, startDt, endDt,
        planet1Params,
        fixedDegree,
        degreeDifference,
        uniDirectionalAspectsFlag=False,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Obtains a list of datetime.datetime objects that contain
        the moments when the aspect specified is active.
        The aspect is measured by formula:
           (planet longitude) - (fixed longitude degree)
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.
        
        planet1Params - Tuple containing:
                      (planetName, centricityType, longitudeType)

                      Where:
                      planetName - str holding the name of the second
                                   planet to do the calculations for.
                      centricityType - str value holding either "geocentric",
                                       "topocentric", or "heliocentric".
                      longitudeType - str value holding either
                                      "tropical" or "sidereal".
                      
        fixedDegree - float holding the fixed degree in the zodiac circle.
                      
        degreeDifference - float value for the number of degrees of
                           separation for this aspect.
                           
        uniDirectionalAspectsFlag - bool value for whether or not
                     uni-directional aspects are enabled or not.  By
                     default, aspects are bi-directional, so Saturn
                     square-aspect Jupiter would be the same as
                     Jupiter square-aspect Saturn.  If this flag is
                     set to True, then those two combinations would be
                     considered unique.  In the case where the flag is
                     set to True, for the aspect to be active,
                     planet2 would need to be 'degreeDifference'
                     degrees in front of planet1.
        
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        
        List of datetime.datetime objects.  Each timestamp in the list
        is the moment where the aspect is active and satisfies the
        given parameters.  In the event of an error, the reference
        None is returned.

        rluu_20130926: This function needs to be tested.  It was copy-and-pasted from another script I wrote this function for, and that original script when I wrote it had some syntax errors, which I believe I applied the fixes to this code copied here.  So... this function 'should' work.  It shouldn't be hard to test and confirm, but I haven't done it.
        """

        log.debug("Entered " + inspect.stack()[0][3] + "()")

        # List of timestamps of the aspects found.
        aspectTimestamps = []
        
        # Make sure the inputs are valid.
        if endDt < startDt:
            log.error("Invalid input: 'endDt' must be after 'startDt'")
            return None

        # Check to make sure planet params were given.
        if len(planet1Params) != 3:
            log.error("planet1Params must be a tuple with 3 elements.")
            return None
        if not isinstance(fixedDegree, (int, float, complex)):
            log.error("fixedDegree must be a number.")
            return None

        # Normalize the fixed degree.
        fixedDegree = Util.toNormalizedAngle(fixedDegree)
        
        log.debug("planet1Params passed in is: {}".\
                  format(planet1Params))
        log.debug("fixedDegree passed in is: {}".\
                  format(fixedDegree))

        # Check inputs of planet parameters.
        planetName = planet1Params[0]
        centricityType = planet1Params[1]
        longitudeType = planet1Params[2]

        # Check inputs for centricity type.
        loweredCentricityType = centricityType.lower()
        if loweredCentricityType != "geocentric" and \
            loweredCentricityType != "topocentric" and \
            loweredCentricityType != "heliocentric":

            log.error("Invalid input: Centricity type is invalid.  " + \
                      "Value given was: {}".format(centricityType))
            return None
        
        # Check inputs for longitude type.
        loweredLongitudeType = longitudeType.lower()
        if loweredLongitudeType != "tropical" and \
            loweredLongitudeType != "sidereal":

            log.error("Invalid input: Longitude type is invalid.  " + \
                      "Value given was: {}".format(longitudeType))
            return None

        # Field name we are getting.
        fieldName = "longitude"
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        planetName = planet1Params[0]
        
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
            Ephemeris.isAscmcPlanetName(planetName):
                
            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
        elif planetName == "Moon":
            # Use a smaller step size for the moon so we can catch
            # smaller aspect sizes.
            stepSizeTd = datetime.timedelta(hours=3)
        
        log.debug("Step size is: {}".format(stepSizeTd))
        
        # Desired angles.  We need to check for planets at these angles.
        desiredAngleDegList = []
        
        desiredAngleDeg1 = Util.toNormalizedAngle(degreeDifference)
        desiredAngleDegList.append(desiredAngleDeg1)
        if Util.fuzzyIsEqual(desiredAngleDeg1, 0):
            desiredAngleDegList.append(360)
        
        if uniDirectionalAspectsFlag == False:
            desiredAngleDeg2 = \
                360 - Util.toNormalizedAngle(degreeDifference)
            if desiredAngleDeg2 not in desiredAngleDegList:
                desiredAngleDegList.append(desiredAngleDeg2)
        
        # Debug output.
        anglesStr = ""
        for angle in desiredAngleDegList:
            anglesStr += "{} ".format(angle)
        log.debug("Angles in desiredAngleDegList: " + anglesStr)

        # Iterate through, appending to aspectTimestamps list as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudesP1 = []
        longitudesP1.append(None)
        longitudesP1.append(None)
        
        longitudesP2 = []
        longitudesP2.append(None)
        longitudesP2.append(None)
        
        def getFieldValue(dt, planetParams, fieldName):
            """Creates the PlanetaryInfo object for the given
            planetParamsList and returns the value of the field
            desired.
            """
        
            log.debug("planetParams passed in is: {}".\
                      format(planetParams))
            t = planetParams
        
            planetName = t[0]
            centricityType = t[1]
            longitudeType = t[2]
                
            pi = Ephemeris.getPlanetaryInfo(planetName, dt)

            log.debug("Planet {} has geo sid longitude: {}".\
                      format(planetName,
                             pi.geocentric["sidereal"]["longitude"]))
            
            fieldValue = None
                
            if centricityType.lower() == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type: {}".\
                          format(centricityType))
                fieldValue = None

            return fieldValue
            
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        currDiff = None
        prevDiff = None
        

        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            longitudesP1[-1] = \
                Util.toNormalizedAngle(\
                getFieldValue(currDt, planet1Params, fieldName))
            
            longitudesP2[-1] = fixedDegree

            log.debug("{} {} is: {}".\
                      format(planet1Params, fieldName,
                             longitudesP1[-1]))
            log.debug("fixedDegree is: {}".format(longitudesP2[-1]))
            
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - longitudesP2[-1])
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff != None and \
                   longitudesP1[-2] != None and \
                   longitudesP2[-2] != None:
                
                if abs(prevDiff - currDiff) > 180:
                    # Probably crossed over 0.  Adjust the prevDiff so
                    # that the rest of the algorithm can continue to
                    # work.
                    if prevDiff > currDiff:
                        prevDiff -= 360
                    else:
                        prevDiff += 360
                        
                    log.debug("After adjustment: prevDiff == {}".\
                              format(prevDiff))
                    log.debug("After adjustment: currDiff == {}".\
                              format(currDiff))

                for desiredAngleDeg in desiredAngleDegList:
                    log.debug("Looking at desiredAngleDeg: {}".\
                              format(desiredAngleDeg))
                    
                    desiredDegree = desiredAngleDeg
                    
                    if prevDiff < desiredDegree and currDiff >= desiredDegree:
                        log.debug("Crossed over {} from below to above!".\
                                  format(desiredDegree))
    
                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1
    
                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            log.debug("Refining between {} and {}".\
                                      format(Ephemeris.datetimeToStr(t1),
                                             Ephemeris.datetimeToStr(t2)))
    
                            # Check the timestamp between.
                            timeWindowTd = t2 - t1
                            halfTimeWindowTd = \
                                datetime.\
                                timedelta(days=(timeWindowTd.days / 2.0),
                                    seconds=(timeWindowTd.seconds / 2.0),
                                    microseconds=\
                                          (timeWindowTd.microseconds / 2.0))
                            testDt = t1 + halfTimeWindowTd
    
                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1Params, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(fixedDegree)
    
                            log.debug("testValueP1 == {}".format(testValueP1))
                            log.debug("testValueP2 == {}".format(testValueP2))
                            
                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360
                                
                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360
                            
                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)
    
                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360
                            
                            log.debug("testDiff == {}".format(testDiff))
                            
                            if testDiff < desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt
    
                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff
    
                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2
                
                            currErrorTd = t2 - t1
                                
                        # Update our lists.
                        steps[-1] = currDt
    
                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)
                     
                    elif prevDiff > desiredDegree and currDiff <= desiredDegree:
                        log.debug("Crossed over {} from above to below!".\
                                  format(desiredDegree))
    
                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1
    
                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            log.debug("Refining between {} and {}".\
                                      format(Ephemeris.datetimeToStr(t1),
                                             Ephemeris.datetimeToStr(t2)))
    
                            # Check the timestamp between.
                            timeWindowTd = t2 - t1
                            halfTimeWindowTd = \
                                datetime.\
                                timedelta(days=(timeWindowTd.days / 2.0),
                                    seconds=(timeWindowTd.seconds / 2.0),
                                    microseconds=\
                                          (timeWindowTd.microseconds / 2.0))
                            testDt = t1 + halfTimeWindowTd
    
                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1ParamsList, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(fixedDegree)
    
                            log.debug("testValueP1 == {}".format(testValueP1))
                            log.debug("testValueP2 == {}".format(testValueP2))
                            
                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360
                                
                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360
    
                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)
    
                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360
                            
                            log.debug("testDiff == {}".format(testDiff))
                            
                            if testDiff > desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt
    
                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff
    
                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2
                                
                            currErrorTd = t2 - t1
    
                        # Update our lists.
                        steps[-1] = currDt
    
                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)
                     
            # Prepare for the next iteration.
            log.debug("steps[-1] is: {}".\
                      format(Ephemeris.datetimeToStr(steps[-1])))
            log.debug("stepSizeTd is: {}".format(stepSizeTd))
            
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]
            longitudesP2.append(None)
            del longitudesP2[0]
            
            # Update prevDiff as the currDiff.
            prevDiff = Util.toNormalizedAngle(currDiff)
            
        log.info("Number of timestamps obtained: {}".\
                 format(len(aspectTimestamps)))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return aspectTimestamps

        
    @staticmethod
    def addLongitudeAspectVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        planet1Name,
        planet1CentricityType,
        planet1LongitudeType,
        planet2Name,
        planet2CentricityType,
        planet2LongitudeType,
        degreeDifference,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where planet 'planet1Name' and planet
        'planet2Name' are 'degreeDifference' degrees apart,
        geocentrically.  This includes approaching and separating
        aspects.

        For example, if the desired degree difference is 72, and
        planets are Mars and Venus, then it will catch Mars 0 deg
        aspecting Venus 72 deg, as well as Mars 0 deg aspecting Venus
        288 deg.

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
        planet1Name - str holding the name of the first planet to do the
                      calculations for.
        planet1CentricityType
                    - str value holding either "geocentric",
                      "topocentric", or "heliocentric".
        planet1LongitudeType
                    - str value holding either "tropical" or "sidereal".
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
        planet2CentricityType
                    - str value holding either "geocentric",
                      "topocentric", or "heliocentric".
        planet2LongitudeType
                    - str value holding either "tropical" or "sidereal".
        degreeDifference - float value for the number of degrees of
                           separation for this aspect.
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
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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

        # Check inputs for centricity type.
        planet1CentricityTypeOrig = planet1CentricityType
        planet1CentricityType = planet1CentricityType.lower()
        if planet1CentricityType != "geocentric" and \
           planet1CentricityType != "topocentric" and \
           planet1CentricityType != "heliocentric":

            log.error("Invalid input: planet1CentricityType is invalid.  " + \
                      "Value given was: {}".format(planet1CentricityTypeOrig))
            rv = False
            return rv

        planet2CentricityTypeOrig = planet2CentricityType
        planet2CentricityType = planet2CentricityType.lower()
        if planet2CentricityType != "geocentric" and \
           planet2CentricityType != "topocentric" and \
           planet2CentricityType != "heliocentric":

            log.error("Invalid input: planet2CentricityType is invalid.  " + \
                      "Value given was: {}".format(planet2CentricityTypeOrig))
            rv = False
            return rv

        # Check inputs for longitude type.
        planet1LongitudeTypeOrig = planet1LongitudeType
        planet1LongitudeType = planet1LongitudeType.lower()
        if planet1LongitudeType != "tropical" and \
           planet1LongitudeType != "sidereal":

            log.error("Invalid input: planet1LongitudeType is invalid.  " + \
                      "Value given was: {}".format(planet1LongitudeTypeOrig))
            rv = False
            return rv

        planet2LongitudeTypeOrig = planet2LongitudeType
        planet2LongitudeType = planet2LongitudeType.lower()
        if planet2LongitudeType != "tropical" and \
           planet2LongitudeType != "sidereal":

            log.error("Invalid input: planet2LongitudeType is invalid.  " + \
                      "Value given was: {}".format(planet2LongitudeTypeOrig))
            rv = False
            return rv

        # Field name we are getting.
        fieldName = "longitude"
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planet1Name)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:]

            if planet1CentricityType.startswith("geo"):
                tag += "_Geo"
            elif planet1CentricityType.startswith("topo"):
                tag += "_Topo"
            elif planet1CentricityType.startswith("helio"):
                tag += "_Helio"

            if planet1LongitudeType.startswith("trop"):
                tag += "_Trop"
            elif planet1LongitudeType.startswith("sid"):
                tag += "_Sid"

            tag += "_" + planet1Name
            
            tag += "_{}_DegreeAspect".\
                   format(degreeDifference, planet1Name, planet2Name)

            if planet2CentricityType.startswith("geo"):
                tag += "_Geo"
            elif planet2CentricityType.startswith("topo"):
                tag += "_Topo"
            elif planet2CentricityType.startswith("helio"):
                tag += "_Helio"

            if planet2LongitudeType.startswith("trop"):
                tag += "_Trop"
            elif planet2LongitudeType.startswith("sid"):
                tag += "_Sid"

            tag += "_" + planet2Name
            
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planet1Name) or \
               Ephemeris.isAscmcPlanetName(planet1Name) or \
               Ephemeris.isHouseCuspPlanetName(planet2Name) or \
               Ephemeris.isAscmcPlanetName(planet2Name):
            
            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)

        log.debug("Step size is: {}".format(stepSizeTd))
        
        # Desired angles.  We need to check for planets at these angles.
        desiredAngleDeg1 = abs(Util.toNormalizedAngle(degreeDifference))
        desiredAngleDeg2 = 360 - abs(Util.toNormalizedAngle(degreeDifference))

        log.debug("desiredAngleDeg1 is: {}".format(desiredAngleDeg1))
        log.debug("desiredAngleDeg2 is: {}".format(desiredAngleDeg2))
        
        # Count of artifacts added.
        numArtifactsAdded = 0
        
        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudesP1 = []
        longitudesP1.append(None)
        longitudesP1.append(None)
        
        longitudesP2 = []
        longitudesP2.append(None)
        longitudesP2.append(None)
        
        def getP1FieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if planet1CentricityType == "geocentric":
                fieldValue = pi.geocentric[planet1LongitudeType][fieldName]
            elif planet1CentricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[planet1LongitudeType][fieldName]
            elif planet1CentricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[planet1LongitudeType][fieldName]
            else:
                log.error("Unknown centricity type: {}".\
                          format(planet1CentricityType))
                fieldValue = None

            return fieldValue
            
        def getP2FieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if planet2CentricityType == "geocentric":
                fieldValue = pi.geocentric[planet2LongitudeType][fieldName]
            elif planet2CentricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[planet2LongitudeType][fieldName]
            elif planet2CentricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[planet2LongitudeType][fieldName]
            else:
                log.error("Unknown centricity type: {}".\
                          format(planet2CentricityType))
                fieldValue = None

            return fieldValue
            
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        
        currDiff = None
        prevDiff = None
        

        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)
            
            longitudesP1[-1] = getP1FieldValue(p1, fieldName)
            longitudesP2[-1] = getP2FieldValue(p2, fieldName)
            
            log.debug("{} {} {} {} is: {}".\
                      format(p1.name, planet1CentricityType,
                             planet1LongitudeType, fieldName,
                             longitudesP1[-1]))
            log.debug("{} {} {} {} is: {}".\
                      format(p2.name, planet2CentricityType,
                             planet2LongitudeType, fieldName,
                             longitudesP2[-1]))

            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - longitudesP2[-1])
                
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff != None and \
                   longitudesP1[-2] != None and \
                   longitudesP2[-2] != None:
                
                if abs(prevDiff - currDiff) > 180:
                    # Probably crossed over 0.  Adjust the prevDiff so
                    # that the rest of the algorithm can continue to
                    # work.
                    if prevDiff > currDiff:
                        prevDiff -= 360
                    else:
                        prevDiff += 360
                        
                    log.debug("After adjustment: prevDiff == {}".\
                              format(prevDiff))
                    log.debug("After adjustment: currDiff == {}".\
                              format(currDiff))
                    
                log.debug("Looking at desiredAngleDeg1: {}".\
                          format(desiredAngleDeg1))
                
                desiredDegree = desiredAngleDeg1
                if prevDiff < desiredDegree and currDiff >= desiredDegree:
                    log.debug("Crossed over {} from below to above!".\
                              format(desiredDegree))

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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planet1Name, testDt)
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, testDt)

                        testValueP1 = getP1FieldValue(p1, fieldName)
                        testValueP2 = getP2FieldValue(p2, fieldName)

                        log.debug("testValueP1 == {}".format(testValueP1))
                        log.debug("testValueP2 == {}".format(testValueP2))
                        
                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        elif longitudesP1[-2] < 120 and testValueP1 > 240:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 -= 360
                            
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360
                        elif longitudesP2[-2] < 120 and testValueP2 > 240:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 -= 360
                        
                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        # Handle special cases of degrees 0 and 360.
                        # Here we adjust testDiff so that it is in the
                        # expected ranges.
                        if Util.fuzzyIsEqual(desiredDegree, 0):
                            if testDiff > 240:
                                testDiff -= 360
                        elif Util.fuzzyIsEqual(desiredDegree, 360):
                            if testDiff < 120:
                                testDiff += 360
                        
                        log.debug("testDiff == {}".format(testDiff))
                        
                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                            longitudesP1[-1] = testValueP1
                            longitudesP2[-1] = testValueP2
            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1

                elif prevDiff > desiredDegree and currDiff <= desiredDegree:
                    log.debug("Crossed over {} from above to below!".\
                              format(desiredDegree))

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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planet1Name, testDt)
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, testDt)

                        testValueP1 = getP1FieldValue(p1, fieldName)
                        testValueP2 = getP2FieldValue(p2, fieldName)

                        log.debug("testValueP1 == {}".format(testValueP1))
                        log.debug("testValueP2 == {}".format(testValueP2))
                        
                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        elif longitudesP1[-2] < 120 and testValueP1 > 240:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 -= 360
                            
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360
                        elif longitudesP2[-2] < 120 and testValueP2 > 240:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 -= 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        # Handle special cases of degrees 0 and 360.
                        # Here we adjust testDiff so that it is in the
                        # expected ranges.
                        if Util.fuzzyIsEqual(desiredDegree, 0):
                            if testDiff > 240:
                                testDiff -= 360
                        elif Util.fuzzyIsEqual(desiredDegree, 360):
                            if testDiff < 120:
                                testDiff += 360
                        
                        log.debug("testDiff == {}".format(testDiff))
                        
                        if testDiff > desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                            longitudesP1[-1] = testValueP1
                            longitudesP2[-1] = testValueP2
                            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1

                log.debug("Looking at desiredAngleDeg2: {}".\
                          format(desiredAngleDeg2))
                
                desiredDegree = desiredAngleDeg2
                if prevDiff < desiredDegree and currDiff >= desiredDegree:
                    log.debug("Crossed over {} from below to above!".\
                              format(desiredDegree))

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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planet1Name, testDt)
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, testDt)

                        testValueP1 = getP1FieldValue(p1, fieldName)
                        testValueP2 = getP2FieldValue(p2, fieldName)

                        log.debug("testValueP1 == {}".format(testValueP1))
                        log.debug("testValueP2 == {}".format(testValueP2))
                        
                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        elif longitudesP1[-2] < 120 and testValueP1 > 240:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 -= 360
                            
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360
                        elif longitudesP2[-2] < 120 and testValueP2 > 240:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 -= 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        # Handle special cases of degrees 0 and 360.
                        # Here we adjust testDiff so that it is in the
                        # expected ranges.
                        if Util.fuzzyIsEqual(desiredDegree, 0):
                            if testDiff > 240:
                                testDiff -= 360
                        elif Util.fuzzyIsEqual(desiredDegree, 360):
                            if testDiff < 120:
                                testDiff += 360
                        
                        log.debug("testDiff == {}".format(testDiff))
                        
                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                            longitudesP1[-1] = testValueP1
                            longitudesP2[-1] = testValueP2
                            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1

                elif prevDiff > desiredDegree and currDiff <= desiredDegree:
                    log.debug("Crossed over {} from above to below!".\
                              format(desiredDegree))

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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planet1Name, testDt)
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, testDt)

                        testValueP1 = getP1FieldValue(p1, fieldName)
                        testValueP2 = getP2FieldValue(p2, fieldName)

                        log.debug("testValueP1 == {}".format(testValueP1))
                        log.debug("testValueP2 == {}".format(testValueP2))
                        
                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        elif longitudesP1[-2] < 120 and testValueP1 > 240:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 -= 360
                            
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360
                        elif longitudesP2[-2] < 120 and testValueP2 > 240:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 -= 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        # Handle special cases of degrees 0 and 360.
                        # Here we adjust testDiff so that it is in the
                        # expected ranges.
                        if Util.fuzzyIsEqual(desiredDegree, 0):
                            if testDiff > 240:
                                testDiff -= 360
                        elif Util.fuzzyIsEqual(desiredDegree, 360):
                            if testDiff < 120:
                                testDiff += 360
                        
                        log.debug("testDiff == {}".format(testDiff))
                        
                        if testDiff > desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                            longitudesP1[-1] = testValueP1
                            longitudesP2[-1] = testValueP2

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                 
            # Prepare for the next iteration.
            log.debug("steps[-1] is: {}".\
                      format(Ephemeris.datetimeToStr(steps[-1])))
            log.debug("stepSizeTd is: {}".format(stepSizeTd))
            
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]
            longitudesP2.append(None)
            del longitudesP2[0]

            # Update prevDiff as the currDiff.
            prevDiff = Util.toNormalizedAngle(currDiff)

        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def _getDatetimesOfElapsedLongitudeDegrees(\
        pcdd, 
        planetName, 
        centricityType,
        longitudeType,
        planetEpocDt,
        desiredDegreesElapsed,
        maxErrorTd=datetime.timedelta(seconds=2)):
        """Returns a list of datetime.datetime objects that hold the
        timestamps when the given planet is at 'degreeElapsed'
        longitude degrees from the longitude degrees calculated at
        moment 'planetEpocDt'.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        planetName - str holding the name of the planet to do the
                     calculations for.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        planetEpocDt - datetime.datetime object for the epoc or reference time.
                       The planet longitude at this moment is taken as
                       the zero-point.  Increments are started from
                       this moment in time.
        desiredDegreesElapsed - float value for the number of longitude degrees
                        elapsed from the longitude at 'planetEpocDt'.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        List of datetime.datetime objects.  The datetime.datetime
        objects in this list are the timestamps where the planet is at
        the elapsed number of degrees away from the longitude at
        'planetEpocDt'.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = []

        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            log.error("Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig))
            rv = []
            return rv

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            log.error("Invalid input: longitudeType is invalid.  " + \
                      "Value given was: {}".format(longitudeTypeOrig))
            rv = []
            return rv

        # Field name we are getting.
        fieldName = "longitude"
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.  Planet should not ever move more than
        # 120 degrees per step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)

        # Running count of number of full 360-degree circles.
        numFullCircles = 0
        
        # Desired degree.
        desiredDegree = None
        
        # Epoc longitude.
        planetEpocLongitude = None

        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(planetEpocDt))
        steps.append(copy.deepcopy(planetEpocDt))

        longitudesP1 = []
        longitudesP1.append(None)
        longitudesP1.append(None)
        
        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        log.debug("Stepping through timestamps from {} ...".\
                  format(Ephemeris.datetimeToStr(planetEpocDt)))

        currDiff = None
        prevDiff = None

        # Current and previous number of degrees elapsed.
        currElapsed = None
        
        done = False
        while not done:
        
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            if planetEpocLongitude == None:
                planetEpocLongitude = getFieldValue(p1, fieldName)
            
            longitudesP1[-1] = getFieldValue(p1, fieldName)
            
            log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))
            
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - planetEpocLongitude)
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff != None and longitudesP1[-2] != None:
                
                if prevDiff > 240 and currDiff < 120:
                    log.debug("Crossed over epoc longitude {} ".\
                              format(planetEpocLongitude) + \
                              "from below to above!")

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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                        testValueP1 = getFieldValue(p1, fieldName)

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - planetEpocLongitude)

                        if testDiff < 120:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                        else:
                            t1 = testDt

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Increment the number of 360-degree circles traversed.
                    numFullCircles += 1

                elif prevDiff < 120 and currDiff > 240:
                    log.debug("Crossed over epoc longitude {} ".\
                              format(planetEpocLongitude) + \
                              "from above to below!")

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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                        testValueP1 = getFieldValue(p1, fieldName)

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - planetEpocLongitude)

                        if testDiff < 120:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Decrement the number of 360-degree circles traversed.
                    numFullCircles -= 1

                # Calculate the total number of degrees elapsed so far.
                currElapsed = (numFullCircles * 360.0) + currDiff

                log.debug("currElapsed == {}".format(currElapsed))
                log.debug("desiredDegreesElapsed == {}".\
                          format(desiredDegreesElapsed))
                
                if currElapsed > desiredDegreesElapsed:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    log.debug("Passed the desired number of " + \
                              "elapsed degrees from below to above.  " + \
                              "Narrowing down to the exact moment in time ...")
                    
                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetEpocLongitude + (desiredDegreesElapsed % 360.0))

                    log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = t2 - t1
                    
                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        log.debug("Refining between {} and {}".\
                                  format(Ephemeris.datetimeToStr(t1),
                                         Ephemeris.datetimeToStr(t2)))

                        # Check the timestamp between.
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValueP1 = getFieldValue(p1, fieldName)

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - desiredDegree)
                        
                        if testDiff < 120:
                            t2 = testDt
                        else:
                            t1 = testDt

                        currErrorTd = t2 - t1

                    # t2 holds the moment in time.
                    rv.append(t2)

                    log.debug("First moment in time found to be: {}".\
                              format(Ephemeris.datetimeToStr(t2)))
                              
                    # Now find the the other elapsed points, if they
                    # exist.  We know it doesn't exist if it traverses
                    # more than 120 degrees from desiredDegree.
                    startDt = t2
                    prevDt = startDt
                    currDt = startDt + stepSizeTd
                    p1 = Ephemeris.getPlanetaryInfo(planetName, prevDt)
                    prevDiff = Util.toNormalizedAngle(\
                        getFieldValue(p1, fieldName) - desiredDegree)
                    currDiff = None

                    log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    while prevDiff <= 120 or prevDiff > 240:
                        p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                        currDiff = Util.toNormalizedAngle(\
                            getFieldValue(p1, fieldName) - desiredDegree)

                        log.debug("currDt == {}, ".\
                                  format(Ephemeris.datetimeToStr(currDt)) + 
                                  "longitude == {}, ".\
                                  format(getFieldValue(p1, fieldName)) + \
                                  "currDiff == {}".\
                                  format(currDiff))

                        if prevDiff > 240 and currDiff < 120:
                            log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "below to above.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = t2 - t1
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                log.debug("Refining between {} and {}".\
                                          format(Ephemeris.datetimeToStr(t1),
                                                 Ephemeris.datetimeToStr(t2)))
                                
                                # Check the timestamp between.
                                timeWindowTd = t2 - t1
                                halfTimeWindowTd = \
                                    datetime.\
                                    timedelta(days=(timeWindowTd.days / 2.0),
                                        seconds=(timeWindowTd.seconds / 2.0),
                                        microseconds=\
                                              (timeWindowTd.microseconds / 2.0))
                                testDt = t1 + halfTimeWindowTd
        
                                p1 = Ephemeris.getPlanetaryInfo(\
                                    planetName, testDt)
                                
                                testValueP1 = getFieldValue(p1, fieldName)
        
                                testDiff = Util.toNormalizedAngle(\
                                    testValueP1 - desiredDegree)
                                
                                if testDiff < 120:
                                    t2 = testDt

                                    currDt = t2
                                    currDiff = testDiff
                                else:
                                    t1 = testDt
        
                                currErrorTd = t2 - t1


                            # currDt holds the moment in time.
                            log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        elif prevDiff < 120 and currDiff > 240:
                            log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "above to below.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = t2 - t1
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                log.debug("Refining between {} and {}".\
                                          format(Ephemeris.datetimeToStr(t1),
                                                 Ephemeris.datetimeToStr(t2)))
                                
                                # Check the timestamp between.
                                timeWindowTd = t2 - t1
                                halfTimeWindowTd = \
                                    datetime.\
                                    timedelta(days=(timeWindowTd.days / 2.0),
                                        seconds=(timeWindowTd.seconds / 2.0),
                                        microseconds=\
                                              (timeWindowTd.microseconds / 2.0))
                                testDt = t1 + halfTimeWindowTd
        
                                p1 = Ephemeris.getPlanetaryInfo(\
                                    planetName, testDt)
                                
                                testValueP1 = getFieldValue(p1, fieldName)
        
                                testDiff = Util.toNormalizedAngle(\
                                    testValueP1 - desiredDegree)
                                
                                if testDiff > 240:
                                    t2 = testDt

                                    currDt = t2
                                    currDiff = testDiff
                                else:
                                    t1 = testDt
        
                                currErrorTd = t2 - t1
        
                            # currDt holds the moment in time.
                            log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        prevDt = currDt
                        currDt = copy.deepcopy(currDt) + stepSizeTd
                        prevDiff = currDiff
                        currDiff = None

                    log.debug("Done searching for timestamps.")
                        
                    # We have our timestamps, so we are done.
                    done = True
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]

            # Update prevDiff as the currDiff.
            prevDiff = currDiff

        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def addPlanetLongitudeTraversalIncrementsVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        planetName, 
        centricityType,
        longitudeType,
        planetEpocDt,
        degreeIncrement,
        color=None):
        """Adds vertical lines to the PriceChartDocumentData object,
        at locations where planet 'planetName' is 'degreeIncrement'
        degree-increments away from the longitude the planet is at at
        'planetEpocDt'.
        
        Maximum error timedelta is 2 seconds.
        
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
        planetName - str holding the name of the planet to do the
                     calculations for.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        planetEpocDt - datetime.datetime object for the epoc or reference time.
                       The planet longitude at this moment is taken as
                       the zero-point.  Increments are started from
                       this moment in time.
        degreeIncrement - float value for the number of longitude degrees
                          to increment from the longitude at 'planetEpocDt'.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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


        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            log.error("Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig))
            rv = False
            return rv

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            log.error("Invalid input: longitudeType is invalid.  " + \
                      "Value given was: {}".format(longitudeTypeOrig))
            rv = False
            return rv

        # Field name we are getting.
        fieldName = "longitude"
        
        # Set the color if it is not already set to something.
        colorWasSpecifiedFlag = True
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:]

            if centricityType.startswith("geo"):
                tag += "_Geo"
            elif centricityType.startswith("topo"):
                tag += "_Topo"
            elif centricityType.startswith("helio"):
                tag += "_Helio"

            if longitudeType.startswith("trop"):
                tag += "_Trop"
            elif longitudeType.startswith("sid"):
                tag += "_Sid"

            tag += "_{}_{}".\
                   format(degreeIncrement, planetName)
            
        log.debug("tag == '{}'".format(tag))

        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Count of artifacts added.
        numArtifactsAdded = 0

        currDt = startDt

        # Get the planet longitude at the epoc moment.
        p1 = Ephemeris.getPlanetaryInfo(planetName, planetEpocDt)
        planetEpocLongitude = getFieldValue(p1, fieldName)

        log.info("Planet epoc datetime  is: {}".\
                  format(Ephemeris.datetimeToStr(planetEpocDt)))
        log.info("Planet epoc longitude is: {}".\
                  format(planetEpocLongitude))
        
        desiredDegreesElapsed = degreeIncrement
        
        while currDt < endDt:
            datetimes = \
                PlanetaryCombinationsLibrary.\
                _getDatetimesOfElapsedLongitudeDegrees(\
                pcdd, planetName, centricityType, longitudeType,
                planetEpocDt, desiredDegreesElapsed)

            log.debug("{} datetimes returned by helper function.".\
                      format(len(datetimes)))
            
            for dt in datetimes:
                # Create the artifact at the timestamp.
                PlanetaryCombinationsLibrary.\
                    addVerticalLine(pcdd, dt,
                                    highPrice, lowPrice, tag, color)
                numArtifactsAdded += 1

            if len(datetimes) == 0:
                log.error("Number of datetimes returned shouldn't be zero.")
                return False
            
            # Prepare for the next iteration.
            currDt = datetimes[-1]
            planetEpocDt = currDt
            
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def getPlanetCrossingLongitudeDegTimestamps(\
        pcdd, startDt, endDt,
        centricityType, longitudeType, planetName, degree,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Returns a list of datetimes of when a certain planet crosses 
        a certain degree of longitude.
        
        The algorithm used assumes that a step size won't move the
        planet more than 1/3 of a circle.
        
        Arguments:
        pcdd          - PriceChartDocumentData object used for geographical 
                        location when initializing the ephemeris.
        startDt       - datetime.datetime object for the starting timestamp
                        to do the calculations for artifacts.
        endDt         - datetime.datetime object for the ending timestamp
                        to do the calculations for artifacts.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        planetName    - str value holding the name fo the planet to do
                        the search for.
        degree        - float value for the degree of longitude that should be
                        crossed in order to trigger a vertical line being drawn.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:

        List of datetime.datetime, containing the timestamps when the 
        planet crosses the degree, within the startDt and endDt.
        
        If an error occurred, the None is returned.
        """


        log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = []

        # Make sure the inputs are valid.
        if endDt < startDt:
            log.error("Invalid input: 'endDt' must be after 'startDt'")
            return None

        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            log.error("Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig))
            return None

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            log.error("Invalid input: longitudeType is invalid.  " + \
                      "Value given was: {}".format(longitudeTypeOrig))
            return None

        # Field name we are getting.
        fieldName = "longitude"
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):
            
            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
            
        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudes = []
        longitudes.append(None)
        longitudes.append(None)
        
        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
            
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            longitudes[-1] = getFieldValue(p1, fieldName)
            
            log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))
            
            if longitudes[-2] != None:
                
                currValue = None
                prevValue = None
                desiredDegree = None
                crossedOverZeroDegrees = None

                # This algorithm assumes that a step size won't move the
                # planet more than 1/3 of a circle.
                if longitudes[-2] > 240 and longitudes[-1] < 120:
                    # Hopped over 0 degrees from below to above.
                    prevValue = longitudes[-2]
                    currValue = longitudes[-1] + 360
                    desiredDegree = degree + 360
                    crossedOverZeroDegrees = True
                elif longitudes[-2] < 120 and longitudes[-1] > 240:
                    # Hopped over 0 degrees from above to below.
                    prevValue = longitudes[-2] + 360
                    currValue = longitudes[-1]
                    desiredDegree = degree
                    crossedOverZeroDegrees = True
                else:
                    # Did not cross 0 degrees.
                    prevValue = longitudes[-2]
                    currValue = longitudes[-1]
                    desiredDegree = degree
                    crossedOverZeroDegrees = False

                if prevValue < desiredDegree and currValue >= desiredDegree:
                    log.debug("Crossed over from below to above!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if longitudes[-2] > 240 and testValue < 120:
                            testValue += 360
                        
                        if testValue < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt
    
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    longitudes[-1] = Util.toNormalizedAngle(currValue)

                    # Append the result datetime found.
                    rv.append(currDt)
                    
                elif prevValue >= desiredDegree and currValue < desiredDegree:
                    log.debug("Crossed over from above to below!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if longitudes[-2] > 240 and testValue < 120:
                            testValue += 360
                        
                        if testValue >= desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                            
                        currErrorTd = t2 - t1
                    
                    # Update our lists.
                    steps[-1] = currDt
                    longitudes[-1] = Util.toNormalizedAngle(currValue)
                    
                    # Append the result datetime found.
                    rv.append(currDt)
            
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudes.append(None)
            del longitudes[0]

        log.info("Number of datetimes found: {}".format(len(rv)))
        
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    
    @staticmethod
    def getGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpoints(\
        pcdd,
        planetName,
        geoRetrogradeDirectTimestampsResultsList,
        maxErrorTd=datetime.timedelta(minutes=1)):
        """Obtains a list of tuples containing data describing
        the timestamps of when a particular planet is conjunct the
        midpoint longitude degree of: 

        - Longitude when the geocentric planet is starting to go retrograde.
        - Longitude when the geocentric planet is starting to go direct.

        There are three conjunctions for each pair of retrograde-direct
        timestamps.  These are called the Least, Mean, and Great conjunctions.

        'Least' conjunction is the first conjunction with that longitude,
        when the planet is currently going direct
        (this lies earlier in time before the Retrograde moment).

        'Mean' conjunction is the second conjunction with that longitude,
        when the planet is currently going retrograde.

        'Great' conjunction is the third conjunction with that longitude,
        when the planet is currently going retrograde.
        
        Note: The midpoint of the retrograde longitude and the 
        direct longitude is different from the midpoint of the 
        direct longitude and the retrograde longitude.  
        The method that deals with the second scenario is
        getGeoConjunctionsOfDirectRetrogradeMidpoints().  
        See that method if that's what I want to get.
        
        Arguments:

        pcdd       - PriceChartDocumentData object that is used for 
                     obtaining geographical location information.
                     This is used to initialize the ephemeris.

        planetName - str holding the name of the
                     planet to do the calculations for.

        geoRetrogradeDirectTimestampsResultsList - 
            List of tuples containing one of following possible entries, 
            depending on whether it is the moment the planet turns 
            direct or when the planet turns retrograde:
    
              (PlanetaryInfo p, "direct")
              (PlanetaryInfo p, "retrograde")
            
            The list of tuples' PlanetaryInfo's datetimes are timestamp-ordered.
            Thus: tup[0][0].dt is a datetime before tup[1][0].dt

        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:

        A list of tuples; each tuple in one of the following formats, 
        depending on whether the timestamp is a least conjunction, 
        mean conjunction or greater conjunction.

            (PlanetaryInfo p, "least")
            (PlanetaryInfo p, "mean")
            (PlanetaryInfo p, "greater")

        In the event of an error, the reference None is returned.
        """
        log.debug("Entered " + inspect.stack()[0][3] + "()")
        log.debug("planetName=" + planetName + ", " +
                  "maxErrorTd=" + str(maxErrorTd))

        # List of tuples that are returned.
        rv = []

        # Indexes into each tuple in list
        # geoRetrogradeDirectTimestampsResultsList:
        
        # Index to reference the PlanetaryInfo, in the tuple.
        piIndex = 0
        # Index for whether the movement is retrograde or direct, in the tuple.
        retroOrDirectIndex = 1
        
        # Make sure the inputs are valid.
        prevDt = None
        currDt = None
        for retroDirectResult in geoRetrogradeDirectTimestampsResultsList:
            if prevDt == None:
                prevDt = retroDirectResult[piIndex].dt
                continue
            elif currDt == None:
                currDt = retroDirectResult[piIndex].dt
            else:
                prevDt = currDt
                currDt = retroDirectResult[piIndex].dt

            if prevDt > currDt:
                log.error("Invalid input: 'geoRetrogradeDirectTimestampsResultsList' must be ordered by timestamp.")
                return None

        # Inputs are valid.

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)

        # Field name we are getting.
        fieldName = "longitude"
        centricityType = "geocentric"
        longitudeType = "tropical"
        
        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        # Iterate through the retrograde and direct data, calculating the
        # midpoints and then working on those.
        stations = []
        stations.append(None)
        stations.append(None)
        stations.append(None)

        if len(geoRetrogradeDirectTimestampsResultsList) < 3:
            log.error("Too low number of " +
                      "geocentric planetary stations detected!  " +
                      "Because of the algorithm I've chosen, " +
                      "you may not get any results.")
            return None
        elif len(geoRetrogradeDirectTimestampsResultsList) <= 3:
            log.warn("Too low number of " +
                      "geocentric planetary stations detected!  " +
                      "Because of the algorithm I've chosen, " +
                      "you may not get many results.")
            
        for i in range(len(geoRetrogradeDirectTimestampsResultsList)):
            log.debug("i == {}".format(i))

            del stations[0]
            stations.append(geoRetrogradeDirectTimestampsResultsList[i])

            # Debug print the values in the 'stations' list.
            for j in range(len(stations)):
                if stations[j] == None:
                    log.debug("stations[{}] == {}".format(j, None))
                    continue
                    
                retroOrDirectStr = ""
                if stations[j][piIndex].geocentric['tropical']['longitude_speed'] >= 0:
                    retroOrDirectStr = "direct"
                else:
                    retroOrDirectStr = "retrograde"
                    
                log.debug("stations[{}] == {} {} @ {} on {}".\
                          format(\
                          j,
                          stations[j][piIndex].name,
                          retroOrDirectStr,
                          stations[j][piIndex].geocentric['tropical']['longitude'],
                          Ephemeris.datetimeToStr(stations[j][piIndex].dt)))

            if i == 0 or i == 1:
                # Need three stations before starting to analyze.
                #
                # This is just so it's a simpler algorithm when computing
                # degree cross-overs.  This means, we would need a wider time
                # frame for the dataset of stations before calculating these
                # conjunctions.  This means I'll need to get stations
                # for about a year earlier than the actual conjunctions
                # I'm looking for.
                continue

            prevStation = geoRetrogradeDirectTimestampsResultsList[i-1]
            currStation = geoRetrogradeDirectTimestampsResultsList[i]

            # Debug printing.
            prevStationRetroOrDirectStr = ""
            if prevStation[piIndex].geocentric['tropical']['longitude_speed'] >= 0:
                prevStationRetroOrDirectStr = "direct"
            else:
                prevStationRetroOrDirectStr = "retrograde"
            log.debug("prevStation(i @ {}) == {} {} @ {}".\
                      format(\
                      i-1,
                      prevStation[piIndex].name,
                      prevStationRetroOrDirectStr,
                      prevStation[piIndex].geocentric['tropical']['longitude']))
            if currStation[piIndex].geocentric['tropical']['longitude_speed'] >= 0:
                currStationRetroOrDirectStr = "direct"
            else:
                currStationRetroOrDirectStr = "retrograde"
            log.debug("currStation(i @ {}) == {} {} @ {}".\
                      format(\
                      i,
                      currStation[piIndex].name,
                      currStationRetroOrDirectStr,
                      currStation[piIndex].geocentric['tropical']['longitude']))
            
            if prevStation[retroOrDirectIndex] == "retrograde" and \
                currStation[retroOrDirectIndex] == "direct":

                # We now have two values to compute a midpoint.
                prevStationLongitude = \
                    prevStation[piIndex].geocentric['tropical']['longitude']
                currStationLongitude = \
                    currStation[piIndex].geocentric['tropical']['longitude']
                    
                # Adjust for if it spans the 0 degree boundary.
                if prevStationLongitude < currStationLongitude:
                    prevStationLongitude += 360
                    
                # Calculate the midpoint.
                midpointLongitude = \
                    Util.toNormalizedAngle((prevStationLongitude +
                                            currStationLongitude) / 2.0)
                
                log.debug("midpointLongitude between {} and {} is: {}".\
                          format(Util.toNormalizedAngle(prevStationLongitude),
                                 Util.toNormalizedAngle(currStationLongitude),
                                 midpointLongitude))
                
                ###############################
                # Get the 'least' conjunction.
                # This is when it crosses the midpointLongitude the 1st time.

                log.debug("Looking for 'least' conjunction ...")
                
                startDt = stations[-3][piIndex].dt
                endDt   = stations[-2][piIndex].dt

                desiredDegree = midpointLongitude
                
                crossingsDts = \
                    PlanetaryCombinationsLibrary.\
                    getPlanetCrossingLongitudeDegTimestamps(\
                        pcdd, startDt, endDt,
                        centricityType, longitudeType, planetName,
                        desiredDegree, maxErrorTd)

                log.debug("Got {} crossings for 'least' conjunctions.".\
                          format(len(crossingsDts)))
                for j in range(len(crossingsDts)):
                    log.debug("crossingsDts[{}] == {}".\
                              format(j, Ephemeris.datetimeToStr(crossingsDts[j])))

                # We expect that we will cross the midpoint before we start
                # going retrograde.  This section of movement should be all
                # direct, therefore only one crossing.
                if len(crossingsDts) != 1:
                    errMsg = "Unexpected number of crossings returned.  " + \
                        "We expected only 1 !!!  There's a bug here."
                    log.error(errMsg)
                    raise RuntimeError(errMsg)

                currDt = crossingsDts[0]
                p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                resultTuple = (p1, "least")
                rv.append(resultTuple)
                
                ###############################
                # Get the 'mean' conjunction.
                # This is when it crosses the midpointLongitude the 2nd time.
                
                log.debug("Looking for 'mean' conjunction ...")
                
                startDt = stations[-2][piIndex].dt
                endDt   = stations[-1][piIndex].dt

                desiredDegree = midpointLongitude
                
                crossingsDts = \
                    PlanetaryCombinationsLibrary.\
                    getPlanetCrossingLongitudeDegTimestamps(\
                        pcdd, startDt, endDt,
                        centricityType, longitudeType, planetName,
                        desiredDegree, maxErrorTd)

                log.debug("Got {} crossings for 'mean' conjunctions.".\
                          format(len(crossingsDts)))
                for j in range(len(crossingsDts)):
                    log.debug("crossingsDts[{}] == {}".\
                              format(j, Ephemeris.datetimeToStr(crossingsDts[j])))

                # We expect that we will cross the midpoint before we start
                # going direct.  This section of movement should be all
                # retrograde, therefore only one crossing.
                if len(crossingsDts) != 1:
                    errMsg = "Unexpected number of crossings returned.  " + \
                        "We expected only 1 !!!  There's a bug here."
                    log.error(errMsg)
                    raise RuntimeError(errMsg)

                currDt = crossingsDts[0]
                p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                resultTuple = (p1, "mean")
                rv.append(resultTuple)

                ###############################
                # Get the 'great' conjunction.
                # This is when it crosses the midpointLongitude the 3rd time.
                
                log.debug("Looking for 'great' conjunction ...")
                
                startDt = stations[-1][piIndex].dt
                endDt   = startDt + datetime.timedelta(days=366)

                # We set endDt to the startDt + a year because we know this is
                # geocentric and every planet will cross the midpoint before
                # the next solar year.  Doing this endDt may yield more than
                # one datetime for the degree crossing here, which is fine.
                # We are looking for the first crossing.
                
                desiredDegree = midpointLongitude
                
                crossingsDts = \
                    PlanetaryCombinationsLibrary.\
                    getPlanetCrossingLongitudeDegTimestamps(\
                        pcdd, startDt, endDt,
                        centricityType, longitudeType, planetName,
                        desiredDegree, maxErrorTd)

                log.debug("Got {} crossings for 'great' conjunctions.".\
                          format(len(crossingsDts)))
                for j in range(len(crossingsDts)):
                    log.debug("crossingsDts[{}] == {}".\
                              format(j, Ephemeris.datetimeToStr(crossingsDts[j])))

                # We expect that we will cross the midpoint before we start
                # going retrograde.

                # Get the first timestamp found.
                currDt = crossingsDts[0]
                p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                resultTuple = (p1, "great")
                rv.append(resultTuple)

        log.debug("Returning {} data points in the list.".format(len(rv)))
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    
    @staticmethod
    def getGeoConjunctionsOfDirectRetrogradeMidpoints(\
        pcdd,
        planetName,
        geoRetrogradeDirectTimestampsResultsList,
        maxErrorTd=datetime.timedelta(minutes=1)):
        """Obtains a list of tuples containing data describing
        the timestamps of when a particular planet is conjunct the
        midpoint longitude degree of: 

        - Longitude when the geocentric planet is starting to go direct.
        - Longitude when the geocentric planet is starting to go retrograde.

        There should be only one conjunction for each pair of direct-retrograde
        timestamps.  
        
        Note: The midpoint of the midpoint of the direct longitude and
        the retrograde longitude is different from the midpoint of the
        retrograde longitude and the direct longitude.  The method
        that deals with the second scenario is
        getGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpoints().
        See that method if that's what I want to get.
        
        Arguments:

        pcdd       - PriceChartDocumentData object that is used for 
                     obtaining geographical location information.
                     This is used to initialize the ephemeris.

        planetName - str holding the name of the
                     planet to do the calculations for.

        geoRetrogradeDirectTimestampsResultsList - 
            List of tuples containing one of following possible entries, 
            depending on whether it is the moment the planet turns 
            direct or when the planet turns retrograde:
    
              (PlanetaryInfo p, "direct")
              (PlanetaryInfo p, "retrograde")
            
            The list of tuples' PlanetaryInfo's datetimes are timestamp-ordered.
            Thus: tup[0][0].dt is a datetime before tup[1][0].dt

        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:

        A list of PlanetaryInfo objects.  Each one representing the
        information about the planet when the planet is the at the
        desired midpoint.
        
        In the event of an error, the reference None is returned.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")
        log.debug("planetName=" + planetName + ", " +
                  "maxErrorTd=" + str(maxErrorTd))

        # List of tuples that are returned.
        rv = []

        # Indexes into each tuple in list
        # geoRetrogradeDirectTimestampsResultsList:
        
        # Index to reference the PlanetaryInfo, in the tuple.
        piIndex = 0
        # Index for whether the movement is retrograde or direct, in the tuple.
        retroOrDirectIndex = 1
        
        # Make sure the inputs are valid.
        prevDt = None
        currDt = None
        for retroDirectResult in geoRetrogradeDirectTimestampsResultsList:
            if prevDt == None:
                prevDt = retroDirectResult[piIndex].dt
                continue
            elif currDt == None:
                currDt = retroDirectResult[piIndex].dt
            else:
                prevDt = currDt
                currDt = retroDirectResult[piIndex].dt

            if prevDt > currDt:
                log.error("Invalid input: 'geoRetrogradeDirectTimestampsResultsList' must be ordered by timestamp.")
                return None

        # Inputs are valid.

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)

        # Field name we are getting.
        fieldName = "longitude"
        centricityType = "geocentric"
        longitudeType = "tropical"
        
        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        # Iterate through the retrograde and direct data, calculating the
        # midpoints and then working on those.
        stations = []
        stations.append(None)
        stations.append(None)

        if len(geoRetrogradeDirectTimestampsResultsList) < 2:
            log.warn("Too low number of " +
                      "geocentric planetary stations detected!")
            
        for i in range(len(geoRetrogradeDirectTimestampsResultsList)):
            log.debug("i == {}".format(i))

            del stations[0]
            stations.append(geoRetrogradeDirectTimestampsResultsList[i])
            
            # Debug print the values in the 'stations' list.
            for j in range(len(stations)):
                if stations[j] == None:
                    log.debug("stations[{}] == {}".format(j, None))
                    continue
                    
                retroOrDirectStr = ""
                if stations[j][piIndex].geocentric['tropical']['longitude_speed'] >= 0:
                    retroOrDirectStr = "direct"
                else:
                    retroOrDirectStr = "retrograde"
                    
                log.debug("stations[{}] == {} {} @ {} on {}".\
                          format(\
                          j,
                          stations[j][piIndex].name,
                          retroOrDirectStr,
                          stations[j][piIndex].geocentric['tropical']['longitude'],
                          Ephemeris.datetimeToStr(stations[j][piIndex].dt)))

            if i == 0:
                # Need two stations before starting to analyze.
                continue

            prevStation = geoRetrogradeDirectTimestampsResultsList[i-1]
            currStation = geoRetrogradeDirectTimestampsResultsList[i]

            # Debug printing.
            prevStationRetroOrDirectStr = ""
            if prevStation[piIndex].geocentric['tropical']['longitude_speed'] >= 0:
                prevStationRetroOrDirectStr = "direct"
            else:
                prevStationRetroOrDirectStr = "retrograde"
            log.debug("prevStation(i @ {}) == {} {} @ {}".\
                      format(\
                      i-1,
                      prevStation[piIndex].name,
                      prevStationRetroOrDirectStr,
                      prevStation[piIndex].geocentric['tropical']['longitude']))
            if currStation[piIndex].geocentric['tropical']['longitude_speed'] >= 0:
                currStationRetroOrDirectStr = "direct"
            else:
                currStationRetroOrDirectStr = "retrograde"
            log.debug("currStation(i @ {}) == {} {} @ {}".\
                      format(\
                      i,
                      currStation[piIndex].name,
                      currStationRetroOrDirectStr,
                      currStation[piIndex].geocentric['tropical']['longitude']))
            
            if prevStation[retroOrDirectIndex] == "direct" and \
                currStation[retroOrDirectIndex] == "retrograde":
                
                # We now have two values to compute a midpoint.
                prevStationLongitude = \
                    prevStation[piIndex].geocentric['tropical']['longitude']
                currStationLongitude = \
                    currStation[piIndex].geocentric['tropical']['longitude']
                    
                # Adjust for if it spans the 0 degree boundary.
                if prevStationLongitude > currStationLongitude:
                    currStationLongitude += 360
                    
                # Calculate the midpoint.
                midpointLongitude = \
                    Util.toNormalizedAngle((prevStationLongitude +
                                            currStationLongitude) / 2.0)

                log.debug("midpointLongitude between {} and {} is: {}".\
                          format(Util.toNormalizedAngle(prevStationLongitude),
                                 Util.toNormalizedAngle(currStationLongitude),
                                 midpointLongitude))
                
                ###############################
                # Get the conjunction.
                # This is when it crosses the midpointLongitude the 1st
                # and only time.

                log.debug("Looking for the conjunction ...")
                
                startDt = stations[-2][piIndex].dt
                endDt   = stations[-1][piIndex].dt
                
                desiredDegree = midpointLongitude
                
                crossingsDts = \
                    PlanetaryCombinationsLibrary.\
                    getPlanetCrossingLongitudeDegTimestamps(\
                        pcdd, startDt, endDt,
                        centricityType, longitudeType, planetName,
                        desiredDegree, maxErrorTd)
                
                log.debug("Got {} crossings for the conjunction.".\
                          format(len(crossingsDts)))
                for j in range(len(crossingsDts)):
                    log.debug("crossingsDts[{}] == {}".\
                              format(j, Ephemeris.datetimeToStr(crossingsDts[j])))
                
                # We expect that we will cross the midpoint before we start
                # going retrograde.  This section of movement should be all
                # direct, therefore only one crossing.
                if len(crossingsDts) != 1:
                    errMsg = "Unexpected number of crossings returned.  " + \
                        "We expected only 1 !!!  There's a bug here."
                    log.error(errMsg)
                    raise RuntimeError(errMsg)

                currDt = crossingsDts[0]
                p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                rv.append(p1)
        
        log.debug("Returning {} data points in the list.".format(len(rv)))
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    
    @staticmethod
    def getGeoRetrogradeDirectTimestamps(\
        pcdd, startDt, endDt,
        planetName,
        maxErrorTd=datetime.timedelta(minutes=1)):
        """Obtains a list of tuples containing data describing
        the timestamps of when the specified planet is going 
        retrograde or direct (i.e. is stationary).
        
        Arguments:
        pcdd      - PriceChartDocumentData object that is used for 
                    obtaining geographical location information.
                    This is used to initialize the ephemeris.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        planetName - str holding the name of the
                     planet to do the calculations for.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:

        List of tuples containing one of following possible entries, 
        depending on whether it is the moment the planet turns 
        direct or when the planet turns retrograde:

          (PlanetaryInfo p, "direct")
          (PlanetaryInfo p, "retrograde")
        
        The list of tuples' PlanetaryInfo's datetimes are timestamp-ordered.
        Thus: tup[0][0].dt is a datetime before tup[1][0].dt

        In the event of an error, the reference None is returned.
        """

        log.debug("Entered " + inspect.stack()[0][3] + "()")
        log.debug("startDt=" + Ephemeris.datetimeToDayStr(startDt) + ", " + 
                  "endDt=" + Ephemeris.datetimeToDayStr(endDt) +  ", " + 
                  "planetName=" + planetName + ", " +
                  "maxErrorTd=" + str(maxErrorTd))
        
        # List of tuples that are returned.
        rv = []
        
        # Make sure the inputs are valid.
        if endDt < startDt:
            log.error("Invalid input: 'endDt' must be after 'startDt'")
            return None

        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
        
        # Field name we are getting.
        fieldName = "longitude_speed"
        centricityType = "geocentric"
        longitudeType = "tropical"

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)
        
        # Now, in UTC.
        now = datetime.datetime.now(pytz.utc)
        
        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))
        
        # Velocity of the steps saved (list of float).
        velocitys = []
        velocitys.append(None)
        velocitys.append(None)

        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        # Iterate through, creating artfacts and adding them as we go.
        log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))
        
        while steps[-1] < endDt:
            currDt = steps[-1]
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
            
            velocitys[-1] = getFieldValue(p1, fieldName)
            
            log.debug("{} velocity is: {}".\
                      format(p1.name, velocitys[-1]))
            
            for i in range(len(steps)):
                log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(velocitys)):
                log.debug("velocitys[{}] == {}".format(i, velocitys[i]))
            
            
            if velocitys[-2] != None:

                prevValue = velocitys[-2]
                currValue = velocitys[-1]
                prevDt = steps[-2]
                currDt = steps[-1]
                desiredVelocity = 0
                
                if prevValue < desiredVelocity and currValue >= desiredVelocity:
                    log.debug("Went from Retrograde to Direct!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if testValue < desiredVelocity:
                            t1 = testDt
                        else:
                            t2 = testDt
    
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                            
                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    velocitys[-1] = currValue

                    pi = Ephemeris.getPlanetaryInfo(planetName, currDt)
                    tup = (pi, "direct")
                    rv.append(tup)
                    
                elif prevValue >= desiredVelocity and currValue < desiredVelocity:
                    log.debug("Went from Direct to Retrograde!")
                    
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
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd
                        
                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValue = getFieldValue(p1, fieldName)

                        if testValue >= desiredVelocity:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currValue = testValue
                        
                        currErrorTd = t2 - t1
                    
                    # Update our lists.
                    steps[-1] = currDt
                    velocitys[-1] = currValue
                    
                    pi = Ephemeris.getPlanetaryInfo(planetName, currDt)
                    tup = (pi, "retrograde")
                    rv.append(tup)
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            velocitys.append(None)
            del velocitys[0]

        log.info("Number of geo retrograde or direct planet timestamps: {}".\
                 format(len(rv)))
            
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addGeoConjunctionsOfDirectRetrogradeMidpointsVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(minutes=1)):
        """Adds vertical line segments whenever the given planet reaches
        conjunction with the midpoint longitude degree of: 

        - Longitude when the geocentric planet is starting to go direct.
        - Longitude when the geocentric planet is starting to go retrograde.

        There should be only one conjunction for each pair of direct-retrograde
        timestamps.  
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the top of the vertical line that is drawn.
        lowPrice  - float value for the low price which represents
                    the bottom of the vertical line that is drawn.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        lighterColor = None
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            lighterColor = color.lighter()
        else:
            lighterColor = color

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:]

            tag += "_Geo_Trop_{}".format(planetName)
            
        log.debug("tag == '{}'".format(tag))

        # Count of artifacts added.
        numArtifactsAdded = 0
        
        geoRetrogradeDirectTimestampsResultsList = \
            PlanetaryCombinationsLibrary.\
            getGeoRetrogradeDirectTimestamps(pcdd, startDt, endDt, 
                                             planetName, maxErrorTd)

        planetaryInfos = \
            PlanetaryCombinationsLibrary.\
            getGeoConjunctionsOfDirectRetrogradeMidpoints(pcdd, planetName,
                geoRetrogradeDirectTimestampsResultsList, maxErrorTd)

        for pi in planetaryInfos:
            # Create the artifact at the timestamp.
            PlanetaryCombinationsLibrary.\
            addVerticalLine(pcdd, pi.dt, highPrice, lowPrice, tag, 
                        lighterColor)
            numArtifactsAdded += 1
    
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
            
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def addGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpointsVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(minutes=1)):
        """Adds vertical line segments whenever the given planet reaches
        conjunction with the midpoint longitude degree of: 

        - Longitude when the geocentric planet is starting to go retrograde.
        - Longitude when the geocentric planet is starting to go direct.

        There are three conjunctions for each pair of retrograde-direct
        timestamps.  These are called the Least, Mean, and Great conjunctions.

        'Least' conjunction is the first conjunction with that longitude,
        when the planet is currently going direct
        (this lies earlier in time before the Retrograde moment).

        'Mean' conjunction is the second conjunction with that longitude,
        when the planet is currently going retrograde.

        'Great' conjunction is the third conjunction with that longitude,
        when the planet is currently going retrograde.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price which represents
                    the top of the vertical line that is drawn.
        lowPrice  - float value for the low price which represents
                    the bottom of the vertical line that is drawn.
        planetName - str holding the name of the planet to do the
                     calculations for.
        color     - QColor object for what color to draw the lines.
                    If this is set to None, then the default color will be used.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.  
        
        Returns:
        True if operation succeeded, False otherwise.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

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
        colorWasSpecifiedFlag = True
        lighterColor = None
        if color == None:
            colorWasSpecifiedFlag = False
            color = AstrologyUtils.getForegroundColorForPlanetName(planetName)
            lighterColor = color.lighter()
        else:
            lighterColor = color

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:]

            tag += "_Geo_Trop_{}".format(planetName)
            
        log.debug("tag == '{}'".format(tag))

        # Count of artifacts added.
        numArtifactsAdded = 0
        
        geoRetrogradeDirectTimestampsResultsList = \
            PlanetaryCombinationsLibrary.\
            getGeoRetrogradeDirectTimestamps(pcdd, startDt, endDt, 
                                             planetName, maxErrorTd)

        tupleResults = \
            PlanetaryCombinationsLibrary.\
            getGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpoints(\
                pcdd, planetName,
                geoRetrogradeDirectTimestampsResultsList, maxErrorTd)

        # Index to reference the PlanetaryInfo, in the tuple.
        piIndex = 0
        # Index for what type of conjunction it is, in the tuple.
        conjunctionTypeIndex = 1

        for tup in tupleResults:
            pi = tup[piIndex]
            conjunctionType = tup[conjunctionTypeIndex]

            # Create the artifact at the timestamp.
            PlanetaryCombinationsLibrary.\
            addVerticalLine(pcdd, pi.dt, highPrice, lowPrice, 
                    tag + "_" + conjunctionType.upper() + "_conjunction",
                    lighterColor)
            numArtifactsAdded += 1
    
        log.info("Number of artifacts added: {}".format(numArtifactsAdded))
            
        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv
    
##############################################################################

