#!/usr/bin/env python3
##############################################################################

import datetime
import pytz

##############################################################################

#timezone = pytz.timezone("US/Eastern")
eastern = pytz.timezone("US/Eastern")
central = pytz.timezone("US/Central")

##############################################################################


geoVenusRetrograde19270820 = datetime.datetime(year=1927, month=8, day=20,
                                           hour=6, minute=39,
                                           tzinfo=eastern)

geoVenusDirect19271001 = datetime.datetime(year=1927, month=10, day=1,
                                           hour=21, minute=47,
                                           tzinfo=eastern)

