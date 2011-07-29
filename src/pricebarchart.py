
# For line separator.
import os

# For logging.
import logging

# For dynamically adding methods to instances.
import types

# For calculating square roots and other calculations.
import math

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
from data_objects import PriceBarChartTextArtifact
from data_objects import PriceBarChartPriceTimeInfoArtifact
from data_objects import PriceBarChartPriceMeasurementArtifact
from data_objects import PriceBarChartTimeRetracementArtifact
from data_objects import PriceBarChartScaling
from data_objects import PriceBarChartSettings

# For conversions from julian day to datetime.datetime and vice versa.
from ephemeris import Ephemeris

# For edit dialogs for modifying the PriceBarChartArtifact objects of
# various PriceBarChartArtifactGraphicsItems.
from pricebarchart_dialogs import PriceBarChartBarCountArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTimeMeasurementArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartModalScaleArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTextArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartPriceTimeInfoArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartPriceMeasurementArtifactEditDialog
from pricebarchart_dialogs import PriceBarChartTimeRetracementArtifactEditDialog

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

    def getPriceBarOpenScenePoint(self):
        """Returns the scene coordinates of the open point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the open of this
        pricebar is.
        """

        openPrice = 0.0
        high = 0.0
        low = 0.0

        if self.priceBar != None:
            openPrice = self.priceBar.open
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) / 2.0

        x = 0.0
        yOpen = -1.0 * (openPrice - priceMidpoint)
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yOpen))

        return rv


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

    def getPriceBarCloseScenePoint(self):
        """Returns the scene coordinates of the close point of this
        PriceBar.

        Returns: QPointF in scene coordinates of where the close of this
        pricebar is.
        """

        close = 0.0
        high = 0.0
        low = 0.0

        if self.priceBar != None:
            close = self.priceBar.close
            high = self.priceBar.high
            low = self.priceBar.low

        priceMidpoint = (high + low) / 2.0

        x = 0.0
        yClose = -1.0 * (close - priceMidpoint)
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yClose))

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
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setAstro1Action = QAction("Set timestamp on Astro Chart &1", parent)
        setAstro2Action = QAction("Set timestamp on Astro Chart &2", parent)
        setAstro3Action = QAction("Set timestamp on Astro Chart &3", parent)
        
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

        scene = self.scene()
        scene.removeItem(self)
        scene.priceBarChartChanged.emit()

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
        
        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartTextArtifact()

        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.textItem = QGraphicsSimpleTextItem("", self)
        self.textItem.setPos(0.0, 0.0)

        # Set the font of the text.
        self.textItemFont = self.artifact.getFont()
        self.textItem.setFont(self.textItemFont)

        # Set the color of the text.
        self.color = self.artifact.getColor()
        
        # Set the pen color of the text.
        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.artifact.getColor())
        self.textItem.setPen(self.textItemPen)

        # Set the brush color of the text.
        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.artifact.getColor())
        self.textItem.setBrush(self.textItemBrush)

        # Apply some size scaling to the text.
        textTransform = QTransform()
        textTransform.scale(self.artifact.getTextXScaling(), \
                            self.artifact.getTextYScaling())
        self.textItem.setTransform(textTransform)

    def setText(self, text):
        """Sets the text in this graphics item.

        Arguments:
        text - str value for the new text.
        """

        self.textItem.setText(text)
        
    def getText(self):
        """Returns the text in this graphics item as a str."""

        return self.textItem.text()
        
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

            self.log.debug("Setting TextGraphicsItem with the " +
                           "following artifact: " + self.artifact.toString())
            self.log.debug("Font in artifact is: " +
                           self.artifact.getFont().toString())
                           
            # Extract and set the internals according to the info 
            # in self.artifact.
            self.setPos(self.artifact.getPos())
            
            # Internal QGraphicsItem that holds the text of the bar count.
            # Initialize to blank and set at the end point.
            self.textItem.setText(self.artifact.getText())

            # Set the font of the text.
            self.textItemFont = self.artifact.getFont()
            self.textItem.setFont(self.textItemFont)

            # Set the color of the text.
            self.color = self.artifact.getColor()
            
            # Set the pen color of the text.
            self.textItemPen = self.textItem.pen()
            self.textItemPen.setColor(self.color)
            self.textItem.setPen(self.textItemPen)

            # Set the brush color of the text.
            self.textItemBrush = self.textItem.brush()
            self.textItemBrush.setColor(self.color)
            self.textItem.setBrush(self.textItemBrush)

            # Apply some size scaling to the text.
            self.textTransform = QTransform()
            self.textTransform.scale(self.artifact.getTextXScaling(), \
                                     self.artifact.getTextYScaling())
            self.textItem.setTransform(self.textTransform)

        else:
            raise TypeError("Expected artifact type: PriceBarChartTextArtifact")
    
        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTextArtifact for this QGraphicsItem 
        so that it may be pickled.
        """

        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartTextArtifact to be 
        # current, then return it.
        self.artifact.setPos(self.pos())
        self.artifact.setText(self.textItem.text())
        self.artifact.setFont(self.textItemFont)
        self.artifact.setColor(self.color)
        self.artifact.setTextXScaling(self.textTransform.m11())
        self.artifact.setTextYScaling(self.textTransform.m22())
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        # Set values from the priceBarChartSettings into the internal
        # member variables.
        
        self.textItemFont = QFont()
        self.textItemFont.fromString(priceBarChartSettings.\
                                     textGraphicsItemDefaultFontDescription) 
        self.color = \
            priceBarChartSettings.textGraphicsItemDefaultColor
        
        self.textTransform = QTransform()
        self.textTransform.scale(priceBarChartSettings.\
                                 textGraphicsItemDefaultXScaling,
                                 priceBarChartSettings.\
                                 textGraphicsItemDefaultYScaling)

        # Update the internal text item.
        self.textItem.setFont(self.textItemFont)

        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.color)
        self.textItem.setPen(self.textItemPen)

        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.color)
        self.textItem.setBrush(self.textItemBrush)

        self.textItem.setTransform(self.textTransform)

        # Schedule an update.
        self.prepareGeometryChange()
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        # No settings.
        pass
    
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Arguments:
        pos - QPointF holding the new position.
        """
        
        super().setPos(pos)
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) is the location of the internal text item
        # in local coordinates.  The QRectF returned is relative to
        # this (0, 0) point.

        textItemBoundingRect = self.textItem.boundingRect()

        # Here we need to scale the bounding rect so that
        # it takes into account the transform that we did.
        width = textItemBoundingRect.width()
        height = textItemBoundingRect.height()

        newWidth = width * self.textTransform.m11()
        newHeight = height * self.textTransform.m22()

        textItemBoundingRect.setWidth(newWidth)
        textItemBoundingRect.setHeight(newHeight)
        
        return textItemBoundingRect

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.textItemPen:
            painter.setPen(self.textItemPen)

        # Draw a dashed-line surrounding the item if it is selected.
        if option.state & QStyle.State_Selected:
            pad = self.textItemPen.widthF() / 2.0;
            
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
        actions relevant to this PriceBarChartArtifactGraphicsItem.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        
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
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()

        self.log.debug("Inside _handleInfoAction(): artifact is: " +
                       artifact.toString())
        
        dialog = PriceBarChartTextArtifactEditDialog(artifact,
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
        dialog = PriceBarChartTextArtifactEditDialog(artifact,
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
            
            self.prepareGeometryChange()

            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()

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
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
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
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
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
        
        # Height of the vertical bar drawn.
        self.timeMeasurementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeMeasurementTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeMeasurementTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextYScaling 

        # Font.
        self.timeMeasurementTextFont = QFont()
        self.timeMeasurementTextFont.fromString(\
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeMeasurementGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeMeasurementGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultColor

        # TimeMeasurementGraphicsItem showBarsTextFlag (bool).
        self.showBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowBarsTextFlag
    
        # TimeMeasurementGraphicsItem showHoursTextFlag (bool).
        self.showHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowHoursTextFlag
    
        # TimeMeasurementGraphicsItem showDaysTextFlag (bool).
        self.showDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowDaysTextFlag
    
        # TimeMeasurementGraphicsItem showWeeksTextFlag (bool).
        self.showWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showMonthsTextFlag (bool).
        self.showMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMonthsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtBarsTextFlag (bool).
        self.showSqrtBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtHoursTextFlag (bool).
        self.showSqrtHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtDaysTextFlag (bool).
        self.showSqrtDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtWeeksTextFlag (bool).
        self.showSqrtWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtMonthsTextFlag (bool).
        self.showSqrtMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMonthsTextFlag

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

        # Variables holding the time measurement values.
        self.numPriceBars = 0
        self.numHours = 0
        self.numDays = 0
        self.numWeeks = 0
        self.numMonths = 0

        self.numSqrtPriceBars = 0
        self.numSqrtHours = 0
        self.numSqrtDays = 0
        self.numSqrtWeeks = 0
        self.numSqrtMonths = 0
        
        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.timeMeasurementBarsText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementHoursText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementDaysText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementWeeksText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementMonthsText = QGraphicsSimpleTextItem("", self)

        self.timeMeasurementSqrtBarsText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementSqrtHoursText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementSqrtDaysText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementSqrtWeeksText = QGraphicsSimpleTextItem("", self)
        self.timeMeasurementSqrtMonthsText = QGraphicsSimpleTextItem("", self)

        # List of text items as created above.  This is so we can more
        # quickly and easily apply new settings.  It also helps for
        # painting things nicely.
        self.textItems = []
        self.textItems.append(self.timeMeasurementBarsText)
        self.textItems.append(self.timeMeasurementHoursText)
        self.textItems.append(self.timeMeasurementDaysText)
        self.textItems.append(self.timeMeasurementWeeksText)
        self.textItems.append(self.timeMeasurementMonthsText)
        
        self.textItems.append(self.timeMeasurementSqrtBarsText)
        self.textItems.append(self.timeMeasurementSqrtHoursText)
        self.textItems.append(self.timeMeasurementSqrtDaysText)
        self.textItems.append(self.timeMeasurementSqrtWeeksText)
        self.textItems.append(self.timeMeasurementSqrtMonthsText)

        for textItem in self.textItems:
            textItem.setPos(self.endPointF)
        
            # Set the font of the text.
            textItem.setFont(self.timeMeasurementTextFont)
        
            # Set the pen color of the text.
            self.timeMeasurementTextPen = textItem.pen()
            self.timeMeasurementTextPen.\
                setColor(self.timeMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.timeMeasurementTextPen)

            # Set the brush color of the text.
            self.timeMeasurementTextBrush = textItem.brush()
            self.timeMeasurementTextBrush.\
                setColor(self.timeMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.timeMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.timeMeasurementTextXScaling, \
                                self.timeMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Flag that indicates that verical dotted lines should be drawn.
        self.drawVerticalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None
        
    def setDrawVerticalDottedLinesFlag(self, flag):
        """If flag is set to true, then the vertical dotted lines are drawn.
        """

        self.drawVerticalDottedLinesFlag = flag

        # Need to call this because the bounding box is updated with
        # all the extra vertical lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.timeMeasurementGraphicsItemBarHeight = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeMeasurementTextXScaling = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeMeasurementTextYScaling = \
            priceBarChartSettings.\
                timeMeasurementGraphicsItemTextYScaling 

        # Font.
        self.timeMeasurementTextFont = QFont()
        self.timeMeasurementTextFont.fromString(\
            priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeMeasurementGraphicsItemTextColor = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeMeasurementGraphicsItemColor = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemDefaultColor

        # TimeMeasurementGraphicsItem showBarsTextFlag (bool).
        self.showBarsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowBarsTextFlag
    
        # TimeMeasurementGraphicsItem showHoursTextFlag (bool).
        self.showHoursTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowHoursTextFlag
    
        # TimeMeasurementGraphicsItem showDaysTextFlag (bool).
        self.showDaysTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowDaysTextFlag
    
        # TimeMeasurementGraphicsItem showWeeksTextFlag (bool).
        self.showWeeksTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showMonthsTextFlag (bool).
        self.showMonthsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowMonthsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtBarsTextFlag (bool).
        self.showSqrtBarsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtHoursTextFlag (bool).
        self.showSqrtHoursTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtDaysTextFlag (bool).
        self.showSqrtDaysTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtWeeksTextFlag (bool).
        self.showSqrtWeeksTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtMonthsTextFlag (bool).
        self.showSqrtMonthsTextFlag = \
            priceBarChartSettings.\
            timeMeasurementGraphicsItemShowSqrtMonthsTextFlag

        ####################################################################

        # Set specific items enabled or disabled, visible or not,
        # based on the above flags being set.
        
        # Set the text items as enabled or disabled, visible or invisible.
        self.timeMeasurementBarsText.setEnabled(self.showBarsTextFlag)
        self.timeMeasurementHoursText.setEnabled(self.showHoursTextFlag)
        self.timeMeasurementDaysText.setEnabled(self.showDaysTextFlag)
        self.timeMeasurementWeeksText.setEnabled(self.showWeeksTextFlag)
        self.timeMeasurementMonthsText.setEnabled(self.showMonthsTextFlag)

        self.timeMeasurementSqrtBarsText.setEnabled(self.showSqrtBarsTextFlag)
        self.timeMeasurementSqrtHoursText.setEnabled(self.showSqrtHoursTextFlag)
        self.timeMeasurementSqrtDaysText.setEnabled(self.showSqrtDaysTextFlag)
        self.timeMeasurementSqrtWeeksText.setEnabled(self.showSqrtWeeksTextFlag)
        self.timeMeasurementSqrtMonthsText.setEnabled(self.showSqrtMonthsTextFlag)
        
        self.timeMeasurementBarsText.setVisible(self.showBarsTextFlag)
        self.timeMeasurementHoursText.setVisible(self.showHoursTextFlag)
        self.timeMeasurementDaysText.setVisible(self.showDaysTextFlag)
        self.timeMeasurementWeeksText.setVisible(self.showWeeksTextFlag)
        self.timeMeasurementMonthsText.setVisible(self.showMonthsTextFlag)

        self.timeMeasurementSqrtBarsText.setVisible(self.showSqrtBarsTextFlag)
        self.timeMeasurementSqrtHoursText.setVisible(self.showSqrtHoursTextFlag)
        self.timeMeasurementSqrtDaysText.setVisible(self.showSqrtDaysTextFlag)
        self.timeMeasurementSqrtWeeksText.setVisible(self.showSqrtWeeksTextFlag)
        self.timeMeasurementSqrtMonthsText.setVisible(self.showSqrtMonthsTextFlag)
        
        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.timeMeasurementTextFont)
        
            # Set the pen color of the text.
            self.timeMeasurementTextPen = textItem.pen()
            self.timeMeasurementTextPen.\
                setColor(self.timeMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.timeMeasurementTextPen)

            # Set the brush color of the text.
            self.timeMeasurementTextBrush = textItem.brush()
            self.timeMeasurementTextBrush.\
                setColor(self.timeMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.timeMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.timeMeasurementTextXScaling, \
                                self.timeMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Update the timeMeasurement text item position.
        self._updateTextItemPositions()

        # Set the new color of the pen for drawing the bar.
        self.timeMeasurementPen.\
            setColor(self.timeMeasurementGraphicsItemColor)
        
        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        # No settings.
        
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
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
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

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
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

    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the timeMeasurement label position.
            
        # X location where to place the item.
        deltaX = self.endPointF.x() - self.startPointF.x()
        x = deltaX / 2

        # Starting Y location to place the text item.
        startY = -2.0

        # Amount to mutiply to get a largest offset from startY.
        offsetY = 1.5

        # j is the running index of the enabled text item.
        j = 0

        # Go through in reverse order since we are placing the
        # items relative to the bar (moving outwards).
        for i in reversed(range(len(self.textItems))):
            # Get the current text item.
            textItem = self.textItems[i]

            # Set the position no matter what, but only increment
            # j if the item is enabled and displayed.  This is so
            # we keep the text items on the graphicsScene close to
            # its parent item.
            y = (startY - (offsetY * j)) * \
                self.timeMeasurementGraphicsItemBarHeight
            textItem.setPos(QPointF(x, y))
            if textItem.isEnabled() and textItem.isVisible():
                j += 1
                    
    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        x = pointF.x()

        newValue = QPointF(x, self.endPointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            # Update the timeMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timemeasurement.
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

            # Update the timeMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timemeasurement.
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

            # Update the timeMeasurement text item position.
            self._updateTextItemPositions()
            
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
            self.numHours
            self.numDays
            self.numWeeks
            self.numMonths

            self.numSqrtPriceBars
            self.numSqrtHours
            self.numSqrtDays
            self.numSqrtWeeks
            self.numSqrtMonths

        to hold the amount of time between the start and end points.
        """

        scene = self.scene()

        # Reset the values.
        self.numPriceBars = 0.0
        self.numHours = 0.0
        self.numDays = 0.0
        self.numWeeks = 0.0
        self.numMonths = 0.0

        self.numSqrtPriceBars = 0.0
        self.numSqrtHours = 0.0
        self.numSqrtDays = 0.0
        self.numSqrtWeeks = 0.0
        self.numSqrtMonths = 0.0
        
        if scene != None:
            # Get all the QGraphicsItems.
            graphicsItems = scene.items()

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
        
            # Calculate the number of (calendar) days.
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

            # Calculate number of days.
            self.numDays = timeDelta.days
            self.numDays += (timeDelta.seconds / 86400.0)

            # Calculate number of hours.
            self.numHours = self.numDays * 24.0
            
            # Calculate number of weeks.
            self.numWeeks = self.numDays / 7.0

            # Calculate number of months.
            daysInMonth = 365.242199 / 12.0
            self.numMonths = self.numDays / daysInMonth

            self.log.debug("self.numPriceBars={}".format(self.numPriceBars))
            self.log.debug("self.numHours={}".format(self.numHours))
            self.log.debug("self.numDays={}".format(self.numDays))
            self.log.debug("self.numWeeks={}".format(self.numWeeks))
            self.log.debug("self.numMonths={}".format(self.numMonths))
            
            self.numSqrtPriceBars = math.sqrt(abs(self.numPriceBars))
            self.numSqrtHours = math.sqrt(abs(self.numHours))
            self.numSqrtDays = math.sqrt(abs(self.numDays))
            self.numSqrtWeeks = math.sqrt(abs(self.numWeeks))
            self.numSqrtMonths = math.sqrt(abs(self.numMonths))

            self.log.debug("self.numSqrtPriceBars={}".format(self.numSqrtPriceBars))
            self.log.debug("self.numSqrtHours={}".format(self.numSqrtHours))
            self.log.debug("self.numSqrtDays={}".format(self.numSqrtDays))
            self.log.debug("self.numSqrtWeeks={}".format(self.numSqrtWeeks))
            self.log.debug("self.numSqrtMonths={}".format(self.numSqrtMonths))
            
        # Update the text of the internal items.
        barsText = "{} B".format(self.numPriceBars)
        hoursText = "{:.2f} H".format(self.numHours)
        daysText = "{:.2f} CD".format(self.numDays)
        weeksText = "{:.2f} W".format(self.numWeeks)
        monthsText = "{:.2f} M".format(self.numMonths)
        
        sqrtBarsText = "{:.2f} sqrt B".format(self.numSqrtPriceBars)
        sqrtHoursText = "{:.2f} sqrt H".format(self.numSqrtHours)
        sqrtDaysText = "{:.2f} sqrt CD".format(self.numSqrtDays)
        sqrtWeeksText = "{:.2f} sqrt W".format(self.numSqrtWeeks)
        sqrtMonthsText = "{:.2f} sqrt M".format(self.numSqrtMonths)
        
        self.timeMeasurementBarsText.setText(barsText)
        self.timeMeasurementHoursText.setText(hoursText)
        self.timeMeasurementDaysText.setText(daysText)
        self.timeMeasurementWeeksText.setText(weeksText)
        self.timeMeasurementMonthsText.setText(monthsText)
        
        self.timeMeasurementSqrtBarsText.setText(sqrtBarsText)
        self.timeMeasurementSqrtHoursText.setText(sqrtHoursText)
        self.timeMeasurementSqrtDaysText.setText(sqrtDaysText)
        self.timeMeasurementSqrtWeeksText.setText(sqrtWeeksText)
        self.timeMeasurementSqrtMonthsText.setText(sqrtMonthsText)
        
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

        self.timeMeasurementTextXScaling = self.artifact.getTextXScaling()
        self.timeMeasurementTextYScaling = self.artifact.getTextYScaling()
        self.timeMeasurementTextFont = self.artifact.getFont()
        self.timeMeasurementGraphicsItemTextColor = self.artifact.getTextColor()
        self.timeMeasurementPen.setColor(self.artifact.getColor())
        
        self.showBarsTextFlag = self.artifact.getShowBarsTextFlag()
        self.showHoursTextFlag = self.artifact.getShowHoursTextFlag()
        self.showDaysTextFlag = self.artifact.getShowDaysTextFlag()
        self.showWeeksTextFlag = self.artifact.getShowWeeksTextFlag()
        self.showMonthsTextFlag = self.artifact.getShowMonthsTextFlag()
        
        self.showSqrtBarsTextFlag = self.artifact.getShowSqrtBarsTextFlag()
        self.showSqrtHoursTextFlag = self.artifact.getShowSqrtHoursTextFlag()
        self.showSqrtDaysTextFlag = self.artifact.getShowSqrtDaysTextFlag()
        self.showSqrtWeeksTextFlag = self.artifact.getShowSqrtWeeksTextFlag()
        self.showSqrtMonthsTextFlag = self.artifact.getShowSqrtMonthsTextFlag()

        #############

        # Set the text items as enabled or disabled, visible or invisible.
        self.timeMeasurementBarsText.setEnabled(self.showBarsTextFlag)
        self.timeMeasurementHoursText.setEnabled(self.showHoursTextFlag)
        self.timeMeasurementDaysText.setEnabled(self.showDaysTextFlag)
        self.timeMeasurementWeeksText.setEnabled(self.showWeeksTextFlag)
        self.timeMeasurementMonthsText.setEnabled(self.showMonthsTextFlag)

        self.timeMeasurementSqrtBarsText.setEnabled(self.showSqrtBarsTextFlag)
        self.timeMeasurementSqrtHoursText.setEnabled(self.showSqrtHoursTextFlag)
        self.timeMeasurementSqrtDaysText.setEnabled(self.showSqrtDaysTextFlag)
        self.timeMeasurementSqrtWeeksText.setEnabled(self.showSqrtWeeksTextFlag)
        self.timeMeasurementSqrtMonthsText.setEnabled(self.showSqrtMonthsTextFlag)
        
        self.timeMeasurementBarsText.setVisible(self.showBarsTextFlag)
        self.timeMeasurementHoursText.setVisible(self.showHoursTextFlag)
        self.timeMeasurementDaysText.setVisible(self.showDaysTextFlag)
        self.timeMeasurementWeeksText.setVisible(self.showWeeksTextFlag)
        self.timeMeasurementMonthsText.setVisible(self.showMonthsTextFlag)

        self.timeMeasurementSqrtBarsText.setVisible(self.showSqrtBarsTextFlag)
        self.timeMeasurementSqrtHoursText.setVisible(self.showSqrtHoursTextFlag)
        self.timeMeasurementSqrtDaysText.setVisible(self.showSqrtDaysTextFlag)
        self.timeMeasurementSqrtWeeksText.setVisible(self.showSqrtWeeksTextFlag)
        self.timeMeasurementSqrtMonthsText.setVisible(self.showSqrtMonthsTextFlag)
        
        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.timeMeasurementTextFont)
        
            # Set the pen color of the text.
            self.timeMeasurementTextPen = textItem.pen()
            self.timeMeasurementTextPen.\
                setColor(self.timeMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.timeMeasurementTextPen)

            # Set the brush color of the text.
            self.timeMeasurementTextBrush = textItem.brush()
            self.timeMeasurementTextBrush.\
                setColor(self.timeMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.timeMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.timeMeasurementTextXScaling, \
                                self.timeMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Update the timeMeasurement text item position.
        self._updateTextItemPositions()
            
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
        
        self.artifact.setTextXScaling(self.timeMeasurementTextXScaling)
        self.artifact.setTextYScaling(self.timeMeasurementTextYScaling)
        self.artifact.setFont(self.timeMeasurementTextFont)
        self.artifact.setTextColor(self.timeMeasurementGraphicsItemTextColor)
        self.artifact.setColor(self.timeMeasurementPen.color())
        
        self.artifact.setShowBarsTextFlag(self.showBarsTextFlag)
        self.artifact.setShowHoursTextFlag(self.showHoursTextFlag)
        self.artifact.setShowDaysTextFlag(self.showDaysTextFlag)
        self.artifact.setShowWeeksTextFlag(self.showWeeksTextFlag)
        self.artifact.setShowMonthsTextFlag(self.showMonthsTextFlag)
        
        self.artifact.setShowSqrtBarsTextFlag(self.showSqrtBarsTextFlag)
        self.artifact.setShowSqrtHoursTextFlag(self.showSqrtHoursTextFlag)
        self.artifact.setShowSqrtDaysTextFlag(self.showSqrtDaysTextFlag)
        self.artifact.setShowSqrtWeeksTextFlag(self.showSqrtWeeksTextFlag)
        self.artifact.setShowSqrtMonthsTextFlag(self.showSqrtMonthsTextFlag)
        
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

        # Initalize to the above boundaries.  We will set them below.
        localHighY = topLeft.y()
        localLowY = bottomRight.y()
        if self.drawVerticalDottedLinesFlag or self.isSelected():
            # Get the highest high, and lowest low PriceBar in local
            # coordinates.
            highestPrice = self.scene().getHighestPriceBar().high
            highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
            localHighestPriceBarY = \
                       self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()

            # Overwrite the high if it is larger.
            if localHighestPriceBarY > localHighY:
                localHighY = localHighestPriceBarY
                
            lowestPrice = self.scene().getLowestPriceBar().low
            lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
            localLowestPriceBarY = \
                      self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
            
            # Overwrite the low if it is smaller.
            if localLowestPriceBarY < localLowY:
                localLowY = localLowestPriceBarY
                
        xValues = []
        xValues.append(topLeft.x())
        xValues.append(bottomRight.x())

        yValues = []
        yValues.append(topLeft.y())
        yValues.append(bottomRight.y())
        yValues.append(localHighY)
        yValues.append(localLowY)

        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.
        """

        # Get the QRectF with just the lines.
        xDelta = self.endPointF.x() - self.startPointF.x()
        
        topLeft = \
            QPointF(0.0, -1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight / 2.0))
        
        bottomRight = \
            QPointF(xDelta, 1.0 *
                    (self.timeMeasurementGraphicsItemBarHeight / 2.0))

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.timeMeasurementPen:
            painter.setPen(self.timeMeasurementPen)
        
        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        x2 = 0.0
        y2 = -1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.timeMeasurementGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle horizontal line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw vertical dotted lines at each enabled tick area if the
        # flag is set to do so, or if it is selected.
        if self.drawVerticalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
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
    
                # Get the highest high, and lowest low PriceBar in local
                # coordinates.
                highestPrice = self.scene().getHighestPriceBar().high
                highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
                localHighY = \
                    self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()
                
                lowestPrice = self.scene().getLowestPriceBar().low
                lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
                localLowY = \
                    self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          
                yValues.append(localHighY)
                yValues.append(localLowY)

                # We have all y values now, so sort them to get the
                # low and high.
                yValues.sort()
                smallestY = yValues[0]
                largestY = yValues[-1]
        
                # Vertical line at the beginning.
                localPosX = 0.0
                startPoint = QPointF(localPosX, largestY)
                endPoint = QPointF(localPosX, smallestY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
            
                # Vertical line at the end.
                localPosX = 0.0 + xDelta
                startPoint = QPointF(localPosX, largestY)
                endPoint = QPointF(localPosX, smallestY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
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
            painter.drawPath(self.shape())
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

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
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
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
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
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


class VerticalTickGraphicsItem(QGraphicsItem):
    """QGraphicsItem that draws a vertical tick line. """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Logger
        self.log = logging.getLogger("pricebarchart.VerticalTickGraphicsItem")

        self.barHeight = 0.2
        
        # Pen which is used to do the painting of the bar tick.
        self.pen = QPen()
        self.penWidth = 0.0
        self.pen.setWidthF(self.penWidth)

    def setPen(self, pen):
        """Sets the pen used to draw this QGraphicsItem."""
        
        self.pen = pen
        
    def setPenWidth(self, penWidth):
        """Sets the pen width used to draw this QGraphicsItem.
        Arguments:

        penWidth - float value for the pen width.
        """
        
        self.penWidth = penWidth
        self.pen.setWidthF(self.penWidth)
    
    def setBarHeight(self, barHeight):
        """Sets the bar height of the tick.

        Arguments:
        barHeight - float value for the bar height.
        """

        self.barHeight = barHeight

    def getBarHeight(self):
        """Returns the bar height of the tick."""
        
        return self.barHeight

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        topLeft = QPointF(self.penWidth * -0.5,
                          1.0 * self.barHeight / 2.0)
        
        bottomRight = QPointF(self.penWidth * 0.5,
                              -1.0 * self.barHeight / 2.0)

        return QRectF(topLeft, bottomRight).normalized()

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.pen:
            painter.setPen(self.pen)
            
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.barHeight / 2.0)
        x2 = 0.0
        y2 = -1.0 * (self.barHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

               
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
        
        # Color of the graphicsitem bar.
        self.modalScaleGraphicsItemColor = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemBarColor

        # Color of the text that is associated with the bar count
        # graphicsitem.
        self.modalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemTextColor

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
        self.dummyItem = QGraphicsSimpleTextItem("", self)
        
        # Set the font of the text.
        self.modalScaleTextFont = QFont("Sans Serif")
        self.modalScaleTextFont.\
            setPointSizeF(self.artifact.getModalScaleGraphicsItemFontSize())

        # Set the pen color of the text.
        self.modalScaleTextPen = self.dummyItem.pen()
        self.modalScaleTextPen.setColor(self.modalScaleGraphicsItemTextColor)

        # Set the brush color of the text.
        self.modalScaleTextBrush = self.dummyItem.brush()
        self.modalScaleTextBrush.setColor(self.modalScaleGraphicsItemTextColor)

        # Degrees of text rotation.
        self.rotationDegrees = 90.0
        
        # Size scaling for the text.
        textTransform = QTransform()
        textTransform.scale(self.modalScaleTextXScaling, \
                            self.modalScaleTextYScaling)
        textTransform.rotate(self.rotationDegrees)
        
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

        # Below is a list of VerticalTickGraphicsItems that correspond
        # to each of the musicalRatios.
        self.verticalTickItems = []
        
        # Initialize to blank and set at the end point.
        for musicalRatio in range(len(self.artifact.getMusicalRatios())):
            verticalTickItem = VerticalTickGraphicsItem(self)
            verticalTickItem.setPos(self.endPointF)
            verticalTickItem.setPen(self.modalScalePen)
            
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

            self.verticalTickItems.append(verticalTickItem)

        # Flag that indicates that verical dotted lines should be drawn.
        self.drawVerticalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None

    def setDrawVerticalDottedLinesFlag(self, flag):
        """If flag is set to true, then the vertical dotted lines are drawn.
        """

        self.drawVerticalDottedLinesFlag = flag
        
        # Need to call this because the bounding box is updated with
        # all the extra vertical lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        ########
        
        # ModalScaleGraphicsItem bar color (QColor).
        self.modalScaleGraphicsItemColor = \
            priceBarChartSettings.modalScaleGraphicsItemBarColor

        # ModalScaleGraphicsItem text color (QColor).
        self.modalScaleGraphicsItemTextColor = \
            priceBarChartSettings.modalScaleGraphicsItemTextColor
        
        # X scaling of the text.
        self.modalScaleTextXScaling = \
            priceBarChartSettings.\
                modalScaleGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.modalScaleTextYScaling = \
            priceBarChartSettings.\
                modalScaleGraphicsItemTextYScaling 

        ########

        # Set values in the artifact.
        
        self.artifact.setModalScaleGraphicsItemBarColor(\
            self.modalScaleGraphicsItemColor)
        self.artifact.setModalScaleGraphicsItemTextColor(\
            self.modalScaleGraphicsItemTextColor)

        self.setArtifact(self.artifact)
        
        self.refreshTextItems()
        
        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        # No settings read from app preferences.
        pass
        
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
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
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
            
            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
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
            for i in range(len(artifact.getMusicalRatios())):
                # Get the MusicalRatio that corresponds to this index.
                musicalRatio = artifact.getMusicalRatios()[i]

                # Here we always set the positions of everything.  If
                # the musicalRatio not enabled, then the corresponding
                # graphics items would have gotten disabled in the
                # self.recalculateModalScale() call above.
                
                # Get the x and y position that will be the new
                # position of the text item.
                (x, y) = artifact.getXYForMusicalRatio(i)

                # Map those x and y to local coordinates.
                pointF = self.mapFromScene(QPointF(x, y))

                # Create the text transform to use.
                textTransform = QTransform()
                textTransform.scale(self.modalScaleTextXScaling, \
                                    self.modalScaleTextYScaling)
                textTransform.rotate(self.rotationDegrees)
                
                # Get the text items for this point on the scale.
                listOfTextItems = self.musicalRatioTextItems[i]

                # For each text item for that point on the scale,
                # set the position.
                for j in range(len(listOfTextItems)):
                    textItem = listOfTextItems[j]
                    # The position set is not exactly at (x, y),
                    # but instead at an offset slightly below that
                    # point so that multiple texts dont' overlap
                    # each other.
                    offsetX = (textItem.boundingRect().height() * 0.5) * j
                    #offsetX = \
                    #    artifact.getModalScaleGraphicsItemBarHeight() * j
                    textItem.setPos(QPointF(pointF.x() - offsetX,
                                            pointF.y()))
                    textItem.setFont(self.modalScaleTextFont)
                    textItem.setPen(self.modalScaleTextPen)
                    textItem.setBrush(self.modalScaleTextBrush)
                    textItem.setTransform(textTransform)
                    
                # Also set the position of the vertical tick line.
                barHeight = artifact.getModalScaleGraphicsItemBarHeight()
                self.verticalTickItems[i].setBarHeight(barHeight)
                self.verticalTickItems[i].setPos(pointF)
                    
            # Call update on this item since positions and child items
            # were updated.
            self.prepareGeometryChange()
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

                        # Make the text visible if it is enabled.
                        textEnabled = artifact.isTextEnabled()
                        textItem.setEnabled(textEnabled)
                        textItem.setVisible(textEnabled)

                        # If text isn't enabled, there's no need to
                        # set the text for it.  Go to the next text item.
                        if textEnabled == False:
                            continue
                    
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

                    # Also enable and set the vertical tick line.
                    self.verticalTickItems[i].setVisible(True)
                    self.verticalTickItems[i].setEnabled(True)
                            
                else:
                    # Disable and make not visable.
                    
                    # Get the text items for this point on the scale.
                    listOfTextItems = self.musicalRatioTextItems[i]
                    
                    # For each text item for that point on the scale,
                    # set as disabled and not visible.
                    for j in range(len(listOfTextItems)):
                        textItem = listOfTextItems[j]
                        textItem.setVisible(False)
                        textItem.setEnabled(False)

                    # Also disable the vertical tick line.
                    self.verticalTickItems[i].setVisible(False)
                    self.verticalTickItems[i].setEnabled(False)
                    

                        
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

        self.modalScaleTextFont.\
            setPointSizeF(self.artifact.getModalScaleGraphicsItemFontSize())
        self.modalScalePen.\
            setColor(self.artifact.getModalScaleGraphicsItemBarColor())
        self.modalScaleTextPen.\
            setColor(self.artifact.getModalScaleGraphicsItemTextColor())
        self.modalScaleTextBrush.\
            setColor(self.artifact.getModalScaleGraphicsItemTextColor())
        

        # Need to recalculate the time measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the measurements will be zero.
        self.refreshTextItems()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartModalScaleArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        # Update the internal self.priceBarChartModalScaleArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)

        # Everything else gets modified only by the edit dialog.
        
        return self.artifact

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) in local coordinates is the center of 
        # the vertical bar that is at the left portion of this widget,
        # and represented in scene coordinates as the self.startPointF 
        # location.
        
        # The QRectF returned is relative to this (0, 0) point.
        barHeight = self.getArtifact().getModalScaleGraphicsItemBarHeight()
        
        xTopLeft = 0.0
        yTopLeft = 1.0 * (barHeight / 2.0)
        
        xBottomLeft = 0.0
        yBottomLeft = -1.0 * (barHeight / 2.0)
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopRight = 0.0 + xDelta
        yTopRight = (1.0 * (barHeight / 2.0)) + yDelta
        
        xBottomRight = 0.0 + xDelta
        yBottomRight = (-1.0 * (barHeight / 2.0)) + yDelta

        # Get the highest high, and lowest low PriceBar in local
        # coordinates.
        highestPrice = self.scene().getHighestPriceBar().high
        highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
        localHighY = \
            self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()

        lowestPrice = self.scene().getLowestPriceBar().low
        lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
        localLowY = \
            self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          

        xValues = []
        xValues.append(xTopLeft)
        xValues.append(xBottomLeft)
        xValues.append(xTopRight)
        xValues.append(xBottomRight)

        yValues = []
        yValues.append(yTopLeft)
        yValues.append(yBottomLeft)
        yValues.append(yTopRight)
        yValues.append(yBottomRight)
        yValues.append(localHighY)
        yValues.append(localLowY)
        
        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.
        """

        barHeight = self.getArtifact().getModalScaleGraphicsItemBarHeight()
        
        # The QRectF returned is relative to this (0, 0) point.

        xTopLeft = 0.0
        yTopLeft = 1.0 * (barHeight / 2.0)
        topLeft = QPointF(xTopLeft, yTopLeft)
        
        xBottomLeft = 0.0
        yBottomLeft = -1.0 * (barHeight / 2.0)
        bottomLeft = QPointF(xBottomLeft, yBottomLeft)
        
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        
        xTopRight = 0.0 + xDelta
        yTopRight = (1.0 * (barHeight / 2.0)) + yDelta
        topRight = QPointF(xTopRight, yTopRight)
        
        xBottomRight = 0.0 + xDelta
        yBottomRight = (-1.0 * (barHeight / 2.0)) + yDelta
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

        self.log.debug("Entered ModalScaleGraphicsItem.paint().  " +
                       "pos is: ({}, {})".format(self.pos().x(),
                                                 self.pos().y()))
                       
        if painter.pen() != self.modalScalePen:
            painter.setPen(self.modalScalePen)

        artifact = self.getArtifact()
        barHeight = artifact.getModalScaleGraphicsItemBarHeight()

        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (barHeight / 2.0)
        x2 = 0.0
        y2 = -1.0 * (barHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = 0.0 + xDelta
        y1 = (1.0 * (barHeight / 2.0)) + yDelta
        x2 = 0.0 + xDelta
        y2 = (-1.0 * (barHeight / 2.0)) + yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw vertical dotted lines at each enabled musicalRatio if
        # the flag is set to do so, or if it is selected.
        if self.drawVerticalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
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
    
                # Get the highest high, and lowest low PriceBar in local
                # coordinates.
                highestPrice = self.scene().getHighestPriceBar().high
                highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
                localHighY = \
                    self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()
                
                lowestPrice = self.scene().getLowestPriceBar().low
                lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
                localLowY = \
                    self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          
                yValues.append(localHighY)
                yValues.append(localLowY)

                # We have all y values now, so sort them to get the
                # low and high.
                yValues.sort()
                smallestY = yValues[0]
                largestY = yValues[-1]
        
                for verticalTickItem in self.verticalTickItems:
                    if verticalTickItem.isEnabled() and \
                       verticalTickItem.isVisible():
                    
                        localPosX = verticalTickItem.pos().x()

                        startPoint = QPointF(localPosX, largestY)
                        endPoint = QPointF(localPosX, smallestY)
                        
                        painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
                
                        painter.setPen(QPen(option.palette.windowText(), 0,
                                            Qt.DashLine))
                        painter.setBrush(Qt.NoBrush)
                        painter.drawLine(startPoint, endPoint)
            
        # Draw a dashed-line surrounding the item if it is selected.
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
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

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
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        rotateDownAction = QAction("Rotate Down", parent)
        rotateUpAction = QAction("Rotate Up", parent)
        reverseAction = QAction("Reverse", parent)
        
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
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
        rotateDownAction.triggered.\
            connect(self._handleRotateDownAction)
        rotateUpAction.triggered.\
            connect(self._handleRotateUpAction)
        reverseAction.triggered.\
            connect(self._handleReverseAction)
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
        rotateDownAction.setEnabled(not readOnlyMode)
        rotateUpAction.setEnabled(not readOnlyMode)
        reverseAction.setEnabled(not readOnlyMode)
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
        menu.addAction(rotateDownAction)
        menu.addAction(rotateUpAction)
        menu.addAction(reverseAction)
        menu.addSeparator()
        menu.addAction(setStartOnAstro1Action)
        menu.addAction(setStartOnAstro2Action)
        menu.addAction(setStartOnAstro3Action)
        menu.addSeparator()
        menu.addAction(setEndOnAstro1Action)
        menu.addAction(setEndOnAstro2Action)
        menu.addAction(setEndOnAstro3Action)

    def rotateDown(self):
        """Causes the ModalScaleGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        self._handleRotateDownAction()
        
    def rotateUp(self):
        """Causes the ModalScaleGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        self._handleRotateUpAction()

    def reverse(self):
        """Causes the ModalScaleGraphicsItem to have its musicalRatios
        reversed.
        """

        self._handleReverseAction()
        
    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
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
        
    def _handleRotateDownAction(self):
        """Causes the ModalScaleGraphicsItem to have its musicalRatios
        rotated down (to the right).
        """

        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()

        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
            else:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
                
            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()
        
    def _handleRotateUpAction(self):
        """Causes the ModalScaleGraphicsItem to have its musicalRatios
        rotated up (to the left).
        """
        
        # Get all the musicalRatios in the internally stored artifact.
        musicalRatios = self.getArtifact().getMusicalRatios()
        
        # See how many enabled musicalRatios there are.  
        numEnabledMusicalRatios = 0
        for musicalRatio in musicalRatios:
            if musicalRatio.isEnabled():
                numEnabledMusicalRatios += 1
                
        if len(musicalRatios) > 0 and numEnabledMusicalRatios > 0:

            if self.artifact.isReversed() == False:
                # Put the first musicalRatio in the back.
                firstRatio = musicalRatios.pop(0)
                musicalRatios.append(firstRatio)
        
                # Rotate until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the first musicalRatio in the back.
                    firstRatio = musicalRatios.pop(0)
                    musicalRatios.append(firstRatio)
            else:
                # Put the last musicalRatio in the front.
                lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                musicalRatios.insert(0, lastRatio)
        
                # Rotate down until there is a musicalRatio at the
                # beginning that is enabled.
                while musicalRatios[0].isEnabled() == False:
                    # Put the last musicalRatio in the front.
                    lastRatio = musicalRatios.pop(len(musicalRatios) - 1)
                    musicalRatios.insert(0, lastRatio)
                

            # Overwrite the old list in the internally stored artifact.
            self.artifact.setMusicalRatios(musicalRatios)

            # Refresh everything.
            self.refreshTextItems()
        
            # Emit that the PriceBarChart has changed so that the
            # dirty flag can be set.
            self.scene().priceBarChartChanged.emit()

    def _handleReverseAction(self):
        """Causes the ModalScaleGraphicsItem to have its musicalRatios
        reversed.
        """
        
        # Flip the flag that indicates that the musical ratios are reversed.
        self.artifact.setReversed(not self.artifact.isReversed())
        
        # Refresh everything.
        self.refreshTextItems()
        
        # Emit that the PriceBarChart has changed so that the
        # dirty flag can be set.
        self.scene().priceBarChartChanged.emit()
        
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

        
class PriceTimeInfoGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBarChartPriceTimeInfoArtifact."""
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartPriceTimeInfoArtifact()

        # Convert object.
        self.convertObj = None
        
        # BirthInfo object that holds information about the birth of
        # this trading entity.  This is used so we can determine
        # amount of time elapsed since birth.
        self.birthInfo = None
        
        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.textItem = QGraphicsSimpleTextItem("", self)
        self.textItem.setPos(0.0, 0.0)

        # Set the font of the text.
        self.textItemFont = self.artifact.getFont()
        self.textItem.setFont(self.textItemFont)

        # Set the color of the text.
        self.color = self.artifact.getColor()
        
        # Set the pen color of the text.
        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.artifact.getColor())
        self.textItem.setPen(self.textItemPen)

        # Set the brush color of the text.
        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.artifact.getColor())
        self.textItem.setBrush(self.textItemBrush)

        # Apply some size scaling to the text.
        textTransform = QTransform()
        textTransform.scale(self.artifact.getTextXScaling(), \
                            self.artifact.getTextYScaling())
        self.textItem.setTransform(textTransform)

        # Flag that indicates that we should draw the line to the
        # infoPointF.
        self.drawLineToInfoPointFFlag = False

    def setDrawLineToInfoPointFFlag(self, flag):
        """If set to true, then a line is drawn from the box to the
        infoPointF point during paint calls.  If false, then that line
        is not drawn.
        """

        self.drawLineToInfoPointFFlag = flag
        
        # Need to call this because the bounding box is updated with
        # all the extra line being drawn.
        self.prepareGeometryChange()
        
    def setConvertObj(self, convertObj):
        """Object for doing conversions from x and datetime and y to
        price.  This should be the graphics scene.  This is used
        because sometimes we want to be able to do conversions and
        stuff before we even add the item to the scene.
        """

        self.convertObj = convertObj
        
    def setBirthInfo(self, birthInfo):
        """Sets the internal BirthInfo object so that time elapsed
        from birth can be calculated.
        """

        self.birthInfo = birthInfo

        # Update the text according to what's in infoPointF and birthInfo.
        self._updateText()
        self.update()
        
    def getBirthInfo(self):
        """Returns the internal BirthInfo object.
        """

        return self.birthInfo

    def setInfoPointF(self, infoPointF):
        """Sets the infoPointF used in this QGraphicsItem.  Also
        updates the artifact accordingly.
        """

        self.artifact.setInfoPointF(infoPointF)
    
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartPriceTimeInfoArtifact object's data
        into this QGraphicsPriceTimeInfoItem.

        Arguments:
        artifact - PriceBarChartPriceTimeInfoArtifact object with information
                   about this PriceTimeInfoGraphisItem
        """

        self.log.debug("Entered setArtifact()")

        if isinstance(artifact, PriceBarChartPriceTimeInfoArtifact):
            self.artifact = artifact

            self.log.debug("Setting PriceTimeInfoGraphicsItem with the " +
                           "following artifact: " + self.artifact.toString())
            self.log.debug("Font in artifact is: " +
                           self.artifact.getFont().toString())
                           
            # Extract and set the internals according to the info 
            # in self.artifact.
            self.setPos(self.artifact.getPos())

            # Update the text according to what's in infoPointF and birthInfo.
            self._updateText()
            
            # Set the font of the text.
            self.textItemFont = self.artifact.getFont()
            self.textItem.setFont(self.textItemFont)

            # Set the color of the text.
            self.color = self.artifact.getColor()
            
            # Set the pen color of the text.
            self.textItemPen = self.textItem.pen()
            self.textItemPen.setColor(self.color)
            self.textItem.setPen(self.textItemPen)

            # Set the brush color of the text.
            self.textItemBrush = self.textItem.brush()
            self.textItemBrush.setColor(self.color)
            self.textItem.setBrush(self.textItemBrush)

            # Apply some size scaling to the text.
            self.textTransform = QTransform()
            self.textTransform.scale(self.artifact.getTextXScaling(), \
                                     self.artifact.getTextYScaling())
            self.textItem.setTransform(self.textTransform)

            self.update()
        else:
            raise TypeError("Expected artifact type: " +
                            "PriceBarChartPriceTimeInfoArtifact")
    
        self.log.debug("Exiting setArtifact()")

    def _updateText(self):
        """Updates the text based on what is in the artifact.
        """

        # This object needs either the self.convertObj set, or the
        # parent graphicsscene set or else it won't have the capacity
        # to do price and datetime conversions to coordinates.
        if self.convertObj == None:
            if self.scene() == None:
                self.log.debug("_updateText(): Not able to update the text " +
                               "because QGraphicsScene for unit conversions " +
                               "was not set (or the item wasn't added to a " +
                               "qgraphicsscene yet")
                self.textItem.setText("INVALID")
                return
            else:
                self.convertObj = self.scene()
        
        # Set the text according to various flags in the artifact.
        # Internal QGraphicsItem that holds the text.
        # Initialize to blank and set at the end point.
        infoPointF = self.artifact.getInfoPointF()
        dt = self.convertObj.sceneXPosToDatetime(infoPointF.x())
        price = self.convertObj.sceneYPosToPrice(infoPointF.y())

        text = ""

        if self.artifact.getShowTimestampFlag():
            text += "t={}".format(Ephemeris.datetimeToDayStr(dt)) + \
                    os.linesep
        if self.artifact.getShowPriceFlag():
            text += "price={}".format(price) + os.linesep
        if self.artifact.getShowSqrtOfPriceFlag():
            text += "sqrt(price)={}".format(math.sqrt(price)) + os.linesep
        if self.artifact.getShowTimeElapsedSinceBirthFlag():
            if self.birthInfo != None:
                # Get the birth timestamp and convert to X coordinate.
                birthDtUtc = self.birthInfo.getBirthUtcDatetime()
                birthX = self.convertObj.datetimeToSceneXPos(birthDtUtc)

                # Find the difference between the info points and birthX
                xDiff = infoPointF.x() - birthX

                text += "elapsed_t=={}".format(xDiff) + os.linesep
        if self.artifact.getShowSqrtOfTimeElapsedSinceBirthFlag():
            if self.birthInfo != None:
                # Get the birth timestamp and convert to X coordinate.
                birthDtUtc = self.birthInfo.getBirthUtcDatetime()
                birthX = self.convertObj.datetimeToSceneXPos(birthDtUtc)

                # Find the difference between the info points and birthX
                xDiff = infoPointF.x() - birthX

                text += "sqrt(elapsed_t)=={}".format(math.sqrt(xDiff)) + \
                        os.linesep
                
        self.textItem.setText(text)
        self.prepareGeometryChange()
        
    def getArtifact(self):
        """Returns a PriceBarChartPriceTimeInfoArtifact for this QGraphicsItem 
        so that it may be pickled.
        """

        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartPriceTimeInfoArtifact to be 
        # current, then return it.
        self.artifact.setPos(self.pos())
        self.artifact.setFont(self.textItemFont)
        self.artifact.setColor(self.color)
        self.artifact.setTextXScaling(self.textTransform.m11())
        self.artifact.setTextYScaling(self.textTransform.m22())
        
        self.log.debug("Exiting getArtifact()")
        
        return self.artifact

    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")

        # Set values from the priceBarChartSettings into the internal
        # member variables.
        
        self.textItemFont = QFont()
        self.textItemFont.\
            fromString(priceBarChartSettings.\
                       priceTimeInfoGraphicsItemDefaultFontDescription) 
        self.color = \
            priceBarChartSettings.priceTimeInfoGraphicsItemDefaultColor
        
        self.textTransform = QTransform()
        self.textTransform.scale(priceBarChartSettings.\
                                 priceTimeInfoGraphicsItemDefaultXScaling,
                                 priceBarChartSettings.\
                                 priceTimeInfoGraphicsItemDefaultYScaling)

        # Update the internal text item.
        self.textItem.setFont(self.textItemFont)

        self.textItemPen = self.textItem.pen()
        self.textItemPen.setColor(self.color)
        self.textItem.setPen(self.textItemPen)

        self.textItemBrush = self.textItem.brush()
        self.textItemBrush.setColor(self.color)
        self.textItem.setBrush(self.textItemBrush)

        self.textItem.setTransform(self.textTransform)

        # Schedule an update.
        self.prepareGeometryChange()
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        # No settings.
        pass

    def setTextLabelEdgeYLocation(self, y):
        """Sets the y location of the edge of the box that is the text
        graphics item.

        Arguments:
        y - float value for the y position of the edge of the box.
        """

        artifact = self.getArtifact()
        infoPointF = artifact.getInfoPointF()
        
        # Here we need to scale the bounding rect so that
        # it takes into account the transform that we did.
        textBoundingRect = self.textItem.boundingRect().normalized()
        width = textBoundingRect.width()
        height = textBoundingRect.height()
        scaledWidth = width * self.textTransform.m11()
        scaledHeight = height * self.textTransform.m22()
        
        if y > infoPointF.y():
            # Below.
            posX = infoPointF.x() - (scaledWidth * 0.5)
            posY = y
            pos = QPointF(posX, posY)
            self.setPos(pos)
        else:
            # Above
            posX = infoPointF.x() - (scaledWidth * 0.5)
            posY = y - scaledHeight
            pos = QPointF(posX, posY)
            self.setPos(pos)

        self.update()
        
    def setPos(self, pos):
        """Overwrites the QGraphicsItem setPos() function.

        Arguments:
        pos - QPointF holding the new position.
        """
        
        super().setPos(pos)

    def _getScaledRectOfTextItem(self):
        """Returns the scaled QRectF of the self.textItem."""
        
        # Coordinate (0, 0) is the location of the internal text item
        # in local coordinates.  The QRectF returned is relative to
        # this (0, 0) point.

        textItemBoundingRect = self.textItem.boundingRect()

        self.log.debug("Bounding rect of textItem is: x={}, y={}, w={}, h={}".\
                       format(textItemBoundingRect.x(),
                              textItemBoundingRect.y(),
                              textItemBoundingRect.width(),
                              textItemBoundingRect.height()))
                       
        # Here we need to scale the bounding rect so that
        # it takes into account the transform that we did.
        width = textItemBoundingRect.width()
        height = textItemBoundingRect.height()
        scaledWidth = width * self.textTransform.m11()
        scaledHeight = height * self.textTransform.m22()

        topLeft = QPointF(0, 0)
        bottomRight = QPointF(scaledWidth, scaledHeight)
        scaledTextRect = QRectF(topLeft, bottomRight)

        return scaledTextRect
    
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        self.log.debug("Entered boundingRect()")

        scaledTextRect = self._getScaledRectOfTextItem()
        
        self.log.debug("scaledTextRect is: x={}, y={}, w={}, h={}".\
                       format(scaledTextRect.x(),
                              scaledTextRect.y(),
                              scaledTextRect.width(),
                              scaledTextRect.height()))
                       
        localInfoPointF = self.mapFromScene(self.artifact.getInfoPointF())
        
        self.log.debug("localInfoPointF is: x={}, y={}".\
                       format(localInfoPointF.x(),
                              localInfoPointF.y()))
                       
        xValues = []
        xValues.append(scaledTextRect.topLeft().x())
        xValues.append(scaledTextRect.bottomLeft().x())
        xValues.append(scaledTextRect.topRight().x())
        xValues.append(scaledTextRect.bottomRight().x())
        xValues.append(localInfoPointF.x())

        yValues = []
        yValues.append(scaledTextRect.topLeft().y())
        yValues.append(scaledTextRect.bottomLeft().y())
        yValues.append(scaledTextRect.topRight().y())
        yValues.append(scaledTextRect.bottomRight().y())
        yValues.append(localInfoPointF.y())

        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        self.log.debug("rv coordinates are: ({}, {}), width={}, height={}".\
                       format(rv.x(), rv.y(), rv.width(), rv.height()))
        
        self.log.debug("Exiting boundingRect()")
        
        return rv
    
    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.
        """

        self.log.debug("Entering shape()")
        
        scaledTextRect = self._getScaledRectOfTextItem()

        painterPath = QPainterPath()
        painterPath.addRect(scaledTextRect)

        self.log.debug("scaledTextRect coordinates are: " +
                       "({}, {}), width={}, height={}".\
                       format(scaledTextRect.x(),
                              scaledTextRect.y(),
                              scaledTextRect.width(),
                              scaledTextRect.height()))
        
        self.log.debug("Exiting shape()")
        
        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        self.log.debug("Entering paint()")
        self.log.debug("self.drawLineToInfoPointFFlag={}".\
                       format(self.drawLineToInfoPointFFlag))
        
        if painter.pen() != self.textItemPen:
            painter.setPen(self.textItemPen)

        if self.drawLineToInfoPointFFlag == True or \
               option.state & QStyle.State_Selected:

            self.log.debug("Drawing the line to the infoPointF...")
            
            # Draw a line to the infoPointF.  Below is setting the colors
            # and drawing parameters.
            pad = self.textItemPen.widthF() / 2.0;
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
    
            scaledTextRect = self._getScaledRectOfTextItem()
            
            topLeft = scaledTextRect.topLeft()
            bottomRight = scaledTextRect.bottomRight()
            localInfoPointF = self.mapFromScene(self.artifact.getInfoPointF())
    
            x = scaledTextRect.width() * 0.5
            y = None
            if localInfoPointF.y() > 0:
                y = scaledTextRect.height()
            else:
                y = 0.0
                
            # Set the start and end points to the line.
            startLinePoint = QPointF(x, y)
            endLinePoint = localInfoPointF
    
            self.log.debug("Start and end points of the line are: " +
                           "({}, {}), ({}, {})".\
                           format(startLinePoint.x(),
                                  startLinePoint.y(),
                                  endLinePoint.x(),
                                  endLinePoint.y()))
            
            # Draw the line.
            painter.drawLine(startLinePoint, endLinePoint)
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawLine(startLinePoint, endLinePoint)
        
        # Draw a dashed-line surrounding the item if it is selected.
        if option.state & QStyle.State_Selected:
            pad = self.textItemPen.widthF() / 2.0;

            self.log.debug("Drawing selected dotted line.")
            
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
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

        self.log.debug("Exiting paint()")
        
    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceBarChartArtifactGraphicsItem.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        
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
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)

        # Add the QActions to the menu.
        menu.addAction(selectAction)
        menu.addAction(unselectAction)
        menu.addSeparator()
        menu.addAction(removeAction)
        menu.addSeparator()
        menu.addAction(infoAction)
        menu.addAction(editAction)

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()

        self.log.debug("Inside _handleInfoAction(): artifact is: " +
                       artifact.toString())
        
        dialog = PriceBarChartPriceTimeInfoArtifactEditDialog(artifact,
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
        dialog = PriceBarChartPriceTimeInfoArtifactEditDialog(artifact,
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
        
        
class PriceMeasurementGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a measurement ruler for price in
    the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point of the start point of the ruler.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceMeasurementGraphicsItem")
        self.log.debug("Entered __init__().")


        ############################################################
        # Set default values for preferences/settings.
        
        # Width of the horizontal bar drawn.
        self.priceMeasurementGraphicsItemBarWidth = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemBarWidth
 
        # X scaling of the text.
        self.priceMeasurementTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.priceMeasurementTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceMeasurementGraphicsItemTextYScaling 

        # Font.
        self.priceMeasurementTextFont = QFont()
        self.priceMeasurementTextFont.fromString(\
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceMeasurementGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.priceMeasurementGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultColor

        # PriceMeasurementGraphicsItem showPriceRangeTextFlag (bool).
        self.showPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowPriceRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtPriceRangeTextFlag (bool).
        self.showSqrtPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag
    
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartPriceMeasurementArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.priceMeasurementPenWidth = 0.0
        self.priceMeasurementPen = QPen()
        self.priceMeasurementPen.\
            setColor(self.priceMeasurementGraphicsItemColor)
        self.priceMeasurementPen.setWidthF(self.priceMeasurementPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Variables holding the price measurement values.
        self.priceRange = 0
        self.sqrtPriceRange = 0
        
        # Internal QGraphicsItem that holds the text of the price measurements.
        # Initialize to blank and set at the end point.
        self.priceMeasurementPriceRangeText = \
            QGraphicsSimpleTextItem("", self)
        self.priceMeasurementSqrtPriceRangeText = \
            QGraphicsSimpleTextItem("", self)

        # List of text items as created above.  This is so we can more
        # quickly and easily apply new settings.  It also helps for
        # painting things nicely.
        self.textItems = []
        self.textItems.append(self.priceMeasurementPriceRangeText)
        self.textItems.append(self.priceMeasurementSqrtPriceRangeText)

        for textItem in self.textItems:
            textItem.setPos(self.endPointF)
        
            # Set the font of the text.
            textItem.setFont(self.priceMeasurementTextFont)
        
            # Set the pen color of the text.
            self.priceMeasurementTextPen = textItem.pen()
            self.priceMeasurementTextPen.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.priceMeasurementTextPen)

            # Set the brush color of the text.
            self.priceMeasurementTextBrush = textItem.brush()
            self.priceMeasurementTextBrush.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.priceMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.priceMeasurementTextXScaling, \
                                self.priceMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Flag that indicates that verical dotted lines should be drawn.
        self.drawVerticalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None
        
    def setDrawVerticalDottedLinesFlag(self, flag):
        """If flag is set to true, then the vertical dotted lines are drawn.
        """

        self.drawVerticalDottedLinesFlag = flag

        # Need to call this because the bounding box is updated with
        # all the extra vertical lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Width of the horizontal bar drawn.
        self.priceMeasurementGraphicsItemBarWidth = \
            priceBarChartSettings.\
                priceMeasurementGraphicsItemDefaultBarWidth
 
        # X scaling of the text.
        self.priceMeasurementTextXScaling = \
            priceBarChartSettings.\
                priceMeasurementGraphicsItemDefaultTextXScaling 

        # Y scaling of the text.
        self.priceMeasurementTextYScaling = \
            priceBarChartSettings.\
                priceMeasurementGraphicsItemDefaultTextYScaling 

        # Font.
        self.priceMeasurementTextFont = QFont()
        self.priceMeasurementTextFont.fromString(\
            priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.priceMeasurementGraphicsItemTextColor = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultTextColor

        # Color of the item.
        self.priceMeasurementGraphicsItemColor = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemDefaultColor

        # PriceMeasurementGraphicsItem showPriceRangeTextFlag (bool).
        self.showPriceRangeTextFlag = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemShowPriceRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtPriceRangeTextFlag (bool).
        self.showSqrtPriceRangeTextFlag = \
            priceBarChartSettings.\
            priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag
    
        ####################################################################

        # Set specific items enabled or disabled, visible or not,
        # based on the above flags being set.
        
        # Set the text items as enabled or disabled, visible or invisible.
        self.priceMeasurementPriceRangeText.\
            setEnabled(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setEnabled(self.showSqrtPriceRangeTextFlag)
        
        self.priceMeasurementPriceRangeText.\
            setVisible(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setVisible(self.showSqrtPriceRangeTextFlag)
        
        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.priceMeasurementTextFont)
        
            # Set the pen color of the text.
            self.priceMeasurementTextPen = textItem.pen()
            self.priceMeasurementTextPen.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.priceMeasurementTextPen)

            # Set the brush color of the text.
            self.priceMeasurementTextBrush = textItem.brush()
            self.priceMeasurementTextBrush.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.priceMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.priceMeasurementTextXScaling, \
                                self.priceMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Update the priceMeasurement text item position.
        self._updateTextItemPositions()

        # Set the new color of the pen for drawing the bar.
        self.priceMeasurementPen.\
            setColor(self.priceMeasurementGraphicsItemColor)
        
        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        # No settings.
        
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
            self.recalculatePriceMeasurement()
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
            # the starting or ending points of the ruler.
            scenePosY = event.scenePos().y()
            self.log.debug("DEBUG: scenePosY={}".format(scenePosY))
            
            startingPointY = self.startPointF.y()
            self.log.debug("DEBUG: startingPointY={}".format(startingPointY))
            endingPointY = self.endPointF.y()
            self.log.debug("DEBUG: endingPointY={}".format(endingPointY))
            
            diff = endingPointY - startingPointY
            self.log.debug("DEBUG: diff={}".format(diff))

            startThreshold = startingPointY + (diff * (1.0 / 5))
            endThreshold = endingPointY - (diff * (1.0 / 5))

            self.log.debug("DEBUG: startThreshold={}".format(startThreshold))
            self.log.debug("DEBUG: endThreshold={}".format(endThreshold))

            if scenePosY <= startThreshold:
                self.draggingStartPointFlag = True
                self.log.debug("DEBUG: self.draggingStartPointFlag={}".
                               format(self.draggingStartPointFlag))
            elif scenePosY >= endThreshold:
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
                    self.setStartPointF(QPointF(self.startPointF.x(),
                                                event.scenePos().y()))
                    self.update()
                elif self.draggingEndPointFlag == True:
                    self.log.debug("DEBUG: self.draggingEndPointFlag={}".
                                   format(self.draggingEndPointFlag))
                    self.setEndPointF(QPointF(self.endPointF.x(),
                                              event.scenePos().y()))
                    self.update()
                else:
                    # This means that the user is dragging the whole
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
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

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
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

    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the priceMeasurement label position.
            
        # Y location where to place the item.
        deltaY = self.endPointF.y() - self.startPointF.y()
        y = deltaY / 2

        # Starting Y location to place the text item.
        startY = y

        # Amount to mutiply to the bar width to get the offset.
        offsetY = 0.3

        # j is the running index of the enabled text item.
        j = 0

        for i in reversed(range(len(self.textItems))):
            # Get the current text item.
            textItem = self.textItems[i]

            # Set the position no matter what, but only increment
            # j if the item is enabled and displayed.  This is so
            # we keep the text items on the graphicsScene close to
            # its parent item.
            x = self.priceMeasurementGraphicsItemBarWidth / 2.0
            y = startY - \
                ((offsetY * j) * self.priceMeasurementGraphicsItemBarWidth)
            textItem.setPos(QPointF(x, y))
            if textItem.isEnabled() and textItem.isVisible():
                j += 1
                    
    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        y = pointF.y()

        newValue = QPointF(self.endPointF.x(), y)

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            # Update the priceMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the pricemeasurement.
                self.recalculatePriceMeasurement()
                self.update()
                
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        y = pointF.y()

        newValue = QPointF(self.startPointF.x(), y)

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the priceMeasurement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the pricemeasurement.
                self.recalculatePriceMeasurement()
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.y() > self.endPointF.y():
            self.log.debug("Normalization of PriceMeasurementGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

            # Update the priceMeasurement text item position.
            self._updateTextItemPositions()
            
            self.recalculatePriceMeasurement()
            
            super().setPos(self.startPointF)
            

    def recalculatePriceMeasurement(self):
        """Sets the internal variables:
        
            self.priceRange
            self.sqrtPriceRange
            
        to hold the amount of price between the start and end points.
        """

        scene = self.scene()

        # Reset the values.
        self.priceRange = 0.0
        self.sqrtPriceRange = 0.0

        if scene != None:
            startPointPrice = \
                scene.sceneYPosToPrice(self.startPointF.y())
            self.log.debug("startPointPrice: {}".format(startPointPrice))
            
            endPointPrice = \
                scene.sceneYPosToPrice(self.endPointF.y())
            self.log.debug("endPointPrice: {}".format(endPointPrice))

            self.priceRange = startPointPrice - endPointPrice
            self.sqrtPriceRange = math.sqrt(abs(self.priceRange))

            self.log.debug("self.priceRange={}".format(self.priceRange))
            self.log.debug("self.sqrtPriceRange={}".format(self.sqrtPriceRange))
            
        # Update the text of the internal items.
        priceRangeText = "{:.4f} range".format(self.priceRange)
        sqrtPriceRangeText = "{:.4f} sqrt range".format(self.sqrtPriceRange)
        
        self.priceMeasurementPriceRangeText.setText(priceRangeText)
        self.priceMeasurementSqrtPriceRangeText.setText(sqrtPriceRangeText)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartPriceMeasurementArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartPriceMeasurementArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartPriceMeasurementArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartPriceMeasurementArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.priceMeasurementTextXScaling = self.artifact.getTextXScaling()
        self.priceMeasurementTextYScaling = self.artifact.getTextYScaling()
        self.priceMeasurementTextFont = self.artifact.getFont()
        self.priceMeasurementGraphicsItemTextColor = \
            self.artifact.getTextColor()
        self.priceMeasurementPen.setColor(self.artifact.getColor())
        
        self.showPriceRangeTextFlag = \
            self.artifact.getShowPriceRangeTextFlag()
        self.showSqrtPriceRangeTextFlag = \
            self.artifact.getShowSqrtPriceRangeTextFlag()

        #############

        # Set the text items as enabled or disabled, visible or invisible.
        self.priceMeasurementPriceRangeText.\
            setEnabled(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setEnabled(self.showSqrtPriceRangeTextFlag)
        
        self.priceMeasurementPriceRangeText.\
            setVisible(self.showPriceRangeTextFlag)
        self.priceMeasurementSqrtPriceRangeText.\
            setVisible(self.showSqrtPriceRangeTextFlag)
        
        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.priceMeasurementTextFont)
        
            # Set the pen color of the text.
            self.priceMeasurementTextPen = textItem.pen()
            self.priceMeasurementTextPen.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setPen(self.priceMeasurementTextPen)

            # Set the brush color of the text.
            self.priceMeasurementTextBrush = textItem.brush()
            self.priceMeasurementTextBrush.\
                setColor(self.priceMeasurementGraphicsItemTextColor)
            
            textItem.setBrush(self.priceMeasurementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.priceMeasurementTextXScaling, \
                                self.priceMeasurementTextYScaling)
            textItem.setTransform(textTransform)

        # Update the priceMeasurement text item position.
        self._updateTextItemPositions()
            
        # Need to recalculate the price measurement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the price measurements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculatePriceMeasurement()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartPriceMeasurementArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartPriceMeasurementArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.artifact.setTextXScaling(self.priceMeasurementTextXScaling)
        self.artifact.setTextYScaling(self.priceMeasurementTextYScaling)
        self.artifact.setFont(self.priceMeasurementTextFont)
        self.artifact.setTextColor(self.priceMeasurementGraphicsItemTextColor)
        self.artifact.setColor(self.priceMeasurementPen.color())
        
        self.artifact.setShowPriceRangeTextFlag(\
            self.showPriceRangeTextFlag)
        self.artifact.setShowSqrtPriceRangeTextFlag(\
            self.showSqrtPriceRangeTextFlag)
        
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
        yDelta = self.endPointF.y() - self.startPointF.y()

        topLeft = \
            QPointF(-1.0 * \
                    (self.priceMeasurementGraphicsItemBarWidth / 2.0),
                    0.0)
        
        bottomRight = \
            QPointF(1.0 * \
                    (self.priceMeasurementGraphicsItemBarWidth / 2.0),
                    yDelta)

        # Initalize to the above boundaries.  We will set them below.
        localHighX = bottomRight.x()
        localLowX = topLeft.x()
        if self.drawVerticalDottedLinesFlag or self.isSelected():
            # Get the last and first PriceBar's timestamp in local
            # coordinates.
            earliestPriceBar = self.scene().getEarliestPriceBar()
            smallestPriceBarX = \
                self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
            localSmallestPriceBarX = \
                self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()

            # Overwrite the low if it is smaller.
            if localSmallestPriceBarX < localLowX:
                localLowX = localSmallestPriceBarX
            
            latestPriceBar = self.scene().getLatestPriceBar()
            largestPriceBarX = \
                self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
            localLargestPriceBarX = \
                self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()
        
            # Overwrite the high if it is larger.
            if localLargestPriceBarX > localHighX:
                localHighX = localLargestPriceBarX
            
        xValues = []
        xValues.append(topLeft.x())
        xValues.append(bottomRight.x())
        xValues.append(localHighX)
        xValues.append(localLowX)

        yValues = []
        yValues.append(topLeft.y())
        yValues.append(bottomRight.y())

        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.
        """

        # Get the QRectF with just the lines.
        yDelta = self.endPointF.y() - self.startPointF.y()

        topLeft = \
            QPointF(-1.0 * (self.priceMeasurementGraphicsItemBarWidth / 2.0),
                    0.0)
        
        bottomRight = \
            QPointF(1.0 * (self.priceMeasurementGraphicsItemBarWidth / 2.0),
                    yDelta)

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.priceMeasurementPen:
            painter.setPen(self.priceMeasurementPen)
        
        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the start point horizontal bar part.
        x1 = -1.0 * (self.priceMeasurementGraphicsItemBarWidth / 2.0)
        y1 = 0.0
        x2 = 1.0 * (self.priceMeasurementGraphicsItemBarWidth / 2.0)
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the end point horizontal bar part.
        yDelta = self.endPointF.y() - self.startPointF.y()
        x1 = -1.0 * (self.priceMeasurementGraphicsItemBarWidth / 2.0)
        y1 = 0.0 + yDelta
        x2 = 1.0 * (self.priceMeasurementGraphicsItemBarWidth / 2.0)
        y2 = 0.0 + yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle vertical line.
        x1 = 0.0
        y1 = 0.0
        x2 = 0.0
        y2 = yDelta
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw vertical dotted lines at each tick area if the flag is
        # set to do so, or if it is selected.
        if self.drawVerticalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.priceMeasurementPen.widthF() / 2.0;
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
    
                # Get the last and first PriceBar's timestamp in local
                # coordinates.
                earliestPriceBar = self.scene().getEarliestPriceBar()
                smallestPriceBarX = \
                    self.scene().datetimeToSceneXPos(earliestPriceBar.timestamp)
                localSmallestPriceBarX = \
                    self.mapFromScene(QPointF(smallestPriceBarX, 0.0)).x()

                latestPriceBar = self.scene().getLatestPriceBar()
                largestPriceBarX = \
                    self.scene().datetimeToSceneXPos(latestPriceBar.timestamp)
                localLargestPriceBarX = \
                    self.mapFromScene(QPointF(largestPriceBarX, 0.0)).x()
            
                xValues.append(localSmallestPriceBarX)
                xValues.append(localLargestPriceBarX)

                # We have all x values now, so sort them to get the
                # low and high.
                xValues.sort()
                smallestX = xValues[0]
                largestX = xValues[-1]
        
                # Horizontal line at the startPoint.
                localPosY = 0.0
                startPoint = QPointF(largestX, localPosY)
                endPoint = QPointF(smallestX, localPosY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
            
                # Horizontal line at the endPoint.
                localPosY = 0.0 + yDelta
                startPoint = QPointF(largestX, localPosY)
                endPoint = QPointF(smallestX, localPosY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.priceMeasurementPen.widthF() / 2.0;
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
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this PriceMeasurementGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        PriceMeasurementGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
        
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
        
        # Enable or disable actions.
        selectAction.setEnabled(True)
        unselectAction.setEnabled(True)
        removeAction.setEnabled(not readOnlyMode)
        infoAction.setEnabled(True)
        editAction.setEnabled(not readOnlyMode)
        setStartOnAstro1Action.setEnabled(True)
        setStartOnAstro2Action.setEnabled(True)
        setStartOnAstro3Action.setEnabled(True)

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

    def _handleSelectAction(self):
        """Causes the QGraphicsItem to become selected."""

        self.setSelected(True)

    def _handleUnselectAction(self):
        """Causes the QGraphicsItem to become unselected."""

        self.setSelected(False)

    def _handleRemoveAction(self):
        """Causes the QGraphicsItem to be removed from the scene."""
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartPriceMeasurementArtifactEditDialog(artifact,
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
        dialog = PriceBarChartPriceMeasurementArtifactEditDialog(artifact,
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
        

class TimeRetracementGraphicsItem(PriceBarChartArtifactGraphicsItem):
    """QGraphicsItem that visualizes a PriceBar counter in the GraphicsView.

    This item uses the origin point (0, 0) in item coordinates as the
    center point height bar, on the start point (left part) of the bar ruler.

    That means when a user creates a new TimeRetracementGraphicsItem
    the position and points can be consistently set.
    """
    
    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = logging.getLogger(\
            "pricebarchart.TimeRetracementGraphicsItem")
        
        self.log.debug("Entered __init__().")

        ############################################################
        # Set default values for preferences/settings.
        
        # Height of the vertical bar drawn.
        self.timeRetracementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeRetracementTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeRetracementTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextYScaling 

        # Font.
        self.timeRetracementTextFont = QFont()
        self.timeRetracementTextFont.fromString(\
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeRetracementGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeRetracementGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultColor

        # TimeRetracementGraphicsItem showBarsTextFlag (bool).
        self.showBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowBarsTextFlag
    
        ############################################################

        # Internal storage object, used for loading/saving (serialization).
        self.artifact = PriceBarChartTimeRetracementArtifact()

        # Read the QSettings preferences for the various parameters of
        # this price bar.
        self.loadSettingsFromAppPreferences()
        
        # Pen which is used to do the painting of the bar ruler.
        self.timeRetracementPenWidth = 0.0
        self.timeRetracementPen = QPen()
        self.timeRetracementPen.setColor(self.timeRetracementGraphicsItemColor)
        self.timeRetracementPen.setWidthF(self.timeRetracementPenWidth)
        
        # Starting point, in scene coordinates.
        self.startPointF = QPointF(0, 0)

        # Ending point, in scene coordinates.
        self.endPointF = QPointF(0, 0)

        # Variables holding the time retracement values.
        self.numPriceBars = 0
        self.numHours = 0
        self.numDays = 0
        self.numWeeks = 0
        self.numMonths = 0

        self.numSqrtPriceBars = 0
        self.numSqrtHours = 0
        self.numSqrtDays = 0
        self.numSqrtWeeks = 0
        self.numSqrtMonths = 0
        
        # Internal QGraphicsItem that holds the text of the bar count.
        # Initialize to blank and set at the end point.
        self.timeRetracementBarsText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementHoursText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementDaysText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementWeeksText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementMonthsText = QGraphicsSimpleTextItem("", self)

        self.timeRetracementSqrtBarsText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementSqrtHoursText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementSqrtDaysText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementSqrtWeeksText = QGraphicsSimpleTextItem("", self)
        self.timeRetracementSqrtMonthsText = QGraphicsSimpleTextItem("", self)

        # List of text items as created above.  This is so we can more
        # quickly and easily apply new settings.  It also helps for
        # painting things nicely.
        self.textItems = []
        self.textItems.append(self.timeRetracementBarsText)
        self.textItems.append(self.timeRetracementHoursText)
        self.textItems.append(self.timeRetracementDaysText)
        self.textItems.append(self.timeRetracementWeeksText)
        self.textItems.append(self.timeRetracementMonthsText)
        
        self.textItems.append(self.timeRetracementSqrtBarsText)
        self.textItems.append(self.timeRetracementSqrtHoursText)
        self.textItems.append(self.timeRetracementSqrtDaysText)
        self.textItems.append(self.timeRetracementSqrtWeeksText)
        self.textItems.append(self.timeRetracementSqrtMonthsText)

        for textItem in self.textItems:
            textItem.setPos(self.endPointF)
        
            # Set the font of the text.
            textItem.setFont(self.timeRetracementTextFont)
        
            # Set the pen color of the text.
            self.timeRetracementTextPen = textItem.pen()
            self.timeRetracementTextPen.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setPen(self.timeRetracementTextPen)

            # Set the brush color of the text.
            self.timeRetracementTextBrush = textItem.brush()
            self.timeRetracementTextBrush.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setBrush(self.timeRetracementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.timeRetracementTextXScaling, \
                                self.timeRetracementTextYScaling)
            textItem.setTransform(textTransform)

        # Flag that indicates that verical dotted lines should be drawn.
        self.drawVerticalDottedLinesFlag = False
        
        # Flags that indicate that the user is dragging either the start
        # or end point of the QGraphicsItem.
        self.draggingStartPointFlag = False
        self.draggingEndPointFlag = False
        self.clickScenePointF = None
        
    def setDrawVerticalDottedLinesFlag(self, flag):
        """If flag is set to true, then the vertical dotted lines are drawn.
        """

        self.drawVerticalDottedLinesFlag = flag

        # Need to call this because the bounding box is updated with
        # all the extra vertical lines being drawn.
        self.prepareGeometryChange()
        
    def loadSettingsFromPriceBarChartSettings(self, priceBarChartSettings):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the given PriceBarChartSettings object.
        """

        self.log.debug("Entered loadSettingsFromPriceBarChartSettings()")
        
        # Height of the vertical bar drawn.
        self.timeRetracementGraphicsItemBarHeight = \
            priceBarChartSettings.\
                timeRetracementGraphicsItemBarHeight 
 
        # X scaling of the text.
        self.timeRetracementTextXScaling = \
            priceBarChartSettings.\
                timeRetracementGraphicsItemTextXScaling 

        # Y scaling of the text.
        self.timeRetracementTextYScaling = \
            priceBarChartSettings.\
                timeRetracementGraphicsItemTextYScaling 

        # Font.
        self.timeRetracementTextFont = QFont()
        self.timeRetracementTextFont.fromString(\
            priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultFontDescription)
        
        # Color of the text that is associated with the graphicsitem.
        self.timeRetracementGraphicsItemTextColor = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultTextColor

        # Color of the item.
        self.timeRetracementGraphicsItemColor = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemDefaultColor

        # TimeRetracementGraphicsItem showBarsTextFlag (bool).
        self.showBarsTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowBarsTextFlag
    
        # TimeRetracementGraphicsItem showHoursTextFlag (bool).
        self.showHoursTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowHoursTextFlag
    
        # TimeRetracementGraphicsItem showDaysTextFlag (bool).
        self.showDaysTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowDaysTextFlag
    
        # TimeRetracementGraphicsItem showWeeksTextFlag (bool).
        self.showWeeksTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowWeeksTextFlag
    
        # TimeRetracementGraphicsItem showMonthsTextFlag (bool).
        self.showMonthsTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowMonthsTextFlag
    
        # TimeRetracementGraphicsItem showSqrtBarsTextFlag (bool).
        self.showSqrtBarsTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowSqrtBarsTextFlag
    
        # TimeRetracementGraphicsItem showSqrtHoursTextFlag (bool).
        self.showSqrtHoursTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowSqrtHoursTextFlag
    
        # TimeRetracementGraphicsItem showSqrtDaysTextFlag (bool).
        self.showSqrtDaysTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowSqrtDaysTextFlag
    
        # TimeRetracementGraphicsItem showSqrtWeeksTextFlag (bool).
        self.showSqrtWeeksTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowSqrtWeeksTextFlag
    
        # TimeRetracementGraphicsItem showSqrtMonthsTextFlag (bool).
        self.showSqrtMonthsTextFlag = \
            priceBarChartSettings.\
            timeRetracementGraphicsItemShowSqrtMonthsTextFlag

        ####################################################################

        # Set specific items enabled or disabled, visible or not,
        # based on the above flags being set.
        
        # Set the text items as enabled or disabled, visible or invisible.
        self.timeRetracementBarsText.setEnabled(self.showBarsTextFlag)
        self.timeRetracementHoursText.setEnabled(self.showHoursTextFlag)
        self.timeRetracementDaysText.setEnabled(self.showDaysTextFlag)
        self.timeRetracementWeeksText.setEnabled(self.showWeeksTextFlag)
        self.timeRetracementMonthsText.setEnabled(self.showMonthsTextFlag)

        self.timeRetracementSqrtBarsText.setEnabled(self.showSqrtBarsTextFlag)
        self.timeRetracementSqrtHoursText.setEnabled(self.showSqrtHoursTextFlag)
        self.timeRetracementSqrtDaysText.setEnabled(self.showSqrtDaysTextFlag)
        self.timeRetracementSqrtWeeksText.setEnabled(self.showSqrtWeeksTextFlag)
        self.timeRetracementSqrtMonthsText.setEnabled(self.showSqrtMonthsTextFlag)
        
        self.timeRetracementBarsText.setVisible(self.showBarsTextFlag)
        self.timeRetracementHoursText.setVisible(self.showHoursTextFlag)
        self.timeRetracementDaysText.setVisible(self.showDaysTextFlag)
        self.timeRetracementWeeksText.setVisible(self.showWeeksTextFlag)
        self.timeRetracementMonthsText.setVisible(self.showMonthsTextFlag)

        self.timeRetracementSqrtBarsText.setVisible(self.showSqrtBarsTextFlag)
        self.timeRetracementSqrtHoursText.setVisible(self.showSqrtHoursTextFlag)
        self.timeRetracementSqrtDaysText.setVisible(self.showSqrtDaysTextFlag)
        self.timeRetracementSqrtWeeksText.setVisible(self.showSqrtWeeksTextFlag)
        self.timeRetracementSqrtMonthsText.setVisible(self.showSqrtMonthsTextFlag)
        
        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.timeRetracementTextFont)
        
            # Set the pen color of the text.
            self.timeRetracementTextPen = textItem.pen()
            self.timeRetracementTextPen.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setPen(self.timeRetracementTextPen)

            # Set the brush color of the text.
            self.timeRetracementTextBrush = textItem.brush()
            self.timeRetracementTextBrush.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setBrush(self.timeRetracementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.timeRetracementTextXScaling, \
                                self.timeRetracementTextYScaling)
            textItem.setTransform(textTransform)

        # Update the timeRetracement text item position.
        self._updateTextItemPositions()

        # Set the new color of the pen for drawing the bar.
        self.timeRetracementPen.\
            setColor(self.timeRetracementGraphicsItemColor)
        
        # Schedule an update.
        self.update()

        self.log.debug("Exiting loadSettingsFromPriceBarChartSettings()")
        
    def loadSettingsFromAppPreferences(self):
        """Reads some of the parameters/settings of this
        PriceBarGraphicsItem from the QSettings object. 
        """

        # No settings.
        
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
            self.recalculateTimeRetracement()
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
                    # ruler.

                    # Do the move.
                    super().mouseMoveEvent(event)
                    
                    # Emit that the PriceBarChart has changed.
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

            self.prepareGeometryChange()
            
            self.scene().priceBarChartChanged.emit()
            
        elif self.draggingEndPointFlag == True:
            self.log.debug("mouseReleaseEvent() when previously dragging " +
                           "endPoint.")
            
            self.draggingEndPointFlag = False

            # Make sure the starting point is to the left of the
            # ending point.
            self.normalizeStartAndEnd()

            self.prepareGeometryChange()
            
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

    def _updateTextItemPositions(self):
        """Updates the location of the internal text items based on
        where the start and end points are.
        """
        
        # Update the timeRetracement label position.
            
        # X location where to place the item.
        deltaX = self.endPointF.x() - self.startPointF.x()
        x = deltaX / 2

        # Starting Y location to place the text item.
        startY = -2.0

        # Amount to mutiply to get a largest offset from startY.
        offsetY = 1.5

        # j is the running index of the enabled text item.
        j = 0

        # Go through in reverse order since we are placing the
        # items relative to the bar (moving outwards).
        for i in reversed(range(len(self.textItems))):
            # Get the current text item.
            textItem = self.textItems[i]

            # Set the position no matter what, but only increment
            # j if the item is enabled and displayed.  This is so
            # we keep the text items on the graphicsScene close to
            # its parent item.
            y = (startY - (offsetY * j)) * \
                self.timeRetracementGraphicsItemBarHeight
            textItem.setPos(QPointF(x, y))
            if textItem.isEnabled() and textItem.isVisible():
                j += 1
                    
    def setStartPointF(self, pointF):
        """Sets the starting point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        x = pointF.x()

        newValue = QPointF(x, self.endPointF.y())

        if self.startPointF != newValue: 
            self.startPointF = newValue

            self.setPos(self.startPointF)

            # Update the timeRetracement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timeretracement.
                self.recalculateTimeRetracement()
                self.update()
                
    def setEndPointF(self, pointF):
        """Sets the ending point of the bar count.  The value passed in
        is the mouse location in scene coordinates.  
        """

        x = pointF.x()

        newValue = QPointF(x, self.startPointF.y())

        if self.endPointF != newValue:
            self.endPointF = newValue

            # Update the timeRetracement text item position.
            self._updateTextItemPositions()
            
            if self.scene() != None:
                # Re-calculate the timeretracement.
                self.recalculateTimeRetracement()
                self.update()

    def normalizeStartAndEnd(self):
        """Sets the starting point X location to be less than the ending
        point X location.
        """

        if self.startPointF.x() > self.endPointF.x():
            self.log.debug("Normalization of TimeRetracementGraphicsItem " +
                           "required.")
            
            # Swap the points.
            temp = self.startPointF
            self.startPointF = self.endPointF
            self.endPointF = temp

            # Update the timeRetracement text item position.
            self._updateTextItemPositions()
            
            self.recalculateTimeRetracement()
            
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

    def recalculateTimeRetracement(self):
        """Sets the internal variables:
        
            self.numPriceBars
            self.numHours
            self.numDays
            self.numWeeks
            self.numMonths

            self.numSqrtPriceBars
            self.numSqrtHours
            self.numSqrtDays
            self.numSqrtWeeks
            self.numSqrtMonths

        to hold the amount of time between the start and end points.
        """

        scene = self.scene()

        # Reset the values.
        self.numPriceBars = 0.0
        self.numHours = 0.0
        self.numDays = 0.0
        self.numWeeks = 0.0
        self.numMonths = 0.0

        self.numSqrtPriceBars = 0.0
        self.numSqrtHours = 0.0
        self.numSqrtDays = 0.0
        self.numSqrtWeeks = 0.0
        self.numSqrtMonths = 0.0
        
        if scene != None:
            # Get all the QGraphicsItems.
            graphicsItems = scene.items()

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
        
            # Calculate the number of (calendar) days.
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

            # Calculate number of days.
            self.numDays = timeDelta.days
            self.numDays += (timeDelta.seconds / 86400.0)

            # Calculate number of hours.
            self.numHours = self.numDays * 24.0
            
            # Calculate number of weeks.
            self.numWeeks = self.numDays / 7.0

            # Calculate number of months.
            daysInMonth = 365.242199 / 12.0
            self.numMonths = self.numDays / daysInMonth

            self.log.debug("self.numPriceBars={}".format(self.numPriceBars))
            self.log.debug("self.numHours={}".format(self.numHours))
            self.log.debug("self.numDays={}".format(self.numDays))
            self.log.debug("self.numWeeks={}".format(self.numWeeks))
            self.log.debug("self.numMonths={}".format(self.numMonths))
            
            self.numSqrtPriceBars = math.sqrt(abs(self.numPriceBars))
            self.numSqrtHours = math.sqrt(abs(self.numHours))
            self.numSqrtDays = math.sqrt(abs(self.numDays))
            self.numSqrtWeeks = math.sqrt(abs(self.numWeeks))
            self.numSqrtMonths = math.sqrt(abs(self.numMonths))

            self.log.debug("self.numSqrtPriceBars={}".format(self.numSqrtPriceBars))
            self.log.debug("self.numSqrtHours={}".format(self.numSqrtHours))
            self.log.debug("self.numSqrtDays={}".format(self.numSqrtDays))
            self.log.debug("self.numSqrtWeeks={}".format(self.numSqrtWeeks))
            self.log.debug("self.numSqrtMonths={}".format(self.numSqrtMonths))
            
        # Update the text of the internal items.
        barsText = "{} B".format(self.numPriceBars)
        hoursText = "{:.2f} H".format(self.numHours)
        daysText = "{:.2f} CD".format(self.numDays)
        weeksText = "{:.2f} W".format(self.numWeeks)
        monthsText = "{:.2f} M".format(self.numMonths)
        
        sqrtBarsText = "{:.2f} sqrt B".format(self.numSqrtPriceBars)
        sqrtHoursText = "{:.2f} sqrt H".format(self.numSqrtHours)
        sqrtDaysText = "{:.2f} sqrt CD".format(self.numSqrtDays)
        sqrtWeeksText = "{:.2f} sqrt W".format(self.numSqrtWeeks)
        sqrtMonthsText = "{:.2f} sqrt M".format(self.numSqrtMonths)
        
        self.timeRetracementBarsText.setText(barsText)
        self.timeRetracementHoursText.setText(hoursText)
        self.timeRetracementDaysText.setText(daysText)
        self.timeRetracementWeeksText.setText(weeksText)
        self.timeRetracementMonthsText.setText(monthsText)
        
        self.timeRetracementSqrtBarsText.setText(sqrtBarsText)
        self.timeRetracementSqrtHoursText.setText(sqrtHoursText)
        self.timeRetracementSqrtDaysText.setText(sqrtDaysText)
        self.timeRetracementSqrtWeeksText.setText(sqrtWeeksText)
        self.timeRetracementSqrtMonthsText.setText(sqrtMonthsText)
        
    def setArtifact(self, artifact):
        """Loads a given PriceBarChartTimeRetracementArtifact object's data
        into this QGraphicsItem.

        Arguments:
        artifact - PriceBarChartTimeRetracementArtifact object with information
                   about this TextGraphisItem
        """

        self.log.debug("Entering setArtifact()")

        if isinstance(artifact, PriceBarChartTimeRetracementArtifact):
            self.artifact = artifact
        else:
            raise TypeError("Expected artifact type: " + \
                            "PriceBarChartTimeRetracementArtifact")

        # Extract and set the internals according to the info 
        # in this artifact object.
        self.setPos(self.artifact.getPos())
        self.setStartPointF(self.artifact.getStartPointF())
        self.setEndPointF(self.artifact.getEndPointF())

        self.timeRetracementTextXScaling = self.artifact.getTextXScaling()
        self.timeRetracementTextYScaling = self.artifact.getTextYScaling()
        self.timeRetracementTextFont = self.artifact.getFont()
        self.timeRetracementGraphicsItemTextColor = self.artifact.getTextColor()
        self.timeRetracementPen.setColor(self.artifact.getColor())
        
        self.showBarsTextFlag = self.artifact.getShowBarsTextFlag()
        self.showHoursTextFlag = self.artifact.getShowHoursTextFlag()
        self.showDaysTextFlag = self.artifact.getShowDaysTextFlag()
        self.showWeeksTextFlag = self.artifact.getShowWeeksTextFlag()
        self.showMonthsTextFlag = self.artifact.getShowMonthsTextFlag()
        
        self.showSqrtBarsTextFlag = self.artifact.getShowSqrtBarsTextFlag()
        self.showSqrtHoursTextFlag = self.artifact.getShowSqrtHoursTextFlag()
        self.showSqrtDaysTextFlag = self.artifact.getShowSqrtDaysTextFlag()
        self.showSqrtWeeksTextFlag = self.artifact.getShowSqrtWeeksTextFlag()
        self.showSqrtMonthsTextFlag = self.artifact.getShowSqrtMonthsTextFlag()

        #############

        # Set the text items as enabled or disabled, visible or invisible.
        self.timeRetracementBarsText.setEnabled(self.showBarsTextFlag)
        self.timeRetracementHoursText.setEnabled(self.showHoursTextFlag)
        self.timeRetracementDaysText.setEnabled(self.showDaysTextFlag)
        self.timeRetracementWeeksText.setEnabled(self.showWeeksTextFlag)
        self.timeRetracementMonthsText.setEnabled(self.showMonthsTextFlag)

        self.timeRetracementSqrtBarsText.setEnabled(self.showSqrtBarsTextFlag)
        self.timeRetracementSqrtHoursText.setEnabled(self.showSqrtHoursTextFlag)
        self.timeRetracementSqrtDaysText.setEnabled(self.showSqrtDaysTextFlag)
        self.timeRetracementSqrtWeeksText.setEnabled(self.showSqrtWeeksTextFlag)
        self.timeRetracementSqrtMonthsText.setEnabled(self.showSqrtMonthsTextFlag)
        
        self.timeRetracementBarsText.setVisible(self.showBarsTextFlag)
        self.timeRetracementHoursText.setVisible(self.showHoursTextFlag)
        self.timeRetracementDaysText.setVisible(self.showDaysTextFlag)
        self.timeRetracementWeeksText.setVisible(self.showWeeksTextFlag)
        self.timeRetracementMonthsText.setVisible(self.showMonthsTextFlag)

        self.timeRetracementSqrtBarsText.setVisible(self.showSqrtBarsTextFlag)
        self.timeRetracementSqrtHoursText.setVisible(self.showSqrtHoursTextFlag)
        self.timeRetracementSqrtDaysText.setVisible(self.showSqrtDaysTextFlag)
        self.timeRetracementSqrtWeeksText.setVisible(self.showSqrtWeeksTextFlag)
        self.timeRetracementSqrtMonthsText.setVisible(self.showSqrtMonthsTextFlag)
        
        # Update all the text items with the new settings.
        for textItem in self.textItems:
            # Set the font of the text.
            textItem.setFont(self.timeRetracementTextFont)
        
            # Set the pen color of the text.
            self.timeRetracementTextPen = textItem.pen()
            self.timeRetracementTextPen.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setPen(self.timeRetracementTextPen)

            # Set the brush color of the text.
            self.timeRetracementTextBrush = textItem.brush()
            self.timeRetracementTextBrush.\
                setColor(self.timeRetracementGraphicsItemTextColor)
            
            textItem.setBrush(self.timeRetracementTextBrush)

            # Apply some size scaling to the text.
            textTransform = QTransform()
            textTransform.scale(self.timeRetracementTextXScaling, \
                                self.timeRetracementTextYScaling)
            textItem.setTransform(textTransform)

        # Update the timeRetracement text item position.
        self._updateTextItemPositions()
            
        # Need to recalculate the time retracement, since the start and end
        # points have changed.  Note, if no scene has been set for the
        # QGraphicsView, then the time retracements will be zero, since it
        # can't look up PriceBarGraphicsItems in the scene.
        self.recalculateTimeRetracement()

        self.log.debug("Exiting setArtifact()")

    def getArtifact(self):
        """Returns a PriceBarChartTimeRetracementArtifact for this
        QGraphicsItem so that it may be pickled.
        """
        
        self.log.debug("Entered getArtifact()")
        
        # Update the internal self.priceBarChartTimeRetracementArtifact 
        # to be current, then return it.

        self.artifact.setPos(self.pos())
        self.artifact.setStartPointF(self.startPointF)
        self.artifact.setEndPointF(self.endPointF)
        
        self.artifact.setTextXScaling(self.timeRetracementTextXScaling)
        self.artifact.setTextYScaling(self.timeRetracementTextYScaling)
        self.artifact.setFont(self.timeRetracementTextFont)
        self.artifact.setTextColor(self.timeRetracementGraphicsItemTextColor)
        self.artifact.setColor(self.timeRetracementPen.color())
        
        self.artifact.setShowBarsTextFlag(self.showBarsTextFlag)
        self.artifact.setShowHoursTextFlag(self.showHoursTextFlag)
        self.artifact.setShowDaysTextFlag(self.showDaysTextFlag)
        self.artifact.setShowWeeksTextFlag(self.showWeeksTextFlag)
        self.artifact.setShowMonthsTextFlag(self.showMonthsTextFlag)
        
        self.artifact.setShowSqrtBarsTextFlag(self.showSqrtBarsTextFlag)
        self.artifact.setShowSqrtHoursTextFlag(self.showSqrtHoursTextFlag)
        self.artifact.setShowSqrtDaysTextFlag(self.showSqrtDaysTextFlag)
        self.artifact.setShowSqrtWeeksTextFlag(self.showSqrtWeeksTextFlag)
        self.artifact.setShowSqrtMonthsTextFlag(self.showSqrtMonthsTextFlag)
        
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
                    (self.timeRetracementGraphicsItemBarHeight / 2.0))
        
        bottomRight = \
            QPointF(xDelta, 1.0 *
                    (self.timeRetracementGraphicsItemBarHeight / 2.0))

        # Initalize to the above boundaries.  We will set them below.
        localHighY = topLeft.y()
        localLowY = bottomRight.y()
        if self.drawVerticalDottedLinesFlag or self.isSelected():
            # Get the highest high, and lowest low PriceBar in local
            # coordinates.
            highestPrice = self.scene().getHighestPriceBar().high
            highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
            localHighestPriceBarY = \
                       self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()

            # Overwrite the high if it is larger.
            if localHighestPriceBarY > localHighY:
                localHighY = localHighestPriceBarY
                
            lowestPrice = self.scene().getLowestPriceBar().low
            lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
            localLowestPriceBarY = \
                      self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
            
            # Overwrite the low if it is smaller.
            if localLowestPriceBarY < localLowY:
                localLowY = localLowestPriceBarY
                
        xValues = []
        xValues.append(topLeft.x())
        xValues.append(bottomRight.x())

        yValues = []
        yValues.append(topLeft.y())
        yValues.append(bottomRight.y())
        yValues.append(localHighY)
        yValues.append(localLowY)

        xValues.sort()
        yValues.sort()
        
        # Find the smallest x and y.
        smallestX = xValues[0]
        smallestY = yValues[0]
        
        # Find the largest x and y.
        largestX = xValues[-1]
        largestY = yValues[-1]
            
        rv = QRectF(QPointF(smallestX, smallestY),
                    QPointF(largestX, largestY))

        return rv

    def shape(self):
        """Overwrites the QGraphicsItem.shape() function to return a
        more accurate shape for collision detection, hit tests, etc.
        """

        # Get the QRectF with just the lines.
        xDelta = self.endPointF.x() - self.startPointF.x()
        
        topLeft = \
            QPointF(0.0, -1.0 *
                    (self.timeRetracementGraphicsItemBarHeight / 2.0))
        
        bottomRight = \
            QPointF(xDelta, 1.0 *
                    (self.timeRetracementGraphicsItemBarHeight / 2.0))

        rectWithoutText = QRectF(topLeft, bottomRight)

        painterPath = QPainterPath()
        painterPath.addRect(rectWithoutText)

        return painterPath
        
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

        if painter.pen() != self.timeRetracementPen:
            painter.setPen(self.timeRetracementPen)
        
        # Keep track of x and y values.  We use this to draw the
        # dotted lines later.
        xValues = []
        yValues = []
        
        # Draw the left vertical bar part.
        x1 = 0.0
        y1 = 1.0 * (self.timeRetracementGraphicsItemBarHeight / 2.0)
        x2 = 0.0
        y2 = -1.0 * (self.timeRetracementGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the right vertical bar part.
        xDelta = self.endPointF.x() - self.startPointF.x()
        x1 = 0.0 + xDelta
        y1 = 1.0 * (self.timeRetracementGraphicsItemBarHeight / 2.0)
        x2 = 0.0 + xDelta
        y2 = -1.0 * (self.timeRetracementGraphicsItemBarHeight / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw the middle horizontal line.
        x1 = 0.0
        y1 = 0.0
        x2 = xDelta
        y2 = 0.0
        painter.drawLine(QLineF(x1, y1, x2, y2))

        xValues.append(x1)
        xValues.append(x2)
        yValues.append(y1)
        yValues.append(y2)
        
        # Draw vertical dotted lines at each enabled tick area if the
        # flag is set to do so, or if it is selected.
        if self.drawVerticalDottedLinesFlag == True or \
           option.state & QStyle.State_Selected:

            if self.scene() != None:
                pad = self.timeRetracementPen.widthF() / 2.0;
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
    
                # Get the highest high, and lowest low PriceBar in local
                # coordinates.
                highestPrice = self.scene().getHighestPriceBar().high
                highestPriceBarY = self.scene().priceToSceneYPos(highestPrice)
                localHighY = \
                    self.mapFromScene(QPointF(0.0, highestPriceBarY)).y()
                
                lowestPrice = self.scene().getLowestPriceBar().low
                lowestPriceBarY = self.scene().priceToSceneYPos(lowestPrice)
                localLowY = \
                    self.mapFromScene(QPointF(0.0, lowestPriceBarY)).y()
                          
                yValues.append(localHighY)
                yValues.append(localLowY)

                # We have all y values now, so sort them to get the
                # low and high.
                yValues.sort()
                smallestY = yValues[0]
                largestY = yValues[-1]
        
                # Vertical line at the beginning.
                localPosX = 0.0
                startPoint = QPointF(localPosX, largestY)
                endPoint = QPointF(localPosX, smallestY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
            
                # Vertical line at the end.
                localPosX = 0.0 + xDelta
                startPoint = QPointF(localPosX, largestY)
                endPoint = QPointF(localPosX, smallestY)
                        
                painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
                painter.setPen(QPen(option.palette.windowText(), 0,
                                    Qt.DashLine))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(startPoint, endPoint)
                
        # Draw the bounding rect if the item is selected.
        if option.state & QStyle.State_Selected:
            pad = self.timeRetracementPen.widthF() / 2.0;
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
            
            painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.shape())

    def appendActionsToContextMenu(self, menu, readOnlyMode=False):
        """Modifies the given QMenu object to update the title and add
        actions relevant to this TimeRetracementGraphicsItem.  Actions that
        are triggered from this menu run various methods in the
        TimeRetracementGraphicsItem to handle the desired functionality.
        
        Arguments:
        menu - QMenu object to modify.
        readOnlyMode - bool value that indicates the actions are to be
                       readonly actions.
        """

        menu.setTitle(self.artifact.getInternalName())
        
        # These are the QActions that are in the menu.
        parent = menu
        selectAction = QAction("&Select", parent)
        unselectAction = QAction("&Unselect", parent)
        removeAction = QAction("Remove", parent)
        infoAction = QAction("&Info", parent)
        editAction = QAction("&Edit", parent)
        setStartOnAstro1Action = \
            QAction("Set start timestamp on Astro Chart &1", parent)
        setStartOnAstro2Action = \
            QAction("Set start timestamp on Astro Chart &2", parent)
        setStartOnAstro3Action = \
            QAction("Set start timestamp on Astro Chart &3", parent)
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
        
        scene = self.scene()
        scene.removeItem(self)

        # Emit signal to show that an item is removed.
        # This sets the dirty flag.
        scene.priceBarChartArtifactGraphicsItemRemoved.emit(self)
        
    def _handleInfoAction(self):
        """Causes a dialog to be executed to show information about
        the QGraphicsItem.
        """

        artifact = self.getArtifact()
        dialog = PriceBarChartTimeRetracementArtifactEditDialog(artifact,
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
        dialog = PriceBarChartTimeRetracementArtifactEditDialog(artifact,
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
        of the start the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart1(self.startPointF.x())
        
    def _handleSetStartOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the start the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart2(self.startPointF.x())
        
    def _handleSetStartOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the start the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart3(self.startPointF.x())
        
    def _handleSetEndOnAstro1Action(self):
        """Causes the astro chart 1 to be set with the timestamp
        of the end the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart1(self.endPointF.x())

    def _handleSetEndOnAstro2Action(self):
        """Causes the astro chart 2 to be set with the timestamp
        of the end the TimeRetracementGraphicsItem.
        """

        self.scene().setAstroChart2(self.endPointF.x())

    def _handleSetEndOnAstro3Action(self):
        """Causes the astro chart 3 to be set with the timestamp
        of the end the TimeRetracementGraphicsItem.
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

    # Signal emitted when a status message should be printed.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
    # Signal emitted when the user desires to change astro chart 1.
    astroChart1Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 2.
    astroChart2Update = QtCore.pyqtSignal(datetime.datetime)
    
    # Signal emitted when the user desires to change astro chart 3.
    astroChart3Update = QtCore.pyqtSignal(datetime.datetime)
    
    
    # Tool modes that this widget can be in.
    ToolMode = {"ReadOnlyPointerTool"  : 0,
                "PointerTool"          : 1,
                "HandTool"             : 2,
                "ZoomInTool"           : 3,
                "ZoomOutTool"          : 4,
                "BarCountTool"         : 5,
                "TimeMeasurementTool"  : 6,
                "ModalScaleTool"       : 7,
                "TextTool"             : 8,
                "PriceTimeInfoTool"    : 9,
                "PriceMeasurementTool" : 10,
                "TimeRetracementTool"  : 11 }



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
        smallMonospacedFont = QFont()
        smallMonospacedFont.setFamily("DejaVu Sans Mono")
        smallMonospacedFont.setPointSize(7)
        self.cursorLocalizedTimestampLabel.setFont(smallMonospacedFont)
        self.cursorUtcTimestampLabel.setFont(smallMonospacedFont)
        self.cursorPriceLabel.setFont(smallMonospacedFont)
        
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
        self.graphicsView.statusMessageUpdate.\
            connect(self.statusMessageUpdate)
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

    def setBirthInfo(self, birthInfo):
        """Sets the birth info for this trading entity.
        
        Arguments:

        birthInfo - BirthInfo object.
        """

        # Pass the information to the graphics scene.  If graphics
        # items need it, it will get it from there.
        self.graphicsScene.setBirthInfo(birthInfo)
        
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

            elif isinstance(artifact, PriceBarChartTextArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = TextGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)

                self.log.debug("Before setting artifact, " +
                               "internal artifact is: " +
                               newItem.getArtifact().toString())
                
                newItem.setArtifact(artifact)

                self.log.debug("After  setting artifact, " +
                               "internal artifact is: " +
                               newItem.getArtifact().toString())
                
                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                self.log.debug("After  adding item,      " +
                               "internal artifact is: " +
                               newItem.getArtifact().toString())
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                addedItemFlag = True
                
            elif isinstance(artifact, PriceBarChartPriceTimeInfoArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = PriceTimeInfoGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)

                # Set the conversion object as the scene so that it
                # can do initial calculations for the text to display.
                newItem.setConvertObj(self.graphicsScene)

                # Set the artifact offically so that it can update the text.
                newItem.setArtifact(artifact)

                # Set the birthInfo in the new item.  This will again
                # trigger a text update.
                birthInfo = self.graphicsScene.getBirthInfo()
                newItem.setBirthInfo(birthInfo)
                
                # Add the item to the graphics scene.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartPriceMeasurementArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = PriceMeasurementGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate price measurement, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculatePriceMeasurement()
        
                addedItemFlag = True

            elif isinstance(artifact, PriceBarChartTimeRetracementArtifact):
                self.log.debug("Loading artifact: " + artifact.toString())
                
                newItem = TimeRetracementGraphicsItem()
                newItem.loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                newItem.setArtifact(artifact)

                # Add the item.
                self.graphicsScene.addItem(newItem)
                
                # Make sure the proper flags are set for the mode we're in.
                self.graphicsView.setGraphicsItemFlagsPerCurrToolMode(newItem)

                # Need to recalculate time retracement, since it wasn't in
                # the QGraphicsScene until now.
                newItem.recalculateTimeRetracement()
        
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
                self.log.debug("Not applying settings to " +
                               "TimeMeasurementGraphicsItem.")
            elif isinstance(item, ModalScaleGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "ModalScaleGraphicsItem.")
            elif isinstance(item, TextGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "TextGraphicsItem.")
            elif isinstance(item, PriceTimeInfoGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "PriceTimeInfoGraphicsItem.")
            elif isinstance(item, PriceMeasurementGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "PriceMeasurementGraphicsItem.")
            elif isinstance(item, TimeRetracementGraphicsItem):
                self.log.debug("Not applying settings to " +
                               "TimeRetracementGraphicsItem.")

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

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.log.debug("Entered toTextToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['TextTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['TextTool']
            self.graphicsView.toTextToolMode()

        self.log.debug("Exiting toTextToolMode()")

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.log.debug("Entered toPriceTimeInfoToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['PriceTimeInfoTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['PriceTimeInfoTool']
            self.graphicsView.toPriceTimeInfoToolMode()

        self.log.debug("Exiting toPriceTimeInfoToolMode()")

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.log.debug("Entered toPriceMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
               PriceBarChartWidget.ToolMode['PriceMeasurementTool']:
            
            self.toolMode = PriceBarChartWidget.ToolMode['PriceMeasurementTool']
            self.graphicsView.toPriceMeasurementToolMode()

        self.log.debug("Exiting toPriceMeasurementToolMode()")

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.log.debug("Entered toTimeRetracementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartWidget.ToolMode['TimeRetracementTool']:
            self.toolMode = PriceBarChartWidget.ToolMode['TimeRetracementTool']
            self.graphicsView.toTimeRetracementToolMode()

        self.log.debug("Exiting toTimeRetracementToolMode()")

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

        # Logger
        self.log = logging.getLogger("pricebarchart.PriceBarChartGraphicsScene")

        # Holds the BirthInfo object.  This is used in calculating
        # information related to astrology.
        self.birthInfo = None
        
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

    def setBirthInfo(self, birthInfo):
        """Sets the birth info for this trading entity.
        
        Arguments:

        birthInfo - BirthInfo object.
        """

        self.birthInfo = birthInfo

        # Go through all the current items, and for every time that
        # needs a current BirthInfo, then set the birthInfo in that
        # item.

        graphicsItems = self.items()
        for item in graphicsItems:
            if isinstance(item, PriceTimeInfoGraphicsItem):
                # Setting birthInfo on this object will cause the
                # whole widget to update it's internal text and info
                # accordingly.
                item.setBirthInfo(self.birthInfo)

    def getBirthInfo(self):
        """Returns the birthInfo for this trading entity as a BirthInfo object.
        """

        return self.birthInfo
    
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


    def getEarliestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the earliest timestamp.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object that has the earliest timestamp.
        """

        earliestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if earliestPriceBar == None:
                    earliestPriceBar = pb
                elif pb.timestamp < earliestPriceBar.timestamp:
                    earliestPriceBar = pb
                    
        return earliestPriceBar

    def getLatestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the latest timestamp.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object that has the latest timestamp.
        """

        latestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if latestPriceBar == None:
                    latestPriceBar = pb
                elif pb.timestamp > latestPriceBar.timestamp:
                    latestPriceBar = pb
                    
        return latestPriceBar

    def getHighestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the highest high price.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object for the highest pricebar in price.
        """

        highestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if highestPriceBar == None:
                    highestPriceBar = pb
                elif pb.hasHigherHighThan(highestPriceBar):
                    highestPriceBar = pb
                    
        
        return highestPriceBar

    def getLowestPriceBar(self):
        """Goes through all the PriceBars, looking at the one that has
        the lowest low price.  This pricebar is returned.
        
        Returns:
        PriceBar - PriceBar object for the lowest pricebar in price.
        """

        lowestPriceBar = None
        
        graphicsItems = self.items()

        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                pb = item.getPriceBar()

                if lowestPriceBar == None:
                    lowestPriceBar = pb
                elif pb.hasLowerLowThan(lowestPriceBar):
                    lowestPriceBar = pb
        
        return lowestPriceBar

    def getClosestPriceBarOHLCPoint(self, pointF):
        """Goes through all the PriceBars, looking at the QPointF of
        the open, high, low, and close of each bar (in price and
        time), and tests it to locate the point out of all the bars
        that is the closest to 'pointF'.

        WARNING: This may not do what you expect to do!  The reason is
        because our current scaling for time (x coordinate) is 1 unit
        of x per day.  Our price scaling (y coordinate) is 1 unit of
        price per y.  This means the 'qgraphicsview' scaling of x and
        y (in appearance) is misleading when compared to actual
        coordinates.  So the algorithm works correctly, but may not
        produce expected results due to a huge skew in scaling.
        
        Returns:
        QPointF - Point that is a scene pos of a open, high, low,
                  or close of a PriceBar, where it is the closest
                  to the given 'pointF'.
        """

        self.log.debug("Entered getClosestPriceBarOHLCPoint()")
        
        # QPointF for the closest point.
        closestPoint = None

        # Smallest length of line from pointF to desired point.
        smallestLength = None
        
        # PriceBarGraphicsItem that is the closest.
        closestPriceBarGraphicsItem = None
        
        graphicsItems = self.items()

        self.log.debug("PointF is: ({}, {})".format(pointF.x(), pointF.y()))
                       
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):
                # Get the points of the open, high, low, and close of
                # this PriceBarGraphicsItem.
                openPointF = item.getPriceBarOpenScenePoint()
                highPointF = item.getPriceBarHighScenePoint()
                lowPointF = item.getPriceBarLowScenePoint()
                closePointF = item.getPriceBarCloseScenePoint()

                self.log.debug("openPointF is: ({}, {})".
                               format(openPointF.x(), openPointF.y()))
                self.log.debug("highPointF is: ({}, {})".
                               format(highPointF.x(), highPointF.y()))
                self.log.debug("lowPointF is: ({}, {})".
                               format(lowPointF.x(), lowPointF.y()))
                self.log.debug("closePointF is: ({}, {})".
                               format(closePointF.x(), closePointF.y()))

                # Create lines so we can get the lengths between the points.
                lineToOpen = QLineF(pointF, openPointF)
                lineToHigh = QLineF(pointF, highPointF)
                lineToLow = QLineF(pointF, lowPointF)
                lineToClose = QLineF(pointF, closePointF)

                lineToOpenLength = lineToOpen.length()
                lineToHighLength = lineToHigh.length()
                lineToLowLength = lineToLow.length()
                lineToCloseLength = lineToClose.length()
                
                self.log.debug("lineToOpenLength is: {}".\
                               format(lineToOpenLength))
                self.log.debug("lineToHighLength is: {}".\
                               format(lineToHighLength))
                self.log.debug("lineToLowLength is: {}".\
                               format(lineToLowLength))
                self.log.debug("lineToCloseLength is: {}".\
                               format(lineToCloseLength))

                # Set the initial smallestLength as the first point if
                # it is not set already.
                if smallestLength == None:
                    closestPoint = openPointF
                    smallestLength = lineToOpen.length()
                    closestPriceBarGraphicsItem = item

                # Test the open, high, low, and close points to see if
                # they are now the closest to pointF.
                if lineToOpenLength < smallestLength:
                    closestPoint = openPointF
                    smallestLength = lineToOpenLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))

                if lineToHighLength < smallestLength:
                    closestPoint = highPointF
                    smallestLength = lineToHighLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))

                if lineToLowLength < smallestLength:
                    closestPoint = lowPointF
                    smallestLength = lineToLowLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))

                if lineToCloseLength < smallestLength:
                    closestPoint = closePointF
                    smallestLength = lineToCloseLength
                    closestPriceBarGraphicsItem = item
                    self.log.debug("New closest point is now: " +
                                   "({}, {})".format(closestPoint.x(),
                                                     closestPoint.y()))
                    
        self.log.debug("Closest point is: ({}, {})".format(closestPoint.x(),
                                                           closestPoint.y()))

        self.log.debug("Exiting getClosestPriceBarOHLCPoint()")
        
        return closestPoint

    def getClosestPriceBarX(self, pointF):
        """Gets the X position value of the closest PriceBar (on the X
        axis) to the given QPointF position.

        Arguments:
        pointF - QPointF to do the lookup on.

        Returns:
        float value for the X value.  If there are no PriceBars, then it
        returns the X given in the input pointF.
        """

        # Get all the QGraphicsItems.
        graphicsItems = self.items()

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

    def getClosestPriceBarOHLCY(self, pointF):
        """Gets the Y position value of the closest open, high, low,
        or close price on all the PriceBars (on the Y axis) to the
        given QPointF position.

        Arguments:
        pointF - QPointF to do the lookup on.

        Returns:
        float value for the Y value.  If there are no PriceBars, then it
        returns the Y given in the input pointF.
        """

        # Get all the QGraphicsItems.
        graphicsItems = self.items()

        closestPriceBarY = None
        currClosestDistance = None

        # Go through the PriceBarGraphicsItems and find the closest one in
        # Y coordinates.
        for item in graphicsItems:
            if isinstance(item, PriceBarGraphicsItem):

                # High price's Y.
                y = item.getPriceBarHighScenePoint().y()
                distance = abs(pointF.y() - y)
                
                if closestPriceBarY == None:
                    closestPriceBarY = y
                    currClosestDistance = distance
                elif (currClosestDistance != None) and \
                        (distance < currClosestDistance):

                    closestPriceBarY = y
                    currClosestDistance = distance

                # Low price's Y.
                y = item.getPriceBarLowScenePoint().y()
                distance = abs(pointF.y() - y)

                if closestPriceBarY == None:
                    closestPriceBarY = y
                    currClosestDistance = distance
                elif (currClosestDistance != None) and \
                        (distance < currClosestDistance):

                    closestPriceBarY = y
                    currClosestDistance = distance
                    
        if closestPriceBarY == None:
            closestPriceBarY = pointF.y()

        return closestPriceBarY

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
    ToolMode = {"ReadOnlyPointerTool"  : 0,
                "PointerTool"          : 1,
                "HandTool"             : 2,
                "ZoomInTool"           : 3,
                "ZoomOutTool"          : 4,
                "BarCountTool"         : 5,
                "TimeMeasurementTool"  : 6,
                "ModalScaleTool"       : 7,
                "TextTool"             : 8,
                "PriceTimeInfoTool"    : 9,
                "PriceMeasurementTool" : 10,
                "TimeRetracementTool"  : 11 }

    # Signal emitted when the mouse moves within the QGraphicsView.
    # The position emitted is in QGraphicsScene x, y, float coordinates.
    mouseLocationUpdate = QtCore.pyqtSignal(float, float)

    # Signal emitted when a status message should be printed.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
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

        # Variable used for storing the new TextGraphicsItem,
        # as it is modified in TextToolMode.
        self.textGraphicsItem = None
        
        # Variable used for storing the new PriceTimeInfoGraphicsItem,
        # as it is modified in PriceTimeInfoToolMode.
        self.priceTimeInfoGraphicsItem = None

        # Variable used for storing the new PriceMeasurementGraphicsItem,
        # as it is modified in PriceMeasurementToolMode.
        self.priceMeasurementGraphicsItem = None

        # Variable used for storing the new TimeRetracementGraphicsItem,
        # as it is modified in TimeRetracementToolMode.
        self.timeRetracementGraphicsItem = None

        # Variable used for storing that snapping to the closest bar
        # high or low is enabled.  Used in PriceTimeInfoTool,
        # TimeMeasurementTool, PriceMeasurementTool, TimeRetracementTool.
        self.snapEnabledFlag = True

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

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            if isinstance(item, PriceBarGraphicsItem):
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))
            elif isinstance(item, PriceBarChartArtifactGraphicsItem):
                item.setReadOnlyFlag(True)
                item.setFlags(QGraphicsItem.GraphicsItemFlags(0))

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

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

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.log.debug("Entered toTextToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['TextTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.textGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toTextToolMode()")

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.log.debug("Entered toPriceTimeInfoToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.priceTimeInfoGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toPriceTimeInfoToolMode()")

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.log.debug("Entered toPriceMeasurementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.priceMeasurementGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toPriceMeasurementToolMode()")

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.log.debug("Entered toTimeRetracementToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']

            self.setCursor(QCursor(Qt.ArrowCursor))
            self.setDragMode(QGraphicsView.NoDrag)

            # Clear out internal working variables.
            self.clickOnePointF = None
            self.clickTwoPointF = None
            self.timeRetracementGraphicsItem = None

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

                items = scene.items()
                for item in items:
                    self.setGraphicsItemFlagsPerCurrToolMode(item)
                    
        self.log.debug("Exiting toTimeRetracementToolMode()")

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
                # See what item type(s) are selected and take action
                # based on that.

                scene = self.scene()
                selectedItems = scene.selectedItems()

                for item in selectedItems:
                    if isinstance(item, ModalScaleGraphicsItem):
                        if qkeyevent.key() == Qt.Key_S:
                            item.rotateUp()
                            self.statusMessageUpdate.emit(\
                                "ModalScaleGraphicsItem rotated UP")
                        elif qkeyevent.key() == Qt.Key_G:
                            item.rotateDown()
                            self.statusMessageUpdate.emit(\
                                "ModalScaleGraphicsItem rotated DOWN")
                        elif qkeyevent.key() == Qt.Key_R:
                            item.reverse()
                            self.statusMessageUpdate.emit(\
                                "ModalScaleGraphicsItem reversed")

                # Pass the key event upwards in case it applies to
                # something else (like a parent widget).
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
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
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

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.textGraphicsItem != None:
                    self.scene().removeItem(self.textGraphicsItem)

                self.textGraphicsItem = None
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.priceTimeInfoGraphicsItem != None:
                    self.scene().removeItem(self.priceTimeInfoGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.priceTimeInfoGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.priceMeasurementGraphicsItem != None:
                    self.scene().removeItem(self.priceMeasurementGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.priceMeasurementGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
            else:
                super().keyPressEvent(qkeyevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            if qkeyevent.key() == Qt.Key_Escape:
                # Escape key causes any currently edited item to
                # be removed and cleared out.  Temporary variables used
                # are cleared out too.
                if self.timeRetracementGraphicsItem != None:
                    self.scene().removeItem(self.timeRetracementGraphicsItem)

                self.clickOnePointF = None
                self.clickTwoPointF = None
                self.timeRetracementGraphicsItem = None
            elif qkeyevent.key() == Qt.Key_Q:
                # Turn on snap functionality.
                self.snapEnabledFlag = True
                self.log.debug("Snap mode enabled.")
                self.statusMessageUpdate.emit("Snap mode enabled")
            elif qkeyevent.key() == Qt.Key_W:
                # Turn off snap functionality.
                self.snapEnabledFlag = False
                self.log.debug("Snap mode disabled.")
                self.statusMessageUpdate.emit("Snap mode disabled")
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

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickOnePointF.setX(x)
                    
                    # Create the TimeMeasurementGraphicsItem and
                    # initialize it to the mouse location.
                    self.timeMeasurementGraphicsItem = \
                        TimeMeasurementGraphicsItem()
                    self.timeMeasurementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    # Set the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.timeMeasurementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(True)
        
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

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickTwoPointF.setX(x)
                    
                    self.timeMeasurementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.timeMeasurementGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.timeMeasurementGraphicsItem.getArtifact()
                                                
                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.timeMeasurementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(False)
                    
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

                    # Set the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.modalScaleGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(True)
                    
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

                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.modalScaleGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(False)
                    
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
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:
            
            self.log.debug("Current toolMode is: TextTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")

                # Create the TextGraphicsItem and initialize it to the
                # mouse location.
                self.textGraphicsItem = TextGraphicsItem()
                self.textGraphicsItem.\
                    loadSettingsFromPriceBarChartSettings(\
                    self.priceBarChartSettings)
                self.textGraphicsItem.setPos(self.mapToScene(qmouseevent.pos()))

                # Now create and run a edit dialog for typing in the text.
                dialog = \
                    PriceBarChartTextArtifactEditDialog(\
                        self.textGraphicsItem.getArtifact(),
                        self.scene(),
                        readOnlyFlag=False)
                rv = dialog.exec_()
                
                # If the user accepts the dialog, then add the item,
                # otherwise, delete and remove.
                if rv == QDialog.Accepted:
                    self.log.debug("PriceBarChartTextArtifactEditDialog " +
                                   "accepted.")
                    self.textGraphicsItem.setArtifact(dialog.getArtifact())
                    self.scene().addItem(self.textGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.textGraphicsItem)
                else:
                    self.log.debug("PriceBarChartTextArtifactEditDialog " +
                                   "rejected.")

                self.textGraphicsItem = None
                
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                # Open a context menu at this location, in readonly mode.
                clickPosF = self.mapToScene(qmouseevent.pos())
                menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                menu.exec_(qmouseevent.globalPos())
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:
            
            self.log.debug("Current toolMode is: PriceTimeInfoTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")

                if self.clickOnePointF == None:
                    
                    self.log.debug("clickOnePointF is None.")

                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # First click sets the position and everything.
                    # Assumes that the text is above the point.
        
                    # Create the PriceTimeInfoGraphicsItem
                    self.priceTimeInfoGraphicsItem = PriceTimeInfoGraphicsItem()
                    self.priceTimeInfoGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                        self.priceBarChartSettings)

                    # Set the flag that indicates that we should draw
                    # a line from the text to the infoPointF.  This is
                    # set to false once we've fully set the item.
                    self.priceTimeInfoGraphicsItem.\
                        setDrawLineToInfoPointFFlag(True)
                    
                    # Set the conversion object as the scene so that it
                    # can do initial calculations for the text to display.
                    self.priceTimeInfoGraphicsItem.\
                        setConvertObj(self.scene())
                    
                    # Location of the graphics item.  This is calculated
                    # below, based on where the used clicked.
                    pos = QPointF()
                
                    # If snap is enabled, then find the closest high, low,
                    # open or close QPointF to the place clicked.
                    infoPointF = self.mapToScene(qmouseevent.pos())
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        # Find if there is a point closer to this
                        # infoPointF related to a PriceBarGraphicsItem.
                        barPoint = \
                            self.scene().getClosestPriceBarOHLCPoint(infoPointF)

                        # If a point was found, then use it as the info point.
                        if barPoint != None:
                            infoPointF = barPoint
                            
                            # Set this also as the first click point,
                            # as if the user clicked perfectly.
                            self.clickOnePointF = infoPointF

                    # Get and modify the artifact.
                    artifact = self.priceTimeInfoGraphicsItem.getArtifact()
                    artifact.setInfoPointF(infoPointF)

                    # Now set the artifact again so we can get an updated
                    # boundingRect size.
                    self.priceTimeInfoGraphicsItem.setArtifact(artifact)
                    boundingRect = self.priceTimeInfoGraphicsItem.boundingRect()

                    # Determine what y pos would be for this new item,
                    # assuming the text will be above the infoPointF.
                    self.priceTimeInfoGraphicsItem.\
                        setTextLabelEdgeYLocation(infoPointF.y())

                    # Set the BirthInfo.
                    birthInfo = self.scene().getBirthInfo()
                    self.priceTimeInfoGraphicsItem.setBirthInfo(birthInfo)
                    
                    # Add the item to the scene.
                    self.scene().addItem(self.priceTimeInfoGraphicsItem)
                    
                elif self.clickOnePointF != None and \
                       self.clickTwoPointF == None and \
                       self.priceTimeInfoGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeInfoGraphicsItem != None.")
                    
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())
                    
                    # Turn off the flag that indicates that we should
                    # draw a line from the text to the infoPointF.  It
                    # will now only draw that line when we have the
                    # item selected.
                    self.priceTimeInfoGraphicsItem.\
                        setDrawLineToInfoPointFFlag(False)
                    
                    # Set the position of the item by calling the set
                    # function for the Y location of the edge of the
                    # text.
                    posY = self.clickTwoPointF.y()
                    self.priceTimeInfoGraphicsItem.\
                        setTextLabelEdgeYLocation(posY)

                    # Done settings values, so clear out working variables.
                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceTimeInfoGraphicsItem = None
                    
            elif qmouseevent.button() & Qt.RightButton:
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.priceTimeInfoGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeInfoGraphicsItem != None.")
                    
                    # Right-click during setting the priceTimeInfoGraphicsItem
                    # causes the currently edited item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.priceTimeInfoGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceTimeInfoGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.priceTimeInfoGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceTimeInfoGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:
            
            self.log.debug("Current toolMode is: PriceMeasurementTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)
                        
                        # Use this Y value.
                        self.clickOnePointF.setY(y)
                    
                    # Create the PriceMeasurementGraphicsItem and
                    # initialize it to the mouse location.
                    self.priceMeasurementGraphicsItem = \
                        PriceMeasurementGraphicsItem()
                    self.priceMeasurementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    # Set the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.priceMeasurementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(True)
        
                    self.priceMeasurementGraphicsItem.\
                        setPos(self.clickOnePointF)
                    self.priceMeasurementGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.priceMeasurementGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.priceMeasurementGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.priceMeasurementGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.priceMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceMeasurementGraphicsItem != None.")
                    
                    # Set the end point of the PriceMeasurementGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar price to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        y = self.scene().getClosestPriceBarOHLCY(infoPointF)
                        
                        # Use this Y value.
                        self.clickTwoPointF.setY(y)
                    
                    self.priceMeasurementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.priceMeasurementGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.priceMeasurementGraphicsItem.getArtifact()
                                                
                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.priceMeasurementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(False)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.priceMeasurementGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.priceMeasurementGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("priceMeasurementGraphicsItem " +
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
                    self.priceMeasurementGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.priceMeasurementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceMeasurementGraphicsItem != None.")
                    
                    # Right-click during setting the
                    # PriceMeasurementGraphicsItem causes the
                    # currently edited bar count item to be removed
                    # and cleared out.  Temporary variables used are
                    # cleared out too.
                    self.scene().removeItem(self.priceMeasurementGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.priceMeasurementGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.priceMeasurementGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "priceMeasurementGraphicsItem == None.")
                    
                    # Open a context menu at this location, in readonly mode.
                    clickPosF = self.mapToScene(qmouseevent.pos())
                    menu = self.createContextMenu(clickPosF, readOnlyFlag=True)
                    menu.exec_(qmouseevent.globalPos())
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:
            
            self.log.debug("Current toolMode is: TimeRetracementTool")

            if qmouseevent.button() & Qt.LeftButton:
                self.log.debug("Qt.LeftButton")
                
                if self.clickOnePointF == None:
                    self.log.debug("clickOnePointF == None")
                
                    self.clickOnePointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickOnePointF.setX(x)
                    
                    # Create the TimeRetracementGraphicsItem and
                    # initialize it to the mouse location.
                    self.timeRetracementGraphicsItem = \
                        TimeRetracementGraphicsItem()
                    self.timeRetracementGraphicsItem.\
                        loadSettingsFromPriceBarChartSettings(\
                            self.priceBarChartSettings)
        
                    # Set the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.  We
                    # will turn these off after the user fully
                    # finishes adding the item.
                    self.timeRetracementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(True)
        
                    self.timeRetracementGraphicsItem.setPos(self.clickOnePointF)
                    self.timeRetracementGraphicsItem.\
                        setStartPointF(self.clickOnePointF)
                    self.timeRetracementGraphicsItem.\
                        setEndPointF(self.clickOnePointF)
                    self.scene().addItem(self.timeRetracementGraphicsItem)
                    
                    # Make sure the proper flags are set for the mode we're in.
                    self.setGraphicsItemFlagsPerCurrToolMode(\
                        self.timeRetracementGraphicsItem)

                elif self.clickOnePointF != None and \
                    self.clickTwoPointF == None and \
                    self.timeRetracementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeRetracementGraphicsItem != None.")
                    
                    # Set the end point of the TimeRetracementGraphicsItem.
                    self.clickTwoPointF = self.mapToScene(qmouseevent.pos())

                    # If snap is enabled, then find the closest
                    # pricebar time to the place clicked.
                    if self.snapEnabledFlag == True:
                        self.log.debug("Snap is enabled, so snapping to " +
                                       "closest pricebar X.")
                        
                        infoPointF = self.mapToScene(qmouseevent.pos())
                        x = self.scene().getClosestPriceBarX(infoPointF)

                        # Use this X value.
                        self.clickTwoPointF.setX(x)
                    
                    self.timeRetracementGraphicsItem.\
                        setEndPointF(self.clickTwoPointF)
                    self.timeRetracementGraphicsItem.normalizeStartAndEnd()
        
                    # Call getArtifact() so that the item's artifact
                    # object gets updated and set.
                    self.timeRetracementGraphicsItem.getArtifact()
                                                
                    # Unset the flag that indicates we should draw
                    # dotted vertical lines at the tick areas.
                    self.timeRetracementGraphicsItem.\
                        setDrawVerticalDottedLinesFlag(False)
                    
                    # Emit that the PriceBarChart has changed.
                    self.scene().priceBarChartArtifactGraphicsItemAdded.\
                        emit(self.timeRetracementGraphicsItem)
                    
                    sceneBoundingRect = \
                        self.timeRetracementGraphicsItem.sceneBoundingRect()
                    
                    self.log.debug("timeRetracementGraphicsItem " +
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
                    self.timeRetracementGraphicsItem = None
                    
                else:
                    self.log.warn("Unexpected state reached.")
                    
            elif qmouseevent.button() & Qt.RightButton:
                
                self.log.debug("Qt.RightButton")
                
                if self.clickOnePointF != None and \
                   self.clickTwoPointF == None and \
                   self.timeRetracementGraphicsItem != None:

                    self.log.debug("clickOnePointF != None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeRetracementGraphicsItem != None.")
                    
                    # Right-click during setting the TimeRetracementGraphicsItem
                    # causes the currently edited bar count item to be
                    # removed and cleared out.  Temporary variables used
                    # are cleared out too.
                    self.scene().removeItem(self.timeRetracementGraphicsItem)

                    self.clickOnePointF = None
                    self.clickTwoPointF = None
                    self.timeRetracementGraphicsItem = None
                    
                elif self.clickOnePointF == None and \
                     self.clickTwoPointF == None and \
                     self.timeRetracementGraphicsItem == None:
                    
                    self.log.debug("clickOnePointF == None, and " +
                                   "clickTwoPointF == None and " +
                                   "timeRetracementGraphicsItem == None.")
                    
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

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            self.log.debug("Current toolMode is: TextTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            self.log.debug("Current toolMode is: PriceTimeInfoTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            self.log.debug("Current toolMode is: PriceMeasurementTool")
            super().mouseReleaseEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            self.log.debug("Current toolMode is: TimeRetracementTool")
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

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:

            super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:

            if self.clickOnePointF != None and \
                self.priceTimeInfoGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Set the position of the item by calling the set
                # function for the Y location of the edge of the
                # text.
                posY = pos.y()
                self.priceTimeInfoGraphicsItem.setTextLabelEdgeYLocation(posY)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:

            if self.clickOnePointF != None and \
                self.priceMeasurementGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # PriceMeasurementGraphicsItem.
                self.priceMeasurementGraphicsItem.setEndPointF(pos)
            else:
                super().mouseMoveEvent(qmouseevent)

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:

            if self.clickOnePointF != None and \
                self.timeRetracementGraphicsItem != None:

                pos = self.mapToScene(qmouseevent.pos())
                
                # Update the end point of the current
                # TimeRetracementGraphicsItem.
                self.timeRetracementGraphicsItem.setEndPointF(pos)
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
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TextTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceTimeInfoTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['PriceMeasurementTool']:
            self.setCursor(QCursor(Qt.ArrowCursor))
        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['TimeRetracementTool']:
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

    
