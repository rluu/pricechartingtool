
# For directory access.
import inspect

# For collections.deque.
import collections

# For timestamps and timezone information.
import datetime
import pytz

# For logging.
import logging
import logging.config

# Import the Ephemeris classes.
from ephemeris import PlanetaryInfo
from ephemeris import Ephemeris

# For generic utility helper methods.
from util import Util

##############################################################################

class LookbackMultipleUtils:
    """Contains various static methods to assist in calculating
    LookbackMultiple periods forwards and backwards.

    Note:
    This class has the following methods for public use:
      initializeEphemeris()
      getDatetimesOfLongitudeDeltaDegreesInFuture()
      getDatetimesOfLongitudeDeltaDegreesInPast()

    The reason why we don't have a generic method for this (without the
    words 'future' or 'past' in the method name) is because we need a
    direction in time to look.  A referenceDt timestamp specified for a
    geocentric planet such as G.Mercury, when Mercury is between it's
    max and min elongation points relative to the Sun can have different
    results, based on the same desiredDeltaDegrees.  For example, if 0
    is specified as the desiredDeltaDegrees when G.Mercury is close
    to the Sun can yield different dates, depending on whether we are
    looking into the past or the future (both correct dates), because
    of direct and retrograde motions.
    """

    # Logger object for this class.
    log = logging.getLogger("lookbackmultiple_calc.LookbackMultipleUtils")

    @staticmethod
    def initializeEphemeris(locationLongitudeDegrees=-74.0064,
                            locationLatitudeDegrees=40.7142,
                            locationElevationMeters=0):
        """Initializes or re-initializes the Ephemeris with the location
        given as parameters.

        Arguments:
        geoLongitudeDeg - Longitude in degrees.
                          West longitudes are negative,
                          East longitudes are positive.
                          Value should be in the range of -180 to 180.
                          Default value is the longitude of New York City.
        geoLatitudeDeg  - Latitude in degrees.  North latitudes are positive,
                          south latitudes are negative.
                          Value should be in the range of -90 to 90.
                          Default value is the latitude of New York City.
        altitudeMeters  - Altitude in meters.

        """

        # Initialize the Ephemeris.
        Ephemeris.initialize()

        # Set a geographic location.
        Ephemeris.setGeographicPosition(locationLongitudeDegrees,
                                        locationLatitudeDegrees,
                                        locationElevationMeters)

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
        longitude degrees relative to the longitude degrees calculated at
        moment 'referenceDt', while stepping into the future in time.

        Returns:
        list of datetime.datetime objects, ordered chronologically
        from oldest to latest, of the timestamps when the planet
        is 'desiredDeltaDegrees' distance relative to the
        planet's longitude position at the reference datetime.datetime.

        Pre-requisites:
        This method assumes that the user has initialized the Ephemeris
        via Ephemeris.initialize() and has called
        Ephemeris.setGeographicPosition() prior to running this method.
        Calling the LookbackMultipleUtils.initializeEphemeris()
        method would work as a substitute for this.

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

        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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
        steps = collections.deque(maxlen=2)
        steps.append(referenceDt)
        steps.append(referenceDt)

        longitudesP1 = collections.deque(maxlen=2)
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

        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
            LookbackMultipleUtils.log.debug("Stepping through timestamps from {} ...".\
                  format(Ephemeris.datetimeToStr(referenceDt)))

        currDiff = None
        prevDiff = None

        # Current and previous number of degrees distance relative that we are
        # away from the longitude at referenceDt.
        currDeltaDegrees = None
        prevDeltaDegrees = None

        done = False
        while not done:

            currDt = steps[-1]
            prevDt = steps[-2]

            if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                LookbackMultipleUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            if planetReferenceLongitude == None:
                planetReferenceLongitude = getFieldValue(p1, fieldName)

                if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                    LookbackMultipleUtils.log.debug("planetReferenceLongitude == {}".\
                                                format(planetReferenceLongitude))

            longitudesP1[-1] = getFieldValue(p1, fieldName)

            if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                LookbackMultipleUtils.log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))

            # Calculate the difference in planet longitudes between the current
            # datetime and the referenceDt.
            # (This value will be in the range [0, 360) ).
            #
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - planetReferenceLongitude)

            if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                LookbackMultipleUtils.log.debug("prevDiff == {}".\
                                                format(prevDiff))
                LookbackMultipleUtils.log.debug("currDiff == {}".\
                                                format(currDiff))

            # If this is not the first iteration of the loop
            # (i.e. we have both a prevDiff and
            # a currDiff to compare).
            if prevDiff != None and longitudesP1[-2] != None:

                if prevDiff > 240 and currDiff < 120:
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from below to above!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                            # Update the prev values.
                            prevDt = t1

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our deque.
                    steps[-1] = currDt
                    steps[-2] = prevDt

                    # Increment the number of 360-degree circles traversed.
                    numFullCircles += 1

                    # Calculate the total number of degrees of distance currently.
                    currDeltaDegrees = (numFullCircles * 360.0) + currDiff

                elif prevDiff < 120 and currDiff > 240:
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from above to below!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                            # Update the prev values.
                            prevDt = t1
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our deque.
                    steps[-1] = currDt
                    steps[-2] = prevDt

                    # Decrement the number of 360-degree circles traversed.
                    numFullCircles -= 1

                    # Calculate the total number of degrees of distance currently.
                    currDeltaDegrees = (numFullCircles * 360.0) + currDiff

                else:
                    # Planet reference longitude not crossed.

                    # Calculate the total number of degrees of distance currently.
                    currDeltaDegrees = (numFullCircles * 360.0) + currDiff

                # If prevDeltaDegrees is not set, then that means this is the first
                # time in this section of code.  Initialize the prevDeltaDegrees.
                if prevDeltaDegrees == None:
                    # Two steps of stepSizeTd never goes more than 360 degrees,
                    # so we can safely use the prevDiff as the
                    # previous delta, without having to worry if we need to
                    # account for multiple full circle revolutions in between.
                    prevDeltaDegrees = prevDiff


                if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                    LookbackMultipleUtils.log.debug("prevDiff == {}".format(prevDiff))
                    LookbackMultipleUtils.log.debug("currDiff == {}".format(currDiff))
                    LookbackMultipleUtils.log.debug("currDeltaDegrees == {}".format(currDeltaDegrees))
                    LookbackMultipleUtils.log.debug("prevDeltaDegrees == {}".format(prevDeltaDegrees))
                    LookbackMultipleUtils.log.debug("desiredDeltaDegrees == {}".format(desiredDeltaDegrees))

                if prevDeltaDegrees < desiredDeltaDegrees and \
                      currDeltaDegrees > desiredDeltaDegrees:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                              "delta degrees from below to above.  " + \
                              "Narrowing down to the exact moment in time ...")

                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetReferenceLongitude +
                        (desiredDeltaDegrees % 360.0))

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))

                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        p1 = Ephemeris.getPlanetaryInfo(planetName, t2)
                        LookbackMultipleUtils.log.debug(\
                            "Found moment time: {}, with longitudeDegree == {}".\
                            format(Ephemeris.datetimeToStr(t2),
                                   getFieldValue(p1, fieldName)))

                elif prevDeltaDegrees > desiredDeltaDegrees and \
                      currDeltaDegrees < desiredDeltaDegrees:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                              "delta degrees from above to below.  " + \
                              "Narrowing down to the exact moment in time ...")

                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetReferenceLongitude +
                        (desiredDeltaDegrees % 360.0))

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))

                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        p1 = Ephemeris.getPlanetaryInfo(planetName, t2)
                        LookbackMultipleUtils.log.debug(\
                            "Found moment time: {}, with longitudeDegree == {}".\
                            format(Ephemeris.datetimeToStr(t2),
                                   getFieldValue(p1, fieldName)))


                # If we have at least one timestamp found, there is only need
                # to continue looking for more potential timestamps if the
                # planet can go retrograde.  Direct-only planets will yield
                # only 1 timestamp, and we have found it already.
                if len(rv) >= 1:
                    if Ephemeris.isDirectOnlyPlanetName(centricityType, planetName):

                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                            LookbackMultipleUtils.log.debug(\
                            "No need to look for anymore timestamps " + \
                            "because this planet doesn't go retrograde.")

                        # Set the done flag, which will stop us from looking
                        # for more timestamps.
                        done = True

                # Test base case to test if the planet will never reach the
                # 'desiredDeltaDegrees' relative to the reference
                # 'planetReferenceLongitude' longitude.
                if currDeltaDegrees - desiredDeltaDegrees > 120:

                    LookbackMultipleUtils.log.debug("Realizing we won't ever reach " + \
                                                    "'desiredDeltaDegrees' if we continue, " + \
                                                    "so setting done = True.")
                    done = True

            # Prepare for the next iteration.
            steps.append(steps[-1] + stepSizeTd)
            longitudesP1.append(None)

            # Update prevDiff with the currDiff.
            prevDiff = currDiff

            # Update prevDeltaDegrees with the currDeltaDegrees.
            prevDeltaDegrees = currDeltaDegrees

        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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
        longitude degrees relative to the longitude degrees calculated at
        moment 'referenceDt', while stepping into the past in time.

        Returns:
        list of datetime.datetime objects, ordered chronologically
        from oldest to latest, of the timestamps when the planet
        is 'desiredDeltaDegrees' distance relative to the
        planet's longitude position at the reference datetime.datetime.

        Pre-requisites:
        This method assumes that the user has initialized the Ephemeris
        via Ephemeris.initialize() and has called
        Ephemeris.setGeographicPosition() prior to running this method.
        Calling the LookbackMultipleUtils.initializeEphemeris()
        method would work as a substitute for this.

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

        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

        # Field name we are getting.
        fieldName = "longitude"

        # Step size timedelta.
        stepSizeTd = \
            LookbackMultipleUtils._getOptimalStepSizeTd(centricityType,
                                                        planetName)
        stepSizeTd = stepSizeTd * -1

        # Running count of number of full 360-degree circles.
        numFullCircles = 0

        # Desired degree.
        desiredDegree = None

        # Longitude of the planet at datetime referenceDt.
        planetReferenceLongitude = None

        # Iterate through, creating artfacts and adding them as we go.
        steps = collections.deque(maxlen=2)
        steps.append(referenceDt)
        steps.append(referenceDt)

        longitudesP1 = collections.deque(maxlen=2)
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

        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
            LookbackMultipleUtils.log.debug("Stepping through timestamps from {} ...".\
                  format(Ephemeris.datetimeToStr(referenceDt)))

        currDiff = None
        prevDiff = None

        # Current and previous number of degrees distance relative that we are
        # away from the longitude at referenceDt.
        currDeltaDegrees = None
        prevDeltaDegrees = None

        done = False
        while not done:

            currDt = steps[-1]
            prevDt = steps[-2]

            if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                LookbackMultipleUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            if planetReferenceLongitude == None:
                planetReferenceLongitude = getFieldValue(p1, fieldName)

                if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                    LookbackMultipleUtils.log.debug("planetReferenceLongitude == {}".\
                                                format(planetReferenceLongitude))

            longitudesP1[-1] = getFieldValue(p1, fieldName)

            if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                LookbackMultipleUtils.log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))

            # Calculate the difference in planet longitudes between the current
            # datetime and the referenceDt.
            # (This value will be in the range [0, 360) ).
            #
            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - planetReferenceLongitude)

            if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                LookbackMultipleUtils.log.debug("prevDiff == {}".\
                                                format(prevDiff))
                LookbackMultipleUtils.log.debug("currDiff == {}".\
                                                format(currDiff))

            # If this is not the first iteration of the loop
            # (i.e. we have both a prevDiff and
            # a currDiff to compare).
            if prevDiff != None and longitudesP1[-2] != None:

                if prevDiff > 240 and currDiff < 120:
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from below to above!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                            # Update the prev values.
                            prevDt = t1

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our deque.
                    steps[-1] = currDt
                    steps[-2] = prevDt

                    # Increment the number of 360-degree circles traversed.
                    numFullCircles += 1

                    # Calculate the total number of degrees of distance currently.
                    currDeltaDegrees = (numFullCircles * 360.0) + currDiff

                elif prevDiff < 120 and currDiff > 240:
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Crossed over planet reference longitude {} ".\
                              format(planetReferenceLongitude) + \
                              "from above to below!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                            # Update the prev values.
                            prevDt = t1
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currDiff = testDiff

                        currErrorTd = Util.absTd(t2 - t1)

                    # Update our deque.
                    steps[-1] = currDt
                    steps[-2] = prevDt

                    # Decrement the number of 360-degree circles traversed.
                    numFullCircles -= 1

                    # Calculate the total number of degrees of distance currently.
                    currDeltaDegrees = (numFullCircles * 360.0) + currDiff

                else:
                    # Planet reference longitude not crossed.

                    # Calculate the total number of degrees of distance currently.
                    currDeltaDegrees = (numFullCircles * 360.0) + currDiff

                # If prevDeltaDegrees is not set, then that means this is the first
                # time in this section of code.  Initialize the prevDeltaDegrees.
                if prevDeltaDegrees == None:
                    # Two steps of stepSizeTd never goes more than 360 degrees,
                    # so we can safely use the prevDiff as the
                    # previous delta, without having to worry if we need to
                    # account for multiple full circle revolutions in between.
                    prevDeltaDegrees = prevDiff


                if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                    LookbackMultipleUtils.log.debug("prevDiff == {}".format(prevDiff))
                    LookbackMultipleUtils.log.debug("currDiff == {}".format(currDiff))
                    LookbackMultipleUtils.log.debug("currDeltaDegrees == {}".format(currDeltaDegrees))
                    LookbackMultipleUtils.log.debug("prevDeltaDegrees == {}".format(prevDeltaDegrees))
                    LookbackMultipleUtils.log.debug("desiredDeltaDegrees == {}".format(desiredDeltaDegrees))

                if prevDeltaDegrees < desiredDeltaDegrees and \
                      currDeltaDegrees > desiredDeltaDegrees:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                              "delta degrees from below to above.  " + \
                              "Narrowing down to the exact moment in time ...")

                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetReferenceLongitude +
                        (desiredDeltaDegrees % 360.0))

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))

                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        p1 = Ephemeris.getPlanetaryInfo(planetName, t2)
                        LookbackMultipleUtils.log.debug(\
                            "Found moment time: {}, with longitudeDegree == {}".\
                            format(Ephemeris.datetimeToStr(t2),
                                   getFieldValue(p1, fieldName)))

                elif prevDeltaDegrees > desiredDeltaDegrees and \
                      currDeltaDegrees < desiredDeltaDegrees:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("Passed the desired number of " + \
                              "delta degrees from above to below.  " + \
                              "Narrowing down to the exact moment in time ...")

                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetReferenceLongitude +
                        (desiredDeltaDegrees % 360.0))

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        LookbackMultipleUtils.log.debug("desiredDegree == {}".format(desiredDegree))

                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = Util.absTd(t2 - t1)

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
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

                    if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                        p1 = Ephemeris.getPlanetaryInfo(planetName, t2)
                        LookbackMultipleUtils.log.debug(\
                            "Found moment time: {}, with longitudeDegree == {}".\
                            format(Ephemeris.datetimeToStr(t2),
                                   getFieldValue(p1, fieldName)))


                # If we have at least one timestamp found, there is only need
                # to continue looking for more potential timestamps if the
                # planet can go retrograde.  Direct-only planets will yield
                # only 1 timestamp, and we have found it already.
                if len(rv) >= 1:
                    if Ephemeris.isDirectOnlyPlanetName(centricityType, planetName):

                        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
                            LookbackMultipleUtils.log.debug(\
                            "No need to look for anymore timestamps " + \
                            "because this planet doesn't go retrograde.")

                        # Set the done flag, which will stop us from looking
                        # for more timestamps.
                        done = True

                # Test base case to test if the planet will never reach the
                # 'desiredDeltaDegrees' relative to the reference
                # 'planetReferenceLongitude' longitude.
                if currDeltaDegrees - desiredDeltaDegrees < -120:

                    LookbackMultipleUtils.log.debug("Realizing we won't ever reach " + \
                                                    "'desiredDeltaDegrees' if we continue, " + \
                                                    "so setting done = True.")
                    done = True

            # Prepare for the next iteration.
            steps.append(steps[-1] + stepSizeTd)
            longitudesP1.append(None)

            # Update prevDiff with the currDiff.
            prevDiff = currDiff

            # Update prevDeltaDegrees with the currDeltaDegrees.
            prevDeltaDegrees = currDeltaDegrees

        if LookbackMultipleUtils.log.isEnabledFor(logging.DEBUG) == True:
            LookbackMultipleUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")

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
            stepSizeTd = datetime.timedelta(hours=5)

        # These planets don't go retrograde, so we don't have to worry about
        # losing data points if our step size is too big.  We just have to keep
        # the step size to lower than 120 degrees.  Here, I'll just
        # use some overly safe values, because planets move a different speeds
        # due to their elliptical orbits.
        if centricityType == "geocentric":
            if planetName == "Moon":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "SunTrueNorthNode":
                stepSizeTd = datetime.timedelta(days=55)
            elif planetName == "SunTrueSouthNode":
                stepSizeTd = datetime.timedelta(days=55)
            elif planetName == "MoonTrueNorthNode":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "MoonTrueSouthNode":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "MoSu":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Sun":
                stepSizeTd = datetime.timedelta(days=55)
        elif centricityType == "heliocentric":
            if planetName == "Mercury":
                stepSizeTd = datetime.timedelta(days=12)
            elif planetName == "Venus":
                stepSizeTd = datetime.timedelta(days=30)
            elif planetName == "Earth":
                stepSizeTd = datetime.timedelta(days=55)
            elif planetName == "Mars":
                stepSizeTd = datetime.timedelta(days=90)
            elif planetName == "Jupiter":
                stepSizeTd = datetime.timedelta(days=360)
            elif planetName == "Saturn":
                stepSizeTd = datetime.timedelta(days=720)
            elif planetName == "Uranus":
                stepSizeTd = datetime.timedelta(days=2100)
            elif planetName == "Neptune":
                stepSizeTd = datetime.timedelta(days=4200)
            elif planetName == "Pluto":
                stepSizeTd = datetime.timedelta(days=4200)

        return stepSizeTd

