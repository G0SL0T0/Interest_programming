import plotly.express as px
import pandas as pd

# Визуализация данных из Instagram
def visualize_instagram_sentiments(sentiments):
    df = pd.DataFrame(sentiments, columns=['sentiment'])
    fig = px.line(df, y='sentiment', title='Instagram Sentiment Analysis')
    fig.show()