import os
from sqlalchemy.sql.operators import op
from telegram import KeyboardButton, ReplyKeyboardMarkup
import telegram

from global_vars import last_update_telegram_id, actions_df, state_node_df

ignore_history = False

bot_token = os.environ.get('bot_token')
bot = telegram.bot.Bot(token=bot_token)

def get_new_updates():
    global ignore_history
    current_updates = bot.get_updates(offset=last_update_telegram_id.get())
    current_updates_id_list = [u.input_id for u in current_updates]
    if ignore_history:
        last_update_telegram_id.set(current_updates_id_list[-1])
        print('IGNORING old updates')
        ignore_history = False
        return []
    if last_update_telegram_id.get() not in current_updates_id_list:
        current_updates.insert(0, None)
        current_updates_id_list.insert(0, last_update_telegram_id.get())
    new_updates = current_updates[current_updates_id_list.index(last_update_telegram_id.get())+1:]
    return new_updates


def bot_reply(state, user_id):
    state_text = state_node_df.loc[state_node_df['state_node_id']==state, 'state_name'].values[0]
    menu = menu_keyboard(actions_df.loc[actions_df['current_state_node_id']==state, 'option_name'])
    bot.send_message(text=state_text, chat_id=user_id, reply_markup=menu)


def bad_message_reply(user_id):
    bot.send_message(text='ההודעה שלך לא הייתה מובנת לי', chat_id=user_id)


def menu_keyboard(option_list):
    return ReplyKeyboardMarkup([[KeyboardButton(o)] for o in option_list])