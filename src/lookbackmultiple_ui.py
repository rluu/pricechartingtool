

# For logging.
import logging

# For newlines.
import os

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import image resources.
import resources

from widgets import ColorIcon

from data_objects import LookbackMultiple

from dialogs import LookbackMultipleEditDialog



class LookbackMultiplePanelWidget(QWidget):
    """Widget holding the QTableView that displays the PriceBar 
    information along with other metrics analysis information.
    """

    # Signal emitted when the LookbackMultiples are modified by the user,
    # either by checking a LookbackMultiple to be enabled, or by
    # double-clicking and editing the particular LookbackMultiple in the list.
    # Loading a new list of LookbackMultiples does not trigger this signal.
    lookbackMultiplesModified = QtCore.pyqtSignal(list)

    # Signal emitted when the "Apply/Redraw Lookback Multiples" button is
    # clicked within this widget.
    applyRedrawLookbackMultiplesButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("lookbackmultiple_ui.LookbackMultiplePanelWidget")

        # Member variables.

        # Holds the reference to the list of lookback multiples.
        self.lookbackMultiples = []

        self.applyRedrawButton = QPushButton("Apply/Redraw Lookback Multiples")

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        
        self.tableWidgetHeaderItem = QTableWidgetItem("Lookback Multiples")
        column = 0
        self.tableWidget.setHorizontalHeaderItem(column, 
                                                 self.tableWidgetHeaderItem)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.applyRedrawButton)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        # Connect signals and slots.
        self.applyRedrawButton.clicked.\
            connect(self.applyRedrawLookbackMultiplesButtonClicked)
        self.tableWidget.itemChanged.\
          connect(self._handleItemChanged)
        self.tableWidget.itemDoubleClicked.\
          connect(self._handleItemDoubleClicked)
        
        self.log.debug("size is: w={},h={}".\
                       format(self.size().width(), 
                              self.size().height()))
        self.log.debug("sizeHint is: w={},h={}".\
                       format(self.sizeHint().width(), 
                              self.sizeHint().height()))

    def getLookbackMultiples(self):
        """Returns the reference to the list of LookbackMultiple objects."""
        
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug("Entered getLookbackMultiples()")

            self.log.debug("len(self.lookbackMultiples) is currently: {}".\
                           format(len(self.lookbackMultiples)))

            self.log.debug("self.lookbackMultiples is currently: ".\
                           format(self.lookbackMultiples))

            for i in range(len(self.lookbackMultiples)):
                lm = self.lookbackMultiples[i]
                self.log.debug("self.lookbackMultiples[{}] is: {}".\
                               format(i, lm.toString()))

            self.log.debug("Exiting getLookbackMultiples()")

        return self.lookbackMultiples


    def setLookbackMultiples(self, lookbackMultiples):
        """Sets the given list of LookbackMultiple objects to be
        visualized in this widget.  This widget can potentially modify
        the LookbackMultiple objects within this list.
        """

        self.log.debug("Entered setLookbackMultiples(lookbackMultiples)")

        if lookbackMultiples == None:
            self.log.error("Error: Invalid arguments.  " + \
                           "lookbackMultiples to load cannot be None.")
            self.log.debug("Exiting loadLookackMultiples(lookbackMultiples)")
            return


        # Here we will disconnect the signal-to-slot for handling when an item
        # is changed.  We will reconnect it at the end of this method after we
        # have made our modifications and created/modified the
        # QTableWidgetItems within the QTableWidget.
        # 
        # Reason: This is because we don't want the signal to propagate
        # upwards to indicate a real change has occured via user interaction
        # from just loading.  
        self.tableWidget.itemChanged.disconnect(self._handleItemChanged)

        self.log.debug("Old lookbackMultiples has length: {}".\
                       format(len(self.lookbackMultiples)))
        self.log.debug("New lookbackMultiples has length: {}".\
                       format(len(lookbackMultiples)))
        self.log.debug("Before setting new lookbackMultiples, " + 
                       "the number of rows is: {}".\
                       format(self.tableWidget.rowCount()))
     
        # Store a reference to the new LookbackMultiples.
        self.lookbackMultiples = lookbackMultiples

        # Update the row count.
        if self.tableWidget.rowCount() != len(self.lookbackMultiples):
            self.tableWidget.setRowCount(len(self.lookbackMultiples))
        
        for i in range(len(self.lookbackMultiples)):
            lookbackMultiple = lookbackMultiples[i]
            row = i
            column = 0
            
            # Get the existing item at the current row and column.  
            # If it doesn't exist, then create it.
            item = self.tableWidget.item(row, column)
            if item == None:
                self.log.debug("Item at (row={}, col={})".\
                               format(row, column) + \
                               " was None, so creating it now.")
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, column, item)

            # Set the internals of the QTableWidgetItem to reflect the
            # LookbackMultiple that it represents.
            if lookbackMultiple.getEnabled():
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
                
            item.setIcon(ColorIcon(lookbackMultiple.getColor()))
            item.setText(lookbackMultiple.toShortString())
            item.setToolTip(\
                self._getToolTipTextTextForLookbackMultiple(lookbackMultiple))
            
        # Reconnect the signal-to-slot, so that user changes to the items will
        # notify us so we can update the internal LookbackMultiple variable(s), 
        # and take any other necessary actions.
        self.tableWidget.itemChanged.connect(self._handleItemChanged)

        self.log.debug("Exiting setLookbackMultiples(lookbackMultiples)")

    
    def _handleItemChanged(self, item):
        """Slot that handles when a QTableWidgetItem changes.
        An example of a change that this handles is the item's check state.
        
        Arguments:
        item - QTableWidgetItem that is sent via Qt's signal to this slot.
        """
        
        self.log.debug("Entered _handleItemChanged(item)")

        self.log.debug("Item changed at (row={}, col={})".\
                       format(item.row(), item.column()))

        # Currently, the only kinds of changes supported are checking the
        # item's state, which will cause the enable state of the underlying
        # LookbackMultiple to be updated.  The other way is to double-click the
        # item to edit it manually, which another method handles this case.
        row = item.row()
        enabledFlag = item.checkState() == Qt.Checked
        if self.lookbackMultiples[row].getEnabled() != enabledFlag:
            self.log.debug("Checkstate was changed to {}.".format(enabledFlag))
            self.lookbackMultiples[row].setEnabled(enabledFlag)

            # Emit that there were modifications to the LoobkackMultiples.
            self.lookbackMultiplesModified.emit(self.lookbackMultiples)
        
        self.log.debug("Exiting _handleItemChanged(item)")
        
    def _handleItemDoubleClicked(self, item):
        """Slot that handles when a QTableWidgetItem is double-clicked.
        This will open up an edit dialog to edit the underlying
        LookbackMultiple.

        Arguments:
        item - QTableWidgetItem that is sent via Qt's signal to this slot.
        """
        
        self.log.debug("Entered _handleItemDoubleClicked(item)")
        
        self.log.debug("Item double-clicked at (row={}, col={})".\
                       format(item.row(), item.column()))
                       
        # Get the LookbackMultiple that underlies this QTableWidgetItem that
        # was double-clicked.
        row = item.row()
        lookbackMultiple = self.lookbackMultiples[row]
        
        # Create a dialog to edit this LookbackMultiple.
        dialog = LookbackMultipleEditDialog(lookbackMultiple)
        
        rv = dialog.exec_()
        if rv == QDialog.Accepted:
            # Dialog was accepted.  Obtain and store the new LookbackMultiple.
            self.log.debug("Edit dialog for the LookbackMultiple was accepted.")
            self.log.debug("Storing new LookbackMultiple back into the list.")

            self.lookbackMultiples[row] = dialog.getLookbackMultiple()
            lookbackMultiple = self.lookbackMultiples[row]

            # Reload the current QTableWidgetItem so that it displays updated
            # information.
            # 
            # (Here we will disconnect the itemChanged signal and then after
            # updates, reconnect it).
            self.tableWidget.itemChanged.disconnect(self._handleItemChanged)

            if lookbackMultiple.getEnabled():
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            item.setIcon(ColorIcon(lookbackMultiple.getColor()))
            item.setText(lookbackMultiple.toShortString())
            item.setToolTip(\
                self._getToolTipTextTextForLookbackMultiple(lookbackMultiple))

            self.tableWidget.itemChanged.connect(self._handleItemChanged)


            # Emit that there were modifications to the LookbackMultiples.
            self.lookbackMultiplesModified.emit(self.lookbackMultiples)
        else:
            self.log.debug("Edit dialog for the LookbackMultiple was rejected.")
        
        self.log.debug("Exiting _handleItemDoubleClicked(item)")
        
    def _getToolTipTextTextForLookbackMultiple(self, lookbackMultiple):
        """Returns a formatted string to use for the tooltip."""
        
        lm = lookbackMultiple
        
        # Newlines.
        endl = os.linesep

        # Assemble substrings used within the final string.
        centricityTypeStr = ""
        if lm.getGeocentricFlag() == True:
            centricityTypeStr = "G."
        if lm.getHeliocentricFlag() == True:
            centricityTypeStr = "H."
            
        planetNameStr = lm.getPlanetName()
        lookbackMultipleStr = "{}".format(lm.getLookbackMultiple())
        
        longitudeTypeStr = ""
        if lm.getTropicalFlag() == True:
            longitudeTypeStr = "Trop."
        if lm.getSiderealFlag() == True:
            longitudeTypeStr = "Sid."
            
        baseUnitStr = "{}".format(lm.getBaseUnit())

        baseUnitTypeStr = ""
        if lm.getBaseUnitTypeDegreesFlag() == True:
            baseUnitTypeStr = "degrees"
        if lm.getBaseUnitTypeRevolutionsFlag() == True:
            baseUnitTypeStr = "revolutions"

        # Build the final string used for the tooltip.
        formattedText = ""
        formattedText += "Name: {}".format(lm.getName()) + endl
        formattedText += "Enabled: {}".format(lm.getEnabled()) + endl
        formattedText += \
            "Summary: {}{} {} {} x {} {}".\
            format(centricityTypeStr, 
                   planetNameStr, 
                   longitudeTypeStr,
                   lookbackMultipleStr, 
                   baseUnitStr, 
                   baseUnitTypeStr) + endl
        formattedText += "Description: {}".format(lm.getDescription())

        return formattedText



