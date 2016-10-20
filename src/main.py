#!/usr/bin/env python3

# For obtaining current directory path information, and creating directories
import os
import sys

# For parsing command-line options
from optparse import OptionParser

# For logging.
import logging
import logging.handlers
import logging.config

# For loading shelves.
import shelve

# Import PyQt classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import from this project.
from ui import MainWindow

# To initialize and shutdown the Ephemeris.
from ephemeris import *

# To initialize the ephemeris calculations caches
# with previously computed results.
from lunar_calendar_utils import LunarCalendarUtils

# Import resources for the icon image.
import resources

##############################################################################

__version__ = "2.2.0"
__date__ = "Sat Feb 27 16:41:03 EST 2016"


# Application Name
APP_NAME = "PriceChartingTool"

# Application Version obtained from subversion revision.
APP_VERSION = __version__

# Application Date obtain from last subversion commit date.
APP_DATE = __date__

# Location of the source directory, based on this main.py file.
SRC_DIR = os.path.abspath(sys.path[0])

# Location of the shelved cache file.
SHELVED_CACHE_FILE = \
        os.path.abspath(os.path.join(SRC_DIR,
                                    ".." + os.sep +
                                    "data" + os.sep +
                                    "cache" + os.sep +
                                    "cache.shelve"))

# Directory where log files will be written.
LOG_DIR = \
    os.path.abspath(os.path.join(SRC_DIR,
                                 ".." + os.sep + "logs"))

# Location of the config file for logging.
LOG_CONFIG_FILE = \
    os.path.abspath(os.path.join(SRC_DIR,
                                 ".." + os.sep +
                                 "conf" + os.sep +
                                 "logging.conf"))

# Application author
APP_AUTHOR = "Ryan Luu"

# Application author's email address.
APP_AUTHOR_EMAIL = "ryanluu@gmail.com"

# Profiler enabled flag.
# Change this flag to turn on profiling.
#
# Note: When profiling is turned on, the output is printed to
# stdout at the time Python exits, so make sure you redirect stdout
# to a file if you want to analyze it!
#
# Also, to look at the output, pipe to sort like as follows:
#
#  cat /tmp/profilerOutput.txt | sort -k1 -r -n | less
#
# Where -k1 says to sort by the first field.  Change the number to
# sort by other fields.
# Where -r says to reverse results (sort by highest to lowest).
# Where -n says to sort numerically, instead of by text values.
#
turnOnProfiler = False

##############################################################################

def main():
    """Creates and runs the PriceChartingTool application."""

    # Parse command-line arguments.
    (options, args) = parseCommandlineArgs()

    # Set up the logger.

    # Parsing the log config file doesn't work on the current version
    # of cx_Freeze (on Windows and on Mac).  The author of cx_Freeze
    # knows about this bug and hopefully the next release of cx_Freeze
    # addresses this issue.  Until then, only parse the config file if
    # this file is referenced as a .py file.
    if sys.argv[0].split(".")[-1] == "py":
        logging.config.fileConfig(LOG_CONFIG_FILE)
    log = logging.getLogger("main")

    log.info("##########################################");
    log.info("# Starting " + sys.argv[0] + ", version " + APP_VERSION);
    log.info("##########################################");

    # Create the Qt application.
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(":/images/rluu/appIcon.png"))

    # Turn off UIEffects so that the application runs faster when doing
    # X11 forwarding.
    app.setEffectEnabled(Qt.UI_AnimateMenu, False)
    app.setEffectEnabled(Qt.UI_FadeMenu, False)
    app.setEffectEnabled(Qt.UI_AnimateCombo, False)
    app.setEffectEnabled(Qt.UI_AnimateTooltip, False)
    app.setEffectEnabled(Qt.UI_FadeTooltip, False)
    app.setEffectEnabled(Qt.UI_AnimateToolBox, False)

    # Initialize the Ephemeris.
    Ephemeris.initialize()

    # Set a default location (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Load any shelved caches.
    loadCachesFromShelve()

    # Create the main window for the app and show it.
    mainWindow = MainWindow(APP_NAME,
                            APP_VERSION,
                            APP_DATE,
                            APP_AUTHOR,
                            APP_AUTHOR_EMAIL)
    mainWindow.show()

    # Cleanup and close the application when the last window is closed.
    app.lastWindowClosed.connect(Ephemeris.closeEphemeris)
    app.lastWindowClosed.connect(saveCachesToShelve)
    app.lastWindowClosed.connect(logging.shutdown)
    app.lastWindowClosed.connect(app.quit)

    return app.exec_()


