import datetime
import flask
import futsu.json
import futsu.storage
import os

app = flask.Flask(__name__)

STAGE = os.environ['STAGE']
CONF_PATH = os.environ['CONF_PATH']
PUBLIC_STATIC_PATH   = os.environ['PUBLIC_STATIC_PATH']
PUBLIC_MUTABLE_PATH  = os.environ['PUBLIC_MUTABLE_PATH']
PRIVATE_STATIC_PATH  = os.environ['PRIVATE_STATIC_PATH']
PRIVATE_MUTABLE_PATH = os.environ['PRIVATE_MUTABLE_PATH']

@app.route('/')
def index():
    now_ts = int(datetime.datetime.now().timestamp())
    timestamp_path = futsu.storage.join(PRIVATE_MUTABLE_PATH,'timestamp')
    print(timestamp_path)

    last_ts = futsu.storage.path_to_bytes(timestamp_path).decode('utf-8') if futsu.storage.is_blob_exist(timestamp_path) else -1
    futsu.storage.bytes_to_path(timestamp_path,f'{now_ts}'.encode('utf-8'))

    return flask.render_template('index.tmpl',
        STAGE=STAGE,
        LAST_TS=last_ts,
        NOW_TS=now_ts,
    )

@app.route('/compute_domain')
def get_compute_domain():
    conf_data = futsu.json.path_to_data(futsu.storage.join(CONF_PATH,'conf.json'))
    return conf_data['COMPUTE_DOMAIN']
