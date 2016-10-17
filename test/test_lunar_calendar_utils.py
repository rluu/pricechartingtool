import unittest

import datetime
import os
import sys
import pytz

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(thisScriptDir) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)

from util import Util
from ephemeris import Ephemeris
from lunar_calendar_utils import LunarDate
from lunar_calendar_utils import LunarTimeDelta
from lunar_calendar_utils import LunarCalendarUtils


##############################################################################

class LunarDateTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize Ephemeris (required).
        Ephemeris.initialize()

        # Set the Location (required).

        # Chicago:
        #lon = -87.627777777777
        #lat = 41.8819444444444444

        # Chantilly/Arlington:
        #lon = -77.084444
        #lat = 38.890277

        # New York City:
        lon = -74.0064
        lat = 40.7142

        #Ephemeris.setGeographicPosition(lon, lat, -68)
        Ephemeris.setGeographicPosition(lon, lat)

    def tearDown(self):
        # Close the Ephemeris so it can do necessary cleanups.
        Ephemeris.closeEphemeris()

    def testCreationAllInts(self):
        lunarDate = LunarDate(2016, 3, 0)
        self.assertEqual(lunarDate.year, 2016)
        self.assertEqual(lunarDate.month, 3)
        self.assertEqual(lunarDate.day, 0)

    def testCreationFloatYear(self):
        with self.assertRaises(ValueError):
            lunarDate = LunarDate(2016.2, 3, 0)

    def testCreationFloatMonth(self):
        with self.assertRaises(ValueError):
            lunarDate = LunarDate(2016, 3.5, 0)

    def testCreationFullMoon(self):
        lunarDate = LunarDate(2016, 1, 15)
        self.assertEqual(lunarDate.year, 2016)
        self.assertEqual(lunarDate.month, 1)
        self.assertEqual(lunarDate.day, 15)
        #print("lunarDate == {}".format(lunarDate))
        dt = LunarCalendarUtils.lunarDateToDatetime(lunarDate)
        #print("dt == {}".format(Ephemeris.datetimeToDayStr(dt)))
        pi = Ephemeris.getPlanetaryInfo("MoSu", dt)
        longitude = pi.geocentric['tropical']['longitude']
        #print("longitude == {}".format(longitude))
        self.assertTrue(Util.fuzzyIsEqual(longitude, 180.0, maxDiff=0.0002))

    def testCreationFloatDay(self):
        lunarDate = LunarDate(2016, 3, 0.5)
        self.assertEqual(lunarDate.year, 2016)
        self.assertEqual(lunarDate.month, 3)
        self.assertEqual(lunarDate.day, 0.5)
        #print("lunarDate == {}".format(lunarDate))
        dt = LunarCalendarUtils.lunarDateToDatetime(lunarDate)
        #print("dt == {}".format(Ephemeris.datetimeToDayStr(dt)))
        pi = Ephemeris.getPlanetaryInfo("MoSu", dt)
        longitude = pi.geocentric['tropical']['longitude']
        #print("longitude == {}".format(longitude))
        self.assertTrue(Util.fuzzyIsEqual(longitude, 6.0, maxDiff=0.0002))

    def testCreationInvalidMonth(self):
        with self.assertRaises(ValueError):
            lunarDate = LunarDate(2012, 13, 5)

    def testAdditionWithWrongType(self):
        lunarDateA = LunarDate(2016, 3, 0.5)
        lunarDateB = LunarDate(2016, 5, 23)
        with self.assertRaises(ValueError):
            lunarDateC = lunarDateA + lunarDateB

    def testAdditionWithLunarTimeDeltaYearAdditionNotLeapYear(self):
        lunarDate = LunarDate(2012, 12, 5)
        lunarTimeDelta = LunarTimeDelta(years=1)
        result = lunarDate + lunarTimeDelta
        self.assertEqual(result, LunarDate(2013, 12, 5))

        # Normal wrapping (non-leap year).
        lunarDate = LunarDate(2012, 7, 15)
        lunarTimeDelta = LunarTimeDelta(months=10)
        result = lunarDate + lunarTimeDelta
        self.assertEqual(result, LunarDate(2013, 5, 15))

    def testAdditionWithLunarTimeDeltaYearAdditionLeapYear(self):
        lunarDate = LunarDate(2013, 7, 15)
        lunarTimeDelta = LunarTimeDelta(years=1)
        result = lunarDate + lunarTimeDelta
        self.assertEqual(result, LunarDate(2014, 7, 15))

        # Normal wrapping (leap year).
        lunarDate = LunarDate(2013, 7, 15)
        lunarTimeDelta = LunarTimeDelta(months=10)
        result = lunarDate + lunarTimeDelta
        self.assertEqual(result, LunarDate(2014, 4, 15))

        # This is showing that adding can result in wrapping
        # of an extra lunar year.
        lunarDate = LunarDate(2013, 13, 5)
        lunarTimeDelta = LunarTimeDelta(years=1)
        result = lunarDate + lunarTimeDelta
        self.assertEqual(result, LunarDate(2015, 1, 5))

        # Adding negative LunarTimeDelta values.
        lunarDate = LunarDate(2013, 13, 5)
        lunarTimeDelta = LunarTimeDelta(years=0, months=-13, days=2)
        result = lunarDate + lunarTimeDelta
        self.assertEqual(result, LunarDate(2012, 12, 7))

    def testSubtractionWithLunarTimeDelta(self):
        lunarDate = LunarDate(2013, 13, 5)
        lunarTimeDelta = LunarTimeDelta(months=5, days=3)
        result = lunarDate - lunarTimeDelta
        self.assertEqual(result, LunarDate(2013, 8, 2))

        # Test wraping months.
        lunarDate = LunarDate(2013, 13, 5)
        lunarTimeDelta = LunarTimeDelta(months=5, days=9)
        result = lunarDate - lunarTimeDelta
        self.assertEqual(result, LunarDate(2013, 7, 26))

        # Test wraping years.
        lunarDate = LunarDate(2013, 13, 5)
        lunarTimeDelta = LunarTimeDelta(months=13)
        result = lunarDate - lunarTimeDelta
        self.assertEqual(result, LunarDate(2012, 12, 5))

        # Subtracting negative LunarTimeDelta values.
        lunarDate = LunarDate(2013, 13, 5)
        lunarTimeDelta = LunarTimeDelta(years=0, months=-13, days=2)
        result = lunarDate - lunarTimeDelta
        self.assertEqual(result, LunarDate(2015, 1, 3))

    def testSubtractionWithLunarDate(self):
        lunarDateA = LunarDate(2013, 13, 5)
        lunarDateB = LunarDate(2012, 12, 5)
        lunarTimeDelta = lunarDateA - lunarDateB
        self.assertEqual(lunarTimeDelta, LunarTimeDelta(years=1, months=1, days=0))

        # Test wraping months.
        lunarDateA = LunarDate(2013, 1, 5)
        lunarDateB = LunarDate(2011, 12, 5)
        lunarTimeDelta = lunarDateA - lunarDateB
        self.assertEqual(lunarTimeDelta, LunarTimeDelta(years=2, months=-11, days=0))

        lunarDateA = LunarDate(2013, 1, 5)
        lunarDateB = LunarDate(2011, 12, 9)
        lunarTimeDelta = lunarDateA - lunarDateB
        self.assertEqual(lunarTimeDelta, LunarTimeDelta(years=2, months=-11, days=-4))

        # Test wraping years.
        lunarDateA = LunarDate(2011, 3, 5)
        lunarDateB = LunarDate(2013, 5, 5)
        lunarTimeDelta = lunarDateA - lunarDateB
        self.assertEqual(lunarTimeDelta, LunarTimeDelta(years=-2, months=-2, days=0))

        # Test not wrapping anything.
        lunarDateA = LunarDate(2013, 5, 5)
        lunarDateB = LunarDate(2011, 3, 5)
        lunarTimeDelta = lunarDateA - lunarDateB
        self.assertEqual(lunarTimeDelta, LunarTimeDelta(years=2, months=2, days=0))

    def testEquals(self):
        lunarDateA = LunarDate(2013, 13, 5.0)
        lunarDateB = LunarDate(2013, 13, 5.0)
        self.assertTrue(lunarDateA == lunarDateB)
        lunarDateA = LunarDate(2013, 13, 5.0)
        lunarDateB = LunarDate(2012, 12, 1.0)
        self.assertFalse(lunarDateA == lunarDateB)

    def testNotEquals(self):
        lunarDateA = LunarDate(2013, 13, 5.0)
        lunarDateB = LunarDate(2013, 13, 6.0)
        self.assertTrue(lunarDateA != lunarDateB)
        lunarDateA = LunarDate(2013, 13, 6.0)
        lunarDateB = LunarDate(2013, 13, 6.0)
        self.assertFalse(lunarDateA != lunarDateB)

    def testGreaterThan(self):
        lunarDateA = LunarDate(2013, 13, 8.0)
        lunarDateB = LunarDate(2013, 13, 5.0)
        self.assertTrue(lunarDateA > lunarDateB)

    def testLessThan(self):
        lunarDateA = LunarDate(2013, 13, 1.0)
        lunarDateB = LunarDate(2013, 13, 5.0)
        self.assertTrue(lunarDateA < lunarDateB)

class LunarTimeDeltaTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize Ephemeris (required).
        Ephemeris.initialize()

        # Set the Location (required).

        # Chicago:
        #lon = -87.627777777777
        #lat = 41.8819444444444444

        # Chantilly/Arlington:
        #lon = -77.084444
        #lat = 38.890277

        # New York City:
        lon = -74.0064
        lat = 40.7142

        #Ephemeris.setGeographicPosition(lon, lat, -68)
        Ephemeris.setGeographicPosition(lon, lat)

    def tearDown(self):
        # Close the Ephemeris so it can do necessary cleanups.
        Ephemeris.closeEphemeris()

    def testAdditionWithLunarTimeDelta(self):
        # Test wrapping months.
        lunarTimeDeltaA = LunarTimeDelta(years=1, months=2, days=3)
        lunarTimeDeltaB = LunarTimeDelta(years=1, months=3, days=29)
        resultTimeDelta = lunarTimeDeltaA + lunarTimeDeltaB
        self.assertTrue(resultTimeDelta == LunarTimeDelta(years=2, months=6, days=2))

        # Test many months, not wrapping years.
        lunarTimeDeltaA = LunarTimeDelta(years=1, months=11, days=3)
        lunarTimeDeltaB = LunarTimeDelta(years=1, months=5, days=29)
        resultTimeDelta = lunarTimeDeltaA + lunarTimeDeltaB
        self.assertTrue(resultTimeDelta == LunarTimeDelta(years=2, months=17, days=2))

    def testSubtractionWithLunarTimeDelta(self):
        # Test wrapping months.
        lunarTimeDeltaA = LunarTimeDelta(years=1, months=2, days=3)
        lunarTimeDeltaB = LunarTimeDelta(years=1, months=3, days=29)
        resultTimeDelta = lunarTimeDeltaA - lunarTimeDeltaB
        self.assertTrue(resultTimeDelta == LunarTimeDelta(years=0, months=-1, days=-26))

        lunarTimeDeltaA = LunarTimeDelta(years=1, months=2, days=3)
        lunarTimeDeltaB = LunarTimeDelta(years=0, months=3, days=4)
        resultTimeDelta = lunarTimeDeltaA - lunarTimeDeltaB
        self.assertTrue(resultTimeDelta == LunarTimeDelta(years=1, months=-1, days=-1))

        lunarTimeDeltaA = LunarTimeDelta(years=5, months=5, days=3)
        lunarTimeDeltaB = LunarTimeDelta(years=0, months=4, days=4)
        resultTimeDelta = lunarTimeDeltaA - lunarTimeDeltaB
        self.assertTrue(resultTimeDelta == LunarTimeDelta(years=5, months=1, days=-1))

        # Test many months, not wrapping years.
        lunarTimeDeltaA = LunarTimeDelta(years=1, months=11, days=3)
        lunarTimeDeltaB = LunarTimeDelta(years=0, months=50, days=1)
        resultTimeDelta = lunarTimeDeltaA - lunarTimeDeltaB
        self.assertTrue(resultTimeDelta == LunarTimeDelta(years=1, months=-39, days=2))

class LunarCalendarUtilsTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize Ephemeris (required).
        Ephemeris.initialize()

        # Set the Location (required).

        # Chicago:
        #lon = -87.627777777777
        #lat = 41.8819444444444444

        # Chantilly/Arlington:
        #lon = -77.084444
        #lat = 38.890277

        # New York City:
        lon = -74.0064
        lat = 40.7142

        #Ephemeris.setGeographicPosition(lon, lat, -68)
        Ephemeris.setGeographicPosition(lon, lat)

    def tearDown(self):
        # Close the Ephemeris so it can do necessary cleanups.
        Ephemeris.closeEphemeris()

    def testIsLunarLeapYear(self):
        # Year 2000 does follow the 19-year sequence.
        # When I checked on paper, by hand, the result of False is correct.
        # There is a full moon on March 20, 2000, G.Sun is at 29 Pis 53.
        # There is a full moon on March 21, 2019, G.Sun is at  0 Ari 09.
        # There is a full moon on March 21, 2038, G.Sun is at  0 Ari 33.
        year = 2000
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))

        # The rest of the test cases follows the 19-year sequence, as expected.

        year = 2001
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2002
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2003
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2004
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2005
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2006
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2007
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2008
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2009
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2010
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2011
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2012
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2013
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2014
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2015
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2016
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2017
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2018
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2019
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2020
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2021
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2022
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2023
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2024
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2025
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2026
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2027
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2028
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2029
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2030
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2031
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2032
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2033
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2034
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2035
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2036
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2037
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2038
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertTrue(LunarCalendarUtils.isLunarLeapYear(year))
        year = 2039
        #print("year == {}, rv == {}".format(year, LunarCalendarUtils.isLunarLeapYear(year)))
        self.assertFalse(LunarCalendarUtils.isLunarLeapYear(year))

    def testDatetimeToLunarDate(self):
        dt = datetime.datetime(2016, 5, 21, 21, 16, 0, tzinfo=pytz.utc)
        lunarDt = LunarCalendarUtils.datetimeToLunarDate(dt)
        self.assertEqual(lunarDt.year, 2016)
        self.assertEqual(lunarDt.month, 3)
        self.assertTrue(Util.fuzzyIsEqual(lunarDt.day, 15, maxDiff=0.001))

        eastern = pytz.timezone('US/Eastern')
        dt = datetime.datetime(2016, 5, 21, 21, 16, 0, tzinfo=eastern)
        lunarDt = LunarCalendarUtils.datetimeToLunarDate(dt)
        self.assertEqual(lunarDt.year, 2016)
        self.assertEqual(lunarDt.month, 3)
        self.assertTrue(Util.fuzzyIsEqual(lunarDt.day, 15.191, maxDiff=0.001))

    def testGetNisan1DatetimeForYear(self):
        # This Nisan 1 happens to be a new moon in Aries.
        nisan1Dt = \
            LunarCalendarUtils.getNisan1DatetimeForYear(1897)
        self.assertEqual(nisan1Dt.year, 1897)
        self.assertEqual(nisan1Dt.month, 4)
        self.assertEqual(nisan1Dt.day, 2)
        self.assertEqual(nisan1Dt.hour, 4)
        self.assertEqual(nisan1Dt.minute, 24)

        nisan1Dt = \
            LunarCalendarUtils.getNisan1DatetimeForYear(2004)
        self.assertEqual(nisan1Dt.year, 2004)
        self.assertEqual(nisan1Dt.month, 3)
        self.assertEqual(nisan1Dt.day, 20)
        self.assertEqual(nisan1Dt.hour, 22)
        self.assertEqual(nisan1Dt.minute, 42)

        eastern = pytz.timezone('US/Eastern')
        nisan1Dt = \
            LunarCalendarUtils.getNisan1DatetimeForYear(2004, tzInfo=eastern)
        self.assertEqual(nisan1Dt.year, 2004)
        self.assertEqual(nisan1Dt.month, 3)
        self.assertEqual(nisan1Dt.day, 20)
        self.assertEqual(nisan1Dt.hour, 17)
        self.assertEqual(nisan1Dt.minute, 42)

    def testLunarDateToDatetime(self):
        lunarDt = LunarDate(2002, 4, 15)
        dt = LunarCalendarUtils.lunarDateToDatetime(lunarDt)
        self.assertEqual(dt.year, 2002)
        self.assertEqual(dt.month, 6)
        self.assertEqual(dt.day, 24)
        self.assertEqual(dt.hour, 21)
        self.assertEqual(dt.minute, 42)

        eastern = pytz.timezone('US/Eastern')
        lunarDt = LunarDate(2002, 4, 15)
        dt = LunarCalendarUtils.lunarDateToDatetime(lunarDt, tzInfo=eastern)
        self.assertEqual(dt.year, 2002)
        self.assertEqual(dt.month, 6)
        self.assertEqual(dt.day, 24)
        self.assertEqual(dt.hour, 17)
        self.assertEqual(dt.minute, 42)

##############################################################################

if __name__ == "__main__":

    # Set to True for enabled logging.
    loggingEnabled = False

    if loggingEnabled:
        import logging
        import sys
        moduleName = "lunar_calendar_utils"
        logger = logging.getLogger(moduleName)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        #formatStr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatStr = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() - %(message)s'
        formatter = logging.Formatter(formatStr)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    unittest.main()

##############################################################################

