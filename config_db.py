import os
import sqlalchemy

def db_connect():
    # create DB connection
    MYSQL_PASS = os.environ['MYSQL_PASS']
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{MYSQL_PASS}@localhost/TwitterDB')
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    return engine, connection, metadata