import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import time

# Настройки для Twitter API
consumer_key = 'KEY'
consumer_secret = 'SECRET'
access_token = 'TOKEN'
access_token_secret = 'TOKEN_SECRET'

# Аутентификация
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Функция для анализа настроений
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Сбор и анализ твитов
def fetch_and_analyze_tweets(query, count=10):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(count)
    sentiments = []
    for tweet in tweets:
        sentiment = analyze_sentiment(tweet.text)
        sentiments.append(sentiment)
        print(f"Tweet: {tweet.text}\nSentiment: {sentiment}\n")
    return sentiments

# Визуализация результатов
def plot_sentiments(sentiments):
    plt.plot(sentiments, marker='o')
    plt.title('Sentiment Analysis over Time')
    plt.xlabel('Tweet Index')
    plt.ylabel('Sentiment Polarity')
    plt.show()

# Основной цикл
if __name__ == "__main__":
    query = "Python"
    while True:
        sentiments = fetch_and_analyze_tweets(query)
        plot_sentiments(sentiments)
        time.sleep(60)  # Обновляем каждую минуту