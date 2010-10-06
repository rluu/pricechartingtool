
# For directory and file access.
import os
import sys
import io

# For access to urllib errors.
import urllib.error

# For logging.
import logging
import logging.config

# For PyQt UI classes.
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# For timezone lookup.
import datetime
import pytz

# Import image resources.
import resources

# For PriceBars
from data_objects import PriceBar
from data_objects import BirthInfo

# For geocoding.
from geonames import GeoNames
from geonames import GeoInfo

# For converting attributes of datetime.datetime objects to str.
from ephemeris import Ephemeris

class PriceChartDocumentWizard(QWizard):
    """QWizard for creating a new PriceChartDocument."""

    def __init__(self, parent=None):
        """Creates and sets up a QWizard for creating a new 
        PriceChartDocument."""

        super().__init__(parent)
        #super(PriceChartDocumentWizard, self).__init__(parent)

        # Logger object for this class.
        self.log = logging.getLogger("dialogs.PriceChartDocumentWizard")
        self.log.debug("Creating PriceChartDocumentWizard ...")

        # Add QWizardPages.
        self.log.debug("Creating PriceChartDocumentIntroWizardPage ...")
        self.addPage(PriceChartDocumentIntroWizardPage())
        self.log.debug("Creating " + \
                       "PriceChartDocumentLoadDataFileWizardPage ...")
        self.addPage(PriceChartDocumentLoadDataFileWizardPage())
        self.log.debug("Creating " + \
                       "PriceChartDocumentLocationTimezoneWizardPage ...")
        self.addPage(PriceChartDocumentLocationTimezoneWizardPage())
        self.log.debug("Creating " + \
                       "PriceChartDocumentConclusionWizardPage ...")
        self.addPage(PriceChartDocumentConclusionWizardPage())

        self.log.debug("Setting up Pixmaps ...")

        # Set the pictures used in the QWizard.
        watermarkPic = QPixmap(":/images/HowToMakeProfitsInCommodities.png")
        backgroundPic = QPixmap(":/images/HowToMakeProfitsInCommodities.png")
        logoPic = QPixmap(":/images/logo_ryan_d1.png").scaled(64, 64)
        bannerPic = QPixmap(":/images/banners/grad23.gif").scaled(640, 72)

        self.setPixmap(QWizard.WatermarkPixmap, watermarkPic)
        self.setPixmap(QWizard.BackgroundPixmap, backgroundPic)
        self.setPixmap(QWizard.LogoPixmap, logoPic)
        self.setPixmap(QWizard.BannerPixmap, bannerPic)

        self.log.debug("Setting window title ...")

        # Set the title of the window.
        self.setWindowTitle("New Price Chart")


class PriceChartDocumentIntroWizardPage(QWizardPage):
    """A QWizardPage that displays an introduction message to the QWizard."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("New Price Chart")
        self.setSubTitle(" ")

        # Create the contents.
        label = QLabel("This wizard will guide you through creating " + \
                       "a Price Chart document.")
        label.setWordWrap(True)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class PriceChartDocumentLoadDataFileWizardPage(QWizardPage):
    """A QWizardPage for loading price data from a file."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.PriceChartDocumentLoadDataFileWizardPage")

        # Set the title strings.
        self.setTitle("Loading Price Data")
        self.setSubTitle(" ")

        # Internal edit widget.
        self.loadDataFileWidget = LoadDataFileWidget()
        self.loadDataFileWidget.setBottomButtonsVisible(False)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.loadDataFileWidget)
        self.setLayout(layout)

        # Register the fields.
        self.registerField("dataFilename*", 
                           self.loadDataFileWidget.filenameLineEdit)
        self.registerField("dataNumLinesToSkip*", 
                           self.loadDataFileWidget.skipLinesSpinBox)

        # Connect signals and slots.
        self.loadDataFileWidget.validationStateChanged.\
            connect(self.completeChanged)

    def isComplete(self):
        """Returns True if validation succeeded, otherwise returns False.
        This function overrides the QWizardPage.isComplete() virtual
        function.
        """

        return self.loadDataFileWidget.isValidated()


