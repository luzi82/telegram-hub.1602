import _db_common

import typing

get_table = _db_common.get_table

#   user_id
#   role_id
#   item_id        = f'USER:{user_id}'       # PKeyHash
#   search_role    = f'USER-ROLE:{role_id}'  # SKey0Hash
#   search_api     = f'USER-API:{api_token}' # SKey1Hash

def get_user(user_id: str) -> typing.Dict[str,typing.Any]:
  item_id        = f'USER:{user_id}'       # PKeyHash

  table = get_table()
  query_ret = table.get_item(
    Key={'PKeyHash': item_id,'PKeyRange':'_'},
  )
  return query_ret.get('Item',None) # type: ignore

def is_user_exist(user_id: str) -> bool:
  item_id        = f'USER:{user_id}'       # PKeyHash

  table = get_table()
  query_ret = table.get_item(
    Key={'PKeyHash': item_id,'PKeyRange':'_'},
    ProjectionExpression='PKeyHash',
  )
  if 'Item' not in query_ret: return False
  if query_ret['Item'] == None: return False
  return True

def is_role_exist(role_id: str) -> bool:
  search_role    = f'USER-ROLE:{role_id}'  # SKey0Hash

  table = get_table()
  query_ret = table.query(
    IndexName="SKey0Idx",
    KeyConditionExpression='SKey0Hash=:search_role',
    ExpressionAttributeValues={
      ':search_role': search_role,
    },
    Select='COUNT',
  )
  count = query_ret['Count']
  return count > 0

def new_user(user_id: str, role_id: str, api_token: str) -> None:
  assert(not is_user_exist(user_id))

  item_id        = f'USER:{user_id}'       # PKeyHash
  search_role    = f'USER-ROLE:{role_id}'  # SKey0Hash
  search_api     = f'USER-API:{api_token}' # SKey1Hash

  table = get_table()
  table.update_item(
    Key={'PKeyHash': item_id, 'PKeyRange':'_'},
    UpdateExpression='''SET
      user_id=:user_id,
      role_id=:role_id,
      SKey0Hash=:search_role,
      SKey0Range=:_,
      SKey1Hash=:search_api,
      SKey1Range=:_
    ''',
    ExpressionAttributeValues={
      ':_': '_',
      ':user_id':     user_id,
      ':role_id':     role_id,
      ':search_role': search_role,
      ':search_api':  search_api,
    },
  )

def set_user_role(user_id: str, role_id: str) -> None:
  item_id        = f'USER:{user_id}'       # PKeyHash
  search_role    = f'USER-ROLE:{role_id}'  # SKey0Hash

  table = get_table()
  table.update_item(
    Key={'PKeyHash': item_id, 'PKeyRange':'_'},
    UpdateExpression='SET role_id=:role_id, SKey0Hash=:search_role',
    ExpressionAttributeValues={
      ':role_id':      role_id,
      ':search_role':  search_role,
    },
  )

def set_user_api_token(user_id: str, api_token: str) -> None:
  item_id        = f'USER:{user_id}'       # PKeyHash
  search_api     = f'USER-API:{api_token}' # SKey1Hash

  table = get_table()
  table.update_item(
    Key={'PKeyHash': item_id, 'PKeyRange':'_'},
    UpdateExpression='SET api_token=:api_token,SKey1Hash=:search_api',
    ExpressionAttributeValues={
      ':api_token':   api_token,
      ':search_api':  search_api,
    },
  )

def get_user_from_api_token(api_token: str) -> typing.Dict[str,typing.Any]:
  search_api     = f'USER-API:{api_token}' # SKey1Hash

  table = get_table()
  query_ret = table.query(
    IndexName="SKey1Idx",
    KeyConditionExpression='SKey1Hash=:search_api',
    ExpressionAttributeValues={
      ':search_api': search_api,
    },
    Limit=1,
  )
  item_list = query_ret['Items']
  assert(len(item_list)<=1)
  if (len(item_list)<=0): return None

  item = item_list[0]

  # item only contains 'PKeyHash/Range and SKey1Hash/Range so need to do again'
  query_ret = table.get_item(
    Key={'PKeyHash': item['PKeyHash'],'PKeyRange':'_'},
  )
  return query_ret.get('Item',None) # type: ignore
