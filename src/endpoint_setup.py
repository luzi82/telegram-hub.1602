import db
import env
import fk
import flask
import futsu.json
import futsu.storage
import logging
import telegram
import tg
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def add_url_rule(app):
  app.add_url_rule('/setup', 'endpoint_setup', endpoint_setup,  methods=['GET','POST'])
  app.add_url_rule('/setup/telegram-auth-callback', 'endpoint_setup_telegram_auth_callback', endpoint_setup_telegram_auth_callback,  methods=['GET','POST'])

def endpoint_setup():
  logger.info(f'KHSFBKKL endpoint_setup')
  if is_setup_done(): return redirect_index()

  if flask.request.method == 'POST':
    step = flask.request.form['step']
    if step == 'new_bot': return s00_new_bot_submit()
    if step == 'new_bot_clean': return s00_new_bot_clean()
    if step == 'bot_set_domain': return s01_bot_set_domain_submit()
    if step == 'bot_set_domain_clean': return s01_bot_set_domain_clean()
    if step == 'th_owner_login_telegram_auth_bypass': return s02_th_owner_login_telegram_auth_bypass()
    return fk.e400('UHBYLYQC step unknown')

  if not futsu.storage.is_blob_exist(env.SETUP_TG_AUTH_BOT_DATA_PATH):
    return s00_new_bot()

  if not futsu.storage.is_blob_exist(env.SETUP_SET_DOMAIN_DONE_PATH):
    return s01_bot_set_domain()

  if not db.is_role_exist('OWNER'):
    return s02_th_owner_login()

  futsu.storage.bytes_to_path(env.SETUP_DONE_PATH,b'')
  return s99_done()

def endpoint_setup_telegram_auth_callback():
  logger.info(f'YBWLYHDB endpoint_setup_telegram_auth_callback')
  if is_setup_done(): return redirect_index()
  return s02_th_owner_login_telegram_auth_callback()

def s00_new_bot(err_msg=None):
  return flask.render_template('setup/s00_new_bot.tmpl',
    PUBLIC_STATIC_HTTP_PATH = env.PUBLIC_STATIC_HTTP_PATH,
    ERR_MSG = err_msg,
  )

def s00_new_bot_submit():
  # if data bot data already exist, ignore and go back setup
  if futsu.storage.is_blob_exist(env.SETUP_TG_AUTH_BOT_DATA_PATH):
    return fk.redirect('/setup')

  token = flask.request.form['token']

  try:
    # get bot data
    bot = telegram.Bot(token)
    bot_user = bot.get_me()
    setup_tg_auth_bot_data = {
      'USER_TOKEN': token,
      'USER_ID': bot_user.id,
      'USER_USERNAME': bot_user.username,
    }
    
    # write bot data
    futsu.json.data_to_path(env.SETUP_TG_AUTH_BOT_DATA_PATH, setup_tg_auth_bot_data)
    
    # redirect setup
    return fk.redirect('/setup')
  except Exception as e:
    traceback.print_exc()
    return s00_new_bot(err_msg=str(e))

def s00_new_bot_clean():
  futsu.storage.rm(env.SETUP_TG_AUTH_BOT_DATA_PATH)
  futsu.storage.rm(env.SETUP_SET_DOMAIN_DONE_PATH)
  return fk.redirect('/setup')


def s01_bot_set_domain():
  setup_tg_auth_bot_data = futsu.json.path_to_data(env.SETUP_TG_AUTH_BOT_DATA_PATH)
  return flask.render_template('setup/s01_bot_set_domain.tmpl',
    PUBLIC_STATIC_HTTP_PATH = env.PUBLIC_STATIC_HTTP_PATH,
    TG_AUTH_BOT_USER_USERNAME = setup_tg_auth_bot_data['USER_USERNAME'],
    HOST = flask.request.host,
  )

def s01_bot_set_domain_submit():
  futsu.storage.bytes_to_path(env.SETUP_SET_DOMAIN_DONE_PATH, b'')
  return fk.redirect('/setup')

def s01_bot_set_domain_clean():
  futsu.storage.rm(env.SETUP_SET_DOMAIN_DONE_PATH)
  return fk.redirect('/setup')


def s02_th_owner_login(err_msg=None):
  conf_data = env.get_conf_data()
  setup_tg_auth_bot_data = futsu.json.path_to_data(env.SETUP_TG_AUTH_BOT_DATA_PATH)
  return flask.render_template('setup/s02_th_owner_login.tmpl',
    PUBLIC_STATIC_HTTP_PATH = env.PUBLIC_STATIC_HTTP_PATH,
    TG_AUTH_BOT_USER_USERNAME = setup_tg_auth_bot_data['USER_USERNAME'],
    HOST = flask.request.host,
    TELEGRAM_AUTH_BYPASS_USER_ID = conf_data['TELEGRAM_AUTH_BYPASS_USER_ID'],
    ERR_MSG = err_msg,
  )

def s02_th_owner_login_telegram_auth_bypass():
  conf_data = env.get_conf_data()
  if not conf_data['TELEGRAM_AUTH_BYPASS_USER_ID']: fk.e400('CAYIGVGS bad TELEGRAM_AUTH_BYPASS_USER_ID')
  db.set_user_role(str(conf_data['TELEGRAM_AUTH_BYPASS_USER_ID']), 'OWNER')
  return fk.redirect('/setup')

def s02_th_owner_login_telegram_auth_callback():
  check_ret = tg.check_telegram_auth_callback()
  if check_ret != 'OK': return s02_th_owner_login(check_ret)
  tguser_id = flask.request.args.get('id')
  db.set_user_role(tguser_id, 'OWNER')
  db_set_user_api_token(tguser_id, th.generate_user_token())
  return fk.redirect('/setup')


def s99_done():
  return flask.render_template('setup/s99_done.tmpl')


def is_setup_done():
  return futsu.storage.is_blob_exist(env.SETUP_DONE_PATH)

def redirect_index():
  return fk.redirect('/')
