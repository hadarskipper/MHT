import os, sys
import pandas as pd
import urllib
import sqlalchemy
from sqlalchemy.types import NVARCHAR

import set_environ

from sql_utils import engine

table_list = [
    'state_nodes',
    'actions'
]


def replace_table_content(table_name, df):
    txt_cols = df.select_dtypes(include = ['object']).columns
    nvarchar_cols = {col_name: NVARCHAR for col_name in txt_cols}
    df.to_sql(con=engine, if_exists='replace', name=table_name, index=False, dtype=nvarchar_cols)

def main():
    for table_name in table_list:
        df = pd.read_csv(os.path.join('db',table_name+'.csv'), )
        replace_table_content(table_name, df)

def load_user_xlsx(file_name):
    user_table_col_rename = {
        'מזהה מצב': 'current_state_node_id',
        'הודעת מצב': 'state_name',
        'תגובה': 'option_name',
        'מצב המשך לפי תגובה': 'end_state_node_id'
    }

    df = pd.read_excel(file_name)
    df = df.rename(columns=user_table_col_rename)

    check_unique = df.groupby('current_state_node_id')['state_name'].nunique()
    check_unique = check_unique.loc[check_unique>1].copy()
    if len(check_unique)>0:
        bad_states = ", ".join([str(state_id) for state_id in check_unique.index])
        raise Exception(f'bad excel state-content. ambiguity of message for states: {bad_states}')

    state_nodes = df.loc[:, ['current_state_node_id', 'state_name']].drop_duplicates()
    state_nodes = state_nodes.rename(columns={'current_state_node_id': 'state_node_id'})
    replace_table_content('state_nodes', state_nodes)

    actions = df.loc[:, ['current_state_node_id','end_state_node_id','option_name']].copy()
    actions.index.name = 'action_id'
    actions = actions.reset_index()
    replace_table_content('actions', actions)

    

if __name__ == '__main__':
    # main()
    load_user_xlsx(sys.argv[1])