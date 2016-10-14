
# For logging.
import logging
import logging.config

from functools import lru_cache

import math
import datetime
import copy

import pytz

from util import Util
from ephemeris import PlanetaryInfo
from ephemeris import Ephemeris
from ephemeris_utils import EphemerisUtils

class LunarDate:
    """
    Representation of a lunar date.

    Terms and Definitions used:

    The first lunar month of a year is the first new moon before the
    solar Spring equinox.

    The year for a given lunar date is defined as the Gregorian calendar year
    which is active at the moment of the first lunar month of that year.

    The first month of a lunar year is lunar month 1,
    which begins at the moment of the first new moon before the
    solar Spring equinox.

    The month in a LunarDate has range of values: [1, 13]

    The day in a LunarDate for the moment of a new moon is 0.0
    The day in a LunarDate for the moment of a full moon is 15.0
    The day in a LunarDate has range of values: [0.0, 30)
    """

    # Logger object for this class.
    log = logging.getLogger("lunar_calendar_utils.LunarDate")

    def __init__(self, year, month, day):
        """Initializes the LunarDate with the given parameters.

        Arguments:

        year   - int value containing the lunar year as defined in the
                 class comments for class LunarDate.

        month  - int value containing the lunar month as defined in the
                 class comments for class LunarDate.

        day    - float value containing the lunar day as defined in the
                 class comments for class LunarDate.
        """

        # Validate constructor arguments.
        if year == None:
            raise ValueError("'year' argument may not be None")
        elif not isinstance(year, int):
            raise ValueError("'year' argument must be of type int")

        if month == None:
            raise ValueError("'month' argument may not be None")
        elif not isinstance(month, int):
            raise ValueError("'month' argument must be of type int")
        elif month < 1 or month > 13:
            raise ValueError("'month' argument is out of range [1, 13]")

        if day == None:
            raise ValueError("'day' argument may not be None")
        elif not (isinstance(day, int) or isinstance(day, float)):
            raise ValueError("'day' argument must be of type int or type float")
        elif day < 0.0 or day >= 30:
            raise ValueError("'day' argument is out of range [0.0, 30)")

        if month == 13 and not LunarDate.isLunarLeapYear(year):
            errStr = "Invalid LunarDate: " + \
              "'month' argument cannot be 13 in a year that " + \
                "is not a lunar leap year.  " + \
                "Values were: (year={}, month={}, day={})".\
                format(year, month, day)
            raise ValueError(errStr)

        # All arguments are valid, so store the values in the object.
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    @lru_cache(maxsize=2048)
    def isLunarLeapYear(lunarYear):
        """
        Returns True if the given lunar calendar year has 13 months
        (i.e. it is a lunar leap year), otherwise False is returned.

        Arguments:
        lunarYear - int value representing the lunar year to check.
        """

        if lunarYear == None:
            raise ValueError("'lunarYear' argument may not be None")
        elif not isinstance(lunarYear, int):
            raise ValueError("'lunarYear' argument must be of type int")

        # Algorithm here is as follows:
        # 1) Get the Nisan 1 date for the year in question.
        # 2) Get the Nisan 1 date for the year following.
        # 3) Find the difference in number of calendar days between the two.
        # 4) If the difference in number of calendar days is closer to
        #    13 lunations, then True is returned.  Otherwise False is returned.

        springEquinoxSearchStartDate = \
            datetime.datetime(year=lunarYear,
                              month=3,
                              day=18,
                              hour=12,
                              minute=0,
                              second=0,
                              tzinfo=pytz.utc)
        springEquinoxSearchEndDate = \
            datetime.datetime(year=lunarYear + 1,
                              month=3,
                              day=25,
                              hour=12,
                              minute=0,
                              second=0,
                              tzinfo=pytz.utc)

        # Get the Spring Equinox dates.  This method call should return 2 datetimes.
        springEquinoxDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
                springEquinoxSearchStartDate,
                springEquinoxSearchEndDate,
                "Sun",
                "geocentric",
                "tropical",
                0,
                maxErrorTd=datetime.timedelta(seconds=1))

        nisan1Dts = []

        for springEquinoxDt in springEquinoxDts:
            newMoonSearchStartDt = springEquinoxDt - datetime.timedelta(days=35)
            newMoonSearchEndDt = springEquinoxDt

            if LunarDate.log.isEnabledFor(logging.DEBUG):
                LunarDate.log.debug("Searching for new moons between " +
                    Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                    Ephemeris.datetimeToStr(newMoonSearchEndDt))

            newMoonDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
                newMoonSearchStartDt,
                newMoonSearchEndDt,
                "MoSu",
                "geocentric",
                "tropical",
                0,
                maxErrorTd=datetime.timedelta(seconds=1))

            if LunarDate.log.isEnabledFor(logging.DEBUG):
                LunarDate.log.debug("Got the following timestamps for G.MoSu crossing "
                    + "0 degrees between the given start and end timestamps for "
                    + "this year: ")
                for newMoonDt in newMoonDts:
                    LunarDate.log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

            if len(newMoonDts) == 0:
                errMsg = \
                    "Did not find any new moons in the time period specified: " + \
                    "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) + \
                    ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt)
                LunarDate.log.error(errMsg)
                raise AssertionError(errMsg)
            elif len(newMoonDts) > 2:
                errMsg = \
                    "Found too many new moons in the time period specified: " + \
                    "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) + \
                    ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt)
                LunarDate.log.error(errMsg)
                raise AssertionError(errMsg)
            else:
                # Append the latest timestamp.
                newMoonDt = newMoonDts[-1]
                nisan1Dts.append(newMoonDt)

        if len(nisan1Dts) != 2:
            errMsg = "Did not find the expected number of new moons!"
            LunarDate.log.error(errMsg)
            raise AssertionError(errMsg)
        if nisan1Dts[-1] < nisan1Dts[-2]:
            errMsg = "Datetimes for Nisan 1 are not ordered as expected!"
            LunarDate.log.error(errMsg)
            raise AssertionError(errMsg)

        # Calculate the time difference from Nisan 1 to Nisan 1.
        # This should be a positive timedelta.
        diffTimeDelta = nisan1Dts[-1] - nisan1Dts[-2]

        if LunarDate.log.isEnabledFor(logging.DEBUG):
            LunarDate.log.debug("diffTimeDelta == {}".format(diffTimeDelta))

        if diffTimeDelta.days > 370:
            # 13 lunar months.
            return True
        else:
            # 12 lunar months.
            return False

    def __lt__(self, other):
        """
        Returns True if LunarDate self is earlier in time than LunarDate other,
        otherwise False is returned.
        """

        if not isinstance(other, LunarDate):
            raise ValueError("'other' argument must be of type LunarDate")

        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        else:
            if self.month < other.month:
                return True
            elif self.month > other.month:
                return False
            else:
                if self.day < other.day:
                    return True
                elif self.day > other.day:
                    return False
                else:
                    # Both LunarDate objects have equal year, month and day.
                    return False

    def __le__(self, other):
        """
        Returns True if any one of the following is True:
          - LunarDate self is earlier in time than LunarDate other.
          - LunarDate self is equals (i.e. at the same time as) LunarDate other.

        Otherwise False is returned.
        """

        if not isinstance(other, LunarDate):
            raise ValueError("'other' argument must be of type LunarDate")

        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        else:
            if self.month < other.month:
                return True
            elif self.month > other.month:
                return False
            else:
                if self.day < other.day:
                    return True
                elif self.day > other.day:
                    return False
                else:
                    # Both LunarDate objects have equal year, month and day.
                    return True

    def __eq__(self, other):
        """
        Returns True if LunarDate self is equal in time to LunarDate other,
        otherwise False is returned.
        """

        if not isinstance(other, LunarDate):
            raise ValueError("'other' argument must be of type LunarDate")

        if self.year == other.year and \
            self.month == other.month and \
            self.day == other.day:

            return True
        else:
            return False

    def __ne__(self, other):
        """
        Returns True if LunarDate self is not equal in time to LunarDate other,
        otherwise False is returned.
        """

        if not isinstance(other, LunarDate):
            raise ValueError("'other' argument must be of type LunarDate")

        if self.year != other.year or \
            self.month != other.month or \
            self.day != other.day:

            return True
        else:
            return False

    def __gt__(self, other):
        """
        Returns True if LunarDate self is later in time than LunarDate other,
        otherwise False is returned.
        """

        if not isinstance(other, LunarDate):
            raise ValueError("'other' argument must be of type LunarDate")

        if self.year < other.year:
            return False
        elif self.year > other.year:
            return True
        else:
            if self.month < other.month:
                return False
            elif self.month > other.month:
                return True
            else:
                if self.day < other.day:
                    return False
                elif self.day > other.day:
                    return True
                else:
                    # Both LunarDate objects have equal year, month and day.
                    return False

    def __ge__(self, other):
        """
        Returns True if any one of the following is True:
          - LunarDate self is later in time than LunarDate other.
          - LunarDate self is equals (i.e. at the same time as) LunarDate other.

        Otherwise False is returned.
        """

        if not isinstance(other, LunarDate):
            raise ValueError("'other' argument must be of type LunarDate")

        if self.year < other.year:
            return False
        elif self.year > other.year:
            return True
        else:
            if self.month < other.month:
                return False
            elif self.month > other.month:
                return True
            else:
                if self.day < other.day:
                    return False
                elif self.day > other.day:
                    return True
                else:
                    # Both LunarDate objects have equal year, month and day.
                    return True

    def __add__(self, lunarTimeDelta):
        """
        This method takes the given LunarTimeDelta and adds it to LunarDate self,
        returning the resulting LunarDate.

        WARNING / Caveats! :

        This method has scenarios which will not yield intuitive/correct results.
        For example, the following addition would give the result:

           LunarDate(2017, 13, 5) + LunarTimeDelta(years=1, months=0, days=0)
             = LunarDate(2019, 1, 5)

        according to this method's algorithm.

        Normally, adding a lunar year should not cause the lunar year of the
        lunar date to move 2 years.  But the technically correct result
        would be an invalid lunar date because resulting year of just
        adding 1 lunar year has no leap month 13.  I considered perhaps
        returning None in this situation, but it is really impossible to
        work out all the scenarios where this could happen for all kinds
        of LunarTimeDelta that could be possibly added to a LunarDate.
        """

        if not isinstance(lunarTimeDelta, LunarTimeDelta):
            errStr = "'lunarTimeDelta' argument must be of type LunarTimeDelta"
            raise ValueError(errStr)

        year = self.year + lunarTimeDelta.years
        month = self.month + lunarTimeDelta.months
        day = self.day + lunarTimeDelta.days

        # Normalize days and adjust the months as needed.
        while day >= 30:
            day -= 30
            month += 1
        while day <= 0:
            day += 30
            month -= 1

        # Normalize months, based on whether it is a leap year.
        while ((LunarDate.isLunarLeapYear(year) and month > 13) or \
               (not LunarDate.isLunarLeapYear(year) and month > 12)):

            if LunarDate.isLunarLeapYear(year) and month > 13:
                month -= 13
                year += 1
            elif not LunarDate.isLunarLeapYear(year) and month > 12:
                month -= 12
                year += 1

        while month < 1:
            if LunarDate.isLunarLeapYear(year - 1) and month < 1:
                month += 13
                year -= 1
            elif not LunarDate.isLunarLeapYear(year - 1) and month < 1:
                month += 12
                year -= 1

        rv = LunarDate(year, month, day)

        if LunarDate.log.isEnabledFor(logging.DEBUG):
            LunarDate.log.debug("{} + {} = {}".format(self, lunarTimeDelta, rv))

        return rv

    def __sub__(self, other):
        """
        This method takes the given LunarTimeDelta and subtracts it from LunarDate self,
        returning the resulting LunarDate.
        """

        rv = None

        if isinstance(other, LunarTimeDelta):
            invertedLunarTimeDelta = \
                LunarTimeDelta(other.years * -1,
                               other.months * -1,
                               other.days * -1)

            rv = self + invertedLunarTimeDelta

            if LunarDate.log.isEnabledFor(logging.DEBUG):
                LunarDate.log.debug("{} - {} = {}".format(self, other, rv))

        elif isinstance(other, LunarDate):
            years = self.year - other.year
            months = self.month - other.month
            days = self.day - other.day

            # Normalize days and adjust the months as needed.
            while days >= 30:
                days -= 30
                months += 1
            while days <= -30:
                days += 30
                months -= 1

            rv = LunarTimeDelta(years, months, days)

            if LunarDate.log.isEnabledFor(logging.DEBUG):
                LunarDate.log.debug("{} - {} = {}".format(self, other, rv))

        else:
            errStr = "'lunarTimeDelta' argument must be of type LunarDate or type LunarTimeDelta"
            raise ValueError(errStr)

        return rv

    def __str__(self):
        """Returns a string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns a string representation of this object."""

        rv = "LunarDate(year={}, month={}, day={})".\
            format(self.year, self.month, self.day)

        return rv

