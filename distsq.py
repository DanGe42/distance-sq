from foursquare import Foursquare, FoursquareException, InvalidAuth
from flask import Flask, render_template, url_for, redirect, request, \
                  session, flash
import time

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
    """ Renders the index page. """
    return render_template('index.html')

@app.route('/login')
def login():
    """ Called when the user clicks the login button. This function redirects to
    the Foursquare OAuth page. """
    client = _get_foursquare()
    auth_uri = client.oauth.auth_url()
    return redirect(auth_uri)

@app.route('/auth')
def auth():
    """ Callback for the Foursquare OAuth page. Foursquare gives us a 'code'
    parameter on this call, so we parse this code and get the access token from
    Foursquare. We store the access token into the session cookie.

    If the user improperly calls this function, we redirect him back to the
    index page with a error message. """

    code = request.args.get("code", None)
    try:
        if code is None or code == "":
            raise FoursquareException

        client = _get_foursquare()
        access_token = client.oauth.get_token(code)
    except FoursquareException:
        flash('Connect to your Foursquare account to log in')
        return redirect(url_for('index'))

    session['access_token'] = access_token
    return redirect(url_for('dashboard'))


@app.route('/dashboard/')
def dashboard():
    """ Renders the dashboard. If the user is not logged in, we return the user
    to the homepage with an error message.

    The dashboard takes user-defined values of start and end times (defined in
    /settings/). If the start and end times are not properly defined, we provide
    default start (current time - 24 hours) and end times (current time). We
    then query Foursquare for checkin data and render it onto dashboard.html.
    """

    client = _get_foursquare()
    try:
        client.set_access_token(session['access_token'])
    except (KeyError, InvalidAuth):
        flash('You are not logged in.')
        return redirect(url_for('index'))

    start = request.args.get("start", None)
    end = request.args.get("end", None)

    params = _set_params(start, end)
    if len(params) == 0:
        flash('Invalid parameters. Defaulting to defaults.')

    checkins = client.users.checkins(params=params)['checkins']
    checkins, locations, bounds, center = _process_checkins(checkins)

    return render_template('dashboard.html', user=client.users()['user'],
                           checkins=checkins,
                           locations= locations, bounds = bounds,
                           center=center, key=API_KEY, start=start, end=end)

def _set_params(start, end):
    """ Take the GET parameters provided to dashboard and puts them into the
    params dictionary passed to the API call in dashboard(). See dashboard() for
    how default values are calculated. """

    params = {}
    try:
        if not start:
            start_time = _get_day_before( int(round(time.time())) )
        else:
            start_time = int(start)

        params['afterTimestamp'] = start_time

        if end:
            params['beforeTimestamp'] = int(end)

        return params
    except ValueError:
        return {}

def _process_checkins(checkins):
    checkins_list = _list_locations(checkins)

    locations = []
    location_names = set()
    center = {}
    bounds = {}

    for checkin in checkins_list:
        if not checkin['name'] in location_names:
            location_names.add(checkin['name'])
            checkin['name'] = checkin['name'].replace(' ', '')
            checkin['name'] = checkin['name'].replace('&', 'and')
            checkin['name'] = checkin['name'].replace('-', '')
            locations.append(checkin)
    if locations:
        center = _find_center(locations)
        bounds = _bounds(locations)
    else:
        center = {'lat' : 39.9524116516, 'long' : -75.1905136108}

    return checkins_list, locations, bounds, center

@app.route('/settings/')
def settings():
    """ Allows the user to change the time range for checkins. If the user is
    not logged in, we redirect him to the home page. """
    if 'access_token' not in session:
        flash('You are not logged in.')
        return redirect(url_for('index'))
    return render_template('settings.html')

@app.route('/logout')
def logout():
    """ Logs the user out by removing the access token from the session cookie.
    """
    if session['access_token']:
        session.pop('access_token', None)
        flash('You have been logged out successfully')
    return redirect(url_for('index'))

def _get_foursquare():
    """ Returns the default Foursquare client object. """
    client = Foursquare(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri="http://127.0.0.1:5000" +
                        url_for('auth'))
    return client

def _list_locations(checkins):
    """ Takes the list of checkins from the Foursquare API and reduces it down
    to a list of dictionaries of a venue name, location, and ID.

    Usage example:
        locations = _list_locations(checkins)
        for location in locations:
            print "name = " + location['name']
            print "latitude = " + location['lat']
            print "longitude = " + location['long']
            print "ID = " + location['id']
            print ""
    """
    result = [{'name': item['venue']['name'],
               'lat': item['venue']['location']['lat'],
               'long': item['venue']['location']['lng'],
               'id': item['id']} for item in checkins['items']]
    return result

def _get_day_before(timestamp):
    """ Returns (timestamp - 24 hours). The timestamp provided is Unix time in
    seconds. """
    return timestamp - (24 * 60 * 60)

def _bounds(dict_list):
    """ Is meant to find the appropriate zoom value based on points on graph
    asssuming 72 DPI printout"""
    max_lat = -90
    min_lat = 90
    max_long = -180
    min_long = 180

    for dict_ in dict_list:
        if dict_['lat'] > max_lat:
            max_lat = dict_['lat']
        elif dict_['lat'] < min_lat:
            min_lat = dict_['lat']
        if dict_['long'] > max_long:
            max_long = dict_['long']
        elif dict_['long'] < max_long:
            min_long = dict_['long']

    return {'min_lat' : min_lat,
            'min_long' : min_long,
            'max_lat' : max_lat,
            'max_long' : max_long}

def _find_center(dict_list):
    """ Is meant to find the center of multiple points on a graph"""
    lat = 0
    lng = 0
    print dict_list
    for dict_ in dict_list:
        lat += dict_['lat']
        lng += dict_['long']
    lat = lat/len(dict_list)
    lng = lng/len(dict_list)
    return {'lat' : lat, 'long' : lng}


if __name__ == '__main__':
    app.run()
