##############################################################################
pyswisseph-1.77.00-0.tar.bz2
##############################################################################

Website: https://pypi.python.org/pypi/pyswisseph

##############################################################################

To build and install run:

tar -xjvf pyswisseph-1.77.00-0.tar.bz2
cd pyswisseph-1.77.00-0
python3 setup.py build
su
python3 setup.py install


##############################################################################

Note_20141105: 
If the build step fails due to error given as follows: 

---------

swephelp/swhgeo.c: In function ‘swh_geoc2d’:
swephelp/swhgeo.c:56:5: error: ISO C90 forbids mixed declarations and code [-Werror=declaration-after-statement]
     char *saveptr;
     ^
swephelp/swhgeo.c:52:29: warning: variable ‘degmax’ set but not used [-Wunused-but-set-variable]
     int deg, dir, min, sec, degmax;
                             ^
cc1: some warnings being treated as errors
error: command 'gcc' failed with exit status 1

---------


The reason for the build failure is because of the way Python3.4 and Python3.5 were built with gcc; CFLAGS were set that clobbered build flags set for all modules after.  See comments in:
http://bugs.python.org/issue21121

The workaround is to run this before building the module:
export CFLAGS=$(python3.4 -c 'import sysconfig; print(sysconfig.get_config_var("CFLAGS").replace("-Werror=declaration-after-statement",""))')

Then you can try again with:
python3 setup.py build

##############################################################################
