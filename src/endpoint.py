import datetime
import flask
app = flask.Flask(__name__)

@app.route('/')
def index():
    now = datetime.datetime.now()
    return flask.render_template(
        'index.html.tmpl',
        now = now,
    )
