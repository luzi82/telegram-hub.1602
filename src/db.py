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

def set_user_role(telegram_user_id, role):
  table = get_table()
  table.update_item(
    Key={
      'HashKey':f'USER {telegram_user_id}',
      'SortKey':'-',
    },
    UpdateExpression='SET UserRole=:user_role,TelegramUserId=:telegram_user_id',
    ExpressionAttributeValues={':user_role':role,':telegram_user_id':telegram_user_id},
  )

def get_hub_list(telegram_user_id):
  table = get_table()
  query_ret = table.query(
    IndexName='IndexHubOwnerTelegramUserId',
    KeyConditionExpression=boto3.dynamodb.conditions.Key('HubOwnerTelegramUserId').eq(telegram_user_id),
  )
  return query_ret['Items']

####################

def get_table():
  dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=env.DYNAMODB_ENDPOINT_URL,
    region_name=env.DYNAMODB_REGION
  )
  table = dynamodb.Table(env.DB_TABLE_NAME)
  return table
