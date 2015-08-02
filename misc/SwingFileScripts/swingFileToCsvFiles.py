#!/usr/bin/env python3
##############################################################################
# Script:  swingFileToCsvFiles.py.py
#
# Description:
#   Takes a SwingFile (.swg) and generates many CSV files from it.
#   One CSV is generated for each PriceBar timestamp in the SwingFile.
#   The CSV files generated have planetary location information
#   contained within.
#
#   To modify columns or parameters used to output the fields,
#   edit the variables at the top of function createCsvFiles()
#   in the source code below.
#
# Dependencies:
#   src/astrologychart.py
#   src/data_objects.py
#   src/ephemeris.py
#
# Usage:
# 
#   ./swingFileToCsvFiles.py.py --help
#   ./swingFileToCsvFiles.py.py --version
#
#   ./swingFileToCsvFiles.py.py \
#                       --swing-file=/tmp/inputSwingFile.swg \
#                       --output-directory=/tmp/swings
#
##############################################################################

import sys
import os
import pickle
import math

# For parsing command-line options
from optparse import OptionParser  

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Include some PriceChartingTool modules.
# This assumes that the relative directory from this script is: ../../src
thisScriptDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.dirname(os.path.dirname(thisScriptDir)) + os.sep + "src"
if srcDir not in sys.path:
    sys.path.insert(0, srcDir)
from ephemeris import Ephemeris
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene
from astrologychart import AstrologyUtils

from swing import SwingFileData

##############################################################################
# Global Variables
##############################################################################

# Version string.
VERSION = "0.1"

# SwingFile (.swg) file that we are reading from.
# This value is specified via command-line option.
swingFile = ""

# Output directory that will contain the generated CSV files.
# This value is specified via command-line option.
outputDirectory = ""

# For logging.
logLevel = logging.DEBUG
#logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

##############################################################################

def shutdown(rc):
    """Exits the script, but first flushes all logging handles, etc."""
    Ephemeris.closeEphemeris()
    logging.shutdown()
    sys.exit(rc)

def picklePriceChartDocumentDataToFile(pcdd, filename):
    """Pickles the given PriceChartDocumentData object to the given
    filename.

    Arguments:
    pcdd     - PriceChartDocumentData object to save.
    filename - str holding the full path of the PriceChartDocument (.pcd) file.
    
    Returns:
    True if the write operation succeeded without problems, False otherwise.
    """

    log.debug("Entered picklePriceChartDocumentDataToFile()")

    # Return value.
    rv = True

    priceChartDocumentData = pcdd

    # Pickle to file.
    with open(filename, "wb") as fh:
        try:
            pickle.dump(priceChartDocumentData, fh) 
            rv = True
        except pickle.PickleError as pe:
            log.error("Error while pickling a " +
                      "PriceChartDocumentData to file " + 
                      filename + 
                      ".  Error is: {}".format(pe) +
                      ".  PriceChartDocumentData object " + 
                      "has the following info: " + 
                      priceChartDocumentData.toString())
            rv = False

    log.debug("Exiting picklePriceChartDocumentDataToFile(), " + \
              "rv == {}".format(rv))
    return rv

def unpickleSwingFileDataFromFile(filename):
    """Un-Pickles a SwingFileData object from file.

    Arguments:
    filename - str holding the full path of the SwingFile (.swg) file.
    
    Returns:
    Upon success: SwingFileData obtained is then returned
    Upon failure: None is returned.
    """

    log.debug("Entered unpickleSwingFileDataFromFile()")

    # Return value.
    rv = None

    # Get the SwingFileData from filename.
    try:
        with open(filename, "rb") as fh:
            try:
                swingFileData = pickle.load(fh)

                # Verify it is a SwingFileData object.
                if isinstance(swingFileData, 
                              SwingFileData) == True:
                    rv = swingFileData
                else:
                    # Print error message.
                    log.error("Cannot load this object.  " + 
                              "The object unpickled from file " + 
                              filename + " is not a " + 
                              "SwingFileData.")
                    rv = None
            except pickle.UnpicklingError as upe:
                log.error("Error while unpickling a " +
                          "SwingFileData from file " + 
                          filename + 
                          ".  Error is: {}".format(upe))
                rv = None
    except IOError as e:
        log.error("IOError while trying to open a file: {}".\
                  format(e))

        rv = None

    #log.debug("rv == {}".format(rv))
    log.debug("Exiting unpickleSwingFileDataFromFile()")
    
    return rv

