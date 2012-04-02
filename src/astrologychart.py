
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

    # Logger object for this class.
    log = logging.getLogger("astrologychart.AstrologyUtils")

    # Number of degrees in a Biblical Circle. (float)
    degreesInBiblicalCircle = 368.18

    # Number of degrees in a 360-degree Circle. (float)
    degreesInCircle = 360.0


    @staticmethod
    def convertLongitudeToNavamsaStr(longitude):
        """Takes a float longitude value and converts it to a str that
        holds the glyph corresponding to its navamsa rasi.

        Arguments:
        longitude - float value for the longitude of the planet.

        Returns:
        str value holding the navamsa rasi glyph.
        """

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

        #signAbbreviations = [\
        #    settings.value(SettingsKeys.signAriesAbbreviationKey,
        #                   SettingsKeys.signAriesAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signTaurusAbbreviationKey,
        #                   SettingsKeys.signTaurusAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signGeminiAbbreviationKey,
        #                   SettingsKeys.signGeminiAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signCancerAbbreviationKey,
        #                   SettingsKeys.signCancerAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signLeoAbbreviationKey,
        #                   SettingsKeys.signLeoAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signVirgoAbbreviationKey,
        #                   SettingsKeys.signVirgoAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signLibraAbbreviationKey,
        #                   SettingsKeys.signLibraAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signScorpioAbbreviationKey,
        #                   SettingsKeys.signScorpioAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signSagittariusAbbreviationKey,
        #                   SettingsKeys.signSagittariusAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signCapricornAbbreviationKey,
        #                   SettingsKeys.signCapricornAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signAquariusAbbreviationKey,
        #                   SettingsKeys.signAquariusAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signPiscesAbbreviationKey,
        #                   SettingsKeys.signPiscesAbbreviationDefValue,
        #                   type=str)]
        
        navamsaSize = 360 / 108.0
        index = math.floor(longitude / navamsaSize) % 12
        
        return signGlyphs[index]
        
    @staticmethod
    def convertLongitudeToStrWithRasiAbbrev(longitude):
        """Takes a float longitude value and converts it to a str
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
        
        #signAbbreviations = [\
        #    settings.value(SettingsKeys.signAriesAbbreviationKey,
        #                   SettingsKeys.signAriesAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signTaurusAbbreviationKey,
        #                   SettingsKeys.signTaurusAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signGeminiAbbreviationKey,
        #                   SettingsKeys.signGeminiAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signCancerAbbreviationKey,
        #                   SettingsKeys.signCancerAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signLeoAbbreviationKey,
        #                   SettingsKeys.signLeoAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signVirgoAbbreviationKey,
        #                   SettingsKeys.signVirgoAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signLibraAbbreviationKey,
        #                   SettingsKeys.signLibraAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signScorpioAbbreviationKey,
        #                   SettingsKeys.signScorpioAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signSagittariusAbbreviationKey,
        #                   SettingsKeys.signSagittariusAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signCapricornAbbreviationKey,
        #                   SettingsKeys.signCapricornAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signAquariusAbbreviationKey,
        #                   SettingsKeys.signAquariusAbbreviationDefValue,
        #                   type=str),
        #    settings.value(SettingsKeys.signPiscesAbbreviationKey,
        #                   SettingsKeys.signPiscesAbbreviationDefValue,
        #                   type=str)]
        
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
    def convertAngleToStrWithRasiAbbrev(longitude):
        """Alias of convertLongitudeToStrWithRasiAbbrev(longitude)."""

        return AstrologyUtils.convertLongitudeToStrWithRasiAbbrev(longitude)
        
    @staticmethod
    def convertLongitudeToNakshatraAbbrev(longitude):
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

        nakshatraSize = 360 / 27.0
        index = math.floor(longitude / nakshatraSize)
        
        return nakshatraAbbrevs[index]

    @staticmethod
    def convertCircleAngleToBiblicalCircleAngle(angle):
        """Converts the given angle in degrees of a 360-degree circle,
        to an angle in degrees of a 368 degree 10 minute 48 second
        circle (A.K.A Biblical Circle).

        Arguments:
        angle - float value for the angle in units of degrees in a
                360-degree circle.

        Returns:
        float value for the angle in units of degrees in a
        368 deg 10' 48" Biblical circle.
        """

        
        proportionOfCircle = \
            angle / AstrologyUtils.degreesInCircle

        biblicalAngle = \
            proportionOfCircle * AstrologyUtils.degreesInBiblicalCircle
        
        return biblicalAngle
    
    @staticmethod
    def convertBiblicalCircleAngleToCircleAngle(biblicalAngle):
        """Converts the given angle in degrees of a 368 degree 10
        minute 48 second circle (A.K.A Biblical Circle) to an angle in
        degrees of a 360-degree circle.

        Arguments:
        biblicalAngle - float value for the angle in units of degrees in a
                        368 deg 10' 48" Biblical circle.

        Returns:
        float value for the angle in units of degrees in a 360-degree circle.
        """

        
        proportionOfCircle = \
            biblicalAngle / AstrologyUtils.degreesInBiblicalCircle

        angle = \
            proportionOfCircle * AstrologyUtils.degreesInCircle
        
        return angle
    
    @staticmethod
    def convertBiblicalCircleAngleToStrWithRasiAbbrev(biblicalAngle):
        """Takes a angle in Biblical degrees and converts it to a string
        in the format: 23 <RASI_GLYPH> 24' 14" that represents the
        zodiac location for that angle.
        
        Arguments:
        biblicalAngle - float value for the angle in units of degrees in a
                        368 deg 10' 48" Biblical circle.

        Returns:
        str - String that is in the above format.  It will always be a
        fixed number of characters.  This means that if it is 8
        degrees, or 8 minutes, or 8 seconds, the string will have a
        space prefixing the 8.
        """

        angle = \
            AstrologyUtils.convertBiblicalCircleAngleToCircleAngle(\
            biblicalAngle)

        return AstrologyUtils.convertLongitudeToStrWithRasiAbbrev(angle)

    @staticmethod
    def convertDegMinSecToAngle(degrees, minutes, seconds):
        """Converts the given degrees, minutes and seconds into a
        float value representing the same angle.

        Arguments:
        degrees - int value for the degrees of the angle.  This may be negative.
        minutes - int value for the minutes of the angle.
        minutes - int value for the seconds of the angle.
        """

        angle = degrees + (minutes / 60) + (seconds / 3600)

        return angle
        
    @staticmethod
    def convertAngleToDegMinSec(angle):
        """Converts the given angle as a float and returns a tuple of
        int values containing the equivalent amount of degrees,
        minutes and seconds.
        
        Arguments:
        angle - float value holding the angle to convert.

        Returns:
        tuple of 3 ints (degrees, minutes, seconds), that represent the angle.
        """

        degrees = int(math.floor(angle))

        leftOver1 = 60.0 * (angle - degrees)
        minutes = int(math.floor(leftOver1))

        leftOver2 = 60.0 * (leftOver1 - minutes)
        seconds = int(round(leftOver2))

        # Handle roll-over due to seconds rounding up to 60.
        if seconds == 60:
            minutes += 1
            seconds = 0

            if minutes == 60:
                degrees += 1
                minutes = 0

        return (degrees, minutes, seconds)
        
    @staticmethod
    def convertAngleToDegMinSecStr(angle):
        """Converts the given angle as a float and returns a str that
        is the value in the format:  XXX° YY' ZZ"
        
        If the angle does not fill the digits, a space will be used so
        that the output is fixed width.
        
        Arguments:
        angle - float value holding the angle to convert.

        Returns:
        str value holding the converted angle with degrees, minutes
        and seconds printed.
        """

        (degrees, minutes, seconds) = \
            AstrologyUtils.convertAngleToDegMinSec(angle)

        rv = "{:>3}° {:>2}' {:>2}\"".format(degrees, minutes, seconds)

        return rv
        
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
        
        if planetName == "H1":
            rv = settings.value(SettingsKeys.planetH1GlyphUnicodeKey,
                                SettingsKeys.planetH1GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H2":
            rv = settings.value(SettingsKeys.planetH2GlyphUnicodeKey,
                                SettingsKeys.planetH2GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H3":
            rv = settings.value(SettingsKeys.planetH3GlyphUnicodeKey,
                                SettingsKeys.planetH3GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H4":
            rv = settings.value(SettingsKeys.planetH4GlyphUnicodeKey,
                                SettingsKeys.planetH4GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H5":
            rv = settings.value(SettingsKeys.planetH5GlyphUnicodeKey,
                                SettingsKeys.planetH5GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H6":
            rv = settings.value(SettingsKeys.planetH6GlyphUnicodeKey,
                                SettingsKeys.planetH6GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H7":
            rv = settings.value(SettingsKeys.planetH7GlyphUnicodeKey,
                                SettingsKeys.planetH7GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H8":
            rv = settings.value(SettingsKeys.planetH8GlyphUnicodeKey,
                                SettingsKeys.planetH8GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H9":
            rv = settings.value(SettingsKeys.planetH9GlyphUnicodeKey,
                                SettingsKeys.planetH9GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H10":
            rv = settings.value(SettingsKeys.planetH10GlyphUnicodeKey,
                                SettingsKeys.planetH10GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H11":
            rv = settings.value(SettingsKeys.planetH11GlyphUnicodeKey,
                                SettingsKeys.planetH11GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "H12":
            rv = settings.value(SettingsKeys.planetH12GlyphUnicodeKey,
                                SettingsKeys.planetH12GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "ARMC":
            rv = settings.value(SettingsKeys.planetARMCGlyphUnicodeKey,
                                SettingsKeys.planetARMCGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Vertex":
            rv = settings.value(SettingsKeys.planetVertexGlyphUnicodeKey,
                                SettingsKeys.planetVertexGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "EquatorialAscendant":
            rv = settings.value(SettingsKeys.planetEquatorialAscendantGlyphUnicodeKey,
                                SettingsKeys.planetEquatorialAscendantGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "CoAscendant1":
            rv = settings.value(SettingsKeys.planetCoAscendant1GlyphUnicodeKey,
                                SettingsKeys.planetCoAscendant1GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "CoAscendant2":
            rv = settings.value(SettingsKeys.planetCoAscendant2GlyphUnicodeKey,
                                SettingsKeys.planetCoAscendant2GlyphUnicodeDefValue,
                                type=str)
        elif planetName == "PolarAscendant":
            rv = settings.value(SettingsKeys.planetPolarAscendantGlyphUnicodeKey,
                                SettingsKeys.planetPolarAscendantGlyphUnicodeDefValue,
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
        elif planetName == "Isis":
            rv = settings.value(SettingsKeys.planetIsisGlyphUnicodeKey,
                                SettingsKeys.planetIsisGlyphUnicodeDefValue,
                                type=str)
        elif planetName == "Nibiru":
            rv = settings.value(SettingsKeys.planetNibiruGlyphUnicodeKey,
                                SettingsKeys.planetNibiruGlyphUnicodeDefValue,
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
            AstrologyUtils.log.warn("Could not find glyph for planet: " + \
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
        
        if planetName == "H1":
            rv = settings.value(SettingsKeys.planetH1GlyphFontSizeKey,
                                SettingsKeys.planetH1GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H2":
            rv = settings.value(SettingsKeys.planetH2GlyphFontSizeKey,
                                SettingsKeys.planetH2GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H3":
            rv = settings.value(SettingsKeys.planetH3GlyphFontSizeKey,
                                SettingsKeys.planetH3GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H4":
            rv = settings.value(SettingsKeys.planetH4GlyphFontSizeKey,
                                SettingsKeys.planetH4GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H5":
            rv = settings.value(SettingsKeys.planetH5GlyphFontSizeKey,
                                SettingsKeys.planetH5GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H6":
            rv = settings.value(SettingsKeys.planetH6GlyphFontSizeKey,
                                SettingsKeys.planetH6GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H7":
            rv = settings.value(SettingsKeys.planetH7GlyphFontSizeKey,
                                SettingsKeys.planetH7GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H8":
            rv = settings.value(SettingsKeys.planetH8GlyphFontSizeKey,
                                SettingsKeys.planetH8GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H9":
            rv = settings.value(SettingsKeys.planetH9GlyphFontSizeKey,
                                SettingsKeys.planetH9GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H10":
            rv = settings.value(SettingsKeys.planetH10GlyphFontSizeKey,
                                SettingsKeys.planetH10GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H11":
            rv = settings.value(SettingsKeys.planetH11GlyphFontSizeKey,
                                SettingsKeys.planetH11GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "H12":
            rv = settings.value(SettingsKeys.planetH12GlyphFontSizeKey,
                                SettingsKeys.planetH12GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "ARMC":
            rv = settings.value(SettingsKeys.planetARMCGlyphFontSizeKey,
                                SettingsKeys.planetARMCGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Vertex":
            rv = settings.value(SettingsKeys.planetVertexGlyphFontSizeKey,
                                SettingsKeys.planetVertexGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "EquatorialAscendant":
            rv = settings.value(SettingsKeys.planetEquatorialAscendantGlyphFontSizeKey,
                                SettingsKeys.planetEquatorialAscendantGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "CoAscendant1":
            rv = settings.value(SettingsKeys.planetCoAscendant1GlyphFontSizeKey,
                                SettingsKeys.planetCoAscendant1GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "CoAscendant2":
            rv = settings.value(SettingsKeys.planetCoAscendant2GlyphFontSizeKey,
                                SettingsKeys.planetCoAscendant2GlyphFontSizeDefValue,
                                type=float)
        elif planetName == "PolarAscendant":
            rv = settings.value(SettingsKeys.planetPolarAscendantGlyphFontSizeKey,
                                SettingsKeys.planetPolarAscendantGlyphFontSizeDefValue,
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
        elif planetName == "Isis":
            rv = settings.value(SettingsKeys.planetIsisGlyphFontSizeKey,
                                SettingsKeys.planetIsisGlyphFontSizeDefValue,
                                type=float)
        elif planetName == "Nibiru":
            rv = settings.value(SettingsKeys.planetNibiruGlyphFontSizeKey,
                                SettingsKeys.planetNibiruGlyphFontSizeDefValue,
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
            AstrologyUtils.log.warn(\
                "Could not find glyph font size for planet: " + \
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
        
        if planetName == "H1":
            rv = settings.value(SettingsKeys.planetH1AbbreviationKey,
                                SettingsKeys.planetH1AbbreviationDefValue,
                                type=str)
        elif planetName == "H2":
            rv = settings.value(SettingsKeys.planetH2AbbreviationKey,
                                SettingsKeys.planetH2AbbreviationDefValue,
                                type=str)
        elif planetName == "H3":
            rv = settings.value(SettingsKeys.planetH3AbbreviationKey,
                                SettingsKeys.planetH3AbbreviationDefValue,
                                type=str)
        elif planetName == "H4":
            rv = settings.value(SettingsKeys.planetH4AbbreviationKey,
                                SettingsKeys.planetH4AbbreviationDefValue,
                                type=str)
        elif planetName == "H5":
            rv = settings.value(SettingsKeys.planetH5AbbreviationKey,
                                SettingsKeys.planetH5AbbreviationDefValue,
                                type=str)
        elif planetName == "H6":
            rv = settings.value(SettingsKeys.planetH6AbbreviationKey,
                                SettingsKeys.planetH6AbbreviationDefValue,
                                type=str)
        elif planetName == "H7":
            rv = settings.value(SettingsKeys.planetH7AbbreviationKey,
                                SettingsKeys.planetH7AbbreviationDefValue,
                                type=str)
        elif planetName == "H8":
            rv = settings.value(SettingsKeys.planetH8AbbreviationKey,
                                SettingsKeys.planetH8AbbreviationDefValue,
                                type=str)
        elif planetName == "H9":
            rv = settings.value(SettingsKeys.planetH9AbbreviationKey,
                                SettingsKeys.planetH9AbbreviationDefValue,
                                type=str)
        elif planetName == "H10":
            rv = settings.value(SettingsKeys.planetH10AbbreviationKey,
                                SettingsKeys.planetH10AbbreviationDefValue,
                                type=str)
        elif planetName == "H11":
            rv = settings.value(SettingsKeys.planetH11AbbreviationKey,
                                SettingsKeys.planetH11AbbreviationDefValue,
                                type=str)
        elif planetName == "H12":
            rv = settings.value(SettingsKeys.planetH12AbbreviationKey,
                                SettingsKeys.planetH12AbbreviationDefValue,
                                type=str)
        elif planetName == "ARMC":
            rv = settings.value(SettingsKeys.planetARMCAbbreviationKey,
                                SettingsKeys.planetARMCAbbreviationDefValue,
                                type=str)
        elif planetName == "Vertex":
            rv = settings.value(SettingsKeys.planetVertexAbbreviationKey,
                                SettingsKeys.planetVertexAbbreviationDefValue,
                                type=str)
        elif planetName == "EquatorialAscendant":
            rv = settings.value(SettingsKeys.planetEquatorialAscendantAbbreviationKey,
                                SettingsKeys.planetEquatorialAscendantAbbreviationDefValue,
                                type=str)
        elif planetName == "CoAscendant1":
            rv = settings.value(SettingsKeys.planetCoAscendant1AbbreviationKey,
                                SettingsKeys.planetCoAscendant1AbbreviationDefValue,
                                type=str)
        elif planetName == "CoAscendant2":
            rv = settings.value(SettingsKeys.planetCoAscendant2AbbreviationKey,
                                SettingsKeys.planetCoAscendant2AbbreviationDefValue,
                                type=str)
        elif planetName == "PolarAscendant":
            rv = settings.value(SettingsKeys.planetPolarAscendantAbbreviationKey,
                                SettingsKeys.planetPolarAscendantAbbreviationDefValue,
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
        elif planetName == "Isis":
            rv = settings.value(SettingsKeys.planetIsisAbbreviationKey,
                                SettingsKeys.planetIsisAbbreviationDefValue,
                                type=str)
        elif planetName == "Nibiru":
            rv = settings.value(SettingsKeys.planetNibiruAbbreviationKey,
                                SettingsKeys.planetNibiruAbbreviationDefValue,
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
            AstrologyUtils.log.warn(\
                "Could not find abbreviation for planet: " + \
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
        
        if planetName == "H1":
            rv = settings.value(SettingsKeys.planetH1ForegroundColorKey,
                                SettingsKeys.planetH1ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H2":
            rv = settings.value(SettingsKeys.planetH2ForegroundColorKey,
                                SettingsKeys.planetH2ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H3":
            rv = settings.value(SettingsKeys.planetH3ForegroundColorKey,
                                SettingsKeys.planetH3ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H4":
            rv = settings.value(SettingsKeys.planetH4ForegroundColorKey,
                                SettingsKeys.planetH4ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H5":
            rv = settings.value(SettingsKeys.planetH5ForegroundColorKey,
                                SettingsKeys.planetH5ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H6":
            rv = settings.value(SettingsKeys.planetH6ForegroundColorKey,
                                SettingsKeys.planetH6ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H7":
            rv = settings.value(SettingsKeys.planetH7ForegroundColorKey,
                                SettingsKeys.planetH7ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H8":
            rv = settings.value(SettingsKeys.planetH8ForegroundColorKey,
                                SettingsKeys.planetH8ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H9":
            rv = settings.value(SettingsKeys.planetH9ForegroundColorKey,
                                SettingsKeys.planetH9ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H10":
            rv = settings.value(SettingsKeys.planetH10ForegroundColorKey,
                                SettingsKeys.planetH10ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H11":
            rv = settings.value(SettingsKeys.planetH11ForegroundColorKey,
                                SettingsKeys.planetH11ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "H12":
            rv = settings.value(SettingsKeys.planetH12ForegroundColorKey,
                                SettingsKeys.planetH12ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "ARMC":
            rv = settings.value(SettingsKeys.planetARMCForegroundColorKey,
                                SettingsKeys.planetARMCForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Vertex":
            rv = settings.value(SettingsKeys.planetVertexForegroundColorKey,
                                SettingsKeys.planetVertexForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "EquatorialAscendant":
            rv = settings.value(SettingsKeys.planetEquatorialAscendantForegroundColorKey,
                                SettingsKeys.planetEquatorialAscendantForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "CoAscendant1":
            rv = settings.value(SettingsKeys.planetCoAscendant1ForegroundColorKey,
                                SettingsKeys.planetCoAscendant1ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "CoAscendant2":
            rv = settings.value(SettingsKeys.planetCoAscendant2ForegroundColorKey,
                                SettingsKeys.planetCoAscendant2ForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "PolarAscendant":
            rv = settings.value(SettingsKeys.planetPolarAscendantForegroundColorKey,
                                SettingsKeys.planetPolarAscendantForegroundColorDefValue,\
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
        elif planetName == "Isis":
            rv = settings.value(SettingsKeys.planetIsisForegroundColorKey,
                                SettingsKeys.planetIsisForegroundColorDefValue,\
                                type=QColor)
        elif planetName == "Nibiru":
            rv = settings.value(SettingsKeys.planetNibiruForegroundColorKey,
                                SettingsKeys.planetNibiruForegroundColorDefValue,\
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
            AstrologyUtils.log.warn(\
                "Could not find foreground color for planet: " + \
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
        
        if planetName == "H1":
            rv = settings.value(SettingsKeys.planetH1BackgroundColorKey,
                                SettingsKeys.planetH1BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H2":
            rv = settings.value(SettingsKeys.planetH2BackgroundColorKey,
                                SettingsKeys.planetH2BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H3":
            rv = settings.value(SettingsKeys.planetH3BackgroundColorKey,
                                SettingsKeys.planetH3BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H4":
            rv = settings.value(SettingsKeys.planetH4BackgroundColorKey,
                                SettingsKeys.planetH4BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H5":
            rv = settings.value(SettingsKeys.planetH5BackgroundColorKey,
                                SettingsKeys.planetH5BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H6":
            rv = settings.value(SettingsKeys.planetH6BackgroundColorKey,
                                SettingsKeys.planetH6BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H7":
            rv = settings.value(SettingsKeys.planetH7BackgroundColorKey,
                                SettingsKeys.planetH7BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H8":
            rv = settings.value(SettingsKeys.planetH8BackgroundColorKey,
                                SettingsKeys.planetH8BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H9":
            rv = settings.value(SettingsKeys.planetH9BackgroundColorKey,
                                SettingsKeys.planetH9BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H10":
            rv = settings.value(SettingsKeys.planetH10BackgroundColorKey,
                                SettingsKeys.planetH10BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H11":
            rv = settings.value(SettingsKeys.planetH11BackgroundColorKey,
                                SettingsKeys.planetH11BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "H12":
            rv = settings.value(SettingsKeys.planetH12BackgroundColorKey,
                                SettingsKeys.planetH12BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "ARMC":
            rv = settings.value(SettingsKeys.planetARMCBackgroundColorKey,
                                SettingsKeys.planetARMCBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Vertex":
            rv = settings.value(SettingsKeys.planetVertexBackgroundColorKey,
                                SettingsKeys.planetVertexBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "EquatorialAscendant":
            rv = settings.value(SettingsKeys.planetEquatorialAscendantBackgroundColorKey,
                                SettingsKeys.planetEquatorialAscendantBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "CoAscendant1":
            rv = settings.value(SettingsKeys.planetCoAscendant1BackgroundColorKey,
                                SettingsKeys.planetCoAscendant1BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "CoAscendant1":
            rv = settings.value(SettingsKeys.planetCoAscendant1BackgroundColorKey,
                                SettingsKeys.planetCoAscendant1BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "CoAscendant2":
            rv = settings.value(SettingsKeys.planetCoAscendant2BackgroundColorKey,
                                SettingsKeys.planetCoAscendant2BackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "PolarAscendant":
            rv = settings.value(SettingsKeys.planetPolarAscendantBackgroundColorKey,
                                SettingsKeys.planetPolarAscendantBackgroundColorDefValue,\
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
        elif planetName == "Isis":
            rv = settings.value(SettingsKeys.planetIsisBackgroundColorKey,
                                SettingsKeys.planetIsisBackgroundColorDefValue,\
                                type=QColor)
        elif planetName == "Nibiru":
            rv = settings.value(SettingsKeys.planetNibiruBackgroundColorKey,
                                SettingsKeys.planetNibiruBackgroundColorDefValue,\
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
            AstrologyUtils.log.warn(\
                "Could not find background color for planet: " + \
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
            self.log.debug("self.numAspectMatches == {}".\
                           format(self.numAspectMatches))
        
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
        if parent != None and isinstance(parent, RadixChartGraphicsItem):
            radius = parent.getInnerRasiRadius()
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

        # Coordinate (0, 0) is the location where the center of the
        # circular radix chart.  

        # Only paint if the item is enabled and visible.
        if self.isEnabled() == False or self.isVisible() == False:
            return
        
        # Get the radius.
        radius = 0.0
        parent = self.parentItem()
        if parent != None and isinstance(parent, RadixChartGraphicsItem):
            
            radius = parent.getInnerRasiRadius()
            if self.log.isEnabledFor(logging.DEBUG) == True:
                self.log.debug("radius obtained from parent is: {}".\
                               format(radius))
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
                    # House cusps shouldn't aspect other house cusps
                    # in the same wheel.  If both planets are house
                    # cusps and in the same wheel, then don't create
                    # the RadixChartAspectGraphicsItem.
                    p1Name = p1.getPlanetName()
                    p2Name = p2.getPlanetName()
                    
                    if Ephemeris.isHouseCuspPlanetName(p1Name) and \
                        Ephemeris.isHouseCuspPlanetName(p2Name) and \
                        p1.getWheelNumber() == p2.getWheelNumber():
                        
                        # Don't create the aspect.
                        pass
                    else:
                        # Create the aspect.
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
            painter.drawLine(QLineF(x1, y1, x2, y2))

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
            painter.drawLine(QLineF(x1, y1, x2, y2))

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
            painter.drawLine(QLineF(x1, y1, x2, y2))

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

        painter.drawLine(QLineF(x1, y1, x2, y2))

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
            painter.drawLine(QLineF(x1, y1, x2, y2))

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
            painter.drawLine(QLineF(x1, y1, x2, y2))

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
        painter.drawLine(QLineF(x1, y1, x2, y2))

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

class LatitudeChartGraphicsItem(QGraphicsItem):
    """QGraphicsItem that paints a chart for displaying various
    planets' latitude.
    """

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        # Logger
        self.log = \
            logging.getLogger("astrologychart.LatitudeGraphicsItem")

        self.rulerWidth = 40.0
        self.rulerHeight = 300.0

        # These are on the verical axis.  Ruler height must be evenly
        # divisible by these tick size numbers below.
        self.bigTickSize = 50.0
        self.smallTickSize = 10.0

        # Value used in getXLocationForPlanetGroupNumber().
        self.planetLineLength = self.rulerWidth
        
    def getPlanetLatitudeGraphicsItem(self, planetName, groupNum):
        """Returns the PlanetLatitudeGraphicsItem with the given
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
        # PlanetLatitudeGraphicsItem.
        for child in children:
            if isinstance(child, PlanetLatitudeGraphicsItem):
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
                            latitude charted.  This index
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
            painter.drawLine(QLineF(x1, y1, x2, y2))

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
            painter.drawLine(QLineF(x1, y1, x2, y2))

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
    
