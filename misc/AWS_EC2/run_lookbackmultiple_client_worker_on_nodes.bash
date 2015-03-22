#!/bin/bash
##############################################################################
# This script runs lookbackmultiple_client_worker.py in the background
# on all the addresses returned by the script
# 'get_node_addresses.bash'.  The lookbackmultiple_client_worker.py
# script execution is initiated via ssh, and it is assumed that all
# these nodes are AWS EC2 instances.
#
# The parameters used for SSH login are defined below, in variables.
#
# The parameters passed to the lookbackmultiple_client_worker.py
# script are defined below, in variables.
##############################################################################

# SSH login parameters for each of the AWS EC2 nodes.
EC2_SSH_IDENTITY_KEY_FILE="/home/rluu/aws_mykeypair.pem"
USERNAME="ec2-user"

# Parameters for the 'lookbackmultiple_client_worker.py' script
# that is used to connect to a LookbackMultiple server.
SERVER_ADDRESS="light.jumpingcrab.com"
SERVER_PORT="1940"
SERVER_AUTH_KEY="password"

# Number of script instances to run per node.  
# 
# It is recommended to set this to the number of processors or cores
# that exist on each AWS EC2 instance.
NUM_SCRIPT_INSTANCES_PER_NODE="1"

##############################################################################

# Directory where this script resides.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd -P "$( dirname "$SOURCE" )" && pwd )"

#echo "DIR is ${DIR}"

# Top-level directory.
pricechartingtool_dir="~/programming/pricechartingtool/master"

# Command to be run on the node to enable the virtualenv Python 3 environment.
virtualenv_activate_cmd="source ${pricechartingtool_dir}/venv/bin/activate"

# Root directory of the script to be run, on the node.
script_root_dir="${pricechartingtool_dir}/misc/LookbackMultipleDistributedParallel"

# Full path of the script to be run, on the node.
script_to_run="${script_root_dir}/lookbackmultiple_client_worker.py --server-address=${SERVER_ADDRESS} --server-port=${SERVER_PORT} --auth-key=${SERVER_AUTH_KEY}"
#echo "script_to_run is: ${script_to_run}"


# Ouptut file for stdout output of the script, on the node.
script_to_run_stdout_file="${script_root_dir}/lookbackmultiple_client_worker.out.txt"

# Ouptut file for stderr output of the script, on the node.
script_to_run_stderr_file="${script_root_dir}/lookbackmultiple_client_worker.err.txt"

# Script that will return the AWS EC2 instances' public DNS hostnames 
# (these are the addresses to our compute nodes).
get_addresses_script="${DIR}/get_node_addresses.bash"

# List of compute node addresses, separated by spaces, all on one line.
addresses="`${get_addresses_script} | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g'`"

# Variable holding the number of compute node addresses.
num_addresses="`echo ${addresses} | wc -w`" 

echo "Number of nodes: ${num_addresses}"
echo ""
echo "The addresses of the nodes are: ${addresses}"
echo ""

# Options to pass to SSH for login and script execution without a password.
ssh_options=" -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ${EC2_SSH_IDENTITY_KEY_FILE}"


# Loop through each of the node addresses, running the script in the
# background, 'NUM_SCRIPT_INSTANCES_PER_NODE' times per node.
#
for address in ${addresses}; do
  for (( i = 0; i < ${NUM_SCRIPT_INSTANCES_PER_NODE}; i++ )); do

    echo "Running lookbackmultiple_client_worker.py on node: ${address}"

    ssh ${ssh_options} ${USERNAME}@${address} "sh -c '${virtualenv_activate_cmd}; nohup ${script_to_run} > ${script_to_run_stdout_file} 2> ${script_to_run_stderr_file} < /dev/null &'"

  done
done

echo ""
echo "Done."

##############################################################################