def ensureDirectoryExists(dirPath):
    """Ensures that the given path is a directory exists.
    If the path does not exist, then a directory for it is created.
    If the path exists but is not a directory, an error is reported and
    shutdown(1) is called.
    """
    
    # Check to see if the outputDirectory exists already.
    if os.path.exists(outputDirectory):
        # Directory outputDirectory exists.
        log.debug("outputDirectory exists.")
        
        # See if it is a directory.
        if os.path.isdir(outputDirectory):
            log.debug("outputDirectory exists, and is a directory.")
        else:
            log.debug("outputDirectory exists, but is not a directory.")
            log.error("The output directory specified exists " + \
                      "but is not a directory.  " + \
                      "Please specify a path that is not an existing file.")
            shutdown(1)
    else:
        # Create the outputDirectory since it does not exist yet.
        log.debug("outputDirectory does not exist.")
        
        try:
            os.makedirs(outputDirectory)
        except OSError as e:
            # EEXIST can happen if a directory is created between the
            # time we do the first check for it and when we try to
            # create the directory.  If it is not errno.EEXIST, then
            # we want to report the error.
            if e.errno != errno.EEXIST:
                log.error("Caught an OSError exception " + \
                          "while trying to create the output directory: {}".\
                          format(e))
                raise

def getPlanetaryInfosForDatetime(dt, birthInfo):
    """Helper function for getting a list of PlanetaryInfo objects
    to display in the astrology chart.
    """

    # Set the location again (required).
    Ephemeris.setGeographicPosition(birthInfo.longitudeDegrees,
                                    birthInfo.latitudeDegrees,
                                    birthInfo.elevation)
    
    # Get planetary info for all the planets.
    planets = []
    
    # Astrological house system for getting the house cusps.
    houseSystem = Ephemeris.HouseSys['Porphyry']
    
    planets.append(Ephemeris.getH1PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH2PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH3PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH4PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH5PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH6PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH7PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH8PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH9PlanetaryInfo(dt, houseSystem))
    planets.append(Ephemeris.getH10PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH11PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getH12PlanetaryInfo(dt, houseSystem))
    planets.append(Ephemeris.getARMCPlanetaryInfo(dt, houseSystem))
    planets.append(Ephemeris.getVertexPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getEquatorialAscendantPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getCoAscendant1PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getCoAscendant2PlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getPolarAscendantPlanetaryInfo(dt, houseSystem))
    #planets.append(Ephemeris.getHoraLagnaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getGhatiLagnaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMeanLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getOsculatingLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(dt))
    #planets.append(Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(dt))
    planets.append(Ephemeris.getSunPlanetaryInfo(dt))
    planets.append(Ephemeris.getMoonPlanetaryInfo(dt))
    planets.append(Ephemeris.getMercuryPlanetaryInfo(dt))
    planets.append(Ephemeris.getVenusPlanetaryInfo(dt))
    planets.append(Ephemeris.getEarthPlanetaryInfo(dt))
    planets.append(Ephemeris.getMarsPlanetaryInfo(dt))
    planets.append(Ephemeris.getJupiterPlanetaryInfo(dt))
    planets.append(Ephemeris.getSaturnPlanetaryInfo(dt))
    planets.append(Ephemeris.getUranusPlanetaryInfo(dt))
    planets.append(Ephemeris.getNeptunePlanetaryInfo(dt))
    planets.append(Ephemeris.getPlutoPlanetaryInfo(dt))
    planets.append(Ephemeris.getMeanNorthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
    planets.append(Ephemeris.getTrueNorthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getTrueSouthNodePlanetaryInfo(dt))
    #planets.append(Ephemeris.getCeresPlanetaryInfo(dt))
    #planets.append(Ephemeris.getPallasPlanetaryInfo(dt))
    #planets.append(Ephemeris.getJunoPlanetaryInfo(dt))
    #planets.append(Ephemeris.getVestaPlanetaryInfo(dt))
    planets.append(Ephemeris.getIsisPlanetaryInfo(dt))
    #planets.append(Ephemeris.getNibiruPlanetaryInfo(dt))
    planets.append(Ephemeris.getChironPlanetaryInfo(dt))
    #planets.append(Ephemeris.getGulikaPlanetaryInfo(dt))
    #planets.append(Ephemeris.getMandiPlanetaryInfo(dt))
    planets.append(Ephemeris.getMeanOfFivePlanetaryInfo(dt))
    planets.append(Ephemeris.getCycleOfEightPlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgJuSaUrNePlanetaryInfo(dt))
    planets.append(Ephemeris.getAvgJuSaPlanetaryInfo(dt))

    return planets

def filterOutNonsensicalValues(planetaryInfo):
    """Here we will do some filtering on the given PlanetaryInfo
    object.  We will be setting some values to None so that the
    field will end up being blank on the table, where it makes
    sense to do so.
    
    Returns:
    PlanetaryInfo with some fields set to None.
    """
    
    p = planetaryInfo
    
    tropical = "tropical"
    sidereal = "sidereal"
    
    if Ephemeris.isHouseCuspPlanetName(p.name) or \
           Ephemeris.isAscmcPlanetName(p.name):
        
        p.geocentric[tropical]['longitude_speed'] = None
        p.geocentric[tropical]['declination'] = None
        p.geocentric[tropical]['declination_speed'] = None
        p.geocentric[tropical]['latitude'] = None
        p.geocentric[tropical]['latitude_speed'] = None
        p.geocentric[sidereal]['longitude_speed'] = None
        p.geocentric[sidereal]['declination'] = None
        p.geocentric[sidereal]['declination_speed'] = None
        p.geocentric[sidereal]['latitude'] = None
        p.geocentric[sidereal]['latitude_speed'] = None
        
        p.heliocentric[tropical]['longitude'] = None
        p.heliocentric[tropical]['longitude_speed'] = None
        p.heliocentric[tropical]['declination'] = None
        p.heliocentric[tropical]['declination_speed'] = None
        p.heliocentric[tropical]['latitude'] = None
        p.heliocentric[tropical]['latitude_speed'] = None
        
        p.heliocentric[sidereal]['longitude'] = None
        p.heliocentric[sidereal]['longitude_speed'] = None
        p.heliocentric[sidereal]['declination'] = None
        p.heliocentric[sidereal]['declination_speed'] = None
        p.heliocentric[sidereal]['latitude'] = None
        p.heliocentric[sidereal]['latitude_speed'] = None
        
    elif p.name == "Sun":
        
        p.heliocentric[tropical]['longitude'] = None
        p.heliocentric[tropical]['longitude_speed'] = None
        p.heliocentric[tropical]['declination'] = None
        p.heliocentric[tropical]['declination_speed'] = None
        p.heliocentric[tropical]['latitude'] = None
        p.heliocentric[tropical]['latitude_speed'] = None
        
        p.heliocentric[sidereal]['longitude'] = None
        p.heliocentric[sidereal]['longitude_speed'] = None
        p.heliocentric[sidereal]['declination'] = None
        p.heliocentric[sidereal]['declination_speed'] = None
        p.heliocentric[sidereal]['latitude'] = None
        p.heliocentric[sidereal]['latitude_speed'] = None
        
    elif p.name == "MeanNorthNode" or \
             p.name == "TrueNorthNode" or \
             p.name == "MeanLunarApogee" or \
             p.name == "OsculatingLunarApogee" or \
             p.name == "InterpolatedLunarApogee" or \
             p.name == "InterpolatedLunarPerigee":
        
        if p.name == "MeanNorthNode" or \
               p.name == "TrueNorthNode":

            p.geocentric[tropical]['latitude'] = None
            p.geocentric[tropical]['latitude_speed'] = None
            
            p.geocentric[sidereal]['latitude'] = None
            p.geocentric[sidereal]['latitude_speed'] = None
            
        p.heliocentric[tropical]['longitude'] = None
        p.heliocentric[tropical]['longitude_speed'] = None
        p.heliocentric[tropical]['declination'] = None
        p.heliocentric[tropical]['declination_speed'] = None
        p.heliocentric[tropical]['latitude'] = None
        p.heliocentric[tropical]['latitude_speed'] = None
        
        p.heliocentric[sidereal]['longitude'] = None
        p.heliocentric[sidereal]['longitude_speed'] = None
        p.heliocentric[sidereal]['declination'] = None
        p.heliocentric[sidereal]['declination_speed'] = None
        p.heliocentric[sidereal]['latitude'] = None
        p.heliocentric[sidereal]['latitude_speed'] = None
        
    elif p.name == "Earth":
        
        p.geocentric[tropical]['longitude'] = None
        p.geocentric[tropical]['longitude_speed'] = None
        p.geocentric[tropical]['declination'] = None
        p.geocentric[tropical]['declination_speed'] = None
        p.geocentric[tropical]['latitude'] = None
        p.geocentric[tropical]['latitude_speed'] = None
        
        p.geocentric[sidereal]['longitude'] = None
        p.geocentric[sidereal]['longitude_speed'] = None
        p.geocentric[sidereal]['declination'] = None
        p.geocentric[sidereal]['declination_speed'] = None
        p.geocentric[sidereal]['latitude'] = None
        p.geocentric[sidereal]['latitude_speed'] = None
        
    return p

class TableFieldInfo:
    # Strings for the different types of planetary coordinate systems.
    geoStr = "Geo. "
    topoStr = "Topo. "
    helioStr = "Helio. "
    
    sidStr = "Sid. "
    tropStr = "Trop. "
    
    mod15LonStr = "Mod 15 Lon."
    mod40LonStr = "Mod 40 Lon."
    
    # Different measurements available.
    longitudeStr = "Lon."
    latitudeStr = "Lat."
    distanceStr = "Dist."
    
    longitudeSpeedStr = "Lon. Speed"
    latitudeSpeedStr = "Lat. Speed"
    distanceSpeedStr = "Dist. Speed"
    
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

    tropical = "tropical"
    sidereal = "sidereal"

    def __init__(self, headerStr, isEnabled):
        self.headerStr = headerStr
        self.isEnabled = isEnabled

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        return ""
    
class PlanetNameField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.planetStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        return p.name

class GeoTropLongitudeField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.longitudeStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToStrWithRasiAbbrev(value)
        return valueStr
    
class HelioTropLongitudeField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.longitudeStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.tropical]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToStrWithRasiAbbrev(value)
        return valueStr
    
