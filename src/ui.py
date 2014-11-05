
# For obtaining the line separator and directory separator.
import os

# For obtaining information about the operating system platform.
import platform

# For comparing timestamps on files.
import time

# For serializing and unserializing objects.
import pickle

# For logging.
import logging

# For launching JHora and Astrolog.
import subprocess

# For timezones in datetime.datetime objects.
import datetime
import pytz

from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# For icon images, etc.
import resources

# For dialogs for user input.
from dialogs import *
from widgets import *

# For data objects manipulated in the ui.
from data_objects import BirthInfo
from data_objects import PriceChartDocumentData

# For widgets used in the ui.
from pricebarchart import *
from pricebarspreadsheet import *
from astrologychart import AstrologyChartWidget
from astrologychart import PlanetaryInfoTableWidget

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
        self.windowMapper.mapped[QWidget].\
            connect(self.mdiArea.setActiveSubWindow)

        # Any updates in window activation will update action objects and
        # the window menu.
        self.mdiArea.subWindowActivated.connect(self._updateActions)
        self.mdiArea.subWindowActivated.connect(self._updateWindowMenu)

        # Variable holding the most recently activated QAction for a
        # tool mode related to creating QGraphicsItems.
        self.mostRecentGraphicsItemToolModeAction = None
        
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

        # Remove old temporary JHora .jhd files that were created by us.
        self.removeOldTemporaryJHoraFiles()

        # Remove old temporary Astrolog .txt files that were created by us.
        self.removeOldTemporaryAstrologFiles()
        
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

        # Create the checkSourceDataFileForPriceBarUpdatesAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/actions/view-refresh.png")
        self.checkSourceDataFileForPriceBarUpdatesAction = \
            QAction(icon, "Chec&k for PriceBar data updates", self)
        self.checkSourceDataFileForPriceBarUpdatesAction.\
            setStatusTip("Check source data file for PriceBar updates")
        self.checkSourceDataFileForPriceBarUpdatesAction.triggered.\
            connect(self._handleCheckSourceDataFileForPriceBarUpdatesAction)
        
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

        # Create the editAppPreferencesAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/categories/preferences-system.png")
        self.editAppPreferencesAction = \
            QAction(icon, "Edit Application &Preferences", self)
        self.editAppPreferencesAction.\
            setStatusTip("Edit Application Preferences")
        self.editAppPreferencesAction.triggered.\
            connect(self._editAppPreferences)

        # Create the editBirthInfoAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/apps/internet-web-browser.png")
        self.editBirthInfoAction = QAction(icon, "Edit &Birth Data", self)
        self.editBirthInfoAction.setStatusTip(
                "Edit the birth time and birth location")
        self.editBirthInfoAction.triggered.connect(self._editBirthInfo)

        # Create the editPriceChartDocumentDataAction.
        icon = QIcon(":/images/rluu/gearGreen.png")
        self.editPriceChartDocumentDataAction = \
            QAction(icon, "Edit PriceChartDocument &Data", self)
        self.editPriceChartDocumentDataAction.\
            setStatusTip("Edit PriceChartDocument Data")
        self.editPriceChartDocumentDataAction.triggered.\
            connect(self._editPriceChartDocumentData)
        
        # Create the editPriceBarChartSettingsAction.
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/categories/applications-system.png")
        self.editPriceBarChartSettingsAction = \
            QAction(icon, "Edit PriceBarChart &Settings", self)
        self.editPriceBarChartSettingsAction.\
            setStatusTip("Edit PriceBarChart Settings")
        self.editPriceBarChartSettingsAction.triggered.\
            connect(self._editPriceBarChartSettings)
        
        # Create the editPriceBarChartScalingAction.
        icon = QIcon(":/images/rluu/triangleRuler.png")
        self.editPriceBarChartScalingAction = \
            QAction(icon, "Edit PriceBarChart S&caling", self)
        self.editPriceBarChartScalingAction.\
            setStatusTip("Edit PriceBarChart Scaling")
        self.editPriceBarChartScalingAction.triggered.\
            connect(self._editPriceBarChartScaling)
        

        ####################
        # Create actions for the Astro Menu.

        self.enableAndShowAstrologyChartAction = \
            QAction("Enable AstrologyChart", self)
        self.enableAndShowAstrologyChartAction.setCheckable(True)
        self.enableAndShowAstrologyChartAction.\
            setStatusTip("Enable AstrologyChart")
        self.enableAndShowAstrologyChartAction.triggered.\
            connect(self._handleEnableAndShowAstrologyChartAction)
        
        self.enableAndShowPlanetaryInfoTableAction = \
            QAction("Enable Planetary Info Table", self)
        self.enableAndShowPlanetaryInfoTableAction.setCheckable(True)
        self.enableAndShowPlanetaryInfoTableAction.\
            setStatusTip("Enable Planetary Info Table")
        self.enableAndShowPlanetaryInfoTableAction.triggered.\
            connect(self._handleEnableAndShowPlanetaryInfoTableAction)
        
        self.trackMouseToAstroChart1Action = \
            QAction("Link mouse pos to Astro Chart 1", self)
        self.trackMouseToAstroChart1Action.setCheckable(True)
        self.trackMouseToAstroChart1Action.\
            setStatusTip("Link mouse pos to Astro Chart 1")
        self.trackMouseToAstroChart1Action.triggered.\
            connect(self._handleTrackMouseToAstroChartAction)
        
        self.trackMouseToAstroChart2Action = \
            QAction("Link mouse pos to Astro Chart 2", self)
        self.trackMouseToAstroChart2Action.setCheckable(True)
        self.trackMouseToAstroChart2Action.\
            setStatusTip("Link mouse pos to Astro Chart 2")
        self.trackMouseToAstroChart2Action.triggered.\
            connect(self._handleTrackMouseToAstroChartAction)
        
        self.trackMouseToAstroChart3Action = \
            QAction("Link mouse pos to Astro Chart 3", self)
        self.trackMouseToAstroChart3Action.setCheckable(True)
        self.trackMouseToAstroChart3Action.\
            setStatusTip("Link mouse pos to Astro Chart 3")
        self.trackMouseToAstroChart3Action.triggered.\
            connect(self._handleTrackMouseToAstroChartAction)

        self.openJHoraWithNoArgsAction = \
            QAction("Open JHora with no args", self)
        self.openJHoraWithNoArgsAction.\
            setStatusTip("Open JHora without any command-line arguments")
        self.openJHoraWithNoArgsAction.triggered.\
            connect(self._handleOpenJHoraWithNoArgsAction)

        self.openJHoraWithLocalizedNowAction = \
            QAction("Open JHora with 'now'", self)
        self.openJHoraWithLocalizedNowAction.setStatusTip(\
            "Open JHora with the current time in the active " + \
            "chart's BirthInfo timezone.")
        self.openJHoraWithLocalizedNowAction.triggered.\
            connect(self._handleOpenJHoraWithLocalizedNowAction)
        
        self.openJHoraWithBirthInfoAction = \
            QAction("Open JHora with the chart's birth info", self)
        self.openJHoraWithBirthInfoAction.\
            setStatusTip("Open JHora with the active chart's BirthInfo")
        self.openJHoraWithBirthInfoAction.triggered.\
            connect(self._handleOpenJHoraWithBirthInfoAction)

        self.openAstrologWithNoArgsAction = \
            QAction("Open Astrolog with no args", self)
        self.openAstrologWithNoArgsAction.\
            setStatusTip("Open Astrolog without any command-line arguments")
        self.openAstrologWithNoArgsAction.triggered.\
            connect(self._handleOpenAstrologWithNoArgsAction)

        self.openAstrologWithLocalizedNowAction = \
            QAction("Open Astrolog with 'now'", self)
        self.openAstrologWithLocalizedNowAction.setStatusTip(\
            "Open Astrolog with the current time in the active " + \
            "chart's BirthInfo timezone.")
        self.openAstrologWithLocalizedNowAction.triggered.\
            connect(self._handleOpenAstrologWithLocalizedNowAction)
        
        self.openAstrologWithBirthInfoAction = \
            QAction("Open Astrolog with the chart's birth info", self)
        self.openAstrologWithBirthInfoAction.\
            setStatusTip("Open Astrolog with the active chart's BirthInfo")
        self.openAstrologWithBirthInfoAction.triggered.\
            connect(self._handleOpenAstrologWithBirthInfoAction)

        self.openAstroChart1WithBirthInfoAction = \
            QAction("Set BirthInfo to Astro Chart 1", self)
        self.openAstroChart1WithBirthInfoAction.triggered.\
            connect(self._handleOpenAstroChart1WithBirthInfoAction)
        
        self.openAstroChart2WithBirthInfoAction = \
            QAction("Set BirthInfo to Astro Chart 2", self)
        self.openAstroChart2WithBirthInfoAction.triggered.\
            connect(self._handleOpenAstroChart2WithBirthInfoAction)
        
        self.openAstroChart3WithBirthInfoAction = \
            QAction("Set BirthInfo to Astro Chart 3", self)
        self.openAstroChart3WithBirthInfoAction.triggered.\
            connect(self._handleOpenAstroChart3WithBirthInfoAction)
        
        self.openAstroChart1WithNowAction = \
            QAction("Set 'now' to Astro Chart 1", self)
        self.openAstroChart1WithNowAction.triggered.\
            connect(self._handleOpenAstroChart1WithNowAction)
        self.openAstroChart2WithNowAction = \
            QAction("Set 'now' to Astro Chart 2", self)
        self.openAstroChart2WithNowAction.triggered.\
            connect(self._handleOpenAstroChart2WithNowAction)
        self.openAstroChart3WithNowAction = \
            QAction("Set 'now' to Astro Chart 3", self)
        self.openAstroChart3WithNowAction.triggered.\
            connect(self._handleOpenAstroChart3WithNowAction)
        
        self.clearAstroChart1Action = \
            QAction("Clear Astro Chart 1", self)
        self.clearAstroChart1Action.triggered.\
            connect(self._handleClearAstroChart1Action)
        self.clearAstroChart2Action = \
            QAction("Clear Astro Chart 2", self)
        self.clearAstroChart2Action.triggered.\
            connect(self._handleClearAstroChart2Action)
        self.clearAstroChart3Action = \
            QAction("Clear Astro Chart 3", self)
        self.clearAstroChart3Action.triggered.\
            connect(self._handleClearAstroChart3Action)
        
        ####################
        # Create actions for the Tools Menu.
        
        # Create the ReadOnlyPointerToolAction.
        icon = QIcon(":/images/qt/pointer.png")
        self.readOnlyPointerToolAction = \
            QAction(icon, "Read-Only Pointer Tool", self)
        self.readOnlyPointerToolAction.setStatusTip("Read-Only Pointer Tool")
        self.readOnlyPointerToolAction.setCheckable(True)
        
        # Create the PointerToolAction.
        icon = QIcon(":/images/rluu/pointerPencil.png")
        self.pointerToolAction = QAction(icon, "Pointer Tool", self)
        self.pointerToolAction.setStatusTip("Pointer Tool")
        self.pointerToolAction.setCheckable(True)

        # Create the HandToolAction.
        icon = QIcon(":/images/rluu/handOpen.png")
        self.handToolAction = QAction(icon, "Hand Tool", self)
        self.handToolAction.setStatusTip("Hand Tool")
        self.handToolAction.setCheckable(True)

        # Create the ZoomInToolAction.
        icon = QIcon(":/images/rluu/zoomInBlue.png")
        self.zoomInToolAction = QAction(icon, "Zoom In Tool", self)
        self.zoomInToolAction.setStatusTip("Zoom In Tool")
        self.zoomInToolAction.setCheckable(True)

        # Create the ZoomOutToolAction.
        icon = QIcon(":/images/rluu/zoomOutBlue.png")
        self.zoomOutToolAction = QAction(icon, "Zoom Out Tool", self)
        self.zoomOutToolAction.setStatusTip("Zoom Out Tool")
        self.zoomOutToolAction.setCheckable(True)

        # Create the BarCountToolAction
        icon = QIcon(":/images/rluu/barCount.png")
        self.barCountToolAction = QAction(icon, "Bar Count Tool", self)
        self.barCountToolAction.setStatusTip("Bar Count Tool")
        self.barCountToolAction.setCheckable(True)

        # Create the TimeMeasurementToolAction
        icon = QIcon(":/images/rluu/timeMeasurement.png")
        self.timeMeasurementToolAction = \
            QAction(icon, "Time Measurement Tool", self)
        self.timeMeasurementToolAction.setStatusTip("Time Measurement Tool")
        self.timeMeasurementToolAction.setCheckable(True)

        # Create the PriceMeasurementToolAction
        icon = QIcon(":/images/rluu/priceMeasurement.png")
        self.priceMeasurementToolAction = \
            QAction(icon, "Price Measurement Tool", self)
        self.priceMeasurementToolAction.setStatusTip("Price Measurement Tool")
        self.priceMeasurementToolAction.setCheckable(True)

        # Create the TimeModalScaleToolAction
        icon = QIcon(":/images/rluu/timeModalScale.png")
        self.timeModalScaleToolAction = \
            QAction(icon, "Time Modal Scale Tool", self)
        self.timeModalScaleToolAction.setStatusTip("Time Modal Scale Tool")
        self.timeModalScaleToolAction.setCheckable(True)

        # Create the PriceModalScaleToolAction
        icon = QIcon(":/images/rluu/priceModalScale.png")
        self.priceModalScaleToolAction = \
            QAction(icon, "Price Modal Scale Tool", self)
        self.priceModalScaleToolAction.setStatusTip("Price Modal Scale Tool")
        self.priceModalScaleToolAction.setCheckable(True)
        
        # Create the PlanetLongitudeMovementMeasurementToolAction
        icon = QIcon(":/images/rluu/planetLongitudeMovementMeasurement.png")
        self.planetLongitudeMovementMeasurementToolAction = \
            QAction(icon, "Planet Longitude Movement Measurement Tool", self)
        self.planetLongitudeMovementMeasurementToolAction.\
            setStatusTip("Planet Longitude Movement Measurement Tool")
        self.planetLongitudeMovementMeasurementToolAction.setCheckable(True)
        
        # Create the TextToolAction
        icon = QIcon(":/images/tango-icon-theme-0.8.90/32x32/mimetypes/font-x-generic.png")
        self.textToolAction = \
            QAction(icon, "Text Tool", self)
        self.textToolAction.setStatusTip("Text Tool")
        self.textToolAction.setCheckable(True)

        # Create the PriceTimeInfoToolAction
        icon = QIcon(":/images/rluu/priceTimeInfo.png")
        self.priceTimeInfoToolAction = \
            QAction(icon, "Price Time Info Tool", self)
        self.priceTimeInfoToolAction.setStatusTip("Price Time Info Tool")
        self.priceTimeInfoToolAction.setCheckable(True)

        # Create the TimeRetracementToolAction
        icon = QIcon(":/images/rluu/timeRetracement.png")
        self.timeRetracementToolAction = \
            QAction(icon, "Time Retracement Tool", self)
        self.timeRetracementToolAction.setStatusTip("Time Retracement Tool")
        self.timeRetracementToolAction.setCheckable(True)

        # Create the PriceRetracementToolAction
        icon = QIcon(":/images/rluu/priceRetracement.png")
        self.priceRetracementToolAction = \
            QAction(icon, "Price Retracement Tool", self)
        self.priceRetracementToolAction.setStatusTip("Price Retracement Tool")
        self.priceRetracementToolAction.setCheckable(True)

        # Create the PriceTimeVectorToolAction
        icon = QIcon(":/images/rluu/ptv.png")
        self.priceTimeVectorToolAction = \
            QAction(icon, "Price Time Vector Tool", self)
        self.priceTimeVectorToolAction.setStatusTip("Price Time Vector Tool")
        self.priceTimeVectorToolAction.setCheckable(True)

        # Create the LineSegment1ToolAction
        icon = QIcon(":/images/rluu/lineSegment.png")
        self.lineSegment1ToolAction = \
            QAction(icon, "Line Segment 1 Tool", self)
        self.lineSegment1ToolAction.setStatusTip("Line Segment 1 Tool")
        self.lineSegment1ToolAction.setCheckable(True)

        # Create the LineSegment2ToolAction
        icon = QIcon(":/images/rluu/lineSegment.png")
        self.lineSegment2ToolAction = \
            QAction(icon, "Line Segment 2 Tool", self)
        self.lineSegment2ToolAction.setStatusTip("Line Segment 2 Tool")
        self.lineSegment2ToolAction.setCheckable(True)

        # Create the OctaveFanToolAction
        icon = QIcon(":/images/rluu/octaveFan.png")
        self.octaveFanToolAction = \
            QAction(icon, "Octave Fan Tool", self)
        self.octaveFanToolAction.setStatusTip("Octave Fan Tool")
        self.octaveFanToolAction.setCheckable(True)

        # Create the FibFanToolAction
        icon = QIcon(":/images/rluu/fibFan.png")
        self.fibFanToolAction = \
            QAction(icon, "Fib Fan Tool", self)
        self.fibFanToolAction.setStatusTip("Fibonacci Fan Tool")
        self.fibFanToolAction.setCheckable(True)

        # Create the GannFanToolAction
        icon = QIcon(":/images/rluu/gannFan.png")
        self.gannFanToolAction = \
            QAction(icon, "Gann Fan Tool", self)
        self.gannFanToolAction.setStatusTip("Gann Fan Tool")
        self.gannFanToolAction.setCheckable(True)

        # Create the VimsottariDasaToolAction
        icon = QIcon(":/images/rluu/vimsottariDasa.png")
        self.vimsottariDasaToolAction = \
            QAction(icon, "Vimsottari Dasa Tool", self)
        self.vimsottariDasaToolAction.\
            setStatusTip("Vimsottari Dasa Tool")
        self.vimsottariDasaToolAction.setCheckable(True)

        # Create the AshtottariDasaToolAction
        icon = QIcon(":/images/rluu/ashtottariDasa.png")
        self.ashtottariDasaToolAction = \
            QAction(icon, "Ashtottari Dasa Tool", self)
        self.ashtottariDasaToolAction.\
            setStatusTip("Ashtottari Dasa Tool")
        self.ashtottariDasaToolAction.setCheckable(True)

        # Create the YoginiDasaToolAction
        icon = QIcon(":/images/rluu/yoginiDasa.png")
        self.yoginiDasaToolAction = \
            QAction(icon, "Yogini Dasa Tool", self)
        self.yoginiDasaToolAction.\
            setStatusTip("Yogini Dasa Tool")
        self.yoginiDasaToolAction.setCheckable(True)

        # Create the DwisaptatiSamaDasaToolAction
        icon = QIcon(":/images/rluu/dwisaptatiSamaDasa.png")
        self.dwisaptatiSamaDasaToolAction = \
            QAction(icon, "DwisaptatiSama Dasa Tool", self)
        self.dwisaptatiSamaDasaToolAction.\
            setStatusTip("DwisaptatiSama Dasa Tool")
        self.dwisaptatiSamaDasaToolAction.setCheckable(True)

        # Create the ShattrimsaSamaDasaToolAction
        icon = QIcon(":/images/rluu/shattrimsaSamaDasa.png")
        self.shattrimsaSamaDasaToolAction = \
            QAction(icon, "ShattrimsaSama Dasa Tool", self)
        self.shattrimsaSamaDasaToolAction.\
            setStatusTip("ShattrimsaSama Dasa Tool")
        self.shattrimsaSamaDasaToolAction.setCheckable(True)

        # Create the DwadasottariDasaToolAction
        icon = QIcon(":/images/rluu/dwadasottariDasa.png")
        self.dwadasottariDasaToolAction = \
            QAction(icon, "Dwadasottari Dasa Tool", self)
        self.dwadasottariDasaToolAction.\
            setStatusTip("Dwadasottari Dasa Tool")
        self.dwadasottariDasaToolAction.setCheckable(True)

        # Create the ChaturaseetiSamaDasaToolAction
        icon = QIcon(":/images/rluu/chaturaseetiSamaDasa.png")
        self.chaturaseetiSamaDasaToolAction = \
            QAction(icon, "ChaturaseetiSama Dasa Tool", self)
        self.chaturaseetiSamaDasaToolAction.\
            setStatusTip("ChaturaseetiSama Dasa Tool")
        self.chaturaseetiSamaDasaToolAction.setCheckable(True)

        # Create the SataabdikaDasaToolAction
        icon = QIcon(":/images/rluu/sataabdikaDasa.png")
        self.sataabdikaDasaToolAction = \
            QAction(icon, "Sataabdika Dasa Tool", self)
        self.sataabdikaDasaToolAction.\
            setStatusTip("Sataabdika Dasa Tool")
        self.sataabdikaDasaToolAction.setCheckable(True)

        # Create the ShodasottariDasaToolAction
        icon = QIcon(":/images/rluu/shodasottariDasa.png")
        self.shodasottariDasaToolAction = \
            QAction(icon, "Shodasottari Dasa Tool", self)
        self.shodasottariDasaToolAction.\
            setStatusTip("Shodasottari Dasa Tool")
        self.shodasottariDasaToolAction.setCheckable(True)

        # Create the PanchottariDasaToolAction
        icon = QIcon(":/images/rluu/panchottariDasa.png")
        self.panchottariDasaToolAction = \
            QAction(icon, "Panchottari Dasa Tool", self)
        self.panchottariDasaToolAction.\
            setStatusTip("Panchottari Dasa Tool")
        self.panchottariDasaToolAction.setCheckable(True)

        # Create the ShashtihayaniDasaToolAction
        icon = QIcon(":/images/rluu/shashtihayaniDasa.png")
        self.shashtihayaniDasaToolAction = \
            QAction(icon, "Shashtihayani Dasa Tool", self)
        self.shashtihayaniDasaToolAction.\
            setStatusTip("Shashtihayani Dasa Tool")
        self.shashtihayaniDasaToolAction.setCheckable(True)

        # Create a QActionGroup because all these tool modes should be
        # exclusive.  
        self.toolActionGroup = QActionGroup(self)
        self.toolActionGroup.setExclusive(True)
        self.toolActionGroup.addAction(self.readOnlyPointerToolAction)
        self.toolActionGroup.addAction(self.pointerToolAction)
        self.toolActionGroup.addAction(self.handToolAction)
        self.toolActionGroup.addAction(self.zoomInToolAction)
        self.toolActionGroup.addAction(self.zoomOutToolAction)
        self.toolActionGroup.addAction(self.barCountToolAction)
        self.toolActionGroup.addAction(self.timeMeasurementToolAction)
        self.toolActionGroup.addAction(self.priceMeasurementToolAction)
        self.toolActionGroup.addAction(self.timeModalScaleToolAction)
        self.toolActionGroup.addAction(self.priceModalScaleToolAction)
        self.toolActionGroup.addAction(self.timeRetracementToolAction)
        self.toolActionGroup.addAction(self.priceRetracementToolAction)
        self.toolActionGroup.\
            addAction(self.planetLongitudeMovementMeasurementToolAction)
        self.toolActionGroup.addAction(self.textToolAction)
        self.toolActionGroup.addAction(self.priceTimeInfoToolAction)
        self.toolActionGroup.addAction(self.priceTimeVectorToolAction)
        self.toolActionGroup.addAction(self.lineSegment1ToolAction)
        self.toolActionGroup.addAction(self.lineSegment2ToolAction)
        self.toolActionGroup.addAction(self.octaveFanToolAction)
        self.toolActionGroup.addAction(self.fibFanToolAction)
        self.toolActionGroup.addAction(self.gannFanToolAction)
        self.toolActionGroup.addAction(self.vimsottariDasaToolAction)
        self.toolActionGroup.addAction(self.ashtottariDasaToolAction)
        self.toolActionGroup.addAction(self.yoginiDasaToolAction)
        self.toolActionGroup.addAction(self.dwisaptatiSamaDasaToolAction)
        self.toolActionGroup.addAction(self.shattrimsaSamaDasaToolAction)
        self.toolActionGroup.addAction(self.dwadasottariDasaToolAction)
        self.toolActionGroup.addAction(self.chaturaseetiSamaDasaToolAction)
        self.toolActionGroup.addAction(self.sataabdikaDasaToolAction)
        self.toolActionGroup.addAction(self.shodasottariDasaToolAction)
        self.toolActionGroup.addAction(self.panchottariDasaToolAction)
        self.toolActionGroup.addAction(self.shashtihayaniDasaToolAction)
        self.toolActionGroup.triggered.connect(self._toolsActionTriggered)
            
        # Default to the ReadOnlyPointerTool being checked by default.
        self.readOnlyPointerToolAction.setChecked(True)

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

        self.showShortcutKeysAction = \
            QAction(QIcon(":/images/downloadatoz.com/MLHotKey.icon.gif"),
                    "&Shortcut Keys", self)
        self.showShortcutKeysAction.setStatusTip("Show shortcut keys")
        self.showShortcutKeysAction.triggered.connect(self._showShortcutKeys)
        
        self.memoryUsageAction = QAction(self.appIcon, "&Memory Usage", self)
        self.memoryUsageAction.\
            setStatusTip("Show application memory utilization.")
        self.memoryUsageAction.triggered.connect(self._memoryUsage)

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
        self.fileMenu.addAction(\
            self.checkSourceDataFileForPriceBarUpdatesAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.printPreviewAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAppAction)

        # Create the Edit menu.
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.editAppPreferencesAction)
        self.editMenu.addAction(self.editBirthInfoAction)
        self.editMenu.addAction(self.editPriceChartDocumentDataAction)
        self.editMenu.addAction(self.editPriceBarChartSettingsAction)
        self.editMenu.addAction(self.editPriceBarChartScalingAction)

        # Create the Astro menu.
        self.astroMenu = self.menuBar().addMenu("&Astro")
        self.astroMenu.addAction(self.enableAndShowAstrologyChartAction)
        self.astroMenu.addAction(self.enableAndShowPlanetaryInfoTableAction)
        self.astroMenu.addSeparator()
        self.astroMenu.addAction(self.trackMouseToAstroChart1Action)
        self.astroMenu.addAction(self.trackMouseToAstroChart2Action)
        self.astroMenu.addAction(self.trackMouseToAstroChart3Action)
        self.astroMenu.addSeparator()
        self.astroMenu.addAction(self.openJHoraWithNoArgsAction)
        self.astroMenu.addAction(self.openJHoraWithLocalizedNowAction)
        self.astroMenu.addAction(self.openJHoraWithBirthInfoAction)
        self.astroMenu.addSeparator()
        self.astroMenu.addAction(self.openAstrologWithNoArgsAction)
        self.astroMenu.addAction(self.openAstrologWithLocalizedNowAction)
        self.astroMenu.addAction(self.openAstrologWithBirthInfoAction)
        self.astroMenu.addSeparator()
        self.astroMenu.addAction(self.openAstroChart1WithBirthInfoAction)
        self.astroMenu.addAction(self.openAstroChart2WithBirthInfoAction)
        self.astroMenu.addAction(self.openAstroChart3WithBirthInfoAction)
        self.astroMenu.addSeparator()
        self.astroMenu.addAction(self.openAstroChart1WithNowAction)
        self.astroMenu.addAction(self.openAstroChart2WithNowAction)
        self.astroMenu.addAction(self.openAstroChart3WithNowAction)
        self.astroMenu.addSeparator()
        self.astroMenu.addAction(self.clearAstroChart1Action)
        self.astroMenu.addAction(self.clearAstroChart2Action)
        self.astroMenu.addAction(self.clearAstroChart3Action)
        
        # Create the Tools menu
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.toolsMenu.addAction(self.readOnlyPointerToolAction)
        self.toolsMenu.addAction(self.pointerToolAction)
        self.toolsMenu.addAction(self.handToolAction)
        self.toolsMenu.addAction(self.zoomInToolAction)
        self.toolsMenu.addAction(self.zoomOutToolAction)
        self.toolsMenu.addAction(self.barCountToolAction)
        self.toolsMenu.addAction(self.timeMeasurementToolAction)
        self.toolsMenu.addAction(self.priceMeasurementToolAction)
        self.toolsMenu.addAction(self.timeModalScaleToolAction)
        self.toolsMenu.addAction(self.priceModalScaleToolAction)
        self.toolsMenu.addAction(self.timeRetracementToolAction)
        self.toolsMenu.addAction(self.priceRetracementToolAction)
        self.toolsMenu.\
            addAction(self.planetLongitudeMovementMeasurementToolAction)
        self.toolsMenu.addAction(self.textToolAction)
        self.toolsMenu.addAction(self.priceTimeInfoToolAction)
        self.toolsMenu.addAction(self.priceTimeVectorToolAction)
        self.toolsMenu.addAction(self.lineSegment1ToolAction)
        self.toolsMenu.addAction(self.lineSegment2ToolAction)
        self.toolsMenu.addAction(self.octaveFanToolAction)
        self.toolsMenu.addAction(self.fibFanToolAction)
        self.toolsMenu.addAction(self.gannFanToolAction)
        self.toolsMenu.addAction(self.vimsottariDasaToolAction)
        self.toolsMenu.addAction(self.ashtottariDasaToolAction)
        self.toolsMenu.addAction(self.yoginiDasaToolAction)
        self.toolsMenu.addAction(self.dwisaptatiSamaDasaToolAction)
        self.toolsMenu.addAction(self.shattrimsaSamaDasaToolAction)
        self.toolsMenu.addAction(self.dwadasottariDasaToolAction)
        self.toolsMenu.addAction(self.chaturaseetiSamaDasaToolAction)
        self.toolsMenu.addAction(self.sataabdikaDasaToolAction)
        self.toolsMenu.addAction(self.shodasottariDasaToolAction)
        self.toolsMenu.addAction(self.panchottariDasaToolAction)
        self.toolsMenu.addAction(self.shashtihayaniDasaToolAction)

        # Create the Window menu.
        self.windowMenu = self.menuBar().addMenu("&Window")
        self._updateWindowMenu()

        # Add a separator between the Window menu and the Help menu.
        self.menuBar().addSeparator()

        # Create the Help menu.
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.showShortcutKeysAction)
        self.helpMenu.addAction(self.memoryUsageAction)
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
        self.fileToolBar.addAction(\
            self.checkSourceDataFileForPriceBarUpdatesAction)
        self.fileToolBar.addSeparator()
        # This action is shown on the toolbar only for non-Mac
        # platforms because it takes too much space on the toolbar on
        # Macbook Pro laptop.  
        if platform.system() != "Darwin":
            self.fileToolBar.addAction(self.printAction)
            self.fileToolBar.addAction(self.printPreviewAction)
        
        # Create the Edit toolbar.
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.setObjectName("editToolBar")
        self.editToolBar.addAction(self.editAppPreferencesAction)
        self.editToolBar.addAction(self.editBirthInfoAction)
        self.editToolBar.addAction(self.editPriceChartDocumentDataAction)
        self.editToolBar.addAction(self.editPriceBarChartSettingsAction)
        self.editToolBar.addAction(self.editPriceBarChartScalingAction)

        # Create the Tools toolbar.
        self.toolsToolBar = self.addToolBar("Tools")
        self.toolsToolBar.setObjectName("toolsToolBar")
        self.toolsToolBar.addAction(self.readOnlyPointerToolAction)
        self.toolsToolBar.addAction(self.pointerToolAction)
        self.toolsToolBar.addAction(self.handToolAction)
        self.toolsToolBar.addAction(self.zoomInToolAction)
        self.toolsToolBar.addAction(self.zoomOutToolAction)
        self.toolsToolBar.addAction(self.barCountToolAction)
        self.toolsToolBar.addAction(self.timeMeasurementToolAction)
        self.toolsToolBar.addAction(self.priceMeasurementToolAction)
        self.toolsToolBar.addAction(self.timeModalScaleToolAction)
        self.toolsToolBar.addAction(self.priceModalScaleToolAction)
        self.toolsToolBar.addAction(self.timeRetracementToolAction)
        self.toolsToolBar.addAction(self.priceRetracementToolAction)
        self.toolsToolBar.\
            addAction(self.planetLongitudeMovementMeasurementToolAction)
        self.toolsToolBar.addAction(self.textToolAction)
        self.toolsToolBar.addAction(self.priceTimeInfoToolAction)
        # This action is shown on the toolbar only for non-Mac
        # platforms because it takes too much space on the toolbar on
        # Macbook Pro laptop.  
        if platform.system() != "Darwin":
            self.toolsToolBar.addAction(self.priceTimeVectorToolAction)
        self.toolsToolBar.addAction(self.lineSegment1ToolAction)
        self.toolsToolBar.addAction(self.lineSegment2ToolAction)
        self.toolsToolBar.addAction(self.octaveFanToolAction)
        self.toolsToolBar.addAction(self.fibFanToolAction)
        self.toolsToolBar.addAction(self.gannFanToolAction)
        self.toolsToolBar.addAction(self.vimsottariDasaToolAction)
        self.toolsToolBar.addAction(self.ashtottariDasaToolAction)
        self.toolsToolBar.addAction(self.yoginiDasaToolAction)
        self.toolsToolBar.addAction(self.dwisaptatiSamaDasaToolAction)
        self.toolsToolBar.addAction(self.shattrimsaSamaDasaToolAction)
        self.toolsToolBar.addAction(self.dwadasottariDasaToolAction)
        self.toolsToolBar.addAction(self.chaturaseetiSamaDasaToolAction)
        self.toolsToolBar.addAction(self.sataabdikaDasaToolAction)
        self.toolsToolBar.addAction(self.shodasottariDasaToolAction)
        self.toolsToolBar.addAction(self.panchottariDasaToolAction)
        self.toolsToolBar.addAction(self.shashtihayaniDasaToolAction)

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
        self.checkSourceDataFileForPriceBarUpdatesAction.setEnabled(isActive)
        self.printAction.setEnabled(isActive)
        self.printPreviewAction.setEnabled(isActive)
        self.exitAppAction.setEnabled(True)

        self.editAppPreferencesAction.setEnabled(True)
        self.editBirthInfoAction.setEnabled(isActive)
        self.editPriceChartDocumentDataAction.setEnabled(isActive)
        self.editPriceBarChartSettingsAction.setEnabled(isActive)
        self.editPriceBarChartScalingAction.setEnabled(isActive)

        self.enableAndShowAstrologyChartAction.setEnabled(isActive)
        self.enableAndShowPlanetaryInfoTableAction.setEnabled(isActive)
        self.trackMouseToAstroChart1Action.setEnabled(isActive)
        self.trackMouseToAstroChart2Action.setEnabled(isActive)
        self.trackMouseToAstroChart3Action.setEnabled(isActive)
        self.openJHoraWithNoArgsAction.setEnabled(True)
        self.openJHoraWithLocalizedNowAction.setEnabled(isActive)
        self.openJHoraWithBirthInfoAction.setEnabled(isActive)
        self.openAstrologWithNoArgsAction.setEnabled(True)
        self.openAstrologWithLocalizedNowAction.setEnabled(isActive)
        self.openAstrologWithBirthInfoAction.setEnabled(isActive)
        self.openAstroChart1WithBirthInfoAction.setEnabled(isActive)
        self.openAstroChart2WithBirthInfoAction.setEnabled(isActive)
        self.openAstroChart3WithBirthInfoAction.setEnabled(isActive)
        self.openAstroChart1WithNowAction.setEnabled(isActive)
        self.openAstroChart2WithNowAction.setEnabled(isActive)
        self.openAstroChart3WithNowAction.setEnabled(isActive)
        self.clearAstroChart1Action.setEnabled(isActive)
        self.clearAstroChart2Action.setEnabled(isActive)
        self.clearAstroChart3Action.setEnabled(isActive)

        self.readOnlyPointerToolAction.setEnabled(isActive)
        self.pointerToolAction.setEnabled(isActive)
        self.handToolAction.setEnabled(isActive)
        self.zoomInToolAction.setEnabled(isActive)
        self.zoomOutToolAction.setEnabled(isActive)
        self.barCountToolAction.setEnabled(isActive)
        self.timeMeasurementToolAction.setEnabled(isActive)
        self.timeModalScaleToolAction.setEnabled(isActive)
        self.priceModalScaleToolAction.setEnabled(isActive)
        self.planetLongitudeMovementMeasurementToolAction.setEnabled(isActive)
        self.textToolAction.setEnabled(isActive)
        self.priceTimeInfoToolAction.setEnabled(isActive)
        self.priceMeasurementToolAction.setEnabled(isActive)
        self.timeRetracementToolAction.setEnabled(isActive)
        self.priceRetracementToolAction.setEnabled(isActive)
        self.priceTimeVectorToolAction.setEnabled(isActive)
        self.lineSegment1ToolAction.setEnabled(isActive)
        self.lineSegment2ToolAction.setEnabled(isActive)
        self.octaveFanToolAction.setEnabled(isActive)
        self.fibFanToolAction.setEnabled(isActive)
        self.gannFanToolAction.setEnabled(isActive)
        self.vimsottariDasaToolAction.setEnabled(isActive)
        self.ashtottariDasaToolAction.setEnabled(isActive)
        self.yoginiDasaToolAction.setEnabled(isActive)
        self.dwisaptatiSamaDasaToolAction.setEnabled(isActive)
        self.shattrimsaSamaDasaToolAction.setEnabled(isActive)
        self.dwadasottariDasaToolAction.setEnabled(isActive)
        self.chaturaseetiSamaDasaToolAction.setEnabled(isActive)
        self.sataabdikaDasaToolAction.setEnabled(isActive)
        self.shodasottariDasaToolAction.setEnabled(isActive)
        self.panchottariDasaToolAction.setEnabled(isActive)
        self.shashtihayaniDasaToolAction.setEnabled(isActive)

        self.closeChartAction.setEnabled(isActive)
        self.closeAllChartsAction.setEnabled(isActive)
        self.tileSubWindowsAction.setEnabled(isActive)
        self.cascadeSubWindowsAction.setEnabled(isActive)
        self.nextSubWindowAction.setEnabled(isActive)
        self.previousSubWindowAction.setEnabled(isActive)

        self.memoryUsageAction.setEnabled(True)
        self.aboutAction.setEnabled(True)
        self.aboutQtAction.setEnabled(True)

        # Depending on whether or not the trackMouseToAstroChart
        # actions are checked, then set the priceChartDocument to
        # correspond to that.
        if isActive:
            flag = self.enableAndShowAstrologyChartAction.isChecked()
            priceChartDocument.setEnableAndShowAstrologyChart(flag)

            flag = self.enableAndShowPlanetaryInfoTableAction.isChecked()
            priceChartDocument.setEnableAndShowPlanetaryInfoTable(flag)
            
            flag = self.trackMouseToAstroChart1Action.isChecked()
            priceChartDocument.setTrackMouseToAstroChart1(flag)

            flag = self.trackMouseToAstroChart2Action.isChecked()
            priceChartDocument.setTrackMouseToAstroChart2(flag)

            flag = self.trackMouseToAstroChart3Action.isChecked()
            priceChartDocument.setTrackMouseToAstroChart3(flag)
        
        # Depending on what ToolMode QAction is checked,
        # set the priceChartDocument to be in that mode.
        if isActive:
            if self.readOnlyPointerToolAction.isChecked():
                priceChartDocument.toReadOnlyPointerToolMode()
            elif self.pointerToolAction.isChecked():
                priceChartDocument.toPointerToolMode()
            elif self.handToolAction.isChecked():
                priceChartDocument.toHandToolMode()
            elif self.zoomInToolAction.isChecked():
                priceChartDocument.toZoomInToolMode()
            elif self.zoomOutToolAction.isChecked():
                priceChartDocument.toZoomOutToolMode()
            elif self.barCountToolAction.isChecked():
                priceChartDocument.toBarCountToolMode()
            elif self.timeMeasurementToolAction.isChecked():
                priceChartDocument.toTimeMeasurementToolMode()
            elif self.timeModalScaleToolAction.isChecked():
                priceChartDocument.toTimeModalScaleToolMode()
            elif self.priceModalScaleToolAction.isChecked():
                priceChartDocument.toPriceModalScaleToolMode()
            elif self.planetLongitudeMovementMeasurementToolAction.isChecked():
                priceChartDocument.\
                    toPlanetLongitudeMovementMeasurementToolMode()
            elif self.textToolAction.isChecked():
                priceChartDocument.toTextToolMode()
            elif self.priceTimeInfoToolAction.isChecked():
                priceChartDocument.toPriceTimeInfoToolMode()
            elif self.priceMeasurementToolAction.isChecked():
                priceChartDocument.toPriceMeasurementToolMode()
            elif self.timeRetracementToolAction.isChecked():
                priceChartDocument.toTimeRetracementToolMode()
            elif self.priceRetracementToolAction.isChecked():
                priceChartDocument.toPriceRetracementToolMode()
            elif self.priceTimeVectorToolAction.isChecked():
                priceChartDocument.toPriceTimeVectorToolMode()
            elif self.lineSegment1ToolAction.isChecked():
                priceChartDocument.toLineSegment1ToolMode()
            elif self.lineSegment2ToolAction.isChecked():
                priceChartDocument.toLineSegment2ToolMode()
            elif self.octaveFanToolAction.isChecked():
                priceChartDocument.toOctaveFanToolMode()
            elif self.fibFanToolAction.isChecked():
                priceChartDocument.toFibFanToolMode()
            elif self.gannFanToolAction.isChecked():
                priceChartDocument.toGannFanToolMode()
            elif self.vimsottariDasaToolAction.isChecked():
                priceChartDocument.toVimsottariDasaToolMode()
            elif self.ashtottariDasaToolAction.isChecked():
                priceChartDocument.toAshtottariDasaToolMode()
            elif self.yoginiDasaToolAction.isChecked():
                priceChartDocument.toYoginiDasaToolMode()
            elif self.dwisaptatiSamaDasaToolAction.isChecked():
                priceChartDocument.toDwisaptatiSamaDasaToolMode()
            elif self.shattrimsaSamaDasaToolAction.isChecked():
                priceChartDocument.toShattrimsaSamaDasaToolMode()
            elif self.dwadasottariDasaToolAction.isChecked():
                priceChartDocument.toDwadasottariDasaToolMode()
            elif self.chaturaseetiSamaDasaToolAction.isChecked():
                priceChartDocument.toChaturaseetiSamaDasaToolMode()
            elif self.sataabdikaDasaToolAction.isChecked():
                priceChartDocument.toSataabdikaDasaToolMode()
            elif self.shodasottariDasaToolAction.isChecked():
                priceChartDocument.toShodasottariDasaToolMode()
            elif self.panchottariDasaToolAction.isChecked():
                priceChartDocument.toPanchottariDasaToolMode()
            elif self.shashtihayaniDasaToolAction.isChecked():
                priceChartDocument.toShashtihayaniDasaToolMode()
            else:
                self.log.warn("No ToolMode QAction is currently selected!")


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
                
                # Increment counter for the window number in the Window
                # menu.
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
        key = "ui/MainWindow/windowGeometry"
        if not settings.contains(key):
            self.windowGeometry = QByteArray()
        else:
            self.windowGeometry = \
                settings.value(key,
                               defaultValue=None,
                               type=QByteArray)
            if self.windowGeometry == None:
                self.windowGeometry = QByteArray()
            
        # Window state.
        key = "ui/MainWindow/windowState"
        if not settings.contains(key):
            self.windowState = QByteArray()
        else:
            self.windowState = \
                settings.value(key,
                               defaultValue=None,
                               type=QByteArray)
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
        key = "ui/MainWindow/windowGeometry"
        if not settings.contains(key) or \
               settings.value(key,
                              defaultValue=None,
                              type=QByteArray) != self.saveGeometry():
                
            settings.setValue(key, self.saveGeometry())
            

        # Window state.
        key = "ui/MainWindow/windowState"
        if not settings.contains(key) or \
               settings.value(key,
                              defaultValue=None,
                              type=QByteArray) != self.saveState():
                
            settings.setValue(key, self.saveState())


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

            # Debug output:
            self.log.debug("Data filename is: " + \
                           wizard.field("dataFilename"))
            self.log.debug("Data num lines to skip is: {}".\
                format(wizard.field("dataNumLinesToSkip")))
            self.log.debug("Timezone is: " + wizard.field("timezone"))
            self.log.debug("Description is: " + wizard.field("description"))


            # Create the document data.
            priceChartDocumentData = PriceChartDocumentData()

            # Load data into it.
            priceChartDocumentData.\
                loadWizardData(wizard.getPriceBars(),
                               wizard.field("dataFilename"),
                               wizard.field("dataNumLinesToSkip"),
                               wizard.field("timezone"),
                               wizard.field("description"))

            # Create a PriceChartDocument with the data.
            priceChartDocument = PriceChartDocument()
            priceChartDocument.\
                setPriceChartDocumentData(priceChartDocumentData)

            # Connect the signal for updating the status bar message.
            priceChartDocument.statusMessageUpdate[str].\
                connect(self.showInStatusBar)

            # Connect signal for launching JHora.
            priceChartDocument.jhoraLaunch.\
                connect(self.handleJhoraLaunch)

            # Connect signal for launching Astrolog.
            priceChartDocument.astrologLaunch.\
                connect(self.handleAstrologLaunch)

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
            settings.value("ui/defaultPriceChartDocumentOpenDirectory",
                           defaultValue="",
                           type=str)

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

                # Connect signal for launching JHora.
                priceChartDocument.jhoraLaunch.\
                    connect(self.handleJhoraLaunch)

                # Connect signal for launching Astrolog.
                priceChartDocument.astrologLaunch.\
                    connect(self.handleAstrologLaunch)

                # Now Add this priceChartDocument to the list of subwindows
                self._addSubWindow(priceChartDocument)

                # Update the statusbar to tell what file was opened.
                statusBarMessage = \
                    "Opened PriceChartDocument {}.".format(filename)

                self.showInStatusBar(statusBarMessage)

                # Update the QSettings value for the default open
                # location if the directory is different.
                
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

    def _handleCheckSourceDataFileForPriceBarUpdatesAction(self):
        """Handles when the
        self.checkSourceDataFileForPriceBarUpdatesAction QAction is
        triggered.  Here we check for any updates to PriceBar data
        from the current active PriceChartDocument's backing CSV data
        file.
        """

        self.log.debug("Entered " +
                       "_handleCheckSourceDataFileForPriceBarUpdatesAction")

        subwindow = self.mdiArea.currentSubWindow()

        if isinstance(subwindow, PriceChartDocument) == True:
            priceChartDocument = subwindow

            priceChartDocument.checkSourceDataFileForPriceBarUpdates()
            
        self.log.debug("Exiting " +
                       "_handleCheckSourceDataFileForPriceBarUpdatesAction")
        
    def handleJhoraLaunch(self, dt=None, birthInfo=None):
        """Opens JHora with the given datetime.datetime timestamp.
        Uses the currently set self.birthInfo object for timezone
        information.

        If 'dt' is None, then JHora is opened without any arguments given.
        Otherwise, both 'dt' and 'birthInfo' need to be set.
        
        Arguments:
        
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in JHora.  If dt is None, then
             JHora is opened without any arguments.

        birthInfo - BirthInfo object holding information about the
                    location/altitude and timezone.  This must be set
                    if 'dt' is not None.
        """

        self.log.debug("Entered handleJhoraLaunch()")

        # Check to make sure inputs are provided as expected.
        if dt == None:
            # Just open JHora without any file specified.
            self.log.debug("dt == None and birthInfo == None.")
            
            # Launch JHora.
            self._execJHora()
            
        elif dt != None and birthInfo != None:
            # Normal case for specifying a timestamp with birthInfo.
            self.log.debug("dt != None and birthInfo != None.")
            
        else:
            self.log.error("If 'dt' argument is provided, " +
                           "then birthInfo cannot be None.") 
            return
        
        self.log.debug("Values being used: " +
                       "dt='{}', birthInfo='{}'".\
                       format(Ephemeris.datetimeToStr(dt),
                              birthInfo.toString()))

        
        # This is chart destination directory path, in the filename format
        # readable on the current operating system.
        chartDestPath = ""

        # This is the chart destination directory path, in the filename format
        # readable on Posix systems (Unix, Linux, Mac OS X).
        chartDestPathPosix = ""
        
        # This is the chart destination directory path, in the filename format
        # readable on Microsoft Windows systems.
        chartDestPathWin = ""

        # Create the appropriate directory and return the paths.
        (chartDestPath, chartDestPathPosix, chartDestPathWin) = \
            self._getJHoraChartDestPath()

        self.log.debug("chartDestPath == " + chartDestPath)
        self.log.debug("chartDestPathPosix == " + chartDestPathPosix)
        self.log.debug("chartDestPathWin == " + chartDestPathWin)
        
        # Create the file to open JHora with.
        filenameTemplate = chartDestPath + os.sep + \
                           "tmp_" + self.appName + "_XXXXXX.jhd"
        self.log.debug("filenameTemplate == " + filenameTemplate)
        
        f = QTemporaryFile(filenameTemplate)

        # Need to disable auto-remove because the QTemporaryFile gets
        # destroyed (garbage collected) before JHora is launched and
        # can read the file.
        f.setAutoRemove(False)

        if f.open(QIODevice.ReadWrite):
            
            # Get the text to go into the file from the input parameters.
            text = self._generateJHoraFileText(dt, birthInfo)

            # Write to the file.
            utf8EncodedText = text.encode('utf-8')
            f.writeData(utf8EncodedText)
            f.close()

            # Launch JHora with the file just created.

            # Get the filename in the Windows path format since that's
            # all wine or Windows knows how to see.
            filename = chartDestPathWin + "\\" + \
                       os.path.basename(f.fileName())
            
            self.log.debug("f.fileName() == " + f.fileName())
            self.log.debug("filename == " + filename)

            self._execJHora(filename)
            
        else:
            errMsg = "JHora launch failed because: " + os.linesep + \
                     "Could not open a temporary file for JHora."
            self.log.error(errMsg)
            
            title = "Error"
            text = errMsg
            buttons = QMessageBox.Ok
            defaultButton = QMessageBox.NoButton
            
            QMessageBox.warning(self, title, text, buttons, defaultButton)
            
        
        self.log.debug("Exiting handleJhoraLaunch()")

    def _getJHoraChartDestPath(self):
        """Returns a tuple of 3 paths (based on operating system) for
        where the JHora .jhd files will be saved to.  The formula for
        this path is based on operating system and application name.
        See code below for details.  This function also creates the
        directory if it doesn't exist already.

        Returns:
        tuple of three items:
           - chartDestPath (str)
               This is chart destination directory path, in the
               filename format readable on the current operating system.
           - chartDestPathPosix (str)
               This is the chart destination directory path, in the
               filename format readable on Posix systems (Unix, Linux,
               Mac OS X).
           - chartDestPathWin (str)
               This is the chart destination directory path, in the
               filename format readable on Microsoft Windows systems.
        """

        self.log.debug("Entered _getJHoraChartDestPath()")
        
        # Make a directory to store our temporary JHora .jhd files.
        # Optimally, we would like to place it within JHora's 'data'
        # directory, but that doesn't work because that directory path
        # has spaces and os.makedirs() will choke on that.

        # This is chart destination directory path, in the filename format
        # readable on the current operating system.
        chartDestPath = ""

        # This is the chart destination directory path, in the filename format
        # readable on Posix systems (Unix, Linux, Mac OS X).
        chartDestPathPosix = ""
        
        # This is the chart destination directory path, in the filename format
        # readable on Microsoft Windows systems.
        chartDestPathWin = ""
        
        try:
            if os.name == "posix":
                self.log.debug("posix")

                chartDestPathPosix = \
                    os.path.expanduser('~') + os.sep + \
                    ".wine/drive_c/" + self.appName + "/data"
                chartDestPathWin = \
                    "C:\\" + self.appName + "\\data"
                
                self.log.debug("chartDestPathPosix == " + chartDestPathPosix)
                self.log.debug("chartDestPathWin == " + chartDestPathWin)
                self.log.debug("os.path.exists(chartDestPathPosix) == {}".\
                               format(os.path.exists(chartDestPathPosix)))
                self.log.debug("os.path.isdir(chartDestPathPosix) == {}".\
                               format(os.path.isdir(chartDestPathPosix)))
                
                if os.path.exists(chartDestPathPosix) and \
                       os.path.isdir(chartDestPathPosix):
                    
                    self.log.debug("Good, directory exists: " +
                                   chartDestPathPosix)
                    
                else:
                    self.log.debug("making dirs: " + chartDestPathPosix)
                    os.makedirs(chartDestPathPosix)

                    
                chartDestPath = chartDestPathPosix
                
            elif os.name == "nt":
                self.log.debug("nt")
            
                chartDestPathWin = \
                    "C:\\" + self.appName + "\\data"

                self.log.debug("chartDestPathWin == " + chartDestPathWin)
                self.log.debug("os.path.exists(chartDestPathWin) == {}".\
                               format(os.path.exists(chartDestPathWin)))
                self.log.debug("os.path.isdir(chartDestPathWin) == {}".\
                               format(os.path.isdir(chartDestPathWin)))
                
                if os.path.exists(chartDestPathWin) and \
                       os.path.isdir(chartDestPathWin):
                    
                    self.log.debug("Good, directory exists: " + \
                                   chartDestPathWin)
                else:
                    self.log.debug("making dirs: " + chartDestPathWin)
                    os.makedirs(chartDestPathWin)

                chartDestPath = chartDestPathWin
                
            else:
                self.log.warn("Operating system unsupported: " + os.name)
                return
            
        except os.error as e:
            
            self.log.error("Error while trying to ensure the " +
                           "JHora chart destination directory exists.  " +
                           "{}".format(e))
            
        self.log.debug("chartDestPath == " + chartDestPath)
        self.log.debug("chartDestPathPosix == " + chartDestPathPosix)
        self.log.debug("chartDestPathWin == " + chartDestPathWin)
        
        self.log.debug("Exiting _getJHoraChartDestPath()")
        
        return (chartDestPath, chartDestPathPosix, chartDestPathWin)
    
    def _execJHora(self, filename=None):
        """Runs the executable JHora.

        Arguments:
        
        filename - str containing the full path of the JHora .jhd to open.
                   This argument can be None if opening JHora without
                   any arguments is desired.
        """

        toExec = ""
        
        if os.name == "posix":
            
            toExec = \
                "wine " + \
                os.path.expanduser('~') + os.sep + \
                ".wine/drive_c/Program\\ Files/Jagannatha\\ Hora/bin/jhora.exe"
            
            if filename != None:
                toExec += " \"" + filename + "\""
            
            self.log.debug("Launching JHora.  toExec is: " + toExec)
            
            p = subprocess.Popen(toExec, shell=True)
            
            self.log.debug("JHora launched.")
            
        elif os.name == "nt":
            
            toExec = \
                "C:\\Program Files\\Jagannatha Hora\\bin\\jhora.exe"
            
            if filename != None:
                toExec += " \"" + filename + "\""
            
            self.log.debug("Launching JHora.  toExec is: " + toExec)

            p = subprocess.Popen(toExec)
            
            self.log.debug("JHora launched.")
            
        else:
            self.log.warn("Operating system unsupported: " + os.name)

        
        
    def _generateJHoraFileText(self, dt, birthInfo):
        """Generates the text that would be in a JHora .jhd file, for
        the information given in the specified datetime.datetime and
        BirthInfo.
        
        Arguments:
        
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in JHora.  

        birthInfo - BirthInfo object holding information about the
                    location/altitude and timezone.


        Notes on text format:

        # Format of the file is all text with Windows newlines:
        #
        # <1>\r\n
        # <2>\r\n
        # <3>\r\n
        # <4>.<5>\r\n
        # <6>.<7>\r\n
        # <8>.<9>\r\n
        # <10>.<11>\r\n
        # <12>\r\n
        # <13>\r\n
        # <14>\r\n
        # <15>\r\n
        # <16>\r\n
        # <17>\r\n
        # <18>\r\n
        # <19>\r\n
        # <20>\r\n
        # <21>\r\n
        # <22>\r\n
        #
        # Where the above values are described as:
        # <1>: Month as an integer.
        # <2>: Day-of-month as an integer.
        # <3>: Year as an integer.
        # <4>: Hour as an integer.
        # <5>: Minutes.  This includes the seconds as a float
        #      within it, but with no decimals.  This value is 15
        #      characters long.
        # 
        #      For example:
        #        - 35 minutes and 45 seconds would be: "357500000000000"
        #        -  5 minutes and 37 seconds would be: "056166666666666"
        # 
        # <6>: Hours of timezone offset in standard time, as an int.
        #      Negative values represent East of GMT, and
        #      positive values represent West of GMT.
        #
        #      Example:
        #        "-9" for 9 Hours East of GMT
        #        "9" for 9 Hours West of GMT
        #
        # <7>: Minutes of timezone offset in standard time, as an
        #      float multiplied by 10000, with no decimal.  Note
        #      when times are in LMT, digits past the first 2
        #      digits are used.
        #
        #      Example:
        #        "400000" for 40 minutes.
        # 
        # <8>: Longitude degrees as an int.
        #      Negative values represent degrees East.
        #
        #      Example:
        #        "-144"
        #        "144"
        #
        # <9>: Longitude minutes and seconds, displayed as an int
        #      but text is as a float multitplied to have 6 digits of
        #      precision total.
        #
        #      Example:
        #        "586833" for 58 minutes 41 seconds
        #
        # <10>: Latitude degrees as an int.
        #      Negative values represent degrees South.
        #
        #      Example:
        #        "-37" for 37 degrees South.
        #
        # <11>: Latitude minutes and seconds, displayed as an int
        #      but text is as a float multitplied to have 6 digits
        #      of precision total.
        #
        #      Example:
        #        "496500" for 49 minutes 39 seconds
        # 
        # <12>: Altitude in meters above sea level,
        #      as a float with 6 digits of precision.  
        #
        #      Example:
        #      "42.000000"
        #
        # <13>: Hours of timezone offset in standard time, as a
        #      float with 6 digits of precision.  Negative values
        #      represent East of GMT, and positive values
        #      represent West of GMT.
        #
        #      Example:
        #        "-9.833333" for 9 Hours 50 Minutes East of GMT
        #        "9.833333" for 9 Hours 50 Minutes West of GMT
        #
        # <14>: Hours of timezone offset if the timestamp is in
        #      daylight savings.  If the location is not in daylight
        #      savings, then this value will show up as the same as
        #      string <13>.
        #
        # <15>: "0" if the location is within the United States.
        #       "1" if the location is outside the United States.
        #
        # <16>: int value.  This is a zero-based index into either
        #      the list of US States or into the list of Countries.
        #
        #      Example:
        #        "11" for Australia
        #        "301" for Virginia, USA
        #
        # <17>: String value for the city name.
        #
        #      Example:
        #        "Arlington"
        #        "Melbourne"
        #
        # <18>: String value for the US State or the Country.
        #
        #      Example:
        #        "Virginia,^USA"
        #        "Australia"
        #
        # <19>: "0" if the timestamp is in the Julian calendar.
        #       "1" if the timestamp is in the Gregorian calendar.
        #
        # <20>: Atmospheric pressure in mbar (hPa).
        #      This is a float value with 6 digits of precision.
        #
        #      Example:
        #        "1013.250000" for 1013.25.
        #
        # <21>: Atmospheric temperature in degrees Celsius.
        #      This is a float value with 6 digits of precision.
        #
        #      Example:
        #        "20.000000" for 20 degrees celsius.
        # 
        # <22>: "0" for unknown gender
        #       "1" for male gender
        #       "2" for female gender
        #
        #################################################################
        """

        self.log.debug("Entered _generateJHoraFileText()")
        
        self.log.debug("dt at input is: " + Ephemeris.datetimeToStr(dt))

        # Flag that indicates that the given timestamp matches the
        # birth timestamp.
        dtEqualsBirthDt = self._datetimeEqualsAdjustedBirthDt(dt, birthInfo)
        
        # Datetime 'dt' needs to be localized to the timezone used in
        # birthInfo so that we may have it if we need it.  Assuming
        # 'dt' is already localized to UTC, GMT, or some other
        # timezone (it is not native and thus has a tzinfo set), then
        # in theory there should be no ambiguity when converting
        # between them.
        tzinfoObj = pytz.timezone(birthInfo.timezoneName)
        relocalizedDt = tzinfoObj.normalize(dt.astimezone(tzinfoObj))
        
        # <1>: Month as an integer.
        field1 = ""
        if dtEqualsBirthDt == True:
            field1 = "{}".format(birthInfo.month)
        else:
            field1 = "{}".format(dt.month)
        self.log.debug("field1 is: {}".format(field1))
        
        # <2>: Day-of-month as an integer.
        field2 = ""
        if dtEqualsBirthDt == True:
            field2 = "{}".format(birthInfo.day)
        else:
            field2 = "{}".format(dt.day)
        self.log.debug("field2 is: {}".format(field2))

        # <3>: Year as an integer.
        field3 = ""
        if dtEqualsBirthDt == True:
            field3 = "{}".format(birthInfo.year)
        else:
            field3 = "{}".format(dt.year)
        self.log.debug("field3 is: {}".format(field3))

        # <4>: Hour as an integer.
        field4 = ""
        if dtEqualsBirthDt == True:
            field4 = "{}".format(birthInfo.hour)
        else:
            field4 = "{}".format(dt.hour)
        self.log.debug("field4 is: {}".format(field4))
        
        # <5>: Minutes.  This includes the seconds as a float
        #      within it, but with no decimals.  This value is 15
        #      characters long.
        # 
        #      For example:
        #        - 35 minutes and 45 seconds would be: "357500000000000"
        #        -  5 minutes and 37 seconds would be: "056166666666666"
        # 
        field5 = ""
        if dtEqualsBirthDt == True:
            minutes = float(birthInfo.minute) + \
                      float(birthInfo.second / 60.0)
            minutes *= 10000000000000
            minutes = int(minutes)
            field5 = "{}".format(minutes)
        else:
            minutes = float(dt.minute) + \
                      float(dt.second / 60.0)
            minutes *= 10000000000000
            minutes = int(minutes)
            field5 = "{}".format(minutes)
        self.log.debug("field5 is: {}".format(field5))
        
        # <6>: Hours of timezone offset, as an int.
        #      Negative values represent East of GMT, and
        #      positive values represent West of GMT.
        #
        #      Example:
        #        "-9" for 9 Hours East of GMT
        #        "9" for 9 Hours West of GMT
        #
        field6 = ""
        totalMinutesOffset = 0

        if dtEqualsBirthDt == True:
            if birthInfo.timeOffsetAutodetectedRadioButtonState == True:
                hoursTimezoneOffset = 0
                minutesTimezoneOffset = 0
            
                offsetTimedelta = relocalizedDt.utcoffset()
                self.log.debug("offsetTimedelta == {}".format(offsetTimedelta))
            
                totalMinutesOffset = \
                    int(round((offsetTimedelta.days * 60 * 24) + \
                              (offsetTimedelta.seconds / 60)))
                hoursTimezoneOffset = abs(totalMinutesOffset) // 60
                
                if totalMinutesOffset > 0 and hoursTimezoneOffset != 0:
                    hoursTimezoneOffset *= -1
                
                field6 = "{}".format(hoursTimezoneOffset)
                
            elif birthInfo.timeOffsetManualEntryRadioButtonState == True:
                totalMinutesOffset = \
                    (birthInfo.timezoneManualEntryHours * 60) + \
                    (birthInfo.timezoneManualEntryMinutes)
                    
                if birthInfo.timezoneManualEntryEastWestComboBoxValue == "E":
                    totalMinutesOffset *= -1
                        
                hoursTimezoneOffset = abs(totalMinutesOffset) // 60
                if totalMinutesOffset < 0 and hoursTimezoneOffset != 0:
                    hoursTimezoneOffset *= -1
                field6 = "{}".format(hoursTimezoneOffset)
                
            elif birthInfo.timeOffsetLMTRadioButtonState == True:
                ratioOfDay = birthInfo.longitudeDegrees / 360.0
                minutesInDay = 60 * 24
                totalMinutesOffset = ratioOfDay * minutesInDay
                    
                hoursTimezoneOffset = abs(totalMinutesOffset) // 60
                if totalMinutesOffset < 0 and hoursTimezoneOffset != 0:
                    hoursTimezoneOffset *= -1
                field6 = "{}".format(hoursTimezoneOffset)
        else:
            offsetTimedelta = dt.utcoffset()            
            self.log.debug("offsetTimedelta == {}".format(offsetTimedelta))
            
            totalMinutesOffset = \
                int(round((offsetTimedelta.days * 60 * 24) + \
                          (offsetTimedelta.seconds / 60)))
            hoursTimezoneOffset = abs(totalMinutesOffset) // 60
            
            if totalMinutesOffset > 0 and hoursTimezoneOffset != 0:
                hoursTimezoneOffset *= -1
            
            field6 = "{}".format(hoursTimezoneOffset)
        self.log.debug("field6 is: {}".format(field6))
        
        # <7>: Minutes of timezone offset in standard time, as an
        #      float multiplied by 10000, with no decimal.  Note
        #      when times are in LMT, digits past the first 2
        #      digits are used.
        #
        #      Example:
        #        "400000" for 40 minutes.
        # 
        minutesTimezoneOffset = abs(totalMinutesOffset) % 60
        field7 = "{}".format(minutesTimezoneOffset * 10000)
        self.log.debug("field7 is: {}".format(field7))
        
        # <8>: Longitude degrees as an int.
        #      Negative values represent degrees East.
        #
        #      Example:
        #        "-144"
        #        "144"
        #
        value = None
        if birthInfo.longitudeDegrees > 0:
            value = -1 * math.floor(birthInfo.longitudeDegrees)
        else:
            value = math.floor(-1 * birthInfo.longitudeDegrees)
        field8 = "{}".format(value)
            
        # <9>: Longitude minutes and seconds, displayed as an int
        #      but text is as a float multitplied to have 6 digits of
        #      precision total.
        #
        #      Example:
        #        "586833" for 58 minutes 41 seconds
        #
        wholeDegs = math.floor(birthInfo.longitudeDegrees)
        fractionalDegs = birthInfo.longitudeDegrees - wholeDegs
        value = math.floor(fractionalDegs * 1000000)
        field9 = "{}".format(value)

        # <10>: Latitude degrees as an int.
        #      Negative values represent degrees South.
        #
        #      Example:
        #        "-37" for 37 degrees South.
        #
        field10 = "{}".format(math.floor(birthInfo.latitudeDegrees))

        # <11>: Latitude minutes and seconds, displayed as an int
        #      but text is as a float multitplied to have 6 digits
        #      of precision total.
        #
        #      Example:
        #        "496500" for 49 minutes 39 seconds
        # 
        wholeDegs = math.floor(birthInfo.latitudeDegrees)
        fractionalDegs = birthInfo.latitudeDegrees - wholeDegs
        value = math.floor(fractionalDegs * 1000000)
        field11 = "{}".format(value)
            
        # <12>: Altitude in meters above sea level,
        #      as a float with 6 digits of precision.  
        #
        #      Example:
        #      "42.000000"
        #
        field12 = "{:.6}".format(float(birthInfo.elevation))
        self.log.debug("field12 (altitude) is: " + field12)
            
        # <13>: Hours of timezone offset in standard time, as a
        #      float with 6 digits of precision.  Negative values
        #      represent East of GMT, and positive values
        #      represent West of GMT.
        #
        #      Example:
        #        "-9.833333" for 9 Hours 50 Minutes East of GMT
        #        "9.833333" for 9 Hours 50 Minutes West of GMT
        #

        offsetTimedelta = Ephemeris.getUtcOffsetForStandardTime(dt.tzinfo)
        totalMinutesOffset = \
            int(round((offsetTimedelta.days * 60 * 24) + \
                      (offsetTimedelta.seconds / 60)))
        hoursTimezoneOffsetFloat = -1 * totalMinutesOffset / 60.0
        field13 = "{:.6}".format(hoursTimezoneOffsetFloat)
        self.log.debug("field13 is: " + field13)

        # <14>: Hours of timezone offset if the timestamp is in
        #      daylight savings.  If the location is not in daylight
        #      savings, then this value will show up as the same as
        #      string <13>.
        #
        field14 = ""
        if dtEqualsBirthDt == True:
            if birthInfo.timeOffsetAutodetectedRadioButtonState == True:
                # This value is calculated for relocalizedDt, as opposed
                # to previous calculations where done on the birthInfo
                # timezone information.
    
                offsetTimedelta = relocalizedDt.utcoffset()
                self.log.debug("offsetTimedelta == {}".format(offsetTimedelta))
                
                totalMinutesOffset = \
                    int(round((offsetTimedelta.days * 60 * 24) + \
                              (offsetTimedelta.seconds / 60)))
                hoursTimezoneOffsetFloat = -1 * totalMinutesOffset / 60.0
                field14 = "{:.6}".format(hoursTimezoneOffsetFloat)
            else:
                # User-specified timezone offset or LMT, so use the
                # value in field13.
                field14 = field13
        else:
            offsetTimedelta = dt.utcoffset()
            self.log.debug("offsetTimedelta == {}".format(offsetTimedelta))
            
            totalMinutesOffset = \
                int(round((offsetTimedelta.days * 60 * 24) + \
                          (offsetTimedelta.seconds / 60)))
            hoursTimezoneOffsetFloat = -1 * totalMinutesOffset / 60.0
            field14 = "{:.6}".format(hoursTimezoneOffsetFloat)
            
        self.log.debug("field14 is: " + field14)

        # <15>: "0" if the location is within the United States.
        #       "1" if the location is outside the United States.
        field15 = ""
        if birthInfo.countryName == "United States":
            self.log.debug("field15 indicates wtihin United States.")
            field15 = "0"
        else:
            self.log.debug("field15 indicates outside United States.")
            field15 = "1"
            
        # <16>: int value.  This is a zero-based index into either
        #      the list of US States or into the list of Countries.
        #
        #      Example:
        #        "11" for Australia
        #        "301" for Virginia, USA
        #
        
        # We don't have the actual full list, so just set it to index 0.
        field16 = "0"

        # <17>: String value for the city name.
        #
        #      Example:
        #        "Arlington"
        #        "Melbourne"
        #
        field17 = birthInfo.locationName

        # <18>: String value for the US State or the Country.
        #
        #      Example:
        #        "Virginia,^USA"
        #        "Australia"
        #
            
        field18 = ""
        if birthInfo.countryName == "United States":
            field18 = "USA"
        else:
            field18 = birthInfo.countryName
        
        # <19>: "0" if the timestamp is in the Julian calendar.
        #       "1" if the timestamp is in the Gregorian calendar.
        #
            
        field19 = ""
        if birthInfo.calendar == "Julian":
            field19 = "0"
        else:
            field19 = "1"
            
        # <20>: Atmospheric pressure in mbar (hPa).
        #      This is a float value with 6 digits of precision.
        #
        #      Example:
        #        "1013.250000" for 1013.25.
        #
            
        # We don't actually record gather this information, so
        # just use a value within the expected range.
        field20 = "{:.6}".format(1023.0)
            
        # <21>: Atmospheric temperature in degrees Celsius.
        #      This is a float value with 6 digits of precision.
        #
        #      Example:
        #        "20.000000" for 20 degrees celsius.
        # 

        # We don't actually record gather this information, so
        # just use a value within the expected range.
        # 21 degrees Celsius is about 70 degrees Fahrenheit.
        field21 = "{:.6}".format(21.0)

        # <22>: "0" for unknown gender
        #       "1" for male gender
        #       "2" for female gender
        
        field22 = "0"

        # Below, {0} is a dummy value, just so the numbers line up
        # with the variable names.
        dummyStr = ""
        text = "{0}" + \
               "{1}\r\n" + \
               "{2}\r\n" + \
               "{3}\r\n" + \
               "{4}.{5}\r\n" + \
               "{6}.{7}\r\n" + \
               "{8}.{9}\r\n" + \
               "{10}.{11}\r\n" + \
               "{12}\r\n" + \
               "{13}\r\n" + \
               "{14}\r\n" + \
               "{15}\r\n" + \
               "{16}\r\n" + \
               "{17}\r\n" + \
               "{18}\r\n" + \
               "{19}\r\n" + \
               "{20}\r\n" + \
               "{21}\r\n" + \
               "{22}\r\n"
        text = text.format(dummyStr,
                           field1,
                           field2,
                           field3,
                           field4,
                           field5,
                           field6,
                           field7,
                           field8,
                           field9,
                           field10,
                           field11,
                           field12,
                           field13,
                           field14,
                           field15,
                           field16,
                           field17,
                           field18,
                           field19,
                           field20,
                           field21,
                           field22)

        self.log.debug("text is: ***" + text + "***")
        
        self.log.debug("Exiting _generateJHoraFileText()")
        
        return text
    
        
    def removeOldTemporaryJHoraFiles(self):
        """Removes any old JHora .jhd files that were previously created by this
        application.  By old, this means older than 180 days.
        """

        self.log.debug("Entered removeOldTemporaryJHoraFiles()")
        
        # This is chart destination directory path, in the filename format
        # readable on the current operating system.
        chartDestPath = ""

        # This is the chart destination directory path, in the filename format
        # readable on Posix systems (Unix, Linux, Mac OS X).
        chartDestPathPosix = ""
        
        # This is the chart destination directory path, in the filename format
        # readable on Microsoft Windows systems.
        chartDestPathWin = ""

        # Get the directory path.
        (chartDestPath, chartDestPathPosix, chartDestPathWin) = \
            self._getJHoraChartDestPath()

        # Current time in seconds since epoch.
        currTimeSecs = int(time.time())
        self.log.debug("Current time is: {}".format(currTimeSecs))

        # Time threshold to keep the JHora .jhd data files.
        secsInDay = 60 * 60 * 24
        timeThresholdSecs = currTimeSecs - (180 * secsInDay)
        
        self.log.info("Scanning for old JHora .jhd files to remove " +
                      "in directory: {}".format(chartDestPath))
        
        for f in os.listdir(chartDestPath):
            fullFilename = chartDestPath + os.sep + f
            self.log.debug("Looking at file: {}".format(fullFilename))
            statinfo = os.lstat(fullFilename)
            
            self.log.debug("Most recent access time is: {}".\
                           format(statinfo.st_atime))
            self.log.debug("Most recent mod time is:    {}".\
                           format(statinfo.st_atime))
            
            if statinfo.st_atime < timeThresholdSecs:
                # Older than our threshold, so try to remove the file.
                try:
                    self.log.info("Removing file: {}".\
                                  format(fullFilename))
                    os.remove(fullFilename)
                except OSError as e:
                    # This can happen on Windows if the file is
                    # currently in use.
                    self.log.warn("Failed to remove old temporary " +
                                  "JHora .jhd file {} because: {}".\
                                  format(f, e))
            
        self.log.debug("Exiting removeOldTemporaryJHoraFiles()")
        
    def handleAstrologLaunch(self, dt=None, birthInfo=None):
        """Opens Astrolog with the given datetime.datetime timestamp.
        Uses the currently set self.birthInfo object for timezone
        information.

        If 'dt' is None, then Astrolog is opened without any arguments given.
        Otherwise, both 'dt' and 'birthInfo' need to be set.
        
        Arguments:
        
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in Astrolog.  If dt is None, then
             Astrolog is opened without any arguments.

        birthInfo - BirthInfo object holding information about the
                    location/altitude and timezone.  This must be set
                    if 'dt' is not None.
        """

        self.log.debug("Entered handleAstrologLaunch()")

        # Check to make sure inputs are provided as expected.
        if dt == None:
            # Just open Astrolog without any file specified.
            self.log.debug("dt == None and birthInfo == None.")
            
            # Launch Astrolog.
            self._execAstrolog()
            
        elif dt != None and birthInfo != None:
            # Normal case for specifying a timestamp with birthInfo.
            self.log.debug("dt != None and birthInfo != None.")
            
        else:
            self.log.error("If 'dt' argument is provided, " +
                           "then birthInfo cannot be None.") 
            return
        
        self.log.debug("Values being used: " +
                       "dt='{}', birthInfo='{}'".\
                       format(Ephemeris.datetimeToStr(dt),
                              birthInfo.toString()))

        
        # This is chart destination directory path, in the filename format
        # readable on the current operating system.
        chartDestPath = ""

        # This is the chart destination directory path, in the filename format
        # readable on Posix systems (Unix, Linux, Mac OS X).
        chartDestPathPosix = ""
        
        # This is the chart destination directory path, in the filename format
        # readable on Microsoft Windows systems.
        chartDestPathWin = ""

        # Create the appropriate directory and return the paths.
        (chartDestPath, chartDestPathPosix, chartDestPathWin) = \
            self._getAstrologChartDestPath()

        self.log.debug("chartDestPath == " + chartDestPath)
        self.log.debug("chartDestPathPosix == " + chartDestPathPosix)
        self.log.debug("chartDestPathWin == " + chartDestPathWin)
        
        # Create the file to open Astrolog with.
        filenameTemplate = chartDestPath + os.sep + \
                           "tmp_" + self.appName + "_Astrolog_XXXXXX.txt"
        self.log.debug("filenameTemplate == " + filenameTemplate)
        
        f = QTemporaryFile(filenameTemplate)

        # Need to disable auto-remove because the QTemporaryFile gets
        # destroyed (garbage collected) before Astrolog is launched and
        # can read the file.
        f.setAutoRemove(False)

        if f.open(QIODevice.ReadWrite):
            
            # Get the text to go into the file from the input parameters.
            text = self._generateAstrologFileText(dt, birthInfo)

            # Write to the file.
            utf8EncodedText = text.encode('utf-8')
            f.writeData(utf8EncodedText)
            f.close()

            # Launch Astrolog with the file just created.

            # Get the filename in the Windows path format since that's
            # all wine or Windows knows how to see.
            filename = chartDestPathWin + "\\" + \
                       os.path.basename(f.fileName())
            
            self.log.debug("f.fileName() == " + f.fileName())
            self.log.debug("filename == " + filename)

            self._execAstrolog(filename)
            
        else:
            errMsg = "Astrolog launch failed because: " + os.linesep + \
                     "Could not open a temporary file for Astrolog."
            self.log.error(errMsg)
            
            title = "Error"
            text = errMsg
            buttons = QMessageBox.Ok
            defaultButton = QMessageBox.NoButton
            
            QMessageBox.warning(self, title, text, buttons, defaultButton)
            
        
        self.log.debug("Exiting handleAstrologLaunch()")

    def _getAstrologChartDestPath(self):
        """Returns a tuple of 3 paths (based on operating system) for
        where the Astrolog .txt files will be saved to.  The formula for
        this path is based on operating system and application name.
        See code below for details.  This function also creates the
        directory if it doesn't exist already.

        Returns:
        tuple of three items:
           - chartDestPath (str)
               This is chart destination directory path, in the
               filename format readable on the current operating system.
           - chartDestPathPosix (str)
               This is the chart destination directory path, in the
               filename format readable on Posix systems (Unix, Linux,
               Mac OS X).
           - chartDestPathWin (str)
               This is the chart destination directory path, in the
               filename format readable on Microsoft Windows systems.
        """

        self.log.debug("Entered _getAstrologChartDestPath()")
        
        # Make a directory to store our temporary .txt files.
        # Optimally, we would like to place it within Astrolog's 'data'
        # directory, but that doesn't work because that directory path
        # has spaces and os.makedirs() will choke on that.

        # This is chart destination directory path, in the filename format
        # readable on the current operating system.
        chartDestPath = ""

        # This is the chart destination directory path, in the filename format
        # readable on Posix systems (Unix, Linux, Mac OS X).
        chartDestPathPosix = ""
        
        # This is the chart destination directory path, in the filename format
        # readable on Microsoft Windows systems.
        chartDestPathWin = ""
        
        try:
            if os.name == "posix":
                self.log.debug("posix")

                chartDestPathPosix = \
                    os.path.expanduser('~') + os.sep + \
                    ".wine/drive_c/" + self.appName + "/data"
                chartDestPathWin = \
                    "C:\\" + self.appName + "\\data"
                
                self.log.debug("chartDestPathPosix == " + chartDestPathPosix)
                self.log.debug("chartDestPathWin == " + chartDestPathWin)
                self.log.debug("os.path.exists(chartDestPathPosix) == {}".\
                               format(os.path.exists(chartDestPathPosix)))
                self.log.debug("os.path.isdir(chartDestPathPosix) == {}".\
                               format(os.path.isdir(chartDestPathPosix)))
                
                if os.path.exists(chartDestPathPosix) and \
                       os.path.isdir(chartDestPathPosix):
                    
                    self.log.debug("Good, directory exists: " +
                                   chartDestPathPosix)
                    
                else:
                    self.log.debug("making dirs: " + chartDestPathPosix)
                    os.makedirs(chartDestPathPosix)

                    
                chartDestPath = chartDestPathPosix
                
            elif os.name == "nt":
                self.log.debug("nt")
            
                chartDestPathWin = \
                    "C:\\" + self.appName + "\\data"

                self.log.debug("chartDestPathWin == " + chartDestPathWin)
                self.log.debug("os.path.exists(chartDestPathWin) == {}".\
                               format(os.path.exists(chartDestPathWin)))
                self.log.debug("os.path.isdir(chartDestPathWin) == {}".\
                               format(os.path.isdir(chartDestPathWin)))
                
                if os.path.exists(chartDestPathWin) and \
                       os.path.isdir(chartDestPathWin):
                    
                    self.log.debug("Good, directory exists: " + \
                                   chartDestPathWin)
                else:
                    self.log.debug("making dirs: " + chartDestPathWin)
                    os.makedirs(chartDestPathWin)

                chartDestPath = chartDestPathWin
                
            else:
                self.log.warn("Operating system unsupported: " + os.name)
                return
            
        except os.error as e:
            
            self.log.error("Error while trying to ensure the " +
                           "Astrolog chart destination directory exists.  " +
                           "{}".format(e))
            
        self.log.debug("chartDestPath == " + chartDestPath)
        self.log.debug("chartDestPathPosix == " + chartDestPathPosix)
        self.log.debug("chartDestPathWin == " + chartDestPathWin)
        
        self.log.debug("Exiting _getAstrologChartDestPath()")
        
        return (chartDestPath, chartDestPathPosix, chartDestPathWin)
    
    def _execAstrolog(self, filename=None):
        """Runs the executable Astrolog.

        Arguments:
        
        filename - str containing the full path of the Astrolog .txt to open.
                   This argument can be None if opening Astrolog without
                   any arguments is desired.
        """

        toExec = ""
        
        if os.name == "posix":
            
            toExec = \
                "wine " + \
                os.path.expanduser('~') + os.sep + \
                ".wine/drive_c/ASTROLOG/ASTROLOG.EXE"
            
            if filename != None:
                toExec += " -i \"" + filename + "\""
            
            self.log.debug("Launching Astrolog.  toExec is: " + toExec)
            
            p = subprocess.Popen(toExec, shell=True)
            
            self.log.debug("Astrolog launched.")
            
        elif os.name == "nt":
            
            toExec = \
                "C:\\ASTROLOG\\ASTROLOG.EXE"
            
            if filename != None:
                toExec += " -i \"" + filename + "\""
            
            self.log.debug("Launching Astrolog.  toExec is: " + toExec)

            p = subprocess.Popen(toExec)
            
            self.log.debug("Astrolog launched.")
            
        else:
            self.log.warn("Operating system unsupported: " + os.name)

        
    def _generateAstrologFileText(self, dt, birthInfo):
        """Generates the text that would be in a Astrolog .txt file, for
        the information given in the specified datetime.datetime and
        BirthInfo.
        
        Arguments:
        
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in Astrolog.  

        birthInfo - BirthInfo object holding information about the
                    location/altitude and timezone.


        Notes on text format:

        # Format of the file is all text with Windows newlines:
        #
        # @0102  ; Astrolog chart info.\r\n
        # /qb <1> <2> <3> <4>:<5><6> <7> <8>  <9>:<10><11> <12>:<13><14>\r\n
        # /zi "" ""\r\n
        #
        #
        # Where the above values are described as:
        # <1>: Month as a 3-letter string with the first letter capitalized.
        # <2>: Day-of-month as an integer.
        # <3>: Year as an integer.
        # <4>: Hour, in 12-hour time, as an integer.  If the number for
        #      the hour is only 1 digit, then leave a space in the first
        #      place.
        # <5>: Minutes, as a two-digit number.
        # <6>: "am" if in the first half of the day,
        #      "pm" if in the second half of the day.
        # <7>: "ST" if in standard time (not daylight savings).
        #      "DT" if in daylight time.
        # <8>: Time offset from GMT when in standard time (i.e. when
        #      not in daylight savings time).  Format is:
        #
        #      1) First charcter is either '+' or '-'.  Time
        #         offsets that are West of GMT are represented by a
        #         '+', East of GMT is '-'.
        #      2) Next one or two characters is the hours offset,
        #         as a 1 or 2 digit int.
        #      3) Next character is a ':'.
        #      4) Next two characters are the minutes offset.
        #
        #      Example:
        #
        #      +5:00   for 5 hours west of GMT.
        # 
        # <9>: Longitude degrees (two characters), displayed as a
        #      positive int.  If the value is only 1 digit, then leave
        #      a space in the first character location.
        #
        # <10>: Longitude minutes (two characters), displayed as a
        #      positive int.  
        #
        # <11>: Longitude polarity.  "E" for East, and "W" for west.
        #
        # <12>: Latitude degrees (two characters), displayed as a
        #      positive int.  If the value is only 1 digit, then leave
        #      a space in the first character location.
        #
        # <13>: Latitude minutes (two characters), displayed as an
        #       positive int.
        #
        # <14>: Latitude polarity.  "N" for North, and "S" for South.
        #
        #        
        # Examples:
        #
        # @0102  ; Astrolog chart info.\r\n
        # /qb Oct 25 1983  2:34pm ST +5:00  77:08W 38:53N\r\n
        # /zi "" ""\r\n
        #
        # @0102  ; Astrolog chart info.\r\n
        # /qb Jul 21 2011  2:52pm DT +5:00  77:24W 38:53N\r\n
        # /zi "" ""\r\n
        #
        # @0102  ; Astrolog chart info.\r\n
        # /qb Jul 1 2011  2:52pm DT -5:00   6:00E  8:53N\r\n
        # /zi "" ""\r\n
        #
        # @0102  ; Astrolog chart info.\r\n
        # /qb Jul 21 2011 12:52pm DT -5:00  20:00E 38:53N\r\n
        # /zi "" ""\r\n
        #
        #################################################################
        """

        self.log.debug("Entered _generateAstrologFileText()")
        
        self.log.debug("dt at input is: " + Ephemeris.datetimeToStr(dt))

        # Flag that indicates that the given timestamp matches the
        # birth timestamp.
        dtEqualsBirthDt = self._datetimeEqualsAdjustedBirthDt(dt, birthInfo)
        
        # Datetime 'dt' needs to be localized to the timezone used in
        # birthInfo so that we may have it if we need it.  Assuming
        # 'dt' is already localized to UTC, GMT, or some other
        # timezone (it is not native and thus has a tzinfo set), then
        # in theory there should be no ambiguity when converting
        # between them.
        tzinfoObj = pytz.timezone(birthInfo.timezoneName)
        relocalizedDt = tzinfoObj.normalize(dt.astimezone(tzinfoObj))
            
        # <1>: Month as a 3-letter string with the first letter capitalized.
        field1 = ""
        if dtEqualsBirthDt == True:
            field1 = Util.monthNumberToAbbrev(birthInfo.month)
        else:
            field1 = Util.monthNumberToAbbrev(dt.month)
        
        # <2>: Day-of-month as an integer.
        field2 = ""
        if dtEqualsBirthDt == True:
            field2 = "{}".format(birthInfo.day)
        else:
            field2 = "{}".format(dt.day)

        # <3>: Year as an integer.
        field3 = ""
        if dtEqualsBirthDt == True:
            field3 = "{}".format(birthInfo.year)
        else:
            field3 = "{}".format(dt.year)

        # <4>: Hour, in 12-hour time, as an integer.  If the number for
        #      the hour is only 1 digit, then leave a space in the first
        #      place.
        field4 = ""
        # <6>: "am" if in the first half of the day,
        #      "pm" if in the second half of the day.
        field6 = ""
        hourToUse = None
        if dtEqualsBirthDt == True:
            hourToUse = birthInfo.hour
        else:
            hourToUse = dt.hour
            
        if hourToUse == 0:
            field4 = "12"
        elif 0 < hourToUse < 13:
            field4 = "{}".format(hourToUse)
        elif 13 <= hourToUse < 24:
            field4 = "{}".format(hourToUse - 12)
            
        if hourToUse < 13:
            field6 = "am"
        else:
            field6 = "pm"

        # <5>: Minutes, as a two-digit number.
        field5 = ""
        if dtEqualsBirthDt == True:
            minutes = float(birthInfo.minute) + \
                      float(birthInfo.second / 60.0)
            minutes = round(minutes)
            field5 = "{}".format(minutes)
        else:
            minutes = float(dt.minute) + \
                      float(dt.second / 60.0)
            minutes = round(minutes)
            field5 = "{}".format(minutes)
        if len(field5) == 1:
            field5 = "0" + field5
            
        self.log.debug("field5 is: {}".format(field5))
        
        # <7>: "ST" if in standard time (not daylight savings).
        #      "DT" if in daylight time.
        field7 = ""
        if dtEqualsBirthDt == True:
            if birthInfo.timeOffsetAutodetectedRadioButtonState == True:
                if relocalizedDt.timetuple().tm_isdst == True:
                    field7 = "DT"
                else:
                    field7 = "ST"
            else:
                field7 = "ST"
        else:
            if dt.timetuple().tm_isdst == True:
                field7 = "DT"
            else:
                field7 = "ST"
        #if relocalizedDt.timetuple().tm_isdst == True:
        #    field7 = "DT"
        #else:
        #    field7 = "ST"

        self.log.debug("field 7 is: {}".format(field7))
            
        # <8>: Time offset from GMT when in standard time (i.e. when
        #      not in daylight savings time).  Format is:
        #
        #      1) First charcter is either '+' or '-'.  Time
        #         offsets that are West of GMT are represented by a
        #         '+', East of GMT is '-'.
        #      2) Next one or two characters is the hours offset,
        #         as a 1 or 2 digit int.
        #      3) Next character is a ':'.
        #      4) Next two characters are the minutes offset.
        #
        #      Example:
        #
        #      +5:00   for 5 hours west of GMT.
        # 
        field8 = ""
        totalMinutesOffset = 0

        if dtEqualsBirthDt == True:
            if birthInfo.timeOffsetAutodetectedRadioButtonState == True:
                hoursTimezoneOffset = 0
                minutesTimezoneOffset = 0
                
                tzinfoObj = pytz.timezone(birthInfo.timezoneName)
                self.log.debug("birthInfo.timezoneName is: " + \
                               birthInfo.timezoneName)
    
                offsetTimedelta = tzinfoObj._utcoffset
                self.log.debug("During standard time, offsetTimedelta == {}".\
                               format(offsetTimedelta))
                
                totalMinutesOffset = \
                    int(round((offsetTimedelta.days * 60 * 24) + \
                              (offsetTimedelta.seconds / 60)))
                
            elif birthInfo.timeOffsetManualEntryRadioButtonState == True:
                totalMinutesOffset = \
                    (birthInfo.timezoneManualEntryHours * 60) + \
                    (birthInfo.timezoneManualEntryMinutes)
                    
                if birthInfo.timezoneManualEntryEastWestComboBoxValue == "W":
                    totalMinutesOffset *= -1
                
            elif birthInfo.timeOffsetLMTRadioButtonState == True:
                ratioOfDay = birthInfo.longitudeDegrees / 360.0
                minutesInDay = 60 * 24
                totalMinutesOffset = ratioOfDay * minutesInDay
        else:
            offsetTimedelta = Ephemeris.getUtcOffsetForStandardTime(dt.tzinfo)
            self.log.debug("offsetTimedelta == {}".format(offsetTimedelta))
            
            totalMinutesOffset = \
                int(round((offsetTimedelta.days * 60 * 24) + \
                          (offsetTimedelta.seconds / 60)))
            
        hoursTimezoneOffset = abs(totalMinutesOffset) // 60
            
        if totalMinutesOffset <= 0:
            field8 += "+"
        else:
            field8 += "-"
        field8 += "{}".format(hoursTimezoneOffset) + ":"
        minutesPart = "{}".format(int(abs(totalMinutesOffset) % 60))
        if len(minutesPart) == 1:
            field8 += "0" + minutesPart
        else:
            field8 += minutesPart
            
        self.log.debug("field8 is: {}".format(field6))

                
        # <9>: Longitude degrees (two characters), displayed as a
        #      positive int.  If the value is only 1 digit, then leave
        #      a space in the first character location.
        #
        field9 = "{}".format(math.floor(abs(birthInfo.longitudeDegrees)))
        if len(field9) == 1:
            field9 = " " + field9
        
        # <10>: Longitude minutes (two characters), displayed as a
        #      positive int.  
        wholeDegs = math.floor(abs(birthInfo.longitudeDegrees))
        fractionalDegs = abs(birthInfo.longitudeDegrees) - wholeDegs
        value = math.floor(fractionalDegs * 60.0)
        field10 = "{}".format(value)
        if len(field10) == 1:
            field10 = "0" + field10

        # <11>: Longitude polarity.  "E" for East, and "W" for west.
        field11 = ""
        if birthInfo.longitudeDegrees >= 0:
            field11 = "E"
        else:
            field11 = "W"
        
        # <12>: Latitude degrees (two characters), displayed as a
        #      positive int.  If the value is only 1 digit, then leave
        #      a space in the first character location.
        #
        field12 = "{}".format(math.floor(abs(birthInfo.latitudeDegrees)))
        if len(field12) == 1:
            field12 = " " + field12
        
        # <13>: Latitude minutes (two characters), displayed as an
        #       positive int.
        #
        wholeDegs = math.floor(abs(birthInfo.latitudeDegrees))
        fractionalDegs = abs(birthInfo.latitudeDegrees) - wholeDegs
        value = math.floor(fractionalDegs * 60)
        field13 = "{}".format(value)
        if len(field13) == 1:
            field13 = "0" + field13
        
        # <14>: Latitude polarity.  "N" for North, and "S" for South.
        #
        field14 = ""
        if birthInfo.latitudeDegrees >= 0:
            field14 = "N"
        else:
            field14 = "S"

        # Below, {0} is a dummy value, just so the numbers line up
        # with the variable names.
        dummyStr = ""
        text = "{0}" + \
               "@0102  ; Astrolog chart info.\r\n" + \
               "/qb {1} {2} {3} {4}:{5}{6} {7} {8}  " + \
               "{9}:{10}{11} {12}:{13}{14}\r\n" + \
               "zi \"\" \"\"\r\n"
        text = text.format(dummyStr,
                           field1,
                           field2,
                           field3,
                           field4,
                           field5,
                           field6,
                           field7,
                           field8,
                           field9,
                           field10,
                           field11,
                           field12,
                           field13,
                           field14)

        self.log.debug("text is: ***" + text + "***")
        
        self.log.debug("Exiting _generateAstrologFileText()")
        
        return text
    
        
    def removeOldTemporaryAstrologFiles(self):
        """Removes any old Astrolog .txt files that were previously
        created by this application.  By old, this means older than
        180 days.
        """
        
        self.log.debug("Entered removeOldTemporaryAstrologFiles()")
        
        # This is chart destination directory path, in the filename format
        # readable on the current operating system.
        chartDestPath = ""

        # This is the chart destination directory path, in the filename format
        # readable on Posix systems (Unix, Linux, Mac OS X).
        chartDestPathPosix = ""
        
        # This is the chart destination directory path, in the filename format
        # readable on Microsoft Windows systems.
        chartDestPathWin = ""

        # Get the directory path.
        (chartDestPath, chartDestPathPosix, chartDestPathWin) = \
            self._getAstrologChartDestPath()

        # Current time in seconds since epoch.
        currTimeSecs = int(time.time())
        self.log.debug("Current time is: {}".format(currTimeSecs))

        # Time threshold to keep the Astrolog .txt data files.
        secsInDay = 60 * 60 * 24
        timeThresholdSecs = currTimeSecs - (180 * secsInDay)
        
        self.log.info("Scanning for old Astrolog .txt files to remove " +
                      "in directory: {}".format(chartDestPath))
        
        for f in os.listdir(chartDestPath):
            fullFilename = chartDestPath + os.sep + f
            self.log.debug("Looking at file: {}".format(fullFilename))
            statinfo = os.lstat(fullFilename)
            
            self.log.debug("Most recent access time is: {}".\
                           format(statinfo.st_atime))
            self.log.debug("Most recent mod time is:    {}".\
                           format(statinfo.st_atime))
            
            if statinfo.st_atime < timeThresholdSecs:
                # Older than our threshold, so try to remove the file.
                try:
                    self.log.info("Removing file: {}".\
                                  format(fullFilename))
                    os.remove(fullFilename)
                except OSError as e:
                    # This can happen on Windows if the file is
                    # currently in use.
                    self.log.warn("Failed to remove old temporary " +
                                  "Astrolog .txt file {} because: {}".\
                                  format(f, e))
        
        self.log.debug("Exiting removeOldTemporaryAstrologFiles()")
        

    def _datetimeEqualsAdjustedBirthDt(self, dt, birthInfo):
        """Returns True if the datetime is given is equal to the
        adjusted birth datetime.
        """

        self.log.debug("Entered _datetimeEqualsAdjustedBirthDt()")
        self.log.debug("dt == {}".format(Ephemeris.datetimeToStr(dt)))
        self.log.debug("birthInfo == {}".format(birthInfo.toString()))
        
        # Return value.
        rv = False
        
        # Get the localized datetime of birth.
        localizedDt = birthInfo.getBirthLocalizedDatetime()

        # Adjust datetime 'dt' back to an unadjusted UTC datetime if
        # the birthInfo is not set to be autodetected.
        if birthInfo.timeOffsetAutodetectedRadioButtonState == True:
            # Nothing extra needs to be done.
            pass
        
        elif birthInfo.timeOffsetManualEntryRadioButtonState == True:
            totalMinutesOffset = \
                (birthInfo.timezoneManualEntryHours * 60) + \
                (birthInfo.timezoneManualEntryMinutes)
                
            if birthInfo.timezoneManualEntryEastWestComboBoxValue == "E":
                totalMinutesOffset *= -1

            localizedDt = \
                localizedDt - datetime.timedelta(minutes=totalMinutesOffset)
            
        elif birthInfo.timeOffsetLMTRadioButtonState == True:
            # Use 4 minutes of time offset for each longitude degree away
            # from 0.
            timeShiftMinutes = self.longitudeDegrees * -4.0
        
            localizedDt = \
                localizedDt - datetime.timedelta(minutes=totalMinutesOffset)

        self.log.debug("localizedDt == {}".format(Ephemeris.datetimeToStr(dt)))
        if localizedDt == dt:
            rv = True
        else:
            rv = False

        self.log.debug("Exiting _datetimeEqualsAdjustedBirthDt(), " + \
                       "rv == {}".format(rv))
        return rv

    def _print(self):
        """Opens up a dialog for printing the current selected document."""

        self.log.debug("Entered _print()")
        
        # TODO: implement this _print() function.
        QMessageBox.information(self, 
                                "Not yet implemented", 
                                "This feature has not yet been implemented.")
        
        self.log.debug("Exiting _print()")


    def _printPreview(self):
        """Opens up a dialog for previewing the current selected document
        for printing.
        """

        self.log.debug("Entered _printPreview()")
        # TODO: implement this _printPreview() function.
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

            self.log.info("Exiting.")
            closeEvent.accept()
        else:
            self.log.debug("Ignoring close event.")

            closeEvent.ignore()

        self.log.debug("Exiting closeEvent()")

    def _exitApp(self):
        """Exits the app by trying to close all windows."""

        self.log.debug("Entered _exitApp()")

        self.log.info("Exiting.")
        qApp.closeAllWindows()

        self.log.debug("Exiting _exitApp()")

    def _editAppPreferences(self):
        """Opens up a dialog for editing the application-wide preferences.
        These values are saved via QSettings."""

        self.log.debug("Entered _editAppPreferences()")

        dialog = AppPreferencesEditDialog()

        retVal = dialog.exec_()

        if retVal == QDialog.Accepted:
            self.log.debug("AppPreferencesDialog accepted")
        else:
            self.log.debug("AppPreferencesDialog rejected")

        self.log.debug("Exiting _editAppPreferences()")

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
                birthInfo = dialog.getBirthInfo()
                priceChartDocument.setBirthInfo(birthInfo)
            else:
                self.log.debug("BirthInfoEditDialog rejected.  " + \
                               "Doing nothing more.")
        else:
            self.log.error("Tried to edit the birth info when either no " +
                           "PriceChartDocument is selected, or some " +
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editBirthInfo()")

    def _editPriceChartDocumentData(self):
        """Opens up a PriceChartDocumentDataEditDialog to edit the
        currently open PriceChartDocument's backing data object.

        If the dialog is accepted, the changes are applied and the dirty
        flag is set.  If the dialog is rejected, then no changes will
        happen.
        """

        self.log.debug("Entered _editPriceChartDocumentData()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the PriceChartDocumentData object.
            priceChartDocumentData = \
                priceChartDocument.getPriceChartDocumentData()

            # Create a dialog to edit the PriceBarChartSettings.
            dialog = PriceChartDocumentDataEditDialog(priceChartDocumentData)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("PriceChartDocumentDataEditDialog accepted.")

                # Reload the entire PriceChartDocument.
                priceChartDocument.\
                    setPriceChartDocumentData(priceChartDocumentData)

                # Set the dirty flag because the settings object has now
                # changed.
                priceChartDocument.setDirtyFlag(True)
            else:
                self.log.debug("PriceChartDocumentDataEditDialog rejected.")
        else:
            self.log.error("Tried to edit the PriceChartDocumentData " + \
                           "when either no " + \
                           "PriceChartDocument is selected, or some " + \
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editPriceChartDocumentData()")

    def _editPriceBarChartSettings(self):
        """Opens up a PriceBarChartSettingsEditDialog to edit
        the PriceBarChartSettings associated with the current active
        PriceChartDocument in the in the UI.  
        
        If the dialog is accepted, the changes are applied and the dirty
        flag is set.  If the dialog is rejected, then no changes will
        happen.
        """

        self.log.debug("Entered _editPriceBarChartSettings()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the PriceBarChartSettings object.
            priceBarChartSettings = \
                priceChartDocument.getPriceChartDocumentData().\
                    priceBarChartSettings

            # Create a dialog to edit the PriceBarChartSettings.
            dialog = PriceBarChartSettingsEditDialog(priceBarChartSettings)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("PriceBarChartSettingsEditDialog accepted.")

                # Apply the settings changes to the PriceChartDocument.
                # This should trigger a redraw of everything in the chart.
                priceChartDocument.\
                    applyPriceBarChartSettings(priceBarChartSettings)

                # Set the dirty flag because the settings object has now
                # changed.
                priceChartDocument.setDirtyFlag(True)
            else:
                self.log.debug("PriceBarChartSettingsEditDialog rejected." + \
                               "  Doing nothing more.")
        else:
            self.log.error("Tried to edit the PriceBarChartSettings " + \
                           "when either no " + \
                           "PriceChartDocument is selected, or some " + \
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editPriceBarChartSettings()")


    def _editPriceBarChartScaling(self):
        """Opens up a PriceBarChartScalingsListEditDialog to edit
        the PriceBarChartScaling associated with the current active
        PriceChartDocument in the in the UI.  
        
        If the dialog is accepted, the changes are applied and the dirty
        flag is set.  If the dialog is rejected, then no changes will
        happen.
        """

        self.log.debug("Entered _editPriceBarChartScaling()")

        # Get current active PriceChartDocument.
        priceChartDocument = self.getActivePriceChartDocument()

        if priceChartDocument != None:
            # Get the PriceBarChartSettings object.
            priceBarChartSettings = \
                priceChartDocument.getPriceChartDocumentData().\
                    priceBarChartSettings

            # Get the list of scalings and the index of the one that is
            # currently applied.
            scalings = \
                priceBarChartSettings.priceBarChartGraphicsViewScalings
            index = \
                priceBarChartSettings.priceBarChartGraphicsViewScalingsIndex

            # Create a dialog to edit the PriceBarChart's list of scalings
            # and which one is currently applied.
            dialog = PriceBarChartScalingsListEditDialog(scalings, index)

            if dialog.exec_() == QDialog.Accepted:
                self.log.debug("PriceBarChartScalingsListEditDialog " + \
                               "accepted.")

                # Get the new values from the dialog.
                scalings = dialog.getPriceBarChartScalings()
                index = dialog.getPriceBarChartScalingsIndex()

                # Set the scaling and index into the PriceBarChartSettings.
                priceBarChartSettings.\
                    priceBarChartGraphicsViewScalings = scalings
                priceBarChartSettings.\
                    priceBarChartGraphicsViewScalingsIndex = index

                # Apply the settings changes to the PriceChartDocument.
                # This should trigger a redraw of everything in the chart.
                priceChartDocument.\
                    applyPriceBarChartSettings(priceBarChartSettings)

                # Set the dirty flag because the settings object has now
                # changed.
                priceChartDocument.setDirtyFlag(True)
            else:
                self.log.debug("PriceBarChartScalingsListEditDialog " + \
                               "rejected.  Doing nothing more.")
        else:
            self.log.error("Tried to edit the PriceBarChart scaling " + \
                           "when either no " + \
                           "PriceChartDocument is selected, or some " + \
                           "other unsupported subwindow was selected.")

        self.log.debug("Exiting _editPriceBarChartScaling()")

    def _handleEnableAndShowAstrologyChartAction(self):
        """Slot function that is called when the user triggers the
        QAction 'self.enableAndShowAstrologyChartAction'.
        """
        
        # This Astro action only makes sense to be triggered if there
        # is a PriceChartDocument open and active.  Check to make sure
        # that is true.
        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        flag = self.enableAndShowAstrologyChartAction.isChecked()
        
        pcd.setEnableAndShowAstrologyChart(flag)

    def _handleEnableAndShowPlanetaryInfoTableAction(self):
        """Slot function that is called when the user triggers the
        QAction 'self.enableAndShowPlanetaryInfoTableAction'.
        """
        
        # This Astro action only makes sense to be triggered if there
        # is a PriceChartDocument open and active.  Check to make sure
        # that is true.
        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        flag = self.enableAndShowPlanetaryInfoTableAction.isChecked()
        
        pcd.setEnableAndShowPlanetaryInfoTable(flag)

    def _handleTrackMouseToAstroChartAction(self):
        """Slot function that is called when the user triggers the QActions:
        self.trackMouseToAstroChart1Action,
        self.trackMouseToAstroChart2Action,
        self.trackMouseToAstroChart3Action.
        """
        
        # These Astro actions only make sense to be triggered if
        # there is a PriceChartDocument open and active.  Check to
        # make sure that is true.
        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        flag1 = self.trackMouseToAstroChart1Action.isChecked()
        flag2 = self.trackMouseToAstroChart2Action.isChecked()
        flag3 = self.trackMouseToAstroChart3Action.isChecked()
        
        pcd.setTrackMouseToAstroChart1(flag1)
        pcd.setTrackMouseToAstroChart2(flag2)
        pcd.setTrackMouseToAstroChart3(flag3)


    def _handleOpenJHoraWithNoArgsAction(self):
        """Slot function that is called when the
        self.openJHoraWithNoArgsAction QAction is triggered.
        """
        
        self._execJHora()

    def _handleOpenJHoraWithLocalizedNowAction(self):
        """Slot function that is called when the
        self.openJHoraWithLocalizedNowAction QAction is triggered.
        """
        
        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        # Get the BirthInfo (location, timezone, etc.) for the current
        # active chart.
        birthInfo = pcd.getBirthInfo()
        tzinfoObj = pytz.timezone(birthInfo.timezoneName)

        # Localize the 'now' timestamp.
        localizedDt = datetime.datetime.now(tzinfoObj)

        self.log.debug("localized now dt is: {}".\
                       format(Ephemeris.datetimeToStr(localizedDt)))
                       
        # Open JHora with these values.
        self.handleJhoraLaunch(localizedDt, birthInfo)

    def _handleOpenJHoraWithBirthInfoAction(self):
        """Slot function that is called when the
        self.openJHoraWithBirthInfoAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        # Get the BirthInfo (location, timezone, etc.) for the current
        # active chart.
        birthInfo = pcd.getBirthInfo()

        # Datetime to send to JHora.
        dt = None
        
        # Get the localized datetime of birth.
        localizedDt = birthInfo.getBirthLocalizedDatetime()

        # Adjust datetime 'dt' back to an unadjusted UTC datetime if
        # the birthInfo is not set to be autodetected.
        if birthInfo.timeOffsetAutodetectedRadioButtonState == True:
            # Nothing extra needs to be done.
            pass
        
        elif birthInfo.timeOffsetManualEntryRadioButtonState == True:
            totalMinutesOffset = \
                (birthInfo.timezoneManualEntryHours * 60) + \
                (birthInfo.timezoneManualEntryMinutes)
                
            if birthInfo.timezoneManualEntryEastWestComboBoxValue == "E":
                totalMinutesOffset *= -1

            localizedDt = \
                localizedDt - datetime.timedelta(minutes=totalMinutesOffset)
            
        elif birthInfo.timeOffsetLMTRadioButtonState == True:
            # Use 4 minutes of time offset for each longitude degree away
            # from 0.
            timeShiftMinutes = self.longitudeDegrees * -4.0
        
            localizedDt = \
                localizedDt - datetime.timedelta(minutes=totalMinutesOffset)
        
        # Open JHora with these values.
        self.handleJhoraLaunch(localizedDt, birthInfo)

    def _handleOpenAstrologWithNoArgsAction(self):
        """Slot function that is called when the
        self.openAstrologWithNoArgsAction QAction is triggered.
        """
        
        self._execAstrolog()

    def _handleOpenAstrologWithLocalizedNowAction(self):
        """Slot function that is called when the
        self.openAstrologWithLocalizedNowAction QAction is triggered.
        """
        
        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        # Get the BirthInfo (location, timezone, etc.) for the current
        # active chart.
        birthInfo = pcd.getBirthInfo()
        tzinfoObj = pytz.timezone(birthInfo.timezoneName)

        # Localize the 'now' timestamp.
        localizedDt = datetime.datetime.now(tzinfoObj)

        # Open Astrolog with these values.
        self.handleAstrologLaunch(localizedDt, birthInfo)

    def _handleOpenAstrologWithBirthInfoAction(self):
        """Slot function that is called when the
        self.openAstrologWithBirthInfoAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        # Get the BirthInfo (location, timezone, etc.) for the current
        # active chart.
        birthInfo = pcd.getBirthInfo()

        # Get the localized datetime of birth.
        localizedDt = birthInfo.getBirthLocalizedDatetime()

        # Adjust datetime 'dt' back to an unadjusted UTC datetime if
        # the birthInfo is not set to be autodetected.
        if birthInfo.timeOffsetAutodetectedRadioButtonState == True:
            # Nothing extra needs to be done.
            pass
        elif birthInfo.timeOffsetManualEntryRadioButtonState == True:
            totalMinutesOffset = \
                (birthInfo.timezoneManualEntryHours * 60) + \
                (birthInfo.timezoneManualEntryMinutes)
                
            if birthInfo.timezoneManualEntryEastWestComboBoxValue == "E":
                totalMinutesOffset *= -1

            localizedDt = \
                localizedDt - datetime.timedelta(minutes=totalMinutesOffset)
        elif birthInfo.timeOffsetLMTRadioButtonState == True:
            # Use 4 minutes of time offset for each longitude degree away
            # from 0.
            timeShiftMinutes = self.longitudeDegrees * -4.0
        
            localizedDt = \
                localizedDt - datetime.timedelta(minutes=totalMinutesOffset)
        
        # Open Astrolog with these values.
        self.handleAstrologLaunch(localizedDt, birthInfo)

    def _handleOpenAstroChart1WithBirthInfoAction(self):
        """Slot function that is called when the
        self.openAstroChart1WithBirthInfoAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.setAstroChart1WithBirthInfo()
        
    def _handleOpenAstroChart2WithBirthInfoAction(self):
        """Slot function that is called when the
        self.openAstroChart2WithBirthInfoAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.setAstroChart2WithBirthInfo()

    def _handleOpenAstroChart3WithBirthInfoAction(self):
        """Slot function that is called when the
        self.openAstroChart3WithBirthInfoAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.setAstroChart3WithBirthInfo()
        
    def _handleOpenAstroChart1WithNowAction(self):
        """Slot function that is called when the
        self.openAstroChart1WithNowAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.setAstroChart1WithNow()

    def _handleOpenAstroChart2WithNowAction(self):
        """Slot function that is called when the
        self.openAstroChart2WithNowAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.setAstroChart2WithNow()

    def _handleOpenAstroChart3WithNowAction(self):
        """Slot function that is called when the
        self.openAstroChart3WithNowAction QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.setAstroChart3WithNow()

    def _handleClearAstroChart1Action(self):
        """Slot function that is called when the
        self.clearAstroChart1Action QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.clearAstroChart1()

    def _handleClearAstroChart2Action(self):
        """Slot function that is called when the
        self.clearAstroChart2Action QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.clearAstroChart2()

    def _handleClearAstroChart3Action(self):
        """Slot function that is called when the
        self.clearAstroChart3Action QAction is triggered.
        """

        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        pcd.clearAstroChart3()

    def _toolsActionTriggered(self, qaction):
        """Slot function that is called when a Tools menu QAction is
        selected/activated.  This changes the Tools mode to whatever the
        new selection is.
        
        Arguments:
        qaction - Reference to the QAction that was triggered.
        """

        self.log.debug("Entered _toolsActionTriggered()")

        # Tool actions only make sense to be triggered if there is a
        # PriceChartDocument open and active.  
        # Check to make sure that is true.
        pcd = self.getActivePriceChartDocument()
        if pcd == None:
            return

        if qaction == self.readOnlyPointerToolAction:
            self.log.debug("readOnlyPointerToolAction triggered.")
            pcd.toReadOnlyPointerToolMode()
        elif qaction == self.pointerToolAction:
            self.log.debug("pointerToolAction triggered.")
            pcd.toPointerToolMode()
        elif qaction == self.handToolAction:
            self.log.debug("handToolAction triggered.")
            pcd.toHandToolMode()
        elif qaction == self.zoomInToolAction:
            self.log.debug("zoomInToolAction triggered.")
            pcd.toZoomInToolMode()
        elif qaction == self.zoomOutToolAction:
            self.log.debug("zoomOutToolAction triggered.")
            pcd.toZoomOutToolMode()
        elif qaction == self.barCountToolAction:
            self.log.debug("barCountToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toBarCountToolMode()
        elif qaction == self.timeMeasurementToolAction:
            self.log.debug("timeMeasurementToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toTimeMeasurementToolMode()
        elif qaction == self.timeModalScaleToolAction:
            self.log.debug("timeModalScaleToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toTimeModalScaleToolMode()
        elif qaction == self.priceModalScaleToolAction:
            self.log.debug("priceModalScaleToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toPriceModalScaleToolMode()
        elif qaction == self.planetLongitudeMovementMeasurementToolAction:
            self.log.debug(\
                "planetLongitudeMovementMeasurementToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toPlanetLongitudeMovementMeasurementToolMode()
        elif qaction == self.textToolAction:
            self.log.debug("textToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toTextToolMode()
        elif qaction == self.priceTimeInfoToolAction:
            self.log.debug("priceTimeInfoToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toPriceTimeInfoToolMode()
        elif qaction == self.priceMeasurementToolAction:
            self.log.debug("priceMeasurementToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toPriceMeasurementToolMode()
        elif qaction == self.timeRetracementToolAction:
            self.log.debug("timeRetracementToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toTimeRetracementToolMode()
        elif qaction == self.priceRetracementToolAction:
            self.log.debug("priceRetracementToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toPriceRetracementToolMode()
        elif qaction == self.priceTimeVectorToolAction:
            self.log.debug("priceTimeVectorToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toPriceTimeVectorToolMode()
        elif qaction == self.lineSegment1ToolAction:
            self.log.debug("lineSegment1ToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toLineSegment1ToolMode()
        elif qaction == self.lineSegment2ToolAction:
            self.log.debug("lineSegment2ToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toLineSegment2ToolMode()
        elif qaction == self.octaveFanToolAction:
            self.log.debug("octaveFanToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toOctaveFanToolMode()
        elif qaction == self.fibFanToolAction:
            self.log.debug("fibFanToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toFibFanToolMode()
        elif qaction == self.gannFanToolAction:
            self.log.debug("gannFanToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toGannFanToolMode()
        elif qaction == self.vimsottariDasaToolAction:
            self.log.debug("vimsottariDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toVimsottariDasaToolMode()
        elif qaction == self.ashtottariDasaToolAction:
            self.log.debug("ashtottariDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toAshtottariDasaToolMode()
        elif qaction == self.yoginiDasaToolAction:
            self.log.debug("yoginiDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toYoginiDasaToolMode()
        elif qaction == self.dwisaptatiSamaDasaToolAction:
            self.log.debug("dwisaptatiSamaDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toDwisaptatiSamaDasaToolMode()
        elif qaction == self.shattrimsaSamaDasaToolAction:
            self.log.debug("shattrimsaSamaDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toShattrimsaSamaDasaToolMode()
        elif qaction == self.dwadasottariDasaToolAction:
            self.log.debug("dwadasottariDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toDwadasottariDasaToolMode()
        elif qaction == self.chaturaseetiSamaDasaToolAction:
            self.log.debug("chaturaseetiSamaDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toChaturaseetiSamaDasaToolMode()
        elif qaction == self.sataabdikaDasaToolAction:
            self.log.debug("sataabdikaDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toSataabdikaDasaToolMode()
        elif qaction == self.shodasottariDasaToolAction:
            self.log.debug("shodasottariDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toShodasottariDasaToolMode()
        elif qaction == self.panchottariDasaToolAction:
            self.log.debug("panchottariDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toPanchottariDasaToolMode()
        elif qaction == self.shashtihayaniDasaToolAction:
            self.log.debug("shashtihayaniDasaToolAction triggered.")
            self.mostRecentGraphicsItemToolModeAction = qaction
            pcd.toShashtihayaniDasaToolMode()
        else:
            self.log.warn("Unknown Tools QAction selected!  " + \
                "There might be something wrong with the code, or " + \
                "I maybe forgot to add a qaction type.")
            
        self.log.debug("Exiting _toolsActionTriggered()")

    
    def keyPressEvent(self, qkeyevent):
        """Overwrites the QGraphicsView.keyPressEvent() function.
        Called when a key is pressed.
        """

        self.log.debug("Entered keyPressEvent()")

        if qkeyevent.key() == Qt.Key_F1 or \
               (platform.system() == "Darwin" and qkeyevent.key() == Qt.Key_1):
            
            self.log.debug("Key Pressed: Qt.Key_F1 or (Qt.Key_1 on Darwin)")
            
            # Trigger ReadOnlyPointerToolAction.
            if self.readOnlyPointerToolAction.isEnabled():
                self.readOnlyPointerToolAction.trigger()
                
        elif qkeyevent.key() == Qt.Key_F2 or \
               (platform.system() == "Darwin" and qkeyevent.key() == Qt.Key_2):
            self.log.debug("Key Pressed: Qt.Key_F2 or (Qt.Key_2 on Darwin)")
            
            # Trigger PointerToolAction.
            if self.pointerToolAction.isEnabled():
                self.pointerToolAction.trigger()

        elif qkeyevent.key() == Qt.Key_F3 or \
               (platform.system() == "Darwin" and qkeyevent.key() == Qt.Key_3):
            self.log.debug("Key Pressed: Qt.Key_F3 or (Qt.Key_3 on Darwin)")

            # Trigger HandToolAction.
            if self.handToolAction.isEnabled():
                self.handToolAction.trigger()

        elif qkeyevent.key() == Qt.Key_F4 or \
               (platform.system() == "Darwin" and qkeyevent.key() == Qt.Key_4):
            self.log.debug("Key Pressed: Qt.Key_F4 or (Qt.Key_4 on Darwin)")
            
            # Trigger the last used QGraphicsItem tool mode QAction.
            if self.mostRecentGraphicsItemToolModeAction != None:
                if self.mostRecentGraphicsItemToolModeAction.isEnabled():
                    self.mostRecentGraphicsItemToolModeAction.trigger()

        else:
            # For any other key just pass the event to the parent to handle.
            super().keyPressEvent(qkeyevent)
            
        self.log.debug("Exiting keyPressEvent()")

    def _showShortcutKeys(self):
        """Opens up a popup window displaying information about the
        supported shortcut keys.
        """
        
        endl = os.linesep

        title = "Shortcut Keys"

        message = \
"""
Shortcut keys:

Tool Modes:
  - Key_F1: ReadOnlyPointerToolAction
  - Key_F2: PointerToolAction
  - Key_F3: HandToolAction
  - Key_F4: Trigger the last used tool mode (that is not one of the above).

Time Modal Scale Tool:
  - Key_S: Rotate the modal scale left.
  - Key_G: Rotate the modal scale right.
  - Key_R: Reverse the direction of the modal scale.

Price Modal Scale Tool:
  - Key_S: Rotate the modal scale down.
  - Key_G: Rotate the modal scale up.
  - Key_R: Reverse the direction of the modal scale.

Octave Fan Tool:
  - Key_S: Rotate the modal scale up.
  - Key_G: Rotate the modal scale down.
  - Key_R: Reverse the direction of the modal scale.

Snap key bindings are:
  - Key_Q: Turn snap mode on.
  - Key_W: Turn snap mode off.

Snap key bindings are supported for the following tools:
  - BarCountTool
  - TimeMeasurementTool
  - PriceMeasurementTool
  - TimeModalScaleTool
  - PriceModalScaleTool
  - PriceTimeInfoTool
  - TimeRetracementTool
  - PriceRetracementTool
  - PriceTimeVectorTool
  - LineSegment1Tool
  - LineSegment2Tool
  - OctaveFanTool
  - FibFanTool
  - GannFanTool
  - VimsottariDasaTool
  - AshtottariDasaTool
  - YoginiDasaTool
  - DwisaptatiSamaDasaTool
  - ShattrimsaSamaDasaTool
  - DwadasottariDasaTool
  - ChaturaseetiSamaDasaTool
  - SataabdikaDasaTool
  - ShodasottariDasaTool
  - PanchottariDasaTool
  - ShashtihayaniDasaTool
"""
        
        QMessageBox.about(self, title, message)
        
    def _memoryUsage(self):
        """Opens a popup window displaying memory utilization
        information about this application.

        Source info on how to do this is from:
        http://stackoverflow.com/questions/938733/python-total-memory-used
        """

        endl = os.linesep

        title = "Memory Usage"

        message = ""
        
        
        if platform.system() == "Linux":
            # Linux.
            message += self.appName + " process status:" + endl + endl

            procStatusFilename = "/proc/{}/status".format(os.getpid())

            try:
                f = open(procStatusFilename)
                for line in f:
                    if line.startswith("Name:") or \
                       line.startswith("Pid:") or \
                       line.startswith("FDSize:") or \
                       line.startswith("VmPeak:") or \
                       line.startswith("VmSize:") or \
                       line.startswith("VmRSS:") or \
                       line.startswith("VmStk:"):

                        message += line
                f.close()
                
                message += endl
                message += endl
                message += "Note: " + endl + endl
                message += "Name   == Command run by this process" + endl
                message += "Pid    == Thread ID" + endl
                message += "FDSize == Number of file descriptors" + endl
                message += "VmPeak == Peak virtual memory size" + endl
                message += "VmSize == Virtual memory size" + endl
                message += "VmRSS  == Resident set size" + endl
                message += "VmStk  == Stack size" + endl
                
            except IOError as e:
                errMsg = "Could not open '{}' to read process status." + \
                         "  {}".format(e)
                self.log.warn(errMsg)
                message += errMsg
                
        elif platform.system() == "Windows":
            # Windows.  The below is untested.
            message += self.appName + " memory usage:" + endl + endl

            from wmi import WMI
            w = WMI('.')
            result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess={}".format(os.getpid()))
            #bytes = int(result[0]['WorkingSet'])
            bytes = int(result[0].WorkingSet)

            kilobytes = bytes / 1024
            megabytes = kilobytes / 1024
            
            message += "Bytes: {}".format(bytes) + endl + \
                       "Kilobytes: {}".format(kilobytes) + endl + \
                       "Megabytes: {}".format(megabytes) + endl
            
        elif platform.system() == "Darwin":
            # MacOS X.
            message += self.appName + " memory usage:" + endl + endl

            # Call ps on this and get the output.
            outputBinary = \
                subprocess.check_output(\
                "ps aux | grep -i python | grep -v 'grep' | grep {}".\
                format(os.getpid()),
                stderr=subprocess.STDOUT,
                shell=True)
            
            outputText = outputBinary.decode("utf-8")

            # Go through all the results of ps.
            foundFlag = False
            for line in outputText.split(os.linesep):
                
                splitLine = line.split()

                # Make sure we don't have an incomplete line.
                if len(splitLine) > 8:
                    # Process ID.
                    pidStr = splitLine[1]
                    
                    # VSZ (Virtual Set Size).
                    vszStr = splitLine[4]

                    # RSS (Resident Set Size).
                    rssStr = splitLine[5]

                    # Only use the values if the process id matches.
                    if os.getpid() == int(pidStr):
                        message += "Pid: {}".format(pidStr) + endl
                        message += "VSZ: {} KB".format(vszStr) + endl
                        message += "RSS: {} KB".format(rssStr) + endl
                        foundFlag = True
                        break

            if foundFlag == True:
                message += endl
                message += "Note:" + endl + endl
                message += "Pid == Process ID" + endl
                message += "VSZ == Virtual Set Size" + endl
                message += "RSS == Resident Set Size" + endl
        else:
            message += "Unable to determine Memory usage."

        QMessageBox.about(self, title, message)

        

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

    # Signal emitted when the user desires to view a datetime.datetime
    # in JHora.
    jhoraLaunch = QtCore.pyqtSignal(datetime.datetime, BirthInfo)
    
    # Signal emitted when the user desires to view a datetime.datetime
    # in Astrolog.
    astrologLaunch = QtCore.pyqtSignal(datetime.datetime, BirthInfo)
    
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
            "Untitled{}".\
                format(PriceChartDocument.untitledDocSequenceNum) + \
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

        # Connect signals and slots.
        self.widgets.priceChartDocumentWidgetChanged.\
            connect(self._handlePriceChartDocumentWidgetChanged)
        self.widgets.statusMessageUpdate.\
            connect(self.statusMessageUpdate)
        self.widgets.jhoraLaunch.\
            connect(self.handleJhoraLaunch)
        self.widgets.astrologLaunch.\
            connect(self.handleAstrologLaunch)
        
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
        try:
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
        except IOError as e:
            self.log.error("IOError while trying to open a file: {}".\
                format(e))

            rv = False

            QMessageBox.warning(None, 
                                "Error", 
                                "IOError exception: " + 
                                os.linesep + os.linesep + "{}".format(e))

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

        # Set the description text.
        self.widgets.\
            setDescriptionText(self.priceChartDocumentData.description)
        
        # Set the timezone.
        self.widgets.setTimezone(self.priceChartDocumentData.locationTimezone)

        # Set the birth info.
        self.widgets.setBirthInfo(self.priceChartDocumentData.birthInfo)

        # Load pricebars.
        priceBars = self.priceChartDocumentData.priceBars
        self.widgets.loadPriceBars(priceBars)

        # Apply the settings objects.
        priceBarChartSettings = \
            self.priceChartDocumentData.priceBarChartSettings
        priceBarSpreadsheetSettings = \
            self.priceChartDocumentData.priceBarSpreadsheetSettings
        self.widgets.applyPriceBarChartSettings(priceBarChartSettings)
        self.widgets.\
            applyPriceBarSpreadsheetSettings(priceBarSpreadsheetSettings)

        # Load the chart artifacts.
        priceBarChartArtifacts = \
            self.priceChartDocumentData.priceBarChartArtifacts
        self.widgets.loadPriceBarChartArtifacts(priceBarChartArtifacts)
        
        # By default, set the flag as dirty.  
        # If this was an open/load from file, the caller of this 
        # function should themselves call the function to set the flag to
        # be not dirty.
        self.setDirtyFlag(True)

        self.log.\
            debug("Exiting setPriceChartDocumentData()")
        
    def applyPriceBarChartSettings(self, priceBarChartSettings):
        """Applies the given PriceBarChartSettings to the underlying
        PriceBarChart.  
        
        The caller is responsible for setting the dirty
        flag if this priceBarChartSettings is different from the 
        currently used internal priceBarChartSettings.
        If it is expected to be the same, then the parent will need to
        explicitly set the dirty flag to False because a redraw of the
        internal widgets will cause signals to be emitted to notify
        higher-up qobjects that there are outstanding changes.
        """

        self.priceChartDocumentData.priceBarChartSettings = \
            priceBarChartSettings

        self.widgets.applyPriceBarChartSettings\
                (self.priceChartDocumentData.priceBarChartSettings)

    def applyPriceBarSpreadsheetSettings(self, priceBarSpreadsheetSettings):
        """Applies the given PriceBarSpreadsheetSettings to the underlying
        PriceBarSpreadsheet.  The caller is responsible for setting the dirty
        flag if this priceBarSpreadsheetSettings is different from the 
        currently used internal priceBarSpreadsheetSettings 
        (which most likely it is).
        """

        self.priceChartDocumentData.priceBarSpreadsheetSettings = \
            priceBarSpreadsheetSettings

        self.widgets.applyPriceBarSpreadsheetSettings\
                (self.priceChartDocumentData.priceBarSpreadsheetSettings)

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

        self.widgets.setBirthInfo(birthInfo)

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
            settings.value("ui/defaultPriceChartDocumentSaveDirectory",
                           defaultValue="",
                           type=str)

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

    def checkSourceDataFileForPriceBarUpdates(self):
        """Checks the original data file from which we got the
        PriceBars to see if there are any updates.  If there aren't
        any differences from when we originally loaded the PriceBars,
        then a statusMessageUpdate is emitted, but nothing else
        happens.  If there are differences, then we'll prompt for
        whether to update or not.
        """

        self.log.debug("Entered checkSourceDataFileForPriceBarUpdates()")

        # First, make sure the original data source CSV file still
        # exists on the file system where we think it is.
        dataSourceFilename = self.priceChartDocumentData.priceBarsFileFilename
        numLinesToSkip = self.priceChartDocumentData.priceBarsFileNumLinesToSkip
        currPriceBars  = self.priceChartDocumentData.priceBars
        timezoneObj = self.priceChartDocumentData.locationTimezone

        self.log.info("Checking to see if the data source CSV file " +
                       "'{}' exists...".format(dataSourceFilename))
        
        if not os.path.exists(dataSourceFilename):
            self.log.info("Data source file does not exist.  " +
                          "Trying to rectify the situation...")
        
            # Popup to let the user know that the backing data source
            # file couldn't be found.  Prompt to see if the user wants
            # to set a new path of the file.
            parent = self
            title = "Data source file missing"
            text = "The CSV text file that was previously used to obtain " + \
                   "the PriceBars can no longer be found.  " + \
                   os.linesep + os.linesep + \
                   "Would you like to re-set the path of the CSV file now?"
            buttons = QMessageBox.Yes | QMessageBox.No
            defaultButton = QMessageBox.NoButton
        
            buttonClicked = \
                QMessageBox.warning(parent, title, text, buttons, defaultButton)

            if buttonClicked == QMessageBox.No:
                # No action desired.
                self.log.info("User declined to update the path to the " +
                              "data source CSV file.")
                return
            else:
                # Prompt for file.

                filename = ""
                keepTrying = True

                # Keep trying until we succeed or the user decides to
                # stop trying.
                while keepTrying == True:
                    self.log.debug("Prompting for the file...")
                    widget = LoadDataFileWidget()
                    widget.hide()
                    widget.handleBrowseButtonClicked()
                    filename = widget.filenameLineEdit.text()

                    self.log.debug("filename selected is: {}".\
                                   format(filename))
                    
                    if filename == "":
                        self.log.debug("An error or invalid file was selected.")
                        
                        parent = self
                        title = "Open file"
                        text = "A valid CSV text file was not selected.  " + \
                               os.linesep + os.linesep + \
                               "Want to try to select a file again?"
                        buttons = QMessageBox.Yes | QMessageBox.No
                        defaultButton = QMessageBox.Yes
                        
                        buttonClicked = \
                            QMessageBox.question(parent, title, text,
                                                 buttons, defaultButton)

                        if buttonClicked == QMessageBox.Yes:
                            keepTrying = True
                            self.log.debug("User wants to select a file again.")
                        
                        else:
                            keepTrying = False
                            self.log.info("User declined to update the " +
                                          "path to the data source CSV file.")
                    else:
                        # We have a filename now.
                        keepTrying = False
                
                if filename != "":
                    text = "Updating the data source filename from " + \
                           "{} to {}".\
                           format(dataSourceFilename, filename)
                    self.log.info(text)
                    self.statusMessageUpdate.emit(text)

                    self.priceChartDocumentData.priceBarsFileFilename = filename
                    dataSourceFilename = filename
                    
                    self.setDirtyFlag(True)
                    
        # If we are still in this function at this point, then the
        # data source filename should be a valid file.
        self.log.info("The data source file has now been confirmed to exist.")
        
        # Make sure the CSV data file is in a valid format.
        self.log.info("Now validating the data in the file...")

        wizard = PriceChartDocumentWizard()
        widget = \
            wizard.priceChartDocumentLoadDataFileWizardPage.loadDataFileWidget
        widget.filenameLineEdit.setText(dataSourceFilename)
        widget.skipLinesSpinBox.setValue(numLinesToSkip)
        widget.handleValidateButtonClicked()
        if not widget.isValidated():
            self.log.warn("Data source file failed validation: {}".\
                          format(dataSourceFilename))
            parent = self
            title = "Data source file validation"
            linesep = "<br />"
            text = "While trying to check for new PriceBar data " + \
                "from the backing data source CSV file ({})".\
                format(dataSourceFilename) + \
                ", an error occured because validation failed.  " + \
                linesep + linesep + \
                "{}".format(widget.validationStatusLabel.text()) + \
                linesep + linesep + \
                "Please correct any format problems before retrying to " + \
                "update with new PriceBar data."
            
            buttons = QMessageBox.Ok
            defaultButton = QMessageBox.Ok
            
            buttonClicked = \
                QMessageBox.warning(parent, title, text,
                                    buttons, defaultButton)
            return
        else:
            self.log.info("Data validation succeeded.")

        # Get the list of new PriceBars.  Here we need to utilize the
        # PriceChartDocumentWizard because the timestamps in the
        # PriceBars need to be in the localized timezone.  This is
        # done by utilizing the wizard and calling the same method we
        # used to create PriceBars originally, but first we must make
        # sure the wizard has all the values it needs (timezone,
        # etc.), just like if we loaded the ui via the user.
        comboBox = wizard.priceChartDocumentLocationTimezoneWizardPage.\
                   locationTimezoneEditWidget.timezoneComboBox
        index = comboBox.findText(timezoneObj.zone)
        if index == -1:
            self.log.error("Couldn't find the timezone in the QComboBox: " + \
                           "{}".format(timezoneObj.zone))
            QMessageBox.warning("Error occurred.  Check the log files for why.")
            return
        else:
            comboBox.setCurrentIndex(index)
        newPriceBars = wizard.getPriceBars()
        
        # If there are differences, prompt via a dialog for action to take.
        dialog = PriceBarsCompareDialog(currPriceBars, newPriceBars, self)
        if not dialog.arePriceBarListsEqual():
            self.log.debug("PriceBar lists are different.")
            
            rv = dialog.exec_()
            if rv == QDialog.Accepted:
                self.log.info("Overwriting current PriceBars with the " +
                              "new PriceBars.")

                # Overwrite list of PriceBars.
                self.priceChartDocumentData.priceBars = newPriceBars

                # Update the UI.
                self.widgets.clearAllPriceBars()
                self.widgets.loadPriceBars(\
                    self.priceChartDocumentData.priceBars)

                # Set the dirty flag since now priceBars are different.
                self.setDirtyFlag(True)

                parent = self
                title = "Information"
                linesep = "<br />"
                text = "PriceBars were updated."
                QMessageBox.information(parent, title, text)

            else:
                self.log.debug("Keeping current PriceBars.")

                parent = self
                title = "Information"
                linesep = "<br />"
                text = "PriceBars unchanged."
                QMessageBox.information(parent, title, text)
                
        else:
            self.log.debug("PriceBar lists are the same.  " + \
                           "No additional actions are required.")

            parent = self
            title = "Information"
            linesep = "<br />"
            text = "PriceBars are already up to date.  "
            QMessageBox.information(parent, title, text)
        
        self.log.debug("Exiting checkSourceDataFileForPriceBarUpdates()")
        
    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool."""

        self.widgets.toReadOnlyPointerToolMode()

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool."""

        self.widgets.toPointerToolMode()

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.widgets.toHandToolMode()

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.widgets.toZoomInToolMode()

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.widgets.toZoomOutToolMode()

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.widgets.toBarCountToolMode()

    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.widgets.toTimeMeasurementToolMode()

    def toTimeModalScaleToolMode(self):
        """Changes the tool mode to be the TimeModalScaleTool."""

        self.widgets.toTimeModalScaleToolMode()

    def toPriceModalScaleToolMode(self):
        """Changes the tool mode to be the PriceModalScaleTool."""

        self.widgets.toPriceModalScaleToolMode()

    def toPlanetLongitudeMovementMeasurementToolMode(self):
        """Changes the tool mode to be the
        PlanetLongitudeMovementMeasurementTool."""

        self.widgets.toPlanetLongitudeMovementMeasurementToolMode()

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.widgets.toTextToolMode()

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.widgets.toPriceTimeInfoToolMode()

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.widgets.toPriceMeasurementToolMode()

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.widgets.toTimeRetracementToolMode()

    def toPriceRetracementToolMode(self):
        """Changes the tool mode to be the PriceRetracementTool."""

        self.widgets.toPriceRetracementToolMode()

    def toPriceTimeVectorToolMode(self):
        """Changes the tool mode to be the PriceTimeVectorTool."""

        self.widgets.toPriceTimeVectorToolMode()

    def toLineSegment1ToolMode(self):
        """Changes the tool mode to be the LineSegment1Tool."""

        self.widgets.toLineSegment1ToolMode()

    def toLineSegment2ToolMode(self):
        """Changes the tool mode to be the LineSegment2Tool."""

        self.widgets.toLineSegment2ToolMode()

    def toOctaveFanToolMode(self):
        """Changes the tool mode to be the OctaveFanTool."""

        self.widgets.toOctaveFanToolMode()

    def toFibFanToolMode(self):
        """Changes the tool mode to be the FibFanTool."""

        self.widgets.toFibFanToolMode()

    def toGannFanToolMode(self):
        """Changes the tool mode to be the GannFanTool."""

        self.widgets.toGannFanToolMode()

    def toVimsottariDasaToolMode(self):
        """Changes the tool mode to be the VimsottariDasaTool."""

        self.widgets.toVimsottariDasaToolMode()

    def toAshtottariDasaToolMode(self):
        """Changes the tool mode to be the AshtottariDasaTool."""

        self.widgets.toAshtottariDasaToolMode()

    def toYoginiDasaToolMode(self):
        """Changes the tool mode to be the YoginiDasaTool."""

        self.widgets.toYoginiDasaToolMode()

    def toDwisaptatiSamaDasaToolMode(self):
        """Changes the tool mode to be the DwisaptatiSamaDasaTool."""

        self.widgets.toDwisaptatiSamaDasaToolMode()

    def toShattrimsaSamaDasaToolMode(self):
        """Changes the tool mode to be the ShattrimsaSamaDasaTool."""

        self.widgets.toShattrimsaSamaDasaToolMode()

    def toDwadasottariDasaToolMode(self):
        """Changes the tool mode to be the DwadasottariDasaTool."""

        self.widgets.toDwadasottariDasaToolMode()

    def toChaturaseetiSamaDasaToolMode(self):
        """Changes the tool mode to be the ChaturaseetiSamaDasaTool."""

        self.widgets.toChaturaseetiSamaDasaToolMode()

    def toSataabdikaDasaToolMode(self):
        """Changes the tool mode to be the SataabdikaDasaTool."""

        self.widgets.toSataabdikaDasaToolMode()

    def toShodasottariDasaToolMode(self):
        """Changes the tool mode to be the ShodasottariDasaTool."""

        self.widgets.toShodasottariDasaToolMode()

    def toPanchottariDasaToolMode(self):
        """Changes the tool mode to be the PanchottariDasaTool."""

        self.widgets.toPanchottariDasaToolMode()

    def toShashtihayaniDasaToolMode(self):
        """Changes the tool mode to be the ShashtihayaniDasaTool."""

        self.widgets.toShashtihayaniDasaToolMode()

    def handleJhoraLaunch(self, dt, birthInfo):
        """Handles a launch of JHora with the given datetime.datetime.
        This function assumes that the birth information is available
        via self.getBirthInfo().

        Arguments:
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in JHora.  This is used to get the
             julian day.
        birthInfo - BirthInfo object with the information about
                    birth set (e.g., birth location, elevation, etc.)
        """

        # Pass the command onto the parent MainWindow to handle.
        self.jhoraLaunch.emit(dt, birthInfo)

    def handleAstrologLaunch(self, dt, birthInfo):
        """Handles a launch of Astrolog with the given datetime.datetime.
        This function assumes that the birth information is available
        via self.getBirthInfo().

        Arguments:
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in Astrolog.  This is used to get the
             julian day.
        birthInfo - BirthInfo object with the information about
                    birth set (e.g., birth location, elevation, etc.)
        """

        # Pass the command onto the parent MainWindow to handle.
        self.astrologLaunch.emit(dt, birthInfo)

    def setEnableAndShowAstrologyChart(self, flag):
        """Shows and sets the link-connection enabled or disabled for
        the AstrologyChart.

        Arguments:
        
        flag - True if the link is to be enabled and widget shown,
               False if the link is to be disabled and widget hidden.
        """

        self.widgets.setEnableAndShowAstrologyChart(flag)
        
    def setEnableAndShowPlanetaryInfoTable(self, flag):
        """Shows and sets the link-connection enabled or disabled for
        the PlanetaryInfoTable.

        Arguments:
        
        flag - True if the link is to be enabled and widget shown,
               False if the link is to be disabled and widget hidden.
        """

        self.widgets.setEnableAndShowPlanetaryInfoTable(flag)
        
    def setTrackMouseToAstroChart1(self, flag):
        """Sets the link-connection enabled or disabled for the
        pricebarchart mouse position to AstroChart1.

        Arguments:
        flag - True if the link is to be enabled, False if the link
               is to be disabled.
        """

        self.widgets.setTrackMouseToAstroChart1(flag)
        
    def setTrackMouseToAstroChart2(self, flag):
        """Sets the link-connection enabled or disabled for the
        pricebarchart mouse position to AstroChart2.

        Arguments:
        flag - True if the link is to be enabled, False if the link
               is to be disabled.
        """

        self.widgets.setTrackMouseToAstroChart2(flag)
        
    def setTrackMouseToAstroChart3(self, flag):
        """Sets the link-connection enabled or disabled for the
        pricebarchart mouse position to AstroChart3.

        Arguments:
        flag - True if the link is to be enabled, False if the link
               is to be disabled.
        """

        self.widgets.setTrackMouseToAstroChart3(flag)

    def setAstroChart1WithBirthInfo(self):
        """Sets AstroChart1 with the info in the BirthInfo of this document.
        """
        
        self.widgets.setAstroChart1WithBirthInfo()
        
    def setAstroChart2WithBirthInfo(self):
        """Sets AstroChart2 with the info in the BirthInfo of this document.
        """
        
        self.widgets.setAstroChart2WithBirthInfo()
        
    def setAstroChart3WithBirthInfo(self):
        """Sets AstroChart3 with the info in the BirthInfo of this document.
        """
        
        self.widgets.setAstroChart3WithBirthInfo()
    
    def setAstroChart1WithNow(self):
        """Sets AstroChart1 with the current time."""
        
        self.widgets.setAstroChart1WithNow()
        
    def setAstroChart2WithNow(self):
        """Sets AstroChart2 with the current time."""
        
        self.widgets.setAstroChart2WithNow()
        
    def setAstroChart3WithNow(self):
        """Sets AstroChart3 with the current time."""
        
        self.widgets.setAstroChart3WithNow()

    def clearAstroChart1(self):
        """Clears the AstroChart1."""

        self.widgets.clearAstroChart1()
        
    def clearAstroChart2(self):
        """Clears the AstroChart2."""

        self.widgets.clearAstroChart2()
        
    def clearAstroChart3(self):
        """Clears the AstroChart3."""

        self.widgets.clearAstroChart3()
        
    def _handlePriceChartDocumentWidgetChanged(self):
        """Slot for when the PriceBarDocumentWidget emits a signal to say
        that the widget(s) changed.  This means the document should be
        marked as dirty.
        """
        
        if self.getDirtyFlag() != True:
            self.setDirtyFlag(True)

    def toString(self):
        """Returns the str representation of this object.
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
        """Returns the str representation of this object.
        """

        return self.toString() 

class PriceChartDocumentWidget(QWidget):
    """Internal widget within a PriceChartDocument (QMdiSubWindow) that
    holds all the other widgets.  This basically serves as a QLayout
    for the PriceChartDocument.
    """

    # Signal emitted when the widgets in the PriceChartDocument changes.
    # This is caused by a meaningful change to either the contents, or the
    # settings object for that widget.
    priceChartDocumentWidgetChanged = QtCore.pyqtSignal()

    # Signal emitted when a status message should be printed.
    statusMessageUpdate = QtCore.pyqtSignal(str)
    
    # Signal emitted when the user desires to view a datetime.datetime
    # in JHora.
    jhoraLaunch = QtCore.pyqtSignal(datetime.datetime, BirthInfo)
    
    # Signal emitted when the user desires to view a datetime.datetime
    # in Astrolog.
    astrologLaunch = QtCore.pyqtSignal(datetime.datetime, BirthInfo)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger("ui.PriceChartDocumentWidget")

        self.birthInfo = BirthInfo()

        # Flags for showing and linking the PlanetaryInfoTable and
        # Astrology Chart.
        self.planetaryInfoTableWidgetEnabled = False
        self.astrologyChartWidgetEnabled = False
        
        # Flags for linking the mouse position of PriceBarChart to the
        # AstroCharts.
        self.trackMouseToAstroChart1Enabled = False
        self.trackMouseToAstroChart2Enabled = False
        self.trackMouseToAstroChart3Enabled = False
        
        # Create the internal widgets displayed.
        self.priceBarChartWidget = PriceBarChartWidget()
        self.priceBarSpreadsheetWidget = PriceBarSpreadsheetWidget()
        self.astrologyChartWidget = AstrologyChartWidget()
        self.planetaryInfoTableWidget = PlanetaryInfoTableWidget()

        # Set the PlanetaryInfoTable and the AstrologyChartWidget to
        # being not visible initially.  User can enable it if he or
        # she wants to use it.
        self.astrologyChartWidget.setVisible(False)
        self.planetaryInfoTableWidget.setVisible(False)

        # Set the birth info.
        self.setBirthInfo(self.birthInfo)


        # QSplitters to divide the internal widgets.
        vsplitter = QSplitter(self)
        vsplitter.setOrientation(Qt.Vertical)
        vsplitter.addWidget(self.astrologyChartWidget)
        vsplitter.addWidget(self.planetaryInfoTableWidget)
        #vsplitter.addWidget(self.priceBarSpreadsheetWidget)
        
        hsplitter = QSplitter(self)
        hsplitter.setOrientation(Qt.Horizontal)
        hsplitter.addWidget(self.priceBarChartWidget)
        hsplitter.addWidget(vsplitter)

        # Setup the layout.
        vlayout = QVBoxLayout()
        vlayout.addWidget(hsplitter)

        self.setLayout(vlayout)

        # Connect signals and slots.
        self.priceBarChartWidget.priceBarChartChanged.\
            connect(self._handleWidgetChanged)
        self.priceBarChartWidget.statusMessageUpdate.\
            connect(self.statusMessageUpdate)
        self.priceBarChartWidget.jhoraLaunch.\
            connect(self.handleJhoraLaunch)
        self.priceBarChartWidget.astrologLaunch.\
            connect(self.handleAstrologLaunch)
        self.priceBarChartWidget.currentTimestampChanged.\
            connect(self._handleCurrentTimestampChanged)
        
    def setBirthInfo(self, birthInfo):
        """Sets the birth info for this trading entity.
        
        Arguments:

        birthInfo - BirthInfo object.
        """

        self.birthInfo = birthInfo

        # Give the self.priceBarChartWidget the birth time.
        self.priceBarChartWidget.setBirthInfo(self.birthInfo)
        
        # Give the self.astrologyChartWidget the birth time.
        self.astrologyChartWidget.setBirthInfo(self.birthInfo)
        
    def setDescriptionText(self, text):
        """Sets the description text of this PriceChartDocument.
        
        Arguments:
            
        text - str variable holding the new text to set the description
               with.
        """

        self.priceBarChartWidget.setDescriptionText(text)
        
    def setTimezone(self, timezone):
        """Sets the timezone of this PriceChartDocument.
        
        Arguments:

        timezone - datetime.tzinfo object to set for the location of this
                   exchange/market.
        """

        self.priceBarChartWidget.setTimezone(timezone)

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

        # Load PriceBars into the PriceBarChart.
        self.priceBarChartWidget.loadPriceBars(priceBars)

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
        
        Note:  This will most likely cause a redraw and thus signals will
        be emitted to say that the view has changed.
        """

        self.log.debug("Entered applyPriceBarChartSettings()")

        self.log.debug("Applying the following settings: {}".\
                       format(priceBarChartSettings.toString()))
        
        self.priceBarChartWidget.\
            applyPriceBarChartSettings(priceBarChartSettings)

        self.log.debug("Exiting applyPriceBarChartSettings()")
        
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

    def toReadOnlyPointerToolMode(self):
        """Changes the tool mode to be the ReadOnlyPointerTool."""

        self.priceBarChartWidget.toReadOnlyPointerToolMode()

    def toPointerToolMode(self):
        """Changes the tool mode to be the PointerTool."""

        self.priceBarChartWidget.toPointerToolMode()

    def toHandToolMode(self):
        """Changes the tool mode to be the HandTool."""

        self.priceBarChartWidget.toHandToolMode()

    def toZoomInToolMode(self):
        """Changes the tool mode to be the ZoomInTool."""

        self.priceBarChartWidget.toZoomInToolMode()

    def toZoomOutToolMode(self):
        """Changes the tool mode to be the ZoomOutTool."""

        self.priceBarChartWidget.toZoomOutToolMode()

    def toBarCountToolMode(self):
        """Changes the tool mode to be the BarCountTool."""

        self.priceBarChartWidget.toBarCountToolMode()

    def toTimeMeasurementToolMode(self):
        """Changes the tool mode to be the TimeMeasurementTool."""

        self.priceBarChartWidget.toTimeMeasurementToolMode()

    def toTimeModalScaleToolMode(self):
        """Changes the tool mode to be the TimeModalScaleTool."""

        self.priceBarChartWidget.toTimeModalScaleToolMode()

    def toPriceModalScaleToolMode(self):
        """Changes the tool mode to be the PriceModalScaleTool."""

        self.priceBarChartWidget.toPriceModalScaleToolMode()

    def toPlanetLongitudeMovementMeasurementToolMode(self):
        """Changes the tool mode to be the
        PlanetLongitudeMovementMeasurementTool."""
        
        self.priceBarChartWidget.\
            toPlanetLongitudeMovementMeasurementToolMode()

    def toTextToolMode(self):
        """Changes the tool mode to be the TextTool."""

        self.priceBarChartWidget.toTextToolMode()

    def toPriceTimeInfoToolMode(self):
        """Changes the tool mode to be the PriceTimeInfoTool."""

        self.priceBarChartWidget.toPriceTimeInfoToolMode()

    def toPriceMeasurementToolMode(self):
        """Changes the tool mode to be the PriceMeasurementTool."""

        self.priceBarChartWidget.toPriceMeasurementToolMode()

    def toTimeRetracementToolMode(self):
        """Changes the tool mode to be the TimeRetracementTool."""

        self.priceBarChartWidget.toTimeRetracementToolMode()

    def toPriceRetracementToolMode(self):
        """Changes the tool mode to be the PriceRetracementTool."""

        self.priceBarChartWidget.toPriceRetracementToolMode()

    def toPriceTimeVectorToolMode(self):
        """Changes the tool mode to be the PriceTimeVectorTool."""

        self.priceBarChartWidget.toPriceTimeVectorToolMode()

    def toLineSegment1ToolMode(self):
        """Changes the tool mode to be the LineSegment1Tool."""

        self.priceBarChartWidget.toLineSegment1ToolMode()

    def toLineSegment2ToolMode(self):
        """Changes the tool mode to be the LineSegment2Tool."""

        self.priceBarChartWidget.toLineSegment2ToolMode()

    def toOctaveFanToolMode(self):
        """Changes the tool mode to be the OctaveFanTool."""

        self.priceBarChartWidget.toOctaveFanToolMode()

    def toFibFanToolMode(self):
        """Changes the tool mode to be the FibFanTool."""

        self.priceBarChartWidget.toFibFanToolMode()

    def toGannFanToolMode(self):
        """Changes the tool mode to be the GannFanTool."""

        self.priceBarChartWidget.toGannFanToolMode()

    def toVimsottariDasaToolMode(self):
        """Changes the tool mode to be the VimsottariDasaTool."""

        self.priceBarChartWidget.toVimsottariDasaToolMode()

    def toAshtottariDasaToolMode(self):
        """Changes the tool mode to be the AshtottariDasaTool."""

        self.priceBarChartWidget.toAshtottariDasaToolMode()

    def toYoginiDasaToolMode(self):
        """Changes the tool mode to be the YoginiDasaTool."""

        self.priceBarChartWidget.toYoginiDasaToolMode()

    def toDwisaptatiSamaDasaToolMode(self):
        """Changes the tool mode to be the DwisaptatiSamaDasaTool."""

        self.priceBarChartWidget.toDwisaptatiSamaDasaToolMode()

    def toShattrimsaSamaDasaToolMode(self):
        """Changes the tool mode to be the ShattrimsaSamaDasaTool."""

        self.priceBarChartWidget.toShattrimsaSamaDasaToolMode()

    def toDwadasottariDasaToolMode(self):
        """Changes the tool mode to be the DwadasottariDasaTool."""

        self.priceBarChartWidget.toDwadasottariDasaToolMode()

    def toChaturaseetiSamaDasaToolMode(self):
        """Changes the tool mode to be the ChaturaseetiSamaDasaTool."""

        self.priceBarChartWidget.toChaturaseetiSamaDasaToolMode()

    def toSataabdikaDasaToolMode(self):
        """Changes the tool mode to be the SataabdikaDasaTool."""

        self.priceBarChartWidget.toSataabdikaDasaToolMode()

    def toShodasottariDasaToolMode(self):
        """Changes the tool mode to be the ShodasottariDasaTool."""

        self.priceBarChartWidget.toShodasottariDasaToolMode()

    def toPanchottariDasaToolMode(self):
        """Changes the tool mode to be the PanchottariDasaTool."""

        self.priceBarChartWidget.toPanchottariDasaToolMode()

    def toShashtihayaniDasaToolMode(self):
        """Changes the tool mode to be the ShashtihayaniDasaTool."""

        self.priceBarChartWidget.toShashtihayaniDasaToolMode()

    def _handleWidgetChanged(self):
        """Handles when the internal widget has some kind of change
        that would cause the document to be dirty.  This is either a
        change in the contents, or perhaps some change in the settings
        object.
        """

        self.priceChartDocumentWidgetChanged.emit()

    def _updatePlanetaryInfoTable(self, dt):
        """Updates the cell values in the PlanetaryInfoTable by
        utilizing 'self.astrologyChartWidget'.
        """

        planetaryInfos = \
            self.astrologyChartWidget.getPlanetaryInfosForDatetime(dt)

        self.planetaryInfoTableWidget.load(planetaryInfos)

    def setEnableAndShowAstrologyChart(self, flag):
        """Shows and sets the link-connection enabled or disabled for
        the AstrologyChart.

        Arguments:
        
        flag - True if the link is to be enabled and widget shown,
               False if the link is to be disabled and widget hidden.
        """

        if self.astrologyChartWidgetEnabled == True and flag == False:
            
            self.priceBarChartWidget.astroChart1Update.\
                disconnect(self.astrologyChartWidget.setAstroChart1Datetime)
            self.priceBarChartWidget.astroChart2Update.\
                disconnect(self.astrologyChartWidget.setAstroChart2Datetime)
            self.priceBarChartWidget.astroChart3Update.\
                disconnect(self.astrologyChartWidget.setAstroChart3Datetime)
        
            self.astrologyChartWidget.setVisible(flag)

            self.astrologyChartWidgetEnabled = flag
            
        elif self.astrologyChartWidgetEnabled == False and flag == True:
            
            self.priceBarChartWidget.astroChart1Update.\
                connect(self.astrologyChartWidget.setAstroChart1Datetime)
            self.priceBarChartWidget.astroChart2Update.\
                connect(self.astrologyChartWidget.setAstroChart2Datetime)
            self.priceBarChartWidget.astroChart3Update.\
                connect(self.astrologyChartWidget.setAstroChart3Datetime)
        
            self.astrologyChartWidget.setVisible(flag)
            
            self.astrologyChartWidgetEnabled = flag
            
    def setEnableAndShowPlanetaryInfoTable(self, flag):
        """Shows and sets the link-connection enabled or disabled for
        the PlanetaryInfoTable.
        
        Arguments:
        
        flag - True if the link is to be enabled and widget shown,
        False if the link is to be disabled and widget hidden.
        """
        
        if self.planetaryInfoTableWidgetEnabled == True and flag == False:

            self.priceBarChartWidget.astroChart1Update.\
                disconnect(self._updatePlanetaryInfoTable)
            self.priceBarChartWidget.astroChart2Update.\
                disconnect(self._updatePlanetaryInfoTable)
            self.priceBarChartWidget.astroChart3Update.\
                disconnect(self._updatePlanetaryInfoTable)
            
            self.planetaryInfoTableWidget.setVisible(flag)
            
            self.planetaryInfoTableWidgetEnabled = flag
            
        elif self.planetaryInfoTableWidgetEnabled == False and flag == True:

            self.priceBarChartWidget.astroChart1Update.\
                connect(self._updatePlanetaryInfoTable)
            self.priceBarChartWidget.astroChart2Update.\
                connect(self._updatePlanetaryInfoTable)
            self.priceBarChartWidget.astroChart3Update.\
                connect(self._updatePlanetaryInfoTable)
        
            self.planetaryInfoTableWidget.setVisible(flag)
            
            self.planetaryInfoTableWidgetEnabled = flag
            
    def setTrackMouseToAstroChart1(self, flag):
        """Sets the link-connection enabled or disabled for the
        pricebarchart mouse position to AstroChart1.

        Arguments:
        flag - True if the link is to be enabled, False if the link
               is to be disabled.
        """

        self.trackMouseToAstroChart1Enabled = flag
        
    def setTrackMouseToAstroChart2(self, flag):
        """Sets the link-connection enabled or disabled for the
        pricebarchart mouse position to AstroChart2.

        Arguments:
        flag - True if the link is to be enabled, False if the link
               is to be disabled.
        """

        self.trackMouseToAstroChart2Enabled = flag
        
    def setTrackMouseToAstroChart3(self, flag):
        """Sets the link-connection enabled or disabled for the
        pricebarchart mouse position to AstroChart3.

        Arguments:
        flag - True if the link is to be enabled, False if the link
               is to be disabled.
        """

        self.trackMouseToAstroChart3Enabled = flag

    def setAstroChart1WithBirthInfo(self):
        """Sets AstroChart1 with the info in the BirthInfo of this document.
        """
        
        # Get the localized datetime of birth.
        localizedDt = self.birthInfo.getBirthLocalizedDatetime()

        if self.astrologyChartWidgetEnabled:
            # Open AstroChart1 with this value.
            self.astrologyChartWidget.setAstroChart1Datetime(localizedDt)

        if self.planetaryInfoTableWidgetEnabled:
            # Set PlanetaryInfoTable with this value.
            self._updatePlanetaryInfoTable(localizedDt)
        
    def setAstroChart2WithBirthInfo(self):
        """Sets AstroChart2 with the info in the BirthInfo of this document.
        """
        
        # Get the localized datetime of birth.
        localizedDt = self.birthInfo.getBirthLocalizedDatetime()

        if self.astrologyChartWidgetEnabled:
            # Open AstroChart2 with this value.
            self.astrologyChartWidget.setAstroChart2Datetime(localizedDt)
        
        if self.planetaryInfoTableWidgetEnabled:
            # Set PlanetaryInfoTable with this value.
            self._updatePlanetaryInfoTable(localizedDt)
        
    def setAstroChart3WithBirthInfo(self):
        """Sets AstroChart3 with the info in the BirthInfo of this document.
        """
        
        # Get the localized datetime of birth.
        localizedDt = self.birthInfo.getBirthLocalizedDatetime()

        if self.astrologyChartWidgetEnabled:
            # Open AstroChart3 with this value.
            self.astrologyChartWidget.setAstroChart3Datetime(localizedDt)
        
        if self.planetaryInfoTableWidgetEnabled:
            # Set PlanetaryInfoTable with this value.
            self._updatePlanetaryInfoTable(localizedDt)
        
    def setAstroChart1WithNow(self):
        """Sets AstroChart1 with the current time."""

        # Get the timezone for the BirthInfo.
        tzinfoObj = pytz.timezone(self.birthInfo.timezoneName)
        
        # Localize the 'now' timestamp.
        localizedDt = datetime.datetime.now(tzinfoObj)
        
        if self.astrologyChartWidgetEnabled:
            # Open AstroChart1 with this value.
            self.astrologyChartWidget.setAstroChart1Datetime(localizedDt)
        
        if self.planetaryInfoTableWidgetEnabled:
            # Set PlanetaryInfoTable with this value.
            self._updatePlanetaryInfoTable(localizedDt)
        
    def setAstroChart2WithNow(self):
        """Sets AstroChart2 with the current time."""
        
        # Get the timezone for the BirthInfo.
        tzinfoObj = pytz.timezone(self.birthInfo.timezoneName)
        
        # Localize the 'now' timestamp.
        localizedDt = datetime.datetime.now(tzinfoObj)
        
        if self.astrologyChartWidgetEnabled:
            # Open AstroChart2 with this value.
            self.astrologyChartWidget.setAstroChart2Datetime(localizedDt)
        
        if self.planetaryInfoTableWidgetEnabled:
            # Set PlanetaryInfoTable with this value.
            self._updatePlanetaryInfoTable(localizedDt)
        
    def setAstroChart3WithNow(self):
        """Sets AstroChart3 with the current time."""
        
        # Get the timezone for the BirthInfo.
        tzinfoObj = pytz.timezone(self.birthInfo.timezoneName)
            
        # Localize the 'now' timestamp.
        localizedDt = datetime.datetime.now(tzinfoObj)
        
        if self.astrologyChartWidgetEnabled:
            # Open AstroChart3 with this value.
            self.astrologyChartWidget.setAstroChart3Datetime(localizedDt)
        
        if self.planetaryInfoTableWidgetEnabled:
            # Set PlanetaryInfoTable with this value.
            self._updatePlanetaryInfoTable(localizedDt)
        
    def clearAstroChart1(self):
        """Clears the AstroChart1."""

        if self.astrologyChartWidgetEnabled:
            self.astrologyChartWidget.clearAstroChart1()
        
        if self.planetaryInfoTableWidgetEnabled:
            self.planetaryInfoTableWidget.clear()
            
    def clearAstroChart2(self):
        """Clears the AstroChart2."""

        if self.astrologyChartWidgetEnabled:
            self.astrologyChartWidget.clearAstroChart2()
        
        if self.planetaryInfoTableWidgetEnabled:
            self.planetaryInfoTableWidget.clear()
            
    def clearAstroChart3(self):
        """Clears the AstroChart3."""

        if self.astrologyChartWidgetEnabled:
            self.astrologyChartWidget.clearAstroChart3()
        
        if self.planetaryInfoTableWidgetEnabled:
            self.planetaryInfoTableWidget.clear()
            
    def handleJhoraLaunch(self, dt):
        """Handles a launch of JHora with the given datetime.datetime.
        This function assumes that the birth information is available
        via self.birthInfo.

        Arguments:
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in JHora.  This is used to get the
             julian day.
        """

        # Pass the command onto the parent MainWindow to handle.
        self.jhoraLaunch.emit(dt, self.birthInfo)
        
    def handleAstrologLaunch(self, dt):
        """Handles a launch of Astrolog with the given datetime.datetime.
        This function assumes that the birth information is available
        via self.birthInfo.

        Arguments:
        dt - datetime.datetime object holding the timestamp to use for
             launching and viewing in Astrolog.  This is used to get the
             julian day.
        """

        # Pass the command onto the parent MainWindow to handle.
        self.astrologLaunch.emit(dt, self.birthInfo)
        
    def _handleCurrentTimestampChanged(self, dt):
        """Handles when the current mouse cursor datetime changes.
        This just calls certain astrology widgets to update their
        display of what the current time is.  
        """
        
        if self.astrologyChartWidgetEnabled:
            
            if self.trackMouseToAstroChart1Enabled:
                self.astrologyChartWidget.setAstroChart1Datetime(dt)
                
            if self.trackMouseToAstroChart2Enabled:
                self.astrologyChartWidget.setAstroChart2Datetime(dt)
                
            if self.trackMouseToAstroChart3Enabled:
                self.astrologyChartWidget.setAstroChart3Datetime(dt)
                
        if self.planetaryInfoTableWidgetEnabled:
            
            if self.trackMouseToAstroChart1Enabled or \
                   self.trackMouseToAstroChart2Enabled or \
                   self.trackMouseToAstroChart3Enabled:
                
                self._updatePlanetaryInfoTable(dt)
                
