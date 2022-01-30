import math
import pandas as pd
from db.sql import engine as sql_connection

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
    return pd.read_sql("select max(update_id) from dbo.raw_updates", con=sql_connection).values[0,0]


@create_module_property_from_init_func
def last_update_handled():
    return pd.read_sql("select max(update_id) from dbo.update_handle_log where log='handled'", con=sql_connection).values[0,0]


@create_module_property_from_init_func
def last_update_telegram_id():
    df = pd.read_sql("select update_telegram_id from dbo.raw_updates where update_id=?", con=sql_connection, params=(int(last_update.get()),))
    if df.empty:
        return -1
    return df.values[0,0]


options_df = pd.read_sql("select * from dbo.options", con=sql_connection)
state_node_df = pd.read_sql("select * from dbo.state_nodes", con=sql_connection)
