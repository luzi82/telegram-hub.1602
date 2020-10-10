import flask
import json

def r200(data=None):
  return flask.Response(
    response = json.dumps({
      'STATUS':'OK',
      'RESULT':data,
    }),
    status = 200,
    mimetype='application/json',
  )

def e400(err_msg):
  return flask.Response(
    response = json.dumps({
      'STATUS':'BAD REQUEST',
      'ERR_MSG':err_msg,
    }),
    status = 400,
    mimetype='application/json',
  )

def e500(err_msg):
  return flask.Response(
    response = json.dumps({
      'STATUS':'BAD REQUEST',
      'ERR_MSG':err_msg,
    }),
    status = 400,
    mimetype='application/json',
  )

def redirect(location):
  return flask.redirect(location)
