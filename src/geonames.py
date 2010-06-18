#!/usr/bin/env python3

# For opening the logging config file.
import os
import sys

# For formatting URLs.
import urllib
import urllib.request
import urllib.parse

# For parsing the XML returned from the GeoNames web service.
import xml.etree.ElementTree as ElementTree

# For logging.
import logging
import logging.config



class GeoNames:
    """This class provides access to the GeoNames geographical database.
    This database provides information on the geographical attributes of
    various cities around the world.  
    """

    # Base URL used for web service queries.
    GEONAMES_BASEURL = "http://ws.geonames.org/"

    # String ISO-636 2-letter language code (e.g., en,de,fr,it,es).
    # Default is "en" (English).
    LANGUAGE_DEFAULT = "en"

    # Country bias for search results.
    # Default is "US" (United States of America).
    COUNTRY_BIAS_DEFAULT = "US"

    # Logger object for this class.
    log = logging.getLogger("geonames.GeoNames")


    def canConnectToWebService():
        """Returns true if we are able to make a connection to the 
        web service.  Returns false otherwise.
        This is useful for testing for an internet connection.
        """

        # Here we just do a HTTP Get on:
        # http://ws.geonames.org/search

        # There are no parameters specified so the results returned should be
        # empty.  E.g., we should see a response like the following:
        #
        # 
        # <geonames style="MEDIUM">
        #   <totalResultsCount>0</totalResultsCount>
        # </geonames>

        # Return value.
        retVal = False

        # Here we assemble the URL that will make up the query.
        url = GeoNames.GEONAMES_BASEURL + "search"

        GeoNames.log.debug("GeoNames.canConnectToWebService(): " + \
                           "request URL is: " + url)

        # Open the URL and read the returned results.
        urlOpener = urllib.request.build_opener()
        request = urllib.request.Request(url)

        GeoNames.log.debug("Opening HTTP request.")
        try:
            response = urlOpener.open(request)

            GeoNames.log.debug("Reading HTTP response.")
            data = response.read()

            # Parse the results.
            rootElement = ElementTree.XML(data)

            if rootElement.tag == "geonames":
                retVal = True
            else:
                GeoNames.log.warn("Got a non-expected XML element tag " +  \
                                  "at the root level: " + rootElement.tag)
                retVal = False

        except urllib.error.URLError as e:
            GeoNames.log.error("Couldn't open the URL due to the " + \
                               "following reason: " + e)
            retVal = False


        return retVal


    def search(placename="", searchStr="", country="", maxRows="100", 
               countryBias=COUNTRY_BIAS_DEFAULT, lang=LANGUAGE_DEFAULT, fuzzy="1"):
        """Does a query for locations matching various search parameters.
        It uses the 'search' function of the GeoNames web service.

        One of the following parameters to this function are required 
        to be specified:
        
              - placename
              - searchStr

        Parameters are:

        placename - String containing the place to search for.
                    If an empty string is specified, then the 'searchStr'
                    parameter needs to be non-empty.  
        searchStr - String containing a the place, country, continent or 
                    admin code to search for.  If an empty string is 
                    specified, then the 'placename' parameter needs to be 
                    non-empty.
        country   - String containing the country to filter results with.  
                    This is the country code in ISO-3166 (two-letter) format.
                    If this string is empty, all countries are searched.
        maxRows   - String containing a number for the maximum number of rows
                    to return.  Per the web service documentation, if this
                    is not specified, then 100 is the default.  Maximum
                    allowable value is 1000.
        countryBias - String holding the country code that search results 
                    will be biased towards.  Default is 'US'.
        lang      - String containing the language to return the results in.  
                    The string should be a ISO-636 2-letter language code.
        fuzzy     - String containing a floating point value between 0 and 1.
                    It defines the fuzzyness of the search terms.
                    Default here and for the web service is "1".


        Returns:    List of GeoInfo objects.

        Raises:     urllib.error.URLError if an internet connection 
                    could not be opened to the web service.


        Please see the following URL for details on the parameters 
        they take to the search web service function: 
        
              http://www.geonames.org/export/geonames-search.html

        """ 

        # Return value.
        geoInfos = []

        # Check input to make sure it's valid.

        # Check to make sure 'placename' or 'searchStr' is a non-empty string.
        if ((placename == None or placename == "") and \
            (searchStr == None or searchStr == "")):
            # Log the error.
            errStr = "GeoNames.search(): " + \
                "Argument 'placename' or 'searchStr' " + \
                "must be a non-empty string"
            GeoNames.log.error(errStr)

            # Return an empty list of GeoInfo.
            return geoInfos

        # Holds the value of maxRows as a integer.
        maxRowsInt = 1

        # Try to cast the 'maxRows' to a int.  It should work fine if
        # the string is a numeric string. 
        try:
            maxRowsInt = int(maxRows)

            # Make sure the value is between 0 and 1.
            if maxRowsInt < 1:
                # Log the error.
                errStr = "GeoNames.search(): " + \
                    "Argument 'maxRows' needs to greater than 0."
                GeoNames.log.error(errStr)
                raise ValueError(errStr)
        except ValueError:
            # Log the error.
            errStr = "Geonames.search(): " + \
                "Argument 'maxRows' is not a numeric string."
            GeoNames.log.error(errStr)
            raise ValueError(errStr)

        # Holds the value of fuzzy as a floating point value.
        fuzzyFloat = 0

        # Try to cast the string 'fuzzy' to a float.  It should work fine if
        # the string is a numeric string. 
        try:
            fuzzyFloat = float(fuzzy)

            # Make sure the value is between 0 and 1.
            if fuzzyFloat < 0.0 or fuzzyFloat > 1.0:
                # Log the error.
                errStr = "GeoNames.search(): " + \
                    "Argument 'fuzzy' needs to have a value between 0 and 1."
                GeoNames.log.error(errStr)
                raise ValueError(errStr)
        except ValueError:
            # Log the error.
            errStr = "Geonames.search(): " + \
                "Argument 'fuzzy' is not a numeric string."
            GeoNames.log.error(errStr)
            raise ValueError(errStr)


        # Here we assemble the URL that will make up the query.
        url = GeoNames.GEONAMES_BASEURL + "search?"

        # Append to the URL, the variables for the placename 
        # search string or the generic search string.
        # One of these should have been specified.
        if ((searchStr != None and searchStr != "") and \
            (placename != None and placename != "")):
            
            # Escape any characters that aren't valid in a URL. 
            searchStr = urllib.parse.quote(searchStr)
            placename = urllib.parse.quote(placename)

            url += "q={}".format(searchStr)
            url += "&name={}".format(placename)

        elif (searchStr != None and searchStr != ""):
            # Escape any characters that aren't valid in a URL. 
            searchStr = urllib.parse.quote(searchStr)

            url += "q={}".format(searchStr)
        
        elif (placename != None and placename != ""):
            # Escape any characters that aren't valid in a URL. 
            placename = urllib.parse.quote(placename)

            url += "name={}".format(placename)


        # Append maximum number of rows returned.
        url += "&maxRows={}".format(maxRowsInt)

        # Append the country.
        if country != None and country != "":
            # Escape any characters that aren't valid in a URL. 
            country = urllib.parse.quote(country.strip())

            url += "&country={}".format(country)

        # Append the country bias.
        if countryBias != None and countryBias != "":
            # Escape any characters that aren't valid in a URL. 
            countryBias = urllib.parse.quote(countryBias.strip())

            url += "&countryBias={}".format(countryBias)

        # Append the language default.
        lang = urllib.parse.quote(lang.strip())
        url += "&lang={}".format(lang)

        # Append the desired type of format returned.
        # Valid values are 'xml', 'json', 'rdf'.
        url += "&type={}".format("xml")

        # Append style.  This is the verbosity of the XML document returned.
        # Valid values are 'SHORT', 'MEDIUM', 'LONG', 'FULL'. 
        url += "&style={}".format("FULL")

        # Append charset.  This specifies the encoding used for the document
        # returned by the web service.
        url += "&charset={}".format("UTF8")

        # Append the desired fuzzy value.
        url += "&fuzzy={}".format(fuzzyFloat)

        
        # Okay, we've completed assembling the URL.
        GeoNames.log.debug("GeoNames.search(): request URL is: " + url)

        # Open the URL and read the returned results.
        urlOpener = urllib.request.build_opener()
        request = urllib.request.Request(url)

        GeoNames.log.debug("Opening HTTP request.")
        response = urlOpener.open(request)

        GeoNames.log.debug("Reading HTTP response.")
        data = response.read()

        # Parse the results and extract GeoInfo objects out of it.
        geoInfos = GeoNames._parseSearchResultXml(data)

        return geoInfos



    def _parseSearchResultXml(data):
        """Parses the search result XML in 'data' and returns the 
        results as a list of GeoInfo objects.
        """

        # Return value.
        geoInfos = []
        
        rootElement = ElementTree.XML(data)

        if rootElement.tag != "geonames":
            GeoNames.log.error("GeoNames.search(): " + \
                      "Got an unexpected XML root element tag '{}'".\
                      format(rootElement.tag))
            return geoInfos

        for child in rootElement.getchildren():
            if child.tag == "totalResultsCount":
                totalResultsCountStr = child.text
                GeoNames.log.debug("HTTP Response: Total results count is " + \
                          totalResultsCountStr)
            elif child.tag == "geoname":
                # This is an entry for a geoname result.

                # Create a GeoInfo object that will contain the info 
                # in this XML element.
                geoInfo = GeoInfo()

                # Iterate through the sub-elements that contain
                # information on the geoname returned.
                for e in child.getchildren():
                    if e.tag == "toponymName":
                        geoInfo.toponymName = e.text
                    elif e.tag == "name":
                        geoInfo.name = e.text
                    elif e.tag == "lat":
                        # Try to convert the string 'lat' to a latitude number.
                        lat = e.text
                        try:
                            geoInfo.latitude = float(lat)
                        except ValueError:
                            warnStr = "Couldn't parse latitude string " + \
                                      "'{}' to a float".format(lat)
                            GeoNames.log.warn(warnStr)
                            geoInfo.latitude = None
                    elif e.tag == "lng":
                        # Try to convert the string 'lng' to a longitude
                        # number.
                        lng = e.text
                        try:
                            geoInfo.longitude = float(lng)
                        except ValueError:
                            warnStr = "Couldn't parse longitude string " + \
                                      "'{}' to a float".format(lng)
                            GeoNames.log.warn(warnStr)
                            geoInfo.longitude = None
                    elif e.tag == "geonameId":
                        # Try to convert the string 'geonameId' to number.
                        geonameId = e.text
                        try:
                            geoInfo.geonameId = int(geonameId)
                        except ValueError:
                            warnStr = "Couldn't parse geonameId string " + \
                                      "'{}' to an int".format(geonameId)
                            GeoNames.log.warn(warnStr)
                            geoInfo.geonameId = None
                    elif e.tag == "countryCode":
                        geoInfo.countryCode = e.text
                    elif e.tag == "countryName":
                        geoInfo.countryName = e.text
                    elif e.tag == "fcl":
                        geoInfo.fcl = e.text
                    elif e.tag == "fclName":
                        geoInfo.fclName = e.text
                    elif e.tag == "fcode":
                        geoInfo.fcode = e.text
                    elif e.tag == "fcodeName":
                        geoInfo.fcodeName = e.text
                    elif e.tag == "population":
                        geoInfo.population = e.text
                        # Try to convert the string 'population' to number.
                        population = e.text
                        try:
                            if population != None:
                                geoInfo.population = int(population)
                            else:
                                geoInfo.population = 0
                        except ValueError:
                            warnStr = "Couldn't parse population string " + \
                                      "'{}' to an int".format(population)
                            GeoNames.log.warn(warnStr)
                            geoInfo.population = 0
                    elif e.tag == "alternateNames":
                        ignoreStr = e.text
                    elif e.tag == "elevation":
                        elevationStr = e.text
                        # Try to convert the string 'elevationStr' to number.
                        try:
                            if elevationStr != None:
                                geoInfo.elevation = float(elevationStr)
                            else:
                                geoInfo.elevation = None
                        except ValueError:
                            warnStr = "Couldn't parse elevation string " + \
                                    "'{}' to float".format(elevationStr)
                            GeoNames.log.warn(warnStr)
                            geoInfo.elevation = None
                    elif e.tag == "continentCode":
                        geoInfo.continentCode = e.text
                    elif e.tag == "adminCode1":
                        geoInfo.adminCode1 = e.text
                    elif e.tag == "adminName1":
                        geoInfo.adminName1 = e.text
                    elif e.tag == "adminCode2":
                        geoInfo.adminCode2 = e.text
                    elif e.tag == "adminName2":
                        geoInfo.adminName2 = e.text
                    elif e.tag == "alternateName":
                        ignoreStr = e.text
                    elif e.tag == "timezone":
                        geoInfo.timezone = e.text
                    elif e.tag == "score":
                        ignoreStr = e.text
                    else:
                        debugStr = \
                            "FYI: Found an unknown element tag under 'geoname':" + \
                            " {}".format(e.text)
                        GeoNames.log.debug(debugStr)
                GeoNames.log.debug("Adding GeoInfo: {}".format(geoInfo))
                geoInfos.append(geoInfo)
            else:
                debugStr = "FYI: Found an unknown element tag under 'geonames':" + \
                    " {}".format(e.text)
                GeoNames.log.debug(debugStr)

        # Return the list of GeoInfo objects parsed from the XML.
        return geoInfos


    def getTimezone(latitude, longitude, radius=None):
        """Returns a string representing the timezone.  
        The returned string is in the format such that it can be 
        looked up in the Olson database (e.g., 'US/Eastern').

        Arguments:
        latitude  - Float value containing the latitude location in degrees.
        longitude - Float value containing the longitude location in degrees.
        radius    - Float value containing the buffer in kilometers for 
                    closest country in coastal areas.  Specifying the 
                    radius parameter is optional.

        Returns:  
        String representing the timezone, for lookup in the Olson database.
        If an error occurred in obtaining the timezone, an empty string is
        returned and the error is logged.

        Raises:     urllib.error.URLError if an internet connection 
                    could not be opened to the web service.
        """

        # Return value.
        retVal = ""

        # Check the input arguments.

        # Latitude must be a float or an int.
        if ((latitude == None) or \
            (type(latitude) != float and type(latitude) != int)):

            errStr = "getTimezone(): Argument 'latitude' must be a float."
            GeoNames.log.error(errStr)
            raise ValueError(errStr)

        # Longitude must be a float or an int.
        if ((longitude == None) or \
            (type(longitude) != float and type(longitude) != int)):

            errStr = "getTimezone(): Argument 'longitude' must be a float."
            GeoNames.log.error(errStr)
            raise ValueError(errStr)

        # Radius is optional, but if it is specified, it has to be a float or
        # an int, and it has to be non-negative.
        if ((radius != None) and \
            ((type(radius) != float and type(radius) != int) or
             (radius < 0.0))):

            errStr = "getTimezone(): " + \
                     "Argument 'radius' must be a non-negative number."
            GeoNames.log.error(errStr)
            raise ValueError(errStr)

        
        # Here we assemble the URL that will make up the query.
        url = GeoNames.GEONAMES_BASEURL + "timezone?"

        # Append to the URL, the variables to the query.
        url += "lat={}".format(latitude)
        url += "&lng={}".format(longitude)
        if radius != None:
            url += "&radius={}".format(radius)


        # Okay, we've completed assembling the URL.
        GeoNames.log.debug("getTimezone(): request URL is: " + url)

        # Open the URL and read the returned results.
        urlOpener = urllib.request.build_opener()
        request = urllib.request.Request(url)

        GeoNames.log.debug("getTimezone(): Opening HTTP request.")
        response = urlOpener.open(request)

        GeoNames.log.debug("getTimezone(): Reading HTTP response.")
        data = response.read()


        # Extract data from the XML.
        rootElement = ElementTree.XML(data)

        if rootElement.tag != "geonames":
            GeoNames.log.error("getTimezone(): " + \
                               "Got an unexpected XML root element tag '{}'".\
                               format(rootElement.tag))
            # Return an empty retVal string.
            retVal = ""
        else:
            for child in rootElement.getchildren():
                if child.tag == "timezone":
                    for e in child.getchildren():
                        if e.tag == "timezoneId":
                            # Found the timezone info we were looking for.
                            # Save it off and break out of the for loops.
                            retVal = e.text
                            break

                # If we have a non-empty return value, then we found out
                # timezone information and can break out of the loops.
                if retVal != "":
                    break

        GeoNames.log.debug("getTimezone(): returning '{}'".format(retVal))
        return retVal
        

    def getElevation(latitude, longitude, source=""):
        """Returns a float representing the elevation of a location in meters.
        This method can utilize one of three sources for the data returned.
        If the location is an ocean or there is no data, an elevation of
        -9999.0 is returned.

        Arguments:
        latitude  - Float value containing the latitude location in degrees.
        longitude - Float value containing the longitude location in degrees.
        source    - String value equaling one of:

                      - ""           - Default, use the best likely source.
                      - "srtm3"      - Use SRTM3
                      - "astergdem"  - Use AsterGDEM
                      - "gtopo30"    - Use GTOPO30

            If the 'source' argument is an empty string, the following
            algorithm is used to determine which elevation source to use:

              - If the latitude is between 60N and 56S, then the 
                SRTM3 data is used.

              - If the latitude is outside 60N and 56S but between 
                83N and 65S, then the Aster Global Digital Elevation Model 
                is used.

              - For all other latitudes, the GTOPO30 model is used.

        Returns:  
        Float value for the elevation in meters.  If the location is 
        an ocean or there is no data, then a value of -9999 is returned.

        Raises:     urllib.error.URLError if an internet connection 
                    could not be opened to the web service.

        Detailed info on the sources for this elevation data:

          - SRTM3

              Source website: 

                http://www2.jpl.nasa.gov/srtm/

              Info from http://www.geonames.org/export/web-services.html

                Shuttle Radar Topography Mission (SRTM) elevation data. SRTM
                consisted of a specially modified radar system that flew
                onboard the Space Shuttle Endeavour during an 11-day mission in
                February of 2000. The dataset covers land areas between 60
                degrees north and 56 degrees south.

                This web service is using SRTM3 data with data points located
                every 3-arc-second (approximately 90 meters) on a
                latitude/longitude grid.  Documentation : Nasa

                Webservice Type : REST
                Url : ws.geonames.org/srtm3?
                Parameters : lat,lng;

                sample area: ca 90m x 90m Result : a single number giving the
                elevation in meters according to srtm3, ocean areas have been
                masked as "no data" and have been assigned a value of -32768

                Example http://ws.geonames.org/srtm3?lat=50.01&lng=10.2

                This service is also available in XML and JSON format:
                ws.geonames.org/srtm3XML?lat=50.01&lng=10.2
                ws.geonames.org/srtm3JSON?lat=50.01&lng=10.2 

          - Aster Global Digital Elevation Model

              Source website: 

                http://asterweb.jpl.nasa.gov/gdem.asp

              Info from http://www.geonames.org/export/web-services.html
              
                Webservice Type : REST
                Url : ws.geonames.org/astergdem?
                Parameters : lat,lng;

                sample are: ca 30m x 30m, between 83N and 65S latitude. 
                Result : a single number giving the elevation in meters
                according to aster gdem, ocean areas have been masked as "no
                data" and have been assigned a value of -9999

                Example http://ws.geonames.org/astergdem?lat=50.01&lng=10.2

                This service is also available in XML and JSON format :
                ws.geonames.org/astergdemXML?lat=50.01&lng=10.2 and
                ws.geonames.org/astergdemJSON?lat=50.01&lng=10.2 


          - GTOPO30

              Source website: 

                http://eros.usgs.gov/#/Find_Data/Products_and_Data_Available/GTOPO30
                http://www1.gsi.go.jp/geowww/globalmap-gsi/gtopo30/README.html

              Info from http://www.geonames.org/export/web-services.html

                GTOPO30 is a global digital elevation model (DEM) with a
                horizontal grid spacing of 30 arc seconds (approximately 1
                kilometer). GTOPO30 was derived from several raster and vector
                sources of topographic information. 

                Webservice Type : REST
                Url : ws.geonames.org/gtopo30?
                Parameters : lat,lng;

                sample area: ca 1km x 1km Result : a single number giving the
                elevation in meters according to gtopo30, ocean areas have 
                been masked as "no data" and have been assigned a value 
                of -9999

                Example http://ws.geonames.org/gtopo30?lat=47.01&lng=10.2

                This service is also available in JSON format : 
                http://ws.geonames.org/gtopo30JSON?lat=47.01&lng=10.2 
        """

        # Return value.  Default to no data.
        retVal = -9999.0

        # Check the input arguments.

        # Latitude must be a float or an int.
        if ((latitude == None) or \
            (type(latitude) != float and type(latitude) != int)):

            errStr = "getElevation(): Argument 'latitude' must be a float."
            GeoNames.log.error(errStr)
            raise ValueError(errStr)

        # Longitude must be a float or an int.
        if ((longitude == None) or \
            (type(longitude) != float and type(longitude) != int)):

            errStr = "getElevation(): Argument 'longitude' must be a float."
            GeoNames.log.error(errStr)
            raise ValueError(errStr)

        # Source string must be one of the valid options.
        if (source != "" and \
            source != "srtm3" and \
            source != "astergdem" and \
            source != "gtopo30"):

            errStr = "getElevation(): Argument 'source' is invalid: {}"
            GeoNames.log.error(errStr.format(source))
            raise ValueError(errStr)



        # Initialize the URL to use as the base URL.
        url = GeoNames.GEONAMES_BASEURL

        if source == "":
            # See where the latitude is, if it is within the range for us to
            # use the higher resolution model(s).
            if (latitude > -56.0 and latitude < 60.0):
                # Use the SRTM3 elevation data.
                GeoNames.log.debug("getElevation(): " + \
                                   "Using SRTM3 elevation data.")
                url += "srtm3?"
            elif (latitude > -65.0 and latitude < 83.0):
                # Use the Aster Global Digital Elevation Model data.
                debugStr = "getElevation(): " + \
                           "Using Aster Global Digital Elevation Model data."
                GeoNames.log.debug(debugStr)
                url += "astergdem?"
            else:
                # Use the GTOPO30 model data.
                GeoNames.log.debug("getElevation(): Using GTOPO30 model data.")
                url += "gtopo30?"
        elif source == "srtm3":
            # Use the SRTM3 elevation data.
            GeoNames.log.debug("getElevation(): Using SRTM3 elevation data.")
            url += "srtm3?"
        elif source == "astergdem":
            # Use the Aster Global Digital Elevation Model data.
            debugStr = "getElevation(): " + \
                       "Using Aster Global Digital Elevation Model data."
            GeoNames.log.debug(debugStr)
            url += "astergdem?"
        elif source == "gtopo30":
            # Use the GTOPO30 model data.
            GeoNames.log.debug("getElevation(): Using GTOPO30 model data.")
            url += "gtopo30?"
        else:
            # Invalid source.
            errStr = "getElevation(): Argument 'source' is invalid: {}"
            GeoNames.log.error(errStr.format(source))
            raise ValueError(errStr)


        # Append to the URL, the variables to the query.
        url += "lat={}".format(latitude)
        url += "&lng={}".format(longitude)

        # Okay, we've completed assembling the URL.
        GeoNames.log.debug("getElevation(): request URL is: " + url)

        # Open the URL and read the returned results.
        urlOpener = urllib.request.build_opener()
        request = urllib.request.Request(url)

        GeoNames.log.debug("getElevation(): Opening HTTP request.")
        response = urlOpener.open(request)

        GeoNames.log.debug("getElevation(): Reading HTTP response.")
        data = response.read()

        GeoNames.log.debug("getElevation(): Data from the response is: {}".\
                         format(data))

        # Decode to a string. 
        dataString = data.decode('utf-8').strip()
        GeoNames.log.debug("getElevation(): Data stripped as a str is: {}".\
                         format(dataString))

        dataInt = int(dataString)
        dataFloat = float(dataString)
        GeoNames.log.debug("getElevation(): Data as an int " + \
                         "({}) and as a float ({})".\
                         format(dataInt, dataFloat))

        # Check to see if it is one of the elevations that would be
        # returned if it was an ocean or no data.
        if dataInt == -9999 or dataInt == -32768:
            retVal = -9999.0
        else:
            retVal = dataFloat

        debugStr = \
                "getElevation(): returning: " + \
                "{} meters for location(lat={}, lon={})"
        GeoNames.log.debug(debugStr.format(retVal, latitude, longitude))
        return retVal