def parseCommandlineArgs():
    """Parses the arguments specified on the command-line.
    Returns (options, args) for the options and arguments passed"""

    # Create the parser
    parser = OptionParser()

    # Specify all valid options.
    parser.add_option("-v", "--version",
                      action="store_true",
                      dest="version",
                      default=False,
                      help="Display application version info and author " + \
                      "contact.")

    # Parse the arguments into options.
    global options
    (options, args) = parser.parse_args()

    # Print version information if the flag was used.
    if (options.version == True):
        print(APP_NAME + " (Version " + APP_VERSION + ")")
        print("By " + APP_AUTHOR + ", " + APP_AUTHOR_EMAIL)
        sys.exit(0)

    return (options, args)


def loadCachesFromShelve():
    """
    Loads previously used caches that were shelved to a file,
    back into the caches.

    This is so we don't have to re-populate the caches all over again
    with calculations that should be the same from run to run.
    """

    log = logging.getLogger("main")

    if not os.path.isfile(SHELVED_CACHE_FILE):
        log.info("Shelve file '" + SHELVED_CACHE_FILE +
                 "' does not exist or it is not a file.  " +
                 "Will skip loading caches from shelve.")

    else:
        # Shelve exists.  Open it.
        log.info("Shelve file '" + SHELVED_CACHE_FILE + "' exists.  " +
                 "Attempting to open ...")
        cacheDict = shelve.open(SHELVED_CACHE_FILE)
        log.info("Shelve file opened for loading: " + SHELVED_CACHE_FILE)

        # Retrieve a copy of each of the caches, and store them
        # for use in the application.
        key = "LunarCalendarUtils.datetimeToLunarDateCache"
        if key in cacheDict:
            cache = cacheDict[key]
            LunarCalendarUtils.datetimeToLunarDateCache = cache
            log.info("Loaded cache '" + key + "' with currsize " +
                "{} from shelve.".format(cache.currsize))
        else:
            log.info("Cache '" + key + "' not found in the shelve.")

        key = "LunarCalendarUtils.getNisan1DatetimeForYearCache"
        if key in cacheDict:
            cache = cacheDict[key]
            LunarCalendarUtils.getNisan1DatetimeForYearCache = cache
            log.info("Loaded cache '" + key + "' with currsize " +
                "{} from shelve.".format(cache.currsize))
        else:
            log.info("Cache '" + key + "' not found in the shelve.")

        key = "LunarCalendarUtils.lunarDateToDatetimeCache"
        if key in cacheDict:
            cache = cacheDict[key]
            LunarCalendarUtils.lunarDateToDatetimeCache = cache
            log.info("Loaded cache '" + key + "' with currsize " +
                "{} from shelve.".format(cache.currsize))
        else:
            log.info("Cache '" + key + "' not found in the shelve.")

        key = "LunarCalendarUtils.isLunarLeapYearCache"
        if key in cacheDict:
            cache = cacheDict[key]
            LunarCalendarUtils.isLunarLeapYearCache = cache
            log.info("Loaded cache '" + key + "' with currsize " +
                "{} from shelve.".format(cache.currsize))
        else:
            log.info("Cache '" + key + "' not found in the shelve.")

        cacheDict.close()


def saveCachesToShelve():
    """
    Store each of the caches we want to persist into the shelve for use
    the next time we open the application.
    """

    log = logging.getLogger("main")

    log.info("Attempting to open shelve file '" + SHELVED_CACHE_FILE +
              "' for saving ...")
    cacheDict = shelve.open(SHELVED_CACHE_FILE)
    log.info("Shelve file opened for saving: " + SHELVED_CACHE_FILE)


    key = "LunarCalendarUtils.datetimeToLunarDateCache"
    cache = LunarCalendarUtils.datetimeToLunarDateCache
    log.info("Saving cache '" + key + "' with currsize " +
              "{} to shelve ...".format(cache.currsize))
    cacheDict[key] = cache

    key = "LunarCalendarUtils.getNisan1DatetimeForYearCache"
    cache = LunarCalendarUtils.getNisan1DatetimeForYearCache
    log.info("Saving cache '" + key + "' with currsize " +
              "{} to shelve ...".format(cache.currsize))
    cacheDict[key] = cache

    key = "LunarCalendarUtils.lunarDateToDatetimeCache"
    cache = LunarCalendarUtils.lunarDateToDatetimeCache
    log.info("Saving cache '" + key + "' with currsize " +
              "{} to shelve ...".format(cache.currsize))
    cacheDict[key] = cache

    key = "LunarCalendarUtils.isLunarLeapYearCache"
    cache = LunarCalendarUtils.isLunarLeapYearCache
    log.info("Saving cache '" + key + "' with currsize " +
              "{} to shelve ...".format(cache.currsize))
    cacheDict[key] = cache


    log.info("Closing shelve ...")
    cacheDict.close()
    log.info("Shelve closed.")


##############################################################################

if __name__ == "__main__":

    # Program return code.
    exitCode = 0

    if turnOnProfiler == True:
        import cProfile
        cProfile.run("main()")
    else:
        exitCode = main()

    sys.exit(exitCode)

##############################################################################
