
# For logging.
import logging

from PyQt4.QtCore import QSignalMapper
from PyQt4.QtGui import *

# For icon images, etc.
import resources


class MainWindow(QMainWindow):
    """The QMainWindow class that is a multiple document interface (MDI)."""

    def __init__(self, appName, appVersion, appDate, parent=None):
        super(MainWindow, self).__init__(parent)

        self.log = logging.getLogger("ui.MainWindow")

        # Save off the application name, version and date.
        self.appName = appName
        self.appVersion = appVersion
        self.appDate = appDate
        self.appIcon = QIcon(":/images/appIcon.png")
        
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

        # Create the editBirthDataAction.
        self.editBirthDataAction = QAction(QIcon(":/images/Edit.png"),
                "&Edit Birth Data", self)
        self.editBirthDataAction.setShortcut("Ctrl+e")
        self.editBirthDataAction.setStatusTip(
                "Edit the name, birth time, and birth place")
        self.editBirthDataAction.triggered.connect(self.editBirthData)


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
        self.editMenu.addAction(self.editBirthDataAction)
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
        self.editToolBar.addAction(self.editBirthDataAction)
        self.editToolBar.addAction(self.editAppPreferencesAction)

    def createStatusBar(self):
        """Creates the QStatusBar by showing the message "Ready"."""

        self.statusBar().showMessage("Ready")

    def updateMenus(self):
        """Updates the menu by enabling various QActions depending on the
        current state of the application."""

        self.log.debug("updateMenus()")
        # TODO:  write this funciton out.

    def readSettings(self):
        self.log.debug("readSettings()")
        pass

    def writeSettings(self):
        self.log.debug("DEBUG: writeSettings()")
        pass

    def newChart(self):
        self.log.debug("DEBUG: newChart()")
        pass

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
        self.log.debug("DEBUG: exitApp()")

        # Hmm, it appears that Alt-F4 does not cause this exitApp function to
        # get called.


        # TODO:  add here some checking to save open unsaved files, and also settings.

        qApp.closeAllWindows()

    def editBirthData(self):
        self.log.debug("DEBUG: editBirthData()")
        pass


    def editAppPreferences(self):
        self.log.debug("DEBUG: editAppPreferences()")
        pass


    def about(self):
        self.log.debug("DEBUG: about()")
        pass


class NewPriceChartDocumentDialog(QDialog):
    """Dialog for creating a new PriceChartDocument."""

    def __init__(self, parent=None, f=None):
        self.log.debug("DEBUG: setting up NewChartDialog")
        pass


class PriceChartDocument(QMdiSubWindow):
    """QMdiSubWindow in the QMdiArea.  This window allows a user to 
    view and edit the data contained in a PriceChartDocumentData object.
    """

