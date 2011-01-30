
# For line separator.
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

# Import image resources.
import resources

# For QSettings keys.
from settings import SettingsKeys

# For PriceBars and artifacts in the chart.
from data_objects import BirthInfo
from data_objects import PriceBar
from data_objects import PriceBarChartBarCountArtifact
from data_objects import PriceBarChartGannFanUpperRightArtifact
from data_objects import PriceBarChartGannFanLowerRightArtifact
from data_objects import PriceBarChartScaling
from data_objects import PriceBarChartSettings
from data_objects import PriceBarChartTextArtifact

# For conversions from julian day to datetime.datetime and vice versa.
from ephemeris import Ephemeris



class PriceBarGraphicsItem(QGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar object.

    There exists two kinds of standard PriceBar drawings:
        - Candle
        - Bar with open and close

    This draws the second one.  It is displayed as a bar with open
    and close ticks on the left and right side.  The bar is drawn with a
    green pen if the high is higher than or equal the low, and drawn as
    red otherwise.
    """
    
    def __init__(self, parent=None, scene=None):

        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarGraphicsItem")
        self.log.debug("Entered __init__().")

        super().__init__(parent, scene)

        # Pen width for PriceBars.
        self.penWidth = \
            PriceBarChartSettings.defaultPriceBarGraphicsItemPenWidth

        # Width of the left extension drawn that represents the open price.
        self.leftExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemLeftExtensionWidth 

        # Width of the right extension drawn that represents the close price.
        self.rightExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemRightExtensionWidth 


        # Internally stored PriceBar.
        self.priceBar = None

        # Pen which is used to do the painting.
        self.pen = QPen()
        self.pen.setColor(QColor(Qt.black))
        self.pen.setWidthF(self.penWidth)

        # Color setting for a PriceBar that has a higher close than open.
        self.higherPriceBarColor = \
            SettingsKeys.higherPriceBarColorSettingsDefValue

        # Color setting for a PriceBar that has a lower close than open.
        self.lowerPriceBarColor = \
            SettingsKeys.lowerPriceBarColorSettingsDefValue

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()


    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        # priceBarGraphicsItemPenWidth (float).
        self.penWidth = priceBarChartSettings.priceBarGraphicsItemPenWidth

        # priceBarGraphicsItemLeftExtensionWidth (float).
        self.leftExtensionWidth = \
            priceBarChartSettings.priceBarGraphicsItemLeftExtensionWidth

        # priceBarGraphicsItemRightExtensionWidth (float).
        self.rightExtensionWidth = \
            priceBarChartSettings.priceBarGraphicsItemRightExtensionWidth


        # Update the pen.
        self.pen.setWidthF(self.penWidth)

        # Schedule an update.
        self.update()


    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        settings = QSettings()

        # higherPriceBarColor
        key = SettingsKeys.higherPriceBarColorSettingsKey
        defaultValue = \
            SettingsKeys.higherPriceBarColorSettingsDefValue
        self.higherPriceBarColor = \
            QColor(settings.value(key, defaultValue))

        # lowerPriceBarColor
        key = SettingsKeys.lowerPriceBarColorSettingsKey
        defaultValue = \
            SettingsKeys.lowerPriceBarColorSettingsDefValue
        self.lowerPriceBarColor = \
            QColor(settings.value(key, defaultValue))


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
                self.setPriceBarColor(self.higherPriceBarColor)
            else:
                self.setPriceBarColor(self.lowerPriceBarColor)
        else:
            # PriceBar is None.  Just use a black bar.
            self.setPriceBarColor(Qt.black)

        # Schedule an update to redraw the QGraphicsItem.
        self.update()

        self.log.debug("Leaving setPriceBar().")

    def getPriceBar(self):
        """Returns the internally stored PriceBar.
        If no PriceBar was previously stored in
        this PriceBarGraphicsItem, then None is returned.
        """

        return self.priceBar
    
    def setPriceBarColor(self, color):
        """Sets the color of the price bar."""

        self.log.debug("Entered setPriceBarColor().")

        if self.pen.color() != color:
            self.log.debug("Updating pen color.")
            self.pen.setColor(color)
            self.update()

        self.log.debug("Leaving setPriceBarColor().")

    def getPriceBarHighScenePoint(self):
        """Returns the scene coordinates of the high point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the high of this
        pricebar is.
        """

        high = 0.0
        low = 0.0

        if self.priceBar != None:
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) / 2.0

        x = 0.0
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yHigh))

        return rv


    def getPriceBarLowScenePoint(self):
        """Returns the scene coordinates of the low point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the high of this
        pricebar is.
        """

        high = 0.0
        low = 0.0

        if self.priceBar != None:
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) / 2.0

        x = 0.0
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yLow))

        return rv

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinates (0, 0) is the center of the widget.  
        # The QRectF returned should be related to this point as the
        # center.

        halfPenWidth = self.penWidth / 2.0

        openPrice = 0.0
        highPrice = 0.0
        lowPrice = 0.0
        closePrice = 0.0

        if self.priceBar != None:
            openPrice = self.priceBar.open
            highPrice = self.priceBar.high
            lowPrice = self.priceBar.low
            closePrice = self.priceBar.close

        # For X we have:
        #     leftExtensionWidth units for the left extension (open price)
        #     rightExtensionWidth units for the right extension (close price)
        #     halfPenWidth on the left side
        #     halfPenWidth on the right side

        # For Y we have:
        #     halfPenWidth for the bottom side.
        #     priceRange units
        #     halfPenWidth for the top side

        priceRange = abs(highPrice - lowPrice)

        x = -1.0 * (self.leftExtensionWidth + halfPenWidth)
        y = -1.0 * ((priceRange / 2.0) + halfPenWidth)

        height = halfPenWidth + priceRange + halfPenWidth

        width = \
                halfPenWidth + \
                self.leftExtensionWidth + \
                self.rightExtensionWidth + \
                halfPenWidth

        return QRectF(x, y, width, height)

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.pen:
            painter.setPen(self.pen)

        openPrice = 0.0
        highPrice = 0.0
        lowPrice = 0.0
        closePrice = 0.0

        if self.priceBar != None:
            openPrice = self.priceBar.open
            highPrice = self.priceBar.high
            lowPrice = self.priceBar.low
            closePrice = self.priceBar.close

        priceRange = abs(highPrice - lowPrice)
        priceMidpoint = (highPrice + lowPrice) / 2.0

        # Draw the stem.
        x1 = 0.0
        y1 = 1.0 * (priceRange / 2.0)
        x2 = 0.0
        y2 = -1.0 * (priceRange / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the left extension (open price).
        x1 = 0.0
        y1 = -1.0 * (openPrice - priceMidpoint)
        x2 = -1.0 * self.leftExtensionWidth
        y2 = y1

        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the right extension (close price).
        x1 = 0.0
        y1 = -1.0 * (closePrice - priceMidpoint)
        x2 = 1.0 * self.rightExtensionWidth
        y2 = y1
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.pen.widthF() / 2.0;
            
            penWidth = 0.0

            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())

    def contextMenuEvent(self, event):
        """Overwrite the QGrpahicsItem.contextMenuEvent() function.
        This is called when a context menu is brought up on this QGraphicsItem.
        Here we bring up a popup menu and provide some options to the user.
        
        Options include:

        - Select the PriceBar (and unselect all other PriceBars).
        - Unselect the PriceBar.
        - Info dialog about this PriceBar.

        TODO:  Add other options to this context menu:
        - Open astrology chart for this PriceBar time.
        - Open Square of 9 chart for this Price.
        - ... (any other number of number charts relevant).
        
        Arguments:

        event - QGraphicsSceneContextMenuEvent object that triggered
                the call of this function.
        """

        # TODO:  add some code here
        pass
    
        
class PriceBarChartArtifactGraphicsItem(QGraphicsItem):
    """QGraphicsItem that has members to indicate and set the
    readOnly mode.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        self.readOnlyFlag = True

    def setReadOnlyFlag(self, flag):
        self.readOnlyFlag = flag

    def getReadOnlyFlag(self):
        return self.readOnlyFlag

class TextGraphicsItem(PriceBarChartArtifactGraphicsItem):
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

class GannFanUpperRightGraphicsItem(PriceBarChartArtifactGraphicsItem):
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
        
class GannFanLowerRightGraphicsItem(PriceBarChartArtifactGraphicsItem):
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
        
class BarCountGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar counter in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new BarCountGraphicsItem the position
    and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger("pricebarchart.BarCountGraphicsItem")
        self.log.debug("Entered __init__().")


        ############################################################
        # Set default values for preferences/settings.
        
        # Color of the bar count graphicsitems.
        self.barCountGraphicsItemColor = \
            SettingsKeys.barCountGraphicsItemColorSettingsDefValue

        # Color of the text that is associated with the bar count
        # graphicsitem.
        self.barCountGraphicsItemTextColor = \
            SettingsKeys.barCountGraphicsItemTextColorSettingsDefValue

        # Height of the vertical bar drawn.
        self.barCountGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.barCountFontSize = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemFontSize 

        # X scaling of the text.
        self.barCountTextXScaling = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.barCountTextYScaling = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextYScaling 

        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.priceBarChartBarCountArtifact = \
            PriceBarChartBarCountArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.barCountPenWidth = 0.0
        self.barCountPen = QPen()
        self.barCountPen.setColor(self.barCountGraphicsItemColor)
        self.barCountPen.setWidthF(self.barCountPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Number of PriceBars between self.startPointF and self.endPointF.
        self.barCount = 0

        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.barCountText = QGraphicsSimpleTextItem("", self)
        self.barCountText.setPos(self.endPointF)

        # Set the font of the text.
        self.barCountTextFont = QFont()
        self.barCountTextFont.setPointSizeF(self.barCountFontSize)
        self.barCountText.setFont(self.barCountTextFont)

        # Set the pen color of the text.
        self.barCountTextPen = self.barCountText.pen()
        self.barCountTextPen.setColor(self.barCountGraphicsItemTextColor)
        self.barCountText.setPen(self.barCountTextPen)

        # Set the brush color of the text.
        self.barCountTextBrush = self.barCountText.brush()
        self.barCountTextBrush.setColor(self.barCountGraphicsItemTextColor)
        self.barCountText.setBrush(self.barCountTextBrush)

        # Apply some size scaling to the text.
        textTransform = QTransform()
        textTransform.scale(self.barCountTextXScaling, \
                            self.barCountTextYScaling)
        self.barCountText.setTransform(textTransform)

        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False

    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.barCountGraphicsItemBarHeight = \
            priceBarChartSettings.\
                barCountGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.barCountFontSize = \
            priceBarChartSettings.\
                barCountGraphicsItemFontSize 

        # X scaling of the text.
        self.barCountTextXScaling = \
            priceBarChartSettings.\
                barCountGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.barCountTextYScaling = \
            priceBarChartSettings.\
                barCountGraphicsItemTextYScaling 

        # Set the font size of the text.
        self.log.debug("Setting font size to: {}".format(self.barCountFontSize))
        self.barCountTextFont = QFont()
        self.barCountTextFont.setPointSizeF(self.barCountFontSize)
        self.barCountText.setFont(self.barCountTextFont)

        # Apply some size scaling to the text.
        self.log.debug("Setting transform: (dx={}, dy={})".\
                       format(self.barCountTextXScaling,
                              self.barCountTextYScaling))
        textTransform = QTransform()
        textTransform.scale(self.barCountTextXScaling, \
                            self.barCountTextYScaling)
        self.barCountText.setTransform(textTransform)

        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        settings = QSettings()

        # barCountGraphicsItemColor
        key = SettingsKeys.barCountGraphicsItemColorSettingsKey
        defaultValue = \
            SettingsKeys.barCountGraphicsItemColorSettingsDefValue
        self.barCountGraphicsItemColor = \
            QColor(settings.value(key, defaultValue))

        # barCountGraphicsItemTextColor
        key = SettingsKeys.barCountGraphicsItemTextColorSettingsKey
        defaultValue = \
            SettingsKeys.barCountGraphicsItemTextColorSettingsDefValue
        self.barCountGraphicsItemTextColor = \
            QColor(settings.value(key, defaultValue))
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        self.startPointF = self.startPointF + posDelta
        self.endPointF  = self.endPointF + posDelta

        if self.scene() != None:
            self.recalculateBarCount()

    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosX = event.scenePos().x()

            startingPointX = self.startPointF.x()
            endingPointX = self.endPointF.x()
            
            diff = endingPointX - startingPointX

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            if scenePosX <= startThreshold:
                self.draggingStartPointFlag = True
            elif scenePosX >= endThreshold:
                self.draggingEndPointFlag = True
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                super().mousePressEvent(event)

        self.log.debug("Leaving mousePressEvent()")
        
    def mouseMoveEvent(self, event):
        """Overwrites the QGraphicsItem mouseMoveEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        if event.buttons() & Qt.LeftButton:
            if self.getReadOnlyFlag() == False:
                if self.draggingStartPointFlag == True: 
                    self.setStartPointF(event.scenePos())
                elif self.draggingEndPointFlag == True:
                    self.setEndPointF(event.scenePos())
                else:
                    # This means that the user is dragging the whole
                    # ruler.  Do the move, but also set emit that the
                    # PriceBarChart has changed.
                    super().mouseMoveEvent(event)
                    self.scene().priceBarChartChanged.emit()
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Overwrites the QGraphicsItem mouseReleaseEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """
        
        self.log.debug("Entered mouseReleaseEvent()")

        if self.draggingStartPointFlag == True or \
                self.draggingEndPointFlag == True:
            
            self.log.debug("mouseReleaseEvent() when previously dragging.")
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.scene().priceBarChartChanged.emit()
        else:
            super().mouseReleaseEvent(event)

        self.log.debug("Exiting mouseReleaseEvent()")

    def setReadOnlyFlag(self, flag):
        """Overwrites the PriceBarChartArtifactGraphicsItem setReadOnlyFlag()
        function.
        """

        # Call the parent's function so that the flag gets set.
        super().setReadOnlyFlag(flag)

        # Make sure the drag flags are disabled.
        if flag == True:
            self.draggingStartPointFlag = False
            self.draggingEndPointFlag = False

    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        The actual start location drawn utilizes the mouse 
        location, and snaps to the closest whole X position.
        """

        #x = self._mousePosToNearestPriceBarX(pointF)
        x = round(pointF.x())

        newValue = QPointF(x, self.endPointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)
            
            # Update the barCount label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            y = 0
            self.barCountText.setPos(QPointF(deltaX, y))

            if self.scene() != None:
                # Re-calculate the bar count.
                self.recalculateBarCount()

                self.update()

    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        The actual start location drawn utilizes the mouse 
        location, and snaps to the closest whole X position.
        """

        #x = self._mousePosToNearestPriceBarX(pointF)
        x = round(pointF.x())

        newValue = QPointF(x, self.startPointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the barCount label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            y = 0
            self.barCountText.setPos(QPointF(deltaX, y))

            if self.scene() != None:
                # Re-calculate the bar count.
                self.recalculateBarCount()

                self.update()


    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.x() > self.endPointF.x():
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

            # Update the barCount label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            y = 0
            self.barCountText.setPos(QPointF(deltaX, y))

            self.recalculateBarCount()
            
            super().setPos(self.startPointF)
            

    def _mousePosToNearestPriceBarX(self, pointF):
        """Gets the X position value of the closest PriceBar (on the X
        axis) to the given mouse position.

        Arguments:
        pointF - QPointF to do the lookup on.

        Returns:
        float value for the X value.  If there are no PriceBars, then it
        returns the X given in the input pointF.
        """

        scene = self.scene()

        # Get all the QGraphicsItems.
        graphicsItems = scene.items()

        closestPriceBarX = None
        currClosestDistance = None

        # Go through the PriceBarGraphicsItems and find the closest one in
        # X coordinates.
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):

                x = item.getPriceBarHighScenePoint().x()
                distance = abs(pointF.x() - x)

                if closestPriceBarX == None:
                    closestPriceBarX = x
                    currClosestDistance = distance
                elif (currClosestDistance != None) and \
                        (distance < currClosestDistance):

                    closestPriceBarX = x
                    currClosestDistance = distance
                    
        if closestPriceBarX == None:
            closestPriceBarX = pointF.x()

        return closestPriceBarX

    def recalculateBarCount(self):
        """Sets the internal variable holding the number of bars in the
        X space between:

        (self.startPointF, self.endPointF]

        In the event self.startPointF or self.endPointF conjoin the X
        value of a PriceBar, the count excludes the bar conjoining
        self.startPointF and includes the bar conjoining self.endPointF.
        If the X values for both points are the same, then the bar count
        is zero.

        Returns:
        int value for the number of bars between the two points.
        """

        scene = self.scene()

        if scene == None:
            self.barCount = 0
        else:
            # Get all the QGraphicsItems.
            graphicsItems = scene.items()

            # Reset the bar count.
            self.barCount = 0

            # Test for special case.
            if self.startPointF.x() == self.endPointF.x():
                self.barCount = 0
            else:
                # Go through the PriceBarGraphicsItems and count the ones in
                # between self.startPointF and self.endPointF.
                for item in graphicsItems:
                    if isinstance(item, PriceBarGraphicsItem):

                        x = item.getPriceBarHighScenePoint().x()

                        # Here we check for the bar being in between
                        # the self.startPointF and the self.endPointF.
                        # This handles the case when the start and end
                        # points are reversed also.
                        if (self.startPointF.x() < x <= self.endPointF.x()) or \
                           (self.endPointF.x() < x <= self.startPointF.x()):
                            
                            self.barCount += 1
                            

        # Update the text of the self.barCountText.
        self.barCountText.setText("{}".format(self.barCount))
        
        return self.barCount

    def setPriceBarChartBarCountArtifact(self, priceBarChartBarCountArtifact):
        """Loads a given PriceBarChartBarCountArtifact object's data
        into this QGraphicsItem.
        """
        
        self.priceBarChartBarCountArtifact = \
            priceBarChartBarCountArtifact 

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.priceBarChartBarCountArtifact.getPos())
        self.setStartPointF(self.priceBarChartBarCountArtifact.getStartPointF())
        self.setEndPointF(self.priceBarChartBarCountArtifact.getEndPointF())

        # Need to recalculate the bar count, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the bar count will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateBarCount()

    def getPriceBarChartBarCountArtifact(self):
        """Returns a PriceBarChartBarCountArtifact for this QGraphicsItem 
        so that it may be pickled.
        """
        
        # Update the internal self.priceBarChartBarCountArtifact 
        # to be current, then return it.

        self.priceBarChartBarCountArtifact.setPos(self.pos())
        self.priceBarChartBarCountArtifact.setStartPointF(self.startPointF)
        self.priceBarChartBarCountArtifact.setEndPointF(self.endPointF)
        
        return self.priceBarChartBarCountArtifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the vertical bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.

        # The QRectF returned is relative to this (0, 0) point.

        # Get the QRectF with just the lines.
        xDelta = self.endPointF.x() - self.startPointF.x()
        
        topLeft = \
            QPointF(0.0, -1.0 * (self.barCountGraphicsItemBarHeight / 2.0))
        
        bottomRight = \
            QPointF(xDelta, 1.0 * (self.barCountGraphicsItemBarHeight / 2.0))
        
        rectWithoutText = QRectF(topLeft, bottomRight)

        return rectWithoutText

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.barCountPen:
            painter.setPen(self.barCountPen)
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.barCountGraphicsItemBarHeight / 2.0)
        x2 = 0.0
        y2 = -1.0 * (self.barCountGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.barCountGraphicsItemBarHeight / 2.0)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.barCountGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the middle horizontal line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.barCountPen.widthF() / 2.0;
            
            penWidth = 0.0

            fgcolor = option.palette.windowText().color()
            
            # Ensure good contrast against fgcolor.
            r = 255
            g = 255
            b = 255
            if fgcolor.red() > 127:
                r = 0
            if fgcolor.green() > 127:
                g = 0
            if fgcolor.blue() > 127:
                b = 0
            
            bgcolor = QColor(r, g, b)
            
            painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())

