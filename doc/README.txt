##############################################################################
# PriceChartingTool
##############################################################################

Author:  Ryan Luu
Email:   ryanluu@gmail.com


Google code project creation:

         2010-05-30 01:26:51 -0400 (Sun, 30 May 2010)

Google code Subversion repository initial import:   

         2010-05-30 01:49:38 -0400 (Sun, 30 May 2010)

Codesion Subversion repository initial import: 

         2010-06-16 01:40:06 -0400 (Wed, 16 Jun 2010)

Location of creation and initial imports: Chantilly, VA

##############################################################################

Description:

This is a Python PyQt project that is used to assist in learning
and research about the price movements of Futures, Currencies and Stocks.

##############################################################################

Requirements:

Dependencies to build/run this project are:

  - Python 3.1
  - PyQt 4.7.5
  - Qt 4.6.3
  - pyswisseph 1.76
      (Uses Swiss Ephemeris version 1.76.00, which was released Aug. 4, 2009)
  - pytz 2010h 
      (Modified version of this release that is compatible with Python 3)

##############################################################################

Steps to run the software:


1) Go to the project directory.

    [rluu@localhost pricechartingtool]$ pwd
    /home/rluu/programming/pricechartingtool

2) Go to the resources subdirectory.

    [rluu@localhost pricechartingtool]$ cd resources/

3) (Re-)generate the resource source file.

    [rluu@localhost resources]$ ./generateResourceSourceFile.sh
    pyrcc4 -py3 -o ./../src/resources.py ./resources.qrc

4) Change directory to the src directory.

    [rluu@localhost resources]$ cd ../src/

5) Run the executable.

    [rluu@localhost src]$ ./main.py

##############################################################################

Directory contents:

pricechartingtool
  |
  |- data: Holds emphemeris data to be used with the Swiss Ephemeris.
  |
  |- doc:  Holds some documentation.
  |
  |- resources:  Holds image files that are processed into a resource .py file.
  |              See file resources/images/source.txt for more details on the
  |              images used.
  |
  |- src:  Holds the Python source code.
  |
  |- tps:  Holds third party software packages.

##############################################################################

Notes to the user of this application:

I have tried to be as accurate as possible in my calculations and usage of
time, but my choice of programming language and libraries used invariably
brings in minor inaccuracies.  Those inaccuracies are noted here so that the
user is aware of them.

Python:
The Python 3.1.2 datetime module, when dealing with timezones, does not allow
tzinfo.utcoffset() to be a a floating point number (You will get the exception:
'ValueError: tzinfo.utcoffset() must return a whole number of minutes') 

Non-whole number of minutes are required to account for leap seconds
added to UTC.  Timezones are based off of an offset from UTC, which started on
January 1, 1972.  UTC has these leap seconds added so that it is not more than
1 second off from UT1 time.  Because of this problem inherent in the built-in
Python datetime module, the pytz timezone library returns a value for
tzinnfo.utcoffset() that is rounded.

Some background information on UTC, timezones, and leap seconds can be found
at the following wikipedia links:
http://en.wikipedia.org/wiki/Coordinated_Universal_Time
http://en.wikipedia.org/wiki/UT1
http://en.wikipedia.org/wiki/Greenwich_Mean_Time
http://en.wikipedia.org/wiki/Time_zone
http://en.wikipedia.org/wiki/Leap_second


Swiss Ephemeris and pyswisseph:
The Swiss Ephemeris utilizes times based off of UTC, Julian Day in UT (UT1),
and Julian Day in ET (TT)

See function definition and prototype for:
void swe_utc_to_jd()
void swe_jdet_to_utc()
void swe_jdut1_to_utc()

Swiss Ephemeris DOES account for leap seconds, but it is not able to know ahead
of time when those will be inserted into UTC beforehand.  They provide a way
for us to account for that.  From the documentation:

The insertion of leap seconds is not known in advance. We will update the Swiss
Ephemeris whenever the IERS announces that a leap second will be inserted.
However, if the user does not want to wait for our update or does not want to
download a new version of the Swiss Ephemeris, he can create a file
swe_leapsec.txt in the ephemeris directory. Insert a line with the date on
which a leap second has to be inserted. The file looks as follows:
# This file contains the dates of leap seconds to be taken into account
#
# # by the Swiss Ephemeris.
#
# # For each new leap second add the date of its insertion in the format
#
# # yyyymmdd, e.g. "20081231" for 21 december 2008
#
20081231


Julian Day Precision:
The Python 3 datetime.datetime object allows specification of time resolution
down to the microsecond.  This is good enough for our purposes, but it should
be noted that Julian Days returned by pyswisseph have limited 
precision (e.g., julian day returned of 2455357.66596).  Because one second of
time is represented by a Julian Day of approximately 0.000011574074074074073,
there will be some imprecision in the conversions between UTC and Julian Day. 



Swiss Ephemeris Sidereal Calculation:
Currently this application uses the Lahiri Ayanamsa for the value for 
the precession of the equinoxes.  As noted by P.V.R Narasimha Rao, the 
Lahiri Ayanamsa has some inconsistencies/inaccuracies.  

There are other ayanamsas or sidereal longitude settings which may be
valuable to explore:

(1) True Chitrapaksha ayanamsa: This fixes Chitra star at 180 deg always. With
regular Lahiri ayanamsa, Chitra star wobbles around 180 deg.

(2) Jagannatha ayanamsa (thanks to Pt Sanjay Rath for suggesting this name):
This fixes Chitra star at 180 deg always and also fixes the two-dimensional
plane on which planetary positions are projected to Vishnunabhi plane (solar
system rotation plane). In regular Lahiri, Chitra wobbles around 180 deg and
the two-dimensional plane of planetary longitudes wobbles around the
Vishnunabhi plane.

(3) Surya Siddhanta calculations.  These calculations for the planet
locations differ from the actual formulas and observations from the Swiss
Ephemeris.  It is said that Surya Siddhanta takes into account the subtle
(energy) bodies of the planets, which at any point may be ahead or behind
the actual physical body of the planet.

I do not yet have the calculations and formulas for these ayanamsas so it is
not currently implemented in this application.



##############################################################################

