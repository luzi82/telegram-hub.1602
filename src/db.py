import boto3
import env

####################
# USER
# HashKey: UserTuid
# Search7: UserRole

def owner_exist():
  table = get_table()
  query_ret = table.query(
    IndexName="IndexSearch7",
    KeyConditionExpression=boto3.dynamodb.conditions.Key('Search7').eq('USER:OWNER'),
    Select='COUNT',
  )
  count = query_ret['Count']
  return count > 0

def set_user_role(user_tuid, user_role):
  table = get_table()
  table.update_item(
    Key={
      'HashKey':f'USER:{user_tuid}',
      'SortKey':'-',
    },
    UpdateExpression='SET UserRole=:user_role,UserTuid=:user_tuid,Search7=:s7',
    ExpressionAttributeValues={
      ':user_role':user_role,
      ':user_tuid':user_tuid,
      ':s7':f'USER:{user_role}',
    },
  )

####################
# HUB
# HashKey: HubId
# Search0: UserTuid

def get_hub_list_from_user(user_tuid):
  table = get_table()
  query_ret = table.query(
    IndexName='IndexSearch0',
    KeyConditionExpression=boto3.dynamodb.conditions.Key('Search0').eq(user_tuid),
  )
  return query_ret['Items']

####################
# common

def get_table():
  dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=env.DYNAMODB_ENDPOINT_URL,
    region_name=env.DYNAMODB_REGION
  )
  table = dynamodb.Table(env.DB_TABLE_NAME)
  return table
