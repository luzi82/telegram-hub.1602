import db_hub_publisher
import db_hub
import env
import flask
import flask_login
import logging
import th

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def add_url_rule(app):
  app.add_url_rule('/bots/',                      'endpoint_bot_list',            endpoint_bot_list)
  app.add_url_rule('/bots/new',                   'endpoint_bot_new',             endpoint_bot_new)
  app.add_url_rule('/bots/<bot_id>/',             'endpoint_bot',                 endpoint_bot)
  app.add_url_rule('/bots/<bot_id>/permissions/', 'endpoint_bot_permission_list', endpoint_bot_permission_list)

def endpoint_bot_list():
  hub_list = db_hub.get_hub_list_from_user(flask_login.current_user.id)
  return flask.render_template('hub/hub_list.tmpl',
    HUB_LIST = hub_list,
  )

def endpoint_bot_new():
  return flask.render_template('hub/hub.new.tmpl')

def endpoint_bot(hub_id):
  hub = db_hub.get_hub(hub_id)
  return flask.render_template('hub/hub.tmpl',
    HUB = hub,
  )

def endpoint_bot_publisher_list(hub_id):
  hub_publisher_list = db_hub_publisher.get_hub_publisher_list_from_hub(hub_id)
  return flask.render_template('hub/hub_publisher_list.tmpl',
    HUB_PUBLISHER_LIST = hub_publisher_list,
  )

def endpoint_bot_chat_list(hub_id):
  chat_list = db_chat_hub.get_chat_list_from_hub(hub_id)
  return flask.render_template('hub/hub_chat_list.tmpl',
    CHAT_LIST = chat_list,
  )
