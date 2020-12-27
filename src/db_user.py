import _db_common

get_table = _db_common.get_table

#  user_id        = user_tg_id              # UserId
#  item_id        = f'USER:{user_id}'       # ItemId
#  search_0_hash  = f'USER-ROLE:{role_id}'  # Search0Hash
#  search_0_range = item_id                 # Search0Range
#  search_1_hash  = f'USER-API:{api_token}' # Search1Hash
#  search_1_range = item_id                 # Search1Range

def get_user(user_id: str) -> dict:
  item_id        = f'USER:{user_id}'       # ItemId

  table = get_table()
  query_ret = table.get_item(
    Key={'UserId': user_id, 'ItemId': item_id},
  )
  return query_ret.get('Item',None)

def is_user_exist(user_id: str) -> bool:
  item_id        = f'USER:{user_id}'       # ItemId

  table = get_table()
  query_ret = table.get_item(
    Key={'UserId': user_id, 'ItemId': item_id},
    ProjectionExpression='ItemId',
  )
  if 'Item' not in query_ret: return False
  if query_ret['Item'] == None: return False
  return True

def is_role_exist(role_id: str) -> bool:
  search_0_hash  = f'USER-ROLE:{role_id}' # Search0Hash 

  table = get_table()
  query_ret = table.query(
    IndexName="Search0Idx",
    KeyConditionExpression='Search0Hash=:search_0_hash',
    ExpressionAttributeValues={
      ':search_0_hash': search_0_hash,
    },
    Select='COUNT',
  )
  count = query_ret['Count']
  return count > 0

def new_user(user_id: str, role_id: str, api_token: str) -> None:
  assert(not is_user_exist(user_id))

  item_id        = f'USER:{user_id}'       # ItemId
  search_0_hash  = f'USER-ROLE:{role_id}'  # Search0Hash
  search_0_range = item_id                 # Search0Range
  search_1_hash  = f'USER-API:{api_token}' # Search1Hash
  search_1_range = item_id                 # Search1Range

  table = get_table()
  table.update_item(
    Key={'UserId': user_id, 'ItemId': item_id},
    UpdateExpression='''SET
      RoleId=:role_id,     Search0Hash=:search_0_hash, Search0Range=:search_0_range,
      ApiToken=:api_token, Search1Hash=:search_1_hash, Search1Range=:search_1_range
    ''',
    ExpressionAttributeValues={
      ':role_id':        role_id,
      ':search_0_hash':  search_0_hash,
      ':search_0_range': search_0_range,
      ':api_token':      api_token,
      ':search_1_hash':  search_1_hash,
      ':search_1_range': search_1_range,
    },
  )

def set_user_role(user_id: str, role_id: str) -> None:
  item_id        = f'USER:{user_id}'      # ItemId
  search_0_hash  = f'USER-ROLE:{role_id}' # Search0Hash
  search_0_range = item_id                # Search0Range

  table = get_table()
  table.update_item(
    Key={'UserId': user_id, 'ItemId': item_id},
    UpdateExpression='SET RoleId=:role_id,Search0Hash=:search_0_hash,Search0Range=:search_0_range',
    ExpressionAttributeValues={
      ':role_id':        role_id,
      ':search_0_hash':  search_0_hash,
      ':search_0_range': search_0_range,
    },
  )

def set_user_api_token(user_id: str, api_token: str) -> None:
  item_id        = f'USER:{user_id}'       # ItemId
  search_1_hash  = f'USER-API:{api_token}' # Search1Hash
  search_1_range = item_id                 # Search1Range

  table = get_table()
  table.update_item(
    Key={'UserId': user_id, 'ItemId': item_id},
    UpdateExpression='SET ApiToken=:api_token,Search1Hash=:search_1_hash,Search1Range=:search_1_range',
    ExpressionAttributeValues={
      ':api_token':      api_token,
      ':search_1_hash':  search_1_hash,
      ':search_1_range': search_1_range,
    },
  )

def get_user_from_api_token(api_token: str) -> str:
  search_1_hash  = f'USER-API:{api_token}' # Search1Hash

  table = get_table()
  query_ret = table.query(
    IndexName="Search1Idx",
    KeyConditionExpression='Search1Hash=:search_1_hash',
    ExpressionAttributeValues={
      ':search_1_hash': search_1_hash,
    },
  )
  item_list = query_ret['Items']
  assert(len(item_list)<=1)
  return item_list[0] if len(item_list) == 1 else None
