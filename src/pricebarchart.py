
# For line separator.
import os

# For logging.
import logging

# For dynamically adding methods to instances.
import types

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
from data_objects import MusicalRatio
from data_objects import PriceBarChartBarCountArtifact
from data_objects import PriceBarChartTimeMeasurementArtifact
from data_objects import PriceBarChartModalScaleArtifact
from data_objects import PriceBarChartGannFanUpperRightArtifact
from data_objects import PriceBarChartGannFanLowerRightArtifact
from data_objects import PriceBarChartScaling
from data_objects import PriceBarChartSettings
from data_objects import PriceBarChartTextArtifact

# For conversions from julian day to datetime.datetime and vice versa.
from ephemeris import Ephemeris

# For edit dialogs for modifying the PriceBarChartArtifact objects of
# various PriceBarChartArtifactGraphicsItems.
from pricebarchart_dialogs import PriceBarChartBarCountArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTimeMeasurementArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartModalScaleArtifactEditDialog

# For edit dialogs.
from dialogs import PriceBarEditDialog

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

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceBarGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        PriceBarGraphicsItem to handle the desired functionality.

        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        # Set the menu title.
        if self.priceBar != None:
            datetimeObj = self.priceBar.timestamp
            timestampStr = Ephemeris.datetimeToDayStr(datetimeObj)
            menu.setTitle("PriceBar_" + timestampStr)
        else:
            menu.setTitle("PriceBar_" + "Unknown")
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("Select", parent)
        unselectAction = QAction("Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("Info", parent)
        editAction = QAction("Edit", parent)
        setAstro1Action = QAction("Set timestamp on Astro Chart 1", parent)
        setAstro2Action = QAction("Set timestamp on Astro Chart 2", parent)
        setAstro3Action = QAction("Set timestamp on Astro Chart 3", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setAstro1Action.triggered.\
            connect(self._handleSetAstro1Action)
        setAstro2Action.triggered.\
            connect(self._handleSetAstro2Action)
        setAstro3Action.triggered.\
            connect(self._handleSetAstro3Action)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(False)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setAstro1Action.setEnabled(True)
        setAstro2Action.setEnabled(True)
        setAstro3Action.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setAstro1Action)
        menu.addAction(setAstro2Action)
        menu.addAction(setAstro3Action)

        return menu

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        self.scene().removeItem(self)
        self.scene().priceBarChartChanged.emit()

    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem pricebar.
        """

        pb = self.getPriceBar()
        
        dialog = PriceBarEditDialog(priceBar=pb, readOnly=True)

        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem pricebar.
        """

        pb = self.getPriceBar()
        
        dialog = PriceBarEditDialog(priceBar=pb, readOnly=False)

        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # Set the item with the new values.

            self.setPriceBar(dialog.getPriceBar())

            # X location based on the timestamp.
            x = self.scene().datetimeToSceneXPos(self.priceBar.timestamp)

            # Y location based on the mid price (average of high and low).
            y = self.scene().priceToSceneYPos(self.priceBar.midPrice())

            # Set the position, in parent coordinates.
            self.setPos(QPointF(x, y))

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()
            
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart1(self.scenePos().x())
        
    def _handleSetAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart2(self.scenePos().x())
        
    def _handleSetAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of this PriceBarGraphicsItem.
        """

        # The GraphicsItem's scene X position represents the time.
        self.scene().setAstroChart3(self.scenePos().x())
        
        
class PriceBarChartArtifactGraphicsItem(QGraphicsItem):
    """QGraphicsItem that has members to indicate and set the
    readOnly mode.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceBarChartArtifactGraphicsItem")
        
        self.readOnlyFlag = True
        self.artifact = None
        
    def setReadOnlyFlag(self, flag):
        self.readOnlyFlag = flag

    def getReadOnlyFlag(self):
        return self.readOnlyFlag

    def setArtifact(self, artifact):
        """Virtual function that is meant to be overwritten by a child class to
        implement the custom functionality of loading the internals of the
        PriceBarChart GraphicsItem, so that it may be displayed in the chart.

        Arguments:
        artifact - PriceBarChartArtifact object to store.
        """

        self.log.debug("Entered " + \
                       "PriceBarChartArtifactGraphicsItem.setArtifact()")

        self.artifact = artifact
        
        self.log.debug("Exiting " + \
                       "PriceBarChartArtifactGraphicsItem.setArtifact()")

    def getArtifact(self):
        """Returns the PriceBarChartArtifact associated with this
        PriceBarChartArtifactGraphicsItem.
        """

        self.log.debug("Entered " + \
                       "PriceBarChartArtifactGraphicsItem.getArtifact()")
        
        if artifact == None:
            raise TypeError("Expected artifact to be not None.")

        self.log.debug("Exiting " + \
                       "PriceBarChartArtifactGraphicsItem.getArtifact()")
        
        return artifact


class TextGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBarChartTextArtifact."""
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartTextArtifact object's data
        into this QGraphicsTextItem.

        Arguments:
        artifact - PriceBarChartTextArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entered setArtifact()")

        if isinstance(artifact, PriceBarChartTextArtifact):
            self.artifact = artifact
        
            # TODO:  Extract and set the internals according to the info 
            # in self.artifact.
        else:
            raise TypeError("Expected artifact type: PriceBarChartTextArtifact")
    
        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTextArtifact for this QGraphicsItem 
        so that it may be pickled.
        """

        self.log.debug("Entered getArtifact()")
        
        # TODO:  Update the internal self.priceBarChartTextArtifact to be 
        # current, then return it.
        
        return self.artifact

        self.log.debug("Exiting getArtifact()")
        

class GannFanUpperRightGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a GannFan opening in the upper 
    right direction.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

    def setArtifact(self, artifact):
        """Loads a given PriceBarChartGannFanUpperRightArtifact object's data
        into this QGraphicsTextItem.

        Arguments:
        artifact - PriceBarChartGannFanUpperRightArtifact object with
                   information about this TextGraphisItem.
        """

        self.log.debug("Entered setArtifact()")

        if isinstance(artifact, PriceBarChartGannFanUpperRightArtifact):
            self.artifact = artifact
        
            # TODO:  Extract and set the internals according to the info 
            # in self.artifact.
        else:
            errStr = "Expected artifact type: " + \
                     "PriceBarChartGannFanUpperRightArtifact"
            raise TypeError(errStr)
    
        self.log.debug("Exiting setArtifact()")

        
    def getArtifact(self):
        """Returns a PriceBarChartGannFanUpperRightArtifact for this
        QGraphicsItem so that it may be pickled.
        """

        self.log.debug("Entered getArtifact()")
        
        # TODO:  Update the internal self.artifact to be 
        # current, then return it.
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

class GannFanLowerRightGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a GannFan opening in the lower 
    right direction.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartGannFanLowerRightArtifact object's data
        into this QGraphicsTextItem.

        Arguments:
        artifact - PriceBarChartGannFanLowerRightArtifact object with
                   information about this TextGraphisItem.
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartGannFanLowerRightArtifact):
            self.artifact = artifact
        
            # TODO:  Extract and set the internals according to the info 
            # in self.artifact.
        else:
            errStr = "Expected artifact type: " + \
                     "PriceBarChartGannFanLowerRightArtifact"
            raise TypeError(errStr)
    
        self.log.debug("Exiting setArtifact()")

        
    def getArtifact(self):
        """Returns a PriceBarChartGannFanLowerRightArtifact for this
        QGraphicsItem so that it may be pickled.
        """

        self.log.debug("Entered getArtifact()")
        
        # TODO:  Update the internal self.artifact to be 
        # current, then return it.
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact
        
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
        self.artifact = PriceBarChartBarCountArtifact()

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
        self.clickScenePointF = None
        
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
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.startPointF.setX(round(self.startPointF.x()))
        self.endPointF = self.endPointF + posDelta
        self.endPointF.setX(round(self.endPointF.x()))

        if self.scene() != None:
            self.recalculateBarCount()
            self.update()

        self.log.debug("Exiting setPos()")
        
    def mousePressEvent(self, event):
        """Overwrites the QGraphicsItem mousePressEvent() function.

        Arguments:
        event - QGraphicsSceneMouseEvent that triggered this call.
        """

        self.log.debug("Entered mousePressEvent()")
        
        # If the item is in read-only mode, simply call the parent
        # implementation of this function.
        if self.getReadOnlyFlag() == True:
            self.log.debug("DEBUG: " + \
                           "getReadOnlyFlag() == True, so passing to super()")
            super().mousePressEvent(event)
        else:
            # If the mouse press is within 1/5th of the bar length to the
            # beginning or end points, then the user is trying to adjust
            # the starting or ending points of the bar counter ruler.
            scenePosX = event.scenePos().x()
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if scenePosX <= startThreshold:
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
            elif scenePosX >= endThreshold:
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
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
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                self.startPointF.y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              self.endPointF.y()))
                    self.update()
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

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)

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
            self.log.debug("Normalization of BarCountGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

        # Update the barCount label position.  For some reason, this
        # is required irregardless of the above if statement.  If we
        # don't do this, then some of the BarCountGraphicsItems
        # created can't be clicked on.  I'm not sure why that is...
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

    def setArtifact(self, artifact):
        """Loads a given PriceBarChartBarCountArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartBarCountArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartBarCountArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        # Need to recalculate the bar count, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the bar count will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateBarCount()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartBarCountArtifact for this QGraphicsItem 
        so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartBarCountArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

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

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this BarCountGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        BarCountGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("Select", parent)
        unselectAction = QAction("Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("Info", parent)
        editAction = QAction("Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart 1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart 2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart 3", parent)
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        self.scene().removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        self.scene().priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the BarCountGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the BarCountGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the BarCountGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the BarCountGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the BarCountGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the BarCountGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

        
class TimeMeasurementGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar counter in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new TimeMeasurementGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger("pricebarchart.TimeMeasurementGraphicsItem")
        self.log.debug("Entered __init__().")


        ############################################################
        # Set default values for preferences/settings.
        
        # Color of the bar count graphicsitems.
        self.timeMeasurementGraphicsItemColor = \
            SettingsKeys.timeMeasurementGraphicsItemColorSettingsDefValue

        # Color of the text that is associated with the bar count
        # graphicsitem.
        self.timeMeasurementGraphicsItemTextColor = \
            SettingsKeys.timeMeasurementGraphicsItemTextColorSettingsDefValue

        # Height of the vertical bar drawn.
        self.timeMeasurementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.timeMeasurementFontSize = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemFontSize 

        # X scaling of the text.
        self.timeMeasurementTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeMeasurementTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextYScaling 

        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartTimeMeasurementArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.timeMeasurementPenWidth = 0.0
        self.timeMeasurementPen = QPen()
        self.timeMeasurementPen.setColor(self.timeMeasurementGraphicsItemColor)
        self.timeMeasurementPen.setWidthF(self.timeMeasurementPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Number of trading days.
        self.numPriceBars = 0
        self.numCalendarDays = 0
        self.numWeeks = 0
        
        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.timeMeasurementBarsText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementCDText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementWeeksText = QGraphicsSimpleTextItem("", self)
        
        self.timeMeasurementBarsText.setPos(self.endPointF)
        self.timeMeasurementCDText.setPos(self.endPointF)
        self.timeMeasurementWeeksText.setPos(self.endPointF)
        
        # Set the font of the text.
        self.timeMeasurementTextFont = QFont("Andale Mono")
        self.timeMeasurementTextFont.setPointSizeF(self.timeMeasurementFontSize)

        self.timeMeasurementBarsText.setFont(self.timeMeasurementTextFont)
        self.timeMeasurementCDText.setFont(self.timeMeasurementTextFont)
        self.timeMeasurementWeeksText.setFont(self.timeMeasurementTextFont)
        
        # Set the pen color of the text.
        self.timeMeasurementTextPen = self.timeMeasurementBarsText.pen()
        self.timeMeasurementTextPen.setColor(self.timeMeasurementGraphicsItemTextColor)
        self.timeMeasurementBarsText.setPen(self.timeMeasurementTextPen)
        self.timeMeasurementCDText.setPen(self.timeMeasurementTextPen)
        self.timeMeasurementWeeksText.setPen(self.timeMeasurementTextPen)

        # Set the brush color of the text.
        self.timeMeasurementTextBrush = self.timeMeasurementBarsText.brush()
        self.timeMeasurementTextBrush.setColor(self.timeMeasurementGraphicsItemTextColor)
        self.timeMeasurementBarsText.setBrush(self.timeMeasurementTextBrush)
        self.timeMeasurementCDText.setBrush(self.timeMeasurementTextBrush)
        self.timeMeasurementWeeksText.setBrush(self.timeMeasurementTextBrush)

        # Apply some size scaling to the text.
        textTransform = QTransform()
        textTransform.scale(self.timeMeasurementTextXScaling, \
                            self.timeMeasurementTextYScaling)
        self.timeMeasurementBarsText.setTransform(textTransform)
        self.timeMeasurementCDText.setTransform(textTransform)
        self.timeMeasurementWeeksText.setTransform(textTransform)

        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.timeMeasurementGraphicsItemBarHeight = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.timeMeasurementFontSize = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemFontSize 

        # X scaling of the text.
        self.timeMeasurementTextXScaling = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeMeasurementTextYScaling = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemTextYScaling 

        # Set the font size of the text.
        self.log.debug("Setting font size to: {}".format(self.timeMeasurementFontSize))
        self.timeMeasurementTextFont = self.timeMeasurementBarsText.font()
        self.timeMeasurementTextFont.setPointSizeF(self.timeMeasurementFontSize)

        self.timeMeasurementBarsText.setFont(self.timeMeasurementTextFont)
        self.timeMeasurementCDText.setFont(self.timeMeasurementTextFont)
        self.timeMeasurementWeeksText.setFont(self.timeMeasurementTextFont)

        # Apply some size scaling to the text.
        self.log.debug("Setting transform: (dx={}, dy={})".\
                       format(self.timeMeasurementTextXScaling,
                              self.timeMeasurementTextYScaling))
        textTransform = QTransform()
        textTransform.scale(self.timeMeasurementTextXScaling, \
                            self.timeMeasurementTextYScaling)

        self.timeMeasurementBarsText.setTransform(textTransform)
        self.timeMeasurementCDText.setTransform(textTransform)
        self.timeMeasurementWeeksText.setTransform(textTransform)

        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        settings = QSettings()

        # timeMeasurementGraphicsItemColor
        key = SettingsKeys.timeMeasurementGraphicsItemColorSettingsKey
        defaultValue = \
            SettingsKeys.timeMeasurementGraphicsItemColorSettingsDefValue
        self.timeMeasurementGraphicsItemColor = \
            QColor(settings.value(key, defaultValue))

        # timeMeasurementGraphicsItemTextColor
        key = SettingsKeys.timeMeasurementGraphicsItemTextColorSettingsKey
        defaultValue = \
            SettingsKeys.timeMeasurementGraphicsItemTextColorSettingsDefValue
        self.timeMeasurementGraphicsItemTextColor = \
            QColor(settings.value(key, defaultValue))
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.startPointF.setX(round(self.startPointF.x()))
        self.endPointF = self.endPointF + posDelta
        self.endPointF.setX(round(self.endPointF.x()))

        if self.scene() != None:
            self.recalculateTimeMeasurement()
            self.update()

        self.log.debug("Exiting setPos()")
        
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
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if scenePosX <= startThreshold:
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
            elif scenePosX >= endThreshold:
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
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
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(QPointF(event.scenePos().x(),
                                                self.startPointF.y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(event.scenePos().x(),
                                              self.endPointF.y()))
                    self.update()
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

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)

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
        """

        x = pointF.x()

        newValue = QPointF(x, self.endPointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)
            
            # Update the timeMeasurement label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            x = deltaX / 2
            yBars  = -5.5 * self.timeMeasurementGraphicsItemBarHeight
            yCD    = -4.0 * self.timeMeasurementGraphicsItemBarHeight
            yWeeks = -2.5 * self.timeMeasurementGraphicsItemBarHeight
            self.timeMeasurementBarsText.setPos(QPointF(x, yBars))
            self.timeMeasurementCDText.setPos(QPointF(x, yCD))
            self.timeMeasurementWeeksText.setPos(QPointF(x, yWeeks))
            
            if self.scene() != None:
                # Re-calculate the bar count.
                self.recalculateTimeMeasurement()
                self.update()

    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        x = pointF.x()

        newValue = QPointF(x, self.startPointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the timeMeasurement label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            x = deltaX / 2
            yBars  = -5.5 * self.timeMeasurementGraphicsItemBarHeight
            yCD    = -4.0 * self.timeMeasurementGraphicsItemBarHeight
            yWeeks = -2.5 * self.timeMeasurementGraphicsItemBarHeight
            self.timeMeasurementBarsText.setPos(QPointF(x, yBars))
            self.timeMeasurementCDText.setPos(QPointF(x, yCD))
            self.timeMeasurementWeeksText.setPos(QPointF(x, yWeeks))
            
            if self.scene() != None:
                # Re-calculate the bar count.
                self.recalculateTimeMeasurement()
                self.update()


    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.x() > self.endPointF.x():
            self.log.debug("Normalization of TimeMeasurementGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

            # Update the timeMeasurement label position.
            deltaX = self.endPointF.x() - self.startPointF.x()
            x = deltaX / 2
            yBars  = -5.5 * self.timeMeasurementGraphicsItemBarHeight
            yCD    = -4.0 * self.timeMeasurementGraphicsItemBarHeight
            yWeeks = -2.5 * self.timeMeasurementGraphicsItemBarHeight
            self.timeMeasurementBarsText.setPos(QPointF(x, yBars))
            self.timeMeasurementCDText.setPos(QPointF(x, yCD))
            self.timeMeasurementWeeksText.setPos(QPointF(x, yWeeks))

            self.recalculateTimeMeasurement()
            
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

    def recalculateTimeMeasurement(self):
        """Sets the internal variables:
        
            self.numPriceBars
            self.numCalendarDays
            self.numWeeks

        to hold the amount of time between the start and end points.
        """

        scene = self.scene()

        if scene == None:
            self.numPriceBars = 0
            self.numCalendarDays = 0
            self.numWeeks = 0
        else:
            # Get all the QGraphicsItems.
            graphicsItems = scene.items()

            # Reset the values.
            self.numPriceBars = 0
            self.numCalendarDays = 0
            self.numWeeks = 0

            # Go through the PriceBarGraphicsItems and count the bars in
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

                        self.numPriceBars += 1
        
            # Calculate the number of calendar days.
            startTimestamp = \
                scene.sceneXPosToDatetime(self.startPointF.x())
            timestampStr = Ephemeris.datetimeToDayStr(startTimestamp)
            
            self.log.debug("startTimestamp: " + timestampStr)
            
            endTimestamp = \
                scene.sceneXPosToDatetime(self.endPointF.x())
            timestampStr = Ephemeris.datetimeToDayStr(endTimestamp)
            
            self.log.debug("endTimestamp: " + timestampStr)
            
            timeDelta = endTimestamp - startTimestamp
            
            self.log.debug("timeDelta is: " + timeDelta.__str__())
            
            self.numCalendarDays = timeDelta.days
            self.numCalendarDays += (timeDelta.seconds / 86400.0)

            # Calculate number of weeks.
            self.numWeeks = self.numCalendarDays / 7.0
            
        # Update the text of the self.timeMeasurementText.
        barsText = "{} Bars".format(self.numPriceBars)
        cdText = "{:.2f} CD".format(self.numCalendarDays)
        weeksText = "{:.2f} Weeks".format(self.numWeeks)
        
        self.timeMeasurementBarsText.setText(barsText)
        self.timeMeasurementCDText.setText(cdText)
        self.timeMeasurementWeeksText.setText(weeksText)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartTimeMeasurementArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartTimeMeasurementArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartTimeMeasurementArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartTimeMeasurementArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        # Need to recalculate the time measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the time measurements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateTimeMeasurement()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTimeMeasurementArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartTimeMeasurementArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

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
            QPointF(0.0, -1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight / 2.0))
        
        bottomRight = \
            QPointF(xDelta, 1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight / 2.0))
        
        rectWithoutText = QRectF(topLeft, bottomRight)

        return rectWithoutText

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.timeMeasurementPen:
            painter.setPen(self.timeMeasurementPen)
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        x2 = 0.0
        y2 = -1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the middle horizontal line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.timeMeasurementPen.widthF() / 2.0;
            
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

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this TimeMeasurementGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        TimeMeasurementGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("Select", parent)
        unselectAction = QAction("Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("Info", parent)
        editAction = QAction("Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart 1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart 2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart 3", parent)
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        self.scene().removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        self.scene().priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeMeasurementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeMeasurementArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then the underlying artifact
            # object was modified.  Set the artifact to this
            # PriceBarChartArtifactGraphicsItem, which will cause it to be
            # reloaded in the scene.
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the TimeMeasurementGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

        
class ModalScaleGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar counter in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new ModalScaleGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger("pricebarchart.ModalScaleGraphicsItem")
        self.log.debug("Entered __init__().")


        ############################################################
        # Set default values for preferences/settings.
        
        # Color of the bar count graphicsitems.
        self.modalScaleGraphicsItemColor = \
            SettingsKeys.modalScaleGraphicsItemColorSettingsDefValue

        # Color of the text that is associated with the bar count
        # graphicsitem.
        self.modalScaleGraphicsItemTextColor = \
            SettingsKeys.modalScaleGraphicsItemTextColorSettingsDefValue

        # Height of the vertical bar drawn.
        self.modalScaleGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.modalScaleFontSize = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemFontSize 

        # X scaling of the text.
        self.modalScaleTextXScaling = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.modalScaleTextYScaling = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemTextYScaling 

        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartModalScaleArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.modalScalePenWidth = 0.0
        self.modalScalePen = QPen()
        self.modalScalePen.setColor(self.modalScaleGraphicsItemColor)
        self.modalScalePen.setWidthF(self.modalScalePenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Dummy item.
        self.modalScaleBarsText = QGraphicsSimpleTextItem("", self)
        
        # Set the font of the text.
        self.modalScaleTextFont = QFont("Andale Mono")
        self.modalScaleTextFont.setPointSizeF(self.modalScaleFontSize)

        # Set the pen color of the text.
        self.modalScaleTextPen = self.modalScaleBarsText.pen()
        self.modalScaleTextPen.setColor(self.modalScaleGraphicsItemTextColor)

        # Set the brush color of the text.
        self.modalScaleTextBrush = self.modalScaleBarsText.brush()
        self.modalScaleTextBrush.setColor(self.modalScaleGraphicsItemTextColor)

        # Size scaling for the text.
        textTransform = QTransform()
        textTransform.scale(self.modalScaleTextXScaling, \
                            self.modalScaleTextYScaling)
        
        # Below is a 2-dimensional list of (3
        # QGraphicsSimpleTextItems), for each of the MusicalRatios in
        # the PriceBarChartModalScaleArtifact.  The 3 texts displayed
        # for each MusicalRatio is:
        #
        # 1) Fraction (or float if no numerator and no denominator is set).
        # 2) Price value.
        # 3) Timestamp value.
        #
        self.musicalRatioTextItems = []

        # Initialize to blank and set at the end point.
        for musicalRatio in range(len(self.artifact.getMusicalRatios())):
            fractionTextItem = QGraphicsSimpleTextItem("", self)
            fractionTextItem.setPos(self.endPointF)
            fractionTextItem.setFont(self.modalScaleTextFont)
            fractionTextItem.setPen(self.modalScaleTextPen)
            fractionTextItem.setBrush(self.modalScaleTextBrush)
            fractionTextItem.setTransform(textTransform)
            
            priceTextItem = QGraphicsSimpleTextItem("", self)
            priceTextItem.setPos(self.endPointF)
            priceTextItem.setFont(self.modalScaleTextFont)
            priceTextItem.setPen(self.modalScaleTextPen)
            priceTextItem.setBrush(self.modalScaleTextBrush)
            priceTextItem.setTransform(textTransform)
            
            timestampTextItem = QGraphicsSimpleTextItem("", self)
            timestampTextItem.setPos(self.endPointF)
            timestampTextItem.setFont(self.modalScaleTextFont)
            timestampTextItem.setPen(self.modalScaleTextPen)
            timestampTextItem.setBrush(self.modalScaleTextBrush)
            timestampTextItem.setTransform(textTransform)
            
            self.musicalRatioTextItems.\
                append([fractionTextItem, priceTextItem, timestampTextItem])

        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.modalScaleGraphicsItemBarHeight = \
            priceBarChartSettings.\
                modalScaleGraphicsItemBarHeight 
 
        # Font size of the text of the bar count.
        self.modalScaleFontSize = \
            priceBarChartSettings.\
                modalScaleGraphicsItemFontSize 

        # X scaling of the text.
        self.modalScaleTextXScaling = \
            priceBarChartSettings.\
                modalScaleGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.modalScaleTextYScaling = \
            priceBarChartSettings.\
                modalScaleGraphicsItemTextYScaling 

        # Font size of the text.
        self.log.debug("Setting font size to: {}".\
                       format(self.modalScaleFontSize))
        self.modalScaleTextFont = self.modalScaleBarsText.font()
        self.modalScaleTextFont.setPointSizeF(self.modalScaleFontSize)

        # Apply some size scaling to the text.
        self.log.debug("Setting transform: (dx={}, dy={})".\
                       format(self.modalScaleTextXScaling,
                              self.modalScaleTextYScaling))
        textTransform = QTransform()
        textTransform.scale(self.modalScaleTextXScaling, \
                            self.modalScaleTextYScaling)

        # Traverse the 2-dimensional list and set each of the text items.
        for i in range(len(self.musicalRatioTextItems)):
            listOfTextItems = self.musicalRatioTextItems[i]
            
            for j in range(len(listOfTextItems)):
                textItem = listOfTextItems[j]
                textItem.setFont(self.modalScaleTextFont)
                textItem.setPen(self.modalScaleTextPen)
                textItem.setBrush(self.modalScaleTextBrush)
                textItem.setTransform(textTransform)

        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        settings = QSettings()

        # modalScaleGraphicsItemColor
        key = SettingsKeys.modalScaleGraphicsItemColorSettingsKey
        defaultValue = \
            SettingsKeys.modalScaleGraphicsItemColorSettingsDefValue
        self.modalScaleGraphicsItemColor = \
            QColor(settings.value(key, defaultValue))

        # modalScaleGraphicsItemTextColor
        key = SettingsKeys.modalScaleGraphicsItemTextColorSettingsKey
        defaultValue = \
            SettingsKeys.modalScaleGraphicsItemTextColorSettingsDefValue
        self.modalScaleGraphicsItemTextColor = \
            QColor(settings.value(key, defaultValue))
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Here we use the new position to re-set the self.startPointF and
        self.endPointF.

        Arguments:
        pos - QPointF holding the new position.
        """
        self.log.debug("Entered setPos()")
        
        super().setPos(pos)

        newScenePos = pos

        posDelta = newScenePos - self.startPointF

        # Update the start and end points accordingly. 
        self.startPointF = self.startPointF + posDelta
        self.endPointF = self.endPointF + posDelta

        if self.scene() != None:
            self.refreshTextItems()
            self.update()

        self.log.debug("Exiting setPos()")
        
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
            self.log.debug("DEBUG: scenePosX={}".format(scenePosX))
            
            startingPointX = self.startPointF.x()
            self.log.debug("DEBUG: startingPointX={}".format(startingPointX))
            endingPointX = self.endPointF.x()
            self.log.debug("DEBUG: endingPointX={}".format(endingPointX))
            
            diff = endingPointX - startingPointX
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointX + (diff * (1.0 / 5))
            endThreshold = endingPointX - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if scenePosX <= startThreshold:
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
            elif scenePosX >= endThreshold:
                self.draggingEndPointFlag = True
                self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                               format(self.draggingEndPointFlag))
            else:
                # The mouse has clicked the middle part of the
                # QGraphicsItem, so pass the event to the parent, because
                # the user wants to either select or drag-move the
                # position of the QGraphicsItem.
                self.log.debug("DEBUG:  Middle part clicked.  " + \
                               "Passing to super().")

                # Save the click position, so that if it is a drag, we
                # can have something to reference from for setting the
                # start and end positions when the user finally
                # releases the mouse button.
                self.clickScenePointF = event.scenePos()
                
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
                    self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                                   format(self.draggingStartPointFlag))
                    self.setStartPointF(event.scenePos())
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(event.scenePos())
                    self.update()
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

        if self.draggingStartPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " + \
                           "startPoint.")
            
            self.draggingStartPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.scene().priceBarChartChanged.emit()
            
        else:
            self.log.debug("mouseReleaseEvent() when NOT previously " + \
                           "dragging an end.")

            if self.getReadOnlyFlag() == False:
                # Update the start and end positions.
                self.log.debug("DEBUG: scenePos: x={}, y={}".
                               format(event.scenePos().x(),
                                      event.scenePos().y()))

                # Calculate the difference between where the user released
                # the button and where the user first clicked the item.
                delta = event.scenePos() - self.clickScenePointF

                self.log.debug("DEBUG: delta: x={}, y={}".
                               format(delta.x(), delta.y()))

                # If the delta is not zero, then update the start and
                # end points by calling setPos() on the new calculated
                # position.
                if delta.x() != 0.0 and delta.y() != 0.0:
                    newPos = self.startPointF + delta
                    self.setPos(newPos)

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

    def refreshTextItems(self):
        """Sets the positions of the text items for the MusicalRatios,
        and updates the text so that they are current.
        """

        # Update the modalScale label text item texts.
        if self.scene() != None:
            self.recalculateModalScale()

            # Traverse the 2-dimensional list and set the position of
            # each of the text items.
            artifact = self.getArtifact()
            for i in range(len(self.musicalRatioTextItems)):
                # Get the MusicalRatio that corresponds to this index.
                musicalRatio = artifact.getMusicalRatios()[i]

                # Verify it is enabled.  If yes, then set the
                # position, otherwise, ignore.
                if musicalRatio.isEnabled() == True:
                    # Get the x and y position that will be the new
                    # position of the text item.
                    (x, y) = artifact.getXYForMusicalRatio(i)

                    # Map those x and y to local coordinates.
                    pointF = self.mapFromScene(QPointF(x, y))
                    
                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]

                    # For each text item for that point on the scale,
                    # set the position.
                    for i in range(len(listOfTextItems)):
                        textItem = listOfTextItems[i]
                        # The position set is not exactly at (x, y),
                        # but instead at an offset slightly below that
                        # point so that multiple texts dont' overlap
                        # each other.
                        offsetY = self.modalScaleGraphicsItemBarHeight * i
                        textItem.setPos(QPointF(pointF.x(),
                                                pointF.y() + offsetY))

            # Call update on this item since positions and child items
            # were updated.
            self.update()

    def setStartPointF(self, pointF):
        """Sets the starting point of the modalScale.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.startPointF != pointF: 
            self.startPointF = pointF

            self.setPos(self.startPointF)
            
            # Update the modalScale label text item positions.
            self.refreshTextItems()            

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.update()

    def setEndPointF(self, pointF):
        """Sets the ending point of the modalScale.  The value passed in
        is the mouse location in scene coordinates.  
        """

        if self.endPointF != pointF:
            self.endPointF = pointF

            self.log.debug("ModalScaleGraphicsItem." +
                           "setEndPointF(QPointF({}, {}))".\
                           format(pointF.x(), pointF.y()))
            
            # Update the modalScale label text item positions.
            self.refreshTextItems()

            # Call update on this item since positions and child items
            # were updated.
            if self.scene() != None:
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.x() > self.endPointF.x():
            self.log.debug("Normalization of ModalScaleGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

            # TODO: not sure if this should go here or after the
            # self.refreshTextItems() call.  Test this to code to make
            # sure the following use case works:
            #
            #  1)  create a ModalScaleGraphicsItem via the tool mode
            #  2) Switch to PointerTool mode.
            #  3) Try to select the middle of the ModalScaleGraphicsItem
            #     that was created.
            #  4) Verify that it can be selected (dotted line outline)
            #     on the first click.
            #
            
            super().setPos(self.startPointF)
            
            # Update the modalScale label text item positions.
            self.refreshTextItems()
            

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

    def recalculateModalScale(self):
        """Updates the text items that represent the ticks on the
        modal scale.  These texts will have accurate values for where
        the notes are in terms of price and time.

        In this process, it also sets the internal variables such that
        a call to self.getArtifact().getXYForMusicalRatio(index) can
        be made and a value returned that is accurate.
        """

        scene = self.scene()

        if scene != None:
            artifact = self.getArtifact()
            musicalRatios = artifact.getMusicalRatios()
            for i in range(len(musicalRatios)):
                musicalRatio = musicalRatios[i]

                if musicalRatio.isEnabled():
                    # Enable and make visible.
                    
                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]
                    
                    # For the text items for that point on the scale,
                    # set the text.  
                    for j in range(len(listOfTextItems)):
                        textItem = listOfTextItems[j]
                        
                        # Enable and make visible.
                        textItem.setEnabled(True)
                        textItem.setVisible(True)
                        
                        if j == 0:
                            # Fraction text.  This is either the
                            # fraction (if the numerator and
                            # denominator are available), or the float
                            # value for the ratio.
                            
                            numerator = musicalRatio.getNumerator()
                            denominator = musicalRatio.getDenominator()
                            
                            if numerator != None and denominator != None:
                                fractionText = \
                                    "{}/{}".format(numerator, denominator)
                                textItem.setText(fractionText)
                            else:
                                ratio = musicalRatio.getRatio()
                                ratioText = "{}".format(ratio)
                                textItem.setText(ratioText)
                        elif j == 1:
                            # Price text.
                            
                            # Get the y location and then convert to a price.
                            (x, y) = artifact.getXYForMusicalRatio(i)
                            price = self.scene().sceneYPosToPrice(y)
                            priceText = "{}".format(price)
                            textItem.setText(priceText)
                        elif j == 2:
                            # Timestamp text.
                            
                            # Get the x location and then convert to a datetime.
                            (x, y) = artifact.getXYForMusicalRatio(i)
                            timestamp = \
                                self.scene().sceneXPosToDatetime(x)
                            timestampText = \
                                Ephemeris.datetimeToDayStr(timestamp)
                            textItem.setText(timestampText)
                else:
                    # Disable and make not visable.
                    
                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]
                    
                    # For each text item for that point on the scale,
                    # set as disabled and not visible.
                    for i in range(len(listOfTextItems)):
                        textItem = listOfTextItems[i]
                        textItem.setEnabled(False)
                        textItem.setVisible(False)
                        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartModalScaleArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartModalScaleArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartModalScaleArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartModalScaleArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        # Need to recalculate the time measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the measurements will be zero.
        self.refreshTextItems()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartModalScaleArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartModalScaleArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the vertical bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.

        # The QRectF returned is relative to this (0, 0) point.

        xTopLeft = 0.0
        yTopLeft = 1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)
        
        xBottomLeft = 0.0
        yBottomLeft = -1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopRight = 0.0 + xDelta
        yTopRight = (1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)) + \
            yDelta
        
        xBottomRight = 0.0 + xDelta
        yBottomRight = (-1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)) + \
            yDelta

        # Find the smallest x and y.
        smallestX = xTopLeft
        if xTopLeft < smallestX:
            smallestX = xTopLeft
        if xBottomLeft < smallestX:
            smallestX = xBottomLeft
        if xTopRight < smallestX:
            smallestX = xTopRight
        if xBottomRight < smallestX:
            smallestX = xBottomRight
            
        smallestY = yTopLeft
        if yTopLeft < smallestY:
            smallestY = yTopLeft
        if yBottomLeft < smallestY:
            smallestY = yBottomLeft
        if yTopRight < smallestY:
            smallestY = yTopRight
        if yBottomRight < smallestY:
            smallestY = yBottomRight
            
        # Find the largest x and y.
        largestX = xTopLeft
        if xTopLeft > largestX:
            largestX = xTopLeft
        if xBottomLeft > largestX:
            largestX = xBottomLeft
        if xTopRight > largestX:
            largestX = xTopRight
        if xBottomRight > largestX:
            largestX = xBottomRight
            
        largestY = yTopLeft
        if yTopLeft > largestY:
            largestY = yTopLeft
        if yBottomLeft > largestY:
            largestY = yBottomLeft
        if yTopRight > largestY:
            largestY = yTopRight
        if yBottomRight > largestY:
            largestY = yBottomRight

        rectWithoutText = QRectF(QPointF(smallestX, smallestY),
                                 QPointF(largestX, largestY)).normalized()

        self.log.debug("smallestX = {}, ".format(smallestX) +
                       "smallestY = {}, ".format(smallestY) +
                       "largestX = {}, ".format(largestX) +
                       "largestY = {}".format(largestY))
        
        return rectWithoutText

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.
        """

        # The QRectF returned is relative to this (0, 0) point.

        xTopLeft = 0.0
        yTopLeft = 1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)
        topLeft = QPointF(xTopLeft, yTopLeft)
        
        xBottomLeft = 0.0
        yBottomLeft = -1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)
        bottomLeft = QPointF(xBottomLeft, yBottomLeft)
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopRight = 0.0 + xDelta
        yTopRight = (1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)) + \
            yDelta
        topRight = QPointF(xTopRight, yTopRight)
        
        xBottomRight = 0.0 + xDelta
        yBottomRight = (-1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)) + \
            yDelta
        bottomRight = QPointF(xBottomRight, yBottomRight)

        points = [topLeft, topRight, bottomRight, bottomLeft]
        polygon = QPolygonF(points)

        painterPath = QPainterPath()
        painterPath.addPolygon(polygon)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.modalScalePen:
            painter.setPen(self.modalScalePen)
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)
        x2 = 0.0
        y2 = -1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = 0.0 + xDelta
        y1 = (1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)) + yDelta
        x2 = 0.0 + xDelta
        y2 = (-1.0 * (self.modalScaleGraphicsItemBarHeight / 2.0)) + yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the middle line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.modalScalePen.widthF() / 2.0;
            
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
            painter.drawPath(self.shape())
            #painter.drawRect(self.boundingRect())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())
            #painter.drawRect(self.boundingRect())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this ModalScaleGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        ModalScaleGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("Select", parent)
        unselectAction = QAction("Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("Info", parent)
        editAction = QAction("Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart 1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart 2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart 3", parent)
        setEndOnAstro1Action = \
            QAction("Set end timestamp on Astro Chart 1", parent)
        setEndOnAstro2Action = \
            QAction("Set end timestamp on Astro Chart 2", parent)
        setEndOnAstro3Action = \
            QAction("Set end timestamp on Astro Chart 3", parent)
        
        selectAction.triggered.\
            connect(self._handleSelectAction)
        unselectAction.triggered.\
            connect(self._handleUnselectAction)
        removeAction.triggered.\
            connect(self._handleRemoveAction)
        infoAction.triggered.\
            connect(self._handleInfoAction)
        editAction.triggered.\
            connect(self._handleEditAction)
        setStartOnAstro1Action.triggered.\
            connect(self._handleSetStartOnAstro1Action)
        setStartOnAstro2Action.triggered.\
            connect(self._handleSetStartOnAstro2Action)
        setStartOnAstro3Action.triggered.\
            connect(self._handleSetStartOnAstro3Action)
        setEndOnAstro1Action.triggered.\
            connect(self._handleSetEndOnAstro1Action)
        setEndOnAstro2Action.triggered.\
            connect(self._handleSetEndOnAstro2Action)
        setEndOnAstro3Action.triggered.\
            connect(self._handleSetEndOnAstro3Action)
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)
        setEndOnAstro1Action.setEnabled(True)
        setEndOnAstro2Action.setEnabled(True)
        setEndOnAstro3Action.setEnabled(True)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        self.scene().removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        self.scene().priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartModalScaleArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=True)
        
        # Run the dialog.  We don't care about what is returned
        # because the dialog is read-only.
        rv = dialog.exec_()
        
    def _handleEditAction(self):
        """Causes a dialog to be executed to edit information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartModalScaleArtifactEditDialog(artifact,
                                                         self.scene(),
                                                         readOnlyFlag=False)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # If the dialog is accepted then get the new artifact and
            # set it to this PriceBarChartArtifactGraphicsItem, which
            # will cause it to be reloaded in the scene.
            artifact = dialog.getArtifact()
            self.setArtifact(artifact)

            # Flag that a redraw of this QGraphicsItem is required.
            self.update()

            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        else:
            # The user canceled so don't change anything.
            pass
        
    def _handleSetStartOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the start the ModalScaleGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the ModalScaleGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the ModalScaleGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the ModalScaleGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the ModalScaleGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the ModalScaleGraphicsItem.
        """

        self.scene().setAstroChart3(self.endPointF.x())

        
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

    # Signal emitted when the user desires to change astro chart 1.
    astroChart1Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 2.
    astroChart2Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 3.
    astroChart3Update = QtCore.pyqtSignal(datetime.datetime)
    
    
    # Tool modes that this widget can be in.
    ToolMode = {"ReadOnlyPointerTool" : 0,
                "PointerTool"         : 1,
                "HandTool"            : 2,
                "ZoomInTool"          : 3,
                "ZoomOutTool"         : 4,
                "BarCountTool"        : 5,
                "TimeMeasurementTool" : 6,
                "ModalScaleTool" : 7 }



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
        
        localizedTimestampStr = "Mouse time: "
        utcTimestampStr = "Mouse time: "
        priceStr = "Mouse price: " 
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
        self.selectedPriceBarTimestampLabel.setFont(smallFont)
        self.selectedPriceBarOpenPriceLabel.setFont(smallFont)
        self.selectedPriceBarHighPriceLabel.setFont(smallFont)
        self.selectedPriceBarLowPriceLabel.setFont(smallFont)
        self.selectedPriceBarClosePriceLabel.setFont(smallFont)

        # Set the cursor timestamp labels as being in a monospaced font.
        smallCourierFont = QFont()
        smallCourierFont.setFamily("Courier")
        smallCourierFont.setPointSize(7)
        self.cursorLocalizedTimestampLabel.setFont(smallCourierFont)
        self.cursorUtcTimestampLabel.setFont(smallCourierFont)
        self.cursorPriceLabel.setFont(smallCourierFont)
        
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

        # Bubble up the signal emission to update the time of the astro charts.
        self.graphicsScene.astroChart1Update.\
            connect(self.astroChart1Update)
        self.graphicsScene.astroChart2Update.\
            connect(self.astroChart2Update)
        self.graphicsScene.astroChart3Update.\
            connect(self.astroChart3Update)
        
        self.log.debug("Leaving __init__()")

    def setTimezone(self, timezone):
        """Sets the timezone used.  This is used for converting mouse
        X location to a datetime.datetime object.
        
        Arguments:
            
        timezone - A datetime.tzinfo object holding the timezone for the
                   pricebars in this widget.
        """

        self.timezone = timezone

        # The PriceBarChartGraphicsScene is actually the object that
        # does the conversions.  Pass the timezone info to that object.
        self.graphicsScene.setTimezone(self.timezone)

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
        timestampStr = "First PriceBar Timestamp: "
        
        if priceBar != None:
            timestampStr += Ephemeris.datetimeToDayStr(priceBar.timestamp)

        self.firstPriceBarTimestampLabel.setText(timestampStr)

    def updateLastPriceBarTimestampLabel(self, priceBar=None):
        """Updates the QLabel holding the timestamp of the last PriceBar
        in the pricebarchart.

        Arguments:

        priceBar - PriceBar object to use for updating the timestamp.  
                   If this argument is None, then the label text will be
                   blank.
        """

        timestampStr = "Last PriceBar Timestamp: "
        
        if priceBar != None:
            timestampStr += Ephemeris.datetimeToDayStr(priceBar.timestamp)
        
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

        localizedTimestampStr = "Mouse time: "
        utcTimestampStr = "Mouse time: "
        priceStr = "Mouse price: " 

        # Set the values if the X and Y positions are valid.
        if sceneXPos != None and sceneYPos != None:

            # Convert coordinate to the actual values they represent.
            timestamp = self.graphicsScene.sceneXPosToDatetime(sceneXPos)
            price = self.graphicsScene.sceneYPosToPrice(sceneYPos)

            # Append to the strings.
            localizedTimestampStr += Ephemeris.datetimeToDayStr(timestamp)
            utcTimestampStr += \
                Ephemeris.datetimeToDayStr(timestamp.astimezone(pytz.utc))
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

        timestampStr = "Timestamp: "
        openStr = "Open: "
        highStr = "High: "
        lowStr = "Low: "
        closeStr = "Close: "

        if priceBar != None:
            timestampStr += Ephemeris.datetimeToDayStr(priceBar.timestamp)
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
            x = self.graphicsScene.datetimeToSceneXPos(priceBar.timestamp)

            # Y location based on the mid price (average of high and low).
            y = self.graphicsScene.priceToSceneYPos(priceBar.midPrice())

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
            if isinstance(item, PriceBarChartArtifactGraphicsItem):
                artifacts.append(item.getArtifact())

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
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate bar count, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculateBarCount()
        
                addedItemFlag = True
                
            elif isinstance(artifact, PriceBarChartTimeMeasurementArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = TimeMeasurementGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate time measurement, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculateTimeMeasurement()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartModalScaleArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = ModalScaleGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate musicalRatios in the scale,
                # since it wasn't in the QGraphicsScene until now.
                newItem.refreshTextItems()
        
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
            elif isinstance(item, TimeMeasurementGraphicsItem):
                self.log.debug("Applying settings to " +
                               "TimeMeasurementGraphicsItem.")
                item.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
            elif isinstance(item, ModalScaleGraphicsItem):
                self.log.debug("Applying settings to " +
                               "ModalScaleGraphicsItem.")
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


    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.log.debug("Entered toTimeMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['TimeMeasurementTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['TimeMeasurementTool']
            self.graphicsView.toTimeMeasurementToolMode()

        self.log.debug("Exiting toTimeMeasurementToolMode()")

    def toModalScaleToolMode(self):
        """Changes the tool mode to be the ModalScaleTool."""

        self.log.debug("Entered toModalScaleToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['ModalScaleTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['ModalScaleTool']
            self.graphicsView.toModalScaleToolMode()

        self.log.debug("Exiting toModalScaleToolMode()")

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
        dt = self.graphicsScene.sceneXPosToDatetime(x)
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

    # Signal emitted when the user desires to change astro chart 1.
    astroChart1Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 2.
    astroChart2Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 3.
    astroChart3Update = QtCore.pyqtSignal(datetime.datetime)
    
    def __init__(self, parent=None):
        """Pass-through to the QGraphicsScene constructor."""

        super().__init__(parent)

        # Holds the timezone as a datetime.tzinfo object.  This is
        # used in conversions of scene position X value to
        # datetime.datetime.
        self.timezone = pytz.utc
        
        # Adding or removing an artifact graphics item counts as
        # something changed.
        self.priceBarChartArtifactGraphicsItemAdded.\
            connect(self.priceBarChartChanged)
        self.priceBarChartArtifactGraphicsItemRemoved.\
            connect(self.priceBarChartChanged)

    def setTimezone(self, timezone):
        """Sets the timezone used.  This is used for converting mouse
        X location to a datetime.datetime object.
        
        Arguments:
            
        timezone - A datetime.tzinfo object holding the timezone for the
                   pricebars in this widget.
        """

        self.timezone = timezone
    
    def sceneXPosToDatetime(self, sceneXPos):
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
    
    def sceneYPosToPrice(self, sceneYPos):
        """Returns a price value for the given Y position in scene
        coordinates.

        Arguments:

        sceneYPos - float value holding the Y position in scene
        coordinates.

        Returns:

        float value for the price that this Y position represents.
        """

        # Make sure I don't return a negative 0.0.
        if (sceneYPos != 0.0):
            return float(-1.0 * sceneYPos)
        else:
            return float(sceneYPos)

    def datetimeToSceneXPos(self, dt):
        """Returns the conversion from datetime.datetime object to what we
        chosen the X coordinate values to be.

        Arguments:

        dt - datetime.datetime object that holds a timestamp.

        Returns:

        float value for the X position that would match up with this timestamp.
        """

        return Ephemeris.datetimeToJulianDay(dt)

    def priceToSceneYPos(self, price):
        """Returns the conversion from price to what we have chosen the Y
        coordinate values to be.

        Arguments:

        price - float value holding the price value.

        Returns:

        float value for the Y position that would match up with this price.
        """

        # Make sure I don't return a negative 0.0.
        if (price != 0.0):
            return float(-1.0 * price)
        else:
            return float(price)


    def setAstroChart1(self, x):
        """Emits the astroChart1Update signal so that an external
        astrology chart can be plotted with a timestamp.

        Arguments:
        
        x - float value for the X position in the QGraphicsScene.  The
            X value represents a certain timestamp (unconverted).
            This function will do the necessary conversion from X
            value to datetime.datetime timestamp.
        """

        # Convert from X to datetime.datetime.
        dt = self.sceneXPosToDatetime(x)
        
        # Emit the desired signal so that the astrology chart can be
        # plotted for this datetime.datetime.
        self.astroChart1Update.emit(dt)
        
    def setAstroChart2(self, x):
        """Emits the astroChart2Update signal so that an external
        astrology chart can be plotted with a timestamp.

        Arguments:
        
        x - float value for the X position in the QGraphicsScene.  The
            X value represents a certain timestamp (unconverted).
            This function will do the necessary conversion from X
            value to datetime.datetime timestamp.
        """

        # Convert from X to datetime.datetime.
        dt = self.sceneXPosToDatetime(x)
        
        # Emit the desired signal so that the astrology chart can be
        # plotted for this datetime.datetime.
        self.astroChart2Update.emit(dt)
        
    def setAstroChart3(self, x):
        """Emits the astroChart3Update signal so that an external
        astrology chart can be plotted with a timestamp.

        Arguments:
        
        x - float value for the X position in the QGraphicsScene.  The
            X value represents a certain timestamp (unconverted).
            This function will do the necessary conversion from X
            value to datetime.datetime timestamp.
        """

        # Convert from X to datetime.datetime.
        dt = self.sceneXPosToDatetime(x)
        
        # Emit the desired signal so that the astrology chart can be
        # plotted for this datetime.datetime.
        self.astroChart3Update.emit(dt)
        
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
                "BarCountTool"        : 5,
                "TimeMeasurementTool" : 6,
                "ModalScaleTool"      : 7 }

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

        # Variable used for storing the new TimeMeasurementGraphicsItem,
        # as it is modified in TimeMeasurementToolMode.
        self.timeMeasurementGraphicsItem = None

        # Variable used for storing the new ModalScaleGraphicsItem,
        # as it is modified in ModalScaleToolMode.
        self.modalScaleGraphicsItem = None

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

        #self.log.debug("setGraphicsItemFlagsPerCurrToolMode(): " +
        #               "toolMode == {}.  ".format(self.toolMode) +
        #               "type(item) == {}.  ".format(type(item)) +
        #               "item is of type PriceBarGraphicsItem: {}.  ".\
        #               format(isinstance(item, PriceBarGraphicsItem)) +
        #               "item is of type PriceBarChartArtifactGraphicsItem: " +
        #               "{}.".
        #               format(isinstance(item,
        #                                 PriceBarChartArtifactGraphicsItem)))
                       
        if self.toolMode == \
               PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            if isinstance(item, PriceBarGraphicsItem):
                flags = QGraphicsItem.GraphicsItemFlags(QGraphicsItem.
                                                        ItemIsSelectable)
                item.setFlags(flags)
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                flags = QGraphicsItem.\
                    GraphicsItemFlags(QGraphicsItem.ItemIsSelectable)
                item.setFlags(flags)
                
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:
             
            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(False)

                flags = QGraphicsItem.\
                    GraphicsItemFlags(QGraphicsItem.ItemIsMovable +
                                      QGraphicsItem.ItemIsSelectable)
                item.setFlags(flags)
                
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

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']:

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

    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.log.debug("Entered toTimeMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.timeMeasurementGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toTimeMeasurementToolMode()")

    def toModalScaleToolMode(self):
        """Changes the tool mode to be the ModalScaleTool."""

        self.log.debug("Entered toModalScaleToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.modalScaleGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toModalScaleToolMode()")

    def createContextMenu(self, clickPosF, readOnlyFlag):
        """Creates a context menu for a right-click somewhere in
        the QGraphicsView, and returns it.

        Arguments:
        clickPosF - QPointF object of the right-click location,
            in scene coordinates.
        readOnlyFlag - bool value that indicates whether or not to
            bring up the menu options for the readonly
            mode or not.
        """

        scene = self.scene()

        # See if the user has right clicked on a QGraphicsItem.
        items = scene.items(clickPosF,
                            Qt.ContainsItemBoundingRect,
                            Qt.AscendingOrder)

        # Here count the number of items at this position that
        # we care about for creating a context menu for.
        debugLogStr = ""
        numContextSubMenuItems = 0

        menu = QMenu(self)
        menu.setTitle("PriceBarChartGraphicsView context menu")
        parent = None

        
        for item in items:
            if isinstance(item, PriceBarGraphicsItem):
                debugLogStr += \
                    "PriceBarGraphicsItem with PriceBar: " + \
                    item.priceBar.toString() + ". "
                
                numContextSubMenuItems += 1

                # Add the menu for this item.  We create the menu this
                # way so that 'submenu' is owned by 'menu'.
                submenu = menu.addMenu("")
                
                # Append actions and update the submenu title.
                item.appendActionsToContextMenu(submenu,
                                                readOnlyMode=readOnlyFlag)

            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                debugLogStr += \
                    "PriceBarChartArtifactGraphicsItem with " + \
                    "artifact info: " + item.artifact.toString() + ". "

                numContextSubMenuItems += 1

                # Add the menu for this item.  We create the menu this
                # way so that 'submenu' is owned by 'menu'.
                submenu = menu.addMenu("")
                
                # Append actions and update the submenu title.
                item.appendActionsToContextMenu(submenu,
                                                readOnlyMode=readOnlyFlag)
            else:
                self.log.debug("Non-PriceBar and Non-artifact item.")


        self.log.debug("{} items under scene clickPosF({}, {}): {}".\
                       format(numContextSubMenuItems,
                              clickPosF.x(),
                              clickPosF.y(),
                              debugLogStr))

        # Add context menu options that are available for all locations.
        menu.addSeparator()

        # Here I am creating QActions that will handle the QMenu
        # option selection, but for setting astro times, I have to
        # jump through a few hoops to be able to pass the
        # information about the recent right-click that caused the
        # context menu to come up.  Maybe there's a better way to
        # do this.
        setAstro1Action = QAction("Set timestamp on Astro Chart 1", parent)
        setAstro2Action = QAction("Set timestamp on Astro Chart 2", parent)
        setAstro3Action = QAction("Set timestamp on Astro Chart 3", parent)

        # Define a method to add to each instance.
        def handleActionTriggered(self):
            self.emit(QtCore.SIGNAL("actionTriggered(QPointF)"), self.data())

        # Add the method to the instances of the actions.
        setAstro1Action.handleActionTriggered = \
            types.MethodType(handleActionTriggered,
                             setAstro1Action)
        setAstro2Action.handleActionTriggered = \
            types.MethodType(handleActionTriggered,
                             setAstro2Action)
        setAstro3Action.handleActionTriggered = \
            types.MethodType(handleActionTriggered,
                             setAstro3Action)

        # Store in the actions, the scene position as a QPointF.
        setAstro1Action.setData(clickPosF)
        setAstro2Action.setData(clickPosF)
        setAstro3Action.setData(clickPosF)

        # Connect the triggered signal to the signal we appended
        # to the instances.
        setAstro1Action.triggered.\
            connect(setAstro1Action.handleActionTriggered)
        setAstro1Action.triggered.\
            connect(setAstro1Action.handleActionTriggered)
        setAstro1Action.triggered.\
            connect(setAstro1Action.handleActionTriggered)

        QtCore.QObject.connect(setAstro1Action,
                               QtCore.SIGNAL("actionTriggered(QPointF)"),
                               self._handleSetAstro1Action)
        QtCore.QObject.connect(setAstro2Action,
                               QtCore.SIGNAL("actionTriggered(QPointF)"),
                               self._handleSetAstro2Action)
        QtCore.QObject.connect(setAstro2Action,
                               QtCore.SIGNAL("actionTriggered(QPointF)"),
                               self._handleSetAstro2Action)

        # TODO: add more options here for showing the sq-of-9,
        # etc. for this price/time.

        menu.addAction(setAstro1Action)
        menu.addAction(setAstro2Action)
        menu.addAction(setAstro3Action)
        return menu
    
    def _handleSetAstro1Action(self, clickPosF):
        """Handles when the user triggers a QAction for setting the
        astro chart.
        """

        # The scene X position represents the time.
        self.scene().setAstroChart1(clickPosF.x())
        
    def _handleSetAstro2Action(self, clickPosF):
        """Handles when the user triggers a QAction for setting the
        astro chart.
        """

        # The scene X position represents the time.
        self.scene().setAstroChart2(clickPosF.x())
        
    def _handleSetAstro3Action(self, clickPosF):
        """Handles when the user triggers a QAction for setting the
        astro chart.
        """

        # The scene X position represents the time.
        self.scene().setAstroChart3(clickPosF.x())
        
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

            if qkeyevent.key() == Qt.Key_Escape:
                # Unselect any selected items.
                self.log.debug("Escape key pressed while in " +
                               "'ReadOnlyPointerTool' mode")
                self.scene().clearSelection()
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Unselect any selected items.
                self.log.debug("Escape key pressed while in 'PointerTool' mode")
                self.scene().clearSelection()
            elif qkeyevent.matches(QKeySequence.Delete):
                # Get the items that are selected, and out of those,
                # remove the PriceBarChartArtifactGraphicsItems.
                self.log.debug("Delete key pressed while in 'PointerTool' mode")
                
                scene = self.scene()
                selectedItems = scene.selectedItems()

                for item in selectedItems:
                    if isinstance(item, PriceBarChartArtifactGraphicsItem):
                        
                        scene.removeItem(item)
        
                        # Emit signal to show that an item is removed.
                        # This sets the dirty flag.
                        scene.priceBarChartArtifactGraphicsItemRemoved.\
                            emit(item)
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

            if qkeyevent.key() == Qt.Key_Escape:
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

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.timeMeasurementGraphicsItem != None:
                    self.scene().removeItem(self.timeMeasurementGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.timeMeasurementGraphicsItem = None

            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.modalScaleGraphicsItem != None:
                    self.scene().removeItem(self.modalScaleGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.modalScaleGraphicsItem = None

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

        # Get the click position in scene coordinates for debugging purposes.
        clickPosF = self.mapToScene(qmouseevent.pos())
        self.log.debug("Click pos in scene coordinates is: ({}, {})".\
                       format(clickPosF.x(), clickPosF.y()))
        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:
            
            self.log.debug("Current toolMode is: ReadOnlyPointerTool")

            if qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())
            else:
                self.log.debug("Passing mouse press event to super().")
                super().mousePressEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            self.log.debug("Current toolMode is: PointerTool")
            
            if qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in non-readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=False)
                menu.exec_(qmouseevent.globalPos())
            else:
                self.log.debug("Passing mouse press event to super().")
                super().mousePressEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            self.log.debug("Current toolMode is: HandTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                self.log.debug("Passing mouse press event to super().")
                # Panning the QGraphicsView.
                super().mousePressEvent(qmouseevent)
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            self.log.debug("Current toolMode is: ZoomInTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
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
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            
            self.log.debug("Current toolMode is: ZoomOutTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
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
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:
            
            self.log.debug("Current toolMode is: BarCountTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF is None.")
                    
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

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "barCountGraphicsItem != None.")
                    
                    # Set the end point of the BarCountGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())
                    self.barCountGraphicsItem.setEndPointF(self.clickTwoPointF)
                    self.barCountGraphicsItem.normalizeStartAndEnd()
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.barCountGraphicsItem.getArtifact()
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.barCountGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.barCountGraphicsItem.sceneBoundingRect()
                    self.log.debug("barCountGraphicsItem " +
                                   "officially added.  " +
                                   "pos is: {}.  ".\
                                   format(self.barCountGraphicsItem.pos()) +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                    
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.barCountGraphicsItem = None

                else:
                    self.log.warn("Unexpected state reached.")

            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.barCountGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "barCountGraphicsItem != None.")
                    
                    # Right-click during setting the BarCountGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.barCountGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.barCountGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.barCountGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "barCountGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:
            
            self.log.debug("Current toolMode is: TimeMeasurementTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # Create the TimeMeasurementGraphicsItem and
                    # initialize it to the mouse location.
                    self.timeMeasurementGraphicsItem = \
                        TimeMeasurementGraphicsItem()
                    self.timeMeasurementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
                    self.timeMeasurementGraphicsItem.setPos(self.clickOnePointF)
                    self.timeMeasurementGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.timeMeasurementGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.timeMeasurementGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.timeMeasurementGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.timeMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeMeasurementGraphicsItem != None.")
                    
                    # Set the end point of the TimeMeasurementGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())
                    self.timeMeasurementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.timeMeasurementGraphicsItem.normalizeStartAndEnd()
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.timeMeasurementGraphicsItem.getArtifact()
                                                
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.timeMeasurementGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.timeMeasurementGraphicsItem.sceneBoundingRect()
                    self.log.debug("timeMeasurementGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))
                                   
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeMeasurementGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.timeMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeMeasurementGraphicsItem != None.")
                    
                    # Right-click during setting the TimeMeasurementGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.timeMeasurementGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeMeasurementGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.timeMeasurementGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeMeasurementGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']:
            
            self.log.debug("Current toolMode is: ModalScaleTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF is None.")
                    
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # Create the ModalScaleGraphicsItem and
                    # initialize it to the mouse location.
                    self.modalScaleGraphicsItem = ModalScaleGraphicsItem()
                    self.modalScaleGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
                    self.modalScaleGraphicsItem.setPos(self.clickOnePointF)
                    self.modalScaleGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.modalScaleGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.modalScaleGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.modalScaleGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.modalScaleGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "modalScaleGraphicsItem != None.")
                    
                    # Set the end point of the ModalScaleGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())
                    self.modalScaleGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.modalScaleGraphicsItem.normalizeStartAndEnd()
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.modalScaleGraphicsItem.getArtifact()
                                                
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.modalScaleGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.modalScaleGraphicsItem.sceneBoundingRect()
                    self.log.debug("modalScaleGraphicsItem " +
                                   "officially added.  " +
                                   "Its sceneBoundingRect is: {}.  ".\
                                   format(sceneBoundingRect) +
                                   "Its x range is: {} to {}.  ".\
                                   format(sceneBoundingRect.left(),
                                          sceneBoundingRect.right()) +
                                   "Its y range is: {} to {}.  ".\
                                   format(sceneBoundingRect.top(),
                                          sceneBoundingRect.bottom()))

                    # TODO: make sure that the modalScaleGraphicsItem
                    # can be created with varying x and y values for
                    # the start and end points (kind of like a 2-d
                    # vector).
                    
                    # Clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.modalScaleGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.modalScaleGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "modalScaleGraphicsItem != None.")
                    
                    # Right-click during setting the ModalScaleGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.modalScaleGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.modalScaleGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.modalScaleGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "modalScaleGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
        else:
            self.log.warn("Current toolMode is: UNKNOWN.")

            # For any other mode we don't have specific functionality
            # for, do a context menu if it is a right-click, otherwise
            # just pass the event to the parent to handle.
            if qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())
            else:
                self.log.debug("Passing mouse press event to super().")
                super().mousePressEvent(qmouseevent)

        self.log.debug("Exiting mousePressEvent()")

    def mouseReleaseEvent(self, qmouseevent):
        """Triggered when the mouse is pressed in this widget."""

        self.log.debug("Entered mouseReleaseEvent()")

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            self.log.debug("Current toolMode is: ReadOnlyPointerTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PointerTool']:

            self.log.debug("Current toolMode is: PointerTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['HandTool']:

            self.log.debug("Current toolMode is: HandTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomInTool']:

            self.log.debug("Current toolMode is: ZoomInTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:

            self.log.debug("Current toolMode is: ZoomOutTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['BarCountTool']:

            self.log.debug("Current toolMode is: BarCountTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            self.log.debug("Current toolMode is: TimeMeasurementTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']:

            self.log.debug("Current toolMode is: ModalScaleTool")
            super().mouseReleaseEvent(qmouseevent)

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent to handle.
            self.log.warn("Current toolMode is: UNKNOWN.")
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

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:

            if self.clickOnePointF != None and \
                self.timeMeasurementGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # TimeMeasurementGraphicsItem.
                self.timeMeasurementGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']:

            if self.clickOnePointF != None and \
                self.modalScaleGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # ModalScaleGraphicsItem.
                self.modalScaleGraphicsItem.setEndPointF(pos)
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
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeMeasurementTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ModalScaleTool']:
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

    
