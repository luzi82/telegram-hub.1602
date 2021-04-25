import boto3 # type: ignore
import env

from typing import Any

_get_table_ret:Any = None
def get_table() -> Any:
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
