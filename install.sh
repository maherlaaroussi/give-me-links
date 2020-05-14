#!/bin/sh
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xzvf geckodriver-v0.26.0-linux64.tar.gz
rm geckodriver-v0.26.0-linux64.tar.gz
mv geckodriver /usr/local/bin
python3 --version
python3 -m venv env
source ./env/bin/activate
python3 -m pip install -r requirements.txt
