#!/usr/bin/env bash
##############################################################################
# Vagrant bootstrap script to get PriceChartingTool up and running
# with Python3, Qt5, and PyQt5.
##############################################################################

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
sudo apt-get install -y zip
sudo apt-get install -y unzip
sudo apt-get install -y python3-pip
sudo apt-get install -y qt5-default
sudo apt-get install -y python3-pyqt5
#sudo apt-get install -y pyqt5-dev-tools

# Install virtualenv and use that instead of using pyvenv,
# because there is a bug with pyvenv on ubuntu/trusty64,
# preventing it from working.  
# In the future, we should be able to switch to using pyvenv instead
# of virtualenv.
sudo pip3 install virtualenv

##############################################################################

cd $PROJECT_HOME

# Create the virtual environment for Python 3.
virtualenv --system-site-packages --always-copy venv

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
cd $PROJECT_HOME

# pyswisseph
cd $PROJECT_HOME/tps/pyswisseph
tar -xjvf pyswisseph-1.77.00-0.tar.bz2
cd pyswisseph-1.77.00-0
python3 setup.py install
cd $PROJECT_HOME

# PyQt5 dependency: sip
cd $PROJECT_HOME/tps/pyqt/5.5
tar -xzvf sip-4.16.9.tar.gz
cd sip-4.16.9
python3 configure.py
make
sudo make install

# PyQt5
cd $PROJECT_HOME/tps/pyqt/5.5
tar -xzvf PyQt-gpl-5.5.tar.gz
cd PyQt-gpl-5.5
python3 configure.py --confirm-license
make
make install

########################################
# Initialize resource files.

cd $PROJECT_HOME/resources
./generateResourceSourceFile.sh
cd $PROJECT_HOME

########################################

# Optionally, run 'qtconfig' and set the look and GUI style to whatever
# is desired.
# 
# The recommended style is "Plastique" because that style will allow
# the PriceBarChartSettings dialog to fit within the vertical size of a
# Macbook Pro 15 inch laptop screen. 

##############################################################################
