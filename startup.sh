#!/usr/bin/env bash

sudo apt-get install python3-pip
pip3 install virtualenv

venv_folder="venv/bin/activate"

if [[ ! -f "$venv_folder" ]]; then
    virtualenv -p python3 venv
fi

source venv/bin/activate

pip3 install -r requirements.txt
python3 Wuerfel_Musik_Trashfloor.py