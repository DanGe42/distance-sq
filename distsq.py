from foursquare import Foursquare, FoursquareException
from pymaps import Icon, Map, PyMap
from flask import Flask, render_template, url_for, redirect, request, abort, \
                  session, flash
import time
import math
app = Flask(__name__)

# configuration
DEBUG = True
SECRET_KEY = "development key"
CLIENT_ID = "TUOPMCKP3D1LZBAUH2UOPOXCG4AXJ224NXZ54BOIWCK5KCI3"
CLIENT_SECRET = "RDBMXGQNQNHAWK1YHZA04TPNYW3LB1UY401QCUPXPKHCOVEN"
API_KEY = "AIzaSyC1yyyR4z1F9aV8FF1Xb-XtbD-UO53aLlY"
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    client = getFoursquare()
    auth_uri = client.oauth.auth_url()
    return redirect(auth_uri)

@app.route('/auth')
def auth():
    code = request.args.get("code", None)
    if code is not None:
        client = getFoursquare()
        access_token = client.oauth.get_token(code)
        session['access_token'] = access_token
        return redirect(url_for('dashboard'))
    else:
        flash('Connect to your Foursquare account to log in')
        return redirect(url_for('index'))


@app.route('/dashboard/')
def dashboard():
    client = getFoursquare()
    try:
        client.set_access_token(session['access_token'])
    except KeyError:
        abort(401)

    start= request.args.get("start", None)
    end = request.args.get("end", None)
    error = ""

    params = {}
    try:
        if not start:
            start_time = _get_day_before(int(round(time.time())))
        else:
            start_time = int(start)
        params['afterTimestamp'] = start_time

        if end:
            params['beforeTimestamp'] = int(end)
    except ValueError:
        flash('Invalid input. Defaulting to defaults.')
        params = {}

    checkins = client.users.checkins(params=params)

    return render_template('dashboard.html', user=client.users()['user'],
                           checkins=_list_locations(checkins['checkins']),
                           error=error)

@app.route('/settings/')
def settings():
    return render_template('settings.html')

@app.route('/logout')
def logout():
    if session['access_token']:
        session.pop('access_token', None)
        flash('You have been logged out successfully')
    return redirect(url_for('index'))

@app.route('/test/')
def test():
    return render_template('test.html', map = showmap())
    #return showmap()

@app.route('/test2/')
def test2():
    client = getFoursquare()
    try:
        client.set_access_token(session['access_token'])
    except KeyError:
        abort(401)

    start= request.args.get("start", None)
    end = request.args.get("end", None)
    error = ""

    params = {}
    try:
        if not start:
            start_time = _get_day_before(int(round(time.time())))
        else:
            start_time = int(start)
        params['afterTimestamp'] = start_time

        if end:
            params['beforeTimestamp'] = int(end)
    except ValueError:
        flash('Invalid input. Defaulting to defaults.')
        params = {}

    checkins = client.users.checkins(params=params)
    checkins = _list_locations(checkins['checkins'])
    locations = []
    location_names = []
    for checkin in checkins:
        if not checkin['name'] in location_names:
          location_names.append(checkin['name'])
          checkin['name'] = checkin['name'].replace(' ', '')
          checkin['name'] = checkin['name'].replace('&', 'and')
          locations.append(checkin)
    center = _find_center(locations)
    bounds = _bounds(locations)

    return render_template('test3.html', user=client.users()['user'],
                           checkins=checkins,
                           error=error, locations= locations, bounds = bounds,
                           center=center, key=API_KEY)

def getFoursquare():
    client = Foursquare(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri="http://127.0.0.1:5000" +
                        url_for('auth'))
    return client

def _list_locations(checkins):
    # result = []
    # for item in checkins['items']:
    #     venue = item['venue']
    #     result.append( (venue['name'], venue['location']['lat'],
    #                     venue['location']['lng'], item['id']) )
    #result = [(item['venue']['name'], item['venue']['location']['lat'],
    #           item['venue']['location']['lng'], item['id'])
    #          for item in checkins['item']]
    result = [{'name': item['venue']['name'],
               'lat': item['venue']['location']['lat'],
               'long': item['venue']['location']['lng'],
               'id': item['id']} for item in checkins['items']]
    return result

def _get_day_before(timestamp):
    return timestamp - (24 * 60 * 60)

def _bounds(dict_list):
    """ Is meant to find the appropriate zoom value based on points on graph asssuming 72 DPI printout"""
    max_lat = -90
    min_lat = 90
    max_long = -180
    min_long = 180
    for dict in dict_list:
        if dict['lat'] > max_lat:
            max_lat = dict['lat']
        elif dict['lat'] < min_lat:
            min_lat = dict['lat']
        if dict['long'] > max_long:
            max_long = dict['long']
        elif dict['long'] < max_long:
            min_long = dict['long']
    return {'min_lat' : min_lat, 'min_long' : min_long, 'max_lat' : max_lat, 'max_long' : max_long}

def _find_center(dict_list):
    """ Is meant to find the center of multiple points on a graph"""
    lat = 0
    long = 0
    print dict_list
    for dict in dict_list:
        lat += dict['lat']
        long += dict['long']
    lat = lat/len(dict_list)
    long = long/len(dict_list)
    return {'lat' : lat, 'long' : long}

#Need to create a global map to be created in the inception of the dashbaord
#thus we need to have methods to change the center, add points, and reset graph if necessary.
if __name__ == '__main__':
    app.run()
