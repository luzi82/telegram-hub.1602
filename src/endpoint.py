import flask
import futsu.json
import futsu.storage
import os

app = flask.Flask(__name__)

STAGE = os.environ['STAGE']
CONF_PATH = os.environ['CONF_PATH']

@app.route('/')
def index():
    return flask.render_template('index.tmpl',
        STAGE=STAGE,
    )

@app.route('/compute_domain')
def get_compute_domain():
    conf_data = futsu.json.path_to_data(futsu.storage.join(CONF_PATH,'conf.json'))
    return conf_data['COMPUTE_DOMAIN']