class PriceBarChartWidget(QWidget):
    """Widget holding the QGraphicsScene and QGraphicsView that displays
    the PriceBar information along with other indicators and analysis
    tools.
    """


    # Signal emitted when the PriceBarChartWidget changes.
    # 
    # Possible changes to the widget that will trigger this include: 
    #   - Any scene change (pricebars, artifacts)
    #   - Any settings change (scaling)
    #   
    # It does NOT include:
    #   - User selecting a pricebar
    #   - User opening a wheel astrology chart from a pricebar
    #
    priceBarChartChanged = QtCore.pyqtSignal()

    # Signal emitted when current timestamp of where the mouse is changes.
    currentTimestampChanged = QtCore.pyqtSignal(datetime.datetime)

    # Tool modes that this widget can be in.
    ToolMode = {"ReadOnlyPointerTool" : 0,
                "PointerTool"         : 1,
                "HandTool"            : 2,
                "ZoomInTool"          : 3,
                "ZoomOutTool"         : 4,
                "BarCountTool"        : 5 }


    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarChartWidget")
        self.log.debug("Entered __init__()")

        # Create the contents.
        self.priceBarChartSettings = PriceBarChartSettings()
        
        # Holds the tool mode that this widget is currently in.
        self.toolMode = PriceBarChartWidget.ToolMode['ReadOnlyPointerTool']

        # Holds the timezone of PriceBars in this widget.  
        # This is a datetime.tzinfo object.  We need this to convert X
        # scene coordinate values to a datetime.datetime object with the
        # correct timezone.
        self.timezone = pytz.utc

        # These are the label widgets at the top of the PriceBarChartWidget.
        self.descriptionLabel = QLabel("")
        self.firstPriceBarTimestampLabel = QLabel("")
        self.lastPriceBarTimestampLabel = QLabel("")
        self.numPriceBarsLabel = QLabel("")
        
        localizedTimestampStr = "Mouse location timestamp: "
        utcTimestampStr = "Mouse location timestamp: "
        priceStr = "Mouse location price: " 
        self.cursorLocalizedTimestampLabel = \
            QLabel(localizedTimestampStr)
        self.cursorUtcTimestampLabel = \
            QLabel(utcTimestampStr)
        self.cursorPriceLabel = \
            QLabel(priceStr)
        
        self.selectedPriceBarTimestampLabel = QLabel("")
        self.selectedPriceBarOpenPriceLabel = QLabel("")
        self.selectedPriceBarHighPriceLabel = QLabel("")
        self.selectedPriceBarLowPriceLabel = QLabel("")
        self.selectedPriceBarClosePriceLabel = QLabel("")
        
        # These labels will have smaller font.
        smallFont = QFont()
        smallFont.setPointSize(7)
        self.descriptionLabel.setFont(smallFont)
        self.firstPriceBarTimestampLabel.setFont(smallFont)
        self.lastPriceBarTimestampLabel.setFont(smallFont)
        self.numPriceBarsLabel.setFont(smallFont)
        self.cursorLocalizedTimestampLabel.setFont(smallFont)
        self.cursorUtcTimestampLabel.setFont(smallFont)
        self.cursorPriceLabel.setFont(smallFont)
        self.selectedPriceBarTimestampLabel.setFont(smallFont)
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
        dataTimeRangeLayout.addWidget(self.descriptionLabel)
        dataTimeRangeLayout.addWidget(self.firstPriceBarTimestampLabel)
        dataTimeRangeLayout.addWidget(self.lastPriceBarTimestampLabel)
        dataTimeRangeLayout.addWidget(self.numPriceBarsLabel)

        cursorInfoLayout = QVBoxLayout()
        cursorInfoLayout.addWidget(self.cursorLocalizedTimestampLabel)
        cursorInfoLayout.addWidget(self.cursorUtcTimestampLabel)
        cursorInfoLayout.addWidget(self.cursorPriceLabel)
       
        priceBarPricesLayout = QVBoxLayout()
        priceBarPricesLayout.addWidget(self.selectedPriceBarTimestampLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarOpenPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarHighPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarLowPriceLabel)
        priceBarPricesLayout.addWidget(self.selectedPriceBarClosePriceLabel)
        
        topLabelsLayout = QHBoxLayout()
        topLabelsLayout.addLayout(dataTimeRangeLayout)
        topLabelsLayout.addLayout(cursorInfoLayout)
        topLabelsLayout.addLayout(priceBarPricesLayout)
        
        layout = QVBoxLayout()
        layout.addLayout(topLabelsLayout)
        layout.addWidget(self.graphicsView)
        self.setLayout(layout)

        self.graphicsView.show()

        # Connect signals and slots.
        self.graphicsView.mouseLocationUpdate.\
            connect(self._handleMouseLocationUpdate)
        self.graphicsScene.priceBarChartChanged.\
            connect(self.priceBarChartChanged)
        self.graphicsScene.selectionChanged.\
            connect(self._handleSelectionChanged)

        self.log.debug("Leaving __init__()")

    def setTimezone(self, timezone):
        """Sets the timezone used.  This is used for converting mouse
        X location to a datetime.datetime object.
        
        Arguments:
            
        timezone - A datetime.tzinfo object holding the timezone for the
                   pricebars in this widget.
        """

        self.timezone = timezone


    def setDescriptionText(self, text):
        """Sets the text of the QLabel self.descriptionLabel."""

        self.descriptionLabel.setText("Description: " + text)

    def updateFirstPriceBarTimestampLabel(self, priceBar=None):
        """Updates the QLabel holding the timestamp of the first PriceBar
        in the pricebarchart.

        Arguments:

        priceBar - PriceBar object to use for updating the timestamp.  
                   If this argument is None, then the label text will be
                   blank.
        """

        # Datetime format to datetime.strftime().
        fmt = "%Y-%m-%d %H:%M:%S %Z %z"

        timestampStr = "First PriceBar Timestamp: "
        
        if priceBar != None:
            timestampStr += "{}".format(priceBar.timestamp.strftime(fmt))

        self.firstPriceBarTimestampLabel.setText(timestampStr)

    def updateLastPriceBarTimestampLabel(self, priceBar=None):
        """Updates the QLabel holding the timestamp of the last PriceBar
        in the pricebarchart.

        Arguments:

        priceBar - PriceBar object to use for updating the timestamp.  
                   If this argument is None, then the label text will be
                   blank.
        """

        # Datetime format to datetime.strftime().
        fmt = "%Y-%m-%d %H:%M:%S %Z %z"

        timestampStr = "Last PriceBar Timestamp: "
        
        if priceBar != None:
            timestampStr += "{}".format(priceBar.timestamp.strftime(fmt))
        
        self.lastPriceBarTimestampLabel.setText(timestampStr)

    def updateNumPriceBarsLabel(self, numPriceBars):
        """Updates the QLabel holding the number of PriceBars
        currently drawn in the pricebarchart.

        Arguments:

        numPriceBars - int value for the number of PriceBars displayed in
                       the PriceBarChart.
        """

        text = "Number of PriceBars: {}".format(numPriceBars)

        self.numPriceBarsLabel.setText(text)

    def updateMouseLocationLabels(self, sceneXPos=None, sceneYPos=None):
        """Updates the QLabels holding the information about the time and
        price of where the mouse position is.  If either of the input
        arguments are None, then the cursor labels are cleared out.
        
        Arguments:
            
        sceneXPos - float value holding the X location of the mouse, in
                    scene coordinates. 
        sceneYPos - float value holding the X location of the mouse, in
                    scene coordinates.
        """

        localizedTimestampStr = "Mouse location timestamp: "
        utcTimestampStr = "Mouse location timestamp: "
        priceStr = "Mouse location price: " 

        # Set the values if the X and Y positions are valid.
        if sceneXPos != None and sceneYPos != None:

            # Convert coordinate to the actual values they represent.
            timestamp = self._sceneXPosToDatetime(sceneXPos)
            price = self._sceneYPosToPrice(sceneYPos)

            # Datetime format to datetime.strftime().
            fmt = "%Y-%m-%d %H:%M:%S %Z %z"

            # Append to the strings.
            localizedTimestampStr += "{}".format(timestamp.strftime(fmt))
            utcTimestampStr += "{}".\
                format(timestamp.astimezone(pytz.utc).strftime(fmt))
            priceStr += "{}".format(price)

        # Actually set the text to the widgets.
        self.cursorLocalizedTimestampLabel.setText(localizedTimestampStr)
        self.cursorUtcTimestampLabel.setText(utcTimestampStr)
        self.cursorPriceLabel.setText(priceStr)

    def updateSelectedPriceBarLabels(self, priceBar=None):
        """Updates the QLabels describing the currently selected PriceBar.
        
        Arguments:

        priceBar - PriceBar object that holds info about the currently
                   selected PriceBar.
        """

        # Datetime format to datetime.strftime().
        fmt = "%Y-%m-%d %H:%M:%S %Z %z"

        timestampStr = "Timestamp: "
        openStr = "Open: "
        highStr = "High: "
        lowStr = "Low: "
        closeStr = "Close: "

        if priceBar != None:
            timestampStr += priceBar.timestamp.strftime(fmt)
            openStr += "{}".format(priceBar.open)
            highStr += "{}".format(priceBar.high)
            lowStr += "{}".format(priceBar.low)
            closeStr += "{}".format(priceBar.close)

        # Only change the labels if they are now different.
        if self.selectedPriceBarTimestampLabel.text() != timestampStr:
            self.selectedPriceBarTimestampLabel.setText(timestampStr)

        if self.selectedPriceBarOpenPriceLabel.text() != openStr:
            self.selectedPriceBarOpenPriceLabel.setText(openStr)

        if self.selectedPriceBarHighPriceLabel.text() != highStr:
            self.selectedPriceBarHighPriceLabel.setText(highStr)

        if self.selectedPriceBarLowPriceLabel.text() != lowStr:
            self.selectedPriceBarLowPriceLabel.setText(lowStr)

        if self.selectedPriceBarClosePriceLabel.text() != closeStr:
            self.selectedPriceBarClosePriceLabel.setText(closeStr)


    def loadPriceBars(self, priceBars):
        """Loads the given PriceBars list into this widget as
        PriceBarGraphicsItems.
        """
        
        self.log.debug("Entered loadPriceBars({} pricebars)".\
                       format(len(priceBars)))

        for priceBar in priceBars:

            # Create the QGraphicsItem
            item = PriceBarGraphicsItem()
            item.loadSettingsFromPriceBarChartSettings(\
                self.priceBarChartSettings)
            item.setPriceBar(priceBar)

            # Add the item.
            self.graphicsScene.addItem(item)

            # Make sure the proper flags are set for the mode we're in.
            self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(item)

            # X location based on the timestamp.
            x = self._datetimeToSceneXPos(priceBar.timestamp)

            # Y location based on the mid price (average of high and low).
            y = self._priceToSceneYPos(priceBar.midPrice())

            # Set the position, in parent coordinates.
            item.setPos(QPointF(x, y))

        # Set the labels for the timestamps of the first and 
        # last pricebars.
        if len(priceBars) > 0:
            firstPriceBar = priceBars[0]
            lastPriceBar = priceBars[-1]

            self.updateFirstPriceBarTimestampLabel(firstPriceBar)
            self.updateLastPriceBarTimestampLabel(lastPriceBar)
            self.updateNumPriceBarsLabel(len(priceBars))
        else:
            # There are no PriceBars.  Update the labels to reflect that.
            self.updateFirstPriceBarTimestampLabel(None)
            self.updateLastPriceBarTimestampLabel(None)
            self.updateNumPriceBarsLabel(len(priceBars))
            
        self.log.debug("Leaving loadPriceBars({} pricebars)".\
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

        # Update the labels describing the pricebarchart.
        self.updateFirstPriceBarTimestampLabel(None)
        self.updateLastPriceBarTimestampLabel(None)
        self.updateNumPriceBarsLabel(0)
        self.updateSelectedPriceBarLabels(None)


    def getPriceBarChartArtifacts(self):
        """Returns the list of PriceBarChartArtifacts that have been used
        to draw the the artifacts in the QGraphicsScene.
        """

        self.log.debug("Entered getPriceBarChartArtifacts()")
        
        # List of PriceBarChartArtifact objects returned.
        artifacts = []
        
        # Go through all the QGraphicsItems and for each artifact type,
        # extract the PriceBarChartArtifact.
        graphicsItems = self.graphicsScene.items()
        
        for item in graphicsItems:
            if isinstance(item, BarCountGraphicsItem):
                artifacts.append(item.getPriceBarChartBarCountArtifact())


        self.log.debug("Number of artifacts being returned is: {}".\
                       format(len(artifacts)))
        
        self.log.debug("Exiting getPriceBarChartArtifacts()")
        
        return artifacts

    def loadPriceBarChartArtifacts(self, priceBarChartArtifacts):
        """Loads the given list of PriceBarChartArtifact objects
        into this widget as QGraphicsItems.

        Arguments:
        
        priceBarChartArtifacts - list of PriceBarChartArtifact objects,
                                 which is used to create various types of
                                 PriceBarChartArtifactGraphicsItem to be
                                 added to the QGraphicsScene.
        """
        
        self.log.debug("Entered loadPriceBarChartArtifacts()")

        self.log.debug("Attempting to load {} artifacts.".\
                       format(len(priceBarChartArtifacts)))

        # Flag to determine if an item was created and added.
        addedItemFlag = False
        
        for artifact in priceBarChartArtifacts:

            # Create the specific PriceBarChartArtifactGraphicsItem,
            # depending on what kind of artifact this is.
            if isinstance(artifact, PriceBarChartBarCountArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = BarCountGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setPriceBarChartBarCountArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate bar count, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculateBarCount()
        
                addedItemFlag = True

        if addedItemFlag == True:
            # Emit that the PriceBarChart has changed.
            self.graphicsScene.priceBarChartChanged.emit()
            
        self.log.debug("Exiting loadPriceBarChartArtifacts()")



    def addPriceBarChartArtifact(self, priceBarChartArtifact):
        """Adds the given PriceBarChartArtifact objects 
        into this widget as QGraphicsItems."""

        # List of one element.
        artifacts = [priceBarChartArtifact]

        # Load it via a list.  If it is added, then it will emit
        # the self.priceBarChartChanged signal for us.
        self.loadPriceBarChartArtifacts(artifacts)
        
    def clearAllPriceBarChartArtifacts(self):
        """Clears all the PriceBarChartArtifact objects from the 
        QGraphicsScene."""

        self.log.debug("Entered clearAllPriceBarChartArtifacts()")

        # Flag to determine if an item was removed.
        removedItemFlag = False
        
        # Go through all the QGraphicsItems and remove the artifact items.
        graphicsItems = self.graphicsScene.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarChartArtifactGraphicsItem):
                self.log.debug("Removing QGraphicsItem for artifact " + \
                               item.toString())
                self.graphicsScene.removeItem(item)
                
                removedItemFlag = True

        if removedItemFlag == True:
            # Emit that the PriceBarChart has changed.
            self.graphicsScene.priceBarChartChanged.emit()
            
        self.log.debug("Exiting clearAllPriceBarChartArtifacts()")
        
    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the settings in the given PriceBarChartSettings object.
        """
        
        self.log.debug("Entering applyPriceBarChartSettings()")

        self.priceBarChartSettings = priceBarChartSettings

        # Save a reference to the current PriceBarChartSettings in the
        # QGraphicsView.  This is used when the user creates new chart
        # artificats at run time.
        self.graphicsView.setPriceBarChartSettings(self.priceBarChartSettings)

        # Flag to indicate if the settings has changed because we
        # corrected an invalid settings field and the settings needs
        # to be re-saved.
        settingsChangedFlag = False

        self.log.debug("Applying QGraphicsView scaling...")

        numScalings = \
            len(self.priceBarChartSettings.priceBarChartGraphicsViewScalings)

        # Get the index for which scaling we should apply.
        currScalingIndex = \
            self.priceBarChartSettings.priceBarChartGraphicsViewScalingsIndex

        # Temporary variable holding the PriceBarChartScaling scaling
        # object to use.
        scaling = PriceBarChartScaling()

        if numScalings >= 1:
            
            if currScalingIndex < 0 or currScalingIndex >= numScalings:
                # Use the first scaling in the list.
                currScalingIndex = 0
                self.priceBarChartSettings.\
                    priceBarChartGraphicsViewScalingsIndex = 0

                settingsChangedFlag = True

            # Use the scaling at index currScalingIndex.
            scaling = \
                self.priceBarChartSettings.\
                    priceBarChartGraphicsViewScalings[currScalingIndex]

        elif numScalings == 0:
            # There are no scalings in the list.  

            # Create a scaling containing the identity matrix, and then
            # add it to the array and then use that scaling.
            scaling = PriceBarChartScaling()
            scaling.name = "Default"

            self.priceBarChartSettings.\
                priceBarChartGraphicsViewScalings.append(scaling)

            self.priceBarChartSettings.\
                priceBarChartGraphicsViewScalingsIndex = 0

            settingsChangedFlag = True

        # Create a new QTransform that holds the scaling we want
        # but preserve the translation and other parts of the
        # transform from what is currently displayed in the
        # QGraphicsView.

        # Get the current QTransform.
        transform = self.graphicsView.transform()

        # Get the QTransform that has the desired scaling from the
        # PriceBarChartSettings.
        scalingTransform = scaling.getTransform()

        # Create a new QTransform that has elements of both.
        newTransform = QTransform(scalingTransform.m11(),
                                  transform.m12(),
                                  transform.m13(),
                                  transform.m21(),
                                  scalingTransform.m22(),
                                  transform.m23(),
                                  transform.m31(),
                                  transform.m32(),
                                  transform.m33())

        # Apply the transform.
        self.graphicsView.setTransform(newTransform)

        # Apply the settings on all the existing relevant QGraphicsItems.
        graphicsItems = self.graphicsScene.items()
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                self.log.debug("Applying settings to PriceBarGraphicsItem.")
                item.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
            elif isinstance(item, BarCountGraphicsItem):
                self.log.debug("Applying settings to BarCountGraphicsItem.")
                item.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)

        if settingsChangedFlag == True:
            # Emit that the PriceBarChart has changed, because we have
            # updated the PriceBarChartSettings.
            self.priceBarChartChanged.emit()

        self.log.debug("Exiting applyPriceBarChartSettings()")

    def getPriceBarChartSettings(self):
        """Returns the current settings used in this PriceBarChartWidget."""
        
        return self.priceBarChartSettings

    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool."""

        self.log.debug("Entered toReadOnlyPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartWidget.ToolMode['ReadOnlyPointerTool']:

            self.toolMode = \
                PriceBarChartWidget.ToolMode['ReadOnlyPointerTool']
            self.graphicsView.toReadOnlyPointerToolMode()

        self.log.debug("Exiting toReadOnlyPointerToolMode()")

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool."""

        self.log.debug("Entered toPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['PointerTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['PointerTool']
            self.graphicsView.toPointerToolMode()

        self.log.debug("Exiting toPointerToolMode()")

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.log.debug("Entered toHandToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['HandTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['HandTool']
            self.graphicsView.toHandToolMode()

        self.log.debug("Exiting toHandToolMode()")

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.log.debug("Entered toZoomInToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['ZoomInTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['ZoomInTool']
            self.graphicsView.toZoomInToolMode()

        self.log.debug("Exiting toZoomInToolMode()")

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.log.debug("Entered toZoomOutToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['ZoomOutTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['ZoomOutTool']
            self.graphicsView.toZoomOutToolMode()

        self.log.debug("Exiting toZoomOutToolMode()")

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.log.debug("Entered toBarCountToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['BarCountTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['BarCountTool']
            self.graphicsView.toBarCountToolMode()

        self.log.debug("Exiting toBarCountToolMode()")


    def _sceneXPosToDatetime(self, sceneXPos):
        """Returns a datetime.datetime object for the given X position in
        scene coordinates.

        Arguments:

        sceneXPos - float value holding the X position in scene coordinates.

        Returns:

        datetime.datetime object holding the timestamp of the input X
        position.  This datetime.datetime object has its timezone set to
        whatever was set in setTimezone() previously.  If nothing was set
        before, then the default timezone is pytz.utc.
        """

        return Ephemeris.julianDayToDatetime(sceneXPos, self.timezone)
    
    def _sceneYPosToPrice(self, sceneYPos):
        """Returns a price value for the given Y position in scene
        coordinates.

        Arguments:

        sceneYPos - float value holding the Y position in scene
        coordinates.

        Returns:

        float value for the price that this Y position represents.
        """

        return float(-1.0 * sceneYPos)

    def _datetimeToSceneXPos(self, dt):
        """Returns the conversion from datetime.datetime object to what we
        chosen the X coordinate values to be.

        Arguments:

        dt - datetime.datetime object that holds a timestamp.

        Returns:

        float value for the X position that would match up with this timestamp.
        """

        return Ephemeris.datetimeToJulianDay(dt)

    def _priceToSceneYPos(self, price):
        """Returns the conversion from price to what we have chosen the Y
        coordinate values to be.

        Arguments:

        price - float value holding the price value.

        Returns:

        float value for the Y position that would match up with this price.
        """

        return float(-1.0 * price)



    def _handleMouseLocationUpdate(self, x, y):
        """Handles mouse location changes in the QGraphicsView.  
        Arguments:

        x - float value of the mouse's X coordinate position, in scene
        coordinates.
        y - float value of the mouse's Y coordinate position, in scene
        coordinates.
        """

        # Update labels that tell where the mouse pointer is.
        self.updateMouseLocationLabels(x, y)

        # Emit a signal so that other widgets/entities can know
        # the timestamp where the mouse pointer is.
        dt = self._sceneXPosToDatetime(x)
        self.currentTimestampChanged.emit(dt)

    def _handleSelectionChanged(self):
        """Handles when the QGraphicsScene has it's selection of
        QGraphicsItems changed.

        This function obtains the selected items, and if there is only
        one PriceBarGraphicsItem selected, then it displays the
        information about that pricebar in the labels at the top of
        the widget.
        """

        selectedItems = self.graphicsScene.selectedItems()

        numPriceBarGraphicsItemsSelected = 0
        lastPriceBarGraphicsItem = None
        
        for item in selectedItems:
            if isinstance(item, PriceBarGraphicsItem):
                numPriceBarGraphicsItemsSelected += 1
                lastPriceBarGraphicsItem = item

        self.log.debug("Number of PriceBarGraphicsItems selected is: {}".\
                       format(numPriceBarGraphicsItemsSelected))

        # Only update the labels with price/time information if there
        # was only one PriceBarGraphicsItem selected.  This is done to
        # avoid confusion in the event that a second
        # PriceBarGraphicsItem is selected and the user didn't notice
        # that it was (to prevent the wrong information from being
        # interpreted).
        if numPriceBarGraphicsItemsSelected == 1:
            priceBar = lastPriceBarGraphicsItem.getPriceBar()
            self.updateSelectedPriceBarLabels(priceBar)
        else:
            self.updateSelectedPriceBarLabels(None)
            
        
class PriceBarChartGraphicsScene(QGraphicsScene):
    """QGraphicsScene holding all the pricebars and artifacts.
    We subclass the QGraphicsScene to allow for future feature additions.
    """

    # Signal emitted when there is an addition of a
    # PriceBarChartArtifactGraphicsItem.
    priceBarChartArtifactGraphicsItemAdded = \
        QtCore.pyqtSignal(PriceBarChartArtifactGraphicsItem)
        
    # Signal emitted when there is a removal of a
    # PriceBarChartArtifactGraphicsItem.
    priceBarChartArtifactGraphicsItemRemoved = \
        QtCore.pyqtSignal(PriceBarChartArtifactGraphicsItem)

    # Signal emitted when there is an addition or removal of a
    # PriceBarChartArtifactGraphicsItem.
    priceBarChartChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Pass-through to the QGraphicsScene constructor."""

        super().__init__(parent)

        # Adding or removing an artifact graphics item counts as
        # something changed.
        self.priceBarChartArtifactGraphicsItemAdded.\
            connect(self.priceBarChartChanged)
        self.priceBarChartArtifactGraphicsItemRemoved.\
            connect(self.priceBarChartChanged)
        
class PriceBarChartGraphicsView(QGraphicsView):
    """QGraphicsView that visualizes the main QGraphicsScene.
    We inherit QGraphicsView because we may want to add 
    custom syncrhonized functionality in other widgets later."""


    # Tool modes that this widget can be in.
    ToolMode = {"ReadOnlyPointerTool" : 0,
                "PointerTool"         : 1,
                "HandTool"            : 2,
                "ZoomInTool"          : 3,
                "ZoomOutTool"         : 4,
                "BarCountTool"        : 5 }

    # Signal emitted when the mouse moves within the QGraphicsView.
    # The position emitted is in QGraphicsScene x, y, float coordinates.
    mouseLocationUpdate = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None):
        """Pass-through to the QGraphicsView constructor."""

        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceBarChartGraphicsView")
        self.log.debug("Entered __init__()")

        # Save the current transformation matrix of the view.
        self.transformationMatrix = None

        # Save the current viewable portion of the scene.
        self.viewableSceneRectF = self.mapToScene(self.rect()).boundingRect()

        # Holds the tool mode that this widget is currently in.
        self.toolMode = \
            PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']

        # Anchor variable we will use for click-drag, etc.
        self.dragAnchorPointF = QPointF()

        # Variable used for storing mouse clicks (used in the various
        # modes for various purposes).
        self.clickOnePointF = None
        self.clickTwoPointF = None

        # Variable used for storing the new BarCountGraphicsItem,
        # as it is modified in BarCountToolMode.
        self.barCountGraphicsItem = None

        # Variable used for holding the PriceBarChartSettings.
        self.priceBarChartSettings = PriceBarChartSettings()
        
        # Get the QSetting key for the zoom scaling amounts.
        self.zoomScaleFactorSettingsKey = \
            SettingsKeys.zoomScaleFactorSettingsKey 

        #self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setInteractive(True)

        # Set some rendering settings so things draw nicely.
        self.setRenderHints(QPainter.Antialiasing | 
                            QPainter.TextAntialiasing | 
                            QPainter.SmoothPixmapTransform)

        # Set to FullViewportUpdate update mode.
        #
        # The default is normally QGraphicsView.MinimalViewportUpdate, but
        # this caused us to have missing parts of artifacts and missing
        # parts of pricebars.  And while performance isn't as great in
        # the FullViewportUpdate mode, we dont' have many things dynamically
        # updating and changing, so it isn't too big of an issue.
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def setPriceBarChartSettings(self, priceBarChartSettings):
        """Stores the reference to PriceBarChartSettings to be used in
        creating new QGraphicsItems.
        """
        
        self.priceBarChartSettings = priceBarChartSettings
        
    def setGraphicsItemFlagsPerCurrToolMode(self, item):
        """Sets the QGraphicsItem flags of the given QGraphicsItem,
        according to what the flags should be set to for the current
        tool mode.

        Arguments:

        item - QGraphicsItem that needs its flags set.
        """
        
        if self.toolMode == \
               PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.ItemIsSelectable)
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.ItemIsSelectable)
                
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:
             
            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(False)
                item.setFlags(QGraphicsItem.ItemIsMovable |
                              QGraphicsItem.ItemIsSelectable)
                
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:
             
            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
             
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

                
    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool.
        
        This has the following effects on QGraphicsItem flags:
          - All PriceBarGraphicsItems are selectable.
          - All PriceBarGraphicsItems are not movable.
          - All PriceBarChartArtifactGraphicsItem are selectable.
          - All PriceBarChartArtifactGraphicsItem are not movable.
        """

        self.log.debug("Entered toReadOnlyPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.RubberBandDrag)

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)

        self.log.debug("Exiting toReadOnlyPointerToolMode()")

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool.
        
        This has the following effects on QGraphicsItem flags:
          - All PriceBarGraphicsItems are not selectable.
          - All PriceBarGraphicsItems are not movable.
          - All PriceBarChartArtifactGraphicsItem are selectable.
          - All PriceBarChartArtifactGraphicsItem are movable.
        """

        self.log.debug("Entered toPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['PointerTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['PointerTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.RubberBandDrag)

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
            
        self.log.debug("Exiting toPointerToolMode()")

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.log.debug("Entered toHandToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['HandTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['HandTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.ScrollHandDrag)

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)

        self.log.debug("Exiting toHandToolMode()")

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.log.debug("Entered toZoomInToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['ZoomInTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['ZoomInTool']

            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(QCursor(Qt.ArrowCursor))

            if self.underMouse():
                pixmap = QPixmap(":/images/rluu/zoomIn.png")
                self.setCursor(QCursor(pixmap))

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toZoomInToolMode()")

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.log.debug("Entered toZoomOutToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['ZoomOutTool']

            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(QCursor(Qt.ArrowCursor))

            if self.underMouse():
                pixmap = QPixmap(":/images/rluu/zoomOut.png")
                self.setCursor(QCursor(pixmap))

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toZoomOutToolMode()")

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.log.debug("Entered toBarCountToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.barCountGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toBarCountToolMode()")

    def wheelEvent(self, qwheelevent):
        """Triggered when the mouse wheel is scrolled."""

        self.log.debug("Entered wheelEvent()")

        # Get the mouse location.  This will be the new center.
        newCenterPointF = self.mapToScene(qwheelevent.pos())

        # Get the QSetting key for the zoom scaling amounts.
        settings = QSettings()
        scaleFactor = \
            float(settings.value(self.zoomScaleFactorSettingsKey, \
                  SettingsKeys.zoomScaleFactorSettingsDefValue))

        # Actually do the scaling of the view.
        if qwheelevent.delta() > 0:
            # Zoom in.
            self.scale(scaleFactor, scaleFactor)
        else:
            # Zoom out.
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

        # Center on the new center.
        self.centerOn(newCenterPointF)

        self.log.debug("Exiting wheelEvent()")

    def keyPressEvent(self, qkeyevent):
        """Overwrites the QGraphicsView.keyPressEvent() function.
        Called when a key is pressed.
        """

        self.log.debug("Entered keyPressEvent()")

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            if qkeyevent.key() & Qt.Key_Delete:
                # Get the items that are selected, and out of those,
                # remove the PriceBarChartArtifactGraphicsItems.
                scene = self.scene()
                selectedItems = scene.selectedItems()

                for item in selectedItems:
                    if isinstance(item, PriceBarChartArtifactGraphicsItem):
                        
                        scene.removeItem(item)
        
                        # Emit signal to show that an item is removed.
                        # This sets the dirty flag.
                        scene.priceBarChartArtifactGraphicsItemRemoved.emit(item)
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            if qkeyevent.key() & Qt.Key_Escape:
                # Escape key causes any currently edited bar count item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.barCountGraphicsItem != None:
                    self.scene().removeItem(self.barCountGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.barCountGraphicsItem = None

            else:
                super().keyPressEvent(qkeyevent)


        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            super().keyPressEvent(qkeyevent)

        
        self.log.debug("Exiting keyPressEvent()")

        
    def mousePressEvent(self, qmouseevent):
        """Triggered when the mouse is pressed in this widget."""

        self.log.debug("Entered mousePressEvent()")

        scene = self.scene()

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            if qmouseevent.button() & Qt.RightButton:
                # TODO:  add the following as code.

                # See if the user has right clicked on a QGraphicsItem.

                clickPosF = self.mapToScene(qmouseevent.pos())
                topItem = scene.itemAt(clickPosF, self.transform())
                # Branch.

                # If more than one QGraphicsItem is here, then
                # bring up a context menu with all the item and choices.

                # If only one QGraphicsItem, then bring up context menu
                # for that item.

                # If no QGraphicsItems, then bring up context menu for
                # those options.

        
                # (Be sure to add a context menu with choices for
                # showing the astro chart at this time, and the 
                # for showing the sq-of-9, etc. for this price/time.
                pass
            else:
                super().mousePressEvent(qmouseevent)


            


        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            super().mousePressEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            # Panning the QGraphicsView.
            super().mousePressEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            if qmouseevent.button() & Qt.LeftButton:
                # New center
                newCenterPointF = self.mapToScene(qmouseevent.pos())

                # Get the QSetting key for the zoom scaling amounts.
                settings = QSettings()
                scaleFactor = \
                    float(settings.value(self.zoomScaleFactorSettingsKey, \
                            SettingsKeys.zoomScaleFactorSettingsDefValue))

                # Actually do the scaling of the view.
                self.scale(scaleFactor, scaleFactor)

                # Center on the new center.
                self.centerOn(newCenterPointF)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            
            if qmouseevent.button() & Qt.LeftButton:
                # New center
                newCenterPointF = self.mapToScene(qmouseevent.pos())

                # Get the QSetting key for the zoom scaling amounts.
                settings = QSettings()
                scaleFactor = \
                    float(settings.value(self.zoomScaleFactorSettingsKey, \
                            SettingsKeys.zoomScaleFactorSettingsDefValue))

                # Actually do the scaling of the view.
                self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

                # Center on the new center.
                self.centerOn(newCenterPointF)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:
            
            if qmouseevent.button() & Qt.LeftButton:
                if self.clickOnePointF == None:
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # Create the BarCountGraphicsItem and initialize it to
                    # the mouse location.
                    self.barCountGraphicsItem = BarCountGraphicsItem()
                    self.barCountGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
                    self.barCountGraphicsItem.setPos(self.clickOnePointF)
                    self.barCountGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.barCountGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.barCountGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.barCountGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.barCountGraphicsItem != None:

                    # Set the end point of the BarCountGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())
                    self.barCountGraphicsItem.setEndPointF(self.clickTwoPointF)
                    self.barCountGraphicsItem.normalizeStartAndEnd()
                                                
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.barCountGraphicsItem)
                    
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.barCountGraphicsItem = None
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.barCountGraphicsItem != None:


                    # Right-click during setting the BarCountGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.barCountGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.barCountGraphicsItem = None
                    
        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            super().mousePressEvent(qmouseevent)

        self.log.debug("Exiting mousePressEvent()")

    def mouseReleaseEvent(self, qmouseevent):
        """Triggered when the mouse is pressed in this widget."""

        self.log.debug("Entered mouseReleaseEvent()")

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            super().mouseReleaseEvent(qmouseevent)

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            super().mouseReleaseEvent(qmouseevent)

        self.log.debug("Exiting mouseReleaseEvent()")

    def mouseMoveEvent(self, qmouseevent):
        """Triggered when the mouse is moving in this widget."""

        # Emit the current mouse location in scene coordinates.
        posScene = self.mapToScene(qmouseevent.pos())
        self.mouseLocationUpdate.emit(posScene.x(), posScene.y())

        
        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            if self.clickOnePointF != None and \
                self.barCountGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # BarCountGraphicsItem.
                self.barCountGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            super().mouseMoveEvent(qmouseevent)



    def enterEvent(self, qevent):
        """Overwrites the QWidget.enterEvent() function.  

        Whenever the mouse enters the area of this widget, this function
        is called.  I've overwritten this function to change the mouse
        cursor according to what tool mode is currently active.

        Arguments:

        qevent - QEvent object that triggered this function call.
        """

        self.log.debug("Entered enterEvent()")

        # Set the cursor shape/image according to what tool mode the
        # pricebarchart is in.

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:
            pixmap = QPixmap(":/images/rluu/zoomIn.png")
            self.setCursor(QCursor(pixmap))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            pixmap = QPixmap(":/images/rluu/zoomOut.png")
            self.setCursor(QCursor(pixmap))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        else:
            self.log.warn("Unknown toolMode while in enterEvent().")

        # Allow any other super classes to process the event as well.
        super().enterEvent(qevent)

        self.log.debug("Exiting enterEvent()")

    def leaveEvent(self, qevent):
        """Overwrites the QWidget.leaveEvent() function.  

        Whenever the mouse leaves the area of this widget, this function
        is called.  I've overwritten this function to change the mouse
        cursor from whatever it is currently set to, back to the original
        pointer cursor.

        Arguments:

        qevent - QEvent object that triggered this function call.
        """

        self.log.debug("Entered leaveEvent()")

        # Set the cursor shape/image to the ArrowCursor.
        self.setCursor(QCursor(Qt.ArrowCursor))

        # Allow any other super classes to process the event as well.
        super().leaveEvent(qevent)

        self.log.debug("Exiting leaveEvent()")

    