class GeoTropMod15LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr + 
                          TableFieldInfo.tropStr +
                          TableFieldInfo.mod15LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['longitude']
        valueStr = ""
        if value != None:
            value = value % 15.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class HelioTropMod15LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.mod15LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.tropical]['longitude']
        valueStr = ""
        if value != None:
            value = value % 15.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class GeoTropMod40LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.mod40LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['longitude']
        valueStr = ""
        if value != None:
            value = value % 40.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class HelioTropMod40LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.mod40LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.tropical]['longitude']
        valueStr = ""
        if value != None:
            value = value % 40.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class GeoSidLongitudeField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.sidStr +
                          TableFieldInfo.longitudeStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToStrWithRasiAbbrev(value)
        return valueStr
    
class HelioSidLongitudeField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.sidStr +
                          TableFieldInfo.longitudeStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToStrWithRasiAbbrev(value)
        return valueStr
    
class GeoSidMod15LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.sidStr +
                          TableFieldInfo.mod15LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            value = value % 15.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class HelioSidMod15LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.sidStr +
                          TableFieldInfo.mod15LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            value = value % 15.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class GeoSidMod40LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.sidStr +
                          TableFieldInfo.mod40LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            value = value % 40.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class HelioSidMod40LonField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.sidStr +
                          TableFieldInfo.mod40LonStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            value = value % 40.0
            valueStr = "{:5.2f}".format(value)
        return valueStr
    
