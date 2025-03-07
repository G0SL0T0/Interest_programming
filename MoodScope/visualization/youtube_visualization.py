import plotly.express as px
import pandas as pd

# Визуализация данных из YouTube
def visualize_youtube_sentiments(sentiments):
    df = pd.DataFrame(sentiments, columns=['sentiment'])
    fig = px.line(df, y='sentiment', title='YouTube Sentiment Analysis')
    fig.show()