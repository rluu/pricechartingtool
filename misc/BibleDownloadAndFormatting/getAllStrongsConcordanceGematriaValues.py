#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This script goes through all the Strong's concordance numbers for
#   and obtains the matching gematria value for that word.  The
#   Strong's Number and gematria value pairs are then written to a CSV
#   file.
#
# Usage:
#
#   1) Update the global variable 'outputFilename' to the desired
#   output CSV filename.
#
#   2) Run the script:
#
#       python3 getAllStrongsConcordanceGematriaValues.py
#
# Note:
#
#   This script will take approximately 105 minutes to run.
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For logging.
import logging

# For connecting to the server via HTTP
import http.cookiejar
import urllib
from urllib import *

##############################################################################


##############################################################################
# Global variables

# Output filename to save the output CSV file to.
outputFilename = "/home/rluu/programming/pricechartingtool/misc/BibleDownloadAndFormatting/BibleGematriaValues.csv"

# Header line to put as the first line of text in the destination file.
headerLine = "\"Strong's Concordance Number\",\"Gematria value\""


# Use Windows newlines in the output file.
newline = "\r\n"

# For logging.
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s: %(message)s',
#                    filename="log.txt",
#                    filemode='w')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)


##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    logging.shutdown()
    sys.exit(rc)

##############################################################################

def getGematriaValueForStrongsConcordanceNumber(strongsNumberStr):
    """Returns the gematria value for the given Strong's Concordance
    Number string.

    Arguments:
    
    strongsNumberStr - str value holding the Strong's Concordance Number
                       string.  The string should be in the format "HXXXX"
                       or "GXXXX", where the X's are numbers.

    Returns:
    int value holding the gematria value for the word connected to
    that concordance number.
    If the gematria value could not be obtained from the URL's returned HTML,
    then an error is logged, and None is returned.
    """

    # Error checking of the input.
    if len(strongsNumberStr) != 5:
        log.error("Invalid Strong's Concordance Number: {}".\
                  format(strongsNumberStr))
        shutdown(1)
        
    if strongsNumberStr[0].upper() != "H" and \
       strongsNumberStr[0].upper() != "G":
        
        log.error("First character of the Strong's Concordance Number " + \
                  "must be a G or H.  " + \
                  "str given was: {}".format(strongsNumberStr))
        shutdown(1)
    
    if not strongsNumberStr[1:5].isdigit():
        
        log.error("Characters in the str are not numerical digits " + \
                  "as expected.  " + \
                  "str given was: {}".format(strongsNumberStr))
        shutdown(1)

    
    # Force the first letter to be uppercase.
    strongsNumberStr = strongsNumberStr[0].upper() + strongsNumberStr[1:]
    
    
    # This is the URL we use to obtain the information about a
    # Strong's Concordance number.
    url = "http://www.biblewheel.com/GR/Strongs.php?" + \
          "PStrongs={}".format(strongsNumberStr)
    
    log.debug("Obtaining gematria value for '{}' by accessing URL: {}".\
              format(strongsNumberStr, url))
    
    opener = urllib.request.build_opener()
    request = urllib.request.Request(url)

    log.debug("Opening HTTP request.")
    response = opener.open(request)

    log.debug("Reading HTTP response.")
    data = response.read().decode()

    log.debug("Processing HTML page ...")

    log.debug(" Data length is: {}".format(len(data)))
    log.debug(" Data read from {} is: ***{}***".format(url, data))
    
    # Get the location where the string 'Gematria:' is found.
    startSearchStr = "Gematria:"
    startLoc = data.find(startSearchStr)
    
    log.debug("startLoc == {}".format(startLoc))

    if startLoc == -1:
        log.error("Could not find a Gematria value for '{}' because " + \
                  "'Gematria:' could not be found in the HTML.")
        log.error("The HTML received was: " + os.linesep + "{}".format(data))
        return None
    
    # Get the location where the next opening tag '<' is.
    endSearchStr = "<"
    endLoc = data.find(endSearchStr, startLoc)
    
    if endLoc == -1:
        log.error("Could not find a Gematria value for '{}' because " + \
                  "an expected following '<' could not be found in the HTML.")
        log.error("The HTML received was: " + os.linesep + "{}".format(data))
        return None
    

    # Extract the gematria value.
    startPos = startLoc + len(startSearchStr)
    endPos = endLoc
    gematriaValueStr = data[startPos:endPos].strip()

    log.debug("Gematria value in str format is: {}".format(gematriaValueStr))

    if not gematriaValueStr.isdigit():
        log.error("Could not find a Gematria value for '{}' because the "
                  "gematria value in str format is not a number.  " + \
                  "The str being analyzed is: {}".format(gematriaValueStr))
        return None

    gematriaValue = int(gematriaValueStr)
    log.debug("Gematria value in int format is: {}".format(gematriaValue))

    return gematriaValue


def getDictionaryOfGreekStrongsConcordanceNumbersToGematriaValues():
    """Returns a dictionary for all the Greek Strong's Concordance
    Numbers to gematria values.

    Returns:
    dict holding the greek Strong's Concordance Number string to
    gematria int values.
    """

    # Return value.
    rv = {}
    
    # The first Strong's Concordance number for the Greek is: G0001
    # The last  Strong's Concordance number for the Greek is: G5624

    firstValue = 1
    lastValue = 5624

    for i in range(firstValue, lastValue + 1):
        # Create the Strong's Concordance Number to look up.
        scn = "G" + "{:04}".format(i)

        # Obtain the Gematria value.
        gematriaValue = getGematriaValueForStrongsConcordanceNumber(scn)

        if gematriaValue != None:
            rv[scn] = gematriaValue
    
    return rv

    
def getDictionaryOfHebrewStrongsConcordanceNumbersToGematriaValues():
    """Returns a dictionary for all the Hebrew Strong's Concordance
    Numbers to gematria values.

    Returns:
    dict holding the greek Strong's Concordance Number string to
    gematria int values.
    """

    # Return value.
    rv = {}
    
    # The first Strong's Concordance number for the Hebrew is: H0001
    # The last  Strong's Concordance number for the Hebrew is: H8674
    
    firstValue = 1
    lastValue = 8674

    for i in range(firstValue, lastValue + 1):
        # Create the Strong's Concordance Number to look up.
        scn = "H" + "{:04}".format(i)

        # Obtain the Gematria value.
        gematriaValue = getGematriaValueForStrongsConcordanceNumber(scn)
    
        if gematriaValue != None:
            rv[scn] = gematriaValue
    
    return rv

##############################################################################

if __name__ == "__main__":

    # Greek.
    log.info("Obtaining Greek gematria values ...")
    dictOfGreekGematriaValues = \
        getDictionaryOfGreekStrongsConcordanceNumbersToGematriaValues()
    
    # Hebrew.
    log.info("Obtaining Hebrew gematria values ...")
    dictOfHebrewGematriaValues = \
        getDictionaryOfHebrewStrongsConcordanceNumbersToGematriaValues()

    # Write to file, truncating if it already exists.
    log.info("Writing to output file '{}' ...".format(outputFilename))

    with open(outputFilename, "w") as f:

        # Write the header line.
        f.write(headerLine + newline)
        
        # Write to file as a CSV.
        for k, v, in sorted(dictOfGreekGematriaValues.items(),
                            key=lambda x: x[0]):
            f.write(k + "," + "{}".format(v) + newline)
            
        for k, v, in sorted(dictOfHebrewGematriaValues.items(),
                            key=lambda x: x[0]):
            f.write(k + "," + "{}".format(v) + newline)
        
    log.info("Done.")
    shutdown(0)

##############################################################################