class GeoSidNavamsaField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.sidStr +
                          "Navamsa"),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToNavamsaStr(value)
        return valueStr
    
class GeoSidNakshatraField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.sidStr +
                          "Nak."),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToNakshatraAbbrev(value)
        return valueStr
    
class GeoSidNakshatraPadaField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.sidStr +
                          "Nak. Pada"),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            padaSize = 360 / 108.0
            pada = (math.floor(value / padaSize) % 4) + 1
            valueStr = "{}".format(pada)
        return valueStr
    
class GeoTropLonSpeedField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.longitudeSpeedStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['longitude_speed']
        valueStr = ""
        if value != None:
            valueStr = "{: 7.3f}".format(value)
        return valueStr
    
class GeoTropDeclinationField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.declinationStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['declination']
        valueStr = ""
        if value != None:
            valueStr = "{: 7.3f}".format(value)
        return valueStr
    
class GeoTropDeclinationSpeedField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.declinationSpeedStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['declination_speed']
        valueStr = ""
        if value != None:
            valueStr = "{: 7.3f}".format(value)
        return valueStr
    
class GeoTropLatitudeField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.latitudeStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['latitude']
        valueStr = ""
        if value != None:
            valueStr = "{: 7.3f}".format(value)
        return valueStr
    
class GeoTropLatitudeSpeedField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.geoStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.latitudeSpeedStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.geocentric[TableFieldInfo.tropical]['latitude_speed']
        valueStr = ""
        if value != None:
            valueStr = "{: 7.3f}".format(value)
        return valueStr
    