class PriceChartDocumentLocationTimezoneWizardPage(QWizardPage):
    """A QWizardPage for setting the location of the trading exchange
    and the timezone that the exchange is in.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.PriceChartDocumentLocationTimezoneWizardPage")

        # Set the title strings.
        self.setTitle("Exchange Timezone")
        self.setSubTitle(" ")

        # Create the contents.
        self.locationTimezoneEditWidget = LocationTimezoneEditWidget()
        self.locationTimezoneEditWidget.setBottomButtonsVisible(False)
        
        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.locationTimezoneEditWidget)
        self.setLayout(layout)

        # Register the fields.
        self.registerField("timezone*", \
                           self.locationTimezoneEditWidget.timezoneComboBox,
                           "currentText")

    def isComplete(self):
        """Returns True if inputs are all entered, otherwise returns False.
        This function overrides the QWizardPage.isComplete() virtual
        function.
        """

        # Combo box always has something valid.
        return True

class PriceChartDocumentConclusionWizardPage(QWizardPage):
    """A QWizardPage for presenting the conclusion to the QWizard."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Conclusion")
        self.setSubTitle(" ")

        # Create the contents.
        label = QLabel("Setup is now complete.  " + \
                       "Please click the Finish button.")
        label.setWordWrap(True)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class LoadDataFileWidget(QWidget):
    """A widget for loading and verifying CSV text files containing 
    price data.
    """

    # Signal emitted when the data file to be loaded has been 
    # validated or becomes unvalidated.  
    # Emitting True means the data file was found to be valid.  
    # Emitting False means the data file was found to be not valid.
    validationStateChanged = QtCore.pyqtSignal(bool)

    # Signal emitted when the Load button is clicked.
    loadButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.LoadDataFileWidget")

        # Validated flag that indicates the file and number of 
        # lines skipped is valid.
        self.validatedFlag = False

        # Internally stored list of pricebars.
        self.priceBars = []

        # Create the contents.

        # Informational labels.
        descriptionLabel = \
            QLabel("Please select a file for loading price data." + \
                   os.linesep + os.linesep + \
                   "The selected file must be in CSV format with each " + \
                   "line of text having fields in the following order: " + \
                   os.linesep)
        descriptionLabel.setWordWrap(True)

        fileInfoDataDescStr = \
                      "<MM/DD/YYYY>," + \
                      "<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>," + \
                      "<Volume>,<OpenInterest>" + os.linesep
        fileInfoLabel = QLabel(fileInfoDataDescStr)
        font = fileInfoLabel.font()
        font.setPointSize(7)
        fileInfoLabel.setFont(font)
        
        # Frame as a separator.
        self.sep1 = QFrame()
        self.sep1.setFrameShape(QFrame.HLine)
        self.sep1.setFrameShadow(QFrame.Sunken)
        self.sep2 = QFrame()
        self.sep2.setFrameShape(QFrame.HLine)
        self.sep2.setFrameShadow(QFrame.Sunken)
        self.sep3 = QFrame()
        self.sep3.setFrameShape(QFrame.HLine)
        self.sep3.setFrameShadow(QFrame.Sunken)

        # Filename selection widgets.
        filenameLabel = QLabel("Filename:")
        self.filenameLineEdit = QLineEdit()
        self.filenameLineEdit.setReadOnly(True)
        self.browseButton = QPushButton(QIcon(":/images/open.png"), 
                                        "Br&owse")

        fileBrowseLayout = QHBoxLayout()
        fileBrowseLayout.addWidget(self.filenameLineEdit)
        fileBrowseLayout.addWidget(self.browseButton)

        self.filePreviewLabel = QLabel("File Preview:")
        self.textViewer = QPlainTextEdit()
        self.textViewer.setReadOnly(True)
        self.textViewer.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Lines skipped selection widgets.
        self.skipLinesLabel = \
            QLabel("N&umber of lines to skip before reading data:")
        self.skipLinesSpinBox = QSpinBox()
        self.skipLinesSpinBox.setMinimum(0)
        self.skipLinesSpinBox.setValue(1)
        self.skipLinesLabel.setBuddy(self.skipLinesSpinBox)

        skipLinesLayout = QHBoxLayout()
        skipLinesLayout.addWidget(self.skipLinesLabel)
        skipLinesLayout.addWidget(self.skipLinesSpinBox)
        skipLinesLayout.addStretch()

        # Validation widgets.
        validateLabel = QLabel("Click to validate: " )
        self.validateButton = QPushButton("&Validate")
        validateLayout = QHBoxLayout()
        validateLayout.addWidget(validateLabel)
        validateLayout.addWidget(self.validateButton)

        self.validationStatusLabel = QLabel("")
        self.validationStatusLabel.setWordWrap(True)
        font = self.validationStatusLabel.font()
        font.setPointSize(8)
        self.validationStatusLabel.setFont(font)

        # Load / Cancel buttons.
        self.loadButton = QPushButton("&Load")
        self.cancelButton = QPushButton("&Cancel")
        bottomButtonsLayout = QHBoxLayout()
        bottomButtonsLayout.addStretch()
        bottomButtonsLayout.addWidget(self.loadButton)
        bottomButtonsLayout.addWidget(self.cancelButton)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(descriptionLabel)
        layout.addWidget(fileInfoLabel)
        layout.addWidget(self.sep1)
        layout.addWidget(filenameLabel)
        layout.addLayout(fileBrowseLayout)
        layout.addWidget(self.filePreviewLabel)
        layout.addWidget(self.textViewer)
        layout.addLayout(skipLinesLayout)
        layout.addWidget(self.sep2)
        layout.addLayout(validateLayout)
        layout.addWidget(self.validationStatusLabel)
        layout.addWidget(self.sep3)
        layout.addLayout(bottomButtonsLayout)

        self.setLayout(layout)

        # Connect signals and slots.
        self.filenameLineEdit.textChanged.\
            connect(self.handleFilenameLineEditChanged)

        self.skipLinesSpinBox.valueChanged.\
            connect(self.handleSkipLinesSpinBoxChanged)

        self.browseButton.clicked.\
            connect(self.handleBrowseButtonClicked)

        self.validateButton.clicked.\
            connect(self.handleValidateButtonClicked)

        self.validationStateChanged.\
            connect(self.setLoadButtonEnabled)

        self.loadButton.clicked.\
            connect(self.loadButtonClicked)

        self.cancelButton.clicked.\
            connect(self.cancelButtonClicked)

    def setLoadButtonEnabled(self, flag):
        """Sets the 'Load' button to be enabled or disabled.
        Argument:
        flag - Boolean for whether or not the button should be enabled.
        """

        self.log.debug("setLoadButtonEnabled(flag={})".format(flag))

        if type(flag) == bool:
            self.loadButton.setEnabled(flag)


    def setBottomButtonsVisible(self, flag):
        """Sets the bottom buttons for accepting and canceling to 
        be visible or not.

        Arguments:
        flag  - Boolean value for setting the widgets visible.
        """

        self.log.debug("setBottomButtonsVisible(flag={})".format(flag))

        if type(flag) == bool:
            self.sep3.setVisible(flag)
            self.loadButton.setVisible(flag)
            self.cancelButton.setVisible(flag)


    def handleFilenameLineEditChanged(self, filename):
        """Sets that the information entered has not been validated.
        """

        self.log.debug("handleFilenameLineEditChanged(filename={})".\
            format(filename))

        if (self.validatedFlag != False):
            self.validatedFlag = False
            self.validationStateChanged.emit(self.validatedFlag)

        # Convert to Python string type.
        filename = str(filename)

        # Clear any text in the file preview viewer.
        self.textViewer.setPlainText("")

        # Clear any text set in the validationStatusLabel.
        self.validationStatusLabel.setText("")


        if filename != "":
            with io.open(filename, "r") as file:
                try:
                    fileText = file.read()
                    self.textViewer.setPlainText(fileText)
                except UnicodeDecodeError as e:
                    errStr = "Error while trying to read file '" + \
                        str(filename) + "'.  Only text files are supported!"
                    self.log.error(errStr)
                    QMessageBox.warning(None,
                                        "Error reading file",
                                        errStr)
                    self.filenameLineEdit.setText("")
                    self.textViewer.setPlainText("")
                except IOError as e:
                    errStr = "I/O Error while trying to read file '" + \
                        filename + "':" + os.linesep + e
                    self.log.error(errStr)
                    QMessageBox.warning(None,
                                        "Error reading file",
                                        errStr)
                    self.filenameLineEdit.setText("")
                    self.textViewer.setPlainText("")


    def handleSkipLinesSpinBoxChanged(self):
        """Sets that the information entered has not been validated.
        The validatedFlag is set to False if it is not already False.
        """

        self.log.debug("handleSkipLinesSpinBoxChanged()")

        if (self.validatedFlag != False):
            self.validatedFlag = False

            self.log.debug("Emitting validationStateChanged({})".\
                format(self.validatedFlag))

            self.validationStateChanged.emit(self.validatedFlag)

    def handleBrowseButtonClicked(self):
        """Opens a QFileDialog for selecting a file.  If a file is selected,
        self.filenameLineEdit will be populated with the selected filename.
        """

        self.log.debug("Entering handleBrowseButtonClicked()")

        # Create a file dialog.
        dialog = QFileDialog();

        # Setup file filters.
        csvTextFilesFilter = "Text files (*.txt)(*.txt)"
        allFilesFilter = "All files (*)(*)"
        #filters = QStringList()
        #filters.append(csvTextFilesFilter)
        #filters.append(allFilesFilter)
        filters = []
        filters.append(csvTextFilesFilter)
        filters.append(allFilesFilter)

        # Apply settings to the dialog.
        dialog.setFileMode(QFileDialog.ExistingFile);
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(csvTextFilesFilter)

        # Run the dialog.
        if dialog.exec_() == QDialog.Accepted:
            # Get the selected files. Note PyQt 4.7.5 returns QStringList
            # as a Python list of str objects now.  This is different from
            # the PyQt 4.6.
            selectedFiles = dialog.selectedFiles()
            if len(selectedFiles) != 0:
                # Set the QLineEdit with the filename.
                self.filenameLineEdit.setText(selectedFiles[0])

        self.log.debug("Leaving handleBrowseButtonClicked()")

    def handleValidateButtonClicked(self):
        """Opens the filename in self.filenameLineEdit and tries to validate
        that the file is a text file and has the expected fields.  
        It also populates the QPlainTextEdit with the data found in the file.

        This is also where the list of PriceBar objects are read and stored.
        """

        self.log.debug("handleValidateButtonClicked()")

        # Assume a valid file unless it's not.
        validFlag = True
        self.validationStatusLabel.setText("")

        # Create a new empty list for PriceBars.  
        # (We do this instead of emptying the list in case someone 
        # grabbed a copy of self.priceBars at some point earlier).
        # We will add to this list as we read valid lines in the file.
        self.priceBars = []

        # Get the fields from which we'll get info to read the file with.
        # Here casting to Python str type is required because 
        # QLineEdits return QString, not str.
        filename = str(self.filenameLineEdit.text())
        numLinesToSkip = self.skipLinesSpinBox.value()

        if filename == "":
            validFlag = False
            validationStr = "Validation failed because" + \
                " the filename cannot be empty."
            self.log.warn(validationStr)
            validationStr = self.toRedString(validationStr)
            self.validationStatusLabel.setText(validationStr)
        else:
            with io.open(filename, "r") as file:
                try:
                    # Go through each line of the file.
                    i = 0
                    for line in file:
                        i += 1

                        # Skip over empty lines and lines before 
                        # line number 'numLinesToSkip'.
                        if i > numLinesToSkip and line.strip() != "":
                            (lineValid, reason) = self.validateLine(line)
                            if lineValid == False:
                                # Invalid line in the file.
                                validFlag = False
                                validationStr = \
                                    "Validation failed on line " + \
                                    "{} because: {}".format(i, reason)
                                self.log.warn(validationStr)
                                validationStr = self.toRedString(validationStr)
                                self.validationStatusLabel.\
                                    setText(validationStr)
                                break
                            else:
                                # Valid line in the file.

                                # Create a PriceBar and append it to 
                                # the PriceBar list.
                                pb = self.convertLineToPriceBar(line)
                                self.priceBars.append(pb)

                except IOError as e:
                    errStr = "I/O Error while trying to read file '" + \
                        filename + "':" + os.linesep + e
                    self.log.error(errStr)
                    QMessageBox.warning(None, "Error reading file", errStr)
                    validationStr = \
                        "Validation failed due to a I/O error.  " + \
                        "Please try again later."
                    self.log.error(validationStr)
                    validationStr = self.toRedString(validationStr)
                    self.validationStatusLabel.setText(validationStr)

        # If the validFlag is still True, then allow the user to 
        # click the 'Next' button.
        if validFlag == True:
            infoStr = "Validated data file {}".format(filename)
            self.log.info(infoStr)
            validationStr = self.toGreenString("Validated")
            self.validationStatusLabel.setText(validationStr)
            if self.validatedFlag == False:
                self.validatedFlag = True
                self.validationStateChanged.emit(self.validatedFlag)

        self.log.debug("Leaving handleValidateButtonClicked()")

    def toRedString(self, string):
        """Wraps the input str with HTML tags to turn it red."""

        return "<font color=\"red\">" + string + "</font>"

    def toGreenString(self, string):
        """Wraps the input str with HTML tags to turn it green."""

        return "<font color=\"green\">" + string + "</font>"


    def validateLine(self, line):
        """Returns a tuple of (boolean, str) that represents if the line
        of text was parsed to be a valid CSV data line.

        If the line of text is valid, the boolean part of the tuple 
        returned is True and the string is returned is empty.

        If the line of text is found to be not valid, the tuple returns
        False and a string explaining why the validation failed.

        The expected format of 'line' is:
        <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>
        """

        self.log.debug("validateLine(line='{}')".format(line))

        # Check the number of fields.
        fields = line.split(",")
        numFieldsExpected = 7
        if len(fields) != numFieldsExpected:
            return (False, "Line does not have {} data fields".\
                    format(numFieldsExpected))

        dateStr = fields[0] 
        openStr = fields[1]
        highStr = fields[2]
        lowStr = fields[3]
        closeStr = fields[4]
        volumeStr = fields[5]
        openIntStr = fields[6]

        dateStrSplit = dateStr.split("/")
        if len(dateStrSplit) != 3:
            return (False, "Format of the date was not MM/DD/YYYY")

        monthStr = dateStrSplit[0]
        dayStr = dateStrSplit[1]
        yearStr = dateStrSplit[2]

        if len(monthStr) != 2:
            return (False, "Month in the date is not two characters long")
        if len(dayStr) != 2:
            return (False, "Day in the date is not two characters long")
        if len(yearStr) != 4:
            return (False, "Year in the date is not four characters long")

        try:
            monthInt = int(monthStr)
            if monthInt < 1 or monthInt > 12:
                return (False, "Month in the date is not between 1 and 12")
        except ValueError as e:
            return (False, "Month in the date is not a number")

        try:
            dayInt = int(dayStr)
            if dayInt < 1 or dayInt > 31:
                return (False, "Day in the date is not between 1 and 31")
        except ValueError as e:
            return (False, "Day in the date is not a number")

        try:
            yearInt = int(yearStr)
        except ValueError as e:
            return (False, "Year in the date is not a number")
                
        try:
            openFloat = float(openStr)
        except ValueError as e:
            return (False, "OpenPrice is not a number")

        try:
            highFloat = float(highStr)
        except ValueError as e:
            return (False, "HighPrice is not a number")

        try:
            lowFloat = float(lowStr)
        except ValueError as e:
            return (False, "LowPrice is not a number")

        try:
            closeFloat = float(closeStr)
        except ValueError as e:
            return (False, "ClosePrice is not a number")

        try:
            volumeFloat = float(volumeStr)
        except ValueError as e:
            return (False, "Volume is not a number")

        try:
            openIntFloat = float(openIntStr)
        except ValueError as e:
            return (False, "OpenInterest is not a number")


        # If it got this far without returning, then everything 
        # checked out fine.
        return (True, "")


    def convertLineToPriceBar(self, line):
        """Convert a line of text from a CSV file to a PriceBar.

        The expected format of 'line' is:
        <MM/DD/YYYY>,<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>,<Volume>,<OpenInterest>

        Returns:
        PriceBar object from the line of text.  If the text was incorrectly
        formatted, then None is returned.  
        """

        self.log.debug("convertLineToPriceBar(line='{}')".format(line))

        # Return value.
        retVal = None

        # Do validation on the line first.
        (validFlag, reasonStr) = self.validateLine(line)

        if validFlag == False:
            self.log.debug("Line conversion failed because: {}" + reasonStr)
            retVal = None
        else:
            # Although we already validated the line, we wrap the parsing 
            # here in a try block just in case something unexpected 
            # was thrown at us.
            try:
                fields = line.split(",")

                dateStr = fields[0] 
                openPrice = float(fields[1])
                highPrice = float(fields[2])
                lowPrice = float(fields[3])
                closePrice = float(fields[4])
                volume = float(fields[5])
                openInt = float(fields[6])

                dateStrSplit = dateStr.split("/")
                month = int(dateStrSplit[0])
                day = int(dateStrSplit[1])
                year = int(dateStrSplit[2])

                # Datetime object is assumed to be in UTC, and the
                # timestamps will have a midnight time (i.e., the 
                # very start of the day).
                timestamp = datetime.datetime(year, month, day, 
                                                tzinfo=pytz.utc)

                # Create the PriceBar with the parsed data.
                retVal = PriceBar(timestamp, 
                                  open=openPrice,
                                  high=highPrice,
                                  low=lowPrice,
                                  close=closePrice,
                                  oi=openInt,
                                  vol=volume)

            except IndexError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an IndexError: " + e)
            except UnicodeDecodeError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an UnicodeDecodeError: " + e)
            except ValueError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an ValueError: " + e)
            except TypeError as e:
                self.log.error("While converting line of text to " + \
                               "PriceBar, got an TypeError: " + e)

        # Return the PriceBar created (or None if an error occurred).
        return retVal


    def isValidated(self):
        """Returns True if validation succeeded, otherwise returns False.
        This function overrides the QWizardPage.isComplete() virtual
        function.
        """

        return self.validatedFlag

    def getPriceBars(self):
        """Returns a list of PriceBars if the opened file has been validated
        successfully (i.e., isValidated() returns True).  If the opened file
        failed validation, this function will return an empty list.
        """
        
        if isValidated():
            self.log.debug("getPriceBars(): returning list of PriceBars " + \
                           "with length {}".format(len(self.priceBars)))
            return self.priceBars
        else:
            self.log.debug("getPriceBars(): File was not validated. " + \
                           "Returning an empty list.")
            return []

