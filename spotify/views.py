from django.shortcuts import get_object_or_404, render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
import random
from user.models import PlayHistory
from django.contrib.auth.models import User
from itertools import combinations

# Fetch client credentials from settings
SPOTIPY_CLIENT_ID = settings.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = settings.SPOTIPY_CLIENT_SECRET

# Initialize spotipy with your client id and secret
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

def search_song(request):
    query = request.GET.get('query')
    # Start with song search
    song_results = sp.search(q=query, type='track', limit=10)
    tracks = []

    for track in song_results['tracks']['items']:
        # Extract the album image URL
        album_image_url = track["album"]["images"][0]["url"] if track["album"]["images"] else None

        # Add the track details to the list
        track_data = {
            "song_name": track["name"],
            "artist_name": track["artists"][0]["name"],
            "album_name": track["album"]["name"],
            "album_image": album_image_url,
            "preview_url": track.get("preview_url"),
        }
        tracks.append(track_data)

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


def all_song():
    # Fetch a list of featured playlists
    playlists = sp.featured_playlists(limit=20)  # You can adjust the limit as needed
    
    # If no playlists were found, return an empty list
    if not playlists['playlists']['items']:
        return []

    # Randomly select a playlist
    selected_playlist = random.choice(playlists['playlists']['items'])
    playlist_uri = selected_playlist['uri']

    # Fetch tracks from the selected playlist
    tracks_data = sp.playlist_tracks(playlist_uri)["items"]

    # Extract essential details for each track
    all_music = []
    for track_data in tracks_data:
        track = track_data["track"]
        
        # Get the track's main artist's details
        artist_uri = track["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        album_image_url = track["album"]["images"][0]["url"] if track["album"]["images"] else None

        all_music.append({
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

    return all_music


def listening_history(user):
    # Fetch the listening history entries for the user
    user_history_entries = PlayHistory.objects.filter(user=user).order_by('date_played')
    # print("listening_history", user_history_entries)

    # Create a dictionary to represent the user's listening history
    user_history = {entry.song_title: 1 for entry in user_history_entries}

    return user_history

def generate_listening_history(min_support_threshold):
    # Fetch all users
    users = User.objects.all()

    # Create a list to store the listening history
    listening_history = []

    # Count occurrences of each item (song) in the entire dataset
    item_counts = {}

    # Iterate through each user
    for user in users:
        # Fetch the listening history entries for the user
        user_history_entries = PlayHistory.objects.filter(user=user).order_by('date_played')
        # print("generate",user_history_entries)

        # Create a list to represent the user's listening history
        user_history = [entry.song_title for entry in user_history_entries]
        # print("user_history",user_history)

        # Update item counts based on the current user's history
        for itemset in combinations(user_history, 2):
            item_counts[itemset] = item_counts.get(itemset, 0) + 1

        # Append the user's history to the listening history list
        listening_history.append(frozenset(user_history))  # Convert to frozenset to ensure unique items
        # print("listening histor",listening_history)

    # Calculate support for each itemset
    dataset_size = len(listening_history)
    itemset_support = {frozenset(itemset): count / dataset_size for itemset, count in item_counts.items() if count / dataset_size >= min_support_threshold}
    # print("itemset",itemset_support)
    # Filter itemsets based on the minimum support threshold
    frequent_itemsets = {support: [itemset for itemset, support_value in itemset_support.items() if support_value == support] for support in set(itemset_support.values())}
    # print("freqient",frequent_itemsets)
    return frequent_itemsets


def generate_association_rules(listening_history, min_support_threshold, min_confidence=0.5):
    rules = []

    # Count occurrences of each item (song) in the entire dataset
    item_counts = {}

    # Update item counts based on the current user's history
    for itemset in combinations(listening_history, 2):
        item_counts[itemset] = item_counts.get(itemset, 0) + 1

    print("Item Counts:", item_counts)

    # Filter itemsets based on the minimum support threshold
    frequent_itemsets = {itemset: count for itemset, count in item_counts.items() if count >= min_support_threshold}

    print("Frequent Itemsets After Filtering (Before Rule Generation):", frequent_itemsets)

    # Calculate support for each itemset after filtering
    dataset_size = len(listening_history)
    itemset_support = {frozenset(itemset): count / dataset_size for itemset, count in frequent_itemsets.items()}

    print("Itemset Support After Filtering:", itemset_support)

    for itemset, support in itemset_support.items():
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent_set = set(antecedent)
                consequent_set = itemset - antecedent_set
                confidence_value = support
                rules.append({
                    'antecedent': antecedent_set,
                    'consequent': consequent_set,
                    'confidence': confidence_value
                })

    print("Generated Rules:", rules)

    return rules


def recommend_songs(listening_history, association_rules):
    recommendations = {}
    print("association_rules", association_rules)
    for rule in association_rules:
        antecedent, consequent, confidence = rule['antecedent'], rule['consequent'], rule['confidence']
        print("confidence",confidence)
        # Convert antecedent and consequent to frozensets
        antecedent_set = frozenset(antecedent)
        consequent_set = frozenset(consequent)

        if antecedent_set.issubset(listening_history):
            likelihood = round(confidence * 100, 4)  # Convert confidence to percentage with 4 decimal places
            for song in consequent_set:
                if song not in listening_history or likelihood > listening_history[song]:
                    listening_history[song] = likelihood
    
    result = [{'song': song, 'confidence': likelihood} for song, likelihood in listening_history.items()]
    # print("result",result)
    return result

def recommend_song(request, username):
    user_obj = get_object_or_404(User, username=username)
    min_support_threshold = 0.2
    min_confidence = 0.5
    
    # Fetch the listening history for the current user
    user_listening_history = listening_history(user_obj)

    # If the user's history is empty, generate random recommendations with high confidence
    if not user_listening_history:
        random_recommendations = generate_random_recommendations(min_confidence)
        context = {
            'user_obj': user_obj,
            'recommended_songs': random_recommendations,
        }
    else:
        frequent_itemsets = generate_listening_history(min_support_threshold)
        association_rules = generate_association_rules(user_listening_history, min_support_threshold, min_confidence)
        print(association_rules)
        recommended_songs = recommend_songs(user_listening_history, association_rules)

        context = {
            'user_obj': user_obj,
            'recommended_songs': recommended_songs,
        }

    return render(request, 'collections.html', context)

def generate_random_recommendations(min_confidence):
    # Generate a list of random songs with high confidence
    all_music = all_song()
    # num_recommendations = min(10, len(all_music))  # Limit to 15 songs or the number of available tracks
    random_songs = get_random_songs(10, all_music)
    random_recommendations = [{'song': song, 'confidence': min_confidence * 100} for song in random_songs]
    return random_recommendations

def get_random_songs(num_songs, featured_tracks):
    # Extract song names from the featured tracks
    all_songs = [track['name'] for track in featured_tracks]
    
    # Replace this with your logic to fetch random songs (e.g., from a database or API)
    return random.sample(all_songs, num_songs)
