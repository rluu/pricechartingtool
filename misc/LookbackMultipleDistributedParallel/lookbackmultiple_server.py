
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


def runServer():
    global serverAddress
    global serverPort
    global authKey

    # Start a shared manager server and access its queues.

    taskQueue = JoinableQueue()
    resultQueue = JoinableQueue()

    QueueManager.register("getTaskQueue", callable=lambda: taskQueue)
    QueueManager.register("getResultQueue", callable=lambda: resultQueue)
    
    manager = QueueManager(address=(serverAddress, serverPort), 
                              authkey=authKey)
    
    server = manager.get_server()

    log.info("LookbackMultiple server starting on port {}".format(serverPort))
    server.serve_forever()
    
    

##############################################################################

if __name__=="__main__":
    runServer()
