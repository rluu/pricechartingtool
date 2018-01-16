
# For obtaining current directory path information, and creating directories
import os
import sys

# For logging.
import logging
import logging.handlers
import logging.config

# For loading shelves.
import shelve

# To initialize the ephemeris calculations caches
# with previously computed results.
from ephemeris import Ephemeris
from lunar_calendar_utils import LunarCalendarUtils

##############################################################################

class Cache:
    """Contains two methods which are used to load and save the caches
    from and into the shelve.
    """

    # Logger object for this class.
    log = logging.getLogger("cache.Cache")

    # Location of the source directory, based on this main.py file.
    SRC_DIR = os.path.abspath(sys.path[0])
    
    # Location of the shelved cache files.
    SHELVED_CACHE_EPHEMERIS_FILE = \
            os.path.abspath(os.path.join(SRC_DIR,
                                        ".." + os.sep +
                                        "data" + os.sep +
                                        "cache" + os.sep +
                                        "cache.Ephemeris.shelve"))
    
    SHELVED_CACHE_LUNARCALENDARUTILS_FILE = \
            os.path.abspath(os.path.join(SRC_DIR,
                                        ".." + os.sep +
                                        "data" + os.sep +
                                        "cache" + os.sep +
                                        "cache.LunarCalendarUtils.shelve"))

    @staticmethod
    def loadCachesFromShelve():
        """
        Loads previously used caches that were shelved to a file,
        back into the caches.
    
        This is so we don't have to re-populate the caches all over again
        with calculations that should be the same from run to run.
        """
    
        ########################################

        shelveFilename = Cache.SHELVED_CACHE_EPHEMERIS_FILE
        
        if not os.path.isfile(shelveFilename):
            Cache.log.info("Shelve file '" + \
                     shelveFilename +
                     "' does not exist or it is not a file.  " +
                     "Will skip loading caches from this shelve.")
        else:
            # Shelve exists.  Open it.
            Cache.log.info("Shelve file '" + shelveFilename + \
                    "' exists.  Attempting to open ...")
            cacheDict = shelve.open(shelveFilename)
            Cache.log.info("Shelve file opened for loading.")
    
            # Retrieve a copy of each of the caches, and store them
            # for use in the application.
            
            key = "Ephemeris.getPlanetaryInfoCache"
            if key in cacheDict:
                Cache.log.debug("Found cache key: {}".format(key))
                cache = cacheDict[key]
                Cache.log.debug("Lookup complete.")
                Ephemeris.getPlanetaryInfoCache = cache
                Cache.log.info("Loaded cache '" + key + "' with currsize " +
                    "{} from shelve.".format(cache.currsize))
            else:
                Cache.log.info("Cache '" + key + "' not found in the shelve.")

            # Close the dictionary.
            cacheDict.close()
    
        ########################################

        shelveFilename = Cache.SHELVED_CACHE_LUNARCALENDARUTILS_FILE
        
        if not os.path.isfile(shelveFilename):
            Cache.log.info("Shelve file '" + \
                     shelveFilename +
                     "' does not exist or it is not a file.  " +
                     "Will skip loading caches from this shelve.")
        else:
            # Shelve exists.  Open it.
            Cache.log.info("Shelve file '" + shelveFilename + \
                    "' exists.  Attempting to open ...")
            cacheDict = shelve.open(shelveFilename)
            Cache.log.info("Shelve file opened for loading.")

            # Retrieve a copy of each of the caches, and store them
            # for use in the application.
            
            key = "LunarCalendarUtils.datetimeToLunarDateCache"
            if key in cacheDict:
                Cache.log.debug("Found cache key: {}".format(key))
                cache = cacheDict[key]
                Cache.log.debug("Lookup complete.")
                LunarCalendarUtils.datetimeToLunarDateCache = cache
                Cache.log.info("Loaded cache '" + key + "' with currsize " +
                    "{} from shelve.".format(cache.currsize))
            else:
                Cache.log.info("Cache '" + key + "' not found in the shelve.")
    
            key = "LunarCalendarUtils.getNisan1DatetimeForYearCache"
            if key in cacheDict:
                Cache.log.debug("Found cache key: {}".format(key))
                cache = cacheDict[key]
                Cache.log.debug("Lookup complete.")
                LunarCalendarUtils.getNisan1DatetimeForYearCache = cache
                Cache.log.info("Loaded cache '" + key + "' with currsize " +
                    "{} from shelve.".format(cache.currsize))
            else:
                Cache.log.info("Cache '" + key + "' not found in the shelve.")
    
            key = "LunarCalendarUtils.lunarDateToDatetimeCache"
            if key in cacheDict:
                Cache.log.debug("Found cache key: {}".format(key))
                cache = cacheDict[key]
                Cache.log.debug("Lookup complete.")
                LunarCalendarUtils.lunarDateToDatetimeCache = cache
                Cache.log.info("Loaded cache '" + key + "' with currsize " +
                    "{} from shelve.".format(cache.currsize))
            else:
                Cache.log.info("Cache '" + key + "' not found in the shelve.")
    
            key = "LunarCalendarUtils.isLunarLeapYearCache"
            if key in cacheDict:
                Cache.log.debug("Found cache key: {}".format(key))
                cache = cacheDict[key]
                Cache.log.debug("Lookup complete.")
                LunarCalendarUtils.isLunarLeapYearCache = cache
                Cache.log.info("Loaded cache '" + key + "' with currsize " +
                    "{} from shelve.".format(cache.currsize))
            else:
                Cache.log.info("Cache '" + key + "' not found in the shelve.")
    
            # Close the dictionary.
            cacheDict.close()
    
    
    @staticmethod
    def saveCachesToShelve():
        """
        Store each of the caches we want to persist into the shelve for use
        the next time we open the application.
        """
    
        ########################################

        shelveFilename = Cache.SHELVED_CACHE_EPHEMERIS_FILE
        
        Cache.log.info("Attempting to open shelve file for saving: '" + \
                shelveFilename + "' ...")
        cacheDict = shelve.open(shelveFilename)
        Cache.log.info("Shelve file opened for saving.")

        key = "Ephemeris.getPlanetaryInfoCache"
        cache = Ephemeris.getPlanetaryInfoCache
        Cache.log.info("Saving cache '" + key + "' with currsize " +
                  "{} to shelve ...".format(cache.currsize))
        cacheDict[key] = cache
        
        Cache.log.info("Closing shelve ...")
        cacheDict.close()
        Cache.log.info("Shelve closed.")

        ########################################

        shelveFilename = Cache.SHELVED_CACHE_LUNARCALENDARUTILS_FILE
        
        Cache.log.info("Attempting to open shelve file for saving: '" + \
                shelveFilename + "' ...")
        cacheDict = shelve.open(shelveFilename)
        Cache.log.info("Shelve file opened for saving.")

        key = "LunarCalendarUtils.datetimeToLunarDateCache"
        cache = LunarCalendarUtils.datetimeToLunarDateCache
        Cache.log.info("Saving cache '" + key + "' with currsize " +
                  "{} to shelve ...".format(cache.currsize))
        cacheDict[key] = cache
    
        key = "LunarCalendarUtils.getNisan1DatetimeForYearCache"
        cache = LunarCalendarUtils.getNisan1DatetimeForYearCache
        Cache.log.info("Saving cache '" + key + "' with currsize " +
                  "{} to shelve ...".format(cache.currsize))
        cacheDict[key] = cache
    
        key = "LunarCalendarUtils.lunarDateToDatetimeCache"
        cache = LunarCalendarUtils.lunarDateToDatetimeCache
        Cache.log.info("Saving cache '" + key + "' with currsize " +
                  "{} to shelve ...".format(cache.currsize))
        cacheDict[key] = cache
    
        key = "LunarCalendarUtils.isLunarLeapYearCache"
        cache = LunarCalendarUtils.isLunarLeapYearCache
        Cache.log.info("Saving cache '" + key + "' with currsize " +
                  "{} to shelve ...".format(cache.currsize))
        cacheDict[key] = cache

        Cache.log.info("Closing shelve ...")
        cacheDict.close()
        Cache.log.info("Shelve closed.")

