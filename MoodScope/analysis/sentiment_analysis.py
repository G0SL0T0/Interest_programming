from transformers import pipeline

# Загрузка модели
sentiment_analyzer = pipeline("sentiment-analysis")

# Анализ настроений
def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return 1 if result['label'] == 'POSITIVE' else -1 if result['label'] == 'NEGATIVE' else 0