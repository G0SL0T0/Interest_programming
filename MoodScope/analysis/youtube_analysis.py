from sentiment_analysis import analyze_sentiment

def analyze_youtube_comments(comments):
    sentiments = []
    for comment in comments:
        if comment:
            sentiment = analyze_sentiment(comment)
            sentiments.append(sentiment)
    return sentiments
