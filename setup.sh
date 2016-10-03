#!/bin/bash 

# test to use compare view feature in github
# Install Pip and virtualenv
sudo apt-get install python-pip python-virtualenv

# Initialize new env here
virtualenv --no-site-packages .

# Activate the environment
source bin/activate

# Install dependencies (Only selenium at the moment)
pip install -r requirements.txt


