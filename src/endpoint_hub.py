import db
import env
import flask
import flask_login
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def add_url_rule(app):
  app.add_url_rule('/hubs', 'endpoint_hub_list', endpoint_hub_list)
  # app.add_url_rule('/hubs/<hub_id>', 'endpoint_hub', endpoint_hub)

def endpoint_hub_list():
  current_user = flask_login.current_user
  hub_list = db.get_hub_list_from_user(current_user.id)
  return flask.render_template('hub/hub_list.tmpl',
    PUBLIC_STATIC_HTTP_PATH = env.PUBLIC_STATIC_HTTP_PATH,
    HUB_LIST = hub_list,
    TELEGRAM_USER_ID = current_user.id,
  )
