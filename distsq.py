import foursquare
from flask import Flask, render_template, url_for, redirect
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
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                   redirect_uri="http://127.0.0.1:5000" + url_for('dashboard'))
    auth_uri = client.oauth.auth_url()
    return redirect(auth_uri)

@app.route('/dashboard/')
def dashboard():
    pass

if __name__ == '__main__':
    app.run()
