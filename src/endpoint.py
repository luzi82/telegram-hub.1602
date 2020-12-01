import datetime
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.datetime.now()
    return f'Hello, World!  Time is {now}.'
