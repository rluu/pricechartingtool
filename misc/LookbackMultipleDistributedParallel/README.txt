##############################################################################
Description:

This directory contains scripts to run LookbackMultiple calculations
distributed.

##############################################################################


##############################################################################
# To run LookbackMultiple calculations distributed.
##############################################################################


./lookbackmultiple_server.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password


./lookbackmultiple_client_worker.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password


python3 lookbackmultiple_client_tasker.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password




##############################################################################
# To kill the running processes via sending SIGINT signals:
##############################################################################


ps -ef | grep python3 | grep lookbackmultiple_server.py | awk -F" " '{print $2}' | xargs kill -s SIGINT


ps -ef | grep python3 | grep lookbackmultiple_client_worker.py | awk -F" " '{print $2}' | xargs kill -s SIGINT


##############################################################################
