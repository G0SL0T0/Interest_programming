import tweepy
from config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

# Аутентификация
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Сбор твитов
def fetch_tweets(query, count=10):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(count)
    return [tweet.text for tweet in tweets]