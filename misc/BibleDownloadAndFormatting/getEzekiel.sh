#!/bin/bash
##############################################################################
# 
# Description: 
#
#   This script uses wget to download HTML files of Bible books and
#   places those HTML files in the directory specified by the variable
#   ${DESTINATION_DIR}.
#
# Source website for the Bible books:
#
#   http://www.blueletterbible.org/Bible.cfm
#
# Usage:
#   
#   1) Ensure the global variables are set correctly.  
#      (They should already be all good to go).
#
#   2) Run the script:
#
#      ./getEzekiel.sh
#
##############################################################################

# URL variable for what Bible to download.
# Currently, the website only supports KJV.
BIBLE="KJV"

# URL variable for what Bible book to download.
BOOK="Eze"

# URL variable for which chapter to download.  
# This is modified by the loop variable.
CHAPTER="0"

# Start and end chapters to download, inclusive.
START_CHAPTER="1"
END_CHAPTER="48"

# Output directory for all the HTML files.  
# This directory gets created if it doesn't already exist.
DESTINATION_DIR="Ezekiel"

######################################


# Create output directory if it doesn't already exist.
mkdir -p "${DESTINATION_DIR}"
PREVDIR=`pwd`

cd "${DESTINATION_DIR}"


# Loop, downloading each chapter of the book.
for i in `seq ${START_CHAPTER} ${END_CHAPTER}`; do 
CHAPTER=$i

# Here we have a variable created and set so that the chapter number
# in the filename of the HTML file will be a fixed width.
CHAPTER_FOR_OUTPUT_FILE=""

if [ ${CHAPTER} -lt 10 ]; then 
  CHAPTER_FOR_OUTPUT_FILE="00${CHAPTER}"
elif [ ${CHAPTER} -lt 100 ]; then
  CHAPTER_FOR_OUTPUT_FILE="0${CHAPTER}"
else
  CHAPTER_FOR_OUTPUT_FILE="${CHAPTER}"
fi

wget -k -E -H --output-document="${BOOK}_${CHAPTER_FOR_OUTPUT_FILE}.html" "http://www.blueletterbible.org/Bible.cfm?b=${BOOK}&c=${CHAPTER}&v=1&t=${BIBLE}&sstr=1"

done




cd "${PREVDIR}"

######################################
