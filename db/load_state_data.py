import os, sys
import pandas as pd
import urllib
import sqlalchemy
from sqlalchemy.types import NVARCHAR

sys.path.insert(0, '..')

from db.sql import engine

table_list = [
    'state_nodes',
    'options'
]


def replace_table_content(table_name):
    df = pd.read_csv(os.path.join('db',table_name+'.csv'), )
    txt_cols = df.select_dtypes(include = ['object']).columns
    nvarchar_cols = {col_name: NVARCHAR for col_name in txt_cols}
    df.to_sql(con=engine, if_exists='replace', name=table_name, schema='dbo', index=False, dtype=nvarchar_cols)

def main():
    for table_name in table_list:
        replace_table_content(table_name)

if __name__ == '__main__':
    main()