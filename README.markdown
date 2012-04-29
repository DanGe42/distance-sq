# Distance Square

Distance Square is a simple web application that aims to help users map out
their travels and finding the most efficient paths between checkpoints using
Foursquare and Google Maps.

## Contributors
Daniel Ge - dange
Dan Trujillo - dtru
Alina Chin - alchin

## How to run
To download the latest iteration of this project,

    git clone git://github.com/DanGe42/distance-sq.git

Ensure that Python 2.7, virtualenv, and pip are installed. For Linux users,
these can easily be installed by the package manager provided by the
distribution.

This project has two main dependencies: Flask and foursquare. To install these
dependencies, run these commands in your bash terminal:

    $ cd distance-sq
    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

It is important to activate the virtualenv before working with the project. It
is not recommended to install these packages on your system globally.

Now that the requirements have been met, we simply run:

    python distsq.py

## Code organization
* distsq.py: The main server backend script for [Flask](http://flask.pocoo.org/).
Flask is a simple lightweight server backend written in Python. This script
handles all routing and authentication.
* templates/: The folder that holds all of our Jinja2 templates, which are used
for rendering the pages sent back to the browser. [Jinja2](http://jinja.pocoo.org/)
is a templating language that mixes Python with HTML.
    * base.html: The base template that provides the HTML skeleton for all other
    templates.
    * index.html: The landing page. This contains the Foursquare login button.
    * dashboard.html: The dashboard page. This contains all information on
    checkins and displays the map.
    * settings.html: This page allows the user to specify the time frame for
    the checkins.

## Known issues
* Currently, the settings page is not intuitive to use. It requires the use of
Unix time in seconds.
