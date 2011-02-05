
# For directory access.
import os
import sys

# For datetimes
import datetime

# For timezone conversion info.
import pytz

# For logging.
import logging
import logging.config

# For PyQt widgets.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from ephemeris import *


class ColorIcon(QIcon):
    """A QIcon hosting just a color."""
    
    def __init__(self, color=None):
        """Initializes a QIcon with a certain color.
        
        Arguments:
            color - QColor object representing the color to set the text.
        """


        # Internally stored QColor object.
        self.color = color

        if color == None:
            self.color = QColor()

        self.pixmap = QPixmap(QSize(32, 32))
        self.pixmap.fill(self.color)

        super().__init__(self.pixmap)

    def getColor(self):
        """Returns the current QColor setting of this widget.  This value
        may be None if no color was set previously.
        """

        return self.color

        
class ColorEditPushButton(QPushButton):
    """A QPushButton but with a color and text."""

    def __init__(self, color=None, text="Edit"):

        super().__init__(ColorIcon(color), text)

        self.color = color

        self.clicked.connect(self._handleButtonClicked)

    def setColor(self, color):
        """Sets the color of held by this widget.

        Arguments:
            color - QColor object representing the new color to use for
                    this widget.  Cannot be None.
        """

        if color != None and self.color != color:
            self.color = color
            self.setIcon(ColorIcon(self.color))

    def getColor(self):
        """Returns the current QColor setting of this widget.  This value
        may be None if no color was set previously.
        """

        return self.color

    def _handleButtonClicked(self):
        """Brings up a color QColorDialog to edit the current color.
        If the new color is valid and it is a different color, then we
        set the button as having the new color.
        """

        # First get the current color.
        currColor = self.getColor()

        # Open a dialog to obtain a new color.
        newColor = QColorDialog.getColor(currColor)

        # If a color was chosen that is different, then set the new color.
        if newColor.isValid() and currColor != newColor:
            self.setColor(newColor)


