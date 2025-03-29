import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from database import fetch_data

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='sentiment-graph'),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)  # Обновление каждую минуту
])

@app.callback(Output('sentiment-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):

    data = fetch_data()
    df = pd.DataFrame(data, columns=['id', 'platform', 'text', 'sentiment', 'timestamp'])
    fig = px.line(df, x='timestamp', y='sentiment', color='platform', title='Sentiment Analysis over Time')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
