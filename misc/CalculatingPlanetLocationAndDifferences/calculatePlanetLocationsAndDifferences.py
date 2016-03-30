#!/usr/bin/env python3
##############################################################################
# Description:
#
# 
# 
# Usage:
#
#   1) Run the script:
#
#           python3 
#
#
##############################################################################

# For obtaining current directory path information, and creating directories
import os
import sys 
import errno

# For copy.deepcopy()
import copy

# For dates.
import datetime

# For logging.
import logging

# For math.floor()
import math

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from astrologychart import AstrologyUtils
from ephemeris import Ephemeris
from data_objects import *


# For variables set to TTTA dates.
from ttta_dates import *
from dow_pivots import *
from planetaryEvents import *
##############################################################################

##############################################################################
# Global variables

# Version string.
VERSION = "0.1"

# Location information to use with the Ephemeris.
locationName = "New York City"
locationLongitude = -74.0064
locationLatitude = 40.7142
locationElevation = 0


loc1Name = "New York City"
loc1Longitude = -74.0064
loc1Latitude = 40.7142
loc1Elevation = 0
nycLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)

loc1Name = "Sherman"
loc1Longitude = -96.609
loc1Latitude = 33.635
loc1Elevation = 0
shermanLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)

loc1Name = "Texarkana"
loc1Longitude = -94.048
loc1Latitude = 33.045
loc1Elevation = 0
texarkanaLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)

loc1Name = "Paris"
loc1Longitude = 2.333
loc1Latitude = 48.87
loc1Elevation = 0
parisLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)

loc1Name = "Chicago"
loc1Longitude = 87.65
loc1Latitude = 41.85
loc1Elevation = 0
chicagoLoc = (loc1Name, loc1Longitude, loc1Latitude, loc1Elevation)



# Timezone information to use with the Ephemeris.
timezone = pytz.timezone("US/Eastern")
eastern = pytz.timezone("US/Eastern")
central =pytz.timezone("US/Central")

# Time of the day to use to whem getting ephemeris measurements.
#hourOfDay = 12
#minuteOfHour = 0

#loc1Tuple = shermanLoc
loc1Tuple = nycLoc



#startDt
dt1 = datetime.datetime(year=2004, month=12, day=4,
                        hour=12, minute=0,
                        tzinfo=eastern)

#dt1 = mrKInNYCPg64
#dt1 = mrKOilStocksHighPg65
#dt1 = mrKOilStocksLowPg65
#dt1 = sfEarthquakePg1
#dt1 = rgBirthday1906Pg1

#dt1 = dow_pivot_19260330
#dt1 = dow_pivot_19260416
#dt1 = dow_pivot_19260424
#dt1 = dow_pivot_19260519
#dt1 = dow_pivot_19260814
#dt1 = dow_pivot_19260824
#dt1 = dow_pivot_19260907
#dt1 = dow_pivot_19261019

