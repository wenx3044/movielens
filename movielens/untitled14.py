

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import requests
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import random


api_key = ''
movie_full = pd.DataFrame()
app = dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])

app.layout = html.Div([
    html.Div([
        html.H3(children='MovieLens Database',
                style={'color': '#8CD8F1 ', 'textAlign': 'center'}),

        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div(children='Search movies by tag',
                                 style={'color': '#8CD8F1 ', 'textAlign': 'right', 'size': 50}),
                    ], width=9),
                    dbc.Col([
                        html.Div([
                            dcc.Input(id='filter_value', value=''),
                        ], ),
                    ], width=8, align='left'),
                ]),
            ]), ),

        html.Br(),

        dbc.Carousel(id='carousel_placeholder',
                     items=[],
                     controls=True,
                     indicators=True,
                     style={'width': 500, 'align': 'center'})
    ]), ])


@app.callback(
    Output('carousel_placeholder', 'items'),
    [Input('filter_value', 'value')])

def create_carousel_content(input_value):
    global movie_full
    if movie_full.empty:
        movie_full = movie_data_loader()

    if input_value == '':
        dff = movie_full.sample(n=12)
    else:
        dff = movie_full[movie_full['tag'] == input_value]

    display_movie_id = dff['movieId'].to_list()
    display_title = dff['title'].to_list()
    display_rating = dff['rating'].to_list()
    # display_genres = dff['genres'].to_list()
    # display_imdb_id = dff['imdbId'].to_list()
    # display_tmdb_id = dff['tmdbId'].to_list()

    movies = []
    for movie_index in range(len(dff)):
        movie_id = str(display_movie_id[movie_index])
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            poster_path = data['poster_path']
            full_path = 'https://via.placeholder.com/150' if not poster_path \
                else f'https://image.tmdb.org/t/p/w500/{poster_path}'
        else:
            full_path = "https://via.placeholder.com/150"
            continue

        movie_information = {
            'key': movie_index,
            'src': full_path,
            'header': str(display_title[movie_index]),
            'caption': str(display_rating[movie_index]),
        }
        movies.append(movie_information)

    return movies


if __name__ == '__main__':
    app.run_server(debug=True)
