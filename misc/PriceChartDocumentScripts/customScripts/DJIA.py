#!/usr/bin/env python3
##############################################################################
# Description:
#
#   Module for adding various PriceBarChartArtifacts to a
#   PriceChartDocumentData object that are relevant to stocks.
#
##############################################################################

# For logging.
import logging

# For timestamps and timezone information.
import datetime
import pytz

# For PyQt UI classes.
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Include some PriceChartingTool modules.
from ephemeris import Ephemeris
from ephemeris_utils import EphemerisUtils
from color import Color
from data_objects import *
from pricebarchart import PriceBarChartGraphicsScene
from util import Util
from lunar_calendar_utils import LunarDate
from lunar_calendar_utils import LunarCalendarUtils

# Holds functions for adding artifacts for various aspects.
from planetaryCombinationsLibrary import PlanetaryCombinationsLibrary

##############################################################################
# Global variables
##############################################################################

# For logging.
#logLevel = logging.DEBUG
logLevel = logging.INFO
logging.basicConfig(format='%(levelname)s: %(message)s')
moduleName = globals()['__name__']
log = logging.getLogger(moduleName)
log.setLevel(logLevel)

# Start and ending timestamps for drawing.

#startDt = datetime.datetime(year=1979, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#startDt = datetime.datetime(year=1995, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
#endDt = datetime.datetime(year=2018, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)

startDt = datetime.datetime(year=1905, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)
#endDt   = datetime.datetime(year=1936, month=1, day=1,
#                            hour=0, minute=0, second=0,
#                            tzinfo=pytz.utc)
endDt   = datetime.datetime(year=1941, month=1, day=1,
                            hour=0, minute=0, second=0,
                            tzinfo=pytz.utc)

# High and low price limits for drawing the vertical lines.
highPrice = 22000.0
#highPrice = 15000.0
#highPrice = 4500.0
#highPrice = 400.0
#lowPrice = 240.0
lowPrice = 35.0
#lowPrice = 800.0
#lowPrice = 4500.0


##############################################################################