##############################################################################

def testLookbackMultiplePanelWidget():
    print("Running " + inspect.stack()[0][3] + "()")
    
    lm1 = LookbackMultiple(name="49ers",
                          description="MyDescription1",
                          lookbackMultiple=1.0,
                          baseUnit=49.0,
                          baseUnitTypeDegreesFlag=False,
                          baseUnitTypeRevolutionsFlag=True,
                          color=QColor(Qt.gray),
                          enabled=False,
                          planetName="Ascendant",
                          geocentricFlag=True,
                          heliocentricFlag=False,
                          tropicalFlag=True,
                          siderealFlag=False)

    lm2 = LookbackMultiple(name="40 deg Earth",
                          description="MyDescription2",
                          lookbackMultiple=1.0,
                          baseUnit=40.0,
                          baseUnitTypeDegreesFlag=True,
                          baseUnitTypeRevolutionsFlag=False,
                          color=QColor(Qt.red),
                          enabled=True,
                          planetName="Earth",
                          geocentricFlag=False,
                          heliocentricFlag=True,
                          tropicalFlag=True,
                          siderealFlag=False)

    lm3 = LookbackMultiple(name="360 deg Moon",
                          description="MyDescription3",
                          lookbackMultiple=1.0,
                          baseUnit=360.0,
                          baseUnitTypeDegreesFlag=True,
                          baseUnitTypeRevolutionsFlag=False,
                          color=QColor(Qt.blue),
                          enabled=True,
                          planetName="Moon",
                          geocentricFlag=True,
                          heliocentricFlag=False,
                          tropicalFlag=True,
                          siderealFlag=False)

    lm4 = LookbackMultiple(name="360 deg G.MoSu",
                          description="MyDescription4",
                          lookbackMultiple=1.0,
                          baseUnit=360.0,
                          baseUnitTypeDegreesFlag=True,
                          baseUnitTypeRevolutionsFlag=False,
                          color=QColor(Qt.black),
                          enabled=True,
                          planetName="MoSu",
                          geocentricFlag=True,
                          heliocentricFlag=False,
                          tropicalFlag=True,
                          siderealFlag=False)

    lookbackMultiples = [lm1, lm2, lm3, lm4]

    widget = LookbackMultiplePanelWidget()
    widget.setLookbackMultiples(lookbackMultiples)

    layout = QVBoxLayout()
    layout.addWidget(widget)
    
    dialog = QDialog()
    dialog.setLayout(layout)
    rv = dialog.exec_()


def testLookbackMultiplePanelWidgetEmpty():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Just display the panel widget without any LookbackMultiples.
    # This is to get an idea about the minimum/default sizes of the widget.
    
    lookbackMultiples = []

    widget = LookbackMultiplePanelWidget()
    #widget.setLookbackMultiples(lookbackMultiples)

    layout = QVBoxLayout()
    layout.addWidget(widget)
    
    dialog = QDialog()
    dialog.setLayout(layout)
    rv = dialog.exec_()

    

##############################################################################

# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect

    # For logging and for exiting.
    import os
    import sys
    
    # Initialize the Ephemeris (required).
    #Ephemeris.initialize()

    # New York City:
    #lon = -74.0064
    #lat = 40.7142
    
    # Set a default location (required).
    #Ephemeris.setGeographicPosition(lon, lat)

    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)


    # Various tests to run:
    testLookbackMultiplePanelWidget()
    testLookbackMultiplePanelWidgetEmpty()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    #app.exec_()

    # Quit.
    print("Exiting.")
    sys.exit()

##############################################################################
