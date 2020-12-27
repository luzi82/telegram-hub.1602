import db_user
import env
import fk
import flask
import flask_login # type: ignore
import logging
import tg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def init_login_manager(login_manager):
  login_manager.user_loader(user_loader)
  login_manager.request_loader(request_loader)
  login_manager.unauthorized_handler(unauthorized_handler)

def add_url_rule(app):
  app.add_url_rule('/login', 'endpoint_login', endpoint_login)
  app.add_url_rule('/login/telegram-auth-callback', 'endpoint_login_telegram_auth_callback', endpoint_login_telegram_auth_callback,  methods=['GET','POST'])
  app.add_url_rule('/login/telegram-auth-bypass', 'endpoint_login_telegram_auth_bypass', endpoint_login_telegram_auth_bypass,  methods=['GET','POST'])
  app.add_url_rule('/logout', 'endpoint_logout', endpoint_logout)
  app.add_url_rule('/api/user', 'api_get_user', api_get_user)

def endpoint_login(err_msg=None):
  conf_data = env.get_conf_data()
  setup_tg_auth_bot_data = env.get_setup_tg_auth_bot_data()
  return flask.render_template('auth/login.tmpl',
    PUBLIC_STATIC_URL_PREFIX = env.PUBLIC_STATIC_URL_PREFIX,
    TG_AUTH_BOT_USER_USERNAME = setup_tg_auth_bot_data['USER_USERNAME'],
    HOST = flask.request.host,
    TELEGRAM_AUTH_BYPASS_USER_ID = conf_data['TELEGRAM_AUTH_BYPASS_USER_ID'],
    ERR_MSG = err_msg,
  )

def endpoint_login_telegram_auth_bypass():
  conf_data = env.get_conf_data()
  if not conf_data['TELEGRAM_AUTH_BYPASS_USER_ID']: fk.e400('BOQMQIAV bad TELEGRAM_AUTH_BYPASS_USER_ID')
  TELEGRAM_AUTH_BYPASS_USER_ID = str(conf_data['TELEGRAM_AUTH_BYPASS_USER_ID'])
  flask_login.login_user(User(TELEGRAM_AUTH_BYPASS_USER_ID))
  return fk.redirect('/')

def endpoint_login_telegram_auth_callback():
  check_ret = tg.check_telegram_auth_callback()
  if check_ret != 'OK': return endpoint_login(check_ret)
  tguser_id = flask.request.args.get('id')
  flask_login.login_user(User(tguser_id))
  return fk.redirect('/')

def endpoint_logout():
  flask_login.logout_user()
  return fk.redirect('/')

@flask_login.login_required
def api_get_user():
  user_id = flask_login.current_user.id
  user_item = db_user.get_user(user_id)
  return fk.r200({
    'user_item':user_item
  })

def user_loader(user_id):
  return User(user_id)

def request_loader(request):
  api_token = request.args.get('api_token')
  if api_token == None: return None
  user_item = db_user.get_user_from_api_token(api_token)
  if user_item == None: return None
  user_id = user_item['UserId']
  return User(user_id)

def unauthorized_handler():
  return fk.redirect('/login')

class User(flask_login.mixins.UserMixin):
  def __init__(self,id):
    self.id = id
