#!/usr/bin/env python3
##############################################################################
# Description:
#
#   This takes as input, a ephemeris spreadsheet CSV file as
#   produced by /home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleHuntingGeneric/makeFilledMasterEphemeris_3p.py, and then orders the
#   longitude measurements of a certain planet or planet combination
#   in a column according to a repeat of a certain number of degrees.
#   It also places the trading-entity's daily high and low prices,
#   connected to each date, in columns next to the planetary
#   measurement.  This script works for both heliocentric and
#   geocentric planets and planet combinations.
#
#   The output CSV file thus will have format as follows:
#
#     <Timestamp>,<Longitude>,<Longitude-(repeatCount * modOffsetPerColumnRepeat)>,<HighPrice>,<LowPrice>,
#     [this set of column headers repeat again, once for each repetition or 'repeat'.]
#
# Background information:
#
#   This script was created because of the homework that was part of
#   BA ACCE5S lesson G (January 2013).  I decided to create this
#   script so that I could do that homework, and also so that similar
#   spreadsheets could be created with this script later, for various
#   other planet combinations.
# 
# Usage steps:
#
#     1) Open the CSV file that contains the input ephemeris spreadsheet.
#
#     2) Determine which column number (0-based index) of longitude
#     data (for whatever planet or planet combination) you want to
#     utilize. The data in this column must be in the
#     always-increasing longitude format.
#
#     3) Determine which starting longitude value (always-increasing
#     longitude) determines the beginning of the first repeat.  
#
#     4) According to the information obtained in the previous steps,
#     set the global variables according to the parameters desired for
#     the output file.
#
#     5) Run the script.
#
#         python3 makeCycleOfRepetitionSpreadsheet.py
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For timestamps and dates.
import datetime
import pytz

# For logging.
import logging

# For math.floor()
#import math

##############################################################################
# Global variables

# Input ephemeris CSV file.
#
# This should be a CSV file similar to something output by the script
# 'makeFilledMasterEphemeris_3p.py'.
#
#
# Directory: cycleHuntingGeneric:
#ephemerisInputFilename = "/home/rluu/programming/pricechartingtool/qt4/misc/EphemerisGeneration/cycleHuntingGeneric/master_3p_ephemeris_nyc_noon.csv"
ephemerisInputFilename = "/home/rluu/programming/pricechartingtool/qt4/misc/EphemerisGeneration/cycleHuntingGeneric/master_2p_ephemeris_nyc_noon.csv"
#
# Directory: TTTA/ephemeris_studies:
#ephemerisInputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/master_3p_ephemeris_nyc_noon.csv"
#ephemerisInputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/temp.csv"


# Timezone used in input ephemeris CSV file.
defaultInputFileTimezone = pytz.timezone("US/Eastern")

# Lines to skip in the ephemeris input file.
#
# This is set to 1 because the first line contains the headers.  This
# is standard and shouldn't need to change.
linesToSkip = 1

# Column number for the timestamp, in the input CSV file, that has the
# timestamp in format "YYYY-MM-DD HH:MM" or "YYYY-MM-DD".
ephemerisInputFileTimestampColumn = 0

# Column number (0-based) for the longitude of a certain planet, or planet
# combination, in the input CSV file.  Currently this script only
# works for planets that move straight forward only (i.e. no
# retrograde).  This column must be in the format of
# always-increasing.  It is assumed that this information is on a
# daily basis.
#
# Note: Helper script '/home/rluu/programming/pricechartingtool/misc/SpreadsheetColumnLetterNumberConversion/columnLettersToColumnIndex.py' can be used to convert between column letters and column index numbers, but note that this script returns values that are 1-based indexes, so you will need to subtract 1 to get the actual index that is 0-based used for the variable below.
#
#ephemerisInputFileLongitudeColumn = 2 # 2 corresponds to column "C", Day count.
#ephemerisInputFileLongitudeColumn = 113 # 113 corresponds to column "DJ", G.Moon.
#ephemerisInputFileLongitudeColumn = 114 # 114 corresponds to column "DK", G.Mercury.
#ephemerisInputFileLongitudeColumn = 115 # 115 corresponds to column "DL", G.Venus.
#ephemerisInputFileLongitudeColumn = 116 # 116 corresponds to column "DM", G.Sun.
#ephemerisInputFileLongitudeColumn = 117 # 117 corresponds to column "DN", G.Mars.
#ephemerisInputFileLongitudeColumn = 118 # 118 corresponds to column "DO", G.Jupiter.
#ephemerisInputFileLongitudeColumn = 120 # 120 corresponds to column "DQ", G.Saturn.
#ephemerisInputFileLongitudeColumn = 139 # 139 corresponds to column "EJ", G.Mood/G.Sun.
#ephemerisInputFileLongitudeColumn = 126 # 126 corresponds to column "DW", H.Mercury.
#ephemerisInputFileLongitudeColumn = 127 # 127 corresponds to column "DX", H.Venus.
#ephemerisInputFileLongitudeColumn = 128 # 128 corresponds to column "DY", H.Earth.
#ephemerisInputFileLongitudeColumn = 129 # 129 corresponds to column "DZ", H.Mars.
#ephemerisInputFileLongitudeColumn = 130 # 130 corresponds to column "EA", H.Jupiter.
#ephemerisInputFileLongitudeColumn = 131 # 131 corresponds to column "EB", H.Saturn.
#ephemerisInputFileLongitudeColumn = 139 # 139 corresponds to column "EJ", G.Moon/G.Sun.
#ephemerisInputFileLongitudeColumn = 200 # 200 corresponds to column "GS", H.Mercury/H.Venus.
#ephemerisInputFileLongitudeColumn = 201 # 201 corresponds to column "GT", H.Mercury/H.Earth.
#ephemerisInputFileLongitudeColumn = 202 # 202 corresponds to column "GU", H.Mercury/H.Mars.
#ephemerisInputFileLongitudeColumn = 209 # 209 corresponds to column "HB", H.Venus/H.Earth.
#ephemerisInputFileLongitudeColumn = 210 # 210 corresponds to column "HC", H.Venus/H.Mars.
#ephemerisInputFileLongitudeColumn = 211 # 211 corresponds to column "HD", H.Venus/H.Jupiter.
#ephemerisInputFileLongitudeColumn = 213 # 213 corresponds to column "HF", H.Venus/H.Saturn.
ephemerisInputFileLongitudeColumn = 217 # 217 corresponds to column "HJ", H.Earth/H.Mars.
#ephemerisInputFileLongitudeColumn = 218 # 218 corresponds to column "HK", H.Earth/H.Jupiter.
#ephemerisInputFileLongitudeColumn = 224 # 224 corresponds to column "HQ", H.Mars/H.Jupiter.
#ephemerisInputFileLongitudeColumn = 226 # 226 corresponds to column "HS", H.Mars/H.Saturn.
#ephemerisInputFileLongitudeColumn = 231 # 231 corresponds to column "HX", H.Jupiter/H.Saturn.
#ephemerisInputFileLongitudeColumn = 232 # 232 corresponds to column "HY", H.Jupiter/H.Uranus.





