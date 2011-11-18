#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for printing information about the BirthInfo in a
#   PriceChartDocumentData object.  BirthInfo printed includes:
#
#    - Birth location name.
#    - Birth country name.
#    - Birth location coordinates.
#    - Birth timestamp as a UTC datetime.datetime
#    - Birth timestamp as a julian day.
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
from geonames import GeoInfo

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
    """
    Module for printing information about the BirthInfo in a
    PriceChartDocumentData object.  BirthInfo printed includes:
 
     - Birth location name.
     - Birth country name.
     - Birth location coordinates.
     - Birth timestamp as a UTC datetime.datetime
     - Birth timestamp as a julian day.

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

    birthInfo = pcdd.birthInfo

    # Convert longitude from a float value to degrees,
    # minutes, seconds and East/West polarity.
    (lonDegrees, lonMinutes, lonSeconds, lonPolarity) = \
        GeoInfo.longitudeToDegMinSec(birthInfo.longitudeDegrees)
    
    # Convert latitude from a float value to degrees, minutes,
    # seconds and North/South polarity.
    (latDegrees, latMinutes, latSeconds, latPolarity) = \
        GeoInfo.latitudeToDegMinSec(birthInfo.latitudeDegrees)
    
    log.info("")
    log.info("Birth location name: {}".format(birthInfo.locationName))
    log.info("Birth location country: {}".format(birthInfo.countryName))
    log.info("Birth location longitude: {} {} {}' {} ({})".\
             format(lonDegrees,
                    lonPolarity,
                    lonMinutes,
                    lonSeconds,
                    birthInfo.longitudeDegrees))
    log.info("Birth location latitude:  {} {} {}' {} ({})".\
             format(latDegrees,
                    latPolarity,
                    latMinutes,
                    latSeconds,
                    birthInfo.latitudeDegrees))

    birthLocalizedDatetime = birthInfo.getBirthLocalizedDatetime()
    birthUtcDatetime = birthInfo.getBirthUtcDatetime()
    birthJd = Ephemeris.datetimeToJulianDay(birthUtcDatetime)
    log.info("Birth timestamp (localized):  {}".\
             format(Ephemeris.datetimeToStr(birthLocalizedDatetime)))
    log.info("Birth timestamp (UTC):        {}".\
             format(Ephemeris.datetimeToStr(birthUtcDatetime)))
    log.info("Birth timestamp (julian day): {}".\
             format(birthJd))
    log.info("")

    rv = 1
    return rv

        
