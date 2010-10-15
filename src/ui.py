
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
        self.appIcon = QIcon(":/images/appIcon.png")
        
        # Set application details so the we can use QSettings default
        # constructor later.
        QCoreApplication.setOrganizationName(appAuthor);
        QCoreApplication.setApplicationName(appName);

        # Settings attributes that are set when _readSettings() is called.
        self.defaultPriceChartDocumentOpenDirectory = ""
        self.defaultPriceChartDocumentSaveDirectory = ""
        self.defaultPriceBarDataOpenDirectory = ""
        self.windowGeometry = QByteArray()
        self.windowState = QByteArray()

        # Create and set up the widgets.
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        # Maps actions in the window menu to changing active document windows.
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped.connect(self.mdiArea.setActiveSubWindow)

        # Any updates in window activation will update menus.
        self.mdiArea.subWindowActivated.connect(self._updateMenus)

        # Create actions, menus, toolbars, statusbar, widgets, etc.
        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()

        self._updateMenus()

        self._readSettings()

        self.restoreGeometry(self.windowGeometry);
        self.restoreState(self.windowState);

        self.setWindowTitle(self.appName)
        self.setWindowIcon(self.appIcon)


    def _createActions(self):
        """Creates all the QAction objects that will be mapped to the 
        choices on the menu, toolbar and keyboard shortcuts."""

        ####################
        # Create actions for the File Menu.

        # Create the newChartAction.
        self.newChartAction = QAction(QIcon(":/images/new.png"), "&New", self)
        self.newChartAction.setShortcut("Ctrl+n")
        self.newChartAction.setStatusTip("Create a new Chart file")
        self.newChartAction.triggered.connect(self._newChart)

        # Create the openChartAction.
        self.openChartAction = QAction(QIcon(":/images/open.png"), 
                "&Open", self)
        self.openChartAction.setShortcut("Ctrl+o")
        self.openChartAction.setStatusTip("Open an existing Chart file")
        self.openChartAction.triggered.connect(self._openChart)

        # Create the saveChartAction.
        self.saveChartAction = QAction(QIcon(":/images/save.png"), 
                "&Save", self)
        self.saveChartAction.setShortcut("Ctrl+s")
        self.saveChartAction.setStatusTip("Save the Chart to disk")
        self.saveChartAction.triggered.connect(self._saveChart)


        # Create the saveAsChartAction.
        self.saveAsChartAction = QAction("Save &As...", self)
        self.saveAsChartAction.setStatusTip("Save the Chart as a new file")
        self.saveAsChartAction.triggered.connect(self._saveAsChart)

        # Create the exitAppAction.
        self.exitAppAction = QAction("E&xit", self)
        self.exitAppAction.setShortcut("Ctrl+q")
        self.exitAppAction.setStatusTip("Exit the application")
        self.exitAppAction.triggered.connect(self._exitApp)

        ####################
        # Create actions for the Edit Menu.

        # Create the editBirthInfoAction.
        self.editBirthInfoAction = QAction(QIcon(":/images/Edit.png"),
                "&Edit Birth Data", self)
        self.editBirthInfoAction.setStatusTip(
                "Edit the birth time and birth location")
        self.editBirthInfoAction.triggered.connect(self._editBirthInfo)


        # Create the editAppPreferencesAction.
        self.editAppPreferencesAction = QAction(QIcon(":/images/gears.png"), 
                "Edit &Preferences", self)
        self.editAppPreferencesAction.setStatusTip("Edit Preferences")
        self.editAppPreferencesAction.triggered.connect(
                self._editAppPreferences)


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
        self.aboutAction.triggered.connect(self._about)

    def _createMenus(self):
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


    def _createToolBars(self):
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

    def _createStatusBar(self):
        """Creates the QStatusBar by showing the message "Ready"."""

        self.statusBar().showMessage("Ready")

    def _updateMenus(self):
        """Updates the menu by enabling various QActions depending on the
        current state of the application."""

        self.log.debug("Entered _updateMenus()")

        # For debugging:
        priceChartDocument = self.getActivePriceChartDocument()
        if priceChartDocument == None:
            print("DEBUG: Entered _updateMenus() with currently active " +
                  "subwindow: == None")
        else:
            print("DEBUG: Entered _updateMenus() with currently active " +
                  "subwindow title: == " + priceChartDocument.title)

        self._updateFileMenu()
        self._updateEditMenu()
        self._updateWindowMenu()

        self.log.debug("Exiting _updateMenus()")


    def _updateFileMenu(self):
        """Updates the File menu according to the state of the current
        document.
        """

        self.log.debug("Entered _updateFileMenu()")
        # TODO:  write this funciton out.
        self.log.debug("Exiting _updateFileMenu()")


    def _updateEditMenu(self):
        """Updates the Edit menu according to the state of the current
        document.
        """

        self.log.debug("Entered _updateEditMenu()")
        # TODO:  write this funciton out.
        self.log.debug("Exiting _updateEditMenu()")

    def _updateWindowMenu(self):
        """Updates the Window menu according to which documents are open
        currently.
        """

        self.log.debug("Entered _updateWindowMenu()")
        # TODO:  write this funciton out.
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

        # Note: Setting the active window here will also cause _updateMenus()
        # to be called, which is what we want.
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
        This includes default directories to open to when the user
        open/saves files, and also the window geometry, etc.

        This function uses QSettings and assumes that the calls to
        QCoreApplication.setOrganizationName(), and 
        QCoreApplication.setApplicationName() have been called 
        previously (so that the QSettings constructor can be called 
        without any parameters specified).
        """

        self.log.debug("Entered _readSettings()")

        # Preference settings.
        settings = QSettings() 

        # Directory location default for the file open dialogs for
        # PriceChartDocument.
        self.defaultPriceChartDocumentOpenDirectory = \
            settings.value("ui/defaultPriceChartDocumentOpenDirectory", "")

        # Directory location default for the file save dialogs for
        # PriceChartDocument.
        self.defaultPriceChartDocumentSaveDirectory = \
            settings.value("ui/defaultPriceChartDocumentSaveDirectory", "")

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
        This includes default directories to open to when the user
        open/saves files, and also the window geometry, etc.

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

        # Directory location default for the file open dialogs for
        # PriceChartDocument.
        if (self.defaultPriceChartDocumentOpenDirectory != 
            settings.value("ui/defaultPriceChartDocumentOpenDirectory", "")):

            settings.setValue("ui/defaultPriceChartDocumentOpenDirectory",
                              self.defaultPriceChartDocumentOpenDirectory)

        # Directory location default for the file save dialogs for
        # PriceChartDocument.
        if (self.defaultPriceChartDocumentSaveDirectory !=
            settings.value("ui/defaultPriceChartDocumentSaveDirectory", "")):

            settings.setValue("ui/defaultPriceChartDocumentSaveDirectory",
                              self.defaultPriceChartDocumentSaveDirectory)

        # Window geometry.
        if (settings.value("ui/MainWindow/windowGeometry").toByteArray() !=
            self.saveGeometry()):

            settings.setValue("ui/MainWindow/windowGeometry", 
                              self.saveGeometry())

        # Window state.
        if (settings.value("ui/MainWindow/windowState").toByteArray() !=
            self.saveState()):

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
            priceChartDocument = PriceChartDocument()
            priceChartDocument.\
                setPriceChartDocumentData(priceChartDocumentData)

            # Add this priceChartDocument to the list of subwindows
            self._addSubWindow(priceChartDocument)
        else:
            self.log.debug("PriceChartDocumentWizard rejected");


        self.log.debug("Exiting _newChart()")

    def _openChart(self):
        self.log.debug("Entered _openChart()")

        # Set filters for what files are displayed.
        filters = \
            PriceChartDocument.fileFilter + ";;" + \
            MainWindow.allFilesFileFilter

        filename = \
            QFileDialog.\
                getOpenFileName(self, 
                                "Open PriceChartDocument File",
                                self.defaultPriceChartDocumentOpenDirectory,
                                filters)

        if filename != "":
            # Load the file.

            # Create the subwindow.
            priceChartDocument = PriceChartDocument()

            # Try to load the file data into the subwindow.
            loadSuccess = \
                priceChartDocument.\
                    unpicklePriceChartDocumentDataFromFile(filename)

            if loadSuccess == True:
                # Load into the object was successful.  
                # Now Add this priceChartDocument to the list of subwindows
                self._addSubWindow(priceChartDocument)

                # Update the statusbar to tell what file was opened.
                statusBarMessage = \
                    "Opened PriceChartDocument {}.".format(filename)
                statusBarTimeoutMsec = \
                    MainWindow.defaultStatusBarMsgTimeMsec

                self.statusBar().showMessage(statusBarMessage,
                                             statusBarTimeoutMsec)

                # Get the directory where this file lives.
                loc = filename.rfind(os.sep)
                directory = filename[:loc]

                # Update the self.defaultPriceChartDocumentOpenDirectory
                # with the directory where filename is, if the directory
                # is different.
                if directory != self.defaultPriceChartDocumentOpenDirectory:
                    self.defaultPriceChartDocumentOpenDirectory = directory
            else:
                # Load failed.  Tell the user via the statusbar.
                statusBarMessage = \
                    "Open operation failed.  " + \
                    "Please see the log file for why."
                statusBarTimeoutMsec = \
                    MainWindow.defaultStatusBarMsgTimeMsec

                self.statusBar().showMessage(statusBarMessage,
                                             statusBarTimeoutMsec)
        else:
            self.log.debug("_openChart(): " +
                           "No filename was selected for opening.")

        self.log.debug("Exiting _openChart()")

    def _saveChart(self):
        """Saves the current subwindow to file.  If the document has not
        been saved before, then a prompt will be brought up for the user
        to specify a filename to save as.

        Returns: True if the save action succeeded.
        """

        self.log.debug("Entered _saveChart()")

        # Return value.
        rv = True

        # Get the active subwindow.
        subwindow = self.mdiArea.currentSubWindow()

        # If it is a PriceChartDocument, we'll save it as one.
        if isinstance(subwindow, PriceChartDocument) == True:
            # A PriceChartDocument is selected.
            priceChartDocument = subwindow

            # See if it has been saved before and has a filename,
            # of it is untitled and never been saved before.
            filename = priceChartDocument.getFilename()

            if filename == "":
                # The document has never been saved before.
                # Bring up the Save As prompt for file.
                rv = self._saveAsChart()
            else:
                # The document has been saved before and has a filename
                # associated with it.
                self.log.debug("_saveChart(): Filename associated with the " + 
                               "PriceChartDocument is: " + filename)

                if os.path.exists(filename):
                    self.log.debug("_saveChart(): Updating existing file: " + 
                                   filename)
                else:
                    self.log.warn("_saveChart(): Filename was non-empty " +
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

                    self.statusBar().\
                        showMessage("PriceChartDocument saved.",
                                    MainWindow.defaultStatusBarMsgTimeMsec)

                    # Get the directory where this file lives.
                    loc = filename.rfind(os.sep)
                    directory = filename[:loc]

                    # Update the self.defaultPriceChartDocumentSaveDirectory
                    # with the directory where filename is, if the directory
                    # is different.
                    if directory != \
                        self.defaultPriceChartDocumentSaveDirectory:

                        self.defaultPriceChartDocumentSaveDirectory = \
                            directory
                else:
                    # Save failure.
                    self.statusBar().\
                        showMessage("Save failed.  " + 
                                    "Please check the log file for why.",
                                    MainWindow.defaultStatusBarMsgTimeMsec)

        else:
            self.log.warn("_saveChart(): " + 
                          "No subwindow is selected, or the selected " + 
                          "subwindow is not a supported document type " +
                          "for saving.")
            rv = False


        self.log.debug("Exiting _saveChart().  Returning {}".format(rv))
        return rv

    def _saveAsChart(self):
        """Brings up a prompt for the user to saves the current subwindow 
        to a new file.  After the user selects the file, it will be saved
        to that file.

        Returns: True if the saveAs action succeeded.
        """

        self.log.debug("Entered _saveAsChart()")

        # Return value.
        rv = True

        # Get the active subwindow.
        subwindow = self.mdiArea.currentSubWindow()

        # If it is a PriceChartDocument, we'll save it as one.
        if isinstance(subwindow, PriceChartDocument) == True:
            # A PriceChartDocument is selected.
            priceChartDocument = subwindow

            # Set filters for what files are displayed.
            filters = \
                PriceChartDocument.fileFilter + ";;" + \
                MainWindow.allFilesFileFilter

            # Prompt for what filename to save the data to.
            filename = QFileDialog.\
                getSaveFileName(self, 
                                "Save As", 
                                self.defaultPriceChartDocumentSaveDirectory, 
                                filters)

            # Convert filename from QString to str.
            filename = str(filename)

            self.log.debug("_saveAsChart(): The user selected filename: " +
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
                        "PriceChartDocument saved to file {}.".\
                        format(filename)
                    statusBarTimeoutMsec = \
                        MainWindow.defaultStatusBarMsgTimeMsec

                    self.statusBar().showMessage(statusBarMessage,
                                                 statusBarTimeoutMsec)

                    # Get the directory where this file lives.
                    loc = filename.rfind(os.sep)
                    directory = filename[:loc]

                    # Update the self.defaultPriceChartDocumentSaveDirectory
                    # with the directory where filename is, if the directory
                    # is different.
                    if directory != \
                            self.defaultPriceChartDocumentSaveDirectory:

                        self.defaultPriceChartDocumentSaveDirectory = \
                                directory
                else:
                    # Save failure.
                    self.statusBar().\
                        showMessage("Save failed.  " + 
                                    "Please check the log file for why.",
                                    MainWindow.defaultStatusBarMsgTimeMsec)
        else:
            self.log.warn("_saveAsChart(): " + 
                           "No subwindow was selected or the " + 
                           "subwindow selected is not a supported " + 
                           "document type for saving.")
            rv = False

        self.log.debug("Exiting _saveAsChart().  Returning {}".format(rv))
        return rv

    def _exitApp(self):
        self.log.debug("Entered _exitApp()")

        # TODO:  need to create/overwrite the closeEvent() function.  This
        # function should do similar functionality.
        #


        # TODO:  add here some checking to save open unsaved files, and also settings.

        self.log.debug("Exiting _exitApp()")
        qApp.closeAllWindows()


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
        self.log.debug("Exiting _editAppPreferences()")
        pass


    def _about(self):
        """Opens a popup window displaying information about this
        application.
        """

        self.log.debug("Entered _about()")

        endl = os.linesep

        title = "About"

        message = self.appName + endl + \
                  endl + \
                  "Version: " + self.appVersion + endl + \
                  "Released: " + self.appDate + endl + \
                  endl + \
                  "Author: " + self.appAuthor + endl + \
                  "Email: " + self.appAuthorEmail

        QMessageBox.about(self, title, message);

        self.log.debug("Exiting _about()")


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
        self.setAttribute(Qt.WA_DeleteOnClose);

        self.setWindowTitle(self.title)

        self.log.debug("Exiting PriceChartDocument()")

    def picklePriceChartDocumentDataToFile(self, filename):
        """Pickles the internal PriceChartDocumentData object to the given
        filename.  If the file currently exists, it will be overwritten.

        Returns True if the write operation succeeded without problems.
        """

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
                               ".  PriceChartDocumentData object " + 
                               "has the following info: " + 
                               priceChartDocumentData.toString())
                rv = False

        return rv

    def unpicklePriceChartDocumentDataFromFile(self, filename):
        """Un-Pickles a PriceChartDocumentData object from file.
        The PriceChartDocumentData obtained is then set to the internal
        PriceChartDocumentData.

        Returns True if the operation succeeded without problems.
        """

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
                               filename)
                rv = False

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

        self.log.\
            debug("Entered getPriceChartDocumentData()")

        # TODO:  write this method.

        self.log.\
            debug("Exiting getPriceChartDocumentData()")

    def setPriceChartDocumentData(self, priceChartDocumentData):
        """Stores the PriceChartDocumentData and sets the widgets with the
        information it requires.
        """

        self.log.\
            debug("Entered setPriceChartDocumentData()")

        self.priceChartDocumentData = priceChartDocumentData

        # TODO:  write this method to set (load) everything into the widgets.

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
        
