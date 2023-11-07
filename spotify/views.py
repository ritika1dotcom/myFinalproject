from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
import random
from .models import Song
from .utils import discover_associations, preprocess_song_data
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd
from django.http import HttpResponse
from spotipy import Spotify


# Fetch client credentials from settings
SPOTIPY_CLIENT_ID = settings.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = settings.SPOTIPY_CLIENT_SECRET

# Initialize spotipy with your client id and secret
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))


def search_song(request):
    query = request.GET.get('query')
    
    # Start with song search
    song_results = sp.search(q=query, type='track', limit=10)
    tracks = song_results['tracks']['items']

    # If no songs found, try searching for artist and their songs
    if not tracks:
        artist_results = sp.search(q=query, type='artist', limit=1)
        
        if artist_results['artists']['items']:
            artist = artist_results['artists']['items'][0]
            artist_id = artist['id']

            # Fetch the albums of the artist
            albums = sp.artist_albums(artist_id, limit=5)  # Setting a limit to fetch 5 albums; you can adjust this
        
            for album in albums['items']:
                album_tracks = sp.album_tracks(album['id'])['items']
                tracks.extend(album_tracks)

    return render(request, 'search.html', {'tracks': tracks})


def featured_music(request):
    # Fetch a list of featured playlists
    playlists = sp.featured_playlists(limit=20)  # You can adjust the limit as needed
    
    # If no playlists were found, return an empty list to the template
    if not playlists['playlists']['items']:
        return render(request, 'home.html', {'featured_tracks': []})
    
    # Randomly select a playlist
    selected_playlist = random.choice(playlists['playlists']['items'])
    playlist_uri = selected_playlist['uri']

    # Fetch tracks from the selected playlist
    tracks_data = sp.playlist_tracks(playlist_uri)["items"]

    # Extract essential details for each track
    featured_tracks = []
    for track_data in tracks_data:
        track = track_data["track"]
        
        # Get the track's main artist's details
        artist_uri = track["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        album_image_url = track["album"]["images"][0]["url"] if track["album"]["images"] else None

        featured_tracks.append({
            "uri": track["uri"],
            "name": track["name"],
            "artist_name": track["artists"][0]["name"],
            "artist_popularity": artist_info["popularity"],
            "artist_genres": artist_info["genres"],
            "album_name": track["album"]["name"],
            "track_popularity": track["popularity"],
            "album_image" : album_image_url,
            "preview_url": track.get("preview_url") 
        })

    return render(request, 'home.html', {'featured_tracks': featured_tracks})


def fetch_and_save_songs(request):
    # Initialize Spotipy with your credentials
    # Query Spotify for song data
    # You can customize the query based on your requirements
    query = request.GET.get('query')
    results = sp.search(q= query, type='track', limit=10)

    # Process and save the song data to your database
    for track in results['tracks']['items']:
        song = Song(
            title=track['name'],
            artist=track['artists'][0]['name'],
            album=track['album']['name'],
            # Add more fields and data as needed
        )
        song.save()

    # Render a template or return a response
    return render(request, 'collections.html')
# myapp/views.py


def discover_song_associations(request):
    # Fetch and preprocess song data
    songs = Song.objects.all()  # Modify this to fetch your songs
    song_data = preprocess_song_data(songs)  # Implement this function

    # Discover associations
    associations = discover_associations(song_data, min_support=0.1, min_threshold=0.7)

    # Render a template or return a response with the discovered associations
    return render(request, 'collections.html', {'associations': associations})
