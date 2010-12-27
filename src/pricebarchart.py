

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

# For PriceBars
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
                "ZoomOutTool"         : 4 }


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
        
        self.cursorLocalizedTimestampLabel = QLabel("")
        self.cursorUtcTimestampLabel = QLabel("")
        self.cursorPriceLabel = QLabel("")
        
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

        self.selectedPriceBarTimestampLabel.setText(timestampStr)
        
        self.selectedPriceBarOpenPriceLabel.setText(openStr)
        self.selectedPriceBarHighPriceLabel.setText(highStr)
        self.selectedPriceBarLowPriceLabel.setText(lowStr)
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
            item.setPriceBar(priceBar)

            # Add the item.
            self.graphicsScene.addItem(item)

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

        # TODO:  write this part.
        return []


    def loadPriceBarChartArtifacts(self, priceBarChartArtifacts):
        """Loads the given list of PriceBarChartArtifact objects 
        into this widget as QGraphicsItems."""
        
        # TODO:  write this part.
        pass
        
    def addPriceBarChartArtifact(self, priceBarChartArtifact):
        """Adds the given PriceBarChartArtifact objects 
        into this widget as QGraphicsItems."""
        
        # TODO:  write this part.
        pass
        
    def clearAllPriceBarChartArtifacts(self):
        """Clears all the PriceBarChartArtifact objects from the 
        QGraphicsScene."""

        # TODO:  write this part.
        pass
        
        
    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the settings in the given PriceBarChartSettings object.
        """
        
        self.log.debug("Entering applyPriceBarChartSettings()")

        self.priceBarChartSettings = priceBarChartSettings
        

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


class PriceBarChartGraphicsScene(QGraphicsScene):
    """QGraphicsScene holding all the pricebars and artifacts.
    We subclass the QGraphicsScene to allow for future feature additions.
    """

    def __init__(self, parent=None):
        """Pass-through to the QGraphicsScene constructor."""

        super().__init__(parent)
    

class PriceBarChartGraphicsView(QGraphicsView):
    """QGraphicsView that visualizes the main QGraphicsScene.
    We subclass the QGraphicsView because we may want to add 
    custom syncrhonized functionality in other widgets later."""


    # Tool modes that this widget can be in.
    ToolMode = {"ReadOnlyPointerTool" : 0,
                "PointerTool"         : 1,
                "HandTool"            : 2,
                "ZoomInTool"          : 3,
                "ZoomOutTool"         : 4 }

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
        #self.transformationMatrix = QTransform(self.viewportTransform())
        self.transformationMatrix = None

        # Save the current viewable portion of the scene.
        self.viewableSceneRectF = self.mapToScene(self.rect()).boundingRect()

        # Holds the tool mode that this widget is currently in.
        self.toolMode = \
            PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']

        # Anchor variable we will use for click-drag, etc.
        self.dragAnchorPointF = QPointF()

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

    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool."""

        self.log.debug("Entered toReadOnlyPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

            self.toolMode = \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']

            self.setCursor(QCursor(Qt.ArrowCursor))

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

            self.setDragMode(QGraphicsView.RubberBandDrag)

        self.log.debug("Exiting toReadOnlyPointerToolMode()")

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool."""

        self.log.debug("Entered toPointerToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['PointerTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['PointerTool']

            self.setCursor(QCursor(Qt.ArrowCursor))

            scene = self.scene()
            if scene != None:
                scene.clearSelection()

            self.setDragMode(QGraphicsView.RubberBandDrag)

        self.log.debug("Exiting toPointerToolMode()")

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.log.debug("Entered toHandToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['HandTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['HandTool']

            self.setCursor(QCursor(Qt.ArrowCursor))

            self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.log.debug("Exiting toHandToolMode()")

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.log.debug("Entered toZoomInToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['ZoomInTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['ZoomInTool']

            self.setCursor(QCursor(Qt.ArrowCursor))

            if self.underMouse():
                pixmap = QPixmap(":/images/rluu/zoomIn.png")
                self.setCursor(QCursor(pixmap))

            self.setDragMode(QGraphicsView.NoDrag)

        self.log.debug("Exiting toZoomInToolMode()")

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.log.debug("Entered toZoomOutToolMode()")

        # Only do something if it is not currently in this mode.
        if self.toolMode != PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            self.toolMode = PriceBarChartGraphicsView.ToolMode['ZoomOutTool']

            self.setCursor(QCursor(Qt.ArrowCursor))

            if self.underMouse():
                pixmap = QPixmap(":/images/rluu/zoomOut.png")
                self.setCursor(QCursor(pixmap))

            self.setDragMode(QGraphicsView.NoDrag)

        self.log.debug("Exiting toZoomOutToolMode()")

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

    def mousePressEvent(self, qmouseevent):
        """Triggered when the mouse is pressed in this widget."""

        self.log.debug("Entered mousePressEvent()")

        scene = self.scene()

        if self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ReadOnlyPointerTool']:

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

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent class to handle.
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

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent class to handle.
            super().mouseReleaseEvent(qmouseevent)

        self.log.debug("Exiting mouseReleaseEvent()")

    def mouseMoveEvent(self, qmouseevent):
        """Triggered when the mouse is moving in this widget."""

        # TODO:  below remove log output
        #self.log.debug("Entered mouseMoveEvent()")

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

        else:
            # For any other mode we don't have specific functionality for,
            # just pass the event to the parent class to handle.
            super().mouseMoveEvent(qmouseevent)

        # TODO:  below remove log output
        #self.log.debug("Exiting mouseMoveEvent()")



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
        self.penWidth = \
            PriceBarChartSettings.defaultPriceBarGraphicsItemPenWidth

        # Pen width for use on highlighted (bold) PriceBars.
        self.boldPenWidth = \
            PriceBarChartSettings.defaultPriceBarGraphicsItemBoldPenWidth

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

        # Flag for bold (highlighted) PriceBar.
        self.bolded = False

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

        # penWidth (float)
        self.penWidth = priceBarChartSettings.penWidth

        # boldPenWidth (float)
        self.boldPenWidth = priceBarChartSettings.boldPenWidth

        # leftExtensionWidth (float)
        self.leftExtensionWidth = priceBarChartSettings.leftExtensionWidth

        # rightExtensionWidth (float)
        self.rightExtensionWidth = priceBarChartSettings.rightExtensionWidth



        # Now that some widths have been changed, update the pen
        # accordinately.
        if self.bolded:
            self.pen.setWidthF(self.boldPenWidth)
        else:
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
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

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
        yHigh = -1.0 * (high - priceMidpoint)
        yLow = -1.0 * (low - priceMidpoint)

        # Return value.
        rv = self.mapToScene(QPointF(x, yLow))

        self.log.debug("Leaving getPriceBarLowScenePoint().")

        return rv

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

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
        #     rightExtensionWidth units for the right extension (close price)
        #     halfPenWidth on the left side
        #     halfPenWidth on the right side

        # For Y we have:
        #     halfPenWidth for the bottom side.
        #     priceRange units
        #     halfPenWidth for the top side

        priceRange = high - low

        x = -1.0 * (self.leftExtensionWidth + halfPenWidth)
        y = -1.0 * ((priceRange / 2.0) + halfPenWidth)

        height = halfPenWidth + priceRange + halfPenWidth

        width = \
                halfPenWidth + \
                self.leftExtensionWidth + \
                self.rightExtensionWidth + \
                halfPenWidth

        return QRectF(x, y, height, width)

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.  Assumes that self.pen is set
        to what we want for the drawing style.
        """

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
        y1 = 1.0 * (priceRange / 2.0)
        x2 = 0.0
        y2 = -1.0 * (priceRange / 2.0)
        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the left extension (open price).
        x1 = 0.0
        y1 = -1.0 * (open - priceMidpoint)
        x2 = -1.0 * self.leftExtensionWidth
        y2 = y1

        painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw the right extension (close price).
        x1 = 0.0
        y1 = -1.0 * (close - priceMidpoint)
        x2 = 1.0 * self.rightExtensionWidth
        y2 = y1
        painter.drawLine(QLineF(x1, y1, x2, y2))


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



