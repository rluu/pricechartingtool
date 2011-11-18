#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Template module for modifying a PriceChartDocumentData object via
#   modifyPriceChartDocument.py.
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
    with the given tag.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.  The value of this field
           may be "" if a tag is not specified by the user.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    # Return value.
    rv = 0

    numArtifacts = len(pcdd.priceBarChartArtifacts)
    log.info("Number of artifacts in this pcdd: {}".format(numArtifacts))

    for i in range(numArtifacts):
        artifact = pcdd.priceBarChartArtifacts[i]
        headerStr = "[{}]: ".format(i)
        
    rv = 1
    return rv

        
