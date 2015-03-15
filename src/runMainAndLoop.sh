#!/bin/bash
##############################################################################

SRCDIR=$( cd "$( dirname "$0" )" && pwd )
PYTHON="/usr/bin/env python3"


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

  # Remove ".pyc" files from the source directory if those artifacts
  # are produced in the source directory.  
  # Python version 3.2 puts these .pyc files in a __pycache__ directory, 
  # which is fine there.

  PYC_FILES=`find ${SRCDIR} -maxdepth 0 -name "*.pyc"`
  #echo "DEBUG: The .pyc files found in the source directory are: ${PYC_FILES}"

  for file in ${PYC_FILES}; do
      echo "Removing file: ${file} ..."
      rm ${file}
  done

  sleep 1

  # Run main python source code file.
  ${PYTHON} ${SRCDIR}/main.py
done


##############################################################################
