#!/usr/bin/env python3
##############################################################################

import datetime
import pytz

##############################################################################

#timezone = pytz.timezone("US/Eastern")
eastern = pytz.timezone("US/Eastern")


# RG first arrival in NYC.
rgFirstArrivalNYC = datetime.datetime(year=1927, month=6, day=12,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# Lindbergh triumphant march up Broadway.
rgFirstArrivalNYC = datetime.datetime(year=1927, month=6, day=13,
                                      hour=12, minute=0,
                                      tzinfo=eastern)


# 69 Wall Street
wallStreet69 = datetime.datetime(year=1927, month=7, day=16,
                                 hour=12, minute=0,
                                 tzinfo=eastern)

# 1928 Presidential Election Forecast.
presForecast = datetime.datetime(year=1927, month=7, day=20,
                                 hour=12, minute=0,
                                 tzinfo=eastern)



# Los Angeles battle: "In the middle of May" [pg. 279].
# LA surrendered on June 14.
losAngeles = datetime.datetime(year=1930, month=5, day=14,
                               hour=12, minute=0,
                               tzinfo=eastern)

