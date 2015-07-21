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

# Import PyQt classes.
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Import from this project.
from ui import MainWindow

# To initialize and shutdown the Ephemeris.
from ephemeris import *

# Import resources for the icon image.
import resources

##############################################################################

__version__ = "2.0.0"
__date__ = "Wed Mar 18 17:49:18 EDT 2015"


# Application Name
APP_NAME = "PriceChartingTool"

# Application Version obtained from subversion revision.
APP_VERSION = __version__

# Application Date obtain from last subversion commit date.
APP_DATE = __date__

# Location of the source directory, based on this main.py file.
SRC_DIR = os.path.abspath(sys.path[0])

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
    
    # Create the main window for the app and show it.
    mainWindow = MainWindow(APP_NAME, 
                            APP_VERSION, 
                            APP_DATE, 
                            APP_AUTHOR, 
                            APP_AUTHOR_EMAIL)
    mainWindow.show()

    # Cleanup and close the application when the last window is closed.
    app.lastWindowClosed.connect(Ephemeris.closeEphemeris)
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
