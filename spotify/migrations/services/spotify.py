import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '8cd97605e5194de4bc654b4f120daf98'
CLIENT_SECRET = '8899652981f040859a6cd2c03fa92b7e'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
