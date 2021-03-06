import functools
import futsu.json # type: ignore
import futsu.storage # type: ignore
import os
import telegram
import typing

STAGE = os.environ['STAGE']
CONF_PATH = os.environ['CONF_PATH']
PUBLIC_STATIC_PATH       = os.environ['PUBLIC_STATIC_PATH']
PUBLIC_MUTABLE_PATH      = os.environ['PUBLIC_MUTABLE_PATH']
PUBLIC_STATIC_URL_PREFIX  = os.environ['PUBLIC_STATIC_URL_PREFIX']
PUBLIC_MUTABLE_URL_PREFIX = os.environ['PUBLIC_MUTABLE_URL_PREFIX']
PRIVATE_STATIC_PATH      = os.environ['PRIVATE_STATIC_PATH']
PRIVATE_MUTABLE_PATH     = os.environ['PRIVATE_MUTABLE_PATH']
DB_TABLE_NAME            = os.environ['DB_TABLE_NAME']
DYNAMODB_ENDPOINT_URL    = os.environ.get('DYNAMODB_ENDPOINT_URL',None)
DYNAMODB_REGION          = os.environ.get('DYNAMODB_REGION',None)

VERSION = 'v1602327422'

PRIVATE_MUTABLE_VERSION_PATH = futsu.storage.join(PRIVATE_MUTABLE_PATH,VERSION)

SETUP_TG_AUTH_BOT_DATA_PATH = futsu.storage.join(PRIVATE_MUTABLE_VERSION_PATH,'SETUP','TG_AUTH_BOT_DATA.json')
SETUP_SET_DOMAIN_DONE_PATH = futsu.storage.join(PRIVATE_MUTABLE_VERSION_PATH,'SETUP','SET_DOMAIN_DONE')
SETUP_DONE_PATH = futsu.storage.join(PRIVATE_MUTABLE_VERSION_PATH,'SETUP','DONE')

SECRET_CONF_PATH = futsu.storage.join(CONF_PATH,'secret.json')

@functools.lru_cache(maxsize=1)
def get_conf_data() -> typing.Dict[str,typing.Any]:
  conf_data:typing.Dict[str,typing.Any] = futsu.json.path_to_data(futsu.storage.join(CONF_PATH,'conf.json'))
  if futsu.storage.is_blob_exist(SECRET_CONF_PATH):
    secret_data = futsu.json.path_to_data(SECRET_CONF_PATH)
    conf_data.update(secret_data)

  if 'TELEGRAM_AUTH_BYPASS_USER_ID' not in conf_data:
    conf_data['TELEGRAM_AUTH_BYPASS_USER_ID'] = None

  return conf_data

@functools.lru_cache(maxsize=1)
def get_setup_tg_auth_bot_data() -> typing.Dict[str,typing.Any]:
  ret:typing.Dict[str,typing.Any] = futsu.json.path_to_data(SETUP_TG_AUTH_BOT_DATA_PATH)
  return ret

def get_telegram_bot() -> telegram.Bot:
  setup_tg_auth_bot_data = get_setup_tg_auth_bot_data()
  token = setup_tg_auth_bot_data['USER_TOKEN']
  bot = telegram.Bot(token)
  return bot
