

# For logging.
import logging

# For newlines.
import os

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import image resources.
import resources

from widgets import ColorIcon

from data_objects import LookbackMultiple

from dialogs import LookbackMultipleEditDialog

# For calculating LookbackMultiple periods using planets.
from ephemeris import Ephemeris

class LookbackMultipleUtils:
    """Contains various static methods to assist in calculating 
    LookbackMultiple periods forwards and backwards.
    """
    
    # Logger object for this class.
    log = logging.getLogger("lookbackmultiple.LookbackMultipleUtils")
    
    # TODO: add more code here for LookbackMultipleUtils methods.
    # Note: below was copied from planetaryCombinationsLibrary.py.  It has not been adapted yet for LookbackMultiple purposes..

    @staticmethod
    def _getDatetimesOfElapsedLongitudeDegrees(\
        pcdd, 
        planetName, 
        centricityType,
        longitudeType,
        planetEpocDt,
        desiredDegreesElapsed,
        maxErrorTd=datetime.timedelta(seconds=2)):
        """Returns a list of datetime.datetime objects that hold the
        timestamps when the given planet is at 'degreeElapsed'
        longitude degrees from the longitude degrees calculated at
        moment 'planetEpocDt'.
        
        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        planetName - str holding the name of the planet to do the
                     calculations for.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        planetEpocDt - datetime.datetime object for the epoc or reference time.
                       The planet longitude at this moment is taken as
                       the zero-point.  Increments are started from
                       this moment in time.
        desiredDegreesElapsed - float value for the number of longitude degrees
                        elapsed from the longitude at 'planetEpocDt'.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        List of datetime.datetime objects.  The datetime.datetime
        objects in this list are the timestamps where the planet is at
        the elapsed number of degrees away from the longitude at
        'planetEpocDt'.
        """
        
        log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = []

        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            log.error("Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig))
            rv = []
            return rv

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            log.error("Invalid input: longitudeType is invalid.  " + \
                      "Value given was: {}".format(longitudeTypeOrig))
            rv = []
            return rv

        # Field name we are getting.
        fieldName = "longitude"
        
        # Initialize the Ephemeris with the birth location.
        log.debug("Setting ephemeris location ...")
        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)

        # Set the step size.  Planet should not ever move more than
        # 120 degrees per step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)

        # Running count of number of full 360-degree circles.
        numFullCircles = 0
        
        # Desired degree.
        desiredDegree = None
        
        # Epoc longitude.
        planetEpocLongitude = None

        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(planetEpocDt))
        steps.append(copy.deepcopy(planetEpocDt))

        longitudesP1 = []
        longitudesP1.append(None)
        longitudesP1.append(None)
        
        def getFieldValue(planetaryInfo, fieldName):
            pi = planetaryInfo
            fieldValue = None
            
            if centricityType == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        log.debug("Stepping through timestamps from {} ...".\
                  format(Ephemeris.datetimeToStr(planetEpocDt)))

        currDiff = None
        prevDiff = None

        # Current and previous number of degrees elapsed.
        currElapsed = None
        
        done = False
        while not done:
        
            currDt = steps[-1]
            prevDt = steps[-2]
            
            log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            if planetEpocLongitude == None:
                planetEpocLongitude = getFieldValue(p1, fieldName)
            
            longitudesP1[-1] = getFieldValue(p1, fieldName)
            
            log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))
            
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - planetEpocLongitude)
            
            log.debug("prevDiff == {}".format(prevDiff))
            log.debug("currDiff == {}".format(currDiff))
            
            if prevDiff != None and longitudesP1[-2] != None:
                
                if prevDiff > 240 and currDiff < 120:
                    log.debug("Crossed over epoc longitude {} ".\
                              format(planetEpocLongitude) + \
                              "from below to above!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1
                    
                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        log.debug("Refining between {} and {}".\
                                  format(Ephemeris.datetimeToStr(t1),
                                         Ephemeris.datetimeToStr(t2)))

                        # Check the timestamp between.
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                        testValueP1 = getFieldValue(p1, fieldName)

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - planetEpocLongitude)

                        if testDiff < 120:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                        else:
                            t1 = testDt

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Increment the number of 360-degree circles traversed.
                    numFullCircles += 1

                elif prevDiff < 120 and currDiff > 240:
                    log.debug("Crossed over epoc longitude {} ".\
                              format(planetEpocLongitude) + \
                              "from above to below!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        log.debug("Refining between {} and {}".\
                                  format(Ephemeris.datetimeToStr(t1),
                                         Ephemeris.datetimeToStr(t2)))

                        # Check the timestamp between.
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)

                        testValueP1 = getFieldValue(p1, fieldName)

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - planetEpocLongitude)

                        if testDiff < 120:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt

                    # Decrement the number of 360-degree circles traversed.
                    numFullCircles -= 1

                # Calculate the total number of degrees elapsed so far.
                currElapsed = (numFullCircles * 360.0) + currDiff

                log.debug("currElapsed == {}".format(currElapsed))
                log.debug("desiredDegreesElapsed == {}".\
                          format(desiredDegreesElapsed))
                
                if currElapsed > desiredDegreesElapsed:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    log.debug("Passed the desired number of " + \
                              "elapsed degrees from below to above.  " + \
                              "Narrowing down to the exact moment in time ...")
                    
                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetEpocLongitude + (desiredDegreesElapsed % 360.0))

                    log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = t2 - t1
                    
                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        log.debug("Refining between {} and {}".\
                                  format(Ephemeris.datetimeToStr(t1),
                                         Ephemeris.datetimeToStr(t2)))

                        # Check the timestamp between.
                        timeWindowTd = t2 - t1
                        halfTimeWindowTd = \
                            datetime.\
                            timedelta(days=(timeWindowTd.days / 2.0),
                                seconds=(timeWindowTd.seconds / 2.0),
                                microseconds=(timeWindowTd.microseconds / 2.0))
                        testDt = t1 + halfTimeWindowTd

                        p1 = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        
                        testValueP1 = getFieldValue(p1, fieldName)

                        testDiff = Util.toNormalizedAngle(\
                            testValueP1 - desiredDegree)
                        
                        if testDiff < 120:
                            t2 = testDt
                        else:
                            t1 = testDt

                        currErrorTd = t2 - t1

                    # t2 holds the moment in time.
                    rv.append(t2)

                    log.debug("First moment in time found to be: {}".\
                              format(Ephemeris.datetimeToStr(t2)))
                              
                    # Now find the the other elapsed points, if they
                    # exist.  We know it doesn't exist if it traverses
                    # more than 120 degrees from desiredDegree.
                    startDt = t2
                    prevDt = startDt
                    currDt = startDt + stepSizeTd
                    p1 = Ephemeris.getPlanetaryInfo(planetName, prevDt)
                    prevDiff = Util.toNormalizedAngle(\
                        getFieldValue(p1, fieldName) - desiredDegree)
                    currDiff = None

                    log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    while prevDiff <= 120 or prevDiff > 240:
                        p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                        currDiff = Util.toNormalizedAngle(\
                            getFieldValue(p1, fieldName) - desiredDegree)

                        log.debug("currDt == {}, ".\
                                  format(Ephemeris.datetimeToStr(currDt)) + 
                                  "longitude == {}, ".\
                                  format(getFieldValue(p1, fieldName)) + \
                                  "currDiff == {}".\
                                  format(currDiff))

                        if prevDiff > 240 and currDiff < 120:
                            log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "below to above.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = t2 - t1
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                log.debug("Refining between {} and {}".\
                                          format(Ephemeris.datetimeToStr(t1),
                                                 Ephemeris.datetimeToStr(t2)))
                                
                                # Check the timestamp between.
                                timeWindowTd = t2 - t1
                                halfTimeWindowTd = \
                                    datetime.\
                                    timedelta(days=(timeWindowTd.days / 2.0),
                                        seconds=(timeWindowTd.seconds / 2.0),
                                        microseconds=\
                                              (timeWindowTd.microseconds / 2.0))
                                testDt = t1 + halfTimeWindowTd
        
                                p1 = Ephemeris.getPlanetaryInfo(\
                                    planetName, testDt)
                                
                                testValueP1 = getFieldValue(p1, fieldName)
        
                                testDiff = Util.toNormalizedAngle(\
                                    testValueP1 - desiredDegree)
                                
                                if testDiff < 120:
                                    t2 = testDt

                                    currDt = t2
                                    currDiff = testDiff
                                else:
                                    t1 = testDt
        
                                currErrorTd = t2 - t1


                            # currDt holds the moment in time.
                            log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        elif prevDiff < 120 and currDiff > 240:
                            log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "above to below.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = t2 - t1
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                log.debug("Refining between {} and {}".\
                                          format(Ephemeris.datetimeToStr(t1),
                                                 Ephemeris.datetimeToStr(t2)))
                                
                                # Check the timestamp between.
                                timeWindowTd = t2 - t1
                                halfTimeWindowTd = \
                                    datetime.\
                                    timedelta(days=(timeWindowTd.days / 2.0),
                                        seconds=(timeWindowTd.seconds / 2.0),
                                        microseconds=\
                                              (timeWindowTd.microseconds / 2.0))
                                testDt = t1 + halfTimeWindowTd
        
                                p1 = Ephemeris.getPlanetaryInfo(\
                                    planetName, testDt)
                                
                                testValueP1 = getFieldValue(p1, fieldName)
        
                                testDiff = Util.toNormalizedAngle(\
                                    testValueP1 - desiredDegree)
                                
                                if testDiff > 240:
                                    t2 = testDt

                                    currDt = t2
                                    currDiff = testDiff
                                else:
                                    t1 = testDt
        
                                currErrorTd = t2 - t1
        
                            # currDt holds the moment in time.
                            log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        prevDt = currDt
                        currDt = copy.deepcopy(currDt) + stepSizeTd
                        prevDiff = currDiff
                        currDiff = None

                    log.debug("Done searching for timestamps.")
                        
                    # We have our timestamps, so we are done.
                    done = True
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]

            # Update prevDiff as the currDiff.
            prevDiff = currDiff

        log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    

