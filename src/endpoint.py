import flask
import os

app = flask.Flask(__name__)

STAGE = os.environ['STAGE']

@app.route('/')
def index():
    return flask.render_template('index.tmpl',
        STAGE=STAGE,
    )
