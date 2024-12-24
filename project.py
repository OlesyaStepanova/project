import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Загрузка данных из CSV
df = pd.read_csv('/Users/gor/Desktop/Анализ данных_Проект/spotify-2023.csv', sep = ',', encoding='latin1')

# Создание приложения Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Дэшборд музыкальных треков"),

    dcc.Dropdown(
        id='artist-filter',
        options=[{'label': artist, 'value': artist} for artist in df['artist(s)_name'].unique()],
        value=df['artist(s)_name'].unique()[0],
        multi=True
    ),

    dcc.Graph(id='total-streams-bar-chart'),
    dcc.Graph(id='streams-by-year-line-chart'),
    dcc.Graph(id='danceability-scatters'),
    dcc.Graph(id='avg-energy-boxplot'),
    dcc.Graph(id='bpm-distribution-histogram'),
    dcc.Graph(id='words_percentage_graph'),
])

@app.callback(
    Output('total-streams-bar-chart', 'figure'),
    Output('streams-by-year-line-chart', 'figure'),
    Output('danceability-scatters', 'figure'),
    Output('avg-energy-boxplot', 'figure'),
    Output('bpm-distribution-histogram', 'figure'),
    Output('words_percentage_graph', 'figure'),
    Input('artist-filter', 'value')
)
def update_graphs(selected_artists):
    if isinstance(selected_artists, str):
        selected_artists = [selected_artists]

    filtered_df = df[df['artist(s)_name'].isin(selected_artists)]

    # 1. Столбчатая диаграмма общего количества стримов
    bar_fig = px.bar(filtered_df.groupby('track_name', as_index=False)['streams'].sum(), x='track_name', y='streams', title="Общее количество стримов по трекам", template='plotly_dark')

    # 2. Линейная диаграмма потоков по годам и месяцам
    line_fig = px.line(filtered_df.groupby('released_year')['streams'].sum().reset_index(), x='released_year', y='streams', title="Потоки по годам", template='plotly_dark')

    # 3. Диаграмма рассеяния танцевальности и энергии
    scatter_fig = px.scatter(filtered_df, x='danceability_%', y='energy_%', color='artist(s)_name', title="Танцевальность и энергия", template='plotly_dark')

    # 4. Ящик с усами для уровня энергии
    box_fig = px.box(filtered_df, y='energy_%', title="Распределение уровня энергии", template='plotly_dark')

    # 5. Гистограмма распределения темпа (BPM)
    histogram_fig = px.histogram(filtered_df, x='bpm', title="Распределение темпа (BPM)", template='plotly_dark')

# 6. Процентное распределение количества слов по песням
    percentage_graph = px.pie(filtered_df, names='track_name', values='speechiness_%', title='Процент слов',template='plotly_dark')

    return bar_fig, line_fig, scatter_fig, box_fig, histogram_fig, percentage_graph

if __name__ == '__main__':
    app.run_server(debug=False)