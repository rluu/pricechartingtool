#!/usr/bin/env python3


# For directory access.
import os
import sys

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

        # TODO:  eventually remove setting the QWizard style.  This is here just for testing what all the views would look like.
        # Set the QWizard style.
        #self.setWizardStyle(QWizard.ClassicStyle)
        #self.setWizardStyle(QWizard.ModernStyle)
        #self.setWizardStyle(QWizard.MacStyle)
        #self.setWizardStyle(QWizard.AeroStyle)

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

        self.setTitle("Loading Price Data")
        self.setSubTitle(" ")

        # Create the contents.

        # Informational labels.
        self.descriptionLabel = \
            QLabel("Please select a file for loading price data." + \
                   os.linesep + os.linesep + \
                   "The selected file must be a CSV data file with the " + \
                   "data fields in the following format: ")
        self.descriptionLabel.setWordWrap(True)

        fileInfoDataDescStr = \
                      "<MM/DD/YYYY>," + \
                      "<OpenPrice>,<HighPrice>,<LowPrice>,<ClosePrice>," + \
                      "<Volume>,<OpenInterest>" + os.linesep
        self.fileInfoLabel = QLabel(fileInfoDataDescStr)


        # Frame as a separator.
        self.sep = QFrame()
        self.sep.setFrameShape(QFrame.HLine)
        self.sep.setFrameShadow(QFrame.Sunken)

        # Filename selection widgets.
        self.filenameLabel = QLabel("Filename:")
        self.filenameLineEdit = QLineEdit()
        self.browseButton = QPushButton(QIcon(":/images/open.png"), "Browse")

        fileBrowseLayout = QHBoxLayout()
        fileBrowseLayout.addWidget(self.filenameLineEdit)
        fileBrowseLayout.addWidget(self.browseButton)


        # Lines skipped selection widgets.
        self.skipLinesLabel = QLabel("Number of lines to skip before reading data:")
        self.skipLinesSpinBox = QSpinBox()
        self.skipLinesSpinBox.setMinimum(0)
        self.skipLinesSpinBox.setValue(1)

        skipLinesLayout = QHBoxLayout()
        skipLinesLayout.addWidget(self.skipLinesLabel)
        skipLinesLayout.addWidget(self.skipLinesSpinBox)
        skipLinesLayout.addStretch()

        # TODO:  add a few more widgets here.
        # TODO:  connect any changes in the widgets to attempt to load the table view widget.  If there are errors (file not found) or (invalid data type in data field), display it in red words right above the table view widget.


        # Register the fields.
        self.registerField("dataFilename*", self.filenameLineEdit)
        self.registerField("dataNumLinesToSkip*", self.skipLinesSpinBox)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.descriptionLabel)
        layout.addWidget(self.fileInfoLabel)
        layout.addWidget(self.sep)
        layout.addWidget(self.filenameLabel)
        layout.addLayout(fileBrowseLayout)
        layout.addLayout(skipLinesLayout)
        self.setLayout(layout)

    def populateTableView(self):
        # TODO:  write this function.
        pass

    def validatePage(self):
        # TODO:  write this function.
        pass


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
    

