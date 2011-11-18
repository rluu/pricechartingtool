#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for drawing two veritcal lines (line segments) at 1/3 and
#   2/3 of the way through the price chart.
#
##############################################################################

# For logging.
import logging

# Include some PriceChartingTool modules.
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene

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

##############################################################################

def modifyPCDD(pcdd, tag):
    """Module for drawing two veritcal lines (line segments) at 1/3
    and 2/3 of the way through the price chart.  The lines will have a
    tag str matching the given tag parameter.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.  

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    # Return value.
    rv = 0

    # Check input.
    if tag == None or tag == "":
        log.error("Must specify a non-empty tag str value.")
        rv = 1
        return rv


    # Get the earliest and latest PriceBar.
    earliestPriceBar = None
    latestPriceBar = None
    lowestPrice = None
    highestPrice = None
    
    for pb in pcdd.priceBars:
        if earliestPriceBar == None:
            earliestPriceBar = pb
        elif pb.timestamp < earliestPriceBar.timestamp:
            earliestPriceBar = pb

        if latestPriceBar == None:
            latestPriceBar = pb
        elif pb.timestamp > latestPriceBar.timestamp:
            latestPriceBar = pb

        if lowestPrice == None:
            lowestPrice = pb.low
        elif pb.low < lowestPrice:
            lowestPrice = pb.low

        if highestPrice == None:
            highestPrice = pb.high
        elif pb.high > highestPrice:
            highestPrice = pb.high
            
    if earliestPriceBar == None or \
           latestPriceBar == None or \
           lowestPrice == None or \
           highestPrice == None:
        
        log.info("No pricebars were found in the document.  " + \
                 "Not doing anything.")
        rv = 1
        return rv

    # Convert the datetimes to julian day.
    earliestPriceBarJd = \
        Ephemeris.datetimeToJulianDay(earliestPriceBar.timestamp)
    latestPriceBarJd = \
        Ephemeris.datetimeToJulianDay(latestPriceBar.timestamp)

    log.debug("earliestPriceBar.timestamp == {}".\
              format(Ephemeris.datetimeToStr(earliestPriceBar.timestamp)))
    log.debug("latestPriceBar.timestamp == {}".\
              format(Ephemeris.datetimeToStr(latestPriceBar.timestamp)))

    log.debug("earliestPriceBarJd == {}".format(earliestPriceBarJd))
    log.debug("latestPriceBarJd == {}".format(latestPriceBarJd))

    diff = latestPriceBarJd - earliestPriceBarJd

    jdLine1 = earliestPriceBarJd + (diff / 3)
    jdLine2 = earliestPriceBarJd + ((diff / 3) * 2)

    dtLine1 = Ephemeris.julianDayToDatetime(jdLine1)
    dtLine2 = Ephemeris.julianDayToDatetime(jdLine2)

    log.debug("Creating scene...")

    # Scene for conversion functions.
    scene = PriceBarChartGraphicsScene()

    log.debug("Converting dt to x...")

    line1X = scene.datetimeToSceneXPos(dtLine1)
    line2X = scene.datetimeToSceneXPos(dtLine2)
    
    log.debug("Converting price to y...")

    lowY = scene.priceToSceneYPos(lowestPrice)
    highY = scene.priceToSceneYPos(highestPrice)
    
    log.debug("Creating line1 artifact ...")
    line1Artifact = PriceBarChartLineSegmentArtifact()
    line1Artifact.addTag(tag)
    line1Artifact.setTiltedTextFlag(False)
    line1Artifact.setAngleTextFlag(False)
    line1Artifact.setColor(QColor(Qt.red))
    line1Artifact.setStartPointF(QPointF(line1X, lowY))
    line1Artifact.setEndPointF(QPointF(line1X, highY))
    
    log.debug("Creating line2 artifact ...")
    line2Artifact = PriceBarChartLineSegmentArtifact()
    line2Artifact.addTag(tag)
    line2Artifact.setTiltedTextFlag(False)
    line2Artifact.setAngleTextFlag(False)
    line2Artifact.setColor(QColor(Qt.blue))
    line2Artifact.setStartPointF(QPointF(line2X, lowY))
    line2Artifact.setEndPointF(QPointF(line2X, highY))

    log.debug("Appending two lines...")

    pcdd.priceBarChartArtifacts.append(line1Artifact)
    pcdd.priceBarChartArtifacts.append(line2Artifact)

    log.debug("Done appending two lines.")
              
    # TODO:  remove the below line (rv=1) during/after testing.
    rv = 1
    
    return rv

        
