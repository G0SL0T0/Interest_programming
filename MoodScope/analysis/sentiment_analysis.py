from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return 1 if result['label'] == 'POSITIVE' else -1 if result['label'] == 'NEGATIVE' else 0
