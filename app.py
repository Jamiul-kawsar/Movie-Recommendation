import streamlit as st
import pickle
import requests
import gdown
import os
import random

#set wide mode
st.set_page_config(layout="wide")

# Load the data
movies = pickle.load(open('movies_list.pkl', 'rb'))
movies_list = movies['title'].values

# Google Drive file ID for similarity.pkl
file_id = "1myEsA8RlFPf0H50FxjouhYh8bSCY-HMc"
output = "similarity.pkl"

# Download the file if it doesn't exist
if not os.path.exists(output):
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# Load the similarity matrix
with open(output, 'rb') as file:
    similarity = pickle.load(file)

print("Data loaded successfully")

# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=11e7832ac1cfb4b42531d16494acbea0"
    response = requests.get(url)
    data = response.json()

    # Handle missing poster_path
    poster_path = data.get('poster_path', None)
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/200x300?text=No+Image"

#  Generate image carousel using valid movie IDs
movies_image = []
for i in range(8):
    movie_id = movies.iloc[random.randint(0, len(movies) - 1)].Movie_id  # Pick random valid ID
    movies_image.append(fetch_poster(movie_id))

#  Streamlit UI
st.title("🎥 Welcome to My Movie Recommendation System!")

#  Show movie carousel
carousel_cols = st.columns(8)
for idx, img in enumerate(movies_image):
    with carousel_cols[idx % 8]:  # Distribute in columns
        st.image(img, width=200)

#  Dropdown for movie selection
select_value = st.selectbox("Select a movie from the dropdown list and get recommendations.", movies_list)

#  Movie Recommendation Function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    
    recommend_movies = []
    recommend_posters = []
    for i in distance[1:7]:  # Top 6 recommendations
        movie_id = movies.iloc[i[0]].Movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    
    return recommend_movies, recommend_posters

#  Show recommendations
if st.button('🎬 Show Recommendations'):
    movies_name, movies_poster = recommend(select_value)
    st.header("Recommended Movies:")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    for i, col in enumerate([col1, col2, col3, col4, col5, col6]):
        with col:
            st.text(movies_name[i])
            st.image(movies_poster[i], width=200)


# Footer Section
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #262730;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 20px;
        }
        .footer a {
            color: #ffcc00;
            text-decoration: none;
        }
        .footer a:hover {
            color:#F62E2E;
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        <p>Made with  by <a href="https://github.com/Jamiul-kawsar" target="_blank">Jamiul Kawsar</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
