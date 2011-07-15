
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

        rv = "[year={}, ".format(self.year) + \
             "month={}, ".format(self.month) + \
             "day={}, ".format(self.day) + \
             "calendar={}, ".format(self.calendar) + \
             "hour={}, ".format(self.hour) + \
             "minute={}, ".format(self.minute) + \
             "second={}, ".format(self.second) + \
             "locationName={}, ".format(self.locationName) + \
             "countryName={}, ".format(self.countryName) + \
             "longitudeDegrees={}, ".format(self.longitudeDegrees) + \
             "latitudeDegrees={}, ".format(self.latitudeDegrees) + \
             "elevation={}, ".format(self.elevation) + \
             "timezoneName={}, ".format(self.timezoneName) + \
             "timezoneOffsetAbbreviation={}, ".\
                format(self.timezoneOffsetAbbreviation) + \
             "timezoneOffsetValueStr={}, ".\
                format(self.timezoneOffsetValueStr) + \
             "timezoneManualEntryHours={}, ".\
                format(self.timezoneManualEntryHours) + \
             "timezoneManualEntryMinutes={}, ".\
                format(self.timezoneManualEntryMinutes) + \
             "timezoneManualEntryEastWestComboBoxValue={}, ".\
                format(self.timezoneManualEntryEastWestComboBoxValue) + \
             "timeOffsetAutodetectedRadioButtonState={}, ".\
                format(self.timeOffsetAutodetectedRadioButtonState) + \
             "timeOffsetManualEntryRadioButtonState={}, ".\
                format(self.timeOffsetManualEntryRadioButtonState) + \
             "timeOffsetLMTRadioButtonState={}]".\
                format(self.timeOffsetLMTRadioButtonState)

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

        # Need to use Ephemeris.datetimeToStr() below because
        # datetime.strftime() datetime.strftime() does not work on
        # years less than 1900.
        
        return "[Timestamp={}, ".\
                   format(Ephemeris.datetimeToStr(self.timestamp)) + \
               "Open={}, ".format(self.open) + \
               "High={}, ".format(self.high) + \
               "Low={}, ".format(self.low) + \
               "Close={}, ".format(self.close) + \
               "OpenInterest={}, ".format(self.oi) + \
               "Volume={}, ".format(self.vol) + \
               "Tags={}]".format(self.tags)

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

class MusicalRatio:
    """Contains information about a musical ratio that makes up a note
    in a scale.  Includes the following information:

    - float value for the ratio.
    - description of the ratio.
    - numerator of the fraction (if applicable)
    - denominator of the fraction (if applicable)
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
        """

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

        return "[ratio={}, ".format(self.ratio) + \
               "description={}, ".format(self.description) + \
               "numerator={}, ".format(self.numerator) + \
               "denominator={}, ".format(self.denominator) + \
               "enabled={}".format(self.enabled) + \
               "]"

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

        rv = "[name={}, ".format(self.getInternalName()) + \
             "pos=({}, {})".format(self.getPos().x(), self.getPos().y()) + \
             "]"

        return rv

class PriceBarChartGannFanUpperRightArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that is the GannFann pointing in 
    the upper right direction."""
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartGannFanUpperRightArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "GannFanUpperRight_" + str(self.uuid)

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        # TODO:  modify this to return all the internal objects for PriceBarChartGannFanUpperRightArtifact.
        rv = "[name={}, ".format(self.getInternalName()) + \
             "pos=({}, {})".format(self.getPos().x(), self.getPos().y()) + \
             "]"

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
            logging.getLogger("data_objects.PriceBarChartGannFanUpperRightArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartGannFanUpperRightArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartGannFanLowerRightArtifact(PriceBarChartArtifact):
    """PriceBarChartArtifact that is the GannFann pointing in 
    the lower right direction.
    """
    
    def __init__(self):
        super().__init__()
        
        # Set the version of this class (used for pickling and unpickling
        # different versions of this class).
        self.classVersion = 1

        # Create the logger.
        self.log = \
            logging.getLogger("data_objects.PriceBarChartGannFanLowerRightArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "GannFanLowerRight_" + str(self.uuid)
   
    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this object."""

        # TODO:  modify this to return all the internal objects for PriceBarChartGannFanLowerRightArtifact.
        rv = "[name={}, ".format(self.getInternalName()) + \
             "pos=({}, {})".format(self.getPos().x(), self.getPos().y()) + \
             "]"

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
            logging.getLogger("data_objects.PriceBarChartGannFanLowerRightArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartGannFanLowerRightArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

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

        rv = "[name={}, ".format(self.getInternalName()) + \
             "pos=({}, {}), ".format(self.getPos().x(), self.getPos().y()) + \
             "startPointF=({}, {}), ".format(self.getStartPointF().x(),
                                             self.getStartPointF().y()) + \
             "endPointF=({}, {}), ".format(self.getEndPointF().x(),
                                           self.getEndPointF().y()) + \
             "]"

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
        self.log = logging.getLogger("data_objects.PriceBarChartTimeMeasurementArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "TimeMeasurement_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

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

        rv = "[name={}, ".format(self.getInternalName()) + \
             "pos=({}, {}), ".format(self.getPos().x(), self.getPos().y()) + \
             "startPointF=({}, {}), ".format(self.getStartPointF().x(),
                                             self.getStartPointF().y()) + \
             "endPointF=({}, {}), ".format(self.getEndPointF().x(),
                                           self.getEndPointF().y()) + \
             "]"

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
        self.log = logging.getLogger("data_objects.PriceBarChartTimeMeasurementArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartTimeMeasurementArtifact.__name__ +
                       " object of version {}".format(self.classVersion))

class PriceBarChartModalScaleArtifact(PriceBarChartArtifact):
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
            logging.getLogger("data_objects.PriceBarChartModalScaleArtifact")

        # Update the internal name so it is the artifact type plus the uuid.
        self.internalName = "ModalScale_" + str(self.uuid)

        # Start and end points of the artifact.
        self.startPointF = QPointF()
        self.endPointF = QPointF()

        # List of used ratios.
        self.musicalRatios = MusicalRatio.getIndianMusicalRatios()
        
        # modalScaleGraphicsItemColor (QColor object).
        self.modalScaleGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemBarColor

        # modalScaleGraphicsItemTextColor (QColor object).
        self.modalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemTextColor

        # ModalScaleGraphicsItem bar height (float).
        self.modalScaleGraphicsItemBarHeight = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemBarHeight

        # ModalScaleGraphicsItem font size (float).
        self.modalScaleGraphicsItemFontSize = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemFontSize

        # Flag for whether or not the musicalRatios are in reverse
        # order.  This affects how ratios are referenced (from the
        # endpoint instead of from the startpoint).
        self.reversedFlag = False

        # Flag for whether or not the text is displayed for enabled
        # MusicalRatios in self.musicalRatios.
        self.textEnabledFlag = False
        
    def setStartPointF(self, startPointF):
        """Stores the starting point of the ModalScaleArtifact.
        Arguments:

        startPointF - QPointF for the starting point of the artifact.
        """
        
        self.startPointF = startPointF
        
    def getStartPointF(self):
        """Returns the starting point of the ModalScaleArtifact."""
        
        return self.startPointF
        
    def setEndPointF(self, endPointF):
        """Stores the ending point of the ModalScaleArtifact.
        Arguments:

        endPointF - QPointF for the ending point of the artifact.
        """
        
        self.endPointF = endPointF
        
    def getEndPointF(self):
        """Returns the ending point of the ModalScaleArtifact."""
        
        return self.endPointF

    def getMusicalRatios(self):
        """Returns the list of MusicalRatio objects."""

        return self.musicalRatios
        
    def setMusicalRatios(self, musicalRatios):
        """Sets the list of MusicalRatio objects."""

        self.musicalRatios = musicalRatios

    def setModalScaleGraphicsItemBarColor(self, modalScaleGraphicsItemBarColor):
        """Sets the bar color.
        
        Arguments:
        modalScaleGraphicsItemBarColor - QColor object for the bar color.
        """
        
        self.modalScaleGraphicsItemBarColor = \
            modalScaleGraphicsItemBarColor

    def getModalScaleGraphicsItemBarColor(self):
        """Gets the bar color as a QColor object."""
        
        return self.modalScaleGraphicsItemBarColor

    def setModalScaleGraphicsItemTextColor(self,
                                           modalScaleGraphicsItemTextColor):
        """Sets the text color.
        
        Arguments:
        modalScaleGraphicsItemTextColor - QColor object for the text color.
        """

        self.modalScaleGraphicsItemTextColor = modalScaleGraphicsItemTextColor
        
    def getModalScaleGraphicsItemTextColor(self):
        """Gets the text color as a QColor object."""

        return self.modalScaleGraphicsItemTextColor
        
    def setModalScaleGraphicsItemBarHeight(self,
                                           modalScaleGraphicsItemBarHeight):
        """Sets the ModalScaleGraphicsItem bar height (float)."""

        self.modalScaleGraphicsItemBarHeight = modalScaleGraphicsItemBarHeight
    
    def getModalScaleGraphicsItemBarHeight(self):
        """Returns the ModalScaleGraphicsItem bar height (float)."""

        return self.modalScaleGraphicsItemBarHeight
    
    def setModalScaleGraphicsItemFontSize(self,
                                          modalScaleGraphicsItemFontSize):
        """Sets the font size of the musical ratio text (float)."""

        self.modalScaleGraphicsItemFontSize = modalScaleGraphicsItemFontSize
    
    def getModalScaleGraphicsItemFontSize(self):
        """Sets the font size of the musical ratio text (float)."""

        return self.modalScaleGraphicsItemFontSize
    
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

        musicalRatiosStr = "["
        for musicalRatio in self.musicalRatios:
            musicalRatiosStr += musicalRatio.toString()
        musicalRatiosStr += "]"
        
        rv = "[name={}, ".format(self.getInternalName()) + \
             "pos=({}, {}), ".format(self.getPos().x(), self.getPos().y()) + \
             "startPointF=({}, {}), ".format(self.getStartPointF().x(),
                                             self.getStartPointF().y()) + \
             "endPointF=({}, {}), ".format(self.getEndPointF().x(),
                                           self.getEndPointF().y()) + \
             "musicalRatios={}, ".format(musicalRatiosStr) + \
             "reversedFlag={}, ".format(self.reversedFlag) + \
             "textEnabledFlag={}, ".format(self.textEnabledFlag) + \
             "modalScaleGraphicsItemBarColor={}, ".\
             format(self.modalScaleGraphicsItemBarColor) + \
             "modalScaleGraphicsItemTextColor={}, ".\
             format(self.modalScaleGraphicsItemTextColor) + \
             "modalScaleGraphicsItemBarHeight={}, ".\
             format(self.modalScaleGraphicsItemBarHeight) + \
             "modalScaleGraphicsItemFontSize={}".\
             format(self.modalScaleGraphicsItemFontSize) + \
             "]"

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
            logging.getLogger("data_objects.PriceBarChartModalScaleArtifact")

        # Log that we set the state of this object.
        self.log.debug("Set state of a " +
                       PriceBarChartModalScaleArtifact.__name__ +
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

        rv = "[name={}, ".format(self.getInternalName()) + \
             "pos=({}, {}), ".format(self.getPos().x(), self.getPos().y()) + \
             "text='{}', ".format(self.text) + \
             "fontDescription='{}', ".format(self.fontDescription) + \
             "color={}, ".format(self.color) + \
             "textXScaling={}, ".format(self.textXScaling) + \
             "textYScaling={}".format(self.textYScaling) + \
             "]"

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

class PriceBarChartScaling:
    """Class that holds information about the scaling of a PriceBarChart.
    """

    def __init__(self, 
                 unitsOfTime=1.0, 
                 unitsOfPrice=1.0, 
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

        # Set the internally stored QTransform.
        self.transform = QTransform()
        self.transform.reset()
        self.transform.scale(self.unitsOfTime, self.unitsOfPrice)

    def setUnitsOfTime(self, unitsOfTime):
        """Updates the units-of-time variable part of scaling.

        Arguments:
            
        unitsOfTime - float value representing the units-of-time part of
        scaling.
        """

        self.unitsOfTime = unitsOfTime

        self.transform.reset()
        self.transform.scale(self.unitsOfTime, self.unitsOfPrice)

    def setUnitsOfPrice(self, unitsOfPrice):
        """Updates the units-of-price variable part of scaling.

        Arguments:
            
        unitsOfPrice - float value representing the units-of-price part of
        scaling.
        """

        self.unitsOfPrice = unitsOfPrice

        self.transform.reset()
        self.transform.scale(self.unitsOfTime, self.unitsOfPrice)

    def getUnitsOfTime(self):
        """Returns the units-of-time part of the ratio used in scaling."""

        return self.unitsOfTime
    
    def getUnitsOfPrice(self):
        """Returns the units-of-price part of the ratio used in scaling."""

        return self.unitsOfPrice

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

    def __str__(self):
        """Returns the string representation of this object."""

        return self.toString()
        
    def toString(self):
        """Returns the string representation of this object."""

        return "[name={}, ".format(self.name) + \
                "description={}, ".format(self.description) + \
                "unitsOfTime={}, ".format(self.unitsOfTime) + \
                "unitsOfPrice={}]".format(self.unitsOfPrice)

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

    # Default font description text (this is basically the QFont,
    # serialized to str) for the TextGraphicsItem.  This includes the
    # font size.
    font = QFont()
    font.setPointSizeF(1.20)
    defaultTextGraphicsItemDefaultFontDescription = font.toString()

    # Default font color for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultColor = QColor(Qt.black)
    
    # Default text X scaling for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultXScaling = 1.0
    
    # Default text Y scaling for the TextGraphicsItem.
    defaultTextGraphicsItemDefaultYScaling = 0.2
    
    # Default value for the BarCountGraphicsItem bar height (float).
    defaultBarCountGraphicsItemBarHeight = 0.2

    # Default value for the BarCountGraphicsItem font size (float).
    defaultBarCountGraphicsItemFontSize = 1.0

    # Default value for the BarCountGraphicsItem text X scaling (float).
    defaultBarCountGraphicsItemTextXScaling = 1

    # Default value for the BarCountGraphicsItem text Y scaling (float).
    defaultBarCountGraphicsItemTextYScaling = 0.2

    # Default value for the TimeMeasurementGraphicsItem bar height (float).
    defaultTimeMeasurementGraphicsItemBarHeight = 0.2

    # Default value for the TimeMeasurementGraphicsItem font size (float).
    defaultTimeMeasurementGraphicsItemFontSize = 1.20

    # Default value for the TimeMeasurementGraphicsItem text X scaling (float).
    defaultTimeMeasurementGraphicsItemTextXScaling = 1

    # Default value for the TimeMeasurementGraphicsItem text Y scaling (float).
    defaultTimeMeasurementGraphicsItemTextYScaling = 0.2

    # Default color for the bar of a ModalScaleGraphicsItem (QColor).
    defaultModalScaleGraphicsItemBarColor = QColor(Qt.black)

    # Default color for the text of a ModalScaleGraphicsItem (QColor).
    defaultModalScaleGraphicsItemTextColor = QColor(Qt.black)
    
    # Default value for the ModalScaleGraphicsItem bar height (float).
    defaultModalScaleGraphicsItemBarHeight = 0.3

    # Default value for the ModalScaleGraphicsItem font size (float).
    defaultModalScaleGraphicsItemFontSize = 1.20

    # Default value for the ModalScaleGraphicsItem text X scaling (float).
    defaultModalScaleGraphicsItemTextXScaling = 1

    # Default value for the ModalScaleGraphicsItem text Y scaling (float).
    defaultModalScaleGraphicsItemTextYScaling = 0.2


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

        # TimeMeasurementGraphicsItem font size (float).
        self.timeMeasurementGraphicsItemFontSize = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemFontSize

        # TimeMeasurementGraphicsItem text X scaling (float).
        self.timeMeasurementGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextXScaling

        # TimeMeasurementGraphicsItem text Y scaling (float).
        self.timeMeasurementGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultTimeMeasurementGraphicsItemTextYScaling

        # ModalScaleGraphicsItem bar color (QColor).
        self.modalScaleGraphicsItemBarColor = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemBarColor

        # ModalScaleGraphicsItem text color (QColor).
        self.modalScaleGraphicsItemTextColor = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemTextColor

        # ModalScaleGraphicsItem text X scaling (float).
        self.modalScaleGraphicsItemTextXScaling = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemTextXScaling

        # ModalScaleGraphicsItem text Y scaling (float).
        self.modalScaleGraphicsItemTextYScaling = \
            PriceBarChartSettings.\
                defaultModalScaleGraphicsItemTextYScaling



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

        # List of PriceBarChart scalings used.
        scalingsStr = ""
        for scaling in self.priceBarChartGraphicsViewScalings:
            scalingsStr += scaling.toString()

        return "[classVersion={}, ".\
                   format(self.classVersion) + \
                "priceBarChartGraphicsViewScalings=[{}], ".\
                    format(scalingsStr) + \
                "priceBarGraphicsItemPenWidth={}, ".\
                    format(self.priceBarGraphicsItemPenWidth) + \
                "priceBarGraphicsItemLeftExtensionWidth={}, ".\
                    format(self.priceBarGraphicsItemLeftExtensionWidth) + \
                "priceBarGraphicsItemRightExtensionWidth={}, ".\
                    format(self.priceBarGraphicsItemRightExtensionWidth) + \
                "textGraphicsItemDefaultFontDescription={}, ".\
                    format(self.textGraphicsItemDefaultFontDescription) + \
                "textGraphicsItemDefaultColor={}, ".\
                    format(self.textGraphicsItemDefaultColor) + \
                "textGraphicsItemDefaultXScaling={}, ".\
                    format(self.textGraphicsItemDefaultXScaling) + \
                "textGraphicsItemDefaultYScaling={}, ".\
                    format(self.textGraphicsItemDefaultYScaling) + \
                "barCountGraphicsItemBarHeight={}, ".\
                    format(self.barCountGraphicsItemBarHeight) + \
                "barCountGraphicsItemFontSize={}, ".\
                    format(self.barCountGraphicsItemFontSize) + \
                "barCountGraphicsItemTextXScaling={}, ".\
                    format(self.barCountGraphicsItemTextXScaling) + \
                "barCountGraphicsItemTextYScaling={}, ".\
                    format(self.barCountGraphicsItemTextYScaling) + \
                "timeMeasurementGraphicsItemBarHeight={}, ".\
                    format(self.timeMeasurementGraphicsItemBarHeight) + \
                "timeMeasurementGraphicsItemFontSize={}, ".\
                    format(self.timeMeasurementGraphicsItemFontSize) + \
                "timeMeasurementGraphicsItemTextXScaling={}, ".\
                    format(self.timeMeasurementGraphicsItemTextXScaling) + \
                "timeMeasurementGraphicsItemTextYScaling={}".\
                    format(self.timeMeasurementGraphicsItemTextYScaling) + \
                "modalScaleGraphicsItemBarColor={}".\
                    format(self.modalScaleGraphicsItemBarColor) + \
                "modalScaleGraphicsItemTextColor={}".\
                    format(self.modalScaleGraphicsItemTextColor) + \
                "modalScaleGraphicsItemTextXScaling={}, ".\
                    format(self.modalScaleGraphicsItemTextXScaling) + \
                "modalScaleGraphicsItemTextYScaling={}".\
                    format(self.modalScaleGraphicsItemTextYScaling) + \
                "]"


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

        return "[classVersion={}".\
                   format(self.classVersion) + \
                "]"

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

    # Shutdown logging so all the file handles get flushed and 
    # cleanup can happen.
    logging.shutdown()

    print("")
    print("Exiting.")


