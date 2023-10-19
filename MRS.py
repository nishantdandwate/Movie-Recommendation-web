import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

similarity = pd.read_pickle('similarity.pkl')
movies_dict = pd.read_pickle('movies.pkl')
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommendation System')

select_movie_name = st.selectbox(
    'Select your favourite movie:-',
    movies['title'].values)

if st.button('Recommend'):
    recommend_movies, recommend_movies_posters = recommend(select_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommend_movies[0])
        st.image(recommend_movies_posters[0])
    with col2:
        st.text(recommend_movies[1])
        st.image(recommend_movies_posters[1])
    with col3:
        st.text(recommend_movies[2])
        st.image(recommend_movies_posters[2])
    with col4:
        st.text(recommend_movies[3])
        st.image(recommend_movies_posters[3])
    with col5:
        st.text(recommend_movies[4])
        st.image(recommend_movies_posters[4])
