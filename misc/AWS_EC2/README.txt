##############################################################################

Description: 

This directory contains scripts for creating AWS EC2 instances,
running my LookbackMultiple calculation scripts on them 
(for calculating dates of cycle periods for cycle hunting/research), 
and terminating the EC2 instances.  Please see the usage steps below for
how to get this all working.

##############################################################################

Dependencies:

- bash
- ssh 
- Python 3, my Python source code, and dependencies.
- aws command line tool.


##############################################################################

Usage steps:


1) Adjust firewall settings on the home internet router to allow incoming connections to the server port.

  http://192.168.1.1/


2) Run the script to start the LookbackMultiple server.

  ./misc/LookbackMultipleDistributedParallel/lookbackmultiple_server.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password



3) Start some EC2 instances on Amazon Web Services (AWS).  This can be done on Amazon's AWS management console in the web browser, or it can be done via scripts that I've written.  Below are the steps to start on-demand EC2 instances via my scripts.  To use spot EC2 instances, please use the AWS management console (https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#SpotInstances:sort=requestId).  

Open script ./start_nodes.bash and ensure that the variable for the number of EC2 instances to create on AWS is set as desired.  If not, modify the variable to be the number of EC2 instances desired.

  emacs ./misc/AWS_EC2/start_nodes.bash

Run the script to create and start the EC2 nodes.  This will create them using the AMI image containing my PriceChartingTool source code and all needed dependencies:

  ./misc/AWS_EC2/start_nodes.bash

It will take some time for the nodes to boot up.  You can run ec2-describe-instance-status to print out the current states of the instances you own and wait for them to all be running.  When the output doesn't have 'initializing', then they have finished starting up.
http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-DescribeInstanceStatus.html


5) The next step is to run my LookbackMultiple client worker code on each of the started nodes.  Running the script below will launch the client worker script on each AWS EC2 instance.

  ./misc/AWS_EC2/run_lookbackmultiple_client_worker_on_nodes.bash

5b) Optionally, run client worker code on any other computers on my home/personal network.  

  ./misc/LookbackMultipleDistributedParallel/lookbackmultiple_client_worker.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password


6) Run the PriceChartingTool UI with the remote parallel LookbackMultiple calculation options enabled in the App Preferences dialog.  Or alternatively, run the command-line script to task the LookbackMultiple server.

  ./misc/LookbackMultipleDistributedParallel/lookbackmultiple_client_tasker.py --server-address=192.168.1.200 --server-port=1940 --auth-key=password


7) When you're done with the needed computations/calculations in the UI or command-line, terminate all the EC2 instances, which will release all the EBS store volumes back to AWS.  This is what we want, since we always create the EC2 instances and their EBS volumes from our private customized AMI.  

  ./misc/AWS_EC2/terminate_nodes.bash

8) Finally, Ctrl-C on the lookbackmultiple_server.py script to stop the server.  Or alternatively, you can run the following to send a SIGINT signal to it.

ps -ef | grep python3 | grep lookbackmultiple_server.py | awk -F" " '{print $2}' | xargs kill -s SIGINT


9) Ensure that all client workers are stopped.

In the previous step, closing the lookbackmultiple_server.py script should have caused the lookbackmultiple client worker scripts to abort with an EOFError, but if this did not happen, you should also ensure they exit by doing a Ctrl-C on them also.  Or, alternatively, you can run the following to send a SIGINT signal to it.  

ps -ef | grep python3 | grep lookbackmultiple_client_worker.py | awk -F" " '{print $2}' | xargs kill -s SIGINT


##############################################################################

Steps to add more nodes when the server and client_workers are already running:


1) Ctrl-C on the LookbackMultiple server script.  This will cause an EOFError on all connected client workers and cause them all to stop running.


  Ctrl-C on:    ./lookbackmultiple_server.py


2) Modify start_nodes.bash and set the INSTANCE_COUNT variable to the number of _additional_ instances that you want.  

  emacs start_nodes.bash

3) Follow the normal steps earlier in this README.txt file, above.


##############################################################################

