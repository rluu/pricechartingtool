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

# For math.floor()
import math

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
logging.basicConfig(format='%(levelname)s: %(message)s')
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
    def isHouseCuspPlanetName(planetName):
        """Returns True if the planet name given is a house cusp.
        Planet name is a house cusp if it is in the form "HX" or "HXX",
        where the letter 'H' is static and the 'X' represents a numerical
        digit.

        Arguments:
        planetName - str for the planet name to analyze.

        Returns:
        True if the planet name represents a astrological house cusp,
        False otherwise.
        """

        # Flag as True until found otherwise.
        isHouseCusp = True

        if 2 <= len(planetName) <= 3:
            # Name of the planet is 2 or 3 letters.
            if planetName[0] != "H":
                isHouseCusp = False
            if not planetName[1].isdigit():
                isHouseCusp = False
            if len(planetName) == 3 and not planetName[2].isdigit():
                isHouseCusp = False
        else:
            isHouseCusp = False

        return isHouseCusp


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
        if PlanetaryCombinationsLibrary.isHouseCuspPlanetName(planetName):
            # House cusps need a smaller step size.
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
                    # Hopped over 0 degrees.
                    prevValue = longitudes[-2]
                    currValue = longitudes[-1] + 360
                    desiredDegree = degree + 360
                    crossedOverZeroDegrees = True
                else:
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
                    
                elif prevValue > desiredDegree and currValue <= desiredDegree:
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
                        
                        if testValue > desiredDegree:
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
            if startPI.geocentric['sidereal']['longitude_speed'] < 0:
                startMotionAbbrev = "R"
            else:
                startMotionAbbrev = "D"
            
            endMotionAbbrev = None
            if endPI.geocentric['sidereal']['longitude_speed'] < 0:
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
            
            speed = p1.geocentric['sidereal']['longitude_speed']
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
                    speed = p1.geocentric['sidereal']['longitude_speed']
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
                    speed = p1.geocentric['sidereal']['longitude_speed']
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
                             p1.geocentric['sidereal']['longitude_speed']))
            
            velocitys[-1] = p1.geocentric['sidereal']['longitude_speed']
            
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
        PlanetaryCombinationsLibrary.\
            addHorizontalLine(pcdd, startDt, endDt, avgPrice,
                              tag="VelocityZeroLine_{}".format(planetName),
                              color=QColor(Qt.black))
        numArtifactsAdded += 1
        
        # Add a horizontal line for the planet's heliocentric speed,
        # if it is not zero.
        #if helioSpeed != 0.0:
            #pricePerSpeedDeg = (highPrice - avgPrice) / maxAbsoluteSpeed
            #print("avgPrice == {}".format(avgPrice))
            #print("maxAbsoluteSpeed == {}".format(maxAbsoluteSpeed))
            #print("pricePerSpeedDeg == {}".format(pricePerSpeedDeg))
            #
            #price = avgPrice + (pricePerSpeedDeg * helioSpeed)
            #print("helioSpeed == {}".format(helioSpeed))
            #print("price == {}".format(price))
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
        planet's latitude degrees.  The start and end points of
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
    def addZeroLatitudeVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's
        latitude changes from increasing to decreasing or
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
    def addLatitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt,
        highPrice, lowPrice,
        planetName,
        color=None,
        maxErrorTd=datetime.timedelta(hours=1)):
        """Adds a vertical line segments whenever a planet's
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
    def addContraparallelLatitudeAspectVerticalLines(\
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
    def addParallelLatitudeAspectVerticalLines(\
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
    def addLongitudeAspectVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        planet1Name, planet2Name,
        centricityType,
        longitudeType,
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
        planet2Name - str holding the name of the second planet to do the
                      calculations for.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
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
            color = AstrologyUtils.getForegroundColorForPlanetName(planet1Name)

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

            tag += "_{}_DegreeAspect_{}_{}".\
                   format(degreeDifference, planet1Name, planet2Name)
            
        log.debug("tag == '{}'".format(tag))
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if PlanetaryCombinationsLibrary.isHouseCuspPlanetName(planet1Name) or \
               PlanetaryCombinationsLibrary.isHouseCuspPlanetName(planet2Name):
            
            # House cusps need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
        
        # Desired angles.  We need to check for planets at these angles.
        desiredAngleDeg1 = abs(Util.toNormalizedAngle(degreeDifference))
        desiredAngleDeg2 = 360 - abs(Util.toNormalizedAngle(degreeDifference))

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

        
        currDiff = None
        prevDiff = None
        

        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))
            
            p1 = Ephemeris.getPlanetaryInfo(planet1Name, currDt)
            p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)
            
            longitudesP1[-1] = getFieldValue(p1, fieldName)
            longitudesP2[-1] = getFieldValue(p2, fieldName)
            
            log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))
            log.debug("{} {} {} {} is: {}".\
                      format(p2.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p2, fieldName)))

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
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)

                        testValueP1 = getFieldValue(p1, fieldName)
                        testValueP2 = getFieldValue(p2, fieldName)

                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

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
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)

                        testValueP1 = getFieldValue(p1, fieldName)
                        testValueP2 = getFieldValue(p2, fieldName)

                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        if testDiff > desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                        
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
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)

                        testValueP1 = getFieldValue(p1, fieldName)
                        testValueP2 = getFieldValue(p2, fieldName)

                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        if testDiff < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

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
                        p2 = Ephemeris.getPlanetaryInfo(planet2Name, currDt)

                        testValueP1 = getFieldValue(p1, fieldName)
                        testValueP2 = getFieldValue(p2, fieldName)

                        if longitudesP1[-2] > 240 and testValueP1 < 120:
                            # Planet 1 hopped over 0 degrees.
                            testValueP1 += 360
                        if longitudesP2[-2] > 240 and testValueP2 < 120:
                            # Planet 2 hopped over 0 degrees.
                            testValueP2 += 360

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - testValueP2)

                        if testDiff > desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Create the artifact at the timestamp.
                    PlanetaryCombinationsLibrary.\
                        addVerticalLine(pcdd, currDt,
                                        highPrice, lowPrice, tag, color)
                    numArtifactsAdded += 1
                 
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]
            longitudesP2.append(None)
            del longitudesP2[0]

            # Update prevDiff as the currDiff.
            prevDiff = currDiff

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
        if PlanetaryCombinationsLibrary.isHouseCuspPlanetName(planetName):
            # House cusps need a smaller step size.
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

