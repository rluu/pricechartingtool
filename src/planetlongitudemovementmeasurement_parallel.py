

# Pool of processes for calculating PlanetLongitudeMovementMeasurements.
from multiprocessing import Pool

import os


def getPlanetLongitudeMovementMeasurementText(argsTuple):
    """Method that is distrubted to dispy's nodes ('dispynode') for
    remote execution.  Module dependencies are imported within the
    method below.

    This method runs the following method:

      planetlongitudemovementmeasurement_calc.PLMMUtils.getPlanetLongitudeMovementMeasurementText()

    Please see documentation for that method for information about
    the functionality, method arguments, and return value(s).
    """


    from planetlongitudemovementmeasurement_calc import PLMMUtils

    i = 0
    planetName = argsTuple[i]
    i += 1
    startTimestamp = argsTuple[i]
    i += 1
    endTimestamp = argsTuple[i]
    i += 1
    showGeocentricRetroAsZeroTextFlag = argsTuple[i]
    i += 1
    showGeocentricRetroAsPositiveTextFlag = argsTuple[i]
    i += 1
    showGeocentricRetroAsNegativeTextFlag = argsTuple[i]
    i += 1
    showHeliocentricTextFlag = argsTuple[i]
    i += 1
    tropicalZodiacFlag = argsTuple[i]
    i += 1
    siderealZodiacFlag = argsTuple[i]
    i += 1
    measurementUnitDegreesEnabled = argsTuple[i]
    i += 1
    measurementUnitCirclesEnabled = argsTuple[i]
    i += 1
    measurementUnitBiblicalCirclesEnabled = argsTuple[i]
    i += 1
    measurementUnit7ersEnabled = argsTuple[i]
    i += 1
    measurementUnit11ersEnabled = argsTuple[i]
    i += 1
    measurementUnit12ersEnabled = argsTuple[i]
    i += 1
    measurementUnit24ersEnabled = argsTuple[i]
    i += 1
    measurementUnit25ersEnabled = argsTuple[i]
    i += 1
    measurementUnit33ersEnabled = argsTuple[i]
    i += 1
    measurementUnit36ersEnabled = argsTuple[i]
    i += 1
    measurementUnit37ersEnabled = argsTuple[i]
    i += 1
    measurementUnit40ersEnabled = argsTuple[i]
    i += 1
    measurementUnit45ersEnabled = argsTuple[i]
    i += 1
    measurementUnit49ersEnabled = argsTuple[i]
    i += 1
    measurementUnit60ersEnabled = argsTuple[i]
    i += 1
    measurementUnit69ersEnabled = argsTuple[i]
    i += 1
    measurementUnit72ersEnabled = argsTuple[i]
    i += 1
    measurementUnit84ersEnabled = argsTuple[i]
    i += 1
    measurementUnit90ersEnabled = argsTuple[i]
    i += 1
    measurementUnit100ersEnabled = argsTuple[i]
    i += 1
    measurementUnit110ersEnabled = argsTuple[i]
    i += 1
    measurementUnit112ersEnabled = argsTuple[i]
    i += 1
    measurementUnit133ersEnabled = argsTuple[i]
    i += 1
    measurementUnit137ersEnabled = argsTuple[i]
    i += 1
    measurementUnit144ersEnabled = argsTuple[i]
    i += 1
    measurementUnit153ersEnabled = argsTuple[i]
    i += 1
    measurementUnit194ersEnabled = argsTuple[i]
    i += 1
    measurementUnit500ersEnabled = argsTuple[i]
    i += 1
    maxErrorTd = argsTuple[i]
    i += 1
    locationLongitudeDegrees = argsTuple[i]
    i += 1
    locationLatitudeDegrees = argsTuple[i]
    i += 1
    locationElevationMeters = argsTuple[i]
    i += 1

    PLMMUtils.initializeEphemeris(locationLongitudeDegrees,
                                  locationLatitudeDegrees,
                                  locationElevationMeters)

    return PLMMUtils.getPlanetLongitudeMovementMeasurementText(\
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
        measurementUnit24ersEnabled,
        measurementUnit25ersEnabled,
        measurementUnit33ersEnabled,
        measurementUnit36ersEnabled,
        measurementUnit37ersEnabled,
        measurementUnit40ersEnabled,
        measurementUnit45ersEnabled,
        measurementUnit49ersEnabled,
        measurementUnit60ersEnabled,
        measurementUnit69ersEnabled,
        measurementUnit72ersEnabled,
        measurementUnit84ersEnabled,
        measurementUnit90ersEnabled,
        measurementUnit100ersEnabled,
        measurementUnit110ersEnabled,
        measurementUnit112ersEnabled,
        measurementUnit133ersEnabled,
        measurementUnit137ersEnabled,
        measurementUnit144ersEnabled,
        measurementUnit153ersEnabled,
        measurementUnit194ersEnabled,
        measurementUnit500ersEnabled,
        maxErrorTd)