class LookbackMultiplePanelWidget(QWidget):
    """Widget holding the QTableView that displays the PriceBar 
    information along with other metrics analysis information.
    """

    # Signal emitted when the LookbackMultiples are modified by the user,
    # either by checking a LookbackMultiple to be enabled, or by
    # double-clicking and editing the particular LookbackMultiple in the list.
    # Loading a new list of LookbackMultiples does not trigger this signal.
    lookbackMultiplesModified = QtCore.pyqtSignal(list)

    # Signal emitted when the "Apply/Redraw Lookback Multiples" button is
    # clicked within this widget.
    applyRedrawLookbackMultiplesButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("lookbackmultiple.LookbackMultiplePanelWidget")

        # Member variables.

        # Holds the reference to the list of lookback multiples.
        self.lookbackMultiples = []

        self.applyRedrawButton = QPushButton("Apply/Redraw Lookback Multiples")

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        
        self.tableWidgetHeaderItem = QTableWidgetItem("Lookback Multiples")
        column = 0
        self.tableWidget.setHorizontalHeaderItem(column, 
                                                 self.tableWidgetHeaderItem)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.applyRedrawButton)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        # Connect signals and slots.
        self.applyRedrawButton.clicked.\
            connect(self.applyRedrawLookbackMultiplesButtonClicked)
        self.tableWidget.itemChanged.\
          connect(self._handleItemChanged)
        self.tableWidget.itemDoubleClicked.\
          connect(self._handleItemDoubleClicked)
        
        self.log.debug("size is: w={},h={}".\
                       format(self.size().width(), 
                              self.size().height()))
        self.log.debug("sizeHint is: w={},h={}".\
                       format(self.sizeHint().width(), 
                              self.sizeHint().height()))

    def getLookbackMultiples(self):
        """Returns the reference to the list of LookbackMultiple objects."""
        
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug("Entered getLookbackMultiples()")

            self.log.debug("len(self.lookbackMultiples) is currently: {}".\
                           format(len(self.lookbackMultiples)))

            self.log.debug("self.lookbackMultiples is currently: ".\
                           format(self.lookbackMultiples))

            for i in range(len(self.lookbackMultiples)):
                lm = self.lookbackMultiples[i]
                self.log.debug("self.lookbackMultiples[{}] is: {}".\
                               format(i, lm.toString()))

            self.log.debug("Exiting getLookbackMultiples()")

        return self.lookbackMultiples


    def setLookbackMultiples(self, lookbackMultiples):
        """Sets the given list of LookbackMultiple objects to be
        visualized in this widget.  This widget can potentially modify
        the LookbackMultiple objects within this list.
        """

        self.log.debug("Entered setLookbackMultiples(lookbackMultiples)")

        if lookbackMultiples == None:
            self.log.error("Error: Invalid arguments.  " + \
                           "lookbackMultiples to load cannot be None.")
            self.log.debug("Exiting loadLookackMultiples(lookbackMultiples)")
            return


        # Here we will disconnect the signal-to-slot for handling when an item
        # is changed.  We will reconnect it at the end of this method after we
        # have made our modifications and created/modified the
        # QTableWidgetItems within the QTableWidget.
        # 
        # Reason: This is because we don't want the signal to propagate
        # upwards to indicate a real change has occured via user interaction
        # from just loading.  
        self.tableWidget.itemChanged.disconnect(self._handleItemChanged)

        self.log.debug("Old lookbackMultiples has length: {}".\
                       format(len(self.lookbackMultiples)))
        self.log.debug("New lookbackMultiples has length: {}".\
                       format(len(lookbackMultiples)))
        self.log.debug("Before setting new lookbackMultiples, " + 
                       "the number of rows is: {}".\
                       format(self.tableWidget.rowCount()))
     
        # Store a reference to the new LookbackMultiples.
        self.lookbackMultiples = lookbackMultiples

        # Update the row count.
        if self.tableWidget.rowCount() != len(self.lookbackMultiples):
            self.tableWidget.setRowCount(len(self.lookbackMultiples))
        
        for i in range(len(self.lookbackMultiples)):
            lookbackMultiple = lookbackMultiples[i]
            row = i
            column = 0
            
            # Get the existing item at the current row and column.  
            # If it doesn't exist, then create it.
            item = self.tableWidget.item(row, column)
            if item == None:
                self.log.debug("Item at (row={}, col={})".\
                               format(row, column) + \
                               " was None, so creating it now.")
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, column, item)

            # Set the internals of the QTableWidgetItem to reflect the
            # LookbackMultiple that it represents.
            if lookbackMultiple.getEnabled():
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
                
            item.setIcon(ColorIcon(lookbackMultiple.getColor()))
            item.setText(lookbackMultiple.toShortString())
            item.setToolTip(\
                self._getToolTipTextTextForLookbackMultiple(lookbackMultiple))
            
        # Reconnect the signal-to-slot, so that user changes to the items will
        # notify us so we can update the internal LookbackMultiple variable(s), 
        # and take any other necessary actions.
        self.tableWidget.itemChanged.connect(self._handleItemChanged)

        self.log.debug("Exiting setLookbackMultiples(lookbackMultiples)")

    
    def _handleItemChanged(self, item):
        """Slot that handles when a QTableWidgetItem changes.
        An example of a change that this handles is the item's check state.
        
        Arguments:
        item - QTableWidgetItem that is sent via Qt's signal to this slot.
        """
        
        self.log.debug("Entered _handleItemChanged(item)")

        self.log.debug("Item changed at (row={}, col={})".\
                       format(item.row(), item.column()))

        # Currently, the only kinds of changes supported are checking the
        # item's state, which will cause the enable state of the underlying
        # LookbackMultiple to be updated.  The other way is to double-click the
        # item to edit it manually, which another method handles this case.
        row = item.row()
        enabledFlag = item.checkState() == Qt.Checked
        if self.lookbackMultiples[row].getEnabled() != enabledFlag:
            self.log.debug("Checkstate was changed to {}.".format(enabledFlag))
            self.lookbackMultiples[row].setEnabled(enabledFlag)

            # Emit that there were modifications to the LoobkackMultiples.
            self.lookbackMultiplesModified.emit(self.lookbackMultiples)
        
        self.log.debug("Exiting _handleItemChanged(item)")
        
    def _handleItemDoubleClicked(self, item):
        """Slot that handles when a QTableWidgetItem is double-clicked.
        This will open up an edit dialog to edit the underlying
        LookbackMultiple.

        Arguments:
        item - QTableWidgetItem that is sent via Qt's signal to this slot.
        """
        
        self.log.debug("Entered _handleItemDoubleClicked(item)")
        
        self.log.debug("Item double-clicked at (row={}, col={})".\
                       format(item.row(), item.column()))
                       
        # Get the LookbackMultiple that underlies this QTableWidgetItem that
        # was double-clicked.
        row = item.row()
        lookbackMultiple = self.lookbackMultiples[row]
        
        # Create a dialog to edit this LookbackMultiple.
        dialog = LookbackMultipleEditDialog(lookbackMultiple)
        
        rv = dialog.exec_()
        if rv == QDialog.Accepted:
            # Dialog was accepted.  Obtain and store the new LookbackMultiple.
            self.log.debug("Edit dialog for the LookbackMultiple was accepted.")
            self.log.debug("Storing new LookbackMultiple back into the list.")

            self.lookbackMultiples[row] = dialog.getLookbackMultiple()
            lookbackMultiple = self.lookbackMultiples[row]

            # Reload the current QTableWidgetItem so that it displays updated
            # information.
            # 
            # (Here we will disconnect the itemChanged signal and then after
            # updates, reconnect it).
            self.tableWidget.itemChanged.disconnect(self._handleItemChanged)

            if lookbackMultiple.getEnabled():
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            item.setIcon(ColorIcon(lookbackMultiple.getColor()))
            item.setText(lookbackMultiple.toShortString())
            item.setToolTip(\
                self._getToolTipTextTextForLookbackMultiple(lookbackMultiple))

            self.tableWidget.itemChanged.connect(self._handleItemChanged)


            # Emit that there were modifications to the LookbackMultiples.
            self.lookbackMultiplesModified.emit(self.lookbackMultiples)
        else:
            self.log.debug("Edit dialog for the LookbackMultiple was rejected.")
        
        self.log.debug("Exiting _handleItemDoubleClicked(item)")
        
    def _getToolTipTextTextForLookbackMultiple(self, lookbackMultiple):
        """Returns a formatted string to use for the tooltip."""
        
        lm = lookbackMultiple
        
        # Newlines.
        endl = os.linesep

        # Assemble substrings used within the final string.
        centricityTypeStr = ""
        if lm.getGeocentricFlag() == True:
            centricityTypeStr = "G."
        if lm.getHeliocentricFlag() == True:
            centricityTypeStr = "H."
            
        planetNameStr = lm.getPlanetName()
        lookbackMultipleStr = "{}".format(lm.getLookbackMultiple())
        
        baseUnitStr = "{}".format(lm.getBaseUnit())

        baseUnitTypeStr = ""
        if lm.getBaseUnitTypeDegreesFlag() == True:
            baseUnitTypeStr = "degrees"
        if lm.getBaseUnitTypeRevolutionsFlag() == True:
            baseUnitTypeStr = "revolutions"

        # Build the final string used for the tooltip.
        formattedText = ""
        formattedText += "Name: {}".format(lm.getName()) + endl
        formattedText += "Enabled: {}".format(lm.getEnabled()) + endl
        formattedText += \
            "Summary: {}{} {} x {} {}".\
            format(centricityTypeStr, 
                   planetNameStr, 
                   lookbackMultipleStr, 
                   baseUnitStr, 
                   baseUnitTypeStr) + endl
        formattedText += "Description: {}".format(lm.getDescription())

        return formattedText