class PlanetLatitudeGraphicsItem(QGraphicsItem):
    """QGraphicsItem that is a 'planet' to be drawn with a
    LatitudeChartGraphicsItem object as its parent QGraphicsItem.
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
        parent - LatitudeChartGraphicsItem that is the parent for this
                 QGraphicsItem.
        scene - QGraphicsScene object to draw this QGraphicsItem on.
        """
        
        super().__init__(parent, scene)
        
        # Logger
        self.log = \
            logging.getLogger("astrologychart.PlanetLatitudeGraphicsItem")

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
        # LatitudeChartGraphicsItem object.
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
        parent -  LatitudeChartGraphicsItem parent object.
        """

        # Verify parent class.
        if parent != None and \
               not isinstance(parent, LatitudeChartGraphicsItem):
            
            raise TypeError("Argument 'parent' is not of type " + \
                            "'LatitudeChartGraphicsItem'")
        
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
        painter.drawLine(QLineF(x1, y1, x2, y2))

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
        # convertSpeedToYLocation() function for the conversion
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
    
        
    def convertSpeedToYValue(self, speed):
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

    def convertYValueToSpeed(self, y):
        """Converts the given y value to a longitude speed (in degrees per day).
        This method does the inverse of convertSpeedToYValue().

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
        y1 = self.convertSpeedToYValue(maxSpeed)
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
        y1 = self.convertSpeedToYValue(minSpeed)
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
        y1 = self.convertSpeedToYValue(zeroSpeed)
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
        y1 = self.convertSpeedToYValue(0)
        x2 = self.rulerWidth
        y2 = y1
        painter.drawLine(QLineF(x1, y1, x2, y2))
        
        # Draw the text for the min, max, and 0 locations on the ruler.
        font = QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(10)

        # Max speed.
        x1 = self.textXLoc
        y1 = self.convertSpeedToYValue(maxSpeed)
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
        y1 = self.convertSpeedToYValue(minSpeed)
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
        y1 = self.convertSpeedToYValue(zeroSpeed)
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
        y1 = self.parentChartGraphicsItem.convertSpeedToYValue(self.speed)
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
                convertSpeedToYValue(self.speed)
        transform.translate(textX, textY)
        transformedTextPath = QPainterPath()
        transformedTextPath.addPath(transform.map(textPath))
        textRect = transformedTextPath.boundingRect()

        # QRectF for the fill area.
        rulerFillAreaRectF = \
            QRectF(QPointF(0.0,
                           self.parentChartGraphicsItem.\
                           convertSpeedToYValue(0.0)),
                   QPointF(self.rulerWidth,
                           self.parentChartGraphicsItem.\
                           convertSpeedToYValue(self.speed))).normalized()

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
        y1 = self.parentChartGraphicsItem.convertSpeedToYValue(self.speed)
        x2 = self.lineEndX
        y2 = y1
        painter.drawLine(QLineF(x1, y1, x2, y2))

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
                convertSpeedToYValue(self.speed)
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
                           convertSpeedToYValue(0.0)),
                   QPointF(self.rulerWidth,
                           self.parentChartGraphicsItem.\
                           convertSpeedToYValue(self.speed))).normalized()
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
        font = QFont()
        #font.setFamily("Courier")
        #font.setFamily("DejaVu Sans Mono")
        #font.setFamily("Lucida Console")  # Lucida Console isn't monospaced?
        font.setFamily("Droid Sans Mono")
        font.setPointSize(10)
        self.setFont(font)

        # Strings for the different types of planetary coordinate systems.
        #geoStr = "Geocentric" + os.linesep
        #topoStr = "Topocentric" + os.linesep
        #helioStr = "Heliocentric" + os.linesep
        geoStr = "Geo." + os.linesep
        topoStr = "Topo." + os.linesep
        helioStr = "Helio." + os.linesep

        #sidStr = "Sidereal" + os.linesep
        #tropStr = "Tropical" + os.linesep
        sidStr = "Sid." + os.linesep
        tropStr = "Trop." + os.linesep

        # Different measurements available.
        #longitudeStr = "Longitude"
        #latitudeStr = "Latitude"
        #distanceStr = "Distance"
        longitudeStr = "Lon."
        latitudeStr = "Lat."
        distanceStr = "Dist."

        longitudeSpeedStr = "Lon. Speed"
        latitudeSpeedStr = "Lat. Speed"
        distanceSpeedStr = "Dist. Speed"

        #rectascensionStr = "Rectascension"
        #declinationStr = "Declination"
        rectascensionStr = "Rect."
        declinationStr = "Decl."

        rectascensionSpeedStr = "Rect. Speed"
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
        numTotalFields = 16
        numColumns = numTotalFields + 1
        self.setColumnCount(numColumns)

        # List of column numbers, for which the text should be aligned
        # in the center.
        self.alignHCenterColumns = []
        
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
        self.setColumnWidth(col, 98)
        col += 1
        
        item = QTableWidgetItem(geoStr + sidStr + longitudeStr)
        item.setToolTip(longitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 98)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + "Navamsa")
        item.setToolTip("Navamsa")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 70)
        self.alignHCenterColumns.append(col)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + "Nak.")
        item.setToolTip("Nakshatra")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 70)
        self.alignHCenterColumns.append(col)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + "Nak. Pada")
        item.setToolTip("Nakshatra Pada")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 76)
        self.alignHCenterColumns.append(col)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + longitudeSpeedStr)
        item.setToolTip(longitudeSpeedStr + degreesPerDayUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 80)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + declinationStr)
        item.setToolTip(declinationStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 76)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + declinationSpeedStr)
        item.setToolTip(declinationSpeedStr + degreesPerDayUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 84)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + latitudeStr)
        item.setToolTip(latitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 80)
        col += 1

        item = QTableWidgetItem(geoStr + sidStr + latitudeSpeedStr)
        item.setToolTip(latitudeSpeedStr + degreesPerDayUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 80)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + longitudeStr)
        item.setToolTip(longitudeStr + degreesUnitsStr)
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 94)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + "Navamsa")
        item.setToolTip("Navamsa")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 70)
        self.alignHCenterColumns.append(col)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + "Nak.")
        item.setToolTip("Nakshatra")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 70)
        self.alignHCenterColumns.append(col)
        col += 1

        item = QTableWidgetItem(helioStr + sidStr + "Nak. Pada")
        item.setToolTip("Nakshatra Pada")
        self.setHorizontalHeaderItem(col, item)
        self.setColumnWidth(col, 76)
        self.alignHCenterColumns.append(col)
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
        # self._getPlanetNamesToDisplayForPlanetaryInfoTable().
        toLoad = []
        for p in planetaryInfos:
            if p.name in self._getPlanetNamesToDisplayForPlanetaryInfoTable():
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

    def _getPlanetNamesToDisplayForPlanetaryInfoTable(self):
        """Function to return a list of planet names that should be
        used to display in the table cells.  This is to help lessen
        the possibly excessive amount of info in the table.
        """

        # Return value.
        enabledPlanetNames = []

        settings = QSettings()
        
        if settings.value(\
            SettingsKeys.planetH1EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH1EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H1")
        
        if settings.value(\
            SettingsKeys.planetH2EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH2EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H2")
        
        if settings.value(\
            SettingsKeys.planetH3EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH3EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H3")
        
        if settings.value(\
            SettingsKeys.planetH4EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH4EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H4")
        
        if settings.value(\
            SettingsKeys.planetH5EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH5EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H5")
        
        if settings.value(\
            SettingsKeys.planetH6EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH6EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H6")
        
        if settings.value(\
            SettingsKeys.planetH7EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH7EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H7")
        
        if settings.value(\
            SettingsKeys.planetH8EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH8EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H8")
        
        if settings.value(\
            SettingsKeys.planetH9EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH9EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H9")
        
        if settings.value(\
            SettingsKeys.planetH10EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH10EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H10")
        
        if settings.value(\
            SettingsKeys.planetH11EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH11EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H11")
        
        if settings.value(\
            SettingsKeys.planetH12EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetH12EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("H12")
        
        if settings.value(\
            SettingsKeys.planetARMCEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetARMCEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("ARMC")
        
        if settings.value(\
            SettingsKeys.planetVertexEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetVertexEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Vertex")
        
        if settings.value(\
            SettingsKeys.planetEquatorialAscendantEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetEquatorialAscendantEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("EquatorialAscendant")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant1EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetCoAscendant1EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant1")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant2EnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetCoAscendant2EnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant2")
        
        if settings.value(\
            SettingsKeys.planetPolarAscendantEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetPolarAscendantEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("PolarAscendant")
        
        if settings.value(\
            SettingsKeys.planetHoraLagnaEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetHoraLagnaEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("HoraLagna")
        
        if settings.value(\
            SettingsKeys.planetGhatiLagnaEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetGhatiLagnaEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("GhatiLagna")
        
        if settings.value(\
            SettingsKeys.planetMeanLunarApogeeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMeanLunarApogeeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("MeanLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetOsculatingLunarApogeeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetOsculatingLunarApogeeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("OsculatingLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarPerigee")
        
        if settings.value(\
            SettingsKeys.planetSunEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetSunEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Sun")
        
        if settings.value(\
            SettingsKeys.planetMoonEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMoonEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Moon")
        
        if settings.value(\
            SettingsKeys.planetMercuryEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMercuryEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Mercury")
        
        if settings.value(\
            SettingsKeys.planetVenusEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetVenusEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Venus")
        
        if settings.value(\
            SettingsKeys.planetEarthEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetEarthEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Earth")
        
        if settings.value(\
            SettingsKeys.planetMarsEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMarsEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Mars")
        
        if settings.value(\
            SettingsKeys.planetJupiterEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetJupiterEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Jupiter")
        
        if settings.value(\
            SettingsKeys.planetSaturnEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetSaturnEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Saturn")
        
        if settings.value(\
            SettingsKeys.planetUranusEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetUranusEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Uranus")
        
        if settings.value(\
            SettingsKeys.planetNeptuneEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetNeptuneEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Neptune")
        
        if settings.value(\
            SettingsKeys.planetPlutoEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetPlutoEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Pluto")
        
        if settings.value(\
            SettingsKeys.planetMeanNorthNodeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMeanNorthNodeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("MeanNorthNode")
        
        if settings.value(\
            SettingsKeys.planetMeanSouthNodeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMeanSouthNodeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("MeanSouthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueNorthNodeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetTrueNorthNodeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("TrueNorthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueSouthNodeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetTrueSouthNodeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("TrueSouthNode")
        
        if settings.value(\
            SettingsKeys.planetCeresEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetCeresEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Ceres")
        
        if settings.value(\
            SettingsKeys.planetPallasEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetPallasEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Pallas")
        
        if settings.value(\
            SettingsKeys.planetJunoEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetJunoEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Juno")
        
        if settings.value(\
            SettingsKeys.planetVestaEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetVestaEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Vesta")
        
        if settings.value(\
            SettingsKeys.planetIsisEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetIsisEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Isis")
        
        if settings.value(\
            SettingsKeys.planetNibiruEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetNibiruEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Nibiru")
        
        if settings.value(\
            SettingsKeys.planetChironEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetChironEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Chiron")
        
        if settings.value(\
            SettingsKeys.planetGulikaEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetGulikaEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Gulika")
        
        if settings.value(\
            SettingsKeys.planetMandiEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMandiEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("Mandi")
        
        if settings.value(\
            SettingsKeys.planetMeanOfFiveEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetMeanOfFiveEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("MeanOfFive")
        
        if settings.value(\
            SettingsKeys.planetCycleOfEightEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetCycleOfEightEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("CycleOfEight")
        
        if settings.value(\
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("AvgMaJuSaUrNePl")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaUrNeEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetAvgJuSaUrNeEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSaUrNe")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaEnabledForPlanetaryInfoTableKey, \
            SettingsKeys.planetAvgJuSaEnabledForPlanetaryInfoTableDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSa")

        
        return enabledPlanetNames
        
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

            # Set alignment.
            if col in self.alignHCenterColumns:
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            
            self.setItem(row, col, item)
        item.setText(p.name)
        col += 1

        # We only use some of the fields.
        
        # While it is possible to do all three types, we just do two here.
        #dicts = [p.geocentric, p.topocentric, p.heliocentric]
        dicts = [p.geocentric, p.heliocentric]

        tropical = "tropical"
        sidereal = "sidereal"
        
        # Populate the item cells for each column.
        longitude = p.geocentric[tropical]['longitude']
        valueStr = \
            AstrologyUtils.\
            convertLongitudeToStrWithRasiAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.geocentric[sidereal]['longitude']
        valueStr = \
            AstrologyUtils.\
            convertLongitudeToStrWithRasiAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.geocentric[sidereal]['longitude']
        valueStr = AstrologyUtils.convertLongitudeToNavamsaStr(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.geocentric[sidereal]['longitude']
        valueStr = \
            AstrologyUtils.\
            convertLongitudeToNakshatraAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.geocentric[sidereal]['longitude']
        padaSize = 360 / 108.0
        pada = (math.floor(longitude / padaSize) % 4) + 1
        valueStr = "{}".format(pada)
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
            convertLongitudeToStrWithRasiAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.heliocentric[sidereal]['longitude']
        valueStr = AstrologyUtils.convertLongitudeToNavamsaStr(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.heliocentric[sidereal]['longitude']
        valueStr = \
            AstrologyUtils.\
            convertLongitudeToNakshatraAbbrev(longitude)
        self._setItemAndToolTip(row, col, valueStr)
        col += 1

        longitude = p.heliocentric[sidereal]['longitude']
        padaSize = 360 / 108.0
        pada = (math.floor(longitude / padaSize) % 4) + 1
        valueStr = "{}".format(pada)
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

            # Set alignment.
            if col in self.alignHCenterColumns:
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            
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

        self.latitudeChart = LatitudeChartGraphicsItem()
        self.latitudeChart.setScale(2.0)
        
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
        
        self.latitudeChartLabel = QGraphicsProxyWidget()
        self.latitudeChartLabel.setWidget(QLabel("Latitude"))
        
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

        declinationWidth = 400
        declinationStartX = x
        declinationStartY = y
        self.declinationChartLabel.setPos(declinationStartX, declinationStartY)
        x += 36
        y += 260
        self.declinationChart.setPos(x, y)

        latitudeWidth = 600
        x = declinationStartX + declinationWidth
        y = declinationStartY
        latitudeStartX = x
        latitudeStartY = y
        self.latitudeChartLabel.setPos(latitudeStartX, latitudeStartY)
        x += 36
        y += 260
        self.latitudeChart.setPos(x, y)
        
        x = 0.0
        y = 0.0
        self.geoTropRadixChartGraphicsItem.setPos(x, y)
        x += radixLength
        self.geoSidRadixChartGraphicsItem.setPos(x, y)
        x += radixLength
        self.helioSidRadixChartGraphicsItem.setPos(x, y)
        x += radixLength
        
        x = -0.45 * radixLength
        y = -0.45 * radixLength
        self.geoTropRadixChartLabel.setPos(x, y)
        x += radixLength
        self.geoSidRadixChartLabel.setPos(x, y)
        x += radixLength
        self.helioSidRadixChartLabel.setPos(x, y)
        x += radixLength

        # Add all the items to the QGraphicsScene.
        self.graphicsScene.addItem(self.locationLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart1DatetimeLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart2DatetimeLabelProxyWidget)
        self.graphicsScene.addItem(self.astroChart3DatetimeLabelProxyWidget)
    
        self.graphicsScene.addItem(self.declinationChart)
        self.graphicsScene.addItem(self.latitudeChart)
        
        self.graphicsScene.addItem(self.geoTropRadixChartGraphicsItem)
        self.graphicsScene.addItem(self.geoSidRadixChartGraphicsItem)
        self.graphicsScene.addItem(self.helioSidRadixChartGraphicsItem)
        
        self.graphicsScene.addItem(self.geoTropRadixChartLabel)
        self.graphicsScene.addItem(self.geoSidRadixChartLabel)
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

        # Astrological house system for getting the house cusps.
        houseSystem = Ephemeris.HouseSys['Porphyry']

        settings = QSettings()
        
        if settings.value(\
            SettingsKeys.planetH1CalculationsEnabledKey, \
            SettingsKeys.planetH1CalculationsEnabledDefValue,
            type=bool):

            self.log.debug("Getting house 1 values...")
            planets.append(Ephemeris.getH1PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH2CalculationsEnabledKey, \
            SettingsKeys.planetH2CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH2PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH3CalculationsEnabledKey, \
            SettingsKeys.planetH3CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH3PlanetaryInfo(dt, houseSystem))

        if settings.value(\
            SettingsKeys.planetH4CalculationsEnabledKey, \
            SettingsKeys.planetH4CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH4PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH5CalculationsEnabledKey, \
            SettingsKeys.planetH5CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH5PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH6CalculationsEnabledKey, \
            SettingsKeys.planetH6CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH6PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH7CalculationsEnabledKey, \
            SettingsKeys.planetH7CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH7PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH8CalculationsEnabledKey, \
            SettingsKeys.planetH8CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH8PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH9CalculationsEnabledKey, \
            SettingsKeys.planetH9CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH9PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH10CalculationsEnabledKey, \
            SettingsKeys.planetH10CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH10PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH11CalculationsEnabledKey, \
            SettingsKeys.planetH11CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH11PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetH12CalculationsEnabledKey, \
            SettingsKeys.planetH12CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getH12PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetARMCCalculationsEnabledKey, \
            SettingsKeys.planetARMCCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getARMCPlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetVertexCalculationsEnabledKey, \
            SettingsKeys.planetVertexCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getVertexPlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetEquatorialAscendantCalculationsEnabledKey, \
            SettingsKeys.planetEquatorialAscendantCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getEquatorialAscendantPlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetCoAscendant1CalculationsEnabledKey, \
            SettingsKeys.planetCoAscendant1CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getCoAscendant1PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetCoAscendant2CalculationsEnabledKey, \
            SettingsKeys.planetCoAscendant2CalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getCoAscendant2PlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetPolarAscendantCalculationsEnabledKey, \
            SettingsKeys.planetPolarAscendantCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getPolarAscendantPlanetaryInfo(dt, houseSystem))
        
        if settings.value(\
            SettingsKeys.planetHoraLagnaCalculationsEnabledKey, \
            SettingsKeys.planetHoraLagnaCalculationsEnabledDefValue,
            type=bool):

            pass # TODO:  update for HoraLagna
            #planets.append(Ephemeris.getHoraLagnaPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetGhatiLagnaCalculationsEnabledKey, \
            SettingsKeys.planetGhatiLagnaCalculationsEnabledDefValue,
            type=bool):

            pass # TODO:  update for GhatiLagna
            #planets.append(Ephemeris.getGhatiLagnaPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetMeanLunarApogeeCalculationsEnabledKey, \
            SettingsKeys.planetMeanLunarApogeeCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getMeanLunarApogeePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetOsculatingLunarApogeeCalculationsEnabledKey, \
            SettingsKeys.planetOsculatingLunarApogeeCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getOsculatingLunarApogeePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarApogeeCalculationsEnabledKey, \
            SettingsKeys.planetInterpolatedLunarApogeeCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarPerigeeCalculationsEnabledKey, \
            SettingsKeys.planetInterpolatedLunarPerigeeCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetSunCalculationsEnabledKey, \
            SettingsKeys.planetSunCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getSunPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetMoonCalculationsEnabledKey, \
            SettingsKeys.planetMoonCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getMoonPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetMercuryCalculationsEnabledKey, \
            SettingsKeys.planetMercuryCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getMercuryPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetVenusCalculationsEnabledKey, \
            SettingsKeys.planetVenusCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getVenusPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetEarthCalculationsEnabledKey, \
            SettingsKeys.planetEarthCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getEarthPlanetaryInfo(dt))
            
        if settings.value(\
            SettingsKeys.planetMarsCalculationsEnabledKey, \
            SettingsKeys.planetMarsCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getMarsPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetJupiterCalculationsEnabledKey, \
            SettingsKeys.planetJupiterCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getJupiterPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetSaturnCalculationsEnabledKey, \
            SettingsKeys.planetSaturnCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getSaturnPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetUranusCalculationsEnabledKey, \
            SettingsKeys.planetUranusCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getUranusPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetNeptuneCalculationsEnabledKey, \
            SettingsKeys.planetNeptuneCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getNeptunePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetPlutoCalculationsEnabledKey, \
            SettingsKeys.planetPlutoCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getPlutoPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetMeanNorthNodeCalculationsEnabledKey, \
            SettingsKeys.planetMeanNorthNodeCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getMeanNorthNodePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetMeanSouthNodeCalculationsEnabledKey, \
            SettingsKeys.planetMeanSouthNodeCalculationsEnabledDefValue,
            type=bool):

            pass # TODO:  update for TrueSouthNode
            #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetTrueNorthNodeCalculationsEnabledKey, \
            SettingsKeys.planetTrueNorthNodeCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getTrueNorthNodePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetTrueSouthNodeCalculationsEnabledKey, \
            SettingsKeys.planetTrueSouthNodeCalculationsEnabledDefValue,
            type=bool):

            pass # TODO:  update for TrueSouthNode
            #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetCeresCalculationsEnabledKey, \
            SettingsKeys.planetCeresCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getCeresPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetPallasCalculationsEnabledKey, \
            SettingsKeys.planetPallasCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getPallasPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetJunoCalculationsEnabledKey, \
            SettingsKeys.planetJunoCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getJunoPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetVestaCalculationsEnabledKey, \
            SettingsKeys.planetVestaCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getVestaPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetIsisCalculationsEnabledKey, \
            SettingsKeys.planetIsisCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getIsisPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetNibiruCalculationsEnabledKey, \
            SettingsKeys.planetNibiruCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getNibiruPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetChironCalculationsEnabledKey, \
            SettingsKeys.planetChironCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getChironPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetGulikaCalculationsEnabledKey, \
            SettingsKeys.planetGulikaCalculationsEnabledDefValue,
            type=bool):

            pass # TODO:  update for Gulika
            #planets.append(Ephemeris.getGulikaPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetMandiCalculationsEnabledKey, \
            SettingsKeys.planetMandiCalculationsEnabledDefValue,
            type=bool):

            pass # TODO:  update for Mandi
            #planets.append(Ephemeris.getMandiPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetMeanOfFiveCalculationsEnabledKey, \
            SettingsKeys.planetMeanOfFiveCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getMeanOfFivePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetCycleOfEightCalculationsEnabledKey, \
            SettingsKeys.planetCycleOfEightCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getCycleOfEightPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetAvgMaJuSaUrNePlCalculationsEnabledKey, \
            SettingsKeys.planetAvgMaJuSaUrNePlCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaUrNeCalculationsEnabledKey, \
            SettingsKeys.planetAvgJuSaUrNeCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getAvgJuSaUrNePlanetaryInfo(dt))
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaCalculationsEnabledKey, \
            SettingsKeys.planetAvgJuSaCalculationsEnabledDefValue,
            type=bool):

            planets.append(Ephemeris.getAvgJuSaPlanetaryInfo(dt))

        return planets

    def _getPlanetNamesToDisplayForDeclination(self):
        """Function to return a list of planet names that should be
        used to display declination information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        # Return value.
        enabledPlanetNames = []

        settings = QSettings()
        
        if settings.value(\
            SettingsKeys.planetH1EnabledForDeclinationKey, \
            SettingsKeys.planetH1EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H1")
        
        if settings.value(\
            SettingsKeys.planetH2EnabledForDeclinationKey, \
            SettingsKeys.planetH2EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H2")
        
        if settings.value(\
            SettingsKeys.planetH3EnabledForDeclinationKey, \
            SettingsKeys.planetH3EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H3")
        
        if settings.value(\
            SettingsKeys.planetH4EnabledForDeclinationKey, \
            SettingsKeys.planetH4EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H4")
        
        if settings.value(\
            SettingsKeys.planetH5EnabledForDeclinationKey, \
            SettingsKeys.planetH5EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H5")
        
        if settings.value(\
            SettingsKeys.planetH6EnabledForDeclinationKey, \
            SettingsKeys.planetH6EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H6")
        
        if settings.value(\
            SettingsKeys.planetH7EnabledForDeclinationKey, \
            SettingsKeys.planetH7EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H7")
        
        if settings.value(\
            SettingsKeys.planetH8EnabledForDeclinationKey, \
            SettingsKeys.planetH8EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H8")
        
        if settings.value(\
            SettingsKeys.planetH9EnabledForDeclinationKey, \
            SettingsKeys.planetH9EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H9")
        
        if settings.value(\
            SettingsKeys.planetH10EnabledForDeclinationKey, \
            SettingsKeys.planetH10EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H10")
        
        if settings.value(\
            SettingsKeys.planetH11EnabledForDeclinationKey, \
            SettingsKeys.planetH11EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H11")
        
        if settings.value(\
            SettingsKeys.planetH12EnabledForDeclinationKey, \
            SettingsKeys.planetH12EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("H12")
        
        if settings.value(\
            SettingsKeys.planetARMCEnabledForDeclinationKey, \
            SettingsKeys.planetARMCEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("ARMC")
        
        if settings.value(\
            SettingsKeys.planetVertexEnabledForDeclinationKey, \
            SettingsKeys.planetVertexEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Vertex")
        
        if settings.value(\
            SettingsKeys.planetEquatorialAscendantEnabledForDeclinationKey, \
            SettingsKeys.planetEquatorialAscendantEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("EquatorialAscendant")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant1EnabledForDeclinationKey, \
            SettingsKeys.planetCoAscendant1EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant1")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant2EnabledForDeclinationKey, \
            SettingsKeys.planetCoAscendant2EnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant2")
        
        if settings.value(\
            SettingsKeys.planetPolarAscendantEnabledForDeclinationKey, \
            SettingsKeys.planetPolarAscendantEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("PolarAscendant")
        
        if settings.value(\
            SettingsKeys.planetHoraLagnaEnabledForDeclinationKey, \
            SettingsKeys.planetHoraLagnaEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("HoraLagna")
        
        if settings.value(\
            SettingsKeys.planetGhatiLagnaEnabledForDeclinationKey, \
            SettingsKeys.planetGhatiLagnaEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("GhatiLagna")
        
        if settings.value(\
            SettingsKeys.planetMeanLunarApogeeEnabledForDeclinationKey, \
            SettingsKeys.planetMeanLunarApogeeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("MeanLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetOsculatingLunarApogeeEnabledForDeclinationKey, \
            SettingsKeys.planetOsculatingLunarApogeeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("OsculatingLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForDeclinationKey, \
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForDeclinationKey, \
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarPerigee")
        
        if settings.value(\
            SettingsKeys.planetSunEnabledForDeclinationKey, \
            SettingsKeys.planetSunEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Sun")
        
        if settings.value(\
            SettingsKeys.planetMoonEnabledForDeclinationKey, \
            SettingsKeys.planetMoonEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Moon")
        
        if settings.value(\
            SettingsKeys.planetMercuryEnabledForDeclinationKey, \
            SettingsKeys.planetMercuryEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Mercury")
        
        if settings.value(\
            SettingsKeys.planetVenusEnabledForDeclinationKey, \
            SettingsKeys.planetVenusEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Venus")
        
        if settings.value(\
            SettingsKeys.planetEarthEnabledForDeclinationKey, \
            SettingsKeys.planetEarthEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Earth")
        
        if settings.value(\
            SettingsKeys.planetMarsEnabledForDeclinationKey, \
            SettingsKeys.planetMarsEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Mars")
        
        if settings.value(\
            SettingsKeys.planetJupiterEnabledForDeclinationKey, \
            SettingsKeys.planetJupiterEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Jupiter")
        
        if settings.value(\
            SettingsKeys.planetSaturnEnabledForDeclinationKey, \
            SettingsKeys.planetSaturnEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Saturn")
        
        if settings.value(\
            SettingsKeys.planetUranusEnabledForDeclinationKey, \
            SettingsKeys.planetUranusEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Uranus")
        
        if settings.value(\
            SettingsKeys.planetNeptuneEnabledForDeclinationKey, \
            SettingsKeys.planetNeptuneEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Neptune")
        
        if settings.value(\
            SettingsKeys.planetPlutoEnabledForDeclinationKey, \
            SettingsKeys.planetPlutoEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Pluto")
        
        if settings.value(\
            SettingsKeys.planetMeanNorthNodeEnabledForDeclinationKey, \
            SettingsKeys.planetMeanNorthNodeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("MeanNorthNode")
        
        if settings.value(\
            SettingsKeys.planetMeanSouthNodeEnabledForDeclinationKey, \
            SettingsKeys.planetMeanSouthNodeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("MeanSouthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueNorthNodeEnabledForDeclinationKey, \
            SettingsKeys.planetTrueNorthNodeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("TrueNorthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueSouthNodeEnabledForDeclinationKey, \
            SettingsKeys.planetTrueSouthNodeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("TrueSouthNode")
        
        if settings.value(\
            SettingsKeys.planetCeresEnabledForDeclinationKey, \
            SettingsKeys.planetCeresEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Ceres")
        
        if settings.value(\
            SettingsKeys.planetPallasEnabledForDeclinationKey, \
            SettingsKeys.planetPallasEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Pallas")
        
        if settings.value(\
            SettingsKeys.planetJunoEnabledForDeclinationKey, \
            SettingsKeys.planetJunoEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Juno")
        
        if settings.value(\
            SettingsKeys.planetVestaEnabledForDeclinationKey, \
            SettingsKeys.planetVestaEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Vesta")
        
        if settings.value(\
            SettingsKeys.planetIsisEnabledForDeclinationKey, \
            SettingsKeys.planetIsisEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Isis")
        
        if settings.value(\
            SettingsKeys.planetNibiruEnabledForDeclinationKey, \
            SettingsKeys.planetNibiruEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Nibiru")
        
        if settings.value(\
            SettingsKeys.planetChironEnabledForDeclinationKey, \
            SettingsKeys.planetChironEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Chiron")
        
        if settings.value(\
            SettingsKeys.planetGulikaEnabledForDeclinationKey, \
            SettingsKeys.planetGulikaEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Gulika")
        
        if settings.value(\
            SettingsKeys.planetMandiEnabledForDeclinationKey, \
            SettingsKeys.planetMandiEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("Mandi")
        
        if settings.value(\
            SettingsKeys.planetMeanOfFiveEnabledForDeclinationKey, \
            SettingsKeys.planetMeanOfFiveEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("MeanOfFive")
        
        if settings.value(\
            SettingsKeys.planetCycleOfEightEnabledForDeclinationKey, \
            SettingsKeys.planetCycleOfEightEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("CycleOfEight")
        
        if settings.value(\
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForDeclinationKey, \
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("AvgMaJuSaUrNePl")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaUrNeEnabledForDeclinationKey, \
            SettingsKeys.planetAvgJuSaUrNeEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSaUrNe")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaEnabledForDeclinationKey, \
            SettingsKeys.planetAvgJuSaEnabledForDeclinationDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSa")


        return enabledPlanetNames
        
    def _getPlanetNamesToDisplayForLatitude(self):
        """Function to return a list of planet names that should be
        used to display latitude information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        # Return value.
        enabledPlanetNames = []

        settings = QSettings()
        
        if settings.value(\
            SettingsKeys.planetH1EnabledForLatitudeKey, \
            SettingsKeys.planetH1EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H1")
        
        if settings.value(\
            SettingsKeys.planetH2EnabledForLatitudeKey, \
            SettingsKeys.planetH2EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H2")
        
        if settings.value(\
            SettingsKeys.planetH3EnabledForLatitudeKey, \
            SettingsKeys.planetH3EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H3")
        
        if settings.value(\
            SettingsKeys.planetH4EnabledForLatitudeKey, \
            SettingsKeys.planetH4EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H4")
        
        if settings.value(\
            SettingsKeys.planetH5EnabledForLatitudeKey, \
            SettingsKeys.planetH5EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H5")
        
        if settings.value(\
            SettingsKeys.planetH6EnabledForLatitudeKey, \
            SettingsKeys.planetH6EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H6")
        
        if settings.value(\
            SettingsKeys.planetH7EnabledForLatitudeKey, \
            SettingsKeys.planetH7EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H7")
        
        if settings.value(\
            SettingsKeys.planetH8EnabledForLatitudeKey, \
            SettingsKeys.planetH8EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H8")
        
        if settings.value(\
            SettingsKeys.planetH9EnabledForLatitudeKey, \
            SettingsKeys.planetH9EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H9")
        
        if settings.value(\
            SettingsKeys.planetH10EnabledForLatitudeKey, \
            SettingsKeys.planetH10EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H10")
        
        if settings.value(\
            SettingsKeys.planetH11EnabledForLatitudeKey, \
            SettingsKeys.planetH11EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H11")
        
        if settings.value(\
            SettingsKeys.planetH12EnabledForLatitudeKey, \
            SettingsKeys.planetH12EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("H12")
        
        if settings.value(\
            SettingsKeys.planetARMCEnabledForLatitudeKey, \
            SettingsKeys.planetARMCEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("ARMC")
        
        if settings.value(\
            SettingsKeys.planetVertexEnabledForLatitudeKey, \
            SettingsKeys.planetVertexEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Vertex")
        
        if settings.value(\
            SettingsKeys.planetEquatorialAscendantEnabledForLatitudeKey, \
            SettingsKeys.planetEquatorialAscendantEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("EquatorialAscendant")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant1EnabledForLatitudeKey, \
            SettingsKeys.planetCoAscendant1EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant1")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant2EnabledForLatitudeKey, \
            SettingsKeys.planetCoAscendant2EnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant2")
        
        if settings.value(\
            SettingsKeys.planetPolarAscendantEnabledForLatitudeKey, \
            SettingsKeys.planetPolarAscendantEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("PolarAscendant")
        
        if settings.value(\
            SettingsKeys.planetHoraLagnaEnabledForLatitudeKey, \
            SettingsKeys.planetHoraLagnaEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("HoraLagna")
        
        if settings.value(\
            SettingsKeys.planetGhatiLagnaEnabledForLatitudeKey, \
            SettingsKeys.planetGhatiLagnaEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("GhatiLagna")
        
        if settings.value(\
            SettingsKeys.planetMeanLunarApogeeEnabledForLatitudeKey, \
            SettingsKeys.planetMeanLunarApogeeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("MeanLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetOsculatingLunarApogeeEnabledForLatitudeKey, \
            SettingsKeys.planetOsculatingLunarApogeeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("OsculatingLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForLatitudeKey, \
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForLatitudeKey, \
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarPerigee")
        
        if settings.value(\
            SettingsKeys.planetSunEnabledForLatitudeKey, \
            SettingsKeys.planetSunEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Sun")
        
        if settings.value(\
            SettingsKeys.planetMoonEnabledForLatitudeKey, \
            SettingsKeys.planetMoonEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Moon")
        
        if settings.value(\
            SettingsKeys.planetMercuryEnabledForLatitudeKey, \
            SettingsKeys.planetMercuryEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Mercury")
        
        if settings.value(\
            SettingsKeys.planetVenusEnabledForLatitudeKey, \
            SettingsKeys.planetVenusEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Venus")
        
        if settings.value(\
            SettingsKeys.planetEarthEnabledForLatitudeKey, \
            SettingsKeys.planetEarthEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Earth")
        
        if settings.value(\
            SettingsKeys.planetMarsEnabledForLatitudeKey, \
            SettingsKeys.planetMarsEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Mars")
        
        if settings.value(\
            SettingsKeys.planetJupiterEnabledForLatitudeKey, \
            SettingsKeys.planetJupiterEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Jupiter")
        
        if settings.value(\
            SettingsKeys.planetSaturnEnabledForLatitudeKey, \
            SettingsKeys.planetSaturnEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Saturn")
        
        if settings.value(\
            SettingsKeys.planetUranusEnabledForLatitudeKey, \
            SettingsKeys.planetUranusEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Uranus")
        
        if settings.value(\
            SettingsKeys.planetNeptuneEnabledForLatitudeKey, \
            SettingsKeys.planetNeptuneEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Neptune")
        
        if settings.value(\
            SettingsKeys.planetPlutoEnabledForLatitudeKey, \
            SettingsKeys.planetPlutoEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Pluto")
        
        if settings.value(\
            SettingsKeys.planetMeanNorthNodeEnabledForLatitudeKey, \
            SettingsKeys.planetMeanNorthNodeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("MeanNorthNode")
        
        if settings.value(\
            SettingsKeys.planetMeanSouthNodeEnabledForLatitudeKey, \
            SettingsKeys.planetMeanSouthNodeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("MeanSouthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueNorthNodeEnabledForLatitudeKey, \
            SettingsKeys.planetTrueNorthNodeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("TrueNorthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueSouthNodeEnabledForLatitudeKey, \
            SettingsKeys.planetTrueSouthNodeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("TrueSouthNode")
        
        if settings.value(\
            SettingsKeys.planetCeresEnabledForLatitudeKey, \
            SettingsKeys.planetCeresEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Ceres")
        
        if settings.value(\
            SettingsKeys.planetPallasEnabledForLatitudeKey, \
            SettingsKeys.planetPallasEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Pallas")
        
        if settings.value(\
            SettingsKeys.planetJunoEnabledForLatitudeKey, \
            SettingsKeys.planetJunoEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Juno")
        
        if settings.value(\
            SettingsKeys.planetVestaEnabledForLatitudeKey, \
            SettingsKeys.planetVestaEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Vesta")
        
        if settings.value(\
            SettingsKeys.planetIsisEnabledForLatitudeKey, \
            SettingsKeys.planetIsisEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Isis")
        
        if settings.value(\
            SettingsKeys.planetNibiruEnabledForLatitudeKey, \
            SettingsKeys.planetNibiruEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Nibiru")
        
        if settings.value(\
            SettingsKeys.planetChironEnabledForLatitudeKey, \
            SettingsKeys.planetChironEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Chiron")
        
        if settings.value(\
            SettingsKeys.planetGulikaEnabledForLatitudeKey, \
            SettingsKeys.planetGulikaEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Gulika")
        
        if settings.value(\
            SettingsKeys.planetMandiEnabledForLatitudeKey, \
            SettingsKeys.planetMandiEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("Mandi")
        
        if settings.value(\
            SettingsKeys.planetMeanOfFiveEnabledForLatitudeKey, \
            SettingsKeys.planetMeanOfFiveEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("MeanOfFive")
        
        if settings.value(\
            SettingsKeys.planetCycleOfEightEnabledForLatitudeKey, \
            SettingsKeys.planetCycleOfEightEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("CycleOfEight")
        
        if settings.value(\
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForLatitudeKey, \
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("AvgMaJuSaUrNePl")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaUrNeEnabledForLatitudeKey, \
            SettingsKeys.planetAvgJuSaUrNeEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSaUrNe")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaEnabledForLatitudeKey, \
            SettingsKeys.planetAvgJuSaEnabledForLatitudeDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSa")


        return enabledPlanetNames
        
    def _getPlanetNamesToDisplayForGeoSidRadixChart(self):
        """Function to return a list of planet names that can be
        used to display longitude information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        # Return value.
        enabledPlanetNames = []
        
        settings = QSettings()
        
        if settings.value(\
            SettingsKeys.planetH1EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH1EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H1")
        
        if settings.value(\
            SettingsKeys.planetH2EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH2EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H2")
        
        if settings.value(\
            SettingsKeys.planetH3EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH3EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H3")
        
        if settings.value(\
            SettingsKeys.planetH4EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH4EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H4")
        
        if settings.value(\
            SettingsKeys.planetH5EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH5EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H5")
        
        if settings.value(\
            SettingsKeys.planetH6EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH6EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H6")
        
        if settings.value(\
            SettingsKeys.planetH7EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH7EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H7")
        
        if settings.value(\
            SettingsKeys.planetH8EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH8EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H8")
        
        if settings.value(\
            SettingsKeys.planetH9EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH9EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H9")
        
        if settings.value(\
            SettingsKeys.planetH10EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH10EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H10")
        
        if settings.value(\
            SettingsKeys.planetH11EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH11EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H11")
        
        if settings.value(\
            SettingsKeys.planetH12EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetH12EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H12")
        
        if settings.value(\
            SettingsKeys.planetARMCEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetARMCEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("ARMC")
        
        if settings.value(\
            SettingsKeys.planetVertexEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetVertexEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Vertex")
        
        if settings.value(\
            SettingsKeys.planetEquatorialAscendantEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetEquatorialAscendantEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("EquatorialAscendant")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant1EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetCoAscendant1EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant1")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant2EnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetCoAscendant2EnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant2")
        
        if settings.value(\
            SettingsKeys.planetPolarAscendantEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetPolarAscendantEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("PolarAscendant")
        
        if settings.value(\
            SettingsKeys.planetHoraLagnaEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetHoraLagnaEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("HoraLagna")
        
        if settings.value(\
            SettingsKeys.planetGhatiLagnaEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetGhatiLagnaEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("GhatiLagna")
        
        if settings.value(\
            SettingsKeys.planetMeanLunarApogeeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMeanLunarApogeeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetOsculatingLunarApogeeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetOsculatingLunarApogeeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("OsculatingLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarPerigee")
        
        if settings.value(\
            SettingsKeys.planetSunEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetSunEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Sun")
        
        if settings.value(\
            SettingsKeys.planetMoonEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMoonEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Moon")
        
        if settings.value(\
            SettingsKeys.planetMercuryEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMercuryEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mercury")
        
        if settings.value(\
            SettingsKeys.planetVenusEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetVenusEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Venus")
        
        if settings.value(\
            SettingsKeys.planetEarthEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetEarthEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Earth")
        
        if settings.value(\
            SettingsKeys.planetMarsEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMarsEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mars")
        
        if settings.value(\
            SettingsKeys.planetJupiterEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetJupiterEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Jupiter")
        
        if settings.value(\
            SettingsKeys.planetSaturnEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetSaturnEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Saturn")
        
        if settings.value(\
            SettingsKeys.planetUranusEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetUranusEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Uranus")
        
        if settings.value(\
            SettingsKeys.planetNeptuneEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetNeptuneEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Neptune")
        
        if settings.value(\
            SettingsKeys.planetPlutoEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetPlutoEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Pluto")
        
        if settings.value(\
            SettingsKeys.planetMeanNorthNodeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMeanNorthNodeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanNorthNode")
        
        if settings.value(\
            SettingsKeys.planetMeanSouthNodeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMeanSouthNodeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanSouthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueNorthNodeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetTrueNorthNodeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("TrueNorthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueSouthNodeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetTrueSouthNodeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("TrueSouthNode")
        
        if settings.value(\
            SettingsKeys.planetCeresEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetCeresEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Ceres")
        
        if settings.value(\
            SettingsKeys.planetPallasEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetPallasEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Pallas")
        
        if settings.value(\
            SettingsKeys.planetJunoEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetJunoEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Juno")
        
        if settings.value(\
            SettingsKeys.planetVestaEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetVestaEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Vesta")
        
        if settings.value(\
            SettingsKeys.planetIsisEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetIsisEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Isis")
        
        if settings.value(\
            SettingsKeys.planetNibiruEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetNibiruEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Nibiru")
        
        if settings.value(\
            SettingsKeys.planetChironEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetChironEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Chiron")
        
        if settings.value(\
            SettingsKeys.planetGulikaEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetGulikaEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Gulika")
        
        if settings.value(\
            SettingsKeys.planetMandiEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMandiEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mandi")
        
        if settings.value(\
            SettingsKeys.planetMeanOfFiveEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetMeanOfFiveEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanOfFive")
        
        if settings.value(\
            SettingsKeys.planetCycleOfEightEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetCycleOfEightEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CycleOfEight")
        
        if settings.value(\
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgMaJuSaUrNePl")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaUrNeEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetAvgJuSaUrNeEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSaUrNe")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaEnabledForGeoSidRadixChartKey, \
            SettingsKeys.planetAvgJuSaEnabledForGeoSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSa")


        return enabledPlanetNames
        
    def _getPlanetNamesToDisplayForGeoTropRadixChart(self):
        """Function to return a list of planet names that can be
        used to display longitude information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        # Return value.
        enabledPlanetNames = []
        
        settings = QSettings()
        
        if settings.value(\
            SettingsKeys.planetH1EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH1EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H1")
        
        if settings.value(\
            SettingsKeys.planetH2EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH2EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H2")
        
        if settings.value(\
            SettingsKeys.planetH3EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH3EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H3")
        
        if settings.value(\
            SettingsKeys.planetH4EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH4EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H4")
        
        if settings.value(\
            SettingsKeys.planetH5EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH5EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H5")
        
        if settings.value(\
            SettingsKeys.planetH6EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH6EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H6")
        
        if settings.value(\
            SettingsKeys.planetH7EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH7EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H7")
        
        if settings.value(\
            SettingsKeys.planetH8EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH8EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H8")
        
        if settings.value(\
            SettingsKeys.planetH9EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH9EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H9")
        
        if settings.value(\
            SettingsKeys.planetH10EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH10EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H10")
        
        if settings.value(\
            SettingsKeys.planetH11EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH11EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H11")
        
        if settings.value(\
            SettingsKeys.planetH12EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetH12EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H12")
        
        if settings.value(\
            SettingsKeys.planetARMCEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetARMCEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("ARMC")
        
        if settings.value(\
            SettingsKeys.planetVertexEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetVertexEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Vertex")
        
        if settings.value(\
            SettingsKeys.planetEquatorialAscendantEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetEquatorialAscendantEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("EquatorialAscendant")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant1EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetCoAscendant1EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant1")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant2EnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetCoAscendant2EnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant2")
        
        if settings.value(\
            SettingsKeys.planetPolarAscendantEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetPolarAscendantEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("PolarAscendant")
        
        if settings.value(\
            SettingsKeys.planetHoraLagnaEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetHoraLagnaEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("HoraLagna")
        
        if settings.value(\
            SettingsKeys.planetGhatiLagnaEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetGhatiLagnaEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("GhatiLagna")
        
        if settings.value(\
            SettingsKeys.planetMeanLunarApogeeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMeanLunarApogeeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetOsculatingLunarApogeeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetOsculatingLunarApogeeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("OsculatingLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarPerigee")
        
        if settings.value(\
            SettingsKeys.planetSunEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetSunEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Sun")
        
        if settings.value(\
            SettingsKeys.planetMoonEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMoonEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Moon")
        
        if settings.value(\
            SettingsKeys.planetMercuryEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMercuryEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mercury")
        
        if settings.value(\
            SettingsKeys.planetVenusEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetVenusEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Venus")
        
        if settings.value(\
            SettingsKeys.planetEarthEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetEarthEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Earth")
        
        if settings.value(\
            SettingsKeys.planetMarsEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMarsEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mars")
        
        if settings.value(\
            SettingsKeys.planetJupiterEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetJupiterEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Jupiter")
        
        if settings.value(\
            SettingsKeys.planetSaturnEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetSaturnEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Saturn")
        
        if settings.value(\
            SettingsKeys.planetUranusEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetUranusEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Uranus")
        
        if settings.value(\
            SettingsKeys.planetNeptuneEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetNeptuneEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Neptune")
        
        if settings.value(\
            SettingsKeys.planetPlutoEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetPlutoEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Pluto")
        
        if settings.value(\
            SettingsKeys.planetMeanNorthNodeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMeanNorthNodeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanNorthNode")
        
        if settings.value(\
            SettingsKeys.planetMeanSouthNodeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMeanSouthNodeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanSouthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueNorthNodeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetTrueNorthNodeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("TrueNorthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueSouthNodeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetTrueSouthNodeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("TrueSouthNode")
        
        if settings.value(\
            SettingsKeys.planetCeresEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetCeresEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Ceres")
        
        if settings.value(\
            SettingsKeys.planetPallasEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetPallasEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Pallas")
        
        if settings.value(\
            SettingsKeys.planetJunoEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetJunoEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Juno")
        
        if settings.value(\
            SettingsKeys.planetVestaEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetVestaEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Vesta")
        
        if settings.value(\
            SettingsKeys.planetIsisEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetIsisEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Isis")
        
        if settings.value(\
            SettingsKeys.planetNibiruEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetNibiruEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Nibiru")
        
        if settings.value(\
            SettingsKeys.planetChironEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetChironEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Chiron")
        
        if settings.value(\
            SettingsKeys.planetGulikaEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetGulikaEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Gulika")
        
        if settings.value(\
            SettingsKeys.planetMandiEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMandiEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mandi")
        
        if settings.value(\
            SettingsKeys.planetMeanOfFiveEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetMeanOfFiveEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanOfFive")
        
        if settings.value(\
            SettingsKeys.planetCycleOfEightEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetCycleOfEightEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CycleOfEight")
        
        if settings.value(\
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgMaJuSaUrNePl")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaUrNeEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetAvgJuSaUrNeEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSaUrNe")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaEnabledForGeoTropRadixChartKey, \
            SettingsKeys.planetAvgJuSaEnabledForGeoTropRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSa")

        
        return enabledPlanetNames
        
    def _getPlanetNamesToDisplayForHelioSidRadixChart(self):
        """Function to return a list of planet names that can be
        used to display longitude information.  This is used because
        some planets don't make sense in this chart and it just clouds
        up the view.
        """

        # Return value.
        enabledPlanetNames = []
        
        settings = QSettings()
        
        if settings.value(\
            SettingsKeys.planetH1EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH1EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H1")
        
        if settings.value(\
            SettingsKeys.planetH2EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH2EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H2")
        
        if settings.value(\
            SettingsKeys.planetH3EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH3EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H3")
        
        if settings.value(\
            SettingsKeys.planetH4EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH4EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H4")
        
        if settings.value(\
            SettingsKeys.planetH5EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH5EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H5")
        
        if settings.value(\
            SettingsKeys.planetH6EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH6EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H6")
        
        if settings.value(\
            SettingsKeys.planetH7EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH7EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H7")
        
        if settings.value(\
            SettingsKeys.planetH8EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH8EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H8")
        
        if settings.value(\
            SettingsKeys.planetH9EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH9EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H9")
        
        if settings.value(\
            SettingsKeys.planetH10EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH10EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H10")
        
        if settings.value(\
            SettingsKeys.planetH11EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH11EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H11")
        
        if settings.value(\
            SettingsKeys.planetH12EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetH12EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("H12")
        
        if settings.value(\
            SettingsKeys.planetARMCEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetARMCEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("ARMC")
        
        if settings.value(\
            SettingsKeys.planetVertexEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetVertexEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Vertex")
        
        if settings.value(\
            SettingsKeys.planetEquatorialAscendantEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetEquatorialAscendantEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("EquatorialAscendant")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant1EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetCoAscendant1EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant1")
        
        if settings.value(\
            SettingsKeys.planetCoAscendant2EnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetCoAscendant2EnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CoAscendant2")
        
        if settings.value(\
            SettingsKeys.planetPolarAscendantEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetPolarAscendantEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("PolarAscendant")
        
        if settings.value(\
            SettingsKeys.planetHoraLagnaEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetHoraLagnaEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("HoraLagna")
        
        if settings.value(\
            SettingsKeys.planetGhatiLagnaEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetGhatiLagnaEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("GhatiLagna")
        
        if settings.value(\
            SettingsKeys.planetMeanLunarApogeeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMeanLunarApogeeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetOsculatingLunarApogeeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetOsculatingLunarApogeeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("OsculatingLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetInterpolatedLunarApogeeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarApogee")
        
        if settings.value(\
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetInterpolatedLunarPerigeeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("InterpolatedLunarPerigee")
        
        if settings.value(\
            SettingsKeys.planetSunEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetSunEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Sun")
        
        if settings.value(\
            SettingsKeys.planetMoonEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMoonEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Moon")
        
        if settings.value(\
            SettingsKeys.planetMercuryEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMercuryEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mercury")
        
        if settings.value(\
            SettingsKeys.planetVenusEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetVenusEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Venus")
        
        if settings.value(\
            SettingsKeys.planetEarthEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetEarthEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Earth")
        
        if settings.value(\
            SettingsKeys.planetMarsEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMarsEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mars")
        
        if settings.value(\
            SettingsKeys.planetJupiterEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetJupiterEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Jupiter")
        
        if settings.value(\
            SettingsKeys.planetSaturnEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetSaturnEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Saturn")
        
        if settings.value(\
            SettingsKeys.planetUranusEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetUranusEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Uranus")
        
        if settings.value(\
            SettingsKeys.planetNeptuneEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetNeptuneEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Neptune")
        
        if settings.value(\
            SettingsKeys.planetPlutoEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetPlutoEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Pluto")
        
        if settings.value(\
            SettingsKeys.planetMeanNorthNodeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMeanNorthNodeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanNorthNode")
        
        if settings.value(\
            SettingsKeys.planetMeanSouthNodeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMeanSouthNodeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanSouthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueNorthNodeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetTrueNorthNodeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("TrueNorthNode")
        
        if settings.value(\
            SettingsKeys.planetTrueSouthNodeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetTrueSouthNodeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("TrueSouthNode")
        
        if settings.value(\
            SettingsKeys.planetCeresEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetCeresEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Ceres")
        
        if settings.value(\
            SettingsKeys.planetPallasEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetPallasEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Pallas")
        
        if settings.value(\
            SettingsKeys.planetJunoEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetJunoEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Juno")
        
        if settings.value(\
            SettingsKeys.planetVestaEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetVestaEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Vesta")
        
        if settings.value(\
            SettingsKeys.planetIsisEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetIsisEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Isis")
        
        if settings.value(\
            SettingsKeys.planetNibiruEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetNibiruEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Nibiru")
        
        if settings.value(\
            SettingsKeys.planetChironEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetChironEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Chiron")
        
        if settings.value(\
            SettingsKeys.planetGulikaEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetGulikaEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Gulika")
        
        if settings.value(\
            SettingsKeys.planetMandiEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMandiEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("Mandi")
        
        if settings.value(\
            SettingsKeys.planetMeanOfFiveEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetMeanOfFiveEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("MeanOfFive")
        
        if settings.value(\
            SettingsKeys.planetCycleOfEightEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetCycleOfEightEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("CycleOfEight")
        
        if settings.value(\
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetAvgMaJuSaUrNePlEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgMaJuSaUrNePl")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaUrNeEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetAvgJuSaUrNeEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSaUrNe")
        
        if settings.value(\
            SettingsKeys.planetAvgJuSaEnabledForHelioSidRadixChartKey, \
            SettingsKeys.planetAvgJuSaEnabledForHelioSidRadixChartDefValue,
            type=bool):

            enabledPlanetNames.append("AvgJuSa")

        
        return enabledPlanetNames
        
    def setAstroChartXDatetime(self, chartNum, dt):
        """Sets the datetime of astrology chart 'chartNum'
        within the radix chart and other charts.

        Arguments:
        chartNum - int value holding the chart number to update.
        dt - datetime.datetime object holding the new timestamp.
        """

        # Wheel number (chart number) that will be updated.
        wheelNumber = chartNum

        # Get filters for what to display.
        planetNamesToDisplayForDeclination = \
            self._getPlanetNamesToDisplayForDeclination()
        planetNamesToDisplayForLatitude = \
            self._getPlanetNamesToDisplayForLatitude()
        planetNamesToDisplayForGeoSidRadixChart = \
            self._getPlanetNamesToDisplayForGeoSidRadixChart()
        planetNamesToDisplayForGeoTropRadixChart = \
            self._getPlanetNamesToDisplayForGeoTropRadixChart()
        planetNamesToDisplayForHelioSidRadixChart = \
            self._getPlanetNamesToDisplayForHelioSidRadixChart()

        # Get the PlanetaryInfo objects.
        planets = self.getPlanetaryInfosForDatetime(dt)
        
        # Update the planets' QGraphicsItems on each radix chart.
        for planet in planets:
            # Location label doesn't need to be updated here because
            # it gets updated when the BirthInfo gets set in this
            # widget.

            # Declination chart.
            planetDeclinationGraphicsItem = \
                self.declinationChart.\
                getPlanetDeclinationGraphicsItem(planet.name, chartNum)
            
            if planet.name in planetNamesToDisplayForDeclination:
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
                        degree=planet.geocentric['tropical']['declination'],
                        velocity=planet.geocentric['tropical']['declination_speed'],
                        planetGroupNumber=chartNum,
                        parent=self.declinationChart)
                else:
                    # The PlanetDeclinationGraphicsItem for this planet
                    # already exists for this chartNum.  Just update it.
                    degree = planet.geocentric['tropical']['declination']
                    velocity = planet.geocentric['tropical']['declination_speed']
                    planetDeclinationGraphicsItem.setDegreeAndVelocity(degree, velocity)
            else:
                if planetDeclinationGraphicsItem != None:
                    # Item exists when this planet should not be
                    # displayed.  The user must have just updated the
                    # settings, so remove the item.
                    self.graphicsScene.removeItem(planetDeclinationGraphicsItem)
        

            
            # Latitude chart.
            planetLatitudeGraphicsItem = \
                self.latitudeChart.\
                getPlanetLatitudeGraphicsItem(planet.name, chartNum)
            
            if planet.name in planetNamesToDisplayForLatitude:
                if planetLatitudeGraphicsItem == None:
                    # No PlanetLatitudeGraphicsItem exists yet for
                    # this planet, so create it.
                    planetLatitudeGraphicsItem = \
                        PlanetLatitudeGraphicsItem(
                        planet.name,
                        AstrologyUtils.getGlyphForPlanetName(planet.name),
                        AstrologyUtils.getGlyphFontSizeForPlanetName(planet.name),
                        AstrologyUtils.getAbbreviationForPlanetName(planet.name),
                        AstrologyUtils.getForegroundColorForPlanetName(planet.name),
                        AstrologyUtils.getBackgroundColorForPlanetName(planet.name),
                        degree=planet.geocentric['tropical']['latitude'],
                        velocity=planet.geocentric['tropical']['latitude_speed'],
                        planetGroupNumber=chartNum,
                        parent=self.latitudeChart)
                else:
                    # The PlanetLatitudeGraphicsItem for this planet
                    # already exists for this chartNum.  Just update it.
                    degree = planet.geocentric['tropical']['latitude']
                    velocity = planet.geocentric['tropical']['latitude_speed']
                    planetLatitudeGraphicsItem.setDegreeAndVelocity(degree, velocity)
            else:
                if planetLatitudeGraphicsItem != None:
                    # Item exists when this planet should not be
                    # displayed.  The user must have just updated the
                    # settings, so remove the item.
                    self.graphicsScene.removeItem(planetLatitudeGraphicsItem)
        

            
            # Geocentric Sidereal.
            radixPlanetGraphicsItem = \
                self.geoSidRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
                
            if planet.name in planetNamesToDisplayForGeoSidRadixChart:
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
            else:
                if radixPlanetGraphicsItem != None:
                    # Item exists when this planet should not be
                    # displayed.  The user must have just updated the
                    # settings, so remove the item.
                    self.graphicsScene.removeItem(radixPlanetGraphicsItem)


            # Geocentric Tropical.
            radixPlanetGraphicsItem = \
                self.geoTropRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
                
            if planet.name in planetNamesToDisplayForGeoTropRadixChart:
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
            else:
                if radixPlanetGraphicsItem != None:
                    # Item exists when this planet should not be
                    # displayed.  The user must have just updated the
                    # settings, so remove the item.
                    self.graphicsScene.removeItem(radixPlanetGraphicsItem)
            

            # Heliocentric Sidereal.
            radixPlanetGraphicsItem = \
                self.helioSidRadixChartGraphicsItem.\
                getRadixPlanetGraphicsItem(planet.name, wheelNumber)
            
            if planet.name in planetNamesToDisplayForHelioSidRadixChart:
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
            else:
                if radixPlanetGraphicsItem != None:
                    # Item exists when this planet should not be
                    # displayed.  The user must have just updated the
                    # settings, so remove the item.
                    self.graphicsScene.removeItem(radixPlanetGraphicsItem)

        # Call update for the declination chart.
        self.declinationChart.update()
        
        # Call update for the latitude chart.
        self.latitudeChart.update()
        
        # Update the aspects for the radix charts.

        # Geocentric Sidereal.
        self.geoSidRadixChartGraphicsItem.redrawAspects()
        self.geoSidRadixChartGraphicsItem.update()
        
        # Geocentric Tropical.
        self.geoTropRadixChartGraphicsItem.redrawAspects()
        self.geoTropRadixChartGraphicsItem.update()

        # Heliocentric Sidereal.
        self.helioSidRadixChartGraphicsItem.redrawAspects()
        self.helioSidRadixChartGraphicsItem.update()

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

        # Get the PlanetaryInfo objects.  The location values in this
        # list aren't used.  We only need this so we have a list of
        # planet names used.
        planets = self.getPlanetaryInfosForDatetime(\
            datetime.datetime.now(pytz.utc))

        for planet in planets:

            # Remove QGraphicsItems on each chart type.
            
            # Update the declination chart.
            planetDeclinationGraphicsItem = \
                self.declinationChart.\
                getPlanetDeclinationGraphicsItem(planet.name, chartNum)

            if planetDeclinationGraphicsItem != None:
                self.graphicsScene.removeItem(planetDeclinationGraphicsItem)
        
            # Update the latitude chart.
            planetLatitudeGraphicsItem = \
                self.latitudeChart.\
                getPlanetLatitudeGraphicsItem(planet.name, chartNum)

            if planetLatitudeGraphicsItem != None:
                self.graphicsScene.removeItem(planetLatitudeGraphicsItem)
        
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

        # Call update for the declination chart.
        self.declinationChart.update()
        
        # Call update for the latitude chart.
        self.latitudeChart.update()
        
        # Update the aspects for the radix charts.
        
        # Geocentric Sidereal.
        self.geoSidRadixChartGraphicsItem.redrawAspects()
        self.geoSidRadixChartGraphicsItem.update()
        
        # Geocentric Tropical.
        self.geoTropRadixChartGraphicsItem.redrawAspects()
        self.geoTropRadixChartGraphicsItem.update()

        # Heliocentric Sidereal.
        self.helioSidRadixChartGraphicsItem.redrawAspects()
        self.helioSidRadixChartGraphicsItem.update()

        
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
        

def testConvertAngleToDegMinSecStr():
    print("Running " + inspect.stack()[0][3] + "()")
    
    angles = [-0.0,
              0.0,
              0,
              0.1,
              0.11111,
              0.8,
              133.333333,
              120,
              144,
              2,
              360,
              721.314]

    for angle in angles:
        formattedStr = AstrologyUtils.convertAngleToDegMinSecStr(angle)
        print("    Angle {:>10} == {}".format(angle, formattedStr))

def testConvertAngleToDegMinSec():
    print("Running " + inspect.stack()[0][3] + "()")

    angles = [-0.0,
              0.0,
              0,
              0.1,
              0.11111,
              0.8,
              133.333333,
              120,
              144,
              2,
              360,
              721.314]

    for angle in angles:
        (deg, min, sec) = AstrologyUtils.convertAngleToDegMinSec(angle)

        print("    Angle {:>10} == {} deg {} min {} sec".\
              format(angle, deg, min, sec))
    
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


def testPlanetLatitudeGraphicsItem():
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
    
    chartItem = LatitudeChartGraphicsItem()
    scene.addItem(chartItem)

    moon = \
        PlanetLatitudeGraphicsItem(
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
        PlanetLatitudeGraphicsItem(
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
        PlanetLatitudeGraphicsItem(
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
        PlanetLatitudeGraphicsItem(
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
        PlanetLatitudeGraphicsItem(
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
        PlanetLatitudeGraphicsItem(
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


def testLatitudeChartGraphicsItem():
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
    
    chartItem = LatitudeChartGraphicsItem()
    
    scene.addItem(chartItem)

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

    p = Ephemeris.getH1PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH2PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH3PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH4PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH5PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH6PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH7PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH8PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH9PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH10PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH11PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH12PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getARMCPlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getVertexPlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getEquatorialAscendantPlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getCoAscendant1PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getCoAscendant2PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getPolarAscendantPlanetaryInfo(now)
    planets.append(p)
    
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

    # TODO:  add HoraLagna, GhatiLagna, Gulika, Mandi, MeanSouthNode, TrueSouthNode.
    
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

    p = Ephemeris.getH1PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH2PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH3PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH4PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH5PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH6PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH7PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH8PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH9PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH10PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH11PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getH12PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getARMCPlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getVertexPlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getEquatorialAscendantPlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getCoAscendant1PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getCoAscendant2PlanetaryInfo(now)
    planets.append(p)
    
    p = Ephemeris.getPolarAscendantPlanetaryInfo(now)
    planets.append(p)
    
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

    # TODO:  add HoraLagna, GhatiLagna, Gulika, Mandi, MeanSouthNode, TrueSouthNode.
    

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
    testConvertAngleToDegMinSecStr()
    testConvertAngleToDegMinSec()
    #testSiderealRadixChartGraphicsItem()
    #testRadixPlanetGraphicsItem()
    #testDeclinationChartGraphicsItem()
    #testPlanetDeclinationGraphicsItem()
    #testLatitudeChartGraphicsItem()
    #testPlanetLatitudeGraphicsItem()
    #testLongitudeSpeedChartGraphicsItem()
    #testPlanetLongitudeSpeedGraphicsItem()
    #testPlanetaryInfoTableWidget()
    #testPlanetaryInfoTableGraphicsItem()
    #testAstrologyChartWidget()
    
    # Exit the app when all windows are closed.
    app.connect(app, SIGNAL("lastWindowClosed()"), logging.shutdown)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

    # Quit.
    print("Exiting.")
    import sys
    sys.exit()
    #app.exec_()
    

        
