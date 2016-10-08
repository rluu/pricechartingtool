
# For logging.
import logging
import logging.config

import inspect
import datetime
import copy

import pytz

from util import Util
from ephemeris import PlanetaryInfo
from ephemeris import Ephemeris


class EphemerisUtils:
    """Class that contains some utility methods for calculating the
    datetimes and degrees of commonly referenced astronomical phenomena.

    Preconditions:
    These methods assume that the Ephemeris is initialized and the
    geographic position is set already.

    TODO_rluu_20160903: The original methods from which this class was
    created/based on was written a while
    ago and so they may not have the most optimal step sizes.
    I may want to add a method to this class like I did
    in src/lookbackmultiple_calc.py with method _getOptimalStepSizeTd() or
    in src/planetlongitudemovementmeasurement_calc.py with method
    _getOptimalStepSizeTd().
    """

    # Logger object for this class.
    log = logging.getLogger("ephemeris_utils.EphemerisUtils")

    @staticmethod
    def getLongitudeAspectTimestamps(\
        startDt,
        endDt,
        planet1ParamsList,
        planet2ParamsList,
        degreeDifference,
        uniDirectionalAspectsFlag=False,
        maxErrorTd=datetime.timedelta(seconds=1)):
        """Obtains a list of datetime.datetime objects that contain
        the moments when the aspect specified is active.

        Warning on usage:
        When planet-longitude-averaging is utilized for the longitude
        of planet1 or planet2, the aspects returned by this function
        cannot be fully relied upon.

        This short-coming happens under these circumstances because it
        is possible that the longitude can abruptly 'jump' or hop a
        large distance when measurements are taken between timestamp
        steps.

        For example, this 'jumping' effect can occur if two planets A
        and B, are both around 355 degrees, and planet A crosses the 0
        degree mark.  Now the average goes from around 355 degrees
        (355 + 355 = 710 / 2 = 355), to about 180 degrees (355 + 0 =
        355 / 2 = about 180).

        While corrections for this can be made for the case of having
        only 2 planets involved, if more planets are involved then the
        adjustment required quickly becomes non-trivial.

        Preconditions:
        This method assumes that the Ephemeris has been initialized and the
        geographic position has been set already.

        Arguments:
        pcdd      - PriceChartDocumentData object that will be modified.
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.

        planet1ParamsList - List of tuples that will be used as parameters
                      for planet1.  Each tuple contained in this list
                      represents parameters for each planet that will
                      get averaged to create what is known as planet1.

                      The contents of the tuple are:
                      (planetName, centricityType, longitudeType)

                      Where:
                      planetName - str holding the name of the second
                                   planet to do the calculations for.
                      centricityType - str value holding either "geocentric",
                                       "topocentric", or "heliocentric".
                      longitudeType - str value holding either
                                      "tropical" or "sidereal".

                      Example: So if someone wanted planet1 to be the
                      average location of of geocentric sidereal
                      Saturn and geocentric sidereal Uranus, the
                      'planet1ParamsList' parameter would be:

                      [("Saturn", "geocentric", "sidereal"),
                       ("Uranus", "geocentric", "sidereal")]

                      If the typical use-case is desired for the
                      longitude of just a single planet, pass a list
                      with only 1 tuple.  As an example, for Mercury
                      it would be:

                      [("Mercury", "heliocentric", "tropical")]

        planet2ParamsList - List of tuples that will be used as parameters
                      for planet2.  For additional details about the
                      format of this parameter field, please see the
                      description for parameter 'planet1ParamsList'

        degreeDifference - float value for the number of degrees of
                           separation for this aspect.

        uniDirectionalAspectsFlag - bool value for whether or not
                     uni-directional aspects are enabled or not.  By
                     default, aspects are bi-directional, so Saturn
                     square-aspect Jupiter would be the same as
                     Jupiter square-aspect Saturn.  If this flag is
                     set to True, then those two combinations would be
                     considered unique.  In the case where the flag is
                     set to True, for the aspect to be active,
                     planet2 would need to be 'degreeDifference'
                     degrees in front of planet1.

        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.

        Returns:

        List of datetime.datetime objects.  Each timestamp in the list
        is the moment where the aspect is active and satisfies the
        given parameters.  In the event of an error, the reference
        None is returned.
        """

        EphemerisUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")

        # List of timestamps of the aspects found.
        aspectTimestamps = []

        # Make sure the inputs are valid.
        if endDt < startDt:
            errMsg = "Invalid input: 'endDt' must be after 'startDt'"
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Check to make sure planet lists were given.
        if len(planet1ParamsList) == 0:
            errMsg = "planet1ParamsList must contain at least 1 tuple."
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)
        if len(planet2ParamsList) == 0:
            errMsg = "planet2ParamsList must contain at least 1 tuple."
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        EphemerisUtils.log.debug("planet1ParamsList passed in is: {}".\
                  format(planet1ParamsList))
        EphemerisUtils.log.debug("planet2ParamsList passed in is: {}".\
                  format(planet2ParamsList))

        # Check for valid inputs in each of the planet parameter lists.
        for planetTuple in planet1ParamsList + planet2ParamsList:
            if len(planetTuple) != 3:
                errMsg = "Input error: " + \
                          "Not enough values given in planet tuple."
                EphemerisUtils.log.error(errMsg)
                raise ValueError(errMsg)

            planetName = planetTuple[0]
            centricityType = planetTuple[1]
            longitudeType = planetTuple[2]

            loweredCentricityType = centricityType.lower()
            if loweredCentricityType != "geocentric" and \
                loweredCentricityType != "topocentric" and \
                loweredCentricityType != "heliocentric":

                errMsg = "Invalid input: Centricity type is invalid.  " + \
                    "Value given was: {}".format(centricityType)
                EphemerisUtils.log.error(errMsg)
                raise ValueError(errMsg)

            # Check inputs for longitude type.
            loweredLongitudeType = longitudeType.lower()
            if loweredLongitudeType != "tropical" and \
                loweredLongitudeType != "sidereal":

                errMsg = "Invalid input: Longitude type is invalid.  " + \
                    "Value given was: {}".format(longitudeType)
                EphemerisUtils.log.error(errMsg)
                raise ValueError(errMsg)

        # Field name we are getting.
        fieldName = "longitude"

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        for planetTuple in planet1ParamsList + planet2ParamsList:
            planetName = planetTuple[0]

            if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

                # House cusps and ascmc planets need a smaller step size.
                stepSizeTd = datetime.timedelta(hours=1)
            elif planetName == "Moon":
                # Use a smaller step size for the moon so we can catch
                # smaller aspect sizes.
                stepSizeTd = datetime.timedelta(hours=3)

        EphemerisUtils.log.debug("Step size is: {}".format(stepSizeTd))

        # Desired angles.  We need to check for planets at these angles.
        desiredAngleDegList = []

        desiredAngleDeg1 = Util.toNormalizedAngle(degreeDifference)
        desiredAngleDegList.append(desiredAngleDeg1)
        if Util.fuzzyIsEqual(desiredAngleDeg1, 0):
            desiredAngleDegList.append(360)

        if uniDirectionalAspectsFlag == False:
            desiredAngleDeg2 = \
                360 - Util.toNormalizedAngle(degreeDifference)
            if desiredAngleDeg2 not in desiredAngleDegList:
                desiredAngleDegList.append(desiredAngleDeg2)

        # Debug output.
        anglesStr = ""
        for angle in desiredAngleDegList:
            anglesStr += "{} ".format(angle)
        EphemerisUtils.log.debug("Angles in desiredAngleDegList: " + anglesStr)

        # Iterate through, appending to aspectTimestamps list as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudesP1 = []
        longitudesP1.append(None)
        longitudesP1.append(None)

        longitudesP2 = []
        longitudesP2.append(None)
        longitudesP2.append(None)

        def getFieldValue(dt, planetParamsList, fieldName):
            """Creates the PlanetaryInfo object for the given
            planetParamsList and returns the value of the field
            desired.
            """

            EphemerisUtils.log.debug("planetParamsList passed in is: {}".\
                      format(planetParamsList))

            unAveragedFieldValues = []

            for t in planetParamsList:
                planetName = t[0]
                centricityType = t[1]
                longitudeType = t[2]

                pi = Ephemeris.getPlanetaryInfo(planetName, dt)

                EphemerisUtils.log.debug("Planet {} has geo sid longitude: {}".\
                          format(planetName,
                                 pi.geocentric["sidereal"]["longitude"]))

                fieldValue = None

                if centricityType.lower() == "geocentric":
                    fieldValue = pi.geocentric[longitudeType][fieldName]
                elif centricityType.lower() == "topocentric":
                    fieldValue = pi.topocentric[longitudeType][fieldName]
                elif centricityType.lower() == "heliocentric":
                    fieldValue = pi.heliocentric[longitudeType][fieldName]
                else:
                    EphemerisUtils.log.error("Unknown centricity type: {}".\
                              format(centricityType))
                    fieldValue = None

                unAveragedFieldValues.append(fieldValue)

            EphemerisUtils.log.debug("unAveragedFieldValues is: {}".\
                      format(unAveragedFieldValues))

            # Average the field values.
            total = 0.0
            for v in unAveragedFieldValues:
                total += v
            averagedFieldValue = total / len(unAveragedFieldValues)

            EphemerisUtils.log.debug("averagedFieldValue is: {}".\
                      format(averagedFieldValue))

            return averagedFieldValue

        EphemerisUtils.log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        currDiff = None
        prevDiff = None


        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]

            EphemerisUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            longitudesP1[-1] = \
                Util.toNormalizedAngle(\
                getFieldValue(currDt, planet1ParamsList, fieldName))
            longitudesP2[-1] = \
                Util.toNormalizedAngle(\
                getFieldValue(currDt, planet2ParamsList, fieldName))

            EphemerisUtils.log.debug("{} {} is: {}".\
                      format(planet1ParamsList, fieldName,
                             longitudesP1[-1]))
            EphemerisUtils.log.debug("{} {} is: {}".\
                      format(planet2ParamsList, fieldName,
                             longitudesP2[-1]))

            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - longitudesP2[-1])

            EphemerisUtils.log.debug("prevDiff == {}".format(prevDiff))
            EphemerisUtils.log.debug("currDiff == {}".format(currDiff))

            if prevDiff != None and \
                   longitudesP1[-2] != None and \
                   longitudesP2[-2] != None:

                if abs(prevDiff - currDiff) > 180:
                    # Probably crossed over 0.  Adjust the prevDiff so
                    # that the rest of the algorithm can continue to
                    # work.
                    if prevDiff > currDiff:
                        prevDiff -= 360
                    else:
                        prevDiff += 360

                    EphemerisUtils.log.debug("After adjustment: prevDiff == {}".\
                              format(prevDiff))
                    EphemerisUtils.log.debug("After adjustment: currDiff == {}".\
                              format(currDiff))

                for desiredAngleDeg in desiredAngleDegList:
                    EphemerisUtils.log.debug("Looking at desiredAngleDeg: {}".\
                              format(desiredAngleDeg))

                    desiredDegree = desiredAngleDeg

                    if prevDiff < desiredDegree and currDiff >= desiredDegree:
                        EphemerisUtils.log.debug("Crossed over {} from below to above!".\
                                  format(desiredDegree))

                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1

                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            EphemerisUtils.log.debug("Refining between {} and {}".\
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

                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1ParamsList, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet2ParamsList, fieldName))

                            EphemerisUtils.log.debug("testValueP1 == {}".format(testValueP1))
                            EphemerisUtils.log.debug("testValueP2 == {}".format(testValueP2))

                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360

                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360

                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)

                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360

                            EphemerisUtils.log.debug("testDiff == {}".format(testDiff))

                            if testDiff < desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt

                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff

                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2

                            currErrorTd = t2 - t1

                        # Update our lists.
                        steps[-1] = currDt

                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)

                    elif prevDiff > desiredDegree and currDiff <= desiredDegree:
                        EphemerisUtils.log.debug("Crossed over {} from above to below!".\
                                  format(desiredDegree))

                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1

                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            EphemerisUtils.log.debug("Refining between {} and {}".\
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

                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1ParamsList, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet2ParamsList, fieldName))

                            EphemerisUtils.log.debug("testValueP1 == {}".format(testValueP1))
                            EphemerisUtils.log.debug("testValueP2 == {}".format(testValueP2))

                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360

                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360

                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)

                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360

                            EphemerisUtils.log.debug("testDiff == {}".format(testDiff))

                            if testDiff > desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt

                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff

                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2

                            currErrorTd = t2 - t1

                        # Update our lists.
                        steps[-1] = currDt

                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)

            # Prepare for the next iteration.
            EphemerisUtils.log.debug("steps[-1] is: {}".\
                      format(Ephemeris.datetimeToStr(steps[-1])))
            EphemerisUtils.log.debug("stepSizeTd is: {}".format(stepSizeTd))

            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]
            longitudesP2.append(None)
            del longitudesP2[0]

            # Update prevDiff as the currDiff.
            prevDiff = Util.toNormalizedAngle(currDiff)

        EphemerisUtils.log.info("Number of timestamps obtained: {}".\
                 format(len(aspectTimestamps)))

        EphemerisUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return aspectTimestamps


    @staticmethod
    def getOnePlanetLongitudeAspectTimestamps(\
        startDt,
        endDt,
        planet1Params,
        fixedDegree,
        degreeDifference,
        uniDirectionalAspectsFlag=False,
        maxErrorTd=datetime.timedelta(seconds=1)):
        """Obtains a list of datetime.datetime objects that contain
        the moments when the aspect specified is active.
        The aspect is measured by formula:
           (planet longitude) - (fixed longitude degree)

        Preconditions:
        This method assumes that the Ephemeris has been initialized and the
        geographic position has been set already.

        Arguments:
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations for artifacts.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations for artifacts.
        highPrice - float value for the high price to end the vertical line.
        lowPrice  - float value for the low price to end the vertical line.

        planet1Params - Tuple containing:
                      (planetName, centricityType, longitudeType)

                      Where:
                      planetName - str holding the name of the second
                                   planet to do the calculations for.
                      centricityType - str value holding either "geocentric",
                                       "topocentric", or "heliocentric".
                      longitudeType - str value holding either
                                      "tropical" or "sidereal".

        fixedDegree - float holding the fixed degree in the zodiac circle.

        degreeDifference - float value for the number of degrees of
                           separation for this aspect.

        uniDirectionalAspectsFlag - bool value for whether or not
                     uni-directional aspects are enabled or not.  By
                     default, aspects are bi-directional, so Saturn
                     square-aspect Jupiter would be the same as
                     Jupiter square-aspect Saturn.  If this flag is
                     set to True, then those two combinations would be
                     considered unique.  In the case where the flag is
                     set to True, for the aspect to be active,
                     planet2 would need to be 'degreeDifference'
                     degrees in front of planet1.

        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.

        Returns:

        List of datetime.datetime objects.  Each timestamp in the list
        is the moment where the aspect is active and satisfies the
        given parameters.  In the event of an error, the reference
        None is returned.

        rluu_20130926: This function needs to be tested.  It was copy-and-pasted from another script I wrote this function for, and that original script when I wrote it had some syntax errors, which I believe I applied the fixes to this code copied here.  So... this function 'should' work.  It shouldn't be hard to test and confirm, but I haven't done it.
        """

        EphemerisUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")

        # List of timestamps of the aspects found.
        aspectTimestamps = []

        # Make sure the inputs are valid.
        if endDt < startDt:
            errMsg = "Invalid input: 'endDt' must be after 'startDt'"
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Check to make sure planet params were given.
        if len(planet1Params) != 3:
            errMsg = "planet1Params must be a tuple with 3 elements."
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)
        if not isinstance(fixedDegree, (int, float, complex)):
            errMsg = "fixedDegree must be a number."
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Normalize the fixed degree.
        fixedDegree = Util.toNormalizedAngle(fixedDegree)

        EphemerisUtils.log.debug("planet1Params passed in is: {}".\
                  format(planet1Params))
        EphemerisUtils.log.debug("fixedDegree passed in is: {}".\
                  format(fixedDegree))

        # Check inputs of planet parameters.
        planetName = planet1Params[0]
        centricityType = planet1Params[1]
        longitudeType = planet1Params[2]

        # Check inputs for centricity type.
        loweredCentricityType = centricityType.lower()
        if loweredCentricityType != "geocentric" and \
            loweredCentricityType != "topocentric" and \
            loweredCentricityType != "heliocentric":

            errMsg = "Invalid input: Centricity type is invalid.  " + \
                "Value given was: {}".format(centricityType)
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Check inputs for longitude type.
        loweredLongitudeType = longitudeType.lower()
        if loweredLongitudeType != "tropical" and \
            loweredLongitudeType != "sidereal":

            errMsg = "Invalid input: Longitude type is invalid.  " + \
                "Value given was: {}".format(longitudeType)
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Field name we are getting.
        fieldName = "longitude"

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)

        planetName = planet1Params[0]

        if Ephemeris.isHouseCuspPlanetName(planetName) or \
            Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)
        elif planetName == "Moon":
            # Use a smaller step size for the moon so we can catch
            # smaller aspect sizes.
            stepSizeTd = datetime.timedelta(hours=3)

        EphemerisUtils.log.debug("Step size is: {}".format(stepSizeTd))

        # Desired angles.  We need to check for planets at these angles.
        desiredAngleDegList = []

        desiredAngleDeg1 = Util.toNormalizedAngle(degreeDifference)
        desiredAngleDegList.append(desiredAngleDeg1)
        if Util.fuzzyIsEqual(desiredAngleDeg1, 0):
            desiredAngleDegList.append(360)

        if uniDirectionalAspectsFlag == False:
            desiredAngleDeg2 = \
                360 - Util.toNormalizedAngle(degreeDifference)
            if desiredAngleDeg2 not in desiredAngleDegList:
                desiredAngleDegList.append(desiredAngleDeg2)

        # Debug output.
        anglesStr = ""
        for angle in desiredAngleDegList:
            anglesStr += "{} ".format(angle)
        EphemerisUtils.log.debug("Angles in desiredAngleDegList: " + anglesStr)

        # Iterate through, appending to aspectTimestamps list as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudesP1 = []
        longitudesP1.append(None)
        longitudesP1.append(None)

        longitudesP2 = []
        longitudesP2.append(None)
        longitudesP2.append(None)

        def getFieldValue(dt, planetParams, fieldName):
            """Creates the PlanetaryInfo object for the given
            planetParamsList and returns the value of the field
            desired.
            """

            EphemerisUtils.log.debug("planetParams passed in is: {}".\
                      format(planetParams))
            t = planetParams

            planetName = t[0]
            centricityType = t[1]
            longitudeType = t[2]

            pi = Ephemeris.getPlanetaryInfo(planetName, dt)

            EphemerisUtils.log.debug("Planet {} has geo sid longitude: {}".\
                      format(planetName,
                             pi.geocentric["sidereal"]["longitude"]))

            fieldValue = None

            if centricityType.lower() == "geocentric":
                fieldValue = pi.geocentric[longitudeType][fieldName]
            elif centricityType.lower() == "topocentric":
                fieldValue = pi.topocentric[longitudeType][fieldName]
            elif centricityType.lower() == "heliocentric":
                fieldValue = pi.heliocentric[longitudeType][fieldName]
            else:
                EphemerisUtils.log.error("Unknown centricity type: {}".\
                          format(centricityType))
                fieldValue = None

            return fieldValue

        EphemerisUtils.log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        currDiff = None
        prevDiff = None


        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]

            EphemerisUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            longitudesP1[-1] = \
                Util.toNormalizedAngle(\
                getFieldValue(currDt, planet1Params, fieldName))

            longitudesP2[-1] = fixedDegree

            EphemerisUtils.log.debug("{} {} is: {}".\
                      format(planet1Params, fieldName,
                             longitudesP1[-1]))
            EphemerisUtils.log.debug("fixedDegree is: {}".format(longitudesP2[-1]))

            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - longitudesP2[-1])

            EphemerisUtils.log.debug("prevDiff == {}".format(prevDiff))
            EphemerisUtils.log.debug("currDiff == {}".format(currDiff))

            if prevDiff != None and \
                   longitudesP1[-2] != None and \
                   longitudesP2[-2] != None:

                if abs(prevDiff - currDiff) > 180:
                    # Probably crossed over 0.  Adjust the prevDiff so
                    # that the rest of the algorithm can continue to
                    # work.
                    if prevDiff > currDiff:
                        prevDiff -= 360
                    else:
                        prevDiff += 360

                    EphemerisUtils.log.debug("After adjustment: prevDiff == {}".\
                              format(prevDiff))
                    EphemerisUtils.log.debug("After adjustment: currDiff == {}".\
                              format(currDiff))

                for desiredAngleDeg in desiredAngleDegList:
                    EphemerisUtils.log.debug("Looking at desiredAngleDeg: {}".\
                              format(desiredAngleDeg))

                    desiredDegree = desiredAngleDeg

                    if prevDiff < desiredDegree and currDiff >= desiredDegree:
                        EphemerisUtils.log.debug("Crossed over {} from below to above!".\
                                  format(desiredDegree))

                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1

                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            EphemerisUtils.log.debug("Refining between {} and {}".\
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

                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1Params, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(fixedDegree)

                            EphemerisUtils.log.debug("testValueP1 == {}".format(testValueP1))
                            EphemerisUtils.log.debug("testValueP2 == {}".format(testValueP2))

                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360

                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360

                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)

                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360

                            EphemerisUtils.log.debug("testDiff == {}".format(testDiff))

                            if testDiff < desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt

                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff

                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2

                            currErrorTd = t2 - t1

                        # Update our lists.
                        steps[-1] = currDt

                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)

                    elif prevDiff > desiredDegree and currDiff <= desiredDegree:
                        EphemerisUtils.log.debug("Crossed over {} from above to below!".\
                                  format(desiredDegree))

                        # This is the upper-bound of the error timedelta.
                        t1 = prevDt
                        t2 = currDt
                        currErrorTd = t2 - t1

                        # Refine the timestamp until it is less than
                        # the threshold.
                        while currErrorTd > maxErrorTd:
                            EphemerisUtils.log.debug("Refining between {} and {}".\
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

                            testValueP1 = \
                                Util.toNormalizedAngle(getFieldValue(\
                                testDt, planet1ParamsList, fieldName))
                            testValueP2 = \
                                Util.toNormalizedAngle(fixedDegree)

                            EphemerisUtils.log.debug("testValueP1 == {}".format(testValueP1))
                            EphemerisUtils.log.debug("testValueP2 == {}".format(testValueP2))

                            if longitudesP1[-2] > 240 and testValueP1 < 120:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 += 360
                            elif longitudesP1[-2] < 120 and testValueP1 > 240:
                                # Planet 1 hopped over 0 degrees.
                                testValueP1 -= 360

                            if longitudesP2[-2] > 240 and testValueP2 < 120:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 += 360
                            elif longitudesP2[-2] < 120 and testValueP2 > 240:
                                # Planet 2 hopped over 0 degrees.
                                testValueP2 -= 360

                            testDiff = Util.toNormalizedAngle(\
                                testValueP1 - testValueP2)

                            # Handle special cases of degrees 0 and 360.
                            # Here we adjust testDiff so that it is in the
                            # expected ranges.
                            if Util.fuzzyIsEqual(desiredDegree, 0):
                                if testDiff > 240:
                                    testDiff -= 360
                            elif Util.fuzzyIsEqual(desiredDegree, 360):
                                if testDiff < 120:
                                    testDiff += 360

                            EphemerisUtils.log.debug("testDiff == {}".format(testDiff))

                            if testDiff > desiredDegree:
                                t1 = testDt
                            else:
                                t2 = testDt

                                # Update the curr values.
                                currDt = t2
                                currDiff = testDiff

                                longitudesP1[-1] = testValueP1
                                longitudesP2[-1] = testValueP2

                            currErrorTd = t2 - t1

                        # Update our lists.
                        steps[-1] = currDt

                        # Store the aspect timestamp.
                        aspectTimestamps.append(currDt)

            # Prepare for the next iteration.
            EphemerisUtils.log.debug("steps[-1] is: {}".\
                      format(Ephemeris.datetimeToStr(steps[-1])))
            EphemerisUtils.log.debug("stepSizeTd is: {}".format(stepSizeTd))

            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]
            longitudesP2.append(None)
            del longitudesP2[0]

            # Update prevDiff as the currDiff.
            prevDiff = Util.toNormalizedAngle(currDiff)

        EphemerisUtils.log.info("Number of timestamps obtained: {}".\
                 format(len(aspectTimestamps)))

        EphemerisUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return aspectTimestamps


    @staticmethod
    def getPlanetCrossingLongitudeDegTimestamps(\
        startDt,
        endDt,
        planetName,
        centricityType,
        longitudeType,
        degree,
        maxErrorTd=datetime.timedelta(seconds=1)):
        """Returns a list of datetimes of when a certain planet crosses
        a certain degree of longitude.

        The algorithm used assumes that a step size won't move the
        planet more than 1/3 of a circle.

        Preconditions:
        This method assumes that the Ephemeris has been initialized and the
        geographic position has been set already.

        Arguments:
        startDt       - datetime.datetime object for the starting timestamp
                        to do the calculations.
        endDt         - datetime.datetime object for the ending timestamp
                        to do the calculations.
        centricityType - str value holding either "geocentric",
                         "topocentric", or "heliocentric".
        longitudeType - str value holding either "tropical" or "sidereal".
        planetName    - str value holding the name fo the planet to do
                        the search for.
        degree        - float value for the degree of longitude that should be
                        crossed in order to trigger a vertical line being drawn.
        maxErrorTd    - datetime.timedelta object holding the maximum
                        time difference between the exact planetary
                        combination timestamp, and the one calculated.
                        This would define the accuracy of the
                        calculations.

        Returns:

        List of datetime.datetime, containing the timestamps when the
        planet crosses the degree, within the startDt and endDt.

        If an error occurred, the None is returned.
        """


        EphemerisUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = []

        # Make sure the inputs are valid.
        if endDt < startDt:
            errMsg = "Invalid input: 'endDt' must be after 'startDt'.  " + \
              "Values given were: endDt={}, startDt={}".\
              format(Ephemeris.datetimeToStr(endDt),
                     Ephemeris.datetimeToStr(startDt))
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        if planetName not in Ephemeris.getSupportedPlanetNamesList():
            errMsg = "Invalid input: planetName is invalid.  " + \
                      "Value given was: {}".format(planetName)
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)
            
        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            errMsg = "Invalid input: centricityType is invalid.  " + \
                      "Value given was: {}".format(centricityTypeOrig)
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            errMsg = "Invalid input: longitudeType is invalid.  " + \
                     "Value given was: {}".format(longitudeTypeOrig)
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Field name we are getting.
        fieldName = "longitude"

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)

        # Iterate through, creating artfacts and adding them as we go.
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        longitudes = []
        longitudes.append(None)
        longitudes.append(None)

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
                EphemerisUtils.log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue


        EphemerisUtils.log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        while steps[-1] < endDt:
            currDt = steps[-1]
            prevDt = steps[-2]

            EphemerisUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            longitudes[-1] = getFieldValue(p1, fieldName)

            EphemerisUtils.log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))

            if longitudes[-2] != None:

                currValue = None
                prevValue = None
                desiredDegree = None
                crossedOverZeroDegrees = None

                # This algorithm assumes that a step size won't move the
                # planet more than 1/3 of a circle.
                if longitudes[-2] > 240 and longitudes[-1] < 120:
                    # Hopped over 0 degrees from below to above.
                    prevValue = longitudes[-2]
                    currValue = longitudes[-1] + 360
                    desiredDegree = degree + 360
                    crossedOverZeroDegrees = True
                elif longitudes[-2] < 120 and longitudes[-1] > 240:
                    # Hopped over 0 degrees from above to below.
                    prevValue = longitudes[-2] + 360
                    currValue = longitudes[-1]
                    desiredDegree = degree
                    crossedOverZeroDegrees = True
                else:
                    # Did not cross 0 degrees.
                    prevValue = longitudes[-2]
                    currValue = longitudes[-1]
                    desiredDegree = degree
                    crossedOverZeroDegrees = False

                if prevValue < desiredDegree and currValue >= desiredDegree:
                    EphemerisUtils.log.debug("Crossed over from below to above!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        EphemerisUtils.log.debug("Refining between {} and {}".\
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

                        testValue = getFieldValue(p1, fieldName)

                        if longitudes[-2] > 240 and testValue < 120:
                            testValue += 360

                        if testValue < desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currValue = testValue

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    longitudes[-1] = Util.toNormalizedAngle(currValue)

                    # Append the result datetime found.
                    rv.append(currDt)

                elif prevValue >= desiredDegree and currValue < desiredDegree:
                    EphemerisUtils.log.debug("Crossed over from above to below!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        EphemerisUtils.log.debug("Refining between {} and {}".\
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

                        testValue = getFieldValue(p1, fieldName)

                        if longitudes[-2] > 240 and testValue < 120:
                            testValue += 360

                        if testValue >= desiredDegree:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currValue = testValue

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    longitudes[-1] = Util.toNormalizedAngle(currValue)

                    # Append the result datetime found.
                    rv.append(currDt)

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudes.append(None)
            del longitudes[0]

        EphemerisUtils.log.info("Number of datetimes found: {}".format(len(rv)))

        EphemerisUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv


    @staticmethod
    def getGeoRetrogradeDirectTimestamps(\
        startDt,
        endDt,
        planetName,
        maxErrorTd=datetime.timedelta(seconds=1)):
        """Obtains a list of tuples containing data describing
        the timestamps of when the specified planet is going
        retrograde or direct (i.e. is stationary).

        Preconditions:
        This method assumes that the Ephemeris has been initialized and the
        geographic position has been set already.

        Arguments:
        startDt   - datetime.datetime object for the starting timestamp
                    to do the calculations.
        endDt     - datetime.datetime object for the ending timestamp
                    to do the calculations.
        planetName - str holding the name of the
                     planet to do the calculations for.
        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.

        Returns:

        List of tuples containing one of following possible entries,
        depending on whether it is the moment the planet turns
        direct or when the planet turns retrograde:

          (PlanetaryInfo p, "direct")
          (PlanetaryInfo p, "retrograde")

        The list of tuples' PlanetaryInfo's datetimes are timestamp-ordered.
        Thus: tup[0][0].dt is a datetime before tup[1][0].dt

        In the event of an error, the reference None is returned.
        """

        EphemerisUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")
        EphemerisUtils.log.debug("startDt=" + Ephemeris.datetimeToDayStr(startDt) + ", " +
                  "endDt=" + Ephemeris.datetimeToDayStr(endDt) +  ", " +
                  "planetName=" + planetName + ", " +
                  "maxErrorTd=" + str(maxErrorTd))

        # List of tuples that are returned.
        rv = []

        # Make sure the inputs are valid.
        if endDt < startDt:
            errMsg = "Invalid input: 'endDt' must be after 'startDt'"
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Set the step size.
        stepSizeTd = datetime.timedelta(days=1)
        if Ephemeris.isHouseCuspPlanetName(planetName) or \
               Ephemeris.isAscmcPlanetName(planetName):

            # House cusps and ascmc planets need a smaller step size.
            stepSizeTd = datetime.timedelta(hours=1)

        # Field name we are getting.
        fieldName = "longitude_speed"
        centricityType = "geocentric"
        longitudeType = "tropical"

        # Set the tag str.
        tag = inspect.stack()[0][3]
        if tag.startswith("add") and len(tag) > 3:
            tag = tag[3:] + "_" + planetName
        EphemerisUtils.log.debug("tag == '{}'".format(tag))

        # Timestamp steps saved (list of datetime.datetime).
        steps = []
        steps.append(copy.deepcopy(startDt))
        steps.append(copy.deepcopy(startDt))

        # Velocity of the steps saved (list of float).
        velocitys = []
        velocitys.append(None)
        velocitys.append(None)

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
                EphemerisUtils.log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue

        # Iterate through, creating artfacts and adding them as we go.
        EphemerisUtils.log.debug("Stepping through timestamps from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startDt),
                         Ephemeris.datetimeToStr(endDt)))

        while steps[-1] < endDt:
            currDt = steps[-1]
            EphemerisUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            velocitys[-1] = getFieldValue(p1, fieldName)

            EphemerisUtils.log.debug("{} velocity is: {}".\
                      format(p1.name, velocitys[-1]))

            for i in range(len(steps)):
                EphemerisUtils.log.debug("steps[{}] == {}".\
                          format(i, Ephemeris.datetimeToStr(steps[i])))
            for i in range(len(velocitys)):
                EphemerisUtils.log.debug("velocitys[{}] == {}".format(i, velocitys[i]))


            if velocitys[-2] != None:

                prevValue = velocitys[-2]
                currValue = velocitys[-1]
                prevDt = steps[-2]
                currDt = steps[-1]
                desiredVelocity = 0

                if prevValue < desiredVelocity and currValue >= desiredVelocity:
                    EphemerisUtils.log.debug("Went from Retrograde to Direct!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        EphemerisUtils.log.debug("Refining between {} and {}".\
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

                        testValue = getFieldValue(p1, fieldName)

                        if testValue < desiredVelocity:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currValue = testValue

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    velocitys[-1] = currValue

                    pi = Ephemeris.getPlanetaryInfo(planetName, currDt)
                    tup = (pi, "direct")
                    rv.append(tup)

                elif prevValue >= desiredVelocity and currValue < desiredVelocity:
                    EphemerisUtils.log.debug("Went from Direct to Retrograde!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        EphemerisUtils.log.debug("Refining between {} and {}".\
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

                        testValue = getFieldValue(p1, fieldName)

                        if testValue >= desiredVelocity:
                            t1 = testDt
                        else:
                            t2 = testDt

                            # Update the curr values.
                            currDt = t2
                            currValue = testValue

                        currErrorTd = t2 - t1

                    # Update our lists.
                    steps[-1] = currDt
                    velocitys[-1] = currValue

                    pi = Ephemeris.getPlanetaryInfo(planetName, currDt)
                    tup = (pi, "retrograde")
                    rv.append(tup)

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            velocitys.append(None)
            del velocitys[0]

        EphemerisUtils.log.info("Number of geo retrograde or direct planet timestamps: {}".\
                 format(len(rv)))

        EphemerisUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

    @staticmethod
    def getDatetimesOfElapsedLongitudeDegrees(\
        planetName,
        centricityType,
        longitudeType,
        planetEpocDt,
        desiredDegreesElapsed,
        maxErrorTd=datetime.timedelta(seconds=1)):
        """Returns a list of datetime.datetime objects that hold the
        timestamps when the given planet is at 'degreeElapsed'
        longitude degrees from the longitude degrees calculated at
        moment 'planetEpocDt'.

        Preconditions:
        This method assumes that the Ephemeris has been initialized and the
        geographic position has been set already.

        Arguments:
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
                        This value must be a number >= 0.
                TODO_rluu_20160915: Made this method work also for negative values of desiredDegreesElapsed.
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

        EphemerisUtils.log.debug("Entered " + inspect.stack()[0][3] + "()")

        # Return value.
        rv = []

        centricityTypeOrig = centricityType
        centricityType = centricityType.lower()
        if centricityType != "geocentric" and \
           centricityType != "topocentric" and \
           centricityType != "heliocentric":

            errMsg = "Invalid input: centricityType is invalid.  " + \
                "Value given was: {}".format(centricityTypeOrig)
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        longitudeTypeOrig = longitudeType
        longitudeType = longitudeType.lower()
        if longitudeType != "tropical" and \
           longitudeType != "sidereal":

            errMsg = "Invalid input: longitudeType is invalid.  " + \
                "Value given was: {}".format(longitudeTypeOrig)
            EphemerisUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Field name we are getting.
        fieldName = "longitude"

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
                EphemerisUtils.log.error("Unknown centricity type.")
                fieldValue = None

            return fieldValue

        EphemerisUtils.log.debug("Stepping through timestamps from {} ...".\
                  format(Ephemeris.datetimeToStr(planetEpocDt)))

        currDiff = None
        prevDiff = None

        # Current and previous number of degrees elapsed.
        currElapsed = None

        done = False
        while not done:

            currDt = steps[-1]
            prevDt = steps[-2]

            EphemerisUtils.log.debug("Looking at currDt == {} ...".\
                      format(Ephemeris.datetimeToStr(currDt)))

            p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)

            if planetEpocLongitude == None:
                planetEpocLongitude = getFieldValue(p1, fieldName)

            longitudesP1[-1] = getFieldValue(p1, fieldName)

            EphemerisUtils.log.debug("{} {} {} {} is: {}".\
                      format(p1.name, centricityType, longitudeType, fieldName,
                             getFieldValue(p1, fieldName)))

            currDiff = Util.toNormalizedAngle(\
                longitudesP1[-1] - planetEpocLongitude)

            EphemerisUtils.log.debug("prevDiff == {}".format(prevDiff))
            EphemerisUtils.log.debug("currDiff == {}".format(currDiff))

            if prevDiff != None and longitudesP1[-2] != None:

                if prevDiff > 240 and currDiff < 120:
                    EphemerisUtils.log.debug("Crossed over epoc longitude {} ".\
                              format(planetEpocLongitude) + \
                              "from below to above!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        EphemerisUtils.log.debug("Refining between {} and {}".\
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
                    EphemerisUtils.log.debug("Crossed over epoc longitude {} ".\
                              format(planetEpocLongitude) + \
                              "from above to below!")

                    # This is the upper-bound of the error timedelta.
                    t1 = prevDt
                    t2 = currDt
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        EphemerisUtils.log.debug("Refining between {} and {}".\
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

                EphemerisUtils.log.debug("currElapsed == {}".format(currElapsed))
                EphemerisUtils.log.debug("desiredDegreesElapsed == {}".\
                          format(desiredDegreesElapsed))

                if currElapsed > desiredDegreesElapsed:
                    # We pased the number of degrees past that we were
                    # looking for.  Now we have to calculate the exact
                    # timestamp and find out if there are other
                    # moments in time where the planet is elapsed this
                    # many degrees (in the event that the planet goes
                    # retrograde).
                    EphemerisUtils.log.debug("Passed the desired number of " + \
                              "elapsed degrees from below to above.  " + \
                              "Narrowing down to the exact moment in time ...")

                    # Actual degree we are looking for.
                    desiredDegree = \
                        Util.toNormalizedAngle(\
                        planetEpocLongitude + (desiredDegreesElapsed % 360.0))

                    EphemerisUtils.log.debug("desiredDegree == {}".format(desiredDegree))

                    # Check starting from steps[-2] to steps[-1] to
                    # see exactly when it passes this desiredDegree.

                    # This is the upper-bound of the error timedelta.
                    t1 = steps[-2]
                    t2 = steps[-1]
                    currErrorTd = t2 - t1

                    # Refine the timestamp until it is less than the threshold.
                    while currErrorTd > maxErrorTd:
                        EphemerisUtils.log.debug("Refining between {} and {}".\
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

                    EphemerisUtils.log.debug("First moment in time found to be: {}".\
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

                    EphemerisUtils.log.debug("desiredDegree == {}".format(desiredDegree))

                    while prevDiff <= 120 or prevDiff > 240:
                        p1 = Ephemeris.getPlanetaryInfo(planetName, currDt)
                        currDiff = Util.toNormalizedAngle(\
                            getFieldValue(p1, fieldName) - desiredDegree)

                        EphemerisUtils.log.debug("currDt == {}, ".\
                                  format(Ephemeris.datetimeToStr(currDt)) +
                                  "longitude == {}, ".\
                                  format(getFieldValue(p1, fieldName)) + \
                                  "currDiff == {}".\
                                  format(currDiff))

                        if prevDiff > 240 and currDiff < 120:
                            EphemerisUtils.log.debug("Passed the desired number of " + \
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
                                EphemerisUtils.log.debug("Refining between {} and {}".\
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
                            EphemerisUtils.log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        elif prevDiff < 120 and currDiff > 240:
                            EphemerisUtils.log.debug("Passed the desired number of " + \
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
                                EphemerisUtils.log.debug("Refining between {} and {}".\
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
                            EphemerisUtils.log.debug("Appending moment in time: {}".\
                                      format(Ephemeris.datetimeToStr(currDt)))
                            rv.append(currDt)

                        prevDt = currDt
                        currDt = copy.deepcopy(currDt) + stepSizeTd
                        prevDiff = currDiff
                        currDiff = None

                    EphemerisUtils.log.debug("Done searching for timestamps.")

                    # We have our timestamps, so we are done.
                    done = True

            # Prepare for the next iteration.
            steps.append(copy.deepcopy(steps[-1]) + stepSizeTd)
            del steps[0]
            longitudesP1.append(None)
            del longitudesP1[0]

            # Update prevDiff as the currDiff.
            prevDiff = currDiff

        EphemerisUtils.log.debug("Exiting " + inspect.stack()[0][3] + "()")
        return rv

##############################################################################

def testGetLongitudeAspectTimestamps():
    print("Running " + inspect.stack()[0][3] + "()")

    eastern = pytz.timezone('US/Eastern')
    startDt = datetime.datetime(1926, 1, 1, 12, 0, 0, tzinfo=eastern)
    endDt = datetime.datetime(1940, 12, 30, 12, 0, 0, tzinfo=eastern)
    planet1Name = "Mercury"
    planet2Name = "Sun"
    centricityType = "geocentric"
    longitudeType = "tropical"
    planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
    planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
    degreeDifference = 5
    uniDirectionalAspectsFlag = True
    maxErrorTd = datetime.timedelta(seconds=1)

    dts = EphemerisUtils.getLongitudeAspectTimestamps(\
        startDt,
        endDt,
        planet1ParamsList,
        planet2ParamsList,
        degreeDifference,
        uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
        maxErrorTd=maxErrorTd)

    print("Timestamps between {} and {} for aspect {} deg between planets {} and {} are:".\
            format(Ephemeris.datetimeToStr(startDt),
                   Ephemeris.datetimeToStr(endDt),
                   degreeDifference,
                   planet1Name,
                   planet2Name))
    for dt in dts:
        print("    {}".format(Ephemeris.datetimeToDayStr(dt)))

def testGetOnePlanetLongitudeAspectTimestamps():
    print("Running " + inspect.stack()[0][3] + "()")

    eastern = pytz.timezone('US/Eastern')
    startDt = datetime.datetime(1926, 1, 1, 12, 0, 0, tzinfo=eastern)
    endDt = datetime.datetime(1940, 12, 30, 12, 0, 0, tzinfo=eastern)
    planet1Name = "Sun"
    centricityType = "geocentric"
    longitudeType = "tropical"
    planet1ParamsList = (planet1Name, centricityType, longitudeType)
    fixedDegree = 0
    degreeDifference = 120
    uniDirectionalAspectsFlag = True
    maxErrorTd = datetime.timedelta(seconds=1)

    dts = EphemerisUtils.getOnePlanetLongitudeAspectTimestamps(\
        startDt,
        endDt,
        planet1ParamsList,
        fixedDegree,
        degreeDifference,
        uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
        maxErrorTd=maxErrorTd)

    print("Timestamps between {} and {} for planet {} having aspect of {} deg to fixed degree {} are:".\
            format(Ephemeris.datetimeToStr(startDt),
                   Ephemeris.datetimeToStr(endDt),
                   planet1Name,
                   degreeDifference,
                   fixedDegree))
    for dt in dts:
        print("    {}".format(Ephemeris.datetimeToDayStr(dt)))

def testGetPlanetCrossingLongitudeDegTimestamps():
    print("Running " + inspect.stack()[0][3] + "()")

    eastern = pytz.timezone('US/Eastern')
    startDt = datetime.datetime(1926, 1, 1, 12, 0, 0, tzinfo=eastern)
    endDt = datetime.datetime(1940, 12, 30, 12, 0, 0, tzinfo=eastern)
    planetName = "Sun"
    centricityType = "geocentric"
    longitudeType = "tropical"
    degree = 120
    maxErrorTd = datetime.timedelta(seconds=1)

    dts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
        startDt,
        endDt,
        planetName,
        centricityType,
        longitudeType,
        degree,
        maxErrorTd=maxErrorTd)

    print("Timestamps between {} and {} for planet {} crossing {} deg are:".\
            format(Ephemeris.datetimeToStr(startDt),
                   Ephemeris.datetimeToStr(endDt),
                   planetName,
                   degree))
    for dt in dts:
        print("    {}".format(Ephemeris.datetimeToDayStr(dt)))

def testGetGeoRetrogradeDirectTimestamps():
    print("Running " + inspect.stack()[0][3] + "()")

    eastern = pytz.timezone('US/Eastern')
    startDt = datetime.datetime(1926, 1, 1, 12, 0, 0, tzinfo=eastern)
    endDt = datetime.datetime(1940, 12, 30, 12, 0, 0, tzinfo=eastern)
    planetName = "Mercury"
    maxErrorTd = datetime.timedelta(seconds=1)

    tuples = EphemerisUtils.getGeoRetrogradeDirectTimestamps(\
        startDt,
        endDt,
        planetName,
        maxErrorTd=maxErrorTd)

    print("Timestamps between {} and {} for geo planet {} retrograde and direct changes are:".\
            format(Ephemeris.datetimeToStr(startDt),
                   Ephemeris.datetimeToStr(endDt),
                   planetName))
    for tup in tuples:
        print("    {} ({})".format(Ephemeris.datetimeToDayStr(tup[0].dt), tup[1]))

def testGetDatetimesOfElapsedLongitudeDegrees():
    print("Running " + inspect.stack()[0][3] + "()")

    eastern = pytz.timezone('US/Eastern')
    planetName = "Mercury"
    centricityType = "geocentric"
    longitudeType = "tropical"
    planetEpocDt = datetime.datetime(1926, 3, 15, 3, 56, 50, tzinfo=eastern)
    desiredDegreesElapsed = 235
    maxErrorTd = datetime.timedelta(seconds=1)

    dts = EphemerisUtils.getDatetimesOfElapsedLongitudeDegrees(\
        planetName,
        centricityType,
        longitudeType,
        planetEpocDt,
        desiredDegreesElapsed,
        maxErrorTd=maxErrorTd)

    print("Timestamps for planet {} elapsing {} deg from its position on {}:".\
            format(planetName,
                   desiredDegreesElapsed,
                   Ephemeris.datetimeToStr(planetEpocDt)))
    for dt in dts:
        print("    {}".format(Ephemeris.datetimeToDayStr(dt)))

##############################################################################

# For debugging the classes in this module during development.
if __name__=="__main__":
    # For timing the calculations.
    import time

    # For filesystem access for logging.
    import os
    import sys

    print("------------------------")


    # Initialize Logging for the Ephemeris class (required).
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    # Set the Location (required).

    # Chicago:
    #lon = -87.627777777777
    #lat = 41.8819444444444444

    # Chantilly/Arlington:
    #lon = -77.084444
    #lat = 38.890277

    # New York City:
    lon = -74.0064
    lat = 40.7142

    #Ephemeris.setGeographicPosition(lon, lat, -68)
    Ephemeris.setGeographicPosition(lon, lat)

    startTime = time.time()

    # Different tests that can be run:
    #testGetLongitudeAspectTimestamps()
    #testGetOnePlanetLongitudeAspectTimestamps()
    #testGetPlanetCrossingLongitudeDegTimestamps()
    #testGetGeoRetrogradeDirectTimestamps()
    testGetDatetimesOfElapsedLongitudeDegrees()

    endTime = time.time()
    print("Calculations took: {} sec".format(endTime - startTime))

    # Close the Ephemeris so it can do necessary cleanups.
    Ephemeris.closeEphemeris()

    # Shutdown logging so all the file handles get flushed and
    # cleanup can happen.
    logging.shutdown()

    print("Exiting.")

##############################################################################