# Filename location of the market data input CSV file.
# This is optional.  If the below path is "", then this parameter is ignored.
marketDataInputFilename = ""
#marketDataInputFilename = "/home/rluu/download/trading/data/data_45YearsOnWallStreet/djia_page_57/djia.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/DJIA/tdow_various_pivots_marked_up_for_ttta_analysis_in_CORS_1895_to_1933.txt"
#marketDataInputFilename = "/home/rluu/download/trading/data/data_45YearsOnWallStreet/djia_page_66/djia.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/DJIA/TDOW1895_1940_HLC_modifiedByRluu_addedOpenEqualsClose.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/DJIA/DJIA.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/DJIA/djia.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/DJIA/DJIA.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/DJIA/DJIA_1980_to_Current.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/ABX/ABX.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/AXP/AXP.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/C/C.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/GG/GG.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/IBM/IBM.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/INTC/INTC.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/JCP/JCP.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/JPM/JPM.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/TDW/TDW.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/stocks/X/X.txt"


# May Coffee.  (Tokyo J-1).
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/futures/KC/KC_K_PriceData.txt"
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/futures/KC/KC_K_TradingCharts.txt"


# March Wheat.
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/Wheat_Alblak_Forecasts_Study_Pricebar_Data/ZW_H_PriceData_and_TFC_Merged.txt"
# May Wheat.
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/Wheat_Alblak_Forecasts_Study_Pricebar_Data/ZW_K_PriceData_and_TFC_Merged.txt"
# July Wheat.
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/Wheat_Alblak_Forecasts_Study_Pricebar_Data/ZW_N_PriceData_and_TFC_Merged.txt"
# December Wheat.
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/futures/ZW/Wheat_Alblak_Forecasts_Study_Pricebar_Data/ZW_Z_PriceData_and_TFC_Merged.txt"
# July Wheat.
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/data/pricebars/futures/W/W_N_GannStyle_TradingCharts.txt"
#marketDataInputFilename = "/home/rluu/download/trading/data/futuresData_TradingCharts/EODFutures/Wheat/July/Wheat_CBOT_Pit_And_Electronic_combined/Wheat_July_CBOT_Pit_And_Electronic_combined_1970_to_2014.txt"

# Gold - June contract (GC_M).
#marketDataInputFilename = "/home/rluu/programming/pricechartingtool/qt4/data/pricebars/futures/GC/GCM.txt"


# Column number for the timestamp.  The timestamp in this column is
# expected to be in the format "MM/DD/YYYY".
#
# For market data obtained from my personal scripts, this is usually column 0.
marketDataInputFileTimestampColumn = 0

# Column number for the high price for a given timestamp.
#
# For market data obtained from my personal scripts, this is usually column 2.
marketDataInputFileHighPriceColumn = 2

# Column number for the low price for a given timestamp.
#
# For market data obtained from my personal scripts, this is usually column 3.
marketDataInputFileLowPriceColumn = 3


# Starting longitude degree in the format of always-increasing longitude.
# This is the starting longitude value of the first 'repeat'.
# Use a value just slightly before the starting date's longitude.
#
#startingLongitude = 53280  # G.Moon at 0 deg Aries on 1996-01-24.
#
#startingLongitude = 157870 # approx G.Moon new moon on 1926-10-06.
#startingLongitude = 92733.47  # G.Moon/G.Sun on 1926-10-23.
#startingLongitude = 100143  # G.Moon on 1926-10-23.
#startingLongitude = 7790  # G.Mercury on 1926-10-23.
#startingLongitude = 7762  # G.Venus on 1926-10-23.
#startingLongitude = 7769.5  # G.Sun on 1926-10-23.
#startingLongitude = 4365.2  # G.Mars on 1926-10-23.
#startingLongitude = 667.465  # G.Jupiter on 1926-10-23.
#startingLongitude = 595.295  # G.Saturn on 1926-10-23.
#startingLongitude = 31240  # H.Mercury on 1926-10-23.
#startingLongitude = 12432  # H.Venus on 1926-10-23.
#startingLongitude = 7589.53  # H.Earth on 1926-10-23.
#startingLongitude = 3994.47  # H.Mars on 1926-10-23.
#
#startingLongitude = 2097.08  # G.Moon on 1906-06-09.
#startingLongitude = 2019.16  # G.Moon/G.Sun on 1906-06-09.
#startingLongitude = 438.94  # G.Mercury on 1906-06-09.
#startingLongitude = 466.84  # G.Venus on 1906-06-09.
#startingLongitude = 437.92  # G.Sun on 1906-06-09.
#startingLongitude = 448.6  # G.Mars on 1906-06-09.
#startingLongitude = 78.6  # G.Jupiter on 1906-06-09.
#startingLongitude = 344.79  # G.Saturn on 1906-06-09.
#startingLongitude = 802.31  # H.Mercury on 1906-06-09.
#startingLongitude = 510  # H.Venus on 1906-06-09.
#startingLongitude = 257.92  # H.Earth on 1906-06-09.
#startingLongitude = 95.41  # H.Mars on 1906-06-09.

