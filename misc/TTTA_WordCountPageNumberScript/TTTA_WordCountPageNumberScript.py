#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Script to search for word-phrase counts and page numbers that the
#   word-phrase shows up on in TTTA.  The phrase searched is case-insensitive.
#
# Usage:
#
#     ./TTTA_WordCountPageNumberScript.py --help
#     ./TTTA_WordCountPageNumberScript.py --version
#
#     ./TTTA_WordCountPageNumberScript.py --input-file=../../doc/TTTA_paragraph_unfilled.txt --word="sleeping gas"
# 
# Note:
#
#   The algorithm used in this script assumes that there is a page
#   break after the last page of the actual document.
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

# For math.floor()
import math

##############################################################################

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Input file.
# This value is obtained via command-line arguments.
inputFile = None

# Search word phrase.
# This value is obtained via command-line arguments.
word = None

# For logging.
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    logging.shutdown()
    
    sys.exit(rc)

##############################################################################

# Create the parser
parser = OptionParser()

# Specify all valid options.
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  default=False,
                  help="Display script version info and author contact.")
    
parser.add_option("--input-file",
                  action="store",
                  type="str",
                  dest="inputFile",
                  default=None,
                  help=\
                  "Specify the input text file of TTTA.",
                  metavar="<FILE>")

parser.add_option("--word",
                  action="store",
                  type="str",
                  dest="word",
                  default=None,
                  help="Specify word phrase to search for.  Use double-quotes for more than one word.  This field is case-insensitive.",
                  metavar="<STRING>")

# Parse the arguments into options.
(options, args) = parser.parse_args()

# Print version information if the flag was used.
if options.version == True:
    print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
    print("By Ryan Luu, ryanluu@gmail.com")
    shutdown(0)

if options.inputFile == None:
    log.error("Please specify an input filename to the " + \
              "--input-file option.")
    shutdown(1)
else:
    inputFile = options.inputFile

if options.word == None:
    log.error("Please specify a search word phrase to the " + \
              "--word option.")
    shutdown(1)
else:
    word = options.word

##############################################################################

matchedWordCount = 0
matchedWordPageNumberStrs = []
dictOfMatchesPerPage = {}

# Read input file.
log.info("Reading file '{}' ...".format(inputFile))
with open(inputFile) as f:
    currPageStr = ""
    currPageMatchCount = 0
    newPageMarker = ""
    wordLowered = word.lower()

    # Note: This algorithm assumes that there is a page break after
    # the last page of the actual document.
    
    for line in f:
        if line.startswith(newPageMarker):
            
            # If there are a page match previously, then
            # add the matched word count to the running total.
            if currPageMatchCount > 0 and currPageStr != "":
                log.debug("Page {} had {} matches.".\
                          format(currPageStr, currPageMatchCount))
                
                matchedWordCount += currPageMatchCount
                matchedWordPageNumberStrs.append(currPageStr)
                dictOfMatchesPerPage[currPageStr] = currPageMatchCount
            
            # Reset the stored values for a page (page str and match count).
            loc = line.find(newPageMarker)
            currPageStr = line[loc:].strip()
            currPageMatchCount = 0
            log.debug("New page: {} ...".format(currPageStr))

        # Get the lower-case version of the line.
        lineLowered = line.lower()

        # Count how many matches are in on this line.
        lineMatchCount = lineLowered.count(wordLowered)

        # If there are matches, add them to the count for this page.
        if lineMatchCount > 0:
            log.debug("Line has {} matches.".format(lineMatchCount))
            currPageMatchCount += lineMatchCount
        

log.info("Search phrase (case-insensitive): \"{}\"".format(word))
log.info("Matches:")
for page in matchedWordPageNumberStrs:
    log.info("Page {:>3}: {:>3} matches.".\
             format(page, dictOfMatchesPerPage[page]))
log.info("Total match count: {}".format(matchedWordCount))

log.info("Done.")
shutdown(0)

