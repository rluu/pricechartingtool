#!/usr/bin/env python3


# For directory and file access.
import os
import sys
import io


# For logging.
import logging
import logging.config

# For PyQt UI classes.
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import image resources.
import resources

class PriceChartDocumentWizard(QWizard):
    """QWizard for creating a new PriceChartDocument."""

    def __init__(self, parent=None):
        """Creates and sets up a QWizard for creating a new 
        PriceChartDocument."""

        super().__init__(parent)
        #super().__init__(self, parent, f)
        #super(PriceChartDocumentWizard, self).__init__(parent)

        # Logger object for this class.
        self.log = logging.getLogger("dialogs.PriceChartDocumentWizard")

        # Add QWizardPages.
        self.addPage(PriceChartDocumentIntroWizardPage())
        self.addPage(PriceChartDocumentLoadDataFileWizardPage())
        self.addPage(PriceChartDocumentConclusionWizardPage())

        # Set the pictures used in the QWizard.
        watermarkPic = QPixmap(":/images/HowToMakeProfitsInCommodities.png")
        backgroundPic = QPixmap(":/images/HowToMakeProfitsInCommodities.png")
        logoPic = QPixmap(":/images/logo_ryan_d1.png").scaled(64, 64)
        bannerPic = QPixmap(":/images/banners/grad23.gif").scaled(640, 72)

        self.setPixmap(QWizard.WatermarkPixmap, watermarkPic)
        self.setPixmap(QWizard.BackgroundPixmap, backgroundPic)
        self.setPixmap(QWizard.LogoPixmap, logoPic)
        self.setPixmap(QWizard.BannerPixmap, bannerPic)

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

        # Validated flag that indicates the file and number of 
        # lines skipped is valid.
        self.validatedFlag = False


        # Set the title strings.
        self.setTitle("Loading Price Data")
        self.setSubTitle(" ")

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
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setFrameShadow(QFrame.Sunken)
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setFrameShadow(QFrame.Sunken)
        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        sep3.setFrameShadow(QFrame.Sunken)

        # Filename selection widgets.
        filenameLabel = QLabel("Filename:")
        self.filenameLineEdit = QLineEdit()
        self.filenameLineEdit.setReadOnly(True)
        self.browseButton = QPushButton(QIcon(":/images/open.png"), "Br&owse")

        fileBrowseLayout = QHBoxLayout()
        fileBrowseLayout.addWidget(self.filenameLineEdit)
        fileBrowseLayout.addWidget(self.browseButton)

        self.filePreviewLabel = QLabel("File Preview:")
        self.textViewer = QPlainTextEdit()
        self.textViewer.setReadOnly(True)
        self.textViewer.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Lines skipped selection widgets.
        self.skipLinesLabel = QLabel("N&umber of lines to skip before reading data:")
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
        font = self.validationStatusLabel.font()
        font.setPointSize(6)
        self.validationStatusLabel.setFont(font)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(descriptionLabel)
        layout.addWidget(fileInfoLabel)
        layout.addWidget(sep1)
        layout.addWidget(filenameLabel)
        layout.addLayout(fileBrowseLayout)
        layout.addWidget(self.filePreviewLabel)
        layout.addWidget(self.textViewer)
        layout.addLayout(skipLinesLayout)
        layout.addWidget(sep2)
        layout.addLayout(validateLayout)
        layout.addWidget(self.validationStatusLabel)
        self.setLayout(layout)

        # Register the fields.
        self.registerField("dataFilename*", self.filenameLineEdit)
        self.registerField("dataNumLinesToSkip*", self.skipLinesSpinBox)

        # Connect signals and slots.
        self.filenameLineEdit.textChanged.\
            connect(self.handleFilenameLineEditChanged)
        self.skipLinesSpinBox.valueChanged.\
            connect(self.handleSkipLinesSpinBoxChanged)
        self.browseButton.clicked.\
            connect(self.handleBrowseButtonClicked)
        self.validateButton.clicked.\
            connect(self.handleValidateButtonClicked)

    def handleFilenameLineEditChanged(self, filename):
        """Sets that the information entered has not been validated.
        """

        if (self.validatedFlag != False):
            self.validatedFlag = False
            self.completeChanged.emit()

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
                    errMsgDialog = QErrorMessage(self)
                    errMsgDialog.setWindowTitle("Error reading file")
                    errMsgDialog.showMessage(errStr)
                    self.filenameLineEdit.setText("")
                    self.textViewer.setPlainText("")
                except IOError as e:
                    errStr = "I/O Error while trying to read file '" + \
                        filename + "':" + os.linesep + e
                    self.log.error(errStr)
                    errMsgDialog = QErrorMessage(self)
                    errMsgDialog.setWindowTitle("Error reading file")
                    errMsgDialog.showMessage(errStr)
                    self.filenameLineEdit.setText("")
                    self.textViewer.setPlainText("")


    def handleSkipLinesSpinBoxChanged(self):
        """Sets that the information entered has not been validated.
        The validatedFlag is set to False, and the QTableView is cleared.
        """

        if (self.validatedFlag != False):
            self.validatedFlag = False
            self.completeChanged.emit()

    def handleBrowseButtonClicked(self):
        """Opens a QFileDialog for selecting a file.  If a file is selected,
        self.filenameLineEdit will be populated with the selected filename.
        """

        self.log.debug("Entering handleBrowseButtonClicked()")

        # Create a file dialog.
        dialog = QFileDialog();

        # Setup file filters.
        filters = QStringList()
        csvTextFilesFilter = "Text files (*.txt)"
        allFilesFilter = "All files (*)"
        filters.append(csvTextFilesFilter)
        filters.append(allFilesFilter)

        # Apply settings to the dialog.
        dialog.setFileMode(QFileDialog.ExistingFile);
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(csvTextFilesFilter)

        # Run the dialog.
        if dialog.exec() == QDialog.Accepted:
            # Get the selected files.
            selectedFiles = dialog.selectedFiles()
            if selectedFiles.isEmpty() == False:
                # Set the QLineEdit with the filename.
                self.filenameLineEdit.setText(selectedFiles.first())

        self.log.debug("Leaving handleBrowseButtonClicked()")

    def handleValidateButtonClicked(self):
        """Opens the filename in self.filenameLineEdit and tries to validate
        that the file is a text file and has the expected fields.  
        It also populates the QTableView with the data found in the file.
        """

        # Assume a valid file unless it's not.
        validFlag = True
        self.validationStatusLabel.setText("")

        # Get the fields from which we'll get info to read the file with.
        # Here casting to Python str type is required because QLineEdits return
        # QString, not str.
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
                    i = 0
                    for line in file:
                        if i >= numLinesToSkip:
                            (lineValid, reason) = self.validateLine(line)
                            if lineValid == False:
                                validFlag = False
                                validationStr = \
                                    "Validation failed on line " + \
                                    "{} because: {}".format(i+1, reason)
                                self.log.warn(validationStr)
                                validationStr = self.toRedString(validationStr)
                                self.validationStatusLabel.\
                                    setText(validationStr)
                                break
                        i += 1

                except IOError as e:
                    errStr = "I/O Error while trying to read file '" + \
                        filename + "':" + os.linesep + e
                    self.log.error(errStr)
                    errMsgDialog = QErrorMessage(self)
                    errMsgDialog.setWindowitle("Error reading file")
                    errMsgDialog.showMessage(errStr)

                    validationStr = \
                        "Validation failed due to a I/O error.  " + \
                        "Please try again later."
                    self.log.error(validationStr)
                    validationStr = self.toRedString(validationStr)
                    self.validationStatusLabel.setText(validationStr)

        # If the validFlag is still True, then allow the user to 
        # click the 'Next' button.
        if validFlag == True:
            validationStr = "Validated data file {}".format(filename)
            self.log.info(validationStr)
            validationStr = self.toGreenString(validationStr)
            self.validationStatusLabel.setText(validationStr)
            self.validatedFlag = True
            self.completeChanged.emit()

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

        # Empty lines are considered valid.
        if line.strip() == "":
            return (True, "")

        # Check the number of fields.
        fields = line.split(",")
        if len(fields) != 7:
            return (False, "Line does not have enough data fields.")

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

    def isComplete(self):
        """Returns True if validation succeeded, otherwise returns False.
        This function overrides the QWizardPage.isComplete() virtual
        function.
        """

        return self.validatedFlag



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



# For debugging the module during development.  
if __name__=="__main__":
    # Initialize Logging for the Ephemeris class (required).
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)

    wizard = PriceChartDocumentWizard()
    wizard.show()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    app.exec_()
    

