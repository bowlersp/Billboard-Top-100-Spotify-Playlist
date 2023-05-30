import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import datetime

SPOTIFY_CLIENT_ID = "80d992fa934f40378787b3061de371cc"
SPOTIFY_SECRET = "baa502202964486ebcd0d9f824ee2f00"
SPOTIFY_REDIRECT_URI = "http://localhost:3000"

##### STEP 1, GETTING ALL THE SONG TITLES #####

travel_date = input(f"which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

URL = f"https://www.billboard.com/charts/hot-100/{travel_date}"

response = requests.get(URL)
top_100_songs = response.text

soup = BeautifulSoup(top_100_songs, "html.parser")
top_100_song_titles = soup.find_all(name="h3", class_="a-no-trucate")

song_titles = []

for song in top_100_song_titles:
    title = song.getText().strip()
    song_titles.append(title)

print(song_titles)


##### STEP 2, SPOTIFY URIS #####


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-library-read playlist-modify-private",
        redirect_uri=SPOTIFY_REDIRECT_URI,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=False,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print(user_id)

uris = [sp.search(title)['tracks']['items'][0]['uri'] for title in song_titles]

#### STEP 3, CREATING THE PLAYLIST ####

PLAYLIST_ID = sp.user_playlist_create(user=user_id, public=False, name=f"{travel_date} Billboard-100")['id']
sp.user_playlist_add_tracks(playlist_id=PLAYLIST_ID, tracks=uris, user=user_id)
