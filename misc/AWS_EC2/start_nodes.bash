#!/bin/bash

AMI_ID="ami-2691bd4e"
INSTANCE_COUNT="3"
INSTANCE_TYPE="t2.micro"
KEY_NAME="mykeypair"
SECURITY_GROUPS="ssh_only"

aws ec2 run-instances --image-id ${AMI_ID} --count ${INSTANCE_COUNT} --instance-type ${INSTANCE_TYPE} --key-name ${KEY_NAME} --security-groups ${SECURITY_GROUPS}