#startingLongitude = 567  # G.Sun on 1906-11-07.
#startingLongitude = 54913   # G.Sun on 1906-11-07.
#startingLongitude = 375
#startingLongitude = 373
#startingLongitude = 30


# For TTTA:
#startingLongitude = 47880 # H.Mercury at 0 deg long, at about 45 CD before 1926.
#startingLongitude = 18720 # H.Venus at 0 deg long, at about 78 CD before 1926.
#startingLongitude = 11520 # H.Earth at 0 deg long, at about 100 CD before 1926.
#startingLongitude = 6120 # H.Mars at 0 deg long, at about 220 CD before 1926.
#startingLongitude = 720 # H.Jupiter at 0 deg long, sometime before 1926.
#startingLongitude = 360 # H.Saturn at 0 deg long, sometime before 1926.

#startingLongitude = 133 + (360*435)
#startingLongitude = 360  # G.Moon/G.Sun at 0 deg Aries on 1969-01-18.
startingLongitude = 360  # Good starting longitude for all planets.
#startingLongitude = 720  # Good starting longitude for all planets if 360 doesn't work.
#startingLongitude = 7216.0  # H.Earth on around 1925-10-09.


# Number of degrees elapsed for each repeat.  A new set of columns in the
# output file will be created after this amount of degrees has been elapsed.
#numDegreesElapsedForRepeat = 360
numDegreesElapsedForRepeat = 180
#numDegreesElapsedForRepeat = 588
#numDegreesElapsedForRepeat = 850
#numDegreesElapsedForRepeat = 1000
#numDegreesElapsedForRepeat = 2400
#numDegreesElapsedForRepeat = 4928
#numDegreesElapsedForRepeat = 360 * 44
#numDegreesElapsedForRepeat = 360 * 252 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 12 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 34 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 12000 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 5 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 20 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 25 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 14 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 71 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 21 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 22 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 24 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 50 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 68 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 69 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 70 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 360 * 7 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 10 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 20 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 14 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 15 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 17 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 21 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 23 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 29 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 34 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 44 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 22 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 49 # For G.Moon.
#numDegreesElapsedForRepeat = 360 * 69 # For G.Moon.
#numDegreesElapsedForRepeat = 24110 # For G.Moon.
#numDegreesElapsedForRepeat = 1800 # For G.Sun (5 rev).
#numDegreesElapsedForRepeat = 2000 # For G.Sun.
#numDegreesElapsedForRepeat = 3600 # For G.Sun (10 rev.)
#numDegreesElapsedForRepeat = 360 * 21 # For H.Mercury
#numDegreesElapsedForRepeat = (360 * 21) + 153 # For H.Mercury
#numDegreesElapsedForRepeat = ((360 * 21) + 153) * 2 # For H.Mercury
#numDegreesElapsedForRepeat = 360 * 22 # For H.Mercury
#numDegreesElapsedForRepeat = 7462 # For H.Mercury
#numDegreesElapsedForRepeat = 7789 # For H.Mercury
#numDegreesElapsedForRepeat = 11850 # For H.Mercury
#numDegreesElapsedForRepeat = 2920 # For H.Venus (8 rev + 40 deg).
#numDegreesElapsedForRepeat = 8.4 * 360 # For H.Venus
#numDegreesElapsedForRepeat = 2933 # For H.Venus
#numDegreesElapsedForRepeat = 3063 # For H.Venus
#numDegreesElapsedForRepeat = 4439 # For H.Venus
#numDegreesElapsedForRepeat = 4643 # For H.Venus
#numDegreesElapsedForRepeat = 4680 # For H.Venus (13 rev).
#numDegreesElapsedForRepeat = 360 * 3 # For H.Venus/H.Earth
#numDegreesElapsedForRepeat = 360 * 4 # For H.Venus/H.Earth
#numDegreesElapsedForRepeat = 360 * 5 # For H.Venus/H.Earth
#numDegreesElapsedForRepeat = 360 * 6 # For H.Venus/H.Earth
#numDegreesElapsedForRepeat = 360 * 7 # For H.Venus/H.Earth
#numDegreesElapsedForRepeat = 1129 # For H.Venus/H.Earth
#numDegreesElapsedForRepeat = 360 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 960 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 1634 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 1613 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 1616 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 808 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 782 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 360 * 3 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 360 * 5 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 432 # For H.Venus/H.Mars
#numDegreesElapsedForRepeat = 1800 # For H.Earth (5 rev).
#numDegreesElapsedForRepeat = 1872 # For H.Earth
#numDegreesElapsedForRepeat = 2732 # For H.Earth.
#numDegreesElapsedForRepeat = 2857 # For H.Earth.
#numDegreesElapsedForRepeat = (360 * 3) + 194 # For H.Mercury/H.Earth
#numDegreesElapsedForRepeat = ((360 * 22) + 155) / 2 # For H.Earth/H.Mars
#numDegreesElapsedForRepeat = 360 * 11 # For H.Earth/H.Mars
#numDegreesElapsedForRepeat = 360 * 1 # For H.Earth/H.Mars
#numDegreesElapsedForRepeat = 360 * 3 # For H.Mars
#numDegreesElapsedForRepeat = 360 * 4 # For H.Mars
#numDegreesElapsedForRepeat = 360 * 5 # For H.Mars
#numDegreesElapsedForRepeat = 432 # For H.Mars
#numDegreesElapsedForRepeat = (360 * 4) - 25 # For H.Mars
#numDegreesElapsedForRepeat = (360 * 4) - 21 # For H.Mars
#numDegreesElapsedForRepeat = 360 * 5 # For H.Mars
#numDegreesElapsedForRepeat = 360 * 6 # For H.Mars
#numDegreesElapsedForRepeat = 360 * 7 # For H.Mars
#numDegreesElapsedForRepeat = 360 * 8 # For H.Mars

