from nltk import FreqDist
from nltk.tokenize import word_tokenize

# Анализ трендов
def analyze_trends(texts):
    words = [word for text in texts for word in word_tokenize(text.lower()) if word.isalpha()]
    freq_dist = FreqDist(words)
    return freq_dist.most_common(10)  # Топ-10 популярных слов