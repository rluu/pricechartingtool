#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for printing generic information about the PriceBars in a
#   PriceChartDocumentData object.  The generic information that is
#   printed includes:
#
#    - Earliest pricebar timestamp as a datetime.datetime and a julian day.
#    - Latest   pricebar timestamp as a datetime.datetime and a julian day.
#    - highest  pricebar high price.
#    - lowest   pricebar low price.
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

def processPCDD(pcdd, tag):
    """Module for printing generic information about the PriceBars in a
    PriceChartDocumentData object.  The generic information that is
    printed includes:
 
     - Earliest pricebar timestamp as a datetime.datetime and a julian day.
     - Latest   pricebar timestamp as a datetime.datetime and a julian day.
     - highest  pricebar high price.
     - lowest   pricebar low price.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.  The value of this field
           may be "" if a tag is not specified by the user.
           This implementation doesn't use this field.
           
    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    This implementation always returns 1.
    """

    # Return value.
    rv = 1

    # List of tuples of the form (datetime.datetime, price).
    priceTimeInfoTupleList = []

    # Counting the number of PriceBarChartPriceTimeInfoArtifact objects.
    numPriceTimeInfoArtifacts = 0

    # Scene used for datetime and price conversions.
    scene = PriceBarChartGraphicsScene()
    
    artifacts = pcdd.priceBarChartArtifacts

    for artifact in artifacts:
        if isinstance(artifact, PriceBarChartPriceTimeInfoArtifact):
            numPriceTimeInfoArtifacts += 1

            infoPointF = artifact.getInfoPointF()
            dt = scene.sceneXPosToDatetime(infoPointF.x())
            price = scene.sceneYPosToPrice(infoPointF.y())

            priceTimeInfoTupleList.append((dt, price))

    # Sort by timestamp, because when obtained they might not be in order:
    sortedPriceTimeInfoTupleList = sorted(priceTimeInfoTupleList,
                                          key=lambda tup: tup[0])

    # Print out the timestamps and price.
    for tup in sortedPriceTimeInfoTupleList:
        dt = tup[0]
        price = tup[1]
        log.info("{},{}".format(Ephemeris.datetimeToDayStr(dt), price))
    
    rv = 1
    return rv

        
