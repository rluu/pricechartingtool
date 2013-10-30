##############################################################################
These steps below create a master generic ephemeris (intraday).

This ephemeris will have the following data:
  date and time
  day of the week
  day count
  week count
  month count
  planet geocentric longitude positions
  planet heliocentric longitude positions
  planet declination position
  planet geocentric latitude position
  planet heliocentric latitude position

##############################################################################

# Step 1:
#
# Open file 'createGenericEphemerisSpreadsheet.py' and ensure the global
# variables are set as you desire them:
#
#        - Start and end dates/timestamps.
#        - Location (coordinates).
#        - Time of day.
#        - Output filename.
#


# Step 2:
# 
# Run the script to generate an ephemeris with just the 1-planet combinations.
# This should produce file: "generic_daily_ephemeris_nyc_noon.csv".
#

python3 createGenericEphemerisSpreadsheet.py


# Step 3:
#
# If you modified the default location when running the first script
# for ephemeris generation, then at this point, you can rename the
# output CSV file(s) to whatever filename is relevant.
#

##############################################################################
