

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz


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
    
##############################################################################
