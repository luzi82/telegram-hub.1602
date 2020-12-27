import flask
import json
from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  import werkzeug.wrappers

def r200(data:Any=None) -> flask.Response:
  return flask.Response(
    response = json.dumps({
      'STATUS':'OK',
      'RESULT':data,
    }),
    status = 200,
    mimetype='application/json',
  )

def e400(err_msg:str) -> flask.Response:
  return flask.Response(
    response = json.dumps({
      'STATUS':'BAD REQUEST',
      'ERR_MSG':err_msg,
    }),
    status = 400,
    mimetype='application/json',
  )

def e403() -> flask.Response:
  return flask.Response(
    response = json.dumps({
      'STATUS':'AUTH ERR',
    }),
    status = 403,
    mimetype='application/json',
  )

def e500(err_msg:Any) -> flask.Response:
  return flask.Response(
    response = json.dumps({
      'STATUS':'SERVER ERR',
      'ERR_MSG':err_msg,
    }),
    status = 400,
    mimetype='application/json',
  )

def redirect(location:str) -> "werkzeug.wrappers.Response":
  return flask.redirect(location)
