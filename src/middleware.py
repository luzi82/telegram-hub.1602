import flask
from werkzeug.datastructures import EnvironHeaders

class WebTemplateMiddleWare:

    def __init__(self, wsgi_app, app):
        self.wsgi_app = wsgi_app
        self.app = app

    def __call__(self, environ, start_response):
        if self.app.debug:
            headers = list(EnvironHeaders(environ).items())
            for k,v in headers:
                print(f'{k}: {v}')
        return self.wsgi_app(environ, start_response)
