#!/bin/sh

# make sure to enter you virtualenv first!
# $ . venv/bin/activate

pip install Flask
pip install poster

# Because the egg in the Python package repo doesn't install properly
pip install -e git://github.com/mLewisLogic/foursquare.git#egg=foursquare
# getting pymaps.py
svn checkout http://pymaps.googlecode.com/svn/trunk/ pymaps-read-only
mv pymaps-read-only/pymaps.py pymaps.py
rm -rf pymaps-read-only