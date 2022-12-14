import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

ansh_uri = "https:e//anshkulshreshtha.github.io/my-sit/"
Client_ID = "25fe9be5b43b468fb8799f99f06d24ea"
Client_Secret = "1e5f8d545b0443d8b6dce5affc7ad1e3"
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

response = requests.get("https://www.billboard.com/charts/hot-100/2000-08-12/" + date)

Soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = Soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=ansh_uri,
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
