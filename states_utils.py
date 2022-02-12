from matplotlib.style import available
import pandas as pd

from global_vars import actions_df, sql_connection
from sql_utils import actions, sql_session

def resolve_state(last_state, message_text):    
    valid_end_state = actions_df.loc[
        (actions_df['current_state_node_id']==last_state) &
        (actions_df['option_name']==message_text)
        , 'end_state_node_id']
    return list(valid_end_state)


def get_last_state(head_id):
    state_history = pd.read_sql("select * from  state_entries where user_id=?", con=sql_connection, params=(head_id,))
    if state_history.empty:
        return 1
    return state_history['state_node_id'].values[-1]

def get_head_contex(head_id):
    return None

def run_head(head_id, last_state, head_contex, input_text):
    query = sql_session.query(actions).filter(actions.current_state_node_id == last_state)
    actions_df = pd.read_sql(query.statement, query.session.bind)
    valid_end_state = actions_df.loc[
        (actions_df['current_state_node_id']==last_state) &
        (actions_df['option_name']==input_text)
        , 'end_state_node_id']
    valid_end_state = list(valid_end_state)
    if len(valid_end_state)==1:
        return valid_end_state[0], 'found new state!'
    else:
        raise RuntimeError('multiple actions available')



def send_output(head_id, new_output):
    pass
    
def move_head(head_id, new_state):
    pass