##############################################################################

def testLookbackMultiplePanelWidget():
    print("Running " + inspect.stack()[0][3] + "()")
    
    lm1 = LookbackMultiple(name="49ers",
                          description="MyDescription1",
                          lookbackMultiple=1.0,
                          baseUnit=49.0,
                          baseUnitTypeDegreesFlag=False,
                          baseUnitTypeRevolutionsFlag=True,
                          color=QColor(Qt.gray),
                          enabled=False,
                          planetName="Ascendant",
                          geocentricFlag=True,
                          heliocentricFlag=False)

    lm2 = LookbackMultiple(name="40 deg Earth",
                          description="MyDescription2",
                          lookbackMultiple=1.0,
                          baseUnit=40.0,
                          baseUnitTypeDegreesFlag=True,
                          baseUnitTypeRevolutionsFlag=False,
                          color=QColor(Qt.red),
                          enabled=True,
                          planetName="Earth",
                          geocentricFlag=False,
                          heliocentricFlag=True)

    lm3 = LookbackMultiple(name="360 deg Moon",
                          description="MyDescription3",
                          lookbackMultiple=1.0,
                          baseUnit=360.0,
                          baseUnitTypeDegreesFlag=True,
                          baseUnitTypeRevolutionsFlag=False,
                          color=QColor(Qt.blue),
                          enabled=True,
                          planetName="Moon",
                          geocentricFlag=True,
                          heliocentricFlag=False)

    lm4 = LookbackMultiple(name="360 deg G.MoSu",
                          description="MyDescription4",
                          lookbackMultiple=1.0,
                          baseUnit=360.0,
                          baseUnitTypeDegreesFlag=True,
                          baseUnitTypeRevolutionsFlag=False,
                          color=QColor(Qt.black),
                          enabled=True,
                          planetName="MoSu",
                          geocentricFlag=True,
                          heliocentricFlag=False)

    lookbackMultiples = [lm1, lm2, lm3, lm4]

    widget = LookbackMultiplePanelWidget()
    widget.setLookbackMultiples(lookbackMultiples)

    layout = QVBoxLayout()
    layout.addWidget(widget)
    
    dialog = QDialog()
    dialog.setLayout(layout)
    rv = dialog.exec_()


def testLookbackMultiplePanelWidgetEmpty():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Just display the panel widget without any LookbackMultiples.
    # This is to get an idea about the minimum/default sizes of the widget.
    
    lookbackMultiples = []

    widget = LookbackMultiplePanelWidget()
    #widget.setLookbackMultiples(lookbackMultiples)

    layout = QVBoxLayout()
    layout.addWidget(widget)
    
    dialog = QDialog()
    dialog.setLayout(layout)
    rv = dialog.exec_()

    

##############################################################################

# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect

    # For logging and for exiting.
    import os
    import sys
    
    # Initialize the Ephemeris (required).
    #Ephemeris.initialize()

    # Set a default location (required).
    #Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)


    # Various tests to run:
    testLookbackMultiplePanelWidget()
    testLookbackMultiplePanelWidgetEmpty()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    #app.exec_()

    # Quit.
    print("Exiting.")
    sys.exit()

##############################################################################
