import tweepy
import sqlalchemy
import os
from config_twitter import create_twitter_api
from config_tone import create_ibm_api, tone_data
from datetime import datetime
from dateutil.parser import parse

# create DB connection
MYSQL_PASS = os.environ['MYSQL_PASS']
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{MYSQL_PASS}@localhost/TwitterDB')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# create table objects
user_table = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
tweet_table = sqlalchemy.Table('tweets', metadata, autoload=True, autoload_with=engine)

# create twitter API object
api = create_twitter_api()
# create ibm API client object and endpoint object
tone_analyzer, end_point = create_ibm_api()

# specify query word and tweet amount
while True:
    try:
        the_date = datetime.now()
        specific_date = f'{the_date.year}-{the_date.month}-{the_date.day}'
        search_word = input('Enter your query word: ')
        num_tweets = int(input('Enter the number of tweets you would like returned: '))
        break
    except TypeError:
        print('''
        Looks like you entered an invalid datatype. Try again
        ''')

# get tweets
tweets = tweepy.Cursor(api.search, q=search_word, lang='en', since=specific_date, tweet_mode='extended').items(num_tweets)
tweet_list = []

# loop through tweets data and add tweets to list
for tweet in tweets:
    tweet_list.append(tweet._json)

for tweet in tweet_list:
    # specify insert values for retweets and normal tweets
    if 'retweeted_status' in tweet.keys():
        is_retweet=True
        retweet_truncated=tweet['full_text']
        full_text=tweet['retweeted_status']['full_text']
        tweet_tone = tone_data(tone_analyzer, full_text)
    else:
        is_retweet=False
        retweet_truncated='NONE'
        full_text=tweet['full_text']
        tweet_tone = tone_data(tone_analyzer, full_text)

    # convert created_at strings into Datetime objects
    tweet_creation = parse(tweet['created_at'])
    user_creation = parse(tweet['user']['created_at'])
    
    # error handle duplicate users
    # set up insert queries
    try:
        user_query = sqlalchemy.insert(user_table).values(
            user_id=tweet['user']['id_str'], screen_name=tweet['user']['screen_name'], 
            description=tweet['user']['description'], created_at=user_creation)

        tweet_query = sqlalchemy.insert(tweet_table).values(
            tweet_id=tweet['id_str'], user_id=tweet['user']['id_str'], 
            created_at=tweet_creation, retweet_truncated=retweet_truncated, 
            full_text=full_text, is_retweet=is_retweet, tweet_tone=tweet_tone)

        result_proxy2 = connection.execute(user_query)
        result_proxy1 = connection.execute(tweet_query)

    except sqlalchemy.exc.IntegrityError as ie:
        print(f'''
        Found a user that already exists:
        {ie.orig}
        {ie.params}
        ''')
        pass