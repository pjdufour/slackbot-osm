#!/bin/bash
echo "Initializing environment for EC@ deployment of Slack Bot OSM"
sudo apt-get update
sudo apt-get upgrade
sudo apt-get update
# Add UbuntuGIS Repository to get latest GDAL package
sudo apt-get install -y python-software-properties
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
# Essential build tools and libraries
sudo apt-get install -y build-essential gettext git python-dev python-pip python-virtualenv
sudo apt-get install -y python-bs4 python-httplib2
sudo apt-get install -y supervisor
sudo pip install virtualenvwrapper
#Add all these lines to ~/.bash_aliases
echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python' >> ~/.bash_aliases
echo 'export WORKON_HOME=~/.venvs' >> ~/.bash_aliases
echo 'source /usr/local/bin/virtualenvwrapper.sh'>> ~/.bash_aliases
echo 'export PIP_DOWNLOAD_CACHE=$HOME/.pip-downloads' >> ~/.bash_aliases
source ~/.bash_aliases
mkvirtualenv slackbotosm
workon slackbotosm
cd ~
pip install -r slackbot-osm.git/requirements.txt
pip install -e slackbot-osm.git
