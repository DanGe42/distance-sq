#!/bin/sh

# make sure to enter you virtualenv first!
# $ . venv/bin/activate

pip install Flask
pip install poster
pip install foursquare

# getting pymaps.py (deprecated, using js instead)
#svn checkout http://pymaps.googlecode.com/svn/trunk/ pymaps-read-only
#mv pymaps-read-only/pymaps.py pymaps.py
#rm -rf pymaps-read-only