class LunarTimeDelta:
    """
    Representation of a time difference specified in lunar measurements.

    When adding a LunarTimeDelta to a LunarDate, the years gets added first,
    then the months and then the days.

    Note:
    A lot of care must be taken if this class is used.
    The reason is that adding LunarTimeDeltas can yield unexpected results
    if operations are not done with care.

    For example:
      LunarTimeDelta(years=1, months=8, days=20) +
      LunarTimeDelta(years=1, months=9, days=15)
        = LunarTimeDelta(years=2, months=18, days=5)

    This class does not convert any amount of months into years!!!!!!!

    This is because lunars years can have either 12 lunar months or
    13 lunar months.

    Note also that LunarTimeDeltas cannot be compared to each other.
    Operations of >, <, <=, >=, etc. don't make sense since we must
    retain the years and months separately.

    For example, there is no clear way to evalulate an expression like this:

      LunarTimeDelta(years=2, months=1, days=20) <
      LunarTimeDelta(years=0, months=59, days=15)

    """

    # Logger object for this class.
    log = logging.getLogger("lunar_calendar_utils.LunarTimeDelta")

    def __init__(self, years=0, months=0, days=0):
        """Initializes the LunarDate with the given parameters.

        Arguments:

        years   - int value containing the amount of lunar years.

        months  - int or float value containing the amount of
                  lunar months.
                  One lunar month is defined as 360 degrees traversal of
                  (Geocentric Moon - Geocentric Sun).

        days    - int or float value containing the amount of
                  lunar days.
                  One lunar day is defined as 1 / 30th of a lunar month.

        The LunarTimeDelta's internal representation normalizes
        the number of days to be in the range: (-30, 0] or [0, 30), adjusting
        the lunar months as necessary to be the same equivalent value.
        """

        # Validate constructor arguments.
        if years == None:
            raise ValueError("'years' argument must not be None")
        elif not isinstance(years, int):
            raise ValueError("'years' argument must be of type int")

        if months == None:
            raise ValueError("'months' argument may not be None")
        elif not (isinstance(months, int) or isinstance(months, float)):
            raise ValueError("'months' argument must be of type int or type float")

        if days == None:
            raise ValueError("'days' argument may not be None")
        elif not (isinstance(days, int) or isinstance(days, float)):
            raise ValueError("'days' argument must be of type int or type float")

        self.years = years
        self.months = months
        self.days = days

        # Normalize days and adjust the months as needed.
        while self.days >= 30:
            self.days -= 30
            self.months += 1
        while self.days <= -30:
            self.days += 30
            self.months -= 1

        if LunarTimeDelta.log.isEnabledFor(logging.DEBUG):
            LunarTimeDelta.log.debug("Final normalized values: {}".format(self.toString()))

    def __add__(self, other):
        """
        This method takes the LunarTimeDelta other and adds it to
        LunarTimeDelta self, returning the resulting LunarTimeDelta.
        """

        if not isinstance(other, LunarTimeDelta):
            errStr = "'other' argument must be of type LunarTimeDelta"
            LunarTimeDelta.log.error(errStr)
            raise ValueError(errStr)

        totalYears = self.years + other.years
        totalMonths = self.months + other.months
        totalDays = self.days + other.days

        while totalDays >= 30:
            totalDays -= 30
            totalMonths += 1
        while totalDays <= -30:
            totalDays += 30
            totalMonths -= 1

        return LunarTimeDelta(years=totalYears, months=totalMonths, days=totalDays)

    def __sub__(self, other):
        """
        This method takes the LunarTimeDelta other and subtracts it from
        LunarTimeDelta self, returning the resulting LunarTimeDelta.
        """

        if not isinstance(other, LunarTimeDelta):
            errStr = "'other' argument must be of type LunarTimeDelta"
            LunarTimeDelta.log.error(errStr)
            raise ValueError(errStr)

        totalYears = self.years - other.years
        totalMonths = self.months - other.months
        totalDays = self.days - other.days

        while totalDays >= 30:
            totalDays -= 30
            totalMonths += 1
        while totalDays <= -30:
            totalDays += 30
            totalMonths -= 1

        return LunarTimeDelta(years=totalYears, months=totalMonths, days=totalDays)

    def __eq__(self, other):
        """
        Returns True if LunarTimeDelta self is equal to
        LunarTimeDelta other, otherwise False is returned.
        """

        if not isinstance(other, LunarTimeDelta):
            raise ValueError("'other' argument must be of type LunarTimeDelta")

        if self.years == other.years and \
            self.months == other.months and \
            self.days == other.days:

            return True
        else:
            return False

    def __ne__(self, other):
        """
        Returns True if LunarTimeDelta self is not equal in time to
        LunarTimeDelta other, otherwise False is returned.
        """

        if not isinstance(other, LunarTimeDelta):
            raise ValueError("'other' argument must be of type LunarTimeDelta")

        if self.years != other.years or \
            self.months != other.months or \
            self.days != other.days:

            return True
        else:
            return False

    def __str__(self):
        """Returns a string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns a string representation of this object."""

        rv = "LunarTimeDelta(years={}, months={}, days={})".\
            format(self.years, self.months, self.days)

        return rv

