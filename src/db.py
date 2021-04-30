import _db_common
import db_spec
import typing
import uuid

get_table = _db_common.get_table

DB_SPEC_DATA = db_spec.DB_SPEC_DATA

def new_item(item_type:str, **kwargs) -> typing.Dict[str,typing.Any]:
  TYPE_DATA = DB_SPEC_DATA['TYPE_DATA_DICT'][item_type]
  INDEX_DATA_LIST = TYPE_DATA['INDEX_DATA_LIST']

  item_uuid = str(uuid.uuid4())

  item_dict = {}
  item_dict.update(kwargs)
  item_dict['TYPEE']=item_type
  for INDEX_DATA in INDEX_DATA_LIST:
    HASH_ATTR_LIST = INDEX_DATA['HASH_ATTR_LIST']
    for HASH_ATTR in HASH_ATTR_LIST:
      if HASH_ATTR not in kwargs: continue
    value = HASH_ATTR_LIST
    value = map(lambda i:kwargs[i], value)
    value = list(value)
    value = [item_type] + value
    value = ':'.join(value)
    item_dict[INDEX_DATA['IDX']+'H'] = value
    item_dict[INDEX_DATA['IDX']+'R'] = '_'

  update_expression = item_dict
  update_expression = [f'{k}=:{k}' for k in item_dict]
  update_expression = ','.join(update_expression)
  update_expression = 'SET '+update_expression

  expression_attribute_values = item_dict
  expression_attribute_values = { f':{k}':v for k,v in item_dict.items()}

  print(update_expression)
  print(expression_attribute_values)

  table = get_table()
  ret = table.update_item(
    Key={'UUIDD': item_uuid},
    UpdateExpression=update_expression,
    ExpressionAttributeValues=expression_attribute_values,
    ReturnValues='ALL_NEW',
  )
  print(ret)

  return ret['Attributes']

def get_item(item_type:str, *args, **kwargs) -> typing.Dict[str,typing.Any]:
  method, query_param_dict = _get_query_method_param_dict(item_type, *args, **kwargs)
  table = get_table()
  if method == 'query': query_param_dict['Limit']=1
  query_ret = getattr(table,method)(
    **query_param_dict
  )
  print(query_ret)
  if 'Items' in query_ret:
    if len(query_ret['Items']) <= 0: return None
    return query_ret['Items'][0]
  if 'Item' in query_ret: return query_ret['Item']
  return None

def get_item_list(item_type:str, *args, **kwargs):
  method, query_param_dict = _get_query_method_param_dict(item_type, *args, **kwargs)
  table = get_table()
  query_ret = getattr(table,method)(**query_param_dict)
  if 'Items' in query_ret: return query_ret['Items']
  if 'Item' in query_ret: return [query_ret['Item']]
  return []

def get_item_count(item_type:str, *args, **kwargs):
  method, query_param_dict = _get_query_method_param_dict(item_type, *args, **kwargs)
  table = get_table()
  query_ret = getattr(table,method)(
    Select='COUNT',
    **query_param_dict
  )
  return query_ret['Count']

def is_item_exist(item_type:str, *args, **kwargs):
  method, query_param_dict = _get_query_method_param_dict(item_type, *args, **kwargs)
  table = get_table()
  query_ret = getattr(table,method)(
    Limit=1,
    ProjectionExpression='UUIDD',
    **query_param_dict
  )
  if 'Items' in query_ret: return len(query_ret['Items'])>0
  if 'Item' in query_ret: return len(query_ret['Item'])!=None
  return False

