
# For line separator.
import os

# For coordinate calculations.
import math

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import image resources.
import resources

# For QSettings keys.
from settings import SettingsKeys

# For BirthInfo.
from data_objects import BirthInfo

# For various utility functions.
from data_objects import Util

# For conversions from julian day to datetime.datetime and vice versa.
from ephemeris import Ephemeris


class AstrologyUtils:
    """Contains various functions used in the conversions between
    various astrological values and fields.
    """

    @staticmethod
    def convertFromLongitudeToStrWithRasiAbbrev(longitude):
        """Takes a float longitude value and converts it to a string
        in the format: 23 <RASI_GLYPH> 24' 14"
        
        Arguments:
        longitude - float value for the longitude of the planet.

        Returns:
        str - String that is in the above format.  It will always be a
        fixed number of characters.  This means that if it is 8
        degrees, or 8 minutes, or 8 seconds, the string will have a
        space prefixing the 8.
        """

        # Make sure the longitude is less than 360 and greater than or
        # equal to 0.
        if longitude >= 360.0 or longitude < 0.0:
            longitude = longitude % 360
        
        # Rasi number, where 0 is Aries.
        rasi = math.floor(longitude / 30.0)

        # Degree in the rasi.
        unflooredDegrees = longitude % 30
        degrees = math.floor(unflooredDegrees)

        # Minutes within the degree.
        unflooredMinutes = (unflooredDegrees - degrees) * 60.0
        minutes = math.floor(unflooredMinutes)

        # Seconds within the degree.
        unflooredSeconds = (unflooredMinutes - minutes) * 60.0
        seconds = math.floor(unflooredSeconds)

        # Preference settings.
        settings = QSettings()
        
        signGlyphs = [\
            settings.value(SettingsKeys.signAriesGlyphUnicodeKey,
                           SettingsKeys.signAriesGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signTaurusGlyphUnicodeKey,
                           SettingsKeys.signTaurusGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signGeminiGlyphUnicodeKey,
                           SettingsKeys.signGeminiGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signCancerGlyphUnicodeKey,
                           SettingsKeys.signCancerGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signLeoGlyphUnicodeKey,
                           SettingsKeys.signLeoGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signVirgoGlyphUnicodeKey,
                           SettingsKeys.signVirgoGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signLibraGlyphUnicodeKey,
                           SettingsKeys.signLibraGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signScorpioGlyphUnicodeKey,
                           SettingsKeys.signScorpioGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signSagittariusGlyphUnicodeKey,
                           SettingsKeys.signSagittariusGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signCapricornGlyphUnicodeKey,
                           SettingsKeys.signCapricornGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signAquariusGlyphUnicodeKey,
                           SettingsKeys.signAquariusGlyphUnicodeDefValue,
                           type=str),
            settings.value(SettingsKeys.signPiscesGlyphUnicodeKey,
                           SettingsKeys.signPiscesGlyphUnicodeDefValue,
                           type=str)]

        signAbbreviations = [\
            settings.value(SettingsKeys.signAriesAbbreviationKey,
                           SettingsKeys.signAriesAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signTaurusAbbreviationKey,
                           SettingsKeys.signTaurusAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signGeminiAbbreviationKey,
                           SettingsKeys.signGeminiAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signCancerAbbreviationKey,
                           SettingsKeys.signCancerAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signLeoAbbreviationKey,
                           SettingsKeys.signLeoAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signVirgoAbbreviationKey,
                           SettingsKeys.signVirgoAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signLibraAbbreviationKey,
                           SettingsKeys.signLibraAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signScorpioAbbreviationKey,
                           SettingsKeys.signScorpioAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signSagittariusAbbreviationKey,
                           SettingsKeys.signSagittariusAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signCapricornAbbreviationKey,
                           SettingsKeys.signCapricornAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signAquariusAbbreviationKey,
                           SettingsKeys.signAquariusAbbreviationDefValue,
                           type=str),
            settings.value(SettingsKeys.signPiscesAbbreviationKey,
                           SettingsKeys.signPiscesAbbreviationDefValue,
                           type=str)]

        degreesStr = "{: >2}".format(degrees)
        rasiStr = signGlyphs[rasi]
        minutesStr = "{:0>02}".format(minutes)
        secondsStr = "{:0>02}".format(seconds)
        
        rv = \
            degreesStr + " " + \
            rasiStr + " " + \
            minutesStr + "' " + \
            secondsStr + "\""

        return rv

    @staticmethod
    def convertFromLongitudeToNakshatraAbbrev(longitude):
        """Takes a float longitude value and converts it to a string
        that is the nakshatra abbreviation for that longitude.
        
        Arguments:
        longitude - float value for the longitude of the planet.

        Returns:
        str - String that is the nakshatra abbreviation for that longitude.
        """

        # Make sure the longitude is less than 360 and greater than or
        # equal to 0.
        if longitude >= 360.0 or longitude < 0.0:
            longitude = longitude % 360
            
        nakshatraAbbrevs = [\
            "Aswi",
            "Bhar",
            "Krit",
            "Rohi",
            "Mrig",
            "Ardr",
            "Puna",
            "Push",
            "Asre",
            "Magh",
            "PPha",
            "UPha",
            "Hast",
            "Chit",
            "Swat",
            "Visa",
            "Anur",
            "Jyes",
            "Mool",
            "PSha",
            "USha",
            "Srav",
            "Dhan",
            "Sata",
            "PBha",
            "UBha",
            "Reva"]
        
        index = math.floor(longitude / (360 / 27))
        
        return nakshatraAbbrevs[index]
        
    @staticmethod
    def getGlyphForPlanetName(planetName):
        """Takes a string value for the planet name and returns the
        unicode glyph value for this planet.
        
        Arguments:
        planetName - str value for the planet name.

        Returns:
        str - String that is unicode glyph for this planet.
        """

        settings = QSettings()

        # Return value.
        rv = None
        
        if planetName == "Ascendant":
            rv = settings.value(SettingsKeys.planetAscendantGlyphUnicodeKey,
                                SettingsKeys.planetAscendantGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Midheaven":
            rv = settings.value(SettingsKeys.planetMidheavenGlyphUnicodeKey,
                                SettingsKeys.planetMidheavenGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "HoraLagna":
            rv = settings.value(SettingsKeys.planetHoraLagnaGlyphUnicodeKey,
                                SettingsKeys.planetHoraLagnaGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "GhatiLagna":
            rv = settings.value(SettingsKeys.planetGhatiLagnaGlyphUnicodeKey,
                                SettingsKeys.planetGhatiLagnaGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "MeanLunarApogee":
            rv = settings.value(SettingsKeys.planetMeanLunarApogeeGlyphUnicodeKey,
                                SettingsKeys.planetMeanLunarApogeeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.value(SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeKey,
                                SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeKey,
                                SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeKey,
                                SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Sun":
            rv = settings.value(SettingsKeys.planetSunGlyphUnicodeKey,
                                SettingsKeys.planetSunGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Moon":
            rv = settings.value(SettingsKeys.planetMoonGlyphUnicodeKey,
                                SettingsKeys.planetMoonGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Mercury":
            rv = settings.value(SettingsKeys.planetMercuryGlyphUnicodeKey,
                                SettingsKeys.planetMercuryGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Venus":
            rv = settings.value(SettingsKeys.planetVenusGlyphUnicodeKey,
                                SettingsKeys.planetVenusGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Earth":
            rv = settings.value(SettingsKeys.planetEarthGlyphUnicodeKey,
                                SettingsKeys.planetEarthGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Mars":
            rv = settings.value(SettingsKeys.planetMarsGlyphUnicodeKey,
                                SettingsKeys.planetMarsGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Jupiter":
            rv = settings.value(SettingsKeys.planetJupiterGlyphUnicodeKey,
                                SettingsKeys.planetJupiterGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Saturn":
            rv = settings.value(SettingsKeys.planetSaturnGlyphUnicodeKey,
                                SettingsKeys.planetSaturnGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Uranus":
            rv = settings.value(SettingsKeys.planetUranusGlyphUnicodeKey,
                                SettingsKeys.planetUranusGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Neptune":
            rv = settings.value(SettingsKeys.planetNeptuneGlyphUnicodeKey,
                                SettingsKeys.planetNeptuneGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Pluto":
            rv = settings.value(SettingsKeys.planetPlutoGlyphUnicodeKey,
                                SettingsKeys.planetPlutoGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "MeanNorthNode":
            rv = settings.value(SettingsKeys.planetMeanNorthNodeGlyphUnicodeKey,
                                SettingsKeys.planetMeanNorthNodeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "MeanSouthNode":
            rv = settings.value(SettingsKeys.planetMeanSouthNodeGlyphUnicodeKey,
                                SettingsKeys.planetMeanSouthNodeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "TrueNorthNode":
            rv = settings.value(SettingsKeys.planetTrueNorthNodeGlyphUnicodeKey,
                                SettingsKeys.planetTrueNorthNodeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "TrueSouthNode":
            rv = settings.value(SettingsKeys.planetTrueSouthNodeGlyphUnicodeKey,
                                SettingsKeys.planetTrueSouthNodeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Ceres":
            rv = settings.value(SettingsKeys.planetCeresGlyphUnicodeKey,
                                SettingsKeys.planetCeresGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Pallas":
            rv = settings.value(SettingsKeys.planetPallasGlyphUnicodeKey,
                                SettingsKeys.planetPallasGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Juno":
            rv = settings.value(SettingsKeys.planetJunoGlyphUnicodeKey,
                                SettingsKeys.planetJunoGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Vesta":
            rv = settings.value(SettingsKeys.planetVestaGlyphUnicodeKey,
                                SettingsKeys.planetVestaGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Chiron":
            rv = settings.value(SettingsKeys.planetChironGlyphUnicodeKey,
                                SettingsKeys.planetChironGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Gulika":
            rv = settings.value(SettingsKeys.planetGulikaGlyphUnicodeKey,
                                SettingsKeys.planetGulikaGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Mandi":
            rv = settings.value(SettingsKeys.planetMandiGlyphUnicodeKey,
                                SettingsKeys.planetMandiGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "MeanOfFive":
            rv = settings.value(SettingsKeys.planetMeanOfFiveGlyphUnicodeKey,
                                SettingsKeys.planetMeanOfFiveGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "CycleOfEight":
            rv = settings.value(SettingsKeys.planetCycleOfEightGlyphUnicodeKey,
                                SettingsKeys.planetCycleOfEightGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "AvgMaJuSaUrNePl":
            rv = settings.value(SettingsKeys.planetAvgMaJuSaUrNePlGlyphUnicodeKey,
                                SettingsKeys.planetAvgMaJuSaUrNePlGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "AvgJuSaUrNe":
            rv = settings.value(SettingsKeys.planetAvgJuSaUrNeGlyphUnicodeKey,
                                SettingsKeys.planetAvgJuSaUrNeGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "AvgJuSa":
            rv = settings.value(SettingsKeys.planetAvgJuSaGlyphUnicodeKey,
                                SettingsKeys.planetAvgJuSaGlyphUnicodeDefValue,
                                type=str)
        else:
            rv = "???"
            self.log.warn("Could not find glyph for planet: " + \
                          planetName + ".  Using default value " + str(rv))

        return rv
    
    @staticmethod
    def getGlyphFontSizeForPlanetName(planetName):
        """Takes a string value for the planet name and returns the
        unicode glyph font size for this planet.
        
        Arguments:
        planetName - str value for the planet name.

        Returns:
        float - value for the font size of the unicode glyph for this planet.
        """

        settings = QSettings()

        # Return value.
        rv = None
        
        if planetName == "Ascendant":
            rv = settings.value(SettingsKeys.planetAscendantGlyphFontSizeKey,
                                SettingsKeys.planetAscendantGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Midheaven":
            rv = settings.value(SettingsKeys.planetMidheavenGlyphFontSizeKey,
                                SettingsKeys.planetMidheavenGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "HoraLagna":
            rv = settings.value(SettingsKeys.planetHoraLagnaGlyphFontSizeKey,
                                SettingsKeys.planetHoraLagnaGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "GhatiLagna":
            rv = settings.value(SettingsKeys.planetGhatiLagnaGlyphFontSizeKey,
                                SettingsKeys.planetGhatiLagnaGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "MeanLunarApogee":
            rv = settings.value(SettingsKeys.planetMeanLunarApogeeGlyphFontSizeKey,
                                SettingsKeys.planetMeanLunarApogeeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.value(SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeKey,
                                SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeKey,
                                SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeKey,
                                SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Sun":
            rv = settings.value(SettingsKeys.planetSunGlyphFontSizeKey,
                                SettingsKeys.planetSunGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Moon":
            rv = settings.value(SettingsKeys.planetMoonGlyphFontSizeKey,
                                SettingsKeys.planetMoonGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Mercury":
            rv = settings.value(SettingsKeys.planetMercuryGlyphFontSizeKey,
                                SettingsKeys.planetMercuryGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Venus":
            rv = settings.value(SettingsKeys.planetVenusGlyphFontSizeKey,
                                SettingsKeys.planetVenusGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Earth":
            rv = settings.value(SettingsKeys.planetEarthGlyphFontSizeKey,
                                SettingsKeys.planetEarthGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Mars":
            rv = settings.value(SettingsKeys.planetMarsGlyphFontSizeKey,
                                SettingsKeys.planetMarsGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Jupiter":
            rv = settings.value(SettingsKeys.planetJupiterGlyphFontSizeKey,
                                SettingsKeys.planetJupiterGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Saturn":
            rv = settings.value(SettingsKeys.planetSaturnGlyphFontSizeKey,
                                SettingsKeys.planetSaturnGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Uranus":
            rv = settings.value(SettingsKeys.planetUranusGlyphFontSizeKey,
                                SettingsKeys.planetUranusGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Neptune":
            rv = settings.value(SettingsKeys.planetNeptuneGlyphFontSizeKey,
                                SettingsKeys.planetNeptuneGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Pluto":
            rv = settings.value(SettingsKeys.planetPlutoGlyphFontSizeKey,
                                SettingsKeys.planetPlutoGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "MeanNorthNode":
            rv = settings.value(SettingsKeys.planetMeanNorthNodeGlyphFontSizeKey,
                                SettingsKeys.planetMeanNorthNodeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "MeanSouthNode":
            rv = settings.value(SettingsKeys.planetMeanSouthNodeGlyphFontSizeKey,
                                SettingsKeys.planetMeanSouthNodeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "TrueNorthNode":
            rv = settings.value(SettingsKeys.planetTrueNorthNodeGlyphFontSizeKey,
                                SettingsKeys.planetTrueNorthNodeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "TrueSouthNode":
            rv = settings.value(SettingsKeys.planetTrueSouthNodeGlyphFontSizeKey,
                                SettingsKeys.planetTrueSouthNodeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Ceres":
            rv = settings.value(SettingsKeys.planetCeresGlyphFontSizeKey,
                                SettingsKeys.planetCeresGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Pallas":
            rv = settings.value(SettingsKeys.planetPallasGlyphFontSizeKey,
                                SettingsKeys.planetPallasGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Juno":
            rv = settings.value(SettingsKeys.planetJunoGlyphFontSizeKey,
                                SettingsKeys.planetJunoGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Vesta":
            rv = settings.value(SettingsKeys.planetVestaGlyphFontSizeKey,
                                SettingsKeys.planetVestaGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Chiron":
            rv = settings.value(SettingsKeys.planetChironGlyphFontSizeKey,
                                SettingsKeys.planetChironGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Gulika":
            rv = settings.value(SettingsKeys.planetGulikaGlyphFontSizeKey,
                                SettingsKeys.planetGulikaGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Mandi":
            rv = settings.value(SettingsKeys.planetMandiGlyphFontSizeKey,
                                SettingsKeys.planetMandiGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "MeanOfFive":
            rv = settings.value(SettingsKeys.planetMeanOfFiveGlyphFontSizeKey,
                                SettingsKeys.planetMeanOfFiveGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "CycleOfEight":
            rv = settings.value(SettingsKeys.planetCycleOfEightGlyphFontSizeKey,
                                SettingsKeys.planetCycleOfEightGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "AvgMaJuSaUrNePl":
            rv = settings.value(SettingsKeys.planetAvgMaJuSaUrNePlGlyphFontSizeKey,
                                SettingsKeys.planetAvgMaJuSaUrNePlGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "AvgJuSaUrNe":
            rv = settings.value(SettingsKeys.planetAvgJuSaUrNeGlyphFontSizeKey,
                                SettingsKeys.planetAvgJuSaUrNeGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "AvgJuSa":
            rv = settings.value(SettingsKeys.planetAvgJuSaGlyphFontSizeKey,
                                SettingsKeys.planetAvgJuSaGlyphFontSizeDefValue,
                                type=float)
        else:
            rv = 10.0
            self.log.warn("Could not find glyph font size for planet: " + \
                          planetName + ".  Using default value " + str(rv))

        return rv

    @staticmethod
    def getAbbreviationForPlanetName(planetName):
        """Takes a planet name string value and returns the planet
        abbreviation for this planet.
        
        Arguments:
        planetName - str value for the planet name.

        Returns:
        str - value for the planet abbreviation.
        """

        settings = QSettings()

        # Return value.
        rv = None
        
        if planetName == "Ascendant":
            rv = settings.value(SettingsKeys.planetAscendantAbbreviationKey,
                                SettingsKeys.planetAscendantAbbreviationDefValue,
                                type=str)
        elif planetName == "Midheaven":
            rv = settings.value(SettingsKeys.planetMidheavenAbbreviationKey,
                                SettingsKeys.planetMidheavenAbbreviationDefValue,
                                type=str)
        elif planetName == "HoraLagna":
            rv = settings.value(SettingsKeys.planetHoraLagnaAbbreviationKey,
                                SettingsKeys.planetHoraLagnaAbbreviationDefValue,
                                type=str)
        elif planetName == "GhatiLagna":
            rv = settings.value(SettingsKeys.planetGhatiLagnaAbbreviationKey,
                                SettingsKeys.planetGhatiLagnaAbbreviationDefValue,
                                type=str)
        elif planetName == "MeanLunarApogee":
            rv = settings.value(SettingsKeys.planetMeanLunarApogeeAbbreviationKey,
                                SettingsKeys.planetMeanLunarApogeeAbbreviationDefValue,
                                type=str)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.value(SettingsKeys.planetOsculatingLunarApogeeAbbreviationKey,
                                SettingsKeys.planetOsculatingLunarApogeeAbbreviationDefValue,
                                type=str)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarApogeeAbbreviationKey,
                                SettingsKeys.planetInterpolatedLunarApogeeAbbreviationDefValue,
                                type=str)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationKey,
                                SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationDefValue,
                                type=str)
        elif planetName == "Sun":
            rv = settings.value(SettingsKeys.planetSunAbbreviationKey,
                                SettingsKeys.planetSunAbbreviationDefValue,
                                type=str)
        elif planetName == "Moon":
            rv = settings.value(SettingsKeys.planetMoonAbbreviationKey,
                                SettingsKeys.planetMoonAbbreviationDefValue,
                                type=str)
        elif planetName == "Mercury":
            rv = settings.value(SettingsKeys.planetMercuryAbbreviationKey,
                                SettingsKeys.planetMercuryAbbreviationDefValue,
                                type=str)
        elif planetName == "Venus":
            rv = settings.value(SettingsKeys.planetVenusAbbreviationKey,
                                SettingsKeys.planetVenusAbbreviationDefValue,
                                type=str)
        elif planetName == "Earth":
            rv = settings.value(SettingsKeys.planetEarthAbbreviationKey,
                                SettingsKeys.planetEarthAbbreviationDefValue,
                                type=str)
        elif planetName == "Mars":
            rv = settings.value(SettingsKeys.planetMarsAbbreviationKey,
                                SettingsKeys.planetMarsAbbreviationDefValue,
                                type=str)
        elif planetName == "Jupiter":
            rv = settings.value(SettingsKeys.planetJupiterAbbreviationKey,
                                SettingsKeys.planetJupiterAbbreviationDefValue,
                                type=str)
        elif planetName == "Saturn":
            rv = settings.value(SettingsKeys.planetSaturnAbbreviationKey,
                                SettingsKeys.planetSaturnAbbreviationDefValue,
                                type=str)
        elif planetName == "Uranus":
            rv = settings.value(SettingsKeys.planetUranusAbbreviationKey,
                                SettingsKeys.planetUranusAbbreviationDefValue,
                                type=str)
        elif planetName == "Neptune":
            rv = settings.value(SettingsKeys.planetNeptuneAbbreviationKey,
                                SettingsKeys.planetNeptuneAbbreviationDefValue,
                                type=str)
        elif planetName == "Pluto":
            rv = settings.value(SettingsKeys.planetPlutoAbbreviationKey,
                                SettingsKeys.planetPlutoAbbreviationDefValue,
                                type=str)
        elif planetName == "MeanNorthNode":
            rv = settings.value(SettingsKeys.planetMeanNorthNodeAbbreviationKey,
                                SettingsKeys.planetMeanNorthNodeAbbreviationDefValue,
                                type=str)
        elif planetName == "MeanSouthNode":
            rv = settings.value(SettingsKeys.planetMeanSouthNodeAbbreviationKey,
                                SettingsKeys.planetMeanSouthNodeAbbreviationDefValue,
                                type=str)
        elif planetName == "TrueNorthNode":
            rv = settings.value(SettingsKeys.planetTrueNorthNodeAbbreviationKey,
                                SettingsKeys.planetTrueNorthNodeAbbreviationDefValue,
                                type=str)
        elif planetName == "TrueSouthNode":
            rv = settings.value(SettingsKeys.planetTrueSouthNodeAbbreviationKey,
                                SettingsKeys.planetTrueSouthNodeAbbreviationDefValue,
                                type=str)
        elif planetName == "Ceres":
            rv = settings.value(SettingsKeys.planetCeresAbbreviationKey,
                                SettingsKeys.planetCeresAbbreviationDefValue,
                                type=str)
        elif planetName == "Pallas":
            rv = settings.value(SettingsKeys.planetPallasAbbreviationKey,
                                SettingsKeys.planetPallasAbbreviationDefValue,
                                type=str)
        elif planetName == "Juno":
            rv = settings.value(SettingsKeys.planetJunoAbbreviationKey,
                                SettingsKeys.planetJunoAbbreviationDefValue,
                                type=str)
        elif planetName == "Vesta":
            rv = settings.value(SettingsKeys.planetVestaAbbreviationKey,
                                SettingsKeys.planetVestaAbbreviationDefValue,
                                type=str)
        elif planetName == "Chiron":
            rv = settings.value(SettingsKeys.planetChironAbbreviationKey,
                                SettingsKeys.planetChironAbbreviationDefValue,
                                type=str)
        elif planetName == "Gulika":
            rv = settings.value(SettingsKeys.planetGulikaAbbreviationKey,
                                SettingsKeys.planetGulikaAbbreviationDefValue,
                                type=str)
        elif planetName == "Mandi":
            rv = settings.value(SettingsKeys.planetMandiAbbreviationKey,
                                SettingsKeys.planetMandiAbbreviationDefValue,
                                type=str)
        elif planetName == "MeanOfFive":
            rv = settings.value(SettingsKeys.planetMeanOfFiveAbbreviationKey,
                                SettingsKeys.planetMeanOfFiveAbbreviationDefValue,
                                type=str)
        elif planetName == "CycleOfEight":
            rv = settings.value(SettingsKeys.planetCycleOfEightAbbreviationKey,
                                SettingsKeys.planetCycleOfEightAbbreviationDefValue,
                                type=str)
        elif planetName == "AvgMaJuSaUrNePl":
            rv = settings.value(SettingsKeys.planetAvgMaJuSaUrNePlAbbreviationKey,
                                SettingsKeys.planetAvgMaJuSaUrNePlAbbreviationDefValue,
                                type=str)
        elif planetName == "AvgJuSaUrNe":
            rv = settings.value(SettingsKeys.planetAvgJuSaUrNeAbbreviationKey,
                                SettingsKeys.planetAvgJuSaUrNeAbbreviationDefValue,
                                type=str)
        elif planetName == "AvgJuSa":
            rv = settings.value(SettingsKeys.planetAvgJuSaAbbreviationKey,
                                SettingsKeys.planetAvgJuSaAbbreviationDefValue,
                                type=str)
        else:
            rv = "???"
            self.log.warn("Could not find abbreviation for planet: " + \
                          planetName + ".  Using default value " + str(rv))

        return rv

    @staticmethod
    def getForegroundColorForPlanetName(planetName):
        """Takes a string value for the planet name and returns the
        planet foreground color for this planet.
        
        Arguments:
        planetName - str value for the planet name.

        Returns:
        str - value for the planet abbreviation.
        """

        settings = QSettings()

        # Return value.
        rv = None
        
        if planetName == "Ascendant":
            rv = settings.value(SettingsKeys.planetAscendantForegroundColorKey,
                                SettingsKeys.planetAscendantForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Midheaven":
            rv = settings.value(SettingsKeys.planetMidheavenForegroundColorKey,
                                SettingsKeys.planetMidheavenForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "HoraLagna":
            rv = settings.value(SettingsKeys.planetHoraLagnaForegroundColorKey,
                                SettingsKeys.planetHoraLagnaForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "GhatiLagna":
            rv = settings.value(SettingsKeys.planetGhatiLagnaForegroundColorKey,
                                SettingsKeys.planetGhatiLagnaForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanLunarApogee":
            rv = settings.value(SettingsKeys.planetMeanLunarApogeeForegroundColorKey,
                                SettingsKeys.planetMeanLunarApogeeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.value(SettingsKeys.planetOsculatingLunarApogeeForegroundColorKey,
                                SettingsKeys.planetOsculatingLunarApogeeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarApogeeForegroundColorKey,
                                SettingsKeys.planetInterpolatedLunarApogeeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorKey,
                                SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Sun":
            rv = settings.value(SettingsKeys.planetSunForegroundColorKey,
                                SettingsKeys.planetSunForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Moon":
            rv = settings.value(SettingsKeys.planetMoonForegroundColorKey,
                                SettingsKeys.planetMoonForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Mercury":
            rv = settings.value(SettingsKeys.planetMercuryForegroundColorKey,
                                SettingsKeys.planetMercuryForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Venus":
            rv = settings.value(SettingsKeys.planetVenusForegroundColorKey,
                                SettingsKeys.planetVenusForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Earth":
            rv = settings.value(SettingsKeys.planetEarthForegroundColorKey,
                                SettingsKeys.planetEarthForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Mars":
            rv = settings.value(SettingsKeys.planetMarsForegroundColorKey,
                                SettingsKeys.planetMarsForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Jupiter":
            rv = settings.value(SettingsKeys.planetJupiterForegroundColorKey,
                                SettingsKeys.planetJupiterForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Saturn":
            rv = settings.value(SettingsKeys.planetSaturnForegroundColorKey,
                                SettingsKeys.planetSaturnForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Uranus":
            rv = settings.value(SettingsKeys.planetUranusForegroundColorKey,
                                SettingsKeys.planetUranusForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Neptune":
            rv = settings.value(SettingsKeys.planetNeptuneForegroundColorKey,
                                SettingsKeys.planetNeptuneForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Pluto":
            rv = settings.value(SettingsKeys.planetPlutoForegroundColorKey,
                                SettingsKeys.planetPlutoForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanNorthNode":
            rv = settings.value(SettingsKeys.planetMeanNorthNodeForegroundColorKey,
                                SettingsKeys.planetMeanNorthNodeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanSouthNode":
            rv = settings.value(SettingsKeys.planetMeanSouthNodeForegroundColorKey,
                                SettingsKeys.planetMeanSouthNodeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "TrueNorthNode":
            rv = settings.value(SettingsKeys.planetTrueNorthNodeForegroundColorKey,
                                SettingsKeys.planetTrueNorthNodeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "TrueSouthNode":
            rv = settings.value(SettingsKeys.planetTrueSouthNodeForegroundColorKey,
                                SettingsKeys.planetTrueSouthNodeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Ceres":
            rv = settings.value(SettingsKeys.planetCeresForegroundColorKey,
                                SettingsKeys.planetCeresForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Pallas":
            rv = settings.value(SettingsKeys.planetPallasForegroundColorKey,
                                SettingsKeys.planetPallasForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Juno":
            rv = settings.value(SettingsKeys.planetJunoForegroundColorKey,
                                SettingsKeys.planetJunoForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Vesta":
            rv = settings.value(SettingsKeys.planetVestaForegroundColorKey,
                                SettingsKeys.planetVestaForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Chiron":
            rv = settings.value(SettingsKeys.planetChironForegroundColorKey,
                                SettingsKeys.planetChironForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Gulika":
            rv = settings.value(SettingsKeys.planetGulikaForegroundColorKey,
                                SettingsKeys.planetGulikaForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Mandi":
            rv = settings.value(SettingsKeys.planetMandiForegroundColorKey,
                                SettingsKeys.planetMandiForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanOfFive":
            rv = settings.value(SettingsKeys.planetMeanOfFiveForegroundColorKey,
                                SettingsKeys.planetMeanOfFiveForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "CycleOfEight":
            rv = settings.value(SettingsKeys.planetCycleOfEightForegroundColorKey,
                                SettingsKeys.planetCycleOfEightForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "AvgMaJuSaUrNePl":
            rv = settings.value(SettingsKeys.planetAvgMaJuSaUrNePlForegroundColorKey,
                                SettingsKeys.planetAvgMaJuSaUrNePlForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "AvgJuSaUrNe":
            rv = settings.value(SettingsKeys.planetAvgJuSaUrNeForegroundColorKey,
                                SettingsKeys.planetAvgJuSaUrNeForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "AvgJuSa":
            rv = settings.value(SettingsKeys.planetAvgJuSaForegroundColorKey,
                                SettingsKeys.planetAvgJuSaForegroundColorDefValue,\
                                type=QColor)
        else:
            rv = QColor(Qt.black)
            self.log.warn("Could not find foreground color for planet: " + \
                          planetName + ".  Using default value " + str(rv))

        return rv

    @staticmethod
    def getBackgroundColorForPlanetName(planetName):
        """Takes a string value for the planet name and returns the
        planet background color for this planet.
        
        Arguments:
        planetName - str value for the planet name.

        Returns:
        str - value for the planet abbreviation.
        """

        settings = QSettings()

        # Return value.
        rv = None
        
        if planetName == "Ascendant":
            rv = settings.value(SettingsKeys.planetAscendantBackgroundColorKey,
                                SettingsKeys.planetAscendantBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Midheaven":
            rv = settings.value(SettingsKeys.planetMidheavenBackgroundColorKey,
                                SettingsKeys.planetMidheavenBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "HoraLagna":
            rv = settings.value(SettingsKeys.planetHoraLagnaBackgroundColorKey,
                                SettingsKeys.planetHoraLagnaBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "GhatiLagna":
            rv = settings.value(SettingsKeys.planetGhatiLagnaBackgroundColorKey,
                                SettingsKeys.planetGhatiLagnaBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanLunarApogee":
            rv = settings.value(SettingsKeys.planetMeanLunarApogeeBackgroundColorKey,
                                SettingsKeys.planetMeanLunarApogeeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.value(SettingsKeys.planetOsculatingLunarApogeeBackgroundColorKey,
                                SettingsKeys.planetOsculatingLunarApogeeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorKey,
                                SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.value(SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorKey,
                                SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Sun":
            rv = settings.value(SettingsKeys.planetSunBackgroundColorKey,
                                SettingsKeys.planetSunBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Moon":
            rv = settings.value(SettingsKeys.planetMoonBackgroundColorKey,
                                SettingsKeys.planetMoonBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Mercury":
            rv = settings.value(SettingsKeys.planetMercuryBackgroundColorKey,
                                SettingsKeys.planetMercuryBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Venus":
            rv = settings.value(SettingsKeys.planetVenusBackgroundColorKey,
                                SettingsKeys.planetVenusBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Earth":
            rv = settings.value(SettingsKeys.planetEarthBackgroundColorKey,
                                SettingsKeys.planetEarthBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Mars":
            rv = settings.value(SettingsKeys.planetMarsBackgroundColorKey,
                                SettingsKeys.planetMarsBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Jupiter":
            rv = settings.value(SettingsKeys.planetJupiterBackgroundColorKey,
                                SettingsKeys.planetJupiterBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Saturn":
            rv = settings.value(SettingsKeys.planetSaturnBackgroundColorKey,
                                SettingsKeys.planetSaturnBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Uranus":
            rv = settings.value(SettingsKeys.planetUranusBackgroundColorKey,
                                SettingsKeys.planetUranusBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Neptune":
            rv = settings.value(SettingsKeys.planetNeptuneBackgroundColorKey,
                                SettingsKeys.planetNeptuneBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Pluto":
            rv = settings.value(SettingsKeys.planetPlutoBackgroundColorKey,
                                SettingsKeys.planetPlutoBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanNorthNode":
            rv = settings.value(SettingsKeys.planetMeanNorthNodeBackgroundColorKey,
                                SettingsKeys.planetMeanNorthNodeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanSouthNode":
            rv = settings.value(SettingsKeys.planetMeanSouthNodeBackgroundColorKey,
                                SettingsKeys.planetMeanSouthNodeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "TrueNorthNode":
            rv = settings.value(SettingsKeys.planetTrueNorthNodeBackgroundColorKey,
                                SettingsKeys.planetTrueNorthNodeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "TrueSouthNode":
            rv = settings.value(SettingsKeys.planetTrueSouthNodeBackgroundColorKey,
                                SettingsKeys.planetTrueSouthNodeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Ceres":
            rv = settings.value(SettingsKeys.planetCeresBackgroundColorKey,
                                SettingsKeys.planetCeresBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Pallas":
            rv = settings.value(SettingsKeys.planetPallasBackgroundColorKey,
                                SettingsKeys.planetPallasBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Juno":
            rv = settings.value(SettingsKeys.planetJunoBackgroundColorKey,
                                SettingsKeys.planetJunoBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Vesta":
            rv = settings.value(SettingsKeys.planetVestaBackgroundColorKey,
                                SettingsKeys.planetVestaBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Chiron":
            rv = settings.value(SettingsKeys.planetChironBackgroundColorKey,
                                SettingsKeys.planetChironBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Gulika":
            rv = settings.value(SettingsKeys.planetGulikaBackgroundColorKey,
                                SettingsKeys.planetGulikaBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Mandi":
            rv = settings.value(SettingsKeys.planetMandiBackgroundColorKey,
                                SettingsKeys.planetMandiBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "MeanOfFive":
            rv = settings.value(SettingsKeys.planetMeanOfFiveBackgroundColorKey,
                                SettingsKeys.planetMeanOfFiveBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "CycleOfEight":
            rv = settings.value(SettingsKeys.planetCycleOfEightBackgroundColorKey,
                                SettingsKeys.planetCycleOfEightBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "AvgMaJuSaUrNePl":
            rv = settings.value(SettingsKeys.planetAvgMaJuSaUrNePlBackgroundColorKey,
                                SettingsKeys.planetAvgMaJuSaUrNePlBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "AvgJuSaUrNe":
            rv = settings.value(SettingsKeys.planetAvgJuSaUrNeBackgroundColorKey,
                                SettingsKeys.planetAvgJuSaUrNeBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "AvgJuSa":
            rv = settings.value(SettingsKeys.planetAvgJuSaBackgroundColorKey,
                                SettingsKeys.planetAvgJuSaBackgroundColorDefValue,\
                                type=QColor)
        else:
            rv = QColor(Qt.transparent)
            self.log.warn("Could not find background color for planet: " + \
                          planetName + ".  Using default value " + str(rv))

        return rv
    

class RadixChartAspectGraphicsItem(QGraphicsItem):
    """QGraphicsItem that represents an aspect on a Radix Chart."""

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
    
        # Logger
        self.log = \
            logging.getLogger("astrologychart.RadixChartAspectGraphicsItem")
            
        # Name of the aspect that is applied.
        self.aspectName = None

        # Angle of the aspect that is applied (the ideal exact angle).
        self.aspectAngle = None
        
        # Orb setting that makes the aspect applicable.
        self.aspectOrb = None

        # Actual aspect angle between the two planets.
        self.actualAspectAngle = None
        
        # Actual orb between the two planets.
        self.actualAspectOrb = None
        
        # Color of the drawn line.
        self.color = None

        # Brush style.
        self.brushStyle = None
        
        # Degree of the first planet.
        self.p1Degree = None

        # Degree of the second planet.
        self.p2Degree = None

        # Wheel number of the first planet.
        self.p1WheelNumber = None
        
        # Wheel number of the second planet.
        self.p2WheelNumber = None
        
        # Use QSettings to get application preferences related to the
        # aspects.
        self.settings = QSettings()

        # Keep a running total of the different number of aspects that
        # apply between these two planets.  Ideally, only one aspect
        # type should apply, but this can happen if the orb is really
        # large.  In this case, we would log a warning and use the last
        # applicable aspect tested.
        self.numAspectMatches = 0
        
        # Start and end points of the line segment, in parent coordinates.
        # These are used by the paint function.
        self.startPointF = QPointF(0.0, 0.0)
        self.endPointF = QPointF(0.0, 0.0)
        
        # Set to not enabled and not visible by default, until other
        # parameters are set.
        self.setEnabled(False)
        self.setVisible(False)

    def setForPlanets(self, p1Degree, p2Degree,
                            p1WheelNumber, p2WheelNumber):
        """Sets the item so that it is applicable for the above parameters.
        
        Arguments:
        p1Degree      - Degrees of longitude for the planet 1.
        p2Degree      - Degrees of longitude for the planet 2.
        p1WheelNumber - Wheel number applicable to planet 1.
        p2WheelNumber - Wheel number applicable to planet 2.
        """
        

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Entered setForPlanets()")
            self.log.debug("p1Degree == {}".format(p1Degree))
            self.log.debug("p2Degree == {}".format(p2Degree))
            self.log.debug("p1WheelNumber == {}".format(p1WheelNumber))
            self.log.debug("p2WheelNumber == {}".format(p2WheelNumber))

        # Set the enabled flag to True unless we find a case where it
        # should be False.
        enabledFlag = True
        
        # Reset the count for the number of aspect matches.
        self.numAspectMatches = 0
        
        # See if the wheel numbers used are applicable.
        
        if (p1WheelNumber == 1 or p2WheelNumber == 1) and \
            self.settings.value(\
            SettingsKeys.aspectAstrologyChart1EnabledKey, \
            SettingsKeys.aspectAstrologyChart1EnabledDefValue,
            type=bool) == False:

            enabledFlag = False

        if (p1WheelNumber == 2 or p2WheelNumber == 2) and \
            self.settings.value(\
            SettingsKeys.aspectAstrologyChart2EnabledKey, \
            SettingsKeys.aspectAstrologyChart2EnabledDefValue,
            type=bool) == False:

            enabledFlag = False
        
        if (p1WheelNumber == 3 or p2WheelNumber == 3) and \
            self.settings.value(\
            SettingsKeys.aspectAstrologyChart3EnabledKey, \
            SettingsKeys.aspectAstrologyChart3EnabledDefValue,
            type=bool) == False:

            enabledFlag = False
        
        if ((p1WheelNumber == 1 and p2WheelNumber == 2) or \
            (p1WheelNumber == 2 and p2WheelNumber == 1)) and \
            self.settings.value(\
            SettingsKeys.aspectBtwnAstrologyChart1And2EnabledKey, \
            SettingsKeys.aspectBtwnAstrologyChart1And2EnabledDefValue,
            type=bool) == False:

            enabledFlag = False
            
        if ((p1WheelNumber == 1 and p2WheelNumber == 3) or \
            (p1WheelNumber == 3 and p2WheelNumber == 1)) and \
            self.settings.value(\
            SettingsKeys.aspectBtwnAstrologyChart1And3EnabledKey, \
            SettingsKeys.aspectBtwnAstrologyChart1And3EnabledDefValue,
            type=bool) == False:

            enabledFlag = False
            
        if ((p1WheelNumber == 2 and p2WheelNumber == 3) or \
            (p1WheelNumber == 3 and p2WheelNumber == 2)) and \
            self.settings.value(\
            SettingsKeys.aspectBtwnAstrologyChart2And3EnabledKey, \
            SettingsKeys.aspectBtwnAstrologyChart2And3EnabledDefValue,
            type=bool) == False:

            enabledFlag = False

        if enabledFlag == False:
            # If this particular combination of chart wheel numbers is
            # not enabled, then set to the item to disabled and return.
            self.log.debug("Not enabled.")
            
            # Set all values to None.
            self.aspectName = None
            self.aspectAngle = None
            self.aspectOrb = None
            self.actualAspectAngle = None
            self.actualAspectOrb = None
            self.color = None
            self.p1Degree = None
            self.p2Degree = None
            self.p1WheelNumber = None
            self.p2WheelNumber = None

            # Set as disabled and not visible.
            self.setEnabled(False)
            self.setVisible(False)

            # Return.
            return

        # Calculate the diffs to determine what kind of aspect this
        # would be.
        diff = Util.toNormalizedAngle(p2Degree - p1Degree)

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("diff == {}".format(diff))
        
        # Conjunction.
        if self.settings.value(\
            SettingsKeys.aspectConjunctionEnabledKey, \
            SettingsKeys.aspectConjunctionEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectConjunctionNameKey,
                SettingsKeys.aspectConjunctionNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectConjunctionAngleKey,
                SettingsKeys.aspectConjunctionAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectConjunctionOrbKey,
                SettingsKeys.aspectConjunctionOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectConjunctionColorKey,
                SettingsKeys.aspectConjunctionColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Opposition.
        if self.settings.value(\
            SettingsKeys.aspectOppositionEnabledKey, \
            SettingsKeys.aspectOppositionEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectOppositionNameKey,
                SettingsKeys.aspectOppositionNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectOppositionAngleKey,
                SettingsKeys.aspectOppositionAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectOppositionOrbKey,
                SettingsKeys.aspectOppositionOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectOppositionColorKey,
                SettingsKeys.aspectOppositionColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Square.
        if self.settings.value(\
            SettingsKeys.aspectSquareEnabledKey, \
            SettingsKeys.aspectSquareEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectSquareNameKey,
                SettingsKeys.aspectSquareNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectSquareAngleKey,
                SettingsKeys.aspectSquareAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectSquareOrbKey,
                SettingsKeys.aspectSquareOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectSquareColorKey,
                SettingsKeys.aspectSquareColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Trine.
        if self.settings.value(\
            SettingsKeys.aspectTrineEnabledKey, \
            SettingsKeys.aspectTrineEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectTrineNameKey,
                SettingsKeys.aspectTrineNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectTrineAngleKey,
                SettingsKeys.aspectTrineAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectTrineOrbKey,
                SettingsKeys.aspectTrineOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectTrineColorKey,
                SettingsKeys.aspectTrineColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Sextile.
        if self.settings.value(\
            SettingsKeys.aspectSextileEnabledKey, \
            SettingsKeys.aspectSextileEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectSextileNameKey,
                SettingsKeys.aspectSextileNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectSextileAngleKey,
                SettingsKeys.aspectSextileAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectSextileOrbKey,
                SettingsKeys.aspectSextileOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectSextileColorKey,
                SettingsKeys.aspectSextileColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Inconjunct.
        if self.settings.value(\
            SettingsKeys.aspectInconjunctEnabledKey, \
            SettingsKeys.aspectInconjunctEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectInconjunctNameKey,
                SettingsKeys.aspectInconjunctNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectInconjunctAngleKey,
                SettingsKeys.aspectInconjunctAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectInconjunctOrbKey,
                SettingsKeys.aspectInconjunctOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectInconjunctColorKey,
                SettingsKeys.aspectInconjunctColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Semisextile.
        if self.settings.value(\
            SettingsKeys.aspectSemisextileEnabledKey, \
            SettingsKeys.aspectSemisextileEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectSemisextileNameKey,
                SettingsKeys.aspectSemisextileNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectSemisextileAngleKey,
                SettingsKeys.aspectSemisextileAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectSemisextileOrbKey,
                SettingsKeys.aspectSemisextileOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectSemisextileColorKey,
                SettingsKeys.aspectSemisextileColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Semisquare.
        if self.settings.value(\
            SettingsKeys.aspectSemisquareEnabledKey, \
            SettingsKeys.aspectSemisquareEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectSemisquareNameKey,
                SettingsKeys.aspectSemisquareNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectSemisquareAngleKey,
                SettingsKeys.aspectSemisquareAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectSemisquareOrbKey,
                SettingsKeys.aspectSemisquareOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectSemisquareColorKey,
                SettingsKeys.aspectSemisquareColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        # Sesquiquadrate.
        if self.settings.value(\
            SettingsKeys.aspectSesquiquadrateEnabledKey, \
            SettingsKeys.aspectSesquiquadrateEnabledDefValue,
            type=bool) == True:

            # Values from QSettings, related to this aspect.
            name = \
                self.settings.value(\
                SettingsKeys.aspectSesquiquadrateNameKey,
                SettingsKeys.aspectSesquiquadrateNameDefValue,
                type=str)
            
            angle = \
                self.settings.value(\
                SettingsKeys.aspectSesquiquadrateAngleKey,
                SettingsKeys.aspectSesquiquadrateAngleDefValue,
                type=float)

            orb = \
                self.settings.value(\
                SettingsKeys.aspectSesquiquadrateOrbKey,
                SettingsKeys.aspectSesquiquadrateOrbDefValue,
                type=float)

            color = \
                self.settings.value(\
                SettingsKeys.aspectSesquiquadrateColorKey,
                SettingsKeys.aspectSesquiquadrateColorDefValue,
                type=QColor)

            self._matchTest(\
                name, angle, orb, color,
                p1Degree, p2Degree, p1WheelNumber, p2WheelNumber,
                diff)

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("self.numAspectMatches == {}".format(self.numAspectMatches))
        
        if self.numAspectMatches == 0:
            # No matches.  Set all values to None.
            self.aspectName = None
            self.aspectAngle = None
            self.aspectOrb = None
            self.actualAspectAngle = None
            self.actualAspectOrb = None
            self.color = None
            self.p1Degree = None
            self.p2Degree = None
            self.p1WheelNumber = None
            self.p2WheelNumber = None

            self.setEnabled(False)
            self.setVisible(False)
            
        elif self.numAspectMatches > 1:
                self.log.warn("Matched more than one aspect type!  " +
                              "Only using the last match '{}'".\
                              format(self.aspectName))
            
        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Exiting setForPlanets()")


    def _matchTest(self, name, angle, orb, color,
                   p1Degree, p2Degree,
                   p1WheelNumber, p2WheelNumber,
                   diff):
        """Helper function to do comparisons for aspect match.  If
        there's a match, then class member variables are set
        appropriately for the setting.

        Arguments:
        name  - str value for the name of the aspect.
        angle - float value for the angle of the desired aspect.
        orb   - float value for the degrees of aspect orb allowable.
        color - QColor object for the color to use if drawing this aspect.
        p1Degree - float value for the degree of planet 1.
        p2Degree - float value for the degree of planet 2.
        p1WheelNumber - int value for the wheel number of planet 1.
        p2WheelNumber - int value for the wheel number of planet 2.
        diff - float value for the normalized difference in degrees
               between planet 1 and 2.
               
        Returns:
        True if a match was found, False otherwise.
        """

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Entered _matchTest()")

        # Return value.
        rv = False
        
        # Move all angle values to between 0 and 1080 so that we
        # don't have to worry about degree overlaps on the
        # boundaries.
        shiftedAngle = angle
        if shiftedAngle < 360:
            shiftedAngle += 360

        minValue = shiftedAngle - orb
        maxValue = shiftedAngle + orb
        
        shiftedDiff = diff
        if shiftedDiff < 360:
            shiftedDiff += 360

        if self.log.isEnabledFor(logging.DEBUG) == True and True == False:
            self.log.debug("name == {}".format(name))
            self.log.debug("angle == {}".format(angle))
            self.log.debug("orb == {}".format(orb))
            self.log.debug("p1Degree == {}".format(p1Degree))
            self.log.debug("p2Degree == {}".format(p2Degree))
            self.log.debug("p1WheelNumber == {}".format(p1WheelNumber))
            self.log.debug("p2WheelNumber == {}".format(p2WheelNumber))
            self.log.debug("diff == {}".format(diff))
            self.log.debug("shiftedAngle == {}".format(shiftedAngle))
            self.log.debug("minValue == {}".format(minValue))
            self.log.debug("maxValue == {}".format(maxValue))
            self.log.debug("shiftedDiff == {}".format(shiftedDiff))

        if minValue <= shiftedDiff <= maxValue:
            # Aspect applies.
            self.numAspectMatches += 1
            
            # Set the values.
            self.aspectName = name
            self.aspectAngle = angle
            self.aspectOrb = orb
            self.actualAspectAngle = diff
            self.actualAspectOrb = diff - angle
            self.color = color
            self.p1Degree = p1Degree
            self.p2Degree = p2Degree
            self.p1WheelNumber = p1WheelNumber
            self.p2WheelNumber = p2WheelNumber

            # Set the brush style.
            # Here we have 7 different brush styles.
            numSlices = 7
            orbRangeSlice = abs(self.aspectOrb) / numSlices
            if self.actualAspectOrb > 180:
                sliceNum = math.floor(abs(self.actualAspectOrb - 360.0) / orbRangeSlice)
            else:
                sliceNum = math.floor(abs(self.actualAspectOrb) / orbRangeSlice)
            
            if sliceNum == 0:
                self.brushStyle = Qt.SolidPattern
            elif sliceNum == 1:
                self.brushStyle = Qt.Dense3Pattern
            elif sliceNum == 2:
                self.brushStyle = Qt.Dense4Pattern
            elif sliceNum == 3:
                self.brushStyle = Qt.Dense5Pattern
            elif sliceNum == 4:
                self.brushStyle = Qt.Dense5Pattern
            elif sliceNum == 5:
                self.brushStyle = Qt.Dense6Pattern
            elif sliceNum == 6:
                self.brushStyle = Qt.Dense6Pattern
            else:
                self.log.error("Invalid sliceNum.  Please investigate why.")
                self.brushStyle = Qt.NoBrush

            if self.log.isEnabledFor(logging.DEBUG) == True and True == False:
                self.log.debug("self.aspectName == {}".format(self.aspectName))
                self.log.debug("self.aspectAngle == {}".format(self.aspectAngle))
                self.log.debug("self.aspectOrb == {}".format(self.aspectOrb))
                self.log.debug("self.actualAspectAngle == {}".format(self.actualAspectAngle))
                self.log.debug("self.actualAspectOrb == {}".format(self.actualAspectOrb))
                self.log.debug("self.p1Degree == {}".format(self.p1Degree))
                self.log.debug("self.p2Degree == {}".format(self.p2Degree))
                self.log.debug("self.p1WheelNumber == {}".format(self.p1WheelNumber))
                self.log.debug("self.p2WheelNumber == {}".format(self.p2WheelNumber))
                self.log.debug("self.brushStyle == {}".format(self.brushStyle))
                self.log.debug("orbRangeSlice == {}".format(orbRangeSlice))
                self.log.debug("sliceNum == {}".format(sliceNum))

                self.log.debug("Matched aspect {}".format(self.aspectName))
            
            self.setEnabled(True)
            self.setVisible(True)
            self.update()
            self.prepareGeometryChange()
            
            rv = True
        else:
            rv = False

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Exiting _matchTest()")
        
        return rv
    
            
    def __str__(self):
        """Returns a str representing this object's contents."""

        return self.toString()
        
    def toString(self):
        """Returns a str representing this object's contents."""

        return Util.objToString(self)
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) is the location where the center of the
        # circular radix chart.  

        # If there are circles for where the planets are drawn (which
        # there should be), then set the radius as the first circle
        # drawn.  This is the one with the smallest radius.

        # Get the radius.
        radius = 0.0
        parent = self.parentItem()
        if parent != None and isinstance(parent, RadixChartGraphicsItem) == True:
            radius = parent.getInnerRasiRadius()
            # TODO:  Remove the line below if the above works.
            #radius = parent.getRadiusForWheelNumber(1)
        else:
            return QRectF()
            
        diameter = radius + radius
        
        x = -1.0 * radius
        y = -1.0 * radius
        width = diameter
        height = diameter
        
        return QRectF(x, y, width, height)
    
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem. """

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Entered paint()")
        
        # Coordinate (0, 0) is the location where the center of the
        # circular radix chart.  

        # Only paint if the item is enabled and visible.
        if self.isEnabled() == False or self.isVisible() == False:
            return
        
        # Get the radius.
        radius = 0.0
        parent = self.parentItem()
        if parent != None and isinstance(parent, RadixChartGraphicsItem) == True:
            radius = parent.getInnerRasiRadius()
            if self.log.isEnabledFor(logging.DEBUG) == True:
                self.log.debug("radius obtained from parent is: {}".format(radius))
        else:
            self.log.error("Unsupported parent QGraphicsItem type.")

        if Util.fuzzyIsEqual(radius, 0.0):
            if self.log.isEnabledFor(logging.DEBUG) == True:
                self.log.debug("Radius is 0.0.  Not drawing anything.")
            return
        
        # Start and end points of the line segment, in parent coordinates.
        # Use the QLineF function to convert from polar coordinates to
        # cartesian.
        self.startPointF = \
            QLineF.fromPolar(radius, self.p1Degree + 180.0).p2()
        self.endPointF = \
            QLineF.fromPolar(radius, self.p2Degree + 180.0).p2()
        
        # Pen and brush for the painting.
        pen = painter.pen()
        pen.setColor(self.color)
        pen.setWidthF(0.0)
        brush = pen.brush()
        brush.setColor(self.color)
        brush.setStyle(self.brushStyle)
        pen.setBrush(brush)
        painter.setPen(pen)
        
        # Draw the line.
        painter.drawLine(self.startPointF, self.endPointF)

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Line was drawn from: ({}, {}) to ({}, {})".\
                           format(self.startPointF.x(), self.startPointF.y(),
                                  self.endPointF.x(), self.endPointF.y()))
            self.log.debug("Exiting paint()")
        

class RadixChartGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is the circle astrology chart."""

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

    def getRadiusForWheelNumber(self, wheelNumber):
        """Virtual function.  Subclasses must overwrite and implement.

        Returns the radius of the circle drawn for the argument wheel
        number.  This value is used by child QGraphicsItems to
        determine where they should be drawn for a certain wheel
        number.  The first wheel is wheel number 0.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius of that wheel number.
        """

        return 0.0

    def getTerminalRadiusForWheelNumber(self, wheelNumber):
        """Virtual function.  Subclasses must overwrite and implement.

        Returns the radius from the origin of where the terminal line
        of child items should terminate for a certain wheel number.
        The returned value is less than the number returned from the
        call to getRadiusForWheelNumber().  The first wheel is wheel
        number 1.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius.
        """

        return 0.0

    
class SiderealRadixChartGraphicsItem(RadixChartGraphicsItem):
    """QGraphicsItem that is the circle chart with the following labels on
    the edges:

    - Number for the Rasi
    - Abbreviation for the Nakshatra
    - Number for the Navamsa Rasi.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)
        
        # Logger
        self.log = \
            logging.getLogger("astrologychart.SiderealRadixChartGraphicsItem")

        # Pen which is used to do the painting.
        self.pen = QPen()
        self.pen.setColor(QColor(Qt.black))
        self.pen.setWidthF(0.0)
        brush = self.pen.brush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        self.pen.setBrush(brush)

        # Below are radius measurements for when drawing.
        
        # Rasi
        self.innerRasiRadius = 300.0
        self.outerRasiRadius = self.innerRasiRadius + 50.0

        # Nakshatra
        self.innerNakshatraRadius = self.outerRasiRadius
        self.outerNakshatraRadius = self.innerNakshatraRadius + 30.0

        # Navamsa
        self.innerNavamsaRadius = self.outerNakshatraRadius
        self.outerNavamsaRadius = self.innerNavamsaRadius + 30.0

        # Circles for the planet locations.
        increment = 52.0
        i = 0
        self.wheelNumberCircleRadius = list()
        self.wheelNumberCircleRadius.\
            append(self.outerNavamsaRadius + increment)
        i += 1
        self.wheelNumberCircleRadius.\
            append(self.wheelNumberCircleRadius[i-1] + increment)
        i += 1
        self.wheelNumberCircleRadius.\
            append(self.wheelNumberCircleRadius[i-1] + increment)
        i += 1
        self.wheelNumberCircleRadius.\
            append(self.wheelNumberCircleRadius[i-1] + increment)

        # Below are the fonts used in drawing text.
        self.rasiLabelFont = QFont()
        self.rasiLabelFont.setFamily("Lucida Console")
        self.rasiLabelFont.setPointSize(14)
        
        self.nakshatraLabelFont = QFont()
        self.nakshatraLabelFont.setFamily("Lucida Console")
        self.nakshatraLabelFont.setPointSize(10)
        
        self.navamsaLabelFont = QFont()
        self.navamsaLabelFont.setFamily("Lucida Console")
        self.navamsaLabelFont.setPointSize(9)

    def getRadiusForWheelNumber(self, wheelNumber):
        """Overwritten function from class RadixChartGraphicsItem.

        Returns the radius of the circle drawn for the argument wheel
        number.  This value is used by child QGraphicsItems to
        determine where they should be drawn for a certain wheel
        number.  The first wheel is wheel number 1.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius of that wheel number.
        """

        # Return value.
        rv = 0.0
        
        if wheelNumber > 0 and wheelNumber <= len(self.wheelNumberCircleRadius):
            rv = self.wheelNumberCircleRadius[wheelNumber-1]
        else:
            self.log.error("Invalid wheelNumber provided to " + \
                           "getRadiusForWheelNumber().  Returning 0.0")
            rv = 0.0

        return rv

    def getTerminalRadiusForWheelNumber(self, wheelNumber):
        """Overwritten function from class RadixChartGraphicsItem.

        Returns the radius from the origin of where the terminal line
        of child items should terminate for a certain wheel number.
        The returned value is less than the number returned from the
        call to getRadiusForWheelNumber().  The first wheel is wheel
        number 1.

        Argument:
        wheelNumber - int value for the wheel number.

        Returns:
        float - value for the radius.
        """

        # Return value.
        rv = 0.0

        # TODO:  Decide if I should always return the same terminalRadiusForWheelNumber for all.
        return self.getInnerRasiRadius()
        #return rv

        if wheelNumber > 0 and wheelNumber <= len(self.wheelNumberCircleRadius):
            rv = self.wheelNumberCircleRadius[wheelNumber-1]
        elif wheelNumber == 0:
            rv = self.outerNavamsaRadius
        else:
            self.log.error("Invalid wheelNumber provided to " + \
                           "getTerminalRadiusForWheelNumber().  Returning 0.0")
            rv = 0.0

        return rv

    def getRadixPlanetGraphicsItem(self, planetName, wheelNumber):
        """Returns the RadixPlanetGraphicsItem with the given planet
        name on the given wheel.  If no match is found, None
        is returned.

        Arguments:
        
        planetName - str value holding the planet name as set in the
        RadixPlanetGraphicsItem.

        wheelNumber - int value holding the wheel number that the
        RadixPlanetGraphicsItem is drawn on in the
        SiderealRadixChartGraphicsItem.
        """

        # Get the child GraphicsItems.
        children = self.childItems()
        
        # Go through them and look at the ones that are
        # RadixPlanetGraphicsItem.
        for child in children:
            if isinstance(child, RadixPlanetGraphicsItem):
                # If the planet name matches and the wheel
                # number matches, then return that QGraphicsItem.
                if child.getPlanetName() == planetName and \
                    child.getWheelNumber() == wheelNumber:
                    
                    return child

        return None

    def redrawAspects(self):
        """If drawing aspects is enabled via Application Preferences
        (QSettings), then this function draws aspects between the
        RadixPlanetGraphicsItems in the given wheelNumber.  The
        aspects drawn are according to the aspects enabled and
        configured in Application Preferences (QSettings).
        """

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Entered redrawAspects()")
        
        # Get the child GraphicsItems.
        children = self.childItems()

        # Get all planet graphics items, and all aspect graphics items.
        planets = []
        aspects = []
        
        # Go through them and look at the ones that are
        # RadixPlanetGraphicsItem.
        for child in children:
            if isinstance(child, RadixPlanetGraphicsItem):
                planets.append(child)
            elif isinstance(child, RadixChartAspectGraphicsItem):
                aspects.append(child)

        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("len(planets) == {}".format(len(planets)))
            self.log.debug("len(aspects) == {}".format(len(aspects)))
        
        # Remove all previously used aspects.
        for aspect in aspects:
            self.scene().removeItem(aspect)
        aspects = []
        
        # Check for aspects with planets in all combinations.
        for i in range(len(planets)):
            for j in range(len(planets)):
                p1 = planets[i]
                p2 = planets[j]

                if self.log.isEnabledFor(logging.DEBUG) == True:
                    self.log.debug("p1 is: name={}, wheelNumber={}, degree={}".\
                                   format(p1.planetName,
                                          p1.wheelNumber,
                                          p1.degree))
                    self.log.debug("p2 is: name={}, wheelNumber={}, degree={}".\
                                   format(p2.planetName,
                                          p2.wheelNumber,
                                          p2.degree))
                
                if not (p1 is p2):
                    aspect = RadixChartAspectGraphicsItem(parent=self)
                    aspect.setForPlanets(p1.getDegree(),
                                         p2.getDegree(),
                                         p1.getWheelNumber(),
                                         p2.getWheelNumber())
                    
        if self.log.isEnabledFor(logging.DEBUG) == True:
            self.log.debug("Exiting redrawAspects()")
        
    def getInnerRasiRadius(self):
        """Returns the radius of the inner Rasi circle."""
        
        return self.innerRasiRadius

    def getOuterRasiRadius(self):
        """Returns the radius of the outer Rasi circle."""

        return self.outerRasiRadius

    def getInnerNakshatraRadius(self):
        """Returns the radius of the inner Nakshatra circle."""
        
        return self.innerNakshatraRadius

    def getOuterNakshatraRadius(self):
        """Returns the radius of the outer Nakshatra circle."""

        return self.outerNakshatraRadius
    
    def getInnerNavamsaRadius(self):
        """Returns the radius of the inner Navamsa circle."""
        
        return self.innerNavamsaRadius

    def getOuterNavamsaRadius(self):
        """Returns the radius of the outer Navamsa circle."""

        return self.outerNavamsaRadius
    
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) is the center of the widget.  
        # The painting should be relative to this point as the
        # center.


        # If there are circles for where the planets are drawn (which
        # there should be), then set the radius as the last circle
        # drawn.  This is the one with the largest radius.
        radius = 0.0
        if len(self.wheelNumberCircleRadius) > 0:
            radius = self.wheelNumberCircleRadius[-1]
            
        diameter = radius + radius
        
        x = -1.0 * radius
        y = -1.0 * radius
        width = diameter
        height = diameter
        
        return QRectF(x, y, width, height)
    
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem. """

        if painter.pen() != self.pen:
            painter.setPen(self.pen)

        # Coordinate (0, 0) is the center of the widget.  
        # The painting should be relative to this point as the
        # center.

        origin = QPointF(0.0, 0.0)


        ########################################
        # Rasi

        # 30 degrees.
        angleRadians = math.pi / 6.0

        # Draw the circles for Rasi.
        painter.drawEllipse(origin, self.innerRasiRadius, self.innerRasiRadius)
        painter.drawEllipse(origin, self.outerRasiRadius, self.outerRasiRadius)

        # Draw the divisions for Rasi.
        for i in range(0, 12):
            x1 = -1.0 * math.cos(angleRadians * i) * self.innerRasiRadius
            y1 =  1.0 * math.sin(angleRadians * i) * self.innerRasiRadius
            x2 = -1.0 * math.cos(angleRadians * i) * self.outerRasiRadius
            y2 =  1.0 * math.sin(angleRadians * i) * self.outerRasiRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Rasi labels.
        for i in range(0, 12):
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.4 * angleRadians)
            
            textLocRadius = \
                ((0.5 * (self.outerRasiRadius + self.innerRasiRadius)) -
                 (0.1 * (self.outerRasiRadius - self.innerRasiRadius)))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            rotationRadians = (math.pi / 2.0) + textLocAngleRadians
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            textPath.addText(0, 0, self.rasiLabelFont, str(i+1))
            
            rotationTransform = QTransform()
            rotationTransform.translate(x, y)
            rotationTransform.rotate(-1.0 * rotationDegrees)

            rotatedTextPath = QPainterPath()
            rotatedTextPath.addPath(rotationTransform.map(textPath))

            # Change the brush to paint it, then restore the old brush.
            oldBrush = painter.brush()
            painter.setBrush(self.pen.brush())
            painter.drawPath(rotatedTextPath)
            painter.setBrush(oldBrush)

        ########################################
        # Nakshatra
        
        # 13 degrees, 20 minutes.
        angleRadians = (2.0 * math.pi) / 27.0
        
        painter.drawEllipse(origin,
                            self.innerNakshatraRadius,
                            self.innerNakshatraRadius)
        painter.drawEllipse(origin,
                            self.outerNakshatraRadius,
                            self.outerNakshatraRadius)

        # Draw the divisions for Nakshatra.
        for i in range(0, 27):
            x1 = -1.0 * math.cos(angleRadians * i) * self.innerNakshatraRadius
            y1 =  1.0 * math.sin(angleRadians * i) * self.innerNakshatraRadius
            x2 = -1.0 * math.cos(angleRadians * i) * self.outerNakshatraRadius
            y2 =  1.0 * math.sin(angleRadians * i) * self.outerNakshatraRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Nakshatra labels.
        nakshatraAbbrev = ["ASWI",
                           "BHAR",
                           "KRIT",
                           "ROHI",
                           "MRIG",
                           "ARDR",
                           "PUNA",
                           "PUSH",
                           "ASLE",
                           "MAGH",
                           "P PH",
                           "U PH",
                           "HAST",
                           "CHIT",
                           "SWAT",
                           "VISH",
                           "ANUR",
                           "JYES",
                           "MOOL",
                           "P ASH",
                           "U ASH",
                           "SRAV",
                           "DHAN",
                           "SHAT",
                           "P BH",
                           "U BH",
                           "REVA"]

        for i in range(0, 27):
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.3 * angleRadians)
            
            textLocRadius = \
                ((0.5 * (self.outerNakshatraRadius +
                         self.innerNakshatraRadius)) -
                 (0.3 * (self.outerNakshatraRadius -
                         self.innerNakshatraRadius)))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            fudgeFactor = \
                (0.01 * textLocAngleRadians)
                        
            rotationRadians = \
                (math.pi / 2.0) + \
                textLocAngleRadians - fudgeFactor
            
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            textPath.addText(0, 0, self.nakshatraLabelFont, nakshatraAbbrev[i])
            
            rotationTransform = QTransform()
            rotationTransform.translate(x, y)
            rotationTransform.rotate(-1.0 * rotationDegrees)

            rotatedTextPath = QPainterPath()
            rotatedTextPath.addPath(rotationTransform.map(textPath))

            # Change the brush to paint it, then restore the old brush.
            oldBrush = painter.brush()
            painter.setBrush(self.pen.brush())
            painter.drawPath(rotatedTextPath)
            painter.setBrush(oldBrush)
            
            
        ########################################
        # Navamsa
        
        # 13 degrees, 20 minutes.
        angleRadians = (2.0 * math.pi) / (108)
        
        painter.drawEllipse(origin,
                            self.innerNavamsaRadius,
                            self.innerNavamsaRadius)
        painter.drawEllipse(origin,
                            self.outerNavamsaRadius,
                            self.outerNavamsaRadius)

        # Draw the divisions for Navamsa.
        for i in range(0, 108):
            x1 = -1.0 * math.cos(angleRadians * i) * self.innerNavamsaRadius
            y1 =  1.0 * math.sin(angleRadians * i) * self.innerNavamsaRadius
            x2 = -1.0 * math.cos(angleRadians * i) * self.outerNavamsaRadius
            y2 =  1.0 * math.sin(angleRadians * i) * self.outerNavamsaRadius
            painter.drawLine(x1, y1, x2, y2)

        # Draw the Navamsa labels.
        for i in range(0, 108):
            rasiNumber = (i + 1) % 12
            if rasiNumber == 0:
                rasiNumber = 12
                
            textLocAngleRadians = \
                (angleRadians * (i + 1)) - (0.3 * angleRadians)
            
            textLocRadius = \
                ((0.5 * (self.outerNavamsaRadius + self.innerNavamsaRadius)) -
                 (0.3 * (self.outerNavamsaRadius - self.innerNavamsaRadius)))
            
            x = -1.0 * math.cos(textLocAngleRadians) * textLocRadius
            y =  1.0 * math.sin(textLocAngleRadians) * textLocRadius

            rotationRadians = (math.pi / 2.0) + textLocAngleRadians
            rotationDegrees = math.degrees(rotationRadians)
            
            textPath = QPainterPath()
            
            textPath.addText(0, 0, self.navamsaLabelFont, str(rasiNumber))
            
            rotationTransform = QTransform()
            rotationTransform.translate(x, y)
            rotationTransform.rotate(-1.0 * rotationDegrees)

            rotatedTextPath = QPainterPath()
            rotatedTextPath.addPath(rotationTransform.map(textPath))

            # Change the brush to paint it, then restore the old brush.
            oldBrush = painter.brush()
            painter.setBrush(self.pen.brush())
            painter.drawPath(rotatedTextPath)
            painter.setBrush(oldBrush)

        
        ########################################
            
        # Two circles for the planet locations.
        for i in range(len(self.wheelNumberCircleRadius)):
            painter.drawEllipse(origin,
                                self.wheelNumberCircleRadius[i],
                                self.wheelNumberCircleRadius[i])

class RadixPlanetGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is a 'planet' to be drawn with a
    RadixChartGraphicsItem object as its parent QGraphicsItem.
    """

    def __init__(self,
                 planetName,
                 planetGlyphUnicode,
                 planetGlyphFontSize,
                 planetAbbreviation,
                 planetForegroundColor,
                 planetBackgroundColor,
                 degree=0.0,
                 velocity=0.0,
                 wheelNumber=1,
                 parent=None,
                 scene=None):
        """Initializes the object with the given arguments.

        Arguments:
        planetName - str holding the planet name.
        planetGlyphUnicode - str holding the planet glyph.
        planetGlyphFontSize - float font size for drawing the glyph.
        planetAbbreviation - str holding the planet abbreviation.
        planetForegroundColor - QColor object for the foreground color to
                                be used for the drawing of the planet.
        planetBackgroundColor - QColor object for the background color to
                                be used for the drawing of the planet.
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        wheelNumber - int value for the wheel number to draw the planet on.
                      The first wheel (circle) is wheel number 1.
        parent - RadixChartGraphicsItem that is the parent for this
                 QGraphicsItem.
        scene - QGraphicsScene object to draw this QGraphicsItem on.
        """
    
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("astrologychart.RadixPlanetGraphicsItem")

        # Save the parameter values.
        self.planetName = planetName
        self.planetGlyphUnicode = planetGlyphUnicode
        self.planetGlyphFontSize = planetGlyphFontSize
        self.planetAbbreviation = planetAbbreviation
        self.planetForegroundColor = planetForegroundColor
        self.planetBackgroundColor = planetBackgroundColor
        self.degree = degree
        self.velocity = velocity
        self.wheelNumber = wheelNumber
        self.radixChartGraphicsItem = parent

        # Get the retrograde symbol.
        # (Below is commented out because we're using parenthesis instead).
        #settings = QSettings()
        #self.planetRetrogradeGlyphUnicode = \
        #    settings.value(SettingsKeys.planetRetrogradeGlyphUnicodeKey,
        #                   SettingsKeys.planetRetrogradeGlyphUnicodeDefValue,
        #                   type=str)
        #self.planetRetrogradeGlyphFontSize = \
        #    settings.value(SettingsKeys.planetRetrogradeGlyphFontSizeKey,
        #                   SettingsKeys.planetRetrogradeGlyphFontSizeDefValue,
        #                   type=float)
        
        # Radius from the origin to draw this planet.
        self.drawPointRadius = 0.0
        self.drawPointTerminalRadius = 0.0

        # Call our overwritten self.setParentItem() manually so that
        # the parent object type can be verified.  This will also
        # subsequently have the (desired) side effect of
        # re-calculating the radisuses above.
        self.setParentItem(parent)

        
    def setParentItem(self, parent):
        """Overwrites QGraphicsItem.setParentItem().  Needed so we can
        save off the parent in self.radixChartGraphicsItem.

        Arguments:
        parent - RadixChartGraphicsItem parent object.
        """

        # Verify parent class.
        if parent != None and not isinstance(parent, RadixChartGraphicsItem):
            raise TypeError("Argument 'parent' is not of type " + \
                            "'RadixChartGraphicsItem'")
        
        # Save off the parent.
        self.radixChartGraphicsItem = parent

        # Call self.setWheelNumber() again so the radiuses can be recalculated.
        self.setWheelNumber(self.wheelNumber)
        
    def setDegree(self, degree):
        """Sets the location of the planet in degrees of the zodiac.

        Arguments:
        
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        """

        self.degree = degree
        self.update()
        
    def getDegree(self):
        """Returns the location of the planet in degrees of the zodiac.

        Returns:
        float - Value representing the degree location of the planet.
                The value returned will be between: [0.0, 360).
        """

        return self.degree

    def setVelocity(self, velocity):
        """Sets the velocity of the planet, in degrees per day.

        Arguments:
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.velocity = velocity
        self.update()

    def getVelocity(self):
        """Returns the velocity of the planet, in degrees per day.

        Returns:
        float - Value for the velocity of the planet, in degrees
                per day.
        """

        return self.velocity

    def setDegreeAndVelocity(self, degree, velocity):
        """Sets the degree location of the planet and the velocity of
        the planet, all at once.

        Arguments:
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.degree = degree
        self.velocity = velocity

        self.update()
        
    def setWheelNumber(self, wheelNumber):
        """Sets the wheel number that it will be drawn on.
        This value represents which 'circle' to use on
        RadixChartGraphicsItem for drawing the planet.
        The first wheel (circle) is wheel number 0.
        
        Arguments:
        wheelNumber - int value for the wheel number to draw the planet on.
                      The first wheel (circle) is wheel number 0.
        """

        self.wheelNumber = wheelNumber

        # Update the radius location point if we have a parent radix chart set.
        if self.radixChartGraphicsItem != None:
            drawPointRadius = \
                self.radixChartGraphicsItem.\
                getRadiusForWheelNumber(self.wheelNumber)
            drawPointTerminalRadius = \
                self.radixChartGraphicsItem.\
                getTerminalRadiusForWheelNumber(self.wheelNumber)

            # Update variables only if new values are different.
            if self.drawPointRadius != drawPointRadius or \
               self.drawPointTerminalRadius != drawPointTerminalRadius:
                
                self.drawPointRadius = drawPointRadius
                self.drawPointTerminalRadius = drawPointTerminalRadius
                
                self.update()

    def getWheelNumber(self):
        """Returns the wheel number that the planet is drawn on.
        This value represents which 'circle' to use on
        RadixChartGraphicsItem for drawing the planet.
        The first wheel (circle) is wheel number 0.

        Returns:
        int - Value representing which wheel number the planet is drawn on.
              A value of 0 indicates the first wheel from the center.
        """

        return self.wheelNumber

    def getPlanetName(self):
        """Returns the planet name."""
        
        return self.planetName
    
    def getPlanetGlyphUnicode(self):
        """Returns the planet glyph in unicode."""

        return self.planetGlyphUnicode

    def getPlanetGlyphFontSize(self):
        """Returns the planet glyph font size."""

        return self.planetGlyphFontSize

    def getPlanetAbbreviation(self):
        """Returns the planet abbreviation."""

        return self.planetAbbreviation

    def getPlanetForegroundColor(self):
        """Returns the planet foreground color as a QColor object."""

        return self.planetForegroundColor

    def getPlanetBackgroundColor(self):
        """Returns the planet background color as a QColor object."""

        return self.planetBackgroundColor

    def __str__(self):
        """Returns a str representing this object's contents."""

        return self.toString()
        
    def toString(self):
        """Returns a str representing this object's contents."""

        return Util.objToString(self)
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem.

        We implement this function by taking all the pieces, and doing
        an logical OR on the areas covered by their rectangles.  The
        rectangles are calculated in the same way that paint() is
        done.  Changes to paint() will required changes to this
        method.
        """

        # QRectF for the line.
        x1 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointRadius
        y1 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointRadius
        x2 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointTerminalRadius
        y2 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointTerminalRadius
        lineRect = QRectF(QPointF(x1, y1), QPointF(x2, y2)).normalized()

        # QRectF for the planet glyph text.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)
        text = self.planetGlyphUnicode
        if self.velocity < 0:
            text = "(" + self.planetGlyphUnicode + ")"
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        rotationTransform = QTransform()
        fudgeDegrees = 0.5
        rotationDegrees = self.degree + fudgeDegrees
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - ((r - self.drawPointRadius) / 3.0)
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))

        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))
        planetTextRect = rotatedTextPath.boundingRect()

        # QRectF for the planet degree location text.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)
        # Normalize degree value.
        degreesInSign = self.degree
        while degreesInSign < 0:
            degreesInSign += 360.0
        while degreesInSign >= 360.0:
            degreesInSign -= 360.0
        # Get integer values of degrees and minutes.
        minutesInDegree = \
            int((degreesInSign - math.floor(degreesInSign)) * 60.0)
        degreesInSign = int(math.floor(degreesInSign))
        # Text.
        text = "{}\u00b0{}'".format(degreesInSign, minutesInDegree)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        rotationTransform = QTransform()
        fudgeDegrees = 1.0
        rotationDegrees = self.degree + fudgeDegrees
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - (2.0 * (r - self.drawPointRadius) / 3.0)
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))
        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))
        planetDegreeTextRect = rotatedTextPath.boundingRect()
        

        # Unite all rectangles.
        rv = lineRect.united(planetTextRect).united(planetDegreeTextRect)
        
        return rv

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.
        
        The painting is done in three parts:
        - Paint the line from the text to the terminal point.
        - Paint the planet glyph as text.
        - Paint the degree location as text.

        Note: boundingRect() utilizes the same calculations as here,
        so if this function changes, then boundingRect() will need to
        be updated as well.
        """

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(self.planetForegroundColor))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(self.planetForegroundColor)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw the line.
        x1 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointRadius
        y1 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointRadius

        x2 = -1.0 * math.cos(math.radians(self.degree)) * \
             self.drawPointTerminalRadius
        y2 =  1.0 * math.sin(math.radians(self.degree)) * \
             self.drawPointTerminalRadius

        painter.drawLine(x1, y1, x2, y2)

        # Draw the text for the planet.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)

        text = self.planetGlyphUnicode
        if self.velocity < 0:
            text = "(" + self.planetGlyphUnicode + ")"
            
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        
        rotationTransform = QTransform()
        fudgeDegrees = 0.5
        rotationDegrees = self.degree + fudgeDegrees
        
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - ((r - self.drawPointRadius) / 3.0)
        
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))

        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))

        painter.drawPath(rotatedTextPath)


        # Draw the text for the degrees of the sign the planet is in.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)

        # Normalize degree value.
        degreesInSign = self.degree
        while degreesInSign < 0:
            degreesInSign += 360.0
        while degreesInSign >= 360.0:
            degreesInSign -= 360.0

        # Get integer values of degrees and minutes.
        minutesInDegree = \
            int((degreesInSign - math.floor(degreesInSign)) * 60.0)
        degreesInSign = int(math.floor(degreesInSign))

        # Text.
        text = "{}\u00b0{}'".format(degreesInSign, minutesInDegree)
        
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        
        rotationTransform = QTransform()
        fudgeDegrees = 1.0
        rotationDegrees = self.degree + fudgeDegrees
        
        r = self.radixChartGraphicsItem.\
            getRadiusForWheelNumber(self.wheelNumber + 1)
        planetTextRadius = r - (2.0 * (r - self.drawPointRadius) / 3.0)
        
        textX = -1.0 * math.cos(math.radians(rotationDegrees)) * \
                planetTextRadius
        textY = 1.0 * math.sin(math.radians(rotationDegrees)) * \
                planetTextRadius
        rotationTransform.translate(textX, textY)
        rotationTransform.rotate(-1.0 * (self.degree + 90))

        rotatedTextPath = QPainterPath()
        rotatedTextPath.addPath(rotationTransform.map(textPath))

        painter.drawPath(rotatedTextPath)

        # Uncomment the below few lines of code to paint the boundingRect().
        # This is here just for future testing purposes.
        #painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        #painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.boundingRect())
        
        # Restore the old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)
        
class DeclinationChartGraphicsItem(QGraphicsItem):
    """QGraphicsItem that paints a chart for displaying various
    planets' declination.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("astrologychart.DeclinationGraphicsItem")

        self.rulerWidth = 40.0
        self.rulerHeight = 600.0

        # These are on the verical axis.  Ruler height must be evenly
        # divisible by these tick size numbers below.
        self.bigTickSize = 50.0
        self.smallTickSize = 10.0

        # Value used in getXLocationForPlanetGroupNumber().
        self.planetLineLength = self.rulerWidth
        
    def getPlanetDeclinationGraphicsItem(self, planetName, groupNum):
        """Returns the PlanetDeclinationGraphicsItem with the given
        planet name and group number.  If no match is found, None is
        returned.

        Arguments:
        
        planetName - str value holding the planet name as set in the
        RadixPlanetGraphicsItem.
        
        groupNum - int value holding the planet group number as set in the
        RadixPlanetGraphicsItem.
        """

        # Get the child GraphicsItems.
        children = self.childItems()
        
        # Go through them and look at the ones that are
        # PlanetDeclinationGraphicsItem.
        for child in children:
            if isinstance(child, PlanetDeclinationGraphicsItem):
                # If the planet name matches then return that
                # QGraphicsItem.
                if child.getPlanetName() == planetName and \
                    child.getPlanetGroupNumber() == groupNum:
                    
                    return child

        return None

    def getXLocationForPlanetGroupNumber(self, planetGroupNumber):
        """Returns the X location away from the origin for
        the location that the child items should draw their planets'
        QGraphicsItems.

        Arguments:
        planetGroupNumber - int value which is an index representing
                            the set of planets that having their
                            declination charted.  This index
                            value is 1-based, so 1 is the first set
                            of planets drawn to the right of the ruler.

        Returns:
        float - Width for where to start drawing the text for a planet.
        """

        x = self.planetLineLength + \
            (planetGroupNumber-1) * (2.0 * self.planetLineLength)

        return x

    
    def convertYValueToDegree(self, y):
        """Converts a tick Y value to it's equivalent in degrees.

        Arguments:
        y - float value for the Y coordinate value.

        Returns
        float - value for the degrees that this Y value represents..
        """

        # Our algorithm for conversion is to drop an order of magnitude.
        return (y / -10.0)
        
    def convertDegreeToYValue(self, degree):
        """Converts a degree value it's equivalent Y value in coordinates.

        Arguments:
        degree - float value for the degree the planet is at.

        Returns
        float - value for the Y coordinate location for the given degree.
        """

        # Our algorithm for conversion is the following.
        return degree * -10.0
        
    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem."""

        # Coordinate (0, 0) is the location where the zero-tick
        # intersects the right side of the ruler.  The painting should
        # be relative to this point as the center.

        x = -1.0 * self.rulerWidth
        y = -1.0 * self.rulerHeight / 2.0
        rectF = QRectF(x, y, self.rulerWidth, self.rulerHeight)

        return rectF
    
    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem. """

        # Coordinate (0, 0) is the location where the zero-tick
        # intersects the right side of the ruler.  The painting should
        # be relative to this point as the center.

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(Qt.black))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(QColor(Qt.black))
        painter.setBrush(brush)

        # Draw the rectangle for the ruler.
        rectF = self.boundingRect()
        painter.drawRect(rectF)

        # Now that the rectangle is drawn.  Everything can have a
        # solid pattern for its brush because we don't paint anything
        # else we don't want filled in.
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        
        # Draw small ticks.
        start = int(-1.0 * self.rulerHeight / 2.0)
        stop = int(self.rulerHeight / 2.0)
        step = int(self.smallTickSize)
        smallTickWidth = self.rulerWidth / 6.0
        for tick in range(start, stop, step):
            # Draw the tick line.
            x1 = -1.0 * smallTickWidth
            y1 = -1.0 * tick
            x2 = 0
            y2 = -1.0 * tick
            painter.drawLine(x1, y1, x2, y2)

        # Draw big ticks
        start = int(-1.0 * self.rulerHeight / 2.0)
        stop = int(self.rulerHeight / 2.0)
        step = int(self.bigTickSize)
        bigTickWidth = self.rulerWidth / 3.0
        for tick in range(start, stop, step):
            # Draw the tick line.
            x1 = -1.0 * bigTickWidth
            y1 = -1.0 * tick
            x2 = -1.0 * smallTickWidth
            y2 = -1.0 * tick
            painter.drawLine(x1, y1, x2, y2)

            # Draw the text for the ticks.
            font = QFont()
            font.setFamily("Lucida Console")
            font.setPointSize(10)
            
            x1 = -1.0 * self.rulerWidth
            y1 = -1.0 * tick
            converted = math.floor(-1 * self.convertYValueToDegree(float(tick)))
            text = "{}\u00b0".format(converted)
            textPath = QPainterPath()
            textPath.addText(0, 0, font, text)
            
            transform = QTransform()
            transform.translate(x1, y1)
            
            translatedPath = QPainterPath()
            translatedPath.addPath(transform.map(textPath))
            
            painter.drawPath(translatedPath)
            
        # Restore old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)
    
class PlanetDeclinationGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is a 'planet' to be drawn with a
    DeclinationChartGraphicsItem object as its parent QGraphicsItem.
    """

    def __init__(self,
                 planetName,
                 planetGlyphUnicode,
                 planetGlyphFontSize,
                 planetAbbreviation,
                 planetForegroundColor,
                 planetBackgroundColor,
                 degree=0.0,
                 velocity=0.0,
                 planetGroupNumber=1,
                 parent=None,
                 scene=None):
        """Initializes the object with the given arguments.

        Arguments:
        planetName - str holding the name of the planet.
        planetGlyphUnicode - str holding the planet glyph.
        planetGlyphFontSize - float font size for drawing the glyph.
        planetAbbreviation - str holding the planet abbreviation.
        planetForegroundColor - QColor object for the foreground color to
                                be used for the drawing of the planet.
        planetBackgroundColor - QColor object for the background color to
                                be used for the drawing of the planet.
        degree - float value for the latitude degree location for where this
                 planet will be drawn.  If the value is not
                 in the range [-180.0, 180), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        planetGroupNumber - int value for the group of planets that this
                            planet belongs to.  This is so planets of
                            the same group (timestamp) can be drawn together.
                            The first group is at number 1.
        parent - DeclinationChartGraphicsItem that is the parent for this
                 QGraphicsItem.
        scene - QGraphicsScene object to draw this QGraphicsItem on.
        """
        
        super().__init__(parent, scene)
        
        # Logger
        self.log = \
            logging.getLogger("astrologychart.PlanetDeclinationGraphicsItem")

        # Save the parameter values.
        self.planetName = planetName
        self.planetGlyphUnicode = planetGlyphUnicode
        self.planetGlyphFontSize = planetGlyphFontSize
        self.planetAbbreviation = planetAbbreviation
        self.planetForegroundColor = planetForegroundColor
        self.planetBackgroundColor = planetBackgroundColor
        self.degree = degree
        self.velocity = velocity
        self.planetGroupNumber = planetGroupNumber
        self.parentChartGraphicsItem = parent

        # Location where the line ends and the text begins.  This
        # value is obtained from the parent
        # DeclinationChartGraphicsItem object.
        self.lineEndX = 0.0

        # Call our overwritten self.setParentItem() manually so that
        # the parent object type can be verified.  This will also
        # subsequently have the (desired) side effect of
        # re-calculating self.lineEndX and updating the QGraphicsItem.
        self.setParentItem(parent)

        
    def setParentItem(self, parent):
        """Overwrites QGraphicsItem.setParentItem().  Needed so we can
        save off the parent in self.parentChartGraphicsItem.

        Arguments:
        parent -  DeclinationChartGraphicsItem parent object.
        """

        # Verify parent class.
        if parent != None and \
               not isinstance(parent, DeclinationChartGraphicsItem):
            
            raise TypeError("Argument 'parent' is not of type " + \
                            "'DeclinationChartGraphicsItem'")
        
        # Save off the parent.
        self.parentChartGraphicsItem = parent

        # Call self.setPlanetGroupNumber() again so the drawn points
        # can be recalculated.
        self.setPlanetGroupNumber(self.planetGroupNumber)
        
    def setDegree(self, degree):
        """Sets the location of the planet in degrees of the zodiac.

        Arguments:
        
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        """

        self.degree = degree
        self.update()
        
    def getDegree(self):
        """Returns the location of the planet in degrees of the zodiac.

        Returns:
        float - Value representing the degree location of the planet.
                The value returned will be between: [0.0, 360).
        """

        return self.degree

    def setVelocity(self, velocity):
        """Sets the velocity of the planet, in degrees per day.

        Arguments:
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.velocity = velocity
        self.update()

    def getVelocity(self):
        """Returns the velocity of the planet, in degrees per day.

        Returns:
        float - Value for the velocity of the planet, in degrees
                per day.
        """

        return self.velocity

    def setDegreeAndVelocity(self, degree, velocity):
        """Sets the degree location of the planet and the velocity of
        the planet, all at once.

        Arguments:
        degree - float value for the degree location for where this
                 planet will be drawn on the zodiac.  If the value is not
                 in the range [0.0, 360), it will be normalized so that it
                 is in that range before drawing.
        velocity - float value for the velocity of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.degree = degree
        self.velocity = velocity

        self.update()
        
    def setPlanetGroupNumber(self, planetGroupNumber):
        """Sets the planet group number that this QGraphicsItem is
        associated with.  The first group is number 1.
        
        Arguments:
        planetGroupNumber - int value for the group of planets that this
                            planet belongs to.  This is so planets of
                            the same group (timestamp) can be drawn together.
                            The first group is at number 1.
        """

        self.planetGroupNumber = planetGroupNumber


        # Update the self.lineEndX location point if we have a parent
        # chart set.
        if self.parentChartGraphicsItem != None:

            lineEndX = \
                self.parentChartGraphicsItem.\
                getXLocationForPlanetGroupNumber(self.planetGroupNumber)

            # Update variable only if the new value is different.
            if self.lineEndX != lineEndX:
                self.lineEndX = lineEndX
                self.update()

    def getPlanetGroupNumber(self):
        """Returns the planet group number that this planet is drawn
        on.  This value represents which group of planets that the
        planet is associated with when drawn on the chart.  The first
        planet group is number 1.

        Returns:

        int - Value representing which planet group number the planet
              is drawn on.  A value of 1 indicates the first group on
              the right of the ruler.
        """

        return self.planetGroupNumber

    def getPlanetName(self):
        """Returns the planet name."""

        return self.planetName

    def getPlanetGlyphUnicode(self):
        """Returns the planet glyph in unicode."""

        return self.planetGlyphUnicode

    def getPlanetGlyphFontSize(self):
        """Returns the planet glyph font size."""

        return self.planetGlyphFontSize

    def getPlanetAbbreviation(self):
        """Returns the planet abbreviation."""

        return self.planetAbbreviation

    def getPlanetForegroundColor(self):
        """Returns the planet foreground color as a QColor object."""

        return self.planetForegroundColor

    def getPlanetBackgroundColor(self):
        """Returns the planet background color as a QColor object."""

        return self.planetBackgroundColor

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem.

        We implement this function by taking all the pieces, and doing
        an logical OR on the areas covered by their rectangles.  The
        rectangles are calculated in the same way that paint() is
        done.  Changes to paint() will required changes to this
        method.
        """

        # QRectF for the line.
        x1 = 0.0
        y1 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        x2 = self.lineEndX
        y2 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        lineRect = QRectF(QPointF(x1, y1), QPointF(x2, y2)).normalized()

        # QRectF for text of the planet glyph and degree.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)
        text = self.planetGlyphUnicode
        text += " {:.3f}\u00b0".format(self.degree)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        textX = self.lineEndX
        textY = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        transform.translate(textX, textY)
        transformedTextPath = QPainterPath()
        transformedTextPath.addPath(transform.map(textPath))
        textRect = transformedTextPath.boundingRect()

        # Unite all rectangles.
        rv = lineRect.united(textRect)
        
        return rv

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.
        
        The painting is done in the following parts:
        - Paint the line from ruler to the location where the text starts.
        - Paint the text for the planet glyph and the degree it is at.

        Note: boundingRect() utilizes the same calculations as here,
        so if this function changes, then boundingRect() will need to
        be updated as well.
        """

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(self.planetForegroundColor))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(self.planetForegroundColor)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw the line.
        x1 = 0.0
        y1 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        x2 = self.lineEndX
        y2 = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        painter.drawLine(x1, y1, x2, y2)

        # Draw the text for the planet.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)

        text = self.planetGlyphUnicode
        text += " {:.3f}\u00b0".format(self.degree)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        
        transform = QTransform()
        textX = self.lineEndX
        textY = self.parentChartGraphicsItem.convertDegreeToYValue(self.degree)
        transform.translate(textX, textY)
        transformedTextPath = QPainterPath()
        transformedTextPath.addPath(transform.map(textPath))
        painter.drawPath(transformedTextPath)

        # Uncomment the below few lines of code to paint the boundingRect().
        # This is here just for future testing purposes.
        #painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        #painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.boundingRect())
        
        # Restore the old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)
        
class LongitudeSpeedChartGraphicsItem(QGraphicsItem):
    """QGraphicsItem that paints a chart for displaying various
    planets' longitude speed.
    """

    def __init__(self, maxSpeed=None, minSpeed=None, parent=None, scene=None):
        """Initializes the LongitudeSpeedChartGraphicsItem with the
        given max and minimum speeds.

        Arguments:
        maxSpeed - float value for the maximum longitude speed in
                   degrees per day.
        minSpeed - float value for the minimum longitude speed in
                   degrees per day.
        """
        
        super().__init__(parent, scene)
        
        # Logger
        self.log = \
            logging.getLogger("astrologychart.LongitudeSpeedChartGraphicsItem")

        # Save off values.
        self.maxSpeed=maxSpeed
        self.minSpeed=minSpeed

        # The 'ruler' bar displayed is a fixed size.  Speed values are
        # scaled to a Y value to fit in the ruler bar.  See the
        # convertFromSpeedToYLocation() function for the conversion
        # algorithm sed.
        self.rulerWidth = 20.0
        self.rulerHeight = 120.0

        # This is the X coordinate location where the text for the
        # min, max and 0 speed are painted.
        self.textXLoc = -35.0
        
    def getRulerWidth(self):
        """Returns the ruler width."""

        return self.rulerWidth

    def getRulerHeight(self):
        """Returns the ruler height."""

        return self.rulerHeight
        
    def setMaxSpeed(self, maxSpeed):
        """Sets the max longitude speed, in degrees per day.

        Arguments:
        maxSpeed - float value for the max longitude speed, in degrees per day.
        """

        self.maxSpeed = maxSpeed

    def getMaxSpeed(self):
        """Returns the max longitude speed, in degrees per day.

        Returns:
        float - Value that is the max longitude speed, in degrees per day.
        """

        return self.maxSpeed
    
    def setMinSpeed(self, minSpeed):
        """Sets the min longitude speed, in degrees per day.

        Arguments:
        minSpeed - float value for the min longitude speed, in degrees per day.
        """

        self.minSpeed = minSpeed

    def getMinSpeed(self):
        """Returns the min longitude speed, in degrees per day.

        Returns:
        float - Value that is the min longitude speed, in degrees per day.
        """

        return self.minSpeed
    
        
    def convertFromSpeedToYValue(self, speed):
        """Converts the given longitude speed (in degrees per day) to
        the coordinate Y value where speed should be plotted.  This
        algorithm sets the minSpeed Y value as the 0 anchor point,
        therefore all coordinates within range should yield a value
        less than or equal to 0.

        Arguments:
        speed - float value for the longitude speed.

        Returns:
        float - value that is the Y coordinate location where the speed
                should be plotted.
        """

        # These local variables hold the min and max speeds used in
        # the calculation.
        maxSpeed = self.maxSpeed
        minSpeed = self.minSpeed
        
        # If self.maxSpeed or self.minSpeed is None, then default to
        # using the range as the ruler height, and the max and min as
        # positive and negative half the ruler height.
        if self.maxSpeed == None or self.minSpeed == None:
            maxSpeed =  1.0 * self.rulerHeight / 2.0
            minSpeed = -1.0 * self.rulerHeight / 2.0

        # See where speed fits in terms of range.
        speedRange = maxSpeed - minSpeed
        amountAboveMinSpeed = speed - minSpeed

        ratio = amountAboveMinSpeed / speedRange
        
        yValue = -1.0 * self.rulerHeight * ratio

        return yValue

    def convertFromYValueToSpeed(self, y):
        """Converts the given y value to a longitude speed (in degrees per day).
        This method does the inverse of convertFromSpeedToYValue().

        Arguments:
        y - float value that is the Y coordinate location where the speed
            is plotted.

        Returns:
        float - value that is the longitude speed, in degrees per day.
        """

        # These local variables hold the min and max speeds used in
        # the calculation.
        maxSpeed = self.maxSpeed
        minSpeed = self.minSpeed
        
        # If self.maxSpeed or self.minSpeed is None, then default to
        # using the range as the ruler height, and the max and min as
        # positive and negative half the ruler height.
        if self.maxSpeed == None or self.minSpeed == None:
            maxSpeed =  1.0 * self.rulerHeight / 2.0
            minSpeed = -1.0 * self.rulerHeight / 2.0


        ratio = y / self.rulerHeight

        speedRange = maxSpeed - minSpeed
        amountAboveMinSpeed = ratio * speedRange
        speed = minSpeed + amountAboveMinSpeed
        
        return speed

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem.
        
        We implement this function by taking all the pieces, and doing
        an logical OR on the areas covered by their rectangles.  The
        rectangles are calculated in the same way that paint() is
        done.  Changes to paint() will required changes to this
        method.
        """

        # Coordinate (0, 0) is the location of the bottom left corner
        # of the ruler.

        # These local variables hold the min and max speeds used in
        # the calculation.
        maxSpeed = self.maxSpeed
        minSpeed = self.minSpeed
        
        # If self.maxSpeed or self.minSpeed is None, then default to
        # using the range as the ruler height, and the max and min as
        # positive and negative half the ruler height.
        if self.maxSpeed == None or self.minSpeed == None:
            maxSpeed =  1.0 * self.rulerHeight / 2.0
            minSpeed = -1.0 * self.rulerHeight / 2.0

        # Rectangle for the ruler.
        x = 0
        y = 0
        width = self.rulerWidth
        height = -1.0 * self.rulerHeight
        rulerRectF = QRectF(x, y, width, height).normalized()

        # For the text for the min, max, and 0 locations on the ruler.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(10)
        
        # Max speed.
        x1 = self.textXLoc
        y1 = self.convertFromSpeedToYValue(maxSpeed)
        # The below format is:
        # - Two digits of precision.
        # - Followed by the degree symbol.
        text = "{:.2f}\u00b0".format(maxSpeed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        transform.translate(x1, y1)
        translatedPath = QPainterPath()
        translatedPath.addPath(transform.map(textPath))
        maxSpeedRectF = translatedPath.boundingRect()
        
        # Min speed.
        x1 = self.textXLoc
        y1 = self.convertFromSpeedToYValue(minSpeed)
        # The below format is:
        # - Two digits of precision.
        # - Followed by the degree symbol.
        text = "{:.2f}\u00b0".format(minSpeed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        transform.translate(x1, y1)
        translatedPath = QPainterPath()
        translatedPath.addPath(transform.map(textPath))
        minSpeedRectF = translatedPath.boundingRect()

        # Zero speed.
        zeroSpeed = 0.0
        x1 = self.textXLoc
        y1 = self.convertFromSpeedToYValue(zeroSpeed)
        # The below format is:
        # - Two digits of precision.
        # - Followed by the degree symbol.
        text = "{:.2f}\u00b0".format(zeroSpeed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        transform.translate(x1, y1)
        translatedPath = QPainterPath()
        translatedPath.addPath(transform.map(textPath))
        zeroSpeedRectF = translatedPath.boundingRect()

        rv = rulerRectF.\
             united(maxSpeedRectF).\
             united(minSpeedRectF).\
             united(zeroSpeedRectF)
        
        return rv

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.

        Note: boundingRect() utilizes the same calculations as here,
        so if this function changes, then boundingRect() will need to
        be updated as well.
        """
        
        # Coordinate (0, 0) is the location of the bottom left corner
        # of the ruler.

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(Qt.black))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(QColor(Qt.black))
        painter.setBrush(brush)

        # These local variables hold the min and max speeds used in
        # the calculation.
        maxSpeed = self.maxSpeed
        minSpeed = self.minSpeed
        
        # If self.maxSpeed or self.minSpeed is None, then default to
        # using the range as the ruler height, and the max and min as
        # positive and negative half the ruler height.
        if self.maxSpeed == None or self.minSpeed == None:
            maxSpeed =  1.0 * self.rulerHeight / 2.0
            minSpeed = -1.0 * self.rulerHeight / 2.0

        # Draw the rectangle for the ruler.
        x = 0
        y = 0
        width = self.rulerWidth
        height = -1.0 * self.rulerHeight
        rectF = QRectF(x, y, width, height).normalized()
        painter.drawRect(rectF)

        # Draw the 0 line.
        x1 = 0
        y1 = self.convertFromSpeedToYValue(0)
        x2 = self.rulerWidth
        y2 = y1
        painter.drawLine(x1, y1, x2, y2)
        
        # Draw the text for the min, max, and 0 locations on the ruler.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(10)

        # Max speed.
        x1 = self.textXLoc
        y1 = self.convertFromSpeedToYValue(maxSpeed)
        # The below format is:
        # - Two digits of precision.
        # - Followed by the degree symbol.
        text = "{:.2f}\u00b0".format(maxSpeed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        transform.translate(x1, y1)
        translatedPath = QPainterPath()
        translatedPath.addPath(transform.map(textPath))
        painter.drawPath(translatedPath)

        # Min speed.
        x1 = self.textXLoc
        y1 = self.convertFromSpeedToYValue(minSpeed)
        # The below format is:
        # - Two digits of precision.
        # - Followed by the degree symbol.
        text = "{:.2f}\u00b0".format(minSpeed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        transform.translate(x1, y1)
        translatedPath = QPainterPath()
        translatedPath.addPath(transform.map(textPath))
        painter.drawPath(translatedPath)
        
        # Zero speed.
        zeroSpeed = 0.0
        x1 = self.textXLoc
        y1 = self.convertFromSpeedToYValue(zeroSpeed)
        # The below format is:
        # - Two digits of precision.
        # - Followed by the degree symbol.
        text = "{:.2f}\u00b0".format(zeroSpeed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        transform.translate(x1, y1)
        translatedPath = QPainterPath()
        translatedPath.addPath(transform.map(textPath))
        painter.drawPath(translatedPath)

        # Uncomment the below few lines of code to paint the boundingRect().
        # This is here just for future testing purposes.
        #painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        #painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.boundingRect())
        
        # Restore old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)
        
class PlanetLongitudeSpeedGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is a 'planet' to be drawn with a
    LongitudeSpeedChartGraphicsItem object as its parent QGraphicsItem.
    """

    def __init__(self,
                 planetGlyphUnicode,
                 planetGlyphFontSize,
                 planetAbbreviation,
                 planetForegroundColor,
                 planetBackgroundColor,
                 speed = 0.0,
                 parent=None,
                 scene=None):
        """Initializes the object with the given arguments.

        Arguments:
        planetGlyphUnicode - str holding the planet glyph.
        planetGlyphFontSize - float font size for drawing the glyph.
        planetAbbreviation - str holding the planet abbreviation.
        planetForegroundColor - QColor object for the foreground color to
                                be used for the drawing of the planet.
        planetBackgroundColor - QColor object for the background color to
                                be used for the drawing of the planet.
        speed - float value for the longitude velocity of the planet,
                in degrees per day.  Negative values indicate
                that the planet is retrograde (if applicable).
        parent - LongitudeSpeedChartGraphicsItem that is the parent for this
                 QGraphicsItem.
        scene - QGraphicsScene object to draw this QGraphicsItem on.
        """
        
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("astrologychart.PlanetLongitudeSpeedGraphicsItem")

        # Save the parameter values.
        self.planetGlyphUnicode = planetGlyphUnicode
        self.planetGlyphFontSize = planetGlyphFontSize
        self.planetAbbreviation = planetAbbreviation
        self.planetForegroundColor = planetForegroundColor
        self.planetBackgroundColor = planetBackgroundColor
        self.speed = speed
        self.parentChartGraphicsItem = parent

        # Fill colors for the ruler area for positive and negative speeds.
        self.positiveSpeedBrush = QBrush(Qt.green, Qt.Dense4Pattern)
        self.negativeSpeedBrush = QBrush(Qt.red, Qt.Dense4Pattern)
        
        # The ruler width.  This value is obtained from the parent
        # LongitudeSpeedChartGraphicsItem object.
        self.rulerWidth = 0.0

        # X location where the line ends and the text starts.
        # This value is updated every time self.rulerWidth is updated.
        self.lineEndX = 0.0

        # Call our overwritten self.setParentItem() manually so that
        # the parent object type can be verified.  This will also
        # subsequently have the (desired) side effect of
        # setting self.rulerWidth and updating the QGraphicsItem.
        self.setParentItem(parent)
        
    def setParentItem(self, parent):
        """Overwrites QGraphicsItem.setParentItem().  Needed so we can
        save off the parent in self.parentChartGraphicsItem.

        Arguments:
        parent -  LongitudeSpeedChartGraphicsItem parent object.
        """

        # Verify parent class.
        if parent != None and \
               not isinstance(parent, LongitudeSpeedChartGraphicsItem):
            
            raise TypeError("Argument 'parent' is not of type " + \
                            "'LongitudeSpeedChartGraphicsItem'")
        
        # Save off the parent.
        self.parentChartGraphicsItem = parent

        # Get values from the parent that we use for drawing.
        self.rulerWidth = self.parentChartGraphicsItem.getRulerWidth()
        self.lineEndX = 1.5 * self.rulerWidth
        self.update()
        
    def setSpeed(self, speed):
        """Sets the speed of the planet, in degrees per day.

        Arguments:
        speed - float value for the speed of the planet, in degrees
                   per day.  Negative values indicate that the planet
                   is retrograde (if applicable).
        """

        self.speed = speed
        self.update()

    def getSpeed(self):
        """Returns the speed of the planet, in degrees per day.

        Returns:
        float - Value for the speed of the planet, in degrees
                per day.
        """

        return self.speed

    def getPlanetGlyphUnicode(self):
        """Returns the planet glyph in unicode."""

        return self.planetGlyphUnicode

    def getPlanetGlyphFontSize(self):
        """Returns the planet glyph font size."""

        return self.planetGlyphFontSize

    def getPlanetAbbreviation(self):
        """Returns the planet abbreviation."""

        return self.planetAbbreviation

    def getPlanetForegroundColor(self):
        """Returns the planet foreground color as a QColor object."""

        return self.planetForegroundColor

    def getPlanetBackgroundColor(self):
        """Returns the planet background color as a QColor object."""

        return self.planetBackgroundColor

    def boundingRect(self):
        """Returns the bounding rectangle for this graphicsitem.

        We implement this function by taking all the pieces, and doing
        an logical OR on the areas covered by their rectangles.  The
        rectangles are calculated in the same way that paint() is
        done.  Changes to paint() will required changes to this
        method.
        """

        # QRectF for the line.
        x1 = 0.0
        y1 = self.parentChartGraphicsItem.convertFromSpeedToYValue(self.speed)
        x2 = self.lineEndX
        y2 = y1
        lineRect = QRectF(QPointF(x1, y1), QPointF(x2, y2)).normalized()

        # QRectF for text of the planet glyph and degree.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)
        text = self.planetGlyphUnicode
        text += "  {}\u00b0/day".format(self.speed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        transform = QTransform()
        textX = self.lineEndX
        textY = self.parentChartGraphicsItem.\
                convertFromSpeedToYValue(self.speed)
        transform.translate(textX, textY)
        transformedTextPath = QPainterPath()
        transformedTextPath.addPath(transform.map(textPath))
        textRect = transformedTextPath.boundingRect()

        # QRectF for the fill area.
        rulerFillAreaRectF = \
            QRectF(QPointF(0.0,
                           self.parentChartGraphicsItem.\
                           convertFromSpeedToYValue(0.0)),
                   QPointF(self.rulerWidth,
                           self.parentChartGraphicsItem.\
                           convertFromSpeedToYValue(self.speed))).normalized()

        # Unite all rectangles.
        rv = lineRect.united(textRect).united(rulerFillAreaRectF)
        
        return rv

    def paint(self, painter, option, widget):
        """Paints this QGraphicsItem.
        
        The painting is done in the following parts:
        - Paint the line from ruler to the location where the text starts.
        - Paint the text for the planet glyph and the degree it is at.
        - Paint the fill-area of the ruler.

        Note: boundingRect() utilizes the same calculations as here,
        so if this function changes, then boundingRect() will need to
        be updated as well.
        """

        # Change the brush and pen in the painter.
        # We will restore it when done.
        oldBrush = painter.brush()
        oldPen = painter.pen()
        pen = painter.pen()
        pen.setColor(QColor(self.planetForegroundColor))
        pen.setWidthF(0.0)
        painter.setPen(pen)
        brush = painter.brush()
        brush.setColor(self.planetForegroundColor)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw the line.
        x1 = 0.0
        y1 = self.parentChartGraphicsItem.convertFromSpeedToYValue(self.speed)
        x2 = self.lineEndX
        y2 = y1
        painter.drawLine(x1, y1, x2, y2)

        # Draw the text for the planet.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(self.planetGlyphFontSize)

        text = self.planetGlyphUnicode
        text += "  {}\u00b0/day".format(self.speed)
        textPath = QPainterPath()
        textPath.addText(0, 0, font, text)
        
        transform = QTransform()
        textX = self.lineEndX
        textY = self.parentChartGraphicsItem.\
                convertFromSpeedToYValue(self.speed)
        transform.translate(textX, textY)
        transformedTextPath = QPainterPath()
        transformedTextPath.addPath(transform.map(textPath))
        painter.drawPath(transformedTextPath)

        # Draw the some fill-in for the area covered by the ruler,
        # above or below 0 speed.  This area drawn has no pen, and a
        # certain brush style.
        rulerFillAreaRectF = \
            QRectF(QPointF(0.0,
                           self.parentChartGraphicsItem.\
                           convertFromSpeedToYValue(0.0)),
                   QPointF(self.rulerWidth,
                           self.parentChartGraphicsItem.\
                           convertFromSpeedToYValue(self.speed))).normalized()
        if self.speed >= 0.0:
            painter.setBrush(self.positiveSpeedBrush)
        else:
            painter.setBrush(self.negativeSpeedBrush)
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRect(rulerFillAreaRectF)

        # Uncomment the below few lines of code to paint the boundingRect().
        # This is here just for future testing purposes.
        #painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        #painter.setBrush(Qt.NoBrush)
        #painter.drawRect(self.boundingRect())
        
        # Restore the old paintbrush and pen.
        painter.setBrush(oldBrush)
        painter.setPen(oldPen)

class PlanetaryInfoTableWidget(QTableWidget):
    """A QTableWidget holding information about a list of planets."""

    def __init__(self, planetaryInfos=[], parent=None):
        """Creates and initializes the widget with the given list of
        PlanetaryInfo objects.
        
        Arguments:
            
        planetaryInfos - list of PlanetaryInfo objects that hold
                         information about the various planets that will
                         be displayed in the QTableWidget.
                         
        """

        super().__init__(parent)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.planetaryInfos = planetaryInfos

        self.log = logging.getLogger("widgets.PlanetaryInfoTableWidget")

        # Set the font so that it is mono-spaced.
        courierFont = QFont()
        courierFont.setFamily("Courier")
        courierFont.setPointSize(8)
        self.setFont(courierFont)

        # Strings for the different types of planetary coordinate systems.
        geoStr = "Geocentric" + os.linesep
        topoStr = "Topocentric" + os.linesep
        helioStr = "Heliocentric" + os.linesep

        sidStr = "Sidereal" + os.linesep
        tropStr = "Tropical" + os.linesep

        # Different measurements available.
        longitudeStr = "Longitude"
        latitudeStr = "Latitude"
        distanceStr = "Distance"

        longitudeSpeedStr = "Longitude Speed"
        latitudeSpeedStr = "Latitude Speed"
        distanceSpeedStr = "Distance Speed"

        rectascensionStr = "Rectascension"
        declinationStr = "Declination"

        rectascensionSpeedStr = "Rectascension Speed"
        declinationSpeedStr = "Decl. Speed"

        xStr = "X Location"
        yStr = "Y Location"
        zStr = "Z Location"

        dxStr = "X Speed"
        dyStr = "Y Speed"
        dzStr = "Z Speed"

        # Units of measurement for the above measurements.
        degreesUnitsStr = " (degrees)"
        auUnitsStr = " (AU)"
        degreesPerDayUnitsStr = " (degrees/day)"
        auPerDayUnitsStr = " (AU/day)"

        # Strings for the 'Planet' header field.
        planetStr = "Planet"
        planetToolTipStr = "Planet"

        # Set the total number of columns.
        numTotalFields = 12
        numColumns = numTotalFields + 1
        self.setColumnCount(numColumns)
        
        # Create all the header QTableWidgetItems.
        col = 0

        tableWidgetItem = QTableWidgetItem(planetStr)
        tableWidgetItem.setToolTip(planetToolTipStr)
        self.setHorizontalHeaderItem(col, tableWidgetItem)
        col += 1

        # Here we've modified it from the total list of fields to
        # only the fields we may be interested in (and in that order).
        item = QTableWidgetItem(geoStr + tropStr + longitudeStr)
        item.setToolTip(longitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 90)
        col += 1
        
        item = QTableWidgetItem(geoStr + sidStr + longitudeStr)
        item.setToolTip(longitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 90)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + "Nakshatra")
        item.setToolTip("Nakshatra")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 70)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + longitudeSpeedStr)
        item.setToolTip(longitudeSpeedStr + degreesPerDayUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + declinationStr)
        item.setToolTip(declinationStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 76)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + declinationSpeedStr)
        item.setToolTip(declinationSpeedStr + degreesPerDayUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 76)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + latitudeStr)
        item.setToolTip(latitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 80)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + latitudeSpeedStr)
        item.setToolTip(latitudeSpeedStr + degreesPerDayUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + longitudeStr)
        item.setToolTip(longitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + "Nakshatra")
        item.setToolTip("Nakshatra")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 80)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + declinationStr)
        item.setToolTip(declinationStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 84)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + latitudeStr)
        item.setToolTip(latitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 84)
        col += 1

        # Now that all the headers are created, load the PlanetaryInfos.
        self.load(self.planetaryInfos)

        # Connect signals and slots.
        self.cellDoubleClicked.\
            connect(self._handleCellDoubleClicked)

    def clear(self):
        """Clears all the rows in the table.  """

        # Load an empty list of PlanetaryInfos to clear.
        self.load([])
        
    def load(self, planetaryInfos):
        """Loads the widgets with the given list of PlanetaryInfo
        objects.
        """
        
        self.log.debug("Entered load()")

        # Make a list of PlanetaryInfos that will actually be loaded,
        # based on if the planet name matches the ones returned by
        # self._getPlanetNamesToDisplayForTable().
        toLoad = []
        for p in planetaryInfos:
            if p.name in self._getPlanetNamesToDisplayForTable():
                toLoad.append(p)

        self.setRowCount(len(toLoad))
        self.clearContents()

        # Load the PlanetaryInfos.
        for i in range(len(toLoad)):

            p = toLoad[i]
            
            if len(self.planetaryInfos) != 0 and i >= len(self.planetaryInfos):
                self._appendPlanetaryInfo(p)
            else:
                self._replaceRowWithPlanetaryInfo(i, p)

        self.planetaryInfos = toLoad

        self.log.debug("Exiting load()")

    def _getPlanetNamesToDisplayForTable(self):
        """Function to return a list of planet names that should be
        used to display in the table cells.  This is to help lessen
        the possibly excessive amount of info in the table.
        """

        toDisplay = \
            ["Ascendant",
             "Midheaven",
             #"HoraLagna",
             #"GhatiLagna",
             #"MeanLunarApogee",
             #"OsculatingLunarApogee",
             #"InterpolatedLunarApogee",
             #"InterpolatedLunarPerigee",
             "Sun",
             "Moon",
             "Mercury",
             "Venus",
             "Earth",
             "Mars",
             "Jupiter",
             "Saturn",
             "Uranus",
             "Neptune",
             "Pluto",
             "MeanNorthNode",
             "MeanSouthNode",
             "TrueNorthNode",
             "TrueSouthNode",
             #"Ceres",
             #"Pallas",
             #"Juno",
             #"Vesta",
             #"Chiron",
             #"Gulika",
             #"Mandi",
             "MeanOfFive",
             "CycleOfEight",
             "AvgMaJuSaUrNePl",
             "AvgJuSaUrNe",
             "AvgJuSa"]

        return toDisplay
        
    def _handleCellDoubleClicked(self, row, column):
        """Triggered when an item is double-clicked.  
        
        This will highlight the entire row of the cell that the user
        double-clicked.
        """

        self.log.debug("QTableWidgetItem double-clicked at " + \
                       "row={}, column={}.".format(row, column))

        # Select the entire row of items where the item was clicked.
        top = row
        bottom = row
        left = 0
        right = self.columnCount() - 1

        range = QTableWidgetSelectionRange(top, left, bottom, right)
        selected = True

        self.setRangeSelected(range, selected)

    def contextMenuEvent(self, qcontextmenuevent):
        """Overwrites the QWidget contextMenuEvent function.

        This brings up a context menu with options:
        - Copy highlighted cell(s) text to clipboard as CSV 
          (without column headers).
        - Copy highlighted cell(s) text to clipboard as CSV
          (with column headers).
        """

        self.log.debug("Entered contextMenuEvent()")

        # First see if any cells are selected.  If there's nothing
        # selected, the actions are disabled.
        cellsAreSelected = False
        if len(self.selectedRanges()) > 0:
            cellsAreSelected = True

        # Open up a context menu.
        menu = QMenu()
        parent = None

        # These are the QActions that are in the menu.
        copyCellTextAsCSVAction = \
            QAction("Copy cell(s) to clipboard as CSV", parent)
        copyCellTextAsCSVAction.triggered.\
            connect(self._selectedCellsTextToClipboard)

        copyCellTextWithColumnHeadersAsCSVAction = \
            QAction("Copy cell(s) to clipboard as CSV " + \
                    "(with column headers)", parent)
        copyCellTextWithColumnHeadersAsCSVAction.triggered.\
            connect(self._selectedCellsAndHeadersTextToClipboard)

        # Enable or disable depending on whether or not cells are selected.
        copyCellTextAsCSVAction.setEnabled(cellsAreSelected)
        copyCellTextWithColumnHeadersAsCSVAction.setEnabled(cellsAreSelected)

        # Add the QActions to the menu.
        menu.addAction(copyCellTextAsCSVAction)
        menu.addAction(copyCellTextWithColumnHeadersAsCSVAction)

        menu.exec_(QCursor.pos())
    
        self.log.debug("Exiting contextMenuEvent()")

    def _selectedCellsTextToClipboard(self, sendColumnHeaders=False):
        """Obtains the selected cells, and turns the text in them to text
        in CSV format.  The text is then copied to the clipboard.

        If the argument 'sendColumnHeaders' is True, then column headers
        are a row in the text sent to the clipboard.
        """

        self.log.debug("Entered _selectedCellsTextToClipboard()")

        # Get the selected ranges.
        selectedRanges = self.selectedRanges()

        numRanges = len(selectedRanges)

        textToClipboard = ""

        for i in range(numRanges):
            r = selectedRanges[i] 

            leftColumn = r.leftColumn()
            rightColumn = r.rightColumn()
            topRow = r.topRow()
            bottomRow = r.bottomRow()

            self.log.debug("DEBUG: " + \
                           "leftColumn={}, ".format(leftColumn) + 
                           "rightColumn={}, ".format(rightColumn) + 
                           "topRow={}, ".format(topRow) + 
                           "bottomRow={}".format(bottomRow))

            if sendColumnHeaders == True:
                for j in range(leftColumn, rightColumn + 1):
                    headerText = self.horizontalHeaderItem(j).text()
                    textToClipboard += headerText.replace(os.linesep, " ")

                    if j != rightColumn:
                        textToClipboard += ","

                textToClipboard += os.linesep

            for j in range(topRow, bottomRow + 1):
                for k in range(leftColumn, rightColumn + 1):
                    textToClipboard += self.item(j, k).text()

                    if k != rightColumn:
                        textToClipboard += ","

                if j != bottomRow:
                    textToClipboard += os.linesep

            textToClipboard += os.linesep + os.linesep

        if textToClipboard == "" and numRanges == 0:
            self.log.debug("No cells were selected.")
        else:
            self.log.debug("Sending the following text to clipboard: " + 
                           textToClipboard)
            clipboard = QApplication.clipboard()
            clipboard.setText(textToClipboard)

        self.log.debug("Exiting _selectedCellsTextToClipboard()")

    def _selectedCellsAndHeadersTextToClipboard(self):
        """Obtains the selected cells and their corresponding header text
        and converts them to CSV format.  That text is then copied to the
        clipboard.
        """

        self.log.debug("Entered _selectedCellsAndHeadersTextToClipboard()")

        self._selectedCellsTextToClipboard(True)

        self.log.debug("Exiting _selectedCellsAndHeadersTextToClipboard()")
    
    def _replaceRowWithPlanetaryInfo(self, row, planetaryInfo):
        """Replaces all the existing QTableWidgetItems in row 'row', with the
        data in PlanetaryInfo 'planetaryInfo'.

        If the row doesn't exist, then QTableWidgetItems are created for
        that row.
        """

        p = planetaryInfo

        # QTableWidgetItem flags.
        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled

        rowCount = self.rowCount()
        col = 0

        # If the row given 
        if row >= rowCount:
            self.setRowCount(row + 1)

        # Item for the planet name.

        # Try to re-use the existing item if one exists already.
        item = self.item(row, col)
        if item == None:
            item = QTableWidgetItem()
            self.setItem(row, col, item)
        item.setText(p.name)
        col += 1

        zodiacs = ['tropical', 'sidereal']

        # Below is all the fields, but we will just use some of the fields,
        #fields = ['longitude',
        #          'latitude',
        #          'distance',
        #          'longitude_speed',
        #          'latitude_speed',
        #          'distance_speed',
        #          'rectascension',
        #          'declination',
        #          'rectascension_speed',
        #          'declination_speed',
        #          'X',
        #          'Y',
        #          'Z',
        #          'dX',
        #          'dY',
        #          'dZ']

        # While it is possible to do all three types, we just do two here.
        #dicts = [p.geocentric, p.topocentric, p.heliocentric]
        dicts = [p.geocentric, p.heliocentric]

        tropical = "tropical"
        sidereal = "sidereal"
        
        # Populate the item cells for each column.
        longitude = p.geocentric[tropical]['longitude']
        valueStr = \
                 AstrologyUtils.\
                 convertFromLongitudeToStrWithRasiAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.geocentric[sidereal]['longitude']
        valueStr = \
                 AstrologyUtils.\
                 convertFromLongitudeToStrWithRasiAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.geocentric[sidereal]['longitude']
        valueStr = \
                 AstrologyUtils.\
                 convertFromLongitudeToNakshatraAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        value = p.geocentric[sidereal]['longitude_speed']
        valueStr = "{:<0.3}".format(value)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        value = p.geocentric[sidereal]['declination']
        valueStr = "{:<0.3}".format(value)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        value = p.geocentric[sidereal]['declination_speed']
        valueStr = "{:<0.3}".format(value)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        value = p.geocentric[sidereal]['latitude']
        valueStr = "{:<0.3}".format(value)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        value = p.geocentric[sidereal]['latitude_speed']
        valueStr = "{:<0.3}".format(value)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.heliocentric[sidereal]['longitude']
        valueStr = \
                 AstrologyUtils.\
                 convertFromLongitudeToStrWithRasiAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.heliocentric[sidereal]['longitude']
        valueStr = \
                 AstrologyUtils.\
                 convertFromLongitudeToNakshatraAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        value = p.heliocentric[sidereal]['declination']
        valueStr = "{:<0.3}".format(value)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        value = p.heliocentric[sidereal]['latitude']
        valueStr = "{:<0.3}".format(value)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1


    def _setItemAndToolTip(self, row, col, valueStr):
        """Returns a str containing the calculated tooltip for the
        given cell.  The tooltip will be in the format"0.1234 degree/day".

        Arguments:
        row - int value holding the row number for the cell.
        col - int value holding the column number for the cell.
        valueStr - str holding the value of the cell.
        """

        # Try to re-use the existing item if one exists already.
        item = self.item(row, col)
        if item == None:
            item = QTableWidgetItem()
            self.setItem(row, col, item)
        item.setText(valueStr)

        # Get what the units is from the header item.
        # This is stored in the tooltip of the header item,
        # and the part of the string we're interested in is
        # the part between the parenthesis.
        headerItem = self.horizontalHeaderItem(col)
        toolTipStr = headerItem.toolTip()
        startParenPos = toolTipStr.find("(")
        endParenPos = toolTipStr.rfind(")")

        if startParenPos != -1 and \
            endParenPos != -1 and \
            startParenPos < endParenPos:

            toolTipStr = \
                valueStr + " " + \
                toolTipStr[startParenPos+1:endParenPos]

            item.setToolTip(toolTipStr)

    
    def _appendPlanetaryInfo(self, planetaryInfo):
        """Appends the info in the PlanetaryInfo object as a row of
        QTableWidgetItems.
        """

        # Here we call the replace function with what would be the next
        # available row.  The replace function is smart enough to create
        # new QTableWidgetItems if it needs them.
        row = self.rowCount()
        self._replaceRowWithPlanetaryInfo(row, planetaryInfo)


class PlanetaryInfoTableGraphicsItem(QGraphicsProxyWidget):
    """QGraphicsProxyWidget (which is also a QGraphicsItem) that
    has a PlanetaryInfoTableWidget embedded within.  This class is
    used so that one can display a table of PlanetaryInfo objects
    within a graphics scene and also scale (grow or shrink) it as needed.
    """

    def __init__(self, planetaryInfos=[], parent=None, scene=None):
        """Creates and initializes the table with the given list of
        PlanetaryInfo objects.
        
        Arguments:
            
        planetaryInfos - list of PlanetaryInfo objects that hold
                         information about the various planets that will
                         be displayed in the internal QTableWidget.
        parent - Parent QGraphicsItem for this object.
        scene - QGraphicsScene object to draw this object on.
        """                 

        super().__init__(parent)

        # Create the internal widget object.
        self.planetaryInfoTableWidget = \
            PlanetaryInfoTableWidget(planetaryInfos)

        # Set the widget for this proxy widget item.
        self.setWidget(self.planetaryInfoTableWidget)

        # Shrink if desired.
        #self.setScale(0.9)

    def load(self, planetaryInfos):
        """Loads the widgets with the given list of PlanetaryInfo
        objects.
        """
        
        self.planetaryInfoTableWidget.load(planetaryInfos)

class AstrologyChartGraphicsView(QGraphicsView):
    """QGraphicsView that visualizes the QGraphicsScene in a
    AstrologyChartWidget.
    """

    def __init__(self, parent=None):
        """Pass-through to the QGraphicsView constructor."""

        super().__init__(parent)

        # Logger
        self.log = \
            logging.getLogger("pricebarchart.PriceBarChartGraphicsView")
        self.log.debug("Entered __init__()")

        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setInteractive(True)
        
        # Set some rendering settings so things draw nicely.
        self.setRenderHints(QPainter.Antialiasing | 
                            QPainter.TextAntialiasing | 
                            QPainter.SmoothPixmapTransform)

        # Set to FullViewportUpdate update mode.
        #
        # The default is normally QGraphicsView.MinimalViewportUpdate, but
        # this caused us to have missing parts of artifacts and missing
        # parts of pricebars.  And while performance isn't as great in
        # the FullViewportUpdate mode, we dont' have many things dynamically
        # updating and changing, so it isn't too big of an issue.
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # For dragging to see different parts of the view.
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
    def wheelEvent(self, qwheelevent):
        """Triggered when the mouse wheel is scrolled."""

        # Save the old transformation anchor and change the current on
        # to anchor under the mouse.  We will put it back at the end
        # of this method.
        oldViewportAnchor = self.transformationAnchor()
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        # Get the QSetting key for the zoom scaling amounts.
        settings = QSettings()
        scaleFactor = \
            settings.value(SettingsKeys.zoomScaleFactorSettingsKey, \
                           SettingsKeys.zoomScaleFactorSettingsDefValue,
                           type=float)
        
        # Actually do the scaling of the view.
        if qwheelevent.delta() > 0:
            # Zoom in.
            self.scale(scaleFactor, scaleFactor)
        else:
            # Zoom out.
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)

        # Put the old transformation anchor back.
        self.setTransformationAnchor(oldViewportAnchor)

        
class AstrologyChartWidget(QWidget):
    """Widget holding the QGraphicsScene and QGraphicsView that displays
    the Astrology information (circle radix and table of PlanetaryInfos).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Logger
        self.log = logging.getLogger("astrologychart.AstrologyChartWidget")
        self.log.debug("Entered __init__()")

        # Holds the birth info, which includes the location and birth time.
        self.birthInfo = BirthInfo()

        # Datetime timestamp of astro chart 1, 2, and 3.  Initialize
        # to the current time in utc.
        self.astroChart1Datetime = datetime.datetime.now(pytz.utc)
        self.astroChart2Datetime = datetime.datetime.now(pytz.utc)
        self.astroChart3Datetime = datetime.datetime.now(pytz.utc)
        
        # Create the contents.

        # Create the QGraphicsScene.
        self.graphicsScene = QGraphicsScene()

        # Set the indexing method to be QGraphicsScene.NoIndex.
        # We need to do this to prevent segmentation faults in Qt's
        # use of a BspTreeIndex.
        self.graphicsScene.setItemIndexMethod(QGraphicsScene.NoIndex)
        
        # Create the QGraphicsView.
        self.graphicsView = AstrologyChartGraphicsView()
        self.graphicsView.setScene(self.graphicsScene)

        self.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setInteractive(True)

        # Set some rendering settings so things draw nicely.
        self.graphicsView.setRenderHints(QPainter.Antialiasing | 
                                         QPainter.TextAntialiasing |
                                         QPainter.SmoothPixmapTransform)

        # Set to FullViewportUpdate update mode.
        #
        # The default is normally QGraphicsView.MinimalViewportUpdate, but
        # this caused us to have missing parts of QGraphicsItems.  And
        # while performance isn't as great in the FullViewportUpdate mode,
        # we dont' have many things dynamically updating and changing, so
        # it isn't too big of an issue.
        self.graphicsView.\
            setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Add and setup things in the QGraphicsScene.
        self.geoSidRadixChartGraphicsItem = SiderealRadixChartGraphicsItem()
        self.geoSidRadixChartGraphicsItem.setScale(0.5)
        self.geoTropRadixChartGraphicsItem = SiderealRadixChartGraphicsItem()
        self.geoTropRadixChartGraphicsItem.setScale(0.5)
        self.helioSidRadixChartGraphicsItem = SiderealRadixChartGraphicsItem()
        self.helioSidRadixChartGraphicsItem.setScale(0.5)

        self.declinationChart = DeclinationChartGraphicsItem()
        self.declinationChart.setScale(0.8)

        # TODO: add these widgets for longitude speeds...?  Maybe it's not worth the effort right now?
        self.longitudeSpeedChart1Mercury = \
            LongitudeSpeedChartGraphicsItem(maxSpeed=16.0,
                                                minSpeed=-5.0)

        # Create a label for the location.
        locationString = \
            self.birthInfo.locationName + "(" + \
            str(self.birthInfo.longitudeDegrees) + ", " + \
            str(self.birthInfo.latitudeDegrees) + ")"
        self.locationLabelWidget = QLabel("Location: " + locationString)
        self.locationLabelProxyWidget = QGraphicsProxyWidget()
        self.locationLabelProxyWidget.setWidget(self.locationLabelWidget)
        
        # Create labels for the timestamps of each astro chart.
        #
        # Need to use the Ephemeris.datetimeToStr() below because
        # datetime.strftime() datetime.strftime() does not work on
        # years less than 1900.
        self.astroChart1DatetimeLabelWidget = \
            QLabel("Chart 1:  " +
                   Ephemeris.datetimeToStr(self.astroChart1Datetime))
        self.astroChart1DatetimeLabelProxyWidget = QGraphicsProxyWidget()
        self.astroChart1DatetimeLabelProxyWidget.\
            setWidget(self.astroChart1DatetimeLabelWidget)
        
        self.astroChart2DatetimeLabelWidget = \
            QLabel("Chart 2:  " +
                   Ephemeris.datetimeToStr(self.astroChart2Datetime))
        self.astroChart2DatetimeLabelProxyWidget = QGraphicsProxyWidget()
        self.astroChart2DatetimeLabelProxyWidget.\
            setWidget(self.astroChart2DatetimeLabelWidget)
        
        self.astroChart3DatetimeLabelWidget = \
            QLabel("Chart 3:  " +
                   Ephemeris.datetimeToStr(self.astroChart3Datetime))
        self.astroChart3DatetimeLabelProxyWidget = QGraphicsProxyWidget()
        self.astroChart3DatetimeLabelProxyWidget.\
            setWidget(self.astroChart3DatetimeLabelWidget)

        self.geoSidRadixChartLabel = QGraphicsProxyWidget()
        self.geoSidRadixChartLabel.setWidget(QLabel("Geocentric Sidereal"))
        self.geoTropRadixChartLabel = QGraphicsProxyWidget()
        self.geoTropRadixChartLabel.setWidget(QLabel("Geocentric Tropical"))
        self.helioSidRadixChartLabel = QGraphicsProxyWidget()
        self.helioSidRadixChartLabel.setWidget(QLabel("Heliocentric Sidereal"))

        self.declinationChartLabel = QGraphicsProxyWidget()
        self.declinationChartLabel.setWidget(QLabel("Declination"))
        
        # Set the positions of the QGraphicsItems then add them to the
        # QGraphicsScene.
        width = SiderealRadixChartGraphicsItem().boundingRect().width()
        radixLength = (width / 2.0) + 40
    
        x = 0
        y = 0
        x -= 0.5 * radixLength
        y += 0.5 * radixLength
        labelHeight = 16
        self.locationLabelProxyWidget.setPos(x, y)
        y += labelHeight
        self.astroChart1DatetimeLabelProxyWidget.setPos(x, y)
        y += labelHeight
        self.astroChart2DatetimeLabelProxyWidget.setPos(x, y)
        y += labelHeight
        self.astroChart3DatetimeLabelProxyWidget.setPos(x, y)
        y += labelHeight
        y += labelHeight
        y += labelHeight

        declinationWidth = 200
        declStartX = x
        declStartY = y
        self.declinationChartLabel.setPos(x, y)
        x += 36
        y += 260
        self.declinationChart.setPos(x, y)

        
        x = 0.0
        y = 0.0
        self.geoSidRadixChartGraphicsItem.setPos(x, y)
        x += radixLength
        self.geoTropRadixChartGraphicsItem.setPos(x, y)
        x += radixLength
        self.helioSidRadixChartGraphicsItem.setPos(x, y)
        x += radixLength
        
        x = -0.45 * radixLength
        y = -0.45 * radixLength
        self.geoSidRadixChartLabel.setPos(x, y)
        x += radixLength
        self.geoTropRadixChartLabel.setPos(x, y)
        x += radixLength
        self.helioSidRadixChartLabel.setPos(x, y)
        x += radixLength

        # Add all the items to the QGraphicsScene.
        self.graphicsScene.addItem(self.locationLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart1DatetimeLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart2DatetimeLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart3DatetimeLabelProxyWidget)
    
        self.graphicsScene.addItem(self.declinationChart)
        
        self.graphicsScene.addItem(self.geoSidRadixChartGraphicsItem)
        self.graphicsScene.addItem(self.geoTropRadixChartGraphicsItem)
        self.graphicsScene.addItem(self.helioSidRadixChartGraphicsItem)
        
        self.graphicsScene.addItem(self.geoSidRadixChartLabel)
        self.graphicsScene.addItem(self.geoTropRadixChartLabel)
        self.graphicsScene.addItem(self.helioSidRadixChartLabel)

        self.graphicsScene.addItem(self.declinationChartLabel)
        

        # Setup the layout.
        layout = QVBoxLayout()
        layout.addWidget(self.graphicsView)
        self.setLayout(layout)
        
        self.log.debug("Leaving __init__()")
        
        
    def setBirthInfo(self, birthInfo):
        """Sets the birth info for this trading entity.
        
        Arguments:

        birthInfo - BirthInfo object.
        """

        self.birthInfo = birthInfo

    def getPlanetaryInfosForDatetime(self, dt):
        """Helper function for getting a list of PlanetaryInfo objects
        to display in the astrology chart.

        """

        # Set the location again (required).
        Ephemeris.setGeographicPosition(self.birthInfo.longitudeDegrees,
                                        self.birthInfo.latitudeDegrees,
                                        self.birthInfo.elevation)

        # Get planetary info for all the planets.
        planets = []

        # TODO:  Add more 'planets' (planetary calculations) here as more
        # are available.

        planets.append(Ephemeris.getSunPlanetaryInfo(dt))
        planets.append(Ephemeris.getMoonPlanetaryInfo(dt))
        planets.append(Ephemeris.getMercuryPlanetaryInfo(dt))
        planets.append(Ephemeris.getVenusPlanetaryInfo(dt))
        planets.append(Ephemeris.getMarsPlanetaryInfo(dt))
        planets.append(Ephemeris.getJupiterPlanetaryInfo(dt))
        planets.append(Ephemeris.getSaturnPlanetaryInfo(dt))
        planets.append(Ephemeris.getUranusPlanetaryInfo(dt))
        planets.append(Ephemeris.getNeptunePlanetaryInfo(dt))
        planets.append(Ephemeris.getPlutoPlanetaryInfo(dt))
        planets.append(Ephemeris.getMeanNorthNodePlanetaryInfo(dt))
        planets.append(Ephemeris.getTrueNorthNodePlanetaryInfo(dt))
        planets.append(Ephemeris.getMeanLunarApogeePlanetaryInfo(dt))
        planets.append(Ephemeris.getOsculatingLunarApogeePlanetaryInfo(dt))
        planets.append(Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(dt))
        planets.append(Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(dt))
        planets.append(Ephemeris.getEarthPlanetaryInfo(dt))
        planets.append(Ephemeris.getChironPlanetaryInfo(dt))
        planets.append(Ephemeris.getMOFPlanetaryInfo(dt))
        planets.append(Ephemeris.getCOEPlanetaryInfo(dt))
        planets.append(Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(dt))
        planets.append(Ephemeris.getAvgJuSaUrNePlanetaryInfo(dt))
        planets.append(Ephemeris.getAvgJuSaPlanetaryInfo(dt))
        
        return planets

    def _getPlanetNamesToDisplayForDeclination(self):
        """Function to return a list of planet names that should be
        used to display declination information.  This is used because
        some planets don't make sense to chart on declination and it
        just clouds up the view.
        """

        toDisplay = \
            ["Sun",
             "Moon",
             "Mercury",
             "Venus",
             "Mars",
             "Jupiter",
             "Saturn",
             "Uranus",
             "Neptune",
             "Pluto",
             "MeanOfFive",
             "CycleOfEight",
             "AvgMaJuSaUrNePl",
             "AvgJuSaUrNe",
             "AvgJuSa"]

        return toDisplay
        
    def _getPlanetNamesToDisplayForGeoSidRadixChart(self):
        """Function to returna list of planet names that can be
        used to display longitude information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        toDisplay = \
            ["Ascendant",
             "Midheaven",
             "HoraLagna",
             "GhatiLagna",
             #"MeanLunarApogee",
             #"OsculatingLunarApogee",
             #"InterpolatedLunarApogee",
             #"InterpolatedLunarPerigee",
             "Sun",
             "Moon",
             "Mercury",
             "Venus",
             #"Earth",
             "Mars",
             "Jupiter",
             "Saturn",
             "Uranus",
             "Neptune",
             "Pluto",
             "MeanNorthNode",
             "MeanSouthNode",
             "TrueNorthNode",
             "TrueSouthNode",
             #"Ceres",
             #"Pallas",
             #"Juno",
             #"Vesta",
             #"Chiron",
             "Gulika",
             "Mandi",
             "MeanOfFive",
             "CycleOfEight",
             "AvgMaJuSaUrNePl",
             "AvgJuSaUrNe",
             "AvgJuSa"]

        return toDisplay

    def _getPlanetNamesToDisplayForGeoTropRadixChart(self):
        """Function to returna list of planet names that can be
        used to display longitude information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        # Use the same values for Geocentric Tropical as used in
        # Geocentric Sidereal.
        return self._getPlanetNamesToDisplayForGeoSidRadixChart()

    def _getPlanetNamesToDisplayForHelioSidRadixChart(self):
        """Function to returna list of planet names that can be
        used to display longitude information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        toDisplay = \
            [#"Ascendant",
             #"Midheaven",
             #"HoraLagna",
             #"GhatiLagna",
             #"MeanLunarApogee",
             #"OsculatingLunarApogee",
             #"InterpolatedLunarApogee",
             #"InterpolatedLunarPerigee",
             #"Sun",
             #"Moon",
             "Mercury",
             "Venus",
             "Earth",
             "Mars",
             "Jupiter",
             "Saturn",
             "Uranus",
             "Neptune",
             "Pluto",
             #"MeanNorthNode",
             #"MeanSouthNode",
             #"TrueNorthNode",
             #"TrueSouthNode",
             #"Ceres",
             #"Pallas",
             #"Juno",
             #"Vesta",
             #"Chiron",
             #"Gulika",
             #"Mandi",
             "MeanOfFive",
             "CycleOfEight",
             "AvgMaJuSaUrNePl",
             "AvgJuSaUrNe",
             "AvgJuSa"]

        return toDisplay

    def setAstroChartXDatetime(self, chartNum, dt):
        """Sets the datetime of astrology chart 'chartNum'
        within the radix chart and other charts.

        Arguments:
        chartNum - int value holding the chart number to update.
        dt - datetime.datetime object holding the new timestamp.
        """

        # Wheel number (chart number) that will be updated.
        wheelNumber = chartNum

        # Get the PlanetaryInfo objects.
        planets = self.getPlanetaryInfosForDatetime(dt)

        # Update the planets' QGraphicsItems on each radix chart.
        for planet in planets:
            # Location label doesn't need to be updated here because
            # it gets updated when the BirthInfo gets set in this
            # widget.

            # Update the declination chart.
            if planet.name in self._getPlanetNamesToDisplayForDeclination():
                planetDeclinationGraphicsItem = \
                    self.declinationChart.\
                    getPlanetDeclinationGraphicsItem(planet.name, chartNum)
                
                if planetDeclinationGraphicsItem == None:
                    # No PlanetDeclinationGraphicsItem exists yet for
                    # this planet, so create it.
                    planetDeclinationGraphicsItem = \
                        PlanetDeclinationGraphicsItem(
                        planet.name,
                        AstrologyUtils.getGlyphForPlanetName(planet.name),
                        AstrologyUtils.getGlyphFontSizeForPlanetName(planet.name),
                        AstrologyUtils.getAbbreviationForPlanetName(planet.name),
                        AstrologyUtils.getForegroundColorForPlanetName(planet.name),
                        AstrologyUtils.getBackgroundColorForPlanetName(planet.name),
                        degree=planet.geocentric['sidereal']['latitude'],
                        velocity=planet.geocentric['sidereal']['longitude_speed'],
                        planetGroupNumber=chartNum,
                        parent=self.declinationChart)
                else:
                    # The PlanetDeclinationGraphicsItem for this planet
                    # already exists for this chartNum.  Just update it.
                    degree = planet.geocentric['sidereal']['latitude']
                    velocity = planet.geocentric['sidereal']['longitude_speed']
                    planetDeclinationGraphicsItem.setDegreeAndVelocity(degree, velocity)

            
            # Geocentric Sidereal.
            if planet.name in \
                   self._getPlanetNamesToDisplayForGeoSidRadixChart():

                radixPlanetGraphicsItem = \
                    self.geoSidRadixChartGraphicsItem.\
                    getRadixPlanetGraphicsItem(planet.name, wheelNumber)
                
                if radixPlanetGraphicsItem == None:
                    # No RadixPlanetGraphicsItem exists for this planet yet,
                    # so create it.
                    
                    # Get all the info needed to create it.
                    glyph = \
                        AstrologyUtils.\
                        getGlyphForPlanetName(planet.name)
                    fontSize = \
                        AstrologyUtils.\
                        getGlyphFontSizeForPlanetName(planet.name)
                    abbrev = \
                        AstrologyUtils.\
                        getAbbreviationForPlanetName(planet.name)
                    foregroundColor = \
                        AstrologyUtils.\
                        getForegroundColorForPlanetName(planet.name)
                    backgroundColor = \
                        AstrologyUtils.\
                        getBackgroundColorForPlanetName(planet.name)
                    degree = planet.geocentric['sidereal']['longitude']
                    velocity = planet.geocentric['sidereal']['longitude_speed']
                    parent = self.geoSidRadixChartGraphicsItem
    
                    # Create the RadixPlanetGraphicsItem.
                    radixPlanetGraphicsItem = \
                        RadixPlanetGraphicsItem(planet.name,
                                                glyph,
                                                fontSize,
                                                abbrev,
                                                foregroundColor,
                                                backgroundColor,
                                                degree,
                                                velocity,
                                                wheelNumber,
                                                parent)
                else:
                    # The item exists already, so just update it with new
                    # values.
                    degree = planet.geocentric['sidereal']['longitude']
                    velocity = planet.geocentric['sidereal']['longitude_speed']
                    
                    radixPlanetGraphicsItem.\
                        setDegreeAndVelocity(degree, velocity)

            # Geocentric Tropical.
            if planet.name in \
                   self._getPlanetNamesToDisplayForGeoTropRadixChart():
                
                radixPlanetGraphicsItem = \
                    self.geoTropRadixChartGraphicsItem.\
                    getRadixPlanetGraphicsItem(planet.name, wheelNumber)
                
                if radixPlanetGraphicsItem == None:
                    # No RadixPlanetGraphicsItem exists for this planet yet,
                    # so create it.
    
                    # Get all the info needed to create it.
                    glyph = \
                        AstrologyUtils.\
                        getGlyphForPlanetName(planet.name)
                    fontSize = \
                        AstrologyUtils.\
                        getGlyphFontSizeForPlanetName(planet.name)
                    abbrev = \
                        AstrologyUtils.\
                        getAbbreviationForPlanetName(planet.name)
                    foregroundColor = \
                        AstrologyUtils.\
                        getForegroundColorForPlanetName(planet.name)
                    backgroundColor = \
                        AstrologyUtils.\
                        getBackgroundColorForPlanetName(planet.name)
                    degree = planet.geocentric['tropical']['longitude']
                    velocity = planet.geocentric['tropical']['longitude_speed']
                    parent = self.geoTropRadixChartGraphicsItem
                    
                    # Create the RadixPlanetGraphicsItem.
                    radixPlanetGraphicsItem = \
                        RadixPlanetGraphicsItem(planet.name,
                                                glyph,
                                                fontSize,
                                                abbrev,
                                                foregroundColor,
                                                backgroundColor,
                                                degree,
                                                velocity,
                                                wheelNumber,
                                                parent)
                else:
                    # The item exists already, so just update it with new
                    # values.
                    degree = planet.geocentric['tropical']['longitude']
                    velocity = planet.geocentric['tropical']['longitude_speed']
                    
                    radixPlanetGraphicsItem.\
                        setDegreeAndVelocity(degree, velocity)

            # Heliocentric Sidereal.
            if planet.name in \
                   self._getPlanetNamesToDisplayForHelioSidRadixChart():
                
                radixPlanetGraphicsItem = \
                    self.helioSidRadixChartGraphicsItem.\
                    getRadixPlanetGraphicsItem(planet.name, wheelNumber)
                
                if radixPlanetGraphicsItem == None:
                    # No RadixPlanetGraphicsItem exists for this planet yet,
                    # so create it.
    
                    # Get all the info needed to create it.
                    glyph = \
                        AstrologyUtils.\
                        getGlyphForPlanetName(planet.name)
                    fontSize = \
                        AstrologyUtils.\
                        getGlyphFontSizeForPlanetName(planet.name)
                    abbrev = \
                        AstrologyUtils.\
                        getAbbreviationForPlanetName(planet.name)
                    foregroundColor = \
                        AstrologyUtils.\
                        getForegroundColorForPlanetName(planet.name)
                    backgroundColor = \
                        AstrologyUtils.\
                        getBackgroundColorForPlanetName(planet.name)
                    degree = \
                        planet.heliocentric['sidereal']['longitude']
                    velocity = \
                        planet.heliocentric['sidereal']['longitude_speed']
                    parent = self.helioSidRadixChartGraphicsItem
    
                    # Create the RadixPlanetGraphicsItem.
                    radixPlanetGraphicsItem = \
                        RadixPlanetGraphicsItem(planet.name,
                                                glyph,
                                                fontSize,
                                                abbrev,
                                                foregroundColor,
                                                backgroundColor,
                                                degree,
                                                velocity,
                                                wheelNumber,
                                                parent)
                else:
                    # The item exists already, so just update it with new
                    # values.
                    degree = \
                        planet.heliocentric['sidereal']['longitude']
                    velocity = \
                        planet.heliocentric['sidereal']['longitude_speed']
                    
                    radixPlanetGraphicsItem.\
                        setDegreeAndVelocity(degree, velocity)

        # Update the aspects for the radix charts.

        # Geocentric Sidereal.
        self.geoSidRadixChartGraphicsItem.redrawAspects()
        
        # Geocentric Tropical.
        self.geoTropRadixChartGraphicsItem.redrawAspects()

        # Heliocentric Sidereal.
        self.helioSidRadixChartGraphicsItem.redrawAspects()

    def setAstroChart1Datetime(self, dt):
        """Sets the datetime of astrology chart 1 within the radix chart.

        Arguments:
        dt - datetime.datetime object holding the new timestamp.
        """

        chartNum = 1

        # Save the datetime used.
        self.astroChart1Datetime = dt

        # Set the label that shows what datetime is used for this
        # chart.
        #
        # Need to use the Ephemeris.datetimeToStr() below because
        # datetime.strftime() datetime.strftime() does not work on
        # years less than 1900.
        self.astroChart1DatetimeLabelWidget.\
            setText(Ephemeris.datetimeToStr(self.astroChart1Datetime))

        # Update the rest of the astro widgets.
        self.setAstroChartXDatetime(chartNum, dt)
    
    def setAstroChart2Datetime(self, dt):
        """Sets the datetime of astrology chart 2 within the radix chart.

        Arguments:
        dt - datetime.datetime object holding the new timestamp.
        """
        
        chartNum = 2

        # Save the datetime used.
        self.astroChart2Datetime = dt
        
        # Set the label that shows what datetime is used for this
        # chart.
        #
        # Need to use the Ephemeris.datetimeToStr() below because
        # datetime.strftime() datetime.strftime() does not work on
        # years less than 1900.
        self.astroChart2DatetimeLabelWidget.\
            setText(Ephemeris.datetimeToStr(self.astroChart2Datetime))

        # Update the rest of the astro widgets.
        self.setAstroChartXDatetime(chartNum, dt)
    
    def setAstroChart3Datetime(self, dt):
        """Sets the datetime of astrology chart 3 within the radix chart.

        Arguments:
        dt - datetime.datetime object holding the new timestamp.
        """
        
        chartNum = 3

        # Save the datetime used.
        self.astroChart3Datetime = dt

        # Set the label that shows what datetime is used for this
        # chart.
        #
        # Need to use the Ephemeris.datetimeToStr() below because
        # datetime.strftime() datetime.strftime() does not work on
        # years less than 1900.
        self.astroChart3DatetimeLabelWidget.\
            setText(Ephemeris.datetimeToStr(self.astroChart3Datetime))

        # Update the rest of the astro widgets.
        self.setAstroChartXDatetime(chartNum, dt)

    def clearAstroChartX(self, chartNum):
        """Clears the astrology chart 'chartNum' within the radix
        chart and other charts.

        Arguments:
        chartNum - int value holding the chart number to update.
        """

        # Wheel number (chart number) that will be updated.
        wheelNumber = chartNum

        # Location label does not need to be updated here because
        # it gets updated when the BirthInfo gets set in this
        # widget.

        # Clear the datetime label widgets depending on which chartNum.
        if chartNum == 1:
            self.astroChart1DatetimeLabelWidget.setText("Chart 1:  ")
        elif chartNum == 2:
            self.astroChart2DatetimeLabelWidget.setText("Chart 2:  ")
        elif chartNum == 3:
            self.astroChart3DatetimeLabelWidget.setText("Chart 3:  ")
        else:
            self.log.warn("Unknown chartNum: {}".format(chartNum))

        # Update the declination chart.
        for planetName in self._getPlanetNamesToDisplayForDeclination():
            planetDeclinationGraphicsItem = \
                self.declinationChart.\
                getPlanetDeclinationGraphicsItem(planetName, chartNum)

            # If an item is found with the given name on the chart
            # number, then remove that item.
            if planetDeclinationGraphicsItem != None:
                self.graphicsScene.removeItem(planetDeclinationGraphicsItem)
        
        # Remove QGraphicsItems on each radix chart.
        
        # Get the PlanetaryInfo objects.  The location values in this
        # list aren't used.  We only need this so we have a list of
        # planet names used.
        planets = self.getPlanetaryInfosForDatetime(\
            datetime.datetime.now(pytz.utc))

        for planet in planets:
            
            # Update the Geocentric Sidereal chart.
            radixPlanetGraphicsItem = \
                self.geoSidRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
            
            if radixPlanetGraphicsItem != None:
                self.graphicsScene.removeItem(radixPlanetGraphicsItem)

            # Update the Geocentric Tropical chart.
            radixPlanetGraphicsItem = \
                self.geoTropRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
            
            if radixPlanetGraphicsItem != None:
                self.graphicsScene.removeItem(radixPlanetGraphicsItem)
            
            # Update the Heliocentric Sidereal chart.
            radixPlanetGraphicsItem = \
                self.helioSidRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
            
            if radixPlanetGraphicsItem != None:
                self.graphicsScene.removeItem(radixPlanetGraphicsItem)


        # Update the aspects for the radix charts.

        # Geocentric Sidereal.
        self.geoSidRadixChartGraphicsItem.redrawAspects()
        
        # Geocentric Tropical.
        self.geoTropRadixChartGraphicsItem.redrawAspects()

        # Heliocentric Sidereal.
        self.helioSidRadixChartGraphicsItem.redrawAspects()

    def clearAstroChart1(self):
        """Clears the AstroChart1 of all planet-related objects."""

        chartNum = 1
        self.clearAstroChartX(chartNum)
        
    def clearAstroChart2(self):
        """Clears the AstroChart2 of all planet-related objects."""

        chartNum = 2
        self.clearAstroChartX(chartNum)
        
    def clearAstroChart3(self):
        """Clears the AstroChart3 of all planet-related objects."""

        chartNum = 3
        self.clearAstroChartX(chartNum)
        
        
def testSiderealRadixChartGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")

    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    item = SiderealRadixChartGraphicsItem()
    
    scene.addItem(item)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()


def testRadixPlanetGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")
    
    from settings import SettingsKeys
    
    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    chartItem = SiderealRadixChartGraphicsItem()
    
    scene.addItem(chartItem)

    jupiter = \
        RadixPlanetGraphicsItem("Jupiter",
                                SettingsKeys.planetJupiterGlyphUnicodeDefValue,
                                SettingsKeys.planetJupiterGlyphFontSizeDefValue,
                                SettingsKeys.planetJupiterAbbreviationDefValue,
                                SettingsKeys.planetJupiterForegroundColorDefValue,
                                SettingsKeys.planetJupiterBackgroundColorDefValue,
                                degree=5.0,
                                velocity=4.0,
                                wheelNumber=2,
                                parent=chartItem)
    venus = \
        RadixPlanetGraphicsItem("Venus",
                                SettingsKeys.planetVenusGlyphUnicodeDefValue,
                                SettingsKeys.planetVenusGlyphFontSizeDefValue,
                                SettingsKeys.planetVenusAbbreviationDefValue,
                                QColor(Qt.red),
                                SettingsKeys.planetVenusBackgroundColorDefValue,
                                degree=9.0,
                                velocity=-2.0,
                                wheelNumber=1,
                                parent=chartItem)
    

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()


def testDeclinationChartGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")
    
    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    chartItem = DeclinationChartGraphicsItem()
    
    scene.addItem(chartItem)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()

def testPlanetDeclinationGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")
    
    from settings import SettingsKeys
    
    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    chartItem = DeclinationChartGraphicsItem()
    scene.addItem(chartItem)

    moon = \
        PlanetDeclinationGraphicsItem(
        "Moon",
        SettingsKeys.planetMoonGlyphUnicodeDefValue,
        SettingsKeys.planetMoonGlyphFontSizeDefValue,
        SettingsKeys.planetMoonAbbreviationDefValue,
        QColor(Qt.blue),
        SettingsKeys.planetMoonBackgroundColorDefValue,
        degree=17.56,
        velocity=2.0,
        planetGroupNumber=1,
        parent=chartItem)
    
    mercury = \
        PlanetDeclinationGraphicsItem(
        "Mercury",
        SettingsKeys.planetMercuryGlyphUnicodeDefValue,
        SettingsKeys.planetMercuryGlyphFontSizeDefValue,
        SettingsKeys.planetMercuryAbbreviationDefValue,
        QColor(Qt.green),
        SettingsKeys.planetMercuryBackgroundColorDefValue,
        degree=5.2,
        velocity=-2.0,
        planetGroupNumber=1,
        parent=chartItem)

    jupiter = \
        PlanetDeclinationGraphicsItem(
        "Jupiter",
        SettingsKeys.planetJupiterGlyphUnicodeDefValue,
        SettingsKeys.planetJupiterGlyphFontSizeDefValue,
        SettingsKeys.planetJupiterAbbreviationDefValue,
        QColor(Qt.red),
        SettingsKeys.planetJupiterBackgroundColorDefValue,
        degree=-8.0,
        velocity=3.0,
        planetGroupNumber=1,
        parent=chartItem)

    moon = \
        PlanetDeclinationGraphicsItem(
        "Moon",
        SettingsKeys.planetMoonGlyphUnicodeDefValue,
        SettingsKeys.planetMoonGlyphFontSizeDefValue,
        SettingsKeys.planetMoonAbbreviationDefValue,
        QColor(Qt.blue),
        SettingsKeys.planetMoonBackgroundColorDefValue,
        degree=5,
        velocity=2.0,
        planetGroupNumber=2,
        parent=chartItem)
    
    mercury = \
        PlanetDeclinationGraphicsItem(
        "Mercury",
        SettingsKeys.planetMercuryGlyphUnicodeDefValue,
        SettingsKeys.planetMercuryGlyphFontSizeDefValue,
        SettingsKeys.planetMercuryAbbreviationDefValue,
        QColor(Qt.green),
        SettingsKeys.planetMercuryBackgroundColorDefValue,
        degree=-9.2,
        velocity=-2.0,
        planetGroupNumber=2,
        parent=chartItem)

    jupiter = \
        PlanetDeclinationGraphicsItem(
        "Jupiter",
        SettingsKeys.planetJupiterGlyphUnicodeDefValue,
        SettingsKeys.planetJupiterGlyphFontSizeDefValue,
        SettingsKeys.planetJupiterAbbreviationDefValue,
        QColor(Qt.red),
        SettingsKeys.planetJupiterBackgroundColorDefValue,
        degree=7.0,
        velocity=3.0,
        planetGroupNumber=2,
        parent=chartItem)
    
    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()


def testLongitudeSpeedChartGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")
    
    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    chartItem = LongitudeSpeedChartGraphicsItem(maxSpeed=32.0,
                                                minSpeed=-10.0)
    
    scene.addItem(chartItem)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()
    

def testPlanetLongitudeSpeedGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")
    
    from settings import SettingsKeys
    
    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    chartItem = LongitudeSpeedChartGraphicsItem(maxSpeed=16.0,
                                                minSpeed=-5.0)
    scene.addItem(chartItem)

    mercury = \
        PlanetLongitudeSpeedGraphicsItem(
        SettingsKeys.planetMercuryGlyphUnicodeDefValue,
        SettingsKeys.planetMercuryGlyphFontSizeDefValue,
        SettingsKeys.planetMercuryAbbreviationDefValue,
        QColor(Qt.green),
        SettingsKeys.planetMercuryBackgroundColorDefValue,
        speed=15.2,
        parent=chartItem)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()


def testPlanetaryInfoTableWidget():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    #print("Now is: {}".format(now))

    planets = []

    # Get planetary info for all the planets, and print out the info.
    p = Ephemeris.getSunPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMoonPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMercuryPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getVenusPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMarsPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getJupiterPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getSaturnPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getUranusPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getNeptunePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getPlutoPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMeanNorthNodePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getTrueNorthNodePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMeanLunarApogeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getEarthPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getChironPlanetaryInfo(now)
    planets.append(p)


    # Various combinations of planets to test.
    widget = PlanetaryInfoTableWidget(planets)
    #widget = PlanetaryInfoTableWidget([])

    layout = QVBoxLayout()
    layout.addWidget(widget)

    dialog = QDialog()
    dialog.setLayout(layout)

    rv = dialog.exec_()

def testPlanetaryInfoTableGraphicsItem():
    print("Running " + inspect.stack()[0][3] + "()")

    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    view.setInteractive(True)

    # Set some rendering settings so things draw nicely.
    view.setRenderHints(QPainter.Antialiasing | 
                        QPainter.TextAntialiasing |
                        QPainter.SmoothPixmapTransform)

    # Set to FullViewportUpdate update mode.
    #
    # The default is normally QGraphicsView.MinimalViewportUpdate, but
    # this caused us to have missing parts of artifacts and missing
    # parts of pricebars.  And while performance isn't as great in
    # the FullViewportUpdate mode, we dont' have many things dynamically
    # updating and changing, so it isn't too big of an issue.
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    #print("Now is: {}".format(now))

    planets = []

    # Get planetary info for all the planets, and print out the info.
    p = Ephemeris.getSunPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMoonPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMercuryPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getVenusPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMarsPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getJupiterPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getSaturnPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getUranusPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getNeptunePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getPlutoPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMeanNorthNodePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getTrueNorthNodePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getMeanLunarApogeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getEarthPlanetaryInfo(now)
    planets.append(p)

    p = Ephemeris.getChironPlanetaryInfo(now)
    planets.append(p)


    item = PlanetaryInfoTableGraphicsItem(planets)
    #item = PlanetaryInfoTableGraphicsItem()

    scene.addItem(item)

    layout = QVBoxLayout()
    layout.addWidget(view)
    
    dialog = QDialog()
    dialog.setLayout(layout)

    dialog.exec_()
    
def testAstrologyChartWidget():
    print("Running " + inspect.stack()[0][3] + "()")

    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    #print("Now is: {}".format(now))

    # Create a BirthInfo object for the location to use.
    birthInfo = BirthInfo(year=1983,
                          month=10,
                          day=25,
                          calendar="Gregorian",
                          hour=14,
                          minute=34,
                          second=0,
                          locationName="Arlington",
                          countryName="",
                          longitudeDegrees=-77.1041666667,
                          latitudeDegrees=38.8811111111,
                          elevation=71,
                          timezoneName="America/New_York",
                          timezoneOffsetAbbreviation="EDT",
                          timezoneOffsetValueStr="-0400",
                          timezoneManualEntryHours=4,
                          timezoneManualEntryMinutes=0,
                          timezoneManualEntryEastWestComboBoxValue='E',
                          timeOffsetAutodetectedRadioButtonState=True,
                          timeOffsetManualEntryRadioButtonState=False,
                          timeOffsetLMTRadioButtonState=False)

    # Create the widget to test/view.
    widget = AstrologyChartWidget()
    widget.setBirthInfo(birthInfo)

    # Set the timestamp in the widget.
    widget.setAstroChart1Datetime(now)
    widget.setAstroChart2Datetime(now)
    widget.setAstroChart3Datetime(now)

    # Display the widget in a dialog.
    layout = QVBoxLayout()
    layout.addWidget(widget)

    dialog = QDialog()
    dialog.setLayout(layout)

    rv = dialog.exec_()
    
# For debugging the module during development.  
if __name__=="__main__":
    # For inspect.stack().
    import inspect
    
    import sys
    
    # Initialize the Ephemeris (required).
    Ephemeris.initialize()

    # Set a default location (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)
    
    # Initialize logging.
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Create the Qt application.
    app = QApplication(sys.argv)

    # Set application details so the we can use QSettings default
    # constructor later.
    appAuthor = "Ryan Luu"
    appName = "PriceChartingTool"
    QCoreApplication.setOrganizationName(appAuthor)
    QCoreApplication.setApplicationName(appName)
        
    # Various tests to run:
    #testSiderealRadixChartGraphicsItem()
    #testRadixPlanetGraphicsItem()
    #testDeclinationChartGraphicsItem()
    #testPlanetDeclinationGraphicsItem()
    testLongitudeSpeedChartGraphicsItem()
    testPlanetLongitudeSpeedGraphicsItem()
    #testPlanetaryInfoTableWidget()
    #testPlanetaryInfoTableGraphicsItem()
    testAstrologyChartWidget()
    
    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()
    #app.exec_()
    

        
