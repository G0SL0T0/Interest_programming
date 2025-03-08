import matplotlib.pyplot as plt
import pandas as pd
from database import fetch_data

# Функция для построения графика настроений
def plot_sentiments():
    # Получаем данные из базы
    data = fetch_data()
    df = pd.DataFrame(data, columns=['id', 'platform', 'text', 'sentiment', 'timestamp'])

    # Группируем по платформе и времени
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    grouped = df.groupby('platform')['sentiment'].resample('1T').mean().unstack(level=0)

    # Строим график
    plt.figure(figsize=(10, 6))
    for platform in grouped.columns:
        plt.plot(grouped.index, grouped[platform], label=platform)

    plt.title('Sentiment Analysis over Time')
    plt.xlabel('Time')
    plt.ylabel('Sentiment Polarity')
    plt.legend()
    plt.grid(True)
    plt.show()

# Функция для построения гистограммы трендов
def plot_trends(trends):
    words, frequencies = zip(*trends)
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color='skyblue')
    plt.title('Top Trends')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()