from data_fetchers.twitter_fetcher import fetch_tweets
from data_fetchers.reddit_fetcher import fetch_reddit_posts
from data_fetchers.vk_fetcher import fetch_vk_posts
from data_fetchers.instagram_fetcher import fetch_instagram_posts
from data_fetchers.youtube_fetcher import fetch_youtube_comments
from analysis.sentiment_analysis import analyze_sentiment
from analysis.trend_analysis import analyze_trends
from visualization.plotly_dash import update_dash_app
from notifications import send_telegram_message
from database import save_to_db
import time

def main():
    query = "Python"
    platforms = {
        "Twitter": fetch_tweets,
        "Reddit": fetch_reddit_posts,
        "VK": fetch_vk_posts,
        "Instagram": fetch_instagram_posts,
        "YouTube": fetch_youtube_comments
    }

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
                    save_to_db(platform_name, text, sentiment)

                    # Отправляем уведомление, если слишком негативное
                    if sentiment < -0.8:
                        send_telegram_message(f"Negative sentiment detected on {platform_name}: {text}")

            except Exception as e:
                print(f"Error fetching data from {platform_name}: {e}")

        # Анализ трендов
        trends = analyze_trends()
        print(f"Top trends: {trends}")

        # Обновляем Dash-приложение
        update_dash_app()

        time.sleep(60)  # Обновляем каждую минуту

if __name__ == "__main__":
    main()