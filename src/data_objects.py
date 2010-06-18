
# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz


class PriceBar:
    """Contains price information for a single interval of time.  
    PriceBar can include the following information: 

    - timestamp as a datetime.datetime object.
    - open, high, low and close prices
    - open interest
    - volume
    - tags

     
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
        Parameters are as follows:
        - timestamp is a datetime.datetime object
        - tags is a list of strings.
        - Other parameters are floats or integer numbers.
        """
        self.log = logging.getLogger("data_objects.PriceBar")

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

        # Datetime format to datetime.strftime().
        fmt = "%Y-%m-%d %H:%M:%S.%f %Z%z"

        return "[Timestamp={}, ".format(self.timestamp.strftime(fmt)) + \
               "Open={}, ".format(self.open) + \
               "High={}, ".format(self.high) + \
               "Low={}, ".format(self.low) + \
               "Close={}, ".format(self.close) + \
               "OpenInterest={}, ".format(self.oi) + \
               "Volume={}, ".format(self.vol) + \
               "Tags={}]".format(self.tags)


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

        # List of PriceBar objects, sorted by timestamp.
        self.priceBars = []

        # Dictionary of str tag to QColor object.
        self.settingsSpreadsheetTagColors = {}

        # List of the class names of SpreadsheetCalcFormulas utilized.
        self.settingsSpreadsheetCalcFormulas = []

        # Configuration for location.
        self.settingsLocationLongitude = 0
        self.settingsLocationLatitude = 0

        # Configuration for the timezone used.  
        # This is the pytz.timezone object that is a subclass of datetime.tzinfo.
        self.settingsLocationTimezone = pytz.utc

        # Index in self.priceBars of the last PriceBar that was selected.  
        # If none were selected at the time the application last closed, it
        # will be default to index 0 if self.priceBars is non-empty, and -1
        # if self.priceBars is empty.  This information allows the UI to center
        # on the same PriceBar the next time the application is opened.
        self.settingsLastPriceBarIndexSelected = -1


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

        # Datetime format to datetime.strftime().
        fmt = "%Y-%m-%d %H:%M:%S.%f %Z%z"

        if len(self.priceBars) > 0:
            firstPriceBarTimestamp = self.priceBars[0].timestamp.strftime(fmt)
            lastPriceBarTimestamp = self.priceBars[-1].timestamp.strftime(fmt)

        return "[classVersion={}, ".\
                   format(self.classVersion) + \
               "numPriceBars={}, ".\
                   format(len(self.priceBars)) + \
               "firstPriceBarTimestamp={}, ".\
                   format(firstPriceBarTimestamp) + \
               "lastPriceBarTimestamp={}, ".\
                   format(lastPriceBarTimestamp) + \
               "settingsSpreadsheetTagColors={}, ".\
                   format(self.settingsSpreadsheetTagColors) + \
               "settingsSpreadsheetCalcFormulas={}, ".\
                   format(self.settingsSpreadsheetCalcFormulas)+ \
               "settingsLocationLongitude={}, ".\
                   format(self.settingsLocationLongitude) + \
               "settingsLocationLatitude={}, ".\
                   format(self.settingsLocationLatitude) + \
               "settingsLocationTimezone={}, ".\
                   format(self.settingsLocationTimezone) + \
               "settingsLastPriceBarIndexSelected={}]".\
                   format(self.settingsLastPriceBarIndexSelected)

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
        self.log.info("Set state of a " + PriceChartDocumentData.__name__ +
                      " object of version " + self.classVersion)


class GlobalDefaultSettings:
    """Class that holds the default settings used in the PriceChartingTool.
    """
    # TODO:  determine if I should use this class and pickle it to a file in the conf directory, or if I should use the Qt QSettings object to save the settings.

    # TODO:  determine what attributes/members should be part of this class.

    def __init__(self):
        # TODO:  write this method
        pass


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


