

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
from data_objects import BirthInfo
from data_objects import DefaultSettingsFactory
from data_objects import PriceBar
from data_objects import PriceBarChartBarCountArtifact
from data_objects import PriceBarChartGannFanUpperRightArtifact
from data_objects import PriceBarChartGannFanLowerRightArtifact
from data_objects import PriceBarChartSettings
from data_objects import PriceBarChartTextArtifact


class PriceBarChartWidget(QWidget):
    """Widget holding the QGraphicsScene and QGraphicsView that displays
    the PriceBar information along with other indicators and analysis
    tools.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarChartWidget")

        # Create the contents.
        self.priceBarChartSettings = PriceBarChartSettings()
        
        # These are the label widgets at the top of the PriceBarChartWidget.
        self.descriptionLabel = QLabel("")
        
        self.firstPriceBarTimestampLabel = QLabel("")
        self.lastPriceBarTimestampLabel = QLabel("")
        
        self.selectedPriceBarTimestampLabel = QLabel("")
        
        self.selectedPriceBarOpenPriceLabel = QLabel("")
        self.selectedPriceBarHighPriceLabel = QLabel("")
        self.selectedPriceBarLowPriceLabel = QLabel("")
        self.selectedPriceBarClosePriceLabel = QLabel("")
        
        # These labels will have smaller font.
        smallFont = QFont()
        smallFont.setPointSize(6)
        self.firstPriceBarTimestampLabel.setFont(smallFont)
        self.lastPriceBarTimestampLabel.setFont(smallFont)
        self.selectedPriceBarOpenPriceLabel.setFont(smallFont)
        self.selectedPriceBarHighPriceLabel.setFont(smallFont)
        self.selectedPriceBarLowPriceLabel.setFont(smallFont)
        self.selectedPriceBarClosePriceLabel.setFont(smallFont)
        
        # Create the QGraphicsView and QGraphicsScene for the display portion.
        self.graphicsScene = QGraphicsScene()
        self.graphicsView = QGraphicsView()
        
        # Setup the layouts.
        dataTimeRangeLayout = QVBoxLayout()
        dataTimeRangeLayout.addWidget(self.firstPriceBarTimestampLabel)
        dataTimeRangeLayout.addWidget(self.lastPriceBarTimestampLabel)
       
        priceBarPricesLayout = QVBoxLayout()
        priceBarPricesLayout.addWidget(self.selectedPriceBarOpenPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarHighPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarLowPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarClosePriceLabel)
        
        topLabelsLayout = QHBoxLayout()
        topLabelsLayout.addWidget(self.descriptionLabel)
        topLabelsLayout.addLayout(dataTimeRangeLayout)
        topLabelsLayout.addWidget(self.selectedPriceBarTimestampLabel)
        topLabelsLayout.addLayout(priceBarPricesLayout)
        
        layout = QVBoxLayout()
        layout.addLayout(topLabelsLayout)
        layout.addWidget(self.graphicsView)
        self.setLayout(layout)

    def loadPriceBars(self, priceBars):
        """Loads the given PriceBars list into this widget as
        PriceBarGraphicsItems.
        """
    
        # TODO:  write this part.
        pass

    def loadArtifacts(self, priceBarChartArtifact):
        """Loads the given list of PriceBarChartArtifact objects 
        into this widget as QGraphicsItems."""
        
        # TODO:  write this part.
        pass
        
        
    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the settings in the given PriceBarChartSettings object.
        """
        
        self.priceBarChartSettings = priceBarChartSettings
        
        # TODO:  add code here for selected bar, scaling, etc. 
        
    
    def getPriceBarChartSettings(self):
        """Returns the current settings used in this PriceBarChartWidget."""
        
        return self.priceBarChartSettings

class PriceBarGraphicsItem(QGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar object."""
    
    def __init__(self, parent=None, scene=None, priceBar=None):
        # TODO:  write this function.
        self.priceBar = priceBar
    
class TextGraphicsItem(QGraphicsTextItem):
    """QGraphicsItem that visualizes a PriceBarChartTextArtifact."""
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
    def setPriceBarChartTextArtifact(self, priceBarChartTextArtifact):
        """Loads a given PriceBarChartTextArtifact object's data
        into this QGraphicsTextItem.
        """
        
        self.priceBarChartTextArtifact = priceBarChartTextArtifact
        
        # TODO:  Extract and set the internals according to the info 
        # in priceBarChartTextArtifact.
    
    def getPriceBarChartTextArtifact(self):
        """Returns a PriceBarChartTextArtifact for this QGraphicsItem 
        so that it may be pickled.
        """
        
        # TODO:  Update the internal self.priceBarChartTextArtifact to be 
        # current, then return it.
        
        return self.priceBarChartTextArtifact

class GannFanUpperRightGraphicsItem(QGraphicsItem):
    """QGraphicsItem that visualizes a GannFan opening in the upper 
    right direction.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
    def setPriceBarChartGannFanUpperRightArtifact(self, priceBarChartGannFanUpperRightArtifact):
        """Loads a given PriceBarChartGannFanUpperRightArtifact object's data
        into this QGraphicsItem.
        """
        
        self.priceBarChartGannFanUpperRightArtifact = \
            priceBarChartGannFanUpperRightArtifact
            
        # TODO:  Extract and set the internals according to the info 
        # in this artifact object.
    
    def getPriceBarChartTextArtifact(self):
        """Returns a PriceBarChartTextArtifact for this QGraphicsItem 
        so that it may be pickled.
        """
        
        # TODO:  Update the internal self.priceBarChartGannFanUpperRightArtifact 
        # to be current, then return it.
        
        return self.priceBarChartGannFanUpperRightArtifact 
        
class GannFanLowerRightGraphicsItem(QGraphicsItem):
    """QGraphicsItem that visualizes a GannFan opening in the lower 
    right direction.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
    def setPriceBarChartGannFanLowerRightArtifact(self, priceBarChartGannFanLowerRightArtifact):
        """Loads a given PriceBarChartGannFanLowerRightArtifact object's data
        into this QGraphicsItem.
        """
        
        self.priceBarChartGannFanLowerRightArtifact = \
            priceBarChartGannFanLowerRightArtifact
            
        # TODO:  Extract and set the internals according to the info 
        # in this artifact object.
    
    def getPriceBarChartTextArtifact(self):
        """Returns a PriceBarChartTextArtifact for this QGraphicsItem 
        so that it may be pickled.
        """
        
        # TODO:  Update the internal self.priceBarChartGannFanLowerRightArtifact 
        # to be current, then return it.
        
        return self.priceBarChartGannFanLowerRightArtifact 
        
class BarCountGraphicsItem(QGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar counter in the GraphicsView.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
    def setPriceBarChartBarCountArtifact(self, priceBarChartBarCountArtifact):
        """Loads a given PriceBarChartBarCountArtifact object's data
        into this QGraphicsItem.
        """
        
        self.priceBarChartBarCountArtifact = \
            priceBarChartBarCountArtifact 
            
        # TODO:  Extract and set the internals according to the info 
        # in this artifact object.
    
    def setPriceBarChartBarCountArtifact(self):
        """Returns a PriceBarChartBarCountArtifact for this QGraphicsItem 
        so that it may be pickled.
        """
        
        # TODO:  Update the internal self.priceBarChartBarCountArtifact 
        # to be current, then return it.
        
        return self.priceBarChartBarCountArtifact