class GeoInfo:
    """Class GeoInfo holds geographical information about a certain place."""

    def __init__(self, 
                 name="", 
                 toponymName="", 
                 latitude=None, 
                 longitude=None, 
                 geonameId=None, 
                 countryCode="",
                 countryName="",
                 fcl="",
                 fclName="",
                 fcode="",
                 fcodeName="",
                 population=0,
                 elevation=None,
                 continentCode="",
                 adminCode1="",
                 adminName1="",
                 adminCode2="",
                 adminName2="",
                 timezone=""):
        """Initializes the GeoInfo object with the arguments provided.

        Arguments:

        name        - String containing the localized name, the preferred name
                      in the language passed in the optional 'lang' parameter
                      or the name that triggered the response in a 'startWith'
                      search.
        toponymName - String containing the main name of the toponym as
                      displayed on the google maps interface page or in the
                      geoname file in the download.
        latitude    - Float value for the latitude location.
        longitude   - Float value for the longitude location.
        geonameId   - Integer value for the ID in GeoNames database.
        countryCode - String containing country code in ISO-3166 (two-letter)
                      format.
        countryName - String containing the country for this GeoInfo place.
        fcl         - String containing the feature class (code character).
        fclName     - String containing the name of the feature class.
        fcode       - String containing the feature code.
        fcodeName   - String containing the name of the feature code.
        population  - Integer containing the population of the GeoInfo place.
        elevation   - Float value for the elevation in meters.
        continentCode - String holding the code for the Continent of the place.
        adminCode1  - String holding the admin code for this location.
                      In the United States this is "VA" for Virginia.
        adminName1  - String holding the admin name for this location.
                      In the United States this is the state (e.g., "Virginia")
        adminCode2  - String holding the second admin code for this location.
                      In the United States this is the County number code.
        adminName2  - String holding the second admin name for this location.
                      In the United States this is the County 
                      (e.g., "Arlington County")
        timezone    - Timezone string for a lookup in the Olson database.
        """

        self.name = name
        self.toponymName = toponymName
        self.latitude = latitude
        self.longitude = longitude
        self.geonameId = geonameId
        self.countryCode = countryCode
        self.countryName = countryName
        self.fcl = fcl
        self.fclName = fclName
        self.fcode = fcode
        self.fcodeName = fcodeName
        self.population = population
        self.elevation = elevation
        self.continentCode = continentCode
        self.adminCode1 = adminCode1
        self.adminName1 = adminName1
        self.adminCode2 = adminCode2
        self.adminName2 = adminName2
        self.timezone = timezone

    def latitudeBreakdown(self):
        """Returns a tuple of (degrees, minutes, seconds, string) for the latitude
        in this GeoInfo object.  

        degrees, minutes, and seconds are int values, and string is 'N' or 'S'.
        """

        string = ""
        if self.latitude >= 0:
            string = "N"
        else:
            string = "S"

        degrees = int(abs(self.latitude))
        minutesFloat = (abs(self.latitude) - float(degrees)) / 60.0
        minutes = int(minutesFloat)
        secondsFloat = (minutesFloat - float(minutes)) / 60.0
        seconds = round(secondsFloat)

        return (degrees, minutes, seconds, string)


    def longitudeBreakdown(self):
        """Returns a tuple of (degrees, minutes, seconds, string) for the longitude
        in this GeoInfo object.  

        degrees, minutes, and seconds are int values, and string is 'E' or 'W'.
        """

        string = ""
        if self.longitude < 0:
            string = 'W'
        else:
            string = 'E'

        degrees = int(abs(self.longitude))
        minutesFloat = (abs(self.latitude) - float(degrees)) / 60.0
        minutes = int(minutesFloat)
        secondsFloat = (minutesFloat - float(minutes)) / 60.0
        seconds = round(secondsFloat)
        
        return (degrees, minutes, seconds, string)


    def latitudeStr(self):
        """Returns a string of the latitude in the form: 28° 14' 23" N
        """

        (degrees, minutes, seconds, string) = self.latitudeBreakdown()
        retVal = "{}\xb0 {}' {}\" {}".format(degrees, minutes, seconds, string)
        return retVal

    def longitudeStr(self):
        """Returns a string of the longitude in the form: 28° 14' 23" E
        """

        (degrees, minutes, seconds, string) = self.longitudeBreakdown()
        retVal = "{}\xb0 {}' {}\" {}".format(degrees, minutes, seconds, string)
        return retVal



    def __str__(self):
        """Returns the string representation of this class."""

        return self.toString()

    def toString(self):
        """Returns the string representation of this class."""

        rv = "[name={}, ".format(self.name) + \
             "toponymName={}, ".format(self.toponymName) + \
             "latitude={}, ".format(self.latitude) + \
             "longitude={}, ".format(self.longitude) + \
             "geonameId={}, ".format(self.geonameId) + \
             "countryCode={}, ".format(self.countryCode) + \
             "countryName={}, ".format(self.countryName) + \
             "fcl={}, ".format(self.fcl) + \
             "fclName={}, ".format(self.fclName) + \
             "fcode={}, ".format(self.fcode) + \
             "fcodeName={}, ".format(self.fcodeName) + \
             "population={}, ".format(self.population) + \
             "elevation={}, ".format(self.elevation) + \
             "continentCode={}, ".format(self.continentCode) + \
             "adminCode1={}, ".format(self.adminCode1) + \
             "adminName1={}, ".format(self.adminName1) + \
             "adminCode2={}, ".format(self.adminCode2) + \
             "adminName2={}, ".format(self.adminName2) + \
             "timezone={}]".format(self.timezone)

        return rv



