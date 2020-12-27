import datetime
import db
import fk
import futsu.aws.s3
import futsu.hash
import futsu.storage
import hashlib
import json
import logging
import os
import random
import string
import telegram

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONF_PATH = os.environ['CONF_PATH']

# def listench(chat_id, word_list):
#     now = int(datetime.datetime.now().timestamp())
#     
#     err_msg = 'listench {} <ch_id> <time> <secret>'.format(chat_id)
# 
#     if len(word_list) != 5: return err_msg
#     _, _chat_id, ch_id, ts, _secret = word_list
# 
#     if _chat_id != str(chat_id): return err_msg
# 
#     ts_int = int(ts)
#     if abs(ts_int-now) > 30: return 'XJRZXOMC: BAD time, now={now}'.format(now=now)
#     
#     secret = os.environ.get('TELEGRAM_HUB_SECRET')
#     secret = '{secret},listench,{chat_id},{ch_id},{ts}'.format(
#         chat_id = chat_id,
#         ch_id = ch_id,
#         ts = ts,
#         secret = secret
#     )
#     secret = futsu.hash.sha256_str(secret)
#     if _secret != secret: return 'BAD secret'
# 
#     bucket = os.environ.get('S3_BUCKET')
#     reg_path = 's3://{bucket}/channel_set/{ch_id}/listen_chat_id_set/{chat_id}'.format(
#         bucket = bucket,
#         ch_id = ch_id,
#         chat_id = chat_id,
#     )
#     futsu.storage.bytes_to_path(reg_path, b'')
#     
#     return 'OK'
# 
# def unlistench(chat_id, word_list):
#     now = int(datetime.datetime.now().timestamp())
#     
#     err_msg = 'unlistench {} <ch_id> <time> <secret>'.format(chat_id)
# 
#     if len(word_list) != 5: return err_msg
#     _, _chat_id, ch_id, ts, _secret = word_list
# 
#     if _chat_id != str(chat_id): return err_msg
# 
#     ts_int = int(ts)
#     if abs(ts_int-now) > 30: return 'EOAUNQBF: BAD time, now={ts_int}'.format(ts_int=ts_int)
#     
#     secret = os.environ.get('TELEGRAM_HUB_SECRET')
#     secret = '{secret},unlistench,{chat_id},{ch_id},{ts}'.format(
#         chat_id = chat_id,
#         ch_id = ch_id,
#         ts = ts,
#         secret = secret,
#     )
#     secret = futsu.hash.sha256_str(secret)
#     if _secret != secret: return 'BAD secret'
# 
#     bucket = os.environ.get('S3_BUCKET')
#     reg_path = 's3://{bucket}/channel_set/{ch_id}/listen_chat_id_set/{chat_id}'.format(
#         bucket = bucket,
#         ch_id = ch_id,
#         chat_id = chat_id,
#     )
#     futsu.storage.rm(reg_path)
# 
#     return 'OK'

# def send_msg(input_json):
#     now = datetime.datetime.now().timestamp()
#     input_data = json.loads(input_json)
# 
#     # check input field
#     format_good = True
#     require_field_list = ['src','ch_id','msg','ts','secret']
#     for require_field in require_field_list:
#         if require_field not in input_json:
#             format_good = False
#     if not format_good:
#         return {
#             'result':'ERROR',
#             'err_code':'ZLXQBZIW',
#             'err_msg':'bad format: src, ch_id, msg, ts, secret',
#         }
# 
#     # check ts
#     ts_int = int(input_data['ts'])
#     if abs(ts_int-now) > 10:
#         return {
#             'result':'ERROR',
#             'err_code':'QZDUHQBF',
#             'err_msg':'Bad ts',
#         }
# 
#     # check secret
#     secret = os.environ.get('TELEGRAM_HUB_SECRET')
#     secret = '{ssecret},send_msg_secret,{src},{ch_id}'.format(ssecret=secret,**input_data)
#     secret = futsu.hash.sha256_str(secret)
#     secret = '{ssecret},send_msg,{msg},{ts}'.format(ssecret=secret,**input_data)
#     secret = futsu.hash.sha256_str(secret)
#     if secret != input_data['secret']:
#         return {
#             'result':'ERROR',
#             'err_code':'XDQFLNTE',
#             'err_msg':'bad secret',
#         }
# 
#     # work
#     S3_BUCKET = os.environ.get('S3_BUCKET')
#     chat_id_list = 's3://{S3_BUCKET}/channel_set/{ch_id}/listen_chat_id_set/'.format(
#         S3_BUCKET = S3_BUCKET,
#         ch_id = input_data['ch_id'],
#     )
#     chat_id_list = futsu.storage.find(chat_id_list)
#     chat_id_list = map(lambda i:i.split('/')[-1], chat_id_list)
#     
#     bot = configure_telegram()
#     for chat_id in chat_id_list:
#         bot.sendMessage(chat_id=chat_id, text=input_data['msg'])
# 
#     return {
#         'result':'OK',
#     }

def generate_user_token():
  char_set = string.ascii_letters+string.digits
  return "".join(random.choice(char_set)for x in range(64))

def configure_telegram():
    """
    Configures the bot with a Telegram Token.

    Returns a bot instance.
    """

    #TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    secret_data = futsu.json.path_to_data(futsu.storage.join(CONF_PATH,'secret.json'))
    TELEGRAM_TOKEN = secret_data['TELEGRAM_TOKEN']
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)

# def user_api(f):
#   def ret_f():
#     api_token = flask.request.args.get('api_token')
#     if api_token == None: return fk.e403()
#     user_item = db.get_user_from_api_token(api_token)
#     if user_item == None: return fk.e403()
#     flask.request.th_user_item = user_item
#     return f()
#   return ret_f
