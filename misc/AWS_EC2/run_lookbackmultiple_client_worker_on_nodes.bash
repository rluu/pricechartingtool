#!/bin/bash
##############################################################################

EC2_SSH_IDENTITY_KEY_FILE="/home/rluu/aws_mykeypair.pem"
USERNAME="ec2-user"

# Parameters for script 'lookbackmultiple_client_worker.py'.
SERVER_ADDRESS="light.jumpingcrab.com"
SERVER_PORT="1940"
SERVER_AUTH_KEY="password"

# Number of script instances to run per node.
NUM_SCRIPT_INSTANCES_PER_NODE="1"

##############################################################################

# Directory where this script resides.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd -P "$( dirname "$SOURCE" )" && pwd )"

#echo "DIR is ${DIR}"


pricechartingtool_dir="~/programming/pricechartingtool/master"
virtualenv_activate_cmd="source ${pricechartingtool_dir}/venv/bin/activate"

script_root_dir="${pricechartingtool_dir}/misc/LookbackMultipleDistributedParallel"

script_to_run="${script_root_dir}/lookbackmultiple_client_worker.py --server-address=${SERVER_ADDRESS} --server-port=${SERVER_PORT} --auth-key=${SERVER_AUTH_KEY}"

script_to_run_stdout_file="${script_root_dir}/lookbackmultiple_client_worker.out.txt"
script_to_run_stderr_file="${script_root_dir}/lookbackmultiple_client_worker.err.txt"

get_addresses_script="${DIR}/get_node_addresses.bash"

#echo "script_to_run is: ${script_to_run}"

addresses="`${get_addresses_script} | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g'`"

num_addresses="`echo ${addresses} | wc -w`" 

echo "Number of nodes: ${num_addresses}"
echo ""
echo "The addresses of the nodes are: ${addresses}"
echo ""

ssh_options=" -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ${EC2_SSH_IDENTITY_KEY_FILE}"


for address in ${addresses}; do
  for (( i = 0; i < ${NUM_SCRIPT_INSTANCES_PER_NODE}; i++ )); do

    echo "Running lookbackmultiple_client_worker.py on node: ${address}"
    ssh ${ssh_options} ${USERNAME}@${address} "sh -c '${virtualenv_activate_cmd}; nohup ${script_to_run} > ${script_to_run_stdout_file} 2> ${script_to_run_stderr_file} < /dev/null &'"

  done
done

echo ""
echo "Done."


  
##############################################################################
