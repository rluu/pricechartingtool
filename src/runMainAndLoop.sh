#!/bin/bash
##############################################################################

SRCDIR=$( cd "$( dirname "$0" )" && pwd )
PYTHON=/usr/bin/python3


# Store each digit of the python3 version.  
# Expected format of the version is: "X.Y.Z" (e.g. "3.2.1").
#
majorVersion=`${PYTHON} --version 2>&1 | gawk '{print $2}' | cut -d"." -f1`
minor1Version=`${PYTHON} --version 2>&1 | gawk '{print $2}' | cut -d"." -f2`
minor2Version=`${PYTHON} --version 2>&1 | gawk '{print $2}' | cut -d"." -f3`

#echo ${majorVersion}
#echo ${minor1Version}
#echo ${minor2Version}



while true; do 
  # Remove ".pyc" files from the source directory if the python3
  # version is less than 3.2.  We do this because prior to version 3.2,
  # python did not put the pyc files into repository directories.
  if [ ${majorVersion} -ge 3 -a ${minor1Version} -lt 2 ]
    then
      rm ${SRCDIR}/*.pyc
      sleep 1
  fi
  
  # Run main python source code file.
  ${PYTHON} ${SRCDIR}/main.py
done


##############################################################################
