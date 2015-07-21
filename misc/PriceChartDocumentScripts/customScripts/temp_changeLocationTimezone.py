#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for modifying a PCDD by removing all the artifacts in it.
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
    """Modifies the PriceChartDocumentData object's internal artifacts
    by removing all PriceBarChartArtifacts that have a matching tag
    with the one specified to this function.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.  The value of this field
           may be "" if a tag is not specified by the user.
           This implementation does not use this parameter.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    # Return value.
    rv = 0

    numArtifacts = len(pcdd.priceBarChartArtifacts)
    log.info("Number of artifacts in this pcdd beforehand: {}".\
             format(numArtifacts))

    pcdd.locationTimezone = pytz.timezone("America/Chicago")

    for pb in pcdd.priceBars:
        pb.timestamp = pb.timestamp.replace(tzinfo=None)
        localizedTimestamp = pcdd.locationTimezone.localize(pb.timestamp)
        pb.timestamp = localizedTimestamp
        
    numArtifacts = len(pcdd.priceBarChartArtifacts)
    log.info("Number of artifacts in this pcdd afterwards: {}".\
             format(numArtifacts))

    return rv

        
