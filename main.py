import requests
import base64
from spotify_clients import CLIENT_ID, CLIENT_SECRET
from collections import Counter
import matplotlib.pyplot as plt

auth_url = "https://accounts.spotify.com/api/token"
auth_header = {}
auth_data = {}


def get_access_token(client_id, client_secret):
    message = f"{client_id}:{client_secret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    auth_header['Authorization'] = f"Basic {base64_message}"
    auth_data['grant_type'] = "client_credentials"

    res = requests.post(auth_url, headers=auth_header, data=auth_data)
    access_token = res.json()['access_token']

    return access_token


def get_playlist_object(token, playlist_id):
    playlist_endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    get_header = {
        "Authorization": "Bearer " + token
    }
    playlist_object = requests.get(playlist_endpoint_url, headers=get_header).json()
    return playlist_object


def get_artist_object(token, artist_id):
    artist_endpoint_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    get_header = {
        "Authorization": "Bearer " + token
    }
    artist_object = requests.get(artist_endpoint_url, headers=get_header).json()
    return artist_object


def main():
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    playlist_id = "6dQXeWKIctLJLrsvU54NId"
    playlist = get_playlist_object(token, playlist_id)
    genre_list = []

    print("Loading...")
    for i in playlist['tracks']['items']:
        artist_id = i['track']['artists'][0]['id']
        artist = get_artist_object(token, artist_id)
        genre_array = artist['genres']
        if len(genre_array) != 0:
            genre_list.append(genre_array[0])

    genre_counter = Counter(genre_list)
    condensed_genres = []
    condensed_count = []

    for i, j in genre_counter.items():
        condensed_genres.append(i)
        condensed_count.append(j)

    plt.barh(condensed_genres, condensed_count, color='#1ed760')
    print("Genre bar char loaded")
    plt.show()


main()
