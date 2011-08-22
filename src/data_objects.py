
# For line separator.
import os

# For logging.
import logging

# For generation of unique PriceBarChartArtifact identifiers.
import uuid

# For timestamps and timezone information.
import datetime
import pytz

# For pickling PyQt types.
from PyQt4.QtGui import QTransform
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPointF

# For datetime.datetime to str conversion.
from ephemeris import Ephemeris

class Util:
    """Contains some generic static functions that may be helpful."""

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
                    rv += "]"
                else:
                    # Normal object that is not a QColor and not a list.
                    rv += "{}={}, ".format(attr, attrObj)
                    
        rv = rv.rstrip(', ')
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
            oi=None, vol=None, tags=[]):
        """Initializes the PriceBar object.  

        Arguments are as follows:
        - open is the open price for the PriceBar, as a float
        - high is the high price for the PriceBar, as a float
        - low is the low price for the PriceBar, as a float
        - close is the close price for the PriceBar, as a float
        - oi is the open interest for the PriceBar, as a float
        - vol is the volume of trade for the PriceBar, as a float
        - timestamp is a datetime.datetime object
        - tags is a list of strings.
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
        self.tags = tags

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
                 enabled=True):
        """Initializes the PriceBar object.  

        Arguments are as follows:
        
        ratio - float value holding the ratio.
        description - str value holding the description of the ratio.
        enabled - bool flag indicating if the ratio is enabled or not.
        """

        # Class version stored for pickling and unpickling.
        self.classVersion = 1

        # Logger object.
        self.log = logging.getLogger("data_objects.Ratio")

        self.ratio = ratio
        self.description = description
        self.enabled = enabled
        
    @staticmethod
    def getSupportedFibRatios():
        """Returns a list of Fibonacci Ratio objects that we plan on
        supporting in this application.
        """

        # Return value.
        ratios = []

        # 0
        ratios.append(Ratio(ratio=0.000,
                               description="0.000",
                               enabled=True))

        # 1 / (phi^3)
        ratios.append(Ratio(ratio=0.23606797695,
                               description="0.236",
                               enabled=True))
        # 1 / (phi^2)
        ratios.append(Ratio(ratio=0.38196601066,
                               description="0.382",
                               enabled=True))
        
        # 1 / phi
        ratios.append(Ratio(ratio=0.61803398827,
                               description="0.618",
                               enabled=True))
        
        # 1 / math.pow(phi, 1/2)
        ratios.append(Ratio(ratio=0.78615137745,
                               description="0.786",
                               enabled=True))
        
        # 1 / math.pow(phi, 1/3)
        ratios.append(Ratio(ratio=0.85179964186,
                               description="0.852",
                               enabled=True))
        
        # 1
        ratios.append(Ratio(ratio=1.000,
                               description="1.000",
                               enabled=True))

        # math.pow(phi, 1/3)
        ratios.append(Ratio(ratio=1.17398499701,
                               description="1.174",
                               enabled=True))
        
        # math.pow(phi, 1/2)
        ratios.append(Ratio(ratio=1.27201965001,
                               description="1.272",
                               enabled=True))
        
        # phi
        ratios.append(Ratio(ratio=1.61803398875,
                               description="1.618",
                               enabled=True))

        # phi^2
        ratios.append(Ratio(ratio=2.61803398859,
                               description="2.618",
                               enabled=True))
        
        # phi^3
        ratios.append(Ratio(ratio=4.23606797711,
                               description="4.236",
                               enabled=False))
        
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

        # List of used ratios.
        self.musicalRatios = MusicalRatio.getIndianMusicalRatios()
        
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
        self.textEnabledFlag = False
        
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
        self.textEnabledFlag = False
        
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
            getLogger("data_objects.PriceBarChartPriceModalScaleArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartPriceModalScaleArtifact.__name__ +
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
        self.classVersion = 1

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
        self.classVersion = 1

        # Description label.
        self.description = ""
        
        # List of PriceBar objects, sorted by timestamp.
        self.priceBars = []
        
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
            
        return "[classVersion={}, ".\
                   format(self.classVersion) + \
                "description={}, ".\
                    format(self.description) + \
                "numPriceBars={}, ".\
                    format(len(self.priceBars)) + \
                "numArtifacts={}, ".\
                    format(len(self.priceBarChartArtifacts)) + \
                "artifacts={}, ".\
                    format(artifactStrings) + \
                "firstPriceBarTimestamp={}, ".\
                    format(firstPriceBarTimestamp) + \
                "lastPriceBarTimestamp={}, ".\
                    format(lastPriceBarTimestamp) + \
                "settingsSpreadsheetTagColors={}, ".\
                    format(self.settingsSpreadsheetTagColors) + \
                "settingsSpreadsheetCalcFormulas={}, ".\
                    format(self.settingsSpreadsheetCalcFormulas) + \
                "priceBarChartSettings={}, ".\
                    format(self.priceBarChartSettings.toString()) + \
                "priceBarSpreadsheetSettings={}, ".\
                    format(self.priceBarSpreadsheetSettings.toString()) + \
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

    # Default value for the BarCountGraphicsItem bar height (float).
    defaultBarCountGraphicsItemBarHeight = 0.2

    # Default value for the BarCountGraphicsItem font size (float).
    defaultBarCountGraphicsItemFontSize = 1.0

    # Default value for the BarCountGraphicsItem text X scaling (float).
    defaultBarCountGraphicsItemTextXScaling = 1.0

    # Default value for the BarCountGraphicsItem text Y scaling (float).
    defaultBarCountGraphicsItemTextYScaling = 0.2

    # Default value for the TimeMeasurementGraphicsItem bar height (float).
    defaultTimeMeasurementGraphicsItemBarHeight = 0.2

    # Default value for the TimeMeasurementGraphicsItem text X scaling (float).
    defaultTimeMeasurementGraphicsItemTextXScaling = 0.2

    # Default value for the TimeMeasurementGraphicsItem text Y scaling (float).
    defaultTimeMeasurementGraphicsItemTextYScaling = 0.04

    # Default font (this is basically the QFont, serialized to
    # str) for the TimeMeasurementGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
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
    defaultTimeMeasurementGraphicsItemShowSqrtBarsTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdBarsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdBarsTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showHoursTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowHoursTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtHoursTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtHoursTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdHoursTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdHoursTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showDaysTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowDaysTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtDaysTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtDaysTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdDaysTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdDaysTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showWeeksTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowWeeksTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtWeeksTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtWeeksTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdWeeksTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdWeeksTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showMonthsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowMonthsTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtMonthsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtMonthsTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdMonthsTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdMonthsTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showTimeRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowTimeRangeTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtTimeRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtTimeRangeTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdTimeRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdTimeRangeTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showScaledValueRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowScaledValueRangeTextFlag = True
    
    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtScaledValueRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdScaledValueRangeTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdScaledValueRangeTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showAyanaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowAyanaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtAyanaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtAyanaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdAyanaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdAyanaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showMuhurtaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowMuhurtaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtMuhurtaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtMuhurtaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdMuhurtaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdMuhurtaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showVaraTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowVaraTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtVaraTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtVaraTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdVaraTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdVaraTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showRtuTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowRtuTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtRtuTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtRtuTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdRtuTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdRtuTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showMasaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowMasaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtMasaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtMasaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdMasaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdMasaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showPaksaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowPaksaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtPaksaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtPaksaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdPaksaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdPaksaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSamaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSamaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrtSamaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrtSamaTextFlag = True

    # Default value for the TimeMeasurementGraphicsItem
    # showSqrdSamaTextFlag (bool).
    defaultTimeMeasurementGraphicsItemShowSqrdSamaTextFlag = True

    # Default color for the bar of a TimeModalScaleGraphicsItem (QColor).
    defaultTimeModalScaleGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a TimeModalScaleGraphicsItem (QColor).
    defaultTimeModalScaleGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the TimeModalScaleGraphicsItem bar height (float).
    defaultTimeModalScaleGraphicsItemBarHeight = 0.3

    # Default value for the TimeModalScaleGraphicsItem font size (float).
    defaultTimeModalScaleGraphicsItemFontSize = 1.20

    # Default value for the TimeModalScaleGraphicsItem text X scaling (float).
    defaultTimeModalScaleGraphicsItemTextXScaling = 1

    # Default value for the TimeModalScaleGraphicsItem text Y scaling (float).
    defaultTimeModalScaleGraphicsItemTextYScaling = 0.2

    # Default color for the bar of a PriceModalScaleGraphicsItem (QColor).
    defaultPriceModalScaleGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a PriceModalScaleGraphicsItem (QColor).
    defaultPriceModalScaleGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the PriceModalScaleGraphicsItem bar width (float).
    defaultPriceModalScaleGraphicsItemBarWidth = 1.0

    # Default value for the PriceModalScaleGraphicsItem font size (float).
    defaultPriceModalScaleGraphicsItemFontSize = 1.20

    # Default value for the PriceModalScaleGraphicsItem text X scaling (float).
    defaultPriceModalScaleGraphicsItemTextXScaling = 1

    # Default value for the PriceModalScaleGraphicsItem text Y scaling (float).
    defaultPriceModalScaleGraphicsItemTextYScaling = 0.2

    # Default font description text (this is basically the QFont,
    # serialized to str) for the TextGraphicsItem.  This includes the
    # font size.
    font = QFont("DejaVu Sans Mono")
    font.setPointSizeF(6)
    defaultTextGraphicsItemDefaultFontDescription = font.toString()

    # Default font color for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default text X scaling for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultXScaling = 0.2
    
    # Default text Y scaling for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultYScaling = 0.04
    
    # Default font description text (this is basically the QFont,
    # serialized to str) for the PriceTimeInfoGraphicsItem.  This
    # includes the font size.
    font = QFont("DejaVu Sans Mono")
    font.setPointSizeF(6)
    defaultPriceTimeInfoGraphicsItemDefaultFontDescription = font.toString()

    # Default font color for the PriceTimeInfoGraphicsItem.
    defaultPriceTimeInfoGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default text X scaling for the PriceTimeInfoGraphicsItem.
    defaultPriceTimeInfoGraphicsItemDefaultXScaling = 0.2
    
    # Default text Y scaling for the PriceTimeInfoGraphicsItem.
    defaultPriceTimeInfoGraphicsItemDefaultYScaling = 0.04

    # Default value for the PriceTimeInfoGraphicsItem
    # showTimestampFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowTimestampFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showPriceFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowPriceFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtPriceFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtPriceFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showTimeElapsedSinceBirthFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowTimeElapsedSinceBirthFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtTimeElapsedSinceBirthFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtTimeElapsedSinceBirthFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showPriceScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowPriceScaledValueFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtPriceScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtPriceScaledValueFlag = True
        
    # Default value for the PriceTimeInfoGraphicsItem
    # showTimeScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowTimeScaledValueFlag = True

    # Default value for the PriceTimeInfoGraphicsItem
    # showSqrtTimeScaledValueFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowSqrtTimeScaledValueFlag = True
        
    # Default value for the PriceTimeInfoGraphicsItem
    # showLineToInfoPointFlag (bool).
    defaultPriceTimeInfoGraphicsItemShowLineToInfoPointFlag = True

    # Default value for the PriceMeasurementGraphicsItem bar width (float).
    defaultPriceMeasurementGraphicsItemBarWidth = 1.0

    # Default value for the PriceMeasurementGraphicsItem text X scaling (float).
    defaultPriceMeasurementGraphicsItemTextXScaling = 0.2

    # Default value for the PriceMeasurementGraphicsItem text Y scaling (float).
    defaultPriceMeasurementGraphicsItemTextYScaling = 0.04

    # Default font (this is basically the QFont, serialized to
    # str) for the PriceMeasurementGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
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
    defaultPriceMeasurementGraphicsItemShowSqrtPriceRangeTextFlag = True

    # Default value for the PriceMeasurementGraphicsItem
    # showScaledValueRangeTextFlag (bool).
    defaultPriceMeasurementGraphicsItemShowScaledValueRangeTextFlag = True
    
    # Default value for the PriceMeasurementGraphicsItem
    # showSqrtScaledValueRangeTextFlag (bool).
    defaultPriceMeasurementGraphicsItemShowSqrtScaledValueRangeTextFlag = True

    # Default value for the TimeRetracementGraphicsItem bar height (float).
    defaultTimeRetracementGraphicsItemBarHeight = 0.2

    # Default value for the TimeRetracementGraphicsItem text X scaling (float).
    defaultTimeRetracementGraphicsItemTextXScaling = 0.2

    # Default value for the TimeRetracementGraphicsItem text Y scaling (float).
    defaultTimeRetracementGraphicsItemTextYScaling = 0.04

    # Default font (this is basically the QFont, serialized to
    # str) for the TimeRetracementGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
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
    defaultTimeRetracementGraphicsItemRatios = Ratio.getSupportedFibRatios()
    
    # Default value for the PriceRetracementGraphicsItem bar width (float).
    defaultPriceRetracementGraphicsItemBarWidth = 1.0

    # Default value for the PriceRetracementGraphicsItem text X scaling (float).
    defaultPriceRetracementGraphicsItemTextXScaling = 0.2

    # Default value for the PriceRetracementGraphicsItem text Y scaling (float).
    defaultPriceRetracementGraphicsItemTextYScaling = 0.04

    # Default font (this is basically the QFont, serialized to
    # str) for the PriceRetracementGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
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
    defaultPriceRetracementGraphicsItemRatios = Ratio.getSupportedFibRatios()

    # Default color for the bar of a PriceTimeVectorGraphicsItem (QColor).
    defaultPriceTimeVectorGraphicsItemColor = QColor(Qt.black)

    # Default color for the text of a PriceTimeVectorGraphicsItem (QColor).
    defaultPriceTimeVectorGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the PriceTimeVectorGraphicsItem bar width (float).
    defaultPriceTimeVectorGraphicsItemBarWidth = 0.3

    # Default value for the PriceTimeVectorGraphicsItem text X scaling (float).
    defaultPriceTimeVectorGraphicsItemTextXScaling = 0.2

    # Default value for the PriceTimeVectorGraphicsItem text Y scaling (float).
    defaultPriceTimeVectorGraphicsItemTextYScaling = 0.04

    # Default font (this is basically the QFont, serialized to
    # str) for the PriceTimeVectorGraphicsItem.  This includes the
    # font size.
    font = QFont("Andale Mono")
    font.setPointSizeF(6)
    defaultPriceTimeVectorGraphicsItemDefaultFontDescription = font.toString()

    # Default value for the PriceTimeVectorGraphicsItem
    # showDistanceTextFlag (bool).
    defaultPriceTimeVectorGraphicsItemShowDistanceTextFlag = True

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
    
    def __init__(self):
        """"Initializes the PriceChartSettings to default values."""

        # Logger
        self.log = logging.getLogger("data_objects.PriceBarChartSettings")

        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

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

        # Width of the left extension drawn that represents the open price.
        # This is a float value.
        self.priceBarGraphicsItemLeftExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemLeftExtensionWidth 

        # Width of the right extension drawn that represents the close price.
        # This is a float value.
        self.priceBarGraphicsItemRightExtensionWidth = \
            PriceBarChartSettings.\
                defaultPriceBarGraphicsItemRightExtensionWidth 

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
            
        # TimeModalScaleGraphicsItem bar color (QColor).
        self.timeModalScaleGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemBarColor

        # TimeModalScaleGraphicsItem text color (QColor).
        self.timeModalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextColor

        # TimeModalScaleGraphicsItem text X scaling (float).
        self.timeModalScaleGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextXScaling

        # TimeModalScaleGraphicsItem text Y scaling (float).
        self.timeModalScaleGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeModalScaleGraphicsItemTextYScaling

        # PriceModalScaleGraphicsItem bar color (QColor).
        self.priceModalScaleGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemBarColor

        # PriceModalScaleGraphicsItem text color (QColor).
        self.priceModalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextColor

        # PriceModalScaleGraphicsItem text X scaling (float).
        self.priceModalScaleGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextXScaling

        # PriceModalScaleGraphicsItem text Y scaling (float).
        self.priceModalScaleGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultPriceModalScaleGraphicsItemTextYScaling

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

        # TODO:  fill this info in for PriceBarSpreadsheetSettings.

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