class LocationTimezoneEditWidget(QWidget):
    """QWidget for searching for a location and timezone."""

    # Signal emitted when the Okay button is clicked.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.LocationTimezoneEditWidget")

        self.log.debug("Checking for internet connection to web service.")

        # Flag to determine if we have an internet connection and can reach
        # GeoNames web service.
        self.geoNamesEnabled = GeoNames.canConnectToWebService()

        if self.geoNamesEnabled:
            self.log.debug("Internet connection to the web service is " + \
                           "available.")
        else:
            self.log.info("Internet connection to the web service is " + \
                          "not available.")

        # Create the contents.

        # Informational labels.
        descriptionLabel = \
            QLabel("Enter a search phrase for the location." + \
                   os.linesep + os.linesep + \
                   "Timezone information will be " + \
                   "determined from the selected search result." + \
                   os.linesep)
        descriptionLabel.setWordWrap(True)

        # Label that is displayed if we can't get to GeoNames.
        geoNamesStatus = \
            "<font color=\"red\">" + \
            "Search functionality is disabled due to failed " + \
            "network connection to GeoNames web service." + \
            "</font>"
        geoNamesStatusLabel = QLabel(geoNamesStatus)
        geoNamesStatusLabel.setWordWrap(True)

        # Frame as a separator.
        self.sep1 = QFrame()
        self.sep1.setFrameShape(QFrame.HLine)
        self.sep1.setFrameShadow(QFrame.Sunken)
        self.sep2 = QFrame()
        self.sep2.setFrameShape(QFrame.HLine)
        self.sep2.setFrameShadow(QFrame.Sunken)
        self.sep3 = QFrame()
        self.sep3.setFrameShape(QFrame.HLine)
        self.sep3.setFrameShadow(QFrame.Sunken)

        # Location search widgets.
        searchLocationLabel = QLabel("Search for &location:")
        self.searchLocationLineEdit = QLineEdit()
        searchLocationLabel.setBuddy(self.searchLocationLineEdit)
        self.searchButton = QPushButton("&Search")
        self.searchLocationLineEdit.returnPressed.\
            connect(self.searchButton.click)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchLocationLineEdit)
        searchLayout.addWidget(self.searchButton)

        # Results selection widgets.
        resultsLabel = QLabel("Search &results:")
        self.resultsComboBox = QComboBox()
        self.resultsComboBox.setDuplicatesEnabled(True)
        resultsLabel.setBuddy(self.resultsComboBox)
        # Disable the QComboBox until the results come in.
        self.resultsComboBox.setEnabled(False)

        # Timezone widgets.
        timezoneLabel = QLabel("Timezone name:")
        self.timezoneComboBox = QComboBox()
        self.timezoneComboBox.addItems(pytz.common_timezones)

        # If GeoNames is not enabled, then disable some widgets.
        if self.geoNamesEnabled == False:
            self.searchLocationLineEdit.setEnabled(False)
            self.searchButton.setEnabled(False)
            self.resultsComboBox.setEnabled(False)

        # Okay / Cancel buttons.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        bottomButtonsLayout = QHBoxLayout()
        bottomButtonsLayout.addStretch()
        bottomButtonsLayout.addWidget(self.okayButton)
        bottomButtonsLayout.addWidget(self.cancelButton)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(descriptionLabel)
        if self.geoNamesEnabled == False:
            layout.addWidget(geoNamesStatusLabel)
        layout.addWidget(self.sep1)
        layout.addWidget(searchLocationLabel)
        layout.addLayout(searchLayout)
        layout.addWidget(resultsLabel)
        layout.addWidget(self.resultsComboBox)
        layout.addWidget(self.sep2)
        layout.addWidget(timezoneLabel)
        layout.addWidget(self.timezoneComboBox)
        layout.addWidget(self.sep3)
        layout.addLayout(bottomButtonsLayout)
        self.setLayout(layout)

        # Connect signals and slots.
        self.searchButton.clicked.connect(self.doLocationSearch)
        self.resultsComboBox.currentIndexChanged[int].\
            connect(self.handleSearchResultSelected)
        self.okayButton.clicked.connect(self.okayButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

    def setBottomButtonsVisible(self, flag):
        """Sets the bottom buttons for accepting and canceling to 
        be visible or not.

        Arguments:
        flag  - Boolean value for setting the widgets visible.
        """

        self.log.debug("setBottomButtonsVisible(flag={})".format(flag))

        if type(flag) == bool:
            self.sep3.setVisible(flag)
            self.okayButton.setVisible(flag)
            self.cancelButton.setVisible(flag)

    def doLocationSearch(self):
        """Uses GeoNames to do a lookup of a location based on the search
        string in self.searchLocationLineEdit.  Results that are returned are
        populated in the self.resultsComboBox.  If there is any error in doing
        the search, a pop-up dialog is displayed with the error description, 
        and the error is logged.
        """

        self.log.debug("Entered doLocationSearch()")

        searchString = str(self.searchLocationLineEdit.text())
        self.log.debug("searchString=" + searchString)

        geoInfos = GeoNames.search(searchStr=searchString, 
                                   countryBias="")

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))


        # Prepare the self.resultsComboBox if there are new results to 
        # populate it with.
        if len(geoInfos) > 0:
            self.log.debug("Clearing resultsComboBox...")
            # Clear the QComboBox of search results.
            self.resultsComboBox.clear()

            self.log.debug("Enabling resultsComboBox...")
            # If the self.resultsComboBox is disabled, then enable it.
            if self.resultsComboBox.isEnabled() == False:
                self.resultsComboBox.setEnabled(True)

        # Populate the self.resultsComboBox.
        for i in range(len(geoInfos)):
            geoInfo = geoInfos[i]

            displayStr = geoInfo.name
            if geoInfo.adminName1 != None and geoInfo.adminName1 != "":
                displayStr += ", " + geoInfo.adminName1
            if geoInfo.countryName != None and geoInfo.countryName != "":
                displayStr += ", " + geoInfo.countryName
            displayStr += " ({}, {})".format(geoInfo.latitudeStr(), 
                                             geoInfo.longitudeStr()) 
            if geoInfo.population != None and geoInfo.population != 0:
                displayStr += " (pop. {})".format(geoInfo.population)

            self.log.debug("Display name is: {}".format(displayStr))
            self.resultsComboBox.addItem(displayStr, geoInfo)

        self.log.debug("Leaving doLocationSearch()")


    def handleSearchResultSelected(self, index):
        """Determines which search result was selected, and populates
        the timezone QComboBox for that location.
        """

        self.log.debug("Entered handleSearchResultSelected(index={})".\
                       format(index))

        # Only makes sense if the index selected is valid.  
        # Theoretically index should only be -1 on the very first load.
        if index == -1:
            return

        # This part is a bit tricky because PyQt has been changing how
        # QVariant data is stored and converted in combo boxes.
        # So here we do some extra checks before casting.
        maybeQVariant = self.resultsComboBox.itemData(index)
        geoInfo = GeoInfo()
        if isinstance(maybeQVariant, QVariant):
            # This is really a QVariant, so use toPyObject().
            geoInfo = maybeQVariant.toPyObject()
        else:
            # PyQt converted it already for us.
            geoInfo = maybeQVariant

        # Make sure geoInfo is not None.  We need it in order to get the
        # timezone information.  It should never be None.
        if geoInfo == None:
            self.log.error("GeoInfo is None, when it should have " + \
                           "been an actual object!")
            return

        # Try to use the timezone in geoInfo first.  If that doesn't 
        # work, then the do a query for the timezone using the latitude and
        # longitude.
        if geoInfo.timezone != None and geoInfo.timezone != "":
            index = self.timezoneComboBox.findText(geoInfo.timezone)
            if index != -1:
                self.timezoneComboBox.setCurrentIndex(index)
            else:
                errStr = "Couldn't find timezone '" + geoInfo.timezone + \
                     "' returned by GeoNames in the pytz " + \
                     "list of timezones."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)
        else:
            # Try to do the query ourselves from GeoNames.getTimezone().
            timezone = None
            try:
                timezone = GeoNames.getTimezone(geoInfo.latitude,
                                                geoInfo.longitude)
            except urllib.error.URLError as e:
                errStr = "Couldn't perform the search because " + \
                         "of the following error: " + e.reason.strerror
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)
                return

            if timezone != None and timezone != "":
                index = self.timezoneComboBox.findText(geoInfo.timezone)
                if index != -1:
                    self.timezoneComboBox.setCurrentIndex(index)
                else:
                    errStr = "Couldn't find timezone '" + timezone + \
                         "' returned by GeoNames in the pytz " + \
                         "list of timezones."
                    self.log.error(errStr)
                    QMessageBox.warning(None, "Error", errStr)
            else:
                errStr = "GeoNames returned a null or empty timezone."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

        self.log.debug("Leaving handleSearchResultSelected()")


    def getTimezoneStr(self):
        """Returns the timezone selected in the QComboBox."""

        return str(self.timezoneComboBox.currentText())