# For debugging the classes during development.  
if __name__=="__main__":
    # Exercising the GeoNames classes.
    print("------------------------")

    # Initialize Logging (required).
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    print("Attempting to test connection...")

    canConnect = GeoNames.canConnectToWebService()

    print("canConnect is {}".format(canConnect))

    print("------------------------")

    if canConnect:
        #print("Doing a search for Arlington in the United States")
        #geoInfos = GeoNames.search(placename="Arlington", 
        #                           country="US", 
        #                           maxRows=10)

        #print("Doing a search for Seattle in the United States")
        #geoInfos = GeoNames.search(placename="Seattle", 
        #                           country="US", 
        #                           maxRows=10)

        print("Doing a search for Anchorage in the United States")
        geoInfos = GeoNames.search(placename="Anchorage", 
                                   country="US", 
                                   maxRows=10)

        print("------------------------")
        print("Got {} results back.".format(len(geoInfos)))
        print("------------------------")

        for i in range(len(geoInfos)):
            print("geoInfos[{}]: {}".format(i, geoInfos[i]))
            print("Timezone for geoInfos[{}] is: {}".\
                  format(i, \
                         GeoNames.getTimezone(geoInfos[i].latitude,  \
                                              geoInfos[i].longitude)))
            print("Elevation for geoInfos[{}] is: {}".\
                  format(i, \
                         GeoNames.getElevation(geoInfos[i].latitude,  \
                                               geoInfos[i].longitude)))
            print("======================================================")

    else:
        print("Couldn't connect.")

    print("------------------------")

    # Shutdown logging so all the file handles get flushed and 
    # cleanup can happen.
    logging.shutdown()

    print("Exiting.")
     


