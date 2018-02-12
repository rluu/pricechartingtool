
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

    ##################################################
    # Variable: longitudeTypeForLongitudeSpeed
    #
    # Description:
    #   All references to longitude_speed need to
    #   be from tropical zodiac measurements!  If I use
    #   sidereal zodiac measurements for getting the
    #   longitude_speed, then the measurements from the
    #   Swiss Ephemeris do not yield the correct values.
    #   I use the following variable in these locations.
    #
    longitudeTypeForLongitudeSpeed = "tropical"

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
        measurementUnit7ersEnabled,
        measurementUnit11ersEnabled,
        measurementUnit12ersEnabled,
        measurementUnit13ersEnabled,
        measurementUnit15ersEnabled,
        measurementUnit16ersEnabled,
        measurementUnit18ersEnabled,
        measurementUnit19ersEnabled,
        measurementUnit22ersEnabled,
        measurementUnit23ersEnabled,
        measurementUnit24ersEnabled,
        measurementUnit25ersEnabled,
        measurementUnit29ersEnabled,
        measurementUnit30ersEnabled,
        measurementUnit31ersEnabled,
        measurementUnit33ersEnabled,
        measurementUnit34ersEnabled,
        measurementUnit36ersEnabled,
        measurementUnit37ersEnabled,
        measurementUnit40ersEnabled,
        measurementUnit42ersEnabled,
        measurementUnit45ersEnabled,
        measurementUnit47ersEnabled,
        measurementUnit49ersEnabled,
        measurementUnit50ersEnabled,
        measurementUnit51ersEnabled,
        measurementUnit51_428ersEnabled,
        measurementUnit52ersEnabled,
        measurementUnit60ersEnabled,
        measurementUnit69ersEnabled,
        measurementUnit70ersEnabled,
        measurementUnit72ersEnabled,
        measurementUnit73ersEnabled,
        measurementUnit75ersEnabled,
        measurementUnit77ersEnabled,
        measurementUnit84ersEnabled,
        measurementUnit88ersEnabled,
        measurementUnit90ersEnabled,
        measurementUnit94ersEnabled,
        measurementUnit99ersEnabled,
        measurementUnit100ersEnabled,
        measurementUnit110ersEnabled,
        measurementUnit112ersEnabled,
        measurementUnit133ersEnabled,
        measurementUnit135ersEnabled,
        measurementUnit137ersEnabled,
        measurementUnit144ersEnabled,
        measurementUnit150ersEnabled,
        measurementUnit153ersEnabled,
        measurementUnit194ersEnabled,
        measurementUnit225ersEnabled,
        measurementUnit275ersEnabled,
        measurementUnit311ersEnabled,
        measurementUnit400ersEnabled,
        measurementUnit500ersEnabled,
        measurementUnit557ersEnabled,
        measurementUnit750ersEnabled,
        measurementUnit945ersEnabled,
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

        measurementUnit7ersEnabled,
                       - bool flag for displaying measurements in number
                         of 7-degree units.

        measurementUnit11ersEnabled,
                       - bool flag for displaying measurements in number
                         of 11-degree units.

        measurementUnit12ersEnabled,
                       - bool flag for displaying measurements in number
                         of 12-degree units.

        measurementUnit13ersEnabled,
                       - bool flag for displaying measurements in number
                         of 13-degree units.

        measurementUnit15ersEnabled,
                       - bool flag for displaying measurements in number
                         of 15-degree units.

        measurementUnit16ersEnabled,
                       - bool flag for displaying measurements in number
                         of 16-degree units.

        measurementUnit18ersEnabled,
                       - bool flag for displaying measurements in number
                         of 18-degree units.

        measurementUnit19ersEnabled,
                       - bool flag for displaying measurements in number
                         of 19-degree units.

        measurementUnit22ersEnabled,
                       - bool flag for displaying measurements in number
                         of 22-degree units.

        measurementUnit23ersEnabled,
                       - bool flag for displaying measurements in number
                         of 23-degree units.

        measurementUnit24ersEnabled,
                       - bool flag for displaying measurements in number
                         of 24-degree units.

        measurementUnit25ersEnabled,
                       - bool flag for displaying measurements in number
                         of 25-degree units.

        measurementUnit29ersEnabled,
                       - bool flag for displaying measurements in number
                         of 29-degree units.

        measurementUnit30ersEnabled,
                       - bool flag for displaying measurements in number
                         of 30-degree units.

        measurementUnit31ersEnabled,
                       - bool flag for displaying measurements in number
                         of 31-degree units.

        measurementUnit33ersEnabled,
                       - bool flag for displaying measurements in number
                         of 33-degree units.

        measurementUnit34ersEnabled,
                       - bool flag for displaying measurements in number
                         of 34-degree units.

        measurementUnit36ersEnabled,
                       - bool flag for displaying measurements in number
                         of 36-degree units.

        measurementUnit37ersEnabled,
                       - bool flag for displaying measurements in number
                         of 37-degree units.

        measurementUnit40ersEnabled,
                       - bool flag for displaying measurements in number
                         of 40-degree units.

        measurementUnit42ersEnabled,
                       - bool flag for displaying measurements in number
                         of 42-degree units.

        measurementUnit45ersEnabled,
                       - bool flag for displaying measurements in number
                         of 45-degree units.

        measurementUnit47ersEnabled,
                       - bool flag for displaying measurements in number
                         of 47-degree units.

        measurementUnit49ersEnabled,
                       - bool flag for displaying measurements in number
                         of 49-degree units.

        measurementUnit50ersEnabled,
                       - bool flag for displaying measurements in number
                         of 50-degree units.

        measurementUnit51ersEnabled,
                       - bool flag for displaying measurements in number
                         of 51-degree units.

        measurementUnit51_428ersEnabled,
                       - bool flag for displaying measurements in number
                         of 51.428-degree units.

        measurementUnit52ersEnabled,
                       - bool flag for displaying measurements in number
                         of 52-degree units.

        measurementUnit60ersEnabled,
                       - bool flag for displaying measurements in number
                         of 60-degree units.

        measurementUnit69ersEnabled,
                       - bool flag for displaying measurements in number
                         of 69-degree units.

        measurementUnit70ersEnabled,
                       - bool flag for displaying measurements in number
                         of 70-degree units.

        measurementUnit72ersEnabled,
                       - bool flag for displaying measurements in number
                         of 72-degree units.

        measurementUnit73ersEnabled,
                       - bool flag for displaying measurements in number
                         of 73-degree units.

        measurementUnit75ersEnabled,
                       - bool flag for displaying measurements in number
                         of 75-degree units.

        measurementUnit77ersEnabled,
                       - bool flag for displaying measurements in number
                         of 77-degree units.

        measurementUnit84ersEnabled,
                       - bool flag for displaying measurements in number
                         of 84-degree units.

        measurementUnit88ersEnabled,
                       - bool flag for displaying measurements in number
                         of 88-degree units.

        measurementUnit90ersEnabled,
                       - bool flag for displaying measurements in number
                         of 90-degree units.

        measurementUnit94ersEnabled,
                       - bool flag for displaying measurements in number
                         of 94-degree units.

        measurementUnit99ersEnabled,
                       - bool flag for displaying measurements in number
                         of 99-degree units.

        measurementUnit100ersEnabled,
                       - bool flag for displaying measurements in number
                         of 100-degree units.

        measurementUnit110ersEnabled,
                       - bool flag for displaying measurements in number
                         of 110-degree units.

        measurementUnit112ersEnabled,
                       - bool flag for displaying measurements in number
                         of 112-degree units.

        measurementUnit133ersEnabled,
                       - bool flag for displaying measurements in number
                         of 133-degree units.

        measurementUnit135ersEnabled,
                       - bool flag for displaying measurements in number
                         of 135-degree units.

        measurementUnit137ersEnabled,
                       - bool flag for displaying measurements in number
                         of 137-degree units.

        measurementUnit144ersEnabled,
                       - bool flag for displaying measurements in number
                         of 144-degree units.

        measurementUnit150ersEnabled,
                       - bool flag for displaying measurements in number
                         of 150-degree units.

        measurementUnit153ersEnabled,
                       - bool flag for displaying measurements in number
                         of 153-degree units.

        measurementUnit194ersEnabled,
                       - bool flag for displaying measurements in number
                         of 194-degree units.

        measurementUnit225ersEnabled,
                       - bool flag for displaying measurements in number
                         of 225-degree units.

        measurementUnit275ersEnabled,
                       - bool flag for displaying measurements in number
                         of 275-degree units.

        measurementUnit311ersEnabled,
                       - bool flag for displaying measurements in number
                         of 311-degree units.

        measurementUnit400ersEnabled,
                       - bool flag for displaying measurements in number
                         of 400-degree units.

        measurementUnit500ersEnabled,
                       - bool flag for displaying measurements in number
                         of 500-degree units.

        measurementUnit557ersEnabled,
                       - bool flag for displaying measurements in number
                         of 557-degree units.

        measurementUnit750ersEnabled,
                       - bool flag for displaying measurements in number
                         of 750-degree units.

        measurementUnit945ersEnabled,
                       - bool flag for displaying measurements in number
                         of 945-degree units.

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
           measurementUnitBiblicalCirclesEnabled == False and \
           measurementUnit7ersEnabled == False and \
           measurementUnit11ersEnabled == False and \
           measurementUnit12ersEnabled == False and \
           measurementUnit13ersEnabled == False and \
           measurementUnit15ersEnabled == False and \
           measurementUnit16ersEnabled == False and \
           measurementUnit18ersEnabled == False and \
           measurementUnit19ersEnabled == False and \
           measurementUnit22ersEnabled == False and \
           measurementUnit23ersEnabled == False and \
           measurementUnit24ersEnabled == False and \
           measurementUnit25ersEnabled == False and \
           measurementUnit29ersEnabled == False and \
           measurementUnit30ersEnabled == False and \
           measurementUnit31ersEnabled == False and \
           measurementUnit33ersEnabled == False and \
           measurementUnit34ersEnabled == False and \
           measurementUnit36ersEnabled == False and \
           measurementUnit37ersEnabled == False and \
           measurementUnit40ersEnabled == False and \
           measurementUnit42ersEnabled == False and \
           measurementUnit45ersEnabled == False and \
           measurementUnit47ersEnabled == False and \
           measurementUnit49ersEnabled == False and \
           measurementUnit50ersEnabled == False and \
           measurementUnit51ersEnabled == False and \
           measurementUnit51_428ersEnabled == False and \
           measurementUnit52ersEnabled == False and \
           measurementUnit60ersEnabled == False and \
           measurementUnit69ersEnabled == False and \
           measurementUnit70ersEnabled == False and \
           measurementUnit72ersEnabled == False and \
           measurementUnit73ersEnabled == False and \
           measurementUnit75ersEnabled == False and \
           measurementUnit77ersEnabled == False and \
           measurementUnit84ersEnabled == False and \
           measurementUnit88ersEnabled == False and \
           measurementUnit90ersEnabled == False and \
           measurementUnit94ersEnabled == False and \
           measurementUnit99ersEnabled == False and \
           measurementUnit100ersEnabled == False and \
           measurementUnit110ersEnabled == False and \
           measurementUnit112ersEnabled == False and \
           measurementUnit133ersEnabled == False and \
           measurementUnit135ersEnabled == False and \
           measurementUnit137ersEnabled == False and \
           measurementUnit144ersEnabled == False and \
           measurementUnit150ersEnabled == False and \
           measurementUnit153ersEnabled == False and \
           measurementUnit194ersEnabled == False and \
           measurementUnit225ersEnabled == False and \
           measurementUnit275ersEnabled == False and \
           measurementUnit311ersEnabled == False and \
           measurementUnit400ersEnabled == False and \
           measurementUnit500ersEnabled == False and \
           measurementUnit557ersEnabled == False and \
           measurementUnit750ersEnabled == False and \
           measurementUnit945ersEnabled == False:

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
                    planetData[i].geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed']

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
                            p.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed']

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
                                   format(t1pi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed']))

                        PLMMUtils.log.debug("t2 == {}, ".\
                                   format(Ephemeris.datetimeToStr(t2pi.dt)) + \
                                   "longitude(tropical) == {}, ".\
                                   format(t2pi.geocentric['tropical']['longitude']) + \
                                   "longitude(sidereal) == {}, ".\
                                   format(t2pi.geocentric['sidereal']['longitude']) + \
                                   "longitude_speed == {}, ".\
                                   format(t2pi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed']))

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

                            if prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed < 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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
                    num7ers = totalDegrees / 7.0
                    num11ers = totalDegrees / 11.0
                    num12ers = totalDegrees / 12.0
                    num13ers = totalDegrees / 13.0
                    num15ers = totalDegrees / 15.0
                    num16ers = totalDegrees / 16.0
                    num18ers = totalDegrees / 18.0
                    num19ers = totalDegrees / 19.0
                    num22ers = totalDegrees / 22.0
                    num23ers = totalDegrees / 23.0
                    num24ers = totalDegrees / 24.0
                    num25ers = totalDegrees / 25.0
                    num29ers = totalDegrees / 29.0
                    num30ers = totalDegrees / 30.0
                    num31ers = totalDegrees / 31.0
                    num33ers = totalDegrees / 33.0
                    num34ers = totalDegrees / 34.0
                    num36ers = totalDegrees / 36.0
                    num37ers = totalDegrees / 37.0
                    num40ers = totalDegrees / 40.0
                    num42ers = totalDegrees / 42.0
                    num45ers = totalDegrees / 45.0
                    num47ers = totalDegrees / 47.0
                    num49ers = totalDegrees / 49.0
                    num50ers = totalDegrees / 50.0
                    num51ers = totalDegrees / 51.0
                    num51_428ers = totalDegrees / (360 / 7.0)
                    num52ers = totalDegrees / 52.0
                    num60ers = totalDegrees / 60.0
                    num69ers = totalDegrees / 69.0
                    num70ers = totalDegrees / 70.0
                    num72ers = totalDegrees / 72.0
                    num73ers = totalDegrees / 73.0
                    num75ers = totalDegrees / 75.0
                    num77ers = totalDegrees / 77.0
                    num84ers = totalDegrees / 84.0
                    num88ers = totalDegrees / 88.0
                    num90ers = totalDegrees / 90.0
                    num94ers = totalDegrees / 94.0
                    num99ers = totalDegrees / 99.0
                    num100ers = totalDegrees / 100.0
                    num110ers = totalDegrees / 110.0
                    num112ers = totalDegrees / 112.0
                    num133ers = totalDegrees / 133.0
                    num135ers = totalDegrees / 135.0
                    num137ers = totalDegrees / 137.0
                    num144ers = totalDegrees / 144.0
                    num150ers = totalDegrees / 150.0
                    num153ers = totalDegrees / 153.0
                    num194ers = totalDegrees / 194.0
                    num225ers = totalDegrees / 225.0
                    num275ers = totalDegrees / 275.0
                    num311ers = totalDegrees / 311.0
                    num400ers = totalDegrees / 400.0
                    num500ers = totalDegrees / 500.0
                    num557ers = totalDegrees / 557.0
                    num750ers = totalDegrees / 750.0
                    num945ers = totalDegrees / 945.0

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

                    if measurementUnit7ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 7ers ".format(num7ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit11ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 11ers ".format(num11ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit12ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 12ers ".format(num12ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit13ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 13ers ".format(num13ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit15ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 15ers ".format(num15ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit16ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 16ers ".format(num16ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit18ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 18ers ".format(num18ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit19ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 19ers ".format(num19ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit22ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 22ers ".format(num22ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit23ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 23ers ".format(num23ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit24ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 24ers ".format(num24ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit25ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 25ers ".format(num25ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit29ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 29ers ".format(num29ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit30ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 30ers ".format(num30ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit31ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 31ers ".format(num31ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit33ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 33ers ".format(num33ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit34ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 34ers ".format(num34ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit36ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 36ers ".format(num36ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit37ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 37ers ".format(num37ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit40ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 40ers ".format(num40ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit42ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 42ers ".format(num42ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit45ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 45ers ".format(num45ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit47ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 47ers ".format(num47ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit49ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 49ers ".format(num49ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit50ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 50ers ".format(num50ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51ers ".format(num51ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51_428ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51.428ers ".format(num51_428ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit52ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 52ers ".format(num52ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit60ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 60ers ".format(num60ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit69ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 69ers ".format(num69ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit70ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 70ers ".format(num70ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit72ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 72ers ".format(num72ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit73ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 73ers ".format(num73ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit75ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 75ers ".format(num75ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit77ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 77ers ".format(num77ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit84ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 84ers ".format(num84ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit88ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 88ers ".format(num88ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit90ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 90ers ".format(num90ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit94ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 94ers ".format(num94ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit99ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 99ers ".format(num99ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit100ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 100ers ".format(num100ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit110ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 110ers ".format(num110ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit112ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 112ers ".format(num112ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit133ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 133ers ".format(num133ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit135ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 135ers ".format(num135ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit137ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 137ers ".format(num137ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit144ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 144ers ".format(num144ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit150ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 150ers ".format(num150ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit153ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 153ers ".format(num153ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit194ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 194ers ".format(num194ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit225ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 225ers ".format(num225ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit275ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 275ers ".format(num275ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit311ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 311ers ".format(num311ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit400ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 400ers ".format(num400ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit500ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 500ers ".format(num500ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit557ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 557ers ".format(num557ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit750ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 750ers ".format(num750ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit945ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 945ers ".format(num945ers)
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

                            if prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed < 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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
                    num7ers = totalDegrees / 7.0
                    num11ers = totalDegrees / 11.0
                    num12ers = totalDegrees / 12.0
                    num13ers = totalDegrees / 13.0
                    num15ers = totalDegrees / 15.0
                    num16ers = totalDegrees / 16.0
                    num18ers = totalDegrees / 18.0
                    num19ers = totalDegrees / 19.0
                    num22ers = totalDegrees / 22.0
                    num23ers = totalDegrees / 23.0
                    num24ers = totalDegrees / 24.0
                    num25ers = totalDegrees / 25.0
                    num29ers = totalDegrees / 29.0
                    num30ers = totalDegrees / 30.0
                    num31ers = totalDegrees / 31.0
                    num33ers = totalDegrees / 33.0
                    num34ers = totalDegrees / 34.0
                    num36ers = totalDegrees / 36.0
                    num37ers = totalDegrees / 37.0
                    num40ers = totalDegrees / 40.0
                    num42ers = totalDegrees / 42.0
                    num45ers = totalDegrees / 45.0
                    num47ers = totalDegrees / 47.0
                    num49ers = totalDegrees / 49.0
                    num50ers = totalDegrees / 50.0
                    num51ers = totalDegrees / 51.0
                    num51_428ers = totalDegrees / (360 / 7.0)
                    num52ers = totalDegrees / 52.0
                    num60ers = totalDegrees / 60.0
                    num69ers = totalDegrees / 69.0
                    num70ers = totalDegrees / 70.0
                    num72ers = totalDegrees / 72.0
                    num73ers = totalDegrees / 73.0
                    num75ers = totalDegrees / 75.0
                    num77ers = totalDegrees / 77.0
                    num84ers = totalDegrees / 84.0
                    num88ers = totalDegrees / 88.0
                    num90ers = totalDegrees / 90.0
                    num94ers = totalDegrees / 94.0
                    num99ers = totalDegrees / 99.0
                    num100ers = totalDegrees / 100.0
                    num110ers = totalDegrees / 110.0
                    num112ers = totalDegrees / 112.0
                    num133ers = totalDegrees / 133.0
                    num135ers = totalDegrees / 135.0
                    num137ers = totalDegrees / 137.0
                    num144ers = totalDegrees / 144.0
                    num150ers = totalDegrees / 150.0
                    num153ers = totalDegrees / 153.0
                    num194ers = totalDegrees / 194.0
                    num225ers = totalDegrees / 225.0
                    num275ers = totalDegrees / 275.0
                    num311ers = totalDegrees / 311.0
                    num400ers = totalDegrees / 400.0
                    num500ers = totalDegrees / 500.0
                    num557ers = totalDegrees / 557.0
                    num750ers = totalDegrees / 750.0
                    num945ers = totalDegrees / 945.0

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

                    if measurementUnit7ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 7ers ".format(num7ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit11ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 11ers ".format(num11ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit12ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 12ers ".format(num12ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit13ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 13ers ".format(num13ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit15ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 15ers ".format(num15ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit16ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 16ers ".format(num16ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit18ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 18ers ".format(num18ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit19ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 19ers ".format(num19ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit22ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 22ers ".format(num22ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit23ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 23ers ".format(num23ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit24ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 24ers ".format(num24ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit25ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 25ers ".format(num25ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit29ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 29ers ".format(num29ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit30ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 30ers ".format(num30ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit31ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 31ers ".format(num31ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit33ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 33ers ".format(num33ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit34ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 34ers ".format(num34ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit36ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 36ers ".format(num36ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit37ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 37ers ".format(num37ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit40ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 40ers ".format(num40ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit42ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 42ers ".format(num42ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit45ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 45ers ".format(num45ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit47ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 47ers ".format(num47ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit49ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 49ers ".format(num49ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit50ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 50ers ".format(num50ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51ers ".format(num51ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51_428ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51.428ers ".format(num51_428ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit52ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 52ers ".format(num52ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit60ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 60ers ".format(num60ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit69ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 69ers ".format(num69ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit70ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 70ers ".format(num70ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit72ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 72ers ".format(num72ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit73ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 73ers ".format(num73ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit75ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 75ers ".format(num75ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit77ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 77ers ".format(num77ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit84ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 84ers ".format(num84ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit88ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 88ers ".format(num88ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit90ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 90ers ".format(num90ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit94ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 94ers ".format(num94ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit99ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 99ers ".format(num99ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit100ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 100ers ".format(num100ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit110ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 110ers ".format(num110ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit112ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 112ers ".format(num112ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit133ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 133ers ".format(num133ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit135ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 135ers ".format(num135ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit137ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 137ers ".format(num137ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit144ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 144ers ".format(num144ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit150ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 150ers ".format(num150ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit153ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 153ers ".format(num153ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit194ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 194ers ".format(num194ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit225ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 225ers ".format(num225ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit275ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 275ers ".format(num275ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit311ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 311ers ".format(num311ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit400ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 400ers ".format(num400ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit500ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 500ers ".format(num500ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit557ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 557ers ".format(num557ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit750ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 750ers ".format(num750ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit945ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 945ers ".format(num945ers)
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
                                                      planetData[i-1].geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed']
                                                      ))
                                PLMMUtils.log.debug("  planetData[{}] ({}): lon == {}, speed == {}".\
                                               format(i,
                                                      Ephemeris.datetimeToStr(planetData[i].dt),
                                                      planetData[i].geocentric[zodiacType]['longitude'],
                                                      planetData[i].geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed']
                                                      ))

                            if prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
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

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed < 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed > 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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
                    num7ers = totalDegrees / 7.0
                    num11ers = totalDegrees / 11.0
                    num12ers = totalDegrees / 12.0
                    num13ers = totalDegrees / 13.0
                    num15ers = totalDegrees / 15.0
                    num16ers = totalDegrees / 16.0
                    num18ers = totalDegrees / 18.0
                    num19ers = totalDegrees / 19.0
                    num22ers = totalDegrees / 22.0
                    num23ers = totalDegrees / 23.0
                    num24ers = totalDegrees / 24.0
                    num25ers = totalDegrees / 25.0
                    num29ers = totalDegrees / 29.0
                    num30ers = totalDegrees / 30.0
                    num31ers = totalDegrees / 31.0
                    num33ers = totalDegrees / 33.0
                    num34ers = totalDegrees / 34.0
                    num36ers = totalDegrees / 36.0
                    num37ers = totalDegrees / 37.0
                    num40ers = totalDegrees / 40.0
                    num42ers = totalDegrees / 42.0
                    num45ers = totalDegrees / 45.0
                    num47ers = totalDegrees / 47.0
                    num49ers = totalDegrees / 49.0
                    num50ers = totalDegrees / 50.0
                    num51ers = totalDegrees / 51.0
                    num51_428ers = totalDegrees / (360 / 7.0)
                    num52ers = totalDegrees / 52.0
                    num60ers = totalDegrees / 60.0
                    num69ers = totalDegrees / 69.0
                    num70ers = totalDegrees / 70.0
                    num72ers = totalDegrees / 72.0
                    num73ers = totalDegrees / 73.0
                    num75ers = totalDegrees / 75.0
                    num77ers = totalDegrees / 77.0
                    num84ers = totalDegrees / 84.0
                    num88ers = totalDegrees / 88.0
                    num90ers = totalDegrees / 90.0
                    num94ers = totalDegrees / 94.0
                    num99ers = totalDegrees / 99.0
                    num100ers = totalDegrees / 100.0
                    num110ers = totalDegrees / 110.0
                    num112ers = totalDegrees / 112.0
                    num133ers = totalDegrees / 133.0
                    num135ers = totalDegrees / 135.0
                    num137ers = totalDegrees / 137.0
                    num144ers = totalDegrees / 144.0
                    num150ers = totalDegrees / 150.0
                    num153ers = totalDegrees / 153.0
                    num194ers = totalDegrees / 194.0
                    num225ers = totalDegrees / 225.0
                    num275ers = totalDegrees / 275.0
                    num311ers = totalDegrees / 311.0
                    num400ers = totalDegrees / 400.0
                    num500ers = totalDegrees / 500.0
                    num557ers = totalDegrees / 557.0
                    num750ers = totalDegrees / 750.0
                    num945ers = totalDegrees / 945.0

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

                    if measurementUnit7ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 7ers ".format(num7ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit11ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 11ers ".format(num11ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit12ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 12ers ".format(num12ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit13ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 13ers ".format(num13ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit15ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 15ers ".format(num15ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit16ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 16ers ".format(num16ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit18ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 18ers ".format(num18ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit19ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 19ers ".format(num19ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit22ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 22ers ".format(num22ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit23ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 23ers ".format(num23ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit24ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 24ers ".format(num24ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit25ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 25ers ".format(num25ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit29ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 29ers ".format(num29ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit30ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 30ers ".format(num30ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit31ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 31ers ".format(num31ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit33ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 33ers ".format(num33ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit34ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 34ers ".format(num34ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit36ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 36ers ".format(num36ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit37ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 37ers ".format(num37ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit40ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 40ers ".format(num40ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit42ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 42ers ".format(num42ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit45ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 45ers ".format(num45ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit47ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 47ers ".format(num47ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit49ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 49ers ".format(num49ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit50ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 50ers ".format(num50ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51ers ".format(num51ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51_428ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51.428ers ".format(num51_428ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit52ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 52ers ".format(num52ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit60ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 60ers ".format(num60ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit69ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 69ers ".format(num69ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit70ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 70ers ".format(num70ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit72ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 72ers ".format(num72ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit73ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 73ers ".format(num73ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit75ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 75ers ".format(num75ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit77ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 77ers ".format(num77ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit84ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 84ers ".format(num84ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit88ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 88ers ".format(num88ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit90ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 90ers ".format(num90ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit94ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 94ers ".format(num94ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit99ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 99ers ".format(num99ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit100ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 100ers ".format(num100ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit110ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 110ers ".format(num110ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit112ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 112ers ".format(num112ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit133ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 133ers ".format(num133ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit135ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 135ers ".format(num135ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit137ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 137ers ".format(num137ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit144ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 144ers ".format(num144ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit150ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 150ers ".format(num150ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit153ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 153ers ".format(num153ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit194ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 194ers ".format(num194ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit225ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 225ers ".format(num225ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit275ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 275ers ".format(num275ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit311ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 311ers ".format(num311ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit400ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 400ers ".format(num400ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit500ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 500ers ".format(num500ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit557ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 557ers ".format(num557ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit750ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 750ers ".format(num750ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit945ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 945ers ".format(num945ers)
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

                            if prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed < 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed > 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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
                    num7ers = totalDegrees / 7.0
                    num11ers = totalDegrees / 11.0
                    num12ers = totalDegrees / 12.0
                    num13ers = totalDegrees / 13.0
                    num15ers = totalDegrees / 15.0
                    num16ers = totalDegrees / 16.0
                    num18ers = totalDegrees / 18.0
                    num19ers = totalDegrees / 19.0
                    num22ers = totalDegrees / 22.0
                    num23ers = totalDegrees / 23.0
                    num24ers = totalDegrees / 24.0
                    num25ers = totalDegrees / 25.0
                    num29ers = totalDegrees / 29.0
                    num30ers = totalDegrees / 30.0
                    num31ers = totalDegrees / 31.0
                    num33ers = totalDegrees / 33.0
                    num34ers = totalDegrees / 34.0
                    num36ers = totalDegrees / 36.0
                    num37ers = totalDegrees / 37.0
                    num40ers = totalDegrees / 40.0
                    num42ers = totalDegrees / 42.0
                    num45ers = totalDegrees / 45.0
                    num47ers = totalDegrees / 47.0
                    num49ers = totalDegrees / 49.0
                    num50ers = totalDegrees / 50.0
                    num51ers = totalDegrees / 51.0
                    num51_428ers = totalDegrees / (360 / 7.0)
                    num52ers = totalDegrees / 52.0
                    num60ers = totalDegrees / 60.0
                    num69ers = totalDegrees / 69.0
                    num70ers = totalDegrees / 70.0
                    num72ers = totalDegrees / 72.0
                    num73ers = totalDegrees / 73.0
                    num75ers = totalDegrees / 75.0
                    num77ers = totalDegrees / 77.0
                    num84ers = totalDegrees / 84.0
                    num88ers = totalDegrees / 88.0
                    num90ers = totalDegrees / 90.0
                    num94ers = totalDegrees / 94.0
                    num99ers = totalDegrees / 99.0
                    num100ers = totalDegrees / 100.0
                    num110ers = totalDegrees / 110.0
                    num112ers = totalDegrees / 112.0
                    num133ers = totalDegrees / 133.0
                    num135ers = totalDegrees / 135.0
                    num137ers = totalDegrees / 137.0
                    num144ers = totalDegrees / 144.0
                    num150ers = totalDegrees / 150.0
                    num153ers = totalDegrees / 153.0
                    num194ers = totalDegrees / 194.0
                    num225ers = totalDegrees / 225.0
                    num275ers = totalDegrees / 275.0
                    num311ers = totalDegrees / 311.0
                    num400ers = totalDegrees / 400.0
                    num500ers = totalDegrees / 500.0
                    num557ers = totalDegrees / 557.0
                    num750ers = totalDegrees / 750.0
                    num945ers = totalDegrees / 945.0

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

                    if measurementUnit7ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 7ers ".format(num7ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit11ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 11ers ".format(num11ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit12ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 12ers ".format(num12ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit13ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 13ers ".format(num13ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit15ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 15ers ".format(num15ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit16ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 16ers ".format(num16ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit18ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 18ers ".format(num18ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit19ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 19ers ".format(num19ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit22ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 22ers ".format(num22ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit23ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 23ers ".format(num23ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit24ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 24ers ".format(num24ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit25ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 25ers ".format(num25ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit29ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 29ers ".format(num29ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit30ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 30ers ".format(num30ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit31ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 31ers ".format(num31ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit33ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 33ers ".format(num33ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit34ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 34ers ".format(num34ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit36ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 36ers ".format(num36ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit37ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 37ers ".format(num37ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit40ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 40ers ".format(num40ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit42ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 42ers ".format(num42ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit45ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 45ers ".format(num45ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit47ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 47ers ".format(num47ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit49ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 49ers ".format(num49ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit50ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 50ers ".format(num50ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51ers ".format(num51ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51_428ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51.428ers ".format(num51_428ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit52ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 52ers ".format(num52ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit60ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 60ers ".format(num60ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit69ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 69ers ".format(num69ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit70ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 70ers ".format(num70ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit72ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 72ers ".format(num72ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit73ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 73ers ".format(num73ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit75ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 75ers ".format(num75ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit77ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 77ers ".format(num77ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit84ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 84ers ".format(num84ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit88ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 88ers ".format(num88ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit90ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 90ers ".format(num90ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit94ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 94ers ".format(num94ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit99ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 99ers ".format(num99ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit100ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 100ers ".format(num100ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit110ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 110ers ".format(num110ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit112ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 112ers ".format(num112ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit133ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 133ers ".format(num133ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit135ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 135ers ".format(num135ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit137ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 137ers ".format(num137ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit144ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 144ers ".format(num144ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit150ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 150ers ".format(num150ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit153ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 153ers ".format(num153ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit194ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 194ers ".format(num194ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit225ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 225ers ".format(num225ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit275ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 275ers ".format(num275ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit311ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 311ers ".format(num311ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit400ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 400ers ".format(num400ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit500ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 500ers ".format(num500ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit557ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 557ers ".format(num557ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit750ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 750ers ".format(num750ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit945ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 945ers ".format(num945ers)
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

                            if prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed < 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed > 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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
                    num7ers = totalDegrees / 7.0
                    num11ers = totalDegrees / 11.0
                    num12ers = totalDegrees / 12.0
                    num13ers = totalDegrees / 13.0
                    num15ers = totalDegrees / 15.0
                    num16ers = totalDegrees / 16.0
                    num18ers = totalDegrees / 18.0
                    num19ers = totalDegrees / 19.0
                    num22ers = totalDegrees / 22.0
                    num23ers = totalDegrees / 23.0
                    num24ers = totalDegrees / 24.0
                    num25ers = totalDegrees / 25.0
                    num29ers = totalDegrees / 29.0
                    num30ers = totalDegrees / 30.0
                    num31ers = totalDegrees / 31.0
                    num33ers = totalDegrees / 33.0
                    num34ers = totalDegrees / 34.0
                    num36ers = totalDegrees / 36.0
                    num37ers = totalDegrees / 37.0
                    num40ers = totalDegrees / 40.0
                    num42ers = totalDegrees / 42.0
                    num45ers = totalDegrees / 45.0
                    num47ers = totalDegrees / 47.0
                    num49ers = totalDegrees / 49.0
                    num50ers = totalDegrees / 50.0
                    num51ers = totalDegrees / 51.0
                    num51_428ers = totalDegrees / (360 / 7.0)
                    num52ers = totalDegrees / 52.0
                    num60ers = totalDegrees / 60.0
                    num69ers = totalDegrees / 69.0
                    num70ers = totalDegrees / 70.0
                    num72ers = totalDegrees / 72.0
                    num73ers = totalDegrees / 73.0
                    num75ers = totalDegrees / 75.0
                    num77ers = totalDegrees / 77.0
                    num84ers = totalDegrees / 84.0
                    num88ers = totalDegrees / 88.0
                    num90ers = totalDegrees / 90.0
                    num94ers = totalDegrees / 94.0
                    num99ers = totalDegrees / 99.0
                    num100ers = totalDegrees / 100.0
                    num110ers = totalDegrees / 110.0
                    num112ers = totalDegrees / 112.0
                    num133ers = totalDegrees / 133.0
                    num135ers = totalDegrees / 135.0
                    num137ers = totalDegrees / 137.0
                    num144ers = totalDegrees / 144.0
                    num150ers = totalDegrees / 150.0
                    num153ers = totalDegrees / 153.0
                    num194ers = totalDegrees / 194.0
                    num225ers = totalDegrees / 225.0
                    num275ers = totalDegrees / 275.0
                    num311ers = totalDegrees / 311.0
                    num400ers = totalDegrees / 400.0
                    num500ers = totalDegrees / 500.0
                    num557ers = totalDegrees / 557.0
                    num750ers = totalDegrees / 750.0
                    num945ers = totalDegrees / 945.0

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

                    if measurementUnit7ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 7ers ".format(num7ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit11ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 11ers ".format(num11ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit12ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 12ers ".format(num12ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit13ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 13ers ".format(num13ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit15ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 15ers ".format(num15ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit16ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 16ers ".format(num16ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit18ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 18ers ".format(num18ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit19ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 19ers ".format(num19ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit22ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 22ers ".format(num22ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit23ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 23ers ".format(num23ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit24ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 24ers ".format(num24ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit25ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 25ers ".format(num25ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit29ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 29ers ".format(num29ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit30ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 30ers ".format(num30ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit31ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 31ers ".format(num31ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit33ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 33ers ".format(num33ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit34ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 34ers ".format(num34ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit36ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 36ers ".format(num36ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit37ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 37ers ".format(num37ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit40ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 40ers ".format(num40ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit42ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 42ers ".format(num42ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit45ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 45ers ".format(num45ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit47ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 47ers ".format(num47ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit49ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 49ers ".format(num49ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit50ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 50ers ".format(num50ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51ers ".format(num51ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51_428ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51.428ers ".format(num51_428ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit52ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 52ers ".format(num52ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit60ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 60ers ".format(num60ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit69ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 69ers ".format(num69ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit70ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 70ers ".format(num70ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit72ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 72ers ".format(num72ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit73ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 73ers ".format(num73ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit75ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 75ers ".format(num75ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit77ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 77ers ".format(num77ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit84ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 84ers ".format(num84ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit88ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 88ers ".format(num88ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit90ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 90ers ".format(num90ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit94ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 94ers ".format(num94ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit99ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 99ers ".format(num99ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit100ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 100ers ".format(num100ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit110ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 110ers ".format(num110ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit112ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 112ers ".format(num112ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit133ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 133ers ".format(num133ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit135ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 135ers ".format(num135ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit137ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 137ers ".format(num137ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit144ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 144ers ".format(num144ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit150ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 150ers ".format(num150ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit153ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 153ers ".format(num153ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit194ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 194ers ".format(num194ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit225ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 225ers ".format(num225ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit275ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 275ers ".format(num275ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit311ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 311ers ".format(num311ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit400ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 400ers ".format(num400ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit500ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 500ers ".format(num500ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit557ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 557ers ".format(num557ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit750ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 750ers ".format(num750ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit945ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 945ers ".format(num945ers)
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

                            if prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                                # Direct motion.
                                # Elapsed amount for this segment should be positive.

                                # Find the amount of longitude elasped.
                                longitudeElapsed = \
                                    currPi.geocentric[zodiacType]['longitude'] - \
                                    prevPi.geocentric[zodiacType]['longitude']

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed < 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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

                                # Protect against bad data from the Swiss
                                # Ephemeris when doing calculations with
                                # TrueNorthNode or TrueSouthNode.
                                # For an example of bad data observed, please see method:
                                #   test_planetlongitudemovementmeasurement_calc.PLMMUtilsTestCase.testGeocentricTrueNorthNodeMovementMultipleRevolutions()
                                if (planetName == "TrueNorthNode" or planetName == "TrueSouthNode") and \
                                    prevPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    currPi.geocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] < 0 and \
                                    not ( \
                                    (0 <= prevPi.geocentric[zodiacType]['longitude'] < 1 and \
                                    359 < currPi.geocentric[zodiacType]['longitude'] < 360) \
                                    or  \
                                    (359 < prevPi.geocentric[zodiacType]['longitude'] < 360 and \
                                    0 <= currPi.geocentric[zodiacType]['longitude'] < 1) \
                                    ) \
                                    and \
                                    longitudeElapsed > 0:

                                    if PLMMUtils.log.isEnabledFor(logging.DEBUG) == True:
                                        PLMMUtils.log.debug("longitudeElapsed == {}".format(longitudeElapsed))
                                        PLMMUtils.log.debug("Skipping append for this iteration.")
                                    continue

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
                    num7ers = totalDegrees / 7.0
                    num11ers = totalDegrees / 11.0
                    num12ers = totalDegrees / 12.0
                    num13ers = totalDegrees / 13.0
                    num15ers = totalDegrees / 15.0
                    num16ers = totalDegrees / 16.0
                    num18ers = totalDegrees / 18.0
                    num19ers = totalDegrees / 19.0
                    num22ers = totalDegrees / 22.0
                    num23ers = totalDegrees / 23.0
                    num24ers = totalDegrees / 24.0
                    num25ers = totalDegrees / 25.0
                    num29ers = totalDegrees / 29.0
                    num30ers = totalDegrees / 30.0
                    num31ers = totalDegrees / 31.0
                    num33ers = totalDegrees / 33.0
                    num34ers = totalDegrees / 34.0
                    num36ers = totalDegrees / 36.0
                    num37ers = totalDegrees / 37.0
                    num40ers = totalDegrees / 40.0
                    num42ers = totalDegrees / 42.0
                    num45ers = totalDegrees / 45.0
                    num47ers = totalDegrees / 47.0
                    num49ers = totalDegrees / 49.0
                    num50ers = totalDegrees / 50.0
                    num51ers = totalDegrees / 51.0
                    num51_428ers = totalDegrees / (360 / 7.0)
                    num52ers = totalDegrees / 52.0
                    num60ers = totalDegrees / 60.0
                    num69ers = totalDegrees / 69.0
                    num70ers = totalDegrees / 70.0
                    num72ers = totalDegrees / 72.0
                    num73ers = totalDegrees / 73.0
                    num75ers = totalDegrees / 75.0
                    num77ers = totalDegrees / 77.0
                    num84ers = totalDegrees / 84.0
                    num88ers = totalDegrees / 88.0
                    num90ers = totalDegrees / 90.0
                    num94ers = totalDegrees / 94.0
                    num99ers = totalDegrees / 99.0
                    num100ers = totalDegrees / 100.0
                    num110ers = totalDegrees / 110.0
                    num112ers = totalDegrees / 112.0
                    num133ers = totalDegrees / 133.0
                    num135ers = totalDegrees / 135.0
                    num137ers = totalDegrees / 137.0
                    num144ers = totalDegrees / 144.0
                    num150ers = totalDegrees / 150.0
                    num153ers = totalDegrees / 153.0
                    num194ers = totalDegrees / 194.0
                    num225ers = totalDegrees / 225.0
                    num275ers = totalDegrees / 275.0
                    num311ers = totalDegrees / 311.0
                    num400ers = totalDegrees / 400.0
                    num500ers = totalDegrees / 500.0
                    num557ers = totalDegrees / 557.0
                    num750ers = totalDegrees / 750.0
                    num945ers = totalDegrees / 945.0

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

                    if measurementUnit7ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 7ers ".format(num7ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit11ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 11ers ".format(num11ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit12ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 12ers ".format(num12ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit13ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 13ers ".format(num13ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit15ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 15ers ".format(num15ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit16ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 16ers ".format(num16ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit18ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 18ers ".format(num18ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit19ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 19ers ".format(num19ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit22ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 22ers ".format(num22ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit23ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 23ers ".format(num23ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit24ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 24ers ".format(num24ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit25ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 25ers ".format(num25ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit29ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 29ers ".format(num29ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit30ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 30ers ".format(num30ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit31ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 31ers ".format(num31ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit33ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 33ers ".format(num33ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit34ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 34ers ".format(num34ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit36ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 36ers ".format(num36ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit37ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 37ers ".format(num37ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit40ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 40ers ".format(num40ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit42ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 42ers ".format(num42ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit45ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 45ers ".format(num45ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit47ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 47ers ".format(num47ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit49ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 49ers ".format(num49ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit50ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 50ers ".format(num50ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51ers ".format(num51ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit51_428ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 51.428ers ".format(num51_428ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit52ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 52ers ".format(num52ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit60ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 60ers ".format(num60ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit69ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 69ers ".format(num69ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit70ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 70ers ".format(num70ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit72ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 72ers ".format(num72ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit73ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 73ers ".format(num73ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit75ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 75ers ".format(num75ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit77ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 77ers ".format(num77ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit84ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 84ers ".format(num84ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit88ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 88ers ".format(num88ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit90ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 90ers ".format(num90ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit94ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 94ers ".format(num94ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit99ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 99ers ".format(num99ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit100ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 100ers ".format(num100ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit110ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 110ers ".format(num110ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit112ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 112ers ".format(num112ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit133ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 133ers ".format(num133ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit135ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 135ers ".format(num135ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit137ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 137ers ".format(num137ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit144ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 144ers ".format(num144ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit150ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 150ers ".format(num150ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit153ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 153ers ".format(num153ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit194ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 194ers ".format(num194ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit225ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 225ers ".format(num225ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit275ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 275ers ".format(num275ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit311ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 311ers ".format(num311ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit400ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 400ers ".format(num400ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit500ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 500ers ".format(num500ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit557ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 557ers ".format(num557ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit750ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 750ers ".format(num750ers)
                        atLeastOneMeasurementAlreadyAddedFlag = True

                    if measurementUnit945ersEnabled == True:
                        if atLeastOneMeasurementAlreadyAddedFlag == True:
                            line += "or "
                        line += "{:.3f} 945ers ".format(num945ers)
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

                        if prevPi.heliocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
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
                num7ers = totalDegrees / 7.0
                num11ers = totalDegrees / 11.0
                num12ers = totalDegrees / 12.0
                num13ers = totalDegrees / 13.0
                num15ers = totalDegrees / 15.0
                num16ers = totalDegrees / 16.0
                num18ers = totalDegrees / 18.0
                num19ers = totalDegrees / 19.0
                num22ers = totalDegrees / 22.0
                num23ers = totalDegrees / 23.0
                num24ers = totalDegrees / 24.0
                num25ers = totalDegrees / 25.0
                num29ers = totalDegrees / 29.0
                num30ers = totalDegrees / 30.0
                num31ers = totalDegrees / 31.0
                num33ers = totalDegrees / 33.0
                num34ers = totalDegrees / 34.0
                num36ers = totalDegrees / 36.0
                num37ers = totalDegrees / 37.0
                num40ers = totalDegrees / 40.0
                num42ers = totalDegrees / 42.0
                num45ers = totalDegrees / 45.0
                num47ers = totalDegrees / 47.0
                num49ers = totalDegrees / 49.0
                num50ers = totalDegrees / 50.0
                num51ers = totalDegrees / 51.0
                num51_428ers = totalDegrees / (360 / 7.0)
                num52ers = totalDegrees / 52.0
                num60ers = totalDegrees / 60.0
                num69ers = totalDegrees / 69.0
                num70ers = totalDegrees / 70.0
                num72ers = totalDegrees / 72.0
                num73ers = totalDegrees / 73.0
                num75ers = totalDegrees / 75.0
                num77ers = totalDegrees / 77.0
                num84ers = totalDegrees / 84.0
                num88ers = totalDegrees / 88.0
                num90ers = totalDegrees / 90.0
                num94ers = totalDegrees / 94.0
                num99ers = totalDegrees / 99.0
                num100ers = totalDegrees / 100.0
                num110ers = totalDegrees / 110.0
                num112ers = totalDegrees / 112.0
                num133ers = totalDegrees / 133.0
                num135ers = totalDegrees / 135.0
                num137ers = totalDegrees / 137.0
                num144ers = totalDegrees / 144.0
                num150ers = totalDegrees / 150.0
                num153ers = totalDegrees / 153.0
                num194ers = totalDegrees / 194.0
                num225ers = totalDegrees / 225.0
                num275ers = totalDegrees / 275.0
                num311ers = totalDegrees / 311.0
                num400ers = totalDegrees / 400.0
                num500ers = totalDegrees / 500.0
                num557ers = totalDegrees / 557.0
                num750ers = totalDegrees / 750.0
                num945ers = totalDegrees / 945.0

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

                if measurementUnit7ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 7ers ".format(num7ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit11ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 11ers ".format(num11ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit12ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 12ers ".format(num12ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit13ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 13ers ".format(num13ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit15ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 15ers ".format(num15ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit16ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 16ers ".format(num16ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit18ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 18ers ".format(num18ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit19ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 19ers ".format(num19ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit22ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 22ers ".format(num22ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit23ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 23ers ".format(num23ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit24ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 24ers ".format(num24ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit25ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 25ers ".format(num25ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit29ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 29ers ".format(num29ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit30ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 30ers ".format(num30ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit31ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 31ers ".format(num31ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit33ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 33ers ".format(num33ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit34ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 34ers ".format(num34ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit36ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 36ers ".format(num36ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit37ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 37ers ".format(num37ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit40ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 40ers ".format(num40ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit42ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 42ers ".format(num42ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit45ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 45ers ".format(num45ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit47ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 47ers ".format(num47ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit49ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 49ers ".format(num49ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit50ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 50ers ".format(num50ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit51ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 51ers ".format(num51ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit51_428ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 51.428ers ".format(num51_428ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit52ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 52ers ".format(num52ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit60ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 60ers ".format(num60ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit69ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 69ers ".format(num69ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit70ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 70ers ".format(num70ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit72ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 72ers ".format(num72ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit73ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 73ers ".format(num73ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit75ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 75ers ".format(num75ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit77ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 77ers ".format(num77ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit84ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 84ers ".format(num84ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit88ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 88ers ".format(num88ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit90ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 90ers ".format(num90ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit94ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 94ers ".format(num94ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit99ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 99ers ".format(num99ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit100ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 100ers ".format(num100ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit110ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 110ers ".format(num110ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit112ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 112ers ".format(num112ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit133ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 133ers ".format(num133ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit135ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 135ers ".format(num135ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit137ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 137ers ".format(num137ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit144ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 144ers ".format(num144ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit150ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 150ers ".format(num150ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit153ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 153ers ".format(num153ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit194ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 194ers ".format(num194ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit225ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 225ers ".format(num225ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit275ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 275ers ".format(num275ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit311ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 311ers ".format(num311ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit400ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 400ers ".format(num400ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit500ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 500ers ".format(num500ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit557ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 557ers ".format(num557ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit750ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 750ers ".format(num750ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit945ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 945ers ".format(num945ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                text += line + os.linesep

            if siderealZodiacFlag == True:
                totalDegrees = 0
                zodiacType = "sidereal"

                for i in range(len(planetData)):
                    if i != 0:
                        prevPi = planetData[i-1]
                        currPi = planetData[i]

                        if prevPi.heliocentric[PLMMUtils.longitudeTypeForLongitudeSpeed]['longitude_speed'] >= 0:
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
                num7ers = totalDegrees / 7.0
                num11ers = totalDegrees / 11.0
                num12ers = totalDegrees / 12.0
                num13ers = totalDegrees / 13.0
                num15ers = totalDegrees / 15.0
                num16ers = totalDegrees / 16.0
                num18ers = totalDegrees / 18.0
                num19ers = totalDegrees / 19.0
                num22ers = totalDegrees / 22.0
                num23ers = totalDegrees / 23.0
                num24ers = totalDegrees / 24.0
                num25ers = totalDegrees / 25.0
                num29ers = totalDegrees / 29.0
                num30ers = totalDegrees / 30.0
                num31ers = totalDegrees / 31.0
                num33ers = totalDegrees / 33.0
                num34ers = totalDegrees / 34.0
                num36ers = totalDegrees / 36.0
                num37ers = totalDegrees / 37.0
                num40ers = totalDegrees / 40.0
                num42ers = totalDegrees / 42.0
                num45ers = totalDegrees / 45.0
                num47ers = totalDegrees / 47.0
                num49ers = totalDegrees / 49.0
                num50ers = totalDegrees / 50.0
                num51ers = totalDegrees / 51.0
                num51_428ers = totalDegrees / (360 / 7.0)
                num52ers = totalDegrees / 52.0
                num60ers = totalDegrees / 60.0
                num69ers = totalDegrees / 69.0
                num70ers = totalDegrees / 70.0
                num72ers = totalDegrees / 72.0
                num73ers = totalDegrees / 73.0
                num75ers = totalDegrees / 75.0
                num77ers = totalDegrees / 77.0
                num84ers = totalDegrees / 84.0
                num88ers = totalDegrees / 88.0
                num90ers = totalDegrees / 90.0
                num94ers = totalDegrees / 94.0
                num99ers = totalDegrees / 99.0
                num100ers = totalDegrees / 100.0
                num110ers = totalDegrees / 110.0
                num112ers = totalDegrees / 112.0
                num133ers = totalDegrees / 133.0
                num135ers = totalDegrees / 135.0
                num137ers = totalDegrees / 137.0
                num144ers = totalDegrees / 144.0
                num150ers = totalDegrees / 150.0
                num153ers = totalDegrees / 153.0
                num194ers = totalDegrees / 194.0
                num225ers = totalDegrees / 225.0
                num275ers = totalDegrees / 275.0
                num311ers = totalDegrees / 311.0
                num400ers = totalDegrees / 400.0
                num500ers = totalDegrees / 500.0
                num557ers = totalDegrees / 557.0
                num750ers = totalDegrees / 750.0
                num945ers = totalDegrees / 945.0

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

                if measurementUnit7ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 7ers ".format(num7ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit11ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 11ers ".format(num11ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit12ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 12ers ".format(num12ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit13ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 13ers ".format(num13ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit15ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 15ers ".format(num15ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit16ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 16ers ".format(num16ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit18ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 18ers ".format(num18ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit19ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 19ers ".format(num19ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit22ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 22ers ".format(num22ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit23ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 23ers ".format(num23ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit24ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 24ers ".format(num24ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit25ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 25ers ".format(num25ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit29ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 29ers ".format(num29ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit30ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 30ers ".format(num30ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit31ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 31ers ".format(num31ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit33ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 33ers ".format(num33ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit34ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 34ers ".format(num34ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit36ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 36ers ".format(num36ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit37ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 37ers ".format(num37ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit40ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 40ers ".format(num40ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit42ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 42ers ".format(num42ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit45ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 45ers ".format(num45ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit47ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 47ers ".format(num47ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit49ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 49ers ".format(num49ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit50ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 50ers ".format(num50ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit51ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 51ers ".format(num51ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit51_428ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 51.428ers ".format(num51_428ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit52ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 52ers ".format(num52ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit60ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 60ers ".format(num60ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit69ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 69ers ".format(num69ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit70ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 70ers ".format(num70ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit72ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 72ers ".format(num72ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit73ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 73ers ".format(num73ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit75ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 75ers ".format(num75ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit77ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 77ers ".format(num77ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit84ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 84ers ".format(num84ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit88ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 88ers ".format(num88ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit90ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 90ers ".format(num90ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit94ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 94ers ".format(num94ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit99ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 99ers ".format(num99ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit100ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 100ers ".format(num100ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit110ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 110ers ".format(num110ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit112ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 112ers ".format(num112ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit133ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 133ers ".format(num133ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit135ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 135ers ".format(num135ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit137ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 137ers ".format(num137ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit144ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 144ers ".format(num144ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit150ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 150ers ".format(num150ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit153ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 153ers ".format(num153ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit194ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 194ers ".format(num194ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit225ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 225ers ".format(num225ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit275ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 275ers ".format(num275ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit311ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 311ers ".format(num311ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit400ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 400ers ".format(num400ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit500ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 500ers ".format(num500ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit557ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 557ers ".format(num557ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit750ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 750ers ".format(num750ers)
                    atLeastOneMeasurementAlreadyAddedFlag = True

                if measurementUnit945ersEnabled == True:
                    if atLeastOneMeasurementAlreadyAddedFlag == True:
                        line += "or "
                    line += "{:.3f} 945ers ".format(num945ers)
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
            elif planetName == "SunTrueNorthNode":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "SunTrueSouthNode":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "MoonTrueNorthNode":
                stepSizeTd = datetime.timedelta(days=4)
            elif planetName == "MoonTrueSouthNode":
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
            elif planetName == "SunTrueNorthNode":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "SunTrueSouthNode":
                stepSizeTd = datetime.timedelta(days=5)
            elif planetName == "MoonTrueNorthNode":
                stepSizeTd = datetime.timedelta(days=4)
            elif planetName == "MoonTrueSouthNode":
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
    # Logging config file specifies the log filename relative to
    # the current directory, so we need to chdir to the SRC_DIR
    # before loading the logging config.
    thisScriptDir = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = thisScriptDir
    os.chdir(SRC_DIR)
    LOG_CONFIG_FILE = \
        os.path.abspath(os.path.join(SRC_DIR, "../conf/logging.conf"))
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
        pass

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
