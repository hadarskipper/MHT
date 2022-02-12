import math
import pandas as pd
from sql_utils import engine as sql_connection

ignore_history = True


class module_property_int():
    def __init__(self, init_func=None):
        self._val = None
        self.init_func = init_func
    # getter method
    def get(self):
        if self._val is None:
            self.reset()
        return self._val
    # setter method
    def set(self, x):
        self._val = int(x)
    # reset
    def reset(self):
        self._val = 0
        if self.init_func:
            self._val = int(self.init_func() or 0)


def create_module_property_from_init_func(init_func):
    return module_property_int(init_func)

@create_module_property_from_init_func
def last_update():
    return pd.read_sql("select max(input_id) from raw_inputs", con=sql_connection).values[0,0]


@create_module_property_from_init_func
def last_input_handled():
    return pd.read_sql("select max(input_id) from  raw_inputs where handled", con=sql_connection).values[0,0]


@create_module_property_from_init_func
def last_update_telegram_id():
    df = pd.read_sql("select update_telegram_id from raw_inputs where input_id=?", con=sql_connection, params=(int(last_update.get()),))
    if df.empty:
        return -1
    return df.values[0,0]


actions_df = pd.read_sql("select * from  actions", con=sql_connection)
state_node_df = pd.read_sql("select * from  state_nodes", con=sql_connection)