class BirthInfoEditWidget(QWidget):
    """QWidget for editing a birth time or defining a new birth time."""

    # Signal emitted when the Okay button is clicked and 
    # validation succeeded.
    okayButtonClicked = QtCore.pyqtSignal()

    # Signal emitted when the Cancel button is clicked.
    cancelButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.BirthInfoEditWidget")

        # Flag to determine if we have an internet connection and can reach
        # GeoNames web service.
        self.geoNamesEnabled = GeoNames.canConnectToWebService()

        if self.geoNamesEnabled:
            self.log.debug("Internet connection to GeoNames web service " + \
                           "is available.")
        else:
            self.log.info("Internet connection to GeoNames web service " + \
                          "is not available.")

        # Spacing amount for indenting inwards for some widgets.
        self.indentSpacing = 60

        # Birth time widgets.
        self.monthLabel = QLabel("&Month")
        self.monthLabel.setAlignment(Qt.AlignCenter)
        self.dayLabel = QLabel("&Day")
        self.dayLabel.setAlignment(Qt.AlignCenter)
        self.yearLabel = QLabel("&Year")
        self.yearLabel.setAlignment(Qt.AlignCenter)
        self.calendarLabel = QLabel("Calendar")
        self.calendarLabel.setAlignment(Qt.AlignCenter)
        self.hourLabel = QLabel("&Hour (0-23)")
        self.hourLabel.setAlignment(Qt.AlignCenter)
        self.minuteLabel = QLabel("M&inute (0-59)")
        self.minuteLabel.setAlignment(Qt.AlignCenter)
        self.secondLabel = QLabel("Second (0-59)")
        self.secondLabel.setAlignment(Qt.AlignCenter)
        self.monthSpinBox = QSpinBox()
        self.monthSpinBox.setMinimum(1)
        self.monthSpinBox.setMaximum(12)
        self.daySpinBox = QSpinBox()
        self.daySpinBox.setMinimum(1)
        self.daySpinBox.setMaximum(31)
        self.yearSpinBox = QSpinBox()
        # Setting minimum year to 2, because below that, the pytz localize()
        # function can cause an OverflowError exception to be raised.
        self.yearSpinBox.setMinimum(2)
        # Maximum year must be set, otherwise the spinbox defaults it to 100.
        self.yearSpinBox.setMaximum(9999)
        self.calendarComboBox = QComboBox()
        self.calendarComboBox.addItem("Gregorian")
        self.calendarComboBox.addItem("Julian")
        self.calendarComboBox.setCurrentIndex(0)
        self.hourSpinBox = QSpinBox()
        self.hourSpinBox.setMinimum(0)
        self.hourSpinBox.setMaximum(23)
        self.minuteSpinBox = QSpinBox()
        self.minuteSpinBox.setMinimum(0)
        self.minuteSpinBox.setMaximum(59)
        self.secondSpinBox = QSpinBox()
        self.secondSpinBox.setMinimum(0)
        self.secondSpinBox.setMaximum(59)

        # Set buddies for birth time widgets.
        self.monthLabel.setBuddy(self.monthSpinBox)
        self.dayLabel.setBuddy(self.daySpinBox)
        self.yearLabel.setBuddy(self.yearSpinBox)
        self.hourLabel.setBuddy(self.hourSpinBox)
        self.minuteLabel.setBuddy(self.minuteSpinBox)

        # Birth time layout.
        self.birthTimeLayout = QGridLayout()
        self.birthTimeLayout.addWidget(self.monthLabel, 0, 0)
        self.birthTimeLayout.addWidget(self.dayLabel, 0, 1)
        self.birthTimeLayout.addWidget(self.yearLabel, 0, 2)
        self.birthTimeLayout.addWidget(self.calendarLabel, 0, 3)
        self.birthTimeLayout.addWidget(self.monthSpinBox, 1, 0)
        self.birthTimeLayout.addWidget(self.daySpinBox, 1, 1)
        self.birthTimeLayout.addWidget(self.yearSpinBox, 1, 2)
        self.birthTimeLayout.addWidget(self.calendarComboBox, 1, 3)
        self.birthTimeLayout.addWidget(self.hourLabel, 2, 0)
        self.birthTimeLayout.addWidget(self.minuteLabel, 2, 1)
        self.birthTimeLayout.addWidget(self.secondLabel, 2, 2)
        self.birthTimeLayout.addWidget(self.hourSpinBox, 3, 0)
        self.birthTimeLayout.addWidget(self.minuteSpinBox, 3, 1)
        self.birthTimeLayout.addWidget(self.secondSpinBox, 3, 2)

        self.birthTimeGroupBox = QGroupBox("Birth Time")
        self.birthTimeGroupBox.setLayout(self.birthTimeLayout)

        # Birth place widgets.
        self.cityNameLabel = QLabel("City N&ame")
        self.cityNameLabel.setAlignment(Qt.AlignCenter)
        self.cityNameLineEdit = QLineEdit()
        self.cityNameLabel.setBuddy(self.cityNameLineEdit)
        self.searchInAllCountriesButton = \
            QPushButton("&Search in all countries")
        self.searchInUsaButton = QPushButton("Search in USA")
        self.cityNameLineEdit.returnPressed.\
            connect(self.searchInAllCountriesButton.click)
        self.countriesComboBox = QComboBox()
        self.countriesComboBox.addItem("", "")
        self.countriesComboBox.addItem("Afghanistan", "AF")
        self.countriesComboBox.addItem("Åland Islands", "AX")
        self.countriesComboBox.addItem("Albania", "AL")
        self.countriesComboBox.addItem("Algeria", "DZ")
        self.countriesComboBox.addItem("American Samoa", "AS")
        self.countriesComboBox.addItem("Andorra", "AD")
        self.countriesComboBox.addItem("Angola", "AO")
        self.countriesComboBox.addItem("Anguilla", "AI")
        self.countriesComboBox.addItem("Antarctica", "AQ")
        self.countriesComboBox.addItem("Antigua and Barbuda", "AG")
        self.countriesComboBox.addItem("Argentina", "AR")
        self.countriesComboBox.addItem("Armenia", "AM")
        self.countriesComboBox.addItem("Aruba", "AW")
        self.countriesComboBox.addItem("Australia", "AU")
        self.countriesComboBox.addItem("Austria", "AT")
        self.countriesComboBox.addItem("Azerbaijan", "AZ")
        self.countriesComboBox.addItem("Bahamas", "BS")
        self.countriesComboBox.addItem("Bahrain", "BH")
        self.countriesComboBox.addItem("Bangladesh", "BD")
        self.countriesComboBox.addItem("Barbados", "BB")
        self.countriesComboBox.addItem("Belarus", "BY")
        self.countriesComboBox.addItem("Belgium", "BE")
        self.countriesComboBox.addItem("Belize", "BZ")
        self.countriesComboBox.addItem("Benin", "BJ")
        self.countriesComboBox.addItem("Bermuda", "BM")
        self.countriesComboBox.addItem("Bhutan", "BT")
        self.countriesComboBox.addItem("Bolivia", "BO")
        self.countriesComboBox.addItem("Bosnia and Herzegovina", "BA")
        self.countriesComboBox.addItem("Botswana", "BW")
        self.countriesComboBox.addItem("Bouvet Island", "BV")
        self.countriesComboBox.addItem("Brazil", "BR")
        self.countriesComboBox.addItem("British Indian Ocean Territory", "IO")
        self.countriesComboBox.addItem("British Virgin Islands", "VG")
        self.countriesComboBox.addItem("Brunei", "BN")
        self.countriesComboBox.addItem("Bulgaria", "BG")
        self.countriesComboBox.addItem("Burkina Faso", "BF")
        self.countriesComboBox.addItem("Burundi", "BI")
        self.countriesComboBox.addItem("Cambodia", "KH")
        self.countriesComboBox.addItem("Cameroon", "CM")
        self.countriesComboBox.addItem("Canada", "CA")
        self.countriesComboBox.addItem("Cape Verde", "CV")
        self.countriesComboBox.addItem("Cayman Islands", "KY")
        self.countriesComboBox.addItem("Central African Republic", "CF")
        self.countriesComboBox.addItem("Chad", "TD")
        self.countriesComboBox.addItem("Chile", "CL")
        self.countriesComboBox.addItem("China", "CN")
        self.countriesComboBox.addItem("Christmas Island", "CX")
        self.countriesComboBox.addItem("Cocos [Keeling] Islands", "CC")
        self.countriesComboBox.addItem("Colombia", "CO")
        self.countriesComboBox.addItem("Comoros", "KM")
        self.countriesComboBox.addItem("Congo [DRC]", "CD")
        self.countriesComboBox.addItem("Congo [Republic]", "CG")
        self.countriesComboBox.addItem("Cook Islands", "CK")
        self.countriesComboBox.addItem("Costa Rica", "CR")
        self.countriesComboBox.addItem("Croatia", "HR")
        self.countriesComboBox.addItem("Cuba", "CU")
        self.countriesComboBox.addItem("Cyprus", "CY")
        self.countriesComboBox.addItem("Czech Republic", "CZ")
        self.countriesComboBox.addItem("Denmark", "DK")
        self.countriesComboBox.addItem("Djibouti", "DJ")
        self.countriesComboBox.addItem("Dominica", "DM")
        self.countriesComboBox.addItem("Dominican Republic", "DO")
        self.countriesComboBox.addItem("East Timor", "TL")
        self.countriesComboBox.addItem("Ecuador", "EC")
        self.countriesComboBox.addItem("Egypt", "EG")
        self.countriesComboBox.addItem("El Salvador", "SV")
        self.countriesComboBox.addItem("Equatorial Guinea", "GQ")
        self.countriesComboBox.addItem("Eritrea", "ER")
        self.countriesComboBox.addItem("Estonia", "EE")
        self.countriesComboBox.addItem("Ethiopia", "ET")
        self.countriesComboBox.addItem("Falkland Islands", "FK")
        self.countriesComboBox.addItem("Faroe Islands", "FO")
        self.countriesComboBox.addItem("Fiji", "FJ")
        self.countriesComboBox.addItem("Finland", "FI")
        self.countriesComboBox.addItem("France", "FR")
        self.countriesComboBox.addItem("French Guiana", "GF")
        self.countriesComboBox.addItem("French Polynesia", "PF")
        self.countriesComboBox.addItem("French Southern Territories", "TF")
        self.countriesComboBox.addItem("Gabon", "GA")
        self.countriesComboBox.addItem("Gambia", "GM")
        self.countriesComboBox.addItem("Georgia", "GE")
        self.countriesComboBox.addItem("Germany", "DE")
        self.countriesComboBox.addItem("Ghana", "GH")
        self.countriesComboBox.addItem("Gibraltar", "GI")
        self.countriesComboBox.addItem("Greece", "GR")
        self.countriesComboBox.addItem("Greenland", "GL")
        self.countriesComboBox.addItem("Grenada", "GD")
        self.countriesComboBox.addItem("Guadeloupe", "GP")
        self.countriesComboBox.addItem("Guam", "GU")
        self.countriesComboBox.addItem("Guatemala", "GT")
        self.countriesComboBox.addItem("Guernsey", "GG")
        self.countriesComboBox.addItem("Guinea-Bissau", "GW")
        self.countriesComboBox.addItem("Guinea", "GN")
        self.countriesComboBox.addItem("Guyana", "GY")
        self.countriesComboBox.addItem("Haiti", "HT")
        self.countriesComboBox.addItem("Heard Island and McDonald Islands", "HM")
        self.countriesComboBox.addItem("Honduras", "HN")
        self.countriesComboBox.addItem("Hong Kong", "HK")
        self.countriesComboBox.addItem("Hungary", "HU")
        self.countriesComboBox.addItem("Iceland", "IS")
        self.countriesComboBox.addItem("India", "IN")
        self.countriesComboBox.addItem("Indonesia", "ID")
        self.countriesComboBox.addItem("Iran", "IR")
        self.countriesComboBox.addItem("Iraq", "IQ")
        self.countriesComboBox.addItem("Ireland", "IE")
        self.countriesComboBox.addItem("Isle of Man", "IM")
        self.countriesComboBox.addItem("Israel", "IL")
        self.countriesComboBox.addItem("Italy", "IT")
        self.countriesComboBox.addItem("Ivory Coast", "CI")
        self.countriesComboBox.addItem("Jamaica", "JM")
        self.countriesComboBox.addItem("Japan", "JP")
        self.countriesComboBox.addItem("Jersey", "JE")
        self.countriesComboBox.addItem("Jordan", "JO")
        self.countriesComboBox.addItem("Kazakhstan", "KZ")
        self.countriesComboBox.addItem("Kenya", "KE")
        self.countriesComboBox.addItem("Kiribati", "KI")
        self.countriesComboBox.addItem("Kosovo", "XK")
        self.countriesComboBox.addItem("Kuwait", "KW")
        self.countriesComboBox.addItem("Kyrgyzstan", "KG")
        self.countriesComboBox.addItem("Laos", "LA")
        self.countriesComboBox.addItem("Latvia", "LV")
        self.countriesComboBox.addItem("Lebanon", "LB")
        self.countriesComboBox.addItem("Lesotho", "LS")
        self.countriesComboBox.addItem("Liberia", "LR")
        self.countriesComboBox.addItem("Libya", "LY")
        self.countriesComboBox.addItem("Liechtenstein", "LI")
        self.countriesComboBox.addItem("Lithuania", "LT")
        self.countriesComboBox.addItem("Luxembourg", "LU")
        self.countriesComboBox.addItem("Macau", "MO")
        self.countriesComboBox.addItem("Macedonia", "MK")
        self.countriesComboBox.addItem("Madagascar", "MG")
        self.countriesComboBox.addItem("Malawi", "MW")
        self.countriesComboBox.addItem("Malaysia", "MY")
        self.countriesComboBox.addItem("Maldives", "MV")
        self.countriesComboBox.addItem("Mali", "ML")
        self.countriesComboBox.addItem("Malta", "MT")
        self.countriesComboBox.addItem("Marshall Islands", "MH")
        self.countriesComboBox.addItem("Martinique", "MQ")
        self.countriesComboBox.addItem("Mauritania", "MR")
        self.countriesComboBox.addItem("Mauritius", "MU")
        self.countriesComboBox.addItem("Mayotte", "YT")
        self.countriesComboBox.addItem("Mexico", "MX")
        self.countriesComboBox.addItem("Micronesia", "FM")
        self.countriesComboBox.addItem("Moldova", "MD")
        self.countriesComboBox.addItem("Monaco", "MC")
        self.countriesComboBox.addItem("Mongolia", "MN")
        self.countriesComboBox.addItem("Montenegro", "ME")
        self.countriesComboBox.addItem("Montserrat", "MS")
        self.countriesComboBox.addItem("Morocco", "MA")
        self.countriesComboBox.addItem("Mozambique", "MZ")
        self.countriesComboBox.addItem("Myanmar [Burma]", "MM")
        self.countriesComboBox.addItem("Namibia", "NA")
        self.countriesComboBox.addItem("Nauru", "NR")
        self.countriesComboBox.addItem("Nepal", "NP")
        self.countriesComboBox.addItem("Netherlands Antilles", "AN")
        self.countriesComboBox.addItem("Netherlands", "NL")
        self.countriesComboBox.addItem("New Caledonia", "NC")
        self.countriesComboBox.addItem("New Zealand", "NZ")
        self.countriesComboBox.addItem("Nicaragua", "NI")
        self.countriesComboBox.addItem("Nigeria", "NG")
        self.countriesComboBox.addItem("Niger", "NE")
        self.countriesComboBox.addItem("Niue", "NU")
        self.countriesComboBox.addItem("Norfolk Island", "NF")
        self.countriesComboBox.addItem("Northern Mariana Islands", "MP")
        self.countriesComboBox.addItem("North Korea", "KP")
        self.countriesComboBox.addItem("Norway", "NO")
        self.countriesComboBox.addItem("Oman", "OM")
        self.countriesComboBox.addItem("Pakistan", "PK")
        self.countriesComboBox.addItem("Palau", "PW")
        self.countriesComboBox.addItem("Palestinian Territories", "PS")
        self.countriesComboBox.addItem("Panama", "PA")
        self.countriesComboBox.addItem("Papua New Guinea", "PG")
        self.countriesComboBox.addItem("Paraguay", "PY")
        self.countriesComboBox.addItem("Peru", "PE")
        self.countriesComboBox.addItem("Philippines", "PH")
        self.countriesComboBox.addItem("Pitcairn Islands", "PN")
        self.countriesComboBox.addItem("Poland", "PL")
        self.countriesComboBox.addItem("Portugal", "PT")
        self.countriesComboBox.addItem("Puerto Rico", "PR")
        self.countriesComboBox.addItem("Qatar", "QA")
        self.countriesComboBox.addItem("Réunion", "RE")
        self.countriesComboBox.addItem("Romania", "RO")
        self.countriesComboBox.addItem("Russia", "RU")
        self.countriesComboBox.addItem("Rwanda", "RW")
        self.countriesComboBox.addItem("Saint Barthélemy", "BL")
        self.countriesComboBox.addItem("Saint Helena", "SH")
        self.countriesComboBox.addItem("Saint Kitts and Nevis", "KN")
        self.countriesComboBox.addItem("Saint Lucia", "LC")
        self.countriesComboBox.addItem("Saint Martin", "MF")
        self.countriesComboBox.addItem("Saint Pierre and Miquelon", "PM")
        self.countriesComboBox.addItem("Saint Vincent and the Grenadines", "VC")
        self.countriesComboBox.addItem("Samoa", "WS")
        self.countriesComboBox.addItem("San Marino", "SM")
        self.countriesComboBox.addItem("São Tomé and Príncipe", "ST")
        self.countriesComboBox.addItem("Saudi Arabia", "SA")
        self.countriesComboBox.addItem("Senegal", "SN")
        self.countriesComboBox.addItem("Serbia and Montenegro", "CS")
        self.countriesComboBox.addItem("Serbia", "RS")
        self.countriesComboBox.addItem("Seychelles", "SC")
        self.countriesComboBox.addItem("Sierra Leone", "SL")
        self.countriesComboBox.addItem("Singapore", "SG")
        self.countriesComboBox.addItem("Slovakia", "SK")
        self.countriesComboBox.addItem("Slovenia", "SI")
        self.countriesComboBox.addItem("Solomon Islands", "SB")
        self.countriesComboBox.addItem("Somalia", "SO")
        self.countriesComboBox.addItem("South Africa", "ZA")
        self.countriesComboBox.addItem("South Georgia and the South Sandwich Islands", "GS")
        self.countriesComboBox.addItem("South Korea", "KR")
        self.countriesComboBox.addItem("Spain", "ES")
        self.countriesComboBox.addItem("Sri Lanka", "LK")
        self.countriesComboBox.addItem("Sudan", "SD")
        self.countriesComboBox.addItem("Suriname", "SR")
        self.countriesComboBox.addItem("Svalbard and Jan Mayen", "SJ")
        self.countriesComboBox.addItem("Swaziland", "SZ")
        self.countriesComboBox.addItem("Sweden", "SE")
        self.countriesComboBox.addItem("Switzerland", "CH")
        self.countriesComboBox.addItem("Syria", "SY")
        self.countriesComboBox.addItem("Taiwan", "TW")
        self.countriesComboBox.addItem("Tajikistan", "TJ")
        self.countriesComboBox.addItem("Tanzania", "TZ")
        self.countriesComboBox.addItem("Thailand", "TH")
        self.countriesComboBox.addItem("Togo", "TG")
        self.countriesComboBox.addItem("Tokelau", "TK")
        self.countriesComboBox.addItem("Tonga", "TO")
        self.countriesComboBox.addItem("Trinidad and Tobago", "TT")
        self.countriesComboBox.addItem("Tunisia", "TN")
        self.countriesComboBox.addItem("Turkey", "TR")
        self.countriesComboBox.addItem("Turkmenistan", "TM")
        self.countriesComboBox.addItem("Turks and Caicos Islands", "TC")
        self.countriesComboBox.addItem("Tuvalu", "TV")
        self.countriesComboBox.addItem("Uganda", "UG")
        self.countriesComboBox.addItem("Ukraine", "UA")
        self.countriesComboBox.addItem("United Arab Emirates", "AE")
        self.countriesComboBox.addItem("United Kingdom", "GB")
        self.countriesComboBox.addItem("United States", "US")
        self.countriesComboBox.addItem("Uruguay", "UY")
        self.countriesComboBox.addItem("U.S. Minor Outlying Islands", "UM")
        self.countriesComboBox.addItem("U.S. Virgin Islands", "VI")
        self.countriesComboBox.addItem("Uzbekistan", "UZ")
        self.countriesComboBox.addItem("Vanuatu", "VU")
        self.countriesComboBox.addItem("Vatican City", "VA")
        self.countriesComboBox.addItem("Venezuela", "VE")
        self.countriesComboBox.addItem("Vietnam", "VN")
        self.countriesComboBox.addItem("Wallis and Futuna", "WF")
        self.countriesComboBox.addItem("Western Sahara", "EH")
        self.countriesComboBox.addItem("Yemen", "YE")
        self.countriesComboBox.addItem("Zambia", "ZM")
        self.countriesComboBox.addItem("Zimbabwe", "ZW")

        self.searchInSpecifiedCountryButton = \
            QPushButton("Search in specified country")

        self.searchLocationLayout = QGridLayout()
        self.searchLocationLayout.addWidget(self.cityNameLabel, 0, 0)
        self.searchLocationLayout.addWidget(self.cityNameLineEdit, 1, 0)
        self.searchLocationLayout.addWidget(self.searchInAllCountriesButton, 
                                            1, 1)
        self.searchLocationLayout.addWidget(self.searchInUsaButton, 2, 1)
        self.searchLocationLayout.addWidget(self.countriesComboBox, 3, 0)
        self.searchLocationLayout.\
            addWidget(self.searchInSpecifiedCountryButton, 3, 1)

        self.birthPlaceSearchResultsLabel = QLabel("Search &results:")
        self.birthPlaceSearchResultsComboBox = QComboBox()
        self.birthPlaceSearchResultsLabel.\
            setBuddy(self.birthPlaceSearchResultsComboBox)
        # Disable the QComboBox until the results come in.
        self.birthPlaceSearchResultsComboBox.setEnabled(False)

        if self.geoNamesEnabled == False:
            self.geoNamesStatusLabel = \
                QLabel("<font color=\"red\">" + \
                       "Search functionality is disabled due to failed " + \
                       "network connection to GeoNames web service." + \
                       "</font>")
        else:
            self.geoNamesStatusLabel = QLabel("")

        self.geoNamesStatusLabel.setWordWrap(True)
        self.birthPlaceSearchResultsLayout = QVBoxLayout()
        self.birthPlaceSearchResultsLayout.addSpacing(20)
        self.birthPlaceSearchResultsLayout.\
            addWidget(self.birthPlaceSearchResultsLabel)
        self.birthPlaceSearchResultsLayout.\
            addWidget(self.birthPlaceSearchResultsComboBox)
        self.birthPlaceSearchResultsLayout.addSpacing(20)
        self.birthPlaceSearchResultsLayout.\
            addWidget(self.geoNamesStatusLabel)

        # Do I want to disable search widgets if the initial connect test
        # failed?  Maybe the second attempt via the search button will work.
        #if self.geoNamesEnabled == False:
        #    self.searchInUsaButton.setEnabled(False)
        #    self.searchInAllCountriesButton.setEnabled(False)
        #    self.searchInSpecifiedCountryButton.setEnabled(False)
        #    self.countriesComboBox.setEnabled(False)

        self.longitudeLabel = QLabel("&Longitude:")
        self.longitudeDegreesLabel = QLabel("Degrees (0-180)")
        self.longitudeMinutesLabel = QLabel("Minutes (0-59)")
        self.longitudeSecondsLabel = QLabel("Seconds (0-59)")

        self.longitudeDegreesSpinBox = QSpinBox()
        self.longitudeLabel.setBuddy(self.longitudeDegreesSpinBox)
        self.longitudeDegreesSpinBox.setMinimum(0)
        self.longitudeDegreesSpinBox.setMaximum(180)
        self.longitudeEastWestComboBox = QComboBox()
        self.longitudeEastWestComboBox.addItem("E", "E")
        self.longitudeEastWestComboBox.addItem("W", "W")
        self.longitudeEastWestComboBox.setCurrentIndex(0)
        self.longitudeMinutesSpinBox = QSpinBox()
        self.longitudeMinutesSpinBox.setMinimum(0)
        self.longitudeMinutesSpinBox.setMaximum(59)
        self.longitudeSecondsSpinBox = QSpinBox()
        self.longitudeSecondsSpinBox.setMinimum(0)
        self.longitudeSecondsSpinBox.setMaximum(59)

        self.lonGridLayout = QGridLayout()
        self.lonGridLayout.addWidget(self.longitudeDegreesLabel, 0, 1)
        self.lonGridLayout.addWidget(self.longitudeMinutesLabel, 0, 3)
        self.lonGridLayout.addWidget(self.longitudeSecondsLabel, 0, 4)
        self.lonGridLayout.addWidget(self.longitudeLabel, 1, 0)
        self.lonGridLayout.addWidget(self.longitudeDegreesSpinBox, 1, 1)
        self.lonGridLayout.addWidget(self.longitudeEastWestComboBox, 1, 2)
        self.lonGridLayout.addWidget(self.longitudeMinutesSpinBox, 1, 3)
        self.lonGridLayout.addWidget(self.longitudeSecondsSpinBox, 1, 4)

        self.longitudeDecimalFormatValueLabel = QLabel("")
        self.lonDecimalLayout = QHBoxLayout()
        self.lonDecimalLayout.addStretch()
        self.lonDecimalLayout.addWidget(self.longitudeDecimalFormatValueLabel)

        self.latitudeLabel = QLabel("Latit&ude:")
        self.latitudeDegreesLabel = QLabel("Degrees (0-90)")
        self.latitudeMinutesLabel = QLabel("Minutes (0-59)")
        self.latitudeSecondsLabel = QLabel("Seconds (0-59)")

        self.latitudeDegreesSpinBox = QSpinBox()
        self.latitudeLabel.setBuddy(self.latitudeDegreesSpinBox)
        self.latitudeDegreesSpinBox.setMinimum(0)
        self.latitudeDegreesSpinBox.setMaximum(90)
        self.latitudeNorthSouthComboBox = QComboBox()
        self.latitudeNorthSouthComboBox.addItem("N", "N")
        self.latitudeNorthSouthComboBox.addItem("S", "S")
        self.latitudeMinutesSpinBox = QSpinBox()
        self.latitudeMinutesSpinBox.setMinimum(0)
        self.latitudeMinutesSpinBox.setMaximum(59)
        self.latitudeSecondsSpinBox = QSpinBox()
        self.latitudeSecondsSpinBox.setMinimum(0)
        self.latitudeSecondsSpinBox.setMaximum(59)

        self.latGridLayout = QGridLayout()
        self.latGridLayout.addWidget(self.latitudeDegreesLabel, 0, 1)
        self.latGridLayout.addWidget(self.latitudeMinutesLabel, 0, 3)
        self.latGridLayout.addWidget(self.latitudeSecondsLabel, 0, 4)
        self.latGridLayout.addWidget(self.latitudeLabel, 1, 0)
        self.latGridLayout.addWidget(self.latitudeDegreesSpinBox, 1, 1)
        self.latGridLayout.addWidget(self.latitudeNorthSouthComboBox, 1, 2)
        self.latGridLayout.addWidget(self.latitudeMinutesSpinBox, 1, 3)
        self.latGridLayout.addWidget(self.latitudeSecondsSpinBox, 1, 4)
        self.latitudeDecimalFormatValueLabel = QLabel("")

        self.latDecimalLayout = QHBoxLayout()
        self.latDecimalLayout.addStretch()
        self.latDecimalLayout.addWidget(self.latitudeDecimalFormatValueLabel)

        self.latLonLayout = QVBoxLayout()
        self.latLonLayout.addLayout(self.lonGridLayout)
        self.latLonLayout.addLayout(self.lonDecimalLayout)
        self.latLonLayout.addLayout(self.latGridLayout)
        self.latLonLayout.addLayout(self.latDecimalLayout)

        self.elevationLabel = QLabel("Ele&vation:")
        self.elevationSpinBox = QSpinBox()
        self.elevationLabel.setBuddy(self.elevationSpinBox)
        # The dead sea is about -400 meters above sea level 
        # and mount everest is about 8850, so these settings should
        # cover just about all scenarios except for in-flight births.
        self.elevationSpinBox.setMinimum(-400)
        self.elevationSpinBox.setMaximum(10000)
        self.elevationSpinBox.setValue(0)
        self.elevationUnitsLabel = QLabel("meters above sea level")

        self.elevationLayout = QHBoxLayout()
        self.elevationLayout.addWidget(self.elevationLabel)
        self.elevationLayout.addWidget(self.elevationSpinBox)
        self.elevationLayout.addWidget(self.elevationUnitsLabel)

        self.birthLocationLayout = QVBoxLayout()
        self.birthLocationLayout.addLayout(self.searchLocationLayout)
        self.birthLocationLayout.addLayout(self.birthPlaceSearchResultsLayout)
        self.birthLocationLayout.addLayout(self.latLonLayout)
        self.birthLocationLayout.addLayout(self.elevationLayout)
        
        self.birthLocationGroupBox = QGroupBox("Birth Location")
        self.birthLocationGroupBox.setLayout(self.birthLocationLayout)
        

        # Timezone widgets.
        self.autodetectedOffsetRadioButton = \
            QRadioButton("Autodetected time&zone time offset")
        self.autodetectedOffsetRadioButton.setChecked(True)
        self.timezoneLabel = QLabel("Timezone: ")
        self.timezoneComboBox = QComboBox()
        self.timezoneComboBox.addItems(pytz.common_timezones)
        self.timezoneLayout = QHBoxLayout()
        self.timezoneLayout.addSpacing(self.indentSpacing)
        self.timezoneLayout.addWidget(self.timezoneLabel)
        self.timezoneLayout.addWidget(self.timezoneComboBox)

        self.timezoneOffsetLabel = QLabel("Time offset: ")
        self.timezoneOffsetValueLabel = QLabel("")
        self.timeOffsetValueLayout = QHBoxLayout()
        self.timeOffsetValueLayout.addSpacing(self.indentSpacing)
        self.timeOffsetValueLayout.addWidget(self.timezoneOffsetLabel)
        self.timeOffsetValueLayout.addWidget(self.timezoneOffsetValueLabel)

        self.manualEntryRadioButton = QRadioButton("Manual &Entry")
        self.timeOffsetHoursLabel = QLabel("Hours")
        self.timeOffsetHoursLabel.setAlignment(Qt.AlignCenter)
        self.timeOffsetMinutesLabel = QLabel("Minutes")
        self.timeOffsetMinutesLabel.setAlignment(Qt.AlignCenter)
        self.timeOffsetHoursSpinBox = QSpinBox()
        self.timeOffsetHoursSpinBox.setMinimum(0)
        self.timeOffsetHoursSpinBox.setMaximum(14)
        self.timeOffsetHoursSpinBox.setEnabled(False)
        self.timeOffsetMinutesSpinBox = QSpinBox()
        self.timeOffsetMinutesSpinBox.setMinimum(0)
        self.timeOffsetMinutesSpinBox.setMaximum(59)
        self.timeOffsetMinutesSpinBox.setEnabled(False)
        self.timeOffsetEastWestComboBox = QComboBox()
        self.timeOffsetEastWestComboBox.addItem("East of UTC", "E")
        self.timeOffsetEastWestComboBox.addItem("West of UTC", "W")
        self.timeOffsetEastWestComboBox.setEnabled(False)
        self.timeOffsetManualEntryGridLayout = QGridLayout()
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetHoursLabel, 0, 0)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetMinutesLabel, 0, 1)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetHoursSpinBox, 1, 0)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetMinutesSpinBox, 1, 1)
        self.timeOffsetManualEntryGridLayout.\
            addWidget(self.timeOffsetEastWestComboBox, 1, 2)
        self.timeOffsetManualEntryLayout = QHBoxLayout()
        self.timeOffsetManualEntryLayout.addSpacing(self.indentSpacing)
        self.timeOffsetManualEntryLayout.\
            addLayout(self.timeOffsetManualEntryGridLayout)

        self.lmtRadioButton = \
            QRadioButton("Local Mean &Time (for really old dates)")
        
        self.timeOffsetLayout = QVBoxLayout()
        self.timeOffsetLayout.addWidget(self.autodetectedOffsetRadioButton)
        self.timeOffsetLayout.addLayout(self.timezoneLayout)
        self.timeOffsetLayout.addLayout(self.timeOffsetValueLayout)
        self.timeOffsetLayout.addWidget(self.manualEntryRadioButton)
        self.timeOffsetLayout.addLayout(self.timeOffsetManualEntryLayout)
        self.timeOffsetLayout.addWidget(self.lmtRadioButton)

        self.timeOffsetGroupBox = QGroupBox("Time Offset")
        self.timeOffsetGroupBox.setLayout(self.timeOffsetLayout)


        # Buttons at bottom.
        self.okayButton = QPushButton("&Okay")
        self.cancelButton = QPushButton("&Cancel")
        self.buttonsAtBottomLayout = QHBoxLayout()
        self.buttonsAtBottomLayout.addStretch()
        self.buttonsAtBottomLayout.addWidget(self.okayButton)
        self.buttonsAtBottomLayout.addWidget(self.cancelButton)

        # Put all layouts/groupboxes together into the widget.
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.birthTimeGroupBox) 
        self.mainLayout.addWidget(self.birthLocationGroupBox) 
        self.mainLayout.addWidget(self.timeOffsetGroupBox) 
        self.mainLayout.addLayout(self.buttonsAtBottomLayout) 

        self.setLayout(self.mainLayout)

        # Connect signals and slots.
        self.okayButton.clicked.connect(self._handleOkayButtonClicked)
        self.cancelButton.clicked.connect(self._handleCancelButtonClicked)

        self.searchInAllCountriesButton.clicked.\
            connect(self._handleSearchInAllCountriesButtonClicked)
        self.searchInUsaButton.clicked.\
            connect(self._handleSearchInUsaButtonClicked)
        self.searchInSpecifiedCountryButton.clicked.\
            connect(self._handleSearchInSpecifiedCountryButtonClicked)

        self.birthPlaceSearchResultsComboBox.currentIndexChanged[int].\
            connect(self._handleSearchResultSelected)

        self.timezoneComboBox.currentIndexChanged[int].\
            connect(self._handleTimezoneComboBoxChanged)

        # Connect the birth time widgets being changed to the 
        # _handleBirthTimeWidgetsChanged slot.
        self.monthSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.daySpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.yearSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.calendarComboBox.currentIndexChanged[int].\
            connect(self._handleBirthTimeWidgetsChanged)
        self.hourSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.minuteSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)
        self.secondSpinBox.valueChanged.\
            connect(self._handleBirthTimeWidgetsChanged)


        # Connect the longitude widgets being changed to the slot to 
        # handle it.
        self.longitudeDegreesSpinBox.valueChanged.\
            connect(self._handleLongitudeEditWidgetChanged)
        self.longitudeEastWestComboBox.currentIndexChanged[int].\
            connect(self._handleLongitudeEditWidgetChanged)
        self.longitudeMinutesSpinBox.valueChanged.\
            connect(self._handleLongitudeEditWidgetChanged)
        self.longitudeSecondsSpinBox.valueChanged.\
            connect(self._handleLongitudeEditWidgetChanged)

        # Connect the latitude widgets being changed to the slot to 
        # handle it.
        self.latitudeDegreesSpinBox.valueChanged.\
            connect(self._handleLatitudeEditWidgetChanged)
        self.latitudeNorthSouthComboBox.currentIndexChanged[int].\
            connect(self._handleLatitudeEditWidgetChanged)
        self.latitudeMinutesSpinBox.valueChanged.\
            connect(self._handleLatitudeEditWidgetChanged)
        self.latitudeSecondsSpinBox.valueChanged.\
            connect(self._handleLatitudeEditWidgetChanged)

        # Connect radio buttons in the time offset groupbox.
        self.autodetectedOffsetRadioButton.clicked.\
            connect(self._handleTimeOffsetRadioButtonClicked)
        self.manualEntryRadioButton.clicked.\
            connect(self._handleTimeOffsetRadioButtonClicked)
        self.lmtRadioButton.clicked.\
            connect(self._handleTimeOffsetRadioButtonClicked)

        # Set the initial values/config in the widgets.

        # Select UTC timezone by default (this should be the last index).
        self.timezoneComboBox.\
            setCurrentIndex(self.timezoneComboBox.count() - 1)

        # Select the text in the first widget so that the user can 
        # immediately type to enter the value of the month.
        self.monthSpinBox.selectAll()


    def validate(self):
        """Validates the input values in the edit widgets.
        Currently this function always returns True since the 
        individual QSpinBox widgets and QComboBox widgets already have 
        validation to make sure they are valid values/format.
        """

        return True


    def setBottomButtonsVisible(self, flag):
        """Sets the bottom buttons for accepting and canceling to 
        be visible or not.

        Arguments:
        flag  - Boolean value for setting the widgets visible.
        """

        self.log.debug("setBottomButtonsVisible(flag={})".format(flag))

        if type(flag) == bool:
            self.loadButton.setVisible(flag)
            self.cancelButton.setVisible(flag)


    def setBirthTimeWidgetValues(self, 
                                 year,
                                 month,
                                 day,
                                 hour,
                                 minute,
                                 second,
                                 calendar="Gregorian"):
        """Fills the birth time edit widgets with the values specified.

        Arguments:
        year    - int value for the year
        month   - int value for the month
        day     - int value for the day
        hour    - int value for the hour
        minute  - int value for the minute
        second  - int value for the second
        calendar - str value, for the calendar system used.
                   This is either 'Gregorian' or 'Julian'.
        """

        # Verify nothing is None.
        if (year == None or \
            month == None or \
            day == None or \
            hour == None or \
            minute == None or \
            second == None or \
            calendar == None):

            self.log.error("Parameters to setBirthTimeWidgetValues() " + 
                           "cannot be None.")
            return
        
        # These are int QSpinBoxes so force values to ints.
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        
        # Year.
        if (year >= self.yearSpinBox.minimum() and \
            year <= self.yearSpinBox.maximum()):

            self.yearSpinBox.setValue(year)
        else:
            self.log.warn("Year {} is outside the expected range [{}, {}].".\
                          format(year, 
                                 self.yearSpinBox.minimum(),
                                 self.yearSpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.yearSpinBox.setValue(year)

        # Month.
        if (month >= self.monthSpinBox.minimum() and \
            month <= self.monthSpinBox.maximum()):

            self.monthSpinBox.setValue(month)
        else:
            self.log.warn("Month {} is outside the expected range [{}, {}].".\
                          format(month, 
                                 self.monthSpinBox.minimum(),
                                 self.monthSpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.monthSpinBox.setValue(month)

        # Day.
        if (day >= self.daySpinBox.minimum() and \
            day <= self.daySpinBox.maximum()):

            self.daySpinBox.setValue(day)
        else:
            self.log.warn("Day {} is outside the expected range [{}, {}].".\
                          format(day, 
                                 self.daySpinBox.minimum(),
                                 self.daySpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.daySpinBox.setValue(day)

        # Hour.
        if (hour >= self.hourSpinBox.minimum() and \
            hour <= self.hourSpinBox.maximum()):

            self.hourSpinBox.setValue(hour)
        else:
            self.log.warn("Hour {} is outside the expected range [{}, {}].".\
                          format(hour, 
                                 self.hourSpinBox.minimum(),
                                 self.hourSpinBox.maximum()) + \
                          "  Forcing it to be within the range.")

            # The QSpinBox will force the value to be within range.
            self.hourSpinBox.setValue(hour)

        # Minute.
        if (minute >= self.minuteSpinBox.minimum() and \
            minute <= self.minuteSpinBox.maximum()):

            self.minuteSpinBox.setValue(minute)
        else:
            warnStr = "Minute {} is outside the expected range [{}, {}].".\
                      format(minute, 
                             self.minuteSpinBox.minimum(),
                             self.minuteSpinBox.maximum()) + \
                      "  Forcing it to be within the range."

            self.log.warn(warnStr)

            # The QSpinBox will force the value to be within range.
            self.minuteSpinBox.setValue(minute)

        # Second.
        if (second >= self.secondSpinBox.minimum() and \
            second <= self.secondSpinBox.maximum()):

            self.secondSpinBox.setValue(second)
        else:
            warnStr = "Second {} is outside the expected range [{}, {}].".\
                      format(second, 
                             self.secondSpinBox.minimum(),
                             self.secondSpinBox.maximum()) + \
                      "  Forcing it to be within the range."

            self.log.warn(warnStr)

            # The QSpinBox will force the value to be within range.
            self.secondSpinBox.setValue(second)

        # Calendar.
        index = self.calendarComboBox.findText(calendar)
        if (index != -1):
            self.calendarComboBox.setCurrentIndex(index)
        else:
            # Unrecognized calendar system specified.  
            warnStr = "Calendar system specified ({}) is not recognized.".\
                format(calendar)
            
            # Don't change anything in the widgets.


    def loadBirthInfo(self, birthInfoObj):
        """Loads the edit widgets with the data contained in the given
        BirthInfo object.

        Arguments:
        birthInfoObj - BirthInfo object containing data attributes for
        all the birth info fields that can be editted with this widget.
        """

        self.monthSpinBox.setValue(birthInfoObj.month)
        self.daySpinBox.setValue(birthInfoObj.day)
        self.yearSpinBox.setValue(birthInfoObj.year)

        # Try to find the index that matches the calendar string that is
        # stored in the BirthInfo object.
        indexToSet = \
            self.calendarComboBox.findText(birthInfoObj.calendar)

        # If the calendar type is not found, then default to whatever the
        # default is at widget creation.
        if indexToSet == -1:
            errStr = "Calendar type '" + birthInfoObj.calendar + \
                     "' is not supported.  Defaulting to " + \
                     self.calendarComboBox.currentText()
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)
        else:
            # Valid index, so set the combo box.
            self.calendarComboBox.setCurrentIndex(indexToSet)

        self.hourSpinBox.setValue(birthInfoObj.hour)
        self.minuteSpinBox.setValue(birthInfoObj.minute)
        self.secondSpinBox.setValue(birthInfoObj.second)

        self.cityNameLineEdit.setText(birthInfoObj.locationName)

        # Try to find the index that matches the countryName string that is
        # stored in the BirthInfo object.
        indexToSet = \
            self.countriesComboBox.findText(birthInfoObj.countryName)

        if indexToSet == -1:
            # Couldn't find a match for the country name string.
            errStr = "Attempted to load an unknown country name: " + \
                birthInfoObj.countryName
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)
        else:
            # Valid index, so set the combo box.
            self.countriesComboBox.setCurrentIndex(indexToSet)

        # No need to load anything into the
        # birthPlaceSearchResultsComboBox.

        # Convert longitude from a float value to degrees,
        # minutes, seconds and East/West polarity.
        (lonDegrees, lonMinutes, lonSeconds, lonPolarity) = \
            GeoInfo.longitudeToDegMinSec(birthInfoObj.longitudeDegrees)
        self.longitudeDegreesSpinBox.setValue(lonDegrees)
        index = self.longitudeEastWestComboBox.findText(lonPolarity)
        self.longitudeEastWestComboBox.setCurrentIndex(index)
        self.longitudeMinutesSpinBox.setValue(lonMinutes)
        self.longitudeSecondsSpinBox.setValue(lonSeconds)

        # Need to convert latitude from float value to degrees, minutes,
        # seconds and North/South polarity.
        (latDegrees, latMinutes, latSeconds, latPolarity) = \
            GeoInfo.latitudeToDegMinSec(birthInfoObj.latitudeDegrees)
        self.latitudeDegreesSpinBox.setValue(latDegrees)
        index = self.latitudeNorthSouthComboBox.findText(latPolarity)
        self.latitudeNorthSouthComboBox.setCurrentIndex(index)
        self.latitudeMinutesSpinBox.setValue(latMinutes)
        self.latitudeSecondsSpinBox.setValue(latSeconds)

        # Elevation.
        self.elevationSpinBox.setValue(birthInfoObj.elevation)

        # Timezone widgets.
        self.autodetectedOffsetRadioButton.\
            setChecked(birthInfoObj.timeOffsetAutodetectedRadioButtonState)
        self.manualEntryRadioButton.\
            setChecked(birthInfoObj.timeOffsetManualEntryRadioButtonState)
        self.lmtRadioButton.\
            setChecked(birthInfoObj.timeOffsetLMTRadioButtonState)

        index = self.timezoneComboBox.findText(birthInfoObj.timezoneName)
        if index != -1:
            self.timezoneComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find the following timezone to load: '" + \
                birthInfoObj.timezoneName + "'"
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)

        # Create and set the string for the timezone offset label.
        self.timezoneOffsetValueLabel.\
            setText(birthInfoObj.timezoneOffsetAbbreviation + " " + \
                    birthInfoObj.timezoneOffsetValueStr)

        # Set the manual entry widgets.
        self.timeOffsetHoursSpinBox.\
            setValue(birthInfoObj.timezoneManualEntryHours)
        self.timeOffsetMinutesSpinBox.\
            setValue(birthInfoObj.timezoneManualEntryMinutes)
        index = self.timeOffsetEastWestComboBox.\
            findData(birthInfoObj.timezoneManualEntryEastWestComboBoxValue)
        if index != -1:
            self.timeOffsetEastWestComboBox.setCurrentIndex(index)
        else:
            errStr = "Couldn't find the following manual entry timezone " + \
                "offset east/west text to load: '" + \
                birthInfoObj.timezoneManualEntryEastWestComboBoxValue + "'"
            self.log.error(errStr)
            QMessageBox.warning(None, "Error", errStr)


    def getBirthInfo(self):
        """Extracts from all the widgets, the edit widget state and
        the birth information, and returns this information as 
        a BirthInfo object.

        Returns:
        BirthInfo - Fully populated BirthInfo object, holding the
        fields and state of this edit widget.
        """

        # Do some conversions first before creating the returned BirthInfo
        # object.

        # Get the longitude in degrees float value.
        longitudeDegrees = \
            GeoInfo.\
            longitudeToDegrees(self.longitudeDegreesSpinBox.value(),
                               self.longitudeMinutesSpinBox.value(),
                               self.longitudeSecondsSpinBox.value(),
                               str(self.longitudeEastWestComboBox.\
                                       currentText()))


        # Get the latitude in degrees float value.
        latitudeDegrees = \
            GeoInfo.\
            latitudeToDegrees(self.latitudeDegreesSpinBox.value(),
                              self.latitudeMinutesSpinBox.value(),
                              self.latitudeSecondsSpinBox.value(),
                              str(self.latitudeNorthSouthComboBox.\
                                      currentText()))

        # Get the timezone abbreviation and timezone offset.  We have to
        # jump through a bunch of hoops to get this.

        timezoneString = str(self.timezoneComboBox.currentText())
        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)
        # Get int values from the QSpinBox widgets.
        year = self.yearSpinBox.value()
        day = self.daySpinBox.value()
        month = self.monthSpinBox.value()
        hour = self.hourSpinBox.value()
        minute = self.minuteSpinBox.value()
        second = self.secondSpinBox.value()
        # Create the localized datetime object.
        datetimeObj = \
            datetime.datetime(year, month, day, hour, minute, second)
        localizedDatetimeObj = tzinfoObj.localize(datetimeObj)

        timezoneOffsetValueStr = \
            Ephemeris.getTimezoneOffsetFromDatetime(localizedDatetimeObj)
        # Here tzname() won't return None because we explicitly specified a
        # pytz tzinfo to the datetime above.
        timezoneOffsetAbbreviation = localizedDatetimeObj.tzname()

        # Finally, create the BirthInfo object with all the required
        # inputs.
        rv = BirthInfo(self.yearSpinBox.value(),
                       self.monthSpinBox.value(),
                       self.yearSpinBox.value(),
                       str(self.calendarComboBox.currentText()),
                       self.hourSpinBox.value(),
                       self.minuteSpinBox.value(),
                       self.secondSpinBox.value(),
                       str(self.cityNameLineEdit.text()),
                       str(self.countriesComboBox.currentText()),
                       longitudeDegrees,
                       latitudeDegrees,
                       self.elevationSpinBox.value(),
                       str(self.timezoneComboBox.currentText()),
                       timezoneOffsetAbbreviation,
                       timezoneOffsetValueStr,
                       self.timeOffsetHoursSpinBox.value(),
                       self.timeOffsetMinutesSpinBox.value(),
                       str(self.timeOffsetEastWestComboBox.currentText()),
                       self.autodetectedOffsetRadioButton.isChecked(),
                       self.manualEntryRadioButton.isChecked(),
                       self.lmtRadioButton.isChecked())

        return rv


    def _handleSearchInAllCountriesButtonClicked(self):
        """Uses GeoNames to do a lookup of a location based on the search
        string in self.cityNameLineEdit.  Results that are returned are
        populated in the self.birthPlaceSearchResultsComboBox.  
        """

        self.log.debug("Entered _handleSearchInAllCountriesButtonClicked()")

        searchString = str(self.cityNameLineEdit.text())
        self.log.debug("searchString=" + searchString)

        geoInfos = []

        try:
            geoInfos = GeoNames.search(searchStr=searchString, 
                                       countryBias="",
                                       country="")
        except urllib.error.URLError as e:
            msgStr = "Couldn't perform the search because " + \
                     "of the following error: " + e.reason.strerror
            QMessageBox.warning(None, "Error", msgStr)
            return

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))

        self._populateSearchResultsComboBox(geoInfos)

        # If there are search results, then select the first result.
        if self.birthPlaceSearchResultsComboBox.count() > 0:
            self.birthPlaceSearchResultsComboBox.setCurrentIndex(0)

        # Here we clear the country selected in the self.countriesComboBox 
        # that # is used for searching in a specified country.  We do this to
        # prevent the user from being confused about the fact that the 
        # results are for a search in all countries, not the country 
        # listened in that selection combo box.  
        # Index 0 here is just an empty string entry.
        self.countriesComboBox.setCurrentIndex(0)

        self.log.debug("Leaving _handleSearchInAllCountriesButtonClicked()")

    def _handleSearchInUsaButtonClicked(self):
        """Uses GeoNames to do a lookup of a location in the US based on the
        search string in self.cityNameLineEdit.  Results that are returned 
        are populated in the self.birthPlaceSearchResultsComboBox.  
        """

        self.log.debug("Entered _handleSearchInUsaButtonClicked()")

        searchString = str(self.cityNameLineEdit.text())
        self.log.debug("searchString=" + searchString)

        geoInfos = []

        try:
            geoInfos = GeoNames.search(searchStr=searchString, 
                                       countryBias="US",
                                       country="US")
        except urllib.error.URLError as e:
            msgStr = "Couldn't perform the search because " + \
                     "of the following error: " + e.reason.strerror
            parent = self
            QMessageBox.warning(parent, "Error", msgStr)
            return

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))

        self._populateSearchResultsComboBox(geoInfos)

        # If there are search results, then select the first result.
        if self.birthPlaceSearchResultsComboBox.count() > 0:
            self.birthPlaceSearchResultsComboBox.setCurrentIndex(0)

        # Here we clear the country selected in the self.countriesComboBox 
        # that # is used for searching in a specified country.  We do this to
        # prevent the user from being confused about the fact that the 
        # results are for a search in all countries, not the country 
        # listened in that selection combo box.  
        # Index 0 here is just an empty string entry.
        self.countriesComboBox.setCurrentIndex(0)

        self.log.debug("Leaving _handleSearchInUsaButtonClicked()")


    def _handleSearchInSpecifiedCountryButtonClicked(self):
        """Uses GeoNames to do a lookup of a location based on the search
        string in self.cityNameLineEdit.  Results that are returned are
        populated in the self.birthPlaceSearchResultsComboBox.  
        """

        self.log.\
            debug("Entered _handleSearchInSpecifiedCountryButtonClicked()")

        searchString = str(self.cityNameLineEdit.text())
        self.log.debug("searchString=" + searchString)


        currIndex = self.countriesComboBox.currentIndex()
        countryName = self.countriesComboBox.itemText(currIndex)

        # This part is a bit tricky because PyQt has been changing how
        # QVariant data is stored and converted in combo boxes.
        # So here we do some extra checks before casting.
        countryCode = ""
        countryCodeQVariant = \
            self.countriesComboBox.itemData(currIndex)
        # Country code returned may be a QVariant storing a str 
        # or QString.
        if isinstance(countryCodeQVariant, QVariant):
            # This is a QVariant, so turn it into a PyObject first before
            # casting to str.
            countryCode = str(countryCodeQVariant.toPyObject())
        else:
            # It is just a str.  Wrap it again for safety's sake.
            countryCode = str(countryCodeQVariant)

        self.log.debug("countryName={}, countryCode={}".\
                       format(countryName, countryCode))

        geoInfos = []

        try:
            geoInfos = GeoNames.search(searchStr=searchString, 
                                       countryBias="",
                                       country=countryCode)
        except urllib.error.URLError as e:
            msgStr = "Couldn't perform the search because " + \
                     "of the following error: " + e.reason.strerror
            parent = self
            QMessageBox.warning(parent, "Error", msgStr)
            return

        self.log.debug("Got {} results back from GeoNames".\
                       format(len(geoInfos)))

        self._populateSearchResultsComboBox(geoInfos)

        # If there are search results, then select the first result.
        if self.birthPlaceSearchResultsComboBox.count() > 0:
            self.birthPlaceSearchResultsComboBox.setCurrentIndex(0)

        self.log.\
            debug("Leaving _handleSearchInSpecifiedCountryButtonClicked()")


    def _populateSearchResultsComboBox(self, geoInfos):
        """Populates self.birthPlaceSearchResultsComboBox with the 
        search results listed in the given list of GeoInfo objects.

        Arguments: 
        geoInfos - List of GeoNames.GeoInfo objects to use to populate 
                   the QComboBox.
        """

        self.log.debug("Entering _populateSearchResultsComboBox()")

        # Prepare the self.birthPlaceSearchResultsComboBox if there are new
        # results to populate it with.

        self.log.debug("Clearing birthPlaceSearchResultsComboBox...")
        # Clear the QComboBox of search results.
        self.birthPlaceSearchResultsComboBox.clear()

        if len(geoInfos) > 0:
            self.log.debug("Enabling birthPlaceSearchResultsComboBox...")
            # If the self.resultsComboBox is disabled, then enable it.
            if self.birthPlaceSearchResultsComboBox.isEnabled() == False:
                self.birthPlaceSearchResultsComboBox.setEnabled(True)

        # Populate the self.birthPlaceSearchResultsComboBox.
        for i in range(len(geoInfos)):
            geoInfo = geoInfos[i]

            displayStr = geoInfo.name
            if geoInfo.adminName1 != None and geoInfo.adminName1 != "":
                displayStr += ", " + geoInfo.adminName1
            if geoInfo.countryName != None and geoInfo.countryName != "":
                displayStr += ", " + geoInfo.countryName
            displayStr += " ({}, {})".format(geoInfo.latitudeStr(), 
                                             geoInfo.longitudeStr()) 
            if geoInfo.population != None and geoInfo.population != 0:
                displayStr += " (pop. {})".format(geoInfo.population)

            self.log.debug("Display name is: {}".format(displayStr))
            self.birthPlaceSearchResultsComboBox.addItem(displayStr, geoInfo)

        self.log.debug("Leaving _populateSearchResultsComboBox()")


    def _handleSearchResultSelected(self, index):
        """Determines which search result was selected, and populates
        the edit widgets with the info of that location.
        """

        self.log.debug("Entered _handleSearchResultSelected(index={})".\
                       format(index))

        # Only makes sense if the index selected is valid.  
        # Theoretically index should only be -1 on the very first load.
        if index == -1:
            return

        # This part is a bit tricky because PyQt has been changing how
        # QVariant data is stored and converted in combo boxes.
        # So here we do some extra checks before casting.
        maybeQVariant = self.birthPlaceSearchResultsComboBox.itemData(index)
        geoInfo = GeoInfo()
        if isinstance(maybeQVariant, QVariant):
            # This is really a QVariant, so use toPyObject().
            geoInfo = maybeQVariant.toPyObject()
        else:
            # PyQt converted it already for us.
            geoInfo = maybeQVariant

        # Make sure geoInfo is not None.  We need it in order to get the
        # timezone information.  It should never be None.
        if geoInfo == None:
            self.log.error("GeoInfo is None, when it should have " + \
                           "been an actual object!")
            return

        # Try to use the timezone in geoInfo first.  If that doesn't 
        # work, then the do a query for the timezone using the latitude and
        # longitude.
        if geoInfo.timezone != None and geoInfo.timezone != "":
            index = self.timezoneComboBox.findText(geoInfo.timezone)
            if index != -1:
                self.timezoneComboBox.setCurrentIndex(index)
            else:
                errStr = "Couldn't find timezone '" + geoInfo.timezone + \
                     "' returned by GeoNames in the pytz " + \
                     "list of timezones."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)
        else:
            # Try to do the query ourselves from GeoNames.getTimezone().
            timezone = None
            try:
                timezone = GeoNames.getTimezone(geoInfo.latitude,
                                                geoInfo.longitude)
            except urllib.error.URLError as e:
                errStr = "Couldn't perform the search because " + \
                         "of the following error: " + e.reason.strerror
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

            if timezone != None and timezone != "":
                index = self.timezoneComboBox.findText(geoInfo.timezone)
                if index != -1:
                    self.timezoneComboBox.setCurrentIndex(index)
                else:
                    errStr = "Couldn't find timezone '" + timezone + \
                         "' returned by GeoNames in the pytz " + \
                         "list of timezones."
                    self.log.error(errStr)
                    QMessageBox.warning(None, "Error", errStr)
            else:
                errStr = "GeoNames returned a null or empty timezone."
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

        
        # Set the longitude.
        (lonDegrees, lonMinutes, lonSeconds, lonPolarity) = \
            GeoInfo.longitudeToDegMinSec(geoInfo.longitude)
        self.longitudeDegreesSpinBox.setValue(lonDegrees)
        index = self.longitudeEastWestComboBox.findText(lonPolarity)
        self.longitudeEastWestComboBox.setCurrentIndex(index)
        self.longitudeMinutesSpinBox.setValue(lonMinutes)
        self.longitudeSecondsSpinBox.setValue(lonSeconds)

        # Set the latitude.
        (latDegrees, latMinutes, latSeconds, latPolarity) = \
            GeoInfo.latitudeToDegMinSec(geoInfo.latitude)
        self.latitudeDegreesSpinBox.setValue(latDegrees)
        index = self.latitudeNorthSouthComboBox.findText(latPolarity)
        self.latitudeNorthSouthComboBox.setCurrentIndex(index)
        self.latitudeMinutesSpinBox.setValue(latMinutes)
        self.latitudeSecondsSpinBox.setValue(latSeconds)

        # Set the elevation.
        elevation = 0
        if geoInfo.elevation != None:
            elevation = geoInfo.elevation
        else:
            # Try to obtain elevation via the GeoNames.getElevation() method.
            try:
                elevation = GeoNames.getElevation(geoInfo.latitude,
                                                  geoInfo.longitude)
            except urllib.error.URLError as e:
                errStr = "Couldn't get the elevation for lat={}, lon={} ".\
                        format(geoInfo.latitude, geoInfo.longitude) + \
                        "because of the following error: " + e.reason.strerror
                self.log.error(errStr)
                QMessageBox.warning(None, "Error", errStr)

                # Set the elevation to 0.
                elevation = 0

        # Set the spinbox.
        if elevation == None or elevation == -9999.0:
            # Elevation is -9999.0 when it is in the ocean or if 
            # there was no data for this location.  
            
            # Here we'll just force the elevation to zero.

            logStr = "Elevation for lat={}, lon={} was {}.".\
               format(geoInfo.latitude, 
                      geoInfo.longitude, 
                      elevation) + \
               "  Forcing elevation to be zero."

            self.log.info(logStr)

            elevation = 0

        elif elevation < self.elevationSpinBox.minimum():
            # Set it to the minimum.
            logStr = "Elevation returned for " + \
               "lat={}, lon={} was {}.".\
               format(geoInfo.latitude, 
                      geoInfo.longitude, 
                      elevation) + \
               "  Forcing elevation to the minimum."
            self.log.info(logStr)

            elevation = self.elevationSpinBox.minimum()

        elif elevation > self.elevationSpinBox.maximum():
            # Set it to the maximum.
            logStr = "Elevation returned for " + \
               "lat={}, lon={} was {}.".\
               format(geoInfo.latitude, 
                      geoInfo.longitude, 
                      elevation) + \
               "  Forcing elevation to the maximum."

            self.log.info(logStr)

            elevation = self.elevationSpinBox.maximum()

        # Set the spinbox.
        self.elevationSpinBox.setValue(int(elevation))

        self.log.debug("Leaving _handleSearchResultSelected()")


    def _handleLongitudeEditWidgetChanged(self):
        """Recalculates the longitude as a float and displays it in 
        the QLabel that holds this value 
        (self.longitudeDecimalFormatValueLabel).
        """

        self.log.debug("Entered _handleLongitudeEditWidgetChanged()")

        degreesInt = self.longitudeDegreesSpinBox.value()
        minutesInt = self.longitudeMinutesSpinBox.value()
        secondsInt = self.longitudeSecondsSpinBox.value()
        polarityStr = str(self.longitudeEastWestComboBox.currentText()) 

        # Do the calculation.
        longitudeFloat = \
            GeoInfo.longitudeToDegrees(degreesInt,
                                       minutesInt,
                                       secondsInt,
                                       polarityStr)

        # Set the QLabel widget.
        self.longitudeDecimalFormatValueLabel.\
            setText("{}".format(longitudeFloat))

        self.log.debug("Leaving _handleLongitudeEditWidgetChanged()")
   
    def _handleLatitudeEditWidgetChanged(self):
        """Recalculates the latitude as a float and displays it in 
        the QLabel that holds this value
        (self.latitudeDecimalFormatValueLabel)
        """

        self.log.debug("Entered _handleLatitudeEditWidgetChanged()")

        degreesInt = self.latitudeDegreesSpinBox.value()
        minutesInt = self.latitudeMinutesSpinBox.value()
        secondsInt = self.latitudeSecondsSpinBox.value()
        polarityStr = str(self.latitudeNorthSouthComboBox.currentText()) 

        # Do the calculation.
        latitudeFloat = \
            GeoInfo.latitudeToDegrees(degreesInt,
                                       minutesInt,
                                       secondsInt,
                                       polarityStr)

        # Set the QLabel widget.
        self.latitudeDecimalFormatValueLabel.\
            setText("{}".format(latitudeFloat))

        self.log.debug("Leaving _handleLatitudeEditWidgetChanged()")

    def _handleTimezoneComboBoxChanged(self, index):
        """Sets the self.timezoneOffsetValueLabel to hold the actual 
        offset amount based off the date and timezone set in the widgets.

        If the radio button for 'Manual Entry' is not selected 
        (the widgets for manual entry are disabled), then this function 
        fills in the value in those widgets.  This is just for convenience 
        so that mods from the auto-detected value can be done.
        """

        self.log.debug("Entered _handleTimezoneComboBoxChanged()")

        # Get the timezone string from the QComboBox (and convert from 
        # QString to str).
        timezoneString = str(self.timezoneComboBox.currentText())

        # Create a timezone object.
        tzinfoObj = pytz.timezone(timezoneString)

        # Get int values from the QSpinBox widgets.
        year = self.yearSpinBox.value()
        day = self.daySpinBox.value()
        month = self.monthSpinBox.value()
        hour = self.hourSpinBox.value()
        minute = self.minuteSpinBox.value()
        second = self.secondSpinBox.value()

        # Create the localized datetime object.
        datetimeObj = \
            datetime.datetime(year, month, day, hour, minute, second)
        localizedDatetimeObj = tzinfoObj.localize(datetimeObj)


        # Here we are creating the string that will be displayed in the label
        # holding the timezone and time offset info.

        # String that holds the time offset from UTC.
        offsetStr = \
            Ephemeris.getTimezoneOffsetFromDatetime(localizedDatetimeObj)

        # Here tzname() won't return None because we explicitly specified a
        # pytz tzinfo to the datetime above.
        timeOffsetString = \
            localizedDatetimeObj.tzname() + " " + offsetStr

        # Set the label.
        self.timezoneOffsetValueLabel.setText(timeOffsetString)

        if self.manualEntryRadioButton.isChecked() == False:
            # Manual Entry widgets are disabled for user input.
            # Here we'll update the widgets' values.

            timeOffsetValueString = offsetStr

            if timeOffsetValueString[0:1] == "+":
                # West of UTC.
                index = self.timeOffsetEastWestComboBox.\
                    findText("West of UTC")
                self.timeOffsetEastWestComboBox.setCurrentIndex(index)
            elif timeOffsetValueString[0:1] == "-":
                # East of UTC.
                index = self.timeOffsetEastWestComboBox.\
                    findText("East of UTC")
                self.timeOffsetEastWestComboBox.setCurrentIndex(index)

            absoluteHoursOffset = int(timeOffsetValueString[1:3])
            absoluteMinutesOffset = int(timeOffsetValueString[3:5])

            self.timeOffsetHoursSpinBox.setValue(absoluteHoursOffset)
            self.timeOffsetMinutesSpinBox.setValue(absoluteMinutesOffset)

        self.log.debug("Leaving _handleTimezoneComboBoxChanged()")

    def _handleBirthTimeWidgetsChanged(self):
        """When the birth time widgets change, the time offset should be
        updated if it is set on 'Autodetected timezone time offset'.  
        This is because certain dates/times will fall under daylight 
        savings and thus the offset will be changed.
        """

        self.log.debug("Entered _handleBirthTimeWidgetsChanged()")

        # Find out what the timezone index is selected.
        index = self.timezoneComboBox.currentIndex()

        # Call the _handleTimezoneComboBoxChanged as if the timezone 
        # changed.  That function will make the necessary calls to update
        # the time offset used.
        self._handleTimezoneComboBoxChanged(index)

        self.log.debug("Leaving _handleBirthTimeWidgetsChanged()")

    def _handleTimeOffsetRadioButtonClicked(self):
        """Called when a radio button is clicked in the 'Time Offset'
        QGroupBox.  This function disables widgets that are under
        the radio button that is not selected.
        """

        self.log.debug("Entered _handleTimeOffsetRadioButtonClicked()")

        # The radio buttons are exclusive, so we can do the logic 
        # like below.

        shouldEnable = self.autodetectedOffsetRadioButton.isChecked()
        self.timezoneComboBox.setEnabled(shouldEnable)

        shouldEnable = self.manualEntryRadioButton.isChecked()
        self.timeOffsetHoursSpinBox.setEnabled(shouldEnable)
        self.timeOffsetMinutesSpinBox.setEnabled(shouldEnable)
        self.timeOffsetEastWestComboBox.setEnabled(shouldEnable)

        self.log.debug("Leaving _handleTimeOffsetRadioButtonClicked()")



    def _handleOkayButtonClicked(self):
        """Called when the okay button is clicked.
        This function validates the input widgets and emits 
        self.okayButtonClicked if the input has been validated
        successfully.
        """

        if self.validate() == True:
            self.okayButtonClicked.emit()

    def _handleCancelButtonClicked(self):
        """Called when the cancel button is clicked.
        This function does nothing but emit the 
        self.cancelButtonClicked signal.
        """

        self.cancelButtonClicked.emit()

