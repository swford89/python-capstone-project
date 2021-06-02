from datetime import datetime
import sqlalchemy
import tweepy
from dateutil.parser import parse
from config_db import db_connect
from config_twitter import create_twitter_api
from config_tone import create_ibm_api, tone_data

def query_params():
    # specify search arguments for tweepy tweets query
    while True:
        try:
            the_date = datetime.now()
            specific_date = f'{the_date.year}-{the_date.month}-{the_date.day}'
            query = input('Enter your query word: ')
            num_tweets = int(input('Enter the number of tweets you would like returned: '))
            break
        except TypeError:
            print('''
            Looks like you entered an invalid datatype. Try again.
            ''')
    return specific_date, query, num_tweets

# call imported functions: DB, twitter API, tone analyzer client
engine,connection, metadata = db_connect()
api = create_twitter_api()
tone_analyzer, end_point = create_ibm_api()

# create/initialize table objects
user_table = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
tweet_table = sqlalchemy.Table('tweets', metadata, autoload=True, autoload_with=engine)

# get tweets
specific_date, query, num_tweets = query_params()
tweets = tweepy.Cursor(api.search, q=query, lang='en', since=specific_date, tweet_mode='extended', result_type='recent').items(num_tweets)

# loop through tweets data and add tweets to list
tweet_list = [tweet._json for tweet in tweets]

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