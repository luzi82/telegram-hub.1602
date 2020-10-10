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
    if flask.request.form['step'] == 'new_bot': return s00_new_bot_submit()
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
  if setup_done(): return redirect_index()

  # if data bot data already exist, ignore and go back setup
  if futsu.storage.is_blob_exist(env.SETUP_TG_AUTH_BOT_DATA_PATH):
    return fk.redirect('/setup')

  token = flask.request.form['token']

  try:
    # get bot data
    bot = telegram.Bot(token)
    bot_user = bot.get_me()
    setup_auth_bot_tg_data = {
      'token': token,
      'user_id': bot_user.id,
      'username': bot_user.username,
    }
    
    # write bot data
    futsu.json.data_to_path(env.SETUP_TG_AUTH_BOT_DATA_PATH, setup_auth_bot_tg_data)
    
    # redirect setup
    return fk.redirect('/setup')
  except Exception as e:
    traceback.print_exc()
    return s00_new_bot(err_msg=str(e))

def setup_done():
  return futsu.storage.is_blob_exist(env.SETUP_DONE_PATH)

def redirect_index():
  return fk.redirect('/')
