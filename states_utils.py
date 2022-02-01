import pandas as pd

from global_vars import options_df, sql_connection

def resolve_state(last_state, message_text):    
    valid_end_state = options_df.loc[
        (options_df['current_state_node_id']==last_state) &
        (options_df['option_name']==message_text)
        , 'end_state_node_id']
    return list(valid_end_state)


def get_last_state(user_id):
    state_history = pd.read_sql("select * from  state_entries where user_id=?", con=sql_connection, params=(user_id,))
    if state_history.empty:
        return 1
    return state_history['state_node_id'].values[-1]
