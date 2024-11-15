import streamlit as st
import pandas as pd
import pickle
import requests


#https://drive.google.com/file/d/19ArrUq-Hso4LEJ6JsgFs8-_D9cQD3Oyh/view?usp=sharing

import gdown

# Google Drive file ID
file_id = "19ArrUq-Hso4LEJ6JsgFs8-_D9cQD3Oyh"

# Download destination
output = "similarity_pkl.pkl"  # Or your desired file name

# Generate download URL
url = f"https://drive.google.com/uc?id={file_id}"

# Download the file
gdown.download(url, output, quiet=False)


with open('movie_dict.pkl', 'rb') as file:
    movie_dict = pickle.load(file)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key= lambda x: x[1])[1:6]
    
    recommendations = {}

    for i in movie_list:
        title = movies.iloc[i[0]].title
        genres = movies.iloc[i[0]].genres  
        top_genres = genres[:5]                # Get the top 5 genres
        cast = movies.iloc[i[0]].cast
        director = movies.iloc[i[0]].director  
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)

        recommendations[title] = {
            'genres': top_genres,
            'cast': cast,
            'director': director,
            'poster': poster
        }

    return recommendations

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a3fb637689bc96cfd67c77a3621bbd75&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
#similarity = pickle.load(open('similarity_pkl.pkl', 'rb'))

with open('similarity_pkl.pkl', 'rb') as file:
    similarity = pickle.load(file)

st.title('Movie Recommender System')


st.markdown(f"#### Select a movie")
selected_movie_name = st.selectbox("", movies['title'].values)
st.markdown("<br>", unsafe_allow_html=True)   


if st.button('Show Recommendation'):
    recommendations = recommend(selected_movie_name)
    st.markdown("<br>", unsafe_allow_html=True)   

    tag_colors = [
            "#FFB6C1", "#FFC0CB", "#DDA0DD", "#F08080", "#FFD700",
            "#98FB98", "#00BFFF", "#D2691E", "#FF6347", "#ADFF2F"
    ]    
     
    
    
    
    for idx, (title, details) in enumerate(recommendations.items()):
        col1, col2 = st.columns([1, 2])  

        
        with col1:
            st.image(details['poster'], use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)

       
        with col2:
            st.markdown(f"### {title}")  # Movie title

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("**Genres:**")
            genre_tags = "".join(
            f"<span style='background-color: {tag_colors[i % len(tag_colors)]}; color: white; padding: 5px 10px; margin: 2px; border-radius: 12px; display: inline-block; font-size: 14px;'>{genre}</span>"
            for i, genre in enumerate(details['genres'])
            )
            col2.markdown(genre_tags, unsafe_allow_html=True)
            
            cast_names = " , ".join(details['cast'])
            st.markdown(f"**Cast:** {cast_names}")

            
            director_name = details['director'][0] if isinstance(details['director'], list) else details['director']
            st.markdown(f"**Director:** {director_name}")

            
            st.markdown("---")

            st.markdown("<br>", unsafe_allow_html=True)
