import boto3
import env

def owner_exist():
  table = get_table()
  query_ret = table.query(
    IndexName='IndexUserRole',
    KeyConditionExpression=boto3.dynamodb.conditions.Key('UserRole').eq('OWNER'),
    Select='COUNT',
  )
  count = query_ret['Count']
  return count > 0


def get_table():
  dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=env.DYNAMODB_ENDPOINT_URL,
    region_name=env.DYNAMODB_REGION
  )
  table = dynamodb.Table(env.DB_TABLE_NAME)
  return table
