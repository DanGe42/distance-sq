#!/bin/sh

# make sure to enter you virtualenv first!
# $ . venv/bin/activate

pip install Flask
pip install poster

# Because the egg in the Python package repo doesn't install properly
pip install -e https://github.com/mLewisLogic/foursquare#egg=foursquare
