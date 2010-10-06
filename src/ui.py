
# For obtaining the line separator.
import os

# For logging.
import logging

from PyQt4.QtCore import QSignalMapper
from PyQt4.QtGui import *

# For icon images, etc.
import resources

# For dialogs for user input.
from dialogs import *

# For data objects manipulated in the ui.
from data_objects import BirthInfo
from data_objects import PriceChartDocumentData

# For widgets used in the ui.
from pricebarchart import *
from pricebarspreadsheet import *


class MainWindow(QMainWindow):
    """The QMainWindow class that is a multiple document interface (MDI)."""

    def __init__(self, appName, appVersion, appDate, parent=None):
        super().__init__(parent)

        self.log = logging.getLogger("ui.MainWindow")

        # Save off the application name, version and date.
        self.appName = appName
        self.appVersion = appVersion
        self.appDate = appDate
        self.appIcon = QIcon(":/images/appIcon.png")
        
        # Initialize the sequence number for untitled documents.
        self.untitledDocSequenceNum = 1

        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        # Maps actions in the window menu to changing active document windows.
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped.connect(self.mdiArea.setActiveSubWindow)

        # Any updates in window activation will update menus.
        self.mdiArea.subWindowActivated.connect(self.updateMenus)

        # Create actions, menus, toolbars, statusbar, widgets, etc.
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.updateMenus()

        self.readSettings()

        self.setWindowTitle(self.appName)
        self.setWindowIcon(self.appIcon)


    def createActions(self):
        """Creates all the QAction objects that will be mapped to the 
        choices on the menu, toolbar and keyboard shortcuts."""

        ####################
        # Create actions for the File Menu.

        # Create the newChartAction.
        self.newChartAction = QAction(QIcon(":/images/new.png"), "&New", self)
        self.newChartAction.setShortcut("Ctrl+n")
        self.newChartAction.setStatusTip("Create a new Chart file")
        self.newChartAction.triggered.connect(self.newChart)

        # Create the openChartAction.
        self.openChartAction = QAction(QIcon(":/images/open.png"), 
                "&Open", self)
        self.openChartAction.setShortcut("Ctrl+o")
        self.openChartAction.setStatusTip("Open an existing Chart file")
        self.openChartAction.triggered.connect(self.openChart)

        # Create the saveChartAction.
        self.saveChartAction = QAction(QIcon(":/images/save.png"), 
                "&Save", self)
        self.saveChartAction.setShortcut("Ctrl+s")
        self.saveChartAction.setStatusTip("Save the Chart to disk")
        self.saveChartAction.triggered.connect(self.saveChart)


        # Create the saveAsChartAction.
        self.saveAsChartAction = QAction("Save &As...", self)
        self.saveAsChartAction.setStatusTip("Save the Chart as a new file")
        self.saveAsChartAction.triggered.connect(self.saveAsChart)

        # Create the exitAppAction.
        self.exitAppAction = QAction("E&xit", self)
        self.exitAppAction.setShortcut("Ctrl+q")
        self.exitAppAction.setStatusTip("Exit the application")
        self.exitAppAction.triggered.connect(self.exitApp)

        ####################
        # Create actions for the Edit Menu.

        # Create the editBirthInfoAction.
        self.editBirthInfoAction = QAction(QIcon(":/images/Edit.png"),
                "&Edit Birth Data", self)
        self.editBirthInfoAction.setStatusTip(
                "Edit the birth time and birth location")
        self.editBirthInfoAction.triggered.connect(self.editBirthInfo)


        # Create the editAppPreferencesAction.
        self.editAppPreferencesAction = QAction(QIcon(":/images/gears.png"), 
                "Edit &Preferences", self)
        self.editAppPreferencesAction.setStatusTip("Edit Preferences")
        self.editAppPreferencesAction.triggered.connect(
                self.editAppPreferences)


        ####################
        # Create actions for the Window menu.

        # Create the closeChartAction.
        self.closeChartAction = QAction("Cl&ose", self)
        self.closeChartAction.setShortcut("Ctrl+F4")
        self.closeChartAction.setStatusTip("Close the active window")
        self.closeChartAction.triggered.connect(
                self.mdiArea.closeActiveSubWindow)

        # Create the closeAllChartsAction.
        self.closeAllChartsAction = QAction("Close &All", self)
        self.closeAllChartsAction.setStatusTip("Close all the windows")
        self.closeAllChartsAction.triggered.connect(
                self.mdiArea.closeAllSubWindows)

        # Create the tileSubWindowsAction.
        self.tileSubWindowsAction = QAction("&Tile", self)
        self.tileSubWindowsAction.setStatusTip("Tile the windows")
        self.tileSubWindowsAction.triggered.connect(
                self.mdiArea.tileSubWindows)

        # Create the cascadeSubWindowsAction.
        self.cascadeSubWindowsAction = QAction("&Cascade", self)
        self.cascadeSubWindowsAction.setStatusTip("Cascade the windows")
        self.cascadeSubWindowsAction.triggered.connect(
                self.mdiArea.cascadeSubWindows)

        # Create the nextSubWindowAction.
        self.nextSubWindowAction = QAction("Ne&xt", self)
        self.nextSubWindowAction.setStatusTip(
                "Move the focus to the next subwindow")
        self.nextSubWindowAction.triggered.connect(
                self.mdiArea.activateNextSubWindow)

        # Create the previousSubWindowAction.
        self.previousSubWindowAction = QAction("Pre&vious", self)
        self.previousSubWindowAction.setStatusTip(
                "Move the focus to the previous subwindow")
        self.previousSubWindowAction.triggered.connect(
                self.mdiArea.activatePreviousSubWindow)

        ####################
        # Create actions for the Help menu.
        self.aboutAction = QAction(self.appIcon, "&About", self)
        self.aboutAction.setStatusTip("Show the application's About box")
        self.aboutAction.triggered.connect(self.about)

    def createMenus(self):
        """Creates the QMenus and adds them to the QMenuBar of the
        QMainWindow"""

        # Create the File menu.
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newChartAction)
        self.fileMenu.addAction(self.openChartAction)
        self.fileMenu.addAction(self.saveChartAction)
        self.fileMenu.addAction(self.saveAsChartAction)
        self.fileMenu.addAction(self.exitAppAction)

        # Create the Edit menu.
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.editBirthInfoAction)
        self.editMenu.addAction(self.editAppPreferencesAction)

        # Create the Window menu.
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.windowMenu.addAction(self.closeChartAction)
        self.windowMenu.addAction(self.closeAllChartsAction)
        self.windowMenu.addAction(self.tileSubWindowsAction)
        self.windowMenu.addAction(self.cascadeSubWindowsAction)
        self.windowMenu.addAction(self.previousSubWindowAction)

        # Add a separator between the Window menu and the Help menu.
        self.menuBar().addSeparator()

        # Create the Help menu.
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)


    def createToolBars(self):
        """Creates the toolbars used in the application"""

        # Create the File toolbar.
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newChartAction)
        self.fileToolBar.addAction(self.openChartAction)
        self.fileToolBar.addAction(self.saveChartAction)

        # Create the Edit toolbar.
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.editBirthInfoAction)
        self.editToolBar.addAction(self.editAppPreferencesAction)

    def createStatusBar(self):
        """Creates the QStatusBar by showing the message "Ready"."""

        self.statusBar().showMessage("Ready")

    def updateMenus(self):
        """Updates the menu by enabling various QActions depending on the
        current state of the application."""

        self.log.debug("Entered updateMenus()")
        print("DEBUG: Entered updateMenus()")

        self.updateFileMenu()
        self.updateEditMenu()
        self.updateWindowMenu()

        self.log.debug("Exiting updateMenus()")


    def updateFileMenu(self):
        """Updates the File menu according to the state of the current
        document.
        """

        self.log.debug("Entered updateFileMenu()")
        # TODO:  write this funciton out.
        self.log.debug("Exiting updateFileMenu()")


    def updateEditMenu(self):
        """Updates the Edit menu according to the state of the current
        document.
        """

        self.log.debug("Entered updateEditMenu()")
        # TODO:  write this funciton out.
        self.log.debug("Exiting updateEditMenu()")

    def updateWindowMenu(self):
        """Updates the Window menu according to which documents are open
        currently.
        """

        self.log.debug("Entered updateWindowMenu()")
        # TODO:  write this funciton out.
        self.log.debug("Exiting updateWindowMenu()")

    def addSubWindow(self, widget):
        """Adds a subwindow to the QMdiArea.  This subwindow is a
        QMdiSubwindow created with the given QWidget 'widget'.
        'widget' may be a QWidget or a QMdiSubWindow.
        After adding the subwindow, the menus are updated appropriately.
        """

        self.log.debug("Entered addSubWindow()")

        mdiSubWindow = self.mdiArea.addSubWindow(widget)
        mdiSubWindow.show()

        # Note: Setting the active window here will also cause updateMenus()
        # to be called, which is what we want.
        self.mdiArea.setActiveSubWindow(mdiSubWindow)

        self.log.debug("Exiting addSubWindow()")



    def readSettings(self):
        self.log.debug("readSettings()")
        pass

    def writeSettings(self):
        self.log.debug("DEBUG: writeSettings()")
        pass

    def newChart(self):
        """Opens a PriceChartDocumentWizard to load information for a new
        price chart.
        """

        self.log.debug("Entered MainWindow.newChart()")

        wizard = PriceChartDocumentWizard()
        returnVal = wizard.exec_() 

        if returnVal == QDialog.Accepted:
            self.log.debug("PriceChartDocumentWizard accepted");

            self.log.debug("Data filename is: " + wizard.field("dataFilename"))
            self.log.debug("Data num lines to skip is: {}".\
                format(wizard.field("dataNumLinesToSkip")))
            self.log.debug("Timezone is: " + wizard.field("timezone"))


            priceChartDocumentData = PriceChartDocumentData()

            priceChartDocumentData.\
                loadWizardData(wizard.field("dataFilename"),
                               wizard.field("dataNumLinesToSkip"),
                               wizard.field("timezone"))

            # Create a PriceChartDocument with the data.
            priceChartDocument = \
                PriceChartDocument(priceChartDocumentData)

            # TODO:  Perhaps title-setting should be done in the
            # PriceChartDocument class itself?  If so, remove
            # self.untitledDocSequenceNum and use a class variable in
            # PriceChartDocument.
            title = "Untitled{}".format(self.untitledDocSequenceNum)
            self.untitledDocSequenceNum += 1
            priceChartDocument.setWindowTitle(title)

            # Add this priceChartDocument to the list of subwindows
            self.addSubWindow(priceChartDocument)
        else:
            self.log.debug("PriceChartDocumentWizard rejected");


        self.log.debug("Exiting MainWindow.newChart()")

    def openChart(self):
        self.log.debug("DEBUG: openChart()")
        pass

    def saveChart(self):
        self.log.debug("DEBUG: saveChart()")
        pass

    def saveAsChart(self):
        self.log.debug("DEBUG: saveAsChart()")
        pass

    def exitApp(self):
        self.log.debug("Entered MainWindow.exitApp()")

        # Hmm, it appears that Alt-F4 does not cause this exitApp function to
        # get called.


        # TODO:  add here some checking to save open unsaved files, and also settings.

        self.log.debug("Exiting MainWindow.exitApp()")
        qApp.closeAllWindows()


    def editBirthInfo(self):
        """Opens up a BirthInfoEditDialog for editing the BirthInfo of the
        current active PriceChartDocument.
        """

        self.log.debug("Entered MainWindow.editBirthInfo()")

        # Get current active PriceChartDocument.
        priceChartDocument = None # TODO: get the active price chart document, error out if none exist.

        # Get the BirthInfo.
        birthInfo = priceChartDocument.priceChartDocumentData.getBirthInfo()

        # Create a dialog to edit the birth info.
        dialog = BirthInfoEditDialog(birthInfo)

        if dialog.exec_() == QDialog.Accepted:
            self.log.debug("BirthInfoEditDialog accepted.  Data is: " + \
                           dialog.getBirthInfo().toString())
            priceChartDocument.priceChartDocumentData.setBirthInfo(birthInfo)
        else:
            self.log.debug("BirthInfoEditDialog rejected. Doing nothing more.")

        self.log.debug("Exiting MainWindow.editBirthInfo()")


    def editAppPreferences(self):
        self.log.debug("DEBUG: editAppPreferences()")
        pass


    def about(self):
        self.log.debug("DEBUG: about()")

        endl = os.linesep

        title = "About"

        message = self.appName + endl + \
                  endl + \
                  "Version: " + self.appVersion + endl + \
                  "Released: " + self.appDate + endl + \
                  endl + \
                  "Author: Ryan Luu" + endl + \
                  "Email: ryanluu@gmail.com"

        QMessageBox.about(self, title, message);

        pass