class PlanetaryInfoTableWidget(QTableWidget):
    """A QTableWidget holding information about a list of planets."""

    def __init__(self, planetaryInfos=[], parent=None):
        """Creates and initializes the widget with the given list of
        PlanetaryInfo objects.
        
        Arguments:
            
        planetaryInfos - list of PlanetaryInfo objects that hold
                         information about the various planets that will
                         be displayed in the QTableWidget.
                         
        """

        super().__init__(parent)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.planetaryInfos = planetaryInfos

        self.log = logging.getLogger("widgets.PlanetaryInfoTableWidget")

        # Strings for the different types of planetary coordinate systems.
        geoStr = "Geocentric" + os.linesep
        topoStr = "Topocentric" + os.linesep
        helioStr = "Heliocentric" + os.linesep

        sidStr = "Sidereal" + os.linesep
        tropStr = "Tropical" + os.linesep

        # Different measurements available.
        longitudeStr = "Longitude"
        latitudeStr = "Latitude"
        distanceStr = "Distance"

        longitudeSpeedStr = "Longitude Speed"
        latitudeSpeedStr = "Latitude Speed"
        distanceSpeedStr = "Distance Speed"

        rectascensionStr = "Rectascension"
        declinationStr = "Declination"

        rectascensionSpeedStr = "Rectascension Speed"
        declinationSpeedStr = "Declination Speed"

        xStr = "X Location"
        yStr = "Y Location"
        zStr = "Z Location"

        dxStr = "X Speed"
        dyStr = "Y Speed"
        dzStr = "Z Speed"

        # Units of measurement for the above measurements.
        degreesUnitsStr = " (degrees)"
        auUnitsStr = " (AU)"
        degreesPerDayUnitsStr = " (degrees/day)"
        auPerDayUnitsStr = " (AU/day)"

        # Strings for the 'Planet' header field.
        planetStr = "Planet"
        planetToolTipStr = "Planet"

        # List of strings containing the different planetary coordinate
        # systems.
        coordinateSystems = []
        coordinateSystems.append(geoStr + sidStr)
        coordinateSystems.append(geoStr + tropStr)
        coordinateSystems.append(topoStr + sidStr)
        coordinateSystems.append(topoStr + tropStr)
        coordinateSystems.append(helioStr + sidStr)
        coordinateSystems.append(helioStr + tropStr)

        # Number of different measurements.
        numMeasurements = 16 * len(coordinateSystems)
        numColumns = 1 + numMeasurements
        self.setColumnCount(numColumns)

        # Create all the header QTableWidgetItems.
        col = 0

        tableWidgetItem = QTableWidgetItem(planetStr)
        tableWidgetItem.setToolTip(planetToolTipStr)
        self.setHorizontalHeaderItem(col, tableWidgetItem)
        col += 1

        for cs in coordinateSystems:
            item = QTableWidgetItem(cs + longitudeStr)
            item.setToolTip(longitudeStr + degreesUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + latitudeStr)
            item.setToolTip(latitudeStr + degreesUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + distanceStr)
            item.setToolTip(distanceStr + auUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + longitudeSpeedStr)
            item.setToolTip(longitudeSpeedStr + degreesPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + latitudeSpeedStr)
            item.setToolTip(latitudeSpeedStr + degreesPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + distanceSpeedStr)
            item.setToolTip(distanceSpeedStr + auPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + rectascensionStr)
            item.setToolTip(rectascensionStr + degreesUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + declinationStr)
            item.setToolTip(declinationStr + degreesUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + rectascensionSpeedStr)
            item.setToolTip(rectascensionSpeedStr + degreesPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + declinationSpeedStr)
            item.setToolTip(declinationSpeedStr + degreesPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + xStr)
            item.setToolTip(xStr + auUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + yStr)
            item.setToolTip(yStr + auUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + zStr)
            item.setToolTip(zStr + auUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + dxStr)
            item.setToolTip(dxStr + auPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + dyStr)
            item.setToolTip(dyStr + auPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

            item = QTableWidgetItem(cs + dzStr)
            item.setToolTip(dzStr + auPerDayUnitsStr)
            self.setHorizontalHeaderItem(col, item)
            col += 1

        # Now that all the headers are created, load the PlanetaryInfos.
        self.load(self.planetaryInfos)

        # Connect signals and slots.
        self.cellDoubleClicked.\
            connect(self._handleCellDoubleClicked)

    def load(self, planetaryInfos):
        """Loads the widgets with the given list of PlanetaryInfo
        objects.
        """
        
        self.log.debug("Entered load()")

        self.setRowCount(len(planetaryInfos))
        self.clearContents()

        for i in range(len(planetaryInfos)):

            p = planetaryInfos[i]

            if i >= len(self.planetaryInfos):
                self._appendPlanetaryInfo(p)
            else:
                self._replaceRowWithPlanetaryInfo(i, p)

        self.planetaryInfos = planetaryInfos

        self.log.debug("Exiting load()")

    def _handleCellDoubleClicked(self, row, column):
        """Triggered when an item is double-clicked.  
        
        This will highlight the entire row of the cell that the user
        double-clicked.
        """

        self.log.debug("QTableWidgetItem double-clicked at " + \
                       "row={}, column={}.".format(row, column))

        # Select the entire row of items where the item was clicked.
        top = row
        bottom = row
        left = 0
        right = self.columnCount() - 1

        range = QTableWidgetSelectionRange(top, left, bottom, right)
        selected = True

        self.setRangeSelected(range, selected)

    def contextMenuEvent(self, qcontextmenuevent):
        """Overwrites the QWidget contextMenuEvent function.

        This brings up a context menu with options:
        - Copy highlighted cell(s) text to clipboard as CSV 
          (without column headers).
        - Copy highlighted cell(s) text to clipboard as CSV
          (with column headers).
        """

        self.log.debug("Entered contextMenuEvent()")

        # First see if any cells are selected.  If there's nothing
        # selected, the actions are disabled.
        cellsAreSelected = False
        if len(self.selectedRanges()) > 0:
            cellsAreSelected = True

        # Open up a context menu.
        menu = QMenu()
        parent = None

        # These are the QActions that are in the menu.
        copyCellTextAsCSVAction = \
            QAction("Copy cell(s) to clipboard as CSV", parent)
        copyCellTextAsCSVAction.triggered.\
            connect(self._selectedCellsTextToClipboard)

        copyCellTextWithColumnHeadersAsCSVAction = \
            QAction("Copy cell(s) to clipboard as CSV " + \
                    "(with column headers)", parent)
        copyCellTextWithColumnHeadersAsCSVAction.triggered.\
            connect(self._selectedCellsAndHeadersTextToClipboard)

        # Enable or disable depending on whether or not cells are selected.
        copyCellTextAsCSVAction.setEnabled(cellsAreSelected)
        copyCellTextWithColumnHeadersAsCSVAction.setEnabled(cellsAreSelected)

        # Add the QActions to the menu.
        menu.addAction(copyCellTextAsCSVAction)
        menu.addAction(copyCellTextWithColumnHeadersAsCSVAction)

        menu.exec_(QCursor.pos())
    
        self.log.debug("Exiting contextMenuEvent()")

    def _selectedCellsTextToClipboard(self, sendColumnHeaders=False):
        """Obtains the selected cells, and turns the text in them to text
        in CSV format.  The text is then copied to the clipboard.

        If the argument 'sendColumnHeaders' is True, then column headers
        are a row in the text sent to the clipboard.
        """

        self.log.debug("Entered _selectedCellsTextToClipboard()")

        # Get the selected ranges.
        selectedRanges = self.selectedRanges()

        numRanges = len(selectedRanges)

        textToClipboard = ""

        for i in range(numRanges):
            r = selectedRanges[i] 

            leftColumn = r.leftColumn()
            rightColumn = r.rightColumn()
            topRow = r.topRow()
            bottomRow = r.bottomRow()

            self.log.debug("DEBUG: " + \
                           "leftColumn={}, ".format(leftColumn) + 
                           "rightColumn={}, ".format(rightColumn) + 
                           "topRow={}, ".format(topRow) + 
                           "bottomRow={}".format(bottomRow))

            if sendColumnHeaders == True:
                for j in range(leftColumn, rightColumn + 1):
                    headerText = self.horizontalHeaderItem(j).text()
                    textToClipboard += headerText.replace(os.linesep, " ")

                    if j != rightColumn:
                        textToClipboard += ","

                textToClipboard += os.linesep

            for j in range(topRow, bottomRow + 1):
                for k in range(leftColumn, rightColumn + 1):
                    textToClipboard += self.item(j, k).text()

                    if k != rightColumn:
                        textToClipboard += ","

                if j != bottomRow:
                    textToClipboard += os.linesep

            textToClipboard += os.linesep + os.linesep

        if textToClipboard == "" and numRanges == 0:
            self.log.debug("No cells were selected.")
        else:
            self.log.debug("Sending the following text to clipboard: " + 
                           textToClipboard)
            clipboard = QApplication.clipboard()
            clipboard.setText(textToClipboard)

        self.log.debug("Exiting _selectedCellsTextToClipboard()")

    def _selectedCellsAndHeadersTextToClipboard(self):
        """Obtains the selected cells and their corresponding header text
        and converts them to CSV format.  That text is then copied to the
        clipboard.
        """

        self.log.debug("Entered _selectedCellsAndHeadersTextToClipboard()")

        self._selectedCellsTextToClipboard(True)

        self.log.debug("Exiting _selectedCellsAndHeadersTextToClipboard()")
    
    def _replaceRowWithPlanetaryInfo(self, row, planetaryInfo):
        """Replaces all the existing QTableWidgetItems in row 'row', with the
        data in PlanetaryInfo 'planetaryInfo'.

        If the row doesn't exist, then QTableWidgetItems are created for
        that row.
        """

        p = planetaryInfo

        # QTableWidgetItem flags.
        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled

        rowCount = self.rowCount()
        col = 0

        # If the row given 
        if row >= rowCount:
            self.setRowCount(row + 1)

        # Item for the planet name.

        # Try to re-use the existing item if one exists already.
        item = self.item(row, col)
        if item == None:
            item = QTableWidgetItem()
            self.setItem(row, col, item)
        item.setText(p.name)
        col += 1

        zodiacs = ['tropical', 'sidereal']

        fields = ['longitude',
                  'latitude',
                  'distance',
                  'longitude_speed',
                  'latitude_speed',
                  'distance_speed',
                  'rectascension',
                  'declination',
                  'rectascension_speed',
                  'declination_speed',
                  'X',
                  'Y',
                  'Z',
                  'dX',
                  'dY',
                  'dZ']

        dicts = [p.geocentric, p.topocentric, p.heliocentric]
        
        for dict in dicts:
            for zodiac in zodiacs:
                for field in fields:

                    # Create the QTableWidgetItem with the string as the
                    # value of the field.
                    valueStr = "{}".format(dict[zodiac][field])

                    # Try to re-use the existing item if one exists already.
                    item = self.item(row, col)
                    if item == None:
                        item = QTableWidgetItem()
                        self.setItem(row, col, item)
                    item.setText(valueStr)

                    # Get what the units is from the header item.
                    # This is stored in the tooltip of the header item,
                    # and the part of the string we're interested in is
                    # the part between the parenthesis.
                    headerItem = self.horizontalHeaderItem(col)
                    toolTipStr = headerItem.toolTip()
                    startParenPos = toolTipStr.find("(")
                    endParenPos = toolTipStr.rfind(")")

                    if startParenPos != -1 and \
                        endParenPos != -1 and \
                        startParenPos < endParenPos:

                        toolTipStr = \
                            valueStr + " " + \
                            toolTipStr[startParenPos+1:endParenPos]

                        item.setToolTip(toolTipStr)

                    col += 1


    def _appendPlanetaryInfo(self, planetaryInfo):
        """Appends the info in the PlanetaryInfo object as a row of
        QTableWidgetItems.
        """

        # Here we call the replace function with what would be the next
        # available row.  The replace function is smart enough to create
        # new QTableWidgetItems if it needs them.
        row = self.rowCount()
        self._replaceRowWithPlanetaryInfo(row, planetaryInfo)


class TimestampEditWidget(QWidget):
    """QWidget for editing/displaying timestamps.
    
    This includes the ability to set whether or not it is in daylight
    savings time or not.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, timestamp, parent=None):
        """Initializes the widgets to hold the datetime.datetime in
        the timestamp variable.

        Arguments:
        timestamp - datetime.datetime object with a non-None pytz timezone.
        """
        
        super().__init__(parent)
        
        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.TimestampEditWidget")

        # Do some input checking.
        if not isinstance(timestamp, datetime.datetime):
            msg = "Argument 'timestamp' is expected to be a " + \
                  "datetime.datetime object."
            self.log.error(msg)
            QMessageBox.warning(self, "Programmer error", msg)
            return
        elif timestamp.tzinfo == None:
            msg = "Argument 'timestamp' is expected to have " + \
                  "tzinfo set in the datetime.datetime object as " + \
                  "a pytz.timezone object."
            self.log.error(msg)
            QMessageBox.warning(self, "Programmer error", msg)
            return
        
        # Save off the timestamp as a datetime.datetime object.
        # This is only modified if save is called.
        self.dt = timestamp

        # QGroupBox to hold the edit widgets and form.
        self.groupBox = QGroupBox("Timestamp:")
        
        # Date and time.
        self.datetimeLabel = QLabel("Date and Time:")
        self.datetimeEditWidget = QDateTimeEdit()
        self.datetimeEditWidget.setMinimumDate(QDate(101, 1, 1))

        # Timezone.
        self.timezoneLabel = QLabel("Timezone:")
        self.timezoneComboBox = QComboBox()
        self.timezoneComboBox.addItems(pytz.common_timezones)

        # Daylight savings modes.
        self.daylightLabel = QLabel("Daylight savings:")
        self.daylightComboBox = QComboBox()
        
        # Form layout.
        self.formLayout = QFormLayout()
        self.formLayout.setLabelAlignment(Qt.AlignLeft)
        self.formLayout.addRow(self.datetimeLabel, self.datetimeEditWidget)
        self.formLayout.addRow(self.timezoneLabel, self.timezoneComboBox)
        self.formLayout.addRow(self.daylightLabel, self.daylightComboBox)

        self.groupBox.setLayout(self.formLayout)

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

        # Now that all the widgets are created, load the values from the
        # timestamp.
        self.loadTimestamp(self.dt)

        # Connect signals and slots.

        # Connect okay and cancel buttons.
        self.datetimeEditWidget.dateTimeChanged.\
            connect(self.updateDaylightComboBox)
        self.timezoneComboBox.currentIndexChanged.\
            connect(self.updateDaylightComboBox)
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def _getAllTzNamesForTimezone(self, tz):
        """Returns a list of str objects, which consist of all the possible
        tznames (e.g, "EST", "EDT"), that are possible in a given timezone.
        The timezone to test against is the pytz.timezone in 'tz'.

        Arguments:

        tz - pytz.timezone object to get the possible tznames from.
        """

        # Return value.
        tznames = []

        # Go through the first day of each month and try to find
        # unique strings for the tzname.  I'm just doing this because
        # it's fast, and I believe all timezones implement their
        # daylight savings time for a span of more than one month a
        # year.
        year = 2010
        day = 1

        for i in range(12):
            month = i + 1
            dt = datetime.datetime(year, month, day, tzinfo=None)
            try:
                name = tz.tzname(dt)
                if name not in tznames:
                    tznames.append(name)
            except pytz.InvalidTimeError as e:
                # Ignore.
                pass

        return sorted(tznames)
    
    def updateDaylightComboBox(self):
        """Updates the daylight savings combo box because the
        timestamp has changed or the timezone has changed.

        This field is only enabled if the timezone has more than one
        tzname (for daylight saving time and standard time).  If we
        can arrive at whether we are in DST time or standard time,
        then this widget will be set to the appropriate selection, and
        the combobox disabled.  If the timestamp and timezone settings
        make the daylightComboBox ambiguous, then the widget becomes
        enabled and user may select which one he/she wants.

        In otherwords, this widget is 'smart'.
        """

        # Construct a datetime.datetime object from the QDateTimeEdit
        # widget's current values.
        qdatetime = self.datetimeEditWidget.dateTime()
        qdate = qdatetime.date()
        qtime = qdatetime.time()

        dt = datetime.datetime(qdate.year(), qdate.month(), qdate.day(),
                               qtime.hour(), qtime.minute(), qtime.second())
        
        timezoneString = str(self.timezoneComboBox.currentText())
        
        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)

        # Populate with possible tznames.
        tznames = self._getAllTzNamesForTimezone(tzinfoObj)
        self.daylightComboBox.clear()
        self.daylightComboBox.addItems(daylightNames)
        if len(daylightNames) < 2:
            self.daylightComboBox.setEnabled(False)

        # Find out if the timestamp is ambiguous.
        try:
            temp = tzinfoObj.localize(dt, is_dst=None)
            
            # If it got here, that means the timestamp is not ambiguous.
            # Select the relevant daylight savings/standard time tzname.
            tznameStr = temp.tzname()

            index = self.daylightComboBox.findText(tznameStr)
            if index != -1:
                self.daylightComboBox.setCurrentIndex(index)
            else:
                errStr = "Couldn't find the tzname " + tznameStr + \
                         " in the combo box list of tznames."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)
            
        except pytz.InvalidTimeError as e:
            # Timestamp is ambiguous in terms of daylight savings time.
            
            # Select the first entry in the combo box, and enable the
            # combo box so the user can pick which one he/she wants.
            if self.daylightComboBox.count() > 0:
                self.daylightComboBox.setCurrentIndex(0)
                self.daylightComboBox.setEnabled(True)
            else:
                errStr = "Timestamp is ambiguous and there are " + \
                         "no possible find the tznames?!?  " + \
                         "How can this be?  There must be a " + \
                         "logic error in my code somewhere..."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

            
    def loadTimestamp(self, timestamp):
        """Loads the widgets with values from the given
        PriceBarChartScaling object.
        """

        self.log.debug("Entered loadTimestamp()")

        # Check inputs.
        if timestamp == None:
            self.log.error("Invalid parameter to loadTimestamp().  " + \
                           "timestamp can't be None.")
            self.log.debug("Exiting loadTimestamp()")
            return
        else:
            self.dt = timestamp 

        # Convert the datetime object to the equivalent qdatetime.
        # Note: Here we are assuming timespec UTC.  This is only for
        # the information internal to QDateTimeEdit.  We keep the
        # actual timezone information in self.dt.
        date = QDate(self.dt.year, self.dt.month, self.dt.day)
        time = QTime(self.dt.hour, self.dt.minute, self.dt.second)
        timespec = Qt.UTC
        qdatetime = QDateTime(date, time, timespec)

        # Set the timestamp.
        self.datetimeEditWidget.setDateTime(qdatetime)

        # Select the timezone.
        index = self.timezoneComboBox.findText(self.dt.tzinfo.zone)
        if index != -1:
            self.timezoneComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find timezone '" + self.dt.tzinfo.zone + \
                     "' in the pytz list of timezones."
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)
            return

        # Call update on the daylight combo box, just so we can get it
        # populated with the correct tznames.  That function may or
        # may not set the current index to match self.dt, so we'll
        # have to manually select the tzname ourselves.
        self.updateDaylightComboBox()

        tznameStr = self.dt.tzname()
        index = self.daylightComboBox.findText(tznameStr)
        if index != -1:
            self.daylightComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find the tzname " + tznameStr + \
                     " in the combo box list of tznames."
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)

        self.log.debug("Exiting loadTimestamp()")
        
    def saveTimestamp(self):
        """Saves the values in the widgets to the 
        PriceBarChartScaling object passed in this class's constructor.
        """
    
        self.log.debug("Entered saveTimestamp()")

        # Get from the QDateTimeEdit the primitives of the timestamp.
        qdatetime = self.datetimeEditWidget.dateTime()
        qdate = qdatetime.date()
        qtime = qdatetime.time()
        year = qdate.year()
        month = qdate.month()
        day = qdate.day()
        hour = qtime.hour()
        minute = qtime.minute()
        second = qtime.second()

        # Create a native datetime with no tzinfo set.
        dt = datetime.datetime(year, month, day, hour, minute, second, \
                               tzinfo=None)
        
        # Get from the timezone combobox the Timezone string.
        timezoneString = str(self.timezoneComboBox.currentText())

        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)

        # Get whether it is in daylightSavings or not.
        
        # Here we have to replicate how we set the values in order to
        # get them, because with the pytz api, there is no other way
        # to test if it is in daylight savings time without actually
        # localizing a datetime.datetime.

        # Find out if the timestamp is ambiguous.
        try:
            localizedDt = tzinfoObj.localize(dt, is_dst=None)
            
            # If it got here, that means the timestamp is not ambiguous.
            self.dt = localizedDt
            
        except pytz.InvalidTimeError as e:
            # Timestamp is ambiguous in terms of daylight savings time.

            # See the tzname for is_dst=True and see what it is for
            # is_dst=False.
            dtDstTrue = tzinfoObj.localize(dt, is_dst=True)
            dtDstFalse = tzinfoObj.localize(dt, is_dst=False)
            
            # Compare this with what is selected in
            # self.daylightComboBox to determine if it is in
            # daylightSavings or not.
            daylightText = self.daylightComboBox.currentText()

            if daylightText == dtDstTrue.tzname():
                self.dt = dtDstTrue
            elif daylightText == dtDstFalse.tzname():
                self.dt = dtDstFalse
            else:
                errStr = "Timestamp NOT saved.  " + os.linesep + \
                         "The timestamp is ambiguous and the " + \
                         "tznames for is_dst=True and is_dst=False " + \
                         "don't match any of the possible tznames " + \
                         "in the self.daylightComboBox!  " + \
                         "This problem needs to be debugged."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

        self.log.debug("Exiting saveTimestamp()")

    def getTimestamp(self):
        """Gets and returns the timestamp as saved in this widget.
        This value only matches what is in the widgets if nothing has
        changed, or if saveTimestamp() has been called previous to
        calling this function.

        Returns:

        datetime.datetime object with it's date and time set, and with
        tzinfo set to a valid pytz.timezone object.
        """

        return self.dt
        
    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveTimestamp()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class TimestampEditDialog(QDialog):
    """QDialog for editing timestamps.
    
    This includes the timezone information (and whether in daylight
    savings or not).
    """

    def __init__(self, timestamp, parent=None):
        """Initializes the internal widgets to hold the
        datetime.datetime in the timestamp variable.

        Arguments:
        timestamp - datetime.datetime object with a non-None pytz timezone.
        """
        
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.TimestampEditDialog")

        self.setWindowTitle("Timestamp")

        # Save a reference to the datetime.datetime timestamp.
        self.dt = timestamp
        
        # Create the contents.
        self.editWidget = TimestampEditWidget(self.dt)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def getTimestamp(self):
        """Returns the internally stored timestamp.

        Returns:

        datetime.datetime object with the tzinfo set to a pytz.timezone.
        This datetime.datetime is the timestamp as edited by the dialog.
        """

        self.dt = self.editWidget.getTimestamp()
        
        return self.dt

    
class PriceBarTagEditWidget(QWidget):
    """QWidget for editing the tags on a PriceBar.
    
    The tags associated with a PriceBar are just a list of strings
    that may have meaning to that particular PriceBar.
    
    For example, different schemes can be used, for example,"H",
    used for a high within 5 bars... and "LL" used for a
    low within 10 bars, etc.
    """

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, tags=[], parent=None):
        """Initializes the edit widget with the given values.

        Arguments:

        tags   - list of str objects.
                 This is the list of tag strings we are editing.

        parent - QWidget parent
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.PriceBarTagEditWidget")

        # Save off the list of tags.
        self.tags = list(tags)

        self.tagsListGroupBox = \
            QGroupBox("List of PriceBar tags:")

        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Layout to hold the list widget.
        self.listWidgetLayout = QVBoxLayout()
        self.listWidgetLayout.addWidget(self.listWidget)

        self.tagsListGroupBox.setLayout(self.listWidgetLayout)
        
        # Buttons for doing actions like adding, removing, and editing a
        # tag, etc.

        self.addTagButton = QPushButton("&Add Tag")
        self.removeTagButton = QPushButton("&Remove Tag")
        self.editTagButton = QPushButton("&Edit Tag")
        self.moveSelectedTagUpButton = QPushButton("Move Tag &up")
        self.moveSelectedTagDownButton = QPushButton("Move Tag &down")

        self.buttonsOnRightLayout = QVBoxLayout()
        self.buttonsOnRightLayout.addWidget(self.addTagButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.addWidget(self.removeTagButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.addWidget(self.editTagButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.\
            addWidget(self.moveSelectedTagUpButton)
        self.buttonsOnRightLayout.addSpacing(5)
        self.buttonsOnRightLayout.\
            addWidget(self.moveSelectedTagDownButton)
        self.buttonsOnRightLayout.addStretch()

        self.mainWidgetsLayout = QHBoxLayout()
        self.mainWidgetsLayout.addWidget(self.tagsListGroupBox)
        self.mainWidgetsLayout.addLayout(self.buttonsOnRightLayout)

        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.mainWidgetsLayout) 
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Connect signals and slots.
        self.listWidget.itemDoubleClicked.\
            connect(self._handleEditTagButtonClicked)
        self.addTagButton.clicked.\
            connect(self._handleAddTagButtonClicked)
        self.removeTagButton.clicked.\
            connect(self._handleRemoveTagButtonClicked)
        self.editTagButton.clicked.\
            connect(self._handleEditTagButtonClicked)
        self.moveSelectedTagUpButton.clicked.\
            connect(self._handleMoveTagUpButtonClicked)
        self.moveSelectedTagDownButton.clicked.\
            connect(self._handleMoveTagDownButtonClicked)

        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

        # Now that all the widgets are created, load the values from the
        # settings.
        self.loadTags(self.tags)


    def loadTags(self, tags):
        """Loads the widgets with values from the given arguments.

        Arguments:

        tags - list of str objects.
        """

        self.log.debug("Entered loadTags()")

        # Save off the values.
        self.tags = list(tags)

        # Populate the QListWidget with the tags.
        self.listWidget.clear()
        for tag in self.tags:
            self._appendTagAsListWidgetItem(tag, False)

        if self.listWidget.count() > 0:
            self.listWidget.setCurrentRow(0)

        self.log.debug("Exiting loadTags()")
        
    def saveTags(self):
        """Ensures the values in the widgets are saved to their
        underlying variables, such that subsequent calls to getTags()
        will return valid values for what has changed.
        """
    
        self.log.debug("Entered saveTag()")

        self.tags = []

        numTags = self.listWidget.count()
        
        for i in range(numTags):
            item = self.listWidget.item(i)
            
            self.tags.append(item.text())
        
        self.log.debug("Exiting saveTag()")


    def getTags(self):
        """Returns the internally stored list of tags which are really
        just a list of str objects.  This may or may not represent
        what is in the widgets, depending on whether or not saveTags
        has been called recently.
        """

        return self.tags

    def _appendTagAsListWidgetItem(self, tag, selectItem=True):
        """Appends the given Tag str object to the
        QListWidget as a QListWidgetItem.

        Arguments:
        
        tag - str which represents the PriceBar tag.

        selectItem - bool flag that indicates whether the item should be
        selected after being created and appended to the list.
        """

        listWidgetItem = QListWidgetItem()

        listWidgetItem.setText(tag)

        self.listWidget.addItem(listWidgetItem)
        
        if selectItem == True:
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)


    def _handleAddTagButtonClicked(self):
        """Called when the 'Add Tag' button is clicked."""

        # Create a dialog and allow the user to edit it.
        accepted = False

        parent = self
        title = "New Tag"
        label = "Tag:"
        echoMode = QLineEdit.Normal
        initialText = ""
        
        (text, accepted) = \
            QInputDialog.getText(parent, title, label, echoMode, initialText)
        
        if accepted == True:
            tag = text.strip()
            if tag != "":
                self._appendTagAsListWidgetItem(tag, True)

    def _handleRemoveTagButtonClicked(self):
        """Called when the 'Remove Tag' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        if row >= 0 and row < self.listWidget.count():
            # It is a valid row.

            # First remove the item from the QListWidget.
            self.listWidget.takeItem(row)

            # If there is another item after that one in the list, then
            # select that one as the current, otherwise select the index
            # before.
            if self.listWidget.item(row) != None:
                # There an item after this one, so set that one as the
                # current.
                self.listWidget.setCurrentRow(row)
            else:
                # The one we just removed was the last item in the
                # list.  Select the one before it if it exists,
                # otherwise, clear out the display fields.
                if row != 0:
                    self.listWidget.setCurrentRow(row - 1)

    def _handleEditTagButtonClicked(self):
        """Called when the 'Edit Tag' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Get the selected item.
        item = self.listWidget.item(row)
        
        # Get the str for editing.
        tag = item.text()
        
        # Create a dialog and allow the user to edit it.
        accepted = False

        parent = self
        title = "Edit Tag"
        label = "Tag:"
        echoMode = QLineEdit.Normal
        initialText = tag
        
        (text, accepted) = \
            QInputDialog.getText(parent, title, label, echoMode, initialText)
        
        if accepted == True:
            text = text.strip()
            if text != "" and text != tag:
                item.setText(text)

    def _handleMoveTagUpButtonClicked(self):
        """Called when the 'Move tag up' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Proceed only if the selected tag is not the top entry in the
        # QListWidget.
        if row > 0:
            # It is not the top row yet, so we can do a swap to move it
            # higher.

            currItem = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, currItem)

            # Set the selected row as the same underlying tag.
            self.listWidget.setCurrentRow(row - 1)

    def _handleMoveTagDownButtonClicked(self):
        """Called when the 'Move tag down' button is clicked."""

        # Get the selected row.
        row = self.listWidget.currentRow()

        # Proceed only if the selected tag is not the bottom entry in
        # the QListWidget.
        if row < (self.listWidget.count() - 1) and row >= 0:
            # It is not the bottom row yet, so we can do a swap to move it
            # lower.

            currItem = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, currItem)

            # Set the selected row as the same underlying tag.
            self.listWidget.setCurrentRow(row + 1)

    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        self.saveTags()
        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()

class PriceBarTagEditDialog(QDialog):
    """QDialog for editing the tags on a PriceBar.

    The tags associated with a PriceBar are just a list of strings
    that may have meaning to that particular PriceBar.
    
    For example, different schemes can be used, for example,"H",
    used for a high within 5 bars... and "LL" used for a
    low within 10 bars, etc.
    """

    def __init__(self, tags=[], parent=None):
        """Initializes the internal edit widget with the given values.

        Arguments:

        tags   - list of str objects.
                 This is the list of tag strings we are editing.

        parent - QWidget parent
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widget.PriceBarTagEditDialog")

        self.setWindowTitle("PriceBar Tags")

        # Save a reference to the PriceBarChartScaling object.
        self.tags = tags

        # Create the contents.
        self.editWidget = PriceBarTagEditWidget(self.tags)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def getTags(self):
        """Returns the internally stored tags.

        Returns:

        list of str objects.  Each str object in the list is a tag.
        """

        self.tags = self.editWidget.getTags()
        
        return self.tags


class PriceBarEditWidget(QWidget):
    """QWidget for editing the a PriceBar."""

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, priceBar, parent=None):
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.PriceBarEditWidget")

        # Save off the PriceBarChartScaling object.
        self.priceBar = priceBar

        # Read-Only flag.
        self.readOnlyFlag = False

        # PriceBar tags, stored in this variable instead of an edit widget.
        # Upon loading a new PriceBar, this variable is set.
        self.tags = []
        
        # QGroupBox to hold the edit widgets and form.
        self.groupBox = \
            QGroupBox("PriceBar:")

        # Timestamp.
        self.timestampLabel = QLabel("Timestamp:")
        self.timestampEditWidget = TimestampEditWidget()

        # Open price.
        self.openPriceLabel = QLabel("Open Price:")
        self.openPriceSpinBox = QDoubleSpinBox()
        self.openPriceSpinBox.setMinimum(0.0)
        self.openPriceSpinBox.setMaximum(999999999.0)

        # High price.
        self.highPriceLabel = QLabel("High Price:")
        self.highPriceSpinBox = QDoubleSpinBox()
        self.highPriceSpinBox.setMinimum(0.0)
        self.highPriceSpinBox.setMaximum(999999999.0)

        # Low price.
        self.lowPriceLabel = QLabel("Low Price:")
        self.lowPriceSpinBox = QDoubleSpinBox()
        self.lowPriceSpinBox.setMinimum(0.0)
        self.lowPriceSpinBox.setMaximum(999999999.0)

        # Close price.
        self.closePriceLabel = QLabel("Close Price:")
        self.closePriceSpinBox = QDoubleSpinBox()
        self.closePriceSpinBox.setMinimum(0.0)
        self.closePriceSpinBox.setMaximum(999999999.0)

        # Open interest.
        self.openInterestLabel = QLabel("Open Interest:")
        self.openInterestSpinBox = QDoubleSpinBox()
        self.openInterestSpinBox.setMinimum(0.0)
        self.openInterestSpinBox.setMaximum(999999999.0)

        # Volume.
        self.volumeLabel = QLabel("Volume:")
        self.volumeSpinBox = QDoubleSpinBox()
        self.volumeSpinBox.setMinimum(0.0)
        self.volumeSpinBox.setMaximum(999999999.0)

        # Tags.
        self.tagsListWidget = QListWidget()
        self.tagsListWidget.clear()
        self.tagsListWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Layout and groupbox to hold the tags list widget.
        self.listWidgetLayout = QVBoxLayout()
        self.listWidgetLayout.addWidget(self.tagsListWidget)
        self.tagsListGroupBox = QGroupBox("Tags:")
        self.tagsListGroupBox.setLayout(self.listWidgetLayout)
        self.tagsListEditButton = QPushButton("Edit Tags")

        # Set widgets in the layouts.
        self.formLayout = QFormLayout()
        self.formLayout.setLabelAlignment(Qt.AlignLeft)
        self.formLayout.addRow(self.timestampLabel,
                               self.timestampEditWidget)
        self.formLayout.addRow(self.openPriceLabel, 
                               self.openPriceSpinBox)
        self.formLayout.addRow(self.lowPriceLabel, 
                               self.lowPriceSpinBox)
        self.formLayout.addRow(self.closePriceLabel, 
                               self.closePriceSpinBox)
        self.formLayout.addRow(self.openInterestLabel, 
                               self.openInterestSpinBox)
        self.formLayout.addRow(self.volumeLabel, 
                               self.volumeSpinBox)
        self.formLayout.addRow(self.tagsListGroupBox, 
                               self.tagsListEditButton)

        self.groupBox.setLayout(self.formLayout)

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

        # Now that all the widgets are created, load the values from the
        # settings.
        self.loadPriceBar(self.priceBar)

        # Connect signals and slots.
        self.tagsListEditButton.clicked.\
            connect(self._handleTagsListEditButtonClicked)
        
        # Connect okay and cancel buttons.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

    def setReadOnly(self, readOnlyFlag):
        """Sets the flag that indicates that this widget is in
        read-only mode.  The effect of this is that the user cannot
        edit any of the fields in the PriceBar.
        """
        
        self.readOnlyFlag = readOnlyFlag

        # Set the internal widgets as readonly or not depending on this flag.
        self.timestampEditWidget.setReadOnly(self.readOnlyFlag)
        self.openPriceSpinBox.setReadOnly(self.readOnlyFlag)
        self.highPriceSpinBox.setReadOnly(self.readOnlyFlag)
        self.lowPriceSpinBox.setReadOnly(self.readOnlyFlag)
        self.closePriceSpinBox.setReadOnly(self.readOnlyFlag)
        self.openInterestSpinBox.setReadOnly(self.readOnlyFlag)
        self.volumeSpinBox.setReadOnly(self.readOnlyFlag)
        self.tagsListEditButton.setEnabled(not self.readOnlyFlag)

        # Don't allow the Okay button to be pressed for saving.
        self.okayButton.setEnabled(not self.readOnlyFlag)
        
    def getReadOnly(self, readOnlyFlag):
        """Returns the flag that indicates that this widget is in
        read-only mode.  If the returned value is True, then it means
        the user cannot edit any of the fields in the PriceBar.
        """
        
        return self.readOnlyFlag

    def loadPriceBar(self, priceBar):
        """Loads the widgets with values from the given
        PriceBar object.
        """

        self.log.debug("Entered loadPriceBar()")

        # Check inputs.
        if priceBar == None:
            self.log.error("Invalid parameter to loadPriceBar().  " + \
                           "priceBar can't be None.")
            self.log.debug("Exiting priceBar()")
            return
        else:
            self.priceBar = priceBar 

        self.timestampEditWidget.loadTimestamp(self.priceBar.timestamp)
        self.openPriceSpinBox.setValue(self.priceBar.open)
        self.highPriceSpinBox.setValue(self.priceBar.high)
        self.lowPriceSpinBox.setValue(self.priceBar.low)
        self.closePriceSpinBox.setValue(self.priceBar.close)
        self.openInterestSpinBox.setValue(self.priceBar.oi)
        self.volumeSpinBox.setValue(self.priceBar.vol)

        self.tags = list(self.priceBar.tags)
        
        # Populate the tagsListWidget with the str objects in
        # self.priceBar.tags.
        self.tagsListWidget.clear();
        for tag in self.tags:
            listWidgetItem = QListWidgetItem()
            listWidgetItem.setText(tag)
            self.tagsListWidget.addItem(listWidgetItem)
        if self.tagsListWidget.count() > 0:
            self.tagsListWidget.setCurrentRow(0)
            
        self.log.debug("Exiting loadPriceBar()")
        
    def savePriceBar(self):
        """Saves the values in the widgets to the 
        PriceBar object passed in this class's constructor.
        """
    
        self.log.debug("Entered savePriceBar()")
        
        self.priceBar.timestamp = self.timestampEditWidget.getTimestamp()
        self.priceBar.open = self.openPriceSpinBox.value()
        self.priceBar.high = self.highPriceSpinBox.value()
        self.priceBar.low = self.lowPriceSpinBox.value()
        self.priceBar.close = self.closePriceSpinBox.value()
        self.priceBar.oi = self.openInterestSpinBox.value()
        self.priceBar.vol = self.volumeSpinBox.value()
        self.priceBar.tags = self.tags

        self.log.debug("Exiting savePriceBar()")

    def getPriceBar(self):
        """Returns the internally stored PriceBar object.
        This may or may not represent what is in the widgets, depending on
        whether or not savePriceBar() has been called.
        """

        return self.priceBar

    def setOkayCancelButtonsVisible(self, visibleFlag):
        """Hides or shows the Okay and Cancel buttons depending on the
        value of visibleFlag.

        Arguments:
        
        visibleFlag - bool value for whether or not to show the Okay
        and Cancel buttons.  If True, then the buttons are visible.
        If False, then the buttons are hidden.  The buttons are
        visible by default.
        """

        self.okayButton.setVisible(visibleFlag)
        self.cancelButton.setVisible(visibleFlag)

    def getOkayCancelButtonsVisible(self):
        """Returns whether or not the Okay and Cancel buttons are visible.

        Returns:
        bool value for whether or not the okay and cancel buttons are visible.
        """

        if self.okayButton.isVisible() and self.cancelButton.isVisible():
            return True
        else:
            return False

    def _handleTagsListEditButtonClicked(self):
        """Called when the 'Edit Tags' button is clicked.
        Opens up a dialog for editing the list of tags.
        """

        dialog = PriceBarTagEditDialog(self.tags, self)
        
        rv = dialog.exec_()
        
        if rv == QDialog.Accepted:
            # Set to self.tags, the values from the QDialog.
            self.tags = dialog.getTags()

            # Clear the list of tags displayed, reset them with the
            # new values.
            self.tagsListWidget.clear();
            for tag in self.tags:
                listWidgetItem = QListWidgetItem()
                listWidgetItem.setText(tag)
                self.tagsListWidget.addItem(listWidgetItem)
            if self.tagsListWidget.count() > 0:
                self.tagsListWidget.setCurrentRow(0)
        
        
    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked."""

        # Only save if the readOnlyFlag is False.
        if self.readOnlyFlag == False:
            self.savePriceBar()

        self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked."""

        self.cancelButtonClicked.emit()


class PriceBarEditDialog(QDialog):
    """QDialog for editing a PriceBar (the fields in it)."""

    def __init__(self, priceBar, readOnly=False, parent=None):
        """Initializes the internal widgets to hold the
        PriceBar in the priceBar variable.

        Arguments:
        
        priceBar - PriceBar object to edit or view in the dialog.
        
        readOnly - bool value for whether or not the user is allowed
                   to edit the fields in the given PriceBar.  If the
                   value is True, then the buttons and widgets allow
                   for modification.  If the value is False, then the
                   fields are viewable only.
        """
        
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("widgets.PriceBarEditDialog")

        self.setWindowTitle("PriceBar")

        # Save a reference to the PriceBar.
        self.priceBar = priceBar

        # Save the readOnly preference.
        self.readOnly = readOnly
        
        # Create the contents.
        self.editWidget = PriceBarEditWidget(self.priceBar)
        self.editWidget.setReadOnly(self.readOnly)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.editWidget)
        self.setLayout(layout)

        self.editWidget.okayButtonClicked.connect(self.accept)
        self.editWidget.cancelButtonClicked.connect(self.reject)

    def getPriceBar(self):
        """Returns the internally stored timestamp.

        Returns:
        PriceBar holding the edited PriceBar.  If the widget is in
        ReadOnly mode, or the user clicked the Cancel button, then the
        PriceBar is unchanged.
        """

        self.priceBar = self.editWidget.getPriceBar()
        
        return self.priceBar

    def loadPriceBar(self, priceBar):
        """Loads the widgets with values from the given
        PriceBar object.

        Arguments:
        priceBar - PriceBar object to load into the widgets.
        """

        self.priceBar = priceBar
        self.editWidget.loadPriceBar(self.priceBar)
        
    def setReadOnly(self, readOnly):
        """Sets the readOnly flag to the value given in 'readOnly'.

        Arguments:
        readOnly - bool value.  If True, then the widgets are made to
        be unmodifiable.  If False, then the widgets can be changed
        and the priceBar can be modified.
        """
        
        self.readOnly = readOnly
        self.editWidget.setReadOnly(self.readOnly)

    def getReadOnly(self):
        """Returns the current setting of the readOnly flag.

        Returns:
        bool value representing whether or not the PriceBar can be modified.
        """

        return self.readOnly

