

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import image resources.
import resources

# For PriceBars
from data_objects import PriceBar
from data_objects import BirthInfo
from data_objects import PriceBarSpreadsheetSettings



class PriceBarSpreadsheetWidget(QWidget):
    """Widget holding the QTableView that displays the PriceBar 
    information along with other metrics analysis information.
    """

    # TODO:  I need to determine what functionality causes the
    # 'priceChartDocumentData' types of internal info to change, and when
    # that happens emit that, so a higher-up parent can set the document
    # as 'dirty', so that the user knows to save to capture these changes.

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("pricebarspreadsheet.PriceBarSpreadsheetWidget")

        # Create the contents.
        self.priceBarSpreadsheetSettings = PriceBarSpreadsheetSettings()

        label = QLabel("dummy label")

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


    def loadPriceBars(self, priceBars):
        """Adds the given list of PriceBar objects to the 
        spreadsheet widget.  
        
        Note if you want to load a whole new set of PriceBar objects, then
        call clearAllPriceBars() first, or else you will retain all the
        old bars.
        """

        # TODO:  write this function.
        pass


    def clearAllPriceBars(self):
        """Removes all the pricebars in this spreadsheet widget."""

        # TODO:  write this function.
        pass


    # TODO:  add functions for doing stuff with tags on the PriceBar
    # objects.


    def applyPriceBarSpreadsheetSettings(self, priceBarSpreadsheetSettings): 
        """Applies the settings in the given PriceBarChartSettings object.
        """
        
        self.priceBarSpreadsheetSettings = priceBarSpreadsheetSettings
        # TODO:  add code here to set all the settings.

    def getPriceBarSpreadsheetSettings(self):
        """Returns the current settings used in this
        PriceBarSpreadsheetWidget.
        """

        return self.priceBarSpreadsheetSettings

