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
#   This server runs forever, until the user either does Ctrl-C or sends a
#   SIGINT signal to the process.
# 
# Usage:
#   
#   ./lookbackmultiple_server.py --server-address=192.168.1.200 --server-port=1940 --auth-key="passphrase"
#
#   ./lookbackmultiple_server.py --server-address=light.jumpingcrab.com --server-port=1940 --auth-key="passphrase"
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

# Server address (str).
# Either a hostname or an IP address.
# This value is obtained via command-line parameter.
serverAddress = ""

# Server port number (int).
# This value is obtained via command-line parameter.
serverPort = None

# Server auth key (bytes).
# This value is obtained via command-line parameter,
# by converting from str to bytes.
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
    log.info("LookbackMultiple server shutting down.")
    shutdown(0)

# Connect the SIGINT signal to the signal handler.
signal.signal(signal.SIGINT, signal_SIGINT_handler)

##############################################################################

class QueueManager(BaseManager):
    pass


def runServer():
    """Runs the server that is a multiprocessing Manager.
    This server manages task and result queues.

    This method should run forever until the user presses Ctrl-C or
    SIGINT is sent to the process.
    """
    global serverAddress
    global serverPort
    global serverAuthKey

    # Start a shared manager server and access its queues.

    taskQueue = JoinableQueue()
    resultQueue = JoinableQueue()

    QueueManager.register("getTaskQueue", callable=lambda: taskQueue)
    QueueManager.register("getResultQueue", callable=lambda: resultQueue)
    
    manager = QueueManager(address=(serverAddress, serverPort), 
                              authkey=serverAuthKey)
    
    server = manager.get_server()

    log.info("LookbackMultiple server starting on address {} and port {}".\
             format(serverAddress, serverPort))

    server.serve_forever()
    
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

    # Run the server.  
    #
    # This method should run forever until the user presses Ctrl-C or SIGINT is
    # sent to the process.
    runServer()

##############################################################################
