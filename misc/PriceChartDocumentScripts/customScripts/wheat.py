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
from ephemeris_utils import EphemerisUtils
from util import Util
from color import Color
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
#startDt = datetime.datetime(year=1904, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=1704, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
startDt = datetime.datetime(year=1968, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=2002, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=2009, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=1959, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)

#endDt = datetime.datetime(year=1914, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=2008, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=2012, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
endDt   = datetime.datetime(year=2017, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=2020, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt = datetime.datetime(year=2002, month=1, day=1,
#                          hour=0, minute=0, second=0,
#                          tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
highPrice = 1200.0
#highPrice = 200.0
lowPrice = 100.0
#lowPrice = 0.0

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

    # Initialize the Ephemeris with the birth location.
    log.debug("Setting ephemeris location ...")
    Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                    pcdd.birthInfo.latitudeDegrees,
                                    pcdd.birthInfo.elevation)

    stepSizeTd = datetime.timedelta(days=3)
    #highPrice = 800.0
    #highPrice = 600.0
    #lowPrice = 600.0
    #lowPrice = 300.0

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.blue))

    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.red))

    if True:
        planetA = ("Mars", "heliocentric", "tropical")
        planetB = ("Saturn", "heliocentric", "tropical")
        degreeDifference = 0
        uniDirectionalAspectsFlag = True
        planetAAndBAspectDts = \
            EphemerisUtils.getLongitudeAspectTimestamps(startDt,
                                                        endDt,
                                                        [planetA],
                                                        [planetB],
                                                        degreeDifference,
                                                        uniDirectionalAspectsFlag)

        for aspectDt in planetAAndBAspectDts:
            log.debug("Looking at aspectDt: " +
                    Ephemeris.datetimeToDayStr(aspectDt) +
                    ", where {} has a {} degree aspect to {}".\
                            format("{} {}".format(planetA[1], planetA[0]),
                                degreeDifference,
                                "{} {}".format(planetB[1], planetB[0])))

            # Draw a vertical line here on the chart.
            tag = "{}_{}_{}_deg_aspect_to_{}_{}".format(
                planetA[1], planetA[0],
                degreeDifference,
                planetB[1], planetB[0])
            color = Color.darkRed
            PlanetaryCombinationsLibrary.\
                addVerticalLine(pcdd, aspectDt, highPrice, lowPrice, tag, color)

            # At this moment in time get all the planets' positions.
            mercuryPI = Ephemeris.getPlanetaryInfo("Mercury", aspectDt)
            venusPI = Ephemeris.getPlanetaryInfo("Venus", aspectDt)
            earthPI = Ephemeris.getPlanetaryInfo("Earth", aspectDt)
            sunPI = Ephemeris.getPlanetaryInfo("Sun", aspectDt)
            marsPI = Ephemeris.getPlanetaryInfo("Mars", aspectDt)
            jupiterPI = Ephemeris.getPlanetaryInfo("Jupiter", aspectDt)
            saturnPI = Ephemeris.getPlanetaryInfo("Saturn", aspectDt)
            avgJuSaPI = Ephemeris.getPlanetaryInfo("AvgJuSa", aspectDt)

            log.debug("H.Earth is at {} degrees.".\
                    format(earthPI.heliocentric['tropical']['longitude']))
            log.debug("H.Mars is at {} degrees.".\
                    format(marsPI.heliocentric['tropical']['longitude']))

            helioMarsToHelioEarthDegrees = \
                Util.toNormalizedAngle(\
                    earthPI.heliocentric['tropical']['longitude'] -
                    marsPI.heliocentric['tropical']['longitude'])

            log.debug("H.Earth is {} degrees ahead of H.Mars.".\
                    format(helioMarsToHelioEarthDegrees))

            # Get the timestamp that H.Mars returns to this location.
            helioMarsReturnDt = \
                EphemerisUtils.getOnePlanetLongitudeAspectTimestamps(\
                startDt=aspectDt,
                endDt=endDt + datetime.timedelta(days=720), # Something a little more than a full H.Mars revolution.
                planet1Params=("Mars", "heliocentric", "tropical"),
                fixedDegree=marsPI.heliocentric['tropical']['longitude'],
                degreeDifference=360,
                uniDirectionalAspectsFlag=True)[0]

            log.debug("One H.Mars revolution from aspectDt {} would be at {}".\
                    format(Ephemeris.datetimeToDayStr(aspectDt),
                        Ephemeris.datetimeToDayStr(helioMarsReturnDt)))

            # Get the next timestamp that transiting H.Mars crosses
            # H.Earth's longitude, at the conjunction timestamp.
            helioMarsAtPrevHelioEarthPosDuringImageDt = \
                EphemerisUtils.getDatetimesOfElapsedLongitudeDegrees(\
                    planetName=planetA[0],
                    centricityType=planetA[1],
                    longitudeType=planetA[2],
                    planetEpocDt=aspectDt,
                    desiredDegreesElapsed=helioMarsToHelioEarthDegrees)[0]

            log.debug("helioMarsAtPrevHelioEarthPosDuringImageDt == {}".\
                format(Ephemeris.datetimeToDayStr(\
                            helioMarsAtPrevHelioEarthPosDuringImageDt)))

            # Draw a vertical line here on the chart.
            tag = "helioMarsAtPrevHelioEarthPosDuringImageDt"
            color = Color.darkOrange
            PlanetaryCombinationsLibrary.\
                addVerticalLine(pcdd, helioMarsAtPrevHelioEarthPosDuringImageDt,
                        highPrice, lowPrice, tag, color)

            # When Sun is in:
            # Gemini: 18, 47-48, 57, 141, 
            # Cancer: 72, 100
            # Do G.Sun movements of 33, 72, 194?, 500, 900?
            #77, 122.75, 155, 
