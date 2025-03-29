import tweepy
from dotenv import load_dotenv
import os
from utils.logging_utils import log_info, log_error

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_SECRET'))
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_SECRET'))
api = tweepy.API(auth)

def fetch_tweets(query, count=10):
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(count)
        log_info(f"Fetched {count} tweets for query: {query}")
        return [tweet.text for tweet in tweets]
    except Exception as e:
        log_error(f"Error fetching tweets: {e}")
        return []