class PlanetLongitudeMovementMeasurementParallel:

    poolSize = os.cpu_count()

    pool = Pool(poolSize)

    @staticmethod
    def getPlanetLongitudeMovementMeasurementText(listOfTuples):
        """
        Arguments:
        listOfTuples - List of tuple objects.  Each tuple has
                       the following within it:

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

        measurementUnit24ersEnabled,
                       - bool flag for displaying measurements in number
                         of 24-degree units.

        measurementUnit25ersEnabled,
                       - bool flag for displaying measurements in number
                         of 25-degree units.

        measurementUnit33ersEnabled,
                       - bool flag for displaying measurements in number
                         of 33-degree units.

        measurementUnit36ersEnabled,
                       - bool flag for displaying measurements in number
                         of 36-degree units.

        measurementUnit37ersEnabled,
                       - bool flag for displaying measurements in number
                         of 37-degree units.

        measurementUnit40ersEnabled,
                       - bool flag for displaying measurements in number
                         of 40-degree units.

        measurementUnit45ersEnabled,
                       - bool flag for displaying measurements in number
                         of 45-degree units.

        measurementUnit49ersEnabled,
                       - bool flag for displaying measurements in number
                         of 49-degree units.

        measurementUnit60ersEnabled,
                       - bool flag for displaying measurements in number
                         of 60-degree units.

        measurementUnit69ersEnabled,
                       - bool flag for displaying measurements in number
                         of 69-degree units.

        measurementUnit72ersEnabled,
                       - bool flag for displaying measurements in number
                         of 72-degree units.

        measurementUnit84ersEnabled,
                       - bool flag for displaying measurements in number
                         of 84-degree units.

        measurementUnit90ersEnabled,
                       - bool flag for displaying measurements in number
                         of 90-degree units.

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

        measurementUnit137ersEnabled,
                       - bool flag for displaying measurements in number
                         of 137-degree units.

        measurementUnit144ersEnabled,
                       - bool flag for displaying measurements in number
                         of 144-degree units.

        measurementUnit153ersEnabled,
                       - bool flag for displaying measurements in number
                         of 153-degree units.

        measurementUnit194ersEnabled,
                       - bool flag for displaying measurements in number
                         of 194-degree units.

        measurementUnit500ersEnabled,
                       - bool flag for displaying measurements in number
                         of 500-degree units.

        maxErrorTd - datetime.timedelta object holding the maximum
                     time difference between the exact planetary
                     combination timestamp, and the one calculated.
                     This would define the accuracy of the
                     calculations.

        locationLongitudeDegrees - float value holding the
                      location longitude in degrees.
                      West longitudes are negative,
                      East longitudes are positive.
                      Value should be in the range of -180 to 180.
        locationLatitudeDegrees - float value holding the
                      location latitude in degrees.
                      North latitudes are positive,
                      South latitudes are negative.
                      Value should be in the range of -90 to 90.
        locationElevationMeters - float value holding the
                      altitude in meters.

        Returns:
        The str containing the planet longitude movement measurements.
        """

        listOfResults = \
            PlanetLongitudeMovementMeasurementParallel.pool.map(
                getPlanetLongitudeMovementMeasurementText, listOfTuples)

        text = ""
        for result in listOfResults:
            if result != "":
                text += result + os.linesep
        text = text.rstrip()

        return text

    @staticmethod
    def shutdown():
        PlanetLongitudeMovementMeasurementParallel.pool.close()


##############################################################################
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

    # For timestamps and timezone information.
    import datetime
    import pytz

    # For logging.
    import logging
    import logging.config

    # Import the Ephemeris classes.
    from ephemeris import PlanetaryInfo
    from ephemeris import Ephemeris

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
        #testLookbackMultipleParallel_speedTestParallel()
        #testLookbackMultipleParallel_speedTestSerial()
        pass

    #startTime = time.time()
    runTests()
    #endTime = time.time()

    #print("")
    #print("Running all tests took: {} sec".format(endTime - startTime))

    #cProfile.run('runTests()')

    # Exit the app when all windows are closed.
    #app.lastWindowClosed.connect(logging.shutdown)
    #app.lastWindowClosed.connect(app.quit)

    #app.exec_()

    # Quit.
    print("Exiting.")
    sys.exit()

##############################################################################