##############################################################################

def testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInFuture():
    """Tests planet movements (both direct and retrograde planets/movements).
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
        print("  Testing G.Mercury moving 360 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1967, 5, 30, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 360

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1968-05-25 21:22:38.054211+00:00")
        print("  Expected resultDts[1] == 1968-06-19 03:27:31.904297+00:00")
        print("  Expected resultDts[2] == 1968-07-09 23:46:24.137980+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 5, 25, 21, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1968-05-28 12:49:42.128906+00:00")
        print("  Expected resultDts[1] == 1968-06-15 14:39:44.472656+00:00")
        print("  Expected resultDts[2] == 1968-07-12 05:10:29.736329+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 5, 25, 21, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 2")
        print("  Expected resultDts[0] == 1968-06-22 22:20:25.195312+00:00")
        print("  Expected resultDts[1] == 1968-07-07 01:03:15.556641+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 6, 19, 3, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1968-07-12 05:45:53.613283+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 6, 19, 3, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 2")
        print("  Expected resultDts[0] == 1968-06-22 21:06:59.238282+00:00")
        print("  Expected resultDts[1] == 1968-07-07 02:04:57.509766+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 7, 9, 23, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1968-07-12 04:52:02.753906+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 7, 9, 23, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 0")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 0 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 5, 25, 21, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 2")
        print("  Expected resultDts[0] == 1968-06-19 04:01:07.675781+00:00")
        print("  Expected resultDts[1] == 1968-07-09 23:22:36.152344+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -0 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 5, 25, 21, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 2")
        print("  Expected resultDts[0] == 1968-06-19 04:01:07.675781+00:00")
        print("  Expected resultDts[1] == 1968-07-09 23:22:36.152344+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 0 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 6, 19, 4, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1968-07-09 23:23:23.173829+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 0 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1967, 9, 11, 12, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 0")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 10 degrees.  From about 4 Gem to 14 Gem.")
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
        print("  Testing G.Mercury moving 5 degrees. From about 4 deg Gem to 9 deg Gem.")
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
        print("  Testing G.Mercury moving 5 degrees. From about 4 deg Gem to 9 deg Gem.")
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
        print("  Testing G.Mercury moving 5 degrees. From about 4 deg Gem to 9 deg Gem.")
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
        print("  Testing G.Mercury moving 360 degrees.  Over an Aries boundary.  From 4 Aries to 4 Aries.")
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
        print("  Testing G.Mercury moving 20 degrees.  From about 27 Pisces to 17 Aries.")
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
        print("  Testing G.Mercury moving 10 degrees.  From about 27 Pisces to 7 Aries.")
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
        print("  Testing G.Mercury moving 10 degrees. From about 27 deg Pisces to 7 deg Aries.")
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
        print("  Testing G.Mercury moving 10 degrees. From about 27 deg Pisces to 7 deg Aries.")
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
        print("  Testing G.Moon moving 22 rev.  From about 0 Taurus to 0 Taurus.")
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
        print("  Testing H.Venus moving 22 rev.  From about 18 Aries to 18 Aries.")
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
        print("  Expected resultDts[0] == 1994-10-20 07:06:05.213014+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mars moving negative degrees (which will never be reached).")
        planetName="Mars"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -50

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 0")

    print("")


def testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInPast():
    """Tests planet movements (both direct and retrograde planets/movements).
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
        print("  Testing G.Mercury moving -360 degrees.  28 Libra to 28 Libra.")
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
        print("  Expected resultDts[0] == 1968-11-07 16:05:41.894530+00:00")
        print("  Expected resultDts[1] == 1968-10-09 15:01:36.240233+00:00")
        print("  Expected resultDts[2] == 1968-09-26 13:28:07.939452+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 5, 25, 21, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 0")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 5, 25, 21, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1968-05-23 16:46:24.814452+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 6, 19, 3, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 2")
        print("  Expected resultDts[0] == 1968-06-15 13:34:43.447265+00:00")
        print("  Expected resultDts[1] == 1968-05-28 13:42:39.375000+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 6, 19, 3, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1968-05-23 17:21:30.234374+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 7, 9, 23, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 2")
        print("  Expected resultDts[0] == 1968-06-15 15:13:29.912109+00:00")
        print("  Expected resultDts[1] == 1968-05-28 12:22:09.345703+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -2 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1968, 7, 9, 23, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -2

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 3")
        print("  Expected resultDts[0] == 1968-07-07 00:30:56.689452+00:00")
        print("  Expected resultDts[1] == 1968-06-22 22:58:44.853515+00:00")
        print("  Expected resultDts[2] == 1968-05-23 16:28:11.015624+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving 0 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1969, 6, 2, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1969-05-05 14:05:10.693359+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mercury moving -0 degrees.")
        planetName="Mercury"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1969, 6, 2, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = -0

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 1")
        print("  Expected resultDts[0] == 1969-05-05 14:05:10.693359+00:00")

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
        print("  Expected resultDts[0] == 1968-11-07 16:29:03.310546+00:00")
        print("  Expected resultDts[1] == 1968-10-09 14:18:25.664061+00:00")
        print("  Expected resultDts[2] == 1968-09-26 14:21:50.009764+00:00")

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
        print("  Testing G.Moon moving -22 rev.  From about 0 Taurus to 0 Taurus.")
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
        print("  Expected resultDts[0] == 1979-05-23 11:35:54.968260+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing H.Venus moving -22 rev.  From about 18 Aries to 18 Aries.")
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
        print("  Expected resultDts[0] == 1981-04-07 16:53:54.786986+00:00")

    if True:
        print("  ------------------------------------------------------------")
        print("  Testing G.Mars moving positive degrees (which will never be reached).")
        planetName="Mars"
        centricityType="geocentric"
        longitudeType="tropical"
        referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
        desiredDeltaDegrees = 50

        resultDts = \
            LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                planetName, centricityType, longitudeType, referenceDt,
                desiredDeltaDegrees)

        printDatetimeResults(resultDts, planetName, centricityType,
                             longitudeType, referenceDt, desiredDeltaDegrees)

        print("  Expected  num results == 0")

    print("")


