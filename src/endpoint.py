import boto3
import datetime
import flask
import fk
import futsu.json
import futsu.storage
import logging
import os
import random
import telegram
import th

STAGE = os.environ['STAGE']
CONF_PATH = os.environ['CONF_PATH']

PUBLIC_STATIC_PATH   = os.environ['PUBLIC_STATIC_PATH']
PUBLIC_MUTABLE_PATH  = os.environ['PUBLIC_MUTABLE_PATH']
PRIVATE_STATIC_PATH  = os.environ['PRIVATE_STATIC_PATH']
PRIVATE_MUTABLE_PATH = os.environ['PRIVATE_MUTABLE_PATH']
DB_TABLE_NAME = os.environ['DB_TABLE_NAME']
DYNAMODB_ENDPOINT_URL = os.environ.get('DYNAMODB_ENDPOINT_URL',None)
DYNAMODB_REGION       = os.environ.get('DYNAMODB_REGION',None)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

configure_telegram = th.configure_telegram

app = flask.Flask(__name__)

@app.route('/')
def index():
    now_ts = int(datetime.datetime.now().timestamp())

    private_dummy_path = futsu.storage.join(PRIVATE_STATIC_PATH,'private.txt')
    private_txt = futsu.storage.path_to_bytes(private_dummy_path).decode('utf-8')

    timestamp_path = futsu.storage.join(PRIVATE_MUTABLE_PATH,'timestamp')
    last_ts = futsu.storage.path_to_bytes(timestamp_path).decode('utf-8') if futsu.storage.is_blob_exist(timestamp_path) else -1
    futsu.storage.bytes_to_path(timestamp_path,f'{now_ts}'.encode('utf-8'))

    job0_timestamp_path = futsu.storage.join(PRIVATE_MUTABLE_PATH,'job0_timestamp')
    job0_ts = futsu.storage.path_to_bytes(job0_timestamp_path).decode('utf-8') if futsu.storage.is_blob_exist(job0_timestamp_path) else -1

    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL, region_name=DYNAMODB_REGION)
    table = dynamodb.Table(DB_TABLE_NAME)
    query_ret = table.query(
      KeyConditionExpression=boto3.dynamodb.conditions.Key('HashKey').eq('rand_txt'),
      Limit=1,
    )
    now_rand = str(random.randrange(100))
    last_rand = query_ret['Items'][0]['Valuee'] if len(query_ret['Items'])>0 else ''
    table.update_item(
      Key={'HashKey':'rand_txt','SortKey':0},
      UpdateExpression='SET Valuee = :v',
      ExpressionAttributeValues={':v':now_rand},
    )

    return flask.render_template('index.tmpl',
        STAGE=STAGE,
        PRIVATE_TXT=private_txt,
        LAST_TS=last_ts,
        NOW_TS=now_ts,
        JOB0_TS=job0_ts,
        LAST_RAND=last_rand,
        NOW_RAND=now_rand,
    )

@app.route('/compute_domain')
def get_compute_domain():
    conf_data = futsu.json.path_to_data(futsu.storage.join(CONF_PATH,'conf.json'))
    return conf_data['COMPUTE_DOMAIN']


@app.route('/telegram/webhook', methods=['POST'])
def post_webhook():
    now = int(datetime.datetime.now().timestamp())

    # event = flask.request.get_json()
    # logger.info(f'Event: {event}')

    bot = configure_telegram()

    # logger.info('JGSQVFPC')
    # if event.get('body') is None:
    #     return fk.e400('NXDQNYUR require body')

    logger.info('RMYYLVSD')
    body_data = flask.request.get_json()
    logger.info(f'body_data: {body_data}')
    if 'message' not in body_data:
        return fk.e400('FEHPCSGD require body.message')
    if 'date' not in body_data['message']:
        return fk.e400('WGQWMYUR require body.date')

    logger.info('LFLCITSK')
    ts_int = int(body_data['message']['date'])
    ts_diff = abs(ts_int-now)
    logger.info('MOSUOFFJ now={now}, ts_int={ts_int}, ts_diff={ts_diff}'.format(
        now=now,
        ts_int=ts_int,
        ts_diff=ts_diff,
    ))
    if abs(ts_int-now) > 30:
        logger.info('AUKKICOG ignore timeout')
        return fk.r200('TIMEOUT') # avoid telegram webhook loop

    update = telegram.Update.de_json(body_data, bot)
    chat_id = update.message.chat.id
    text = update.message.text

    word_list = text.split(' ')
    word_list = filter(lambda i:len(i)>0, word_list)
    word_list = list(word_list)

    ret_text = None
    if word_list[0] == '/start':
        ret_text = "Hello from telegram-hub.1602"

    if ret_text is not None:
        bot.sendMessage(chat_id=chat_id, text=ret_text)
        logger.info('Message sent')

    return fk.r200()


# TODO: remove me
@app.route('/set_webhook')
def get_setwebhook():
    host = flask.request.host
    bot = configure_telegram()
    url = f'https://{host}/telegram/webhook'
    logger.info(f'FZKSPASM URL: {url}')
    set_webhook_result = bot.set_webhook(url, timeout=30)

    if set_webhook_result:
        return fk.r200({'set_webhook_result':set_webhook_result})

    return fk.e500({'set_webhook_result':set_webhook_result})
