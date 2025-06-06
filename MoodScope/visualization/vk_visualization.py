import plotly.express as px
import pandas as pd

def visualize_vk_sentiments(sentiments):
    df = pd.DataFrame(sentiments, columns=['sentiment'])
    fig = px.line(df, y='sentiment', title='VK Sentiment Analysis')
    fig.show()
