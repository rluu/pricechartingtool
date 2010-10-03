

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




class PriceBarSpreadsheetWidget(QWidget):
    """Widget holding the QTableView that displays the PriceBar 
    information along with other metrics analysis information.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("pricebarspreadsheet.PriceBarSpreadsheetWidget")

        # Create the contents.
        label = QLabel("dummy label")

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


