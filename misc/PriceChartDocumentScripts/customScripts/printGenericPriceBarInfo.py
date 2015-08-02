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

    # Get the number of PriceBars.
    numPriceBars = len(pcdd.priceBars)
    
    # Get the earliest and latest PriceBar.
    earliestPriceBar = None
    latestPriceBar = None
    lowestPrice = None
    highestPrice = None
    lowestClosePrice = None
    highestClosePrice = None

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
            
        if lowestClosePrice == None:
            lowestClosePrice = pb.close
        elif pb.close < lowestClosePrice:
            lowestClosePrice = pb.close

        if highestClosePrice == None:
            highestClosePrice = pb.close
        elif pb.close > highestClosePrice:
            highestClosePrice = pb.close
            
    log.info("")
    log.info("Number of PriceBars: {}".format(numPriceBars))

    if numPriceBars > 0:

        # Make sure we got values for everything.
        if earliestPriceBar == None or \
               latestPriceBar == None or \
               lowestPrice == None or \
               highestPrice == None or \
               lowestClosePrice == None or \
               highestClosePrice == None:
            
            log.error("PriceBars existed, but we are missing some set values.")
            rv = 1
            return rv
        
        # Convert the datetimes to julian day.
        earliestPriceBarJd = \
            Ephemeris.datetimeToJulianDay(earliestPriceBar.timestamp)
        latestPriceBarJd = \
            Ephemeris.datetimeToJulianDay(latestPriceBar.timestamp)

        # Print the information to log.
        log.info("EarliestPriceBar datetime   == {}".\
                 format(Ephemeris.datetimeToStr(earliestPriceBar.timestamp)))
        log.info("LatestPriceBar   datetime   == {}".\
                 format(Ephemeris.datetimeToStr(latestPriceBar.timestamp)))
        log.info("EarliestPriceBar julian day == {}".format(earliestPriceBarJd))
        log.info("LatestPriceBar   julian day == {}".format(latestPriceBarJd))
        log.info("Lowest  PriceBar LOW   price == {}".format(highestPrice))
        log.info("Highest PriceBar HIGH  price == {}".format(highestPrice))
        log.info("Lowest  PriceBar CLOSE price == {}".format(highestPrice))
        log.info("Highest PriceBar CLOSE price == {}".format(highestPrice))
        
    log.info("")

    rv = 1
    return rv

        