#dt1 = marieBirthdayCandidatePg179
#dt1 = ww1BrokeOutPg7
#dt1 = usEnteredWorldWarPg10
#dt1 = windowPg40
#dt1 = christmas1926Pg42
#dt1 = letterOfCommendationPg43
#dt1 = letterRGTexarkanatoMrKpg62
#dt1 = letterWalterInNYCPg63
#dt1 = letterRGtoMrK2Pg65
#dt1 = rgRoadToFameAndFortunePg70
#dt1 = marieLetterToRgPg71
#dt1 = futureCyclesPg75
#dt1 = ww1OutbreakPg80
#dt1 = nonStopFlightToIrelandPg87
#dt1 = mrKFaithInRgPg91
#dt1 = rgGreatVictoryPg92
#dt1 = marieHopePrayLoveOfHeartPg94
#dt1 = cottonStartedUpFastPg94
#dt1 = cottonAdvancePg94
#dt1 = noProfitMarieFaith400pg95
#dt1 = marieFaithTradeCottonPurchasePg96
#dt1 = floodStartedMississippiValleyPg96
#dt1 = stLouisBirthdayPg96
#dt1 = fortuneSmilingPg97
#dt1 = marieLoveAndTrustPg97
#dt1 = rgGreatestWeekUpToThatTimePg101
#dt1 = rgAndMrKConferencePrivateOfficePg101
#dt1 = rgGreatestWeekUpToThatTimePg102
#dt1 = marieOverjoyedAtRGSuccessPg103
#dt1 = mariesPromisePg103
#dt1 = timeToStartBuyingWheatAndCornPg103
#dt1 = rgBuysCornForMariesAccountPg103
#dt1 = lindberghOverIrelandPg105
#dt1 = rgRedLetterDayPg105
#dt1 = rgLightestHeartPg108
#dt1 = rgAndMarieInDallasPg110
#dt1 = rgAndMarieReturnToShermanPg111
#dt1 = rgAndMarieInShermanPg111
#dt1 = rgSaysGoodbyeToMariePg111
#dt1 = rgLastDayInMrKOfficePg112
#dt1 = rgCycleTheoryPg112
#dt1 = rgMrKWeddingPresentPg113
#dt1 = rgCallsMarieOverLongDistanceBcSuccessPg114
#dt1 = rgRailroadStationAtTexarkanaTicketPg115
#dt1 = rgHeartInThroatPg116
#dt1 = rgMariePlansOnSunshineSpecialPg116
#dt1 = searchForMariePg118
#dt1 = marieMysteriousLetterPg120
#dt1 = rgAirplaneToSilverSpringPg257_candidate1
#dt1 = nearlyNoonUnionStationClockPg123
#dt1 = noonUnionStationClockPg123
#dt1 = rgTroubledAndDiscouragedHeartSadPg124
#dt1 = rgTimeAppointedToWaitPg125
#dt1 = rgHopelessToWaitSecretConfidedPg131
#dt1 = rgHeartHeavyShockRingPg133
#dt1 = sunThruWindowOfHotelPg137
#dt1 = prayerToUniversalPowerSignNeedPg140
#dt1 = rgHoldingRAFactPg146
#dt1 = mrKOnTelephoneWireJune6Pg147
#dt1 = mrKOnTelephoneWireJune7Pg147
#dt1 = openingOnTuesdayMorningJune7Pg152
#dt1 = stantonsDeepLetterToRGAtPlantersPg153
#dt1 = letterRgToStantonsPg154
#dt1 = newspapersWereOutPg156
#dt1 = sunsetDayWaningSadnessPg156
#dt1 = personalNoticesPlacedPg157
#dt1 = rgDreamsOfHisBirthdayPg160
#dt1 = rgBirthday1927Pg161
#dt1 = clockAt11OnRGBirthdayMindRevertPg162
#dt1 = clockAt12OnRGBirthdayPg162
#dt1 = clockAfter12OnRGBirthdayPg162
#dt1 = rgBeganToBeDisappointedOverHopefulPg163
#dt1 = rgBoughtEveningNewsPaperLookedOverFinancialPagePg171
#dt1 = rgSeesMadamCleoPg172
#dt1 = mrKLeavingOnSunshineSpecialPg179
#dt1 = mrKStLouisArrivalPg179
#dt1 = mrKAndRgAtUnionStationStLouisCandidate1Pg180
#dt1 = mrKAndRgAtUnionStationStLouisCandidate2Pg180
#dt1 = rgFirstArrivalNYCPg184
#dt1 = mrKAndWalterTalkAboutRGPg186
#dt1 = lindberghMarchUpBroadwayPg187
#dt1 = oneForAllPlayPg187
#dt1 = timeFactorDiscoveryPg197
#dt1 = majorMotorsPyramidPg197
#dt1 = wallStreet69Pg217
#dt1 = presElectionForecastPg218
#dt1 = geoVenusRetrograde19270820
#dt1 = geoVenusDirect19271001
#dt1 = justBeforeChristmasPg222
#dt1 = aFewDaysBeforeChristmasPg223
#dt1 = motherInNYPg224
#dt1 = rgBirthday1928
#dt1 = rgFlightToParisPg240
#dt1 = rgLadyBersfordInSebringPg267
#dt1 = rgBirthday1929
#dt1 = walterEdnaMarriage
#dt1 = dow_pivot_19300416
#dt1 = losAngeles
#dt1 = attackOnStLouisStartedPg315
#dt1 = franceAttackOnEnglandGermany1_Pg318
#dt1 = chicagoWhiteFlag_10am_Pg322

#dt1 = detroit1_RadiumRay_10pm_Pg345
#dt1 = detroit1_12am_Pg347
#dt1 = detroit2_3pm_Pg349
#dt1 = detroit2_5pm_Pg350

#dt1 = mamMotorPg353
#dt1 = mamFirstFlightPg354

#dt1 = franceAttackOnEnglandGermany2_Pg357

#dt1 = battleOfBostonPg358

#dt1 = nycGiganticAttack_8pm_Pg361
#dt1 = nycGiganticAttack_10pm_Pg361
#dt1 = nycGiganticAttack_1010pm_Pg362
#dt1 = nycGiganticAttack_12am_Pg365
#dt1 = nycGiganticAttack_1230am_Pg366

#dt1 = presidentOnMammouthBuilding_4am_Pg375

#dt1 = rgBirthday1932

#dt1 = colonelEdnaKennelworthInWashingtonPg383
#dt1 = battleOfWashingtonPg383

#dt1 = rgSevenDays_7am_Pg393
#dt1 = rgSevenDays_10am_Pg393

