#!/bin/sh

##############################################################################

# Note: This script assumes that the TFCCommodityCharts data scraper
# has already been run recently.

##############################################################################
# Corn section.
##############################################################################

function corn() {
  
  # This basically copies stuff to directory
  # /home/rluu/programming/pricechartingtool/data/pricebars/futures/C/
  # from the stuff gathered from
  # /home/rluu/download/trading/data/futuresData_PriceData/EODFutures/C
  # and 
  # /home/rluu/download/trading/data/futuresData_PriceData/Cont_contract/
  #
  # This only needs to be run once, since I do not update the data
  # from PriceData.  That is why it is commented out.
  #
  #./specific/getFuturesData_Corn_PriceData.bash
    
  # This basically updates directory
  # /home/rluu/programming/pricechartingtool/data/pricebars/futures/ZC/
  # with the stuff gathered from 
  # /home/rluu/programming/DataScraper_TFCCommodityCharts/data/ZC/
  ./specific/getFuturesData_Corn_TFCCommodityCharts.bash
  
  # Combine daily PriceBar data from PriceData and TFC to create a merged file.
  # Contract month letters for CORN.
  CONTRACTS="H K N U Z"
  for CONTRACT in $CONTRACTS; do
      ./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/C/C_${CONTRACT}_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZC/ZC_Weekly_20081017_to_20090731_TFC.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZC/ZC_${CONTRACT}_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZC/ZC_${CONTRACT}_PriceData_and_TFC_Merged.txt
  done
  
  # Combine the PriceData May Weekly Corn with TFC Weekly.
  ./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/C/C_K_Weekly_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZC/ZC_Weekly_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZC/ZC_Weekly_PriceData_1969_to_2008_and_TFC_2008_to_Current_Merged.txt

}

##############################################################################
# Soybeans section.
##############################################################################

function soybeans() {
  
  # This basically copies stuff to directory
  # /home/rluu/programming/pricechartingtool/data/pricebars/futures/S/
  # from the stuff gathered from
  # /home/rluu/download/trading/data/futuresData_PriceData/EODFutures/S
  # and 
  # /home/rluu/download/trading/data/futuresData_PriceData/Cont_contract/
  #
  # This only needs to be run once, since I do not update the data
  # from PriceData.  That is why it is commented out.
  #
  #./specific/getFuturesData_Soybeans_PriceData.bash
  
  # This basically updates directory
  # /home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/
  # with the stuff gathered from 
  # /home/rluu/programming/DataScraper_TFCCommodityCharts/data/ZS/
  ./specific/getFuturesData_Soybeans_TFCCommodityCharts.bash
  
  # Combine daily PriceBar data from PriceData and TFC to create a merged file.
  # Contract month letters for SOYBEANS.
  CONTRACTS="K X"
  for CONTRACT in $CONTRACTS; do
      ./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/S/S_${CONTRACT}_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_Weekly_20081017_to_20090731_TFC.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_${CONTRACT}_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_${CONTRACT}_PriceData_and_TFC_Merged.txt
  done
  
  # Combine the PriceData May Weekly Soybeans with TFC Weekly.
  ./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/S/S_K_Weekly_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_Weekly_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZS/ZS_Weekly_PriceData_1969_to_2008_and_TFC_2008_to_Current_Merged.txt

}

##############################################################################
# Wheat section.
##############################################################################

function wheat() {
  
  # This basically copies stuff to directory
  # /home/rluu/programming/pricechartingtool/data/pricebars/futures/W/
  # from the stuff gathered from
  # /home/rluu/download/trading/data/futuresData_PriceData/EODFutures/W
  # and 
  # /home/rluu/download/trading/data/futuresData_PriceData/Cont_contract/
  #
  # This only needs to be run once, since I do not update the data
  # from PriceData.  That is why it is commented out.
  #
  #./specific/getFuturesData_Wheat_PriceData.bash
  
  # This basically updates directory
  # /home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/
  # with the stuff gathered from 
  # /home/rluu/programming/DataScraper_TFCCommodityCharts/data/ZW/
  ./specific/getFuturesData_Wheat_TFCCommodityCharts.bash
  
  # Combine daily PriceBar data from PriceData and TFC to create a merged file.
  # Contract month letters for WHEAT.
  CONTRACTS="H K N U Z"
  for CONTRACT in $CONTRACTS; do
      ./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/W/W_${CONTRACT}_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/ZW_Weekly_20081017_to_20090731_TFC.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/ZW_${CONTRACT}_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/ZW_${CONTRACT}_PriceData_and_TFC_Merged.txt
  done
  
  # Combine the PriceData May Weekly Wheat with TFC Weekly.
  ./mergeAndAppendFiles.py --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/W/W_K_Weekly_PriceData.txt --input-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/ZW_Weekly_TFC.txt --output-file=/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/ZW_Weekly_PriceData_1969_to_2008_and_TFC_2008_to_Current_Merged.txt

}

##############################################################################

# Run functions above.
corn
soybeans
wheat

