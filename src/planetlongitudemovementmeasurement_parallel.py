

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
