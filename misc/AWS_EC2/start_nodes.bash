#!/bin/bash
##############################################################################
# This script creates and starts 'On-Demand' AWS EC2 instances
# according to the parameters given in the variables below.
##############################################################################

AMI_ID="ami-5cb18534"
INSTANCE_COUNT="10"
INSTANCE_TYPE="t2.micro"
KEY_NAME="mykeypair"
SECURITY_GROUPS="ssh_only"

##############################################################################

aws ec2 run-instances --image-id ${AMI_ID} --count ${INSTANCE_COUNT} --instance-type ${INSTANCE_TYPE} --key-name ${KEY_NAME} --security-groups ${SECURITY_GROUPS}

##############################################################################
