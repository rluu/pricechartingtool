#!/usr/bin/env bash

##############################################################################
# Variables.

# Get the directory where this script is running.
scriptDirectory=`dirname "$0"`

# Shared directory with the virtual machine's host operating system,
# which is mapped to the project's top-level directory.
export PROJECT_HOME=/vagrant

##############################################################################
# Install operating system packages.

sudo apt-get update

#sudo apt-get install -y emacs23
sudo apt-get install -y git
sudo apt-get install -y unzip
sudo apt-get install -y libqt4-dev
sudo apt-get install -y qt4-qtconfig
sudo apt-get install -y python3-pip

# Install virtualenv and use that instead of using pyvenv,
# because there is a bug with pyvenv on ubuntu/trusty64,
# preventing it from working.  
# In the future, we should be able to switch to using pyvenv instead
# of virtualenv.
sudo pip3 install virtualenv

##############################################################################

cd $PROJECT_HOME

# Create the virtual environment for Python 3.
virtualenv venv

source ./venv/bin/activate

########################################
# Install third party software.

# pytz
cd $PROJECT_HOME/tps/pytz
tar -xjvf pytz-2014.9.tar.bz2
cd pytz-2014.9
python3 setup.py install
cd $PROJECT_HOME/venv/lib/python3.4/site-packages/
unzip pytz-2014.9-py3.4.egg

# pyswisseph
cd $PROJECT_HOME/tps/pyswisseph
tar -xjvf pyswisseph-1.77.00-0.tar.bz2
cd pyswisseph-1.77.00-0
python3 setup.py install

# PyQt4 dependency: sip
cd $PROJECT_HOME/tps/pyqt/4.11.3
tar -xzvf sip-4.16.5.tar.gz
cd sip-4.16.5
python3 configure.py
make
sudo make install

# PyQt4
cd $PROJECT_HOME/tps/pyqt/4.11.3
tar -xzvf PyQt-x11-gpl-4.11.3.tar.gz
cd PyQt-x11-gpl-4.11.3
python3 configure.py --confirm-license
make
make install

########################################
# Initialize resource files.

cd $PROJECT_HOME/resources
./generateResourceSourceFile.sh
cd ..

########################################

# Optionally, run 'qtconfig' and set the look and GUI style to whatever
# is desired.

##############################################################################
