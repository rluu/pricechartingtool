
import sys
import os

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
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene

class SwingFileData(object):
    """Contains information about a set of swing pivots for a certain
    trading entity.
    """
    
    def __init__(self):
        # Description of the trading entity, extracted from the PCD file.
        self.tradingEntityDescription = ""

        # Text describing the parameters used in extracting the swing
        # pivots.  This includes time range the pivots were extracted
        # from, as well as what constitutes a short-term high versus a
        # intermediate-term high, etc.
        self.swingFileDescription = ""
        
        # Filename that holds the source PCD file the data was extracted from.
        # This is blank if a PCD file was not used to derive the data.
        self.sourcePcdFilename = ""
        
        # Filename that holds the original source of the pricebar data.
        # Usually this is a CSV text file.
        self.sourcePriceBarDataFilename = ""

        # BirthInfo object for natal birth information.
        self.birthInfo = BirthInfo()
        
        # List of PriceBar objects that represent the swings, sorted
        # by timestamp.  This pricebars have their tags set according
        # to certains strings, according to whether the PriceBar is a
        # high or a low.  For example:
        # H, HH, HHH, L, LL, LLL, etc.
        #
        self.priceBars = []
        
        # Configuration for the timezone used.  
        # This is the pytz.timezone object that is a subclass of 
        # datetime.tzinfo.
        self.locationTimezone = pytz.utc
        
        # Notes text extracted from the source PCD file.
        self.userNotes = ""

    def loadPriceChartDocumentData(self, pcdFile, pcdd):
        """Extracts the relevant data we care about from the given
        PriceChartDocumentData file.

        Arguments:
        pcdFile - str object holding the path to the PCD file.
        pcdd    - PriceChartDocumentData object from which to
                  extract information from for our data fields.
        """
        
        self.tradingEntityDescription = pcdd.description
        self.swingFileDescription = "PriceBars have not been tagged."
        self.sourcePcdFilename = pcdFile
        self.sourcePriceBarDataFilename = pcdd.priceBarsFileFilename
        self.birthInfo = pcdd.birthInfo
        self.priceBars = pcdd.priceBars
        self.locationTimezone = pcdd.locationTimezone
        self.userNotes = pcdd.userNotes
        
    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        return rv
        
    def __str__(self):
        """Returns the string representation of most of the attributes in this
        PriceChartDocumentData object.
        """
        
        return self.toString()
    
