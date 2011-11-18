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
    with the given tag.

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
    
    #print("pcdd == {}".format(pcdd.toString()))
    
    log.info("Number of artifacts in this pcdd: {}".\
              format(len(pcdd.priceBarChartArtifacts)))
    
    for i in range(len(pcdd.priceBarChartArtifacts)):
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

        
