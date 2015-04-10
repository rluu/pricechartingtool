
# Commands that were run to get the CSV data:

for i in `seq 1959 2015`; do wget https://www.quandl.com/api/v1/datasets/CME/WZ${i}.csv; done;


# COmmands run to do the CSV file format conversion.

#!/bin/bash

DATADIR=/home/rluu/programming/pricechartingtool/master/data/pricebars/futures/ZW/Quandl/from_quandl_dot_com

OUTPUTDIR=/home/rluu/programming/pricechartingtool/master/data/pricebars/futures/ZW/Quandl/from_quandl_dot_com_converted

convertScript=/home/rluu/programming/pricechartingtool/master/misc/DataFormatting/Quandl/reformatFuturesData_Quandl_CSV_File.py

mergeAndAppendScript=/home/rluu/programming/pricechartingtool/master/misc/DataFormatting/mergeAndAppendFiles.py

mkdir -p ${OUTPUTDIR}

for i in `seq 1959 2015`; do ${convertScript} --input-file=${DATADIR}/WZ${i}.csv --output-file=${OUTPUTDIR}/WZ${i}.txt; done

CMD="${mergeAndAppendScript} --output-file=WZ_combined.txt"

cd ${OUTPUTDIR}
for file in `ls`; do
  CMD="${CMD} --input-file=${file}"
done

echo "Command to run is: ${CMD}"
${CMD}

