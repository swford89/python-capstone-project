import os
import sqlalchemy

# create connection to DB to store tweets in
mysql_pass = os.environ['MYSQL_PASS']
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{mysql_pass}@localhost/TwitterDB')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# create tables into which tweets will be stored in DB
user_table = sqlalchemy.Table(
    'users', metadata, 
    sqlalchemy.Column('user_id', sqlalchemy.String(50), primary_key=True),
    sqlalchemy.Column('screen_name', sqlalchemy.String(20)),
    sqlalchemy.Column('description', sqlalchemy.String(500)),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime()),
)

tweet_table = sqlalchemy.Table(
    'tweets', metadata, 
    sqlalchemy.Column('tweet_id', sqlalchemy.String(50), primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.String(50), sqlalchemy.ForeignKey('users.user_id')),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime()),
    sqlalchemy.Column('retweet_truncated', sqlalchemy.String(500)),
    sqlalchemy.Column('full_text', sqlalchemy.String(500)),
    sqlalchemy.Column('is_retweet', sqlalchemy.Boolean()),
    sqlalchemy.Column('tweet_tone', sqlalchemy.String(50))
    )

metadata.create_all(engine)