class HelioSidNavamsaField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.sidStr +
                          "Navamsa"),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToNavamsaStr(value)
        return valueStr
    
class HelioSidNakshatraField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.sidStr +
                          "Nak."),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            valueStr = \
                AstrologyUtils.\
                convertLongitudeToNakshatraAbbrev(value)
        return valueStr
    
class HelioSidNakshatraPadaField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.sidStr +
                          "Nak. Pada"),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.sidereal]['longitude']
        valueStr = ""
        if value != None:
            padaSize = 360 / 108.0
            pada = (math.floor(value / padaSize) % 4) + 1
            valueStr = "{}".format(pada)
        return valueStr
    
class HelioTropLatitudeField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.latitudeStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.tropical]['latitude']
        valueStr = ""
        if value != None:
            valueStr = "{: 7.3f}".format(value)
        return valueStr
    
class HelioTropLatitudeSpeedField(TableFieldInfo):
    def __init__(self, isEnabled):
        super().__init__(\
            headerStr=str(TableFieldInfo.helioStr +
                          TableFieldInfo.tropStr +
                          TableFieldInfo.latitudeSpeedStr),
            isEnabled=isEnabled)

    def getValue(self, p):
        """Virtual function that returns a string for the field value.
        Arguments:
        p - PlanetaryInfo object for this row.
        """
        
        value = p.heliocentric[TableFieldInfo.tropical]['latitude_speed']
        valueStr = ""
        if value != None:
            valueStr = "{: 7.3f}".format(value)
        return valueStr
    
def createCsvFiles(swingFileData, outputDirectory):
    """Creates CSV files in the given outputDirectory.  Each CSV file
    contains information about the planets at the moment of the high
    or low PriceBar.  
    """

    # If there are no PriceBars in swingFileData, then there is
    # nothing to do, so return.
    if len(swingFileData.priceBars) == 0:
        return

    # Make sure the directory exists.
    ensureDirectoryExists(outputDirectory)

    ############################
    # Flags for the fields.
    # This is also the order in which they will be output.
    #
    tableFieldInfos = []
    tableFieldInfos.append(PlanetNameField(isEnabled=True))
    tableFieldInfos.append(GeoTropLongitudeField(isEnabled=True))
    tableFieldInfos.append(HelioTropLongitudeField(isEnabled=True))
    tableFieldInfos.append(GeoTropMod15LonField(isEnabled=True))
    tableFieldInfos.append(HelioTropMod15LonField(isEnabled=True))
    tableFieldInfos.append(GeoTropMod40LonField(isEnabled=True))
    tableFieldInfos.append(HelioTropMod40LonField(isEnabled=True))
    tableFieldInfos.append(GeoSidLongitudeField(isEnabled=True))
    tableFieldInfos.append(HelioSidLongitudeField(isEnabled=True))
    tableFieldInfos.append(GeoSidMod15LonField(isEnabled=True))
    tableFieldInfos.append(HelioSidMod15LonField(isEnabled=True))
    tableFieldInfos.append(GeoSidMod40LonField(isEnabled=True))
    tableFieldInfos.append(HelioSidMod40LonField(isEnabled=True))
    tableFieldInfos.append(GeoSidNavamsaField(isEnabled=True))
    tableFieldInfos.append(GeoSidNakshatraField(isEnabled=True))
    tableFieldInfos.append(GeoSidNakshatraPadaField(isEnabled=True))
    tableFieldInfos.append(GeoTropLonSpeedField(isEnabled=True))
    tableFieldInfos.append(GeoTropDeclinationField(isEnabled=True))
    tableFieldInfos.append(GeoTropDeclinationSpeedField(isEnabled=True))
    tableFieldInfos.append(GeoTropLatitudeField(isEnabled=True))
    tableFieldInfos.append(GeoTropLatitudeSpeedField(isEnabled=True))
    tableFieldInfos.append(HelioSidNavamsaField(isEnabled=True))
    tableFieldInfos.append(HelioSidNakshatraField(isEnabled=True))
    tableFieldInfos.append(HelioSidNakshatraPadaField(isEnabled=True))
    tableFieldInfos.append(HelioTropLatitudeField(isEnabled=True))
    tableFieldInfos.append(HelioTropLatitudeSpeedField(isEnabled=True))

    
    endl = "\n"

    log.info("Found {} PriceBars in this SwingFile.".\
             format(len(swingFileData.priceBars)))
    
    # Go through each PriceBar in the swing file.
    # Each PriceBar in the swing file will get it's own CSV file created.
    for pb in swingFileData.priceBars:
        
        # Get a list of the PlanetaryInfos.
        planetaryInfos = \
            getPlanetaryInfosForDatetime(pb.timestamp,
                                         swingFileData.birthInfo)
        for i in range(len(planetaryInfos)):
            planetaryInfos[i] = \
                filterOutNonsensicalValues(planetaryInfos[i])
        
        # Text for this CSV file.
        text = ""
        
        # Get number of enabled fields.
        numEnabledFields = 0
        for tableFieldInfo in tableFieldInfos:
            if tableFieldInfo.isEnabled == True:
                numEnabledFields += 1
        
        # Get the headers.
        for tableFieldInfo in tableFieldInfos:
            if tableFieldInfo.isEnabled == True:
                text += tableFieldInfo.headerStr + ","
        if numEnabledFields > 0:
            text = text[:-1]
        text += endl

        # Get a row for each of the planets.
        for planetaryInfo in planetaryInfos:
            for tableFieldInfo in tableFieldInfos:
                if tableFieldInfo.isEnabled == True:
                    text += tableFieldInfo.getValue(planetaryInfo)
                    text += ","
            if numEnabledFields > 0:
                text = text[:-1]
            text += endl

        
        # Assemble what will be the filename of the CSV file.
        filename = "{}{:02}{:02}_{:02}{:02}_Tags".\
              format(pb.timestamp.year,
                     pb.timestamp.month,
                     pb.timestamp.day,
                     pb.timestamp.hour,
                     pb.timestamp.minute)
        for tag in pb.tags:
            filename += "_" + tag
        filename += ".csv"
        filename = outputDirectory + os.sep + filename
        
        # Write to file.
        log.info("Writing to file '{}' ...".format(filename))
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        
##############################################################################

