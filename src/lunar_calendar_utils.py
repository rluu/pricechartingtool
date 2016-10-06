
# For logging.
import logging
import logging.config

from functools import lru_cache

import inspect
import datetime
import copy

import pytz

from util import Util
from ephemeris import PlanetaryInfo
from ephemeris import Ephemeris

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

        springEquinoxSearchStartDate = datetime.datetime(lunarYear, 3, 18, 12, 0, 0, tzInfo=pytz.utc)
        springEquinoxSearchEndDate = datetime.datetime(lunarYear + 1, 3, 25, 12, 0, 0, tzInfo=pytz.utc)

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
                LunarDate.log.error("Did not find any new moons in the time period specified: " +
                    "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) +
                    ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt))
            elif len(newMoonDts) > 2:
                LunarDate.log.error("Found too many new moons in the time period specified: " +
                    "newMoonSearchStartDt=" + Ephemeris.datetimeToStr(newMoonSearchStartDt) +
                    ", newMoonSearchEndDt="+ Ephemeris.datetimeToStr(newMoonSearchEndDt))
            else:
                # Append the latest timestamp.
                newMoonDt = newMoonDts[-1]
                nisan1Dts.append(newMoonDt)

        if len(nisan1Dts != 2):
            LunarDate.log.error("Did not find the expected number of new moons!")
        if nisan1Dts[-1] < nisan1Dts[-2]:
            LunarDate.log.error("Datetimes for Nisan 1 are not ordered as expected!")

        # Calculate the time difference from Nisan 1 to Nisan 1.
        # This should be a positive timedelta.
        diffTimeDelta = nisan1Dts[-1] - nisan1Dts[-2]

        if LunarDate.log.isEnabledFor(logging.DEBUG):
            LunarDate.log.debug("diffTimeDelta == " + diffTimeDelta)
            
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
        """

        if not isinstance(lunarTimeDelta, LunarTimeDelta):
            errStr = "'lunarTimeDelta' argument must be of type LunarTimeDelta"
            raise ValueError(errStr)
        
        # TODO_rluu: Write code here.

        # TODO_rluu: Make sure to handle case to return if lunar date in the 13th month + lunar year,
        # then should None be returned?
        pass
        
    def __sub__(self, lunarTimeDelta):
        """
        This method takes the given LunarTimeDelta and subtracts it from LunarDate self, 
        returning the resulting LunarDate.
        """
        
        if not isinstance(lunarTimeDelta, LunarTimeDelta):
            errStr = "'lunarTimeDelta' argument must be of type LunarTimeDelta"
            raise ValueError(errStr)

        # TODO_rluu: Write code here.
        pass
        
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
        elif not (isinstance(month, int) or isinstance(month, float)):
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
            LunarTimeDelta.log.debug(errStr)
            raise ValueError(errStr)

        totalYears = self.years + other.years
        totalMonths = self.months + other.months
        totalDays = self.days + other.days

        while totalDays >= 30:
            totalDays -= 30
            totalMonths += 1
        while totalDays <= 30:
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
            LunarTimeDelta.log.debug(errStr)
            raise ValueError(errStr)

        totalYears = self.years - other.years
        totalMonths = self.months - other.months
        totalDays = self.days - other.days

        while totalDays >= 30:
            totalDays -= 30
            totalMonths += 1
        while totalDays <= 30:
            totalDays += 30
            totalMonths -= 1

        return LunarTimeDelta(years=totalYears, months=totalMonths, days=totalDays)
        
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
    
    @staticmethod
    def datetimeToLunarDate(dt):
        """
        Converts the given datetime.datetime to a LunarDate object.

        Returns:
        LunarDate object representing the same moment in time as the 
        given datetime.datetime object.
        """
        # TODO_rluu: Write code here.
        pass

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
        # TODO_rluu: Write code here.
        pass


    @staticmethod
    def isLunarLeapYear(lunarYear):
        """
        Returns True if the given lunar calendar year has 13 months 
        (i.e. it is a lunar leap year), otherwise False is returned.

        Arguments:
        lunarYear - int value representing the lunar year to check.
        """

        return LunarDate.isLunarLeapYear(lunarYear)

    @staticmethod
    def isSolarEclipse(lunarDate):
        """
        Returns True if the given LunarDate is taking place during a
        Solar eclipse, otherwise False is returned.

        Arguments:
        lunarDate - LunarDate object holding the timestamp to check.
        """
        # TODO_rluu: Write code here.
        pass

    @staticmethod
    def isLunarEclipse(lunarDate):
        """
        Returns True if the given LunarDate is taking place during a
        Lunar eclipse, otherwise False is returned.

        Arguments:
        lunarDate - LunarDate object holding the timestamp to check.
        """
        # TODO_rluu: Write code here.
        pass

    
    
