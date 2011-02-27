
# For line separator.
import os

# For logging.
import logging
import logging.config

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# For PriceBars and artifacts in the chart.
from data_objects import BirthInfo
from data_objects import PriceBar
from data_objects import PriceBarChartBarCountArtifact
from data_objects import PriceBarChartGannFanUpperRightArtifact
from data_objects import PriceBarChartGannFanLowerRightArtifact
from data_objects import PriceBarChartScaling
from data_objects import PriceBarChartSettings
from data_objects import PriceBarChartTextArtifact

from dialogs import TimestampEditWidget

# This file contains the edit widgets and dialogs for editing the
# fields in various PriceBarChartArtifact objects within the context
# of a PriceBarChart.



class PriceBarChartBarCountArtifactEditWidget(QWidget):
    """QWidget for editing some of the member objects in a
    PriceBarChartBarCountArtifact within the context of a
    PriceBarChart.  This means that fields that are editable in the
    widgets are not actually a one-to-one mapping with the members in
    a PriceBarChartBarCountArtifact.  They are derivatives of it such
    that the user can modify it without having to do the underlying
    conversions.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self,
                 artifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """QWidget for editing some of the fields of a
        PriceBarChartBarCountArtifact object.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object to edit.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartBarCountArtifactEditWidget")

        # Save off the artifact object.
        self.artifact = artifact

        # Save off the scene object used for unit conversions.
        self.convertObj = convertObj
        
        # Save off the readOnlyFlag
        self.readOnlyFlag = readOnlyFlag
        
        # QGroupBox to hold the edit widgets and form.
        self.groupBox = QGroupBox("PriceBarChartBarCountArtifact Data:")


        lineEditWidth = 420
        
        self.internalNameLabel = QLabel("Internal name:")
        self.internalNameLineEdit = QLineEdit()
        self.internalNameLineEdit.setMinimumWidth(lineEditWidth)

        self.uuidLabel = QLabel("Uuid:")
        self.uuidLineEdit = QLineEdit()
        self.uuidLineEdit.setMinimumWidth(lineEditWidth)

        self.priceLocationValueLabel = QLabel("Artifact location (in price):")
        self.priceLocationValueSpinBox = QDoubleSpinBox()
        self.priceLocationValueSpinBox.setMinimum(0.0)
        self.priceLocationValueSpinBox.setMaximum(999999999.0)

        self.startPointDatetimeLocationWidget = TimestampEditWidget()
        self.startPointDatetimeLocationWidget.groupBox.\
            setTitle("BarCount Start Point (in time)")
        self.startPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.startPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        self.endPointDatetimeLocationWidget = TimestampEditWidget()
        self.endPointDatetimeLocationWidget.groupBox.\
            setTitle("BarCount End Point (in time)")
        self.endPointDatetimeLocationWidget.okayButton.setVisible(False)
        self.endPointDatetimeLocationWidget.cancelButton.setVisible(False)
        
        # Layout.
        self.gridLayout = QGridLayout()

        # Row.
        r = 0

        # Alignments.
        al = Qt.AlignLeft
        ar = Qt.AlignRight

        self.gridLayout.addWidget(self.internalNameLabel, r, 0, al)
        self.gridLayout.addWidget(self.internalNameLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.uuidLabel, r, 0, al)
        self.gridLayout.addWidget(self.uuidLineEdit, r, 1, al)
        r += 1
        self.gridLayout.addWidget(self.priceLocationValueLabel, r, 0, al)
        self.gridLayout.addWidget(self.priceLocationValueSpinBox, r, 1, al)
        r += 1

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.startPointDatetimeLocationWidget)
        self.layout.addWidget(self.endPointDatetimeLocationWidget)
        
        self.groupBox.setLayout(self.layout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.groupBox) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)
        
        self.setReadOnly(self.readOnlyFlag)
        
        # Now that all the widgets are created, load the values from the
        # artifact object.
        self.loadValues(self.artifact)

        # Connect signals and slots.

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        # Need to reload the artifact, so that the proper conversion
        # is done with the new conversion object.
        self.loadValues(self.artifact)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
        
    def getArtifact(self):
        """Returns the internally stored artifact object.

        Note: If saveValues() was called previously, then this object
        was updated with the values from the edit widgets.
        """

        return self.artifact
        
    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
        ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        # Set the internal widgets as readonly or not depending on this flag.
        self.internalNameLineEdit.setReadOnly(True)
        self.uuidLineEdit.setReadOnly(True)
        self.priceLocationValueSpinBox.setReadOnly(self.readOnlyFlag)
        self.startPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        self.endPointDatetimeLocationWidget.setReadOnly(self.readOnlyFlag)
        
        # Don't allow the Okay button to be pressed for saving.
        self.okayButton.setEnabled(not self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields in the PriceBar.
        """
        
        return self.readOnlyFlag

    def loadValues(self, artifact):
        """Loads the widgets with values from the given
        PriceBarChartBarCountArtifact.

        Note: Upon calling saveValues(), the edit widget overwrites
        the values in the object pointed to by 'artifact' with the
        values in the edit widgets.

        Arguments:
        
        artifact - PriceBarChartBarCountArtifact object to load the
        values into the edit widgets.  
        """

        self.log.debug("Entered loadValues()")

        # Check inputs.
        if artifact == None:
            self.log.error("Invalid parameter to " + \
                           "loadValues().  artifact can't be None.")
            self.log.debug("Exiting loadValues()")
            return
        else:
            self.artifact = artifact

        # Set the widgets.
        self.internalNameLineEdit.\
            setText(self.artifact.getInternalName())
        self.uuidLineEdit.\
            setText(str(self.artifact.getUuid()))

        locationPointY = self.artifact.startPointF.y()
        locationPointPrice = self.convertObj.sceneYPosToPrice(locationPointY)
        self.priceLocationValueSpinBox.setValue(locationPointPrice)
        
        startPointX = self.artifact.startPointF.x()
        startPointDatetime = self.convertObj.sceneXPosToDatetime(startPointX)
        self.startPointDatetimeLocationWidget.\
            loadTimestamp(startPointDatetime)
        
        endPointX = self.artifact.endPointF.x()
        endPointDatetime = self.convertObj.sceneXPosToDatetime(endPointX)
        self.endPointDatetimeLocationWidget.\
            loadTimestamp(endPointDatetime)
        
        self.log.debug("Exiting loadValues()")
        
    def saveValues(self):
        """Saves the values in the widgets to the
        PriceBarChartBarCountArtifact object passed in this class's
        constructor or the loadValues() function.
        """
    
        self.log.debug("Entered saveValues()")

        # Call save on the timestamp widgets.
        self.startPointDatetimeLocationWidget.saveTimestamp()
        self.endPointDatetimeLocationWidget.saveTimestamp()
        
        # Position and start point should be the same values.

        price = self.priceLocationValueSpinBox.value()
        y = self.convertObj.priceToSceneYPos(price)

        startPointDatetime = \
            self.startPointDatetimeLocationWidget.getTimestamp()
        endPointDatetime = \
            self.endPointDatetimeLocationWidget.getTimestamp()
                          
        startPointX = self.convertObj.datetimeToSceneXPos(startPointDatetime)
        endPointX = self.convertObj.datetimeToSceneXPos(endPointDatetime)

        posF = QPointF(startPointX, y)
        startPointF = QPointF(startPointX, y)
        endPointF = QPointF(endPointX, y)

        # Set the values in the artifact.
        self.artifact.setPos(posF)
        self.artifact.setStartPointF(startPointF)
        self.artifact.setEndPointF(endPointF)

        self.log.debug("Exiting saveValues()")


    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveValues()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarChartBarCountArtifactEditDialog(QDialog):
    """QDialog for editing some of the members objects in a 
    PriceBarChartBarCountArtifact.
    """

    def __init__(self,
                 priceBarChartBarCountArtifact,
                 convertObj,
                 readOnlyFlag=False,
                 parent=None):
        """Initializes the dialog and internal widget with the values
        from the given PriceBarChartBarCountArtifact.
        
        Note: The 'priceBarChartBarCountArtifact' object gets modified
        if the user clicks the 'Okay' button.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object to edit.
                   This object gets modified if the user clicks the
                   'Okay' button.
        convertObj - PriceBarChartGraphicsScene object that is used for
                unit conversions (x position to time, y position to price).
        readOnlyFlag - bool value used to set the widgets in readonly mode.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.PriceBarChartBarCountArtifactEditDialog")

        self.setWindowTitle("Edit PriceBarChartBarCountArtifact Data")

        # Check input.
        if not isinstance(priceBarChartBarCountArtifact,
                          PriceBarChartBarCountArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      " constructor.")
            return

        # Save a reference to the artifact object.
        self.artifact = priceBarChartBarCountArtifact

        # Save a reference to the conversion object.
        self.convertObj = convertObj
        
        # Save the readOnlyFlag value.
        self.readOnlyFlag = readOnlyFlag
        
        # Create the contents.
        self.editWidget = \
            PriceBarChartBarCountArtifactEditWidget(self.artifact,
                                                    self.convertObj,
                                                    self.readOnlyFlag)
        
        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def setReadOnly(self, readOnlyFlag):
        """Sets the internal edit widgets to be read only or not
        depending on the bool state of readOnlyFlag.

        Arguments:
        readOnlyFlag - bool value indicating whether the widget is in
                       ReadOnly mode.
        """

        self.readOnlyFlag = readOnlyFlag

        self.editWidget.setReadOnly(self.readOnlyFlag)
        
    def getReadOnly(self):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields.
        """
        
        return self.readOnlyFlag

    def setConvertObj(self, convertObj):
        """Sets the object that is used for the conversion between
        scene position and timestamp or price.

        Arguments:
        convertObj - PriceBarChartGraphicsScene object that is used
                     for scene position conversions of X point to
                     timestamp and Y point to price.
        """

        self.convertObj = convertObj

        self.editWidget.setConvertObj(self.convertObj)
        
    def getConvertObj(self):
        """Returns the object used for conversion calculations between
        scene position point and timestamp or price.

        Returns:
        PriceBarChartGraphicsScene object that is used
        for scene position conversions of X point to
        timestamp and Y point to price.
        """

        return self.convertObj
    
    def setArtifact(self, artifact):
        """Loads the edit widget with the given artifact object.
        
        Note:  Upon clicking 'Okay' this object will be modified.

        Arguments:
        artifact - PriceBarChartBarCountArtifact object to load the
                   widgets with.
        """

        # Check input.
        if not isinstance(artifact,
                          PriceBarChartBarCountArtifact):
            log.error("Input type invalid to " + self.__class__.__name__ +
                      ".setArtifact()")
            return

        self.artifact = artifact

        self.editWidget.loadValues(self.artifact)

    def getArtifact(self):
        """Returns a reference to the internally stored artifact object.
        
        Note: If the 'Okay' button was previously clicked, then this
        object is modified with the widget's values, otherwise it is
        unchanged.
        """

        return self.artifact


def testPriceBarChartBarCountArtifactEditDialog():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Create an artifact.
    artifact = PriceBarChartBarCountArtifact()

    # Set the artifact's position and start/end points.  It needs to
    # be at a position where the converted datetime.datetime is
    # greater than the datetime.datetime.MINYEAR.
    # A X value of 2100000 is in year 927.
    pos = QPointF(2100000, -1000)
    artifact.setPos(pos)
    artifact.setStartPointF(pos)
    artifact.setEndPointF(QPoint(pos.x() + 1000, pos.y()))

    # Create an object for doing unit conversions.
    eastern = pytz.timezone('US/Eastern')
    from pricebarchart import PriceBarChartGraphicsScene
    convertObj = PriceBarChartGraphicsScene()
    convertObj.setTimezone(eastern)
    
    # Run the dialog in readonly mode.
    print("Before (readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=True)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))

    
    # Run the dialog in non-readonly mode.
    print("Before (not readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))
    dialog = PriceBarChartBarCountArtifactEditDialog(artifact,
                                                     convertObj,
                                                     readOnlyFlag=False)
    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted")
    else:
        print("Rejected")
    print("After  (not readonly), PriceBarChartBarCountArtifact: {}".\
          format(artifact.toString()))
    

# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
    import os
    import sys
    
    from ephemeris import Ephemeris
    
    # Initialize the Ephemeris (required).
    Ephemeris.initialize()

    # Set a default location (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)
    
    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)

    # Various tests to run:
    testPriceBarChartBarCountArtifactEditDialog()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()
    #app.exec_()
    