class PriceChartDocument(QMdiSubWindow):
    """QMdiSubWindow in the QMdiArea.  This window allows a user to 
    view and edit the data contained in a PriceChartDocumentData object.
    """

    def __init__(self, 
                 priceChartDocumentData=PriceChartDocumentData(), 
                 parent=None):
        """Creates the QMdiSubWindow with the internal widgets,
        and loads the given PriceChartDocumentData object.
        """
        super().__init__(parent)

        self.log = logging.getLogger("ui.PriceChartDocument")
        self.log.debug("Entered PriceChartDocument()")

        self.widgets = PriceChartDocumentWidget()
        self.setWidget(self.widgets)

        # According to the Qt QMdiArea documentation:
        # 
        #   When you create your own subwindow, you must set the
        #   Qt.WA_DeleteOnClose  widget attribute if you want the window to
        #   be deleted when closed in the MDI area. If not, the window will
        #   be hidden and the MDI area will not activate the next subwindow.
        #
        self.setAttribute(Qt.WA_DeleteOnClose);

        self.loadPriceChartDocumentData(priceChartDocumentData)

        self.log.debug("Exiting PriceChartDocument()")

    def getPriceChartDocumentData(self):
        """Obtains all the data in the widgets and puts it into the
        internal PriceChartDocumentData object, then returns that object.
        """
        self.log.\
            debug("Entered PriceChartDocument.getPriceChartDocumentData()")

        # TODO:  write this method.

        self.log.\
            debug("Exiting PriceChartDocument.getPriceChartDocumentData()")

    def loadPriceChartDocumentData(self, priceChartDocumentData):
        """Stores the PriceChartDocumentData and sets the widgets with the
        information it requires.
        """

        self.log.\
            debug("Entered PriceChartDocument.loadPriceChartDocumentData()")

        self.priceChartDocumentData = priceChartDocumentData
        # TODO:  write this method.

        self.log.\
            debug("Exiting PriceChartDocument.loadPriceChartDocumentData()")
        

class PriceChartDocumentWidget(QWidget):
    """Internal widget within a PriceChartDocument (QMdiSubWindow) that
    holds all the other widgets.  This basically serves as a QLayout
    for the PriceChartDocument.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger("ui.PriceChartDocumentWidget")

        # Create the internal widgets displayed.
        self.priceBarChartWidget = PriceBarChartWidget()
        self.priceBarSpreadsheetWidget = PriceBarSpreadsheetWidget()

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.priceBarChartWidget)
        layout.addWidget(self.priceBarSpreadsheetWidget)
        self.setLayout(layout)
        
