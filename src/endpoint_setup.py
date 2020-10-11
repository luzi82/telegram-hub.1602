import db
import env
import fk
import flask
import futsu.json
import futsu.storage
import logging
import telegram
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def add_url_rule(app):
  #def i(a,b):
  #  app.add_url_rule(a, b, locals()[b])
  #i('/setup', 'endpoint_setup')
  #i('/setup/new_bot_done', 'endpoint_s00_new_bot_done')
  app.add_url_rule('/setup', 'endpoint_setup', endpoint_setup,  methods=['GET','POST'])

def endpoint_setup():
  logger.info(f'KHSFBKKL endpoint_setup')
  if setup_done(): return redirect_index()

  if flask.request.method == 'POST':
    step = flask.request.form['step']
    if step == 'new_bot': return s00_new_bot_submit()
    if step == 'new_bot_clean': return s00_new_bot_clean()
    if step == 'bot_set_domain': return s01_bot_set_domain_submit()
    if step == 'bot_set_domain_clean': return s01_bot_set_domain_clean()
    return fk.e400('UHBYLYQC step unknown')

  if not futsu.storage.is_blob_exist(env.SETUP_TG_AUTH_BOT_DATA_PATH):
    return s00_new_bot()

  if not futsu.storage.is_blob_exist(env.SETUP_SET_DOMAIN_DONE_PATH):
    return s01_bot_set_domain()

  if not db.owner_exist():
    return s02_th_owner_login()

  futsu.storage.bytes_to_path(env.SETUP_DONE_PATH,b'')
  return s99_done()

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
    futsu.json.bytes_to_path(env.SETUP_TG_AUTH_BOT_DATA_PATH, setup_tg_auth_bot_data)
    
    # redirect setup
    return fk.redirect('/setup')
  except Exception as e:
    traceback.print_exc()
    return s00_new_bot(err_msg=str(e))

def s00_new_bot_clean():
  futsu.storage.rm(env.SETUP_TG_AUTH_BOT_DATA_PATH)
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


def s02_th_owner_login():
  setup_tg_auth_bot_data = futsu.json.path_to_data(env.SETUP_TG_AUTH_BOT_DATA_PATH)
  return flask.render_template('setup/s02_th_owner_login.tmpl',
    PUBLIC_STATIC_HTTP_PATH = env.PUBLIC_STATIC_HTTP_PATH,
    TG_AUTH_BOT_USER_USERNAME = setup_tg_auth_bot_data['USER_USERNAME'],
    HOST = flask.request.host,
  )


def setup_done():
  return futsu.storage.is_blob_exist(env.SETUP_DONE_PATH)

def redirect_index():
  return fk.redirect('/')
