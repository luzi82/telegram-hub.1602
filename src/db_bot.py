import _db_common

get_table = _db_common.get_table

#  user_id
#  bot_tg_id
#  bot_id  = f'{user_id}:{bot_tg_id}'
#  item_id = f'BOT:{bot_id}'          # PKeyHash

def get_bot(bot_id):
  item_id = f'BOT:{bot_id}'
  
  table = get_table()
  query_ret = table.query(
    IndexName='BotIdx',
    KeyConditionExpression='BotId=:bot_id AND ItemId=:item_id',
    ExpressionAttributeValues={
      ':bot_id':  bot_id,
      ':item_id': item_id,
    },
  )
  item_list = query_ret.get('Items',[])
  assert(len(item_list)<=1)
  if len(item_list) != 1: return None
  return item_list[0]

def is_bot_exist(bot_id):
  item_id = f'BOT:{bot_id}'
  
  table = get_table()
  query_ret = table.query(
    IndexName='BotIdx',
    KeyConditionExpression='BotId=:bot_id AND ItemId=:item_id',
    ExpressionAttributeValues={
      ':bot_id':  bot_id,
      ':item_id': item_id,
    },
    Select='COUNT',
  )
  return query_ret['Count'] > 0

def get_bot_list_from_user(user_id):
  table = get_table()
  query_ret = table.query(
    KeyConditionExpression='UserId=:user_id AND begins_with(ItemId,:item_id_prefix)',
    ExpressionAttributeValues={
      ':user_id':        user_id,
      ':item_id_prefix': 'BOT:',
    }
  )
  return query_ret['Items']

def new_bot(user_id, bot_tg_id): # return bot_id
  bot_id  = f'{user_id}:{bot_tg_id}' # BotId
  item_id = f'BOT:{bot_id}'          # ItemId

  assert(not is_bot_exist(bot_id))

  table = get_table()
  table.update_item(
    Key={'UserId': user_id, 'ItemId': item_id},
    UpdateExpression='SET BotId=:bot_id',
    ExpressionAttributeValues={
      ':bot_id': bot_id,
    },
  )
  return bot_id

def rm_bot(bot_id):
  table = get_table()
  query_ret = table.query(
    IndexName='BotIdx',
    KeyConditionExpression='BotId=:bot_id',
    ExpressionAttributeValues={
      ':bot_id':  bot_id,
    },
    ProjectionExpression='UserId, ItemId',
  )
  if 'Items' not in query_ret: return
  item_list = query_ret['Items']
  with table.batch_writer() as table_batch:
    for item in item_list:
      table_batch.delete_item(Key=item)
