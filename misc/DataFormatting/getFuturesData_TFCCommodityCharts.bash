#!/bin/bash
##############################################################################
#
# Description:
#
#   This script obtains futures pricebar data and puts it in the
#   destination location.  To use this script, modify the below
#   variables and run.
#
#
##############################################################################
# Global variables
##############################################################################

# Top-level directory of PriceChartingTool.
PCT_DIR=/home/rluu/programming/pricechartingtool

# Directory where the miscellaneous scripts are located.
SCRIPTS_DIR=$PCT_DIR/misc/DataFormatting

# Location where data directories reside.
TFC_EODFUTURES_SOURCE_DIR=/home/rluu/programming/DataScraper_TFCCommodityCharts/data

# Trading entity symbol.
SYMBOL=ZS

# Contract month letters.  (If all letters are specified, then if no
# input files are found for a certain contract month, then the output
# file for that contract month will pretty much be empty (it will only
# have the header line as the contents).
CONTRACTS="F G H J K M N Q U V X Z"

# Output directory.
OUTPUT_DIR="$PCT_DIR/data/pricebars/futures/$SYMBOL"

##############################################################################

# Make sure output directory exists.
mkdir -p $OUTPUT_DIR

##############################################################################

# Gather and format the data from all the monthly contracts.
echo "Gathering and formatting data for monthly contracts of symbol $SYMBOL ..."
for CONTRACT in $CONTRACTS; do
    # Output filename.
    OUTPUT_FILE_BASENAME="${SYMBOL}_${CONTRACT}_TFC.txt"
    OUTPUT_FILE="$PCT_DIR/data/pricebars/futures/$SYMBOL/$OUTPUT_FILE_BASENAME"

    # Gather and format data.
    $SCRIPTS_DIR/dataFormatting.py --source-data-dir="$TFC_EODFUTURES_SOURCE_DIR/$SYMBOL" --contract-letter=$CONTRACT --output-file="$OUTPUT_FILE"
done
    
# Copy the continuous contract files.
echo "Copying data for continous data of symbol $SYMBOL ..."

# Weekly.
OUTPUT_FILE_BASENAME=${SYMBOL}_Weekly_TFC.txt
OUTPUT_FILE=$PCT_DIR/data/pricebars/futures/$SYMBOL/$OUTPUT_FILE_BASENAME
cp -f $TFC_EODFUTURES_SOURCE_DIR/$SYMBOL/${SYMBOL}_Weekly.txt $OUTPUT_FILE
chmod 664 "$OUTPUT_FILE"

# Monthly.
OUTPUT_FILE_BASENAME=${SYMBOL}_Monthly_TFC.txt
OUTPUT_FILE=$PCT_DIR/data/pricebars/futures/$SYMBOL/$OUTPUT_FILE_BASENAME
cp -f $TFC_EODFUTURES_SOURCE_DIR/$SYMBOL/${SYMBOL}_Monthly.txt $OUTPUT_FILE
chmod 664 "$OUTPUT_FILE"

echo "Done."

##############################################################################
