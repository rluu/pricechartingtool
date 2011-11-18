#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for modifying a PCDD by adding the 'tags' empty list to all
#   PriceBarChartArtifacts that don't already have that field in their
#   object dictionary.  This was needed because I intended to support
#   additional tagging functionality for all artifacts, and to be able
#   to add and remove them via tags.
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
#logLevel = logging.DEBUG
logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

def modifyPCDD(pcdd, tag):
    """Modifies the PriceChartDocumentData object's internal artifacts
    by adding the 'tags' empty list to all PriceBarChartArtifacts that
    don't already have that field in their object dictionary.  This was
    needed because I intended to support additional tagging
    functionality for all artifacts, and to be able to add and
    remove them via tags.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.  The value of this field
           may be "" if a tag is not specified by the user.
           This parameter is not used in this implementation of modifyPCDD().

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
        
        if 'tags' in artifact.__dict__:
            log.info(headerStr + "Already Exists.")
            log.debug(headerStr + "tags is: {}".format(artifact.tags))
        else:
            log.debug(headerStr + \
                      "tags does NOT exist in the dictionary.  Adding it...")
            artifact.tags = []
            
            if 'tags' in artifact.__dict__:
                log.info(headerStr + "Fixed.")
            else:
                log.error(headerStr + \
                          "Yikes, tags still doesn't exist.  " + \
                          "Please look into why this happened.")
                # Don't save changes.
                rv = 1
                
    return rv

        
