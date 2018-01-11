##############################################################################
The scripts in this directory create CSV files with information related to geocentric lunar dates.
##############################################################################


Usage:

1) Open the script file 'calculatePlanetLunarDates.py' and 
update the variables:

     - ephemeris location
     - start and end timestamps
     - list of desired lunar dates each year

2) Run the script:

    python3 calculatePlanetLunarDates.py

This should produce the following file:

    planetLunarDates.csv

3) The above will produce the results sorted by timestamp, follow the steps below:

Running the following commands below to produce the results sorted by timestamp.  The below assumes the second column is the Julian day.



INPUT_FILE=planetDirectAndRetrograde.csv
OUTPUT_FILE=planetDirectAndRetrograde_TimestampSorted.csv

COLUMN_TO_SORT_BY=2
TEMP_FILE=tempfile_for_sorting_purposes_only.csv

head -n 1 ${INPUT_FILE} > ${OUTPUT_FILE}
NUM_LINES=`wc -l ${INPUT_FILE} | cut -d' ' -f1`
NUM_LINES_CONTENT=`expr ${NUM_LINES} - 1`
echo ${NUM_LINES_CONTENT}

sort --field-separator=, --key=${COLUMN_TO_SORT_BY} ${INPUT_FILE} > ${TEMP_FILE}
head -n ${NUM_LINES_CONTENT} ${TEMP_FILE} >> ${OUTPUT_FILE}

rm ${TEMP_FILE}




##############################################################################
