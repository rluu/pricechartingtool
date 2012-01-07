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
  - Qt 4.7.4
  - PyQt 4.8.5
  - pyswisseph 1.76
      (Uses Swiss Ephemeris version 1.76.00, which was released Aug. 4, 2009)
  - pytz 2010h 
      (Modified version of this release that is compatible with Python 3)

##############################################################################

Notes for building on the Linux platform: 

  If compiling Qt from source on Linux, make sure to include the
  following tags or else the subsequent PyQt compile will fail when
  trying to find phonon header files:

     [rluu@vapor qt-src-dir]$ ./configure -phonon -phonon-backend


##############################################################################

Notes for running on the Windows platform:

  Preferred way to get this going is:

   1) Install Python3 for Windows.

   2) Install the binary PyQt executable for Windows.  (This includes Qt).

   3) Install MinGW/MSYS.

   4) Install pytz.

   5) Install pyswisseph.  See below for the hacks necessary to get
   this working.
   
   6) Run pricechartingtool source code.

##############################################################################

Notes for building on the Windows platform:

  Note that these steps include the compiling of Qt and PyQt.  When I
  went through these steps, it worked on Windows 7, except whenever I
  would open a pop-up dialog off of the main window, it would crash
  the program.  It is suspected that it is because of a bad release of
  PyQt.  The binary installer of PyQt for windows worked fine.
  Proceed with that in mind.


Steps for building on the Windows platform:
  
  Download and install MinGW.  Also install some additional packages
  by running the following in a MinGW/MSYS shell.

    mingw-get install gcc g++ mingw32-make msys-wget msys-zip msys-unzip

  Download and install Python 3 for Windows.  The rest of this how-to
  section assumes that Python 3.2 was installed, and to directory
  C:\Python32.

  Run the following in a MinGW/MSYS shell to add a symbolic link from
  python.exe to python3.exe.

    cd /c/Python32/
    ln -s python.exe python3.exe

  Download and install Qt4 for Windows MinGW.  If the Qt4 installer
  complains about not being able to find w32api.h, check to make sure
  it exists in that directory.  If the file is there in the expected
  location then ignore that warning.

  Add the following paths to the Windows PATH environment variable: 

    C:\MinGW\msys\1.0\bin
    C:\MinGW\bin
    C:\Python32
    C:\Qt\4.7.4\bin

  In MinGW/MSYS, add the following to ~/.bashrc (and change the
  install paths accordingly):

    export QTDIR=/c/Qt/4.7.4
    export PATH=/c/Python32:$QTDIR/bin:/mingw/bin:$PATH

  Note that ~/.bashrc does not get sourced by MinGW/MSYS
  automatically, so it needs to be done each time you open a shell.
  
  Next, move the MSYS sh.exe because it confuses mingw32-make.exe when
  installing SIP and PyQt4 Makefiles.  It should be moved back after
  the install of those two packages.
  
    Open a cmd.exe window and run:

      mv C:\MinGW\msys\1.0\bin\sh.exe C:\MinGW\msys\1.0\bin\sh_moved.exe
	   
  Install SIP:

    Open a cmd.exe window and run:

      cd C:\MinGW\msys\1.0\home\rluu\programming\pricechartingtool\tps\pyqt\4.8.5
      unzip sip-4.12.4.zip
      cd sip-4.12.4
      python configure.py -p win32-g++
      mingw32-make install

  Install PyQt4:

    Open a cmd.exe window and run:

      cd C:\MinGW\msys\1.0\home\rluu\programming\pricechartingtool\tps\pyqt\4.8.5
      unzip PyQt-win-gpl-4.8.5.zip
      cd PyQt-win-gpl-4.8.5
      python configure.py -p win32-g++
      mingw32-make install

  Install pytz:

    Open a cmd.exe window and run:

      cd C:\MinGW\msys\1.0\home\rluu\programming\pricechartingtool\tps\pytz
      tar xjvf pytz-2010h.modsForPython3.tar.bz2
      cd pytz-2010h
      python setup.py install

  Install pyswisseph (requires the following hacks to build on MinGW):

    Do the following to fix an error that would normally happen during
    compilation of pyswisseph (and possibly other packages).  
    The error seen without this fix is: 'error: Unable to find vcvarsall.bat'.
    
      Create or edit file C:\Python32\Lib\distutils\distutils.cfg 
      so that it has the following contents:

        [build]
        compiler=mingw32
    
    Edit C:\Python32\Lib\distutils\cygwinccompiler.py to avoid a gcc
    compiler error where gcc doesn't know what what the command-line
    option '-mno-cygwin' is.  Here we will remove all locations where
    '-mno-cygwin' is found in this file.
    
      vim /c/Python32/Lib/distutils/cygwinccompiler.py

        :%s/-mno-cygwin //gc
        :wq

    Open up a MinGW/MSYS shell window and run the following.

      cd /home/rluu/programming/pricechartingtool/tps/pyswisseph
      tar xjvf pyswisseph-1.76.00-0.tar.bz2
      cd pyswisseph-1.76.00-0

    Edit the Makefile and change the CC variable so that it uses gcc
    instead of cc.

      vim src/Makefile

    Edit file 'pyswisseph.c' and and c-style comments around "#define
    USE_SWEPHELP".  This has to happen because this part of pyswisseph
    uses pthread, setenv(), and unsetenv(), which are supported only
    on POSIX.  Usage of those POSIX features are minimal, so if I
    wanted to, I could one day modify that code so that it is more
    platform-independent.

    Edit the top-level setup.py file:
      
      Edit 'include_dirs' variable and remove 'swephelp' from that list.

      Edit 'sources' variable and comment out all files listed that
      start with 'swephelp'.

    Now build pyswisseph and it should work:

      python setup.py install