#dt1 = allCitiesInWorldWhereSCGDestroyedBuildingsHeardFromPg403

#dt1 = peaceConference_10am_Pg407
#dt1 = peaceConference_11am_Pg407
#dt1 = peaceConference_lateEvening_Pg415

#dt1 = timeAfterDiscoveryOfAmerica



loc2Tuple = nycLoc

#endDt
dt2 = datetime.datetime(year=2011, month=8, day=30,
                        hour=12, minute=0,
                        tzinfo=eastern)

#dt2 = mrKInNYCPg64
#dt2 = mrKOilStocksHighPg65
#dt2 = mrKOilStocksLowPg65
#dt2 = sfEarthquakePg1
#dt2 = marieBirthdayCandidatePg179
#dt2 = windowPg40
#dt2 = christmas1926Pg42
#dt2 = letterOfCommendationPg43
#dt2 = letterRGTexarkanatoMrKpg62
#dt2 = letterWalterInNYCPg63
#dt2 = letterRGtoMrK2Pg65
#dt2 = rgRoadToFameAndFortunePg70
#dt2 = marieLetterToRgPg71
#dt2 = futureCyclesPg75
#dt2 = ww1OutbreakPg80
#dt2 = mrKFaithInRgPg91
#dt2 = rgGreatVictoryPg92
#dt2 = marieHopePrayLoveOfHeartPg94
#dt2 = cottonStartedUpFastPg94
#dt2 = cottonAdvancePg94
#dt2 = noProfitMarieFaith400pg95
#dt2 = marieFaithTradeCottonPurchasePg96
#dt2 = floodStartedMississippiValleyPg96
#dt2 = stLouisBirthdayPg96
#dt2 = fortuneSmilingPg97
#dt2 = marieLoveAndTrustPg97
#dt2 = rgGreatestWeekUpToThatTimePg101
#dt2 = rgAndMrKConferencePrivateOfficePg101
#dt2 = rgGreatestWeekUpToThatTimePg102
#dt2 = marieOverjoyedAtRGSuccessPg103
#dt2 = mariesPromisePg103
#dt2 = timeToStartBuyingWheatAndCornPg103
#dt2 = rgBuysCornForMariesAccountPg103
#dt2 = lindberghOverIrelandPg105
#dt2 = rgRedLetterDayPg105
#dt2 = rgLightestHeartPg108
#dt2 = rgAndMarieInDallasPg110
#dt2 = rgAndMarieReturnToShermanPg111
#dt2 = rgAndMarieInShermanPg111
#dt2 = rgSaysGoodbyeToMariePg111
#dt2 = rgLastDayInMrKOfficePg112
#dt2 = rgCycleTheoryPg112
#dt2 = rgMrKWeddingPresentPg113
#dt2 = rgCallsMarieOverLongDistanceBcSuccessPg114
#dt2 = rgRailroadStationAtTexarkanaTicketPg115
#dt2 = rgHeartInThroatPg116
#dt2 = rgMariePlansOnSunshineSpecialPg116
#dt2 = searchForMariePg118
#dt2 = marieMysteriousLetterPg120
#dt2 = nearlyNoonUnionStationClockPg123
#dt2 = noonUnionStationClockPg123
#dt2 = rgTroubledAndDiscouragedHeartSadPg124
#dt2 = rgTimeAppointedToWaitPg125
#dt2 = rgHopelessToWaitSecretConfidedPg131
#dt2 = rgHeartHeavyShockRingPg133
#dt2 = sunThruWindowOfHotelPg137
#dt2 = prayerToUniversalPowerSignNeedPg140
#dt2 = rgHoldingRAFactPg146
#dt2 = mrKOnTelephoneWireJune6Pg147
#dt2 = mrKOnTelephoneWireJune7Pg147
#dt2 = openingOnTuesdayMorningJune7Pg152
#dt2 = stantonsDeepLetterToRGAtPlantersPg153
#dt2 = letterRgToStantonsPg154
#dt2 = newspapersWereOutPg156
#dt2 = sunsetDayWaningSadnessPg156
#dt2 = personalNoticesPlacedPg157
#dt2 = rgDreamsOfHisBirthdayPg160
#dt2 = rgBirthday1927Pg161
#dt2 = clockAt11OnRGBirthdayMindRevertPg162
#dt2 = clockAt12OnRGBirthdayPg162
#dt2 = clockAfter12OnRGBirthdayPg162
#dt2 = rgBeganToBeDisappointedOverHopefulPg163
#dt2 = rgBoughtEveningNewsPaperLookedOverFinancialPagePg171
#dt2 = rgSeesMadamCleoPg172
#dt2 = mrKLeavingOnSunshineSpecialPg179
#dt2 = mrKStLouisArrivalPg179
#dt2 = mrKAndRgAtUnionStationStLouisCandidate1Pg180
#dt2 = mrKAndRgAtUnionStationStLouisCandidate2Pg180
#dt2 = rgFirstArrivalNYCPg184
#dt2 = mrKAndWalterTalkAboutRGPg186
#dt2 = lindberghMarchUpBroadwayPg187
#dt2 = oneForAllPlayPg187
#dt2 = timeFactorDiscoveryPg197
#dt2 = majorMotorsPyramidPg197
#dt2 = wallStreet69Pg217
#dt2 = presElectionForecastPg218
#dt2 = justBeforeChristmasPg222
#dt2 = aFewDaysBeforeChristmasPg223
#dt2 = motherInNYPg224
#dt2 = rgBirthday1928
#dt2 = rgFlightToParisPg240
#dt2 = rgBirthday1929
#dt2 = walterEdnaMarriage
#dt2 = losAngeles
#dt2 = franceAttackOnEnglandGermany1_Pg318
#dt2 = chicagoWhiteFlag_10am_Pg322

