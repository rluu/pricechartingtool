
import os
import sys

# For logging.
import logging
import logging.config

# For timestamps and timezone information.
import datetime
import pytz

# For timing the calculations.
import time

from multiprocessing.managers import BaseManager

from multiprocessing import JoinableQueue

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)

#from lookbackmultiple_parallel import LookbackMultipleParallel


##############################################################################

serverAddress = "192.168.1.200"
serverPort = 1940
authKey = b"ryans_password"

# For logging.
logLevel = logging.DEBUG
#logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)


##############################################################################

class QueueManager(BaseManager):
    pass


def runClientTasker():
    global serverAddress
    global serverPort
    global authKey

    # Connect to a manager server and access its queues.

    QueueManager.register("getTaskQueue", callable=lambda: taskQueue)
    QueueManager.register("getResultQueue", callable=lambda: resultQueue)
    
    manager = QueueManager(address=(serverAddress, serverPort), 
                           authkey=authKey)
    manager.connect()
    
    log.info("LookbackMultiple client tasker connected to {}:{}".\
             format(serverAddress, serverPort))
    
    taskQueue = manager.getTaskQueue()
    resultQueue = manager.getResultQueue()
    
    log.info("LookbackMultiple client tasker now creating tasks ...")
    
    speedTestDistributedParallel(taskQueue, resultQueue)

    log.info("LookbackMultiple client tasker is done.")


def speedTestDistributedParallel(taskQueue, resultQueue):
    """Tests to see how long it takes to do some distributed
    computations in parallel.
    """

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

        log.debug("  Testing G.MoSu, {} iterations, with maxErrorTd={}".\
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

            methodToRun = "getDatetimesOfLongitudeDeltaDegreesInFuture"
            #methodToRun = "getDatetimesOfLongitudeDeltaDegreesInPast"
            taskId = i

            args = (methodToRun,
                    taskId,
                    planetName, 
                    centricityType, 
                    longitudeType, 
                    referenceDt, 
                    desiredDeltaDegrees, 
                    maxErrorTd, 
                    locationLongitudeDegrees, 
                    locationLatitudeDegrees, 
                    locationElevationMeters)
            
            argsTupleList.append(args)

        # Submit tasks.
        log.debug("Submitting {} tasks ...".format(len(argsTupleList)))
        for argsTuple in argsTupleList:
            
            log.debug("About to submit argsTuple: {}".\
                      format(argsTuple))
            taskQueue.put(argsTuple)

        log.debug("Submitting of {} tasks completed.".\
                  format(len(argsTupleList)))
            
        # Block, waiting for all the tasks to complete.
        log.debug("Waiting for all tasks to complete ...")
        taskQueue.join()

        #log.debug("Tasks completed.  Now analyzing results ...")
        log.debug("Now analyzing results ...")
        
        resultCount = 0
        while resultCount < len(argsTupleList):

            # Get a result.
            (argsTuple, resultDts) = resultQueue.get()

            argIndex = 0
            methodToRun = argsTuple[argIndex]
            argIndex += 1
            taskId = argsTuple[argIndex]
            argIndex += 1
            planetName = argsTuple[argIndex]
            argIndex += 1
            centricityType = argsTuple[argIndex]
            argIndex += 1
            longitudeType = argsTuple[argIndex]
            argIndex += 1
            referenceDt = argsTuple[argIndex]
            argIndex += 1
            desiredDeltaDegrees = argsTuple[argIndex]
            argIndex += 1
            maxErrorTd = argsTuple[argIndex]
            argIndex += 1
            locationLongitudeDegrees = argsTuple[argIndex]
            argIndex += 1
            locationLatitudeDegrees = argsTuple[argIndex]
            argIndex += 1
            locationElevationMeters = argsTuple[argIndex]
            argIndex += 1
            
            endl = os.linesep

            argsTupleStr = \
                "methodToRun == {}".format(methodToRun) + endl + \
                "taskId == {}".format(taskId) + endl + \
                "planetName == {}".format(planetName) + endl + \
                "centricityType == {}".format(centricityType) + endl + \
                "longitudeType == {}".format(longitudeType) + endl + \
                "referenceDt == {}".format(referenceDt) + endl + \
                "desiredDeltaDegrees == {}".format(desiredDeltaDegrees) + endl + \
                "maxErrorTd == {}".format(maxErrorTd) + endl + \
                "locationLongitudeDegrees == {}".format(locationLongitudeDegrees) + endl + \
                "locationLatitudeDegrees == {}".format(locationLatitudeDegrees) + endl + \
                "locationElevationMeters == {}".format(locationElevationMeters)



            log.debug("Obtained result: " + \
                      "argsTuple == {}, ".format(argsTuple) + 
                      "len(resultDts) == {}".format(len(resultDts)))
            for i in range(len(resultDts)):
                dt = resultDts[i]
                log.debug("  resultDts[{}] == {}".format(i, dt))

            resultQueue.task_done()

            resultCount += 1
            log.debug("We have consumed {} total results now.".\
                      format(resultCount))
     
        log.debug("Done consuming all tasks submitted.") 
        endTime = time.time()

        log.debug("  Calculations in distributed parallel took: {} sec".\
              format(endTime - startTime))


##############################################################################

if __name__=="__main__":
    runClientTasker()
