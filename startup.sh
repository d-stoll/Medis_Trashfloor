#!/usr/bin/env bash

sudo apt-get install python3-pip
pip3 install virtualenv

virtualenv -p python3 venv

source venv/bin/activate


pip3 install -r requirements.txt

python3 Wuerfel_Musik_Trashfloor.py