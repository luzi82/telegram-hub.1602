import datetime
import futsu.storage
import os

STAGE = os.environ['STAGE']
CONF_PATH = os.environ['CONF_PATH']
PUBLIC_STATIC_PATH   = os.environ['PUBLIC_STATIC_PATH']
PUBLIC_MUTABLE_PATH  = os.environ['PUBLIC_MUTABLE_PATH']
PRIVATE_STATIC_PATH  = os.environ['PRIVATE_STATIC_PATH']
PRIVATE_MUTABLE_PATH = os.environ['PRIVATE_MUTABLE_PATH']
DB_TABLE_NAME = os.environ['DB_TABLE_NAME']
DYNAMODB_ENDPOINT_URL = None # TODO for local

def job0(event, context):
  now_ts = int(datetime.datetime.now().timestamp())
  job0_timestamp_path = futsu.storage.join(PRIVATE_MUTABLE_PATH,'job0_timestamp')
  futsu.storage.bytes_to_path(job0_timestamp_path,f'{now_ts}'.encode('utf-8'))
