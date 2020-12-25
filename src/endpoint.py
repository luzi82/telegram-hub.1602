import datetime
import flask
app = flask.Flask(__name__)

@app.route('/')
def index():
    now = datetime.datetime.now()
    flask_request_host_url = flask.request.host_url
    return flask.render_template(
        'index.html.tmpl',
        now = now,
        flask_request_host_url = flask_request_host_url,
    )
