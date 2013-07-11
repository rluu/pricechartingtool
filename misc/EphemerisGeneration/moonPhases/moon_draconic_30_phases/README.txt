##############################################################################
These steps below create an ephemeris containing 
30 Moon phases of a Draconic month.


This resulting ephemeris will have the following data:
  date and time
  day of the week
  day count
  week count
  month count

  planet geocentric longitude positions

  G.Moon/G.Sun
  G.Moon/G.Sun % 360
  G.Moon_Draconic_Month_Phase (Values in range: [1, 30])

  planet declination position
  planet geocentric latitude position
  2-planet geocentric combinations

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
# This should produce file: "sun_moon_node_ephemeris_nyc.csv".
#

python3 createGenericEphemerisSpreadsheet.py


# Step 3:
#
# Create the ephemeris spreadsheet with the 2-planet combinations.
# This will calculate and produce a column for the moon phases also.
# 
# This should read in file: "sun_moon_node_ephemeris_nyc.csv".
# This should produce file: "moon_draconic_30_phases_ephemeris_nyc.csv".
#

python3 makeFilledMasterEphemeris_2p_moon_draconic_30_phases.py


# Step 4:
#
# If you modified the default location when running the first script
# for ephemeris generation, then at this point, you can rename the
# output CSV file(s) to whatever filename is relevant.
#

##############################################################################