#numDegreesElapsedForRepeat = 1942 # For H. Mars.  "11 years" in TTTA.

#numDegreesElapsedForRepeat = 625 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = 725 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = 804 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = 340 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = 170 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = 750 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = 3910 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = 1164 # For H.Mars/H.Jupiter.
#numDegreesElapsedForRepeat = (360 * 6) + 25 # For H.Mars/H.Jupiter.

#numDegreesElapsedForRepeat = 222.6 # For H.Jupiter
#numDegreesElapsedForRepeat = 233 # For H.Jupiter
#numDegreesElapsedForRepeat = 440 # For H.Jupiter

#numDegreesElapsedForRepeat = 84 # For G.Saturn

#numDegreesElapsedForRepeat = 360 # For H.Earth/H.Mars
#numDegreesElapsedForRepeat = 360 * 7 # For H.Earth/H.Mars
#numDegreesElapsedForRepeat = 288 # For H.Venus/H.Earth
#numDegreesElapsedForRepeat = 420 # For H.Mercury
#numDegreesElapsedForRepeat = 49 # For H.Earth
#numDegreesElapsedForRepeat = 60 # For G.Mars


#numDegreesElapsedForRepeat = 37 * 1 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 2 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 3 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 4 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 5 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 7 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 10 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 11 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 12 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 13 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 15 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 20 # For G.Moon/G.Sun.
#numDegreesElapsedForRepeat = 37 * 30 # For G.Moon/G.Sun.

# Ouptut CSV file.  
outputFilename = "/tmp/H.Earth_H.Mars_180_deg_repeats.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/CountingWheelsFrom_19060609/H.Mars_180_deg_repeats.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/research/stocks/DJIA/G.Moon_15840_deg_repeats_or_sheet_of_44.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/G.Sun_7_degree_repeats_1776_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_360_deg_repeats.csv"

# "Time"(s) in TTTA.
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/CalendarDay_sheet_of_850.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/CalendarDay_sheet_of_1000.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/CalendarDay_sheet_of_588.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Sun_sheet_of_180_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Sun_sheet_of_1000_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Sun_sheet_of_1800_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Sun_sheet_of_2400_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Sun_sheet_of_4928_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Sun_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Sun_sheet_of_252.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_7.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_14.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_15.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_17.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_23.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_29.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_34.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_49.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_24110_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_sheet_of_7.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mercury_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mercury_sheet_of_1781.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mercury_sheet_of_7789.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Venus_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Venus_sheet_of_2933_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Venus_sheet_of_3063_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Venus_sheet_of_4439_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Venus_H.Earth_sheet_of_1129_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Earth_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Earth_sheet_of_2732_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_sheet_of_1942_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Jupiter_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Jupiter_sheet_of_440_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Saturn_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Saturn_sheet_of_84_deg.csv"

#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Earth_49_degree_repeats_to_NYC_Battle.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_24840_deg_repeats_or_sheet_of_69.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_68.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_sheet_of_17.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_1440_deg_repeats_or_sheet_of_4.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_1800_deg_repeats_or_sheet_of_5.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_2160_deg_repeats_or_sheet_of_6.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_2520_deg_repeats_or_sheet_of_7.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_2880_deg_repeats_or_sheet_of_8.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mercury_360_deg_repeats_or_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Venus_360_deg_repeats_or_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Earth_360_deg_repeats_or_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_360_deg_repeats_or_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Jupiter_360_deg_repeats_or_sheet_of_1.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Saturn_360_deg_repeats_or_sheet_of_1.csv"


#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_H.Jupiter_804_deg_repeats_or_sheet_of_2.2333.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_H.Jupiter_170_deg_repeats_or_sheet_of_0.47222.csv"

#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Jupiter_sheet_of_222.6_deg.csv"

#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_4320_deg_repeats_or_sheet_of_12.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_sheet_of_34.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_4320_deg_repeats_or_sheet_of_24.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_12000_deg_repeats_or_sheet_of_33.333.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_1800_deg_repeats_or_sheet_of_5.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_7200_deg_repeats_or_sheet_of_20.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_9000_deg_repeats_or_sheet_of_25.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_5040_deg_repeats_or_sheet_of_14.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_7560_deg_repeats_or_sheet_of_21.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_7920_deg_repeats_or_sheet_of_22.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_8640_deg_repeats_or_sheet_of_24.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_18000_deg_repeats_or_sheet_of_50.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_248400_deg_repeats_or_sheet_of_69.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/G.Moon_G.Sun_25200_deg_repeats_or_sheet_of_70.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/doc/notes/TTTA/ephemeris_studies/H.Mars_H.Jupiter_2185_deg_or_6.07_circle_repeats.csv"




# Wheat
#
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Sun_3600_deg_repeats_December_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Sun_2000_deg_repeats_July_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Sun_2000_deg_repeats_July_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Sun_2000_deg_repeats_July_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Moon_7920_deg_or_22_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_7560_deg_or_21_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_7920_deg_or_22_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_11850_deg_repeats_July_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_4643_deg_repeats_July_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_2920_deg_repeats_July_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_1872_deg_repeats_July_Wheat.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1080_deg_or_3_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_7920_deg_or_22_circle_repeats_March_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_2880_deg_or_8_circle_repeats_March_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1440_deg_or_4_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1800_deg_or_5_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_2160_deg_or_6_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_1080_deg_or_3_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_1440_deg_or_4_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_1800_deg_or_5_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_2160_deg_or_6_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_2520_deg_or_7_circle_repeats_July_Wheat_1969_to_2016.csv"

#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_1800_deg_or_5_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_1800_deg_or_5_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_360_deg_or_1_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_1634_deg_or_4.5388_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_1613_deg_or_4.5388_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_1616_deg_or_4.488_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_808_deg_or_2.244_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Jupiter_360_deg_or_1_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_2857_deg_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_4037.5_deg_or_11.215_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_360_deg_or_1_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_1080_deg_or_3_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_2520_deg_or_7_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Moon_G.Sun_90720_deg_or_252_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_782_deg_or_2.1722_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_960_deg_or_2.666_circle_repeats_July_Wheat_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Jupiter_233_deg_repeats_July_Wheat.csv"


