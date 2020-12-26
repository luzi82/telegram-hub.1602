import db
import env
import flask
import flask_login
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def add_url_rule(app):
  app.add_url_rule('/hubs/',                     'endpoint_hub_list',           endpoint_hub_list)
  app.add_url_rule('/hubs/new',                 'endpoint_hub_new',            endpoint_hub_new)
  app.add_url_rule('/hubs/<hub_id>/',            'endpoint_hub',                endpoint_hub)
  app.add_url_rule('/hubs/<hub_id>/publishers/', 'endpoint_hub_publisher_list', endpoint_hub_publisher_list)
  app.add_url_rule('/hubs/<hub_id>/chats/',      'endpoint_hub_chat_list',      endpoint_hub_chat_list)

def endpoint_hub_list():
  hub_list = db.get_hub_list_from_user(flask_login.current_user.id)
  return flask.render_template('hub/hub_list.tmpl',
    HUB_LIST = hub_list,
  )

def endpoint_hub_new():
  return flask.render_template('hub/hub.new.tmpl')

def endpoint_hub(hub_id):
  hub = db.get_hub(hub_id)
  return flask.render_template('hub/hub.tmpl',
    HUB = hub,
  )

def endpoint_hub_publisher_list(hub_id):
  hub_publisher_list = db.get_hub_publisher_list_from_hub(hub_id)
  return flask.render_template('hub/hub_publisher_list.tmpl',
    HUB_PUBLISHER_LIST = hub_publisher_list,
  )

def endpoint_hub_chat_list(hub_id):
  chat_list = db.get_chat_list_from_hub(hub_id)
  return flask.render_template('hub/hub_chat_list.tmpl',
    CHAT_LIST = chat_list,
  )