#dt2 = detroit1_RadiumRay_10pm_Pg345
#dt2 = detroit1_12am_Pg347
#dt2 = detroit2_3pm_Pg349
#dt2 = detroit2_5pm_Pg350

#dt2 = mamMotorPg353
#dt2 = mamFirstFlightPg354

#dt2 = franceAttackOnEnglandGermany2_Pg357

#dt2 = battleOfBostonPg358

#dt2 = nycGiganticAttack_8pm_Pg361
#dt2 = nycGiganticAttack_10pm_Pg361
#dt2 = nycGiganticAttack_1010pm_Pg362
#dt2 = nycGiganticAttack_12am_Pg365
#dt2 = nycGiganticAttack_1230am_Pg366

#dt2 = presidentOnMammouthBuilding_4am_Pg375

#dt2 = rgBirthday1932

#dt2 = battleOfWashingtonPg383

#dt2 = rgSevenDays_7am_Pg393
#dt2 = rgSevenDays_10am_Pg393

#dt2 = allCitiesInWorldWhereSCGDestroyedBuildingsHeardFromPg403

#dt2 = peaceConference_10am_Pg407
#dt2 = peaceConference_11am_Pg407
#dt2 = peaceConference_lateEvening_Pg415

#dt2 = timeAfterDiscoveryOfAmerica


# Step size used when incrementing through all the timestamps between
# startDt and endDt.
stepSizeTd = datetime.timedelta(days=1)

# Error threshold for calculating timestamps.
maxErrorTd = datetime.timedelta(minutes=1)

# Destination output CSV file.
outputFilename = "/home/rluu/programming/pricechartingtool/misc/CalculatingPlanetConjunctions/planetGeocentricConjunctions.csv"

# Planet names to do calculations for.
geocentricPlanetNames = [\
    "H1",
    #"H4",
    #"H7",
    #"H10",
    "Moon",
    "MoSu",
    "Sun",
    "Mercury",
    "Venus",
    #"Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    #"Uranus",
    #"Neptune",
    #"Pluto",
    "TrueNorthNode",
    #"Chiron",
    #"Isis"
    ]

# Planet names to do calculations for.
heliocentricPlanetNames = [\
    #"Moon",
    "Mercury",
    "Venus",
    #"Sun",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    #"Uranus",
    #"Neptune",
    #"Pluto",
    #"TrueNorthNode",
    #"Chiron",
    #"Isis",


#    "MeVe",
#    "MeEa",
#    "MeMa",
#    "MeJu",
#    "MeSa",
###    #"MeUr",
#    "VeEa",
#    "VeMa",
#    "VeJu",
#    "VeSa",
##    #"VeUr",
#    "EaMa",
#    "EaJu",
#    "EaSa",
#    #"EaUr",
#    "MaJu",
#    "MaSa",
#    #"MaUr",
#    "JuSa",
#    #"JuUr",
#    #"SaUr",
    ]

# Line separator.
endl = os.linesep

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
    Ephemeris.closeEphemeris()
    
    logging.shutdown()
    
    sys.exit(rc)

##############################################################################

def isNumber(numStr):
    """Returns True if the string is a number."""

    rv = True
    
    for letter in numStr:
        if not (letter.isdigit() or letter == "."):
            rv = False
            break

    return rv

def formatToDateStr(dt):
    """Returns a date string in the format: "YYYY-MM-DD".

    Arguments:
    dt - datetime.datetime object.

    Returns:
    str object holding the date in format "YYYY-MM-DD".
    """

    dateStr = "{:04}-{:02}-{:02}".\
              format(dt.year, dt.month, dt.day)
    
    return dateStr

