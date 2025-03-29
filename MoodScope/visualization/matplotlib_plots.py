import matplotlib.pyplot as plt
import pandas as pd
from database import fetch_data
from utils.logging_utils import log_info, log_error

def plot_sentiments():
    try:
        data = fetch_data()
        df = pd.DataFrame(data, columns=['id', 'platform', 'text', 'sentiment', 'timestamp'])

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        grouped = df.groupby('platform')['sentiment'].resample('1T').mean().unstack(level=0)

        plt.figure(figsize=(10, 6))
        for platform in grouped.columns:
            plt.plot(grouped.index, grouped[platform], label=platform)

        plt.title('Sentiment Analysis over Time')
        plt.xlabel('Time')
        plt.ylabel('Sentiment Polarity')
        plt.legend()
        plt.grid(True)
        plt.show()
        log_info("Sentiment plot generated successfully.")
    except Exception as e:
        log_error(f"Error generating sentiment plot: {e}")

def plot_trends(trends):
    try:
        words, frequencies = zip(*trends)
        plt.figure(figsize=(10, 6))
        plt.bar(words, frequencies, color='skyblue')
        plt.title('Top Trends')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.show()
        log_info("Trends plot generated successfully.")
    except Exception as e:
        log_error(f"Error generating trends plot: {e}")
