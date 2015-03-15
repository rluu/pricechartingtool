#!/usr/bin/env python3
##############################################################################
# 
# Description:
# 
#   Runs a server that is a Python multiprocessing Manager for managing task
#   queues and result queues.  Accepts connections on a certain port from other
#   multiprocessing clients that are either workers or taskers.  Work tasks
#   submitted to the task queue by the tasker is pulled out and consumed by the
#   workers.  When the worker completes the task, the worker puts the result
#   that is computed for the task onto the result queue.  The tasker can then
#   pull results from the result queue.  There can be many workers in this
#   model.
#   
# Usage:
#   
#   ./lookbackmultiple_client_tasker.py --server-address=192.168.1.200 --server-port=1940 --auth-key="passphrase"
#
#   ./lookbackmultiple_client_tasker.py --server-address=light.jumpingcrab.com --server-port=1940 --auth-key="passphrase"
#
#
##############################################################################

# For obtaining current directory path information.
import os
import sys

# For logging.
import logging
import logging.config

# For timestamps and timezone information.
import datetime
import pytz

# For catching the signal interrupt.
import signal

# For parsing command-line options.
from optparse import OptionParser  

# For timing the calculations.
import time

# For multiprocessing features.
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

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Server address.  
# This value is obtained via command-line parameter.
serverAddress = ""

# Server port number.
# This value is obtained via command-line parameter.
serverPort = None

# Server auth key.
# This value is obtained via command-line parameter.
serverAuthKey = b""


# For logging.
#logLevel = logging.DEBUG
logLevel = logging.INFO
#logging.basicConfig(format='%(levelname)s: %(message)s')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""

    logging.shutdown()
    sys.exit(rc)

def signal_SIGINT_handler(signal, frame):
    """Handles when SIGINT is received."""

    log.info("Caught SIGINT.")
    log.info("LookbackMultiple client tasker shutting down.")
    shutdown(0)

# Connect the SIGINT signal to the signal handler.
signal.signal(signal.SIGINT, signal_SIGINT_handler)

##############################################################################

class QueueManager(BaseManager):
    pass

def runClientTasker():
    global serverAddress
    global serverPort
    global serverAuthKey

    # Connect to a manager server and access its queues.

    QueueManager.register("getTaskQueue", callable=lambda: taskQueue)
    QueueManager.register("getResultQueue", callable=lambda: resultQueue)
    
    manager = QueueManager(address=(serverAddress, serverPort), 
                           authkey=serverAuthKey)
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

        log.info("  Testing G.MoSu, {} iterations, with maxErrorTd={}".\
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
        log.info("Submitting {} tasks ...".format(len(argsTupleList)))
        for argsTuple in argsTupleList:
            
            log.debug("About to submit argsTuple: {}".\
                      format(argsTuple))
            taskQueue.put(argsTuple)

        log.info("Submitting of {} tasks completed.".\
                  format(len(argsTupleList)))
            
        # Block, waiting for all the tasks to complete.
        log.info("Waiting for all tasks to complete ...")
        taskQueue.join()

        #log.debug("Tasks completed.  Now analyzing results ...")
        log.info("Now analyzing results ...")
        
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
            log.info("We have consumed {} total results now.".\
                      format(resultCount))
     
        log.info("Done consuming all tasks submitted.") 
        endTime = time.time()

        log.info("  Calculations in distributed parallel took: {} sec".\
              format(endTime - startTime))


##############################################################################

if __name__=="__main__":
    # Create the parser
    parser = OptionParser()

    # Specify all valid options.
    parser.add_option("-v", "--version",
                      action="store_true",
                      dest="version",
                      default=False,
                      help="Display script version info and author contact.")
    
    parser.add_option("--server-address",
                  action="store",
                  type="str",
                  dest="serverAddress",
                  default=None,
                  help="Specify the server hostname or IP address.  " + \
                       "Example: '192.168.1.200'.  " + \
                       "Example: 'mycomputer.example.com'.  " + \
                       "This is a required field.",
                  metavar="<ADDRESS>")

    parser.add_option("--server-port",
                  action="store",
                  type="int",
                  dest="serverPort",
                  default=None,
                  help="Specify the server port number.  " + \
                       "Example: '9999'.  " + \
                       "This is a required field.",
                  metavar="<PORT>")

    parser.add_option("--auth-key",
                  action="store",
                  type="str",
                  dest="serverAuthKey",
                  default=None,
                  help="Specify server authentication key-phrase.  " + \
                       "Example: 'passphrase'.  ",
                  metavar="<PASSWORD>")

    # Parse the arguments into options.
    (options, args) = parser.parse_args()
     
    # Print version information if the flag was used.
    if options.version == True:
        print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
        print("By Ryan Luu, ryanluu@gmail.com")
        shutdown(0)
    
    # Server address argument.
    if options.serverAddress == None:
        log.error("Please specify a server address to the " + \
                  "--server-address option.")
        shutdown(1)
    else:
        serverAddress = options.serverAddress
        log.debug("serverAddress == {}".format(serverAddress))
    
    # Server port argument.
    if options.serverPort == None:
        log.error("Please specify a server port to the " + \
                  "--server-port option.")
        shutdown(1)
    else:
        serverPort = options.serverPort
        log.debug("serverPort == {}".format(serverPort))
    
    # Server authentication key argument.
    if options.serverAuthKey == None:
        log.error("Please specify a server auth key to the " + \
                  "--auth-key option.")
        shutdown(1)
    else:
        serverAuthKey = options.serverAuthKey.encode("utf-8")
        log.debug("serverAuthKey == {}".format(serverAuthKey))

    # Run the client tasker.
    #
    # This runs until the tasks submitted return with results.
    runClientTasker()

##############################################################################