# Gold - June contract (GC_M).
#outputFilename = "/home/rluu/programming/pricechartingtool/qt4/misc/EphemerisGeneration/cycleOfRepetition/G.Mars_60_deg_repeats_June_Gold_GC_M.csv"


# TDW
#
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_1800_deg_or_5_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_1080_deg_or_3_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1440_deg_or_4_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1415_deg_or_3.9305_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1419_deg_or_3.94167_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1800_deg_or_5_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_432_deg_or_1.2_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_7713_deg_or_21.425_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_15426_deg_or_42.85_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_15426_deg_or_42.85_circle_repeats_TDW_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Jupiter_804_deg_or_2.2333_circle_repeats_TDW_1969_to_2016.csv"

# Barrick Gold Corporation Stock.  Symbol: ABX
#
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/ABX_G.Moon_sheet_of_20_rev.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_1800_deg_or_5_circle_repeats_ABX_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/ABX_G.Sun_sheet_of_3600_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Moon_15840_deg_or_44_circle_repeats_ABX_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1440_deg_or_4_circle_repeats_ABX_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_432_deg_or_1.2_circle_repeats_ABX_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_1800_deg_or_5_circle_repeats_ABX_1969_to_2016.csv"

# Citigroup (Symbol: C)
#
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/C_H.Earth_sheet_of_1800_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/C_H.Venus_H.Earth_sheet_of_1800_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/C_G.Sun_sheet_of_3600_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_1080_deg_or_3_circle_repeats_C_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Jupiter_360_deg_or_1_circle_repeats_C_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Jupiter_360_deg_or_1_circle_repeats_C_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_1800_deg_or_5_circle_repeats_C_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_2520_deg_or_7_circle_repeats_C_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/C_H.Mars_sheet_of_1942_deg.csv"

#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Saturn_360_deg_or_1_circle_repeats_X_1969_to_2016.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Saturn_360_deg_or_1_circle_repeats_X_1969_to_2016.csv"

# Stock JC Penny.  Symbol: JCP
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/JCP_G.Sun_sheet_of_3600_deg.csv"

# Stock JP Morgan.  Symbol: JPM
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/JPM_G.Sun_sheet_of_3600_deg.csv"

# TTTA dow.
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Moon_5040_deg_or_14_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Moon_7560_deg_or_21_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/G.Moon_7920_deg_or_22_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_420_deg_or_1.1666_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_7920_deg_or_22_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_H.Earth_1274_deg_or_3.54_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Jupiter_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Saturn_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_H.Venus_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mercury_H.Earth_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_1800_deg_or_5_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Earth_288_deg_or_0.8_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Mars_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Jupiter_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Venus_H.Saturn_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Jupiter_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Jupiter_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Jupiter_750_deg_or_2.0833_circle_repeats_DJIA_1980_to_Current.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Saturn_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Earth_H.Mars_1080_deg_or_3_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Mars_H.Jupiter_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Jupiter_H.Saturn_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/H.Jupiter_H.Uranus_360_deg_or_1_circle_repeats_DJIA_1894_to_1935.csv"


# Dow current period.
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/DJIA_H.Mars_sheet_of_1942_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/DJIA_H.Jupiter_sheet_of_233_deg.csv"

# Intel stock.  Symbol: INTC
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/INTC_G.Sun_sheet_of_1800_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/INTC_G.Sun_sheet_of_3600_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/INTC_H.Mars_sheet_of_1942_deg.csv"


# American Express stock.  Symbol: AXP
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/AXP_G.Sun_sheet_of_3600_deg.csv"

# IBM stock.  Symbol: IBM
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/IBM_G.Sun_sheet_of_3600_deg.csv"

# Goldcorp stock.  Symbol: GG
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/GG_G.Sun_sheet_of_3600_deg.csv"
#outputFilename = "/home/rluu/programming/pricechartingtool/misc/EphemerisGeneration/cycleOfRepetition/GG_G.Moon_sheet_of_44_rev.csv"


# For logging.
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
#log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    
    # Close the Ephemeris so it can do necessary cleanups.
    #Ephemeris.closeEphemeris()
    
    logging.shutdown()
    
    sys.exit(rc)

def toNormalizedAngle(angleDeg):
    """Normalizes the given angle to a value in the range [0, 360).

    Arguments:
    angleDeg - float value in degrees of an angle to normalize.

    Returns:
    float value holding the equivalent angle, but in the range [0, 360).
    """

    a = float(angleDeg)
        
    while a < 0.0:
        a += 360.0
    while a >= 360.0:
        a -= 360.0

    return a
    
