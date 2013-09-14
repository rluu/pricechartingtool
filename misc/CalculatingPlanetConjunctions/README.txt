##############################################################################
The scripts in this directory create CSV files with information related to planetary conjunctions, both geocentric and heliocentric.  
##############################################################################


Usage:

1) For geocentric planets, or heliocentric planets, open the
cooresponding script:

calculatePlanetGeocentricConjunctions.py
calculatePlanetHeliocentricConjunctions.py


2) Update variables
     - ephemeris location
     - start and end timestamps
     - desired planets for conjunctions.

3) Run the script:

    python3 calculatePlanetGeocentricConjunctions.py
    python3 calculatePlanetHeliocentricConjunctions.py


This should produce the following files, respectively:

    planetGeocentricConjunctions.csv
    planetHeliocentricConjunctions.csv


The above will produce the results sorted by planet combination.  
To get the results sorted by timestamp, follow the steps below:

Running the following commands below to produce the results sorted by timestamp.  The below assumes the second column is the Julian day.

###############

INPUT_FILE=planetGeocentricConjunctions.csv
OUTPUT_FILE=planetGeocentricConjunctions_TimestampSorted.csv

#INPUT_FILE=planetHeliocentricConjunctions.csv
#OUTPUT_FILE=planetHeliocentricConjunctions_TimestampSorted.csv

COLUMN_TO_SORT_BY=2
TEMP_FILE=tempfile_for_sorting_purposes_only.csv

head -n 1 ${INPUT_FILE} > ${OUTPUT_FILE}
NUM_LINES=`wc -l ${INPUT_FILE} | cut -d' ' -f1`
NUM_LINES_CONTENT=`expr ${NUM_LINES} - 1`
echo ${NUM_LINES_CONTENT}

sort --field-separator=, --key=${COLUMN_TO_SORT_BY} ${INPUT_FILE} > ${TEMP_FILE}
head -n ${NUM_LINES_CONTENT} ${TEMP_FILE} >> ${OUTPUT_FILE}

rm ${TEMP_FILE}


###############

##############################################################################
