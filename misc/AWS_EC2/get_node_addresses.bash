#!/bin/bash
##############################################################################
# Prints out a list of public DNS names of the AWS EC2 instances running
# the image given in the 'AMI_ID' global variable below.
##############################################################################

# Global Variables
AMI_ID="ami-2691bd4e"

##############################################################################

# Get a list of all the instance IDs.
INSTANCE_IDS=`aws ec2 describe-instances  --filters "Name=image-id,Values=${AMI_ID}" | grep InstanceId | cut -d":" -f2 | cut -d"\"" -f2`

#echo "The list of instance ids that use AMI ${AMI_ID} are: ${INSTANCE_IDS}"

#echo "Now getting the DNS names of these instances..."

for instance_id in ${INSTANCE_IDS}; do

  #echo "Working on instance: ${instance_id} ..."
  
  publicDnsNameEntry=`aws ec2 describe-instances --filter "Name=instance-id,Values=${instance_id}" | grep PublicDnsName | grep -v "null" | tail -n 1`

  #echo -e "publicDnsNameEntry is: ${publicDnsNameEntry}"

  publicDnsNameEntryNoSpaces="$(echo -e "${publicDnsNameEntry}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

  #echo -e "publicDnsNameEntryNoSpaces is ${publicDnsNameEntryNoSpaces}"

  domainName="$(echo -e "${publicDnsNameEntryNoSpaces}" | cut -d":" -f2 | cut -d"\"" -f2)"

  #echo "Domain name is: ${domainName}"

  if [ -n "${domainName}" ]
  then
    echo "${domainName}"
  fi
done

#echo "done."

##############################################################################
