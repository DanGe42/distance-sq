from flask import Flask
app = Flask(__name__)

# configuration
DEBUG = True
SECRET_KEY = "development key"

app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
