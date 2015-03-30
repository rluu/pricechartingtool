#!/bin/bash
##############################################################################
# Terminates all the AWS EC2 instances running the AMI image given in the
# 'AMI_ID' variable below.
##############################################################################

AMI_ID="ami-5cb18534"

##############################################################################

# Get a list of all the instance IDs.
INSTANCE_IDS=`aws ec2 describe-instances  --filters "Name=image-id,Values=${AMI_ID}" | grep InstanceId | cut -d":" -f2 | cut -d"\"" -f2`

#echo "The list of instance ids that use AMI ${AMI_ID} are: ${INSTANCE_IDS}"

for instance_id in ${INSTANCE_IDS}; do

  #echo "Working on instance: ${instance_id} ..."
  
  aws ec2 terminate-instances --instance-ids "${instance_id}"

done

##############################################################################
