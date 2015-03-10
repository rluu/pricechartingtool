
# For line separator.
import os

# For logging.
import logging

# For generation of unique PriceBarChartArtifact identifiers.
import uuid

# For inspect.stack().
import inspect

# For timestamps and timezone information.
import datetime
import pytz

# For pickling PyQt types.
from PyQt4.QtGui import QTransform
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPointF
from PyQt4.QtCore import QLineF
from PyQt4.QtCore import QRectF

# For getting QSettings values.
from PyQt4.QtCore import QSettings

# For datetime.datetime to str conversion.
from ephemeris import Ephemeris

# For QSettings keys.
from settings import SettingsKeys

class Util:
    """Contains some generic static functions that may be helpful."""

    @staticmethod
    def monthNumberToAbbrev(monthNumber):
        """Converts the given month number to a 3-letter abbreviation
        for the month.  The monthNumber is 1-based, so 1 will convert
        to 'Jan'.

        Arguments:
        monthNumber - int for the month number, where 1 represents January.

        Returns:
        str value holding the month abbreviation (e.g. 'Jan').  If the
                  input is invalid, then None is returned.
        
        """

        rv = None

        if monthNumber == 1:
            rv = "Jan"
        elif monthNumber == 2:
            rv = "Feb"
        elif monthNumber == 3:
            rv = "Mar"
        elif monthNumber == 4:
            rv = "Apr"
        elif monthNumber == 5:
            rv = "May"
        elif monthNumber == 6:
            rv = "Jun"
        elif monthNumber == 7:
            rv = "Jul"
        elif monthNumber == 8:
            rv = "Aug"
        elif monthNumber == 9:
            rv = "Sep"
        elif monthNumber == 10:
            rv = "Oct"
        elif monthNumber == 11:
            rv = "Nov"
        elif monthNumber == 12:
            rv = "Dec"
        else:
            rv = None

        return rv
            
    @staticmethod
    def monthAbbrevToNumber(monthAbbrev):
        """Converts the given month 3-letter abbreviation to the month
        number.  The monthNumber is 1-based, so 'Jan' will convert to 1.

        Arguments:
        monthAbbrev - str holding the abbreviation of the month.

        Returns:
        int value holding the month number.  The number is 1-based,
        ie. 1 maps to January.  input is invalid, then None is
        returned.
        """

        rv = None

        ma = monthAbbrev.lower()

        if ma == "jan":
            rv = 1
        elif ma == "feb":
            rv = 2
        elif ma == "mar":
            rv = 3
        elif ma == "apr":
            rv = 4
        elif ma == "may":
            rv = 5
        elif ma == "jun":
            rv = 6
        elif ma == "jul":
            rv = 7
        elif ma == "aug":
            rv = 8
        elif ma == "sep":
            rv = 9
        elif ma == "oct":
            rv = 10
        elif ma == "nov":
            rv = 11
        elif ma == "dec":
            rv = 12
        else:
            rv = None

        return rv
            
    @staticmethod
    def absTd(timedelta):
        """Returns the absolute value of this datetime.timedelta object.
        This is to ensure timedeltas are positive for comparison purposes.
        """
        
        if timedelta < datetime.timedelta(0):
            return timedelta * -1
        else:
            return timedelta
        
    @staticmethod
    def fuzzyIsEqual(f1, f2, maxDiff=0.00000001):
        """Fuzzy test for floating point values being equal.
        
        Arguments:
        f1 - float value to test against variable f2.
        f2 - float value to test against variable f1.
        maxDiff - float value for the maximum difference before
                  f1 and f2 are not considered equal.

        Returns:
        bool value - True if the values are within maxDiff
                     from each other, False otherwise.
        """

        if abs(f1 - f2) <= maxDiff:
            return True
        else:
            return False
    
    @staticmethod
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
    
    @staticmethod
    def qColorToStr(qcolor):
        """Returns a string formatting of a QColor object."""

        #return "QColor(r={},g={},b={},a={})".\
        #       format(qcolor.red(),
        #              qcolor.green(),
        #              qcolor.blue(),
        #              qcolor.alpha())
        
        #return "QColor(h={},s={},v={},a={})".\
        #       format(qcolor.hue(),
        #              qcolor.saturation(),
        #              qcolor.value(),
        #              qcolor.alpha())
    
        return "QColor(h={},s={},v={},r={},g={},b={},a={})".\
               format(qcolor.hue(),
                      qcolor.saturation(),
                      qcolor.value(),
                      qcolor.red(),
                      qcolor.green(),
                      qcolor.blue(),
                      qcolor.alpha())

    @staticmethod
    def objToString(obj):
        """Returns a string representing the given object's contents."""
        
        rv = "["
        rv += "{}, ".format(type(obj))

        for attr in dir(obj):
            # Print if the attribute:
            #   - Doesn't start with '__'.
            #   - Isn't a Logger
            #   - Isn't callable.
            if not attr.startswith('__') and \
                   not isinstance(getattr(obj, attr), logging.Logger) and \
                   not hasattr(getattr(obj, attr), '__call__'):
                
                attrObj = getattr(obj, attr)

                # Do special handling for QColor objects and lists.
                if isinstance(attrObj, QColor):
                    rv += "{}={}, ".\
                          format(attr, Util.qColorToStr(attrObj))
                elif isinstance(attrObj, list):
                    rv += "{}=[".format(attr)
                    for item in attrObj:
                        rv += "{}, ".format(item)
                    rv = rv.rstrip(', ')
                    rv += "], "
                else:
                    # Normal object that is not a QColor and not a list.
                    rv += "{}={}, ".format(attr, attrObj)

        if rv.endswith(", "):
            rv = rv[:-2]
        rv += "]"

        return rv
        
class BirthInfo:
    """Contains data related to the birth of an entity or person.
    See the documentation for the '__init__()' function to see what
    data it holds.
    """

    def __init__(self,
                 year=2,
                 month=1,
                 day=1,
                 calendar='Gregorian',
                 hour=0,
                 minute=0,
                 second=0,
                 locationName="",
                 countryName="",
                 longitudeDegrees=0,
                 latitudeDegrees=0,
                 elevation=0,
                 timezoneName='UTC',
                 timezoneOffsetAbbreviation='UTC',
                 timezoneOffsetValueStr='+0000',
                 timezoneManualEntryHours=0,
                 timezoneManualEntryMinutes=0,
                 timezoneManualEntryEastWestComboBoxValue='W',
                 timeOffsetAutodetectedRadioButtonState=True,
                 timeOffsetManualEntryRadioButtonState=False,
                 timeOffsetLMTRadioButtonState=False):
        """Initializes the member variables to the values specified
        as arguments.

        Arguments:

        year             - int value for the birth year.
        month            - int value for the birth month.
        day              - int value for the birth day.
        calendar         - str value for the calendar system used.  
                           Can be 'Gregorian' or 'Julian'.
        hour             - int value for the birth hour.
        minute           - int value for the birth minute.
        second           - int value for the birth second.
        locationName     - str value for the birth location (city, etc.).
        countryName      - str value containing country name.
        longitudeDegrees - float value for the geographical longitude 
                           location of birth.  Positive longitudes refer
                           to East, and negative longitudes refer to West.
        latitudeDegrees  - float value for the geographical latitude 
                           location of birth.  Positive latitudes refer to
                           North, and negative latitudes refer to South.
        elevation        - int value for the birth location elevation 
                           in meters.
        timezoneName     - str value holding the name of the timezone.  
                           This is a string like "US/Eastern" or "Asia/Tokyo".
        timezoneOffsetAbbreviation 
                         - str value holding the abbreviation for the time 
                           offset used.  This is a string like "EST" or "EDT".
        timezoneOffsetValueStr 
                         - str value for the time offset.  It is a string 
                           in the defined format like "+0500" or "-0200".
        timezoneManualEntryHours 
                         - int value for the manual time offset 'hours' value.
        timezoneManualEntryMinutes 
                         - int value for the manual time offset 
                           'minutes' value.
        timezoneManualEntryEastWestComboBoxValue 
                         - str value for whether the manual time offset 
                           spinbox is west of UTC or east of UTC.  
                           Valid values for this are 'W' and 'E'.
        timeOffsetAutodetectedRadioButtonState 
                         - bool value for whether or not the radio button 
                           for autodetected time offset is checked.
        timeOffsetManualEntryRadioButtonState 
                         - bool value for whether or not the radio button 
                           for manual entry time offset is checked.
        timeOffsetLMTRadioButtonState 
                         - bool value for whether or not the radio button 
                           for local mean time is checked.
        """

        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = logging.getLogger("data_objects.BirthInfo")

        # Store values.
        self.year = year
        self.month = month
        self.day = day
        self.calendar = calendar
        self.hour = hour
        self.minute = minute
        self.second = second
        self.locationName = locationName
        self.countryName = countryName
        self.longitudeDegrees = longitudeDegrees
        self.latitudeDegrees = latitudeDegrees
        self.elevation = elevation
        self.timezoneName = timezoneName
        self.timezoneOffsetAbbreviation = timezoneOffsetAbbreviation
        self.timezoneOffsetValueStr = timezoneOffsetValueStr
        self.timezoneManualEntryHours = timezoneManualEntryHours
        self.timezoneManualEntryMinutes = timezoneManualEntryMinutes
        self.timezoneManualEntryEastWestComboBoxValue = \
                timezoneManualEntryEastWestComboBoxValue
        self.timeOffsetAutodetectedRadioButtonState = \
                timeOffsetAutodetectedRadioButtonState
        self.timeOffsetManualEntryRadioButtonState = \
                timeOffsetManualEntryRadioButtonState
        self.timeOffsetLMTRadioButtonState = \
                timeOffsetLMTRadioButtonState

        # Check inputs.
        # Only one of the following flags should be True,
        # and they should not all be False.
        #
        #     timeOffsetAutodetectedRadioButtonState
        #     timeOffsetManualEntryRadioButtonState
        #     timeOffsetLMTRadioButtonState
        trueCount = 0
        if timeOffsetAutodetectedRadioButtonState == True:
            trueCount += 1
        if timeOffsetManualEntryRadioButtonState == True:
            trueCount += 1
        if timeOffsetLMTRadioButtonState == True:
            trueCount += 1

        if trueCount == 0:
            # Log an error.  One of the three options should have been chosen.
            errStr = "Invalid arguments specified.  One of the " + \
                     "radio buttons should be checked."
            self.log.error(errStr)
            raise ValueError(errStr)
        elif trueCount > 1:
            # Log an error.  More than one can't be True.
            errStr = "Invalid arguments specified.  Only one of the " + \
                     "radio buttons can be checked."
            self.log.error(errStr)
            raise ValueError(errStr)

    def getBirthLocalizedDatetime(self):
        """Takes the date, time and timezone information in this
        object and attempts to convert it to a localized
        datetime.datetime to be returned.  There is no guarentee that
        the datetime.datetime to be returned is localized.

        If the 'self.timeOffsetAutodetectedRadioButtonState' flag is
        set, a localized datetime.datetime for the birth time will be
        returned.

        If the 'self.timeOffsetAutodetectedRadioButtonState' flag is
        NOT set (some other option was selected, like user-specified
        or LMT), then a UTC datetime.datetime for the birth time will
        be returned.

        Returns:
        datetime.datetime that represents the birth time.  Best effort
        is made to localize this datetime.
        """

        self.log.debug("Entered getBirthLocalizedDatetime()")

        # Return value.
        datetimeObj = None

        # Create a native datetime.datetime object first.
        nativeDatetimeObj = \
            datetime.datetime(self.year,
                              self.month,
                              self.day,
                              self.hour,
                              self.minute,
                              self.second)

        # See which timezone mode is specified.

        if self.timeOffsetAutodetectedRadioButtonState == True:
            self.log.debug("timeOffsetAutodetectedRadioButtonState == True")

            # Create a timezone object to be used.
            tzinfoObj = pytz.timezone(self.timezoneName)

            # Localize the datetime.datetime to the timezone specified.
            localizedDatetimeObj = tzinfoObj.localize(nativeDatetimeObj)

            # Set the datetime.datetime to the return value.
            datetimeObj = localizedDatetimeObj

            self.log.debug("datetimeObj == {}".\
                           format(Ephemeris.datetimeToStr(datetimeObj)))
            
        elif self.timeOffsetManualEntryRadioButtonState == True:
            self.log.debug("timeOffsetManualEntryRadioButtonState == True")
            
            # Localize the datetime.datetime as UTC.
            utcDatetimeObj = pytz.utc.localize(nativeDatetimeObj)
            self.log.debug("utcDatetimeObj == {}".\
                           format(Ephemeris.datetimeToStr(utcDatetimeObj)))
            
            # Add the offset.  We can do this type of arithmetic
            # because the datetime.datetime is now in UTC and there
            # are no daylight savings shifts to worry about.
            numSeconds = \
                (self.timezoneManualEntryHours * 60 * 60) + \
                (self.timezoneManualEntryMinutes * 60)

            if self.timezoneManualEntryEastWestComboBoxValue == 'E':
                numSeconds *= -1

            self.log.debug("numSeconds == {}".format(numSeconds))
            
            datetimeObj = \
                utcDatetimeObj + datetime.timedelta(seconds=numSeconds)
            self.log.debug("datetimeObj == {}".\
                           format(Ephemeris.datetimeToStr(datetimeObj)))
            
        elif self.timeOffsetLMTRadioButtonState == True:
            self.log.debug("timeOffsetLMTRadioButtonState == True")
            
            # For the LMT conversion to UTC, should I be
            # taking into account the axis tilt of the Earth (23.5
            # degrees) and the precession of the equinoxes for the
            # calculation of the time offset from UTC?

            # Perhaps that's the right way to do it, but I'm lazy
            # and will just do the technique advocated and used by
            # everyone else, which is a simple 4 minutes of time for
            # each 1 arc degree of longitude.


            # Localize the datetime.datetime as UTC.
            utcDatetimeObj = pytz.utc.localize(nativeDatetimeObj)
            self.log.debug("utcDatetimeObj == {}".\
                           format(Ephemeris.datetimeToStr(utcDatetimeObj)))
            
            # Use 4 minutes of time offset for each longitude degree away
            # from 0.
            timeShiftMinutes = self.longitudeDegrees * -4.0

            # Add the time delta and use that as the datetime.
            datetimeObj = \
                utcDatetimeObj + datetime.timedelta(minutes=timeShiftMinutes)
            self.log.debug("datetimeObj == {}".\
                           format(Ephemeris.datetimeToStr(datetimeObj)))
        else:
            # Log an error.  This should never happen since we checked
            # the inputs in __init__().
            self.log.warn("None of the known timezone offset options were set!")

        self.log.debug("Leaving getBirthLocalizedDatetime()")
        return datetimeObj
    
    def getBirthUtcDatetime(self):
        """Takes the date, time and timezone information in this 
        object and converts it to a UTC datetime.datetime object,
        such that it represents the same moment in time.
        This datetime.datetime object is returned.

        Returns:
        datetime.datetime that represents the birth time, in UTC time.
        """

        self.log.debug("Entered getBirthUtcDatetime()")

        # Return value.
        datetimeObj = None

        # Create a native datetime.datetime object first.
        nativeDatetimeObj = \
            datetime.datetime(self.year,
                              self.month,
                              self.day,
                              self.hour,
                              self.minute,
                              self.second)

        # See which timezone mode is specified.

        if self.timeOffsetAutodetectedRadioButtonState == True:
            # Create a timezone object to be used.
            timezone = pytz.timezone(self.timezoneName)

            # Localize the datetime.datetime to the timezone specified.
            localizedDatetimeObj = timezone.localize(nativeDatetimeObj)

            # Get the datetime.datetime in UTC.
            datetimeObj = localizedDatetimeObj.astimezone(pytz.utc)

        elif self.timeOffsetManualEntryRadioButtonState == True:
            # Localize the datetime.datetime as UTC.
            utcDatetimeObj = pytz.utc.localize(nativeDatetimeObj)

            # Add the offset.  We can do this type of arithmetic
            # because the datetime.datetime is now in UTC and there
            # are no daylight savings shifts to worry about.
            numSeconds = \
                (self.timezoneManualEntryHours * 60 * 60) + \
                (self.timezoneManualEntryMinutes * 60)

            if self.timezoneManualEntryEastWestComboBoxValue == 'E':
                numSeconds *= -1

            datetimeObj = \
                utcDatetimeObj + datetime.timedelta(seconds=numSeconds)
            
        elif self.timeOffsetLMTRadioButtonState == True:
            # For the LMT conversion to UTC, should I be
            # taking into account the axis tilt of the Earth (23.5
            # degrees) and the precession of the equinoxes for the
            # calculation of the time offset from UTC?

            # Perhaps that's the right way to do it, but I'm lazy
            # and will just do the technique advocated and used by
            # everyone else, which is a simple 4 minutes of time for
            # each 1 arc degree of longitude.


            # Localize the datetime.datetime as UTC.
            utcDatetimeObj = pytz.utc.localize(nativeDatetimeObj)

            # Use 4 minutes of time offset for each longitude degree away
            # from 0.
            timeShiftMinutes = self.longitudeDegrees * -4.0

            # Add the time delta and use that as the datetime.
            datetimeObj = \
                utcDatetimeObj + datetime.timedelta(minutes=timeShiftMinutes)
        else:
            # Log an error.  This should never happen since we checked
            # the inputs in __init__().
            self.log.warn("None of the radio buttons were checked!")

        self.log.debug("Leaving getBirthUtcDatetime()")
        return datetimeObj


    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv


    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.BirthInfo")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " + BirthInfo.__name__ +
                       " object of version {}".format(self.classVersion))




class PriceBar:
    """Contains price information for a single interval of time.  
    PriceBar can include the following information: 

    - timestamp as a datetime.datetime object.
    - open, high, low and close prices as floats
    - open interest as float
    - volume as float
    - tags as list of str

     
    The 'tags' is a list of strings to tag a bar as holding a certain
    attributes.  By convention, (initially anyways), it is used to indicate if
    the price bar is a high or low bar, and to what degree.  The convention is
    to use 'H' for a local high, 'HH' for a high over a larger range, 'HHH'
    etc.  In a similar manner, 'L', 'LL', 'LLL'  is used to indicate if it is a
    low.  If multiple tags apply to a pricebar then the tags ar separated by a
    space.
    """


    def __init__(self, timestamp, open=None, high=None, low=None, close=None, 
            oi=None, vol=None, tags=list()):
        """Initializes the PriceBar object.  

        Arguments are as follows:
        - open is the open price for the PriceBar, as a float
        - high is the high price for the PriceBar, as a float
        - low is the low price for the PriceBar, as a float
        - close is the close price for the PriceBar, as a float
        - oi is the open interest for the PriceBar, as a float
        - vol is the volume of trade for the PriceBar, as a float
        - timestamp is a datetime.datetime object
        - tags is a list of str.
        """

        self.log = logging.getLogger("data_objects.PriceBar")

        # Class version stored for pickling and unpickling.
        self.classVersion = 1

        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.oi = oi
        self.vol = vol
        self.tags = list(tags)

        # Do a bit of error checking.
        if high != None and low != None:
            if high < low:
                self.log.warn("Created a PriceBar with a high price lower " +
                              "than the low price.") 

    def midPrice(self):
        """Returns the average of the high and low.  I.e., ((high+low)/2.0)
        If high is None or low is None, then None is returned.
        """

        if self.high == None or self.low == None:
            return None
        else:
            return (self.high + self.low) / 2.0

    def addTag(self, tagToAdd):
        """Adds a given tag string to the tags for this PriceBar"""

        # Strip any leading or trailing whitespace
        tagToAdd = tagToAdd.strip()

        # The tag added must be non-empty and must not already exist in the
        # list.
        if tagToAdd != "" and tagToAdd not in self.tags:
            self.tags.append(tagToAdd)

    def hasTag(self, tagToCheck):
        """Returns True if the given tagToCheck is in the list of tags"""

        if tagToCheck in self.tags:
            return True
        else:
            return False

    def clearTags(self):
        """Clears all the tags associated with this PriceBar."""

        self.tags = []

    def removeTag(self, tagToRemove):
        """Removes a given tag string from the tags in this PriceBar."""

        while tagToRemove in self.tags:
            self.tags.remove(tagToRemove)


    def hasHigherHighThan(self, anotherPriceBar):
        """Returns True if this PriceBar has a higher high price than pricebar
        'anotherPriceBar'
        """

        if self.high == None:
            return False
        elif anotherPriceBar.high == None:
            return True
        else:
            if self.high > anotherPriceBar.high:
                return True
            else:
                return False

    def hasLowerLowThan(self, anotherPriceBar):
        """Returns True if this PriceBar has a lower low price than pricebar
        'anotherPriceBar'
        """

        if self.low == None:
            return False
        elif anotherPriceBar.low == None:
            return True
        else:
            if self.low < anotherPriceBar.low:
                return True
            else:
                return False


    def toString(self):
        """Returns the string representation of the PriceBar data"""

        rv = Util.objToString(self)
        
        return rv

    def __eq__(self, other):
        """Returns True if the two PriceBars are equal."""
        
        rv = True

        leftObj = self
        rightObj = other

        if rightObj == None:
            return False
        
        self.log.debug("leftObj: {}".format(leftObj.toString()))
        self.log.debug("rightObj: {}".format(rightObj.toString()))

        if leftObj.classVersion != rightObj.classVersion:
            self.log.debug("classVersion differs.")
            rv = False
        if leftObj.timestamp != rightObj.timestamp:
            self.log.debug("timestamp differs.")
            rv = False
        if leftObj.open != rightObj.open:
            self.log.debug("open differs.")
            rv = False
        if leftObj.high != rightObj.high:
            self.log.debug("high differs.")
            rv = False
        if leftObj.low != rightObj.low:
            self.log.debug("low differs.")
            rv = False
        if leftObj.close != rightObj.close:
            self.log.debug("close differs.")
            rv = False
        if leftObj.oi != rightObj.oi:
            self.log.debug("oi differs.")
            rv = False
        if leftObj.vol != rightObj.vol:
            self.log.debug("vol differs.")
            rv = False
            
        if len(leftObj.tags) != len(rightObj.tags):
            self.log.debug("len(tags) differs.")
            rv = False
        else:
            for i in range(len(leftObj.tags)):
                if leftObj.tags[i] != rightObj.tags[i]:
                    self.log.debug("tags differs.")
                    rv = False
                    break

        self.log.debug("__eq__() returning: {}".format(rv))
        
        return rv

    def __ne__(self, other):
        """Returns True if the PriceBars are not equal.
        Returns False otherwise."""

        return not self.__eq__(other)
    
    def __str__(self):
        """Returns the string representation of the PriceBar data"""

        return self.toString()

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.PriceBar")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " + PriceBar.__name__ +
                       " object of version {}".format(self.classVersion))

class Ratio:
    """Contains information about a ratio.  Includes the
    following information:

    - float value for the ratio.
    - description of the ratio (optional).
    - enabled flag.
    """

    def __init__(self,
                 ratio,
                 description="",
                 enabled=True,
                 mathDescription=""):
        """Initializes the PriceBar object.  

        Arguments are as follows:
        
        ratio - float value holding the ratio.
        description - str value holding the description of the ratio.
        enabled - bool flag indicating if the ratio is enabled or not.
        mathDescription - str value holding the mathematical
                          description of the ratio value.
        """

        # Class version stored for pickling and unpickling.
        self.classVersion = 2

        # Logger object.
        self.log = logging.getLogger("data_objects.Ratio")

        self.ratio = ratio
        self.description = description
        self.enabled = enabled
        self.mathDescription = mathDescription

    @staticmethod
    def getSupportedRetracementRatios():
        """Returns a list of Ratio objects that we plan on supporting
        in this application for TimeRetracementArtifacts and
        PriceRetracementArtifacts.

        For the source of these ratios below, see the following books:
        Geometry of Markets (beginning of the book before first numbered page).
        Geometry of Markets (Chapter 2, Page 9).
        Geometry of Markets (Chapter 6, Page 50).
        Geometry of Markets II (pg. 8)
        """

        # Return value.
        ratios = []

        # Append each of the Fibonnaci ratios.
        ratios.extend(Ratio.getSupportedFibRatios())

        # Append other ratios that are geometric or harmonic.

        ############
        
        # 0 / 1
        ratios.append(Ratio(ratio=0.0,
                            description="0.000",
                            enabled=True,
                            mathDescription="0 / 1"))

        # 1 / 8
        ratios.append(Ratio(ratio=0.125,
                            description="0.125",
                            enabled=False,
                            mathDescription="1 / 8"))

        # 1 / 4
        ratios.append(Ratio(ratio=0.25,
                            description="0.250",
                            enabled=True,
                            mathDescription="1 / 4"))

        # 3 / 8
        ratios.append(Ratio(ratio=0.375,
                            description="0.375",
                            enabled=False,
                            mathDescription="3 / 8"))

        # 1 / 3
        ratios.append(Ratio(ratio=0.333333333333333,
                            description="0.333",
                            enabled=True,
                            mathDescription="1 / 3"))

        # 1 / 2
        ratios.append(Ratio(ratio=0.5,
                            description="0.500",
                            enabled=True,
                            mathDescription="1 / 2"))
        
        # 5 / 8
        ratios.append(Ratio(ratio=0.625,
                            description="0.625",
                            enabled=False,
                            mathDescription="5 / 8"))

        # 2 / 3
        ratios.append(Ratio(ratio=0.66666666666666,
                            description="0.666",
                            enabled=True,
                            mathDescription="2 / 3"))
        
        # 3 / 4
        ratios.append(Ratio(ratio=0.75,
                            description="0.750",
                            enabled=True,
                            mathDescription="3 / 4"))

        # 7 / 8
        ratios.append(Ratio(ratio=0.875,
                            description="0.875",
                            enabled=False,
                            mathDescription="7 / 8"))

        # 1 / 1
        ratios.append(Ratio(ratio=1.0,
                            description="1.000",
                            enabled=True,
                            mathDescription="1"))
        
        # 4 / 3
        ratios.append(Ratio(ratio=1.333333333333,
                            description="1.333",
                            enabled=True,
                            mathDescription="4 / 3"))
        
        # 3 / 2
        ratios.append(Ratio(ratio=1.5,
                            description="1.500",
                            enabled=True,
                            mathDescription="3 / 2"))
        
        # 2 / 1
        ratios.append(Ratio(ratio=2.0,
                            description="2.000",
                            enabled=True,
                            mathDescription="2 / 1"))
        
        # 3 / 1
        ratios.append(Ratio(ratio=3.0,
                            description="3.000",
                            enabled=True,
                            mathDescription="3 / 1"))
        
        # 4 / 1
        ratios.append(Ratio(ratio=4.0,
                            description="4.000",
                            enabled=False,
                            mathDescription="4 / 1"))
        
        # 5 / 1
        ratios.append(Ratio(ratio=5.0,
                            description="5.000",
                            enabled=False,
                            mathDescription="5 / 1"))
        
        # 6 / 1
        ratios.append(Ratio(ratio=6.0,
                            description="6.000",
                            enabled=False,
                            mathDescription="6 / 1"))
        
        # 7 / 1
        ratios.append(Ratio(ratio=7.0,
                            description="7.000",
                            enabled=False,
                            mathDescription="7 / 1"))
        
        # 8 / 1
        ratios.append(Ratio(ratio=8.0,
                            description="8.000",
                            enabled=False,
                            mathDescription="8 / 1"))
        
        ############
        
        # 1 / (2 * math.sqrt(2))
        ratios.append(Ratio(ratio=0.353553390593274,
                            description="0.354",
                            enabled=True,
                            mathDescription="1 / (2 * math.sqrt(2))"))
        
        # 1 / math.sqrt(5)
        ratios.append(Ratio(ratio=0.447213595499958,
                            description="0.447",
                            enabled=True,
                            mathDescription="1 / math.sqrt(5)"))
        
        # 1 / math.sqrt(3)
        ratios.append(Ratio(ratio=0.577350269189626,
                            description="0.577",
                            enabled=True,
                            mathDescription="1 / math.sqrt(3)"))
        
        # 1 / math.sqrt(2)
        ratios.append(Ratio(ratio=0.577350269189626,
                            description="0.577",
                            enabled=True,
                            mathDescription="1 / math.sqrt(2)"))
        
        # math.sqrt(2)
        ratios.append(Ratio(ratio=1.4142135623731,
                            description="1.414",
                            enabled=True,
                            mathDescription="math.sqrt(2)"))
        
        # math.sqrt(3)
        ratios.append(Ratio(ratio=1.73205080756888,
                            description="1.732",
                            enabled=True,
                            mathDescription="math.sqrt(3)"))
        
        # math.sqrt(5)
        ratios.append(Ratio(ratio=2.2360679775,
                            description="2.236",
                            enabled=True,
                            mathDescription="math.sqrt(5)"))

        ############

        # Sort by ratio value.
        ratios.sort(key=lambda r: r.ratio)
        
        # Put the unique ratios in a new list called 'ratios_unique'.
        ratios_unique = []
        for i in range(len(ratios)):
            currRatio = ratios[i]
            
            if i == 0:
                ratios_unique.append(currRatio)
            else:
                prevRatio = ratios[i-1]

                if not Util.fuzzyIsEqual(currRatio.ratio, prevRatio.ratio):
                    # Ratio is different from the one before it, so append.
                    ratios_unique.append(currRatio)


        # Store the unique ratios as the ratios to be returned.
        ratios = ratios_unique

        return ratios
    
    @staticmethod
    def getSupportedFibRatios():
        """Returns a list of Fibonacci Ratio objects that we plan on
        supporting in this application.

        For the source of these ratios below, see the following books:
        Geometry of Markets (beginning of the book before first numbered page).
        Geometry of Markets (Chapter 2, Page 9).
        Geometry of Markets (Chapter 6, Page 50).
        Geometry of Markets II (pg. 8)
        """

        # Return value.
        ratios = []

        # 0
        ratios.append(Ratio(ratio=0.000,
                            description="0.000",
                            enabled=True,
                            mathDescription="0"))
        
        # (1 / phi)^4
        ratios.append(Ratio(ratio=0.14589803375,
                            description="0.146",
                            enabled=True,
                            mathDescription="(1 / phi)^4"))
        
        # (1 / phi)^3
        ratios.append(Ratio(ratio=0.23606797695,
                            description="0.236",
                            enabled=True,
                            mathDescription="(1 / phi)^3"))
        
        # (1 / phi)^2
        ratios.append(Ratio(ratio=0.38196601066,
                            description="0.382",
                            enabled=True,
                            mathDescription="(1 / phi)^2"))
        
        # (1 / phi)^1
        ratios.append(Ratio(ratio=0.61803398827,
                            description="0.618",
                            enabled=True,
                            mathDescription="(1 / phi)^1"))
        
        # math.sqrt(1 / phi)
        ratios.append(Ratio(ratio=0.78615137745,
                            description="0.786",
                            enabled=True,
                            mathDescription="math.sqrt(1 / phi)"))
        
        # math.pow((1 / phi), 1/3)
        ratios.append(Ratio(ratio=0.85179964186,
                            description="0.852",
                            enabled=True,
                            mathDescription="math.pow((1 / phi), 1/3)"))
        
        # 1
        ratios.append(Ratio(ratio=1.000,
                            description="1.000",
                            enabled=True,
                            mathDescription="1"))
        
        # 0.5 + (1 / phi)
        ratios.append(Ratio(ratio=1.11803398875,
                            description="1.118",
                            enabled=True,
                            mathDescription="0.5 + (1 / phi)"))
        
        # math.pow(phi, 1/3)
        ratios.append(Ratio(ratio=1.17398499701,
                            description="1.174",
                            enabled=True,
                            mathDescription="math.pow(phi, 1/3)"))
        
        # math.sqrt(phi)
        ratios.append(Ratio(ratio=1.27201965001,
                            description="1.272",
                            enabled=True,
                            mathDescription="math.sqrt(phi)"))
        
        # math.sqrt(phi)^2
        ratios.append(Ratio(ratio=1.61803398875,
                            description="1.618",
                            enabled=True,
                            mathDescription="math.sqrt(phi)^2"))
        
        # math.sqrt(1^2 + phi^2)
        ratios.append(Ratio(ratio=1.90211303259,
                            description="1.902",
                            enabled=True,
                            mathDescription="math.sqrt(1^2 + phi^2)"))
        
        # math.sqrt(phi)^3
        ratios.append(Ratio(ratio=2.05817102727,
                            description="2.058",
                            enabled=True,
                            mathDescription="math.sqrt(phi)^3"))
        
        # math.sqrt(phi)^4
        ratios.append(Ratio(ratio=2.61803398859,
                            description="2.618",
                            enabled=True,
                            mathDescription="math.sqrt(phi)^4"))
        
        # math.sqrt(phi)^5
        ratios.append(Ratio(ratio=3.33019067679,
                            description="3.330",
                            enabled=True,
                            mathDescription="math.sqrt(phi)^5"))
        
        # math.sqrt(phi)^6
        ratios.append(Ratio(ratio=4.2360679775,
                            description="4.236",
                            enabled=False,
                            mathDescription="math.sqrt(phi)^6"))
        
        return ratios
    
    @staticmethod
    def getSupportedGannFanRatios():
        """Returns a list of Gann Ratio objects that we plan on
        supporting in this application.
        """

        # Return value.
        ratios = []


        # These ratios below are multiplied by 90 degrees to get the
        # angle that will be drawn in the QGraphicsItem.
        
        
        # 0
        ratios.append(Ratio(ratio=0.000,
                            description="0x1",
                            enabled=True))
        
        # 1 / 8
        ratios.append(Ratio(ratio=0.125,
                            description="1x4",
                            enabled=True))
        
        # 1 / 6
        ratios.append(Ratio(ratio=1.0/6.0,
                            description="1x3",
                            enabled=True))
        
        # 1 / 4
        ratios.append(Ratio(ratio=0.250,
                            description="1x2",
                            enabled=True))
        
        # 1 / 3
        ratios.append(Ratio(ratio=1.0/3.0,
                            description="1x1.5",
                            enabled=True))
        
        # 1 / 2
        ratios.append(Ratio(ratio=0.500,
                            description="1x1",
                            enabled=True))
        
        # 2 / 3
        ratios.append(Ratio(ratio=2.0/3.0,
                            description="1.5x1",
                            enabled=True))
        
        # 3 / 4
        ratios.append(Ratio(ratio=0.750,
                            description="2x1",
                            enabled=True))
        
        # 5 / 6
        ratios.append(Ratio(ratio=5.0/6.0,
                            description="3x1",
                            enabled=True))
        
        # 7 / 8
        ratios.append(Ratio(ratio=0.875,
                            description="4x1",
                            enabled=True))
        
        # 1
        ratios.append(Ratio(ratio=1.000,
                            description="1x0",
                            enabled=True))
        
        return ratios
    
    def getRatio(self):
        """Returns the float ratio value.
        """

        return self.ratio

    def setRatio(self, ratio):
        """Sets the ratio.
        
        Arguments:
        ratio - float value for the ratio.
        """
        
        self.ratio = ratio
    
    def getDescription(self):
        """Returns the str description value.
        """

        return self.description

    def setDescription(self, description):
        """Sets the description.
        
        Arguments:
        description - str value for the description.
        """
        
        self.description = description
    
    def isEnabled(self):
        """Returns the whether or not the MusicalRatio is enabled.
        """

        return self.enabled
    
    def getEnabled(self):
        """Returns the whether or not the MusicalRatio is enabled.
        """

        return self.enabled

    def setEnabled(self, enabled):
        """Sets whether or not the MusicalRatio is enabled.
        
        Arguments:
        enabled - bool value for the enabled.
        """
        
        self.enabled = enabled
    
    def getMathDescription(self):
        """Returns the str mathDescription value.
        """

        return self.mathDescription

    def setMathDescription(self, mathDescription):
        """Sets the mathDescription.
        
        Arguments:
        mathDescription - str value for the mathDescription.
        """
        
        self.mathDescription = mathDescription
    
    def toString(self):
        """Returns the string representation of the data."""

        rv = Util.objToString(self)
        
        return rv

    def __str__(self):
        """Returns the string representation of the PriceBar data"""

        return self.toString()

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.Ratio")

        # Update the object to the most current version if it is not current.
        if self.classVersion < 2:
            self.log.info("Detected an old class version of " + \
                          "Ratio (version {}).  ".\
                          format(self.classVersion))

            if self.classVersion == 1:
                # Version 2 added the following member variables:
                #
                # self.mathDescription
                #
                
                try:
                    # See if the variable is set.
                    self.mathDescription
    
                    # If it got here, then the field is already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have this field.")
                    
                except AttributeError:
                    # Variable was not set.  Set it to the default value.
                    self.mathDescription = ""
                    
                    self.log.debug("Added field 'mathDescription' " + \
                                   "to the loaded Ratio.")
                    
                    # Update the class version.
                    prevClassVersion = self.classVersion
                    self.classVersion = 2
            
                    self.log.info("Object has been updated from " + \
                                  "version {} to version {}.".\
                                  format(prevClassVersion, self.classVersion))
            
        # Log that we set the state of this object.
        self.log.debug("Set state of a " + Ratio.__name__ +
                       " object of version {}".format(self.classVersion))


class MusicalRatio(Ratio):
    """Contains information about a musical ratio that makes up a note
    in a scale.  Includes the following information:

    - float value for the ratio.
    - description of the ratio.
    - numerator of the fraction (if applicable)
    - denominator of the fraction (if applicable)
    - enabled flag indicating whether or not the musical ratio is enabled.
    """


    def __init__(self,
                 ratio,
                 description="",
                 numerator=None,
                 denominator=None,
                 enabled=True):
        """Initializes the PriceBar object.  

        Arguments are as follows:
        
        ratio - float value holding the ratio for the musical note.
        description - str value holding the description of the ratio.
        numerator - int value holding the numerator of
                    the fraction (if applicable)
        denominator - int value holding the denominator of the
                    fraction (if applicable)
        enabled - bool value indicating if the musical ratio is
                  enabled or disabled.
        """
        super().__init__(ratio, description, enabled)
        
        # Class version stored for pickling and unpickling.
        self.classVersion = 1

        # Logger object.
        self.log = logging.getLogger("data_objects.MusicalRatio")

        self.ratio = ratio
        self.description = description
        self.numerator = numerator
        self.denominator = denominator
        self.enabled = enabled
        
    @staticmethod
    def getIndianMusicalRatios():
        """Returns a list of MusicalRatio objects that contain all the
        Indian shrutis.
        """

        # Return value.
        ratios = []

        ratios.append(MusicalRatio(ratio=1/1.0,
                                   description="(P1) (1/1) (Do) Kṣobhinī",
                                   numerator=1,
                                   denominator=1,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=256/243.0,
                                   description="(m2) (256/243) Tīvrā",
                                   numerator=256,
                                   denominator=243,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=16/15.0,
                                   description="(m2) (16/15) Kumudvatī",
                                   numerator=16,
                                   denominator=15,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=10/9.0,
                                   description="(M2) (10/9) Mandā",
                                   numerator=10,
                                   denominator=9,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=9/8.0,
                                   description="(M2) (9/8) (Re) Chandovatī",
                                   numerator=9,
                                   denominator=8,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=32/27.0,
                                   description="(m3) (32/27) Dayāvatī",
                                   numerator=32,
                                   denominator=27,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=6/5.0,
                                   description="(m3) (6/5) Ranjanī",
                                   numerator=6,
                                   denominator=5,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=5/4.0,
                                   description="(M3) (5/4) (Mi) Raktikā",
                                   numerator=5,
                                   denominator=4,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=81/64.0,
                                   description="(M3) (81/64) Raudrī",
                                   numerator=81,
                                   denominator=64,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=4/3.0,
                                   description="(P4) (4/3) (Fa) Krodhā",
                                   numerator=4,
                                   denominator=3,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=27/20.0,
                                   description="(P4) (27/20) Vajrikā",
                                   numerator=27,
                                   denominator=20,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=45/32.0,
                                   description="(A4) (45/32) Prasāriṇī",
                                   numerator=45,
                                   denominator=32,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=729/512.0,
                                   description="(A4) (729/512) Prīti",
                                   numerator=729,
                                   denominator=512,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=3/2.0,
                                   description="(P5) (3/2) (So) Mārjanī",
                                   numerator=3,
                                   denominator=2,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=128/81.0,
                                   description="(m6) (128/81) Kṣiti",
                                   numerator=128,
                                   denominator=81,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=8/5.0,
                                   description="(m6) (8/5) Raktā",
                                   numerator=8,
                                   denominator=5,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=5/3.0,
                                   description="(M6) (5/3) (La) Sandīpanī",
                                   numerator=5,
                                   denominator=3,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=27/16.0,
                                   description="(M6) (27/16) Ālāpinī",
                                   numerator=27,
                                   denominator=16,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=16/9.0,
                                   description="(m7) (16/9) Madantī",
                                   numerator=16,
                                   denominator=9,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=9/5.0,
                                   description="(m7) (9/5) Rohiṇī",
                                   numerator=9,
                                   denominator=5,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=15/8.0,
                                   description="(M7) (15/8) (Ti) Ramyā",
                                   numerator=15,
                                   denominator=8,
                                   enabled=True))

        ratios.append(MusicalRatio(ratio=243/128.0,
                                   description="(M7) (243/128) Ugrā",
                                   numerator=243,
                                   denominator=128,
                                   enabled=True))

        #ratios.append(MusicalRatio(ratio=2/1.0,
        #                           description="(P8) (2/1) (Do) Kṣobhinī",
        #                           numerator=2,
        #                           denominator=1,
        #                           enabled=True))

        return ratios
    
    @staticmethod
    def getNonIndianPythagoreanMusicalRatios():
        """Returns a list of MusicalRatio objects that are the
        Pythagorean musical ratios not already covered by the Indian
        musical ratios.
        """

        ratios = []
        
        ratios.append(MusicalRatio(ratio=1024/729.0,
                                   description="(d5) Pythagorean Tuning",
                                   numerator=1024,
                                   denominator=729,
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getMusicalRatiosForTimeModalScaleGraphicsItem():
        """Returns a list of MusicalRatios to be used for the
        TimeModalScale.
        """

        musicalRatios = MusicalRatio.getIndianMusicalRatios()

        # Set certain MusicalRatios as enabled or disabled.
        for i in range(len(musicalRatios)):
            musicalRatio = musicalRatios[i]

            numerator = musicalRatio.getNumerator()
            denominator = musicalRatio.getDenominator()
            
            if numerator == 1 and denominator == 1:
                musicalRatio.setEnabled(True)
            elif numerator == 256 and denominator == 243:
                musicalRatio.setEnabled(False)
            elif numerator == 16 and denominator == 15:
                musicalRatio.setEnabled(False)
            elif numerator == 10 and denominator == 9:
                musicalRatio.setEnabled(False)
            elif numerator == 9 and denominator == 8:
                musicalRatio.setEnabled(True)
            elif numerator == 32 and denominator == 27:
                musicalRatio.setEnabled(False)
            elif numerator == 6 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 5 and denominator == 4:
                musicalRatio.setEnabled(True)
            elif numerator == 81 and denominator == 64:
                musicalRatio.setEnabled(False)
            elif numerator == 4 and denominator == 3:
                musicalRatio.setEnabled(True)
            elif numerator == 27 and denominator == 20:
                musicalRatio.setEnabled(False)
            elif numerator == 45 and denominator == 32:
                musicalRatio.setEnabled(False)
            elif numerator == 729 and denominator == 512:
                musicalRatio.setEnabled(False)
            elif numerator == 3 and denominator == 2:
                musicalRatio.setEnabled(True)
            elif numerator == 128 and denominator == 81:
                musicalRatio.setEnabled(False)
            elif numerator == 8 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 5 and denominator == 3:
                musicalRatio.setEnabled(True)
            elif numerator == 27 and denominator == 16:
                musicalRatio.setEnabled(False)
            elif numerator == 16 and denominator == 9:
                musicalRatio.setEnabled(False)
            elif numerator == 9 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 15 and denominator == 8:
                musicalRatio.setEnabled(True)
            elif numerator == 243 and denominator == 128:
                musicalRatio.setEnabled(False)
            elif numerator == 2 and denominator == 1:
                musicalRatio.setEnabled(False)
            else:
                currMethodName = inspect.stack()[0][3] + "()"
                
                print("WARNING: " + currMethodName + ": " + 
                      "Unknown musical ratio: " + musicalRatio.toString())
                
                musicalRatio.setEnabled(False)

        return musicalRatios
    
    @staticmethod
    def getMusicalRatiosForPriceModalScaleGraphicsItem():
        """Returns a list of MusicalRatios to be used for the
        PriceModalScale.
        """

        musicalRatios = MusicalRatio.getIndianMusicalRatios()

        # Set certain MusicalRatios as enabled or disabled.
        for i in range(len(musicalRatios)):
            musicalRatio = musicalRatios[i]

            numerator = musicalRatio.getNumerator()
            denominator = musicalRatio.getDenominator()
            
            if numerator == 1 and denominator == 1:
                musicalRatio.setEnabled(True)
            elif numerator == 256 and denominator == 243:
                musicalRatio.setEnabled(False)
            elif numerator == 16 and denominator == 15:
                musicalRatio.setEnabled(False)
            elif numerator == 10 and denominator == 9:
                musicalRatio.setEnabled(False)
            elif numerator == 9 and denominator == 8:
                musicalRatio.setEnabled(True)
            elif numerator == 32 and denominator == 27:
                musicalRatio.setEnabled(False)
            elif numerator == 6 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 5 and denominator == 4:
                musicalRatio.setEnabled(True)
            elif numerator == 81 and denominator == 64:
                musicalRatio.setEnabled(False)
            elif numerator == 4 and denominator == 3:
                musicalRatio.setEnabled(True)
            elif numerator == 27 and denominator == 20:
                musicalRatio.setEnabled(False)
            elif numerator == 45 and denominator == 32:
                musicalRatio.setEnabled(False)
            elif numerator == 729 and denominator == 512:
                musicalRatio.setEnabled(False)
            elif numerator == 3 and denominator == 2:
                musicalRatio.setEnabled(True)
            elif numerator == 128 and denominator == 81:
                musicalRatio.setEnabled(False)
            elif numerator == 8 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 5 and denominator == 3:
                musicalRatio.setEnabled(True)
            elif numerator == 27 and denominator == 16:
                musicalRatio.setEnabled(False)
            elif numerator == 16 and denominator == 9:
                musicalRatio.setEnabled(False)
            elif numerator == 9 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 15 and denominator == 8:
                musicalRatio.setEnabled(True)
            elif numerator == 243 and denominator == 128:
                musicalRatio.setEnabled(False)
            elif numerator == 2 and denominator == 1:
                musicalRatio.setEnabled(False)
            else:
                currMethodName = inspect.stack()[0][3] + "()"
                
                print("WARNING: " + currMethodName + ": " + 
                      "Unknown musical ratio: " + musicalRatio.toString())
                
                musicalRatio.setEnabled(False)

        return musicalRatios
    
    @staticmethod
    def getMusicalRatiosForOctaveFanGraphicsItem():
        """Returns a list of MusicalRatios to be used for the
        PriceModalScale.
        """

        musicalRatios = MusicalRatio.getIndianMusicalRatios()

        # Set certain MusicalRatios as enabled or disabled.
        for i in range(len(musicalRatios)):
            musicalRatio = musicalRatios[i]

            numerator = musicalRatio.getNumerator()
            denominator = musicalRatio.getDenominator()
            
            if numerator == 1 and denominator == 1:
                musicalRatio.setEnabled(True)
            elif numerator == 256 and denominator == 243:
                musicalRatio.setEnabled(False)
            elif numerator == 16 and denominator == 15:
                musicalRatio.setEnabled(False)
            elif numerator == 10 and denominator == 9:
                musicalRatio.setEnabled(False)
            elif numerator == 9 and denominator == 8:
                musicalRatio.setEnabled(True)
            elif numerator == 32 and denominator == 27:
                musicalRatio.setEnabled(False)
            elif numerator == 6 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 5 and denominator == 4:
                musicalRatio.setEnabled(True)
            elif numerator == 81 and denominator == 64:
                musicalRatio.setEnabled(False)
            elif numerator == 4 and denominator == 3:
                musicalRatio.setEnabled(True)
            elif numerator == 27 and denominator == 20:
                musicalRatio.setEnabled(False)
            elif numerator == 45 and denominator == 32:
                musicalRatio.setEnabled(False)
            elif numerator == 729 and denominator == 512:
                musicalRatio.setEnabled(False)
            elif numerator == 3 and denominator == 2:
                musicalRatio.setEnabled(True)
            elif numerator == 128 and denominator == 81:
                musicalRatio.setEnabled(False)
            elif numerator == 8 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 5 and denominator == 3:
                musicalRatio.setEnabled(True)
            elif numerator == 27 and denominator == 16:
                musicalRatio.setEnabled(False)
            elif numerator == 16 and denominator == 9:
                musicalRatio.setEnabled(False)
            elif numerator == 9 and denominator == 5:
                musicalRatio.setEnabled(False)
            elif numerator == 15 and denominator == 8:
                musicalRatio.setEnabled(True)
            elif numerator == 243 and denominator == 128:
                musicalRatio.setEnabled(False)
            elif numerator == 2 and denominator == 1:
                musicalRatio.setEnabled(False)
            else:
                currMethodName = inspect.stack()[0][3] + "()"
                
                print("WARNING: " + currMethodName + ": " + 
                      "Unknown musical ratio: " + musicalRatio.toString())
                
                musicalRatio.setEnabled(False)

        return musicalRatios
    
    @staticmethod
    def getVimsottariDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Vimsottari dasa in this application.

        Dasa description:
        Vimsottari dasa is a general purpose nakshatra dasa that shows
        all the events in a native's life from the vantage point of
        native's mind.  It tracks the changes throughout one's life.
        It is one of the most important of all dasas in Kali Yuga.
        Though it is normally started from moon's nakshatra it can
        also be started from Kshema, Utpanna and Adhana taras, lagna,
        Maandi and Trisphuta.
        """

        # Return value.
        ratios = []

        settings = QSettings()

        ketu = 7.0
        venus = 20.0
        sun = 6.0
        moon = 10.0
        mars = 7.0
        rahu = 18.0
        jupiter = 16.0
        saturn = 19.0
        mercury = 17.0
        
        total = 120.0
        
        # Ketu.
        ketuStart = 0.0
        key = SettingsKeys.planetMeanSouthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanSouthNodeAbbreviationDefValue
        ketuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(ketuStart / total),
                                   description=ketuDescription,
                                   numerator=int(ketuStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = ketuStart + ketu
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Sun.
        sunStart = venusStart + venus
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = sunStart + sun
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = moonStart + moon
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Rahu.
        rahuStart = marsStart + mars
        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanNorthNodeAbbreviationDefValue
        rahuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(rahuStart / total),
                                   description=rahuDescription,
                                   numerator=int(rahuStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = rahuStart + rahu
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = jupiterStart + jupiter
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = saturnStart + saturn
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getAshtottariDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Ashtottari dasa in this application.

        Dasa description:
        Ashtottari dasa is a popular nakshatra dasa.  Some hold it to
        be universally applicable.  Some apply it for daytime births
        in Krishna paksha and night time births in Sukla paksha.  Some
        apply it when Rahu is in a trine or quadrant from lagna lord
        (but not in lagna).  As it is based on a 108-year cycle, some
        use it as an ayur dasa and time death from it.  As only chara
        karakas figure in it, some use it as a dasa that shows
        sustenance and raja yogas.
        """

        # Return value.
        ratios = []

        settings = QSettings()

        rahu = 12.0
        venus = 21.0
        sun = 6.0
        moon = 15.0
        mars = 8.0
        mercury = 17.0
        saturn = 10.0
        jupiter = 19.0
        
        total = 108.0
        
        # Rahu.
        rahuStart = 0.0
        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanNorthNodeAbbreviationDefValue
        rahuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(rahuStart / total),
                                   description=rahuDescription,
                                   numerator=int(rahuStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = rahuStart + rahu
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Sun.
        sunStart = venusStart + venus
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = sunStart + sun
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = moonStart + moon
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = marsStart + mars
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = mercuryStart + mercury
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = saturnStart + saturn
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getYoginiDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Yogini dasa in this application.
        
        Dasa description:
        Yogini dasa is a tantrik dasa that shows the impact of various
        Yoginis on a person at various times.
        """

        # Return value.
        ratios = []

        settings = QSettings()

        moon = 1.0
        sun = 2.0
        jupiter = 3.0
        mars = 4.0
        mercury = 5.0
        saturn = 6.0
        venus = 7.0
        rahu = 8.0
        
        total = 36.0
        
        # Moon.
        moonStart = 0.0
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Sun.
        sunStart = moonStart + moon
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = sunStart + sun
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = jupiterStart + jupiter
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = marsStart + mars
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = mercuryStart + mercury
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = saturnStart + saturn
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Rahu.
        rahuStart = venusStart + venus
        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanNorthNodeAbbreviationDefValue
        rahuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(rahuStart / total),
                                   description=rahuDescription,
                                   numerator=int(rahuStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getDwisaptatiSamaDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for DwisaptatiSama dasa in this application.

        Dasa description:
        Dwi-saptati sama dasa is a conditional nakshatra dasa that is
        applicable if lagna lord is in 7th or 7th lord is in lagna.
        """
        
        # Return value.
        ratios = []

        settings = QSettings()

        sun = 9.0
        moon = 9.0
        mars = 9.0
        mercury = 9.0
        jupiter = 9.0
        venus = 9.0
        saturn = 9.0
        rahu = 9.0
        
        total = 72.0
        
        # Sun.
        sunStart = 0.0
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = sunStart + sun
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = moonStart + moon
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = marsStart + mars
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = mercuryStart + mercury
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = jupiterStart + jupiter
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Saturn.
        saturnStart = venusStart + venus
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Rahu.
        rahuStart = saturnStart + saturn
        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanNorthNodeAbbreviationDefValue
        rahuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(rahuStart / total),
                                   description=rahuDescription,
                                   numerator=int(rahuStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getShattrimsaSamaDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for ShattrimsaSama dasa in this application.

        Dasa description:
        Shat-trimsa sama dasa is a conditional nakshatra dasa that is
        applicable for daytime births in Sun's hora and night-time
        births in Moon's hora.
        """

        # Return value.
        ratios = []

        settings = QSettings()

        moon = 1.0
        sun = 2.0
        jupiter = 3.0
        mars = 4.0
        mercury = 5.0
        saturn = 6.0
        venus = 7.0
        rahu = 8.0
        
        total = 36.0
        
        # Moon.
        moonStart = 0.0
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Sun.
        sunStart = moonStart + moon
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = sunStart + sun
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = jupiterStart + jupiter
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = marsStart + mars
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = mercuryStart + mercury
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = saturnStart + saturn
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Rahu.
        rahuStart = venusStart + venus
        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanNorthNodeAbbreviationDefValue
        rahuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(rahuStart / total),
                                   description=rahuDescription,
                                   numerator=int(rahuStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getDwadasottariDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Dwadasottari dasa in this application.

        Dasa description:
        Dwadasottari dasa is a conditional nakshatra dasa that is
        applicable if lagna is in Venusian amsa.
        """

        # Return value.
        ratios = []

        settings = QSettings()

        sun = 7.0
        jupiter = 9.0
        ketu = 11.0
        mercury = 13.0
        rahu = 15.0
        mars = 17.0
        saturn = 19.0
        moon = 21.0
        
        total = 112.0
        
        # Sun.
        sunStart = 0.0
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = sunStart + sun
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Ketu.
        ketuStart = jupiterStart + jupiter
        key = SettingsKeys.planetMeanSouthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanSouthNodeAbbreviationDefValue
        ketuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(ketuStart / total),
                                   description=ketuDescription,
                                   numerator=int(ketuStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Mercury.
        mercuryStart = ketuStart + ketu
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Rahu.
        rahuStart = mercuryStart + mercury
        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanNorthNodeAbbreviationDefValue
        rahuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(rahuStart / total),
                                   description=rahuDescription,
                                   numerator=int(rahuStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = rahuStart + rahu
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = marsStart + mars
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = saturnStart + saturn
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getChaturaseetiSamaDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for ChaturaseetiSama dasa in this application.

        Dasa description:
        Chaturaseeti sama dasa is a conditional nakshatra dasa that is
        applicable if the 10th lord is in the 10th house.
        """

        # Return value.
        ratios = []

        settings = QSettings()

        sun = 12.0
        moon = 12.0
        mars = 12.0
        mercury = 12.0
        jupiter = 12.0
        venus = 12.0
        saturn = 12.0
        
        total = 84.0
        
        # Sun.
        sunStart = 0.0
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = sunStart + sun
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = moonStart + moon
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = marsStart + mars
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = mercuryStart + mercury
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = jupiterStart + jupiter
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Saturn.
        saturnStart = venusStart + venus
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getSataabdikaDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Sataabdika dasa in this application.

        Dasa description:
        Sataabdika dasa is a conditional nakshatra dasa that is
        applicable if lagna is in vargottama.
        """

        # Return value.
        ratios = []

        settings = QSettings()

        sun = 5.0
        moon = 5.0
        venus = 10.0
        mercury = 10.0
        jupiter = 20.0
        mars = 20.0
        saturn = 30.0
        
        total = 100.0
        
        # Sun.
        sunStart = 0.0
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = sunStart + sun
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = moonStart + moon
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Mercury.
        mercuryStart = venusStart + venus
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = mercuryStart + mercury
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = jupiterStart + jupiter
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = marsStart + mars
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getShodasottariDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Shodasottari dasa in this application.

        Dasa description:
        Shodasottari dasa is a conditional nakshatra dasa that is
        applicable if lagna is in Moon's hora in Krishna paksha or in
        Sun's hora in Sukla paksha.
        """
        
        # Return value.
        ratios = []
        
        settings = QSettings()

        sun = 11.0
        mars = 12.0
        jupiter = 13.0
        saturn = 14.0
        ketu = 15.0
        moon = 16.0
        mercury = 17.0
        venus = 18.0
        
        total = 116.0
        
        # Sun.
        sunStart = 0.0
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = sunStart + sun
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = marsStart + mars
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = jupiterStart + jupiter
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Ketu.
        ketuStart = saturnStart + saturn
        key = SettingsKeys.planetMeanSouthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanSouthNodeAbbreviationDefValue
        ketuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(ketuStart / total),
                                   description=ketuDescription,
                                   numerator=int(ketuStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = ketuStart + ketu
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = moonStart + moon
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = mercuryStart + mercury
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        return ratios
    
    @staticmethod
    def getPanchottariDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Panchottari dasa in this application.

        Dasa description:
        Panchottari dasa is a conditional nakshatra dasa that is
        applicable if lagna is in Cancer in rasi and dwadasamsa.
        """
        
        # Return value.
        ratios = []
        
        settings = QSettings()

        sun = 12.0
        mercury = 13.0
        saturn = 14.0
        mars = 15.0
        venus = 16.0
        moon = 17.0
        jupiter = 18.0
        
        total = 105.0
        
        # Sun.
        sunStart = 0.0
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = sunStart + sun
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Saturn.
        saturnStart = mercuryStart + mercury
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = saturnStart + saturn
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = marsStart + mars
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Moon.
        moonStart = venusStart + venus
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Jupiter.
        jupiterStart = moonStart + moon
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    @staticmethod
    def getShashtihayaniDasaMusicalRatios():
        """Returns a list of MusicalRatio objects that we plan on
        supporting for Shashtihayani dasa in this application.

        Dasa description:
        Shashtihayani dasa is a conditional nakshatra dasa that is
        applicable if Sun is in lagna.
        """
        
        # Return value.
        ratios = []
        
        settings = QSettings()

        jupiter = 10.0
        sun = 10.0
        mars = 10.0
        moon = 6.0
        mercury = 6.0
        venus = 6.0
        saturn = 6.0
        rahu = 6.0
        
        total = 60.0
        
        # Jupiter.
        jupiterStart = 0.0
        key = SettingsKeys.planetJupiterAbbreviationKey
        defaultValue = SettingsKeys.planetJupiterAbbreviationDefValue
        jupiterDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(jupiterStart / total),
                                   description=jupiterDescription,
                                   numerator=int(jupiterStart),
                                   denominator=int(total),
                                   enabled=True))

        # Sun.
        sunStart = jupiterStart + jupiter
        key = SettingsKeys.planetSunAbbreviationKey
        defaultValue = SettingsKeys.planetSunAbbreviationDefValue
        sunDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(sunStart / total),
                                   description=sunDescription,
                                   numerator=int(sunStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mars.
        marsStart = sunStart + sun
        key = SettingsKeys.planetMarsAbbreviationKey
        defaultValue = SettingsKeys.planetMarsAbbreviationDefValue
        marsDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(marsStart / total),
                                   description=marsDescription,
                                   numerator=int(marsStart),
                                   denominator=int(total),
                                   enabled=True))

        # Moon.
        moonStart = marsStart + mars
        key = SettingsKeys.planetMoonAbbreviationKey
        defaultValue = SettingsKeys.planetMoonAbbreviationDefValue
        moonDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(moonStart / total),
                                   description=moonDescription,
                                   numerator=int(moonStart),
                                   denominator=int(total),
                                   enabled=True))

        # Mercury.
        mercuryStart = moonStart + moon
        key = SettingsKeys.planetMercuryAbbreviationKey
        defaultValue = SettingsKeys.planetMercuryAbbreviationDefValue
        mercuryDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(mercuryStart / total),
                                   description=mercuryDescription,
                                   numerator=int(mercuryStart),
                                   denominator=int(total),
                                   enabled=True))

        # Venus.
        venusStart = mercuryStart + mercury
        key = SettingsKeys.planetVenusAbbreviationKey
        defaultValue = SettingsKeys.planetVenusAbbreviationDefValue
        venusDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(venusStart / total),
                                   description=venusDescription,
                                   numerator=int(venusStart),
                                   denominator=int(total),
                                   enabled=True))
        
        # Saturn.
        saturnStart = venusStart + venus
        key = SettingsKeys.planetSaturnAbbreviationKey
        defaultValue = SettingsKeys.planetSaturnAbbreviationDefValue
        saturnDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(saturnStart / total),
                                   description=saturnDescription,
                                   numerator=int(saturnStart),
                                   denominator=int(total),
                                   enabled=True))

        # Rahu.
        rahuStart = saturnStart + saturn
        key = SettingsKeys.planetMeanNorthNodeAbbreviationKey
        defaultValue = SettingsKeys.planetMeanNorthNodeAbbreviationDefValue
        rahuDescription = settings.value(key, defaultValue, type=str)
        ratios.append(MusicalRatio(ratio=float(rahuStart / total),
                                   description=rahuDescription,
                                   numerator=int(rahuStart),
                                   denominator=int(total),
                                   enabled=True))

        return ratios
    
    def getNumerator(self):
        """Returns the int value that is the numerator portion of the
        fraction.  This can be None if it was not previously set.
        """

        return self.numerator

    def setNumerator(self, numerator):
        """Sets the value that is the numerator portion of the fraction.
        
        Arguments:
        numerator - int value for the numerator.
        """
        
        self.numerator = numerator
    
    def getDenominator(self):
        """Returns the int value that is the denominator portion of the
        fraction.  This can be None if it was not previously set.
        """

        return self.denominator

    def setDenominator(self, denominator):
        """Sets the value that is the denominator portion of the fraction.
        
        Arguments:
        denominator - int value for the denominator.
        """
        
        self.denominator = denominator
    
    def isEnabled(self):
        """Returns True if the MusicalRatio is set as enabled."""

        return self.enabled

    def setEnabled(self, enabledFlag):
        """Sets whether or not the MusicalRatio is set as enabled."""
        
        self.enabled = enabledFlag
        
    def inverted(self):
        """Returns the same MusicalRatio, but just inverted.
        '(Inverted)' str is added to the description.
        The returned MusicalRatio has the same enabled state.
        """

        inverted = \
            MusicalRatio(ratio=(1 / self.getRatio()),
                         description=self.getDescription() + " (Inverted)",
                         numerator=self.getDenominator(),
                         denominator=self.getNumerator(),
                         enabled=self.getEnabled())

        return inverted
    
    def toString(self):
        """Returns the string representation of the data."""

        rv = Util.objToString(self)
        
        return rv

    def __str__(self):
        """Returns the string representation of the PriceBar data"""

        return self.toString()

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.MusicalRatio")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " + MusicalRatio.__name__ +
                       " object of version {}".format(self.classVersion))


class PriceBarChartArtifact:
    """Base class for user-added artifacts in the PriceBarChartWidget.
    Sub-classes to this must be pickleable.

    This class includes tags as a list of str.  Tags are to identify
    artifacts with certain attributes.  This is useful if artifacts
    are added or removed via an external script.  They can seek and
    reference artifacts they added or removed by tags.  
    """
    
    def __init__(self):
        """Initializes attributes and members common to all 
        PriceBarChartArtifacts.
        """
        
        # UUID.
        self.uuid = uuid.uuid1()
        
        self.internalName = "UntypedArtifact_" + str(uuid.uuid1())
        
        # Position of the artifact QGraphicsItem.
        self.position = QPointF()

        # Tags
        self.tags = []

    def setPos(self, pointF):
        """Stores the position of the artifact, in scene coordinates.
        Arguments:

        pointF - QPointF of the position of the artifact, in scene coordinates.
        """

        self.position = pointF

    def getPos(self):
        """Returns the position of the artifact, in scene coordinates."""

        return self.position

    def getInternalName(self):
        """Returns the internal name of the artifact."""

        return self.internalName

    def getUuid(self):
        """Returns the uuid associated with this artifact."""
        
        return self.uuid

    def addTag(self, tagToAdd):
        """Adds a given tag string to the tags for this artifact.

        Arguments:
        tagToAdd - str that holds the tag.
        """

        # Strip any leading or trailing whitespace
        tagToAdd = tagToAdd.strip()

        # The tag added must be non-empty and must not already exist in the
        # list.
        if tagToAdd != "" and tagToAdd not in self.tags:
            self.tags.append(tagToAdd)

    def getTags(self):
        """Returns a list of str that are the tags for this artifact."""

        return self.tags
    
    def hasTag(self, tagToCheck):
        """Returns True if the given 'tagToCheck' str is in the list of tags."""

        if tagToCheck in self.tags:
            return True
        else:
            return False

    def clearTags(self):
        """Clears all the tags associated with this PriceBar."""

        self.tags = []

    def removeTag(self, tagToRemove):
        """Removes a given tag string from the tags in this PriceBar."""

        while tagToRemove in self.tags:
            self.tags.remove(tagToRemove)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv


class PriceBarChartBarCountArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates bar counts starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartBarCountArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "BarCount_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

    def setStartPointF(self, startPointF):
        """Stores the starting point of the BarCountArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the BarCountArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the BarCountArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the BarCountArtifact."""
        
        return self.endPointF
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartBarCountArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartBarCountArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartTimeMeasurementArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartTimeMeasurementArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "TimeMeasurement_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemTextYScaling
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultFontDescription
        
        # QColor can be pickled   
        self.textColor = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultTextColor

        # QColor can be pickled   
        self.color = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultColor

        # Flags for displaying various text.
        self.showBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowBarsTextFlag
        
        self.showSqrtBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtBarsTextFlag
        
        self.showSqrdBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdBarsTextFlag
        
        self.showHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowHoursTextFlag
        
        self.showSqrtHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtHoursTextFlag
        
        self.showSqrdHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdHoursTextFlag
        
        self.showDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowDaysTextFlag
        
        self.showSqrtDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtDaysTextFlag
        
        self.showSqrdDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdDaysTextFlag
        
        self.showWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowWeeksTextFlag
        
        self.showSqrtWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtWeeksTextFlag
        
        self.showSqrdWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdWeeksTextFlag
        
        self.showMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMonthsTextFlag
        
        self.showSqrtMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMonthsTextFlag
        
        self.showSqrdMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMonthsTextFlag
        
        self.showTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowTimeRangeTextFlag
        
        self.showSqrtTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag

        self.showSqrdTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag

        self.showScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowScaledValueRangeTextFlag

        self.showSqrtScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag

        self.showSqrdScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag

        self.showAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowAyanaTextFlag
        
        self.showSqrtAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtAyanaTextFlag
        
        self.showSqrdAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdAyanaTextFlag
        
        self.showMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMuhurtaTextFlag
        
        self.showSqrtMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag
        
        self.showSqrdMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag
        
        self.showVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowVaraTextFlag
        
        self.showSqrtVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtVaraTextFlag
        
        self.showSqrdVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdVaraTextFlag
        
        self.showRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowRtuTextFlag
        
        self.showSqrtRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtRtuTextFlag
        
        self.showSqrdRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdRtuTextFlag
        
        self.showMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMasaTextFlag
        
        self.showSqrtMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMasaTextFlag
        
        self.showSqrdMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMasaTextFlag
        
        self.showPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowPaksaTextFlag
        
        self.showSqrtPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtPaksaTextFlag
        
        self.showSqrdPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdPaksaTextFlag
        
        self.showSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSamaTextFlag
        
        self.showSqrtSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtSamaTextFlag
        
        self.showSqrdSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdSamaTextFlag
        
        
    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setTextColor(self, textColor):
        """Sets the color for this artifact's text.

        Arguments:
        textColor - QColor object holding the color of the text.
        """

        self.textColor = textColor

    def getTextColor(self):
        """Returns the color of this artifact's text as a QColor."""

        return self.textColor

    def setColor(self, color):
        """Sets the color for this artifact.

        Arguments:
        color - QColor object holding the color of the text.
        """

        self.color = color

    def getColor(self):
        """Returns the color of this artifact as a QColor."""

        return self.color

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setShowBarsTextFlag(self, flag):
        """Sets the flag that indicates that the text for the number
        of bars should be displayed.
        """

        self.showBarsTextFlag = flag
        
    def getShowBarsTextFlag(self):
        """Returns the flag that indicates that the text for the
        number of bars should be displayed.
        """

        return self.showBarsTextFlag
        
    def setShowSqrtBarsTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of
        the number of bars should be displayed.
        """

        self.showSqrtBarsTextFlag = flag
        
    def getShowSqrtBarsTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt
        of the number of bars should be displayed.
        """

        return self.showSqrtBarsTextFlag
        
    def setShowSqrdBarsTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrd of
        the number of bars should be displayed.
        """

        self.showSqrdBarsTextFlag = flag
        
    def getShowSqrdBarsTextFlag(self):
        """Returns the flag that indicates that the text for the sqrd
        of the number of bars should be displayed.
        """

        return self.showSqrdBarsTextFlag
        
    def setShowHoursTextFlag(self, flag):
        """Sets the flag that indicates that the text for the number
        of hours should be displayed.
        """

        self.showHoursTextFlag = flag
        
    def getShowHoursTextFlag(self):
        """Returns the flag that indicates that the text for the
        number of hours should be displayed.
        """

        return self.showHoursTextFlag
        
    def setShowSqrtHoursTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of
        the number of hours should be displayed.
        """

        self.showSqrtHoursTextFlag = flag
        
    def getShowSqrtHoursTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt
        of the number of hours should be displayed.
        """

        return self.showSqrtHoursTextFlag
        
    def setShowSqrdHoursTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrd of
        the number of hours should be displayed.
        """

        self.showSqrdHoursTextFlag = flag
        
    def getShowSqrdHoursTextFlag(self):
        """Returns the flag that indicates that the text for the sqrd
        of the number of hours should be displayed.
        """

        return self.showSqrdHoursTextFlag
        
    def setShowDaysTextFlag(self, flag):
        """Sets the flag that indicates that the text for the number
        of days should be displayed.
        """

        self.showDaysTextFlag = flag
        
    def getShowDaysTextFlag(self):
        """Returns the flag that indicates that the text for the
        number of days should be displayed.
        """

        return self.showDaysTextFlag
        
    def setShowSqrtDaysTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of
        the number of days should be displayed.
        """

        self.showSqrtDaysTextFlag = flag
        
    def getShowSqrtDaysTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt
        of the number of days should be displayed.
        """

        return self.showSqrtDaysTextFlag
        
    def setShowSqrdDaysTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrd of
        the number of days should be displayed.
        """

        self.showSqrdDaysTextFlag = flag
        
    def getShowSqrdDaysTextFlag(self):
        """Returns the flag that indicates that the text for the sqrd
        of the number of days should be displayed.
        """

        return self.showSqrdDaysTextFlag
        
    def setShowWeeksTextFlag(self, flag):
        """Sets the flag that indicates that the text for the number
        of weeks should be displayed.
        """

        self.showWeeksTextFlag = flag
        
    def getShowWeeksTextFlag(self):
        """Returns the flag that indicates that the text for the
        number of weeks should be displayed.
        """

        return self.showWeeksTextFlag
        
    def setShowSqrtWeeksTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of
        the number of weeks should be displayed.
        """

        self.showSqrtWeeksTextFlag = flag
        
    def getShowSqrtWeeksTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt
        of the number of weeks should be displayed.
        """

        return self.showSqrtWeeksTextFlag
        
    def setShowSqrdWeeksTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrd of
        the number of weeks should be displayed.
        """

        self.showSqrdWeeksTextFlag = flag
        
    def getShowSqrdWeeksTextFlag(self):
        """Returns the flag that indicates that the text for the sqrd
        of the number of weeks should be displayed.
        """

        return self.showSqrdWeeksTextFlag
        
    def setShowMonthsTextFlag(self, flag):
        """Sets the flag that indicates that the text for the number
        of months should be displayed.
        """

        self.showMonthsTextFlag = flag
        
    def getShowMonthsTextFlag(self):
        """Returns the flag that indicates that the text for the
        number of months should be displayed.
        """

        return self.showMonthsTextFlag
        
    def setShowSqrtMonthsTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of
        the number of months should be displayed.
        """

        self.showSqrtMonthsTextFlag = flag
        
    def getShowSqrtMonthsTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt
        of the number of months should be displayed.
        """

        return self.showSqrtMonthsTextFlag
        
    def setShowSqrdMonthsTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrd of
        the number of months should be displayed.
        """

        self.showSqrdMonthsTextFlag = flag
        
    def getShowSqrdMonthsTextFlag(self):
        """Returns the flag that indicates that the text for the sqrd
        of the number of months should be displayed.
        """

        return self.showSqrdMonthsTextFlag
        
    def setShowTimeRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the time
        range should be displayed.
        """

        self.showTimeRangeTextFlag = flag
        
    def getShowTimeRangeTextFlag(self):
        """Returns the flag that indicates that the text for the
        time range should be displayed.
        """

        return self.showTimeRangeTextFlag
        
    def setShowSqrtTimeRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of
        the time range should be displayed.
        """

        self.showSqrtTimeRangeTextFlag = flag
        
    def getShowSqrtTimeRangeTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt
        of the time range should be displayed.
        """

        return self.showSqrtTimeRangeTextFlag
        
    def setShowSqrdTimeRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrd of
        the time range should be displayed.
        """

        self.showSqrdTimeRangeTextFlag = flag
        
    def getShowSqrdTimeRangeTextFlag(self):
        """Returns the flag that indicates that the text for the sqrd
        of the time range should be displayed.
        """

        return self.showSqrdTimeRangeTextFlag
        
    def setShowScaledValueRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the scaled
        value representing the time range should be displayed.
        """

        self.showScaledValueRangeTextFlag = flag
        
    def getShowScaledValueRangeTextFlag(self):
        """Returns the flag that indicates that the text for the
        scaled value representing the time range should be displayed.
        """

        return self.showScaledValueRangeTextFlag

    def setShowSqrtScaledValueRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of scaled
        value representing the time range should be displayed.
        """

        self.showSqrtScaledValueRangeTextFlag = flag
        
    def getShowSqrtScaledValueRangeTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt of
        scaled value representing the time range should be displayed.
        """

        return self.showSqrtScaledValueRangeTextFlag

    def setShowSqrdScaledValueRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrd of scaled
        value representing the time range should be displayed.
        """

        self.showSqrdScaledValueRangeTextFlag = flag
        
    def getShowSqrdScaledValueRangeTextFlag(self):
        """Returns the flag that indicates that the text for the sqrd of
        scaled value representing the time range should be displayed.
        """

        return self.showSqrdScaledValueRangeTextFlag

    def setShowAyanaTextFlag(self, flag):
        """Sets the flag that indicates that the text for ayana (6
        months) count of time should be displayed.
        """

        self.showAyanaTextFlag = flag
        
    def getShowAyanaTextFlag(self):
        """Returns the flag that indicates that the text for ayana (6
        months) count of time should be displayed.
        """

        return self.showAyanaTextFlag

    def setShowSqrtAyanaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrt ayana
        (6 months) count of time should be displayed.
        """

        self.showSqrtAyanaTextFlag = flag
        
    def getShowSqrtAyanaTextFlag(self):
        """Returns the flag that indicates that the text for sqrt
        ayana (6 months) count of time should be displayed.
        """

        return self.showSqrtAyanaTextFlag

    def setShowSqrdAyanaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrd ayana
        (6 months) count of time should be displayed.
        """

        self.showSqrdAyanaTextFlag = flag
        
    def getShowSqrdAyanaTextFlag(self):
        """Returns the flag that indicates that the text for sqrd
        ayana (6 months) count of time should be displayed.
        """

        return self.showSqrdAyanaTextFlag

    def setShowMuhurtaTextFlag(self, flag):
        """Sets the flag that indicates that the text for muhurta (48
        minutes) count of time should be displayed.
        """

        self.showMuhurtaTextFlag = flag
        
    def getShowMuhurtaTextFlag(self):
        """Returns the flag that indicates that the text for muhurta
        (48 minutes) count of time should be displayed.
        """

        return self.showMuhurtaTextFlag

    def setShowSqrtMuhurtaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrt muhurta
        (48 minutes) count of time should be displayed.
        """

        self.showSqrtMuhurtaTextFlag = flag
        
    def getShowSqrtMuhurtaTextFlag(self):
        """Returns the flag that indicates that the text for sqrt
        muhurta (48 minutes) count of time should be displayed.
        """

        return self.showSqrtMuhurtaTextFlag

    def setShowSqrdMuhurtaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrd muhurta
        (48 minutes) count of time should be displayed.
        """

        self.showSqrdMuhurtaTextFlag = flag
        
    def getShowSqrdMuhurtaTextFlag(self):
        """Returns the flag that indicates that the text for sqrd
        muhurta (48 minutes) count of time should be displayed.
        """

        return self.showSqrdMuhurtaTextFlag

    def setShowVaraTextFlag(self, flag):
        """Sets the flag that indicates that the text for vara
        (24-hour day) count of time should be displayed.
        """

        self.showVaraTextFlag = flag
        
    def getShowVaraTextFlag(self):
        """Returns the flag that indicates that the text for vara
        (24-hour day) count of time should be displayed.
        """

        return self.showVaraTextFlag

    def setShowSqrtVaraTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrt vara
        (24-hour day) count of time should be displayed.
        """

        self.showSqrtVaraTextFlag = flag
        
    def getShowSqrtVaraTextFlag(self):
        """Returns the flag that indicates that the text for sqrt vara
        (24-hour day) count of time should be displayed.
        """

        return self.showSqrtVaraTextFlag

    def setShowSqrdVaraTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrd vara
        (24-hour day) count of time should be displayed.
        """

        self.showSqrdVaraTextFlag = flag
        
    def getShowSqrdVaraTextFlag(self):
        """Returns the flag that indicates that the text for sqrd vara
        (24-hour day) count of time should be displayed.
        """

        return self.showSqrdVaraTextFlag

    def setShowRtuTextFlag(self, flag):
        """Sets the flag that indicates that the text for rtu (season
        of 2 months) count of time should be displayed.
        """

        self.showRtuTextFlag = flag
        
    def getShowRtuTextFlag(self):
        """Returns the flag that indicates that the text for rtu
        (season of 2 months) count of time should be displayed.
        """

        return self.showRtuTextFlag

    def setShowSqrtRtuTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrt rtu
        (season of 2 months) count of time should be displayed.
        """

        self.showSqrtRtuTextFlag = flag
        
    def getShowSqrtRtuTextFlag(self):
        """Returns the flag that indicates that the text for sqrt rtu
        (season of 2 months) count of time should be displayed.
        """

        return self.showSqrtRtuTextFlag

    def setShowSqrdRtuTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrd rtu
        (season of 2 months) count of time should be displayed.
        """

        self.showSqrdRtuTextFlag = flag
        
    def getShowSqrdRtuTextFlag(self):
        """Returns the flag that indicates that the text for sqrd rtu
        (season of 2 months) count of time should be displayed.
        """

        return self.showSqrdRtuTextFlag

    def setShowMasaTextFlag(self, flag):
        """Sets the flag that indicates that the text for masa
        (full-moon to full-moon month) count of time should be
        displayed.
        """

        self.showMasaTextFlag = flag
        
    def getShowMasaTextFlag(self):
        """Returns the flag that indicates that the text for masa
        (full-moon to full-moon month) count of time should be
        displayed.
        """

        return self.showMasaTextFlag

    def setShowSqrtMasaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrt masa
        (full-moon to full-moon month) count of time should be
        displayed.
        """

        self.showSqrtMasaTextFlag = flag
        
    def getShowSqrtMasaTextFlag(self):
        """Returns the flag that indicates that the text for sqrt masa
        (full-moon to full-moon month) count of time should be
        displayed.
        """

        return self.showSqrtMasaTextFlag

    def setShowSqrdMasaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrd masa
        (full-moon to full-moon month) count of time should be
        displayed.
        """

        self.showSqrdMasaTextFlag = flag
        
    def getShowSqrdMasaTextFlag(self):
        """Returns the flag that indicates that the text for sqrd masa
        (full-moon to full-moon month) count of time should be
        displayed.
        """

        return self.showSqrdMasaTextFlag

    def setShowPaksaTextFlag(self, flag):
        """Sets the flag that indicates that the text for paksa
        (15-day fortnight) count of time should be displayed.
        """

        self.showPaksaTextFlag = flag
        
    def getShowPaksaTextFlag(self):
        """Returns the flag that indicates that the text for paksa
        (15-day fortnight) count of time should be displayed.
        """

        return self.showPaksaTextFlag

    def setShowSqrtPaksaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrt paksa
        (15-day fortnight) count of time should be displayed.
        """

        self.showSqrtPaksaTextFlag = flag
        
    def getShowSqrtPaksaTextFlag(self):
        """Returns the flag that indicates that the text for sqrt
        paksa (15-day fortnight) count of time should be displayed.
        """

        return self.showSqrtPaksaTextFlag

    def setShowSqrdPaksaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrd paksa
        (15-day fortnight) count of time should be displayed.
        """

        self.showSqrdPaksaTextFlag = flag
        
    def getShowSqrdPaksaTextFlag(self):
        """Returns the flag that indicates that the text for sqrd
        paksa (15-day fortnight) count of time should be displayed.
        """

        return self.showSqrdPaksaTextFlag

    def setShowSamaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sama (year) count
        of time should be displayed.
        """

        self.showSamaTextFlag = flag
        
    def getShowSamaTextFlag(self):
        """Returns the flag that indicates that the text for sama
        (year) count of time should be displayed.
        """

        return self.showSamaTextFlag

    def setShowSqrtSamaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrt sama
        (year) count of time should be displayed.
        """

        self.showSqrtSamaTextFlag = flag
        
    def getShowSqrtSamaTextFlag(self):
        """Returns the flag that indicates that the text for sqrt sama
        (year) count of time should be displayed.
        """

        return self.showSqrtSamaTextFlag

    def setShowSqrdSamaTextFlag(self, flag):
        """Sets the flag that indicates that the text for sqrd sama
        (year) count of time should be displayed.
        """

        self.showSqrdSamaTextFlag = flag
        
    def getShowSqrdSamaTextFlag(self):
        """Returns the flag that indicates that the text for sqrd sama
        (year) count of time should be displayed.
        """

        return self.showSqrdSamaTextFlag

    def setStartPointF(self, startPointF):
        """Stores the starting point of the TimeMeasurementArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the TimeMeasurementArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the TimeMeasurementArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the TimeMeasurementArtifact."""
        
        return self.endPointF
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartTimeMeasurementArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartTimeMeasurementArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartTimeModalScaleArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartTimeModalScaleArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "TimeModalScale_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultTimeModalScaleGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the TimeModalScaleArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the TimeModalScaleArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the TimeModalScaleArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the TimeModalScaleArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        #self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        #self.log.debug("startPoint is: ({}, {})".
        #               format(startPointX, startPointY))
        #self.log.debug("endPoint is: ({}, {})".
        #               format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        #self.log.debug("deltaX is: {}".format(deltaX))
        #self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        #self.log.debug("There are {} number of musical ratios.".\
        #               format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            #self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
            #               format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                #self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                #               format(xOffset, yOffset))
                
            if i == index:
                #self.log.debug("At the i == index, where i == {}.".format(i))
                #self.log.debug("MusicalRatio is: {}".\
                #               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                #self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                #self.log.debug("Adjusting to start points, (x={}, y={})".
                #               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                #self.log.debug("For index {}, ".format(i) +
                #               "normalized x and y from startPoint is: " +
                #               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        #self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
        #               "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartTimeModalScaleArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartTimeModalScaleArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartPriceModalScaleArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartPriceModalScaleArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "PriceModalScale_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used ratios.
        self.musicalRatios = MusicalRatio.getIndianMusicalRatios()
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextColor

        # barWidth (float).
        self.barWidth = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemBarWidth

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultPriceModalScaleGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the PriceModalScaleArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the PriceModalScaleArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the PriceModalScaleArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the PriceModalScaleArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarWidth(self, barWidth):
        """Sets the bar width (float)."""

        self.barWidth = barWidth
    
    def getBarWidth(self):
        """Returns the bar width (float)."""

        return self.barWidth
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        #self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        #self.log.debug("startPoint is: ({}, {})".
        #               format(startPointX, startPointY))
        #self.log.debug("endPoint is: ({}, {})".
        #               format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        #self.log.debug("deltaX is: {}".format(deltaX))
        #self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        #self.log.debug("There are {} number of musical ratios.".\
        #               format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            #self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
            #               format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                #self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                #               format(xOffset, yOffset))
                
            if i == index:
                #self.log.debug("At the i == index, where i == {}.".format(i))
                #self.log.debug("MusicalRatio is: {}".\
                #               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                #self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                #self.log.debug("For index {}, ".format(i) +
                #               "normalized x and y from startPoint is: " +
                #               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        #self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
        #               "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartPriceModalScaleArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartPriceModalScaleArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartPlanetLongitudeMovementMeasurementArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the planet longitude
    movement measurement starting at the given PriceBar timestamp and
    the given Y offset from the center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 5

        # Create the logger.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartPlanetLongitudeMovementMeasurementArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = \
            "PlanetLongitudeMovementMeasurement_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTextYScaling
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription
        
        # QColor can be pickled   
        self.textColor = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultTextColor

        # QColor can be pickled   
        self.color = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemBarHeight

        # Text rotation angle, in degrees (float).
        self.textRotationAngle = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTextRotationAngle

        # Flag for measuring planet geocentric longitude movement,
        # where retrograde movements count as zero.
        self.showGeocentricRetroAsZeroTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag
        
        # Flag for measuring planet geocentric longitude movement,
        # where retrograde movements count as positive values.
        self.showGeocentricRetroAsPositiveTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag
        
        # Flag for measuring planet geocentric longitude movement,
        # where retrograde movements count as negative values.
        self.showGeocentricRetroAsNegativeTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag
        
        # Flag for measuring planet heliocentric longitude movement.
        self.showHeliocentricTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag
        
        # Flag for using the tropical zodiac in measurements.
        self.tropicalZodiacFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag
        
        # Flag for using the sidereal zodiac in measurements.
        self.siderealZodiacFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag
        
        # Flag for displaying measurements in degrees.
        self.measurementUnitDegreesEnabled = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled
        
        # Flag for displaying measurements in number of circles.
        self.measurementUnitCirclesEnabled = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled
        
        # Flag for displaying measurements in number of biblical circles.
        self.measurementUnitBiblicalCirclesEnabled = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled
        
        # Flag for measurement of planet H1 enabled.
        self.planetH1EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag
        
        # Flag for measurement of planet H2 enabled.
        self.planetH2EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag
        
        # Flag for measurement of planet H3 enabled.
        self.planetH3EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag
        
        # Flag for measurement of planet H4 enabled.
        self.planetH4EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag
        
        # Flag for measurement of planet H5 enabled.
        self.planetH5EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag
        
        # Flag for measurement of planet H6 enabled.
        self.planetH6EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag
        
        # Flag for measurement of planet H7 enabled.
        self.planetH7EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag
        
        # Flag for measurement of planet H8 enabled.
        self.planetH8EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag
        
        # Flag for measurement of planet H9 enabled.
        self.planetH9EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag
        
        # Flag for measurement of planet H10 enabled.
        self.planetH10EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag
        
        # Flag for measurement of planet H11 enabled.
        self.planetH11EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag
        
        # Flag for measurement of planet H12 enabled.
        self.planetH12EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag
        
        # Flag for measurement of planet ARMC enabled.
        self.planetARMCEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag
        
        # Flag for measurement of planet Vertex enabled.
        self.planetVertexEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag
        
        # Flag for measurement of planet EquatorialAscendant enabled.
        self.planetEquatorialAscendantEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag
        
        # Flag for measurement of planet CoAscendant1 enabled.
        self.planetCoAscendant1EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag
        
        # Flag for measurement of planet CoAscendant2 enabled.
        self.planetCoAscendant2EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag
        
        # Flag for measurement of planet PolarAscendant enabled.
        self.planetPolarAscendantEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag
        
        # Flag for measurement of planet HoraLagna enabled.
        self.planetHoraLagnaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag
        
        # Flag for measurement of planet GhatiLagna enabled.
        self.planetGhatiLagnaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag
        
        # Flag for measurement of planet MeanLunarApogee enabled.
        self.planetMeanLunarApogeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag
        
        # Flag for measurement of planet OsculatingLunarApogee enabled.
        self.planetOsculatingLunarApogeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag
        
        # Flag for measurement of planet InterpolatedLunarApogee enabled.
        self.planetInterpolatedLunarApogeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag
        
        # Flag for measurement of planet InterpolatedLunarPerigee enabled.
        self.planetInterpolatedLunarPerigeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag
        
        # Flag for measurement of planet Sun enabled.
        self.planetSunEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag
        
        # Flag for measurement of planet Moon enabled.
        self.planetMoonEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag
        
        # Flag for measurement of planet Mercury enabled.
        self.planetMercuryEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag
        
        # Flag for measurement of planet Venus enabled.
        self.planetVenusEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag
        
        # Flag for measurement of planet Earth enabled.
        self.planetEarthEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag
        
        # Flag for measurement of planet Mars enabled.
        self.planetMarsEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag
        
        # Flag for measurement of planet Jupiter enabled.
        self.planetJupiterEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag
        
        # Flag for measurement of planet Saturn enabled.
        self.planetSaturnEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag
        
        # Flag for measurement of planet Uranus enabled.
        self.planetUranusEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag
        
        # Flag for measurement of planet Neptune enabled.
        self.planetNeptuneEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag
        
        # Flag for measurement of planet Pluto enabled.
        self.planetPlutoEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag
        
        # Flag for measurement of planet MeanNorthNode enabled.
        self.planetMeanNorthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag
        
        # Flag for measurement of planet MeanSouthNode enabled.
        self.planetMeanSouthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag
        
        # Flag for measurement of planet TrueNorthNode enabled.
        self.planetTrueNorthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag
        
        # Flag for measurement of planet TrueSouthNode enabled.
        self.planetTrueSouthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag
        
        # Flag for measurement of planet Ceres enabled.
        self.planetCeresEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag
        
        # Flag for measurement of planet Pallas enabled.
        self.planetPallasEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag
        
        # Flag for measurement of planet Juno enabled.
        self.planetJunoEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag
        
        # Flag for measurement of planet Vesta enabled.
        self.planetVestaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag
        
        # Flag for measurement of planet Isis enabled.
        self.planetIsisEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag
        
        # Flag for measurement of planet Nibiru enabled.
        self.planetNibiruEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag
        
        # Flag for measurement of planet Chiron enabled.
        self.planetChironEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag
        
        # Flag for measurement of planet Gulika enabled.
        self.planetGulikaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag
        
        # Flag for measurement of planet Mandi enabled.
        self.planetMandiEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag
        
        # Flag for measurement of planet MeanOfFive enabled.
        self.planetMeanOfFiveEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag
        
        # Flag for measurement of planet CycleOfEight enabled.
        self.planetCycleOfEightEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag
        
        # Flag for measurement of planet AvgMaJuSaUrNePl enabled.
        self.planetAvgMaJuSaUrNePlEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag
        
        # Flag for measurement of planet AvgJuSaUrNe enabled.
        self.planetAvgJuSaUrNeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag
        
        # Flag for measurement of planet AvgJuSa enabled.
        self.planetAvgJuSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag
        
        # Flag for measurement of planet MoSu enabled.
        self.planetMoSuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag
        
        # Flag for measurement of planet MeVe enabled.
        self.planetMeVeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag
        
        # Flag for measurement of planet MeEa enabled.
        self.planetMeEaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag
        
        # Flag for measurement of planet MeMa enabled.
        self.planetMeMaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag
        
        # Flag for measurement of planet MeJu enabled.
        self.planetMeJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag
        
        # Flag for measurement of planet MeSa enabled.
        self.planetMeSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag
        
        # Flag for measurement of planet MeUr enabled.
        self.planetMeUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag
        
        # Flag for measurement of planet VeEa enabled.
        self.planetVeEaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag
        
        # Flag for measurement of planet VeMa enabled.
        self.planetVeMaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag
        
        # Flag for measurement of planet VeJu enabled.
        self.planetVeJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag
        
        # Flag for measurement of planet VeSa enabled.
        self.planetVeSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag
        
        # Flag for measurement of planet VeUr enabled.
        self.planetVeUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag
        
        # Flag for measurement of planet EaMa enabled.
        self.planetEaMaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag
        
        # Flag for measurement of planet EaJu enabled.
        self.planetEaJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag
        
        # Flag for measurement of planet EaSa enabled.
        self.planetEaSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag
        
        # Flag for measurement of planet EaUr enabled.
        self.planetEaUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag
        
        # Flag for measurement of planet MaJu enabled.
        self.planetMaJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag
        
        # Flag for measurement of planet MaSa enabled.
        self.planetMaSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag
        
        # Flag for measurement of planet MaUr enabled.
        self.planetMaUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag
        
        # Flag for measurement of planet JuSa enabled.
        self.planetJuSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag
        
        # Flag for measurement of planet JuUr enabled.
        self.planetJuUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag
        
        # Flag for measurement of planet SaUr enabled.
        self.planetSaUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag
        
        
    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setTextColor(self, textColor):
        """Sets the color for this artifact's text.

        Arguments:
        textColor - QColor object holding the color of the text.
        """

        self.textColor = textColor

    def getTextColor(self):
        """Returns the color of this artifact's text as a QColor."""

        return self.textColor

    def setColor(self, color):
        """Sets the color for this artifact.

        Arguments:
        color - QColor object holding the color of the text.
        """

        self.color = color

    def getColor(self):
        """Returns the color of this artifact as a QColor."""

        return self.color

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the PlanetLongitudeMovementMeasurementArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the PlanetLongitudeMovementMeasurementArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the PlanetLongitudeMovementMeasurementArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the PlanetLongitudeMovementMeasurementArtifact."""
        
        return self.endPointF

    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setTextRotationAngle(self, textRotationAngle):
        """Sets the text rotation angle.

        Arguments:
        textRotationAngle - float value for the rotation angle of the text.
                            0.0 is the same as no rotation.
        """

        self.textRotationAngle = textRotationAngle

    def getTextRotationAngle(self):
        """Returns float value for the text rotation angle.  A value
        of 0.0 refers to no rotation.
        """

        return self.textRotationAngle
        
    def setGeocentricRetroAsZeroTextFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as zero.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.showGeocentricRetroAsZeroTextFlag = flag
        
    def getGeocentricRetroAsZeroTextFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as zero.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.showGeocentricRetroAsZeroTextFlag

    def setGeocentricRetroAsPositiveTextFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as positive.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.showGeocentricRetroAsPositiveTextFlag = flag
        
    def getGeocentricRetroAsPositiveTextFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as positive.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.showGeocentricRetroAsPositiveTextFlag

    def setGeocentricRetroAsNegativeTextFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as negative.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.showGeocentricRetroAsNegativeTextFlag = flag
        
    def getGeocentricRetroAsNegativeTextFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as negative.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.showGeocentricRetroAsNegativeTextFlag

    def setHeliocentricTextFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as negative.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.showHeliocentricTextFlag = flag
        
    def getHeliocentricTextFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement should be measured, where retrograde
        movements count as negative.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.showHeliocentricTextFlag

    def setTropicalZodiacFlag(self, flag):
        """Sets the flag that indicates that the tropical zodiac
        should be used in measurements.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.tropicalZodiacFlag = flag
        
    def getTropicalZodiacFlag(self):
        """Returns the flag that indicates that the tropical zodiac
        should be used in measurements.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.tropicalZodiacFlag

    def setSiderealZodiacFlag(self, flag):
        """Sets the flag that indicates that the sidereal zodiac
        should be used in measurements.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.siderealZodiacFlag = flag
        
    def getSiderealZodiacFlag(self):
        """Returns the flag that indicates that the sidereal zodiac
        should be used in measurements.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.siderealZodiacFlag

    def setMeasurementUnitDegreesEnabled(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed in units
        of degrees.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.measurementUnitDegreesEnabled = flag
        
    def getMeasurementUnitDegreesEnabled(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed in units
        of degrees.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.measurementUnitDegreesEnabled

    def setMeasurementUnitCirclesEnabled(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed in units
        of circles.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.measurementUnitCirclesEnabled = flag
        
    def getMeasurementUnitCirclesEnabled(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed in units
        of circles.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.measurementUnitCirclesEnabled

    def setMeasurementUnitBiblicalCirclesEnabled(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed in units
        of biblical circles.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.measurementUnitBiblicalCirclesEnabled = flag
        
    def getMeasurementUnitBiblicalCirclesEnabled(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed in units
        of biblical circles.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.measurementUnitBiblicalCirclesEnabled

    def setPlanetH1EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH1EnabledFlag = flag
        
    def getPlanetH1EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH1EnabledFlag

    def setPlanetH2EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH2EnabledFlag = flag
        
    def getPlanetH2EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH2EnabledFlag

    def setPlanetH3EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH3EnabledFlag = flag
        
    def getPlanetH3EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH3EnabledFlag

    def setPlanetH4EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH4EnabledFlag = flag
        
    def getPlanetH4EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH4EnabledFlag

    def setPlanetH5EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH5EnabledFlag = flag
        
    def getPlanetH5EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH5EnabledFlag

    def setPlanetH6EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH6EnabledFlag = flag
        
    def getPlanetH6EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH6EnabledFlag

    def setPlanetH7EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH7EnabledFlag = flag
        
    def getPlanetH7EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH7EnabledFlag

    def setPlanetH8EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH8EnabledFlag = flag
        
    def getPlanetH8EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH8EnabledFlag

    def setPlanetH9EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH9EnabledFlag = flag
        
    def getPlanetH9EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH9EnabledFlag

    def setPlanetH10EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH10EnabledFlag = flag
        
    def getPlanetH10EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH10EnabledFlag

    def setPlanetH11EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH11EnabledFlag = flag
        
    def getPlanetH11EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH11EnabledFlag

    def setPlanetH12EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetH12EnabledFlag = flag
        
    def getPlanetH12EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetH12EnabledFlag

    def setPlanetARMCEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetARMCEnabledFlag = flag
        
    def getPlanetARMCEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetARMCEnabledFlag

    def setPlanetVertexEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVertexEnabledFlag = flag
        
    def getPlanetVertexEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVertexEnabledFlag

    def setPlanetEquatorialAscendantEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetEquatorialAscendantEnabledFlag = flag
        
    def getPlanetEquatorialAscendantEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetEquatorialAscendantEnabledFlag

    def setPlanetCoAscendant1EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetCoAscendant1EnabledFlag = flag
        
    def getPlanetCoAscendant1EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetCoAscendant1EnabledFlag

    def setPlanetCoAscendant2EnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetCoAscendant2EnabledFlag = flag
        
    def getPlanetCoAscendant2EnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetCoAscendant2EnabledFlag

    def setPlanetPolarAscendantEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetPolarAscendantEnabledFlag = flag
        
    def getPlanetPolarAscendantEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetPolarAscendantEnabledFlag

    def setPlanetHoraLagnaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetHoraLagnaEnabledFlag = flag
        
    def getPlanetHoraLagnaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetHoraLagnaEnabledFlag

    def setPlanetGhatiLagnaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetGhatiLagnaEnabledFlag = flag
        
    def getPlanetGhatiLagnaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetGhatiLagnaEnabledFlag

    def setPlanetMeanLunarApogeeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeanLunarApogeeEnabledFlag = flag
        
    def getPlanetMeanLunarApogeeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeanLunarApogeeEnabledFlag

    def setPlanetOsculatingLunarApogeeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetOsculatingLunarApogeeEnabledFlag = flag
        
    def getPlanetOsculatingLunarApogeeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetOsculatingLunarApogeeEnabledFlag

    def setPlanetInterpolatedLunarApogeeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetInterpolatedLunarApogeeEnabledFlag = flag
        
    def getPlanetInterpolatedLunarApogeeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetInterpolatedLunarApogeeEnabledFlag

    def setPlanetInterpolatedLunarPerigeeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetInterpolatedLunarPerigeeEnabledFlag = flag
        
    def getPlanetInterpolatedLunarPerigeeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetInterpolatedLunarPerigeeEnabledFlag

    def setPlanetSunEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetSunEnabledFlag = flag
        
    def getPlanetSunEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetSunEnabledFlag

    def setPlanetMoonEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMoonEnabledFlag = flag
        
    def getPlanetMoonEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMoonEnabledFlag

    def setPlanetMercuryEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMercuryEnabledFlag = flag
        
    def getPlanetMercuryEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMercuryEnabledFlag

    def setPlanetVenusEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVenusEnabledFlag = flag
        
    def getPlanetVenusEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVenusEnabledFlag

    def setPlanetEarthEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetEarthEnabledFlag = flag
        
    def getPlanetEarthEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetEarthEnabledFlag

    def setPlanetMarsEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMarsEnabledFlag = flag
        
    def getPlanetMarsEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMarsEnabledFlag

    def setPlanetJupiterEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetJupiterEnabledFlag = flag
        
    def getPlanetJupiterEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetJupiterEnabledFlag

    def setPlanetSaturnEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetSaturnEnabledFlag = flag
        
    def getPlanetSaturnEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetSaturnEnabledFlag

    def setPlanetUranusEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetUranusEnabledFlag = flag
        
    def getPlanetUranusEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetUranusEnabledFlag

    def setPlanetNeptuneEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetNeptuneEnabledFlag = flag
        
    def getPlanetNeptuneEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetNeptuneEnabledFlag

    def setPlanetPlutoEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetPlutoEnabledFlag = flag
        
    def getPlanetPlutoEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetPlutoEnabledFlag

    def setPlanetMeanNorthNodeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeanNorthNodeEnabledFlag = flag
        
    def getPlanetMeanNorthNodeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeanNorthNodeEnabledFlag

    def setPlanetMeanSouthNodeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeanSouthNodeEnabledFlag = flag
        
    def getPlanetMeanSouthNodeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeanSouthNodeEnabledFlag

    def setPlanetTrueNorthNodeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetTrueNorthNodeEnabledFlag = flag
        
    def getPlanetTrueNorthNodeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetTrueNorthNodeEnabledFlag

    def setPlanetTrueSouthNodeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetTrueSouthNodeEnabledFlag = flag
        
    def getPlanetTrueSouthNodeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetTrueSouthNodeEnabledFlag

    def setPlanetCeresEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetCeresEnabledFlag = flag
        
    def getPlanetCeresEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetCeresEnabledFlag

    def setPlanetPallasEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetPallasEnabledFlag = flag
        
    def getPlanetPallasEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetPallasEnabledFlag

    def setPlanetJunoEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetJunoEnabledFlag = flag
        
    def getPlanetJunoEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetJunoEnabledFlag

    def setPlanetVestaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVestaEnabledFlag = flag
        
    def getPlanetVestaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVestaEnabledFlag

    def setPlanetIsisEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetIsisEnabledFlag = flag
        
    def getPlanetIsisEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetIsisEnabledFlag

    def setPlanetNibiruEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetNibiruEnabledFlag = flag
        
    def getPlanetNibiruEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetNibiruEnabledFlag

    def setPlanetChironEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetChironEnabledFlag = flag
        
    def getPlanetChironEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetChironEnabledFlag

    def setPlanetGulikaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetGulikaEnabledFlag = flag
        
    def getPlanetGulikaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetGulikaEnabledFlag

    def setPlanetMandiEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMandiEnabledFlag = flag
        
    def getPlanetMandiEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMandiEnabledFlag

    def setPlanetMeanOfFiveEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeanOfFiveEnabledFlag = flag
        
    def getPlanetMeanOfFiveEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeanOfFiveEnabledFlag

    def setPlanetCycleOfEightEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetCycleOfEightEnabledFlag = flag
        
    def getPlanetCycleOfEightEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetCycleOfEightEnabledFlag

    def setPlanetAvgMaJuSaUrNePlEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetAvgMaJuSaUrNePlEnabledFlag = flag
        
    def getPlanetAvgMaJuSaUrNePlEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetAvgMaJuSaUrNePlEnabledFlag

    def setPlanetAvgJuSaUrNeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetAvgJuSaUrNeEnabledFlag = flag
        
    def getPlanetAvgJuSaUrNeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetAvgJuSaUrNeEnabledFlag

    def setPlanetAvgJuSaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetAvgJuSaEnabledFlag = flag
        
    def getPlanetAvgJuSaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetAvgJuSaEnabledFlag

    def setPlanetMoSuEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMoSuEnabledFlag = flag
        
    def getPlanetMoSuEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMoSuEnabledFlag

    def setPlanetMeVeEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeVeEnabledFlag = flag
        
    def getPlanetMeVeEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeVeEnabledFlag

    def setPlanetMeEaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeEaEnabledFlag = flag
        
    def getPlanetMeEaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeEaEnabledFlag

    def setPlanetMeMaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeMaEnabledFlag = flag
        
    def getPlanetMeMaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeMaEnabledFlag

    def setPlanetMeJuEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeJuEnabledFlag = flag
        
    def getPlanetMeJuEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeJuEnabledFlag

    def setPlanetMeSaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeSaEnabledFlag = flag
        
    def getPlanetMeSaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeSaEnabledFlag

    def setPlanetMeUrEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMeUrEnabledFlag = flag
        
    def getPlanetMeUrEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMeUrEnabledFlag

    def setPlanetVeEaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVeEaEnabledFlag = flag
        
    def getPlanetVeEaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVeEaEnabledFlag

    def setPlanetVeMaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVeMaEnabledFlag = flag
        
    def getPlanetVeMaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVeMaEnabledFlag

    def setPlanetVeJuEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVeJuEnabledFlag = flag
        
    def getPlanetVeJuEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVeJuEnabledFlag

    def setPlanetVeSaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVeSaEnabledFlag = flag
        
    def getPlanetVeSaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVeSaEnabledFlag

    def setPlanetVeUrEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetVeUrEnabledFlag = flag
        
    def getPlanetVeUrEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetVeUrEnabledFlag

    def setPlanetEaMaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetEaMaEnabledFlag = flag
        
    def getPlanetEaMaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetEaMaEnabledFlag

    def setPlanetEaJuEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetEaJuEnabledFlag = flag
        
    def getPlanetEaJuEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetEaJuEnabledFlag

    def setPlanetEaSaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetEaSaEnabledFlag = flag
        
    def getPlanetEaSaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetEaSaEnabledFlag

    def setPlanetEaUrEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetEaUrEnabledFlag = flag
        
    def getPlanetEaUrEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetEaUrEnabledFlag

    def setPlanetMaJuEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMaJuEnabledFlag = flag
        
    def getPlanetMaJuEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMaJuEnabledFlag

    def setPlanetMaSaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMaSaEnabledFlag = flag
        
    def getPlanetMaSaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMaSaEnabledFlag

    def setPlanetMaUrEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetMaUrEnabledFlag = flag
        
    def getPlanetMaUrEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetMaUrEnabledFlag

    def setPlanetJuSaEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetJuSaEnabledFlag = flag
        
    def getPlanetJuSaEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetJuSaEnabledFlag

    def setPlanetJuUrEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetJuUrEnabledFlag = flag
        
    def getPlanetJuUrEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetJuUrEnabledFlag

    def setPlanetSaUrEnabledFlag(self, flag):
        """Sets the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        self.planetSaUrEnabledFlag = flag
        
    def getPlanetSaUrEnabledFlag(self):
        """Returns the flag that indicates that the planet geocentric
        longitude movement measurements should be displayed for this
        planet.

        Arguments:
        flag - bool value for the enabled flag.
        """

        return self.planetSaUrEnabledFlag

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state

    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartPlanetLongitudeMovementMeasurementArtifact")

        # Update the object to the most current version if it is not current.
        if self.classVersion < 5:
            self.log.info("Detected an old class version of " + \
                          "PriceBarChartPlanetLongitudeMovementMeasurementArtifact (version {}).  ".\
                          format(self.classVersion))

            if self.classVersion == 1:
                # Version 2 fixed the mis-named variables for enabling
                # various planets.  These incorrect names had "show" in
                # the front, and were not declared in the initialization
                # function.
                # 
                # Version 2 also adds the following member variables:
                #
                # self.planetMeVeEnabledFlag
                # self.planetMeEaEnabledFlag
                # self.planetMeMaEnabledFlag
                # self.planetMeJuEnabledFlag
                # self.planetMeSaEnabledFlag
                # self.planetMeUrEnabledFlag
                # self.planetVeEaEnabledFlag
                # self.planetVeMaEnabledFlag
                # self.planetVeJuEnabledFlag
                # self.planetVeSaEnabledFlag
                # self.planetVeUrEnabledFlag
                # self.planetEaMaEnabledFlag
                # self.planetEaJuEnabledFlag
                # self.planetEaSaEnabledFlag
                # self.planetEaUrEnabledFlag
                # self.planetMaJuEnabledFlag
                # self.planetMaSaEnabledFlag
                # self.planetMaUrEnabledFlag
                # self.planetJuSaEnabledFlag
                # self.planetJuUrEnabledFlag
                # self.planetSaUrEnabledFlag
                #
    
                
                # Fix variables to use more correct names.
    
                try:
                    # Copy over the value to the new variable.
                    self.measurementUnitDegreesEnabled = \
                        self.showMeasurementUnitDegreesEnabled
                    del(self.showMeasurementUnitDegreesEnabled)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.measurementUnitDegreesEnabled = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled
                
                try:
                    # Copy over the value to the new variable.
                    self.measurementUnitCirclesEnabled = \
                        self.showMeasurementUnitCirclesEnabled
                    del(self.showMeasurementUnitCirclesEnabled)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.measurementUnitCirclesEnabled = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH1EnabledFlag = \
                        self.showPlanetH1EnabledFlag
                    del(self.showPlanetH1EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH1EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH2EnabledFlag = \
                        self.showPlanetH2EnabledFlag
                    del(self.showPlanetH2EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH2EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH3EnabledFlag = \
                        self.showPlanetH3EnabledFlag
                    del(self.showPlanetH3EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH3EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH4EnabledFlag = \
                        self.showPlanetH4EnabledFlag
                    del(self.showPlanetH4EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH4EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH5EnabledFlag = \
                        self.showPlanetH5EnabledFlag
                    del(self.showPlanetH5EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH5EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH6EnabledFlag = \
                        self.showPlanetH6EnabledFlag
                    del(self.showPlanetH6EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH6EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH7EnabledFlag = \
                        self.showPlanetH7EnabledFlag
                    del(self.showPlanetH7EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH7EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH8EnabledFlag = \
                        self.showPlanetH8EnabledFlag
                    del(self.showPlanetH8EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH8EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH9EnabledFlag = \
                        self.showPlanetH9EnabledFlag
                    del(self.showPlanetH9EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH9EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH10EnabledFlag = \
                        self.showPlanetH10EnabledFlag
                    del(self.showPlanetH10EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH10EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH11EnabledFlag = \
                        self.showPlanetH11EnabledFlag
                    del(self.showPlanetH11EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH11EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetH12EnabledFlag = \
                        self.showPlanetH12EnabledFlag
                    del(self.showPlanetH12EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetH12EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetARMCEnabledFlag = \
                        self.showPlanetARMCEnabledFlag
                    del(self.showPlanetARMCEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetARMCEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetVertexEnabledFlag = \
                        self.showPlanetVertexEnabledFlag
                    del(self.showPlanetVertexEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetVertexEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetEquatorialAscendantEnabledFlag = \
                        self.showPlanetEquatorialAscendantEnabledFlag
                    del(self.showPlanetEquatorialAscendantEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetEquatorialAscendantEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetCoAscendant1EnabledFlag = \
                        self.showPlanetCoAscendant1EnabledFlag
                    del(self.showPlanetCoAscendant1EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetCoAscendant1EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetCoAscendant2EnabledFlag = \
                        self.showPlanetCoAscendant2EnabledFlag
                    del(self.showPlanetCoAscendant2EnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetCoAscendant2EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag
    
                try:
                    # Copy over the value to the new variable.
                    self.planetPolarAscendantEnabledFlag = \
                        self.showPlanetPolarAscendantEnabledFlag
                    del(self.showPlanetPolarAscendantEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetPolarAscendantEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetHoraLagnaEnabledFlag = \
                        self.showPlanetHoraLagnaEnabledFlag
                    del(self.showPlanetHoraLagnaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetHoraLagnaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetGhatiLagnaEnabledFlag = \
                        self.showPlanetGhatiLagnaEnabledFlag
                    del(self.showPlanetGhatiLagnaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetGhatiLagnaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMeanLunarApogeeEnabledFlag = \
                        self.showPlanetMeanLunarApogeeEnabledFlag
                    del(self.showPlanetMeanLunarApogeeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMeanLunarApogeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetOsculatingLunarApogeeEnabledFlag = \
                        self.showPlanetOsculatingLunarApogeeEnabledFlag
                    del(self.showPlanetOsculatingLunarApogeeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetOsculatingLunarApogeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetInterpolatedLunarApogeeEnabledFlag = \
                        self.showPlanetInterpolatedLunarApogeeEnabledFlag
                    del(self.showPlanetInterpolatedLunarApogeeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetInterpolatedLunarApogeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetInterpolatedLunarPerigeeEnabledFlag = \
                        self.showPlanetInterpolatedLunarPerigeeEnabledFlag
                    del(self.showPlanetInterpolatedLunarPerigeeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetInterpolatedLunarPerigeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetSunEnabledFlag = \
                        self.showPlanetSunEnabledFlag
                    del(self.showPlanetSunEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetSunEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMoonEnabledFlag = \
                        self.showPlanetMoonEnabledFlag
                    del(self.showPlanetMoonEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMoonEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMercuryEnabledFlag = \
                        self.showPlanetMercuryEnabledFlag
                    del(self.showPlanetMercuryEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMercuryEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetVenusEnabledFlag = \
                        self.showPlanetVenusEnabledFlag
                    del(self.showPlanetVenusEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetVenusEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetEarthEnabledFlag = \
                        self.showPlanetEarthEnabledFlag
                    del(self.showPlanetEarthEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetEarthEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMarsEnabledFlag = \
                        self.showPlanetMarsEnabledFlag
                    del(self.showPlanetMarsEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMarsEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetJupiterEnabledFlag = \
                        self.showPlanetJupiterEnabledFlag
                    del(self.showPlanetJupiterEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetJupiterEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetSaturnEnabledFlag = \
                        self.showPlanetSaturnEnabledFlag
                    del(self.showPlanetSaturnEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetSaturnEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetUranusEnabledFlag = \
                        self.showPlanetUranusEnabledFlag
                    del(self.showPlanetUranusEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetUranusEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetNeptuneEnabledFlag = \
                        self.showPlanetNeptuneEnabledFlag
                    del(self.showPlanetNeptuneEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetNeptuneEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetPlutoEnabledFlag = \
                        self.showPlanetPlutoEnabledFlag
                    del(self.showPlanetPlutoEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetPlutoEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMeanNorthNodeEnabledFlag = \
                        self.showPlanetMeanNorthNodeEnabledFlag
                    del(self.showPlanetMeanNorthNodeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMeanNorthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMeanSouthNodeEnabledFlag = \
                        self.showPlanetMeanSouthNodeEnabledFlag
                    del(self.showPlanetMeanSouthNodeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMeanSouthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetTrueNorthNodeEnabledFlag = \
                        self.showPlanetTrueNorthNodeEnabledFlag
                    del(self.showPlanetTrueNorthNodeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetTrueNorthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetTrueSouthNodeEnabledFlag = \
                        self.showPlanetTrueSouthNodeEnabledFlag
                    del(self.showPlanetTrueSouthNodeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetTrueSouthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetCeresEnabledFlag = \
                        self.showPlanetCeresEnabledFlag
                    del(self.showPlanetCeresEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetCeresEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetPallasEnabledFlag = \
                        self.showPlanetPallasEnabledFlag
                    del(self.showPlanetPallasEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetPallasEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetJunoEnabledFlag = \
                        self.showPlanetJunoEnabledFlag
                    del(self.showPlanetJunoEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetJunoEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetVestaEnabledFlag = \
                        self.showPlanetVestaEnabledFlag
                    del(self.showPlanetVestaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetVestaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetIsisEnabledFlag = \
                        self.showPlanetIsisEnabledFlag
                    del(self.showPlanetIsisEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetIsisEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetNibiruEnabledFlag = \
                        self.showPlanetNibiruEnabledFlag
                    del(self.showPlanetNibiruEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetNibiruEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetChironEnabledFlag = \
                        self.showPlanetChironEnabledFlag
                    del(self.showPlanetChironEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetChironEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetGulikaEnabledFlag = \
                        self.showPlanetGulikaEnabledFlag
                    del(self.showPlanetGulikaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetGulikaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMandiEnabledFlag = \
                        self.showPlanetMandiEnabledFlag
                    del(self.showPlanetMandiEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMandiEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetMeanOfFiveEnabledFlag = \
                        self.showPlanetMeanOfFiveEnabledFlag
                    del(self.showPlanetMeanOfFiveEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetMeanOfFiveEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetCycleOfEightEnabledFlag = \
                        self.showPlanetCycleOfEightEnabledFlag
                    del(self.showPlanetCycleOfEightEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetCycleOfEightEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetAvgMaJuSaUrNePlEnabledFlag = \
                        self.showPlanetAvgMaJuSaUrNePlEnabledFlag
                    del(self.showPlanetAvgMaJuSaUrNePlEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetAvgMaJuSaUrNePlEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetAvgJuSaUrNeEnabledFlag = \
                        self.showPlanetAvgJuSaUrNeEnabledFlag
                    del(self.showPlanetAvgJuSaUrNeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetAvgJuSaUrNeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag
                
                try:
                    # Copy over the value to the new variable.
                    self.planetAvgJuSaEnabledFlag = \
                        self.showPlanetAvgJuSaEnabledFlag
                    del(self.showPlanetAvgJuSaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.planetAvgJuSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag
                
    
                # Handle variables that were added in this version.
                try:
                    # See if the variables are set.
                    self.planetMeVeEnabledFlag
                    self.planetMeEaEnabledFlag
                    self.planetMeMaEnabledFlag
                    self.planetMeJuEnabledFlag
                    self.planetMeSaEnabledFlag
                    self.planetMeUrEnabledFlag
                    self.planetVeEaEnabledFlag
                    self.planetVeMaEnabledFlag
                    self.planetVeJuEnabledFlag
                    self.planetVeSaEnabledFlag
                    self.planetVeUrEnabledFlag
                    self.planetEaMaEnabledFlag
                    self.planetEaJuEnabledFlag
                    self.planetEaSaEnabledFlag
                    self.planetEaUrEnabledFlag
                    self.planetMaJuEnabledFlag
                    self.planetMaSaEnabledFlag
                    self.planetMaUrEnabledFlag
                    self.planetJuSaEnabledFlag
                    self.planetJuUrEnabledFlag
                    self.planetSaUrEnabledFlag
                    
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")
                    
                except AttributeError:
                    # Variables were not set.  Set them to the default
                    # values.
                    
                    self.planetMeVeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag
                    
                    self.planetMeEaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag
                    
                    self.planetMeMaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag
                    
                    self.planetMeJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag
                    
                    self.planetMeSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag
                    
                    self.planetMeUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag
                    
                    self.planetVeEaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag
                    
                    self.planetVeMaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag
                    
                    self.planetVeJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag
                    
                    self.planetVeSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag
                    
                    self.planetVeUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag
                    
                    self.planetEaMaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag
                    
                    self.planetEaJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag
                    
                    self.planetEaSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag
                    
                    self.planetEaUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag
                    
                    self.planetMaJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag
                    
                    self.planetMaSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag
                    
                    self.planetMaUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag
                    
                    self.planetJuSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag
                    
                    self.planetJuUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag
                    
                    self.planetSaUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag
                    
                    
                    self.log.debug("Added fields " + \
                                   "'self.planetMeVeEnabledFlag', " + \
                                   "'self.planetMeEaEnabledFlag', " + \
                                   "'self.planetMeMaEnabledFlag', " + \
                                   "'self.planetMeJuEnabledFlag', " + \
                                   "'self.planetMeSaEnabledFlag', " + \
                                   "'self.planetMeUrEnabledFlag', " + \
                                   "'self.planetVeEaEnabledFlag', " + \
                                   "'self.planetVeMaEnabledFlag', " + \
                                   "'self.planetVeJuEnabledFlag', " + \
                                   "'self.planetVeSaEnabledFlag', " + \
                                   "'self.planetVeUrEnabledFlag', " + \
                                   "'self.planetEaMaEnabledFlag', " + \
                                   "'self.planetEaJuEnabledFlag', " + \
                                   "'self.planetEaSaEnabledFlag', " + \
                                   "'self.planetEaUrEnabledFlag', " + \
                                   "'self.planetMaJuEnabledFlag', " + \
                                   "'self.planetMaSaEnabledFlag', " + \
                                   "'self.planetMaUrEnabledFlag', " + \
                                   "'self.planetJuSaEnabledFlag', " + \
                                   "'self.planetJuUrEnabledFlag', " + \
                                   "'self.planetSaUrEnabledFlag', " + \
                                   "to the loaded object.")
                
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 2
                                  
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 2:
                # Version 3 adds the following member variables:
                #
                # self.measurementUnitBiblicalCirclesEnabled
                #
    
                try:
                    # See if the variable is set.
                    self.measurementUnitBiblicalCirclesEnabled
    
                    # If it got here, then the field is already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have this field.")
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # Use the default value.
                    self.measurementUnitBiblicalCirclesEnabled = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled
    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 3
                                  
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 3:
                # Version 4 adds the following member variables:
                #
                # self.planetMoSuEnabledFlag
                #
    
                # Handle variables that were added in this version.
                try:
                    # See if the variable is set.
                    self.planetMoSuEnabledFlag
    
                    # If it got here, then the field is already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have this field.")
                except AttributeError:
                    # Variables were not set.  Set them to the default
                    # values.
                    
                    self.planetMoSuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag
                    
                    self.log.debug("Added field " + \
                                   "'self.planetMoSuEnabledFlag' " + \
                                   "to the loaded object.")
                                   
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 4
                                  
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 4:
                # Version 5 removed the following member variables:
                #
                # self.planetMeVeEaEnabledFlag
                # self.planetMeVeMaEnabledFlag
                # self.planetVeEaMeEnabledFlag
                # self.planetVeEaMaEnabledFlag
                # self.planetVeMaMeEnabledFlag
                # self.planetVeMaEaEnabledFlag
                # self.planetEaMaMeEnabledFlag
                # self.planetEaMaVeEnabledFlag
                # self.planetMaJuMeEnabledFlag
                # self.planetMaJuVeEnabledFlag
                # self.planetMaJuEaEnabledFlag
                # self.planetEaJuMeEnabledFlag
                # self.planetEaJuVeEnabledFlag
                # self.planetEaSaMeEnabledFlag
                # self.planetEaSaVeEnabledFlag
                # self.planetEaSaMaEnabledFlag
                #

                try:
                    del(self.planetMeVeEaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetMeVeMaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetVeEaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetVeEaMaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetVeMaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetVeMaEaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetEaMaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetEaMaVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetMaJuMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetMaJuVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetMaJuEaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetEaJuMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetEaJuVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetEaSaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetEaSaVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass
                
                try:
                    del(self.planetEaSaMaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                self.log.debug("Removed fields " + \
                               "'self.planetMeVeEaEnabledFlag', " + \
                               "'self.planetMeVeMaEnabledFlag', " + \
                               "'self.planetVeEaMeEnabledFlag', " + \
                               "'self.planetVeEaMaEnabledFlag', " + \
                               "'self.planetVeMaMeEnabledFlag', " + \
                               "'self.planetVeMaEaEnabledFlag', " + \
                               "'self.planetEaMaMeEnabledFlag', " + \
                               "'self.planetEaMaVeEnabledFlag', " + \
                               "'self.planetMaJuMeEnabledFlag', " + \
                               "'self.planetMaJuVeEnabledFlag', " + \
                               "'self.planetMaJuEaEnabledFlag', " + \
                               "'self.planetEaJuMeEnabledFlag', " + \
                               "'self.planetEaJuVeEnabledFlag', " + \
                               "'self.planetEaSaMeEnabledFlag', " + \
                               "'self.planetEaSaVeEnabledFlag', " + \
                               "'self.planetEaSaMaEnabledFlag', " + \
                               "from the loaded object.")
                                   
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 5
                                  
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
                
        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartPlanetLongitudeMovementMeasurementArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartTextArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that is a piece of text in the 
    PriceBarChartWidget.
    """
    
    def __init__(self, text=""):
        """Initializes the PriceBarChartTextArtifact with
        the given values.
        """
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 2

        # Create the logger.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartTextArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "Text_" + str(self.uuid)

        # Holds the text that is displayed.
        self.text = text
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.defaultTextGraphicsItemDefaultFontDescription
        
        # QColor can be pickled   
        self.color = PriceBarChartSettings.defaultTextGraphicsItemDefaultColor
        
        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.defaultTextGraphicsItemDefaultXScaling
        self.textYScaling = \
            PriceBarChartSettings.defaultTextGraphicsItemDefaultYScaling

        # Rotation angle, in degrees.
        self.textRotationAngle = \
            PriceBarChartSettings.defaultTextGraphicsItemDefaultRotationAngle

    def setText(self, text):
        """Sets the text that makes up this PriceBarChartTextArtifact.

        Arguments:
        text - str value for the text to display.
        """

        self.text = text

    def getText(self):
        """Returns the text of this PriceBarChartTextArtifact as a str."""

        return self.text

    def setFont(self, font):
        """Sets the font of this PriceBarChartTextArtifact.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this PriceBarChartTextArtifact as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setColor(self, color):
        """Sets the text color for this PriceBarChartTextArtifact.

        Arguments:
        color - QColor object holding the color of the text.
        """

        self.color = color

    def getColor(self):
        """Returns the color of this PriceBarChartTextArtifact as a QColor."""

        return self.color

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setTextRotationAngle(self, textRotationAngle):
        """Sets the text rotation angle.

        Arguments:
        textRotationAngle - float value for the rotation angle of the text.
                            0.0 is the same as no rotation.
        """

        self.textRotationAngle = textRotationAngle

    def getTextRotationAngle(self):
        """Returns float value for the text rotation angle.  A value
        of 0.0 refers to no rotation.
        """

        return self.textRotationAngle
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()
        
    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartTextArtifact")

        # Update the object to the most current version if it is not current.
        if self.classVersion < 2:
            self.log.info("Detected an old class version of " + \
                          "PriceBarChartTextArtifact (version {}).  ".\
                          format(self.classVersion))

            if self.classVersion == 1:
                # Version 2 added member variable for
                # TextGraphicsItem default rotation angle.
                try:
                    # See if the variable is set.
                    self.textRotationAngle

                    # If it got here, then the field is already set.
                    self.log.warn("Hmm, strange.  Version 1 of this " + \
                                  "class shouldn't have this field.")
                    
                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.
                    self.textRotationAngle = \
                        PriceBarChartSettings.\
                        defaultTextGraphicsItemDefaultRotationAngle

                    self.log.debug("Added field 'textRotationAngle' " + \
                                  "to the loaded PriceBarChartTextArtifact.")

                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 2
                
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartTextArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartPriceTimeInfoArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that contains info about text that
    describes a certain point in time and price.
    """
    
    def __init__(self):
        """Initializes the PriceBarChartPriceTimeInfoArtifact with
        the given values.
        """
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartPriceTimeInfoArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "PriceTimeInfo_" + str(self.uuid)

        # Location of the point of the price and time info.
        self.infoPointF = QPointF()

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemDefaultFontDescription
        
        # QColor can be pickled   
        self.color = PriceBarChartSettings.\
                     defaultPriceTimeInfoGraphicsItemDefaultColor

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemDefaultXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemDefaultYScaling
        
        # Flags for what to show in the text.
        self.showTimestampFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowTimestampFlag
        
        self.showPriceFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowPriceFlag
        
        self.showSqrtPriceFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtPriceFlag
        
        self.showTimeElapsedSinceBirthFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag
        
        self.showSqrtTimeElapsedSinceBirthFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag

        self.showPriceScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowPriceScaledValueFlag
        
        self.showSqrtPriceScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag
        
        self.showTimeScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowTimeScaledValueFlag
        
        self.showSqrtTimeScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag
        
        # Flag to show the line from the text to the info point.
        self.showLineToInfoPointFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowLineToInfoPointFlag
        
        
    def setInfoPointF(self, infoPointF):
        """Sets the point of info for the price and time, as a QPointF
        in scene coordinates.

        Arguments:
        pointF - QPointF for the location of referenced price and time.
        """

        self.infoPointF = infoPointF

    def getInfoPointF(self):
        """Returns the QPointF for the location of the referenced
        price and time.
        """

        return self.infoPointF

    def setFont(self, font):
        """Sets the font of this PriceBarChartPriceTimeInfoArtifact.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this PriceBarChartPriceTimeInfoArtifact
        as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setColor(self, color):
        """Sets the text color for this PriceBarChartPriceTimeInfoArtifact.

        Arguments:
        color - QColor object holding the color of the text.
        """

        self.color = color

    def getColor(self):
        """Returns the color of this
        PriceBarChartPriceTimeInfoArtifact as a QColor."""

        return self.color

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setShowTimestampFlag(self, showTimestampFlag):
        """Sets the flag for showing the timestamp in the text."""

        self.showTimestampFlag = showTimestampFlag

    def getShowTimestampFlag(self):
        """Returns the flag for showing the timestamp in the text."""

        return self.showTimestampFlag
    
    def setShowPriceFlag(self, showPriceFlag):
        """Sets the flag for showing the price in the text."""

        self.showPriceFlag = showPriceFlag

    def getShowPriceFlag(self):
        """Returns the flag for showing the price in the text."""

        return self.showPriceFlag
    
    def setShowSqrtPriceFlag(self, showSqrtPriceFlag):
        """Sets the flag for showing the square root of price in the
        text.
        """

        self.showSqrtPriceFlag = showSqrtPriceFlag

    def getShowSqrtPriceFlag(self):
        """Returns the flag for showing the square root of price in
        the text.
        """

        return self.showSqrtPriceFlag
    
    def setShowTimeElapsedSinceBirthFlag(self, showTimeElapsedSinceBirthFlag):
        """Sets the flag for showing the time elapsed since birth in
        the text.
        """

        self.showTimeElapsedSinceBirthFlag = showTimeElapsedSinceBirthFlag

    def getShowTimeElapsedSinceBirthFlag(self):
        """Returns the flag for showing the time elapsed since birth
        in the text.
        """

        return self.showTimeElapsedSinceBirthFlag
    
    def setShowSqrtTimeElapsedSinceBirthFlag(\
        self, showSqrtTimeElapsedSinceBirthFlag):
        """Sets the flag for showing the square root of time elapsed
        since birth in the text.
        """

        self.showSqrtTimeElapsedSinceBirthFlag = \
            showSqrtTimeElapsedSinceBirthFlag

    def getShowSqrtTimeElapsedSinceBirthFlag(self):
        """Returns the flag for showing the square root of time
        elapsed since birth in the text.
        """

        return self.showSqrtTimeElapsedSinceBirthFlag

    def setShowPriceScaledValueFlag(self, showPriceScaledValueFlag):
        """Sets the flag for showing the price scaled value in the text."""

        self.showPriceScaledValueFlag = showPriceScaledValueFlag
        
    def getShowPriceScaledValueFlag(self):
        """Gets the flag for showing the price scaled value in the text."""

        return self.showPriceScaledValueFlag
        
    def setShowSqrtPriceScaledValueFlag(self, showSqrtPriceScaledValueFlag):
        """Sets the flag for showing the sqrt of price scaled value in
        the text.
        """

        self.showSqrtPriceScaledValueFlag = showSqrtPriceScaledValueFlag
        
    def getShowSqrtPriceScaledValueFlag(self):
        """Gets the flag for showing the sqrt of price scaled value in
        the text.
        """

        return self.showSqrtPriceScaledValueFlag
        
    def setShowTimeScaledValueFlag(self, showTimeScaledValueFlag):
        """Sets the flag for showing the time in scaled value units in
        the text."""

        self.showTimeScaledValueFlag = showTimeScaledValueFlag
        
    def getShowTimeScaledValueFlag(self):
        """Gets the flag for showing the time in scaled value units in
        the text."""

        return self.showTimeScaledValueFlag
        
    def setShowSqrtTimeScaledValueFlag(self, showSqrtTimeScaledValueFlag):
        """Sets the flag for showing the sqrt of time, in scaled value
        units in the text.
        """

        self.showSqrtTimeScaledValueFlag = showSqrtTimeScaledValueFlag
        
    def getShowSqrtTimeScaledValueFlag(self):
        """Gets the flag for showing the sqrt of time, in scaled value
        units in the text.
        """

        return self.showSqrtTimeScaledValueFlag
        
    def setShowLineToInfoPointFlag(self, showLineToInfoPointFlag):
        """Sets the flag for showing the line from the text to the info point.
        """

        self.showLineToInfoPointFlag = showLineToInfoPointFlag

    def getShowLineToInfoPointFlag(self):
        """Returns the flag for showing the line from the text to the
        info point.
        """

        return self.showLineToInfoPointFlag
    
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()
        
    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv
    
    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartPriceTimeInfoArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartTextArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartPriceMeasurementArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the price measurement starting 
    at the given start and end prices, given as two QPointFs.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartPriceMeasurementArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "PriceMeasurement_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemTextYScaling
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultFontDescription
        
        # QColor can be pickled   
        self.textColor = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultTextColor

        # QColor can be pickled   
        self.color = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultColor

        # Flags for displaying various text.
        self.showPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowPriceRangeTextFlag
        
        self.showSqrtPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag

        self.showScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowScaledValueRangeTextFlag

        self.showSqrtScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag
        
    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setTextColor(self, textColor):
        """Sets the color for this artifact's text.

        Arguments:
        textColor - QColor object holding the color of the text.
        """

        self.textColor = textColor

    def getTextColor(self):
        """Returns the color of this artifact's text as a QColor."""

        return self.textColor

    def setColor(self, color):
        """Sets the color for this artifact.

        Arguments:
        color - QColor object holding the color of the text.
        """

        self.color = color

    def getColor(self):
        """Returns the color of this artifact as a QColor."""

        return self.color

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setShowPriceRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the price
        range should be displayed.
        """

        self.showPriceRangeTextFlag = flag
        
    def getShowPriceRangeTextFlag(self):
        """Returns the flag that indicates that the text for the
        price range should be displayed.
        """

        return self.showPriceRangeTextFlag
        
    def setShowSqrtPriceRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of
        the price range should be displayed.
        """

        self.showSqrtPriceRangeTextFlag = flag
        
    def getShowSqrtPriceRangeTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt
        of the price range should be displayed.
        """

        return self.showSqrtPriceRangeTextFlag
        
    def setShowScaledValueRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the scaled
        value representing the price range should be displayed.
        """

        self.showScaledValueRangeTextFlag = flag
        
    def getShowScaledValueRangeTextFlag(self):
        """Returns the flag that indicates that the text for the
        scaled value representing the price range should be displayed.
        """

        return self.showScaledValueRangeTextFlag

    def setShowSqrtScaledValueRangeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the sqrt of scaled
        value representing the price range should be displayed.
        """

        self.showSqrtScaledValueRangeTextFlag = flag
        
    def getShowSqrtScaledValueRangeTextFlag(self):
        """Returns the flag that indicates that the text for the sqrt of
        scaled value representing the price range should be displayed.
        """

        return self.showSqrtScaledValueRangeTextFlag

    def setStartPointF(self, startPointF):
        """Stores the starting point of the PriceMeasurementArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the PriceMeasurementArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the PriceMeasurementArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the PriceMeasurementArtifact."""
        
        return self.endPointF
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartPriceMeasurementArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartPriceMeasurementArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartTimeRetracementArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time
    retracement starting at the given timestamp and the given ending
    timestamp.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartTimeRetracementArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "TimeRetracement_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemTextYScaling
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultFontDescription
        
        # QColor can be pickled
        self.textColor = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultTextColor

        # QColor can be pickled   
        self.color = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultColor

        # Flags for displaying various parts of the graphics item.
        self.showFullLines = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowFullLinesFlag

        self.showTimeText = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowTimeTextFlag
        
        self.showPercentText = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowPercentTextFlag

        # List of Ratio objects for the different ratios supported.
        self.ratios = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemRatios

    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setTextColor(self, textColor):
        """Sets the color for this artifact's text.

        Arguments:
        textColor - QColor object holding the color of the text.
        """

        self.textColor = textColor

    def getTextColor(self):
        """Returns the color of this artifact's text as a QColor."""

        return self.textColor

    def setColor(self, color):
        """Sets the color for this artifact.

        Arguments:
        color - QColor object holding the color of the text.
        """

        self.color = color

    def getColor(self):
        """Returns the color of this artifact as a QColor."""

        return self.color

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setShowFullLinesFlag(self, flag):
        """Sets the flag that indicates that the lines for the
        retracement should be displayed.
        """

        self.showFullLines = flag
        
    def getShowFullLinesFlag(self):
        """Returns the flag that indicates that the lines for the
        retracement should be displayed.
        """

        return self.showFullLines
        
    def setShowTimeTextFlag(self, flag):
        """Sets the flag that indicates that the text for the
        timestamp should be displayed.
        """

        self.showTimeText = flag
        
    def getShowTimeTextFlag(self):
        """Returns the flag that indicates that the text for the
        timestamp should be displayed.
        """

        return self.showTimeText
        
    def setShowPercentTextFlag(self, flag):
        """Sets the flag that indicates that the text for the
        timestamp should be displayed.
        """

        self.showPercentText = flag
        
    def getShowPercentTextFlag(self):
        """Returns the flag that indicates that the text for the
        timestamp should be displayed.
        """

        return self.showPercentText

    def setRatios(self, ratios):
        """Sets the list of Ratio objects, which is the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        self.ratios = ratios
    
    def getRatios(self):
        """Returns a list of Ratio objects, which holds the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        return self.ratios
    
    def setStartPointF(self, startPointF):
        """Stores the starting point of the TimeRetracementArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the TimeRetracementArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the TimeRetracementArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the TimeRetracementArtifact."""
        
        return self.endPointF
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartTimeRetracementArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartTimeRetracementArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartPriceRetracementArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the price
    retracement starting at the given price and the given ending
    price.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartPriceRetracementArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "PriceRetracement_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemTextYScaling
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultFontDescription
        
        # QColor can be pickled
        self.textColor = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultTextColor

        # QColor can be pickled   
        self.color = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultColor

        # Flags for displaying various parts of the graphics item.
        self.showFullLines = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowFullLinesFlag

        self.showPriceText = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowPriceTextFlag
        
        self.showPercentText = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowPercentTextFlag

        # List of Ratio objects for the different ratios supported.
        self.ratios = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemRatios

    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setTextColor(self, textColor):
        """Sets the color for this artifact's text.

        Arguments:
        textColor - QColor object holding the color of the text.
        """

        self.textColor = textColor

    def getTextColor(self):
        """Returns the color of this artifact's text as a QColor."""

        return self.textColor

    def setColor(self, color):
        """Sets the color for this artifact.

        Arguments:
        color - QColor object holding the color of the text.
        """

        self.color = color

    def getColor(self):
        """Returns the color of this artifact as a QColor."""

        return self.color

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setShowFullLinesFlag(self, flag):
        """Sets the flag that indicates that the lines for the
        retracement should be displayed.
        """

        self.showFullLines = flag
        
    def getShowFullLinesFlag(self):
        """Returns the flag that indicates that the lines for the
        retracement should be displayed.
        """

        return self.showFullLines
        
    def setShowPriceTextFlag(self, flag):
        """Sets the flag that indicates that the text for the
        pricestamp should be displayed.
        """

        self.showPriceText = flag
        
    def getShowPriceTextFlag(self):
        """Returns the flag that indicates that the text for the
        price should be displayed.
        """

        return self.showPriceText
        
    def setShowPercentTextFlag(self, flag):
        """Sets the flag that indicates that the text for the
        percent should be displayed.
        """

        self.showPercentText = flag
        
    def getShowPercentTextFlag(self):
        """Returns the flag that indicates that the text for the
        percent should be displayed.
        """

        return self.showPercentText

    def setRatios(self, ratios):
        """Sets the list of Ratio objects, which is the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        self.ratios = ratios
    
    def getRatios(self):
        """Returns a list of Ratio objects, which holds the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        return self.ratios
    
    def setStartPointF(self, startPointF):
        """Stores the starting point of the PriceRetracementArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the PriceRetracementArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the PriceRetracementArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the PriceRetracementArtifact."""
        
        return self.endPointF
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger(\
            "data_objects.PriceBarChartPriceRetracementArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartPriceRetracementArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartPriceTimeVectorArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the measurement of
    distance and distance squared of a vector.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartPriceTimeVectorArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "PriceTimeVector_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTextYScaling
        
        # priceTimeVectorGraphicsItemColor (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemColor

        # priceTimeVectorGraphicsItemTextColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemTextColor

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemDefaultFontDescription
        
        # Flag for whether or not the text is displayed for distance.
        self.showDistanceTextFlag = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemShowDistanceTextFlag
        
        # Flag for whether or not the text is displayed for distance.
        self.showSqrtDistanceTextFlag = \
            PriceBarChartSettings.\
                defaultPriceTimeVectorGraphicsItemShowSqrtDistanceTextFlag

        # Flag for whether or not the text is displayed for distance
        # in scaledValue units.
        self.showDistanceScaledValueTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag
        
        # Flag for whether or not the text is displayed for distance
        # in scaledValue units.
        self.showSqrtDistanceScaledValueTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag

        # Flag for whether or not to show the text as tilted at the
        # angle parallel to the line.
        self.tiltedTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTiltedTextFlag

        # Flag for whether or not to show the text holding the scaled
        # angle of the PriceTimeVector.
        self.angleTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemAngleTextFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the PriceTimeVectorArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the PriceTimeVectorArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the PriceTimeVectorArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the PriceTimeVectorArtifact."""
        
        return self.endPointF

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def getShowDistanceTextFlag(self):
        """Returns the showDistanceTextFlag."""

        return self.showDistanceTextFlag
        
    def setShowDistanceTextFlag(self, flag):
        """Sets a new value for the showDistanceTextFlag."""

        self.showDistanceTextFlag = flag
        
    def getShowSqrtDistanceTextFlag(self):
        """Returns the showSqrtDistanceTextFlag."""

        return self.showSqrtDistanceTextFlag
        
    def setShowSqrtDistanceTextFlag(self, flag):
        """Sets a new value for the showSqrtDistanceTextFlag."""

        self.showSqrtDistanceTextFlag = flag
        
    def getShowDistanceScaledValueTextFlag(self):
        """Returns the showDistanceScaledValueTextFlag."""

        return self.showDistanceScaledValueTextFlag
        
    def setShowDistanceScaledValueTextFlag(self, flag):
        """Sets a new value for the showDistanceScaledValueTextFlag."""

        self.showDistanceScaledValueTextFlag = flag
        
    def getShowSqrtDistanceScaledValueTextFlag(self):
        """Returns the showSqrtDistanceScaledValueTextFlag."""

        return self.showSqrtDistanceScaledValueTextFlag
        
    def setShowSqrtDistanceScaledValueTextFlag(self, flag):
        """Sets a new value for the showSqrtDistanceScaledValueTextFlag."""

        self.showSqrtDistanceScaledValueTextFlag = flag
        
    def getTiltedTextFlag(self):
        """Returns the tiltedTextFlag."""

        return self.tiltedTextFlag
        
    def setTiltedTextFlag(self, flag):
        """Sets a new value for the tiltedTextFlag."""

        self.tiltedTextFlag = flag
        
    def getAngleTextFlag(self):
        """Returns the angleTextFlag."""

        return self.angleTextFlag
        
    def setAngleTextFlag(self, flag):
        """Sets a new value for the angleTextFlag."""

        self.angleTextFlag = flag
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartPriceTimeVectorArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartPriceTimeVectorArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartLineSegmentArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates a line segment on the
    graphics scene.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartLineSegmentArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "LineSegment_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextYScaling
        
        # lineSegmentGraphicsItemColor (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemColor

        # lineSegmentGraphicsItemTextColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultLineSegmentGraphicsItemTextColor

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemDefaultFontDescription
        
        # Flag for whether or not to show the text as tilted at the
        # angle parallel to the line.
        self.tiltedTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTiltedTextFlag

        # Flag for whether or not to show the text holding the scaled
        # angle of the LineSegment.
        self.angleTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemAngleTextFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the LineSegmentArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the LineSegmentArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the LineSegmentArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the LineSegmentArtifact."""
        
        return self.endPointF

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def getTiltedTextFlag(self):
        """Returns the tiltedTextFlag."""

        return self.tiltedTextFlag
        
    def setTiltedTextFlag(self, flag):
        """Sets a new value for the tiltedTextFlag."""

        self.tiltedTextFlag = flag
        
    def getAngleTextFlag(self):
        """Returns the angleTextFlag."""

        return self.angleTextFlag
        
    def setAngleTextFlag(self, flag):
        """Sets a new value for the angleTextFlag."""

        self.angleTextFlag = flag
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartLineSegmentArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartLineSegmentArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartOctaveFanArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the the data elements of a
    OctaveFanGraphicsItem.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartOctaveFanArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "OctaveFan_" + str(self.uuid)

        # Origin point and the two leg points of the artifact.
        self.originPointF = QPointF()
        self.leg1PointF = QPointF()
        self.leg2PointF = QPointF()
        
        # List of used ratios.
        self.musicalRatios = MusicalRatio.getIndianMusicalRatios()
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemBarColor
        
        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextColor
        
        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = False
        
    def setOriginPointF(self, originPointF):
        """Stores the origin point of the OctaveFanArtifact.
        Arguments:

        originPointF - QPointF for the origin point of the artifact.
        """
        
        self.originPointF = originPointF
        
    def getOriginPointF(self):
        """Returns the origin point of the OctaveFanArtifact."""
        
        return self.originPointF
        
    def setLeg1PointF(self, leg1PointF):
        """Stores the leg1 point of the OctaveFanArtifact.
        Arguments:

        leg1PointF - QPointF for the leg1 point of the artifact.
        """
        
        self.leg1PointF = leg1PointF
        
    def getLeg1PointF(self):
        """Returns the leg1 point of the OctaveFanArtifact."""
        
        return self.leg1PointF

    def setLeg2PointF(self, leg2PointF):
        """Stores the leg2 point of the OctaveFanArtifact.
        Arguments:

        leg2PointF - QPointF for the leg2 point of the artifact.
        """
        
        self.leg2PointF = leg2PointF
        
    def getLeg2PointF(self):
        """Returns the leg2 point of the OctaveFanArtifact."""
        
        return self.leg2PointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self,
                             index, 
                             scaledOriginPointF,
                             scaledLeg1PointF,
                             scaledLeg2PointF):
        """Returns the x and y location of where this musical ratio
        point would exist, based on the MusicalRatio ordering and the
        scaledOriginPointF, scaledLeg1PointF, and scaledLeg2PointF
        locations.  This method does it's calculation based on 3
        points, and the point returned is along the outter edge of a
        bounding rectangle created by the 3 points.  The calculated point
        returned is based angular musical ratios.  

        Arguments:
        
        index - int value for index into self.musicalRatios that the
                user is looking for the musical ratio for.  This value
                must be within the valid index limits.
        scaledOriginPointF - Origin point of the octave fan, in scaled
                             coordinates.
        scaledLeg1PointF   - Leg1 point of the octave fan, in scaled
                             coordinates.
        scaledLeg2PointF   - Leg2 point of the octave fan, in scaled
                             coordinates.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point in scaled
        coordinates.  This is where the musical ratio would exist.
        The caller must then unscale it back to scene or local
        coordinates as needed.
        """

        #self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Get the musical ratios.
        musicalRatios = self.getMusicalRatios()
        
        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(musicalRatios) > 0 and index >= len(musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return


        # Return values.
        x = None
        y = None


        # Simple test cases when some points are the same value.
        if scaledOriginPointF == scaledLeg1PointF and \
           scaledOriginPointF == scaledLeg2PointF:

            # All three points the same.
            #self.log.debug("All three points are the same, so we will " +
            #               "return the same point as the position " +
            #               "of the musical ratio.")
            x = scaledOriginPointF.x()
            y = scaledOriginPointF.y()
            return (x, y)
        
        elif scaledOriginPointF == scaledLeg1PointF and \
             scaledOriginPointF != scaledLeg2PointF:

            # scaledOriginPointF and scaledLeg1PointF points are the same.
            #self.log.debug("scaledOriginPointF and scaledLeg1PointF " +
            #               "are equal, so we will" +
            #               "return the scaledLeg2PointF as the " +
            #               "position of the same point as the position " +
            #               "of the musical ratio.")
            x = scaledLeg2PointF.x()
            y = scaledLeg2PointF.y()
            return (x, y)

        elif scaledOriginPointF != scaledLeg1PointF and \
             scaledOriginPointF == scaledLeg2PointF:
            
            # scaledOriginPointF and scaledLeg2PointF points are the same.
            #self.log.debug("scaledOriginPointF and scaledLeg2PointF " +
            #               "are equal, so we will" +
            #               "return the scaledLeg1PointF as the " +
            #               "position of the same point as the position " +
            #               "of the musical ratio.")
            x = scaledLeg1PointF.x()
            y = scaledLeg1PointF.y()
            return (x, y)

        else:
            
            # All three points the different.
            self.log.debug("All three points are different, so " +
                           "continuing on to do the calculations.")

        #self.log.debug("scaledOriginPointF is: ({}, {})".\
        #               format(scaledOriginPointF.x(),
        #                      scaledOriginPointF.y()))
        #self.log.debug("scaledLeg1PointF is: ({}, {})".\
        #               format(scaledLeg1PointF.x(),
        #                      scaledLeg1PointF.y()))
        #self.log.debug("scaledLeg2PointF is: ({}, {})".\
        #               format(scaledLeg2PointF.x(),
        #                      scaledLeg2PointF.y()))

        # Calculate the angle between the two line segments.
        leg1 = QLineF(scaledOriginPointF, scaledLeg1PointF)
        leg2 = QLineF(scaledOriginPointF, scaledLeg2PointF)

        #self.log.debug("Angle of leg1 is: {}".format(leg1.angle()))
        #self.log.debug("Angle of leg2 is: {}".format(leg2.angle()))
        
        
        # The angle returned by QLineF.angleTo() is always normalized.
        angleDegDelta = leg1.angleTo(leg2)

        #self.log.debug("Angle of leg1 to leg2 is: " +
        #               "angleDegDelta == {} deg".format(angleDegDelta))
        
        # If the delta angle is greater than 180, then subtract 360
        # because we don't want to draw the fan on the undesired side
        # of the angle.
        if angleDegDelta > 180:
            angleDegDelta -= 360
        
        #self.log.debug("Adjusted angle difference is: " + \
        #               "angleDegDelta == {} deg".format(angleDegDelta))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        angleDegOffset = 0.0

        #self.log.debug("There are {} number of musical ratios.".\
        #               format(len(musicalRatios)))

        for i in range(len(musicalRatios)):
            musicalRatio = musicalRatios[i]
            
            #self.log.debug("musicalRatios[{}].getRatio() is: {}".\
            #               format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                angleDegOffset = \
                    angleDegDelta * (musicalRatio.getRatio() - 1.0)

                #self.log.debug("At i == 0.  angleDegOffset={}".\
                #               format(angleDegOffset))
                
            if i == index:
                #self.log.debug("At the i == index, where i == {}.".format(i))
                #self.log.debug("MusicalRatio is: {}".\
                #               format(musicalRatio.getRatio()))
                
                angleDeg = \
                    (angleDegDelta * (musicalRatio.getRatio() - 1.0)) - \
                    angleDegOffset

                #self.log.debug("(angleDeg={})".format(angleDeg))

                # If we are reversed, then reference the offset angle
                # from the leg1 angle instead of the leg2 angle.
                #self.log.debug("self.isReversed() == {}".\
                #               format(self.isReversed()))
                if self.isReversed() == False:
                    angleDeg = leg1.angle() + angleDeg
                else:
                    angleDeg = leg2.angle() - angleDeg

                #self.log.debug("Adjusting to leg point angles, (angleDeg={})".
                #               format(angleDeg))

                angleDeg = Util.toNormalizedAngle(angleDeg)
                
                #self.log.debug("After normalizing angleDeg, (angleDeg={})".
                #               format(angleDeg))

                # Normalize angleDeg be within the range of
                # leg1.angle() and leg2.angle().  We have to jump
                # around a bit here to do the calculations because
                # points could be around the 0 degree point at
                # 3 o'clock.

                # Calculate which leg's angle the angleDeg is closest to.
                lineToAngleDeg = QLineF(scaledOriginPointF, scaledLeg1PointF)
                lineToAngleDeg.setAngle(angleDeg)
                angleToLeg1 = lineToAngleDeg.angleTo(leg1)
                angleToLeg2 = lineToAngleDeg.angleTo(leg2)

                #self.log.debug("angleToLeg1 == {} deg".format(angleToLeg1))
                #self.log.debug("angleToLeg2 == {} deg".format(angleToLeg2))

                if angleDegDelta >= 0:
                    # leg2 is higher in angle than leg1.
                    self.log.debug("leg2 is higher in angle than leg1.")
                    
                    if Util.fuzzyIsEqual(angleToLeg2, 0.0) and \
                             self.isReversed():
                        self.log.debug("At leg2 angle while reversed.  " + \
                                       "Adjusting to be perfect.")
                        angleDeg = leg2.angle()
                    elif angleToLeg1 < 180 and angleToLeg2 < 180:
                        self.log.debug("Below fan.  Adjusting.")
                        angleDeg += abs(angleDegDelta)
                    elif angleToLeg1 >= 180 and angleToLeg2 < 180:
                        self.log.debug("Within bounds.")
                    elif angleToLeg1 >= 180 and angleToLeg2 >= 180:
                        self.log.debug("Above fan.  Adjusting.")
                        angleDeg -= abs(angleDegDelta)
                    else:
                        self.log.warn("Unknown case.  " + \
                                      "Variables are: " + \
                                      "angleDegDelta == {}".\
                                      format(angleDegDelta) + \
                                      "angleToLeg1 == {}".\
                                      format(angleToLeg1) + \
                                      "angleToLeg2 == {}".\
                                      format(angleToLeg2))
                else:
                    # leg1 is higher in angle than leg2.
                    self.log.debug("leg1 is higher in angle than leg2.")

                    if Util.fuzzyIsEqual(angleToLeg2, 0.0) and \
                             self.isReversed():
                        self.log.debug("At leg2 angle while reversed.  " + \
                                       "Adjusting to be perfect.")
                        angleDeg = leg2.angle()
                    elif angleToLeg1 < 180 and angleToLeg2 < 180:
                        self.log.debug("Below fan.  Adjusting.")
                        angleDeg += abs(angleDegDelta)
                    elif angleToLeg1 < 180 and angleToLeg2 >= 180:
                        self.log.debug("Within bounds.")
                    elif angleToLeg1 >= 180 and angleToLeg2 >= 180:
                        self.log.debug("Above fan.  Adjusting.")
                        angleDeg -= abs(angleDegDelta)
                    else:
                        self.log.warn("Unknown case.  " + \
                                      "Variables are: " + \
                                      "angleDegDelta == {}".\
                                      format(angleDegDelta) + \
                                      "angleToLeg1 == {}".\
                                      format(angleToLeg1) + \
                                      "angleToLeg2 == {}".\
                                      format(angleToLeg2))
                        
                #self.log.debug("For index {}, ".format(i) +
                #               "normalized angleDeg to within " +
                #               "leg1 and leg2 is: {}".format(angleDeg))

                # Now that we have the angle, determine the
                # intersection point along the edge of the rectangle.

                # Find the smallest x and y values, and the largest x
                # and y values of the 3 points: scaledOriginPointF,
                # scaledLeg1PointF, and scaledLeg2PointF.  These will
                # be used to construct 4 line segments, which we will
                # use for calculating intersection points with the
                # line segment drawn from scaledOriginPointF at an
                # angle of 'angleDeg'.
                xValues = []
                xValues.append(scaledOriginPointF.x())
                xValues.append(scaledLeg1PointF.x())
                xValues.append(scaledLeg2PointF.x())

                yValues = []
                yValues.append(scaledOriginPointF.y())
                yValues.append(scaledLeg1PointF.y())
                yValues.append(scaledLeg2PointF.y())

                xValues.sort()
                yValues.sort()

                # Find the smallest x and y.
                smallestX = xValues[0]
                smallestY = yValues[0]
        
                # Find the largest x and y.
                largestX = xValues[-1]
                largestY = yValues[-1]

                # Rectangle bounding all 3 points.
                containingRectF = \
                    QRectF(QPointF(smallestX, smallestY),
                           QPointF(largestX, largestY))
                
                # Four lines that bound the 3 points.
                line1 = QLineF(smallestX, smallestY,
                               smallestX, largestY)
                line2 = QLineF(smallestX, smallestY,
                               largestX, smallestY)
                line3 = QLineF(largestX, largestY,
                               largestX, smallestY)
                line4 = QLineF(largestX, largestY,
                               smallestX, largestY)
                lines = []
                lines.append(line1)
                lines.append(line2)
                lines.append(line3)
                lines.append(line4)
                
                # Here in the process, I'm trying to handle special
                # cases of 0, 90, 180, 270 degrees where the end
                # values are easily defined since it appears to choke
                # up the algorithm below.
                if Util.fuzzyIsEqual(angleDeg, 0.0) or \
                       Util.fuzzyIsEqual(angleDeg, -0.0):
                    self.log.debug("Special case angle: 0.0")
                    x = largestX
                    y = scaledOriginPointF.y()
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                
                elif Util.fuzzyIsEqual(angleDeg, 90.0) or \
                         Util.fuzzyIsEqual(angleDeg, -270.0):
                    self.log.debug("Special case angle: 90.0")
                    x = scaledOriginPointF.x()
                    y = smallestY
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                    
                elif Util.fuzzyIsEqual(angleDeg, 180.0) or \
                         Util.fuzzyIsEqual(angleDeg, -180.0):
                    self.log.debug("Special case angle: 180.0")
                    x = smallestX
                    y = scaledOriginPointF.y()
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                    
                elif Util.fuzzyIsEqual(angleDeg, 270.0) or \
                         Util.fuzzyIsEqual(angleDeg, -90.0):
                    self.log.debug("Special case angle: 270.0")
                    x = scaledOriginPointF.x()
                    y = largestY
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break

                else:
                    self.log.debug("Regular case.")
                    
                # Get the line from scaledOriginPointF outwards at the
                # 'angleDeg' angle.  We just don't know what length it
                # should be.
                lineToAngleDeg = QLineF(scaledOriginPointF, scaledLeg1PointF)
                lineToAngleDeg.setAngle(angleDeg)

                #self.log.debug("lineToAngleDeg.p1 == ({}, {})".\
                #               format(lineToAngleDeg.p1().x(),
                #                      lineToAngleDeg.p1().y()))
                #self.log.debug("lineToAngleDeg.p2 == ({}, {})".\
                #               format(lineToAngleDeg.p2().x(),
                #                      lineToAngleDeg.p2().y()))
                
                # Find the intesections with the line segments in 'lines'.
                intersectionPoints = []
                for l in lines:
                    # Infinite line intersection algorithm taken from:
                    # http://wiki.processing.org/w/Line-Line_intersection
                    x1 = lineToAngleDeg.p1().x()
                    y1 = lineToAngleDeg.p1().y()
                    x2 = lineToAngleDeg.p2().x()
                    y2 = lineToAngleDeg.p2().y()
                    x3 = l.p1().x()
                    y3 = l.p1().y()
                    x4 = l.p2().x()
                    y4 = l.p2().y()
                    
                    bx = x2 - x1
                    by = y2 - y1
                    dx = x4 - x3
                    dy = y4 - y3 
                    b_dot_d_perp = bx*dy - by*dx

                    if Util.fuzzyIsEqual(abs(b_dot_d_perp), 0.0):
                        continue
                    
                    cx = x3-x1
                    cy = y3-y1
                    t = (cx*dy - cy*dx) / b_dot_d_perp
 
                    x = x1+t*bx
                    y = y1+t*by

                    intersectionPoint = QPointF(x, y)
                    intersectionPoints.append(intersectionPoint)
        
                    #self.log.debug("Appended intersection point: ({}, {})".\
                    #               format(intersectionPoint.x(),
                    #                      intersectionPoint.y()))

                # Normalized angleDeg.
                normalizedAngleDeg = Util.toNormalizedAngle(angleDeg)
                
                # Process the intersection points.
                closestPointToCorrectAngle = None
                smallestAngleDiff = None
                
                for p in intersectionPoints:
                    #self.log.debug("Looking at point: ({}, {})".\
                    #               format(p.x(), p.y()))
                    
                    # Flag that indicates the intersection point is
                    # also the origin point.
                    pEqualsOriginPointF = \
                        Util.fuzzyIsEqual(p.x(), scaledOriginPointF.x()) and \
                        Util.fuzzyIsEqual(p.y(), scaledOriginPointF.y())

                    #self.log.debug("pEqualsOriginPointF   == {}".\
                    #               format(pEqualsOriginPointF))

                    # Flag that indicates that p is within or on the
                    # edge of 'containingRectF'.
                    xWithinContainingRect = \
                        (smallestX < p.x() or \
                         Util.fuzzyIsEqual(p.x(), smallestX)) and \
                        (p.x() < largestX or \
                         Util.fuzzyIsEqual(p.x(), largestX))
                    yWithinContainingRect = \
                        (smallestY < p.y() or \
                         Util.fuzzyIsEqual(p.y(), smallestY)) and \
                        (p.y() < largestY or \
                         Util.fuzzyIsEqual(p.y(), largestY))
                    pWithinContainingRect = \
                        xWithinContainingRect and yWithinContainingRect
                                          
                    #self.log.debug("xWithinContainingRect == {}".\
                    #               format(xWithinContainingRect))
                    #self.log.debug("yWithinContainingRect == {}".\
                    #               format(yWithinContainingRect))
                    #self.log.debug("pWithinContainingRect == {}".\
                    #               format(pWithinContainingRect))

                    # Only look at intersection points that are not
                    # the origin and within or on the edge of
                    # 'containingRectF'.
                    if pWithinContainingRect and not pEqualsOriginPointF:

                        angle = QLineF(scaledOriginPointF, p).angle()
                        diff = abs(normalizedAngleDeg - \
                                   Util.toNormalizedAngle(angle))

                        #self.log.debug("diff in angle is:       {}".\
                        #               format(diff))
                        #self.log.debug("smallest angle diff is: {}".\
                        #               format(diff))
        
                        if closestPointToCorrectAngle == None and \
                           smallestAngleDiff == None:

                            closestPointToCorrectAngle = p
                            smallestAngleDiff = diff

                        elif diff < smallestAngleDiff:
                            
                            closestPointToCorrectAngle = p
                            smallestAngleDiff = diff

                if len(intersectionPoints) == 0:
                    # Couldn't find any intersection points.
                    self.log.warn("Couldn't find any intersection points!")
                    x = None
                    y = None
                elif closestPointToCorrectAngle == None:
                    # Use origin point as the intersection.
                    x = scaledOriginPointF.x()
                    y = scaledOriginPointF.y()
                else:
                    # The closest point it the point we are looking for.
                    x = closestPointToCorrectAngle.x()
                    y = closestPointToCorrectAngle.y()
                    
                # Break out of for loop since we handled the index we
                # were looking to process.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartOctaveFanArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartOctaveFanArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartFibFanArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the the data elements of a
    FibFanGraphicsItem.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartFibFanArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "FibFan_" + str(self.uuid)

        # Origin point and the two leg points of the artifact.
        self.originPointF = QPointF()
        self.leg1PointF = QPointF()
        self.leg2PointF = QPointF()
        
        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemTextYScaling
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemDefaultFontDescription
        
        # QColor can be pickled
        self.textColor = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemDefaultTextColor

        # QColor can be pickled   
        self.color = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemDefaultColor

        # List of Ratio objects for the different ratios supported.
        self.ratios = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemRatios

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = False
        
    def setOriginPointF(self, originPointF):
        """Stores the origin point of the FibFanArtifact.
        Arguments:

        originPointF - QPointF for the origin point of the artifact.
        """
        
        self.originPointF = originPointF
        
    def getOriginPointF(self):
        """Returns the origin point of the FibFanArtifact."""
        
        return self.originPointF
        
    def setLeg1PointF(self, leg1PointF):
        """Stores the leg1 point of the FibFanArtifact.
        Arguments:

        leg1PointF - QPointF for the leg1 point of the artifact.
        """
        
        self.leg1PointF = leg1PointF
        
    def getLeg1PointF(self):
        """Returns the leg1 point of the FibFanArtifact."""
        
        return self.leg1PointF

    def setLeg2PointF(self, leg2PointF):
        """Stores the leg2 point of the FibFanArtifact.
        Arguments:

        leg2PointF - QPointF for the leg2 point of the artifact.
        """
        
        self.leg2PointF = leg2PointF
        
    def getLeg2PointF(self):
        """Returns the leg2 point of the FibFanArtifact."""
        
        return self.leg2PointF

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setTextColor(self, textColor):
        """Sets the color for this artifact's text.

        Arguments:
        textColor - QColor object holding the color of the text.
        """

        self.textColor = textColor

    def getTextColor(self):
        """Returns the color of this artifact's text as a QColor."""

        return self.textColor

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        ratios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the ratios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def setRatios(self, ratios):
        """Sets the list of Ratio objects, which is the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        self.ratios = ratios
    
    def getRatios(self):
        """Returns a list of Ratio objects, which holds the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        return self.ratios
    
    def getXYForRatio(self,
                      index, 
                      scaledOriginPointF,
                      scaledLeg1PointF,
                      scaledLeg2PointF):
        """Returns the x and y location of where this ratio point
        would exist, based on the Ratio ordering and the
        scaledOriginPointF, scaledLeg1PointF, and scaledLeg2PointF
        locations.  This method does it's calculation based on 3
        points, and the point returned is along the outter edge of a
        bounding rectangle created by the 3 points.  The calculated
        point returned is based angular ratios.

        Arguments:
        
        index - int value for index into self.ratios that the
                user is looking for the ratio for.  This value
                must be within the valid index limits.
        scaledOriginPointF - Origin point of the fib fan, in scaled
                             coordinates.
        scaledLeg1PointF   - Leg1 point of the fib fan, in scaled
                             coordinates.
        scaledLeg2PointF   - Leg2 point of the fib fan, in scaled
                             coordinates.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point in scaled
        coordinates.  This is where the ratio would exist.
        The caller must then unscale it back to scene or local
        coordinates as needed.
        """

        #self.log.debug("Entered getXYForRatio({})".format(index))

        # Get the ratios.
        ratios = self.getRatios()
        
        # Validate input.
        if index < 0:
            self.log.error("getXYForRatio(): Invalid index: {}".
                           format(index))
            return
        if len(ratios) > 0 and index >= len(ratios):
            self.log.error("getXYForRatio(): Index out of range: {}".
                           format(index))
            return


        # Return values.
        x = None
        y = None


        # Simple test cases when some points are the same value.
        if scaledOriginPointF == scaledLeg1PointF and \
           scaledOriginPointF == scaledLeg2PointF:

            # All three points the same.
            #self.log.debug("All three points are the same, so we will " +
            #               "return the same point as the position " +
            #               "of the ratio.")
            x = scaledOriginPointF.x()
            y = scaledOriginPointF.y()
            return (x, y)
        
        elif scaledOriginPointF == scaledLeg1PointF and \
             scaledOriginPointF != scaledLeg2PointF:

            # scaledOriginPointF and scaledLeg1PointF points are the same.
            #self.log.debug("scaledOriginPointF and scaledLeg1PointF " +
            #               "are equal, so we will" +
            #               "return the scaledLeg2PointF as the " +
            #               "position of the same point as the position " +
            #               "of the ratio.")
            x = scaledLeg2PointF.x()
            y = scaledLeg2PointF.y()
            return (x, y)

        elif scaledOriginPointF != scaledLeg1PointF and \
             scaledOriginPointF == scaledLeg2PointF:
            
            # scaledOriginPointF and scaledLeg2PointF points are the same.
            #self.log.debug("scaledOriginPointF and scaledLeg2PointF " +
            #               "are equal, so we will" +
            #               "return the scaledLeg1PointF as the " +
            #               "position of the same point as the position " +
            #               "of the ratio.")
            x = scaledLeg1PointF.x()
            y = scaledLeg1PointF.y()
            return (x, y)

        else:
            
            # All three points the different.
            self.log.debug("All three points are different, so " +
                           "continuing on to do the calculations.")

        #self.log.debug("scaledOriginPointF is: ({}, {})".\
        #               format(scaledOriginPointF.x(),
        #                      scaledOriginPointF.y()))
        #self.log.debug("scaledLeg1PointF is: ({}, {})".\
        #               format(scaledLeg1PointF.x(),
        #                      scaledLeg1PointF.y()))
        #self.log.debug("scaledLeg2PointF is: ({}, {})".\
        #               format(scaledLeg2PointF.x(),
        #                      scaledLeg2PointF.y()))

        # Calculate the angle between the two line segments.
        leg1 = QLineF(scaledOriginPointF, scaledLeg1PointF)
        leg2 = QLineF(scaledOriginPointF, scaledLeg2PointF)

        #self.log.debug("Angle of leg1 is: {}".format(leg1.angle()))
        #self.log.debug("Angle of leg2 is: {}".format(leg2.angle()))
        
        
        # The angle returned by QLineF.angleTo() is always normalized.
        angleDegDelta = leg1.angleTo(leg2)

        #self.log.debug("Angle of leg1 to leg2 is: " +
        #               "angleDegDelta == {} deg".format(angleDegDelta))
        
        # As opposed to how things are done in the other fan tool,
        # we don't want to do any adjusting, so the below is commented out.
        #if angleDegDelta > 180:
        #    angleDegDelta -= 360
        
        #self.log.debug("Adjusted angle difference is: " + \
        #               "angleDegDelta == {} deg".format(angleDegDelta))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        angleDegOffset = 0.0

        #self.log.debug("There are {} number of ratios.".\
        #               format(len(ratios)))

        for i in range(len(ratios)):
            ratio = ratios[i]
            
            #self.log.debug("ratios[{}].getRatio() is: {}".\
            #               format(i, ratio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                angleDegOffset = \
                    angleDegDelta * (ratio.getRatio())

                #self.log.debug("At i == 0.  angleDegOffset={}".\
                #               format(angleDegOffset))
                
            if i == index:
                #self.log.debug("At the i == index, where i == {}.".format(i))
                #self.log.debug("ratio is: {}".\
                #               format(ratio.getRatio()))
                
                angleDeg = \
                    (angleDegDelta * ratio.getRatio()) - \
                    angleDegOffset

                #self.log.debug("(angleDeg={})".format(angleDeg))

                angleDeg = leg1.angle() + angleDeg

                #self.log.debug("Adjusting to leg point angles, (angleDeg={})".
                #               format(angleDeg))

                angleDeg = Util.toNormalizedAngle(angleDeg)
                
                #self.log.debug("After normalizing angleDeg, (angleDeg={})".
                #               format(angleDeg))

                # Now that we have the angle, determine the
                # intersection point along the edge of the giant
                # rectangle.
                
                # Find the smallest x and y values, and the largest x
                # and y values of the 3 points bounding
                # scaledOriginPointF, from all directions:
                # scaledOriginPointF, scaledLeg1PointF, and
                # scaledLeg2PointF.  These will be used to construct 4
                # line segments, which we will use for calculating
                # intersection points with the line segment drawn from
                # scaledOriginPointF at an angle of 'angleDeg'.
                xValues = []
                xValues.append(scaledOriginPointF.x())
                xValues.append(scaledLeg1PointF.x())
                xValues.append(scaledLeg2PointF.x())
                xValues.append(scaledOriginPointF.x() - \
                               (scaledLeg1PointF.x() - scaledOriginPointF.x()))
                xValues.append(scaledOriginPointF.x() - \
                               (scaledLeg2PointF.x() - scaledOriginPointF.x()))

                
                yValues = []
                yValues.append(scaledOriginPointF.y())
                yValues.append(scaledLeg1PointF.y())
                yValues.append(scaledLeg2PointF.y())
                yValues.append(scaledOriginPointF.y() - \
                               (scaledLeg1PointF.y() - scaledOriginPointF.y()))
                yValues.append(scaledOriginPointF.y() - \
                               (scaledLeg2PointF.y() - scaledOriginPointF.y()))

                xValues.sort()
                yValues.sort()

                # Find the smallest x and y.
                smallestX = xValues[0]
                smallestY = yValues[0]
        
                # Find the largest x and y.
                largestX = xValues[-1]
                largestY = yValues[-1]

                # Rectangle bounding the points.
                containingRectF = \
                    QRectF(QPointF(smallestX, smallestY),
                           QPointF(largestX, largestY))
                
                # Four lines that bound the points.
                line1 = QLineF(smallestX, smallestY,
                               smallestX, largestY)
                line2 = QLineF(smallestX, smallestY,
                               largestX, smallestY)
                line3 = QLineF(largestX, largestY,
                               largestX, smallestY)
                line4 = QLineF(largestX, largestY,
                               smallestX, largestY)
                lines = []
                lines.append(line1)
                lines.append(line2)
                lines.append(line3)
                lines.append(line4)
                
                # Here in the process, I'm trying to handle special
                # cases of 0, 90, 180, 270 degrees where the end
                # values are easily defined since it appears to choke
                # up the algorithm below.
                if Util.fuzzyIsEqual(angleDeg, 0.0) or \
                       Util.fuzzyIsEqual(angleDeg, -0.0):
                    self.log.debug("Special case angle: 0.0")
                    x = largestX
                    y = scaledOriginPointF.y()
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                
                elif Util.fuzzyIsEqual(angleDeg, 90.0) or \
                         Util.fuzzyIsEqual(angleDeg, -270.0):
                    self.log.debug("Special case angle: 90.0")
                    x = scaledOriginPointF.x()
                    y = smallestY
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                    
                elif Util.fuzzyIsEqual(angleDeg, 180.0) or \
                         Util.fuzzyIsEqual(angleDeg, -180.0):
                    self.log.debug("Special case angle: 180.0")
                    x = smallestX
                    y = scaledOriginPointF.y()
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                    
                elif Util.fuzzyIsEqual(angleDeg, 270.0) or \
                         Util.fuzzyIsEqual(angleDeg, -90.0):
                    self.log.debug("Special case angle: 270.0")
                    x = scaledOriginPointF.x()
                    y = largestY
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break

                else:
                    self.log.debug("Regular case.")
                    
                # Get the line from scaledOriginPointF outwards at the
                # 'angleDeg' angle.  We just don't know what length it
                # should be.
                lineToAngleDeg = QLineF(scaledOriginPointF, scaledLeg1PointF)
                lineToAngleDeg.setAngle(angleDeg)

                #self.log.debug("lineToAngleDeg.p1 == ({}, {})".\
                #               format(lineToAngleDeg.p1().x(),
                #                      lineToAngleDeg.p1().y()))
                #self.log.debug("lineToAngleDeg.p2 == ({}, {})".\
                #               format(lineToAngleDeg.p2().x(),
                #                      lineToAngleDeg.p2().y()))
                
                # Find the intesections with the line segments in 'lines'.
                intersectionPoints = []
                for l in lines:
                    # Infinite line intersection algorithm taken from:
                    # http://wiki.processing.org/w/Line-Line_intersection
                    x1 = lineToAngleDeg.p1().x()
                    y1 = lineToAngleDeg.p1().y()
                    x2 = lineToAngleDeg.p2().x()
                    y2 = lineToAngleDeg.p2().y()
                    x3 = l.p1().x()
                    y3 = l.p1().y()
                    x4 = l.p2().x()
                    y4 = l.p2().y()
                    
                    bx = x2 - x1
                    by = y2 - y1
                    dx = x4 - x3
                    dy = y4 - y3 
                    b_dot_d_perp = bx*dy - by*dx

                    if Util.fuzzyIsEqual(abs(b_dot_d_perp), 0.0):
                        continue
                    
                    cx = x3-x1
                    cy = y3-y1
                    t = (cx*dy - cy*dx) / b_dot_d_perp
 
                    x = x1+t*bx
                    y = y1+t*by

                    intersectionPoint = QPointF(x, y)
                    intersectionPoints.append(intersectionPoint)
        
                    #self.log.debug("Appended intersection point: ({}, {})".\
                    #               format(intersectionPoint.x(),
                    #                      intersectionPoint.y()))

                # Normalized angleDeg.
                normalizedAngleDeg = Util.toNormalizedAngle(angleDeg)
                
                # Process the intersection points.
                closestPointToCorrectAngle = None
                smallestAngleDiff = None
                
                for p in intersectionPoints:
                    #self.log.debug("Looking at point: ({}, {})".\
                    #               format(p.x(), p.y()))
                    
                    # Flag that indicates the intersection point is
                    # also the origin point.
                    pEqualsOriginPointF = \
                        Util.fuzzyIsEqual(p.x(), scaledOriginPointF.x()) and \
                        Util.fuzzyIsEqual(p.y(), scaledOriginPointF.y())

                    #self.log.debug("pEqualsOriginPointF   == {}".\
                    #               format(pEqualsOriginPointF))

                    # Flag that indicates that p is within or on the
                    # edge of 'containingRectF'.
                    xWithinContainingRect = \
                        (smallestX < p.x() or \
                         Util.fuzzyIsEqual(p.x(), smallestX)) and \
                        (p.x() < largestX or \
                         Util.fuzzyIsEqual(p.x(), largestX))
                    yWithinContainingRect = \
                        (smallestY < p.y() or \
                         Util.fuzzyIsEqual(p.y(), smallestY)) and \
                        (p.y() < largestY or \
                         Util.fuzzyIsEqual(p.y(), largestY))
                    pWithinContainingRect = \
                        xWithinContainingRect and yWithinContainingRect
                                          
                    #self.log.debug("xWithinContainingRect == {}".\
                    #               format(xWithinContainingRect))
                    #self.log.debug("yWithinContainingRect == {}".\
                    #               format(yWithinContainingRect))
                    #self.log.debug("pWithinContainingRect == {}".\
                    #               format(pWithinContainingRect))

                    if pWithinContainingRect and not pEqualsOriginPointF:

                        angle = QLineF(scaledOriginPointF, p).angle()
                        diff = abs(normalizedAngleDeg - \
                                   Util.toNormalizedAngle(angle))

                        #self.log.debug("diff in angle is:       {}".\
                        #               format(diff))
                        #self.log.debug("smallest angle diff is: {}".\
                        #               format(diff))
        
                        if closestPointToCorrectAngle == None and \
                           smallestAngleDiff == None:

                            closestPointToCorrectAngle = p
                            smallestAngleDiff = diff

                        elif diff < smallestAngleDiff:
                            
                            closestPointToCorrectAngle = p
                            smallestAngleDiff = diff

                if len(intersectionPoints) == 0:
                    # Couldn't find any intersection points.
                    self.log.warn("Couldn't find any intersection points!")
                    x = None
                    y = None
                elif closestPointToCorrectAngle == None:
                    # Use origin point as the intersection.
                    x = scaledOriginPointF.x()
                    y = scaledOriginPointF.y()
                else:
                    # The closest point it the point we are looking for.
                    x = closestPointToCorrectAngle.x()
                    y = closestPointToCorrectAngle.y()
                    
                # Break out of for loop since we handled the index we
                # were looking to process.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.ratios.
            self.log.warn("getXYForRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartFibFanArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartFibFanArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartGannFanArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the the data elements of a
    GannFanGraphicsItem.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartGannFanArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "GannFan_" + str(self.uuid)

        # Origin point and the two leg points of the artifact.
        self.originPointF = QPointF()
        self.leg1PointF = QPointF()
        self.leg2PointF = QPointF()
        
        # Scaling the text, to make it bigger or smaller.
        self.textXScaling = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemTextXScaling
        self.textYScaling = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemTextYScaling
        
        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString()
        self.fontDescription = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemDefaultFontDescription
        
        # QColor can be pickled
        self.textColor = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemDefaultTextColor

        # QColor can be pickled   
        self.color = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemDefaultColor

        # List of Ratio objects for the different ratios supported.
        self.ratios = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemRatios

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = False
        
    def setOriginPointF(self, originPointF):
        """Stores the origin point of the GannFanArtifact.
        Arguments:

        originPointF - QPointF for the origin point of the artifact.
        """
        
        self.originPointF = originPointF
        
    def getOriginPointF(self):
        """Returns the origin point of the GannFanArtifact."""
        
        return self.originPointF
        
    def setLeg1PointF(self, leg1PointF):
        """Stores the leg1 point of the GannFanArtifact.
        Arguments:

        leg1PointF - QPointF for the leg1 point of the artifact.
        """
        
        self.leg1PointF = leg1PointF
        
    def getLeg1PointF(self):
        """Returns the leg1 point of the GannFanArtifact."""
        
        return self.leg1PointF

    def setLeg2PointF(self, leg2PointF):
        """Stores the leg2 point of the GannFanArtifact.
        Arguments:

        leg2PointF - QPointF for the leg2 point of the artifact.
        """
        
        self.leg2PointF = leg2PointF
        
    def getLeg2PointF(self):
        """Returns the leg2 point of the GannFanArtifact."""
        
        return self.leg2PointF

    def setTextXScaling(self, textXScaling):
        """Sets the text X scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textXScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textXScaling = textXScaling

    def getTextXScaling(self):
        """Returns float value for the text X scaling, used in making
        the text bigger or smaller.
        """

        return self.textXScaling
        
    def setTextYScaling(self, textYScaling):
        """Sets the text Y scaling, used in making the text 
        bigger or smaller.

        Arguments:
        textYScaling - float value for the scaling used.
                       1.0 is no change in scaling.
        """

        self.textYScaling = textYScaling

    def getTextYScaling(self):
        """Returns float value for the text Y scaling, used in making
        the text bigger or smaller.
        """

        return self.textYScaling
        
    def setFont(self, font):
        """Sets the font of this artifact's text.

        Arguments:
        font - QFont object that is used for the drawing of the text.
        """

        # QFont cannot be pickled, but we can utilize
        # QFont.toString() and then QFont.fromString().
        self.fontDescription = font.toString()

    def getFont(self):
        """Returns the font of this artifact's text as a QFont.
        """

        # We obtain the QFont by calling QFont.fromString().
        font = QFont()
        font.fromString(self.fontDescription)

        return font
        
    def setTextColor(self, textColor):
        """Sets the color for this artifact's text.

        Arguments:
        textColor - QColor object holding the color of the text.
        """

        self.textColor = textColor

    def getTextColor(self):
        """Returns the color of this artifact's text as a QColor."""

        return self.textColor

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        ratios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the ratios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def setRatios(self, ratios):
        """Sets the list of Ratio objects, which is the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        self.ratios = ratios
    
    def getRatios(self):
        """Returns a list of Ratio objects, which holds the ratios
        supported, and whether they are enabled or not for this
        artifact.
        """

        return self.ratios
    
    def getXYForRatio(self,
                      index, 
                      scaledOriginPointF,
                      scaledLeg1PointF,
                      scaledLeg2PointF):
        """Returns the x and y location of where this ratio point
        would exist, based on the Ratio ordering and the
        scaledOriginPointF, scaledLeg1PointF, and scaledLeg2PointF
        locations.  This method does it's calculation based on 3
        points, and the point returned is along the outter edge of a
        bounding rectangle created by the 3 points.  The calculated
        point returned is based angular ratios.

        Arguments:
        
        index - int value for index into self.ratios that the
                user is looking for the ratio for.  This value
                must be within the valid index limits.
        scaledOriginPointF - Origin point of the gann fan, in scaled
                             coordinates.
        scaledLeg1PointF   - Leg1 point of the gann fan, in scaled
                             coordinates.
        scaledLeg2PointF   - Leg2 point of the gann fan, in scaled
                             coordinates.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point in scaled
        coordinates.  This is where the ratio would exist.
        The caller must then unscale it back to scene or local
        coordinates as needed.
        """

        #self.log.debug("Entered getXYForRatio({})".format(index))

        # Get the ratios.
        ratios = self.getRatios()
        
        # Validate input.
        if index < 0:
            self.log.error("getXYForRatio(): Invalid index: {}".
                           format(index))
            return
        if len(ratios) > 0 and index >= len(ratios):
            self.log.error("getXYForRatio(): Index out of range: {}".
                           format(index))
            return


        # Return values.
        x = None
        y = None


        # Simple test cases when some points are the same value.
        if scaledOriginPointF == scaledLeg1PointF and \
           scaledOriginPointF == scaledLeg2PointF:

            # All three points the same.
            #self.log.debug("All three points are the same, so we will " +
            #               "return the same point as the position " +
            #               "of the ratio.")
            x = scaledOriginPointF.x()
            y = scaledOriginPointF.y()
            return (x, y)
        
        elif scaledOriginPointF == scaledLeg1PointF and \
             scaledOriginPointF != scaledLeg2PointF:

            # scaledOriginPointF and scaledLeg1PointF points are the same.
            #self.log.debug("scaledOriginPointF and scaledLeg1PointF " +
            #               "are equal, so we will" +
            #               "return the scaledLeg2PointF as the " +
            #               "position of the same point as the position " +
            #               "of the ratio.")
            x = scaledLeg2PointF.x()
            y = scaledLeg2PointF.y()
            return (x, y)

        elif scaledOriginPointF != scaledLeg1PointF and \
             scaledOriginPointF == scaledLeg2PointF:
            
            # scaledOriginPointF and scaledLeg2PointF points are the same.
            #self.log.debug("scaledOriginPointF and scaledLeg2PointF " +
            #               "are equal, so we will" +
            #               "return the scaledLeg1PointF as the " +
            #               "position of the same point as the position " +
            #               "of the ratio.")
            x = scaledLeg1PointF.x()
            y = scaledLeg1PointF.y()
            return (x, y)

        else:
            
            # All three points the different.
            self.log.debug("All three points are different, so " +
                           "continuing on to do the calculations.")

        #self.log.debug("scaledOriginPointF is: ({}, {})".\
        #               format(scaledOriginPointF.x(),
        #                      scaledOriginPointF.y()))
        #self.log.debug("scaledLeg1PointF is: ({}, {})".\
        #               format(scaledLeg1PointF.x(),
        #                      scaledLeg1PointF.y()))
        #self.log.debug("scaledLeg2PointF is: ({}, {})".\
        #               format(scaledLeg2PointF.x(),
        #                      scaledLeg2PointF.y()))

        # Calculate the angle between the two line segments.
        leg1 = QLineF(scaledOriginPointF, scaledLeg1PointF)
        leg2 = QLineF(scaledOriginPointF, scaledLeg2PointF)

        #self.log.debug("Angle of leg1 is: {}".format(leg1.angle()))
        #self.log.debug("Angle of leg2 is: {}".format(leg2.angle()))
        
        
        # The angle returned by QLineF.angleTo() is always normalized.
        angleDegDelta = leg1.angleTo(leg2)

        #self.log.debug("Angle of leg1 to leg2 is: " +
        #               "angleDegDelta == {} deg".format(angleDegDelta))
        
        # Adjust so that the angle is between (-180 and 180].
        if angleDegDelta > 180:
            angleDegDelta -= 360
        
        #self.log.debug("Adjusted angle difference is: " + \
        #               "angleDegDelta == {} deg".format(angleDegDelta))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        angleDegOffset = 0.0

        #self.log.debug("There are {} number of ratios.".\
        #               format(len(ratios)))

        for i in range(len(ratios)):
            ratio = ratios[i]
            
            #self.log.debug("ratios[{}].getRatio() is: {}".\
            #               format(i, ratio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                angleDegOffset = \
                    angleDegDelta * (ratio.getRatio())

                #self.log.debug("At i == 0.  angleDegOffset={}".\
                #               format(angleDegOffset))
                
            if i == index:
                #self.log.debug("At the i == index, where i == {}.".format(i))
                #self.log.debug("ratio is: {}".\
                #               format(ratio.getRatio()))
                
                angleDeg = \
                    (angleDegDelta * ratio.getRatio()) - \
                    angleDegOffset
                
                #self.log.debug("(angleDeg={})".format(angleDeg))
                
                angleDeg = leg1.angle() + angleDeg
                
                #self.log.debug("Adjusting to leg point angles, (angleDeg={})".
                #               format(angleDeg))

                angleDeg = Util.toNormalizedAngle(angleDeg)
                
                #self.log.debug("After normalizing angleDeg, (angleDeg={})".
                #               format(angleDeg))

                # Now that we have the angle, determine the
                # intersection point along the edge of the giant
                # rectangle.

                # Find the smallest x and y values, and the largest x
                # and y values of the 3 points bounding
                # scaledOriginPointF, from all directions:
                # scaledOriginPointF, scaledLeg1PointF, and
                # scaledLeg2PointF.  These will be used to construct 4
                # line segments, which we will use for calculating
                # intersection points with the line segment drawn from
                # scaledOriginPointF at an angle of 'angleDeg'.
                xValues = []
                xValues.append(scaledOriginPointF.x())
                xValues.append(scaledLeg1PointF.x())
                xValues.append(scaledLeg2PointF.x())
                #xValues.append(scaledOriginPointF.x() - \
                #               (scaledLeg1PointF.x() - scaledOriginPointF.x()))
                #xValues.append(scaledOriginPointF.x() - \
                #               (scaledLeg2PointF.x() - scaledOriginPointF.x()))

                
                yValues = []
                yValues.append(scaledOriginPointF.y())
                yValues.append(scaledLeg1PointF.y())
                yValues.append(scaledLeg2PointF.y())
                #yValues.append(scaledOriginPointF.y() - \
                #               (scaledLeg1PointF.y() - scaledOriginPointF.y()))
                #yValues.append(scaledOriginPointF.y() - \
                #               (scaledLeg2PointF.y() - scaledOriginPointF.y()))

                xValues.sort()
                yValues.sort()

                # Find the smallest x and y.
                smallestX = xValues[0]
                smallestY = yValues[0]
        
                # Find the largest x and y.
                largestX = xValues[-1]
                largestY = yValues[-1]

                # Rectangle bounding the points.
                containingRectF = \
                    QRectF(QPointF(smallestX, smallestY),
                           QPointF(largestX, largestY))

                # Four lines that bound the points.
                line1 = QLineF(smallestX, smallestY,
                               smallestX, largestY)
                line2 = QLineF(smallestX, smallestY,
                               largestX, smallestY)
                line3 = QLineF(largestX, largestY,
                               largestX, smallestY)
                line4 = QLineF(largestX, largestY,
                               smallestX, largestY)
                lines = []
                lines.append(line1)
                lines.append(line2)
                lines.append(line3)
                lines.append(line4)

                # Here in the process, I'm trying to handle special
                # cases of 0, 90, 180, 270 degrees where the end
                # values are easily defined since it appears to choke
                # up the algorithm below.
                if Util.fuzzyIsEqual(angleDeg, 0.0) or \
                       Util.fuzzyIsEqual(angleDeg, -0.0):
                    self.log.debug("Special case angle: 0.0")
                    x = largestX
                    y = scaledOriginPointF.y()
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                
                elif Util.fuzzyIsEqual(angleDeg, 90.0) or \
                         Util.fuzzyIsEqual(angleDeg, -270.0):
                    self.log.debug("Special case angle: 90.0")
                    x = scaledOriginPointF.x()
                    y = smallestY
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                    
                elif Util.fuzzyIsEqual(angleDeg, 180.0) or \
                         Util.fuzzyIsEqual(angleDeg, -180.0):
                    self.log.debug("Special case angle: 180.0")
                    x = smallestX
                    y = scaledOriginPointF.y()
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break
                    
                elif Util.fuzzyIsEqual(angleDeg, 270.0) or \
                         Util.fuzzyIsEqual(angleDeg, -90.0):
                    self.log.debug("Special case angle: 270.0")
                    x = scaledOriginPointF.x()
                    y = largestY
                    
                    # Break out of for loop since we handled the index we
                    # were looking to process.
                    break

                else:
                    self.log.debug("Regular case.")
                    
                # Get the line from scaledOriginPointF outwards at the
                # 'angleDeg' angle.  We just don't know what length it
                # should be.
                lineToAngleDeg = QLineF(scaledOriginPointF, scaledLeg1PointF)
                lineToAngleDeg.setAngle(angleDeg)

                #self.log.debug("lineToAngleDeg.p1 == ({}, {})".\
                #               format(lineToAngleDeg.p1().x(),
                #                      lineToAngleDeg.p1().y()))
                #self.log.debug("lineToAngleDeg.p2 == ({}, {})".\
                #               format(lineToAngleDeg.p2().x(),
                #                      lineToAngleDeg.p2().y()))
                
                # Find the intesections with the line segments in 'lines'.
                intersectionPoints = []
                for l in lines:
                    # Infinite line intersection algorithm taken from:
                    # http://wiki.processing.org/w/Line-Line_intersection
                    x1 = lineToAngleDeg.p1().x()
                    y1 = lineToAngleDeg.p1().y()
                    x2 = lineToAngleDeg.p2().x()
                    y2 = lineToAngleDeg.p2().y()
                    x3 = l.p1().x()
                    y3 = l.p1().y()
                    x4 = l.p2().x()
                    y4 = l.p2().y()
                    
                    bx = x2 - x1
                    by = y2 - y1
                    dx = x4 - x3
                    dy = y4 - y3 
                    b_dot_d_perp = bx*dy - by*dx

                    if Util.fuzzyIsEqual(abs(b_dot_d_perp), 0.0):
                        continue
                    
                    cx = x3-x1
                    cy = y3-y1
                    t = (cx*dy - cy*dx) / b_dot_d_perp
 
                    x = x1+t*bx
                    y = y1+t*by

                    intersectionPoint = QPointF(x, y)
                    intersectionPoints.append(intersectionPoint)
        
                    #self.log.debug("Appended intersection point: ({}, {})".\
                    #               format(intersectionPoint.x(),
                    #                      intersectionPoint.y()))

                # Normalized angleDeg.
                normalizedAngleDeg = Util.toNormalizedAngle(angleDeg)
                
                # Process the intersection points.
                closestPointToCorrectAngle = None
                smallestAngleDiff = None
                
                for p in intersectionPoints:
                    #self.log.debug("Looking at point: ({}, {})".\
                    #               format(p.x(), p.y()))
                    
                    # Flag that indicates the intersection point is
                    # also the origin point.
                    pEqualsOriginPointF = \
                        Util.fuzzyIsEqual(p.x(), scaledOriginPointF.x()) and \
                        Util.fuzzyIsEqual(p.y(), scaledOriginPointF.y())

                    #self.log.debug("pEqualsOriginPointF   == {}".\
                    #               format(pEqualsOriginPointF))

                    # Flag that indicates that p is within or on the
                    # edge of 'containingRectF'.
                    xWithinContainingRect = \
                        (smallestX < p.x() or \
                         Util.fuzzyIsEqual(p.x(), smallestX)) and \
                        (p.x() < largestX or \
                         Util.fuzzyIsEqual(p.x(), largestX))
                    yWithinContainingRect = \
                        (smallestY < p.y() or \
                         Util.fuzzyIsEqual(p.y(), smallestY)) and \
                        (p.y() < largestY or \
                         Util.fuzzyIsEqual(p.y(), largestY))
                    pWithinContainingRect = \
                        xWithinContainingRect and yWithinContainingRect
                                          
                    #self.log.debug("xWithinContainingRect == {}".\
                    #               format(xWithinContainingRect))
                    #self.log.debug("yWithinContainingRect == {}".\
                    #               format(yWithinContainingRect))
                    #self.log.debug("pWithinContainingRect == {}".\
                    #               format(pWithinContainingRect))

                    if pWithinContainingRect and not pEqualsOriginPointF:

                        angle = QLineF(scaledOriginPointF, p).angle()
                        diff = abs(normalizedAngleDeg - \
                                   Util.toNormalizedAngle(angle))

                        #self.log.debug("diff in angle is:       {}".\
                        #               format(diff))
                        #self.log.debug("smallest angle diff is: {}".\
                        #               format(diff))
        
                        if closestPointToCorrectAngle == None and \
                           smallestAngleDiff == None:

                            closestPointToCorrectAngle = p
                            smallestAngleDiff = diff

                        elif diff < smallestAngleDiff:
                            
                            closestPointToCorrectAngle = p
                            smallestAngleDiff = diff

                if len(intersectionPoints) == 0:
                    # Couldn't find any intersection points.
                    self.log.warn("Couldn't find any intersection points!")
                    x = None
                    y = None
                elif closestPointToCorrectAngle == None:
                    # Use origin point as the intersection.
                    x = scaledOriginPointF.x()
                    y = scaledOriginPointF.y()
                else:
                    # The closest point it the point we are looking for.
                    x = closestPointToCorrectAngle.x()
                    y = closestPointToCorrectAngle.y()
                    
                # Break out of for loop since we handled the index we
                # were looking to process.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.ratios.
            self.log.warn("getXYForRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartGannFanArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartGannFanArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartVimsottariDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartVimsottariDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "VimsottariDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultVimsottariDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the VimsottariDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the VimsottariDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the VimsottariDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the VimsottariDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartVimsottariDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartVimsottariDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartAshtottariDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartAshtottariDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "AshtottariDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultAshtottariDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the AshtottariDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the AshtottariDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the AshtottariDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the AshtottariDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartAshtottariDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartAshtottariDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartYoginiDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartYoginiDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "YoginiDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultYoginiDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the YoginiDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the YoginiDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the YoginiDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the YoginiDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartYoginiDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartYoginiDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartDwisaptatiSamaDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartDwisaptatiSamaDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "DwisaptatiSamaDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultDwisaptatiSamaDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the DwisaptatiSamaDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the DwisaptatiSamaDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the DwisaptatiSamaDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the DwisaptatiSamaDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartDwisaptatiSamaDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartDwisaptatiSamaDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartShattrimsaSamaDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartShattrimsaSamaDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "ShattrimsaSamaDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultShattrimsaSamaDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the ShattrimsaSamaDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the ShattrimsaSamaDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the ShattrimsaSamaDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the ShattrimsaSamaDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartShattrimsaSamaDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartShattrimsaSamaDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartDwadasottariDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartDwadasottariDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "DwadasottariDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultDwadasottariDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the DwadasottariDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the DwadasottariDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the DwadasottariDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the DwadasottariDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartDwadasottariDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartDwadasottariDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartChaturaseetiSamaDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartChaturaseetiSamaDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "ChaturaseetiSamaDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultChaturaseetiSamaDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the ChaturaseetiSamaDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the ChaturaseetiSamaDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the ChaturaseetiSamaDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the ChaturaseetiSamaDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartChaturaseetiSamaDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartChaturaseetiSamaDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartSataabdikaDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartSataabdikaDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "SataabdikaDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultSataabdikaDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the SataabdikaDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the SataabdikaDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the SataabdikaDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the SataabdikaDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartSataabdikaDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartSataabdikaDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartShodasottariDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartShodasottariDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "ShodasottariDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultShodasottariDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the ShodasottariDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the ShodasottariDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the ShodasottariDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the ShodasottariDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartShodasottariDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartShodasottariDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartPanchottariDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartPanchottariDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "PanchottariDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultPanchottariDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the PanchottariDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the PanchottariDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the PanchottariDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the PanchottariDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartPanchottariDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartPanchottariDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartShashtihayaniDasaArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that indicates the time measurement starting 
    at the given PriceBar timestamp and the given Y offset from the 
    center of the bar.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartShashtihayaniDasaArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "ShashtihayaniDasa_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used musical ratios.
        self.musicalRatios = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemMusicalRatios
        
        # color (QColor).
        self.color = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemBarColor

        # textColor (QColor).
        self.textColor = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemTextColor

        # barHeight (float).
        self.barHeight = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemBarHeight

        # fontSize (float).
        self.fontSize = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = \
            PriceBarChartSettings.\
            defaultShashtihayaniDasaGraphicsItemTextEnabledFlag
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the ShashtihayaniDasaArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the ShashtihayaniDasaArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the ShashtihayaniDasaArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the ShashtihayaniDasaArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setColor(self, color):
        """Sets the bar color.
        
        Arguments:
        color - QColor object for the bar color.
        """
        
        self.color = color

    def getColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.color

    def setTextColor(self, textColor):
        """Sets the text color.
        
        Arguments:
        textColor - QColor object for the text color.
        """

        self.textColor = textColor
        
    def getTextColor(self):
        """Gets the text color as a QColor object."""

        return self.textColor
        
    def setBarHeight(self, barHeight):
        """Sets the bar height (float)."""

        self.barHeight = barHeight
    
    def getBarHeight(self):
        """Returns the bar height (float)."""

        return self.barHeight
    
    def setFontSize(self, fontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.fontSize = fontSize
    
    def getFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.fontSize
    
    def isReversed(self):
        """Returns whether or not the musicalRatios are in reversed order.
        This value is used to tell how ratios are referenced (from the
        endpoint instead of from the startpoint).
        """

        return self.reversedFlag

    def setReversed(self, reversedFlag):
        """Sets the reversed flag.  This value is used to tell how
        the musical ratios are referenced (from the endpoint instead of from the
        startpoint).

        Arguments:
        reversedFlag - bool value for whether or not the musicalRatios
                       are reversed.
        """

        self.reversedFlag = reversedFlag
        
    def isTextEnabled(self):
        """Returns whether or not the text is enabled for the
        musicalRatios that are enabled.
        """

        return self.textEnabledFlag

    def setTextEnabled(self, textEnabledFlag):
        """Sets the textEnabled flag.  This value is used to tell
        whether or not the text is enabled for the musicalRatios that
        are enabled.

        Arguments:
        textEnabledFlag - bool value for whether or not the text is enabled.
        """

        self.textEnabledFlag = textEnabledFlag
        
    def getXYForMusicalRatio(self, index):
        """Returns the x and y location of where this musical ratio
        would exist, based on the MusicalRatio ordering and the
        startPoint and endPoint locations.

        Arguments:
        
        index - int value for index into self.musicalRatios that the
        user is looking for the musical ratio for.  This value must be
        within the valid index limits.

        Returns:
        
        Tuple of 2 floats, representing (x, y) point.  This is where
        the musical ratio would exist.
        """

        self.log.debug("Entered getXYForMusicalRatio({})".format(index))

        # Validate input.
        if index < 0:
            self.log.error("getXYForMusicalRatio(): Invalid index: {}".
                           format(index))
            return
        if len(self.musicalRatios) > 0 and index >= len(self.musicalRatios):
            self.log.error("getXYForMusicalRatio(): Index out of range: {}".
                           format(index))
            return
        
        # Return values.
        x = None
        y = None

        startPointX = self.startPointF.x()
        startPointY = self.startPointF.y()
        endPointX = self.endPointF.x()
        endPointY = self.endPointF.y()

        self.log.debug("startPoint is: ({}, {})".
                       format(startPointX, startPointY))
        self.log.debug("endPoint is: ({}, {})".
                       format(endPointX, endPointY))
        
        deltaX = endPointX - startPointX
        deltaY = endPointY - startPointY
        
        self.log.debug("deltaX is: {}".format(deltaX))
        self.log.debug("deltaY is: {}".format(deltaY))
        
        # Need to maintain offsets so that if the ratios are rotated a
        # certain way, then we have the correct starting point.
        xOffset = 0.0
        yOffset = 0.0

        
        self.log.debug("There are {} number of musical ratios.".\
                       format(len(self.musicalRatios)))

        for i in range(len(self.musicalRatios)):
            musicalRatio = self.musicalRatios[i]
            
            self.log.debug("self.musicalRatios[{}].getRatio() is: {}".\
                           format(i, musicalRatio.getRatio()))
            if i == 0:
                # Store the offset for future indexes.
                xOffset = deltaX * (musicalRatio.getRatio() - 1.0)
                yOffset = deltaY * (musicalRatio.getRatio() - 1.0)

                self.log.debug("At i == 0.  xOffset={}, yOffset={}".\
                               format(xOffset, yOffset))
                
            if i == index:
                self.log.debug("At the i == index, where i == {}.".format(i))
                self.log.debug("MusicalRatio is: {}".\
                               format(musicalRatio.getRatio()))
                
                x = (deltaX * (musicalRatio.getRatio() - 1.0)) - xOffset
                y = (deltaY * (musicalRatio.getRatio() - 1.0)) - yOffset

                self.log.debug("(x={}, y={})".format(x, y))

                # Normalize x and y to be within the range of
                # [startPointX, endPointX] and [startPointY,
                # endPointY]

                # If we are reversed, then reference the offset x and
                # y from the end point instead of the start point.
                if self.isReversed() == False:
                    x = startPointX + x
                    y = startPointY + y
                else:
                    x = endPointX - x
                    y = endPointY - y
                    

                self.log.debug("Adjusting to start points, (x={}, y={})".
                               format(x, y))
                
                while x < startPointX and x < endPointX:
                    x += abs(deltaX)
                while x > startPointX and x > endPointX:
                    x -= abs(deltaX)
                while y < startPointY and y < endPointY:
                    y += abs(deltaY)
                while y > startPointY and y > endPointY:
                    y -= abs(deltaY)

                self.log.debug("For index {}, ".format(i) +
                               "normalized x and y from startPoint is: " +
                               "({}, {})".format(x, y))

                # Break out of for loop because we found what we are
                # looking for, which is the x and y values.
                break

        if x == None or y == None:
            # This means that the index requested that the person
            # passed in as a parameter is an index that doesn't map to
            # list length of self.musicalRatios.
            self.log.warn("getXYForMusicalRatio(): " +
                          "Index provided is out of range!")
            # Reset values to 0.
            x = 0.0
            y = 0.0
            
        self.log.debug("Exiting getXYForMusicalRatio({}), ".format(index) + \
                       "Returning ({}, {})".format(x, y))
        return (x, y)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.\
            getLogger("data_objects.PriceBarChartShashtihayaniDasaArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartShashtihayaniDasaArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartScaling:
    """Class that holds information about the scaling of a PriceBarChart.
    """

    def __init__(self, 
                 unitsOfTime=1.0, 
                 unitsOfPrice=1.0,
                 viewScalingX=1.0,
                 viewScalingY=1.0,
                 name="", 
                 description=""):
        """Initializes the members in this class.  
        If default arguments are used, then an identity matrix is
        used for the scaling.
        """

        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = logging.getLogger("data_objects.PriceBarChartScaling")

        # Store class members.
        self.name = name
        self.description = description
        self.unitsOfTime = unitsOfTime
        self.unitsOfPrice = unitsOfPrice

        # Scaling used for the view.
        self.viewScalingX = 1.0
        self.viewScalingY = 1.0
        
        # Set the internally stored QTransform.
        self.transform = QTransform()
        self.transform.reset()
        self.transform.scale(self.viewScalingX, self.viewScalingY)

    def setUnitsOfTime(self, unitsOfTime):
        """Updates the units-of-time variable part of scaling.

        Arguments:
            
        unitsOfTime - float value representing the units-of-time part of
        scaling.
        """

        self.unitsOfTime = unitsOfTime

    def getUnitsOfTime(self):
        """Returns the units-of-time part of the ratio used in scaling."""

        return self.unitsOfTime
    
    def setUnitsOfPrice(self, unitsOfPrice):
        """Updates the units-of-price variable part of scaling.

        Arguments:
            
        unitsOfPrice - float value representing the units-of-price part of
        scaling.
        """

        self.unitsOfPrice = unitsOfPrice

    def getUnitsOfPrice(self):
        """Returns the units-of-price part of the ratio used in scaling."""

        return self.unitsOfPrice

    def setViewScalingX(self, viewScalingX):
        """Sets the scaling used for the view, which is separate from
        the normal scaling of units.
        """

        self.viewScalingX = viewScalingX

        self._updateTransform()

    def getViewScalingX(self):
        """Gets the scaling used for the view, which is separate from
        the normal scaling of units.
        """

        return self.viewScalingX

    def setViewScalingY(self, viewScalingY):
        """Sets the scaling used for the view, which is separate from
        the normal scaling of units.
        """

        self.viewScalingY = viewScalingY

        self._updateTransform()
        
    def getViewScalingY(self):
        """Gets the scaling used for the view, which is separate from
        the normal scaling of units.
        """

        return self.viewScalingY

    def getTransform(self):
        """Returns the QTransform holding the settings for scaling as
        indicated by the variables in this class."""

        return QTransform(self.transform.m11(),
                          self.transform.m12(),
                          self.transform.m13(),
                          self.transform.m21(),
                          self.transform.m22(),
                          self.transform.m23(),
                          self.transform.m31(),
                          self.transform.m32(),
                          self.transform.m33())

    def _updateTransform(self):
        """Updates the self.transform object with the view scaling
        values set in this object.
        """
        
        self.transform.reset()
        self.transform.scale(self.viewScalingX, self.viewScalingY)
        
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()
        
    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv
    
    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartScaling")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartScaling.__name__ +
                       " object of version {}".format(self.classVersion))

class LookbackMultiple:
    """Contains data and parameters for the amount of time to look
    back when drawing or comparing past PriceBar data to current
    present PriceBar data.
    """

    def __init__(self,
                 name="",
                 description="",
                 lookbackMultiple=1.0,
                 baseUnit=1.0,
                 baseUnitTypeDegreesFlag=False,
                 baseUnitTypeRevolutionsFlag=True,
                 color=QColor(Qt.blue),
                 enabled=False,
                 planetName="Sun",
                 geocentricFlag=True,
                 heliocentricFlag=False,
                 tropicalFlag=True,
                 siderealFlag=False
                 ):
        """Initializes the member variables to the values specified as
        arguments.

        The lookback period of time is determined by multiplying,
        depending on whether the baseUnit is in degrees or in
        revolutions:
        
            lookbackMultiple * baseUnit * 1.0
            lookbackMultiple * baseUnit * 360.0

        Arguments:
        
        name     - str value for the name of the LookbackMultiple.
                   This is the display name used in the UI.
    
        description - str value for the description of the LookbackMultiple.

        lookbackMultiple - float value for the multiple to look back.
        
        baseUnit - float value for the base unit to look back.
        
        baseUnitTypeDegreesFlag - boolean for indicating that the
                                  baseUnit is in degrees.  If this
                                  value if True, then
                                  baseUnitTypeRevolutionsFlag must be
                                  False.  If this value is False, then
                                  baseUnitTypeRevolutionsFlag must be
                                  True.
        
        baseUnitTypeRevolutionsFlag - boolean for indicating that the
                                      baseUnit is in revolutions.  If
                                      this value is True, then
                                      baseUnitTypeDegreesFlag must be
                                      False.  If this value is False,
                                      then baseUnitTypeDegreesFlag
                                      must be True.

        color - QColor object holding the color that will be used to
                draw the PriceBars of the past history.

        enabled - boolean for whether this LookbackMultiple is enabled
                  or disabled.  An enabled LookbackMultiple is drawn.
        
        planetName - str value holding a valid planet name (from
                     Ephemeris.py) to use for the looking back in time.
        
        geocentricFlag - boolean flag indicating that the lookback is
                         to be done with geocentric planet
                         measurements.  If this value is True, then
                         heliocentricFlag must be False.  If this
                         value is False, then heliocentricFlag must be
                         True.
        
        heliocentricFlag - boolean flag indicating that the lookback
                         is to be done with heliocentric planet
                         measurements.  If this value is True, then
                         geocentricFlag must be False.  If this value
                         is False, then geocentricFlag must be True.

        tropicalFlag - boolean flag that indicates that the measurements 
                       are using the tropical zodiac.  If this value 
                       is True then siderealFlag must be False.  
                       If this value is False, then siderealFlag must be True.

        siderealFlag - boolean flag that indicates that the measurements 
                       are using sidereal zodiac.  If this value
                       is True then tropicalFlag must be False.
                       If this value is False then tropicalFlag must be True.
        """

        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = logging.getLogger("data_objects.LookbackMultiple")

        # Validate input.

        if baseUnitTypeDegreesFlag == None or \
           baseUnitTypeRevolutionsFlag == None or \
           baseUnitTypeDegreesFlag == baseUnitTypeRevolutionsFlag:
            self.log.error("Invalid parameters.  " +
                           "Base Planet for the LookbackMulitple must be " +
                           "either geocentric or heliocentric.")
            self.log.error("baseUnitTypeDegreesFlag == {}".
                           format(baseUnitTypeDegreesFlag))
            self.log.error("baseUnitTypeRevolutionsFlag == {}".
                           format(baseUnitTypeRevolutionsFlag))
            return
            
        if geocentricFlag == None or heliocentricFlag == None or \
               geocentricFlag == heliocentricFlag:
            self.log.error("Invalid parameters.  " +
                           "Planet for the LookbackMulitple must be " +
                           "either geocentric or heliocentric.")
            self.log.error("geocentricFlag == {}".format(geocentricFlag))
            self.log.error("heliocentricFlag == {}".format(heliocentricFlag))
            return
        
        if planetName == "" or \
                planetName not in Ephemeris.getSupportedPlanetNamesList():

            self.log.error("Invalid planet name given: '{}'".format(planetName))
            return

        if tropicalFlag == None or siderealFlag == None or \
            tropicalFlag == siderealFlag:

            self.log.error("Invalid parameters.  " +
                           "zodiac type for the longitude " + 
                           "measurements must be " +
                           "either tropical or sidereal.")
            self.log.error("tropicalFlag == {}".format(tropicalFlag))
            self.log.error("siderealFlag == {}".format(siderealFlag))
            return

        # Display name.  (str)
        self.name = name

        # Description.  (str)
        self.description = description

        # Multiple.  (float)
        self.lookbackMultiple = lookbackMultiple

        # Base unit that gets multipled to the lookback multiple.
        self.baseUnit = baseUnit
        
        # Flag that indicates the base unit is in units degrees.
        self.baseUnitTypeDegreesFlag = baseUnitTypeDegreesFlag
        
        # Flag that indicates the base unit is in units revolutions.
        self.baseUnitTypeRevolutionsFlag = baseUnitTypeRevolutionsFlag
        
        # Color to draw the past history.  (QColor)
        self.color = color

        # Enabled flag.  (boolean)
        self.enabled = enabled

        # Planet name of the planet to use for looking back.  (str)
        self.planetName = planetName

        # Flag that indicates to use geocentric planet measurements. (boolean)
        self.geocentricFlag = geocentricFlag

        # Flag that indicates to use heliocentric planet measurements. (boolean)
        self.heliocentricFlag = heliocentricFlag

        # Flag that indicates to use the tropical zodiac for longitude
        # measurements. (boolean)
        self.tropicalFlag = tropicalFlag

        # Flag that indicates to use the sidereal zodiac for longitude
        # measurements. (boolean)
        self.siderealFlag = siderealFlag


    def getName(self):
        """Returns the display name of the LookbackMultiple."""
        
        return self.name

    def setName(self, name):
        """Sets the display name of the LookbackMultiple.

        Arguments:
        name - str value represneting the name of the LookbackMultiple."
        """

        self.name = name

    def getDescription(self):
        """Returns the description of the LookbackMultiple."""
        
        return self.description

    def setDescription(self, description):
        """Sets the description of the LookbackMultiple.

        Arguments:
        description - str value representing the description of the 
                      LookbackMultiple.
        """

        self.description = description

    def getLookbackMultiple(self):
        """Returns the multiple of time to look backwards in time."""

        return self.lookbackMultiple

    def setLookbackMultiple(self, lookbackMultiple):
        """Sets the multiple of time to look backwards in time.

        Arguments:
        lookbackMultiple - float value representing the multiple of
                           time to look backwards.
        """

        self.lookbackMultiple = lookbackMultiple

    def getBaseUnit(self):
        """Returns the base unit multiple to look back in time."""

        return self.baseUnit
    
    def setBaseUnit(self, baseUnit):
        """Sets the base unit multiple to look back in time.

        Arguments:
        baseUnit - float value for the base unit to look back.
        """

        self.baseUnit = baseUnit

    def getBaseUnitTypeDegreesFlag(self):
        """Returns the boolean flag that indicates whether or not the
        baseUnit is in degrees.
        """

        return self.baseUnitTypeDegreesFlag

    def setBaseUnitTypeDegreesFlag(self, baseUnitTypeDegreesFlag):
        """Sets the boolean flag that indicates whether or not the
        baseUnit is in degrees.

        Note: Setting this flag will automatically set the
        baseUnitTypeRevolutionsFlag to the opposite of this value.

        Arguments:
        baseUnitTypeDegreesFlag - boolean value for indicating that the
                                  baseUnit is in degrees.  
        """

        self.baseUnitTypeDegreesFlag = baseUnitTypeDegreesFlag
        self.baseUnitTypeRevolutionsFlag = not baseUnitTypeDegreesFlag

    def getBaseUnitTypeRevolutionsFlag(self):
        """Returns the boolean flag that indicates whether or not the
        baseUnit is in revolutions.
        """

        return self.baseUnitTypeRevolutionsFlag

    def setBaseUnitTypeRevolutionsFlag(self, baseUnitTypeRevolutionsFlag):
        """Sets the boolean flag that indicates whether or not the
        baseUnit is in revolutions.

        Note: Setting this flag will automatically set the
        baseUnitTypeDegreesFlag to the opposite of this value.

        Arguments:
        baseUnitTypeRevolutionsFlag - boolean value for indicating that the
                                  baseUnit is in revolutions.  
        """

        self.baseUnitTypeRevolutionsFlag = baseUnitTypeRevolutionsFlag
        self.baseUnitTypeDegreesFlag = not baseUnitTypeRevolutionsFlag


    def getColor(self):
        """Returns the color of the PriceBars for the lookback multiple, as
        a QColor object.
        """

        return self.color
        
    def setColor(self, color):
        """Sets the color of the PriceBars for the lookback multiple.

        Arguments:
        color - QColor object holding the color that will be used to
                draw the PriceBars of the past history.
        """

        self.color = color

    def getEnabled(self):
        """Returns the boolean flag for whether this LookbackMultiple
        is enabled or disabled.  An enabled LookbackMultiple is
        drawn.
        """

        return self.enabled

    def setEnabled(self, enabled):
        """Sets the flag for whether this LookbackMultiple
        is enabled or disabled.  An enabled LookbackMultiple is
        drawn.

        Arguments:
        enabled - boolean for whether this LookbackMultiple is enabled
                  or disabled.  An enabled LookbackMultiple is drawn.
        """

        self.enabled = enabled

    def getPlanetName(self):
        """Returns the name of the planet (from the list in
        Ephemeris.py) to use for the lookback multiple.
        """

        return self.planetName

    def setPlanetName(self, planetName):
        """Sets the name of the planet (from the list in
        Ephemeris.py) to use for the lookback multiple.

        Arguments:
        planetName - str value holding a valid planet name (from
                     Ephemeris.py) to use for the looking back in time.
        """

        self.planetName = planetName
        
    def getGeocentricFlag(self):
        """Returns the boolean flag indicating that the lookback is to
        be done with geocentric planet measurements.
        """

        return self.geocentricFlag

    def setGeocentricFlag(self, geocentricFlag):
        """Sets the boolean flag indicating that the lookback is to
        be done with geocentric planet measurements.
        
        Note: Setting this flag will automatically set the
        heliocentricFlag to the opposite of this value.
        """

        self.geocentricFlag = geocentricFlag
        self.heliocentricFlag = not geocentricFlag

    def getHeliocentricFlag(self):
        """Returns the boolean flag indicating that the lookback is to
        be done with heliocentric planet measurements.
        """

        return self.heliocentricFlag

    def setHeliocentricFlag(self, heliocentricFlag):
        """Sets the boolean flag indicating that the lookback is to
        be done with heliocentric planet measurements.
        
        Note: Setting this flag will automatically set the
        geocentricFlag to the opposite of this value.
        """

        self.heliocentricFlag = heliocentricFlag
        self.geocentricFlag = not heliocentricFlag
        
    def getTropicalFlag(self):
        """Returns the boolean flag that indicates that the tropical
        zodiac should be used for longitude measurements.
        """

        return self.tropicalFlag

    def setTropicalFlag(self, tropicalFlag):
        """Sets the boolean flag that indicates that the tropical
        zodiac should be used for longitude measurements.

        Note: Setting this flag will automatically set the
        siderealFlag to the opposite of this value.
        """

        self.tropicalFlag = tropicalFlag
        self.siderealFlag = not tropicalFlag

    def getSiderealFlag(self):
        """Returns the boolean flag that indicates that the sidereal
        zodiac should be used for longitude measurements.
        """

        return self.siderealFlag

    def setSiderealFlag(self, siderealFlag):
        """Sets the boolean flag that indicates that the sidereal
        zodiac should be used for longitude measurements.

        Note: Setting this flag will automatically set the
        tropicalFlag to the opposite of this value.
        """

        self.siderealFlag = siderealFlag
        self.tropicalFlag = not siderealFlag

    def toShortString(self):
        """Returns a short str representation of only some of the member
        variables of this object.

        The returned string is in the format of:
        
            MyName (G.Mars Trop. 3 x 1 rev.)
            MyName (G.MoSu Trop. 7 x 360 deg.)
            MyName (H.Venus Sid. 1.618 x 360 deg.)
        """

        nameStr = self.name

        centricityTypeStr = ""
        if self.geocentricFlag == True:
            centricityTypeStr = "G."
        if self.heliocentricFlag == True:
            centricityTypeStr = "H."
            
        planetNameStr = self.planetName
        lookbackMultipleStr = "{}".format(self.lookbackMultiple)
        
        longitudeTypeStr = ""
        if self.tropicalFlag == True:
            longitudeTypeStr = "Trop."
        if self.siderealFlag == True:
            longitudeTypeStr = "Sid."
            
        baseUnitStr = "{}".format(self.baseUnit)

        baseUnitTypeStr = ""
        if self.baseUnitTypeDegreesFlag == True:
            baseUnitTypeStr = "deg."
        if self.baseUnitTypeRevolutionsFlag == True:
            baseUnitTypeStr = "rev."

        # Return value.
        rv = "{} ({}{} {} {} x {} {})".\
            format(nameStr, 
                   centricityTypeStr, 
                   planetNameStr, 
                   longitudeTypeStr,
                   lookbackMultipleStr, 
                   baseUnitStr, 
                   baseUnitTypeStr)
        
        return rv


    def toString(self):
        """Returns the string representation of most of the attributes in this
        LookbackMultiple object.
        """
        
        rv = Util.objToString(self)

        return rv

    def __eq__(self, other):
        """Returns True if the two LookbackMultiples are equal."""
        
        rv = True
        
        leftObj = self
        rightObj = other
        
        if rightObj == None:
            return False
        
        self.log.debug("leftObj: {}".format(leftObj.toString()))
        self.log.debug("rightObj: {}".format(rightObj.toString()))

        if leftObj.classVersion != rightObj.classVersion:
            self.log.debug("classVersion differs.")
            rv = False
        if leftObj.name != rightObj.name:
            self.log.debug("name differs.")
            rv = False
        if leftObj.description != rightObj.description:
            self.log.debug("description differs.")
            rv = False
        if leftObj.lookbackMultiple != rightObj.lookbackMultiple:
            self.log.debug("lookbackMultiple differs.")
            rv = False
        if leftObj.baseUnit != rightObj.baseUnit:
            self.log.debug("baseUnit differs.")
            rv = False
        if leftObj.baseUnitTypeDegreesFlag != rightObj.baseUnitTypeDegreesFlag:
            self.log.debug("baseUnitTypeDegreesFlag differs.")
            rv = False
        if leftObj.baseUnitTypeRevolutionsFlag != \
                rightObj.baseUnitTypeRevolutionsFlag:
            self.log.debug("baseUnitTypeRevolutionsFlag differs.")
            rv = False
        if leftObj.color != rightObj.color:
            self.log.debug("color differs.")
            rv = False
        if leftObj.enabled != rightObj.enabled:
            self.log.debug("enabled differs.")
            rv = False
        if leftObj.planetName != rightObj.planetName:
            self.log.debug("planetName differs.")
            rv = False
        if leftObj.geocentricFlag != rightObj.geocentricFlag:
            self.log.debug("geocentricFlag differs.")
            rv = False
        if leftObj.heliocentricFlag != rightObj.heliocentricFlag:
            self.log.debug("heliocentricFlag differs.")
            rv = False
        if leftObj.tropicalFlag != rightObj.tropicalFlag:
            self.log.debug("tropicalFlag differs.")
            rv = False
        if leftObj.siderealFlag != rightObj.siderealFlag:
            self.log.debug("siderealFlag differs.")
            rv = False

        self.log.debug("__eq__() returning: {}".format(rv))
        
        return rv

    def __ne__(self, other):
        """Returns True if the LookbackMultiples are not equal.
        Returns False otherwise."""

        return not self.__eq__(other)
    
    def __str__(self):
        """Returns the string representation of most of the attributes in this
        LookbackMultiple object.
        """

        return self.toString()

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.LookbackMultiple")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " + LookbackMultiple.__name__ +
                       " object of version {}".format(self.classVersion))


class LookbackMultiplePriceBar:
    """Contains price information for a historic period of time,
    projected onto the current time period.
    
    The this class has the same information provided as member
    variables, and methods as the regular PriceBar class, but it is not
    a subclass of a PriceBar.  

    TODO:  improve documentation and commenting here for LookbackMultiplePriceBar.

    LookbackMultiplePriceBar can include the following information: 

    - timestamp of the current period of time.
    - timestamp of the historic period of time.  
    (this is extracted from the PriceBar)
    - PriceBar object for the price information of a historical time period.
    - LookbackMultiple object for this LookbackMultiplePriceBar
    """
    
    def __init__(self, lookbackMultiple, historicPriceBar):
        """Initializes the PriceBar object.  

# currentPriceBar - this is calculated based on the arguments given.  

        Arguments are as follows: 
TODO:  Think about what variables and information would be needed in this class. 
        lookbackMultiple - LookbackMultiple that is associated with this LookbackMultiplePriceBar.
        priceBar - PriceBar object that is the closest 
        """

        self.log = logging.getLogger("data_objects.LookbackMultiple")

        # Class version stored for pickling and unpickling.
        self.classVersion = 1

        # Verify that neither of the inputs are None.
        

        self.lookbackMultiple = lookbackMultiple
        self.historicPriceBar = historicPriceBar

        
        # Member variables that hold information about this particular
        # LookbackMultiplePriceBar's information.  
        # 
        # The data of member variables are basically the historic PriceBar, but
        # projected into the future by the LookbackMultiple's time period.  The
        # price data here is not meaningful, because it is the historic
        # PriceBar's information, but with scaling applied for charting
        # purposes, and it is only meaningful relative to other
        # LookbackMultiplePriceBar next to this one.
        self.timestamp = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.oi = None
        self.vol = None
        self.tags = []

        
        #self.currentTimestamp = self.currentPriceBar.timestamp
        #self.historicTimestamp = self.historicPriceBar.timestamp
        
    def recalculateCurrentTimestamp(self):
        """Based on the information in self.lookbackMultiple, this
        method will recalculate the currentTimestamp corresponding to
        the lookback period.
        """
        
        # TODO:  add code here for recalculateCurrentTimestamp().  To think about: Should I even be making ephemeris-type calculations within a LookbackMultiplePriceBar?  Or should the ephemeris-type calculations be done in a separate class or method somewhere else?
        pass
    

    def midPrice(self):
        """Returns the average of the high and low.  I.e., ((high+low)/2.0)
        If high is None or low is None, then None is returned.
        """

        if self.high == None or self.low == None:
            return None
        else:
            return (self.high + self.low) / 2.0

    def addTag(self, tagToAdd):
        """Adds a given tag string to the tags for this 
        LookbackMultiplePriceBar."""

        # Strip any leading or trailing whitespace
        tagToAdd = tagToAdd.strip()

        # The tag added must be non-empty and must not already exist in the
        # list.
        if tagToAdd != "" and tagToAdd not in self.tags:
            self.tags.append(tagToAdd)

    def hasTag(self, tagToCheck):
        """Returns True if the given tagToCheck is in the list of tags."""

        if tagToCheck in self.tags:
            return True
        else:
            return False

    def clearTags(self):
        """Clears all the tags associated with this LookbackMultiplePriceBar."""

        self.tags = []

    def removeTag(self, tagToRemove):
        """Removes a given tag string from the tags in this
        LookbackMultiplePriceBar.
        """

        while tagToRemove in self.tags:
            self.tags.remove(tagToRemove)


    def hasHigherHighThan(self, anotherLookbackMultiplePriceBar):
        """Returns True if this LookbackMultiplePriceBar has a higher
        high price than LookbackMultiplePicebar
        'anotherLookbackMultiplePriceBar'
        """

        if self.high == None:
            return False
        elif anotherLookbackMultiplePriceBar.high == None:
            return True
        else:
            if self.high > anotherLookbackMultiplePriceBar.high:
                return True
            else:
                return False

    def hasLowerLowThan(self, anotherLookbackMultiplePriceBar):
        """Returns True if this LookbackMultiplePriceBar has a lower low
        price than LookbackMultpile 'anotherLookbackMultiplePriceBar'
        """

        if self.low == None:
            return False
        elif anotherLookbackMultiplePriceBar.low == None:
            return True
        else:
            if self.low < anotherLookbackMultiplePriceBar.low:
                return True
            else:
                return False


    def toString(self):
        """Returns the string representation of the
        LookbackMultiplePriceBar data.
        """

        rv = Util.objToString(self)
        
        return rv

    def __eq__(self, other):
        """Returns True if the two LookbackMultiplePriceBars are equal."""
        
        rv = True

        leftObj = self
        rightObj = other

        if rightObj == None:
            return False
        
        self.log.debug("leftObj: {}".format(leftObj.toString()))
        self.log.debug("rightObj: {}".format(rightObj.toString()))

        if leftObj.classVersion != rightObj.classVersion:
            self.log.debug("classVersion differs.")
            rv = False
        if leftObj.lookbackMultiple != rightObj.lookbackMultiple:
            self.log.debug("lookbackMultiple differs.")
            rv = False
        if leftObj.historicPriceBar != rightObj.historicPriceBar:
            self.log.debug("historicPriceBar differs.")
            rv = False
        if leftObj.timestamp != rightObj.timestamp:
            self.log.debug("timestamp differs.")
            rv = False
        if leftObj.open != rightObj.open:
            self.log.debug("open differs.")
            rv = False
        if leftObj.high != rightObj.high:
            self.log.debug("high differs.")
            rv = False
        if leftObj.low != rightObj.low:
            self.log.debug("low differs.")
            rv = False
        if leftObj.close != rightObj.close:
            self.log.debug("close differs.")
            rv = False
        if leftObj.oi != rightObj.oi:
            self.log.debug("oi differs.")
            rv = False
        if leftObj.vol != rightObj.vol:
            self.log.debug("vol differs.")
            rv = False
            
        if len(leftObj.tags) != len(rightObj.tags):
            self.log.debug("len(tags) differs.")
            rv = False
        else:
            for i in range(len(leftObj.tags)):
                if leftObj.tags[i] != rightObj.tags[i]:
                    self.log.debug("tags differs.")
                    rv = False
                    break

        self.log.debug("__eq__() returning: {}".format(rv))
        
        return rv

    def __ne__(self, other):
        """Returns True if the LookbackMultiplePriceBars are not equal.
        Returns False otherwise.
        """

        return not self.__eq__(other)
    
    def __str__(self):
        """Returns the string representation of the
        LookbackMultiplePriceBar data.
        """

        return self.toString()

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.LookbackMultiplePriceBar")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " + LookbackMultiplePriceBar.__name__ +
                       " object of version {}".format(self.classVersion))


class PriceChartDocumentData:
    """Contains all the data about the price chart and price data.
    This class is used for holding the data so that it can be 
    pickled and unpickled.
    """

    def __init__(self):
        """Initializes all instance variables."""

        # Logger
        self.log = logging.getLogger("data_objects.PriceChartDocumentData")

        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 2

        # Description label.
        self.description = ""
        
        # List of PriceBar objects, sorted by timestamp.
        self.priceBars = []
        
        # List of LookbackMultiple objects.
        self.lookbackMultiples = \
            PriceChartDocumentData.createDefaultLookbackMultiples()

        # List of PriceBarChartArtifact objects.
        self.priceBarChartArtifacts = []

        # BirthInfo object for natal birth information.
        self.birthInfo = BirthInfo()

        # Dictionary of str tag to QColor object.
        self.settingsSpreadsheetTagColors = {}

        # List of the class names of SpreadsheetCalcFormulas utilized.
        self.settingsSpreadsheetCalcFormulas = []

        # Settings information for the PriceBarChartWidget.
        self.priceBarChartSettings = PriceBarChartSettings()

        # Settings information for the PriceBarSpreadsheetWidget.
        self.priceBarSpreadsheetSettings = PriceBarSpreadsheetSettings()


        # Configuration for the timezone used.  
        # This is the pytz.timezone object that is a subclass of 
        # datetime.tzinfo.
        self.locationTimezone = pytz.utc

        # Configuration for the filename that holds the source price bar
        # data.
        self.priceBarsFileFilename = ""

        # Configuration for the number of lines to skip in the file.
        self.priceBarsFileNumLinesToSkip = 0

        # Index in self.priceBars of the last PriceBar that was selected.  
        # If none were selected at the time the application last closed, it
        # will be default to index 0 if self.priceBars is non-empty, and -1
        # if self.priceBars is empty.  This information allows the UI to 
        # center on the same PriceBar the next time the application is opened.
        self.settingsLastPriceBarIndexSelected = -1

        # Notes that are added by the user in the the GUI.
        self.userNotes = ""

        
    @staticmethod
    def createDefaultLookbackMultiples():
        """Returns a list of LookbackMultiple objects that can be used as 
        a default initial set.
        """

        # TODO: add code here for createDefaultLookbackMultiples().
        
        return []

    def setDescription(self, description):
        """Sets the description of this trading entity."""

        self.description = description

    def getDescription(self):
        """Returns the description of this trading entity."""

        return self.description

    def setBirthInfo(self, birthInfo):
        """Sets the birth natal information for this trading entity.
        Parameters:
            
        birthInfo - BirthInfo object holding the birth information.
        """

        self.log.debug("Entered PricechartDocumentData.setBirthInfo()")

        self.birthInfo = birthInfo

        self.log.debug("Exiting PricechartDocumentData.setBirthInfo()")


    def getBirthInfo(self):
        """Returns the birth info used for this trading entity."""

        return self.birthInfo

    def getUserNotes(self):
        """Returns the user notes about this trading entity."""

        return self.userNotes

    def setUserNotes(self, userNotes):
        """Sets the user notes about this trading entity."""

        self.userNotes = userNotes

    def getPriceBarsFileFilename(self):
        """Returns the source data file filename which we got the
        PriceBar data from.
        """

        return self.priceBarsFileFilename
        
    def setPriceBarsFileFilename(self, filename):
        """Sets the source data file filename which we got the
        PriceBar data from.
        """

        self.priceBarsFileFilename = filename
        
    def loadWizardData(self,
                       priceBars,
                       priceBarsFileFilename, 
                       priceBarsFileNumLinesToSkip,
                       locationTimezone,
                       description=""):
        """Loads data into this class object from the information provided
        in the parameters.  
        
        Note:  The locationTimezone argument here is only set into the internal
        member variable.  The self.birthInfo BirthInfo object does not get
        set with this value.

        Parameters:

        priceBars - list of PriceBar objects.

        priceBarsFileFilename - str holding the filename of a CSV text
                                file with price bar data.

        priceBarsFileNumLinesToSkip - int holding number of lines to skip
                                      in the file above before reading CSV 
                                      pricebar data.

        locationTimezone - Timezone name as a string, like "US/Eastern" or
                           "UTC"

        description - str holding the description of the 
                      PriceChartDocumentData
        """

        self.log.debug("Entered PricechartDocumentData.load()")

        # Store the data into variables in this class.
        self.priceBars = priceBars
        self.priceBarsFileFilename = priceBarsFileFilename
        self.priceBarsFileNumLinesToSkip = priceBarsFileNumLinesToSkip
        self.locationTimezone = pytz.timezone(locationTimezone)
        self.description = description

        self.log.debug("Number of priceBars loaded is: {}".\
                       format(len(priceBars)))

        self.log.debug("Exiting PricechartDocumentData.load()")


    def getUniquePriceBarTags(self):
        """Returns a list of strings that are the tags used in the internal 
        PriceBars. 
        """

        allTags = []
        for pb in self.priceBars:
            for tag in pb.tags:
                if (tag not in allTags):
                    allTags.append(tag)

        return allTags


    def toString(self):
        """Returns the string representation of most of the attributes in this
        PriceChartDocumentData object.
        """
        
        # Strings that hold the timestamp info of the first and last PriceBar
        # in the priceBars list.
        firstPriceBarTimestamp = ""
        lastPriceBarTimestamp = ""

        # Need to use Ephemeris.datetimeToStr() below because
        # datetime.strftime() datetime.strftime() does not work on
        # years less than 1900.
        
        if len(self.priceBars) > 0:
            firstPriceBarTimestamp = \
                Ephemeris.datetimeToStr(self.priceBars[0].timestamp)
            lastPriceBarTimestamp = \
                Ephemeris.datetimeToStr(self.priceBars[-1].timestamp)

        artifactStrings = "["
        for artifact in self.priceBarChartArtifacts:
            artifactStrings += "[{}]".format(artifact.toString())
        artifactStrings += "]"
            
        return "[{}, ".\
                   format(type(self)) + \
                "classVersion={}, ".\
                   format(self.classVersion) + \
                "description={}, ".\
                    format(self.description) + \
                "numPriceBars={}, ".\
                    format(len(self.priceBars)) + \
                "numLookbackMultiples={}, ".\
                    format(len(self.lookbackMultiples)) + \
                "numArtifacts={}, ".\
                    format(len(self.priceBarChartArtifacts)) + \
                "artifacts=[OMITTED], " + \
                "firstPriceBarTimestamp={}, ".\
                    format(firstPriceBarTimestamp) + \
                "lastPriceBarTimestamp={}, ".\
                    format(lastPriceBarTimestamp) + \
                "settingsSpreadsheetTagColors=[OMITTED], " + \
                "settingsSpreadsheetCalcFormulas=[OMITTED], " + \
                "priceBarChartSettings=[OMITTED], " + \
                "priceBarSpreadsheetSettings=[OMITTED], " + \
                "locationTimezone={}, ".\
                    format(self.locationTimezone) + \
                "priceBarsFileFilename={}, ".\
                    format(self.priceBarsFileFilename) + \
                "priceBarsFileNumLinesToSkip={}, ".\
                    format(self.priceBarsFileNumLinesToSkip) + \
                "settingsLastPriceBarIndexSelected={}, ".\
                    format(self.settingsLastPriceBarIndexSelected) + \
                "userNotes='{}']".\
                    format(self.userNotes)

    def __str__(self):
        """Returns the string representation of most of the attributes in this
        PriceChartDocumentData object.
        """

        return self.toString()

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.PriceChartDocumentData")

        # Update the object to the most current version if it is not current.
        if self.classVersion < 2:
            self.log.info("Detected an old class version of " + \
                          "PriceChartDocumentData (version {}).  ".\
                          format(self.classVersion))
            
            if self.classVersion == 1:
                # Version 2 added the following member variables:
                #
                # self.lookbackMultiples
                #
                
                try:
                    # See if the variable is set.
                    self.lookbackMultiples
                    
                    # If it got here, then the field is already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have this field.")
                    
                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # initial values.
                    self.lookbackMultiples = \
                        PriceChartDocumentData.createDefaultLookbackMultiples()

                    self.log.debug("Added field " + \
                                   "'lookbackMultiples' " + \
                                   "to the loaded PriceChartDocumentData.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 2
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
        # Log that we set the state of this object.
        self.log.debug("Set state of a " + PriceChartDocumentData.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartSettings:
    """Class that holds the default settings used in the
    PriceBarChartWidget.
    """

    # Default pen width for non-highlighted price bar.
    defaultPriceBarGraphicsItemPenWidth = 0.0

    # Default width of the left extension (opening price) of a price bar.
    defaultPriceBarGraphicsItemLeftExtensionWidth = 0.5

    # Default width of the right extension (closing price) of a price bar.
    defaultPriceBarGraphicsItemRightExtensionWidth = 0.5

    # Default pen width for a non-highlighted 
    # LookbackMultiplePriceBarGraphicsItem.
    defaultLookbackMultiplePriceBarGraphicsItemPenWidth = 0.0

    # Default width of the left extension (opening price) of a 
    # LookbackMultiplePriceBarGraphicsItem.
    defaultLookbackMultiplePriceBarGraphicsItemLeftExtensionWidth = 0.5

    # Default width of the right extension (closing price) of a 
    # LookbackMultiplePriceBarGraphicsItem.
    defaultLookbackMultiplePriceBarGraphicsItemRightExtensionWidth = 0.5

    # Default value for the BarCountGraphicsItem bar height (float).
    defaultBarCountGraphicsItemBarHeight = 4.0

    # Default value for the BarCountGraphicsItem font size (float).
    defaultBarCountGraphicsItemFontSize = 10.0

    # Default value for the BarCountGraphicsItem text X scaling (float).
    defaultBarCountGraphicsItemTextXScaling = 1.0

    # Default value for the BarCountGraphicsItem text Y scaling (float).
    defaultBarCountGraphicsItemTextYScaling = 1.0

    # Default value for the TimeMeasurementGraphicsItem bar height (float).
    defaultTimeMeasurementGraphicsItemBarHeight = 8.0

    # Default value for the TimeMeasurementGraphicsItem text X scaling (float).
    defaultTimeMeasurementGraphicsItemTextXScaling = 1.0

    # Default value for the TimeMeasurementGraphicsItem text Y scaling (float).
    defaultTimeMeasurementGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the TimeMeasurementGraphicsItem.  This includes the
    # font size.
    font = QFont("Droid Sans Mono")
    font.setPointSizeF(8)
    defaultTimeMeasurementGraphicsItemDefaultFontDescription = font.toString()

    # TimeMeasurementGraphicsItem default text color.
    defaultTimeMeasurementGraphicsItemDefaultTextColor = QColor(Qt.black)
    
    # TimeMeasurementGraphicsItem default color.
    defaultTimeMeasurementGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default value for the TimeMeasurementGraphicsItem
    # showBarsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowBarsTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtBarsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtBarsTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdBarsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdBarsTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showHoursTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowHoursTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtHoursTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtHoursTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdHoursTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdHoursTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showDaysTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowDaysTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtDaysTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtDaysTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdDaysTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdDaysTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showWeeksTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowWeeksTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtWeeksTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtWeeksTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdWeeksTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdWeeksTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showMonthsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowMonthsTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtMonthsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtMonthsTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdMonthsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdMonthsTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showTimeRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowTimeRangeTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtTimeRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdTimeRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showScaledValueRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowScaledValueRangeTextFlag = False
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtScaledValueRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdScaledValueRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showAyanaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowAyanaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtAyanaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtAyanaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdAyanaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdAyanaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showMuhurtaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowMuhurtaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtMuhurtaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdMuhurtaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showVaraTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowVaraTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtVaraTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtVaraTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdVaraTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdVaraTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showRtuTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowRtuTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtRtuTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtRtuTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdRtuTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdRtuTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showMasaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowMasaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtMasaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtMasaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdMasaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdMasaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showPaksaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowPaksaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtPaksaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtPaksaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdPaksaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdPaksaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSamaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSamaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtSamaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtSamaTextFlag = False

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdSamaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdSamaTextFlag = False

    # Default musical ratios enabled in a
    # TimeModalScaleGraphicsItem (list of MusicalRatio)
    defaultTimeModalScaleGraphicsItemMusicalRatios = \
        MusicalRatio.getMusicalRatiosForTimeModalScaleGraphicsItem()
    
    # Default color for the bar of a TimeModalScaleGraphicsItem (QColor).
    defaultTimeModalScaleGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a TimeModalScaleGraphicsItem (QColor).
    defaultTimeModalScaleGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the TimeModalScaleGraphicsItem bar height (float).
    defaultTimeModalScaleGraphicsItemBarHeight = 14.0

    # Default value for the TimeModalScaleGraphicsItem font size (float).
    defaultTimeModalScaleGraphicsItemFontSize = 8.0

    # Default value for the TimeModalScaleGraphicsItem text X scaling (float).
    defaultTimeModalScaleGraphicsItemTextXScaling = 1.0

    # Default value for the TimeModalScaleGraphicsItem text Y scaling (float).
    defaultTimeModalScaleGraphicsItemTextYScaling = 1.0

    # Default value for the TimeModalScaleGraphicsItem
    # textEnabledFlag (bool).
    defaultTimeModalScaleGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # PriceModalScaleGraphicsItem (list of MusicalRatio)
    defaultPriceModalScaleGraphicsItemMusicalRatios = \
        MusicalRatio.getMusicalRatiosForPriceModalScaleGraphicsItem()
    
    # Default color for the bar of a PriceModalScaleGraphicsItem (QColor).
    defaultPriceModalScaleGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a PriceModalScaleGraphicsItem (QColor).
    defaultPriceModalScaleGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the PriceModalScaleGraphicsItem bar width (float).
    defaultPriceModalScaleGraphicsItemBarWidth = 14.0

    # Default value for the PriceModalScaleGraphicsItem font size (float).
    defaultPriceModalScaleGraphicsItemFontSize = 8.0

    # Default value for the PriceModalScaleGraphicsItem text X scaling (float).
    defaultPriceModalScaleGraphicsItemTextXScaling = 1.0

    # Default value for the PriceModalScaleGraphicsItem text Y scaling (float).
    defaultPriceModalScaleGraphicsItemTextYScaling = 1.0

    # Default value for the PriceModalScaleGraphicsItem
    # textEnabledFlag (bool).
    defaultPriceModalScaleGraphicsItemTextEnabledFlag = True

    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # bar height (float).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemBarHeight = 8.0
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # text rotation angle, in degrees (float).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemTextRotationAngle = 90.0
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # text X scaling (float).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemTextXScaling = 1.0

    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # text Y scaling (float).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to str)
    # for the PlanetLongitudeMovementMeasurementGraphicsItem.
    # This includes the font size.
    font = QFont("Droid Sans Mono")
    font.setPointSizeF(8)
    defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription = font.toString()

    # PlanetLongitudeMovementMeasurementGraphicsItem default text color.
    defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultTextColor = QColor(Qt.black)
    
    # PlanetLongitudeMovementMeasurementGraphicsItem default color.
    defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # showGeocentricRetroAsZeroTextFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag = False
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # showGeocentricRetroAsPositiveTextFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag = False
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # showGeocentricRetroAsNegativeTextFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag = True
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # showHeliocentricTextFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag = False
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # tropicalZodiacFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag = True
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # siderealZodiacFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag = False
    
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # measurementUnitDegreesEnabled (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled = True

    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # measurementUnitCirclesEnabled (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled = True

    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # measurementUnitBiblicalCirclesEnabled (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled = False

    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH1EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH2EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH3EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH4EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH5EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH6EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH7EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH8EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH9EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH10EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH11EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetH12EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetARMCEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVertexEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetEquatorialAscendantEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetCoAscendant1EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetCoAscendant2EnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetPolarAscendantEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetHoraLagnaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetGhatiLagnaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeanLunarApogeeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetOsculatingLunarApogeeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetInterpolatedLunarApogeeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetInterpolatedLunarPerigeeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetSunEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMoonEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMercuryEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag = True
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVenusEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetEarthEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMarsEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetJupiterEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetSaturnEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetUranusEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetNeptuneEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetPlutoEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeanNorthNodeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeanSouthNodeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetTrueNorthNodeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetTrueSouthNodeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetCeresEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetPallasEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetJunoEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVestaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetIsisEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetNibiruEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetChironEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetGulikaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMandiEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeanOfFiveEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetCycleOfEightEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetAvgMaJuSaUrNePlEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetAvgJuSaUrNeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetAvgJuSaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMoSuEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeVeEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeEaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeMaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeJuEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeSaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMeUrEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVeEaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVeMaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVeJuEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVeSaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetVeUrEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetEaMaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetEaJuEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetEaSaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetEaUrEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMaJuEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMaSaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetMaUrEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetJuSaEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetJuUrEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag = False
        
    # Default value for the PlanetLongitudeMovementMeasurementGraphicsItem
    # planetSaUrEnabledFlag (bool).
    defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag = False
        
    # Default font description text (this is basically the QFont,
    # serialized to str) for the TextGraphicsItem.  This includes the
    # font size.
    font = QFont("Droid Sans")
    font.setPointSizeF(10)
    defaultTextGraphicsItemDefaultFontDescription = font.toString()

    # Default font color for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default text X scaling for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultXScaling = 1.0
    
    # Default text Y scaling for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultYScaling = 1.0

    # Default text rotation angle, in degrees (float).
    defaultTextGraphicsItemDefaultRotationAngle = 0.0
    
    # Default font description text (this is basically the QFont,
    # serialized to str) for the PriceTimeInfoGraphicsItem.  This
    # includes the font size.
    font = QFont("Droid Sans")
    font.setPointSizeF(8)
    defaultPriceTimeInfoGraphicsItemDefaultFontDescription = font.toString()

    # Default font color for the PriceTimeInfoGraphicsItem.
    defaultPriceTimeInfoGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default text X scaling for the PriceTimeInfoGraphicsItem.
    defaultPriceTimeInfoGraphicsItemDefaultXScaling = 1.0
    
    # Default text Y scaling for the PriceTimeInfoGraphicsItem.
    defaultPriceTimeInfoGraphicsItemDefaultYScaling = 1.0

    # Default value for the PriceTimeInfoGraphicsItem
    # showTimestampFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowTimestampFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showPriceFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowPriceFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtPriceFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtPriceFlag = False

    # Default value for the PriceTimeInfoGraphicsItem
    # showTimeElapsedSinceBirthFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag = False

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtTimeElapsedSinceBirthFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag = False

    # Default value for the PriceTimeInfoGraphicsItem
    # showPriceScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowPriceScaledValueFlag = False

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtPriceScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag = False
        
    # Default value for the PriceTimeInfoGraphicsItem
    # showTimeScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowTimeScaledValueFlag = False

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtTimeScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag = False
        
    # Default value for the PriceTimeInfoGraphicsItem
    # showLineToInfoPointFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowLineToInfoPointFlag = True

    # Default value for the PriceMeasurementGraphicsItem bar width (float).
    defaultPriceMeasurementGraphicsItemBarWidth = 4.0

    # Default value for the PriceMeasurementGraphicsItem text X scaling (float).
    defaultPriceMeasurementGraphicsItemTextXScaling = 1.0

    # Default value for the PriceMeasurementGraphicsItem text Y scaling (float).
    defaultPriceMeasurementGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the PriceMeasurementGraphicsItem.  This includes the
    # font size.
    font = QFont("Droid Sans Mono")
    font.setPointSizeF(8)
    defaultPriceMeasurementGraphicsItemDefaultFontDescription = font.toString()

    # PriceMeasurementGraphicsItem default text color.
    defaultPriceMeasurementGraphicsItemDefaultTextColor = QColor(Qt.black)
    
    # PriceMeasurementGraphicsItem default color.
    defaultPriceMeasurementGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default value for the PriceMeasurementGraphicsItem
    # showPriceRangeTextFlag (bool).
    defaultPriceMeasurementGraphicsItemShowPriceRangeTextFlag = True
    
    # Default value for the PriceMeasurementGraphicsItem
    # showSqrtPriceRangeTextFlag (bool).
    defaultPriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag = False

    # Default value for the PriceMeasurementGraphicsItem
    # showScaledValueRangeTextFlag (bool).
    defaultPriceMeasurementGraphicsItemShowScaledValueRangeTextFlag = False
    
    # Default value for the PriceMeasurementGraphicsItem
    # showSqrtScaledValueRangeTextFlag (bool).
    defaultPriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = False

    # Default value for the TimeRetracementGraphicsItem bar height (float).
    defaultTimeRetracementGraphicsItemBarHeight = 4.0

    # Default value for the TimeRetracementGraphicsItem text X scaling (float).
    defaultTimeRetracementGraphicsItemTextXScaling = 1.0

    # Default value for the TimeRetracementGraphicsItem text Y scaling (float).
    defaultTimeRetracementGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the TimeRetracementGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(7)
    defaultTimeRetracementGraphicsItemDefaultFontDescription = font.toString()

    # TimeRetracementGraphicsItem default text color.
    defaultTimeRetracementGraphicsItemDefaultTextColor = QColor(Qt.black)
    
    # TimeRetracementGraphicsItem default color.
    defaultTimeRetracementGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default value for the TimeRetracementGraphicsItem
    # showFullLinesFlag (bool).
    defaultTimeRetracementGraphicsItemShowFullLinesFlag = True
    
    # Default value for the TimeRetracementGraphicsItem
    # showTimeTextFlag (bool).
    defaultTimeRetracementGraphicsItemShowTimeTextFlag = True
    
    # Default value for the TimeRetracementGraphicsItem
    # showPercentTextFlag (bool).
    defaultTimeRetracementGraphicsItemShowPercentTextFlag = True
    
    # Default value for the TimeRetracementGraphicsItem
    # ratios (list of Ratio).
    defaultTimeRetracementGraphicsItemRatios = \
        Ratio.getSupportedRetracementRatios()
    
    # Default value for the PriceRetracementGraphicsItem bar width (float).
    defaultPriceRetracementGraphicsItemBarWidth = 4.0

    # Default value for the PriceRetracementGraphicsItem text X scaling (float).
    defaultPriceRetracementGraphicsItemTextXScaling = 1.0

    # Default value for the PriceRetracementGraphicsItem text Y scaling (float).
    defaultPriceRetracementGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the PriceRetracementGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(7)
    defaultPriceRetracementGraphicsItemDefaultFontDescription = font.toString()

    # PriceRetracementGraphicsItem default text color.
    defaultPriceRetracementGraphicsItemDefaultTextColor = QColor(Qt.black)
    
    # PriceRetracementGraphicsItem default color.
    defaultPriceRetracementGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default value for the PriceRetracementGraphicsItem
    # showFullLinesFlag (bool).
    defaultPriceRetracementGraphicsItemShowFullLinesFlag = True
    
    # Default value for the PriceRetracementGraphicsItem
    # showPriceTextFlag (bool).
    defaultPriceRetracementGraphicsItemShowPriceTextFlag = True
    
    # Default value for the PriceRetracementGraphicsItem
    # showPercentTextFlag (bool).
    defaultPriceRetracementGraphicsItemShowPercentTextFlag = True
    
    # Default value for the PriceRetracementGraphicsItem
    # ratios (list of Ratio).
    defaultPriceRetracementGraphicsItemRatios = \
        Ratio.getSupportedRetracementRatios()

    # Default color for the bar of a PriceTimeVectorGraphicsItem (QColor).
    defaultPriceTimeVectorGraphicsItemColor = QColor(Qt.black)

    # Default color for the text of a PriceTimeVectorGraphicsItem (QColor).
    defaultPriceTimeVectorGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the PriceTimeVectorGraphicsItem bar width (float).
    defaultPriceTimeVectorGraphicsItemBarWidth = 3.3

    # Default value for the PriceTimeVectorGraphicsItem text X scaling (float).
    defaultPriceTimeVectorGraphicsItemTextXScaling = 1.0

    # Default value for the PriceTimeVectorGraphicsItem text Y scaling (float).
    defaultPriceTimeVectorGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the PriceTimeVectorGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
    defaultPriceTimeVectorGraphicsItemDefaultFontDescription = font.toString()

    # Default value for the PriceTimeVectorGraphicsItem
    # showDistanceTextFlag (bool).
    defaultPriceTimeVectorGraphicsItemShowDistanceTextFlag = False

    # Default value for the PriceTimeVectorGraphicsItem 
    # showSqrtDistanceTextFlag (bool).
    defaultPriceTimeVectorGraphicsItemShowSqrtDistanceTextFlag = False

    # Default value for the PriceTimeVectorGraphicsItem
    # showDistanceScaledValueTextFlag (bool).
    defaultPriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag = True

    # Default value for the PriceTimeVectorGraphicsItem 
    # showSqrtDistanceScaledValueTextFlag (bool).
    defaultPriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag = False

    # Default value for the PriceTimeVectorGraphicsItem 
    # tiltedTextFlag (bool).
    defaultPriceTimeVectorGraphicsItemTiltedTextFlag = True
    
    # Default value for the PriceTimeVectorGraphicsItem 
    # angleTextFlag (bool).
    defaultPriceTimeVectorGraphicsItemAngleTextFlag = False
    
    # Default color for the bar of a LineSegmentGraphicsItem (QColor).
    defaultLineSegmentGraphicsItemColor = QColor(Qt.black)

    # Default color for the text of a LineSegmentGraphicsItem (QColor).
    defaultLineSegmentGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the LineSegmentGraphicsItem bar width (float).
    defaultLineSegmentGraphicsItemBarWidth = 3.3

    # Default value for the LineSegmentGraphicsItem text X scaling (float).
    defaultLineSegmentGraphicsItemTextXScaling = 1.0

    # Default value for the LineSegmentGraphicsItem text Y scaling (float).
    defaultLineSegmentGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the LineSegmentGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
    defaultLineSegmentGraphicsItemDefaultFontDescription = font.toString()

    # Default value for the LineSegmentGraphicsItem 
    # tiltedTextFlag (bool).
    defaultLineSegmentGraphicsItemTiltedTextFlag = True
    
    # Default value for the LineSegmentGraphicsItem 
    # angleTextFlag (bool).
    defaultLineSegmentGraphicsItemAngleTextFlag = False
    
    # Default musical ratios enabled in a
    # OctaveFanGraphicsItem (list of MusicalRatio)
    defaultOctaveFanGraphicsItemMusicalRatios = \
        MusicalRatio.getMusicalRatiosForOctaveFanGraphicsItem()
    
    # Default color for the bar of a OctaveFanGraphicsItem (QColor).
    defaultOctaveFanGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a OctaveFanGraphicsItem (QColor).
    defaultOctaveFanGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the OctaveFanGraphicsItem bar height (float).
    defaultOctaveFanGraphicsItemBarHeight = 3.3

    # Default value for the OctaveFanGraphicsItem font size (float).
    defaultOctaveFanGraphicsItemFontSize = 5.0

    # Default value for the OctaveFanGraphicsItem text X scaling (float).
    defaultOctaveFanGraphicsItemTextXScaling = 1.0

    # Default value for the OctaveFanGraphicsItem text Y scaling (float).
    defaultOctaveFanGraphicsItemTextYScaling = 1.0

    # Default value for the OctaveFanGraphicsItem
    # textEnabledFlag (bool).
    defaultOctaveFanGraphicsItemTextEnabledFlag = True

    # Default value for the FibFanGraphicsItem text X scaling (float).
    defaultFibFanGraphicsItemTextXScaling = 1.0

    # Default value for the FibFanGraphicsItem text Y scaling (float).
    defaultFibFanGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the FibFanGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
    defaultFibFanGraphicsItemDefaultFontDescription = font.toString()

    # FibFanGraphicsItem default text color.
    defaultFibFanGraphicsItemDefaultTextColor = QColor(Qt.black)
    
    # FibFanGraphicsItem default color.
    defaultFibFanGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default value for the FibFanGraphicsItem
    # ratios (list of Ratio).
    defaultFibFanGraphicsItemRatios = Ratio.getSupportedFibRatios()
    
    # Default value for the FibFanGraphicsItem bar height (float).
    defaultFibFanGraphicsItemBarHeight = 3.3

    # Default value for the FibFanGraphicsItem
    # textEnabledFlag (bool).
    defaultFibFanGraphicsItemTextEnabledFlag = True

    # Default value for the GannFanGraphicsItem text X scaling (float).
    defaultGannFanGraphicsItemTextXScaling = 1.0

    # Default value for the GannFanGraphicsItem text Y scaling (float).
    defaultGannFanGraphicsItemTextYScaling = 1.0

    # Default font (this is basically the QFont, serialized to
    # str) for the GannFanGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
    defaultGannFanGraphicsItemDefaultFontDescription = font.toString()

    # GannFanGraphicsItem default text color.
    defaultGannFanGraphicsItemDefaultTextColor = QColor(Qt.black)
    
    # GannFanGraphicsItem default color.
    defaultGannFanGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default value for the GannFanGraphicsItem
    # ratios (list of Ratio).
    defaultGannFanGraphicsItemRatios = Ratio.getSupportedGannFanRatios()
    
    # Default value for the GannFanGraphicsItem bar height (float).
    defaultGannFanGraphicsItemBarHeight = 3.3

    # Default value for the GannFanGraphicsItem
    # textEnabledFlag (bool).
    defaultGannFanGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # VimsottariDasaGraphicsItem (list of MusicalRatio)
    defaultVimsottariDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getVimsottariDasaMusicalRatios()
    
    # Default color for the bar of a VimsottariDasaGraphicsItem (QColor).
    defaultVimsottariDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a VimsottariDasaGraphicsItem (QColor).
    defaultVimsottariDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the VimsottariDasaGraphicsItem bar height (float).
    defaultVimsottariDasaGraphicsItemBarHeight = 4.0

    # Default value for the VimsottariDasaGraphicsItem font size (float).
    defaultVimsottariDasaGraphicsItemFontSize = 5.0

    # Default value for the VimsottariDasaGraphicsItem text X scaling (float).
    defaultVimsottariDasaGraphicsItemTextXScaling = 1.0

    # Default value for the VimsottariDasaGraphicsItem text Y scaling (float).
    defaultVimsottariDasaGraphicsItemTextYScaling = 1.0

    # Default value for the VimsottariDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultVimsottariDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # AshtottariDasaGraphicsItem (list of MusicalRatio)
    defaultAshtottariDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getAshtottariDasaMusicalRatios()
    
    # Default color for the bar of a AshtottariDasaGraphicsItem (QColor).
    defaultAshtottariDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a AshtottariDasaGraphicsItem (QColor).
    defaultAshtottariDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the AshtottariDasaGraphicsItem bar height (float).
    defaultAshtottariDasaGraphicsItemBarHeight = 4.0

    # Default value for the AshtottariDasaGraphicsItem font size (float).
    defaultAshtottariDasaGraphicsItemFontSize = 5.0

    # Default value for the AshtottariDasaGraphicsItem text X scaling (float).
    defaultAshtottariDasaGraphicsItemTextXScaling = 1.0

    # Default value for the AshtottariDasaGraphicsItem text Y scaling (float).
    defaultAshtottariDasaGraphicsItemTextYScaling = 1.0

    # Default value for the AshtottariDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultAshtottariDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # YoginiDasaGraphicsItem (list of MusicalRatio)
    defaultYoginiDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getYoginiDasaMusicalRatios()
    
    # Default color for the bar of a YoginiDasaGraphicsItem (QColor).
    defaultYoginiDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a YoginiDasaGraphicsItem (QColor).
    defaultYoginiDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the YoginiDasaGraphicsItem bar height (float).
    defaultYoginiDasaGraphicsItemBarHeight = 4.0

    # Default value for the YoginiDasaGraphicsItem font size (float).
    defaultYoginiDasaGraphicsItemFontSize = 5.0

    # Default value for the YoginiDasaGraphicsItem text X scaling (float).
    defaultYoginiDasaGraphicsItemTextXScaling = 1.0

    # Default value for the YoginiDasaGraphicsItem text Y scaling (float).
    defaultYoginiDasaGraphicsItemTextYScaling = 1.0

    # Default value for the YoginiDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultYoginiDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # DwisaptatiSamaDasaGraphicsItem (list of MusicalRatio)
    defaultDwisaptatiSamaDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getDwisaptatiSamaDasaMusicalRatios()
    
    # Default color for the bar of a DwisaptatiSamaDasaGraphicsItem (QColor).
    defaultDwisaptatiSamaDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a DwisaptatiSamaDasaGraphicsItem (QColor).
    defaultDwisaptatiSamaDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the DwisaptatiSamaDasaGraphicsItem bar height (float).
    defaultDwisaptatiSamaDasaGraphicsItemBarHeight = 4.0

    # Default value for the DwisaptatiSamaDasaGraphicsItem font size (float).
    defaultDwisaptatiSamaDasaGraphicsItemFontSize = 5.0

    # Default value for the DwisaptatiSamaDasaGraphicsItem text X
    # scaling (float).
    defaultDwisaptatiSamaDasaGraphicsItemTextXScaling = 1.0

    # Default value for the DwisaptatiSamaDasaGraphicsItem text Y
    # scaling (float).
    defaultDwisaptatiSamaDasaGraphicsItemTextYScaling = 1.0

    # Default value for the DwisaptatiSamaDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultDwisaptatiSamaDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # ShattrimsaSamaDasaGraphicsItem (list of MusicalRatio)
    defaultShattrimsaSamaDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getShattrimsaSamaDasaMusicalRatios()
    
    # Default color for the bar of a ShattrimsaSamaDasaGraphicsItem (QColor).
    defaultShattrimsaSamaDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a ShattrimsaSamaDasaGraphicsItem (QColor).
    defaultShattrimsaSamaDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the ShattrimsaSamaDasaGraphicsItem bar height (float).
    defaultShattrimsaSamaDasaGraphicsItemBarHeight = 4.0

    # Default value for the ShattrimsaSamaDasaGraphicsItem font size (float).
    defaultShattrimsaSamaDasaGraphicsItemFontSize = 5.0

    # Default value for the ShattrimsaSamaDasaGraphicsItem text X
    # scaling (float).
    defaultShattrimsaSamaDasaGraphicsItemTextXScaling = 1.0

    # Default value for the ShattrimsaSamaDasaGraphicsItem text Y
    # scaling (float).
    defaultShattrimsaSamaDasaGraphicsItemTextYScaling = 1.0

    # Default value for the ShattrimsaSamaDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultShattrimsaSamaDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # DwadasottariDasaGraphicsItem (list of MusicalRatio)
    defaultDwadasottariDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getDwadasottariDasaMusicalRatios()
    
    # Default color for the bar of a DwadasottariDasaGraphicsItem (QColor).
    defaultDwadasottariDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a DwadasottariDasaGraphicsItem (QColor).
    defaultDwadasottariDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the DwadasottariDasaGraphicsItem bar height (float).
    defaultDwadasottariDasaGraphicsItemBarHeight = 4.0

    # Default value for the DwadasottariDasaGraphicsItem font size (float).
    defaultDwadasottariDasaGraphicsItemFontSize = 5.0

    # Default value for the DwadasottariDasaGraphicsItem text X
    # scaling (float).
    defaultDwadasottariDasaGraphicsItemTextXScaling = 1.0

    # Default value for the DwadasottariDasaGraphicsItem text Y
    # scaling (float).
    defaultDwadasottariDasaGraphicsItemTextYScaling = 1.0

    # Default value for the DwadasottariDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultDwadasottariDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # ChaturaseetiSamaDasaGraphicsItem (list of MusicalRatio)
    defaultChaturaseetiSamaDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getChaturaseetiSamaDasaMusicalRatios()
    
    # Default color for the bar of a ChaturaseetiSamaDasaGraphicsItem (QColor).
    defaultChaturaseetiSamaDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a ChaturaseetiSamaDasaGraphicsItem (QColor).
    defaultChaturaseetiSamaDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the ChaturaseetiSamaDasaGraphicsItem bar height (float).
    defaultChaturaseetiSamaDasaGraphicsItemBarHeight = 4.0

    # Default value for the ChaturaseetiSamaDasaGraphicsItem font size (float).
    defaultChaturaseetiSamaDasaGraphicsItemFontSize = 5.0

    # Default value for the ChaturaseetiSamaDasaGraphicsItem text X
    # scaling (float).
    defaultChaturaseetiSamaDasaGraphicsItemTextXScaling = 1.0

    # Default value for the ChaturaseetiSamaDasaGraphicsItem text Y
    # scaling (float).
    defaultChaturaseetiSamaDasaGraphicsItemTextYScaling = 1.0

    # Default value for the ChaturaseetiSamaDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultChaturaseetiSamaDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # SataabdikaDasaGraphicsItem (list of MusicalRatio)
    defaultSataabdikaDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getSataabdikaDasaMusicalRatios()
    
    # Default color for the bar of a SataabdikaDasaGraphicsItem (QColor).
    defaultSataabdikaDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a SataabdikaDasaGraphicsItem (QColor).
    defaultSataabdikaDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the SataabdikaDasaGraphicsItem bar height (float).
    defaultSataabdikaDasaGraphicsItemBarHeight = 4.0

    # Default value for the SataabdikaDasaGraphicsItem font size (float).
    defaultSataabdikaDasaGraphicsItemFontSize = 5.0

    # Default value for the SataabdikaDasaGraphicsItem text X
    # scaling (float).
    defaultSataabdikaDasaGraphicsItemTextXScaling = 1.0

    # Default value for the SataabdikaDasaGraphicsItem text Y
    # scaling (float).
    defaultSataabdikaDasaGraphicsItemTextYScaling = 1.0

    # Default value for the SataabdikaDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultSataabdikaDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # ShodasottariDasaGraphicsItem (list of MusicalRatio)
    defaultShodasottariDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getShodasottariDasaMusicalRatios()
    
    # Default color for the bar of a ShodasottariDasaGraphicsItem (QColor).
    defaultShodasottariDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a ShodasottariDasaGraphicsItem (QColor).
    defaultShodasottariDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the ShodasottariDasaGraphicsItem bar height (float).
    defaultShodasottariDasaGraphicsItemBarHeight = 4.0

    # Default value for the ShodasottariDasaGraphicsItem font size (float).
    defaultShodasottariDasaGraphicsItemFontSize = 5.0

    # Default value for the ShodasottariDasaGraphicsItem text X
    # scaling (float).
    defaultShodasottariDasaGraphicsItemTextXScaling = 1.0

    # Default value for the ShodasottariDasaGraphicsItem text Y
    # scaling (float).
    defaultShodasottariDasaGraphicsItemTextYScaling = 1.0

    # Default value for the ShodasottariDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultShodasottariDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # PanchottariDasaGraphicsItem (list of MusicalRatio)
    defaultPanchottariDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getPanchottariDasaMusicalRatios()
    
    # Default color for the bar of a PanchottariDasaGraphicsItem (QColor).
    defaultPanchottariDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a PanchottariDasaGraphicsItem (QColor).
    defaultPanchottariDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the PanchottariDasaGraphicsItem bar height (float).
    defaultPanchottariDasaGraphicsItemBarHeight = 4.0

    # Default value for the PanchottariDasaGraphicsItem font size (float).
    defaultPanchottariDasaGraphicsItemFontSize = 5.0

    # Default value for the PanchottariDasaGraphicsItem text X
    # scaling (float).
    defaultPanchottariDasaGraphicsItemTextXScaling = 1.0

    # Default value for the PanchottariDasaGraphicsItem text Y
    # scaling (float).
    defaultPanchottariDasaGraphicsItemTextYScaling = 1.0

    # Default value for the PanchottariDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultPanchottariDasaGraphicsItemTextEnabledFlag = True

    # Default musical ratios enabled in a
    # ShashtihayaniDasaGraphicsItem (list of MusicalRatio)
    defaultShashtihayaniDasaGraphicsItemMusicalRatios = \
        MusicalRatio.getShashtihayaniDasaMusicalRatios()
    
    # Default color for the bar of a ShashtihayaniDasaGraphicsItem (QColor).
    defaultShashtihayaniDasaGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a ShashtihayaniDasaGraphicsItem (QColor).
    defaultShashtihayaniDasaGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the ShashtihayaniDasaGraphicsItem bar height (float).
    defaultShashtihayaniDasaGraphicsItemBarHeight = 4.0

    # Default value for the ShashtihayaniDasaGraphicsItem font size (float).
    defaultShashtihayaniDasaGraphicsItemFontSize = 5.0

    # Default value for the ShashtihayaniDasaGraphicsItem text X
    # scaling (float).
    defaultShashtihayaniDasaGraphicsItemTextXScaling = 1.0

    # Default value for the ShashtihayaniDasaGraphicsItem text Y
    # scaling (float).
    defaultShashtihayaniDasaGraphicsItemTextYScaling = 1.0

    # Default value for the ShashtihayaniDasaGraphicsItem
    # textEnabledFlag (bool).
    defaultShashtihayaniDasaGraphicsItemTextEnabledFlag = True


    def __init__(self):
        """Initializes the PriceChartSettings to default values."""

        # Logger
        self.log = logging.getLogger("data_objects.PriceBarChartSettings")

        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 11

        # List of scalings used in the PriceBarChartGraphicsView.  
        # This is list of PriceBarChartScaling objects.
        self.priceBarChartGraphicsViewScalings = []

        # Index into the self.priceBarChartGraphicsViewScalings list of
        # PriceBarChartScalings objects that indicates
        # which scaling to use.  
        self.priceBarChartGraphicsViewScalingsIndex = -1

        # Pen width for PriceBars.
        # This is a float value.
        self.priceBarGraphicsItemPenWidth = \
            PriceBarChartSettings.defaultPriceBarGraphicsItemPenWidth 

        # Width of the left extension drawn that represents the open price of a
        # PriceBar.  This is a float value.
        self.priceBarGraphicsItemLeftExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemLeftExtensionWidth 

        # Width of the right extension drawn that represents the close price of
        # a PriceBar.  This is a float value.
        self.priceBarGraphicsItemRightExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemRightExtensionWidth 

        # Pen width for LookbackMultiplePriceBars.
        # This is a float value.
        self.lookbackMultiplePriceBarGraphicsItemPenWidth = \
            PriceBarChartSettings.defaultLookbackMultiplePriceBarGraphicsItemPenWidth 

        # Width of the left extension drawn that represents the open price of a
        # LookbackMultiplePriceBar.  This is a float value.
        self.lookbackMultiplePriceBarGraphicsItemLeftExtensionWidth = \
            PriceBarChartSettings.\
                defaultLookbackMultiplePriceBarGraphicsItemLeftExtensionWidth 

        # Width of the right extension drawn that represents the close price of
        # a LookbackMultiplePriceBar.  This is a float value.
        self.lookbackMultiplePriceBarGraphicsItemRightExtensionWidth = \
            PriceBarChartSettings.\
                defaultLookbackMultiplePriceBarGraphicsItemRightExtensionWidth 

        # BarCountGraphicsItem bar height (float).
        self.barCountGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemBarHeight

        # BarCountGraphicsItem font size (float).
        self.barCountGraphicsItemFontSize = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemFontSize

        # BarCountGraphicsItem text X scaling (float).
        self.barCountGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextXScaling

        # BarCountGraphicsItem text Y scaling (float).
        self.barCountGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultBarCountGraphicsItemTextYScaling

        # TimeMeasurementGraphicsItem bar height (float).
        self.timeMeasurementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemBarHeight

        # TimeMeasurementGraphicsItem text X scaling (float).
        self.timeMeasurementGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextXScaling

        # TimeMeasurementGraphicsItem text Y scaling (float).
        self.timeMeasurementGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the TimeMeasurementGraphicsItem.  This includes the
        # font size.
        self.timeMeasurementGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultFontDescription

        # TimeMeasurementGraphicsItem default text color.
        self.timeMeasurementGraphicsItemDefaultTextColor = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultTextColor
        
        # TimeMeasurementGraphicsItem default color.
        self.timeMeasurementGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemDefaultColor
        
        # TimeMeasurementGraphicsItem showBarsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtBarsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtBarsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdBarsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdBarsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdBarsTextFlag
    
        # TimeMeasurementGraphicsItem showHoursTextFlag (bool).
        self.timeMeasurementGraphicsItemShowHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtHoursTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtHoursTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdHoursTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdHoursTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdHoursTextFlag
    
        # TimeMeasurementGraphicsItem showDaysTextFlag (bool).
        self.timeMeasurementGraphicsItemShowDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtDaysTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtDaysTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdDaysTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdDaysTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdDaysTextFlag
    
        # TimeMeasurementGraphicsItem showWeeksTextFlag (bool).
        self.timeMeasurementGraphicsItemShowWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtWeeksTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showSqrdWeeksTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdWeeksTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdWeeksTextFlag
    
        # TimeMeasurementGraphicsItem showMonthsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMonthsTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtMonthsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMonthsTextFlag

        # TimeMeasurementGraphicsItem showSqrdMonthsTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdMonthsTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMonthsTextFlag

        # TimeMeasurementGraphicsItem showTimeRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowTimeRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtTimeRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag

        # TimeMeasurementGraphicsItem showSqrdTimeRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag

        # TimeMeasurementGraphicsItem showScaledValueRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowScaledValueRangeTextFlag
    
        # TimeMeasurementGraphicsItem showSqrtScaledValueRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag

        # TimeMeasurementGraphicsItem showSqrdScaledValueRangeTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag

        # TimeMeasurementGraphicsItem showAyanaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowAyanaTextFlag

        # TimeMeasurementGraphicsItem showSqrtAyanaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtAyanaTextFlag

        # TimeMeasurementGraphicsItem showSqrdAyanaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdAyanaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdAyanaTextFlag

        # TimeMeasurementGraphicsItem showMuhurtaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMuhurtaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrtMuhurtaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrdMuhurtaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag
            
        # TimeMeasurementGraphicsItem showVaraTextFlag (bool).
        self.timeMeasurementGraphicsItemShowVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowVaraTextFlag
            
        # TimeMeasurementGraphicsItem showSqrtVaraTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtVaraTextFlag
            
        # TimeMeasurementGraphicsItem showSqrdVaraTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdVaraTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdVaraTextFlag
            
        # TimeMeasurementGraphicsItem showRtuTextFlag (bool).
        self.timeMeasurementGraphicsItemShowRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowRtuTextFlag
            
        # TimeMeasurementGraphicsItem showSqrtRtuTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtRtuTextFlag
            
        # TimeMeasurementGraphicsItem showSqrdRtuTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdRtuTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdRtuTextFlag
            
        # TimeMeasurementGraphicsItem showMasaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowMasaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrtMasaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtMasaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrdMasaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdMasaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdMasaTextFlag
            
        # TimeMeasurementGraphicsItem showPaksaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowPaksaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrtPaksaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtPaksaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrdPaksaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdPaksaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdPaksaTextFlag
            
        # TimeMeasurementGraphicsItem showSamaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSamaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrtSamaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrtSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrtSamaTextFlag
            
        # TimeMeasurementGraphicsItem showSqrdSamaTextFlag (bool).
        self.timeMeasurementGraphicsItemShowSqrdSamaTextFlag = \
            PriceBarChartSettings.\
            defaultTimeMeasurementGraphicsItemShowSqrdSamaTextFlag

        # TimeModalScaleGraphicsItem musical ratios (list of MusicalRatio).
        self.timeModalScaleGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemMusicalRatios

        # TimeModalScaleGraphicsItem bar color (QColor).
        self.timeModalScaleGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemBarColor

        # TimeModalScaleGraphicsItem text color (QColor).
        self.timeModalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextColor

        # TimeModalScaleGraphicsItem bar height (float).
        self.timeModalScaleGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemBarHeight

        # TimeModalScaleGraphicsItem font size (float).
        self.timeModalScaleGraphicsItemFontSize = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemFontSize
        
        # TimeModalScaleGraphicsItem text X scaling (float).
        self.timeModalScaleGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextXScaling

        # TimeModalScaleGraphicsItem text Y scaling (float).
        self.timeModalScaleGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextYScaling

        # TimeModalScaleGraphicsItem textEnabledFlag (bool).
        self.timeModalScaleGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextEnabledFlag

        # PriceModalScaleGraphicsItem musical ratios (list of MusicalRatio).
        self.priceModalScaleGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemMusicalRatios

        # PriceModalScaleGraphicsItem bar color (QColor).
        self.priceModalScaleGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemBarColor

        # PriceModalScaleGraphicsItem text color (QColor).
        self.priceModalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextColor

        # PriceModalScaleGraphicsItem bar width (float).
        self.priceModalScaleGraphicsItemBarWidth = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemBarWidth

        # PriceModalScaleGraphicsItem font size (float).
        self.priceModalScaleGraphicsItemFontSize = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemFontSize
        
        # PriceModalScaleGraphicsItem text X scaling (float).
        self.priceModalScaleGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextXScaling

        # PriceModalScaleGraphicsItem text Y scaling (float).
        self.priceModalScaleGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextYScaling

        # PriceModalScaleGraphicsItem textEnabledFlag (bool).
        self.priceModalScaleGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextEnabledFlag

        # PlanetLongitudeMovementMeasurementGraphicsItem bar height (float).
        self.planetLongitudeMovementMeasurementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemBarHeight

        # PlanetLongitudeMovementMeasurementGraphicsItem
        # text rotation angle (float).
        self.planetLongitudeMovementMeasurementGraphicsItemTextRotationAngle = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTextRotationAngle

        # PlanetLongitudeMovementMeasurementGraphicsItem text X scaling (float).
        self.planetLongitudeMovementMeasurementGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTextXScaling

        # PlanetLongitudeMovementMeasurementGraphicsItem text Y scaling (float).
        self.planetLongitudeMovementMeasurementGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the PlanetLongitudeMovementMeasurementGraphicsItem.
        # This includes the font size.
        self.planetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription

        # PlanetLongitudeMovementMeasurementGraphicsItem default text color.
        self.planetLongitudeMovementMeasurementGraphicsItemDefaultTextColor = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultTextColor
        
        # PlanetLongitudeMovementMeasurementGraphicsItem default color.
        self.planetLongitudeMovementMeasurementGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultColor
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # showGeocentricRetroAsZeroTextFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag
    
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # showGeocentricRetroAsPositiveTextFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag
    
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # showGeocentricRetroAsNegativeTextFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag
    
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # showHeliocentricTextFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag
    
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # tropicalZodiacFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag
    
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # siderealZodiacFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag
    
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # measurementUnitDegreesEnabled (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled

        # PlanetLongitudeMovementMeasurementGraphicsItem
        # measurementUnitCirclesEnabled (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled

        # PlanetLongitudeMovementMeasurementGraphicsItem
        # measurementUnitBiblicalCirclesEnabled (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled

        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH1EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH2EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH3EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH4EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH5EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH6EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH7EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH8EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH9EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH10EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH11EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetH12EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetARMCEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVertexEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetEquatorialAscendantEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetCoAscendant1EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetCoAscendant2EnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetPolarAscendantEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetHoraLagnaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetGhatiLagnaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeanLunarApogeeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetOsculatingLunarApogeeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetInterpolatedLunarApogeeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetInterpolatedLunarPerigeeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetSunEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMoonEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMercuryEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVenusEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetEarthEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMarsEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetJupiterEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetSaturnEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetUranusEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetNeptuneEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetPlutoEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeanNorthNodeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeanSouthNodeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetTrueNorthNodeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetTrueSouthNodeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetCeresEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetPallasEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetJunoEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVestaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetIsisEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetNibiruEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetChironEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetGulikaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMandiEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeanOfFiveEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetCycleOfEightEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetAvgMaJuSaUrNePlEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetAvgJuSaUrNeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetAvgJuSaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMoSuEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeVeEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeEaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeMaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeJuEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeSaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMeUrEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVeEaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVeMaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVeJuEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVeSaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetVeUrEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetEaMaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetEaJuEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetEaSaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetEaUrEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMaJuEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMaSaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetMaUrEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetJuSaEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetJuUrEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag
        
        # PlanetLongitudeMovementMeasurementGraphicsItem
        # planetSaUrEnabledFlag (bool).
        self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag = \
            PriceBarChartSettings.\
            defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag
        
        
        # Default font description text (this is basically the QFont,
        # serialized to str) for the TextGraphicsItem.  This includes the
        # font size.
        self.textGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultTextGraphicsItemDefaultFontDescription

        # TextGraphicsItem default font color.
        self.textGraphicsItemDefaultColor = \
            PriceBarChartSettings.defaultTextGraphicsItemDefaultColor
        
        # TextGraphicsItem default text X scaling.
        self.textGraphicsItemDefaultXScaling = \
            PriceBarChartSettings.\
            defaultTextGraphicsItemDefaultXScaling

        # TextGraphicsItem default text Y scaling.
        self.textGraphicsItemDefaultYScaling = \
            PriceBarChartSettings.\
            defaultTextGraphicsItemDefaultYScaling

        # TextGraphicsItem default rotation angle.
        self.textGraphicsItemDefaultRotationAngle = \
            PriceBarChartSettings.\
            defaultTextGraphicsItemDefaultRotationAngle
        
        # Default font description text (this is basically the QFont,
        # serialized to str) for the PriceTimeInfoGraphicsItem.  This
        # includes the font size.
        self.priceTimeInfoGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemDefaultFontDescription
            
        # PriceTimeInfoGraphicsItem default font color.
        self.priceTimeInfoGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemDefaultColor
    
        # PriceTimeInfoGraphicsItem default text X scaling.
        self.priceTimeInfoGraphicsItemDefaultXScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemDefaultXScaling
    
        # PriceTimeInfoGraphicsItem default text Y scaling.
        self.priceTimeInfoGraphicsItemDefaultYScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemDefaultYScaling

        # PriceTimeInfoGraphicsItem showTimestampFlag (bool).
        self.priceTimeInfoGraphicsItemShowTimestampFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowTimestampFlag

        # PriceTimeInfoGraphicsItem showPriceFlag (bool).
        self.priceTimeInfoGraphicsItemShowPriceFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowPriceFlag

        # PriceTimeInfoGraphicsItem showSqrtPriceFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtPriceFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtPriceFlag

        # PriceTimeInfoGraphicsItem showTimeElapsedSinceBirthFlag (bool).
        self.priceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag

        # PriceTimeInfoGraphicsItem showSqrtTimeElapsedSinceBirthFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag

        # PriceTimeInfoGraphicsItem showPriceScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowPriceScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowPriceScaledValueFlag

        # PriceTimeInfoGraphicsItem showSqrtPriceScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag
        
        # PriceTimeInfoGraphicsItem showTimeScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowTimeScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowTimeScaledValueFlag

        # PriceTimeInfoGraphicsItem showSqrtTimeScaledValueFlag (bool).
        self.priceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag
        
        # PriceTimeInfoGraphicsItem showLineToInfoPointFlag (bool).
        self.priceTimeInfoGraphicsItemShowLineToInfoPointFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeInfoGraphicsItemShowLineToInfoPointFlag

        # PriceMeasurementGraphicsItem default bar width (float).
        self.priceMeasurementGraphicsItemDefaultBarWidth = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemBarWidth
            
        # PriceMeasurementGraphicsItem default text X scaling (float).
        self.priceMeasurementGraphicsItemDefaultTextXScaling = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemTextXScaling

        # PriceMeasurementGraphicsItem default text Y scaling (float).
        self.priceMeasurementGraphicsItemDefaultTextYScaling = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemTextYScaling

        # PriceMeasurementGraphicsItem default font description (this
        # is basically the QFont, serialized to str).  This includes
        # the font size.
        self.priceMeasurementGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultFontDescription

        # PriceMeasurementGraphicsItem default text color.
        self.priceMeasurementGraphicsItemDefaultTextColor = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultTextColor
    
        # PriceMeasurementGraphicsItem default color.
        self.priceMeasurementGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemDefaultColor
    
        # PriceMeasurementGraphicsItem showPriceRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowPriceRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtPriceRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag

        # PriceMeasurementGraphicsItem showScaledValueRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowScaledValueRangeTextFlag
    
        # PriceMeasurementGraphicsItem showSqrtScaledValueRangeTextFlag (bool).
        self.priceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = \
            PriceBarChartSettings.\
            defaultPriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag
    
        # TimeRetracementGraphicsItem bar height (float).
        self.timeRetracementGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemBarHeight

        # TimeRetracementGraphicsItem text X scaling (float).
        self.timeRetracementGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextXScaling

        # TimeRetracementGraphicsItem text Y scaling (float).
        self.timeRetracementGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeRetracementGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the TimeRetracementGraphicsItem.  This includes the
        # font size.
        self.timeRetracementGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultFontDescription

        # TimeRetracementGraphicsItem default text color.
        self.timeRetracementGraphicsItemDefaultTextColor = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultTextColor
        
        # TimeRetracementGraphicsItem default color.
        self.timeRetracementGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemDefaultColor

        # TimeRetracementGraphicsItem showFullLinesFlag (bool).
        self.timeRetracementGraphicsItemShowFullLinesFlag = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowFullLinesFlag
    
        # TimeRetracementGraphicsItem showTimeTextFlag (bool).
        self.timeRetracementGraphicsItemShowTimeTextFlag = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowTimeTextFlag
    
        # TimeRetracementGraphicsItem showPercentTextFlag (bool).
        self.timeRetracementGraphicsItemShowPercentTextFlag = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemShowPercentTextFlag
    
        # TimeRetracementGraphicsItem ratios (list of Ratio).
        self.timeRetracementGraphicsItemRatios = \
            PriceBarChartSettings.\
            defaultTimeRetracementGraphicsItemRatios

        # PriceRetracementGraphicsItem bar width (float).
        self.priceRetracementGraphicsItemBarWidth = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemBarWidth

        # PriceRetracementGraphicsItem text X scaling (float).
        self.priceRetracementGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemTextXScaling

        # PriceRetracementGraphicsItem text Y scaling (float).
        self.priceRetracementGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceRetracementGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the PriceRetracementGraphicsItem.  This includes the
        # font size.
        self.priceRetracementGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultFontDescription

        # PriceRetracementGraphicsItem default text color.
        self.priceRetracementGraphicsItemDefaultTextColor = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultTextColor
        
        # PriceRetracementGraphicsItem default color.
        self.priceRetracementGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemDefaultColor

        # PriceRetracementGraphicsItem showFullLinesFlag (bool).
        self.priceRetracementGraphicsItemShowFullLinesFlag = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowFullLinesFlag
    
        # PriceRetracementGraphicsItem showPriceTextFlag (bool).
        self.priceRetracementGraphicsItemShowPriceTextFlag = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowPriceTextFlag
    
        # PriceRetracementGraphicsItem showPercentTextFlag (bool).
        self.priceRetracementGraphicsItemShowPercentTextFlag = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemShowPercentTextFlag
    
        # PriceRetracementGraphicsItem ratios (list of Ratio).
        self.priceRetracementGraphicsItemRatios = \
            PriceBarChartSettings.\
            defaultPriceRetracementGraphicsItemRatios

        # PriceTimeVectorGraphicsItem bar color (QColor).
        self.priceTimeVectorGraphicsItemColor = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemColor

        # PriceTimeVectorGraphicsItem text color (QColor).
        self.priceTimeVectorGraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTextColor
    
        # PriceTimeVectorGraphicsItem bar width (float).
        self.priceTimeVectorGraphicsItemBarWidth = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemBarWidth

        # PriceTimeVectorGraphicsItem text X scaling (float).
        self.priceTimeVectorGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTextXScaling

        # PriceTimeVectorGraphicsItem text Y scaling (float).
        self.priceTimeVectorGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the PriceTimeVectorGraphicsItem.  This includes the
        # font size.
        self.priceTimeVectorGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemDefaultFontDescription

        # PriceTimeVectorGraphicsItem showDistanceTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowDistanceTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowDistanceTextFlag

        # PriceTimeVectorGraphicsItem showSqrtDistanceTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowSqrtDistanceTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowSqrtDistanceTextFlag

        # PriceTimeVectorGraphicsItem showDistanceScaledValueTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowDistanceScaledValueTextFlag

        # PriceTimeVectorGraphicsItem
        # showSqrtDistanceScaledValueTextFlag (bool).
        self.priceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemShowSqrtDistanceScaledValueTextFlag

        # PriceTimeVectorGraphicsItem tiltedTextFlag (bool).
        self.priceTimeVectorGraphicsItemTiltedTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemTiltedTextFlag
    
        # PriceTimeVectorGraphicsItem angleTextFlag (bool).
        self.priceTimeVectorGraphicsItemAngleTextFlag = \
            PriceBarChartSettings.\
            defaultPriceTimeVectorGraphicsItemAngleTextFlag
    
        # LineSegment1GraphicsItem bar color (QColor).
        self.lineSegment1GraphicsItemColor = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemColor

        # LineSegment1GraphicsItem text color (QColor).
        self.lineSegment1GraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextColor
    
        # LineSegment1GraphicsItem bar width (float).
        self.lineSegment1GraphicsItemBarWidth = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemBarWidth

        # LineSegment1GraphicsItem text X scaling (float).
        self.lineSegment1GraphicsItemTextXScaling = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextXScaling

        # LineSegment1GraphicsItem text Y scaling (float).
        self.lineSegment1GraphicsItemTextYScaling = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the LineSegment1GraphicsItem.  This includes the
        # font size.
        self.lineSegment1GraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemDefaultFontDescription

        # LineSegment1GraphicsItem tiltedTextFlag (bool).
        self.lineSegment1GraphicsItemTiltedTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTiltedTextFlag
    
        # LineSegment1GraphicsItem angleTextFlag (bool).
        self.lineSegment1GraphicsItemAngleTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemAngleTextFlag

        # LineSegment2GraphicsItem bar color (QColor).
        self.lineSegment2GraphicsItemColor = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemColor

        # LineSegment2GraphicsItem text color (QColor).
        self.lineSegment2GraphicsItemTextColor = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextColor
    
        # LineSegment2GraphicsItem bar width (float).
        self.lineSegment2GraphicsItemBarWidth = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemBarWidth

        # LineSegment2GraphicsItem text X scaling (float).
        self.lineSegment2GraphicsItemTextXScaling = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextXScaling

        # LineSegment2GraphicsItem text Y scaling (float).
        self.lineSegment2GraphicsItemTextYScaling = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the LineSegment2GraphicsItem.  This includes the
        # font size.
        self.lineSegment2GraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemDefaultFontDescription

        # LineSegment2GraphicsItem tiltedTextFlag (bool).
        self.lineSegment2GraphicsItemTiltedTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemTiltedTextFlag
    
        # LineSegment2GraphicsItem angleTextFlag (bool).
        self.lineSegment2GraphicsItemAngleTextFlag = \
            PriceBarChartSettings.\
            defaultLineSegmentGraphicsItemAngleTextFlag

        # OctaveFanGraphicsItem musical ratios (list of MusicalRatio).
        self.octaveFanGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemMusicalRatios

        # OctaveFanGraphicsItem bar height (float)
        self.octaveFanGraphicsItemBarHeight = \
            PriceBarChartSettings.\
            defaultOctaveFanGraphicsItemBarHeight
        
        # OctaveFanGraphicsItem bar color (QColor).
        self.octaveFanGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemBarColor

        # OctaveFanGraphicsItem text color (QColor).
        self.octaveFanGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextColor

        # OctaveFanGraphicsItem text X scaling (float).
        self.octaveFanGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextXScaling

        # OctaveFanGraphicsItem text Y scaling (float).
        self.octaveFanGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextYScaling

        # OctaveFanGraphicsItem textEnabledFlag (bool).
        self.octaveFanGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultOctaveFanGraphicsItemTextEnabledFlag

        # FibFanGraphicsItem text X scaling (float).
        self.fibFanGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemTextXScaling

        # FibFanGraphicsItem text Y scaling (float).
        self.fibFanGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the FibFanGraphicsItem.  This includes the
        # font size.
        self.fibFanGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemDefaultFontDescription

        # FibFanGraphicsItem default text color.
        self.fibFanGraphicsItemDefaultTextColor = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemDefaultTextColor
    
        # FibFanGraphicsItem default color.
        self.fibFanGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemDefaultColor
    
        # FibFanGraphicsItem ratios (list of Ratio).
        self.fibFanGraphicsItemRatios = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemRatios

        # FibFanGraphicsItem bar height (float).
        self.fibFanGraphicsItemBarHeight = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemBarHeight

        # FibFanGraphicsItem textEnabledFlag (bool).
        self.fibFanGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
            defaultFibFanGraphicsItemTextEnabledFlag

        # GannFanGraphicsItem text X scaling (float).
        self.gannFanGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemTextXScaling

        # GannFanGraphicsItem text Y scaling (float).
        self.gannFanGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemTextYScaling

        # Default font (this is basically the QFont, serialized to
        # str) for the GannFanGraphicsItem.  This includes the
        # font size.
        self.gannFanGraphicsItemDefaultFontDescription = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemDefaultFontDescription

        # GannFanGraphicsItem default text color.
        self.gannFanGraphicsItemDefaultTextColor = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemDefaultTextColor
    
        # GannFanGraphicsItem default color.
        self.gannFanGraphicsItemDefaultColor = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemDefaultColor
    
        # GannFanGraphicsItem ratios (list of Ratio).
        self.gannFanGraphicsItemRatios = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemRatios

        # GannFanGraphicsItem bar height (float).
        self.gannFanGraphicsItemBarHeight = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemBarHeight

        # GannFanGraphicsItem textEnabledFlag (bool).
        self.gannFanGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
            defaultGannFanGraphicsItemTextEnabledFlag

        # VimsottariDasaGraphicsItem musical ratios (list of MusicalRatio).
        self.vimsottariDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemMusicalRatios

        # VimsottariDasaGraphicsItem bar color (QColor).
        self.vimsottariDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemBarColor

        # VimsottariDasaGraphicsItem text color (QColor).
        self.vimsottariDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemTextColor

        # VimsottariDasaGraphicsItem text X scaling (float).
        self.vimsottariDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemTextXScaling

        # VimsottariDasaGraphicsItem text Y scaling (float).
        self.vimsottariDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemTextYScaling

        # VimsottariDasaGraphicsItem textEnabledFlag (bool).
        self.vimsottariDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultVimsottariDasaGraphicsItemTextEnabledFlag

        # AshtottariDasaGraphicsItem musical ratios (list of MusicalRatio).
        self.ashtottariDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemMusicalRatios

        # AshtottariDasaGraphicsItem bar color (QColor).
        self.ashtottariDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemBarColor

        # AshtottariDasaGraphicsItem text color (QColor).
        self.ashtottariDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemTextColor

        # AshtottariDasaGraphicsItem text X scaling (float).
        self.ashtottariDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemTextXScaling

        # AshtottariDasaGraphicsItem text Y scaling (float).
        self.ashtottariDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemTextYScaling

        # AshtottariDasaGraphicsItem textEnabledFlag (bool).
        self.ashtottariDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultAshtottariDasaGraphicsItemTextEnabledFlag

        # YoginiDasaGraphicsItem musical ratios (list of MusicalRatio).
        self.yoginiDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemMusicalRatios

        # YoginiDasaGraphicsItem bar color (QColor).
        self.yoginiDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemBarColor

        # YoginiDasaGraphicsItem text color (QColor).
        self.yoginiDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemTextColor

        # YoginiDasaGraphicsItem text X scaling (float).
        self.yoginiDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemTextXScaling

        # YoginiDasaGraphicsItem text Y scaling (float).
        self.yoginiDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemTextYScaling

        # YoginiDasaGraphicsItem textEnabledFlag (bool).
        self.yoginiDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultYoginiDasaGraphicsItemTextEnabledFlag

        # DwisaptatiSamaDasaGraphicsItem musical ratios (list of MusicalRatio).
        self.dwisaptatiSamaDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemMusicalRatios

        # DwisaptatiSamaDasaGraphicsItem bar color (QColor).
        self.dwisaptatiSamaDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemBarColor

        # DwisaptatiSamaDasaGraphicsItem text color (QColor).
        self.dwisaptatiSamaDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemTextColor

        # DwisaptatiSamaDasaGraphicsItem text X scaling (float).
        self.dwisaptatiSamaDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemTextXScaling

        # DwisaptatiSamaDasaGraphicsItem text Y scaling (float).
        self.dwisaptatiSamaDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemTextYScaling

        # DwisaptatiSamaDasaGraphicsItem textEnabledFlag (bool).
        self.dwisaptatiSamaDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultDwisaptatiSamaDasaGraphicsItemTextEnabledFlag

        # ShattrimsaSamaDasaGraphicsItem musical ratios (list of MusicalRatio).
        self.shattrimsaSamaDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemMusicalRatios

        # ShattrimsaSamaDasaGraphicsItem bar color (QColor).
        self.shattrimsaSamaDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemBarColor

        # ShattrimsaSamaDasaGraphicsItem text color (QColor).
        self.shattrimsaSamaDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemTextColor

        # ShattrimsaSamaDasaGraphicsItem text X scaling (float).
        self.shattrimsaSamaDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemTextXScaling

        # ShattrimsaSamaDasaGraphicsItem text Y scaling (float).
        self.shattrimsaSamaDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemTextYScaling

        # ShattrimsaSamaDasaGraphicsItem textEnabledFlag (bool).
        self.shattrimsaSamaDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultShattrimsaSamaDasaGraphicsItemTextEnabledFlag

        # DwadasottariDasaGraphicsItem musical ratios (list of MusicalRatio).
        self.dwadasottariDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemMusicalRatios

        # DwadasottariDasaGraphicsItem bar color (QColor).
        self.dwadasottariDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemBarColor

        # DwadasottariDasaGraphicsItem text color (QColor).
        self.dwadasottariDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemTextColor

        # DwadasottariDasaGraphicsItem text X scaling (float).
        self.dwadasottariDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemTextXScaling

        # DwadasottariDasaGraphicsItem text Y scaling (float).
        self.dwadasottariDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemTextYScaling

        # DwadasottariDasaGraphicsItem textEnabledFlag (bool).
        self.dwadasottariDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultDwadasottariDasaGraphicsItemTextEnabledFlag

        # ChaturaseetiSamaDasaGraphicsItem musical ratios
        # (list of MusicalRatio).
        self.chaturaseetiSamaDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemMusicalRatios

        # ChaturaseetiSamaDasaGraphicsItem bar color (QColor).
        self.chaturaseetiSamaDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemBarColor

        # ChaturaseetiSamaDasaGraphicsItem text color (QColor).
        self.chaturaseetiSamaDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemTextColor

        # ChaturaseetiSamaDasaGraphicsItem text X scaling (float).
        self.chaturaseetiSamaDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemTextXScaling

        # ChaturaseetiSamaDasaGraphicsItem text Y scaling (float).
        self.chaturaseetiSamaDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemTextYScaling

        # ChaturaseetiSamaDasaGraphicsItem textEnabledFlag (bool).
        self.chaturaseetiSamaDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultChaturaseetiSamaDasaGraphicsItemTextEnabledFlag

        # SataabdikaDasaGraphicsItem musical ratios
        # (list of MusicalRatio).
        self.sataabdikaDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemMusicalRatios

        # SataabdikaDasaGraphicsItem bar color (QColor).
        self.sataabdikaDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemBarColor

        # SataabdikaDasaGraphicsItem text color (QColor).
        self.sataabdikaDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemTextColor

        # SataabdikaDasaGraphicsItem text X scaling (float).
        self.sataabdikaDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemTextXScaling

        # SataabdikaDasaGraphicsItem text Y scaling (float).
        self.sataabdikaDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemTextYScaling

        # SataabdikaDasaGraphicsItem textEnabledFlag (bool).
        self.sataabdikaDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultSataabdikaDasaGraphicsItemTextEnabledFlag

        # ShodasottariDasaGraphicsItem musical ratios
        # (list of MusicalRatio).
        self.shodasottariDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemMusicalRatios

        # ShodasottariDasaGraphicsItem bar color (QColor).
        self.shodasottariDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemBarColor

        # ShodasottariDasaGraphicsItem text color (QColor).
        self.shodasottariDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemTextColor

        # ShodasottariDasaGraphicsItem text X scaling (float).
        self.shodasottariDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemTextXScaling

        # ShodasottariDasaGraphicsItem text Y scaling (float).
        self.shodasottariDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemTextYScaling

        # ShodasottariDasaGraphicsItem textEnabledFlag (bool).
        self.shodasottariDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultShodasottariDasaGraphicsItemTextEnabledFlag

        # PanchottariDasaGraphicsItem musical ratios
        # (list of MusicalRatio).
        self.panchottariDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemMusicalRatios

        # PanchottariDasaGraphicsItem bar color (QColor).
        self.panchottariDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemBarColor

        # PanchottariDasaGraphicsItem text color (QColor).
        self.panchottariDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemTextColor

        # PanchottariDasaGraphicsItem text X scaling (float).
        self.panchottariDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemTextXScaling

        # PanchottariDasaGraphicsItem text Y scaling (float).
        self.panchottariDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemTextYScaling

        # PanchottariDasaGraphicsItem textEnabledFlag (bool).
        self.panchottariDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultPanchottariDasaGraphicsItemTextEnabledFlag

        # ShashtihayaniDasaGraphicsItem musical ratios
        # (list of MusicalRatio).
        self.shashtihayaniDasaGraphicsItemMusicalRatios = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemMusicalRatios

        # ShashtihayaniDasaGraphicsItem bar color (QColor).
        self.shashtihayaniDasaGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemBarColor

        # ShashtihayaniDasaGraphicsItem text color (QColor).
        self.shashtihayaniDasaGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemTextColor

        # ShashtihayaniDasaGraphicsItem text X scaling (float).
        self.shashtihayaniDasaGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemTextXScaling

        # ShashtihayaniDasaGraphicsItem text Y scaling (float).
        self.shashtihayaniDasaGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemTextYScaling

        # ShashtihayaniDasaGraphicsItem textEnabledFlag (bool).
        self.shashtihayaniDasaGraphicsItemTextEnabledFlag = \
            PriceBarChartSettings.\
                defaultShashtihayaniDasaGraphicsItemTextEnabledFlag


    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = logging.getLogger("data_objects.PriceBarChartSettings")

        # Update the object to the most current version if it is not current.
        if self.classVersion < 11:
            self.log.info("Detected an old class version of " + \
                          "PriceBarChartSettings (version {}).  ".\
                          format(self.classVersion))
            
            if self.classVersion == 1:
                # Version 2 added the following member variables:
                #
                # self.textGraphicsItemDefaultRotationAngle
                #
                
                try:
                    # See if the variable is set.
                    self.textGraphicsItemDefaultRotationAngle

                    # If it got here, then the field is already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have this field.")
                    
                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.
                    self.textGraphicsItemDefaultRotationAngle = \
                        PriceBarChartSettings.\
                        defaultTextGraphicsItemDefaultRotationAngle

                    self.log.debug("Added field " + \
                                   "'textGraphicsItemDefaultRotationAngle' " + \
                                   "to the loaded PriceBarChartSettings.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 2
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 2:
                # Version 3 added the following member variables:
                #
                # self.timeModalScaleGraphicsItemBarHeight
                # self.timeModalScaleGraphicsItemFontSize
                # self.priceModalScaleGraphicsItemBarWidth
                # self.priceModalScaleGraphicsItemFontSize
                #
                
                try:
                    # See if the variables are set.
                    self.timeModalScaleGraphicsItemBarHeight
                    self.timeModalScaleGraphicsItemFontSize
                    self.priceModalScaleGraphicsItemBarWidth
                    self.priceModalScaleGraphicsItemFontSize
                    
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")

                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.

                    # TimeModalScaleGraphicsItem bar height (float).
                    self.timeModalScaleGraphicsItemBarHeight = \
                        PriceBarChartSettings.\
                        defaultTimeModalScaleGraphicsItemBarHeight

                    # TimeModalScaleGraphicsItem font size (float).
                    self.timeModalScaleGraphicsItemFontSize = \
                        PriceBarChartSettings.\
                        defaultTimeModalScaleGraphicsItemFontSize
        
                    # PriceModalScaleGraphicsItem bar width (float).
                    self.priceModalScaleGraphicsItemBarWidth = \
                        PriceBarChartSettings.\
                        defaultPriceModalScaleGraphicsItemBarWidth

                    # PriceModalScaleGraphicsItem font size (float).
                    self.priceModalScaleGraphicsItemFontSize = \
                        PriceBarChartSettings.\
                        defaultPriceModalScaleGraphicsItemFontSize
        
                    self.log.debug("Added fields " + \
                                   "'timeModalScaleGraphicsItemBarHeight', "
                                   "'timeModalScaleGraphicsItemFontSize', "
                                   "'priceModalScaleGraphicsItemBarWidth', "
                                   "'priceModalScaleGraphicsItemFontSize', "
                                   "to the loaded PriceBarChartSettings.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 3
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 3:
                # Version 4 added the following member variables:
                #
                # self.planetLongitudeMovementMeasurementGraphicsItemBarHeight
                # self.planetLongitudeMovementMeasurementGraphicsItemTextRotationAngle
                # self.planetLongitudeMovementMeasurementGraphicsItemTextXScaling
                # self.planetLongitudeMovementMeasurementGraphicsItemTextYScaling
                # self.planetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription
                # self.planetLongitudeMovementMeasurementGraphicsItemDefaultTextColor
                # self.planetLongitudeMovementMeasurementGraphicsItemDefaultColor
                # self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled
                # self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag
                #
                
                try:
                    # See if the variables are set.
                    self.planetLongitudeMovementMeasurementGraphicsItemBarHeight
                    self.planetLongitudeMovementMeasurementGraphicsItemTextRotationAngle
                    self.planetLongitudeMovementMeasurementGraphicsItemTextXScaling
                    self.planetLongitudeMovementMeasurementGraphicsItemTextYScaling
                    self.planetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription
                    self.planetLongitudeMovementMeasurementGraphicsItemDefaultTextColor
                    self.planetLongitudeMovementMeasurementGraphicsItemDefaultColor
                    self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled
                    self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag
                    
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")

                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.

                    # PlanetLongitudeMovementMeasurementGraphicsItem bar height (float).
                    self.planetLongitudeMovementMeasurementGraphicsItemBarHeight = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemBarHeight
            
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # text rotation angle (float).
                    self.planetLongitudeMovementMeasurementGraphicsItemTextRotationAngle = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemTextRotationAngle
            
                    # PlanetLongitudeMovementMeasurementGraphicsItem text X scaling (float).
                    self.planetLongitudeMovementMeasurementGraphicsItemTextXScaling = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemTextXScaling
            
                    # PlanetLongitudeMovementMeasurementGraphicsItem text Y scaling (float).
                    self.planetLongitudeMovementMeasurementGraphicsItemTextYScaling = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemTextYScaling
            
                    # Default font (this is basically the QFont, serialized to
                    # str) for the PlanetLongitudeMovementMeasurementGraphicsItem.
                    # This includes the font size.
                    self.planetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription
            
                    # PlanetLongitudeMovementMeasurementGraphicsItem default text color.
                    self.planetLongitudeMovementMeasurementGraphicsItemDefaultTextColor = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultTextColor
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem default color.
                    self.planetLongitudeMovementMeasurementGraphicsItemDefaultColor = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemDefaultColor
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # showGeocentricRetroAsZeroTextFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag
                
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # showGeocentricRetroAsPositiveTextFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag
                
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # showGeocentricRetroAsNegativeTextFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag
                
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # showHeliocentricTextFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag
                
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # tropicalZodiacFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag
                
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # siderealZodiacFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag
                
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # measurementUnitDegreesEnabled (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled
            
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # measurementUnitCirclesEnabled (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled

                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH1EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH2EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH3EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH4EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH5EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH6EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH7EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH8EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH9EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH10EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH11EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetH12EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetARMCEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVertexEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetEquatorialAscendantEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetCoAscendant1EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetCoAscendant2EnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetPolarAscendantEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetHoraLagnaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetGhatiLagnaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeanLunarApogeeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetOsculatingLunarApogeeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetInterpolatedLunarApogeeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetInterpolatedLunarPerigeeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetSunEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMoonEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMercuryEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVenusEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetEarthEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMarsEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetJupiterEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetSaturnEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetUranusEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetNeptuneEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetPlutoEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeanNorthNodeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeanSouthNodeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetTrueNorthNodeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetTrueSouthNodeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetCeresEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetPallasEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetJunoEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVestaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetIsisEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetNibiruEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetChironEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetGulikaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMandiEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeanOfFiveEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetCycleOfEightEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetAvgMaJuSaUrNePlEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetAvgJuSaUrNeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetAvgJuSaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag
                    
                    self.log.debug(\
                        "Added fields " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemBarHeight', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemTextRotationAngle', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemTextXScaling', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemTextYScaling', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemDefaultFontDescription', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemDefaultTextColor', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemDefaultColor', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsZeroTextFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsPositiveTextFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemShowGeocentricRetroAsNegativeTextFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemShowHeliocentricTextFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemTropicalZodiacFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemSiderealZodiacFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitDegreesEnabled', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitCirclesEnabled', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH1EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH2EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH3EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH4EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH5EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH6EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH7EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH8EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH9EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH10EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH11EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetH12EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetARMCEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVertexEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetEquatorialAscendantEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant1EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetCoAscendant2EnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetPolarAscendantEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetHoraLagnaEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetGhatiLagnaEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeanLunarApogeeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetOsculatingLunarApogeeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarApogeeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetInterpolatedLunarPerigeeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetSunEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMoonEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMercuryEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVenusEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetEarthEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMarsEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetJupiterEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetSaturnEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetUranusEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetNeptuneEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetPlutoEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeanNorthNodeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeanSouthNodeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetTrueNorthNodeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetTrueSouthNodeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetCeresEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetPallasEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetJunoEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVestaEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetIsisEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetNibiruEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetChironEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetGulikaEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMandiEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeanOfFiveEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetCycleOfEightEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetAvgMaJuSaUrNePlEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaUrNeEnabledFlag', " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetAvgJuSaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 4
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 4:
                # Version 5 added the following member variables:
                #
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag
                #
                
                try:
                    # See if the variables are set.
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag
                    
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")

                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.

                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeVeEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeEaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeEaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeMaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeMaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeJuEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeJuEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeSaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeSaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMeUrEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMeUrEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVeEaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVeMaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVeJuEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVeJuEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVeSaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVeSaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetVeUrEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetVeUrEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetEaMaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetEaJuEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetEaSaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetEaUrEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetEaUrEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMaJuEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMaSaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMaSaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMaUrEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMaUrEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetJuSaEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetJuSaEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetJuUrEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetJuUrEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetSaUrEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetSaUrEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 5
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 5:
                # Version 6 added the following:
                #
                #   Many more supported Ratios for:
                #     self.priceRetracementGraphicsItemRatios
                #     self.timeRetracementGraphicsItemRatios
                #
                
                # See if the number of Ratios is the same.
                if len(self.timeRetracementGraphicsItemRatios) == \
                       len(PriceBarChartSettings.defaultTimeRetracementGraphicsItemRatios) \
                       and \
                       len(self.priceRetracementGraphicsItemRatios) == \
                       len(PriceBarChartSettings.defaultPriceRetracementGraphicsItemRatios):
                    
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")
                else:
                    # Add any Ratios in
                    # PriceBarChartSettings.defaultTimeRetracementGraphicsItemRatios
                    # that are not already in
                    # self.timeRetracementGraphicsItemRatios.
                    
                    for defaultRatio in PriceBarChartSettings.defaultTimeRetracementGraphicsItemRatios:
                        alreadyAddedFlag = False
                        
                        # Go through the ratios and see if
                        # defaultRatio is already in there.
                        for ratio in self.timeRetracementGraphicsItemRatios:
                            if Util.fuzzyIsEqual(ratio.ratio, defaultRatio.ratio):
                                alreadyAddedFlag = True

                                # We won't change the preference for
                                # if it is enabled or not, but we will
                                # overwrite the 'description' and
                                # 'mathDescription' fields for this
                                # ratio so that they are updated.
                                ratio.setDescription(defaultRatio.getDescription())
                                ratio.setMathDescription(defaultRatio.getMathDescription())
                                
                        if alreadyAddedFlag != True:
                            # This ratio is not in the current list
                            # and should be added.
                            self.timeRetracementGraphicsItemRatios.append(defaultRatio)
                            
                    # Sort by ratio value.
                    self.timeRetracementGraphicsItemRatios.sort(key=lambda r: r.ratio)


                    # Add any Ratios in
                    # PriceBarChartSettings.defaultPriceRetracementGraphicsItemRatios
                    # that are not already in
                    # self.priceRetracementGraphicsItemRatios.
                    
                    for defaultRatio in PriceBarChartSettings.defaultPriceRetracementGraphicsItemRatios:
                        alreadyAddedFlag = False

                        # Go through the ratios and see if
                        # defaultRatio is already in there.
                        for ratio in self.priceRetracementGraphicsItemRatios:
                            if Util.fuzzyIsEqual(ratio.ratio, defaultRatio.ratio):
                                alreadyAddedFlag = True

                                # We won't change the preference for
                                # if it is enabled or not, but we will
                                # overwrite the 'description' and
                                # 'mathDescription' fields for this
                                # ratio so that they are updated.
                                ratio.setDescription(defaultRatio.getDescription())
                                ratio.setMathDescription(defaultRatio.getMathDescription())
                                
                        if alreadyAddedFlag != True:
                            # This ratio is not in the current list
                            # and should be added.
                            self.priceRetracementGraphicsItemRatios.append(defaultRatio)
                            
                    # Sort by ratio value.
                    self.priceRetracementGraphicsItemRatios.sort(key=lambda r: r.ratio)


                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 6
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                    
            if self.classVersion == 6:
                # Version 7 added the following member variables:
                #
                # self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled
                #
                
                try:
                    # See if the variable is set already.
                    self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled
                    
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")

                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.

                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # measurementUnitBiblicalCirclesEnabled (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled
                    
                    self.log.debug("Added field(s): " + \
                                   "'planetLongitudeMovementMeasurementGraphicsItemMeasurementUnitBiblicalCirclesEnabled', " + \
                                   "to the loaded PriceBarChartSettings.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 7
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 7:
                # Version 8 removed the following member variables:
                #
                #   self.lineSegmentGraphicsItemColor
                #   self.lineSegmentGraphicsItemTextColor
                #   self.lineSegmentGraphicsItemBarWidth
                #   self.lineSegmentGraphicsItemTextXScaling
                #   self.lineSegmentGraphicsItemTextYScaling
                #   self.lineSegmentGraphicsItemDefaultFontDescription
                #   self.lineSegmentGraphicsItemTiltedTextFlag
                #   self.lineSegmentGraphicsItemAngleTextFlag
                #
                #   
                # 
                # Version 8 added the following member variables:
                #                
                #   self.lineSegment1GraphicsItemColor
                #   self.lineSegment1GraphicsItemTextColor
                #   self.lineSegment1GraphicsItemBarWidth
                #   self.lineSegment1GraphicsItemTextXScaling
                #   self.lineSegment1GraphicsItemTextYScaling
                #   self.lineSegment1GraphicsItemDefaultFontDescription
                #   self.lineSegment1GraphicsItemTiltedTextFlag
                #   self.lineSegment1GraphicsItemAngleTextFlag
                #   self.lineSegment2GraphicsItemColor
                #   self.lineSegment2GraphicsItemTextColor
                #   self.lineSegment2GraphicsItemBarWidth
                #   self.lineSegment2GraphicsItemTextXScaling
                #   self.lineSegment2GraphicsItemTextYScaling
                #   self.lineSegment2GraphicsItemDefaultFontDescription
                #   self.lineSegment2GraphicsItemTiltedTextFlag
                #   self.lineSegment2GraphicsItemAngleTextFlag
                #
                #

                try:
                    # See if the variable is set already.
                    
                    self.lineSegment1GraphicsItemColor
                    self.lineSegment1GraphicsItemTextColor
                    self.lineSegment1GraphicsItemBarWidth
                    self.lineSegment1GraphicsItemTextXScaling
                    self.lineSegment1GraphicsItemTextYScaling
                    self.lineSegment1GraphicsItemDefaultFontDescription
                    self.lineSegment1GraphicsItemTiltedTextFlag
                    self.lineSegment1GraphicsItemAngleTextFlag
                    self.lineSegment2GraphicsItemColor
                    self.lineSegment2GraphicsItemTextColor
                    self.lineSegment2GraphicsItemBarWidth
                    self.lineSegment2GraphicsItemTextXScaling
                    self.lineSegment2GraphicsItemTextYScaling
                    self.lineSegment2GraphicsItemDefaultFontDescription
                    self.lineSegment2GraphicsItemTiltedTextFlag
                    self.lineSegment2GraphicsItemAngleTextFlag
                    
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")

                except AttributeError:
                    # Variable was not set.  Set the new variables to
                    # what the old one was set to.
                    
                    self.lineSegment1GraphicsItemColor = \
                        self.lineSegmentGraphicsItemColor
                    self.lineSegment1GraphicsItemTextColor = \
                        self.lineSegmentGraphicsItemTextColor
                    self.lineSegment1GraphicsItemBarWidth = \
                        self.lineSegmentGraphicsItemBarWidth
                    self.lineSegment1GraphicsItemTextXScaling = \
                        self.lineSegmentGraphicsItemTextXScaling
                    self.lineSegment1GraphicsItemTextYScaling = \
                        self.lineSegmentGraphicsItemTextYScaling
                    self.lineSegment1GraphicsItemDefaultFontDescription = \
                        self.lineSegmentGraphicsItemDefaultFontDescription
                    self.lineSegment1GraphicsItemTiltedTextFlag = \
                        self.lineSegmentGraphicsItemTiltedTextFlag
                    self.lineSegment1GraphicsItemAngleTextFlag = \
                        self.lineSegmentGraphicsItemAngleTextFlag
                    self.lineSegment2GraphicsItemColor = \
                        self.lineSegmentGraphicsItemColor
                    self.lineSegment2GraphicsItemTextColor = \
                        self.lineSegmentGraphicsItemTextColor
                    self.lineSegment2GraphicsItemBarWidth = \
                        self.lineSegmentGraphicsItemBarWidth
                    self.lineSegment2GraphicsItemTextXScaling = \
                        self.lineSegmentGraphicsItemTextXScaling
                    self.lineSegment2GraphicsItemTextYScaling = \
                        self.lineSegmentGraphicsItemTextYScaling
                    self.lineSegment2GraphicsItemDefaultFontDescription = \
                        self.lineSegmentGraphicsItemDefaultFontDescription
                    self.lineSegment2GraphicsItemTiltedTextFlag = \
                        self.lineSegmentGraphicsItemTiltedTextFlag
                    self.lineSegment2GraphicsItemAngleTextFlag = \
                        self.lineSegmentGraphicsItemAngleTextFlag
                    
                    
                    self.log.debug("Added field(s): " + \
                                   "'lineSegment1GraphicsItemColor', " + \
                                   "'lineSegment1GraphicsItemTextColor', " + \
                                   "'lineSegment1GraphicsItemBarWidth', " + \
                                   "'lineSegment1GraphicsItemTextXScaling', " + \
                                   "'lineSegment1GraphicsItemTextYScaling', " + \
                                   "'lineSegment1GraphicsItemDefaultFontDescription', " + \
                                   "'lineSegment1GraphicsItemTiltedTextFlag', " + \
                                   "'lineSegment1GraphicsItemAngleTextFlag', " + \
                                   "'lineSegment2GraphicsItemColor', " + \
                                   "'lineSegment2GraphicsItemTextColor', " + \
                                   "'lineSegment2GraphicsItemBarWidth', " + \
                                   "'lineSegment2GraphicsItemTextXScaling', " + \
                                   "'lineSegment2GraphicsItemTextYScaling', " + \
                                   "'lineSegment2GraphicsItemDefaultFontDescription', " + \
                                   "'lineSegment2GraphicsItemTiltedTextFlag', " + \
                                   "'lineSegment2GraphicsItemAngleTextFlag', " + \
                                   "to the loaded PriceBarChartSettings.")

                    # Remove old fields.
                    del self.lineSegmentGraphicsItemColor
                    del self.lineSegmentGraphicsItemTextColor
                    del self.lineSegmentGraphicsItemBarWidth
                    del self.lineSegmentGraphicsItemTextXScaling
                    del self.lineSegmentGraphicsItemTextYScaling
                    del self.lineSegmentGraphicsItemDefaultFontDescription
                    del self.lineSegmentGraphicsItemTiltedTextFlag
                    del self.lineSegmentGraphicsItemAngleTextFlag
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 8
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 8:
                # Version 9 added the following member variables:
                #
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag
                #

                try:
                    # See if the variables are set.
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag
                
                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")

                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.

                    # PlanetLongitudeMovementMeasurementGraphicsItem
                    # planetMoSuEnabledFlag (bool).
                    self.planetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag = \
                        PriceBarChartSettings.\
                        defaultPlanetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag
                    
                    self.log.debug(\
                        "Added field " + \
                        "'planetLongitudeMovementMeasurementGraphicsItemPlanetMoSuEnabledFlag', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 9
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 9:
                # Version 10 removed the following member variables:
                #
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeMaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaMeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaMaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaMeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaMeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaVeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuMeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuVeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEaEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuMeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuVeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaMeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaVeEnabledFlag
                # self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaMaEnabledFlag
                #

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeMaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaMaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaMeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaVeEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                try:
                    del(self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaMaEnabledFlag)
                except AttributeError:
                    # Member variable doesn't exist or is not set yet.
                    # No need to do anything special.
                    pass

                self.log.debug(\
                    "Removed fields " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeEaEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetMeVeMaEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaMeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeEaMaEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaMeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetVeMaEaEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaMeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaMaVeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuMeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuVeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetMaJuEaEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuMeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaJuVeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaMeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaVeEnabledFlag', " + \
                    "'self.planetLongitudeMovementMeasurementGraphicsItemPlanetEaSaMaEnabledFlag', " + \
                    "from the loaded PriceBarChartSettings.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 10
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                
            if self.classVersion == 10:
                # Version 11 added the following member variables:
                #
                # self.lookbackMultiplePriceBarGraphicsItemPenWidth
                # self.lookbackMultiplePriceBarGraphicsItemLeftExtensionWidth
                # self.lookbackMultiplePriceBarGraphicsItemRightExtensionWidth
                
                try:
                    # See if the variables are set.
                    self.lookbackMultiplePriceBarGraphicsItemPenWidth
                    self.lookbackMultiplePriceBarGraphicsItemLeftExtensionWidth
                    self.lookbackMultiplePriceBarGraphicsItemRightExtensionWidth

                    # If it got here, then the fields are already set.
                    self.log.warn("Hmm, strange.  Version {} of this ".\
                                  format(self.classVersion) + \
                                  "class shouldn't have these fields.")

                except AttributeError:
                    # Variable was not set.  Set it to the default
                    # PriceBarChartSettings value.

                    # Pen width for LookbackMultiplePriceBars.
                    # This is a float value.
                    self.lookbackMultiplePriceBarGraphicsItemPenWidth = \
                      PriceBarChartSettings.defaultLookbackMultiplePriceBarGraphicsItemPenWidth 

                      # Width of the left extension drawn that represents the
                      # open price of a LookbackMultiplePriceBar.  This is a
                      # float value.
                    self.lookbackMultiplePriceBarGraphicsItemLeftExtensionWidth = \
                      PriceBarChartSettings.\
                      defaultLookbackMultiplePriceBarGraphicsItemLeftExtensionWidth 

                      # Width of the right extension drawn that represents the
                      # close price of a LookbackMultiplePriceBar.  This is a
                      # float value.
                    self.lookbackMultiplePriceBarGraphicsItemRightExtensionWidth = \
                      PriceBarChartSettings.\
                      defaultLookbackMultiplePriceBarGraphicsItemRightExtensionWidth 

                    self.log.debug(\
                                   "Added field " + \
                        "'lookbackMultiplePriceBarGraphicsItemPenWidth', " + \
                        "'lookbackMultiplePriceBarGraphicsItemLeftExtensionWidth', " + \
                        "'lookbackMultiplePriceBarGraphicsItemRightExtensionWidth', " + \
                        "to the loaded PriceBarChartSettings.")
                    
                # Update the class version.
                prevClassVersion = self.classVersion
                self.classVersion = 11
        
                self.log.info("Object has been updated from " + \
                              "version {} to version {}.".\
                              format(prevClassVersion, self.classVersion))
                

        # Log that we set the state of this object.
        self.log.debug("Set state of a " + PriceBarChartSettings.__name__ +
                       " object of version {}".format(self.classVersion))

    def toString(self):
        """Returns the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()


class PriceBarSpreadsheetSettings:
    """Class that holds the default settings used in the
    PriceBarSpreadsheetWidget.
    """

    def __init__(self):
        """"Initializes the PriceChartSettings to default values."""

        # Logger
        self.log = \
            logging.getLogger("data_objects.PriceBarSpreadsheetSettings")

        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # TODO:  write this __init__ function for PriceBarSpreadsheetSettings.

    def __getstate__(self):
        """Returns the object's state for pickling purposes."""

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()

        # Remove items we don't want to pickle.
        del state['log']

        return state


    def __setstate__(self, state):
        """Restores the object's state for unpickling purposes."""

        # Restore instance attributes.
        self.__dict__.update(state)

        # Re-open the logger because it was not pickled.
        self.log = \
            logging.getLogger("data_objects.PriceBarSpreadsheetSettings")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " + 
                       PriceBarSpreadsheetSettings.__name__ +
                       " object of version {}".format(self.classVersion))

    def toString(self):
        """Prints the string representation of this object."""

        rv = Util.objToString(self)
        
        return rv
    
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

# For debugging during development.  
if __name__=="__main__":
    print("------------------------")
    # Testing to make sure sorting works.  

    import time
    
    pcdd = PriceChartDocumentData()
   
    pb1 = PriceBar(datetime.datetime.now(pytz.utc), 5, 9, 1, 5)
    time.sleep(1)
    pb2 = PriceBar(datetime.datetime.now(pytz.utc), 5, 10, 2, 5)
    time.sleep(1)
    pb3 = PriceBar(datetime.datetime.now(pytz.utc), 5, 8, 3, 5)

    dt = datetime.datetime.now(pytz.utc)
    dt = dt - datetime.timedelta(days=(365 * 800))
    pb4 = PriceBar(dt, 5, 3, 4, 5)
    
    pcdd.priceBars.append(pb4)
    pcdd.priceBars.append(pb3)
    pcdd.priceBars.append(pb2)
    pcdd.priceBars.append(pb1)
   
    pcdd.priceBars.sort(key=lambda pb: pb.timestamp)
    
    print("Printing out price bars ...")
    
    for i in range(0, len(pcdd.priceBars)):
        print("pb[{}]: ".format(i) + \
              pcdd.priceBars[i].toString())


    print("")
    print("Printing out PriceChartDocumentData ...")
    print("{}".format(pcdd.toString()))

    print("")
    print("Trying to print a PriceBarChartSettings.")
    ppcs = PriceBarChartSettings()
    print(ppcs.toString())

    x = [1, 2, 3, 4]
    print(x)
    
    # Shutdown logging so all the file handles get flushed and 
    # cleanup can happen.
    logging.shutdown()

    print("")
    print("Exiting.")


