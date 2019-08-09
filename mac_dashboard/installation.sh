#!/bin/bash

#install python
sudo apt install python3-pip
#install depepndencies, use "pip freeze" for us to get the required versions etc
#pip install -r requirements.txt
#pip freeze > requirenents.txt to get the file
sudo pip install scapy
sudo pip install request
pip3 install netdisco
sudo pip install --ignore-installed six pandas
sudo pip install matplotlib
sudo pip install --user --upgrade matplotlib
sudo pip install flask
sudo pip install pillow
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
#Install python3
pip3 install flask