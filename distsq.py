from foursquare import Foursquare, FoursquareException
from flask import Flask, render_template, url_for, redirect, request, abort, \
                  session
app = Flask(__name__)

# configuration
DEBUG = True
SECRET_KEY = "development key"
CLIENT_ID = "TUOPMCKP3D1LZBAUH2UOPOXCG4AXJ224NXZ54BOIWCK5KCI3"
CLIENT_SECRET = "RDBMXGQNQNHAWK1YHZA04TPNYW3LB1UY401QCUPXPKHCOVEN"

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
        return render_template('dashboard.html', user=client.users()['user'])
    except AttributeError:
        abort(401)

@app.route('/logout')
def logout():
    session.pop('client', None)
    return redirect(url_for('index'))

def getFoursquare():
    client = Foursquare(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri="http://127.0.0.1:5000" +
                        url_for('login'))
    return client

if __name__ == '__main__':
    app.run()
