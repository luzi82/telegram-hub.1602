import boto3 # type: ignore
import env

_get_table_ret = None
def get_table():
  global _get_table_ret
  if _get_table_ret: return _get_table_ret
  dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=env.DYNAMODB_ENDPOINT_URL,
    region_name=env.DYNAMODB_REGION
  )
  table = dynamodb.Table(env.DB_TABLE_NAME)
  _get_table_ret = table
  return _get_table_ret
