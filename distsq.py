from foursquare import Foursquare, FoursquareException
from pymaps import Icon, Map, PyMap
from flask import Flask, render_template, url_for, redirect, request, abort, \
                  session
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

@app.route('/auth')
def auth():
    client = getFoursquare()
    auth_uri = client.oauth.auth_url()
    return redirect(auth_uri)

@app.route('/login')
def login():
    code = request.args.get("code", None)
    if code is not None:
        client = getFoursquare()
        access_token = client.oauth.get_token(code)
        session['access_token'] = access_token
        return redirect(url_for('dashboard'))
    else:
        abort(401)


@app.route('/dashboard/')
def dashboard():
    client = getFoursquare()
    try:
        client.set_access_token(session['access_token'])
        return render_template('dashboard.html', user=client.users()['user'],
                               checkins=client.users.checkins()['checkins'])
    except AttributeError:
        abort(401)

@app.route('/logout')
def logout():
    session.pop('client', None)
    return redirect(url_for('index'))

@app.route('/test/')
def test():
    #return render_template('test.html', map = showmap())
    return showmap()

def getFoursquare():
    client = Foursquare(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri="http://127.0.0.1:5000" +
                        url_for('login'))
    return client

def showmap():
    # Create a map
    tmap = Map()
    tmap.zoom = 17

    #Test lat and lognitue coordinates
    lat = 0.0
    long = 0.0
    
    #These coordinates are for Hong Kong
    dlat = "22 15 0 N"
    dlong = "114 10 60 E"

    dlat = dlat.rsplit(" ")
    dlong = dlong.rsplit(" ")

    #Convert the coordinates
    #lat = getcords(float(dlat[0]), float(dlat[1]), float(dlat[2]), dlat[3])
    #long = getcords(float(dlong[0]), float(dlong[1]), float(dlong[2]), dlong[3])
    lat = 39.9524
    long = -75.190521

    pointhtml = "hello there!"
    
    #Creates new icon
    icon1 = Icon('icon1')

    point = (lat, long, pointhtml, icon1.id)

    tmap.setpoint(point)
    tmap.center = (lat, long)

    gmap = PyMap(key=API_KEY, maplist=[tmap])
    gmap.addicon(icon1)
    
    mapcode = gmap.pymapjs()

    #return mapcode
    return gmap.showhtml()

def getcords(deg, mins, sec, ind):
    
    #Calculate total number of seconds
    secs = float((mins * 60) + sec)

    #Fractional number of seconds divided by 3600
    frac = float(sec / 3600)

    #Add fractional degrees to whole degrees
    degrees = float(deg + frac)

    if ind == 'W':
        deg = deg * -1
    elif ind == 'S':
        deg = deg * -1

    return float(deg)

def center(lat, long):
    """ Is meant to find the center of multiple points on a graph"""
    return (lat, long)

#Need to create a global map to be created in the inception of the dashbaord
#thus we need to have methods to change the center, add points, and reset graph if necessary.

if __name__ == '__main__':
    app.run()
