from sentiment_analysis import analyze_sentiment

def analyze_instagram_posts(posts):
    sentiments = []
    for post in posts:
        if post:  # Если пост не пустой
            sentiment = analyze_sentiment(post)
            sentiments.append(sentiment)
    return sentiments
