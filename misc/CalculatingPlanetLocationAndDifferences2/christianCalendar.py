#!/usr/bin/env python3
##############################################################################

import datetime
import pytz

##############################################################################

#timezone = pytz.timezone("US/Eastern")
eastern = pytz.timezone("US/Eastern")
central = pytz.timezone("US/Central")

##############################################################################


nativityOfTheotokos = datetime.datetime(year=1926, month=9, day=8,
                                           hour=12, minute=0,
                                           tzinfo=eastern)

elevationOfHolyCross = datetime.datetime(year=1926, month=9, day=14,
                                           hour=12, minute=0,
                                           tzinfo=eastern)

