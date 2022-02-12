
import traceback
import asyncio
import time
import json
from sqlalchemy.sql.functions import user
from sqlalchemy import insert
import telegram
from datetime import datetime
import pandas as pd
from telegram.update import Update

from global_vars import last_update_telegram_id, sql_connection, last_input_handled, last_update
from sql_utils import db_meta, sql_session, raw_inputs, state_entries
from states_utils import get_head_contex, move_head, resolve_state, get_last_state, run_head, send_output
from telegram_utils import bad_message_reply, bot_reply, bot

async def null_coro():
    pass

async def digest(new_updates):
    print(f'starting to digest {len(new_updates)} update')
    last_update_telegram_id.set(new_updates[-1].input_id)
    for i, update in enumerate(new_updates):
        digest_update(update, name=f'{i+1}:{len(new_updates)}')

def digest_update(update: telegram.Update, name=None):
    input_id = last_update.get() + 1
    insert_values = dict(input_id=input_id,
                         update_telegram_id=update.input_id,
                         content=update.message.text,
                         telegram_json=update.to_json(),
                         recived_datetime=datetime.now(),
                         sent_datetime=None,
                         head_id=update.message.from_user.id)
    stmt = insert(db_meta.tables['raw_inputs']).values(**insert_values)
    result = sql_connection.execute(stmt)
    last_update.set(input_id)
    if name:
        print(f'digested {name}. assigned id: {input_id}')
    else:
        print(f'digested {input_id}')
    



async def handle_all():
    while last_input_handled.get() < last_update.get():
        try:
            handle_input(last_input_handled.get() + 1)
        except Exception as e:
            print(e)
            raise e



def handle_input(input_id):
    print(f'starting to handle {input_id}')
    # retrive data
    input_row = pd.read_sql("select content, head_id from raw_inputs where input_id=?", con=sql_connection, params=(input_id,))
    if input_row.empty: # missing rows in db
        next_input_waiting_tobe_handled = pd.read_sql("select min(input_id) from raw_inputs where input_id>?", con=sql_connection, params=(input_id,)).values[0,0]
        last_input_handled.set(next_input_waiting_tobe_handled - 1)
        return

    input_text = input_row.values[0,0]
    head_id = input_row.values[0,1]
            
    # handle
    head_contex = get_head_contex()
    last_state = get_last_state(head_id)
    new_state, new_output = run_head(head_id, last_state, head_contex, input_text)
    
    send_output(head_id, new_state, new_output)
    move_head(head_id, new_state)
    log_input_as_handled(input_id)
    print(f'finished handling  {input_id}')
    last_input_handled.set(input_id)


def log_new_state(new_state, user_id):
    insert_values = dict(user_id=user_id, state_node_id=new_state,
                         state_entry_datetime=datetime.now())
    stmt = insert(db_meta.tables['state_entries']).values(**insert_values)
    result = sql_connection.execute(stmt)


def log_input_as_handled(input_id):    
    input_row = raw_inputs.query.filter_by(input_id=input_id).first()
    input_row.handled = True
    sql_session.commit()

