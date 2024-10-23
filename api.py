import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to fetch album cover
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Fallback image

# Function to recommend songs based on genre features
def recommend(song):
    index = music[music['track_name'] == song].index[0]  # Adjusted for new dataset
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_music_names = []
    recommended_music_posters = []
    
    for i in distances[1:6]:
        artist = music.iloc[i[0]].track_artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].track_name, artist))
        recommended_music_names.append(music.iloc[i[0]].track_name)
    
    return recommended_music_names, recommended_music_posters

# Streamlit App UI
st.header('Music Recommender System Based on Genre')

# Load the pickled genre-based data
music = pickle.load(open('df_genre.pkl', 'rb'))  # New dataframe based on genre
similarity = pickle.load(open('similarity_genre.pkl', 'rb'))  # Genre-based similarity matrix

music_list = music['track_name'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])