# Do H.Mars movements of 70?, 72 [cancer], 80, 98, 100 [cancer], 120, 122.75, 137, 147, 150, 153, 169?, #
# 314?, 370?, 441?, 540, 588, 637?
# Do G.Mars movements of 108?, 112, 140?, 210?, 360, 368.25, 432?, 
# Do H.Mercury movements of 1000 [cancer], 2000? 4000?
            # Take some measurements from here.
            longitudeTraversalMeasurements = \
                [72, 80, 98, 100, 120, 137, 147, 150, 153, 169, 314, 370, 441, 540, 588, 637]

            for traversalMeasurement in longitudeTraversalMeasurements:
                dt = \
                    EphemerisUtils.getDatetimesOfElapsedLongitudeDegrees(\
                        planetName=planetA[0],
                        centricityType="heliocentric",
                        longitudeType="tropical",
                        planetEpocDt=helioMarsAtPrevHelioEarthPosDuringImageDt,
                        desiredDegreesElapsed=traversalMeasurement)[0]

                log.debug("{} {} moving {} deg from {} is: {}".format(\
                        planetA[1], planetA[0],
                        traversalMeasurement,
                        Ephemeris.datetimeToDayStr(\
                            helioMarsAtPrevHelioEarthPosDuringImageDt),
                        Ephemeris.datetimeToDayStr(dt)))

                avgHighLowPrice = (highPrice + lowPrice) / 2
                y = \
                    PlanetaryCombinationsLibrary.scene.priceToSceneYPos(avgHighLowPrice)
                startX = \
                    PlanetaryCombinationsLibrary.scene.datetimeToSceneXPos(\
                        helioMarsAtPrevHelioEarthPosDuringImageDt)
                endX = \
                    PlanetaryCombinationsLibrary.scene.datetimeToSceneXPos(dt)

                artifact = PriceBarChartPlanetLongitudeMovementMeasurementArtifact()
                artifact.setStartPointF(QPointF(startX, y))
                artifact.setEndPointF(QPointF(endX, y))
                artifact.textXScaling = 2.0
                artifact.textYScaling = 1.0
                artifact.showHeliocentricTextFlag = True
                artifact.tropicalZodiacFlag = True
                artifact.measurementUnitDegreesEnabled = True
                artifact.measurementUnitCirclesEnabled = False
                artifact.measurementUnitBiblicalCirclesEnabled = False
                artifact.planetMarsEnabledFlag = True
                artifact.addTag("H.Mars_moves_{}_deg".format(traversalMeasurement))
                pcdd.priceBarChartArtifacts.append(artifact)

        success = True

    #if True:
    #    degreeValue = 0
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Moon", "geocentric", "tropical",
    #        "Sun", "geocentric", "tropical",
    #        degreeValue, color=QColor(Qt.blue))

    #if True:
    #    degreeValue = 180
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Moon", "geocentric", "tropical",
    #        "Sun", "geocentric", "tropical",
    #        degreeValue, color=QColor(Qt.red))

    # Works with a high percentage.
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioJupiterSaturn15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)

    # Works maybe 50% of the time to show turns, and 25% of the time
    # to show time frames.  It is a little sloppy at places, so this
    # needs more investigation.
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoJupiterSaturn15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)

    # A few major turns hit exactly.  Some minor turns hit.
    # Needs more investigation.
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioSaturnUranus15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoSaturnUranus15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)

    # There is definitely a Mars-Venus connection, but there is more
    # to it... there are a lot of false hits with just 15x.
    #success = PlanetaryCombinationsLibrary.\
    #    addGeoVenusMars15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioVenusMars15xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)

    #success = PlanetaryCombinationsLibrary.\
    #    addHelioVenusMars90xVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)
    #success = PlanetaryCombinationsLibrary.\
    #    addHelioVenus265DegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)


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

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetCrossingLongitudeDegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "geocentric", "sidereal", "Venus", 358)
    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetCrossingLongitudeDegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "geocentric", "sidereal", "Mars", 297)

    #degreeValue = 180
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Mars", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    degreeValue)

    #divisor = 13
    #incrementSize = 14.4 # 360 / divisor
    #for i in range(divisor):
    #    if i == 0:
    #        continue
    #    degreeValue = i * incrementSize
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Venus", "geocentric", "sidereal",
    #        "Mars", "geocentric", "sidereal",
    #        degreeValue)

    #divisor = 5
    #incrementSize = 72 # 360 / divisor
    #for i in range(divisor):
    #    if i == 0:
    #        continue
    #    degreeValue = i * incrementSize
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Venus", "geocentric", "sidereal",
    #        "Mars", "geocentric", "sidereal",
    #        degreeValue)

    #divisor = 12
    #incrementSize = 30 # 360 / divisor
    #for i in range(divisor):
    #    if i == 0:
    #        continue
    #    degreeValue = i * incrementSize
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Saturn", "geocentric", "sidereal",
    #        "TrueNorthNode", "geocentric", "sidereal",
    #        degreeValue)

    #divisor = 12
    #incrementSize = 30 # 360 / divisor
    #for i in range(divisor):
    #    degreeValue = i * incrementSize
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Jupiter", "heliocentric", "sidereal",
    #        "Saturn", "heliocentric", "sidereal",
    #        degreeValue)

    #divisor = 9
    #incrementSize = 40 # 360 / divisor
    #for i in range(divisor):
    #    degreeValue = (3.3333333333 / 2.0) + (i * incrementSize)
    #    success = PlanetaryCombinationsLibrary.\
    #        addPlanetCrossingLongitudeDegVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "heliocentric", "sidereal",
    #        "Venus", degreeValue)

    #divisor = 12
    #incrementSize = 30 # 360 / divisor
    #for i in range(divisor):
    #    degreeValue = 15 + (i * incrementSize)
    #    success = PlanetaryCombinationsLibrary.\
    #        addPlanetCrossingLongitudeDegVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "geocentric", "sidereal",
    #        "Venus", degreeValue)

    #divisor = 24
    #incrementSize = 360 / divisor # 15
    #for i in range(divisor):
    #    degreeValue = i * incrementSize
    #    success = PlanetaryCombinationsLibrary.\
    #        addPlanetCrossingLongitudeDegVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "geocentric", "tropical",
    #        "Sun", degreeValue)

    # This needs more investigation.
    #divisor = 10
    #incrementSize = 36
    #for i in range(divisor):
    #    degreeValue = i * incrementSize
    #    success = PlanetaryCombinationsLibrary.\
    #        addPlanetCrossingLongitudeDegVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "geocentric", "tropical",
    #        "Venus", degreeValue)

    #divisor = 25
    #incrementSize = 360 / divisor # 15
    #for i in range(divisor):
    #    degreeValue = i * incrementSize
    #    success = PlanetaryCombinationsLibrary.\
    #        addPlanetCrossingLongitudeDegVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "geocentric", "tropical",
    #        "Venus", degreeValue)

    #degreeValue = 90 + 17 + (44/60.0)
    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetCrossingLongitudeDegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "heliocentric", "sidereal",
    #    "Saturn", degreeValue)
    #degreeValue = 240 + 21 + (25/60.0)
    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetCrossingLongitudeDegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "heliocentric", "sidereal",
    #    "Mercury", degreeValue)
    #degreeValue = 150 + 18 + (0/60.0)
    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetCrossingLongitudeDegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "heliocentric", "sidereal",
    #    "Venus", degreeValue)


    ####################################################################
    # Bayer's combinations from George Wollsten
    #
    # rluu: They don't really work as described in cleartext.  I need
    # to decode the text to see if there are deeper meanings and
    # deeper rules given.
    ####################################################################
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Jupiter", "heliocentric", "sidereal",
    #    "Mercury", "heliocentric", "sidereal", 0)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Saturn", "heliocentric", "sidereal",
    #    "Mercury", "heliocentric", "sidereal", 0)
    #degreeValue = 0
    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetCrossingLongitudeDegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "heliocentric", "tropical",
    #    "Mercury", degreeValue)
    #degreeValue = 180
    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetCrossingLongitudeDegVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "heliocentric", "tropical",
    #    "Mercury", degreeValue)
    ####################################################################

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.blue))

    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.red))

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=None)

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=None)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Mars", "geocentric", "sidereal",
    #    54)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "heliocentric", "sidereal",
    #    "Mars", "heliocentric", "sidereal",
    #    0)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Mars", "Earth",
    #    "heliocentric", "sidereal", 0)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Mars", "Earth",
    #    "heliocentric", "sidereal", 180)

    #step = 15
    #start = 0
    #stop = 180 + step # Add step to make it inclusive.
    #for degreeDifference in range(start, stop, step):
    #    success = PlanetaryCombinationsLibrary.\
    #        addLongitudeAspectVerticalLines(\
    #        pcdd, startDt, endDt, highPrice, lowPrice,
    #        "Venus", "heliocentric", "sidereal",
    #        "Earth", "heliocentric", "sidereal",
    #        degreeDifference)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Jupiter", "heliocentric", "sidereal",
    #    "Uranus", "heliocentric", "sidereal",
    #    0)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "heliocentric", "sidereal",
    #    "Earth", "heliocentric", "sidereal",
    #    10)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Mars", "geocentric", "sidereal",
    #    17.5)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Sun", "geocentric", "sidereal",
    #    0)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Mars", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    180)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Uranus", "geocentric", "sidereal",
    #    "Venus", "geocentric", "sidereal",
    #    72)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Uranus", "geocentric", "sidereal",
    #    "Venus", "geocentric", "sidereal",
    #    144)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Uranus", "geocentric", "sidereal",
    #    "Venus", "geocentric", "sidereal",
    #    216)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Uranus", "geocentric", "sidereal",
    #    "Venus", "geocentric", "sidereal",
    #    288)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    0)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    30)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    60)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    90)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    120)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    150)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Uranus", "geocentric", "sidereal",
    #    180)

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Mars", "geocentric", "sidereal",
    #    90)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Saturn", "geocentric", "sidereal",
    #    "Pluto", "geocentric", "sidereal",
    #    0)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Saturn", "geocentric", "sidereal",
    #    "Pluto", "geocentric", "sidereal",
    #    90)
    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Saturn", "geocentric", "sidereal",
    #    "Pluto", "geocentric", "sidereal",
    #    180)

    stepSizeTd = datetime.timedelta(days=3)
    #highPrice = 800.0
    #highPrice = 600.0
    #lowPrice = 600.0
    #lowPrice = 300.0

    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mercury",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mars",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Uranus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Saturn",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="MeanOfFive",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="CycleOfEight",
    #    color=None, stepSizeTd=stepSizeTd)

    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice=700, lowPrice=660,
    #    planetName="Moon",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mercury",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mars",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Jupiter",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Saturn",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Uranus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Neptune",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Pluto",
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
    #    pcdd, startDt, endDt, price=p, planetName="ARMC")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Vertex")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="EquatorialAscendant")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="CoAscendant1")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="CoAscendant2")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="PolarAscendant")
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



    #success = PlanetaryCombinationsLibrary.\
    #    addZeroDeclinationVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice, planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addDeclinationVelocityPolarityChangeVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice, planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addGeoLongitudeElongationVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice, planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addGeoLongitudeElongationVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice, planetName="Mercury")

    #success = PlanetaryCombinationsLibrary.\
    #    addContraparallelDeclinationAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addParallelDeclinationAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetOOBVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus")

    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus")
    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Jupiter", stepSizeTd=datetime.timedelta(days=7))
    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Saturn", stepSizeTd=datetime.timedelta(days=7))
    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Uranus", stepSizeTd=datetime.timedelta(days=7))

    #success =  PlanetaryCombinationsLibrary.\
    #    addZeroGeoLatitudeVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeVelocityPolarityChangeVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice, planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addContraparallelGeoLatitudeAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addParallelGeoLatitudeAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetLongitudeTraversalIncrementsVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    planetEpocDt=datetime.datetime(year=1976, month=4, day=1,
    #                                   hour=13, minute=0, second=0,
    #                                   tzinfo=pytz.utc),
    #    degreeIncrement=18)

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetLongitudeTraversalIncrementsVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "heliocentric", "sidereal",
    #    planetEpocDt=datetime.datetime(year=1970, month=3, day=21,
    #                                   hour=0, minute=0, second=0,
    #                                   tzinfo=pytz.utc),
    #    degreeIncrement=30)

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetLongitudeTraversalIncrementsVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Sun", "geocentric", "tropical",
    #    planetEpocDt=datetime.datetime(year=1970, month=3, day=21,
    #                                   hour=6, minute=0, second=0,
    #                                   tzinfo=pytz.utc),
    #    degreeIncrement=15)

    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury")

    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus")

    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mars")

    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Jupiter")

    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeVelocityPolarityChangeVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Saturn")

    #success = PlanetaryCombinationsLibrary.\
    #    addLongitudeAspectVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    "Venus", "heliocentric", "sidereal",
    #    0)


    # Doesn't work well for wheat.
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
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Aligns with some turns but misses with many others.
    # Needs some refinement.
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
                "Mars", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

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
                "Mars", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Does not work that well for wheat.
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
                "Mars", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 8.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Mars", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if success == True:
        log.debug("Success!")
        rv = 0
    else:
        log.debug("Failure!")
        rv = 1

    return rv

