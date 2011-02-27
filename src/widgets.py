
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


def testPlanetaryInfoTableWidget():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    print("Now is: {}".format(now))

    planets = []

    # Get planetary info for all the planets, and print out the info.
    p = Ephemeris.getSunPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMoonPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMercuryPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getVenusPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMarsPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getJupiterPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getSaturnPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getUranusPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getNeptunePlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getPlutoPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMeanNorthNodePlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getTrueNorthNodePlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMeanLunarApogeePlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getEarthPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getChironPlanetaryInfo(now)
    planets.append(p)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))

    # Various combinations of planets to test.
    widget = PlanetaryInfoTableWidget(planets)
    #widget = PlanetaryInfoTableWidget([])

    layout = QVBoxLayout()
    layout.addWidget(widget)

    dialog = QDialog()
    dialog.setLayout(layout)

    rv = dialog.exec_()
    if rv == QDialog.Accepted:
        print("Accepted.")
    else:
        print("Rejected.")

# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
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
    
    testPlanetaryInfoTableWidget()
        
    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    #app.exec_()

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()


