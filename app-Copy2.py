'''
import streamlit as st
import pandas as pd
import pickle
import requests

# Streamlit run /Users/rishisrivastava/coding/projects/movie_recommendation_system/app-Copy2.py

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key= lambda x: x[1])[1:6]
    
    recommendations = {}

    for i in movie_list:
        title = movies.iloc[i[0]].title
        genres = movies.iloc[i[0]].genres  # Assuming genres is a list
        top_genres = genres[:5]  # Get the top 5 genres
        cast = movies.iloc[i[0]].cast
        director = movies.iloc[i[0]].director  # Make sure 'director' is the correct column name
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

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit title
st.title('Movie Recommender System')

# Select box for movie selection
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommendations = recommend(selected_movie_name)

    # Loop through the recommendations and display them
    for title, details in recommendations.items():
        st.markdown(f"### {title}")
        
        # Display movie poster
        st.image(details['poster'])
        
        # Display genres as tags
        st.markdown("**Genres:**")
        for genre in details['genres']:
            st.markdown(f"<span style='background-color: #f0f0f0; padding: 5px; border-radius: 10px;'>{genre}</span>", unsafe_allow_html=True)
        
        # Display cast as tags
        st.markdown("**Cast:**")
        for actor in details['cast']:
            st.markdown(f"<span style='background-color: #e0e0e0; padding: 5px; border-radius: 10px;'>{actor}</span>", unsafe_allow_html=True)
        
        # Display director name
        st.markdown(f"**Director:** {details['director']}")
        
        # Add separator for better UI
        st.markdown("---")

st.title('Movie Recommender System')

selected_movie_name = st.selectbox("Select a movie",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
'''


import streamlit as st
import pandas as pd
import pickle
import requests

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
    </style>
""", unsafe_allow_html=True)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key= lambda x: x[1])[1:6]
    
    recommendations = {}

    for i in movie_list:
        title = movies.iloc[i[0]].title
        genres = movies.iloc[i[0]].genres  # Assuming genres is a list
        top_genres = genres[:5]  # Get the top 5 genres
        cast = movies.iloc[i[0]].cast
        director = movies.iloc[i[0]].director  # Ensure 'director' is a string, not a list
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

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit title
st.title('Movie Recommender System')

# Select box for movie selection
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommendations = recommend(selected_movie_name)

    # Create columns with doubled width
    col_count = 5  # Number of columns you want to show
    cols = st.columns([2, 2, 2, 2, 2])  # Adjust proportions for column width

    # Color palette for tags
    tag_colors = [
        "#FFB6C1", "#FFC0CB", "#DDA0DD", "#F08080", "#FFD700",
        "#98FB98", "#00BFFF", "#D2691E", "#FF6347", "#ADFF2F"
    ]

    # Loop through the recommendations and display them in columns
    for idx, (title, details) in enumerate(recommendations.items()):
        # If there are more movies than columns, we cycle through columns
        col = cols[idx % col_count]

        # Display movie title
        col.markdown(f"### {title}")
        
        # Display movie poster
        col.image(details['poster'])
        
        # Display genres as tags
        col.markdown("**Genres:**")
        genre_tags = "".join(
            f"<span style='background-color: {tag_colors[i % len(tag_colors)]}; color: white; padding: 5px 10px; margin: 2px; border-radius: 12px; display: inline-block; font-size: 14px;'>{genre}</span>"
            for i, genre in enumerate(details['genres'])
        )
        col.markdown(genre_tags, unsafe_allow_html=True)

        # Add space between genres and cast
        col.markdown("<br>", unsafe_allow_html=True)

        # Creative display for cast (just as a list with some style)
        col.markdown("**Cast:**")
        cast_names = ", ".join(details['cast'])  # Joining names as a single string
        col.markdown(f"<div style='font-family: Montserrat, sans-serif; font-size: 14px; color: #d6d6d6; font-weight: bold;'> {cast_names} </div>" , unsafe_allow_html=True)

        # Add space between cast and director
        col.markdown("<br>", unsafe_allow_html=True)

        # Display director name properly (removing brackets and making it more readable)
        director_name = details['director'][0] if isinstance(details['director'], list) else details['director']
        col.markdown("**Director:**")

        director_name = ", ".join(details['director'])  # Joining names as a single string
        col.markdown(f"<div style='font-family: Montserrat, sans-serif; font-size: 14px; color: #d6d6d6; '> {director_name} </div>", unsafe_allow_html=True)


        
        # Add separator for better UI (optional)
        col.markdown("---")
