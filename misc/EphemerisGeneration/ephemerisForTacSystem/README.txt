##############################################################################
Steps to do things related to the IBM trading system given by TAC in
WITS post #61757 and #61777.
##############################################################################

Contents of this file:

  Goal: Chart the cycle pivots on a chart in PriceChartingTool.

  Goal: Create a CSV file with price data, ephemeris data, composite
        planet data for cycles, and the 2-planet and 3-planet pivots
        marked.

##############################################################################

Goal: 
Chart the cycle pivots on a chart in PriceChartingTool.


Steps:

# Generate ephemeris.

./createLongitudeSpreadsheetFile_forTacSystem.py --centricity=heliocentric --zodiac=tropical --calculate-midpoints=false --start-timestamp=199001 --end-timestamp=201312 --output-file=TacEphemeris.csv

# Generate ephemeris with composite planet calculations.
# This below will produce TacEphemeris2.csv

python3 readCsvFileAndAddFields.py

# Open the PriceChartDocumentScripts script and make sure that all the
# global variables are set appropriately for the action you want.  For
# the 2-planet cycle, you will need to comment or uncomment-out
# various lines in the global variables section.

emacs /home/rluu/programming/pricechartingtool/misc/PriceChartDocumentScripts/customScripts/addVerticalLinesForCsvFileEphemerisCycle.py

# Run the PriceChartDocumentScripts script to modify the PCD file.

./modifyPriceChartDocument.py --pcd-file=/home/rluu/programming/pricechartingtool/data/PriceChartDocumentFiles/IBM.pcd --script-file=./customScripts/addVerticalLinesForCsvFileEphemerisCycle.py

##############################################################################

Goal: 
Create a CSV file with price data, ephemeris data, composite planet data for cycles, and the 2-planet and 3-planet pivots marked.


Steps:

# Generate ephemeris.

./createLongitudeSpreadsheetFile_forTacSystem.py --centricity=heliocentric --zodiac=tropical --calculate-midpoints=false --start-timestamp=196201 --end-timestamp=201412 --output-file=TacEphemeris.csv


# Generate ephemeris with composite planet calculations.
# This below will produce TacEphemeris2.csv

python3 readCsvFileAndAddFields.py


# Run the following to calculate 2-planet cycle hit dates.
# This will produce file cycleHitDates2P.csv

python3 get2PlanetCycleHitDates.py


# Run the following to calculate 3-planet cycle hit dates.
# This will produce file cycleHitDates3P.csv

python3 get3PlanetCycleHitDates.py


# Run the following to combine all the outputted CSV files:
#  - IBM.txt (IBM pricebar data CSV file).
#  - TacEphemeris2.csv
#  - cycleHitDates2P.csv
#  - cycleHitDates3P.csv
#
# This script will also add ephemeris planet positions to the spreadsheet.  
#
