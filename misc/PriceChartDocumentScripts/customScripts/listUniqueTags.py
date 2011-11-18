#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for listing all the unique artifact tags in a
#   PriceChartDocumentData object.
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
#logLevel = logging.DEBUG
logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

def processPCDD(pcdd, tag):
    """Lists all the unique artifact tags in a
    PriceChartDocumentData object.

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

    # Dictionary.  The keys are unique tags, and the value for the key
    # is the artifact count that uses that particular tag.
    uniqueTags = {}

    numArtifacts = len(pcdd.priceBarChartArtifacts)
    log.info("Number of artifacts in this pcdd: {}".format(numArtifacts))

    for i in range(numArtifacts):
        artifact = pcdd.priceBarChartArtifacts[i]
        
        for tag in artifact.tags:
            if tag != "":
                if tag not in uniqueTags.keys():
                    # First time seeing this tag.
                    # Initialize the count to 1.
                    uniqueTags[tag] = 1
                else:
                    # Tag was seen previously.
                    # Increment the count.
                    uniqueTags[tag] = uniqueTags[tag] + 1
                    
                log.debug("Tag='{}', ArtifactCount={}".\
                        format(tag, uniqueTags[tag]))
            
    log.info("Number of unique tags: {}".format(len(uniqueTags.keys())))

    # Put all the unique tags in a sorted list.
    sortedUniqueTags = []
    for tag in uniqueTags.keys():
        sortedUniqueTags.append(tag)
    sortedUniqueTags.sort()

    # Iterate through the sorted unique tags, printing them and their
    # artifact count.
    for tag in sortedUniqueTags:
        log.info("Tag='{}', ArtifactCount={}".\
                 format(tag, uniqueTags[tag]))

    return rv

        
