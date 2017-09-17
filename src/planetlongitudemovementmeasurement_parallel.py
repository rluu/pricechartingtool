

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
    measurementUnit13ersEnabled = argsTuple[i]
    i += 1
    measurementUnit15ersEnabled = argsTuple[i]
    i += 1
    measurementUnit16ersEnabled = argsTuple[i]
    i += 1
    measurementUnit18ersEnabled = argsTuple[i]
    i += 1
    measurementUnit19ersEnabled = argsTuple[i]
    i += 1
    measurementUnit22ersEnabled = argsTuple[i]
    i += 1
    measurementUnit23ersEnabled = argsTuple[i]
    i += 1
    measurementUnit24ersEnabled = argsTuple[i]
    i += 1
    measurementUnit25ersEnabled = argsTuple[i]
    i += 1
    measurementUnit29ersEnabled = argsTuple[i]
    i += 1
    measurementUnit30ersEnabled = argsTuple[i]
    i += 1
    measurementUnit31ersEnabled = argsTuple[i]
    i += 1
    measurementUnit33ersEnabled = argsTuple[i]
    i += 1
    measurementUnit34ersEnabled = argsTuple[i]
    i += 1
    measurementUnit36ersEnabled = argsTuple[i]
    i += 1
    measurementUnit37ersEnabled = argsTuple[i]
    i += 1
    measurementUnit40ersEnabled = argsTuple[i]
    i += 1
    measurementUnit42ersEnabled = argsTuple[i]
    i += 1
    measurementUnit45ersEnabled = argsTuple[i]
    i += 1
    measurementUnit47ersEnabled = argsTuple[i]
    i += 1
    measurementUnit49ersEnabled = argsTuple[i]
    i += 1
    measurementUnit50ersEnabled = argsTuple[i]
    i += 1
    measurementUnit51ersEnabled = argsTuple[i]
    i += 1
    measurementUnit51_428ersEnabled = argsTuple[i]
    i += 1
    measurementUnit52ersEnabled = argsTuple[i]
    i += 1
    measurementUnit60ersEnabled = argsTuple[i]
    i += 1
    measurementUnit69ersEnabled = argsTuple[i]
    i += 1
    measurementUnit70ersEnabled = argsTuple[i]
    i += 1
    measurementUnit72ersEnabled = argsTuple[i]
    i += 1
    measurementUnit73ersEnabled = argsTuple[i]
    i += 1
    measurementUnit75ersEnabled = argsTuple[i]
    i += 1
    measurementUnit77ersEnabled = argsTuple[i]
    i += 1
    measurementUnit84ersEnabled = argsTuple[i]
    i += 1
    measurementUnit88ersEnabled = argsTuple[i]
    i += 1
    measurementUnit90ersEnabled = argsTuple[i]
    i += 1
    measurementUnit94ersEnabled = argsTuple[i]
    i += 1
    measurementUnit99ersEnabled = argsTuple[i]
    i += 1
    measurementUnit100ersEnabled = argsTuple[i]
    i += 1
    measurementUnit110ersEnabled = argsTuple[i]
    i += 1
    measurementUnit112ersEnabled = argsTuple[i]
    i += 1
    measurementUnit133ersEnabled = argsTuple[i]
    i += 1
    measurementUnit135ersEnabled = argsTuple[i]
    i += 1
    measurementUnit137ersEnabled = argsTuple[i]
    i += 1
    measurementUnit144ersEnabled = argsTuple[i]
    i += 1
    measurementUnit150ersEnabled = argsTuple[i]
    i += 1
    measurementUnit153ersEnabled = argsTuple[i]
    i += 1
    measurementUnit194ersEnabled = argsTuple[i]
    i += 1
    measurementUnit225ersEnabled = argsTuple[i]
    i += 1
    measurementUnit275ersEnabled = argsTuple[i]
    i += 1
    measurementUnit311ersEnabled = argsTuple[i]
    i += 1
    measurementUnit400ersEnabled = argsTuple[i]
    i += 1
    measurementUnit500ersEnabled = argsTuple[i]
    i += 1
    measurementUnit557ersEnabled = argsTuple[i]
    i += 1
    measurementUnit750ersEnabled = argsTuple[i]
    i += 1
    measurementUnit945ersEnabled = argsTuple[i]
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
    # Logging config file specifies the log filename relative to
    # the current directory, so we need to chdir to the SRC_DIR
    # before loading the logging config.
    SRC_DIR = os.path.abspath(sys.path[0])
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
