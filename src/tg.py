import datetime
import env
import flask
import hashlib
import hmac

from typing import Any

def check_telegram_auth_callback() -> str:
  NOW_TIMESTAMP = datetime.datetime.now().timestamp()

  TELEGRAM_BOT_USER_TOKEN = env.get_setup_tg_auth_bot_data()['USER_TOKEN']

  arg_hash = flask.request.args.get('hash')
  _data_check_str:Any = flask.request.args
  _data_check_str = _data_check_str.items()
  _data_check_str = filter(lambda i:i[0]!='hash',_data_check_str)
  _data_check_str = sorted(_data_check_str)
  _data_check_str = map(lambda i:f"{i[0]}={i[1]}",_data_check_str)
  data_check_str = "\n".join(_data_check_str)
  secret_key_bin = sha256_bin(TELEGRAM_BOT_USER_TOKEN)
  expected_hash_str = hmacsha256_str(secret_key_bin, data_check_str)
  if arg_hash != expected_hash_str:
    return 'ERR_BAD_HASH_CZBKCEQV'

  # check timestamp
  arg_authdate = str(flask.request.args.get('auth_date'))
  arg_authdate_int = int(arg_authdate)
  if abs(arg_authdate_int-NOW_TIMESTAMP) > 10:
    return 'ERR_BAD_TIMESTAMP_JLHIEQCT'

  return 'OK'

def sha256_bin(msg_str:str) -> bytes:
    m = hashlib.sha256()
    m.update(msg_str.encode('utf8'))
    return m.digest()

def hmacsha256_str(key_bin:bytes, msg_str:str) -> str:
    return hmac.new(
        key=key_bin,
        msg=msg_str.encode('utf8'),
        digestmod=hashlib.sha256,
    ).hexdigest()
