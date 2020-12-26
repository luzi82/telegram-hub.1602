import sys
sys.path.append('src')

import db_bot
#import db_chat
#import db_chat_hub
#import db_hub
#import db_hub_publisher
#import db_publisher
import db_user

#########
# USER

assert(not db_user.is_role_exist('VECPFUBZ'))

db_user.new_user('1234','VECPFUBZ','QCLOUEDB')
db_user.set_user_role('1234','VECPFUBZ')
db_user.set_user_api_token('1234','QCLOUEDB')

assert(db_user.is_role_exist('VECPFUBZ'))

user_item = db_user.get_user('1234')
print(user_item)

user_item = db_user.get_user_from_api_token('QCLOUEDB')
assert(user_item['UserId']=='1234')

########
# BOT

db_bot.new_bot('1234', 'DROPYXLW')

bot_item = db_bot.get_bot('1234:DROPYXLW')
print(bot_item)

db_bot.new_bot('1234', 'XXMETXWP')
db_bot.new_bot('1234', 'WLNSRWBL')

bot_item_list = db_bot.get_bot_list_from_user('1234')
assert(len(bot_item_list)==3)

db_bot.rm_bot('1234:XXMETXWP')

bot_item_list = db_bot.get_bot_list_from_user('1234')
assert(len(bot_item_list)==2)

########
# CHAT

db_chat.new_chat('1234:DROPYXLW','MEQWHMSC')

chat_item = db_chat.get_chat('1234:DROPYXLW:MEQWHMSC')
print(f'chat_item = {chat_item}')

db_chat.new_chat('1234:DROPYXLW','FSSMUDAA')
db_chat.new_chat('1234:DROPYXLW','JDGARDNH')

chat_item_list = db_chat.get_chat_list_from_bot('1234:DROPYXLW')
assert(len(chat_item_list)==3)

db_chat.rm_chat('1234:DROPYXLW:FSSMUDAA')

chat_item_list = db_chat.get_chat_list_from_bot('1234:DROPYXLW')
assert(len(bot_item_list)==2)

########
# HUB

db_hub.new_hub('1234','AUDVNEVS')

hub_item = db_hub.get_hub('1234:AUDVNEVS')
print(f'hub_item = {hub_item}')

db_hub.new_hub('1234','CXCXSIJJ')
db_hub.new_hub('1234','PXEOIXAV')

hub_item_list = db_hub.get_hub_list_from_user('1234')
assert(len(hub_item_list)==3)

db_hub.rm_hub('1234:CXCXSIJJ')

hub_item_list = db_hub.get_hub_list_from_user('1234')
assert(len(hub_item_list)==2)

########
# PUBLISHER

db_publisher.new_publisher('1234','XLZCXHXF')

publisher_item = db_publisher.get_publisher('1234:XLZCXHXF')
print(f'publisher_item = {publisher_item}')

db_publisher.new_publisher('1234','DHVCVRWG')
db_publisher.new_publisher('1234','MJUXIKII')

publisher_item_list = db_publisher.get_publisher_list_from_user('1234')
assert(len(publisher_item_list)==3)

db_publisher.rm_publisher('1234:DHVCVRWG')

publisher_item_list = db_publisher.get_publisher_list_from_user('1234')
assert(len(publisher_item_list)==2)

########
# CHAT-HUB

db_chat_hub.set_chat_hub('1234','1234:DROPYXLW','1234:AUDVNEVS')

chat_hub_item = db_chat_hub.get_chat_hub('1234:1234:DROPYXLW:1234:AUDVNEVS')
print(f'chat_hub_item = {chat_hub_item}')

db_chat_hub.get_chat_hub_list_from_chat('1234:DROPYXLW')
db_chat_hub.get_chat_hub_list_from_hub('1234:AUDVNEVS')

db_chat_hub.set_chat_hub('1234','1234:DROPYXLW','1234:PXEOIXAV')
db_chat_hub.rm_chat_hub('1234:1234:DROPYXLW:1234:PXEOIXAV')

########
# HUB-PUBLISHER

db_hub_publisher.set_hub_publisher('1234','1234:AUDVNEVS','1234:XLZCXHXF')

hub_publisher_item = db_hub_publisher.get_hub_publisher('1234:1234:AUDVNEVS:1234:XLZCXHXF')
print(f'hub_publisher_item = {hub_publisher_item}')

db_hub_publisher.get_hub_publisher_list_from_hub('1234:AUDVNEVS')
db_hub_publisher.get_hub_publisher_list_from_publisher('1234:XLZCXHXF')

db_hub_publisher.set_hub_publisher('1234','1234:AUDVNEVS','1234:MJUXIKII')
db_hub_publisher.rm_hub_publisher('1234:1234:AUDVNEVS:1234:MJUXIKII')
