

# For logging.
import logging

# For newlines.
import os

# For printing out the current method's name.
import inspect

# For copy.deepcopy.
import copy

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

from data_objects import Util
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
    
    @staticmethod
    def getDatetimesOfLongitudeDeltaDegreesInFuture(\
        planetName, 
        centricityType,
        longitudeType,
        referenceDt,
        desiredDeltaDegrees,
        maxErrorTd=datetime.timedelta(seconds=2)):
        """Returns a list of datetime.datetime objects that hold the
        timestamps when the given planet is at 'desiredDeltaDegrees'
        longitude degrees from the longitude degrees calculated at
        moment 'referenceDt'.  Since this method looks in the future, 
        the 'desiredDeltaDegrees' value needs to be positive.

        Returns:
        list of datetime.datetime objects, ordered chronologically 
        from oldest to latest, of the timestamps when the planet 
        is 'desiredDeltaDegrees' distance relative to the 
        planet's longitude position at the reference datetime.datetime.
        
        Pre-requisites:
        This method assumes that the user has initialized the Ephemeris 
        and has called Ephemeris.setGeographicPosition() prior to running
        this method.

        Arguments:
        planetName - str holding the name of the planet to do the
                     calculations for.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        referenceDt - datetime.datetime object for the reference time.
                      The planet longitude at this moment is taken as
                      the zero-point.  Increments or decrements in time 
                      are started from this moment in time.
        desiredDeltaDegrees - float value for the number of longitude degrees
                        elapsed from the longitude at 'referenceDt'.
                        This parameter must be a positive value.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        List of datetime.datetime objects.  The datetime.datetime
        objects in this list are the timestamps where the planet is at
        the elapsed number of degrees away from the longitude at
        'referenceDt'.
        """
        
        LookbackMultipleUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = []

        # Verify inputs.
        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            errMsg = "Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig)
            LookbackMultipleUtils.log.error(errMsg)
            raise ValueError(errMsg)

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            errMsg = "Invalid input: longitudeType is invalid.  " + \
                      "Value given was: {}".format(longitudeTypeOrig)
            LookbackMultipleUtils.log.error(errMsg)
            raise ValueError(errMsg)

        if desiredDeltaDegrees < 0:
            errMsg = "Invalid input: " + \
                      "desiredDeltaDegrees must be a positive value.  " + \
                      "Value given was: {}".format(desiredDeltaDegrees)
            LookbackMultipleUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Field name we are getting.
        fieldName = "longitude"

        # Step size timedelta.  
        stepSizeTd = \
            LookbackMultipleUtils._getOptimalStepSizeTd(centricityType, 
                                                        planetName)
        
        # Running count of number of full 360-degree circles.
        numFullCircles = 0
        
        # Desired degree.
        desiredDegree = None
        
        # Longitude of the planet at datetime referenceDt.
        planetReferenceLongitude = None

        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(referenceDt))
        steps.append(copy.deepcopy(referenceDt))

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
                LookbackMultipleUtils.log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        LookbackMultipleUtils.log.debug("Stepping through timestamps from {} ...".\
                  format(Ephemeris.datetimeToStr(referenceDt)))

        currDiff = None
        prevDiff = None

        # Current and previous number of degrees elapsed.
        currElapsed = None
        
        done = False
        while not done:
        
            currDt = steps[-1]
            prevDt = steps[-2]
            
            LookbackMultipleUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            if planetReferenceLongitude == None:
                planetReferenceLongitude = getFieldValue(p1, fieldName)
                LookbackMultipleUtils.log.debug("planetReferenceLongitude == {}".\
                                                format(planetReferenceLongitude))
            
            longitudesP1[-1] = getFieldValue(p1, fieldName)
            
            LookbackMultipleUtils.log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))
            
            # Calculate the difference in planet longitudes between the current
            # datetime and the referenceDt.  
            # (This value will be in the range [0, 360) ).
            #
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - planetReferenceLongitude)
            
            LookbackMultipleUtils.log.debug("prevDiff == {}".format(prevDiff))
            LookbackMultipleUtils.log.debug("currDiff == {}".format(currDiff))
            
            # If this is not the first iteration of the loop 
            # (i.e. we have both a prevDiff and a currDiff to compare).
            if prevDiff != None and longitudesP1[-2] != None:
                
                if prevDiff > 240 and currDiff < 120:
                    LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from below to above!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)
                    
                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
                            testValueP1 - planetReferenceLongitude)

                        if testDiff < 120:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                        else:
                            t1 = testDt

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our lists.
                    steps[-1] = currDt

                    # Increment the number of 360-degree circles traversed.
                    numFullCircles += 1

                elif prevDiff < 120 and currDiff > 240:
                    LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from above to below!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
                            testValueP1 - planetReferenceLongitude)

                        if testDiff < 120:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our lists.
                    steps[-1] = currDt

                    # Decrement the number of 360-degree circles traversed.
                    numFullCircles -= 1

                # Calculate the total number of degrees elapsed so far.
                currElapsed = (numFullCircles * 360.0) + currDiff

                LookbackMultipleUtils.log.debug("currElapsed == {}".format(currElapsed))
                LookbackMultipleUtils.log.debug("desiredDeltaDegrees == {}".\
                          format(desiredDeltaDegrees))
                
                if currElapsed > desiredDeltaDegrees:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                              "elapsed degrees from below to above.  " + \
                              "Narrowing down to the exact moment in time ...")
                    
                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetReferenceLongitude + 
                        (desiredDeltaDegrees % 360.0))

                    LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = Util.absTd(t2 - t1)
                    
                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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

                        currErrorTd = Util.absTd(t2 - t1)

                    # t2 holds the moment in time.
                    rv.append(t2)

                    LookbackMultipleUtils.log.debug("First moment in time found to be: {}".\
                              format(Ephemeris.datetimeToStr(t2)))

                    # Now we will want to find the other elapsed points, if they
                    # exist.  We know it doesn't exist if it traverses
                    # more than 120 degrees from desiredDegree.
                    startDt = t2
                    prevDt = startDt
                    currDt = startDt + stepSizeTd
                    p1 = Ephemeris.getPlanetaryInfo(planetName, prevDt)
                    prevDiff = Util.toNormalizedAngle(\
                        getFieldValue(p1, fieldName) - desiredDegree)
                    currDiff = None

                    LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    # There is only need to continue looking for more potential
                    # timestamps if the planet can go retrograde.  Direct-only
                    # planets will yield only 1 timestamp, and we have found it
                    # already.
                    if centricityType == "heliocentric" or \
                        (centricityType == "geocentric" and \
                         (planetName == "Sun" or
                          planetName == "Moon" or
                          planetName == "MoSu")):
                         
                         LookbackMultipleUtils.log.debug(\
                             "No need to look for anymore timestamps " + \
                             "because this planet doesn't go retrograde.")

                         # Set the done flag, which will stop us from looking
                         # for more timestamps.
                         done = True
                    
                    while (prevDiff <= 120 or prevDiff > 240) and done != True:

                        p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                        currDiff = Util.toNormalizedAngle(\
                            getFieldValue(p1, fieldName) - desiredDegree)

                        LookbackMultipleUtils.log.debug("currDt == {}, ".\
                                  format(Ephemeris.datetimeToStr(currDt)) + 
                                  "longitude == {}, ".\
                                  format(getFieldValue(p1, fieldName)) + \
                                  "currDiff == {}".\
                                  format(currDiff))

                        if prevDiff > 240 and currDiff < 120:
                            LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "below to above.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = Util.absTd(t2 - t1)
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
        
                                currErrorTd = Util.absTd(t2 - t1)


                            # currDt holds the moment in time.
                            LookbackMultipleUtils.log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        elif prevDiff < 120 and currDiff > 240:
                            LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "above to below.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = Util.absTd(t2 - t1)
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
        
                                currErrorTd = Util.absTd(t2 - t1)
        
                            # currDt holds the moment in time.
                            LookbackMultipleUtils.log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        prevDt = currDt
                        currDt = copy.deepcopy(currDt) + stepSizeTd
                        prevDiff = currDiff
                        currDiff = None

                    LookbackMultipleUtils.log.debug("Done searching for timestamps.")
                        
                    # We have our timestamps, so we are done.
                    done = True
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]

            # Update prevDiff as the currDiff.
            prevDiff = currDiff

        LookbackMultipleUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

        
    @staticmethod
    def getDatetimesOfLongitudeDeltaDegreesInPast(\
        planetName, 
        centricityType,
        longitudeType,
        referenceDt,
        desiredDeltaDegrees,
        maxErrorTd=datetime.timedelta(seconds=2)):
        """Returns a list of datetime.datetime objects that hold the
        timestamps when the given planet is at 'desiredDeltaDegrees'
        longitude degrees from the longitude degrees calculated at
        moment 'referenceDt'.  Since this method looks in the past, 
        the 'desiredDeltaDegrees' value needs to be negative.

        Returns:
        list of datetime.datetime objects, ordered chronologically 
        from oldest to latest, of the timestamps when the planet 
        is 'desiredDeltaDegrees' distance relative to the 
        planet's longitude position at the reference datetime.datetime.
        
        Pre-requisites:
        This method assumes that the user has initialized the Ephemeris 
        and has called Ephemeris.setGeographicPosition() prior to running
        this method.

        Arguments:
        planetName - str holding the name of the planet to do the
                     calculations for.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        referenceDt - datetime.datetime object for the reference time.
                      The planet longitude at this moment is taken as
                      the zero-point.  Increments or decrements in time 
                      are started from this moment in time.
        desiredDeltaDegrees - float value for the number of longitude degrees
                        elapsed from the longitude at 'referenceDt'.
                        This parameter must be a negative value.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.  
        
        Returns:
        List of datetime.datetime objects.  The datetime.datetime
        objects in this list are the timestamps where the planet is at
        the elapsed number of degrees away from the longitude at
        'referenceDt'.
        """
        
        LookbackMultipleUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = []

        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            errMsg = "Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig)
            LookbackMultipleUtils.log.error(errMsg)
            raise ValueError(errMsg)

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            errMsg = "Invalid input: longitudeType is invalid.  " + \
                      "Value given was: {}".format(longitudeTypeOrig)
            LookbackMultipleUtils.log.error(errMsg)
            raise ValueError(errMsg)

        if desiredDeltaDegrees > 0:
            errMsg = "Invalid input: " + \
                      "desiredDeltaDegrees must be a negative value.  " + \
                      "Value given was: {}".format(desiredDeltaDegrees)
            LookbackMultipleUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Field name we are getting.
        fieldName = "longitude"

        # Step size timedelta.  
        stepSizeTd = \
            LookbackMultipleUtils._getOptimalStepSizeTd(centricityType, 
                                                        planetName)
        
        # Invert the step size if desiredDeltaDegrees is zero or negative.
        if desiredDeltaDegrees <= 0:
            stepSizeTd = stepSizeTd * -1

        # Running count of number of full 360-degree circles.
        numFullCircles = 0
        
        # Desired degree.
        desiredDegree = None
        
        # Longitude of the planet at datetime referenceDt.
        planetReferenceLongitude = None

        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(referenceDt))
        steps.append(copy.deepcopy(referenceDt))

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
                LookbackMultipleUtils.log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue
            
        LookbackMultipleUtils.log.debug("Stepping through timestamps from {} ...".\
                  format(Ephemeris.datetimeToStr(referenceDt)))

        currDiff = None
        prevDiff = None

        # Current and previous number of degrees elapsed.
        currElapsed = None
        
        done = False
        while not done:
        
            currDt = steps[-1]
            prevDt = steps[-2]
            
            LookbackMultipleUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            if planetReferenceLongitude == None:
                planetReferenceLongitude = getFieldValue(p1, fieldName)
                LookbackMultipleUtils.log.debug("planetReferenceLongitude == {}".\
                                                format(planetReferenceLongitude))

            longitudesP1[-1] = getFieldValue(p1, fieldName)
            
            LookbackMultipleUtils.log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))
            
            # Calculate the difference in planet longitudes between the current
            # datetime and the referenceDt.  
            # (This value will be in the range [0, 360) ).
            #
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - planetReferenceLongitude)

            LookbackMultipleUtils.log.debug("prevDiff == {}".format(prevDiff))
            LookbackMultipleUtils.log.debug("currDiff == {}".format(currDiff))
            
            # If this is not the first iteration of the loop 
            # (i.e. we have both a prevDiff and a currDiff to compare).
            if prevDiff != None and longitudesP1[-2] != None:
                
                if prevDiff > 240 and currDiff < 120:
                    LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from below to above!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)
                    
                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
                            testValueP1 - planetReferenceLongitude)

                        if testDiff < 120:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff
                        else:
                            t1 = testDt

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our lists.
                    steps[-1] = currDt

                    # Increment the number of 360-degree circles traversed.
                    numFullCircles += 1

                elif prevDiff < 120 and currDiff > 240:
                    LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from above to below!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
                            testValueP1 - planetReferenceLongitude)

                        if testDiff < 120:
                            t1 = testDt
                        else:
                            t2 = testDt
                            
                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                            LookbackMultipleUtils.log.debug("currDiff updated to: {}".format(currDiff))

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our lists.
                    steps[-1] = currDt

                    # Decrement the number of 360-degree circles traversed.
                    numFullCircles -= 1

                # Calculate the total number of degrees elapsed so far.
                currElapsed = (numFullCircles * 360.0) + currDiff

                LookbackMultipleUtils.log.debug("currElapsed == {}".format(currElapsed))
                LookbackMultipleUtils.log.debug("desiredDeltaDegrees == {}".\
                          format(desiredDeltaDegrees))
                
                if currElapsed < desiredDeltaDegrees:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                              "elapsed degrees from above to below.  " + \
                              "Narrowing down to the exact moment in time ...")
                    
                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetReferenceLongitude + 
                        (desiredDeltaDegrees % 360.0))

                    LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = Util.absTd(t2 - t1)
                    
                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
                        
                        if testDiff > 240:
                            t2 = testDt
                        else:
                            t1 = testDt

                        currErrorTd = Util.absTd(t2 - t1)

                    # t2 holds the moment in time.
                    rv.append(t2)

                    LookbackMultipleUtils.log.debug("First moment in time found to be: {}".\
                              format(Ephemeris.datetimeToStr(t2)))

                    # Now we will want to find the other elapsed points, if they
                    # exist.  We know it doesn't exist if it traverses
                    # more than 120 degrees from desiredDegree.
                    startDt = t2
                    prevDt = startDt
                    currDt = startDt + stepSizeTd
                    p1 = Ephemeris.getPlanetaryInfo(planetName, prevDt)
                    prevDiff = Util.toNormalizedAngle(\
                        getFieldValue(p1, fieldName) - desiredDegree)
                    currDiff = None

                    LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))
                    
                    # There is only need to continue looking for more potential
                    # timestamps if the planet can go retrograde.  Direct-only
                    # planets will yield only 1 timestamp, and we have found it
                    # already.
                    if centricityType == "heliocentric" or \
                        (centricityType == "geocentric" and \
                         (planetName == "Sun" or 
                          planetName == "Moon" or 
                          planetName == "MoSu")):
                         
                         LookbackMultipleUtils.log.debug(\
                             "No need to look for anymore timestamps " + \
                             "because this planet doesn't go retrograde.")

                         # Set the done flag, which will stop us from looking
                         # for more timestamps.
                         done = True
                    
                    while (prevDiff >= 240 or prevDiff < 120) and done != True:

                        p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                        currDiff = Util.toNormalizedAngle(\
                            getFieldValue(p1, fieldName) - desiredDegree)

                        LookbackMultipleUtils.log.debug("currDt == {}, ".\
                                  format(Ephemeris.datetimeToStr(currDt)) + 
                                  "longitude == {}, ".\
                                  format(getFieldValue(p1, fieldName)) + \
                                  "currDiff == {}".\
                                  format(currDiff))

                        if prevDiff < 120 and currDiff > 240:
                            LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "below to above.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = Util.absTd(t2 - t1)
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
        
                                currErrorTd = Util.absTd(t2 - t1)


                            # currDt holds the moment in time.
                            LookbackMultipleUtils.log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        elif prevDiff > 240 and currDiff < 120:
                            LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                                      "elapsed degrees from " + \
                                      "above to below.  " + \
                                      "Narrowing down to the exact moment " + \
                                      "in time ...")
                    
                            # This is the upper-bound of the error timedelta.
                            t1 = prevDt
                            t2 = currDt
                            currErrorTd = Util.absTd(t2 - t1)
                            
                            # Refine the timestamp until it is less
                            # than the threshold.
                            while currErrorTd > maxErrorTd:
                                LookbackMultipleUtils.log.debug("Refining between {} and {}".\
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
        
                                currErrorTd = Util.absTd(t2 - t1)
        
                            # currDt holds the moment in time.
                            LookbackMultipleUtils.log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        prevDt = currDt
                        currDt = copy.deepcopy(currDt) + stepSizeTd
                        prevDiff = currDiff
                        currDiff = None

                    LookbackMultipleUtils.log.debug("Done searching for timestamps.")
                        
                    # We have our timestamps, so we are done.
                    done = True
                    
            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]

            # Update prevDiff as the currDiff.
            prevDiff = currDiff

        LookbackMultipleUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")
        
        # The order of the datetimes in the list to be returned should be
        # chronological.  The way we extracted it was from later time to
        # earlier time, so we need to reverse it before returning.
        rv.reverse()
        return rv


    @staticmethod
    def _getOptimalStepSizeTd(centricityType, planetName):
        """Helper function that will try to determine a better step size
        for supporting other methods of LookbackMultipleUtils.
        
        The step size chosen here is dependent on centricityType and planetName.
        """
        
        # This is the default step size.  
        # Planet should not ever move more than 120 degrees per step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Optimize the step size accord to the planet being used.
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=4)

        # These planets don't go retrograde, so we don't have to worry about
        # losing data points if our step size is too big.  We just have to keep
        # the step size to lower than 120 degrees.  Here, I'll just
        # use some overly safe values, because planets move a different speeds
        # due to their elliptical orbits.
        if centricityType == "geocentric":
            if planetName == "Moon":
                stepSizeTd = datetime.timedelta(days=3)
            elif planetName == "MoSu":
                stepSizeTd = datetime.timedelta(days=3)
            elif planetName == "Sun":
                stepSizeTd = datetime.timedelta(days=40)
        elif centricityType == "heliocentric":
            if planetName == "Mercury":
                stepSizeTd = datetime.timedelta(days=3)
            elif planetName == "Venus":
                stepSizeTd = datetime.timedelta(days=10)
            elif planetName == "Earth":
                stepSizeTd = datetime.timedelta(days=40)
            elif planetName == "Mars":
                stepSizeTd = datetime.timedelta(days=60)
            elif planetName == "Jupiter":
                stepSizeTd = datetime.timedelta(days=120)
            elif planetName == "Saturn":
                stepSizeTd = datetime.timedelta(days=180)
            elif planetName == "Uranus":
                stepSizeTd = datetime.timedelta(days=240)
            elif planetName == "Neptune":
                stepSizeTd = datetime.timedelta(days=300)
            elif planetName == "Pluto":
                stepSizeTd = datetime.timedelta(days=400)

        return stepSizeTd


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
        
        longitudeTypeStr = ""
        if lm.getTropicalFlag() == True:
            longitudeTypeStr = "Trop."
        if lm.getSiderealFlag() == True:
            longitudeTypeStr = "Sid."
            
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
            "Summary: {}{} {} {} x {} {}".\
            format(centricityTypeStr, 
                   planetNameStr, 
                   longitudeTypeStr,
                   lookbackMultipleStr, 
                   baseUnitStr, 
                   baseUnitTypeStr) + endl
        formattedText += "Description: {}".format(lm.getDescription())

        return formattedText



