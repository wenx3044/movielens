#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 04:45:40 2021

@author: xinwen
"""

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import requests
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


def movie_data_loader():
    
    class Movie(object):
        """ Movie class that stores movie attributes.
        """

        def __init__(self, movie_id, title, genres):
      
            self.movie_id = movie_id
            self.title = title
            self.genres = genres


    class User(object):
        """ User class that stores user attributes.
        """

        def __init__(self, user_id, gender, age, occupation, zip_code):
            
            self.user_id = user_id
            self.gender = gender
            self.age = age
            self.occupation = occupation
            self.zip_code = zip_code


    class Rating(object):
        """ Rating class that relates a user to a movie with a given rating.
        """

        def __init__(self, user_id, movie_id, rating, timestamp):
        
            self.user_id = user_id
            self.movie_id = movie_id
            self.rating = rating
            self.timestamp = timestamp
    # read movielens.org datasets
    class Recommender(object):
     """ Recommender class that recommends movies based on a user's attributes.
    """
    movies_file = 'movies.dat'
    ratings_file = 'ratings.dat'
    users_file = 'users.dat'

    def __init__(self):
        self.movie_id_to_movie = {}
        self.user_id_to_user = {}
        self.user_id_to_rating = {}
        self.rated_movies = {}
        self.load_data()

    def load_data(self):
        """ load all movie, user, and rating data from external files
        """

        # movies data
        with open(Recommender.movies_file) as f:
            lis = [line.split() for line in f]
            print(lis)
        for line in lines:
            words = line.split('::')
            movie_id = int(words[0])
            title = words[1]
            genres = words[2].split('|')
            movie = Movie(movie_id, title, genres)
            self.movie_id_to_movie[movie_id] = movie

        # users data
        with open(Recommender.users_file) as f:
            lines = f.read().splitlines()
        for line in lines:
            words = line.split('::')
            user_id = int(words[0])
            gender = words[1]
            age = int(words[2])
            occupation = int(words[3])
            zip_code = words[4]
            user = User(user_id, gender, age, occupation, zip_code)
            self.user_id_to_user[user_id] = user

        # ratings data
        with open(Recommender.ratings_file) as f:
            lines = f.read().splitlines()
        for line in lines:
            words = line.split('::')
            user_id = int(words[0])
            movie_id = int(words[1])
            rating = int(words[2])
            timestamp = words[3]
            rating = Rating(user_id, movie_id, rating, timestamp)
            self.user_id_to_rating[user_id] = rating

api_key = ''
lines = pd.DataFrame()
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H3('MovieLens Database',
                style={'color': '#8CD8F1 ', 'textAlign': 'center'}),

        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div('Search movies by tag',
                                 style={'color': '#8CD8F1 ', 'textAlign': 'right', 'size': 38}),
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            dcc.Input(id='filter_value', value=''),
                        ], ),
                    ], width=6, align='left'),
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
    [Input('filter_value', 'value')]
)
def create_carousel_content(input_value):
    global lines
    if lines.empty:
        lines = movie_data_loader()

    if input_value == '':
        dff = lines.sample(n=12)
    else:
        dff = lines[lines['tag'] == input_value]

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