def processPCDD(pcdd, tag):
    """Module for adding various PriceBarChartArtifacts that are
    relevant to the chart.  The tag str used for the created
    artifacts is based the name of the function that is being called,
    without the 'add' string at the beginning.

    Arguments:
    pcdd - PriceChartDocumentData object that will be modified.
    tag  - str containing the tag.
           This implementation does not use this value.

    Returns:
    0 if the changes are to be saved to file.
    1 if the changes are NOT to be saved to file.
    """

    global highPrice
    global lowPrice

    # Return value.
    rv = 0

    stepSizeTd = datetime.timedelta(days=3)
    #highPrice = 800.0
    #highPrice = 600.0
    #lowPrice = 600.0
    #lowPrice = 300.0
    
    eastern = pytz.timezone("US/Eastern")
    central = pytz.timezone("US/Central")
    
    # Chicago:
    #lon = -87.627777777777
    #lat = 41.8819444444444444
    
    # New York City:
    lon = -74.0064
    lat = 40.7142
    
    Ephemeris.setGeographicPosition(lon, lat)
    success = True

    if False:
        for i in [0, 90, 180, 270]:
            planetName = "Jupiter"
            centricityType = "geocentric"
            longitudeType = "tropical"
            desiredDegree = Util.toNormalizedAngle(45 + i)
            maxErrorTd = datetime.timedelta(minutes=1)

            origPlanetName = planetName
            origCentricityType = centricityType
            
            dts = \
                EphemerisUtils.\
                getPlanetCrossingLongitudeDegTimestamps(\
                    startDt, endDt,
                    planetName,
                    centricityType, longitudeType, 
                    desiredDegree, maxErrorTd)

            tag = \
              origCentricityType + "_" + origPlanetName + \
              "_crossing_" + str(desiredDegree)
              
            color = Color.darkRed
            
            for dt in dts:
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)
        
    
    if False:
        for i in [0, 90, 180, 270]:
            planetName = "Venus"
            centricityType = "geocentric"
            longitudeType = "tropical"
            desiredDegree = 30 + i
            maxErrorTd = datetime.timedelta(minutes=1)

            origPlanetName = planetName
            origCentricityType = centricityType
            
            dts = \
                EphemerisUtils.\
                getPlanetCrossingLongitudeDegTimestamps(\
                    startDt, endDt,
                    planetName,
                    centricityType, longitudeType, 
                    desiredDegree, maxErrorTd)

            tag = \
              origCentricityType + "_" + origPlanetName + \
              "_crossing_" + str(desiredDegree)
              
            color = Color.darkRed
            
            for dt in dts:
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        planet1Name = "Mars"
        planet2Name = "Jupiter"
        centricityType = "geocentric"
        longitudeType = "tropical"
        planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
        planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
        degreeDifference = 0
        uniDirectionalAspectsFlag = True
        maxErrorTd = datetime.timedelta(minutes=1)

        dts = EphemerisUtils.getLongitudeAspectTimestamps(\
            startDt,
            endDt,
            planet1ParamsList,
            planet2ParamsList,
            degreeDifference,
            uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
            maxErrorTd=maxErrorTd)

        for dt in dts:
            tag = planet1Name + "_conjunct_" + planet2Name
            color = Color.darkRed
            PlanetaryCombinationsLibrary.addVerticalLine(\
                pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for i in [25, 360 - 25]:
            planet1Name = "Sun"
            planet2Name = "Mercury"
            centricityType = "geocentric"
            longitudeType = "tropical"
            planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
            planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
            degreeDifference = i
            uniDirectionalAspectsFlag = True
            maxErrorTd = datetime.timedelta(minutes=1)
    
            dts = EphemerisUtils.getLongitudeAspectTimestamps(\
                startDt,
                endDt,
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
                maxErrorTd=maxErrorTd)
    
            for dt in dts:
                tag = planet1Name + "_aspect_" + planet2Name + \
                    "_" + str(degreeDifference) + "_deg"
                color = Color.darkRed
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for i in [37, 360 - 37]:
            planet1Name = "Sun"
            planet2Name = "Venus"
            centricityType = "geocentric"
            longitudeType = "tropical"
            planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
            planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
            degreeDifference = i
            uniDirectionalAspectsFlag = True
            maxErrorTd = datetime.timedelta(minutes=1)
    
            dts = EphemerisUtils.getLongitudeAspectTimestamps(\
                startDt,
                endDt,
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
                maxErrorTd=maxErrorTd)
    
            for dt in dts:
                tag = planet1Name + "_aspect_" + planet2Name + \
                    "_" + str(degreeDifference) + "_deg"
                color = Color.darkRed
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for i in [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
            planet1Name = "Mars"
            planet2Name = "TrueNorthNode"
            centricityType = "geocentric"
            longitudeType = "tropical"
            planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
            planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
            degreeDifference = i
            uniDirectionalAspectsFlag = True
            maxErrorTd = datetime.timedelta(minutes=1)
    
            dts = EphemerisUtils.getLongitudeAspectTimestamps(\
                startDt,
                endDt,
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
                maxErrorTd=maxErrorTd)
    
            for dt in dts:
                tag = planet1Name + "_aspect_" + planet2Name + \
                    "_" + str(degreeDifference) + "_deg"
                color = Color.darkRed
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        angle = 122.75
        for i in [angle]:
            planet1Name = "Mars"
            planet2Name = "TrueNorthNode"
            centricityType = "geocentric"
            longitudeType = "tropical"
            planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
            planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
            degreeDifference = i
            uniDirectionalAspectsFlag = True
            maxErrorTd = datetime.timedelta(minutes=1)
    
            dts = EphemerisUtils.getLongitudeAspectTimestamps(\
                startDt,
                endDt,
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
                maxErrorTd=maxErrorTd)
    
            for dt in dts:
                tag = planet1Name + "_aspect_" + planet2Name + \
                    "_" + str(degreeDifference) + "_deg"
                color = Color.darkRed
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        # Wrong.
        angle = 37
        for i in [angle, 360 - angle]:
            planet1Name = "Venus"
            planet2Name = "TrueNorthNode"
            centricityType = "geocentric"
            longitudeType = "tropical"
            planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
            planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
            degreeDifference = i
            uniDirectionalAspectsFlag = True
            maxErrorTd = datetime.timedelta(minutes=1)
    
            dts = EphemerisUtils.getLongitudeAspectTimestamps(\
                startDt,
                endDt,
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
                maxErrorTd=maxErrorTd)
    
            for dt in dts:
                tag = planet1Name + "_aspect_" + planet2Name + \
                    "_" + str(degreeDifference) + "_deg"
                color = Color.darkRed
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        planet1Name = "Sun"
        planet2Name = "Mars"
        centricityType = "geocentric"
        longitudeType = "tropical"
        planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
        planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
        degreeDifference = 0
        uniDirectionalAspectsFlag = True
        maxErrorTd = datetime.timedelta(minutes=1)

        dts = EphemerisUtils.getLongitudeAspectTimestamps(\
            startDt,
            endDt,
            planet1ParamsList,
            planet2ParamsList,
            degreeDifference,
            uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
            maxErrorTd=maxErrorTd)

        for dt in dts:
            tag = planet1Name + "_conjunct_" + planet2Name
            color = Color.darkRed
            PlanetaryCombinationsLibrary.addVerticalLine(\
                pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for i in range(12):
            planetName = "Mars"
            centricityType = "geocentric"
            longitudeType = "tropical"
            desiredDegree = i * (360 / 12.0)
            maxErrorTd = datetime.timedelta(minutes=1)

            origPlanetName = planetName
            origCentricityType = centricityType
            
            dts = \
                EphemerisUtils.\
                getPlanetCrossingLongitudeDegTimestamps(\
                    startDt, endDt,
                    planetName,
                    centricityType, longitudeType, 
                    desiredDegree, maxErrorTd)
            tag = \
              origCentricityType + "_" + origPlanetName + \
              "_crossing_" + str(desiredDegree) + \
              "_degrees"

            color = Color.darkRed

            for dt in dts:
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        for i in range(12):
            planetName = "Venus"
            centricityType = "geocentric"
            longitudeType = "tropical"
            desiredDegree = i * (360 / 12.0)
            maxErrorTd = datetime.timedelta(minutes=1)

            origPlanetName = planetName
            origCentricityType = centricityType
            
            crossingsDts = \
                EphemerisUtils.\
                getPlanetCrossingLongitudeDegTimestamps(\
                    startDt, endDt,
                    planetName,
                    centricityType, longitudeType, 
                    desiredDegree, maxErrorTd)

            for crossingsDt in crossingsDts:
                planetName = "Sun"
                centricityType = "geocentric"
                longitudeType = "tropical"
                planetEpocDt = crossingsDt
                desiredDegreesElapsed = 0 * 360
                maxErrorTd = datetime.timedelta(minutes=1)

                dts = \
                    EphemerisUtils.\
                    getDatetimesOfElapsedLongitudeDegrees(\
                        planetName,
                        centricityType,
                        longitudeType,
                        planetEpocDt,
                        desiredDegreesElapsed,
                        maxErrorTd)

                tag = \
                  origCentricityType + "_" + origPlanetName + \
                  "_crossing_" + str(desiredDegree) + \
                  "_plus_" + centricityType + "_" + planetName + \
                  "_traversing_" + str(desiredDegreesElapsed) + \
                  "_degrees"

                color = Color.darkRed

                for dt in dts:
                    PlanetaryCombinationsLibrary.addVerticalLine(\
                        pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for i in range(12):
            planetName = "Venus"
            centricityType = "geocentric"
            longitudeType = "tropical"
            desiredDegree = i * (360 / 12.0)
            maxErrorTd = datetime.timedelta(minutes=1)

            origPlanetName = planetName
            origCentricityType = centricityType
            
            crossingsDts = \
                EphemerisUtils.\
                getPlanetCrossingLongitudeDegTimestamps(\
                    startDt, endDt,
                    planetName,
                    centricityType, longitudeType, 
                    desiredDegree, maxErrorTd)

            for crossingsDt in crossingsDts:
                planetName = "Sun"
                centricityType = "geocentric"
                longitudeType = "tropical"
                planetEpocDt = crossingsDt
                desiredDegreesElapsed = 0 * 360
                maxErrorTd = datetime.timedelta(minutes=1)

                dts = \
                    EphemerisUtils.\
                    getDatetimesOfElapsedLongitudeDegrees(\
                        planetName,
                        centricityType,
                        longitudeType,
                        planetEpocDt,
                        desiredDegreesElapsed,
                        maxErrorTd)

                tag = \
                  origCentricityType + "_" + origPlanetName + \
                  "_crossing_" + str(desiredDegree) + \
                  "_plus_" + centricityType + "_" + planetName + \
                  "_traversing_" + str(desiredDegreesElapsed) + \
                  "_degrees"

                color = Color.darkRed

                for dt in dts:
                    PlanetaryCombinationsLibrary.addVerticalLine(\
                        pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for i in range(12):
            planetName = "Venus"
            centricityType = "geocentric"
            longitudeType = "tropical"
            desiredDegree = i * (360 / 12.0)
            maxErrorTd = datetime.timedelta(minutes=1)

            origPlanetName = planetName
            origCentricityType = centricityType
            
            crossingsDts = \
                EphemerisUtils.\
                getPlanetCrossingLongitudeDegTimestamps(\
                    startDt, endDt,
                    planetName,
                    centricityType, longitudeType, 
                    desiredDegree, maxErrorTd)

            for crossingsDt in crossingsDts:
                planetName = "Sun"
                centricityType = "geocentric"
                longitudeType = "tropical"
                planetEpocDt = crossingsDt
                desiredDegreesElapsed = 1 * 360
                maxErrorTd = datetime.timedelta(minutes=1)

                dts = \
                    EphemerisUtils.\
                    getDatetimesOfElapsedLongitudeDegrees(\
                        planetName,
                        centricityType,
                        longitudeType,
                        planetEpocDt,
                        desiredDegreesElapsed,
                        maxErrorTd)

                tag = \
                  origCentricityType + "_" + origPlanetName + \
                  "_crossing_" + str(desiredDegree) + \
                  "_plus_" + centricityType + "_" + planetName + \
                  "_traversing_" + str(desiredDegreesElapsed) + \
                  "_degrees"

                color = Color.darkRed

                for dt in dts:
                    PlanetaryCombinationsLibrary.addVerticalLine(\
                        pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for i in range(7):
            planet1Name = "Venus"
            planet2Name = "TrueNorthNode"
            centricityType = "geocentric"
            longitudeType = "tropical"
            planet1ParamsList = [(planet1Name, centricityType, longitudeType)]
            planet2ParamsList = [(planet2Name, centricityType, longitudeType)]
            degreeDifference = i * (360 / 7.0)
            uniDirectionalAspectsFlag = True
            maxErrorTd = datetime.timedelta(minutes=1)

            origPlanetName = planet1Name + planet2Name
            origCentricityType = centricityType
            desiredDegree = degreeDifference
            
            crossingsDts = EphemerisUtils.getLongitudeAspectTimestamps(\
                startDt,
                endDt,
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag=uniDirectionalAspectsFlag,
                maxErrorTd=maxErrorTd)

            for crossingsDt in crossingsDts:
                planetName = "Sun"
                centricityType = "geocentric"
                longitudeType = "tropical"
                planetEpocDt = crossingsDt
                desiredDegreesElapsed = 3 * 360
                maxErrorTd = datetime.timedelta(minutes=1)

                dts = \
                    EphemerisUtils.\
                    getDatetimesOfElapsedLongitudeDegrees(\
                        planetName,
                        centricityType,
                        longitudeType,
                        planetEpocDt,
                        desiredDegreesElapsed,
                        maxErrorTd)

                tag = \
                  origCentricityType + "_" + origPlanetName + \
                  "_crossing_" + str(desiredDegree) + \
                  "_plus_" + centricityType + "_" + planetName + \
                  "_traversing_" + str(desiredDegreesElapsed) + \
                  "_degrees"

                color = Color.darkRed

                for dt in dts:
                    PlanetaryCombinationsLibrary.addVerticalLine(\
                        pcdd, dt, highPrice, lowPrice, tag, color)
        
    if False:
        for year in range(1896, 1940):
            if False:
                month = 1
                day = 0
                dt = \
                  LunarCalendarUtils.lunarDateToDatetime(
                      LunarDate(year=year, month=month, day=day),
                      tzInfo=central)
                tag = "LunarDate({}, {}, {})".format(year, month, day)
                color = Color.gray
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

            if False:
                month = 1
                day = 15
                dt = \
                  LunarCalendarUtils.lunarDateToDatetime(
                      LunarDate(year=year, month=month, day=day),
                      tzInfo=central)
                tag = "LunarDate({}, {}, {}) - Pesach / Easter full moon".format(year, month, day)
                color = Color.lightRed
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

            if False:
                month = 1
                day = 15
                dt1 = \
                    LunarCalendarUtils.lunarDateToDatetime(
                      LunarDate(year=year, month=month, day=day),
                      tzInfo=central)

                calendarDays = 49
                degreesElapsed = calendarDays * 360
                dts = \
                    EphemerisUtils.getDatetimesOfElapsedLongitudeDegrees(\
                        "AsSu", "geocentric", "tropical", dt1, degreesElapsed)
                dt = dts[0]
                tag = "Shavuot / Pentecost / Easter + {} CD.".format(calendarDays)
                
                color = Color.red
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

            if False:
                month = 7
                day = 0
                dt = \
                  LunarCalendarUtils.lunarDateToDatetime(
                      LunarDate(year=year, month=month, day=day),
                      tzInfo=central)
                tag = "LunarDate({}, {}, {}) - Rosh Hashanah".format(year, month, day)
                color = Color.gray
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

            if False:
                month = 7
                day = 15
                dt = \
                  LunarCalendarUtils.lunarDateToDatetime(
                      LunarDate(year=year, month=month, day=day),
                      tzInfo=central)
                tag = "LunarDate({}, {}, {}) - Sukkot".format(year, month, day)
                color = Color.darkRed
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

            if False:
                # Marie's birthday?
                # 194
                month = 7
                day = 14
                dt = \
                  LunarCalendarUtils.lunarDateToDatetime(
                      LunarDate(year=year, month=month, day=day),
                      tzInfo=central)
                tag = "LunarDate({}, {}, {})".format(year, month, day)
                color = Color.lightGray
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

            if False:
                # June 19, 1927.  Pg. 197
                # (+360, +588)
                # 79
                month = 3
                day = 19
                dt = \
                  LunarCalendarUtils.lunarDateToDatetime(
                      LunarDate(year=year, month=month, day=day),
                      tzInfo=central)
                tag = "LunarDate({}, {}, {}) - pg. 197".format(year, month, day)
                color = Color.lightYellow
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        # January 24, 1927.  Pg. 70
        # (+360, (+194, +388, +582))
        # 79
        month = 11
        day = 20
        year = 1926
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - pg. 70".format(year, month, day)
        color = Color.lightOrange
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        # RG's birthday 1906.  Texarkana? (Pg. 1)
        # 79
        month = 3
        day = 19
        year = 1906
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - Texarkana - pg. 1".format(year, month, day)
        color = Color.lightRed
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        # RG's birthday.  St. Marie?  (Pg. 226)
        # 69
        month = 3
        day = 9
        year = 1927
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - pg. 226".format(year, month, day)
        color = Color.lightRed
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

        # RG's birthday.  (Pg. 271)
        # Jubilee
        month = 4
        day = 2
        year = 1929
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - pg. 271".format(year, month, day)
        color = Color.lightRed
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        # Charles A. Lindbergh lands in Paris.  Pg. 105.
        # RG red letter day.  Pg. 105.
        # Gregorian date of May 21, 1927.
        # 49
        month = 2
        day = 19
        year = 1927
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - Paris - pg. 105".format(year, month, day)
        color = Color.lightRed
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

        # Supreme Commander Gordon in Paris.  Pg. 395.
        # 49
        month = 2
        day = 19
        year = 1932
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - SCG in Paris - pg. 395".format(year, month, day)
        color = Color.lightRed
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        # Walter talk with Robert.  Pg. 239
        # 274
        # Measure from here forwards and backwards!
        month = 11
        day = 4
        year = 1928
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - Middle of January, 1929 - pg. 239".format(year, month, day)
        color = Color.lightOrange
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        # Presidential Forecast?  (July 20, 1927) Pg. 218
        # 111
        month = 4
        day = 21
        year = 1927
        dt = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=year, month=month, day=day),
              tzInfo=central)
        tag = "LunarDate({}, {}, {}) - Presidential Forecast - pg. 218".format(year, month, day)
        color = Color.lightOrange
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        christmas1926Pg42 = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=1926, month=12, day=25),
              tzInfo=central)
        dt = christmas1926Pg42
        tag = "christmas1926Pg42"
        color = Color.blue
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        letterOfCommendationPg43 = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=1927, month=1, day=1),
              tzInfo=eastern)
        dt = letterOfCommendationPg43
        tag = "letterOfCommendationPg43"
        color = Color.orange
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        rgRoadToFameAndFortunePg70 = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=1927, month=1, day=24),
              tzInfo=central)
        dt = rgRoadToFameAndFortunePg70
        tag = "rgRoadToFameAndFortunePg70"
        color = Color.orange
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        marieHopePrayLoveOfHeartPg94 = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=1927, month=2, day=7),
              tzInfo=eastern)
        dt = marieHopePrayLoveOfHeartPg94
        tag = "marieHopePrayLoveOfHeartPg94"
        color = Color.red
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)
            
    if False:
        marieLoveAndTrustPg97 = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=1927, month=5, day=1),
              tzInfo=eastern)
        dt = marieLoveAndTrustPg97
        tag = "marieLoveAndTrustPg97"
        color = Color.lightRed
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        rgRedLetterDayPg105 = \
          LunarCalendarUtils.lunarDateToDatetime(
              LunarDate(year=1927, month=5, day=21),
              tzInfo=eastern)
        dt = rgRedLetterDayPg105
        tag = "rgRedLetterDayPg105"
        color = Color.lightRed
        PlanetaryCombinationsLibrary.addVerticalLine(\
            pcdd, dt, highPrice, lowPrice, tag, color)

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "heliocentric", "tropical",
            "Mars", "heliocentric", "tropical",
            degreeValue, color=Color.darkYellow)

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury", "heliocentric", "tropical",
            "Earth", "heliocentric", "tropical",
            degreeValue, color=Color.lightBabyBlue)

    if False:
        degreeValue = 279
        color = Color.lightRed
        success = PlanetaryCombinationsLibrary.\
            addPlanetCrossingLongitudeDegVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "geocentric", "tropical", "Mercury", degreeValue, color)
        
    if False:
        degreeValue = 192
        color = Color.lightOrange
        success = PlanetaryCombinationsLibrary.\
            addPlanetCrossingLongitudeDegVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "geocentric", "tropical", "Venus", degreeValue, color)
        
    if False:
        degreeValue = 69
        success = PlanetaryCombinationsLibrary.\
            addPlanetCrossingLongitudeDegVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "heliocentric", "tropical", "Venus", degreeValue)
        
    if False:
        degreeValue = 192
        success = PlanetaryCombinationsLibrary.\
            addPlanetCrossingLongitudeDegVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "heliocentric", "tropical", "Venus", degreeValue)
        
    if False:
        degreeValue = 275
        success = PlanetaryCombinationsLibrary.\
            addPlanetCrossingLongitudeDegVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "heliocentric", "tropical", "Venus", degreeValue)
        
    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLongitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        "Mercury")

    if True:
        success = PlanetaryCombinationsLibrary.\
        addGeoLongitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        "Venus")

    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLongitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        "Mars")

    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLongitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        "Jupiter")

    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLongitudeVelocityPolarityChangeVerticalLines(\
        pcdd, startDt, endDt, highPrice, lowPrice,
        "Saturn")

    ######################################

    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoConjunctionsOfDirectRetrogradeMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury")
    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury")


    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoConjunctionsOfDirectRetrogradeMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus")
    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus")


    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoConjunctionsOfDirectRetrogradeMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mars")
    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mars")


    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoConjunctionsOfDirectRetrogradeMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Jupiter")
    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Jupiter")


    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoConjunctionsOfDirectRetrogradeMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Saturn")
    if False:
        success = PlanetaryCombinationsLibrary.\
        addGeoLeastMeanGreatConjunctionsOfRetrogradeDirectMidpointsVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Saturn")

    ######################################

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.blue))

    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Moon", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=QColor(Qt.red))

    ######################################

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "heliocentric", "tropical",
            "Mars", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.red))
    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "heliocentric", "tropical",
            "Mars", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.darkMagenta))

    ######################################

    if True:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "geocentric", "tropical",
            "Sun", "geocentric", "tropical",
            degreeValue, color=Color.purple)
        
    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "heliocentric", "tropical",
            "Earth", "heliocentric", "tropical",
            degreeValue, color=Color.veryLightPurple)
        
    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "heliocentric", "tropical",
            "Earth", "heliocentric", "tropical",
            degreeValue, color=Color.veryLightPurple)
        
    ######################################

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury", "heliocentric", "tropical",
            "Earth", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.green))

    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Mercury", "heliocentric", "tropical",
            "Earth", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.darkYellow))
            #degreeValue, color=QColor(Qt.darkGreen))

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "heliocentric", "tropical",
            "Earth", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.magenta))

    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Venus", "heliocentric", "tropical",
            "Earth", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.darkMagenta))

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Earth", "heliocentric", "tropical",
            "Mars", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.red))

    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Earth", "heliocentric", "tropical",
            "Mars", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.darkRed))

    if False:
        degreeValue = 0
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Earth", "heliocentric", "tropical",
            "Jupiter", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.cyan))

    if False:
        degreeValue = 180
        success = PlanetaryCombinationsLibrary.\
            addLongitudeAspectVerticalLines(\
            pcdd, startDt, endDt, highPrice, lowPrice,
            "Earth", "heliocentric", "tropical",
            "Jupiter", "heliocentric", "tropical",
            degreeValue, color=QColor(Qt.darkCyan))

    ######################################

    if False:
        for degreeValue in [180]:
            success = PlanetaryCombinationsLibrary.\
                addPlanetCrossingLongitudeDegVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "geocentric", "tropical", "Mercury", degreeValue)

    if False:
        for degreeValue in [180]:
            success = PlanetaryCombinationsLibrary.\
                addPlanetCrossingLongitudeDegVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "geocentric", "tropical", "Venus", degreeValue)

    if False:
        for degreeValue in [180]:
            success = PlanetaryCombinationsLibrary.\
                addPlanetCrossingLongitudeDegVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "geocentric", "tropical", "Mars", degreeValue)

    if False:
        for degreeValue in [0, 90, 180, 270]:
            success = PlanetaryCombinationsLibrary.\
                addPlanetCrossingLongitudeDegVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "geocentric", "tropical", "Jupiter", degreeValue)

    if False:
        if False:
            degreeValue = 0
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.darkRed)

            degreeValue = 90
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.lightRed)

            degreeValue = 180
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.lightRed)

            degreeValue = 270
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.lightRed)

        if False:
            degreeValue = 120
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.darkBabyBlue)

            degreeValue = 240
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.lightBabyBlue)

        if False:
            degreeValue = 33
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.purple)

            degreeValue = 153
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeValue, color=Color.lightPurple)

        if False:
            unit = 360 / 7.0
            degreeValues = [\
                    unit * 1,
                    unit * 2,
                    unit * 3,
                    unit * 4,
                    unit * 5,
                    unit * 6]
            for degreeValue in degreeValues:
                success = PlanetaryCombinationsLibrary.\
                    addLongitudeAspectVerticalLines(\
                    pcdd, startDt, endDt, highPrice, lowPrice,
                    "Sun", "geocentric", "tropical",
                    "TrueNorthNode", "geocentric", "tropical",
                    degreeValue, color=Color.veryLightPink)

    ######################################

    # Works well.
    if False:
        step = 360 / 20.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Works well.
    if False:
        step = 360 / 16.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Works well.
    if False:
        step = 360 / 16.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "heliocentric", "tropical",
                "Saturn", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Works pretty well.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Meh.
    if False:
        step = 360 / 18.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Works well.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Saturn", "geocentric", "tropical",
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Catches some highs and lows, many small ones also, so it isn't
    # that that great.
    if False:
        step = 360 / 20.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Saturn", "geocentric", "tropical",
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Did not work well.
    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Saturn", "geocentric", "tropical",
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Did not work work.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Saturn", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Caught some small turns, but then some looks like a handful of misses too.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 14.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Saturn", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 14.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Catches some bottoms very nicely, other turns probably need
    # other planets contributing.
    if False:
        step = 360 / 14.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    #########################################################################
    # The below entries were copied from my studies of stock LVS, so the comments may not be accurate.

    # This works well.  You can see the pulses of energy with this.
    if False:
        step = 360 / 16.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "tropical",
                "Saturn", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Did not work well.
    if False:
        step = 360 / 8.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step
    # Did not work well.
    if False:
        step = 360 / 16.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Jupiter", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # May be worth investigating further (or looking at different numbers).
    if False:
        step = 360 / 28.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Saturn", "geocentric", "tropical",
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "geocentric", "tropical",
                "Venus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Venus-Uranus didn't have much show up.

    # Planets may be related but this did not work well.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "tropical",
                "Saturn", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # This combination of planets is worth looking more closely at.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 18.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Worked okay, but need to half this interval.
    if False:
        step = 360 / 8.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # DId not work well.
    if False:
        step = 360 / 14.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Saturn", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Did not work well.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mars", "heliocentric", "tropical",
                "Venus", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Did not work well.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "Jupiter", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    # Did not work well.
    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "geocentric", "tropical",
                "Uranus", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "heliocentric", "tropical",
                "Mars", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Mercury", "heliocentric", "tropical",
                "Mars", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 12.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "tropical",
                "Mercury", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 24.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "tropical",
                "Mars", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "MeanNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "MeanNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 5.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 8.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Uranus", "heliocentric", "tropical",
                "Earth", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 8.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Neptune", "heliocentric", "tropical",
                "Earth", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 25
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "heliocentric", "tropical",
                "Saturn", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 7.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Venus", "geocentric", "tropical",
                "Venus", "heliocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        step = 360 / 12.0
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            success = PlanetaryCombinationsLibrary.\
                addLongitudeAspectVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "Sun", "geocentric", "tropical",
                "TrueNorthNode", "geocentric", "tropical",
                degreeDiff)
            degreeDiff += step

    if False:
        #start = 16.6666 + (11 * 30) # Sun position
        #start = 4.5333 + (10 * 30) # Venus position
        #start = 4.6 # Mercury position
        #start = 28.89 + (10 * 30) # Mars Helio position
        #start = (3 * 30) + 8.4 # Moon position.
        #start = (5 * 30) + 10.066 # Saturn position
        #start = (5 * 30) + 17.5 # TNode position
        #divisor = 5
        divisor = 2
        #divisor = 8
        #divisor = 24
        #divisor = 25
        #divisor = 120
        for i in range(divisor):
            degreeValue = Util.toNormalizedAngle(start + (i * 360 / divisor))
            success = PlanetaryCombinationsLibrary.\
                      addPlanetCrossingLongitudeDegVerticalLines(\
                pcdd, startDt, endDt, highPrice, lowPrice,
                "heliocentric", "tropical",
                "Mars", degreeValue)

    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mercury",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mars",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Uranus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Saturn",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="MeanOfFive",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoLongitudeVelocityLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="CycleOfEight",
    #    color=None, stepSizeTd=stepSizeTd)

    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice=700, lowPrice=660,
    #    planetName="Moon",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mercury",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Mars",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Jupiter",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Saturn",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Uranus",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Neptune",
    #    color=None, stepSizeTd=stepSizeTd)
    #success = PlanetaryCombinationsLibrary.addGeoDeclinationLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Pluto",
    #    color=None, stepSizeTd=stepSizeTd)


    p = 1000
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H1")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H2")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H3")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H4")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H5")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H6")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H7")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H8")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H9")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H10")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H11")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="H12")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="ARMC")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Vertex")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="EquatorialAscendant")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="CoAscendant1")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="CoAscendant2")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="PolarAscendant")
    #p += 20
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Sun")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Moon")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Mercury")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Venus")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Mars")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Jupiter")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Saturn")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Uranus")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Neptune")
    #p += 200
    #success = PlanetaryCombinationsLibrary.\
    #    addTimeMeasurementAndTiltedTextForNakshatraTransits(
    #    pcdd, startDt, endDt, price=p, planetName="Pluto")
    #p += 200


    if False:
        success = PlanetaryCombinationsLibrary.\
            addZeroDeclinationVerticalLines(
                pcdd, startDt, endDt, highPrice, lowPrice,
                planetName="Venus",
                color=Color.darkRed)
    
        success = PlanetaryCombinationsLibrary.\
            addDeclinationVelocityPolarityChangeVerticalLines(
                pcdd, startDt, endDt, highPrice, lowPrice,
                planetName="Venus",
                color=Color.lightRed)

    if False:
        success = PlanetaryCombinationsLibrary.\
            addGeoLongitudeElongationVerticalLines(
            pcdd, startDt, endDt, highPrice, lowPrice, planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addGeoLongitudeElongationVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice, planetName="Mercury")

    #success = PlanetaryCombinationsLibrary.\
    #    addContraparallelDeclinationAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addParallelDeclinationAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetOOBVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus")

    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus")
    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Jupiter", stepSizeTd=datetime.timedelta(days=7))
    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Saturn", stepSizeTd=datetime.timedelta(days=7))
    #success =  PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Uranus", stepSizeTd=datetime.timedelta(days=7))

    #success =  PlanetaryCombinationsLibrary.\
    #    addZeroGeoLatitudeVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addGeoLatitudeVelocityPolarityChangeVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice, planetName="Venus")

    #success = PlanetaryCombinationsLibrary.\
    #    addContraparallelGeoLatitudeAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addParallelGeoLatitudeAspectVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    planet1Name="Venus", planet2Name="Mars")

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetLongitudeTraversalIncrementsVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "geocentric", "sidereal",
    #    planetEpocDt=datetime.datetime(year=1976, month=4, day=1,
    #                                   hour=13, minute=0, second=0,
    #                                   tzinfo=pytz.utc),
    #    degreeIncrement=18)

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetLongitudeTraversalIncrementsVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Venus", "heliocentric", "sidereal",
    #    planetEpocDt=datetime.datetime(year=1970, month=3, day=21,
    #                                   hour=0, minute=0, second=0,
    #                                   tzinfo=pytz.utc),
    #    degreeIncrement=30)

    #success = PlanetaryCombinationsLibrary.\
    #    addPlanetLongitudeTraversalIncrementsVerticalLines(
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Sun", "geocentric", "tropical",
    #    planetEpocDt=datetime.datetime(year=1970, month=3, day=21,
    #                                   hour=6, minute=0, second=0,
    #                                   tzinfo=pytz.utc),
    #    degreeIncrement=15)

    #success = PlanetaryCombinationsLibrary.\
    #    addGeoLongitudeVelocityPolarityChangeVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice,
    #    "Mercury")


    #success = PlanetaryCombinationsLibrary.\
    #    addBayerTimeFactorsAstroVerticalLines(\
    #    pcdd, startDt, endDt, highPrice, lowPrice)

    ############################################################################

    # Testing new functions for longitude aspect timestamps.
    if False:
        aspectGroup = []
        step = 180
        start = 0
        stop = 180
        degreeDiff = start
        while degreeDiff < stop or Util.fuzzyIsEqual(degreeDiff, stop):
            aspectGroup.append(degreeDiff)
            degreeDiff += step

        planet1ParamsList = [("Venus", "geocentric", "sidereal")]
        planet2ParamsList = [("Uranus", "geocentric", "sidereal")]
        uniDirectionalAspectsFlag = True

        Ephemeris.setGeographicPosition(pcdd.birthInfo.longitudeDegrees,
                                        pcdd.birthInfo.latitudeDegrees,
                                        pcdd.birthInfo.elevation)
        
        for aspect in aspectGroup:
            degreeDifference = aspect

            # Get the timestamps of the aspect.
            timestamps = \
                EphemerisUtils.getLongitudeAspectTimestamps(\
                startDt, endDt,
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag)

            # Get the tag str for the aspect.
            tag = \
                PlanetaryCombinationsLibrary.getTagNameForLongitudeAspect(\
                planet1ParamsList,
                planet2ParamsList,
                degreeDifference,
                uniDirectionalAspectsFlag)

            # Get the color to apply.
            from astrologychart import AstrologyUtils
            color = AstrologyUtils.\
                    getForegroundColorForPlanetName(planet1ParamsList[0][0])

            # Draw the aspects.
            for dt in timestamps:
                PlanetaryCombinationsLibrary.addVerticalLine(\
                    pcdd, dt, highPrice, lowPrice, tag, color)

            log.info("Added {} artifacts for aspect {} degrees.".\
                      format(len(timestamps), degreeDifference))
        success = True

    ############################################################################

    if success == True:
        log.debug("Success!")
        rv = 0
    else:
        log.debug("Failure!")
        rv = 1

    return rv

##############################################################################
