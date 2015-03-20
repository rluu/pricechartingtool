##############################################################################
This directory contains scripts for creating EC2 instances, running scripts on them, and terminating the EC2 instances.
##############################################################################


Dependencies:

bash
ssh 
aws command line tool.

##############################################################################

Usage steps:


1) Run the script to start the LookbackMultiple server.

  ./misc/LookbackMultipleDistributedParallel/lookbackmultiple_server.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password


2) Adjust firewall settings on the home internet router to allow incoming connections to the server port.

  http://192.168.1.1/


3) Open script ./start_nodes.bash and ensure that the variable for the number of EC2 instances to create on AWS is set as desired.  If not, modify the variable to be the number of EC2 instances desired.

  emacs start_nodes.bash


4) Run the script to start the nodes.  This will create them using the AMI image containing the Python3 source code and dependencies:

  ./start_nodes.bash


It will take some time for the nodes to boot up.  You can run ec2-describe-instance-status to print out the current states of the instances you own and wait for them to all be running.  When the output doesn't have 'initializing', then they have finished starting up.
http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-DescribeInstanceStatus.html


5) Run my LookbackMultiple client worker code on each of the started nodes.

  ./run_lookbackmultiple_client_worker_on_nodes.bash


5b) Optionally, run client worker code on any other computers on my home/personal network.  

  ./lookbackmultiple_client_worker.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password


6) Run the PriceChartingTool UI with the remote parallel LookbackMultiple calculation options enabled in the App Preferences dialog.  Alternatively, run the command-line script to task the LookbackMultiple server.

  ./lookbackmultiple_client_tasker.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password


7) When you're done with the needed computations/calculations in the UI or command-line, terminate all the EC2 instances, which will release all the EBS store volumes back to AWS.  This is what we want, since we always create the EC2 instances and their EBS volumes from our private customized AMI.  

  ./terminate_nodes.bash


##############################################################################


Steps to add more nodes when the server and client_workers are already running:


1) Ctrl-C on the LookbackMultiple server script.  This will cause an EOFError on all connected client workers.  


  Ctrl-C on:    ./lookbackmultiple_server.py


2) Modify start_nodes.bash and set the INSTANCE_COUNT variable to the number of additional instances that you want.  

  emacs start_nodes.bash

3) Follow the normal steps earlier in this README.txt file, above.


##############################################################################

