import flask
import typing
# import werkzeug.types # type: ignore
from typing import Any
from typing import Callable
from werkzeug.datastructures import EnvironHeaders
#from werkzeug.types import WSGIEnvironment

class WebTemplateMiddleWare:

    def __init__(self, wsgi_app: Callable[..., Any], app: flask.Flask) -> None:
        self.wsgi_app = wsgi_app
        self.app = app

    def __call__(self, environ: Any, start_response: Callable[..., Any]) -> Any:
        if self.app.debug:
            headers = list(EnvironHeaders(environ).items()) # type: ignore
            for k,v in headers:
                print(f'{k}: {v}')
        return self.wsgi_app(environ, start_response)