##############################################################################

General info about compiling PyQt with MinGW:

  If compiling SIP or PyQt on Windows platform using MinGW, use the following 
  configure command so that the environment can be detected correctly: 

     python configure.py -p win32-g++
  
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

Shortcut keys (also listed in the Help menu):

Tool Modes:
  - Key_F1: ReadOnlyPointerToolAction
  - Key_F2: PointerToolAction
  - Key_F3: HandToolAction
  - Key_F4: Trigger the last used tool mode (that is not one of the above).

Time Modal Scale Tool:
  - Key_S: Rotate the modal scale left.
  - Key_G: Rotate the modal scale right.
  - Key_R: Reverse the direction of the modal scale.

Price Modal Scale Tool:
  - Key_S: Rotate the modal scale down.
  - Key_G: Rotate the modal scale up.
  - Key_R: Reverse the direction of the modal scale.

Octave Fan Tool:
  - Key_S: Rotate the modal scale up.
  - Key_G: Rotate the modal scale down.
  - Key_R: Reverse the direction of the modal scale.

Snap key bindings are:
  - Key_Q: Turn snap mode on.
  - Key_W: Turn snap mode off.

Snap key bindings are supported for the following tools:
  - BarCountTool
  - TimeMeasurementTool
  - PriceMeasurementTool
  - TimeModalScaleTool
  - PriceModalScaleTool
  - PriceTimeInfoTool
  - TimeRetracementTool
  - PriceRetracementTool
  - PriceTimeVectorTool
  - LineSegmentTool
  - OctaveFanTool
  - FibFanTool
  - GannFanTool
  - VimsottariDasaTool
  - AshtottariDasaTool
  - YoginiDasaTool
  - DwisaptatiSamaDasaTool
  - ShattrimsaSamaDasaTool
  - DwadasottariDasaTool
  - ChaturaseetiSamaDasaTool
  - SataabdikaDasaTool
  - ShodasottariDasaTool
  - PanchottariDasaTool
  - ShashtihayaniDasaTool
  
##############################################################################

Note: 

Temporary JHora .jhd files that are created will be placed in directory:

   For Linux:
     ~/.wine/drive_c/PriceChartingTool/data/

   For Mac OS X:
     ~/.wine/drive_c/PriceChartingTool/data/

   For Microsoft Windows:
     C:\PriceChartingTool\data\

The files in the above paths will be removed at startup if the file is
older than 180 days.

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


Swiss Ephemeris calculation anomalies found by me (rluu):

1) Calculating the geocentric declination of the Sun when the
Ephemeris is set to sidereal yields different values than when it is
queried when set to tropical.  The difference is small, but
significant since there should not be any differences of declination
because declination is measured on a different axis.  The different
seen was about 0.0006 degrees, or over two arc seconds.  Differences
may be larger when looking at other planets.  In this program I will
try to use geocentric tropical settings whenever getting declination.

2) Values obtained by quering the heliocentric declination of the
Earth is not correct.  The results seen appear to be just -1 times the
geocentric declination of the Sun.  My guess is other heliocentric
declinations are probably wrong too.


##############################################################################