def testLookbackMultipleUtils_speedTest():
    """Tests to see how long it takes to do some computations."""

    print("Running " + inspect.stack()[0][3] + "()")

    # For timing the calculations.
    import time

    if False:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)

        print("  Testing G.AsSu moving 360 rev., 3 times, with maxErrorTd={}".\
              format(maxErrorTd))

        startTime = time.time()

        for i in range(3):
            planetName="AsSu"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            desiredDeltaDegrees = -360 * 360

            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt,
                    desiredDeltaDegrees, maxErrorTd)

        endTime = time.time()
        print("    Calculations took: {} sec".format(endTime - startTime))

    if False:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)

        print("  Testing G.SunTrueNorthNode moving 360 rev., 3 times, with maxErrorTd={}".\
              format(maxErrorTd))

        startTime = time.time()

        for i in range(3):
            planetName="SunTrueNorthNode"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            desiredDeltaDegrees = -360 * 360

            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt,
                    desiredDeltaDegrees, maxErrorTd)

    if False:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)

        print("  Testing G.SunTrueSouthNode moving 360 rev., 3 times, with maxErrorTd={}".\
              format(maxErrorTd))

        startTime = time.time()

        for i in range(3):
            planetName="SunTrueSouthNode"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            desiredDeltaDegrees = -360 * 360

            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt,
                    desiredDeltaDegrees, maxErrorTd)

    if False:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)

        print("  Testing G.MoonTrueNorthNode moving 360 rev., 3 times, with maxErrorTd={}".\
              format(maxErrorTd))

        startTime = time.time()

        for i in range(3):
            planetName="MoonTrueNorthNode"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            desiredDeltaDegrees = -360 * 360

            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt,
                    desiredDeltaDegrees, maxErrorTd)

    if False:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)

        print("  Testing G.MoonTrueSouthNode moving 360 rev., 3 times, with maxErrorTd={}".\
              format(maxErrorTd))

        startTime = time.time()

        for i in range(3):
            planetName="MoonTrueSouthNode"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            desiredDeltaDegrees = -360 * 360

            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt,
                    desiredDeltaDegrees, maxErrorTd)

    if False:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)

        print("  Testing G.MoSu moving 360 rev., 3 times, with maxErrorTd={}".\
              format(maxErrorTd))

        startTime = time.time()

        for i in range(3):
            planetName="MoSu"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            desiredDeltaDegrees = -360 * 360

            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt,
                    desiredDeltaDegrees, maxErrorTd)

    if True:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)

        print("  Testing G.MoSu moving 12 rev., 30 times, with maxErrorTd={}".\
              format(maxErrorTd))

        startTime = time.time()

        for i in range(30):
            planetName="MoSu"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            desiredDeltaDegrees = -360 * 12

            resultDts = \
                LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(
                    planetName, centricityType, longitudeType, referenceDt,
                    desiredDeltaDegrees, maxErrorTd)

        endTime = time.time()
        print("    Calculations took: {} sec".format(endTime - startTime))

##############################################################################

# For debugging the module during development.
if __name__=="__main__":
    # For inspect.stack().
    import inspect

    # For profiling.
    #import cProfile

    # For timing the calculations.
    import time

    # For logging and for exiting.
    import os
    import sys

    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)
    #logging.disable(logging.CRITICAL)

    # Initialize the Ephemeris (required).
    Ephemeris.initialize()

    # New York City:
    lon = -74.0064
    lat = 40.7142

    # Set a default location (required).
    Ephemeris.setGeographicPosition(lon, lat)

    # Create the Qt application.
    #app = QApplication(sys.argv)

    # Various tests to run:

    def runTests():
        testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInFuture()
        testLookbackMultipleUtils_getDatetimesOfLongitudeDeltaDegreesInPast()
        testLookbackMultipleUtils_speedTest()

    startTime = time.time()
    runTests()
    endTime = time.time()

    print("")
    print("Running all tests took: {} sec".format(endTime - startTime))

    #cProfile.run('runTests()')

    # Exit the app when all windows are closed.
    #app.lastWindowClosed.connect(logging.shutdown)
    #app.lastWindowClosed.connect(app.quit)

    #app.exec_()

    # Quit.
    print("Exiting.")
    sys.exit()

##############################################################################