class LunarCalendarUtils:
    """
    Contains some methods to help work between Gregorian calendar dates and
    astronomical lunar calendar dates.

    For definitions of the terms used (e.g. 'year', 'month', 'day', etc.)
    relative to lunar dates, please see the class comment for
    the LunarDate class.
    """

    # Logger object for this class.
    log = logging.getLogger("lunar_calendar_utils.LunarCalendarUtils")

    @lru_cache(maxsize=4194304)
    @staticmethod
    def datetimeToLunarDate(dt):
        """
        Converts the given datetime.datetime to a LunarDate object.

        Returns:
        LunarDate object representing the same moment in time as the
        given datetime.datetime object.
        """

        if dt == None:
            errMsg = "Input 'dt' must not be None."
            LunarCalendarUtils.log.error(errMsg)
            raise ValueError(errMsg)

        if dt.tzinfo == None:
            errMsg = "Input 'dt' must have a tzinfo specified.  " + \
                "dt was: {}".format(Ephemeris.datetimeToStr(dt))
            LunarCalendarUtils.log.error(errMsg)
            raise ValueError(errMsg)

        # Determine what lunar year 'dt' falls under.

        # Get the Nisan 1 timestamp in the form of a datetime
        # for the same datetime.year and the year before,
        # then test those dates with datetime 'dt'.
        nisan1DtA = \
            LunarCalendarUtils.getNisan1DatetimeForYear(dt.year - 1, dt.tzinfo)
        nisan1DtB = \
            LunarCalendarUtils.getNisan1DatetimeForYear(dt.year, dt.tzinfo)
        nisan1Dt = None

        if dt >= nisan1DtB:
            nisan1Dt = nisan1DtB
        else:
            nisan1Dt = nisan1DtA

        lunarYear = nisan1Dt.year
        if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
            LunarCalendarUtils.log.debug("lunarYear == {}".format(lunarYear))

        isLeapYear = LunarDate.isLunarLeapYear(lunarYear)
        if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
            LunarCalendarUtils.log.debug("isLeapYear == {}".format(isLeapYear))

        numMonths = None
        if isLeapYear:
            numMonths = 13
        else:
            numMonths = 12

        # Determine what lunar month 'dt' falls under.

        # Use an approximation of the lunar month to determine
        # what lunar month to begin testing from.
        diffTd = dt - nisan1Dt

        # Divide by 29.535, which is the average lunation
        # amount of days.
        startingMonth = math.floor(diffTd.days / 29.535)
        if startingMonth < 1:
            startingMonth = 1

        lunarMonth = None
        for i in range(startingMonth, numMonths + 1):
            if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
                LunarCalendarUtils.log.debug("i == {}".format(i))

            testLunarDate = LunarDate(nisan1Dt.year, i, 0)
            testDt = LunarCalendarUtils.lunarDateToDatetime(testLunarDate, dt.tzinfo)

            if dt > testDt:
               lunarMonth = i
            else:
                break

        LunarCalendarUtils.log.debug("lunarMonth == {}".format(lunarMonth))

        # Determine what lunar day 'dt' falls under.
        pi = Ephemeris.getPlanetaryInfo("MoSu", dt)
        longitude = pi.geocentric['tropical']['longitude']
        lunarDay = longitude / 12.0
        LunarCalendarUtils.log.debug("lunarDay == {}".format(lunarDay))

        rv = LunarDate(lunarYear, lunarMonth, lunarDay)
        LunarCalendarUtils.log.debug("rv == {}".format(rv))

        return rv

    @staticmethod
    @lru_cache(maxsize=8192)
    def getNisan1DatetimeForYear(year, tzInfo=pytz.utc):
        """Returns the datetime.datetime for the timestamp of
        the first new moon before the Spring equinox of the
        gregorian year specified.

        Returns:
        datetime.datetime representing the Nisan 1 astronomical date.
        The timestamp will be in the timezone indicated by tzInfo,
        or UTC if none is specified.
        """

        # Validate arguments.
        if year == None:
            raise ValueError("'year' argument must not be None")
        elif not isinstance(year, int):
            raise ValueError("'year' argument must be of type int")

        springEquinoxSearchStartDate = \
            datetime.datetime(year=year,
                              month=3,
                              day=18,
                              hour=12,
                              minute=0,
                              second=0,
                              tzinfo=pytz.utc)
        springEquinoxSearchEndDate = \
            datetime.datetime(year=year,
                              month=3,
                              day=25,
                              hour=12,
                              minute=0,
                              second=0,
                              tzinfo=pytz.utc)

        # Get the Spring Equinox date.  This method call should return 1 datetime.
        springEquinoxDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
                springEquinoxSearchStartDate,
                springEquinoxSearchEndDate,
                "Sun",
                "geocentric",
                "tropical",
                0,
                maxErrorTd=datetime.timedelta(seconds=1))

        nisan1Dts = []

        for springEquinoxDt in springEquinoxDts:
            newMoonSearchStartDt = springEquinoxDt - datetime.timedelta(days=35)
            newMoonSearchEndDt = springEquinoxDt

            if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
                LunarCalendarUtils.log.debug("Searching for new moons between " +
                    Ephemeris.datetimeToStr(newMoonSearchStartDt) + " and " +
                    Ephemeris.datetimeToStr(newMoonSearchEndDt))

            newMoonDts = EphemerisUtils.getPlanetCrossingLongitudeDegTimestamps(\
                newMoonSearchStartDt,
                newMoonSearchEndDt,
                "MoSu",
                "geocentric",
                "tropical",
                0,
                maxErrorTd=datetime.timedelta(seconds=1))

            if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
                LunarCalendarUtils.log.debug("Got the following timestamps for G.MoSu crossing "
                    + "0 degrees between the given start and end timestamps for "
                    + "this year: ")
                for newMoonDt in newMoonDts:
                    LunarCalendarUtils.log.debug("  " + Ephemeris.datetimeToDayStr(newMoonDt))

            if len(newMoonDts) == 0:
                errMsg = \
                    "Did not find any new moons in the time period specified: " + \
                    "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) + \
                    ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt)
                LunarCalendarUtils.log.error(errMsg)
                raise AssertionError(errMsg)
            elif len(newMoonDts) > 2:
                errMsg = \
                    "Found too many new moons in the time period specified: " + \
                    "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) + \
                    ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt)
                LunarCalendarUtils.log.error(errMsg)
                raise AssertionError(errMsg)
            else:
                # Append the latest timestamp.
                newMoonDt = newMoonDts[-1]
                nisan1Dts.append(newMoonDt)

        if len(nisan1Dts) != 1:
            errMsg = "Did not find the expected number of new moons!"
            LunarCalendarUtils.log.error(errMsg)
            raise AssertionError(errMsg)

        nisan1Dt = nisan1Dts[0]

        if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
            LunarCalendarUtils.log.debug("nisan1Dt == " + Ephemeris.datetimeToDayStr(nisan1Dt))

        # Convert to the timezone specified.
        rv = tzInfo.normalize(nisan1Dt.astimezone(tzInfo))

        if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
            LunarCalendarUtils.log.debug("rv == " + Ephemeris.datetimeToDayStr(rv))
            
        return rv

    @staticmethod
    def lunarDateToDatetime(lunarDate, tzInfo=pytz.utc):
        """
        Converts the given LunarDate object to a datetime.datetime.
        The returned datetime object is created
        with the timestamp in the timezone specified (or UTC by default if the
        argument is not specified).

        Returns:
        datetime.datetime object representing the same moment in time as the
        given LunarDate object.
        """

        # Algorithm here is as follows:
        # 1) Get the Nisan 1 date for the year in question.
        # 2) Get the degrees of G.MoSu that needs to be elapsed.
        # 3) Get the datetime of that many degrees of G.MoSu elapsed.
        # 4) Convert the datetime to the localized timezone for return.

        nisan1Dt = LunarCalendarUtils.getNisan1DatetimeForYear(lunarDate.year, tzInfo)

        desiredDegreesElapsed = ((lunarDate.month - 1) * 360) + (lunarDate.day * 12)

        # This is the desired datetime to return, but in UTC timezone.
        dtUtc = None

        # This is the desired datetime to return, but in the the tzInfo timezone.
        rv = None

        # For G.MoSu, if desiredDegreesElapsed is 0, then there's no
        # need to do the ephemeris calculation because the user is looking for
        # the Nisan 1 datetime, which we've already calculated.
        if desiredDegreesElapsed == 0.0:
            rv = nisan1Dt
        else:
            dts = EphemerisUtils.getDatetimesOfElapsedLongitudeDegrees(\
                "MoSu",
                "geocentric",
                "tropical",
                nisan1Dt,
                desiredDegreesElapsed,
                maxErrorTd=datetime.timedelta(seconds=1))

            if len(dts) != 1:
                errMsg = "Did not find the expected number of datetimes!"
                LunarCalendarUtils.log.error(errMsg)
                raise AssertionError(errMsg)

            dtUtc = dts[0]

            # Convert to the timezone specified.
            rv = tzInfo.normalize(dtUtc.astimezone(tzInfo))

        if LunarCalendarUtils.log.isEnabledFor(logging.DEBUG):
            if dtUtc != None:
                debugStr = "{} converted to UTC datetime is: {}".\
                    format(lunarDate, Ephemeris.datetimeToDayStr(dtUtc))
                LunarCalendarUtils.log.debug(debugStr)

            debugStr = "{} converted to localized datetime is: {}".\
                format(lunarDate, Ephemeris.datetimeToDayStr(rv))
            LunarCalendarUtils.log.debug(debugStr)

        return rv

    @staticmethod
    def isLunarLeapYear(lunarYear):
        """
        Returns True if the given lunar calendar year has 13 months
        (i.e. it is a lunar leap year), otherwise False is returned.

        Arguments:
        lunarYear - int value representing the lunar year to check.
        """

        return LunarDate.isLunarLeapYear(lunarYear)

##############################################################################

