# Steps taken to get my software up and running on a Amazon Linux image.

# Connect to the EC2 instance.
ssh -i aws_mykeypair.pem ec2-user@ec2-52-0-155-248.compute-1.amazonaws.com

# Install security updates if this is the first time logging in.
sudo yum update

# Copy over .screenrc.  
scp -i aws_mykeypair.pem .screenrc ec2-user@ec2-52-0-155-248.compute-1.amazonaws.com:~/

# What do I want in my .bashrc?
alias sl='ls'

# Fix error when using less or vim that says:
#   E437: terminal capability “cm” required
sudo yum install ncurses-term

# Install various packages/libraries required for the Python3 build.
sudo yum install gcc
sudo yum install zlib-devel
sudo yum install readline-devel
sudo yum install openssl-devel

# Install Python 3.  
# Python 3.4 now comes with pip, so there's no need to install that separately.
mkdir download
cd download
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar -xzvf Python-3.4.3.tgz
./configure
make
# By doing sudo make install, Python 3 would get installed as 'python' which is not what we want.  We want it to be installed to a binary such as 'python3.4'.  make altinstall gives us that capability.
sudo make altinstall

# Install virtualenv.
sudo /usr/local/bin/pip3.4 install virtualenv

# Install packages. 
# git needed to obtain my source code.
sudo yum install git

git config --global user.name "Ryan Luu"
git config --global user.email "ryanluu@gmail.com"

# Get most recent version of my software.
mkdir -p ~/programming/pricechartingtool/master
cd ~/programming/pricechartingtool/master
git clone --depth=1 https://github.com/rluu/pricechartingtool.git .


# Use virtualenv.
cd ~/programming/pricechartingtool/master
virtualenv venv
source venv/bin/activate

# Install dependencies from tps.

# Install pytz.
cd ~/programming/pricechartingtool/master/tps/pytz
tar -xjvf pytz-2014.9.tar.bz2
cd pytz-2014.9
python3 setup.py install

# Extract the pytz egg so that pytz.timezone() runs faster 
# (otherwise the first usage takes several seconds!).
pip unzip pytz

# Install pyswisseph
cd ~/programming/pricechartingtool/master/tps/pyswisseph
tar -xjvf pyswisseph-1.77.00-0.tar.bz2
cd pyswisseph-1.77.00-0
python3 setup.py install

# After this, we should be able to run non-Qt components/modules.
cd ~/programming/pricechartingtool/master/src
python3 ephemeris.py
python3 lookbackmultiple_calc.py

