
# For directory access.
import inspect

# For line separators / newlines.
import os

# For deepcopy.
import copy

# For timestamps and timezone information.
import datetime
import pytz

# For logging.
import logging
import logging.config

# Import the Ephemeris classes.
from ephemeris import PlanetaryInfo
from ephemeris import Ephemeris
from astrologychart import AstrologyUtils

# For generic utility helper methods.
from util import Util

##############################################################################

class PLMMUtils:
    """
    PLMMUtils is short for PlanetLongitudeMovementMeasurementUtils.
    PLMMUtils contains various static methods to assist in calculating
    planet longitude movement measurements.

    Note:
    This class has the following methods for public use:
      initializeEphemeris()
      getPlanetLongitudeMovementMeasurementText()
    """

    # Logger object for this class.
    log = logging.getLogger("planetlongitudemovementmeasurement_calc.PLMMUtils")

    # Size of a circle, in degrees.
    #
    # Here we define our own value instead of using the value in
    # AstrologyUtils.degreesInCircle because it is possible we may
    # want to test different sizes of a 'circle'.
    circleSizeInDegrees = 360.0

    # All references to longitude_speed need to
    # be from tropical zodiac measurements!  If I use
    # sidereal zodiac measurements for getting the
    # longitude_speed, then the measurements from the
    # Swiss Ephemeris do not yield the correct values.
    # I use the following variable in these locations.
    zodiacTypeForLongitudeSpeed = "tropical"


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
    def getPlanetLongitudeMovementMeasurementText(\
        planetName,
        startTimestamp,
        endTimestamp,
        showGeocentricRetroAsZeroTextFlag,
        showGeocentricRetroAsPositiveTextFlag,
        showGeocentricRetroAsNegativeTextFlag,
        showHeliocentricTextFlag,
        tropicalZodiacFlag,
        siderealZodiacFlag,
        measurementUnitDegreesEnabled,
        measurementUnitCirclesEnabled,
        measurementUnitBiblicalCirclesEnabled,
        maxErrorTd=datetime.timedelta(minutes=1)):
        """Measures the planet longitude movement between two timestamps.
        The measurements are returned in a multi-line str.

        If 'startTimestamp' and 'endTimestamp' are the same timestamp,
        then an empty str is returned.  If 'startTimestamp' is not
        before 'endTimestamp' then the two timestamps will be swapped so that
        'startTimestamp' is always before 'endTimestamp'.

        Pre-requisites:
        This method assumes that the user has initialized the Ephemeris
        via Ephemeris.initialize() and has called
        Ephemeris.setGeographicPosition() prior to running this method.
        Calling the PLMMUtils.initializeEphemeris()
        method would work as a substitute for this.

        Arguments:

        planetName     - str holding the name of the planet to do the
                         calculations for.

        startTimestamp - datetime.datetime holding the beginning timestamp
                         for measurement.  If this value is after 'endTimestamp',
                         then the algorithm for this method will swap
                         'startTimestamp' and 'endTimestamp' so that
                         'startTimestamp' is always before 'endTimestamp'.

        endTimestamp   - datetime.datetime holding the ending timestamp
                         for measurement.  If this value is before 'endTimestamp',
                         then the algorithm for this method will swap
                         'startTimestamp' and 'endTimestamp' so that
                         'startTimestamp' is always before 'endTimestamp'.

        showGeocentricRetroAsZeroTextFlag
                       - bool flag for this measurement type to be included.

        showGeocentricRetroAsPositiveTextFlag
                       - bool flag for this measurement type to be included.

        showGeocentricRetroAsNegativeTextFlag
                       - bool flag for this measurement type to be included.

        showHeliocentricTextFlag,
                       - bool flag for this measurement type to be included.

        tropicalZodiacFlag
                       - bool flag for measuring with the tropical Zodiac.

        siderealZodiacFlag
                       - bool flag for measuring with the sidereal Zodiac.

        measurementUnitDegreesEnabled,
                       - bool flag for measuring in units of degrees.

        measurementUnitCirclesEnabled,
                       - bool flag for measuring in units of circles.

        measurementUnitBiblicalCirclesEnabled,
                       - bool flag for measuring in units of
                         George Bayer's biblical circles.

        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.

        Returns:
        str containing the planet longitude movement
        measurements between two timestamps, as measured in various
        units, zodiacs and centricity types.
        """

        if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
            PLMMUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        text = ""


        timestampStr = Ephemeris.datetimeToDayStr(startTimestamp)
        if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
            PLMMUtils.log.debug("startTimestamp: " + timestampStr)


        timestampStr = Ephemeris.datetimeToDayStr(endTimestamp)
        if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
            PLMMUtils.log.debug("endTimestamp: " + timestampStr)

        # If startTimestamp is after endTimestamp, then swap their
        # values.  This can happen if the person is measuring
        # 'backwards' from the future towards the past.  We have
        # to swap the values or else some of the measurements
        # would be totally invalid (due to how we subtract and
        # normalize to get elapsed longitude).
        if startTimestamp > endTimestamp:
            if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                PLMMUtils.log.debug("endTimestamp is < startTimestamp." + \
                                    "Swapping them.")
            temp = startTimestamp
            startTimestamp = endTimestamp
            endTimestamp = temp

        # If the start and end timestamps are the same, then
        # don't do any calculations.  Return an empty 'text' str.
        if startTimestamp == endTimestamp:
            return text

        # If at least one of the zodiacs are not selected,
        # then don't do any calculations.
        if tropicalZodiacFlag == False and \
           siderealZodiacFlag == False:

            return text

        # If there are no measurement unit types specified,
        # then don't do calculations for any planets.
        if measurementUnitDegreesEnabled == False and \
           measurementUnitCirclesEnabled == False and \
           measurementUnitBiblicalCirclesEnabled == False:

            return text

        # Flag indicating that geocentric measurements are to be done.
        isGeocentricEnabled = \
            showGeocentricRetroAsZeroTextFlag == True or \
            showGeocentricRetroAsPositiveTextFlag == True or \
            showGeocentricRetroAsNegativeTextFlag == True

        # Flag indicating that heliocentric measurements are to be done.
        isHeliocentricEnabled = showHeliocentricTextFlag

        # List of PlanetaryInfo objects for this particular
        # planet, sorted by timestamp.
        planetData = []


        # Step size to use in populating the data list with
        # PlanetaryInfos.

        stepSizeTd = \
            PLMMUtils._getOptimalStepSizeTd(planetName,
                                            isGeocentricEnabled,
                                            isHeliocentricEnabled)

        if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
            PLMMUtils.log.debug("stepSizeTd == " + stepSizeTd)
            PLMMUtils.log.debug("Stepping through from {} to {} ...".\
                format(Ephemeris.datetimeToStr(startTimestamp),
                       Ephemeris.datetimeToStr(endTimestamp)))

        # Current datetime as we step through all the
        # timestamps between the start and end timestamp.
        currDt = copy.deepcopy(startTimestamp)

        # Step through the timestamps, calculating the planet positions.
        while currDt < endTimestamp:
            p = Ephemeris.getPlanetaryInfo(planetName, currDt)
            planetData.append(p)

            # Increment step size.
            currDt += stepSizeTd

        # We must also append the planet calculation for the end timestamp.
        p = Ephemeris.getPlanetaryInfo(planetName, endTimestamp)
        planetData.append(p)

        # Geocentric measurement.
        if isGeocentricEnabled == True and \
                not Ephemeris.isHeliocentricOnlyPlanetName(planetName):

            # Get the PlanetaryInfos for the timestamps of the
            # planet at the moment right after the
            # longitude_speed polarity changes.
            additionalPlanetaryInfos = []

            prevLongitudeSpeed = None

            for i in range(len(planetData)):
                currLongitudeSpeed = \
                    planetData[i].geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed']

                if prevLongitudeSpeed != None and \
                   ((prevLongitudeSpeed < 0 and currLongitudeSpeed >= 0) or \
                   (prevLongitudeSpeed >= 0 and currLongitudeSpeed < 0)):

                    # Polarity changed.
                    # Try to narrow down the exact moment in
                    # time when this occured.
                    t1 = planetData[i-1].dt
                    t2 = planetData[i].dt
                    currErrorTd = t2 - t1

                    while currErrorTd > maxErrorTd:
                        if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                            PLMMUtils.log.debug("Refining between {} and {}".\
                                           format(Ephemeris.datetimeToStr(t1),
                                                  Ephemeris.datetimeToStr(t2)))

                        # Check the timestamp between.
                        diffTd = t2 - t1
                        halfDiffTd = \
                            datetime.\
                            timedelta(days=(diffTd.days / 2.0),
                                      seconds=(diffTd.seconds / 2.0),
                                      microseconds=(diffTd.\
                                                    microseconds / 2.0))
                        testDt = t1 + halfDiffTd

                        p = Ephemeris.getPlanetaryInfo(planetName, testDt)
                        testLongitudeSpeed = \
                            p.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed']

                        if ((prevLongitudeSpeed < 0 and \
                             testLongitudeSpeed >= 0) or \
                            (prevLongitudeSpeed >= 0 and \
                             testLongitudeSpeed < 0)):

                            # Polarity change at the test timestamp.
                            t2 = testDt

                        else:
                            # No polarity change yet.
                            t1 = testDt

                        # Update the currErrorTd.
                        currErrorTd = t2 - t1

                    PLMMUtils.log.debug("Broke out of loop to find " + \
                                   "velocity polarity change.  " + \
                                   "currErrorTd is: {}, ".\
                                   format(currErrorTd))

                    # Timestamp at t2 is now within the amount
                    # of the time error threshold ('maxErrorTd')
                    # following the polarity change.
                    # Append this value to the list.
                    p = Ephemeris.getPlanetaryInfo(planetName, t2)
                    additionalPlanetaryInfos.append(p)

                    t1pi = planetData[i-1]
                    t2pi = Ephemeris.getPlanetaryInfo(planetName, t2)

                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                        PLMMUtils.log.debug("t1 == {}, ".\
                                   format(Ephemeris.datetimeToStr(t1pi.dt)) + \
                                   "longitude(tropical) == {}, ".\
                                   format(t1pi.geocentric['tropical']['longitude']) + \
                                   "longitude(sidereal) == {}, ".\
                                   format(t1pi.geocentric['sidereal']['longitude']) + \
                                   "longitude_speed == {}, ".\
                                   format(t1pi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed']))

                        PLMMUtils.log.debug("t2 == {}, ".\
                                   format(Ephemeris.datetimeToStr(t2pi.dt)) + \
                                   "longitude(tropical) == {}, ".\
                                   format(t2pi.geocentric['tropical']['longitude']) + \
                                   "longitude(sidereal) == {}, ".\
                                   format(t2pi.geocentric['sidereal']['longitude']) + \
                                   "longitude_speed == {}, ".\
                                   format(t2pi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed']))

                    # There is no need to update
                    # currLongitudeSpeed here, because the
                    # longitude_speed for 'p' should be the
                    # same polarity.

                # Update prevLongitudeSpeed.
                prevLongitudeSpeed = currLongitudeSpeed

            # Sort all the extra PlanetaryInfo objects by timestamp.
            additionalPlanetaryInfos = \
                sorted(additionalPlanetaryInfos, key=lambda c: c.dt)

            # Insert PlanetaryInfos from
            # 'additionalPlanetaryInfos' into 'planetData' at
            # the timestamp-ordered location.
            currLoc = 0
            for i in range(len(additionalPlanetaryInfos)):
                pi = additionalPlanetaryInfos[i]

                insertedFlag = False

                while currLoc < len(planetData):
                    if pi.dt < planetData[currLoc].dt:
                        planetData.insert(currLoc, pi)
                        insertedFlag = True
                        currLoc += 1
                        break
                    else:
                        currLoc += 1

                if insertedFlag == False:
                    # PlanetaryInfo 'pi' has a timestamp that
                    # is later than the last PlanetaryInfo in
                    # 'planetData', so just append it.
                    planetData.append(pi)

                    # Increment currLoc so that the rest of
                    # the PlanetaryInfos in
                    # 'additionalPlanetaryInfos' can be
                    # appended without doing anymore timestamp tests.
                    currLoc += 1

            # Do summations to determine the measurements.

            if showGeocentricRetroAsZeroTextFlag == True:
                if tropicalZodiacFlag == True:
                    totalDegrees = 0
                    zodiacType = "tropical"

                    for i in range(len(planetData)):
                        if i != 0:
                            prevPi = planetData[i-1]
                            currPi = planetData[i]

                            if prevPi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                longitudeElapsed = \
                                    Util.toNormalizedAngle(longitudeElapsed)

                                totalDegrees += longitudeElapsed
                            else:
                                # Retrograde motion.
                                # Elapsed amount for this segment should be negative.

                                # Retrograde movements are considered as zero.
                                longitudeElapsed = 0
                                totalDegrees += longitudeElapsed

                    # Line of text.  We append measurements to
                    # this line of text depending on what
                    # measurements are enabled.
                    line = "G T {} moves ".format(planetName)

                    numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                    numBiblicalCircles = \
                        totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                    # Flag that indicates at least one
                    # measurement unit type is already
                    # appended to the line of text.
                    atLeastOneMeasurementAlreadyAddedFlag = False

                    if measurementUnitDegreesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.2f} deg ".format(totalDegrees)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} cir ".format(numCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitBiblicalCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} bcir ".format(numBiblicalCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    # Append last part of the line.
                    line += "(r as 0)"

                    text += line + os.linesep

                if siderealZodiacFlag == True:
                    totalDegrees = 0
                    zodiacType = "sidereal"

                    for i in range(len(planetData)):
                        if i != 0:
                            prevPi = planetData[i-1]
                            currPi = planetData[i]

                            if prevPi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                longitudeElapsed = \
                                    Util.toNormalizedAngle(longitudeElapsed)

                                totalDegrees += longitudeElapsed
                            else:
                                # Retrograde motion.
                                # Elapsed amount for this segment should be negative.

                                # Retrograde movements are considered as zero.
                                longitudeElapsed = 0
                                totalDegrees += longitudeElapsed

                    # Line of text.  We append measurements to
                    # this line of text depending on what
                    # measurements are enabled.
                    line = "G S {} moves ".format(planetName)

                    numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                    numBiblicalCircles = \
                        totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                    # Flag that indicates at least one
                    # measurement unit type is already
                    # appended to the line of text.
                    atLeastOneMeasurementAlreadyAddedFlag = False

                    if measurementUnitDegreesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.2f} deg ".format(totalDegrees)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} cir ".format(numCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitBiblicalCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} bcir ".format(numBiblicalCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    # Append last part of the line.
                    line += "(r as 0)"

                    text += line + os.linesep

            if showGeocentricRetroAsPositiveTextFlag == True:
                if tropicalZodiacFlag == True:
                    totalDegrees = 0
                    zodiacType = "tropical"

                    for i in range(len(planetData)):
                        if i != 0:
                            prevPi = planetData[i-1]
                            currPi = planetData[i]

                            if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                PLMMUtils.log.debug("-------------------------------------------------")
                                PLMMUtils.log.debug("  planetData[{}] ({}): lon == {}, speed == {}".\
                                               format(i-1,
                                                      Ephemeris.datetimeToStr(planetData[i-1].dt),
                                                      planetData[i-1].geocentric[zodiacType]['longitude'],
                                                      planetData[i-1].geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed']
                                                      ))
                                PLMMUtils.log.debug("  planetData[{}] ({}): lon == {}, speed == {}".\
                                               format(i,
                                                      Ephemeris.datetimeToStr(planetData[i].dt),
                                                      planetData[i].geocentric[zodiacType]['longitude'],
                                                      planetData[i].geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed']
                                                      ))

                            if prevPi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                    PLMMUtils.log.debug("Direct motion: " + \
                                                   "longitudeElapsed " + \
                                                   "(before reduction): {}".\
                                                   format(longitudeElapsed))

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                longitudeElapsed = \
                                    Util.toNormalizedAngle(longitudeElapsed)

                                totalDegrees += longitudeElapsed

                                if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                    PLMMUtils.log.debug("Direct motion: Added amount: {}".\
                                                   format(longitudeElapsed))
                            else:
                                # Retrograde motion.
                                # Elapsed amount for this segment should be negative.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                    PLMMUtils.log.debug("Retrograde motion: " + \
                                                   "longitudeElapsed " + \
                                                   "(before reduction): {}".\
                                                   format(longitudeElapsed))

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                if longitudeElapsed > 0:
                                    longitudeElapsed -= 360

                                # Since this is retrograde
                                # movement, as we are counting
                                # retrograde movements as
                                # positive values, negate it
                                # before adding.
                                totalDegrees += abs(longitudeElapsed)

                                if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                    PLMMUtils.log.debug("Retrograde motion: Added amount: {}".\
                                                   format(abs(longitudeElapsed)))

                    # Line of text.  We append measurements to
                    # this line of text depending on what
                    # measurements are enabled.
                    line = "G T {} moves ".format(planetName)

                    numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                    numBiblicalCircles = \
                        totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                    # Flag that indicates at least one
                    # measurement unit type is already
                    # appended to the line of text.
                    atLeastOneMeasurementAlreadyAddedFlag = False

                    if measurementUnitDegreesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.2f} deg ".format(totalDegrees)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} cir ".format(numCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitBiblicalCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} bcir ".format(numBiblicalCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    # Append last part of the line.
                    line += "(r as +)"

                    text += line + os.linesep

                if siderealZodiacFlag == True:
                    totalDegrees = 0
                    zodiacType = "sidereal"

                    for i in range(len(planetData)):
                        if i != 0:
                            prevPi = planetData[i-1]
                            currPi = planetData[i]

                            if prevPi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                longitudeElapsed = \
                                    Util.toNormalizedAngle(longitudeElapsed)

                                totalDegrees += longitudeElapsed
                            else:
                                # Retrograde motion.
                                # Elapsed amount for this segment should be negative.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                if longitudeElapsed > 0:
                                    longitudeElapsed -= 360

                                # Since this is retrograde
                                # movement, as we are counting
                                # retrograde movements as
                                # positive values, negate it
                                # before adding.
                                totalDegrees += abs(longitudeElapsed)

                    # Line of text.  We append measurements to
                    # this line of text depending on what
                    # measurements are enabled.
                    line = "G S {} moves ".format(planetName)

                    numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                    numBiblicalCircles = \
                        totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                    # Flag that indicates at least one
                    # measurement unit type is already
                    # appended to the line of text.
                    atLeastOneMeasurementAlreadyAddedFlag = False

                    if measurementUnitDegreesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.2f} deg ".format(totalDegrees)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} cir ".format(numCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitBiblicalCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} bcir ".format(numBiblicalCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    # Append last part of the line.
                    line += "(r as +)"

                    text += line + os.linesep

            if showGeocentricRetroAsNegativeTextFlag == True:
                if tropicalZodiacFlag == True:
                    totalDegrees = 0
                    zodiacType = "tropical"

                    for i in range(len(planetData)):
                        if i != 0:
                            prevPi = planetData[i-1]
                            currPi = planetData[i]

                            if prevPi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                longitudeElapsed = \
                                    Util.toNormalizedAngle(longitudeElapsed)

                                totalDegrees += longitudeElapsed
                            else:
                                # Retrograde motion.
                                # Elapsed amount for this segment should be negative.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                if longitudeElapsed > 0:
                                    longitudeElapsed -= 360

                                totalDegrees += longitudeElapsed

                    # Line of text.  We append measurements to
                    # this line of text depending on what
                    # measurements are enabled.
                    line = "G T {} moves ".format(planetName)

                    numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                    numBiblicalCircles = \
                        totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                    # Flag that indicates at least one
                    # measurement unit type is already
                    # appended to the line of text.
                    atLeastOneMeasurementAlreadyAddedFlag = False

                    if measurementUnitDegreesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.2f} deg ".format(totalDegrees)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} cir ".format(numCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitBiblicalCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} bcir ".format(numBiblicalCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    # Append last part of the line.
                    line += "(r as -)"

                    text += line + os.linesep

                if siderealZodiacFlag == True:
                    totalDegrees = 0
                    zodiacType = "sidereal"

                    for i in range(len(planetData)):
                        if i != 0:
                            prevPi = planetData[i-1]
                            currPi = planetData[i]

                            if prevPi.geocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                longitudeElapsed = \
                                    Util.toNormalizedAngle(longitudeElapsed)

                                totalDegrees += longitudeElapsed
                            else:
                                # Retrograde motion.
                                # Elapsed amount for this segment should be negative.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # See if there was a crossing of the
                                # 0 degree point or the 360 degree point.
                                # If so, make the necessary adjustments
                                # so that the longitude elapsed is
                                # correct.
                                if longitudeElapsed > 0:
                                    longitudeElapsed -= 360

                                totalDegrees += longitudeElapsed

                    # Line of text.  We append measurements to
                    # this line of text depending on what
                    # measurements are enabled.
                    line = "G T {} moves ".format(planetName)

                    numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                    numBiblicalCircles = \
                        totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                    # Flag that indicates at least one
                    # measurement unit type is already
                    # appended to the line of text.
                    atLeastOneMeasurementAlreadyAddedFlag = False

                    if measurementUnitDegreesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.2f} deg ".format(totalDegrees)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} cir ".format(numCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnitBiblicalCirclesEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} bcir ".format(numBiblicalCircles)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    # Append last part of the line.
                    line += "(r as -)"

                    text += line + os.linesep

        # Heliocentric measurement.
        if isHeliocentricEnabled == True and \
                not Ephemeris.isGeocentricOnlyPlanetName(planetName):

            if tropicalZodiacFlag == True:
                totalDegrees = 0
                zodiacType = "tropical"

                for i in range(len(planetData)):
                    if i != 0:
                        prevPi = planetData[i-1]
                        currPi = planetData[i]

                        if prevPi.heliocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                            # Direct motion.
                            # Elapsed amount for this segment should be positive.

                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.heliocentric[zodiacType]['longitude'] - \
                                prevPi.heliocentric[zodiacType]['longitude']

                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            longitudeElapsed = \
                                Util.toNormalizedAngle(longitudeElapsed)

                            totalDegrees += longitudeElapsed
                        else:
                            # Retrograde motion.
                            # Elapsed amount for this segment should be negative.

                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.heliocentric[zodiacType]['longitude'] - \
                                prevPi.heliocentric[zodiacType]['longitude']

                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            if longitudeElapsed > 0:
                                longitudeElapsed -= 360

                            totalDegrees += longitudeElapsed

                # Line of text.  We append measurements to
                # this line of text depending on what
                # measurements are enabled.
                line = "H T {} moves ".format(planetName)

                numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                numBiblicalCircles = \
                    totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                # Flag that indicates at least one
                # measurement unit type is already
                # appended to the line of text.
                atLeastOneMeasurementAlreadyAddedFlag = False

                if measurementUnitDegreesEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.2f} deg ".format(totalDegrees)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnitCirclesEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} cir ".format(numCircles)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnitBiblicalCirclesEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} bcir ".format(numBiblicalCircles)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                text += line + os.linesep

            if siderealZodiacFlag == True:
                totalDegrees = 0
                zodiacType = "sidereal"

                for i in range(len(planetData)):
                    if i != 0:
                        prevPi = planetData[i-1]
                        currPi = planetData[i]

                        if prevPi.heliocentric[PLMMUtils.zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                            # Direct motion.
                            # Elapsed amount for this segment should be positive.

                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.heliocentric[zodiacType]['longitude'] - \
                                prevPi.heliocentric[zodiacType]['longitude']

                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            longitudeElapsed = \
                                Util.toNormalizedAngle(longitudeElapsed)

                            totalDegrees += longitudeElapsed
                        else:
                            # Retrograde motion.
                            # Elapsed amount for this segment should be negative.

                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.heliocentric[zodiacType]['longitude'] - \
                                prevPi.heliocentric[zodiacType]['longitude']

                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            if longitudeElapsed > 0:
                                longitudeElapsed -= 360

                            totalDegrees += longitudeElapsed

                # Line of text.  We append measurements to
                # this line of text depending on what
                # measurements are enabled.
                line = "H S {} moves ".format(planetName)

                numCircles = totalDegrees / PLMMUtils.circleSizeInDegrees
                numBiblicalCircles = \
                    totalDegrees / AstrologyUtils.degreesInBiblicalCircle

                # Flag that indicates at least one
                # measurement unit type is already
                # appended to the line of text.
                atLeastOneMeasurementAlreadyAddedFlag = False

                if measurementUnitDegreesEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.2f} deg ".format(totalDegrees)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnitCirclesEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} cir ".format(numCircles)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnitBiblicalCirclesEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} bcir ".format(numBiblicalCircles)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                text += line + os.linesep

        text = text.rstrip()

        if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
            PLMMUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")

        return text


    @staticmethod
    def _getOptimalStepSizeTd(planetName, isGeocentricEnabled, isHeliocentricEnabled):
        """Helper function that will try to determine a better step size
        for supporting other methods of PLMMUtils.

        The step size chosen here is dependent on planetName and whether
        geocentric, heliocentric or a combination of both are used.

        # The step size should cause the planet to move less
        # than 120 degrees in all cases, and idealy much less
        # than this, that way we can easily narrow down when
        # the planet passes the 0 degree or 360 degree
        # threshold, and also so it is easier to narrow down
        # when retrograde periods happen.  If the step size is
        # too large, it is possible that we would miss a whole
        # time window of retrograde movement, so discretion
        # has to be used in determining what to use for this value.
        #
        # Here we will set it to 1 day for the default case,
        # but if the planet name is a house cusp then shrink
        # the step size so we will get the correct resolution.
        # Also, if the planet name is an outer planet with a
        # large period, we can increase the step size slightly
        # to improve performance.
        """

        # This is the default step size.
        # Planet should not ever move more than 120 degrees per step size.
        stepSizeTd = datetime.timedelta(days=1)

        # Optimize the step size accord to the planet being used.
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=5)
            return stepSizeTd

        # These planets don't go retrograde, so we don't have to worry about
        # losing data points if our step size is too big.  We just have to keep
        # the step size to lower than 120 degrees.  Here, I'll just
        # use some overly safe values, because planets move a different speeds
        # due to their elliptical orbits.

        if isGeocentricEnabled and isHeliocentricEnabled:

            if planetName == "Moon":
                stepSizeTd = datetime.timedelta(days=4)
            elif planetName == "MoSu":
                stepSizeTd = datetime.timedelta(days=4)
            elif planetName == "Sun":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Mercury":
                stepSizeTd = datetime.timedelta(days=3)
            elif planetName == "Venus":
                stepSizeTd = datetime.timedelta(days=3)
            elif planetName == "Earth":
                stepSizeTd = datetime.timedelta(days=10)
            elif planetName == "Mars":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Jupiter":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Saturn":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Uranus":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Neptune":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Pluto":
                stepSizeTd = datetime.timedelta(days=5)

        elif isGeocentricEnabled:
            if planetName == "Moon":
                stepSizeTd = datetime.timedelta(days=4)
            elif planetName == "MoSu":
                stepSizeTd = datetime.timedelta(days=4)
            elif planetName == "Sun":
                stepSizeTd = datetime.timedelta(days=5)

        elif isHeliocentricEnabled:
            if planetName == "Mercury":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "Venus":
                stepSizeTd = datetime.timedelta(days=10)
            elif planetName == "Earth":
                stepSizeTd = datetime.timedelta(days=10)
            elif planetName == "Mars":
                stepSizeTd = datetime.timedelta(days=10)
            elif planetName == "Jupiter":
                stepSizeTd = datetime.timedelta(days=20)
            elif planetName == "Saturn":
                stepSizeTd = datetime.timedelta(days=20)
            elif planetName == "Uranus":
                stepSizeTd = datetime.timedelta(days=20)
            elif planetName == "Neptune":
                stepSizeTd = datetime.timedelta(days=20)
            elif planetName == "Pluto":
                stepSizeTd = datetime.timedelta(days=20)

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
