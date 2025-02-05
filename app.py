import streamlit as st
import pickle
import requests


# Load the data
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

pickle.load(open('simIlarity.pkl', 'rb'))


st.header("Movie Recommendation System")
select_value = st.selectbox("Select a movie", movies_list)

# show the movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=11e7832ac1cfb4b42531d16494acbea0".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda vector: vector[1])
    recommend_movies = []
    recommend_posters = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].Movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movies_id))
    return recommend_movies, recommend_posters

# show recommand
if st.button('Show Recommend'):
    movies_name, movies_poster = recommend(select_value)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movies_name[0])
        st.image(movies_poster[0])

    with col2:
        st.text(movies_name[1])
        st.image(movies_poster[1])

    with col3:
        st.text(movies_name[2])
        st.image(movies_poster[2])

    with col4:
        st.text(movies_name[3])
        st.image(movies_poster[3])

    with col5:
        st.text(movies_name[4])
        st.image(movies_poster[4])

