from sqlalchemy import create_engine, MetaData
import urllib
import os

server = '127.0.0.1'
database = 'telegram'

user = 'sa'
password = os.environ.get('SA_PASSWORD')


db_url_connect = "mssql+pyodbc:///?odbc_connect={}".format(urllib.parse.quote_plus("DRIVER=ODBC Driver 17 for SQL Server;SERVER={0};PORT=1433;DATABASE={1};UID={2};PWD={3};TDS_Version=8.0;charset=utf8".format(server, database, user, password)))
engine = create_engine(db_url_connect)

db_meta = MetaData()
db_meta.reflect(engine)
