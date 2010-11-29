
# For logging.
import logging

# PyQt classes.
from PyQt4 import QtCore
from PyQt4.QtCore import QDateTime


class SpreadsheetCalcFormula:
    """Base class for calculation formulas done in the spreadsheet view.
    More sophisticated formulas (derived classes) for making calculations can
    be created that take more parameters than just the timestamp."""

    def __init__(self, name="", shortName="", description="", units=""):
        """Initializes the object variables with default values."""
        
        self.log = logging.getLogger("spreadsheet_calc.SpreadsheetCalcFormula")

        self.name = name
        self.shortName = shortName
        self.description = description
        self.units = units

    def getName(self):
        """Returns the name of the spreadsheet calculation formula."""
        return self.name

    def getShortName(self):
        """Returns the short name of the spreadsheet calculation formula.
        This is used for column headings of tables."""
        return self.shortName

    def getDescription(self):
        """Returns a description of the spreadsheet calculation formula.
        This explains what is being calculated when calc() is run and possibly
        how that result is being arrived at (the actual formula)."""
        return self.description

    def getUnits(self):
        """Returns what units is returned for the value returned by the calc()
        call."""
        return self.units

    def calc(self, timestamp):
        """Makes a calculation based on the timestamp and returns the result.
        Parameter 'timestamp' is a QDateTime object."""
        # Abstract base class that does no calculation.  Return -1.
        return -1

    def toString(self):
        """Returns the info about the class in String form."""
        return "[Name={}, ShortName={}, Description={}, Units={}]".\
            format(self.name, self.shortName, self.description, self.units)

class SunLocationHeliocentricSiderealCalcFormula(SpreadsheetCalcFormula):
    """Sun heliocentric location, in sidereal degrees."""

    def __init__(self):
        """Initializes the class with the data fields."""
        name = "Sun Location Heliocentric Sidereal"
        shortName = "SunLoc (HS)"
        description = "Heliocentric location of the Sun, in sidereal degrees"
        units = "degrees"
        super().__init__(name, shortName, description, units)

    def calc(self, timestamp):
        """Makes a calculation based on the timestamp and returns the result.
        Parameter 'timestamp' is a QDateTime object."""


class SunLocationGeocentricSiderealCalcFormula(SpreadsheetCalcFormula):
    """Sun geocentric location, in sidereal degrees."""

    def __init__(self):
        """Initializes the class with the data fields."""
        name = "Sun Location Geocentric Sidereal"
        shortName = "SunLoc (HS)"
        description = "Geocentric location of the Sun, in sidereal degrees"
        units = "degrees"
        super().__init__(name, shortName, description, units)

    def calc(self, timestamp):
        """Makes a calculation based on the timestamp and returns the result.
        Parameter 'timestamp' is a QDateTime object."""


# TODO:  create classes below here that derive from SpreadsheetCalcFormula and
# can calculate the info based off a timestamp.

