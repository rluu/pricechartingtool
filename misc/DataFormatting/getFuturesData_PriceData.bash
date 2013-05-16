#!/bin/bash
##############################################################################
#
# Description:
#
#   This script obtains futures pricebar data from locations on the
#   filesystem and puts it in the destination location, formatted with
#   'dataFormatting.py'.  To use this script, modify the below
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
PRICEDATA_EODFUTURES_SOURCE_DIR=/home/rluu/download/trading/data/futuresData_PriceData/EODFutures
PRICEDATA_CONTINUOUS_FUTURES_SOURCE_DIR=/home/rluu/download/trading/data/futuresData_PriceData/Cont_contract
# Trading entity symbol.
#SYMBOL=S
SYMBOL=KC

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
    OUTPUT_FILE_BASENAME="${SYMBOL}_${CONTRACT}_PriceData.txt"
    OUTPUT_FILE="$PCT_DIR/data/pricebars/futures/$SYMBOL/$OUTPUT_FILE_BASENAME"

    # Gather and format data.
    $SCRIPTS_DIR/dataFormatting.py --source-data-dir="$PRICEDATA_EODFUTURES_SOURCE_DIR/$SYMBOL" --contract-letter=$CONTRACT --output-file="$OUTPUT_FILE"

    # Convert daily data to weekly.
    INPUT_FILE="$OUTPUT_FILE"
    OUTPUT_FILE_BASENAME="${SYMBOL}_${CONTRACT}_Weekly_PriceData.txt"
    OUTPUT_FILE="$PCT_DIR/data/pricebars/futures/$SYMBOL/$OUTPUT_FILE_BASENAME"
    $SCRIPTS_DIR/convertDailyToWeekly.py --input-file="$INPUT_FILE" --output-file="$OUTPUT_FILE"
done
    
# Copy the continuous contract file.
echo "Copying data for continous contracts of symbol $SYMBOL ..."

# Output filename.
OUTPUT_FILE_BASENAME="${SYMBOL}_ContinuousContract_PriceData.txt"
OUTPUT_FILE="$PCT_DIR/data/pricebars/futures/$SYMBOL/$OUTPUT_FILE_BASENAME"
cp -f $PRICEDATA_CONTINUOUS_FUTURES_SOURCE_DIR/${SYMBOL}.txt "$OUTPUT_FILE"
chmod 644 "$OUTPUT_FILE"

echo "Done."

##############################################################################
