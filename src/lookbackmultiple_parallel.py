

# Pool of processes for calculating LookbackMultiples.
from multiprocessing import Pool

import os
    

def getDatetimesOfLongitudeDeltaDegreesInFuture(argsTuple):
    """Method that is distrubted to dispy's nodes ('dispynode') for
    remote execution.  Module dependencies are imported within the
    method below.
    
    This method runs the following method:

      lookbackmultiple_calc.LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture()

    Please see documentation for that method for information about 
    the functionality, method arguments, and return value(s).
    """
    

    from lookbackmultiple_calc import LookbackMultipleUtils

    planetName = argsTuple[0]
    centricityType = argsTuple[1]
    longitudeType = argsTuple[2]
    referenceDt = argsTuple[3]
    desiredDeltaDegrees = argsTuple[4]
    maxErrorTd = argsTuple[5]
    locationLongitudeDegrees = argsTuple[6]
    locationLatitudeDegrees = argsTuple[7]
    locationElevationMeters = argsTuple[8]

    LookbackMultipleUtils.initializeEphemeris(locationLongitudeDegrees, 
                                              locationLatitudeDegrees,
                                              locationElevationMeters)
    
    return LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInFuture(\
        planetName, 
        centricityType,
        longitudeType,
        referenceDt,
        desiredDeltaDegrees,
        maxErrorTd)
        
    
def getDatetimesOfLongitudeDeltaDegreesInPast(argsTuple):
    """Method that is distrubted to dispy's nodes ('dispynode') for
    remote execution.  Module dependencies are imported within the
    method below.
    
    This method runs the following method:

      lookbackmultiple_calc.LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast()

    Please see documentation for that method for information about 
    the functionality, method arguments, and return value(s).
    """
        
    from lookbackmultiple_calc import LookbackMultipleUtils
    
    planetName = argsTuple[0]
    centricityType = argsTuple[1]
    longitudeType = argsTuple[2]
    referenceDt = argsTuple[3]
    desiredDeltaDegrees = argsTuple[4]
    maxErrorTd = argsTuple[5]
    locationLongitudeDegrees = argsTuple[6]
    locationLatitudeDegrees = argsTuple[7]
    locationElevationMeters = argsTuple[8]

    LookbackMultipleUtils.initializeEphemeris(locationLongitudeDegrees, 
                                              locationLatitudeDegrees,
                                              locationElevationMeters)
    
    return LookbackMultipleUtils.getDatetimesOfLongitudeDeltaDegreesInPast(\
        planetName, 
        centricityType,
        longitudeType,
        referenceDt,
        desiredDeltaDegrees,
        maxErrorTd)
    

class LookbackMultipleParallel:
    
    poolSize = os.cpu_count()
    
    pool = Pool(poolSize)
    
    @staticmethod
    def getDatetimesOfLongitudeDeltaDegreesInFutureParallel(listOfTuples):
        """
        Arguments:
        listOfTuples - List of tuple objects.  Each tuple has 
                       the following within it:
            
            planetName - str holding the name of the planet to do the
                         calculations for.
            centricityType - str value holding either "geocentric",
                             "topocentric", or "heliocentric".
            longitudeType - str value holding either "tropical" or "sidereal".
            referenceDt - datetime.datetime object for the reference time.
                          The planet longitude at this moment is taken as
                          the zero-point.  Increments or decrements in time 
                          are started from this moment in time.
            desiredDeltaDegrees - float value for the number of 
                            longitude degrees elapsed from the 
                            longitude at 'referenceDt'.
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
        List of list of datetime.datetime objects.
        Each list within the list corresponds to the
        respective tuple within listOfTuples
        The datetime.datetime objects are the timestamps
        where the planet is at the elapsed number of
        degrees away from the longitude at 'referenceDt'.
        """

        listOfResults = \
            LookbackMultipleParallel.pool.map(
                getDatetimesOfLongitudeDeltaDegreesInFuture, listOfTuples)
            
        return listOfResults

    @staticmethod
    def getDatetimesOfLongitudeDeltaDegreesInPastParallel(listOfTuples):
        """
        Arguments:
        listOfTuples - List of tuple objects.  Each tuple has 
                       the following within it:
            
            planetName - str holding the name of the planet to do the
                         calculations for.
            centricityType - str value holding either "geocentric",
                             "topocentric", or "heliocentric".
            longitudeType - str value holding either "tropical" or "sidereal".
            referenceDt - datetime.datetime object for the reference time.
                          The planet longitude at this moment is taken as
                          the zero-point.  Increments or decrements in time 
                          are started from this moment in time.
            desiredDeltaDegrees - float value for the number of 
                            longitude degrees elapsed from the 
                            longitude at 'referenceDt'.
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
        List of list of datetime.datetime objects.
        Each list within the list corresponds to the
        respective tuple within listOfTuples
        The datetime.datetime objects are the timestamps
        where the planet is at the elapsed number of
        degrees away from the longitude at 'referenceDt'.
        """
        
        listOfResults = \
            LookbackMultipleParallel.pool.map(\
                getDatetimesOfLongitudeDeltaDegreesInPast, listOfTuples)
            
        return listOfResults

    @staticmethod
    def shutdown():
        LookbackMultipleParallel.pool.close()
            
            