if __name__ == "__main__":
    
    # Create the parser
    parser = OptionParser()
    
    # Specify all valid options.
    parser.add_option("-v", "--version",
                      action="store_true",
                      dest="version",
                      default=False,
                      help="Display script version info and author contact.")
    
    parser.add_option("--swing-file",
                      action="store",
                      type="str",
                      dest="swingFile",
                      default=None,
                      help="Specify the SwingFile (.swg) file " + \
                           "to load.",
                      metavar="<FILE>")
    
    parser.add_option("--output-directory",
                      action="store",
                      type="str",
                      dest="outputDirectory",
                      default=None,
                      help="Specify a directory to place the CSV files " + \
                      "into.  This can be a directory that exists already " + \
                      "or one that does not yet exist.",
                      metavar="<DIRECTORY>")
    
    # Parse the arguments into options.
    (options, args) = parser.parse_args()
    
    # Print version information if the flag was used.
    if (options.version == True):
        print(os.path.basename(sys.argv[0]) + " (Version " + VERSION + ")")
        print("By Ryan Luu, ryanluu@gmail.com")
        shutdown(0)
    
    # Get the pcd filename.
    if (options.swingFile == None):
        log.error("Please specify a SwingFile (.swg) file with " +
                  "the --swing-file option.")
        shutdown(1)
    else:
        log.debug("options.swingFile == {}".format(options.swingFile))
        swingFile = os.path.abspath(options.swingFile)
        log.debug("swingFile == {}".format(swingFile))
    
    # Get the output directory.
    if (options.outputDirectory != None):
        log.debug("options.outputDirectory == {}".\
                  format(options.outputDirectory))
        outputDirectory = os.path.abspath(options.outputDirectory)
        log.debug("outputDirectory == {}".\
                  format(outputDirectory))
        log.debug("os.path.dirname(outputDirectory) == {}".\
                  format(os.path.dirname(outputDirectory)))
    else:
        log.error("Please specify an output directory to " +
                  "the --output-directory option.")
        shutdown(1)
    
    ######################################
    
    # Initialize Ephemeris (required).
    Ephemeris.initialize()
    
    # Open the SwingFile.
    log.info("Loading SwingFile '{}' ...".format(swingFile))
    swingFileData = unpickleSwingFileDataFromFile(swingFile)
    if swingFileData == None:
        # Retrieval failed.  An error message should have been logged.
        shutdown(1)
    
    log.info("Creating CSV files ...")

    createCsvFiles(swingFileData, outputDirectory)
    
    # Execution completed.
    log.info("Done.")
    shutdown(0)

##############################################################################
