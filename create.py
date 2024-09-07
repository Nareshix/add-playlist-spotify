import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# replace these with your own Spotify Developer credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='8411596211a64142bed0144002c264f7',
                                               client_secret='4bb7a249093643adabe8c044ccca158f',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='playlist-modify-public'))

# Replace with your Spotify username
username = 'y5vyj749z7pbn8hk4mbdrtk5a'

# Read song titles from text file
with open('songs.txt', 'r', encoding='utf-8') as file:
    songs = [line.strip() for line in file.readlines()]

# Create a new playlist
playlist_name = "My Generated Playlist"
playlist = sp.user_playlist_create(username, playlist_name, public=True)

# Search for a track on Spotify
def search_song(song):
    results = sp.search(q=song, limit=1, type='track')
    if results['tracks']['items']:
        return results['tracks']['items'][0]['id']
    return None

# Search and add songs to playlist
track_ids = []
for song in songs:
    print(f"Searching for: {song}")
    track_id = search_song(song)
    if track_id:
        track_ids.append(track_id)
    else:
        print(f"Could not find: {song}")
    time.sleep(0.5)  # Adding a delay to avoid hitting rate limits

# Add tracks to the playlist if found
if track_ids:
    def add_tracks_to_playlist(sp, playlist_id, track_ids):
        # Spotify allows a maximum of 100 track URIs per request, so I start splitting .
        batch_size = 100
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            sp.playlist_add_items(playlist_id, batch)

    # Add tracks to the playlist
    add_tracks_to_playlist(sp, playlist['id'], track_ids)
    print(f"Added {len(track_ids)} songs to the playlist '{playlist_name}'")
else:
    print("No songs were added to the playlist.")