##############################################################################

def testLookbackMultipleParallel_speedTestParallel():
    """Tests to see how long it takes to do some computations in parallel."""

    print("Running " + inspect.stack()[0][3] + "()")
    
    # For timing the calculations.
    import time

    eastern = pytz.timezone('US/Eastern')
    maxErrorTd = datetime.timedelta(seconds=2)
    locationLongitudeDegrees = -74.0064
    locationLatitudeDegrees = 40.7142
    locationElevationMeters = 0

    if True:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)
        
        numIterations = 8

        print("  Testing G.MoSu, {} iterations, with maxErrorTd={}".\
              format(numIterations, maxErrorTd))
        
        startTime = time.time()
        
        argsTupleList = []
        resultsList = []

        for i in range(numIterations):
            planetName="MoSu"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            #desiredDeltaDegrees = 360 * 360
            desiredDeltaDegrees = 360 * ((i+1) * 37)

            args = (planetName, centricityType, longitudeType, referenceDt, 
                    desiredDeltaDegrees, maxErrorTd, 
                    locationLongitudeDegrees, 
                    locationLatitudeDegrees, 
                    locationElevationMeters)
        
            argsTupleList.append(args)

        # Compute results.
        resultsList = \
            LookbackMultipleParallel.\
            getDatetimesOfLongitudeDeltaDegreesInFutureParallel(argsTupleList)
        
        for i in range(len(resultsList)):
            print("  JobSubmission {}:".format(i))
            resultDts = resultsList[i]
            
            for j in range(len(resultDts)):
                resultDt = resultDts[j]
                print("    resultDt[{}] == {}".format(j, resultDt))
        

        endTime = time.time()
        print("  Calculations in parallel took: {} sec".\
              format(endTime - startTime))


def testLookbackMultipleParallel_speedTestSerial():
    """Tests to see how long it takes to do some computations in serial."""

    print("Running " + inspect.stack()[0][3] + "()")
    
    # For timing the calculations.
    import time

    # For directly calling the computation methods.
    from lookbackmultiple_calc import LookbackMultipleUtils

    eastern = pytz.timezone('US/Eastern')
    maxErrorTd = datetime.timedelta(seconds=2)
    locationLongitudeDegrees = -74.0064
    locationLatitudeDegrees = 40.7142
    locationElevationMeters = 0

    if True:
        maxErrorTd = datetime.timedelta(minutes=60)
        #maxErrorTd = datetime.timedelta(minutes=5)
        #maxErrorTd = datetime.timedelta(seconds=2)
        
        numIterations = 8

        print("  Testing G.MoSu, {} iterations, with maxErrorTd={}".\
              format(numIterations, maxErrorTd))
        
        startTime = time.time()
        
        argsTupleList = []
        resultsList = []

        for i in range(numIterations):
            planetName="MoSu"
            centricityType="geocentric"
            longitudeType="tropical"
            referenceDt = datetime.datetime(1994, 10, 20, 0, 0, tzinfo=pytz.utc)
            #desiredDeltaDegrees = 360 * 360
            desiredDeltaDegrees = 360 * ((i+1) * 37)

            LookbackMultipleUtils.initializeEphemeris(locationLongitudeDegrees, 
                                                      locationLatitudeDegrees,
                                                      locationElevationMeters)
    
            resultDts = \
                LookbackMultipleUtils.\
                getDatetimesOfLongitudeDeltaDegreesInFuture(
                    planetName, centricityType, longitudeType, referenceDt, 
                    desiredDeltaDegrees, maxErrorTd)

            resultsList.append(resultDts)


        for i in range(len(resultsList)):
            print("  JobSubmission {}:".format(i))
            resultDts = resultsList[i]
            
            for j in range(len(resultDts)):
                resultDt = resultDts[j]
                print("    resultDt[{}] == {}".format(j, resultDt))
        

        endTime = time.time()
        print("  Calculations in serial took: {} sec".\
              format(endTime - startTime))


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
        testLookbackMultipleParallel_speedTestParallel()
        testLookbackMultipleParallel_speedTestSerial()

    #startTime = time.time()
    runTests()
    #endTime = time.time()

    #print("")
    #print("Running all tests took: {} sec".format(endTime - startTime))

    #cProfile.run('runTests()')
    
    # Exit the app when all windows are closed.
    #app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    #app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    #app.exec_()

    # Quit.
    print("Exiting.")
    sys.exit()

##############################################################################
