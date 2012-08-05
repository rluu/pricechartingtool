##############################################################################
Steps to do things related to the cycle hunting in stock PAAS.
##############################################################################

Contents of this file:

  Goal: Chart the cycle pivots on a chart in PriceChartingTool.

##############################################################################

Goal: 
Chart the cycle pivots on a chart in PriceChartingTool.


Steps:

# Generate ephemeris.

./createLongitudeSpreadsheetFileForCycleHunting.py --centricity=heliocentric --zodiac=tropical --calculate-midpoints=false --start-timestamp=199506 --end-timestamp=201412 --output-file=PAAS_Ephemeris.csv

# Generate ephemeris with composite planet calculations.
# This below will produce TacEphemeris2.csv

python3 readCsvFileAndAddFields.py

# Open the PriceChartDocumentScripts script and make sure that all the
# global variables are set appropriately for the action you want.  For
# the 2-planet cycle, you will need to comment or uncomment-out
# various lines in the global variables section.

emacs /home/rluu/programming/pricechartingtool/misc/PriceChartDocumentScripts/customScripts/addVerticalLinesForCsvFileEphemerisCycle.py

# Run the PriceChartDocumentScripts script to modify the PCD file.

./modifyPriceChartDocument.py --pcd-file=/home/rluu/programming/pricechartingtool/data/PriceChartDocumentFiles/PAAS.pcd --script-file=./customScripts/addVerticalLinesForCsvFileEphemerisCycle_PAAS.py

##############################################################################
