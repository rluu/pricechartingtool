

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


    # Signal emitted when the PriceBarChartWidget changes.
    # 
    # Possible changes to the widget that will trigger this include: 
    #   - Any scene change (pricebars, artifacts)
    #   - Any view change (viewable area changed)
    #   
    # It does NOT include:
    #   - User selecting a pricebar
    #   - User opening a wheel astrology chart from a pricebar
    #
    priceBarChartChanged = QtCore.pyqtSignal()


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

        # Connect signals and slots.
        self.graphicsView.transformMatrixChanged.\
            connect(self._handlePriceBarChartGraphicsViewMatrixChanged)

        self.log.debug("Leaving __init__()")

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

            # X location will be the proleptic Gregorian ordinal
            # of the date of the PriceBar.
            ordinateDate = priceBar.timestamp.toordinal()
            x = ordinateDate

            # Y location will be the mid price of the bar.
            y = priceBar.midPrice()

            # Set the position, in parent coordinates.
            item.setPos(QPointF(x, y))

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
        
        self.priceBarChartSettings = priceBarChartSettings
        
        # TODO:  Write this part.


        # TODO:  What I need to figure out is if it is only necessary to do:
        # TODO:     - Call resize function of the PriceBarChartGraphicsView
        # TODO:  or if I need to do all of the following:
        # TODO:     - Call resize function of the QGraphicsView with the
        # TODO:       size value.
        # TODO:     - Send a signal up to the parent PriceChartDocument and
        # TODO:       have them call resize with the size value.
        # TODO:  And for the second group, what is the correct order of
        # TODO:  invocation that?
    

        # TODO:  Then I need to apply the scaling, viewable area, etc. )
        # by using the stored matrix object.  This is done by calling the
        # setTransform() function to set the viewable area of the scene. 
        # (Do I need to call a mapFromScene() for this first?)

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

    def _handlePriceBarChartGraphicsViewMatrixChanged(self, qmatrix):
        """Qt slot for handling when the internal
        PriceBarChartGraphicsView has it's transformation matrix changed.

        It updates the internal self.priceBarChartSettings object and then
        emits priceBarChartChanged so that any objects connected to that
        signal can be notified (e.g. the parent that will mark the
        pricechartdocument as being 'dirty').
        """

        # TODO:  write this function.

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

    defaultZoomScaleFactor = 1.2

    # Signal emitted when the mouse moves within the QGraphicsView.
    # The position emitted is in QGraphicsScene x, y, float coordinates.
    mouseLocationUpdate = QtCore.pyqtSignal(float, float)

    # Signal emitted when transformation matrix in the QGraphicsView changes.
    # This holds scaling and zoom amount.
    transformMatrixChanged = QtCore.pyqtSignal(QTransform)

    # Signal emitted when the viewable area of a sceneRect in a
    # PriceBarChartGraphicsView changes.  The QRect emitted is in scene
    # coordinates.
    viewableAreaChanged = QtCore.pyqtSignal(QRectF)
    
    def __init__(self, parent=None):
        """Pass-through to the QGraphicsView constructor."""

        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceBarChartGraphicsView")
        self.log.debug("Entered __init__()")

        # Save the current transformation matrix of the view.
        self.transformationMatrix = QTransform(self.viewportTransform())

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

    def zoomToFullScene(self):
        """Zooms the QGraphicsView so that the whole QGraphicsScene is
        viewable.  This keeps the aspect ratio.
        """

        scene = self.scene()
        if scene != None:
            self.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

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
                            PriceBarChartGraphicsView.defaultZoomScaleFactor))

                # Actually do the scaling of the view.
                self.scale(scaleFactor, scaleFactor)

                # Center on the new center.
                self.centerOn(newCenterPointF)

            elif qmouseevent.button() & Qt.RightButton:
                self.zoomToFullScene()

        elif self.toolMode == \
                PriceBarChartGraphicsView.ToolMode['ZoomOutTool']:
            
            if qmouseevent.button() & Qt.LeftButton:
                # New center
                newCenterPointF = self.mapToScene(qmouseevent.pos())

                # Get the QSetting key for the zoom scaling amounts.
                settings = QSettings()
                scaleFactor = \
                    float(settings.value(self.zoomScaleFactorSettingsKey, \
                            PriceBarChartGraphicsView.defaultZoomScaleFactor))

                # Actually do the scaling of the view.
                self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

                # Center on the new center.
                self.centerOn(newCenterPointF)

            elif qmouseevent.button() & Qt.RightButton:
                self.zoomToFullScene()
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

        self.log.debug("Entered mouseMoveEvent()")

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

        self.log.debug("Exiting mouseMoveEvent()")



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

    
    def viewportEvent(self, qevent):
        """Overwrites the QGraphicsView.viewportEvent() function.

        This is overwritten so that we can obtain any changes in the
        viewable area of the QGraphicsView.
        """

        self.log.debug("Entering viewportEvent()")

        # Call the parent viewportEvent() function so things actually get
        # scrolled.
        rv = super().viewportEvent(qevent)

        # If the viewable area of the scene changed, emit that.
        viewableSceneRectF = self.mapToScene(self.rect()).boundingRect()
        if self.viewableSceneRectF != viewableSceneRectF:
            self.viewableSceneRectF = viewableSceneRectF
            self.viewableAreaChanged.emit(self.viewableSceneRectF)

        self.log.debug("Exiting viewportEvent()")
        return rv


    def paintEvent(self, qpaintevent):
        """Overwrites the QGraphicsView.paintEvent() function.

        We overwrite this because we want to know when the viewable area
        of the scene that is shown in this QGraphicsView changes.
        There appears to be no signal that is emitted when that happens,
        so we will just implement that signal ourselves by overwriting
        this function and emitting signals every time the viewable area
        changes.  
        """

        self.log.debug("Entering paintEvent()")

        # Call the parent paintEvent() so things actually get drawn.
        super().paintEvent(qpaintevent)

        # If the viewable area of the scene changed, emit that.
        viewableSceneRectF = self.mapToScene(self.rect()).boundingRect()
        if self.viewableSceneRectF != viewableSceneRectF:
            self.viewableSceneRectF = viewableSceneRectF
            self.viewableAreaChanged.emit(self.viewableSceneRectF)

        # If the transformation matrix changed, then emit that.
        transform = self.viewportTransform()
        if self.transformationMatrix != transform:
            # Use the __init__ function again so we're not continually
            # creating and destroying objects.
            self.transformationMatrix.__init__(transform)

            self.transformMatrixChanged.emit(self.transformationMatrix)

        self.log.debug("Exiting paintEvent()")

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
    
    # Default color for higher price bars.
    defaultHigherPriceBarColor = QColor(Qt.green)

    # Default color for lower price bars.
    defaultLowerPriceBarColor = QColor(Qt.red)

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
        self.higherPriceBarColor = self.defaultHigherPriceBarColor

        # Color setting for a PriceBar that has a lower close than open.
        self.lowerPriceBarColor = self.defaultLowerPriceBarColor

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
        defaultValue = PriceBarGraphicsItem.defaultHigherPriceBarColor
        self.higherPriceBarColor = \
            QColor(settings.value(key, defaultValue))

        # lowerPriceBarColor
        key = SettingsKeys.lowerPriceBarColorSettingsKey
        defaultValue = PriceBarGraphicsItem.defaultLowerPriceBarColor
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