def rm_item(item_type:str, *args, **kwargs):
  method, query_param_dict = _get_query_method_param_dict(item_type, *args, **kwargs)
  table = get_table()
  if method == 'get_item':
    try:
      delete_item_kwargs = {
        'Key':query_param_dict['Key'],
      }
      if 'FilterExpression' in query_param_dict:
        delete_item_kwargs['ConditionExpression'] = query_param_dict['FilterExpression']
      if 'ExpressionAttributeValues' in query_param_dict:
        delete_item_kwargs['ExpressionAttributeValues'] = query_param_dict['ExpressionAttributeValues']
      table.delete_item(**delete_item_kwargs)
      return True
    except Exception as e:
      if str(type(e)) == "<class 'botocore.errorfactory.ConditionalCheckFailedException'>":
        return False
      raise e
  elif method == 'query':
    query_ret = getattr(table,method)(
      ProjectionExpression='UUIDD',
      **query_param_dict
    )
    if len(query_ret['Items'])<=0:return False
    item_list = query_ret['Items']
    with table.batch_writer() as table_batch:
      for item in item_list:
        table_batch.delete_item(Key=item)
    return True
  assert(False)

def _get_query_method_param_dict(item_type:str, *args, **kwargs):
  ret = __get_query_method_param_dict(item_type, *args, **kwargs)
  print(ret)
  return ret

def __get_query_method_param_dict(item_type:str, *args, **kwargs):
  if len(args)>1:
    assert(False)

  if len(args)==1:
    filter_dict = kwargs

    filter_expression = filter_dict
    filter_expression = map(lambda k:f'{k}=:{k}',filter_expression.keys())
    filter_expression = ' AND '.join(filter_expression)

    expression_attribute_values = filter_dict
    expression_attribute_values = {f':{k}':v for k,v in filter_dict.items()}
    query_param = {
      'Key':{'UUIDD': args[0]},
    }
    if len(filter_expression) > 0: query_param['FilterExpression'] = filter_expression
    if len(expression_attribute_values) > 0: query_param['ExpressionAttributeValues'] = expression_attribute_values
    return 'get_item', query_param

  if len(kwargs)>0:
    TYPE_DATA = DB_SPEC_DATA['TYPE_DATA_DICT'][item_type]
    INDEX_DATA_LIST = TYPE_DATA['INDEX_DATA_LIST']

    best_index_data = None
    best_attr_list_len = 0
    for INDEX_DATA in INDEX_DATA_LIST:
      HASH_ATTR_LIST = INDEX_DATA['HASH_ATTR_LIST']
      if len(HASH_ATTR_LIST) <= best_attr_list_len: continue
      #print(f'GHOMFPXL {HASH_ATTR_LIST}')
      #hash_attr_set = set(HASH_ATTR_LIST)
      all_good = HASH_ATTR_LIST
      all_good = map(lambda i:i in kwargs.keys(),all_good)
      #all_good = list(all_good)
      #print(f'AQRASGPI {all_good}')
      all_good = all(all_good)
      if not all_good: continue
      best_index_data = INDEX_DATA
      best_attr_list_len = len(HASH_ATTR_LIST)

    assert(best_index_data!=None)

    HASH_ATTR_LIST = best_index_data['HASH_ATTR_LIST']

    hash_value = HASH_ATTR_LIST
    hash_value = [kwargs[i] for i in hash_value]
    hash_value = [item_type] + hash_value
    hash_value = ':'.join(hash_value)

    hash_attr_set = set(HASH_ATTR_LIST)
    filter_dict = kwargs.keys() - hash_attr_set
    filter_dict = {k:kwargs[k] for k in filter_dict}

    filter_expression = filter_dict
    filter_expression = map(lambda k:f'{k}=:{k}',filter_expression.keys())
    filter_expression = ' AND '.join(filter_expression)

    expression_attribute_values = filter_dict
    expression_attribute_values = {f':{k}':v for k,v in filter_dict.items()}
    expression_attribute_values[':__IDX_HASH_VALUE'] = hash_value

    query_param = {
      'IndexName':best_index_data['IDX'],
      'KeyConditionExpression':'{k}=:__IDX_HASH_VALUE'.format(k=best_index_data['IDX']+'H'),
      'ExpressionAttributeValues':expression_attribute_values,
    }
    if len(filter_expression) > 0: query_param['FilterExpression'] = filter_expression
    return 'query', query_param

  assert(False)
