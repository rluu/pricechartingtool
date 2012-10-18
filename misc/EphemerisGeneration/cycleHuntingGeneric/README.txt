##############################################################################
These steps below create a master generic ephemeris for noon at NYC.

This ephemeris will have the following data:
  planet geocentric positions
  planet heliocentric positions
  planet declination position
  planet latitude position
  2-planet geocentric combinations
  2-planet heliocentric combinations
  3-planet geocentric combinations
  3-planet heliocentric combinations

##############################################################################

# Step 1:
#
# Open file 'createGenericEphemerisSpreadsheet.py' and ensure the global
# variables are set as you desire them:
#
#        - Start and end dates
#        - Location (coordinates).
#        - Time of day.
#


# Step 2:
# 
# Run the script to generate an ephemeris with just the 1-planet combinations.
# This should produce file: "generic_daily_ephemeris_nyc_noon.csv".
#

python3 createGenericEphemerisSpreadsheet.py


# Step 3:
#
# Create the ephemeris spreadsheet with the 2-planet combinations.
# 
# This should read in file: "generic_daily_ephemeris_nyc_noon.csv".
# This should produce file: "master_2p_ephemeris_nyc_noon.csv".
#

python3 makeFilledMasterEphemeris_2p.py


# Step 4:
#
# Create the ephemeris spreadsheet with the 3-planet combinations.
# 
# This should read in file: "master_2p_ephemeris_nyc_noon.csv".
# This should produce file: "master_3p_ephemeris_nyc_noon.csv".
#

python3 makeFilledMasterEphemeris_3p.py


# Step 5:
#
# If you modified the default location when running the first script
# for ephemeris generation, then at this point, you can rename the
# output CSV file(s) to whatever filename is relevant.
#

##############################################################################
