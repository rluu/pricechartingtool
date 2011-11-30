#!/bin/sh

##############################################################################

# Note: This script assumes that the data scraper has already been run
# recently.


##############################################################################
# Soybeans section.
##############################################################################

# Basically just updates directory 
# /home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/
# with the stuff gathered from 
# /home/rluu/programming/DataScraper_TFCCommodityCharts/data/ZS/
./getFuturesData_TFCCommodityCharts.bash

# Combine daily PriceBar data from PriceData and TFC to create a merged file.
# Contract month letters for SOYBEANS.
CONTRACTS="K X"
for CONTRACT in $CONTRACTS; do
    ./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/S/S_${CONTRACT}_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/Soybeans_Weekly_20081017_to_20090731_TFC.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_${CONTRACT}_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_${CONTRACT}_PriceData_and_TFC_Merged.txt
done

# Combine the PriceData May Weekly Soybeans with TFC Weekly.
./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/S/S_K_Weekly_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_Weekly_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_Weekly_PriceData_1969_to_2008_and_TFC_2008_to_Current_Merged.txt

##############################################################################

