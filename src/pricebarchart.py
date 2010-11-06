

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
        self.log.debug("Entered __init__()")

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
        self.graphicsScene = PriceBarChartGraphicsScene()
        self.graphicsView = PriceBarChartGraphicsView()
        self.graphicsView.setScene(self.graphicsScene)
        
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

        self.graphicsView.show()

        self.log.debug("Leaving __init__()")

    def loadDayPriceBars(self, priceBars):
        """Loads the given PriceBars list into this widget as
        PriceBarGraphicsItems.
        """
        
        self.log.debug("Entered loadDayPriceBars({} pricebars)".\
                       format(len(priceBars)))

        for priceBar in priceBars:

            # Create the QGraphicsItem
            item = DayPriceBarGraphicsItem()
            item.setPriceBar(priceBar)

            # X location will be the proleptic Gregorian ordinal
            # of the date of the PriceBar.
            ordinateDate = priceBar.timestamp.toordinal()
            x = ordinateDate

            # Y location will be the mid price of the bar.
            y = priceBar.midPrice()

            # Set the position, in parent coordinates.
            item.setPos(QPointF(x, y))

            # Add the item.
            self.graphicsScene.addItem(item)

        self.log.debug("Leaving loadDayPriceBars({} pricebars)".\
                       format(len(priceBars)))

    def loadWeekPriceBars(self, priceBars):
        """Loads the given PriceBars list into this widget as
        PriceBarGraphicsItems.
        """
        
        self.log.debug("Entered loadWeekPriceBars({} pricebars)".\
                       format(len(priceBars)))
        
        for priceBar in priceBars:

            # Create the QGraphicsItem
            item = WeekPriceBarGraphicsItem()
            item.setScene(self.graphicsScene)
            item.setPriceBar(priceBar)

            # X location will be the proleptic Gregorian ordinal
            # of the date of the PriceBar.
            ordinateDate = priceBar.timestamp.toordinal()
            x = ordinateDate

            # Y location will be the mid price of the bar.
            y = priceBar.midPrice()

            # Set the position, in parent coordinates.
            item.setPos(QPointF(x, y))

            # Add the item.
            self.graphicsScene.addItem(item)

        self.log.debug("Leaving loadWeekPriceBars({} pricebars)".\
                       format(len(priceBars)))

    def clearAllPriceBars(self):
        """Clears all the PriceBar QGraphicsItems from the 
        QGraphicsScene."""

        # Get all the QGraphicsItems.
        graphicsItems = self.graphicsScene.items()

        # Only remove the PriceBarGraphicsItem items.
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                self.graphicsScene.removeItem(item)


    def loadArtifacts(self, priceBarChartArtifacts):
        """Loads the given list of PriceBarChartArtifact objects 
        into this widget as QGraphicsItems."""
        
        # TODO:  write this part.
        pass
        
    def addArtifact(self, priceBarChartArtifact):
        """Adds the given PriceBarChartArtifact objects 
        into this widget as QGraphicsItems."""
        
        # TODO:  write this part.
        pass
        
    def clearAllArtifacts(self):
        """Clears all the artifact QGraphicsItems from the 
        QGraphicsScene."""

        # TODO:  write this part.
        pass
        
        
    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the settings in the given PriceBarChartSettings object.
        """
        
        self.priceBarChartSettings = priceBarChartSettings
        
        # TODO:  add code here to set all the settings (scaling, etc. )
        
    
    def getPriceBarChartSettings(self):
        """Returns the current settings used in this PriceBarChartWidget."""
        
        return self.priceBarChartSettings

class PriceBarChartGraphicsScene(QGraphicsScene):
    """QGraphicsScene holding all the pricebars and artifacts.
    We subclass the QGraphicsScene to allow for future feature additions.
    """

    def __init__(self, parent=None):
        """Pass-through to the QGraphicsView constructor."""

        super().__init__(parent)
    

class PriceBarChartGraphicsView(QGraphicsView):
    """QGraphicsView that visualizes the main QGraphicsScene.
    We subclass the QGraphicsView because we may want to add 
    custom syncrhonized functionality in other widgets later."""


    def __init__(self, parent=None):
        """Pass-through to the QGraphicsView constructor."""

        super().__init__(parent)
    



class PriceBarGraphicsItem(QGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar object.

    There exists two kinds of standard PriceBar drawings:
        - Candle
        - Bar with open and close

    This class draws the second one.  It is displayed as a bar with open
    and close ticks on the left and right side.  The bar is drawn with a
    green pen if the high is higher than or equal the low, and drawn as
    red otherwise.
    """
    
    def __init__(self, parent=None, scene=None):
        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarGraphicsItem")
        self.log.debug("Entered __init__().")

        super().__init__(parent, scene)

        # Pen width for standard PriceBars (not highlighted or not bold)
        self.penWidth = 1.0

        # Pen width for use on highlighted (bold) PriceBars.
        self.boldPenWidth = 2.0

        # Width of the left extension drawn that represents the open price.
        self.leftExtensionWidth = 1.0

        # Width of the stem drawn that represents the price range.
        self.stemWidth = 1.0

        # Width of the right extension drawn that represents the close price.
        self.rightExtensionWidth = 1.0

        # Internally stored PriceBar.
        self.priceBar = None

        # Pen which is used to do the painting.
        self.pen = QPen()
        self.pen.setColor(QColor(Qt.black))
        self.pen.setWidthF(self.penWidth)

        # Flag for bold (highlighted) PriceBar.
        self.bolded = False

        self.log.debug("Leaving __init__().")

    def setPriceBar(self, priceBar):
        """Sets the internally used priceBar.  
        This has an effect on the color of the pricebar.
        """

        self.log.debug("Entered setPriceBar().  priceBar={}".\
                       format(priceBar.toString()))

        self.priceBar = priceBar

        # Set if it is a green or red pricebar.
        if self.priceBar != None:
            if self.priceBar.open <= self.priceBar.close:
                self.setPriceBarColor(Qt.green)
            else:
                self.setPriceBarColor(Qt.red)
        else:
            # PriceBar is None.  Just use a black bar.
            self.setPriceBarColor(Qt.black)

        self.setBolded(False)

        
        # Schedule an update to redraw the QGraphicsItem.
        self.update()

        self.log.debug("Leaving setPriceBar().")

    def setPriceBarColor(self, color):
        """Sets the color of the price bar."""

        self.log.debug("Entered setPriceBarColor().")

        if self.pen.color() != color:
            self.log.debug("Updating pen color.")
            self.pen.setColor(color)
            self.update()

        self.log.debug("Leaving setPriceBarColor().")

    def setBolded(self, bolded):
        """Sets whether or not the PriceBar is displayed as bolded. 
        This means it is highlighted in some way and has a thicker pen.

        Arguments: 

        bolded - bool, True if the PriceBar should be bold (highlighted),
        False, if it should be drawn regularly.
        """

        self.log.debug("Entered setBolded({}).".format(bolded))

        # Only update if the new value is different from the current
        # value.
        if self.bolded != bolded:
            self.bolded = bolded

            if self.bolded:
                self.pen.setWidthF(self.boldPenWidth)
            else:
                self.pen.setWidthF(self.penWidth)
            
            # Schedule a redraw.
            self.update()

        self.log.debug("Leaving setBolded().")

    def getPriceBarHighScenePoint(self):
        """Returns the scene coordinates of the high point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the high of this
        pricebar is.
        """

        self.log.debug("Entered getPriceBarHighScenePoint().")

        high = 0.0
        low = 0.0

        if self.priceBar != None:
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) / 2.0

        x = 0.0
        yHigh = high - priceMidpoint
        yLow = low - priceMidpoint

        # Return value.
        rv = self.mapToScene(QPointF(x, yHigh))

        self.log.debug("Leaving getPriceBarHighScenePoint().")

        return rv


    def getPriceBarLowScenePoint(self):
        """Returns the scene coordinates of the low point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the high of this
        pricebar is.
        """

        self.log.debug("Entered getPriceBarLowScenePoint().")

        high = 0.0
        low = 0.0

        if self.priceBar != None:
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) / 2.0

        x = 0.0
        yHigh = high - priceMidpoint
        yLow = low - priceMidpoint

        # Return value.
        rv = self.mapToScene(QPointF(x, yLow))

        self.log.debug("Leaving getPriceBarLowScenePoint().")

        return rv

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        self.log.debug("Entered boundingRect().")

        # Coordinates (0, 0) is the center of the widget.  
        # The QRectF returned should be related to this point as the
        # center.

        halfPenWidth = self.boldPenWidth / 2.0

        open = 0.0
        high = 0.0
        low = 0.0
        close = 0.0

        if self.priceBar != None:
            open = self.priceBar.open
            high = self.priceBar.high
            low = self.priceBar.low
            close = self.priceBar.close

        # For X we have:
        #     leftExtensionWidth units for the left extension (open price)
        #     stemWidth units for the stem (price range)
        #     rightExtensionWidth units for the right extension (close price)
        #     halfPenWidth on the left side
        #     halfPenWidth on the right side

        # For Y we have:
        #     halfPenWidth for the bottom side.
        #     priceRange units
        #     halfPenWidth for the top side

        priceRange = high - low

        x = -1 * (self.leftExtensionWidth + halfPenWidth)
        y = -1 * ((priceRange / 2.0) + halfPenWidth)

        height = halfPenWidth + priceRange + halfPenWidth

        width = \
                halfPenWidth + \
                self.leftExtensionWidth + \
                self.stemWidth + \
                self.rightExtensionWidth + \
                halfPenWidth

        self.log.debug("Leaving boundingRect().")
        return QRectF(x, y, height, width)

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        self.log.debug("Entered paint()")

        if painter.pen() != self.pen:
            painter.setPen(self.pen)

        open = 0.0
        high = 0.0
        low = 0.0
        close = 0.0

        if self.priceBar != None:
            open = self.priceBar.open
            high = self.priceBar.high
            low = self.priceBar.low
            close = self.priceBar.close

        priceRange = high - low

        priceMidpoint = (high + low) / 2.0

        # Draw the stem.
        x1 = 0.0
        y1 = -1.0 * (priceRange / 2.0)
        x2 = 0.0
        y2 = 1.0 * (priceRange / 2.0)
        painter.drawLine(x1, y1, x2, y2)

        # Draw the left extension (open price).
        x1 = 0.0
        y1 = high - priceMidpoint
        x2 = -1.0 * self.leftExtensionWidth
        y2 = y1
        painter.drawLine(x1, y1, x2, y2)

        # Draw the right extension (close price).
        x1 = 0.0
        y1 = low - priceMidpoint
        x2 = 1.0 * self.rightExtensionWidth
        y2 = y1
        painter.drawLine(x1, y1, x2, y2)

        self.log.debug("Leaving paint()")
    
class DayPriceBarGraphicsItem(PriceBarGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar over a Day timeframe.

    This class exists to customize internal size settings.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Pen width for standard PriceBars (not highlighted or not bold)
        self.penWidth = 1.0

        # Pen width for use on highlighted (bold) PriceBars.
        self.boldPenWidth = 2.0

        # Width of the left extension drawn that represents the open price.
        self.leftExtensionWidth = 1.0

        # Width of the stem drawn that represents the price range.
        self.stemWidth = 1.0

        # Width of the right extension drawn that represents the close price.
        self.rightExtensionWidth = 1.0

class WeekPriceBarGraphicsItem(PriceBarGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar over a Week timeframe.

    This class exists to customize internal size settings.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Pen width for standard PriceBars (not highlighted or not bold)
        self.penWidth = 7.0

        # Pen width for use on highlighted (bold) PriceBars.
        self.boldPenWidth = 14.0

        # Width of the left extension drawn that represents the open price.
        self.leftExtensionWidth = 7.0

        # Width of the stem drawn that represents the price range.
        self.stemWidth = 7.0

        # Width of the right extension drawn that represents the close price.
        self.rightExtensionWidth = 7.0




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



