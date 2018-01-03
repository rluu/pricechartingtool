#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for modifying a PCDD by removing all the artifacts that
#   have a matching tag with the one specified to processPCCD().
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
    by removing all PriceBarChartArtifacts that have a matching tag
    with the one specified to this function.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.  The value of this field
           may be "" if a tag is not specified by the user, but
           an error will be reported in that case and a
           return code of 1 returned.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    # Return value.
    rv = 0

    numArtifactsBeforehand = len(pcdd.priceBarChartArtifacts)

    # Keep only artifacts that have no tags.  
    # (i.e. artifacts with tags are removed).
    pcdd.priceBarChartArtifacts[:] = \
        [artifact for artifact in pcdd.priceBarChartArtifacts \
        if not artifactHasNonEmptyTag(artifact)]

    numArtifactsAfterwards = len(pcdd.priceBarChartArtifacts)
    numArtifactsRemoved = numArtifactsBeforehand - numArtifactsAfterwards

    log.info("Number of artifacts in this pcdd beforehand: {}".\
             format(numArtifactsBeforehand))
    log.info("Number of artifacts in this pcdd afterwards: {}".\
             format(numArtifactsAfterwards))
    log.info("Number of artifacts in this pcdd that were removed is: {}".\
             format(numArtifactsRemoved))

    return rv

def artifactHasNonEmptyTag(artifact):
    rv = False
    for tag in artifact.tags:
        if tag != "":
            log.info("Artifact {} has tags: {}".\
                    format(artifact.getInternalName(), artifact.tags))
            rv = True
            break
    return rv

