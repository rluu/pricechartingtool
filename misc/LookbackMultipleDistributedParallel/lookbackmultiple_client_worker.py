
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

from lookbackmultiple_calc import LookbackMultipleUtils



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


def runClientWorker():
    global serverAddress
    global serverPort
    global authKey

    # Connect to a manager server and access its queues.

    QueueManager.register("getTaskQueue", callable=lambda: taskQueue)
    QueueManager.register("getResultQueue", callable=lambda: resultQueue)
    
    manager = QueueManager(address=(serverAddress, serverPort), 
                           authkey=authKey)
    manager.connect()
    
    log.info("LookbackMultiple client worker connected to {}:{}".\
             format(serverAddress, serverPort))
    
    taskQueue = manager.getTaskQueue()
    resultQueue = manager.getResultQueue()
    
    log.info("LookbackMultiple client worker now processing taskQueue ...")
    
    # Process the queues.
    done = False
    while not done:
        argsTuple = taskQueue.get() # If queue is empty, then this will block.
        
        log.debug("Obtained a task.  argsTuple == {}".format(argsTuple))

        if argsTuple is None:
            done = True

            log.debug("LookbackMultiple client worker received None argument.")
    
        else:
            # Do computation.
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
            

            LookbackMultipleUtils.\
                initializeEphemeris(locationLongitudeDegrees, 
                                    locationLatitudeDegrees,
                                    locationElevationMeters)
    
            if methodToRun == "getDatetimesOfLongitudeDeltaDegreesInFuture":

                resultDts = \
                    LookbackMultipleUtils.\
                    getDatetimesOfLongitudeDeltaDegreesInFuture(\
                        planetName, 
                        centricityType,
                        longitudeType,
                        referenceDt,
                        desiredDeltaDegrees,
                        maxErrorTd)
                
                result = (argsTuple, resultDts)
                
                resultQueue.put(result)
                
                taskQueue.task_done()

            elif methodToRun == "getDatetimesOfLongitudeDeltaDegreesInPast":
                resultDts = \
                    LookbackMultipleUtils.\
                    getDatetimesOfLongitudeDeltaDegreesInFuture(\
                        planetName, 
                        centricityType,
                        longitudeType,
                        referenceDt,
                        desiredDeltaDegrees,
                        maxErrorTd)

                result = (argsTuple, resultDts)
                
                resultQueue.put(result)
                
                taskQueue.task_done()

    log.info("LookbackMultiple client worker is done.")

##############################################################################

if __name__=="__main__":
    runClientWorker()