class BirthInfoEditDialog(QDialog):
    """QDialog for editing a birth time of defining a new birth time."""

    def __init__(self, birthInfo=BirthInfo(), parent=None):
        """Initializes the QDialog with the info from birthInfo.

        Paraters:
        birthInfo - BirthInfo object to load the widgets with.
        parent    - QWidget parent.
        """

        super().__init__(parent)

        # Logger object for this class.
        self.log = logging.\
            getLogger("dialogs.BirthInfoEditDialog")

        # Create the contents.
        self.birthInfoEditWidget = BirthInfoEditWidget()
        self.birthInfoEditWidget.loadBirthInfo(birthInfo)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.birthInfoEditWidget)
        self.setLayout(layout)

        self.birthInfoEditWidget.okayButtonClicked.connect(self.accept)
        self.birthInfoEditWidget.cancelButtonClicked.connect(self.reject)


    def getBirthInfo(self):
        """Returns the BirthInfo object as is/was displayed in the widgets.
        """

        return self.birthInfoEditWidget.getBirthInfo()

# For debugging the module during development.  
if __name__=="__main__":
    # Initialize Logging for the Ephemeris class (required).
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    wizard = PriceChartDocumentWizard()
    returnVal = wizard.exec_()

    if returnVal == QDialog.Accepted:
        print("Accepted!");
        print("Data filename is: " + wizard.field("dataFilename"))
        print("Data num lines to skip is: {}".\
            format(wizard.field("dataNumLinesToSkip")))
        print("Timezone is: " + wizard.field("timezone"))
    else:
        print("Rejected!")

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()

    #loadDataFileWizardPage = \
    #    PriceChartDocumentLoadDataFileWizardPage()
    #loadDataFileWizardPage.show()
    #loadDataFileWidget = LoadDataFileWidget()
    #loadDataFileWidget.show()


    #locationTimezoneWizardPage = \
    #    PriceChartDocumentLocationTimezoneWizardPage()
    #locationTimezoneWizardPage.show()
    #locationTimezoneEditWidget = LocationTimezoneEditWidget()
    #locationTimezoneEditWidget.show()


    #msgStr = "Couldn't perform the search because " + \
    #         "of the following error: "
    #parent = None
    #QMessageBox.warning(parent, "Error", msgStr)

    
    #bew = BirthInfoEditWidget()
    #bew.show()

    #bied = BirthInfoEditDialog()
    #if bied.exec_() == QDialog.Accepted:
    #    print("Accepted!")
    #    print("BirthInfo accepted is: " + bied.getBirthInfo().toString())
    #else:
    #    print("Rejected!")


    #app.exec_()
    

