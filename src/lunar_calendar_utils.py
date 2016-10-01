
# For logging.
import logging
import logging.config

from functools import lru_cache
from functools import total_ordering

import inspect
import datetime
import copy

import pytz

from util import Util
from ephemeris import PlanetaryInfo
from ephemeris import Ephemeris

@total_ordering
class LunarDate:
    """
    This class represents a lunar date.
    
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

        if year == None:
            raise ValueError("'year' argument may not be None")
        elif not isinstance(year, int):
            raise ValueError("'year' argument must be of type int")

        # TODO_rluu: Write code here.
        pass
        
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
        
    def __add__(self, lunarTimeDelta):
        """
        # TODO_rluu: Write comment here.
        """

        if not isinstance(lunarTimeDelta, LunarTimeDelta):
            errStr = "'lunarTimeDelta' argument must be of type LunarTimeDelta"
            raise ValueError(errStr)

        # TODO_rluu: Write code here.
        pass
        
    def __sub__(self, lunarTimeDelta):
        """
        # TODO_rluu: Write comment here.
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

        rv = "[year={}, month={}, day={}]".\
            format(self.year, self.month, self.day)

        return rv

class LunarTimeDelta:
    # TODO_rluu: Write code here.
    pass

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

    
    