def convertTimestampStrToDatetime(timestampStr):
    """Converts a timestamp str from the CSV file to a datetime, and
    returns that datetime object.  If an error occurs in the
    conversion process, then None is returned.
    
    The timestamp str format can be in "YYYY-MM-DD HH:MM" or "YYYY-MM-DD".  

    If the timestamp str is given in the format "YYYY-MM-DD", then this
    function assumes that for a date given, the timestamp will be
    at 12:00 pm (noon).

    Prerequisites:
    'defaultInputFileTimezone' global variable is set to the
    pytz.timezone object used for the timestamp str.
    
    Parameters:
    timestampStr - str input value in the format
                  of "YYYY-MM-DD HH:MM" or "YYYY-MM-DD".  
    
    Return value:
    datetime.datetime object containing the equivalent timestamp.
    None is returned if an error occured during hte conversion process.
    """
    
    # Check input string for correct formatting.
    if len(timestampStr) != len("YYYY-MM-DD") and \
       len(timestampStr) != len("YYYY-MM-DD HH:MM"):
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None
    
    elif timestampStr[4] != "-" or timestampStr[7] != "-":
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None


    yearStr = timestampStr[0:4]
    monthStr = timestampStr[5:7]
    dayStr = timestampStr[8:10]

    hourStr = None
    minuteStr = None

    if len(timestampStr) == len("YYYY-MM-DD HH:MM"):
        hourStr = timestampStr[11:13]
        minuteStr = timestampStr[14:16]
    else:
        hourStr = "12"
        minuteStr = "00"
    
    # Test to make sure all the str values are digits before
    # converting to int values.
    for letter in yearStr:
        if not letter.isdigit():
            log.error("There is a non-digit year value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in monthStr:
        if not letter.isdigit():
            log.error("There is a non-digit month value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in dayStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in hourStr:
        if not letter.isdigit():
            log.error("There is a non-digit hour value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in minuteStr:
        if not letter.isdigit():
            log.error("There is a non-digit minute value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    # Convert the substrings to int values for the parts of the date/time.
    year = int(yearStr)
    month = int(monthStr)
    day = int(dayStr)
    hour = int(hourStr)
    minute = int(minuteStr)
    
    rv = datetime.datetime(year, month, day, hour, minute, \
                           tzinfo=defaultInputFileTimezone)
    
    return rv


def convertTimestampStrToDatetime2(timestampStr):
    """Converts a timestamp str from the CSV file to a datetime, and
    returns that datetime object.  If an error occurs in the
    conversion process, then None is returned.
    
    The timestamp str format can be in "MM/DD/YYYY HH:MM" or "MM/DD/YYYY".  

    If the timestamp str is given in the format "MM/DD/YYYY", then this
    function assumes that for a date given, the timestamp will be
    at 12:00 pm (noon).

    Prerequisites:
    'defaultInputFileTimezone' global variable is set to the
    pytz.timezone object used for the timestamp str.
    
    Parameters:
    timestampStr - str input value in the format
                  of "MM/DD/YYYY HH:MM" or "MM/DD/YYYY".
    
    Return value:
    datetime.datetime object containing the equivalent timestamp.
    None is returned if an error occured during hte conversion process.
    """
    
    # Check input string for correct formatting.
    if len(timestampStr) != len("MM/DD/YYYY") and \
       len(timestampStr) != len("MM/DD/YYYY HH:MM"):
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None
    
    elif timestampStr[2] != "/" or timestampStr[5] != "/":
        log.error("Read a timestamp from the CSV file that is " + \
                  "not in the correct format.  timestampStr == '{}'".\
                  format(timestampStr))
        return None


    monthStr = timestampStr[0:2]
    dayStr = timestampStr[3:5]
    yearStr = timestampStr[6:10]

    hourStr = None
    minuteStr = None

    if len(timestampStr) == len("MM/DD/YYYY HH:MM"):
        hourStr = timestampStr[11:13]
        minuteStr = timestampStr[14:16]
    else:
        hourStr = "12"
        minuteStr = "00"
    
    # Test to make sure all the str values are digits before
    # converting to int values.
    for letter in yearStr:
        if not letter.isdigit():
            log.error("There is a non-digit year value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in monthStr:
        if not letter.isdigit():
            log.error("There is a non-digit month value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in dayStr:
        if not letter.isdigit():
            log.error("There is a non-digit day value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in hourStr:
        if not letter.isdigit():
            log.error("There is a non-digit hour value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None
    for letter in minuteStr:
        if not letter.isdigit():
            log.error("There is a non-digit minute value found in " + \
                      "timestampStr '{}'".format(timestampStr))
            return None

    # Convert the substrings to int values for the parts of the date/time.
    year = int(yearStr)
    month = int(monthStr)
    day = int(dayStr)
    hour = int(hourStr)
    minute = int(minuteStr)
    
    rv = datetime.datetime(year, month, day, hour, minute, \
                           tzinfo=defaultInputFileTimezone)
    
    return rv



##############################################################################

# Holds the header line of the ephemeris input file.  We will use this
# header line in the output file.
headerLine = ""

# Modulus offset of degrees per column of timestamp and planet and price.  
modOffsetPerColumnRepeat = numDegreesElapsedForRepeat % 360

# List of lists.  Each item in this list is a list containing the
# fields of text of the input ephemeris CSV file.
listOfEphemerisDataValues = []


# Read in the ephemeris input file:
log.info("Reading from ephemeris input file: '{}' ...".\
         format(ephemerisInputFilename))
try:
    with open(ephemerisInputFilename, "r") as f:
        i = 0
        for line in f:
            line = line.strip()
            if line == "":
                # Empty line, do nothing for this line.
                # Go to next line.
                i += 1
            elif i < linesToSkip:
                # Header line.
                headerLine = line
                i += 1
            else:
                # Normal data line.
                dataValues = line.split(",")
                listOfEphemerisDataValues.append(dataValues)
                i += 1
        
except IOError as e:
    errStr = "I/O Error while trying to read file '" + \
             ephemerisInputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)

# Extract from the headerLine, the header str for the measurement we
# are obtaining.
headerStrForPlanetMeasurement = \
    headerLine.split(",")[ephemerisInputFileLongitudeColumn]


# List of lists.  Each item in this list is a list containing the
# fields of text of the market data input CSV file.
listOfMarketDataDataValues = []

if marketDataInputFilename != None and marketDataInputFilename != "":
    log.info("Reading from market data input file: '{}' ...".\
             format(marketDataInputFilename))
    try:
        with open(marketDataInputFilename, "r") as f:
            i = 0
            for line in f:
                line = line.strip()
                if line == "":
                    # Empty line, do nothing for this line.
                    # Go to next line.
                    i += 1
                elif i < linesToSkip:
                    # Header line.
                    headerLine = line
                    i += 1
                else:
                    # Normal data line.
                    dataValues = line.split(",")
                    listOfMarketDataDataValues.append(dataValues)
                    i += 1
    except IOError as e:
        errStr = "I/O Error while trying to read file '" + \
                 marketDataInputFilename + "':" + os.linesep + str(e)
        log.error(errStr)
        shutdown(1)

# List of lists.  This is for ephemeris values.  Each item is list
# which holds all the rows for that of repeat of
# 'numDegreesElapsedForRepeat' degrees.
listOfOutputEphemerisColumns = []

# Number of cycles.  This is a counter variable that holds the number
# of complete cycle repeat.  If a geocentric planet is retrograde and
# revisits a degree, that doesn't count as a complete cycle.
numFullCycles = 0

# List of lists.  This list holds all the rows for a
# particular repeat of 'numDegreesElapsedForRepeat' degrees.
# Each item in this list is a list of values [timestamp, longitude value % 360].
currRepeatRowsList = []


# This value is the idealized starting value for the always-increasing
# longitude.  From this value we calculate the elapsed degrees for the
# particular 'repeat'.
#
# On the first 'repeat', this starting value is equal to 'startingLongitude'.
# 
startingValue = None


# Previous value of the always-increasing longitude value.
prevValue = None
# Current value of the always-increasing longitude value.
currValue = None

for i in range(0, len(listOfEphemerisDataValues)):
    currRow = listOfEphemerisDataValues[i]
    
    timestampStr = currRow[ephemerisInputFileTimestampColumn]
    currValueStr = currRow[ephemerisInputFileLongitudeColumn]

    
    log.debug("i == {}".format(i))
    log.debug("timestampStr == '{}'".format(timestampStr))
    log.debug("currValueStr == '{}'".format(currValueStr))
    
    currValue = float(currValueStr)
    
    log.debug("currValue == {}".format(currValue))
    
    # We need to find the starting point if it is not already set.
    # This only happens at the very beginning when we have not found
    # our starting point.
    if startingValue == None:
        # We need two columns to see it cross over the
        # 'startingLongitude' value.
        if prevValue != None:
            # We have two values now from which to compare.
            if prevValue < startingLongitude and \
               currValue >= startingLongitude:
                
                # Get the idealized starting value.  
                startingValue = startingLongitude

                # We have a new startingValue, so clear out currRepeatRowsList.
                currRepeatRowsList = []
                
    if startingValue != None:
        # See if we have elapsed our desired number of degrees.
        elapsed = currValue - startingValue

        if elapsed > numDegreesElapsedForRepeat:
            # We have elapsed our desired number of degrees for a 'repeat'.
            # Append all the information for the previous repeat.
            listOfOutputEphemerisColumns.append(currRepeatRowsList)

            numFullCycles += 1
            
            # Calculate the new startingValue for the next 'repeat'.
            startingValue = startingValue + numDegreesElapsedForRepeat

            # We have a new startingValue, so clear out the currRepeatRowsList.
            currRepeatRowsList = []

        elif currValue < startingValue and prevValue > startingValue:
            
            # Geocentric planet is retrograde:
            # 
            # The planet crossed from over to under the previous repeat degree.

            # Note: This algorithm may miss some hits if the
            # day-resolution is not fine enough for fast planets like
            # G.Mercury.
            
            # We have elapsed our desired number of degrees that
            # matches a 'repeat'.  
            # Append all the information for the previous repeat.
            listOfOutputEphemerisColumns.append(currRepeatRowsList)

            # No need to update 'startingValue' variable.

            # Clear out the currRepeatRowsList since we hit the repeat degree.
            currRepeatRowsList = []

        elif currValue > startingValue and prevValue < startingValue:
            
            # Geocentric planet is direct:
            # 
            # The planet crossed from under to over the previous repeat degree.

            # We have elapsed our desired number of degrees that
            # matches a 'repeat'.  Append all the information for the
            # previous repeat.
            listOfOutputEphemerisColumns.append(currRepeatRowsList)

            # No need to update 'startingValue' variable.

            # Clear out the currRepeatRowsList since we hit the repeat degree.
            currRepeatRowsList = []

        # Add an entry for the current row and values.

        # Below uses the mod-360 longitude value.
        rowToAdd = timestampStr + "," + str(currValue % 360)

        # Below uses the always-increasing longitude value.  (commented out).
        # rowToAdd = timestampStr + "," + currValueStr

        # Below is the column of information for the offset
        # normalization, so that we can compare similar numbers of
        # degrees between previous repeats.
        multipleOfOffsetToSubtract = len(listOfOutputEphemerisColumns) - 1
        if multipleOfOffsetToSubtract <= 0:
            # No multiple because
            rowToAdd += "," + str(toNormalizedAngle((currValue % 360)))
        else:
            rowToAdd += "," + \
                        str(toNormalizedAngle((currValue % 360) - \
                                              (modOffsetPerColumnRepeat * \
                                              multipleOfOffsetToSubtract)))
        
        currRepeatRowsList.append(rowToAdd)

    # Update the curr and prev values for the next iteration.
    prevValue = currValue
    currValue = None

log.info("We have found {} complete cycle repeats in this data.".\
         format(numFullCycles))
log.info("Each repeat is the elapsing of {} degrees (or {} full circles).".\
         format(numDegreesElapsedForRepeat,
                numDegreesElapsedForRepeat / 360.0))

if numFullCycles != len(listOfOutputEphemerisColumns):
    log.info("We have found {} hits to the repeat degree in this data.  ".\
             format(len(listOfOutputEphemerisColumns)) + \
             "(This can happen for geocentric planets).")
         
# At this point, we've gone through all the rows in our input
# ephemeris file.  There may be rows that didn't complete a full
# 'repeat'; if so, then we'll just append those values for an
# incomplete repeat.
if len(currRepeatRowsList) != 0:
    listOfOutputEphemerisColumns.append(currRepeatRowsList)
    

log.info("Matching up ephemeris dates to market data ...")

# This is the current index that we are at while traversing list of
# rows of market data.  This is so we don't have to search through the
# whole market data list to find a matching date for each ephemeris
# timestamp.  We assume that the market data is in sequential order
# from earliest timestamp to later timestamp.
currIndexInMarketData = 0

# Now we will find the market data (high price and low price) for each
# corresponding date.  This algorithm below assumes that the market
# data is ordered from earlier timestamp to later timestamp.
for i in range(0, len(listOfOutputEphemerisColumns)):
    repeatRowsList = listOfOutputEphemerisColumns[i]

    for j in range(0, len(repeatRowsList)):
        row = repeatRowsList[j]
        rowSplit = row.split(",")
        
        # Get the timestamp str, which should be the first item in this list.
        timestampStr = rowSplit[0]
        
        # Turn this timestampStr into a datetime.
        ephemerisDt = convertTimestampStrToDatetime(timestampStr)

        # Data we are seeking that matches this timestamp date.
        marketDataDt = None
        highPriceStr = None
        lowPriceStr = None
        
        # Find the next market data row that matches the date.
        for k in range(currIndexInMarketData, len(listOfMarketDataDataValues)):
            currRow = listOfMarketDataDataValues[k]
            
            marketDataTimestampStr = currRow[marketDataInputFileTimestampColumn]
            currHighPriceStr = currRow[marketDataInputFileHighPriceColumn]
            currLowPriceStr = currRow[marketDataInputFileLowPriceColumn]
    
            # Convert the timestampStr to a datetime.
            # This timestamp str is expected to be in format "MM/DD/YYYY".
            currMarketDataDt = \
                convertTimestampStrToDatetime2(marketDataTimestampStr)
    
            if currMarketDataDt.date() == ephemerisDt.date():
                # This is what we're looking for.  The dates match.  Store
                # the data connected to this row.
                marketDataDt = currMarketDataDt
                highPriceStr = currHighPriceStr
                lowPriceStr = currLowPriceStr
                
                # Increment the index of where we are in the market data
                # so we don't have to search from the beginning all over
                # again when we look at the next ephemeris timestamp.
                currIndexInMarketData = k + 1
                break
            
            elif currMarketDataDt.date() < ephemerisDt.date():
                # Market data date is currently before the ephemeris date.
                # Look at the next market data date...
                currIndexInMarketData = k + 1
                continue
            
            elif currMarketDataDt.date() > ephemerisDt.date():
                # The current market data date is after the current
                # ephemeris date.  Break out of this for loop until we get
                # to that matching date in the ephemeris timestamps.
    
                # This date for the ephemeris doesn't appear to have a
                # matching market date (the ephemeris date might be a
                # weekend), so we'll set the market data values we are
                # looking for to None.
                marketDataDt = None
                highPriceStr = None
                lowPriceStr = None
    
                break

        # See if we found market data matching this ephemeris timestamp date.
        if marketDataDt != None and \
           highPriceStr != None and \
           lowPriceStr != None:

            log.debug("We found market data matching ephemeris timestamp: {}".\
                      format(ephemerisDt))
            
            # We have high and low price data matching the ephemeris
            # timestamp date.
            
            # Append the high and low prices to the row.
            listOfOutputEphemerisColumns[i][j] += \
                "," + highPriceStr + "," + lowPriceStr
            
            log.debug("listOfOutputEphemerisColumns[{}][{}] == {}".\
                      format(i, j, listOfOutputEphemerisColumns[i][j]))
                    
        else:
            log.debug("We DID NOT find market data matching ephemeris timestamp: {}".format(ephemerisDt))
            
            # We don't have any price data matching the ephemeris
            # timestamp date.  Use blank values for the high and low prices.
            listOfOutputEphemerisColumns[i][j] += "," + ","

            log.debug("listOfOutputEphemerisColumns[{}][{}] == {}".\
                      format(i, j, listOfOutputEphemerisColumns[i][j]))
            
                    


# Debug output:
for i in range(0, len(listOfOutputEphemerisColumns)):
    repeatRowsList = listOfOutputEphemerisColumns[i]
    for j in range(0, len(repeatRowsList)):
        row = repeatRowsList[j]
        log.debug("row for [{}][{}] == {}".format(i, j, row))
#shutdown(0)

# Write to output file.
log.info("Writing to output file: '{}' ...".format(outputFilename))

# String used for when there is no more data for this 'repeat' row.
emptyRepeatRowLine = ",,,,"

outputHeaderLine = ""
for i in range(0, len(listOfOutputEphemerisColumns)):
    multipleOfOffsetToSubtract = i - 1
    if multipleOfOffsetToSubtract < 0:
        outputHeaderLine += "Timestamp,{},{},HighPrice,LowPrice,".\
                            format(headerStrForPlanetMeasurement,
                                   headerStrForPlanetMeasurement)
    else:
        outputHeaderLine += "Timestamp,{},{}-({}*{}),HighPrice,LowPrice,".\
                            format(headerStrForPlanetMeasurement,
                                   headerStrForPlanetMeasurement,
                                   multipleOfOffsetToSubtract,
                                   modOffsetPerColumnRepeat)
    
# Strip off the trailing comma.
if len(outputHeaderLine) > 0:
    outputHeaderLine = outputHeaderLine[:-1]
    
try:
    with open(outputFilename, "w", encoding="utf-8") as f:
        endl = "\n"
        f.write(outputHeaderLine + endl)

        # Keep looping until there are no more rows written.
        rowWasWritten = True

        # Current index into all the repeats.
        repeatRowIndex = 0
        
        while rowWasWritten == True:
            # Reset the loop condition varible.
            rowWasWritten = False

            line = ""
            for i in range(0, len(listOfOutputEphemerisColumns)):
                
                repeatRowsList = listOfOutputEphemerisColumns[i]

                if repeatRowIndex < len(repeatRowsList):
                    row = repeatRowsList[repeatRowIndex]

                    log.debug("row == {}".format(row))
                    
                    line += row + ","
                    
                    log.debug("line == {}".format(line))
                    
                    rowWasWritten = True
                else:
                    line += emptyRepeatRowLine + ","

            # Remove the trailing comma.
            line = line[:-1]

            # Write the line to file.
            f.write(line + endl)
            
            # Increment the repeatRowIndex.
            repeatRowIndex += 1
            
except IOError as e:
    errStr = "I/O Error while trying to write file '" + \
             outputFilename + "':" + os.linesep + str(e)
    log.error(errStr)
    shutdown(1)


log.info("Done.")
shutdown(0)

##############################################################################