##############################################################################

def testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInFuture():
    """Tests planet movements.

    For retrograde planet movements, there are 5 basic test locations, 
    which in the tests will be described as Points A, B, C, D, and E.

    Point A: Planet going direct.
             Longitude location less than retrograde movement location, and 
             less than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
    Point B: Planet going direct.
             Longitude location less than retrograde movement location, and
             greater than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
             This is the first time the planet goes direct, crossing 
             this longitude degree.
    Point C: Planet going retrograde.
             Longitude location less than retrograde movement location, and
             greater than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
    Point D: Planet going direct.
             Longitude location less than retrograde movement location, and
             greater than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
             This is the second time the planet goes direct, crossing 
             this longitude degree.
    Point E: Planet going direct.
             Longitude location greater than retrograde movement location.
    """

    
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Assumes that Ephemeris has been initialized by this point of execution.


    eastern = pytz.timezone('US/Eastern')

    def printDatetimeResults(resultDts, planetName, centricityType, longitudeType, referenceDt, desiredDeltaDegrees):
        print("  Result datetimes for planetName={}, centricityType={}, longitudeType={}, referenceDt={}, desiredDeltaDegrees={} are:".\
              format(planetName, 
                     centricityType, 
                     longitudeType, 
                     referenceDt, 
                     desiredDeltaDegrees))

        print("  Actual    num results == {}".format(len(resultDts)))

        for i in range(len(resultDts)):
            dt = resultDts[i]
            print("  Actual   resultDts[{}] == {}".format(i, dt))


    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Sun moving 3 degrees, not crossing 0 Aries.")
        planetName="Sun"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1983, 10, 25, 19, 34, tzinfo=eastern)
        desiredDeltaDegrees = 3

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
            planetName, centricityType, longitudeType, referenceDt, 
            desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)
        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1983-10-28 19:43:36.123047-04:56")


    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Sun moving 150 degrees, crossing 0 Aries.")
        planetName="Sun"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1983, 10, 25, 19, 34, tzinfo=eastern)
        desiredDeltaDegrees = 150

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1984-03-22 06:15:13.681641-04:56")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Sun moving 510 degrees, crossing 0 Aries.")
        planetName="Sun"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1983, 10, 25, 19, 34, tzinfo=eastern)
        desiredDeltaDegrees = 510

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1985-03-22 12:02:53.752443-04:56")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 360 degrees.  Point A to Points B/C/D.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 5, 10, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 360

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1969-05-05 10:48:05.009766+00:00")
        print("  Expected resultDts[1] == 1969-06-02 06:33:37.089845+00:00")
        print("  Expected resultDts[2] == 1969-06-18 12:00:05.273439+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 10 degrees.  Point B to Points E.  From about 4 Gem to 14 Gem.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1969, 5, 4, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 10

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1969-06-27 19:19:03.457032+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 5 degrees. Point B to Points B/C/D.  From about 4 deg Gem to 9 deg Gem.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1969, 5, 4, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 5

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1969-05-09 12:37:25.166016+00:00")
        print("  Expected resultDts[1] == 1969-05-26 22:51:00.351563+00:00")
        print("  Expected resultDts[2] == 1969-06-23 02:29:24.843751+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 5 degrees. Point B to Points D.  From about 4 deg Gem to 9 deg Gem.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1969, 6, 5, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 5

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1969-06-23 11:22:08.466798+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 5 degrees. Point C to Points D.  From about 4 deg Gem to 9 deg Gem.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1969, 6, 16, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 5

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1969-06-23 10:24:30.410156+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 360 degrees.  Point A to Points B/C/D.  Over an Aries boundary.  From 4 Aries to 4 Aries.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1978, 3, 13, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 360

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1979-03-07 17:51:40.341797+00:00")
        print("  Expected resultDts[1] == 1979-03-22 23:18:08.525391+00:00")
        print("  Expected resultDts[2] == 1979-04-22 17:11:26.425782+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 20 degrees.  Point B to Points E.  From about 27 Pisces to 17 Aries.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1979, 3, 2, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 20
        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultsDt[0] == 1979-05-02 17:28:46.611329+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 10 degrees.  Point B to Points B/C/D.  From about 27 Pisces to 7 Aries.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1979, 3, 2, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 10

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1979-03-10 17:36:09.580079+00:00")
        print("  Expected resultDts[1] == 1979-03-19 12:57:09.052735+00:00")
        print("  Expected resultDts[2] == 1979-04-24 23:16:49.423829+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 10 degrees. Point B to Points D.  From about 27 deg Pisces to 7 deg Aries.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1979, 4, 1, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 10

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1979-04-25 06:17:36.005860+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 10 degrees. Point C to Points D.  From about 27 deg Pisces to 7 deg Aries.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1979, 4, 14, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 10

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1979-04-25 09:26:57.626954+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Moon moving 22 rev. Point A to Point E.  From about 0 Taurus to 0 Taurus.")
        planetName="Moon"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1979, 5, 23, 12, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 360 * 22

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1981-01-13 22:23:20.537117+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing H.Venus moving 22 rev. Point A to Point E.  From about 18 Aries to 18 Aries.")
        planetName="Venus"
        centricityType="heliocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1981, 4, 8, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 360 * 22

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1994-10-20 07:06:05.625006+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mars moving invalid input: negative degrees.")
        planetName="Mars"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -50

        exceptionThrownFlag = False
        try: 
            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                    planetName, centricityType, longitudeType, referenceDt, 
                    desiredDeltaDegrees)

            printDatetimeResults(resultDts, planetName, centricityType, 
                                 longitudeType, referenceDt, desiredDeltaDegrees)
        except ValueError as e:
            exceptionThrownFlag = True

        if exceptionThrownFlag == False:
            print("  Test Failure: Exception was not thrown as expected.")
        else:
            print("  Test Success: Exception was thrown as expected.")
                

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mars moving 0 degrees into the future.")
        planetName="Mars"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1994-10-20 00:00:01.318360+00:00")


    print("")


def testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInPast():
    """Tests planet movements.

    For retrograde planet movements, there are 5 basic test locations, 
    which in the tests will be described as Points A, B, C, D, and E.

    Point A: Planet going direct.
             Longitude location less than retrograde movement location, and 
             less than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
    Point B: Planet going direct.
             Longitude location less than retrograde movement location, and
             greater than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
             This is the first time the planet goes direct, crossing 
             this longitude degree.
    Point C: Planet going retrograde.
             Longitude location less than retrograde movement location, and
             greater than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
    Point D: Planet going direct.
             Longitude location less than retrograde movement location, and
             greater than the longitude location of the direct movement 
             that follows in time after the retrograde movement.  
             This is the second time the planet goes direct, crossing 
             this longitude degree.
    Point E: Planet going direct.
             Longitude location greater than retrograde movement location.
    """

    
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Assumes that Ephemeris has been initialized by this point of execution.


    eastern = pytz.timezone('US/Eastern')

    def printDatetimeResults(resultDts, planetName, centricityType, longitudeType, referenceDt, desiredDeltaDegrees):
        print("  Result datetimes for planetName={}, centricityType={}, longitudeType={}, referenceDt={}, desiredDeltaDegrees={} are:".\
              format(planetName, 
                     centricityType, 
                     longitudeType, 
                     referenceDt, 
                     desiredDeltaDegrees))

        print("  Actual    num results == {}".format(len(resultDts)))

        for i in range(len(resultDts)):
            dt = resultDts[i]
            print("  Actual   resultDts[{}] == {}".format(i, dt))


    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Sun moving -3 degrees, not crossing 0 Aries.")
        planetName="Sun"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1983, 10, 25, 19, 34, tzinfo=eastern)
        desiredDeltaDegrees = -3

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
            planetName, centricityType, longitudeType, referenceDt, 
            desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)
        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1983-10-22 19:16:21.027832-04:56")


    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Sun moving -150 degrees, crossing 0 Aries.")
        planetName="Sun"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1983, 10, 25, 19, 34, tzinfo=eastern)
        desiredDeltaDegrees = -150

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1983-05-23 12:32:07.500000-04:56")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Sun moving -510 degrees, crossing 0 Aries.")
        planetName="Sun"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1983, 10, 25, 19, 34, tzinfo=eastern)
        desiredDeltaDegrees = -510

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1982-05-23 06:46:31.354980-04:56")


    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -360 degrees.  Point E to Points B/C/D.  28 Libra to 28 Libra.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1969, 11, 1, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -360

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1968-09-26 13:28:07.939452+00:00")
        print("  Expected resultDts[1] == 1968-10-09 15:01:36.240233+00:00")
        print("  Expected resultDts[2] == 1968-11-07 16:05:41.894530+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -5 degrees.  3 Scorp to 28 Libra.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 11, 11, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -5

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1968-09-26 14:21:50.009764+00:00")
        print("  Expected resultDts[1] == 1968-10-09 14:18:25.664061+00:00")
        print("  Expected resultDts[2] == 1968-11-07 16:29:03.310546+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -5 degrees.  Retrograde 26 Libra to 21 Libra direct.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 10, 12, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -5

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1968-09-18 07:05:23.437499+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -5 degrees.  Direct 26 Libra to 21 Libra direct.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 9, 23, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -5

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1968-09-17 20:48:15.996093+00:00")


    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Moon moving 22 rev. Point E to Point A.  From about 0 Taurus to 0 Taurus.")
        planetName="Moon"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1981, 1, 13, 22, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -360 * 22

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1979-05-23 11:35:54.638665+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing H.Venus moving 22 rev. Point E to Point A.  From about 18 Aries to 18 Aries.")
        planetName="Venus"
        centricityType="heliocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -360 * 22

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1981-04-07 16:53:55.922122+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mars moving invalid input: positive degrees.")
        planetName="Mars"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 50

        exceptionThrownFlag = False
        try: 
            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt, 
                    desiredDeltaDegrees)
    
            printDatetimeResults(resultDts, planetName, centricityType, 
                                 longitudeType, referenceDt, desiredDeltaDegrees)
        except ValueError as e:
            exceptionThrownFlag = True

        if exceptionThrownFlag == False:
            print("  Test Failure: Exception was not thrown as expected.")
        else:
            print("  Test Success: Exception was thrown as expected.")
                

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mars moving 0 degrees into the past.")
        planetName="Mars"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt, 
                desiredDeltaDegrees)
    
        printDatetimeResults(resultDts, planetName, centricityType, 
                             longitudeType, referenceDt, desiredDeltaDegrees)
                
        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1994-10-19 23:59:58.681640+00:00")


    print("")


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
                          heliocentricFlag=False,
                          tropicalFlag=True,
                          siderealFlag=False)

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
                          heliocentricFlag=True,
                          tropicalFlag=True,
                          siderealFlag=False)

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
                          heliocentricFlag=False,
                          tropicalFlag=True,
                          siderealFlag=False)

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
                          heliocentricFlag=False,
                          tropicalFlag=True,
                          siderealFlag=False)

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
    Ephemeris.initialize()

    # New York City:
    lon = -74.0064
    lat = 40.7142
    
    # Set a default location (required).
    Ephemeris.setGeographicPosition(lon, lat)

    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)


    # Various tests to run:
    testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInFuture()
    testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInPast()
    #testLookbackMultiplePanelWidget()
    #testLookbackMultiplePanelWidgetEmpty()

    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    #app.exec_()

    # Quit.
    print("Exiting.")
    sys.exit()

##############################################################################