def formatToDateAndTimeStr(dt):
    """Returns a timestamp string in the format: "YYYY-MM-DD HH:MM"
    
    Arguments:
    dt - datetime.datetime object.

    Returns:
    str object holding the date in format "YYYY-MM-DD HH:MM".
    """

    dateAndTimeStr = "{:04}-{:02}-{:02} {:02}:{:02}".\
              format(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    
    return dateAndTimeStr


def getPlanetsForDatetimeAndTimezone(dt, locTuple):
    """Returns a string with the planet longitude position for the given
    datetime and timezone.
    """

    locName = locTuple[0]
    locLongitude = locTuple[1]
    locLatitude = locTuple[2]
    locElevation = locTuple[3]

    # Set the Location (required).
    Ephemeris.setGeographicPosition(locLongitude,
                                    locLatitude,
                                    locElevation)

    longitudeType = "tropical"
    fieldName = "longitude"

    rv = "For datetime: " + Ephemeris.datetimeToDayStr(dt) + \
         ", location: " + locName + endl

    
    for planetName in geocentricPlanetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, dt)

        longitude = pi.geocentric[longitudeType][fieldName]
                           
        # Format differently for lunation phase of G.MoSu.
        if planetName == "MoSu":
            rv += "  {: <14}".format("G." + planetName + ": ") + \
                  "{:>.3f}".format(longitude) + \
                  "    Phase (of max 30): {:.2f}".format(longitude / 12.0) + \
                  endl
        else:
            rv += "  {: <14}".format("G." + planetName + ": ") + \
                  "{:>.3f}".format(longitude) + \
                  endl

    rv += endl
        
    for planetName in heliocentricPlanetNames:
        pi = Ephemeris.getPlanetaryInfo(planetName, dt)

        rv += "  {: <14}".format("H." + planetName + ": ") + \
              "{:>.3f}".format(pi.heliocentric[longitudeType][fieldName]) + \
              endl
        
    return rv


