from sqlalchemy import create_engine, ForeignKey, MetaData
from sqlalchemy import Column, Date, Integer, String, DATETIME, NVARCHAR, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

import urllib
import os

from sympy import content

ECHO_SQL = False

# server = '127.0.0.1'
# database = 'telegram'

# user = 'sa'
# password = os.environ.get('SA_PASSWORD')


# mssql_db_url_connect = "mssql+pyodbc:///?odbc_connect={}".format(urllib.parse.quote_plus("DRIVER=ODBC Driver 17 for SQL Server;SERVER={0};PORT=1433;DATABASE={1};UID={2};PWD={3};TDS_Version=8.0;charset=utf8".format(server, database, user, password)))
# sqlite_db_file_path = os.path.join(os.getcwd(),'IAF_corona_bot.db')
sqlite_db_file_path = os.path.join(os.getcwd(),'system.db')
sqlite_db_url_connect = f'sqlite:///{sqlite_db_file_path}'
engine = create_engine(sqlite_db_url_connect, echo=ECHO_SQL)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
sql_session = Session()

Base = declarative_base()

class raw_inputs(Base):

    __tablename__ = "raw_inputs"

    input_id = Column(Integer, primary_key=True)
    update_telegram_id = Column(Integer)
    content = Column(NVARCHAR)
    telegram_json = Column(NVARCHAR)
    recived_datetime = Column(DATETIME)
    sent_datetime = Column(DATETIME)
    head_id = Column(Integer)
    handled = Column(BOOLEAN)


class state_entries(Base):

    __tablename__ = "state_entries"

    state_entry_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    state_node_id = Column(Integer)  
    state_entry_datetime = Column(DATETIME)


class state_nodes(Base):

    __tablename__ = "state_nodes"

    state_node_id = Column(Integer, primary_key=True)
    state_name = Column(NVARCHAR)

class actions(Base):

    __tablename__ = "actions"

    action_id = Column(Integer, primary_key=True)
    current_state_node_id = Column(Integer)
    end_state_node_id = Column(Integer)
    action_type  = Column(NVARCHAR)
    action_orders = Column(NVARCHAR)


Base.metadata.create_all(engine)
db_meta = Base.metadata