# For debugging the module during development.  
if __name__=="__main__":
    from ephemeris import Ephemeris

    # Initialize Logging for the Ephemeris class (required).
    Ephemeris.initialize()

    # Set a default location (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)


    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    print("Now is: {}".format(now))

    planets = []

    # Get planetary info for all the planets, and print out the info.
    p = Ephemeris.getSunPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getMoonPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getMercuryPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getVenusPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getMarsPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getJupiterPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getSaturnPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getUranusPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getNeptunePlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getPlutoPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getMeanNorthNodePlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getTrueNorthNodePlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getMeanLunarApogeePlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getEarthPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    p = Ephemeris.getChironPlanetaryInfo(now)
    planets.append(p)
    #print("At {}, planet '{}' has the following info: \n{}".\
    #        format(now, p.name, p.toString()))
    
    
    #widget = PlanetaryInfoTableWidget(planets)
    #widget = PlanetaryInfoTableWidget([])
    #widget.show()


    #tags = ["hello", "myname_is", "a happy camper", "LLLL", "HH"]
    #dialog = PriceBarTagEditDialog(tags)
    #rv = dialog.exec()
    #if rv == QDialog.Accepted:
    #    print("Accepted")
    #    tags = dialog.getTags()
    #    print("{}".format(tags))
    #else:
    #    print("Rejected")
    #    tags = dialog.getTags()
    #    print("{}".format(tags))


    # Quit.
    #print("Exiting.")
    #import sys
    #sys.exit()
        
    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    app.exec_()

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()


