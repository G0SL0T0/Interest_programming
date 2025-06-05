import tweepy
import praw
import vk_api
import instaloader
from googleapiclient.discovery import build
from textblob import TextBlob
import matplotlib.pyplot as plt
import time

# Twitter функции
twitter_auth = tweepy.OAuthHandler('TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET')
twitter_auth.set_access_token('TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET')
twitter_api = tweepy.API(twitter_auth)

# Reddit функция
reddit = praw.Reddit(
    client_id='REDDIT_CLIENT_ID',
    client_secret='REDDIT_CLIENT_SECRET',
    user_agent='REDDIT_USER_AGENT'
)

# Настройки для VK
vk_session = vk_api.VkApi(token='VK_ACCESS_TOKEN')
vk_api = vk_session.get_api()

# Настройки для Instagram
instagram_loader = instaloader.Instaloader()

# Настройки для YouTube
youtube_api_key = 'YOUTUBE_API_KEY'
youtube_service = build('youtube', 'v3', developerKey=youtube_api_key)

# Функция для анализа настроений
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Сбор данных из Twitter
def fetch_tweets(query, count=10):
    tweets = tweepy.Cursor(twitter_api.search_tweets, q=query, lang="en").items(count)
    return [tweet.text for tweet in tweets]

# Сбор данных из Reddit
def fetch_reddit_posts(query, count=10):
    posts = reddit.subreddit('all').search(query, limit=count)
    return [post.title for post in posts]

# Сбор данных из VK
def fetch_vk_posts(query, count=10):
    posts = vk_api.wall.search(q=query, count=count)
    return [post['text'] for post in posts['items']]

# Сбор данных из Instagram
def fetch_instagram_posts(query, count=10):
    posts = instagram_loader.get_hashtag_posts(query)
    return [post.caption for post in posts[:count]]

# Сбор данных (комментарии)
def fetch_youtube_comments(video_id, count=10):
    comments = youtube_service.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=count,
        textFormat="plainText"
    ).execute()
    return [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in comments['items']]

# Основной цикл
if __name__ == "__main__":
    platforms = {
        "Twitter": fetch_tweets,
        "Reddit": fetch_reddit_posts,
        "VK": fetch_vk_posts,
        "Instagram": fetch_instagram_posts,
        "YouTube": fetch_youtube_comments
    }

    query = "Python"
    sentiments = []

    while True:
        for platform_name, fetch_function in platforms.items():
            print(f"Fetching data from {platform_name}...")
            try:
                if platform_name == "YouTube":
                    data = fetch_function("VIDEO_ID")  # ID видео
                else:
                    data = fetch_function(query)
                for text in data:
                    sentiment = analyze_sentiment(text)
                    sentiments.append(sentiment)
                    print(f"Platform: {platform_name}\nText: {text}\nSentiment: {sentiment}\n")
            except Exception as e:
                print(f"Error fetching data from {platform_name}: {e}")

        # Визуализация
        plt.plot(sentiments, marker='o')
        plt.title('Sentiment Analysis over Time')
        plt.xlabel('Data Point Index')
        plt.ylabel('Sentiment Polarity')
        plt.show()

        time.sleep(60)  # Обновляем каждую минуту