def getLongitudeDiffBetweenDatetimes(planetName,
                                     centricityType,
                                     dt1,
                                     loc1Tuple,
                                     dt2,
                                     loc2Tuple):

    startTimestamp = dt1
    endTimestamp = dt2

    loc1Name = loc1Tuple[0]
    loc1Longitude = loc1Tuple[1]
    loc1Latitude = loc1Tuple[2]
    loc1Elevation = loc1Tuple[3]

    loc2Name = loc2Tuple[0]
    loc2Longitude = loc2Tuple[1]
    loc2Latitude = loc2Tuple[2]
    loc2Elevation = loc2Tuple[3]


    # maxErrorTd - datetime.timedelta object holding the maximum
    #              time difference between the exact planetary
    #              timestamp for the phenomena, and the one
    #              calculated.  This would define the accuracy of
    #              the calculations.
    #
    maxErrorTd = datetime.timedelta(seconds=4)

    # Size of a circle, in degrees.
    #
    # Here we define our own value instead of using the value in
    # AstrologyUtils.degreesInCircle because it is possible we may
    # want to test different sizes of a 'circle'.
    circleSizeInDegrees = 360.0
        
    # All references to longitude_speed need to
    # be from tropical zodiac measurements!  If I use
    # sidereal zodiac measurements for getting the
    # longitude_speed, then the measurements from the
    # Swiss Ephemeris do not yield the correct values.
    # I use the following variable in these locations.
    zodiacTypeForLongitudeSpeed = "tropical"

    tropicalZodiacFlag = True

    # Text to set in the text item.
    text = ""

    # Total number of degrees elapsed.
    totalDegrees = 0
    
    Ephemeris.setGeographicPosition(loc1Longitude,
                                    loc1Latitude,
                                    loc1Elevation)
    
    # List of PlanetaryInfo objects for this particular
    # planet, sorted by timestamp.
    planetData = []
                
    # Step size to use in populating the data list with
    # PlanetaryInfos.
    #
    # The step size should cause the planet to move less
    # than 120 degrees in all cases, and idealy much less
    # than this, that way we can easily narrow down when
    # the planet passes the 0 degree or 360 degree
    # threshold, and also so it is easier to narrow down
    # when retrograde periods happen.  If the step size is
    # too large, it is possible that we would miss a whole
    # time window of retrograde movement, so discretion
    # has to be used in determining what to use for this value.
    #
    # Here we will set it to 1 day for the default case,
    # but if the planet name is a house cusp then shrink
    # the step size so we will get the correct resolution.
    # Also, if the planet name is an outer planet with a
    # large period, we can increase the step size slightly
    # to improve performance.
    stepSizeTd = datetime.timedelta(days=1)

    
    if Ephemeris.isHouseCuspPlanetName(planetName) or \
           Ephemeris.isAscmcPlanetName(planetName):
                    
        stepSizeTd = datetime.timedelta(hours=1)
                    
    elif planetName == "Jupiter" or \
         planetName == "Saturn" or \
         planetName == "Neptune" or \
         planetName == "Uranus" or \
         planetName == "Pluto":
                    
        stepSizeTd = datetime.timedelta(days=5)
                
        log.debug("Stepping through from {} to {} ...".\
                  format(Ephemeris.datetimeToStr(startTimestamp),
                         Ephemeris.datetimeToStr(endTimestamp)))
                
    # Current datetime as we step through all the
    # timestamps between the start and end timestamp.
    currDt = copy.deepcopy(startTimestamp)
                
    # Step through the timestamps, calculating the planet positions.
    while currDt < endTimestamp:
        p = Ephemeris.getPlanetaryInfo(planetName, currDt)
        planetData.append(p)
                    
        # Increment step size.
        currDt += stepSizeTd
                    
    # We must also append the planet calculation for the end timestamp.
    Ephemeris.setGeographicPosition(loc2Longitude,
                                    loc2Latitude,
                                    loc2Elevation)
    p = Ephemeris.getPlanetaryInfo(planetName, endTimestamp)
    planetData.append(p)
                
    # Geocentric measurement.
    if centricityType == "geocentric":
                    
        # Get the PlanetaryInfos for the timestamps of the
        # planet at the moment right after the
        # longitude_speed polarity changes.
        additionalPlanetaryInfos = []
                    
        prevLongitudeSpeed = None
                    
        for i in range(len(planetData)):
            currLongitudeSpeed = \
                planetData[i].geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']
                        
            if prevLongitudeSpeed != None and \
               ((prevLongitudeSpeed < 0 and currLongitudeSpeed >= 0) or \
               (prevLongitudeSpeed >= 0 and currLongitudeSpeed < 0)):
                            
                # Polarity changed.
                # Try to narrow down the exact moment in
                # time when this occured.
                t1 = planetData[i-1].dt
                t2 = planetData[i].dt
                currErrorTd = t2 - t1
                            
                while currErrorTd > maxErrorTd:
                    if log.isEnabledFor(logging.DEBUG) == True:
                        log.debug("Refining between {} and {}".\
                                       format(Ephemeris.datetimeToStr(t1),
                                              Ephemeris.datetimeToStr(t2)))
                                
                    # Check the timestamp between.
                    diffTd = t2 - t1
                    halfDiffTd = \
                        datetime.\
                        timedelta(days=(diffTd.days / 2.0),
                                  seconds=(diffTd.seconds / 2.0),
                                  microseconds=(diffTd.\
                                                microseconds / 2.0))
                    testDt = t1 + halfDiffTd

                    p = Ephemeris.getPlanetaryInfo(planetName, testDt)
                    testLongitudeSpeed = \
                        p.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']

                    if ((prevLongitudeSpeed < 0 and \
                         testLongitudeSpeed >= 0) or \
                        (prevLongitudeSpeed >= 0 and \
                         testLongitudeSpeed < 0)):

                        # Polarity change at the test timestamp.
                        t2 = testDt

                    else:
                        # No polarity change yet.
                        t1 = testDt

                    # Update the currErrorTd.
                    currErrorTd = t2 - t1
                            
                log.debug("Broke out of loop to find " + \
                               "velocity polarity change.  " + \
                               "currErrorTd is: {}, ".\
                               format(currErrorTd))
                                           
                # Timestamp at t2 is now within the amount
                # of the time error threshold ('maxErrorTd')
                # following the polarity change.
                # Append this value to the list.
                p = Ephemeris.getPlanetaryInfo(planetName, t2)
                additionalPlanetaryInfos.append(p)

                t1pi = planetData[i-1]
                t2pi = Ephemeris.getPlanetaryInfo(planetName, t2)
                            
                if log.isEnabledFor(logging.DEBUG) == True:
                    log.debug("t1 == {}, ".\
                               format(Ephemeris.datetimeToStr(t1pi.dt)) + \
                               "longitude(tropical) == {}, ".\
                               format(t1pi.geocentric['tropical']['longitude']) + \
                               "longitude(sidereal) == {}, ".\
                               format(t1pi.geocentric['sidereal']['longitude']) + \
                               "longitude_speed == {}, ".\
                               format(t1pi.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']))
                                
                    log.debug("t2 == {}, ".\
                               format(Ephemeris.datetimeToStr(t2pi.dt)) + \
                               "longitude(tropical) == {}, ".\
                               format(t2pi.geocentric['tropical']['longitude']) + \
                               "longitude(sidereal) == {}, ".\
                               format(t2pi.geocentric['sidereal']['longitude']) + \
                               "longitude_speed == {}, ".\
                               format(t2pi.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed']))
                            
                # There is no need to update
                # currLongitudeSpeed here, because the
                # longitude_speed for 'p' should be the
                # same polarity.
                            
            # Update prevLongitudeSpeed.
            prevLongitudeSpeed = currLongitudeSpeed
                        
        # Sort all the extra PlanetaryInfo objects by timestamp.
        additionalPlanetaryInfos = \
            sorted(additionalPlanetaryInfos, key=lambda c: c.dt)
                    
        # Insert PlanetaryInfos from
        # 'additionalPlanetaryInfos' into 'planetData' at
        # the timestamp-ordered location.
        currLoc = 0
        for i in range(len(additionalPlanetaryInfos)):
            pi = additionalPlanetaryInfos[i]

            insertedFlag = False
                        
            while currLoc < len(planetData):
                if pi.dt < planetData[currLoc].dt:
                    planetData.insert(currLoc, pi)
                    insertedFlag = True
                    currLoc += 1
                    break
                else:
                    currLoc += 1
                        
            if insertedFlag == False:
                # PlanetaryInfo 'pi' has a timestamp that
                # is later than the last PlanetaryInfo in
                # 'planetData', so just append it.
                planetData.append(pi)

                # Increment currLoc so that the rest of
                # the PlanetaryInfos in
                # 'additionalPlanetaryInfos' can be
                # appended without doing anymore timestamp tests.
                currLoc += 1

        # Do summations to determine the measurements.
        showGeocentricRetroAsNegativeTextFlag = True
        if showGeocentricRetroAsNegativeTextFlag == True:
            if tropicalZodiacFlag == True:
                totalDegrees = 0
                zodiacType = "tropical"
                            
                for i in range(len(planetData)):
                    if i != 0:
                        prevPi = planetData[i-1]
                        currPi = planetData[i]

                        if prevPi.geocentric[zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                            # Direct motion.
                            # Elapsed amount for this segment should be positive.
                                        
                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.geocentric[zodiacType]['longitude'] - \
                                prevPi.geocentric[zodiacType]['longitude']
                                        
                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            longitudeElapsed = \
                                Util.toNormalizedAngle(longitudeElapsed)

                            totalDegrees += longitudeElapsed
                        else:
                            # Retrograde motion.
                            # Elapsed amount for this segment should be negative.
                            
                            # Find the amount of longitude elasped.
                            longitudeElapsed = \
                                currPi.geocentric[zodiacType]['longitude'] - \
                                prevPi.geocentric[zodiacType]['longitude']

                            # See if there was a crossing of the
                            # 0 degree point or the 360 degree point.
                            # If so, make the necessary adjustments
                            # so that the longitude elapsed is
                            # correct.
                            if longitudeElapsed > 0:
                                longitudeElapsed -= 360

                            totalDegrees += longitudeElapsed
                                    
                # Line of text.  We append measurements to
                # this line of text depending on what
                # measurements are enabled.
                line = "G T {} moves ".format(planetName)

                numCircles = totalDegrees / circleSizeInDegrees
                numBiblicalCircles = \
                    totalDegrees / AstrologyUtils.degreesInBiblicalCircle
                            
                line += "{:.2f} deg ".format(totalDegrees)

                # Append last part of the line.
                line += "(r as -)"
                            
                text += line + os.linesep
                            
    if centricityType == "heliocentric":

        if tropicalZodiacFlag == True:
            totalDegrees = 0
            zodiacType = "tropical"
                        
            for i in range(len(planetData)):
                if i != 0:
                    prevPi = planetData[i-1]
                    currPi = planetData[i]
                                
                    if prevPi.heliocentric[zodiacTypeForLongitudeSpeed]['longitude_speed'] >= 0:
                        # Direct motion.
                        # Elapsed amount for this segment should be positive.
                                    
                        # Find the amount of longitude elasped.
                        longitudeElapsed = \
                            currPi.heliocentric[zodiacType]['longitude'] - \
                            prevPi.heliocentric[zodiacType]['longitude']
                                    
                        # See if there was a crossing of the
                        # 0 degree point or the 360 degree point.
                        # If so, make the necessary adjustments
                        # so that the longitude elapsed is
                        # correct.
                        longitudeElapsed = \
                            Util.toNormalizedAngle(longitudeElapsed)
                                    
                        totalDegrees += longitudeElapsed
                    else:
                        # Retrograde motion.
                        # Elapsed amount for this segment should be negative.
                                    
                        # Find the amount of longitude elasped.
                        longitudeElapsed = \
                            currPi.heliocentric[zodiacType]['longitude'] - \
                            prevPi.heliocentric[zodiacType]['longitude']
                                    
                        # See if there was a crossing of the
                        # 0 degree point or the 360 degree point.
                        # If so, make the necessary adjustments
                        # so that the longitude elapsed is
                        # correct.
                        if longitudeElapsed > 0:
                            longitudeElapsed -= 360
                                        
                        totalDegrees += longitudeElapsed
                                    
            # Line of text.  We append measurements to
            # this line of text depending on what
            # measurements are enabled.
            line = "H T {} moves ".format(planetName)
                            
            numCircles = totalDegrees / circleSizeInDegrees
            numBiblicalCircles = \
                totalDegrees / AstrologyUtils.degreesInBiblicalCircle
            
            line += "{:.2f} deg ".format(totalDegrees)

            text += line + os.linesep
                        
    text = text.rstrip()
    
    return totalDegrees

    
def getPlanetDiffsForDatetimes(dt1,
                               loc1Tuple,
                               dt2,
                               loc2Tuple):
    """Returns a string with the planet longitude differences between the given
    datetimes and location.
    """

    loc1Name = loc1Tuple[0]
    loc1Longitude = loc1Tuple[1]
    loc1Latitude = loc1Tuple[2]
    loc1Elevation = loc1Tuple[3]

    loc2Name = loc2Tuple[0]
    loc2Longitude = loc2Tuple[1]
    loc2Latitude = loc2Tuple[2]
    loc2Elevation = loc2Tuple[3]


    longitudeType = "tropical"
    fieldName = "longitude"

    rv = "Between datetime: " + Ephemeris.datetimeToDayStr(dt1) + \
         ", location: " + loc1Name + " and " + endl
    rv += "        datetime: " + Ephemeris.datetimeToDayStr(dt2) + \
         ", location: " + loc2Name + endl


    calendarDayDiff = dt2 - dt1
    rv += "  Diff calendar days: {}".format(calendarDayDiff) + endl
    
    for planetName in geocentricPlanetNames:

        longitudeDiff = getLongitudeDiffBetweenDatetimes(planetName,
                                                         "geocentric",
                                                         dt1,
                                                         loc1Tuple,
                                                         dt2,
                                                         loc2Tuple)
        longitudeDiffFullRevs = int(longitudeDiff // 360)
        longitudeDiffMod360 = longitudeDiff % 360
        
        # Format differently for lunation phase of G.MoSu.
        if planetName == "MoSu":
            rv += "  {: <16}".format("Diff G." + planetName + ": ") + \
                  "{:>10.3f}".format(longitudeDiff) + \
                  "    or  {:>4} rev + {:>7.3f} deg".format(longitudeDiffFullRevs,
                                                            longitudeDiffMod360) + \
                  "     PhaseCountTotal: {:.2f}, Phase (of max 30): {:.2f}".\
                  format(longitudeDiff / 12.0, longitudeDiffMod360 / 12.0) + \
                  endl
        else:
            rv += "  {: <16}".format("Diff G." + planetName + ": ") + \
                  "{:>10.3f}".format(longitudeDiff) + \
                  "    or  {:>4} rev + {:>7.3f} deg".format(longitudeDiffFullRevs,
                                                            longitudeDiffMod360) + \
                  endl
            
    rv += endl
        
    for planetName in heliocentricPlanetNames:

        longitudeDiff = getLongitudeDiffBetweenDatetimes(planetName,
                                                         "heliocentric",
                                                         dt1,
                                                         loc1Tuple,
                                                         dt2,
                                                         loc2Tuple)
        longitudeDiffFullRevs = int(longitudeDiff // 360)
        longitudeDiffMod360 = longitudeDiff % 360
        
        rv += "  {: <16}".format("Diff H." + planetName + ": ") + \
              "{:>10.3f}".format(longitudeDiff) + \
              "    or  {:>4} rev + {:>7.3f} deg".format(longitudeDiffFullRevs,
                                                        longitudeDiffMod360) + \
              endl
        
    return rv




##############################################################################

if __name__ == "__main__":
    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    printDt1 = True
    #printDt1 = False
    
    printDt2 = True
    #printDt2 = False
    
    printDiff = True
    #printDiff = False

    if 'printDt1' in locals() and printDt1 == True:
        outputStr = getPlanetsForDatetimeAndTimezone(dt1,
                                                     loc1Tuple)
        print(outputStr)


    if 'printDt2' in locals() and printDt2 == True:
        outputStr = getPlanetsForDatetimeAndTimezone(dt2,
                                                     loc2Tuple)
        print(outputStr)


    if 'printDiff' in locals() and printDiff == True:
        outputStr = getPlanetDiffsForDatetimes(dt1,
                                               loc1Tuple,
                                               dt2,
                                               loc2Tuple)
        print(outputStr)


    #log.info("Done.")
    shutdown(0)

##############################################################################
