
import traceback
import asyncio
import time
import json
from sqlalchemy.sql.functions import user
from telegram import KeyboardButton, ReplyKeyboardMarkup, bot
from sqlalchemy import insert
import telegram
from datetime import datetime
import pandas as pd
from telegram.update import Update

from global_vars import last_update_telegram_id, sql_connection, last_update_handled, last_update
from db.sql import db_meta
from states_utils import resolve_state, get_last_state
from telegram_utils import bad_message_reply, bot_reply, bot

async def null_coro():
    pass

async def digest(new_updates):
    print(f'starting to digest {len(new_updates)} update')
    last_update_telegram_id.set(new_updates[-1].update_id)
    for i, update in enumerate(new_updates):
        digest_update(update, name=f'{i+1}:{len(new_updates)}')

def digest_update(update: telegram.Update, name=None):
    update_id = last_update.get() + 1
    insert_values = dict(update_id=update_id,
                         update_telegram_id=update.update_id,
                         content=update.to_json(),
                         recived_datetime=datetime.now(),
                         sent_datetime=None,
                         from_id=update.message.from_user.id)
    stmt = insert(db_meta.tables['raw_updates']).values(**insert_values)
    result = sql_connection.execute(stmt)
    last_update.set(update_id)
    if name:
        print(f'digested {name}. assigned id: {update_id}')
    else:
        print(f'digested {update_id}')
    



async def handle_all():
    while last_update_handled.get() < last_update.get():
        try:
            handle_update(last_update_handled.get() + 1)
        except Exception as e:
            print(e)
            raise e



def handle_update(update_id):
    print(f'starting to handle {update_id}')
    # retrive data
    update_row = pd.read_sql("select content, from_id from dbo.raw_updates where update_id=?", con=sql_connection, params=(update_id,))
    if update_row.empty: # missing rows in db
        next_update_waiting_tobe_handled = pd.read_sql("select min(update_id) from dbo.raw_updates where update_id>?", con=sql_connection, params=(update_id,)).values[0,0]
        last_update_handled.set(next_update_waiting_tobe_handled - 1)
        return
    update = telegram.Update.de_json(bot=bot, data=json.loads(update_row.values[0,0]))
    message_text = update.message.text
    user_id = update_row.values[0,1]
    
    # handle
    last_state = get_last_state(user_id)
    new_state_list = resolve_state(last_state, message_text)
    if len(new_state_list)==1:
        new_state = new_state_list[0]
        bot_reply(new_state, user_id)
        log_new_state(new_state, user_id)
    else:
        bad_message_reply(user_id)
        bot_reply(last_state, user_id)
    log_update_as_handled(update_id)
    print(f'finished handling  {update_id}')
    last_update_handled.set(update_id)


def log_new_state(new_state, user_id):
    insert_values = dict(user_id=user_id, state_node_id=new_state,
                         state_entry_datetime=datetime.now())
    stmt = insert(db_meta.tables['state_entries']).values(**insert_values)
    result = sql_connection.execute(stmt)


def log_update_as_handled(update_id):
    insert_values = dict(update_id=update_id,
                         log='handled',
                         log_code=1,
                         log_datetime=datetime.now())
    stmt = insert(db_meta.tables['update_handle_log']).values(**insert_values)
    result = sql_connection.execute(stmt)

