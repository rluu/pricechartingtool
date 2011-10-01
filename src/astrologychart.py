
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
                           SettingsKeys.signAriesGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signTaurusGlyphUnicodeKey,
                           SettingsKeys.signTaurusGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signGeminiGlyphUnicodeKey,
                           SettingsKeys.signGeminiGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signCancerGlyphUnicodeKey,
                           SettingsKeys.signCancerGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signLeoGlyphUnicodeKey,
                           SettingsKeys.signLeoGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signVirgoGlyphUnicodeKey,
                           SettingsKeys.signVirgoGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signLibraGlyphUnicodeKey,
                           SettingsKeys.signLibraGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signScorpioGlyphUnicodeKey,
                           SettingsKeys.signScorpioGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signSagittariusGlyphUnicodeKey,
                           SettingsKeys.signSagittariusGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signCapricornGlyphUnicodeKey,
                           SettingsKeys.signCapricornGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signAquariusGlyphUnicodeKey,
                           SettingsKeys.signAquariusGlyphUnicodeDefValue),
            settings.value(SettingsKeys.signPiscesGlyphUnicodeKey,
                           SettingsKeys.signPiscesGlyphUnicodeDefValue)]

        signAbbreviations = [\
            settings.value(SettingsKeys.signAriesAbbreviationKey,
                           SettingsKeys.signAriesAbbreviationDefValue),
            settings.value(SettingsKeys.signTaurusAbbreviationKey,
                           SettingsKeys.signTaurusAbbreviationDefValue),
            settings.value(SettingsKeys.signGeminiAbbreviationKey,
                           SettingsKeys.signGeminiAbbreviationDefValue),
            settings.value(SettingsKeys.signCancerAbbreviationKey,
                           SettingsKeys.signCancerAbbreviationDefValue),
            settings.value(SettingsKeys.signLeoAbbreviationKey,
                           SettingsKeys.signLeoAbbreviationDefValue),
            settings.value(SettingsKeys.signVirgoAbbreviationKey,
                           SettingsKeys.signVirgoAbbreviationDefValue),
            settings.value(SettingsKeys.signLibraAbbreviationKey,
                           SettingsKeys.signLibraAbbreviationDefValue),
            settings.value(SettingsKeys.signScorpioAbbreviationKey,
                           SettingsKeys.signScorpioAbbreviationDefValue),
            settings.value(SettingsKeys.signSagittariusAbbreviationKey,
                           SettingsKeys.signSagittariusAbbreviationDefValue),
            settings.value(SettingsKeys.signCapricornAbbreviationKey,
                           SettingsKeys.signCapricornAbbreviationDefValue),
            settings.value(SettingsKeys.signAquariusAbbreviationKey,
                           SettingsKeys.signAquariusAbbreviationDefValue),
            settings.value(SettingsKeys.signPiscesAbbreviationKey,
                           SettingsKeys.signPiscesAbbreviationDefValue)]

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
        
        if planetName == "Ascendant":
            rv = settings.\
                value(SettingsKeys.planetAscendantGlyphUnicodeKey,
                      SettingsKeys.planetAscendantGlyphUnicodeDefValue)
        elif planetName == "Midheaven":
            rv = settings.\
                value(SettingsKeys.planetMidheavenGlyphUnicodeKey,
                      SettingsKeys.planetMidheavenGlyphUnicodeDefValue)
        elif planetName == "HoraLagna":
            rv = settings.\
                value(SettingsKeys.planetHoraLagnaGlyphUnicodeKey,
                      SettingsKeys.planetHoraLagnaGlyphUnicodeDefValue)
        elif planetName == "GhatiLagna":
            rv = settings.\
                value(SettingsKeys.planetGhatiLagnaGlyphUnicodeKey,
                      SettingsKeys.planetGhatiLagnaGlyphUnicodeDefValue)
        elif planetName == "MeanLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetMeanLunarApogeeGlyphUnicodeKey,
                      SettingsKeys.planetMeanLunarApogeeGlyphUnicodeDefValue)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeKey,
                      SettingsKeys.planetOsculatingLunarApogeeGlyphUnicodeDefValue)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeKey,
                      SettingsKeys.planetInterpolatedLunarApogeeGlyphUnicodeDefValue)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeKey,
                      SettingsKeys.planetInterpolatedLunarPerigeeGlyphUnicodeDefValue)
        elif planetName == "Sun":
            rv = settings.\
                value(SettingsKeys.planetSunGlyphUnicodeKey,
                      SettingsKeys.planetSunGlyphUnicodeDefValue)
        elif planetName == "Moon":
            rv = settings.\
                value(SettingsKeys.planetMoonGlyphUnicodeKey,
                      SettingsKeys.planetMoonGlyphUnicodeDefValue)
        elif planetName == "Mercury":
            rv = settings.\
                value(SettingsKeys.planetMercuryGlyphUnicodeKey,
                      SettingsKeys.planetMercuryGlyphUnicodeDefValue)
        elif planetName == "Venus":
            rv = settings.\
                value(SettingsKeys.planetVenusGlyphUnicodeKey,
                      SettingsKeys.planetVenusGlyphUnicodeDefValue)
        elif planetName == "Earth":
            rv = settings.\
                value(SettingsKeys.planetEarthGlyphUnicodeKey,
                      SettingsKeys.planetEarthGlyphUnicodeDefValue)
        elif planetName == "Mars":
            rv = settings.\
                value(SettingsKeys.planetMarsGlyphUnicodeKey,
                      SettingsKeys.planetMarsGlyphUnicodeDefValue)
        elif planetName == "Jupiter":
            rv = settings.\
                value(SettingsKeys.planetJupiterGlyphUnicodeKey,
                      SettingsKeys.planetJupiterGlyphUnicodeDefValue)
        elif planetName == "Saturn":
            rv = settings.\
                value(SettingsKeys.planetSaturnGlyphUnicodeKey,
                      SettingsKeys.planetSaturnGlyphUnicodeDefValue)
        elif planetName == "Uranus":
            rv = settings.\
                value(SettingsKeys.planetUranusGlyphUnicodeKey,
                      SettingsKeys.planetUranusGlyphUnicodeDefValue)
        elif planetName == "Neptune":
            rv = settings.\
                value(SettingsKeys.planetNeptuneGlyphUnicodeKey,
                      SettingsKeys.planetNeptuneGlyphUnicodeDefValue)
        elif planetName == "Pluto":
            rv = settings.\
                value(SettingsKeys.planetPlutoGlyphUnicodeKey,
                      SettingsKeys.planetPlutoGlyphUnicodeDefValue)
        elif planetName == "MeanNorthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanNorthNodeGlyphUnicodeKey,
                      SettingsKeys.planetMeanNorthNodeGlyphUnicodeDefValue)
        elif planetName == "MeanSouthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanSouthNodeGlyphUnicodeKey,
                      SettingsKeys.planetMeanSouthNodeGlyphUnicodeDefValue)
        elif planetName == "TrueNorthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueNorthNodeGlyphUnicodeKey,
                      SettingsKeys.planetTrueNorthNodeGlyphUnicodeDefValue)
        elif planetName == "TrueSouthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueSouthNodeGlyphUnicodeKey,
                      SettingsKeys.planetTrueSouthNodeGlyphUnicodeDefValue)
        elif planetName == "Ceres":
            rv = settings.\
                value(SettingsKeys.planetCeresGlyphUnicodeKey,
                      SettingsKeys.planetCeresGlyphUnicodeDefValue)
        elif planetName == "Pallas":
            rv = settings.\
                value(SettingsKeys.planetPallasGlyphUnicodeKey,
                      SettingsKeys.planetPallasGlyphUnicodeDefValue)
        elif planetName == "Juno":
            rv = settings.\
                value(SettingsKeys.planetJunoGlyphUnicodeKey,
                      SettingsKeys.planetJunoGlyphUnicodeDefValue)
        elif planetName == "Vesta":
            rv = settings.\
                value(SettingsKeys.planetVestaGlyphUnicodeKey,
                      SettingsKeys.planetVestaGlyphUnicodeDefValue)
        elif planetName == "Chiron":
            rv = settings.\
                value(SettingsKeys.planetChironGlyphUnicodeKey,
                      SettingsKeys.planetChironGlyphUnicodeDefValue)
        elif planetName == "Gulika":
            rv = settings.\
                value(SettingsKeys.planetGulikaGlyphUnicodeKey,
                      SettingsKeys.planetGulikaGlyphUnicodeDefValue)
        elif planetName == "Mandi":
            rv = settings.\
                value(SettingsKeys.planetMandiGlyphUnicodeKey,
                      SettingsKeys.planetMandiGlyphUnicodeDefValue)
        elif planetName == "MeanOfFive":
            rv = settings.\
                value(SettingsKeys.planetMeanOfFiveGlyphUnicodeKey,
                      SettingsKeys.planetMeanOfFiveGlyphUnicodeDefValue)
        elif planetName == "CycleOfEight":
            rv = settings.\
                value(SettingsKeys.planetCycleOfEightGlyphUnicodeKey,
                      SettingsKeys.planetCycleOfEightGlyphUnicodeDefValue)
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
        
        if planetName == "Ascendant":
            rv = float(settings.\
                value(SettingsKeys.planetAscendantGlyphFontSizeKey,
                      SettingsKeys.planetAscendantGlyphFontSizeDefValue))
        elif planetName == "Midheaven":
            rv = float(settings.\
                value(SettingsKeys.planetMidheavenGlyphFontSizeKey,
                      SettingsKeys.planetMidheavenGlyphFontSizeDefValue))
        elif planetName == "HoraLagna":
            rv = float(settings.\
                value(SettingsKeys.planetHoraLagnaGlyphFontSizeKey,
                      SettingsKeys.planetHoraLagnaGlyphFontSizeDefValue))
        elif planetName == "GhatiLagna":
            rv = float(settings.\
                value(SettingsKeys.planetGhatiLagnaGlyphFontSizeKey,
                      SettingsKeys.planetGhatiLagnaGlyphFontSizeDefValue))
        elif planetName == "MeanLunarApogee":
            rv = float(settings.\
                value(SettingsKeys.planetMeanLunarApogeeGlyphFontSizeKey,
                      SettingsKeys.planetMeanLunarApogeeGlyphFontSizeDefValue))
        elif planetName == "OsculatingLunarApogee":
            rv = float(settings.\
                value(SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeKey,
                      SettingsKeys.planetOsculatingLunarApogeeGlyphFontSizeDefValue))
        elif planetName == "InterpolatedLunarApogee":
            rv = float(settings.\
                value(SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeKey,
                      SettingsKeys.planetInterpolatedLunarApogeeGlyphFontSizeDefValue))
        elif planetName == "InterpolatedLunarPerigee":
            rv = float(settings.\
                value(SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeKey,
                      SettingsKeys.planetInterpolatedLunarPerigeeGlyphFontSizeDefValue))
        elif planetName == "Sun":
            rv = float(settings.\
                value(SettingsKeys.planetSunGlyphFontSizeKey,
                      SettingsKeys.planetSunGlyphFontSizeDefValue))
        elif planetName == "Moon":
            rv = float(settings.\
                value(SettingsKeys.planetMoonGlyphFontSizeKey,
                      SettingsKeys.planetMoonGlyphFontSizeDefValue))
        elif planetName == "Mercury":
            rv = float(settings.\
                value(SettingsKeys.planetMercuryGlyphFontSizeKey,
                      SettingsKeys.planetMercuryGlyphFontSizeDefValue))
        elif planetName == "Venus":
            rv = float(settings.\
                value(SettingsKeys.planetVenusGlyphFontSizeKey,
                      SettingsKeys.planetVenusGlyphFontSizeDefValue))
        elif planetName == "Earth":
            rv = float(settings.\
                value(SettingsKeys.planetEarthGlyphFontSizeKey,
                      SettingsKeys.planetEarthGlyphFontSizeDefValue))
        elif planetName == "Mars":
            rv = float(settings.\
                value(SettingsKeys.planetMarsGlyphFontSizeKey,
                      SettingsKeys.planetMarsGlyphFontSizeDefValue))
        elif planetName == "Jupiter":
            rv = float(settings.\
                value(SettingsKeys.planetJupiterGlyphFontSizeKey,
                      SettingsKeys.planetJupiterGlyphFontSizeDefValue))
        elif planetName == "Saturn":
            rv = float(settings.\
                value(SettingsKeys.planetSaturnGlyphFontSizeKey,
                      SettingsKeys.planetSaturnGlyphFontSizeDefValue))
        elif planetName == "Uranus":
            rv = float(settings.\
                value(SettingsKeys.planetUranusGlyphFontSizeKey,
                      SettingsKeys.planetUranusGlyphFontSizeDefValue))
        elif planetName == "Neptune":
            rv = float(settings.\
                value(SettingsKeys.planetNeptuneGlyphFontSizeKey,
                      SettingsKeys.planetNeptuneGlyphFontSizeDefValue))
        elif planetName == "Pluto":
            rv = float(settings.\
                value(SettingsKeys.planetPlutoGlyphFontSizeKey,
                      SettingsKeys.planetPlutoGlyphFontSizeDefValue))
        elif planetName == "MeanNorthNode":
            rv = float(settings.\
                value(SettingsKeys.planetMeanNorthNodeGlyphFontSizeKey,
                      SettingsKeys.planetMeanNorthNodeGlyphFontSizeDefValue))
        elif planetName == "MeanSouthNode":
            rv = float(settings.\
                value(SettingsKeys.planetMeanSouthNodeGlyphFontSizeKey,
                      SettingsKeys.planetMeanSouthNodeGlyphFontSizeDefValue))
        elif planetName == "TrueNorthNode":
            rv = float(settings.\
                value(SettingsKeys.planetTrueNorthNodeGlyphFontSizeKey,
                      SettingsKeys.planetTrueNorthNodeGlyphFontSizeDefValue))
        elif planetName == "TrueSouthNode":
            rv = float(settings.\
                value(SettingsKeys.planetTrueSouthNodeGlyphFontSizeKey,
                      SettingsKeys.planetTrueSouthNodeGlyphFontSizeDefValue))
        elif planetName == "Ceres":
            rv = float(settings.\
                value(SettingsKeys.planetCeresGlyphFontSizeKey,
                      SettingsKeys.planetCeresGlyphFontSizeDefValue))
        elif planetName == "Pallas":
            rv = float(settings.\
                value(SettingsKeys.planetPallasGlyphFontSizeKey,
                      SettingsKeys.planetPallasGlyphFontSizeDefValue))
        elif planetName == "Juno":
            rv = float(settings.\
                value(SettingsKeys.planetJunoGlyphFontSizeKey,
                      SettingsKeys.planetJunoGlyphFontSizeDefValue))
        elif planetName == "Vesta":
            rv = float(settings.\
                value(SettingsKeys.planetVestaGlyphFontSizeKey,
                      SettingsKeys.planetVestaGlyphFontSizeDefValue))
        elif planetName == "Chiron":
            rv = float(settings.\
                value(SettingsKeys.planetChironGlyphFontSizeKey,
                      SettingsKeys.planetChironGlyphFontSizeDefValue))
        elif planetName == "Gulika":
            rv = float(settings.\
                value(SettingsKeys.planetGulikaGlyphFontSizeKey,
                      SettingsKeys.planetGulikaGlyphFontSizeDefValue))
        elif planetName == "Mandi":
            rv = float(settings.\
                value(SettingsKeys.planetMandiGlyphFontSizeKey,
                      SettingsKeys.planetMandiGlyphFontSizeDefValue))
        elif planetName == "MeanOfFive":
            rv = float(settings.\
                value(SettingsKeys.planetMeanOfFiveGlyphFontSizeKey,
                      SettingsKeys.planetMeanOfFiveGlyphFontSizeDefValue))
        elif planetName == "CycleOfEight":
            rv = float(settings.\
                value(SettingsKeys.planetCycleOfEightGlyphFontSizeKey,
                      SettingsKeys.planetCycleOfEightGlyphFontSizeDefValue))
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
        
        if planetName == "Ascendant":
            rv = settings.\
                value(SettingsKeys.planetAscendantAbbreviationKey,
                      SettingsKeys.planetAscendantAbbreviationDefValue)
        elif planetName == "Midheaven":
            rv = settings.\
                value(SettingsKeys.planetMidheavenAbbreviationKey,
                      SettingsKeys.planetMidheavenAbbreviationDefValue)
        elif planetName == "HoraLagna":
            rv = settings.\
                value(SettingsKeys.planetHoraLagnaAbbreviationKey,
                      SettingsKeys.planetHoraLagnaAbbreviationDefValue)
        elif planetName == "GhatiLagna":
            rv = settings.\
                value(SettingsKeys.planetGhatiLagnaAbbreviationKey,
                      SettingsKeys.planetGhatiLagnaAbbreviationDefValue)
        elif planetName == "MeanLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetMeanLunarApogeeAbbreviationKey,
                      SettingsKeys.planetMeanLunarApogeeAbbreviationDefValue)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetOsculatingLunarApogeeAbbreviationKey,
                      SettingsKeys.planetOsculatingLunarApogeeAbbreviationDefValue)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarApogeeAbbreviationKey,
                      SettingsKeys.planetInterpolatedLunarApogeeAbbreviationDefValue)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationKey,
                      SettingsKeys.planetInterpolatedLunarPerigeeAbbreviationDefValue)
        elif planetName == "Sun":
            rv = settings.\
                value(SettingsKeys.planetSunAbbreviationKey,
                      SettingsKeys.planetSunAbbreviationDefValue)
        elif planetName == "Moon":
            rv = settings.\
                value(SettingsKeys.planetMoonAbbreviationKey,
                      SettingsKeys.planetMoonAbbreviationDefValue)
        elif planetName == "Mercury":
            rv = settings.\
                value(SettingsKeys.planetMercuryAbbreviationKey,
                      SettingsKeys.planetMercuryAbbreviationDefValue)
        elif planetName == "Venus":
            rv = settings.\
                value(SettingsKeys.planetVenusAbbreviationKey,
                      SettingsKeys.planetVenusAbbreviationDefValue)
        elif planetName == "Earth":
            rv = settings.\
                value(SettingsKeys.planetEarthAbbreviationKey,
                      SettingsKeys.planetEarthAbbreviationDefValue)
        elif planetName == "Mars":
            rv = settings.\
                value(SettingsKeys.planetMarsAbbreviationKey,
                      SettingsKeys.planetMarsAbbreviationDefValue)
        elif planetName == "Jupiter":
            rv = settings.\
                value(SettingsKeys.planetJupiterAbbreviationKey,
                      SettingsKeys.planetJupiterAbbreviationDefValue)
        elif planetName == "Saturn":
            rv = settings.\
                value(SettingsKeys.planetSaturnAbbreviationKey,
                      SettingsKeys.planetSaturnAbbreviationDefValue)
        elif planetName == "Uranus":
            rv = settings.\
                value(SettingsKeys.planetUranusAbbreviationKey,
                      SettingsKeys.planetUranusAbbreviationDefValue)
        elif planetName == "Neptune":
            rv = settings.\
                value(SettingsKeys.planetNeptuneAbbreviationKey,
                      SettingsKeys.planetNeptuneAbbreviationDefValue)
        elif planetName == "Pluto":
            rv = settings.\
                value(SettingsKeys.planetPlutoAbbreviationKey,
                      SettingsKeys.planetPlutoAbbreviationDefValue)
        elif planetName == "MeanNorthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanNorthNodeAbbreviationKey,
                      SettingsKeys.planetMeanNorthNodeAbbreviationDefValue)
        elif planetName == "MeanSouthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanSouthNodeAbbreviationKey,
                      SettingsKeys.planetMeanSouthNodeAbbreviationDefValue)
        elif planetName == "TrueNorthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueNorthNodeAbbreviationKey,
                      SettingsKeys.planetTrueNorthNodeAbbreviationDefValue)
        elif planetName == "TrueSouthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueSouthNodeAbbreviationKey,
                      SettingsKeys.planetTrueSouthNodeAbbreviationDefValue)
        elif planetName == "Ceres":
            rv = settings.\
                value(SettingsKeys.planetCeresAbbreviationKey,
                      SettingsKeys.planetCeresAbbreviationDefValue)
        elif planetName == "Pallas":
            rv = settings.\
                value(SettingsKeys.planetPallasAbbreviationKey,
                      SettingsKeys.planetPallasAbbreviationDefValue)
        elif planetName == "Juno":
            rv = settings.\
                value(SettingsKeys.planetJunoAbbreviationKey,
                      SettingsKeys.planetJunoAbbreviationDefValue)
        elif planetName == "Vesta":
            rv = settings.\
                value(SettingsKeys.planetVestaAbbreviationKey,
                      SettingsKeys.planetVestaAbbreviationDefValue)
        elif planetName == "Chiron":
            rv = settings.\
                value(SettingsKeys.planetChironAbbreviationKey,
                      SettingsKeys.planetChironAbbreviationDefValue)
        elif planetName == "Gulika":
            rv = settings.\
                value(SettingsKeys.planetGulikaAbbreviationKey,
                      SettingsKeys.planetGulikaAbbreviationDefValue)
        elif planetName == "Mandi":
            rv = settings.\
                value(SettingsKeys.planetMandiAbbreviationKey,
                      SettingsKeys.planetMandiAbbreviationDefValue)
        elif planetName == "MeanOfFive":
            rv = settings.\
                value(SettingsKeys.planetMeanOfFiveAbbreviationKey,
                      SettingsKeys.planetMeanOfFiveAbbreviationDefValue)
        elif planetName == "CycleOfEight":
            rv = settings.\
                value(SettingsKeys.planetCycleOfEightAbbreviationKey,
                      SettingsKeys.planetCycleOfEightAbbreviationDefValue)
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
        
        if planetName == "Ascendant":
            rv = settings.\
                value(SettingsKeys.planetAscendantForegroundColorKey,
                      SettingsKeys.planetAscendantForegroundColorDefValue)
        elif planetName == "Midheaven":
            rv = settings.\
                value(SettingsKeys.planetMidheavenForegroundColorKey,
                      SettingsKeys.planetMidheavenForegroundColorDefValue)
        elif planetName == "HoraLagna":
            rv = settings.\
                value(SettingsKeys.planetHoraLagnaForegroundColorKey,
                      SettingsKeys.planetHoraLagnaForegroundColorDefValue)
        elif planetName == "GhatiLagna":
            rv = settings.\
                value(SettingsKeys.planetGhatiLagnaForegroundColorKey,
                      SettingsKeys.planetGhatiLagnaForegroundColorDefValue)
        elif planetName == "MeanLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetMeanLunarApogeeForegroundColorKey,
                      SettingsKeys.planetMeanLunarApogeeForegroundColorDefValue)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetOsculatingLunarApogeeForegroundColorKey,
                      SettingsKeys.planetOsculatingLunarApogeeForegroundColorDefValue)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarApogeeForegroundColorKey,
                      SettingsKeys.planetInterpolatedLunarApogeeForegroundColorDefValue)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorKey,
                      SettingsKeys.planetInterpolatedLunarPerigeeForegroundColorDefValue)
        elif planetName == "Sun":
            rv = settings.\
                value(SettingsKeys.planetSunForegroundColorKey,
                      SettingsKeys.planetSunForegroundColorDefValue)
        elif planetName == "Moon":
            rv = settings.\
                value(SettingsKeys.planetMoonForegroundColorKey,
                      SettingsKeys.planetMoonForegroundColorDefValue)
        elif planetName == "Mercury":
            rv = settings.\
                value(SettingsKeys.planetMercuryForegroundColorKey,
                      SettingsKeys.planetMercuryForegroundColorDefValue)
        elif planetName == "Venus":
            rv = settings.\
                value(SettingsKeys.planetVenusForegroundColorKey,
                      SettingsKeys.planetVenusForegroundColorDefValue)
        elif planetName == "Earth":
            rv = settings.\
                value(SettingsKeys.planetEarthForegroundColorKey,
                      SettingsKeys.planetEarthForegroundColorDefValue)
        elif planetName == "Mars":
            rv = settings.\
                value(SettingsKeys.planetMarsForegroundColorKey,
                      SettingsKeys.planetMarsForegroundColorDefValue)
        elif planetName == "Jupiter":
            rv = settings.\
                value(SettingsKeys.planetJupiterForegroundColorKey,
                      SettingsKeys.planetJupiterForegroundColorDefValue)
        elif planetName == "Saturn":
            rv = settings.\
                value(SettingsKeys.planetSaturnForegroundColorKey,
                      SettingsKeys.planetSaturnForegroundColorDefValue)
        elif planetName == "Uranus":
            rv = settings.\
                value(SettingsKeys.planetUranusForegroundColorKey,
                      SettingsKeys.planetUranusForegroundColorDefValue)
        elif planetName == "Neptune":
            rv = settings.\
                value(SettingsKeys.planetNeptuneForegroundColorKey,
                      SettingsKeys.planetNeptuneForegroundColorDefValue)
        elif planetName == "Pluto":
            rv = settings.\
                value(SettingsKeys.planetPlutoForegroundColorKey,
                      SettingsKeys.planetPlutoForegroundColorDefValue)
        elif planetName == "MeanNorthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanNorthNodeForegroundColorKey,
                      SettingsKeys.planetMeanNorthNodeForegroundColorDefValue)
        elif planetName == "MeanSouthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanSouthNodeForegroundColorKey,
                      SettingsKeys.planetMeanSouthNodeForegroundColorDefValue)
        elif planetName == "TrueNorthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueNorthNodeForegroundColorKey,
                      SettingsKeys.planetTrueNorthNodeForegroundColorDefValue)
        elif planetName == "TrueSouthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueSouthNodeForegroundColorKey,
                      SettingsKeys.planetTrueSouthNodeForegroundColorDefValue)
        elif planetName == "Ceres":
            rv = settings.\
                value(SettingsKeys.planetCeresForegroundColorKey,
                      SettingsKeys.planetCeresForegroundColorDefValue)
        elif planetName == "Pallas":
            rv = settings.\
                value(SettingsKeys.planetPallasForegroundColorKey,
                      SettingsKeys.planetPallasForegroundColorDefValue)
        elif planetName == "Juno":
            rv = settings.\
                value(SettingsKeys.planetJunoForegroundColorKey,
                      SettingsKeys.planetJunoForegroundColorDefValue)
        elif planetName == "Vesta":
            rv = settings.\
                value(SettingsKeys.planetVestaForegroundColorKey,
                      SettingsKeys.planetVestaForegroundColorDefValue)
        elif planetName == "Chiron":
            rv = settings.\
                value(SettingsKeys.planetChironForegroundColorKey,
                      SettingsKeys.planetChironForegroundColorDefValue)
        elif planetName == "Gulika":
            rv = settings.\
                value(SettingsKeys.planetGulikaForegroundColorKey,
                      SettingsKeys.planetGulikaForegroundColorDefValue)
        elif planetName == "Mandi":
            rv = settings.\
                value(SettingsKeys.planetMandiForegroundColorKey,
                      SettingsKeys.planetMandiForegroundColorDefValue)
        elif planetName == "MeanOfFive":
            rv = settings.\
                value(SettingsKeys.planetMeanOfFiveForegroundColorKey,
                      SettingsKeys.planetMeanOfFiveForegroundColorDefValue)
        elif planetName == "CycleOfEight":
            rv = settings.\
                value(SettingsKeys.planetCycleOfEightForegroundColorKey,
                      SettingsKeys.planetCycleOfEightForegroundColorDefValue)
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
        
        if planetName == "Ascendant":
            rv = settings.\
                value(SettingsKeys.planetAscendantBackgroundColorKey,
                      SettingsKeys.planetAscendantBackgroundColorDefValue)
        elif planetName == "Midheaven":
            rv = settings.\
                value(SettingsKeys.planetMidheavenBackgroundColorKey,
                      SettingsKeys.planetMidheavenBackgroundColorDefValue)
        elif planetName == "HoraLagna":
            rv = settings.\
                value(SettingsKeys.planetHoraLagnaBackgroundColorKey,
                      SettingsKeys.planetHoraLagnaBackgroundColorDefValue)
        elif planetName == "GhatiLagna":
            rv = settings.\
                value(SettingsKeys.planetGhatiLagnaBackgroundColorKey,
                      SettingsKeys.planetGhatiLagnaBackgroundColorDefValue)
        elif planetName == "MeanLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetMeanLunarApogeeBackgroundColorKey,
                      SettingsKeys.planetMeanLunarApogeeBackgroundColorDefValue)
        elif planetName == "OsculatingLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetOsculatingLunarApogeeBackgroundColorKey,
                      SettingsKeys.planetOsculatingLunarApogeeBackgroundColorDefValue)
        elif planetName == "InterpolatedLunarApogee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorKey,
                      SettingsKeys.planetInterpolatedLunarApogeeBackgroundColorDefValue)
        elif planetName == "InterpolatedLunarPerigee":
            rv = settings.\
                value(SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorKey,
                      SettingsKeys.planetInterpolatedLunarPerigeeBackgroundColorDefValue)
        elif planetName == "Sun":
            rv = settings.\
                value(SettingsKeys.planetSunBackgroundColorKey,
                      SettingsKeys.planetSunBackgroundColorDefValue)
        elif planetName == "Moon":
            rv = settings.\
                value(SettingsKeys.planetMoonBackgroundColorKey,
                      SettingsKeys.planetMoonBackgroundColorDefValue)
        elif planetName == "Mercury":
            rv = settings.\
                value(SettingsKeys.planetMercuryBackgroundColorKey,
                      SettingsKeys.planetMercuryBackgroundColorDefValue)
        elif planetName == "Venus":
            rv = settings.\
                value(SettingsKeys.planetVenusBackgroundColorKey,
                      SettingsKeys.planetVenusBackgroundColorDefValue)
        elif planetName == "Earth":
            rv = settings.\
                value(SettingsKeys.planetEarthBackgroundColorKey,
                      SettingsKeys.planetEarthBackgroundColorDefValue)
        elif planetName == "Mars":
            rv = settings.\
                value(SettingsKeys.planetMarsBackgroundColorKey,
                      SettingsKeys.planetMarsBackgroundColorDefValue)
        elif planetName == "Jupiter":
            rv = settings.\
                value(SettingsKeys.planetJupiterBackgroundColorKey,
                      SettingsKeys.planetJupiterBackgroundColorDefValue)
        elif planetName == "Saturn":
            rv = settings.\
                value(SettingsKeys.planetSaturnBackgroundColorKey,
                      SettingsKeys.planetSaturnBackgroundColorDefValue)
        elif planetName == "Uranus":
            rv = settings.\
                value(SettingsKeys.planetUranusBackgroundColorKey,
                      SettingsKeys.planetUranusBackgroundColorDefValue)
        elif planetName == "Neptune":
            rv = settings.\
                value(SettingsKeys.planetNeptuneBackgroundColorKey,
                      SettingsKeys.planetNeptuneBackgroundColorDefValue)
        elif planetName == "Pluto":
            rv = settings.\
                value(SettingsKeys.planetPlutoBackgroundColorKey,
                      SettingsKeys.planetPlutoBackgroundColorDefValue)
        elif planetName == "MeanNorthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanNorthNodeBackgroundColorKey,
                      SettingsKeys.planetMeanNorthNodeBackgroundColorDefValue)
        elif planetName == "MeanSouthNode":
            rv = settings.\
                value(SettingsKeys.planetMeanSouthNodeBackgroundColorKey,
                      SettingsKeys.planetMeanSouthNodeBackgroundColorDefValue)
        elif planetName == "TrueNorthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueNorthNodeBackgroundColorKey,
                      SettingsKeys.planetTrueNorthNodeBackgroundColorDefValue)
        elif planetName == "TrueSouthNode":
            rv = settings.\
                value(SettingsKeys.planetTrueSouthNodeBackgroundColorKey,
                      SettingsKeys.planetTrueSouthNodeBackgroundColorDefValue)
        elif planetName == "Ceres":
            rv = settings.\
                value(SettingsKeys.planetCeresBackgroundColorKey,
                      SettingsKeys.planetCeresBackgroundColorDefValue)
        elif planetName == "Pallas":
            rv = settings.\
                value(SettingsKeys.planetPallasBackgroundColorKey,
                      SettingsKeys.planetPallasBackgroundColorDefValue)
        elif planetName == "Juno":
            rv = settings.\
                value(SettingsKeys.planetJunoBackgroundColorKey,
                      SettingsKeys.planetJunoBackgroundColorDefValue)
        elif planetName == "Vesta":
            rv = settings.\
                value(SettingsKeys.planetVestaBackgroundColorKey,
                      SettingsKeys.planetVestaBackgroundColorDefValue)
        elif planetName == "Chiron":
            rv = settings.\
                value(SettingsKeys.planetChironBackgroundColorKey,
                      SettingsKeys.planetChironBackgroundColorDefValue)
        elif planetName == "Gulika":
            rv = settings.\
                value(SettingsKeys.planetGulikaBackgroundColorKey,
                      SettingsKeys.planetGulikaBackgroundColorDefValue)
        elif planetName == "Mandi":
            rv = settings.\
                value(SettingsKeys.planetMandiBackgroundColorKey,
                      SettingsKeys.planetMandiBackgroundColorDefValue)
        elif planetName == "MeanOfFive":
            rv = settings.\
                value(SettingsKeys.planetMeanOfFiveBackgroundColorKey,
                      SettingsKeys.planetMeanOfFiveBackgroundColorDefValue)
        elif planetName == "CycleOfEight":
            rv = settings.\
                value(SettingsKeys.planetCycleOfEightBackgroundColorKey,
                      SettingsKeys.planetCycleOfEightBackgroundColorDefValue)
        else:
            rv = QColor(Qt.transparent)
            self.log.warn("Could not find background color for planet: " + \
                          planetName + ".  Using default value " + str(rv))

        return rv
    
    
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

        # TODO:  Decide if I should always return terminalRadiusForWheelNumber at 0.0.
        return rv
    
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
        #                   SettingsKeys.planetRetrogradeGlyphUnicodeDefValue)
        #self.planetRetrogradeGlyphFontSize = \
        #    settings.value(SettingsKeys.planetRetrogradeGlyphFontSizeKey,
        #                   SettingsKeys.planetRetrogradeGlyphFontSizeDefValue)
        
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

    def load(self, planetaryInfos):
        """Loads the widgets with the given list of PlanetaryInfo
        objects.
        """
        
        self.log.debug("Entered load()")

        self.setRowCount(len(planetaryInfos))
        self.clearContents()

        for i in range(len(planetaryInfos)):

            p = planetaryInfos[i]

            if i >= len(self.planetaryInfos):
                self._appendPlanetaryInfo(p)
            else:
                self._replaceRowWithPlanetaryInfo(i, p)

        self.planetaryInfos = planetaryInfos

        self.log.debug("Exiting load()")

    def sizeHint(self):
        """Overwrites QWidget.sizeHint() to make the widget display
        all columns without requiring a scrollbar.
        """

        return QSize(1180, 640)
    
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
            float(settings.value(SettingsKeys.zoomScaleFactorSettingsKey, \
                                 SettingsKeys.zoomScaleFactorSettingsDefValue))
        
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

        # Create the QGraphicsView and QGraphicsScene for the display portion.
        self.graphicsScene = QGraphicsScene()
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

        # TODO:  Uncomment below to re-add PlanetaryInfoTableGraphicsItem().  It's left out because it doesn't add much value and is slow.
        #self.planetaryInfoTable = PlanetaryInfoTableGraphicsItem()
        
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

        x = 0.0
        y = 0.0
        y += 0.5 * radixLength
        x += 0.5 * radixLength
        #self.planetaryInfoTable.setPos(x, y)

        
        # Add all the items to the QGraphicsScene.
        self.graphicsScene.addItem(self.locationLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart1DatetimeLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart2DatetimeLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart3DatetimeLabelProxyWidget)
    
        self.graphicsScene.addItem(self.declinationChart)
        
        #self.graphicsScene.addItem(self.planetaryInfoTable)
        
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

    def _getPlanetaryInfosForDatetime(self, dt):
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
        
        p = Ephemeris.getSunPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMoonPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMercuryPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getVenusPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMarsPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getJupiterPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getSaturnPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getUranusPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getNeptunePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getPlutoPlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMeanNorthNodePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getTrueNorthNodePlanetaryInfo(dt)
        planets.append(p)
        p = Ephemeris.getMeanLunarApogeePlanetaryInfo(dt)
        planets.append(p)
        #p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(dt)
        #planets.append(p)
        #p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(dt)
        #planets.append(p)
        #p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(dt)
        #planets.append(p)
        p = Ephemeris.getEarthPlanetaryInfo(dt)
        planets.append(p)
        #p = Ephemeris.getChironPlanetaryInfo(dt)
        #planets.append(p)
        
        return planets

    def _getPlanetNamesToDisplayForDeclination(self):
        """Function to return a list of planet names that should be
        used to display declination information.  This is used because
        some planets don't make sense to chart on declination and it
        just clouds up the view..
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
             "Pluto"]

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
        planets = self._getPlanetaryInfosForDatetime(dt)

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
            radixPlanetGraphicsItem = \
                self.geoSidRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
            if radixPlanetGraphicsItem == None:
                # No RadixPlanetGraphicsItem exists for this planet yet,
                # so create it.

                # Get all the info needed to create it.
                glyph = \
                    AstrologyUtils.getGlyphForPlanetName(planet.name)
                fontSize = \
                    AstrologyUtils.getGlyphFontSizeForPlanetName(planet.name)
                abbrev = \
                    AstrologyUtils.getAbbreviationForPlanetName(planet.name)
                foregroundColor = \
                    AstrologyUtils.getForegroundColorForPlanetName(planet.name)
                backgroundColor = \
                    AstrologyUtils.getBackgroundColorForPlanetName(planet.name)
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
                
                radixPlanetGraphicsItem.setDegreeAndVelocity(degree, velocity)


            # Geocentric Tropical.
            radixPlanetGraphicsItem = \
                self.geoTropRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
            if radixPlanetGraphicsItem == None:
                # No RadixPlanetGraphicsItem exists for this planet yet,
                # so create it.

                # Get all the info needed to create it.
                glyph = \
                    AstrologyUtils.getGlyphForPlanetName(planet.name)
                fontSize = \
                    AstrologyUtils.getGlyphFontSizeForPlanetName(planet.name)
                abbrev = \
                    AstrologyUtils.getAbbreviationForPlanetName(planet.name)
                foregroundColor = \
                    AstrologyUtils.getForegroundColorForPlanetName(planet.name)
                backgroundColor = \
                    AstrologyUtils.getBackgroundColorForPlanetName(planet.name)
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
                
                radixPlanetGraphicsItem.setDegreeAndVelocity(degree, velocity)

            # Heliocentric Sidereal.
            radixPlanetGraphicsItem = \
                self.helioSidRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
            if radixPlanetGraphicsItem == None:
                # No RadixPlanetGraphicsItem exists for this planet yet,
                # so create it.

                # Get all the info needed to create it.
                glyph = \
                    AstrologyUtils.getGlyphForPlanetName(planet.name)
                fontSize = \
                    AstrologyUtils.getGlyphFontSizeForPlanetName(planet.name)
                abbrev = \
                    AstrologyUtils.getAbbreviationForPlanetName(planet.name)
                foregroundColor = \
                    AstrologyUtils.getForegroundColorForPlanetName(planet.name)
                backgroundColor = \
                    AstrologyUtils.getBackgroundColorForPlanetName(planet.name)
                degree = planet.heliocentric['sidereal']['longitude']
                velocity = planet.heliocentric['sidereal']['longitude_speed']
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
                degree = planet.heliocentric['sidereal']['longitude']
                velocity = planet.heliocentric['sidereal']['longitude_speed']
                
                radixPlanetGraphicsItem.setDegreeAndVelocity(degree, velocity)

            
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
        planets = self._getPlanetaryInfosForDatetime(\
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
    

        
