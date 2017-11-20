##############################################################################
These steps below create an ephemeris containing 
Sunrise and Sunset times each day.


This resulting ephemeris will have the following data:
  date and time
  day of the week
  day count
  week count
  month count

  sunrise time
  G.Ascendant position
  G.Moon position
  G.Sun position

##############################################################################

# Step 1:
#
# Open file 'createGenericEphemerisSpreadsheet.py' and ensure the global
# variables are set as you desire them:
#
#        - Start and end dates
#        - Location (coordinates).
#

# Step 2:
# 
# Run the script to generate an ephemeris with just the 1-planet combinations.
# This should produce file: "sunrise_sunset_ephemeris_alexandria_va.csv".
#

python3 createGenericEphemerisSpreadsheet.py

# Step 3:
#
# If you modified the default location when running the first script
# for ephemeris generation, then at this point, you can rename the
# output CSV file(s) to whatever filename is relevant.
#

##############################################################################
