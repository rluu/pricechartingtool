
# For obtaining the line separator and directory separator.
import os

# For serializing and unserializing objects.
import pickle

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

    # Filter for opening files of all types of file extensions.
    allFilesFileFilter = "All files (*)"

    # Default timeout for showing a message in the QStatusBar.
    defaultStatusBarMsgTimeMsec = 4000

    
    def __init__(self, 
                 appName, 
                 appVersion, 
                 appDate, 
                 appAuthor,
                 appAuthorEmail, 
                 parent=None):
        super().__init__(parent)

        self.log = logging.getLogger("ui.MainWindow")

        # Save off the application name, version and date.
        self.appName = appName
        self.appVersion = appVersion
        self.appDate = appDate
        self.appAuthor = appAuthor
        self.appAuthorEmail = appAuthorEmail
        self.appIcon = QIcon(":/images/rluu/appIcon.png")
        
        # Set application details so the we can use QSettings default
        # constructor later.
        QCoreApplication.setOrganizationName(appAuthor)
        QCoreApplication.setApplicationName(appName)

        # Settings attributes that are set when _readSettings() is called.
        self.defaultPriceBarDataOpenDirectory = ""
        self.windowGeometry = QByteArray()
        self.windowState = QByteArray()

        # Create and set up the widgets.
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        # Maps actions in the window menu to changing active document windows.
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.mdiArea.setActiveSubWindow)

        # Any updates in window activation will update action objects and
        # the window menu.
        self.mdiArea.subWindowActivated.connect(self._updateActions)
        self.mdiArea.subWindowActivated.connect(self._updateWindowMenu)

        # Create actions, menus, toolbars, statusbar, widgets, etc.
        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()

        self._updateActions()
        self._updateWindowMenu()

        self._readSettings()

        self.restoreGeometry(self.windowGeometry)
        self.restoreState(self.windowState)

        self.setWindowTitle(self.appName)
        self.setWindowIcon(self.appIcon)


    def _createActions(self):
        """Creates all the QAction objects that will be mapped to the 
        choices on the menu, toolbar and keyboard shortcuts."""

        ####################
        # Create actions for the File Menu.

        # Create the newChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-new.png")
        self.newChartAction = QAction(icon, "&New", self)
        self.newChartAction.setShortcut("Ctrl+n")
        self.newChartAction.setStatusTip("Create a new Chart file")
        self.newChartAction.triggered.connect(self._newChart)

        # Create the openChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-open.png")
        self.openChartAction = QAction(icon, "&Open", self)
        self.openChartAction.setShortcut("Ctrl+o")
        self.openChartAction.setStatusTip("Open an existing Chart file")
        self.openChartAction.triggered.connect(self._openChart)

        # The closeChartAction is used in the File menu, but created below
        # in the section for the Window menu.

        # Create the saveChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-save.png")
        self.saveChartAction = QAction(icon, "&Save", self)
        self.saveChartAction.setShortcut("Ctrl+s")
        self.saveChartAction.setStatusTip("Save the Chart to disk")
        self.saveChartAction.triggered.connect(self._saveChart)

        # Create the saveAsChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-save-as.png")
        self.saveAsChartAction = QAction(icon, "Save &As...", self)
        self.saveAsChartAction.setStatusTip("Save the Chart as a new file")
        self.saveAsChartAction.triggered.connect(self._saveAsChart)

        # Create the printAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-print.png")
        self.printAction = QAction(icon, "&Print", self)
        self.printAction.setShortcut("Ctrl+p")
        self.printAction.setStatusTip("Print the Chart")
        self.printAction.triggered.connect(self._print)

        # Create the printPreviewAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/document-print-preview.png")
        self.printPreviewAction = QAction(icon, "Print Pre&view", self)
        self.printPreviewAction.\
            setStatusTip("Preview the document before printing")
        self.printPreviewAction.triggered.connect(self._printPreview)

        # Create the exitAppAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/system-log-out.png")
        self.exitAppAction = QAction(icon, "E&xit", self)
        self.exitAppAction.setShortcut("Ctrl+q")
        self.exitAppAction.setStatusTip("Exit the application")
        self.exitAppAction.triggered.connect(self._exitApp)

        ####################
        # Create actions for the Edit Menu.

        # Create the editBirthInfoAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/apps/internet-web-browser.png")
        self.editBirthInfoAction = QAction(icon, "&Edit Birth Data", self)
        self.editBirthInfoAction.setStatusTip(
                "Edit the birth time and birth location")
        self.editBirthInfoAction.triggered.connect(self._editBirthInfo)


        # Create the editAppPreferencesAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/categories/preferences-system.png")
        self.editAppPreferencesAction = \
            QAction(icon, "Edit &Preferences", self)
        self.editAppPreferencesAction.setStatusTip("Edit Preferences")
        self.editAppPreferencesAction.triggered.\
            connect(self._editAppPreferences)


        ####################
        # Create actions for the Window menu.

        # Create the closeChartAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/status/image-missing.png")
        self.closeChartAction = QAction(icon, "&Close", self)
        self.closeChartAction.setShortcut("Ctrl+F4")
        self.closeChartAction.setStatusTip("Close the active window")
        self.closeChartAction.triggered.connect(self._closeChart)

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
        self.cascadeSubWindowsAction = QAction("Ca&scade", self)
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

        # Create a separator for the Window menu.
        self.windowMenuSeparator = QAction(self)
        self.windowMenuSeparator.setSeparator(True)

        # Create a QActionGroup for the list of windows.
        self.windowMenuActionGroup = QActionGroup(self)
        self.windowMenuActionGroup.setExclusive(True)

        ####################
        # Create actions for the Help menu.
        self.aboutAction = QAction(self.appIcon, "&About", self)
        self.aboutAction.\
            setStatusTip("Show information about this application.")
        self.aboutAction.triggered.connect(self._about)

        self.aboutQtAction = \
            QAction(QIcon(":/images/qt/qt-logo.png"), "About &Qt", self)
        self.aboutQtAction.setStatusTip("Show information about Qt.")
        self.aboutQtAction.triggered.connect(self._aboutQt)


    def _createMenus(self):
        """Creates the QMenus and adds them to the QMenuBar of the
        QMainWindow"""

        # Create the File menu.
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newChartAction)
        self.fileMenu.addAction(self.openChartAction)
        self.fileMenu.addAction(self.closeChartAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveChartAction)
        self.fileMenu.addAction(self.saveAsChartAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.printPreviewAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAppAction)

        # Create the Edit menu.
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.editBirthInfoAction)
        self.editMenu.addAction(self.editAppPreferencesAction)

        # Create the Window menu.
        self.windowMenu = self.menuBar().addMenu("&Window")
        self._updateWindowMenu()

        # Add a separator between the Window menu and the Help menu.
        self.menuBar().addSeparator()

        # Create the Help menu.
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)


    def _createToolBars(self):
        """Creates the toolbars used in the application"""

        # Create the File toolbar.
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setObjectName("fileToolBar")
        self.fileToolBar.addAction(self.newChartAction)
        self.fileToolBar.addAction(self.openChartAction)
        self.fileToolBar.addAction(self.saveChartAction)
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.printAction)
        self.fileToolBar.addAction(self.printPreviewAction)

        # Create the Edit toolbar.
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.setObjectName("editToolBar")
        self.editToolBar.addAction(self.editBirthInfoAction)
        self.editToolBar.addAction(self.editAppPreferencesAction)

    def _createStatusBar(self):
        """Creates the QStatusBar by showing the message "Ready"."""

        self.statusBar().showMessage("Ready")

    def _updateActions(self):
        """Updates the QActions (enable or disable) depending on the
        current state of the application."""

        self.log.debug("Entered _updateActions()")

        priceChartDocument = self.getActivePriceChartDocument()

        # Flag for whether or not a PriceChartDocument is active or not.
        # Initialize to False.
        isActive = False

        if priceChartDocument == None:
            isActive = False
            self.log.debug("Currently active subwindow is: None")
        else:
            isActive = True
            self.log.debug("Currently active subwindow title is: " + 
                           priceChartDocument.title)

        # Set the QActions according to whether it is always True, always
        # False, or dependent on whether a PriceChartDocument is selected.
        self.newChartAction.setEnabled(True)
        self.openChartAction.setEnabled(True)

        self.saveChartAction.setEnabled(isActive)
        self.saveAsChartAction.setEnabled(isActive)
        self.printAction.setEnabled(isActive)
        self.printPreviewAction.setEnabled(isActive)

        self.exitAppAction.setEnabled(True)

        self.editBirthInfoAction.setEnabled(isActive)

        self.editAppPreferencesAction.setEnabled(True)

        self.closeChartAction.setEnabled(isActive)
        self.closeAllChartsAction.setEnabled(isActive)
        self.tileSubWindowsAction.setEnabled(isActive)
        self.cascadeSubWindowsAction.setEnabled(isActive)
        self.nextSubWindowAction.setEnabled(isActive)
        self.previousSubWindowAction.setEnabled(isActive)

        self.aboutAction.setEnabled(True)
        self.aboutQtAction.setEnabled(True)

        self.log.debug("Exiting _updateActions()")

    def _updateWindowMenu(self):
        """Updates the Window menu according to which documents are open
        currently.
        """

        self.log.debug("Entered _updateWindowMenu()")

        for action in self.windowMenuActionGroup.actions():
            self.windowMenuActionGroup.removeAction(action)

        # Clear the Window menu and re-add all the standard actions that
        # always show up.
        self.windowMenu.clear()

        self.windowMenu.addAction(self.nextSubWindowAction)
        self.windowMenu.addAction(self.previousSubWindowAction)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.closeChartAction)
        self.windowMenu.addAction(self.closeAllChartsAction)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileSubWindowsAction)
        self.windowMenu.addAction(self.cascadeSubWindowsAction)
        self.windowMenu.addAction(self.windowMenuSeparator)

        # Get the list of subwindows.
        subwindows = self.mdiArea.subWindowList()

        if len(subwindows) > 0:
            self.windowMenuSeparator.setVisible(True)
        else:
            self.windowMenuSeparator.setVisible(False)

        # j is the counter for the document list in the Menu.
        j = 1

        # i is the index into the subwindows available.
        # Some of these subwindows may not be PriceChartDocuments, or
        # things we know how to get a name/title/filename for.
        for i in range(len(subwindows)):
            subwindow = subwindows[i]

            # Number windows only if it is a PriceChartDocument.
            if isinstance(subwindow, PriceChartDocument) == True:
                priceChartDocument = subwindow

                # Build the text that will go in the menu's QAction.
                # Here we will have a short-cut (underscore) only if
                # the window count is single digits.
                text = ""
                if j < 10:
                    text += "&"
                text += "{} {}".format(j, priceChartDocument.title)

                # Create the action.
                action = QAction(text, self)
                action.setCheckable(True)

                # Add the action to the QActionGroup.
                self.windowMenuActionGroup.addAction(action)

                # Add the action to the menu.
                self.windowMenu.addAction(action)

                # Set the action as checked if it is the active
                # PriceChartDocument.
                if priceChartDocument == self.getActivePriceChartDocument():
                    action.setChecked(True)
                else:
                    action.setChecked(False)

                # Add the action to the signal mapper that will connect
                # this action being triggered to the related 
                # priceChartDocument.
                self.windowMapper.setMapping(action, priceChartDocument)
                action.triggered.connect(self.windowMapper.map)
                
                # Increment counter for the window number in the Window menu.
                j += 1
            else:
                self.log.debug("Currently only supporting windows that " + 
                               "are PriceChartDocument types only.")

        self.log.debug("Exiting _updateWindowMenu()")

    def _addSubWindow(self, widget):
        """Adds a subwindow to the QMdiArea.  This subwindow is a
        QMdiSubwindow created with the given QWidget 'widget'.
        'widget' may be a QWidget or a QMdiSubWindow.
        After adding the subwindow, the menus are updated appropriately.
        """

        self.log.debug("Entered _addSubWindow()")

        mdiSubWindow = self.mdiArea.addSubWindow(widget)
        mdiSubWindow.show()

        # Set the active subwindow so that subsequent update functions can
        # be called via signals-and-slots.
        self.mdiArea.setActiveSubWindow(mdiSubWindow)

        self.log.debug("Exiting _addSubWindow()")

    def getActivePriceChartDocument(self):
        """Returns a reference to the currently selected
        PriceChartDocument.  If no PriceChartDocument is selected 
        (nothing selected, or some other kind of document selected), 
        then None is returned.
        """

        subwindow = self.mdiArea.currentSubWindow()

        if isinstance(subwindow, PriceChartDocument) == True:
            return subwindow
        else:
            return None


    def _readSettings(self):
        """
        Reads in QSettings values for preferences and default values.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Entered _readSettings()")

        # Preference settings.
        settings = QSettings() 

        # Window geometry.
        self.windowGeometry = \
            settings.value("ui/MainWindow/windowGeometry")
        if self.windowGeometry == None:
            self.windowGeometry = QByteArray()
            
        # Window state.
        self.windowState = \
            settings.value("ui/MainWindow/windowState")
        if self.windowState == None:
            self.windowState = QByteArray()


        self.log.debug("Exiting _readSettings()")

    def _writeSettings(self):
        """
        Writes current settings values to the QSettings object.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Entered _writeSettings()")

        # Preference settings.
        settings = QSettings() 

        # Only write the settings if the value has changed.

        # Window geometry.
        if settings.value("ui/MainWindow/windowGeometry") != \
                self.saveGeometry():

            settings.setValue("ui/MainWindow/windowGeometry", 
                              self.saveGeometry())

        # Window state.
        if settings.value("ui/MainWindow/windowState") != self.saveState():
            settings.setValue("ui/MainWindow/windowState", self.saveState())


        self.log.debug("Exiting _writeSettings()")

    def _newChart(self):
        """Opens a PriceChartDocumentWizard to load information for a new
        price chart.
        """

        self.log.debug("Entered _newChart()")

        wizard = PriceChartDocumentWizard()
        returnVal = wizard.exec_() 

        if returnVal == QDialog.Accepted:
            self.log.debug("PriceChartDocumentWizard accepted")

            self.log.debug("Data filename is: " + \
                           wizard.field("dataFilename"))

            self.log.debug("Data num lines to skip is: {}".\
                format(wizard.field("dataNumLinesToSkip")))

            self.log.debug("Timezone is: " + wizard.field("timezone"))


            priceChartDocumentData = PriceChartDocumentData()

            priceChartDocumentData.\
                loadWizardData(wizard.getPriceBars(),
                               wizard.field("dataFilename"),
                               wizard.field("dataNumLinesToSkip"),
                               wizard.field("timezone"))

            # Create a PriceChartDocument with the data.
            priceChartDocument = PriceChartDocument()
            priceChartDocument.\
                setPriceChartDocumentData(priceChartDocumentData)

            # Connect the signal for updating the status bar message.
            priceChartDocument.statusMessageUpdate[str].\
                connect(self.showInStatusBar)

            # Add this priceChartDocument to the list of subwindows
            self._addSubWindow(priceChartDocument)

        else:
            self.log.debug("PriceChartDocumentWizard rejected")


        self.log.debug("Exiting _newChart()")

    def _openChart(self):
        """Interactive dialogs to open an existing PriceChartDocument.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Entered _openChart()")

        # Set filters for what files are displayed.
        filters = \
            PriceChartDocument.fileFilter + ";;" + \
            MainWindow.allFilesFileFilter

        # Directory location default for the file open dialogs for
        # PriceChartDocument.
        settings = QSettings()
        defaultPriceChartDocumentOpenDirectory = \
            settings.value("ui/defaultPriceChartDocumentOpenDirectory", "")

        filename = \
            QFileDialog.\
                getOpenFileName(self, 
                                "Open PriceChartDocument File",
                                defaultPriceChartDocumentOpenDirectory,
                                filters)

        if filename != "":
            # Okay, so the person chose a file that is non-empty.  
            # See if this filename has already been opened in another
            # PriceChartDocument.  If this is so, prompt to make sure the
            # user wants to open two PriceChartDocuments that point to the
            # same file.  
            filenameAlreadyOpened = False

            # Get the list of subwindows.
            subwindows = self.mdiArea.subWindowList()

            # i is the index into the subwindows available.
            # Some of these subwindows may not be PriceChartDocuments, or
            # things we know how to get a name/title/filename for.
            for i in range(len(subwindows)):
                subwindow = subwindows[i]

                if isinstance(subwindow, PriceChartDocument) == True:
                    priceChartDocument = subwindow

                    if priceChartDocument.filename == filename:
                        filenameAlreadyOpened = True

            if filenameAlreadyOpened == True:
                # Prompt to make sure the user wants to open
                # another PriceChartDocument with the same
                # filename.
                title = "File Already Open"
                text = "The filename you have selected is already open " + \
                       "in another subwindow." + os.linesep + os.linesep + \
                       "Do you still want to open this file?"
                buttons = (QMessageBox.Yes | QMessageBox.No)
                defaultButton = QMessageBox.No

                buttonClicked = \
                    QMessageBox.warning(self, title, text, buttons, 
                                        defaultButton)

                if buttonClicked == QMessageBox.No:
                    # The user doesn't want to load this file.
                    # Exit this function.
                    return
            
            # Load the file.

            # Create the subwindow.
            priceChartDocument = PriceChartDocument()

            # Try to load the file data into the subwindow.
            loadSuccess = \
                priceChartDocument.\
                    unpicklePriceChartDocumentDataFromFile(filename)

            if loadSuccess == True:
                # Load into the object was successful.  

                # Connect the signal for updating the status bar message.
                priceChartDocument.statusMessageUpdate[str].\
                    connect(self.showInStatusBar)

                # Now Add this priceChartDocument to the list of subwindows
                self._addSubWindow(priceChartDocument)

                # Update the statusbar to tell what file was opened.
                statusBarMessage = \
                    "Opened PriceChartDocument {}.".format(filename)

                self.showInStatusBar(statusBarMessage)

                # Get the directory where this file lives.
                loc = filename.rfind(os.sep)
                directory = filename[:loc]

                # Compare the directory of the file chosen with the
                # QSettings value for the default open location.  
                # If they are different, then set a new default.
                if directory != defaultPriceChartDocumentOpenDirectory:
                    settings.\
                        setValue("ui/defaultPriceChartDocumentOpenDirectory",
                                 directory)
            else:
                # Load failed.  Tell the user via the statusbar.
                statusBarMessage = \
                    "Open operation failed.  " + \
                    "Please see the log file for why."

                self.showInStatusBar(statusBarMessage)
        else:
            self.log.debug("_openChart(): " +
                           "No filename was selected for opening.")

        self.log.debug("Exiting _openChart()")

    def _closeChart(self):
        """Attempts to closes the current QMdiSubwindow.  If things should
        be saved, dialogs will be brought up to get that to happen.
        """

        self.log.debug("Entered _closeChart()")

        subwindow = self.mdiArea.currentSubWindow()

        subwindow.close()

        self.log.debug("Exiting _closeChart()")

    def _saveChart(self):
        """Saves the current QMdiSubwindow.
        
        Returns True if the save action suceeded, False otherwise.
        """

        self.log.debug("Entered _saveChart()")

        # Return value.
        rv = False

        subwindow = self.mdiArea.currentSubWindow()

        if isinstance(subwindow, PriceChartDocument) == True:
            priceChartDocument = subwindow

            rv = priceChartDocument.saveChart()
        else:
            self.log.warn("Saving this QMdiSubwindow type is not supported.")
            rv = False
            
        self.log.debug("Exiting _saveChart() with rv == {}".format(rv))
        return rv

    def _saveAsChart(self):
        """Saves the current QMdiSubwindow to a new file.
        
        Returns True if the save action suceeded, False otherwise.
        """

        self.log.debug("Entered _saveAsChart()")

        # Return value.
        rv = False

        subwindow = self.mdiArea.currentSubWindow()

        if isinstance(subwindow, PriceChartDocument) == True:
            priceChartDocument = subwindow

            rv = priceChartDocument.saveAsChart()
        else:
            self.log.warn("'Save As' for this QMdiSubwindow type " + 
                          "is not supported.")
            rv = False
            
        self.log.debug("Exiting _saveAsChart() with rv == {}".format(rv))
        return rv

    def showInStatusBar(self, text):
        """Shows the given text in the MainWindow status bar for
        timeoutMSec milliseconds.
        """

        self.statusBar().showMessage(text, 
                                     MainWindow.defaultStatusBarMsgTimeMsec)

    def _print(self):
        """Opens up a dialog for printing the current selected document."""

        self.log.debug("Entered _print()")
        # TODO: write this function.
        QMessageBox.information(self, 
                                "Not yet implemented", 
                                "This feature has not yet been implemented.")
        self.log.debug("Exiting _print()")


    def _printPreview(self):
        """Opens up a dialog for previewing the current selected document
        for printing.
        """

        self.log.debug("Entered _printPreview()")
        # TODO: write this function.
        QMessageBox.information(self, 
                                "Not yet implemented", 
                                "This feature has not yet been implemented.")
        self.log.debug("Exiting _printPreview()")

    def closeEvent(self, closeEvent):
        """Attempts to close the QMainWindow.  Does any cleanup necessary."""

        self.log.debug("Entered closeEvent()")

        # Flag that indicates that we should exit. 
        shouldExit = True
        
        # Get the list of subwindows.
        subwindows = self.mdiArea.subWindowList()

        # Go through each subwindow and try to close each.
        for subwindow in subwindows:
            subwindowClosed = subwindow.close()

            # If a subwindow is not closed (i.e., the user clicked
            # cancel), then we will not exit the application.
            if subwindowClosed == False:
                shouldExit = False
                break


        # Accept the close event if the flag is set.
        if shouldExit == True:
            self.log.debug("Accepting close event.")

            # Save application settings/preferences.
            self._writeSettings()

            closeEvent.accept()
        else:
            self.log.debug("Ignoring close event.")

            closeEvent.ignore()

        self.log.debug("Exiting closeEvent()")

    def _exitApp(self):
        """Exits the app by trying to close all windows."""

        self.log.debug("Entered _exitApp()")

        qApp.closeAllWindows()

        self.log.debug("Exiting _exitApp()")


    def _editBirthInfo(self):
        """Opens up a BirthInfoEditDialog for editing the BirthInfo of the
        current active PriceChartDocument.
        """

        self.log.debug("Entered _editBirthInfo()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the BirthInfo.
            birthInfo = priceChartDocument.getBirthInfo()

            # Create a dialog to edit the birth info.
            dialog = BirthInfoEditDialog(birthInfo)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("BirthInfoEditDialog accepted.  Data is: " + \
                               dialog.getBirthInfo().toString())
                priceChartDocument.setBirthInfo(birthInfo)
            else:
                self.log.debug("BirthInfoEditDialog rejected.  " + \
                               "Doing nothing more.")

        else:
            self.log.error("Tried to edit the birth info when either no " +
                           "PriceChartDocument is selected, or some " +
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editBirthInfo()")


    def _editAppPreferences(self):
        self.log.debug("Entered _editAppPreferences()")
        # TODO:  implement this function.
        QMessageBox.information(self, 
                                "Not yet implemented", 
                                "This feature has not yet been implemented.")
        self.log.debug("Exiting _editAppPreferences()")


    def _about(self):
        """Opens a popup window displaying information about this
        application.
        """

        endl = os.linesep

        title = "About"

        message = self.appName + endl + \
                  endl + \
                  self.appName + " is a PyQt application that " + \
                  "is a research tool for the study of the financial " + \
                  "markets." + \
                  endl + \
                  endl + \
                  "Version: " + self.appVersion + endl + \
                  "Released: " + self.appDate + endl + \
                  endl + \
                  "Author: " + self.appAuthor + endl + \
                  "Email: " + self.appAuthorEmail

        QMessageBox.about(self, title, message)

    def _aboutQt(self):
        """Opens a popup window displaying information about the Qt
        toolkit used in this application.
        """

        title = "About Qt"
        QMessageBox.aboutQt(self, title)


class PriceChartDocument(QMdiSubWindow):
    """QMdiSubWindow in the QMdiArea.  This window allows a user to 
    view and edit the data contained in a PriceChartDocumentData object.
    """

    # Initialize the sequence number for untitled documents.
    untitledDocSequenceNum = 1

    # File extension.
    fileExtension = ".pcd"

    # File filter.
    fileFilter = "PriceChartDocument files (*" + fileExtension + ")"

    # Modified-file string that is displayed in the window title after the
    # filename.
    modifiedFileStr = " (*)"

    # Signal emitted when the object wants to display something to the
    # status bar.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Creates the QMdiSubWindow with the internal widgets,
        and loads the given PriceChartDocumentData object.
        """
        super().__init__(parent)

        self.log = logging.getLogger("ui.PriceChartDocument")
        self.log.debug("Entered PriceChartDocument()")

        
        # Create internal data attributes.
        self.priceChartDocumentData = PriceChartDocumentData()

        self.dirtyFlag = True
        self.isUntitled = True
        self.filename = ""

        self.title = \
            "Untitled{}".format(PriceChartDocument.untitledDocSequenceNum) + \
            PriceChartDocument.fileExtension +  \
            PriceChartDocument.modifiedFileStr 
        PriceChartDocument.untitledDocSequenceNum += 1

        # Create the internal widget(s).
        self.widgets = PriceChartDocumentWidget()
        self.setWidget(self.widgets)

        # According to the Qt QMdiArea documentation:
        # 
        #   When you create your own subwindow, you must set the
        #   Qt.WA_DeleteOnClose  widget attribute if you want the window to
        #   be deleted when closed in the MDI area. If not, the window will
        #   be hidden and the MDI area will not activate the next subwindow.
        #
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setWindowTitle(self.title)

        self.log.debug("Exiting PriceChartDocument()")

    def picklePriceChartDocumentDataToFile(self, filename):
        """Pickles the internal PriceChartDocumentData object to the given
        filename.  If the file currently exists, it will be overwritten.

        Returns True if the write operation succeeded without problems.
        """

        self.log.debug("Entered picklePriceChartDocumentDataToFile()")

        # Return value.
        rv = True

        # Get the internal PriceChartDocumentData.
        priceChartDocumentData = self.getPriceChartDocumentData()

        # Pickle to file.
        with open(filename, "wb") as fh:
            try:
                pickle.dump(priceChartDocumentData, fh) 
                rv = True
            except pickle.PickleError as pe:
                self.log.error("Error while pickling a " +
                               "PriceChartDocumentData to file " + 
                               filename + 
                               ".  Error is: {}".format(pe) +
                               ".  PriceChartDocumentData object " + 
                               "has the following info: " + 
                               priceChartDocumentData.toString())
                rv = False

        self.log.debug("Exiting picklePriceChartDocumentDataToFile(), " + \
                       "rv = {}".format(rv))
        return rv

    def unpicklePriceChartDocumentDataFromFile(self, filename):
        """Un-Pickles a PriceChartDocumentData object from file.
        The PriceChartDocumentData obtained is then set to the internal
        PriceChartDocumentData.

        Returns True if the operation succeeded without problems.
        """

        self.log.debug("Entered unpicklePriceChartDocumentDataFromFile()")

        # Return value.
        rv = False

        # Get the PriceChartDocumentData from filename.
        with open(filename, "rb") as fh:
            try:
                priceChartDocumentData = pickle.load(fh)

                # Verify it is a PriceChartDocumentData object.
                if isinstance(priceChartDocumentData, 
                              PriceChartDocumentData) == True:
                    self.setPriceChartDocumentData(priceChartDocumentData)
                    self.setFilename(filename)
                    self.setDirtyFlag(False)
                    rv = True
                else:
                    # Print error message.
                    self.log.error("Cannot load this object.  " + 
                                   "The object unpickled from file " + 
                                   filename + " is not a " + 
                                   "PriceChartDocumentData.")
                    rv = False
            except pickle.UnpicklingError as upe:
                self.log.error("Error while unpickling a " +
                               "PriceChartDocumentData from file " + 
                               filename + 
                               ".  Error is: {}".format(upe))
                rv = False

        self.log.debug("Exiting unpicklePriceChartDocumentDataFromFile(), " +
                       "rv = {}".format(rv))
        return rv

    def setFilename(self, filename):
        """Sets the filename of the document.  This also sets the window
        title as well.
        """

        self.log.debug("Entered setFilename()")

        if self.filename != filename:
            self.log.debug("Updating filename to: " + filename)

            self.filename = filename

            self.isUntitled = False

            # The title is set to the filename without the path.
            loc = self.filename.rfind(os.sep)
            loc += len(os.sep)

            self.title = self.filename[loc:]
            self.setWindowTitle(self.title)
        else:
            self.log.debug("Filename didn't change.  No need to update.")

        self.log.debug("Exiting setFilename()")

    def getFilename(self):
        """Returns the currently set filename.  This is an empty str if
        the filename has not been set yet.
        """

        return self.filename


    def getPriceChartDocumentData(self):
        """Obtains all the data in the widgets and puts it into the
        internal PriceChartDocumentData object, then returns that object.

        Returns: PriceChartDocumentData object that holds all the
        information about this document as stored in the widgets.
        """

        self.log.debug("Entered getPriceChartDocumentData()")

        
        # The PriceBars reference in self.priceChartDocumentData
        # should hold the internal bars, since this is the reference that
        # passed into the child widgets to load stuff.  If there are bars
        # added (via dialogs or some other means), the list that 
        # the reference is pointing to should have those new bars.  
        # The same should be true with the BirthInfo.
        # Therefore, all we need to retrieve is the pricebarchart
        # artifacts and the settings objects.

        self.priceChartDocumentData.priceBarChartArtifacts = \
            self.widgets.getPriceBarChartArtifacts()

        self.priceChartDocumentData.priceBarChartSettings = \
            self.widgets.getPriceBarChartSettings()

        self.priceChartDocumentData.priceBarSpreadsheetSettings = \
            self.widgets.getPriceBarSpreadsheetSettings()

        self.log.debug("Exiting getPriceChartDocumentData()")

        return self.priceChartDocumentData

    def setPriceChartDocumentData(self, priceChartDocumentData):
        """Stores the PriceChartDocumentData and sets the widgets with the
        information it requires.
        """

        self.log.\
            debug("Entered setPriceChartDocumentData()")

        # Store the object reference.
        self.priceChartDocumentData = priceChartDocumentData
            
        self.log.debug("Number of priceBars is: {}".\
                format(len(self.priceChartDocumentData.priceBars)))

        # Clear all the old data.
        self.widgets.clearAllPriceBars()
        self.widgets.clearAllPriceBarChartArtifacts()

        # Load pricebars and chart artifacts.
        priceBars = self.priceChartDocumentData.priceBars
        priceBarChartArtifacts = \
            self.priceChartDocumentData.priceBarChartArtifacts
        self.widgets.loadPriceBars(priceBars)
        self.widgets.loadPriceBarChartArtifacts(priceBarChartArtifacts)

        # Apply the settings objecdts.
        priceBarChartSettings = \
            self.priceChartDocumentData.priceBarChartSettings
        priceBarSpreadsheetSettings = \
            self.priceChartDocumentData.priceBarSpreadsheetSettings
        self.widgets.applyPriceBarChartSettings(priceBarChartSettings)
        self.widgets.\
            applyPriceBarSpreadsheetSettings(priceBarSpreadsheetSettings)

        # By default, set the flag as dirty.  
        # If this was an open/load from file, the caller of this 
        # function should themselves call the function to set the flag to
        # be not dirty.
        self.setDirtyFlag(True)

        self.log.\
            debug("Exiting setPriceChartDocumentData()")
        
    def getBirthInfo(self):
        """Returns the internal BirthInfo object from the internal
        PriceChartDocumentData object.
        """

        self.log.debug("Entered getBirthInfo()")
        self.log.debug("Exiting getBirthInfo()")
        return self.priceChartDocumentData.getBirthInfo()

    def setBirthInfo(self, birthInfo):
        """Sets the the internal BirthInfo in the internal
        PriceChartDocumentData object.  This also causes the dirty flag to
        be set on the document.
        """

        self.log.debug("Entered setBirthInfo()")

        self.priceChartDocumentData.setBirthInfo(birthInfo)
        self.setDirtyFlag(True)

        self.log.debug("Exiting setBirthInfo()")

    def getDirtyFlag(self):
        """Returns the dirty flag value."""

        return self.dirtyFlag

    def setDirtyFlag(self, dirtyFlag):
        """Sets the flag that says that the PriceChartDocument is dirty.
        The document being dirty means that the document has modifications
        that have not been saved to file (or other persistent backend).

        Parameters:
        dirtyFlag - bool value for what the dirty flag is.  True means
        there are modifications not saved yet.
        """

        self.log.debug("Entered setDirtyFlag({})".format(dirtyFlag))

        # Set the flag first.
        self.dirtyFlag = dirtyFlag

        modFileStr = PriceChartDocument.modifiedFileStr
        modFileStrLen = len(PriceChartDocument.modifiedFileStr)

        if self.dirtyFlag == True:
            # Modify the title, but only if it isn't already there.
            if self.title[(-1 * modFileStrLen):] != modFileStr:
                self.title += modFileStr
        else:
            # Remove the modified-file string from the title if it is
            # already there.
            if (len(self.title) >= modFileStrLen and \
                self.title[(-1 * modFileStrLen):] == modFileStr):

                # Chop off the string.
                self.title = self.title[:(-1 * modFileStrLen)]

        # Actually update the window title if it is now different.
        if self.title != str(self.windowTitle()):
            self.setWindowTitle(self.title)

        self.log.debug("Exiting setDirtyFlag({})".format(dirtyFlag))

    def closeEvent(self, closeEvent):
        """Closes this QMdiSubWindow.
        If there are unsaved modifications, then the user will be prompted
        for saving.
        """
        
        self.log.debug("Entered closeEvent()")

        priceChartDocument = self

        # Prompt for saving if there are unsaved modifications.
        if priceChartDocument.getDirtyFlag() == True:
            title = "Save before closing?"
            text = "This PriceChartDocument has not been saved yet." + \
                   os.linesep + os.linesep + \
                   "Save before closing?"
            buttons = (QMessageBox.Save | 
                       QMessageBox.Discard | 
                       QMessageBox.Cancel)

            defaultButton = QMessageBox.Save 

            buttonClicked = \
                QMessageBox.question(self, title, text, 
                                     buttons, defaultButton)

            # Check what button was clicked in the prompt.
            if buttonClicked == QMessageBox.Save:
                # Save the document before closing.
                debugMsg = "closeEvent(): " + \
                    "User chose to save mods to PriceChartDocument: " + \
                    priceChartDocument.toString()

                self.log.debug(debugMsg)

                # Only close if the save action succeeded.
                # We can always prompt again and they can click discard if
                # they really don't want to save.
                if self.saveChart() == True:
                    self.log.debug("Save was successful.  " + \
                                   "Now closing PriceChartDocument.")
                    closeEvent.accept()
                else:
                    self.log.debug("Save was not successful.  " + \
                                   "Ignoring close event.")
                    closeEvent.ignore()

            elif buttonClicked == QMessageBox.Discard:
                # Discard modifications.  Here we just send a close event.
                debugMsg = "closeEvent(): " + \
                    "Discarding modifications to PriceChartDocument: " + \
                    priceChartDocument.toString()

                self.log.debug(debugMsg)

                closeEvent.accept()

            elif buttonClicked == QMessageBox.Cancel:
                # Use clicked cancel, meaning he doesn't want to close the
                # chart after all.
                debugMsg = "closeEvent(): " + \
                    "Canceled closeChart for PriceChartDocument: " + \
                    priceChartDocument.toString()

                self.log.debug(debugMsg)

                closeEvent.ignore()
        else:
            # Document is not dirty (it has been saved).  Just close.
            self.log.debug("Document has no unsaved mods.  " + \
                           "Just closing the PriceChartDocument: " + \
                           priceChartDocument.toString())

            closeEvent.accept()

        self.log.debug("Exiting closeEvent()")

    def saveChart(self):
        """Saves this PriceChartDocument.
        If the document has not been saved before, then a prompt 
        will be brought up for the user to specify a filename 
        to save as.

        Returns: True if the save action succeeded.
        """

        self.log.debug("Entered saveChart()")

        # Return value.
        rv = True

        priceChartDocument = self

        # See if it has been saved before and has a filename,
        # of it is untitled and never been saved before.
        filename = priceChartDocument.getFilename()

        if filename == "":
            # The document has never been saved before.
            # Bring up the Save As prompt for file.
            rv = self.saveAsChart()
        else:
            # The document has been saved before and has a filename
            # associated with it.
            self.log.debug("saveChart(): " + 
                           "Filename associated with " +
                           "the PriceChartDocument is: " + filename)

            if os.path.exists(filename):
                self.log.debug("saveChart(): " + 
                               "Updating existing file: " + 
                               filename)
            else:
                self.log.warn("saveChart(): " +
                              "Filename was non-empty " +
                              "and set to a file that does not exist!  " +
                              "This is an invalid state.  Filenames " + 
                              "should only be set if it was previously " +
                              "saved to the given filename.")

            # Pickle to file.
            rv = priceChartDocument.\
                    picklePriceChartDocumentDataToFile(filename)

            # Clear the dirty flag if the operation was successful.
            if rv == True:
                self.log.info("PriceChartDocumentData saved to file: " + 
                              filename)

                if self.log.isEnabledFor(logging.DEBUG):
                    # Get the data object for debugging messages.
                    priceChartDocumentData = \
                        priceChartDocument.getPriceChartDocumentData()

                    debugMsg = \
                        "File '{}' ".format(filename) + \
                        "now holds the following " + \
                        "PriceChartDocumentData: " + \
                        priceChartDocumentData.toString()

                    self.log.debug(debugMsg)

                # Filename shouldn't have changed, so there's no need to
                # set it again.
                priceChartDocument.setDirtyFlag(False)

                self.statusMessageUpdate.emit("PriceChartDocument saved.")
            else:
                # Save failure.
                self.statusMessageUpdate.emit("Save failed.  " + 
                                "Please check the log file for why.")

        self.log.debug("Exiting saveChart().  Returning {}".format(rv))
        return rv


    def saveAsChart(self):
        """Brings up a prompt for the user to save this 
        PriceChartDocument to a new file.  After the 
        user selects the file, it will be saved
        to that file.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).

        Returns: True if the saveAs action succeeded.
        """

        self.log.debug("Entered saveAsChart()")

        # Return value.
        rv = True

        priceChartDocument = self

        # Set filters for what files are displayed.
        filters = \
            PriceChartDocument.fileFilter + ";;" + \
            MainWindow.allFilesFileFilter

        # Directory location default for the file save dialogs for
        # PriceChartDocument.
        settings = QSettings()
        defaultPriceChartDocumentSaveDirectory = \
            settings.value("ui/defaultPriceChartDocumentSaveDirectory", "")

        # Prompt for what filename to save the data to.
        filename = QFileDialog.\
            getSaveFileName(self, 
                            "Save As", 
                            defaultPriceChartDocumentSaveDirectory, 
                            filters)

        # Convert filename from QString to str.
        filename = str(filename)

        self.log.debug("saveAsChart(): The user selected filename: " +
                       filename + " as what they wanted to save to.")

        # Verify input.
        if filename == "":
            # The user must of clicked cancel at the file dialog prompt.
            rv = False
        else:
            # Pickle to file.
            rv = priceChartDocument.\
                    picklePriceChartDocumentDataToFile(filename)

            # If the save operation was successful, then update the
            # filename and clear the dirty flag.
            if rv == True:
                self.log.info("PriceChartDocumentData saved to " + 
                              "new file: " + filename)

                if self.log.isEnabledFor(logging.DEBUG):
                    # Get the data object for debugging messages.
                    priceChartDocumentData = \
                        priceChartDocument.getPriceChartDocumentData()

                    debugMsg = \
                        "File '{}' ".format(filename) + \
                        "now holds the following " + \
                        "PriceChartDocumentData: " + \
                        priceChartDocumentData.toString()

                    self.log.debug(debugMsg)

                priceChartDocument.setFilename(filename)
                priceChartDocument.setDirtyFlag(False)
 
                statusBarMessage = \
                    "PriceChartDocument saved to file {}.".format(filename)

                self.statusMessageUpdate.emit(statusBarMessage)

                # Get the directory where this file lives.
                loc = filename.rfind(os.sep)
                directory = filename[:loc]

                # Update the self.defaultPriceChartDocumentSaveDirectory
                # with the directory where filename is, if the directory
                # is different.
                if directory != defaultPriceChartDocumentSaveDirectory:
                    settings.\
                        setValue("ui/defaultPriceChartDocumentSaveDirectory",
                                 directory)
            else:
                # Save failure.
                self.statusMessageUpdate.emit("Save failed.  " + 
                                "Please check the log file for why.")

        self.log.debug("Exiting saveAsChart().  Returning {}".format(rv))
        return rv


    def toString(self):
        """Returns the str representation of this class object.
        """

        # Return value.
        rv = \
            "[title={}, ".format(self.title) + \
            "filename={}, ".format(self.filename) + \
            "isUntitled={}, ".format(self.isUntitled) + \
            "dirtyFlag={}, ".format(self.dirtyFlag) + \
            "priceChartDocumentData={}]".\
                format(self.priceChartDocumentData.toString())

        return rv

    def __str__(self):
        """Returns the str representation of this class object.
        """

        return self.toString() 

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
        
    def clearAllPriceBars(self):
        """Clears all PriceBars from all the internal widgets.
        This is called if a full reload is desired.
        After this call, one can then call loadPriceBars(priceBars) 
        with all the pricebars to be loaded.
        """

        self.log.debug("Entered clearAllPriceBars()")

        # PriceBars in the PriceBarChart.
        self.priceBarChartWidget.clearAllPriceBars()

        # PriceBars in the PriceBarSpreadsheet.
        self.priceBarSpreadsheetWidget.clearAllPriceBars()

        self.log.debug("Leaving clearAllPriceBars()")
        
    def clearAllPriceBarChartArtifacts(self):
        """Clears all the PriceBarChartArtifact objects from the 
        PriceBarChartWidget."""

        self.priceBarChartWidget.clearAllPriceBarChartArtifacts()


    def loadPriceBars(self, priceBars):
        """Loads the price bars into the widgets.
        
        Arguments:
            
        priceBars - list of PriceBar objects with the price data.
        """

        self.log.debug("Entered loadPriceBars({} pricebars)".\
                       format(len(priceBars)))

        # TODO:  Decide if we should be doing things by explicit time
        # frames or if we should be loading things generically.

        # Load PriceBars into the PriceBarChart.
        self.priceBarChartWidget.loadDayPriceBars(priceBars)

        # Load PriceBars into the PriceBarSpreadsheet.
        self.priceBarSpreadsheetWidget.loadPriceBars(priceBars)

        self.log.debug("Leaving loadPriceBars({} pricebars)".\
                       format(len(priceBars)))

    def loadPriceBarChartArtifacts(self, priceBarChartArtifacts):
        """Loads the PriceBarChart artifacts.

        Arguments:

        priceBarChartArtifacts - list of PriceBarArtifact objects.
        """

        self.log.debug("Entered loadPriceBarChartArtifacts({} artifacts)".\
                       format(len(priceBarChartArtifacts)))

        self.priceBarChartWidget.\
            loadPriceBarChartArtifacts(priceBarChartArtifacts)

        self.log.debug("Leaving loadPriceBarChartArtifacts({} artifacts)".\
                       format(len(priceBarChartArtifacts)))

    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the given PriceBarChartSettings object to the
        internal PriceBarChartWidget.
        """

        self.priceBarChartWidget.\
            applyPriceBarChartSettings(priceBarChartSettings)

    def applyPriceBarSpreadsheetSettings(self, priceBarSpreadsheetSettings):
        """Applies the given PriceBarSpreadsheetSettings object to the
        internal PriceBarSpreadsheetWidget.
        """

        self.priceBarSpreadsheetWidget.\
            applyPriceBarSpreadsheetSettings(priceBarSpreadsheetSettings)

    def getPriceBarChartArtifacts(self):
        """Returns the list of PriceBarChartArtifacts that are used in the
        PriceBarChartWidget.
        """

        return self.priceBarChartWidget.getPriceBarChartArtifacts()

    def getPriceBarChartSettings(self):
        """Obtains the current PriceBarChartSettings object from the
        PriceBarChartWidget.
        """

        return self.priceBarChartWidget.getPriceBarChartSettings()

    def getPriceBarSpreadsheetSettings(self):
        """Obtains the current PriceBarSpreadsheetsettings object from the
        PriceBarSpreadsheetWidget.
        """

        return self.priceBarSpreadsheetWidget.\
                getPriceBarSpreadsheetSettings()


