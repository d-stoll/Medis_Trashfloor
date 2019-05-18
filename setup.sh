#!/bin/bash

sudo apt-get install build-essential python-dev python-pip unzip wget scons swig

wget https://github.com/jgarff/rpi_ws281x/archive/master.zip
unzip master.zip
cd rpi_ws281x-master
sudo scons

pip install -r requirements.txt