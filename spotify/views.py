from django.shortcuts import get_object_or_404, render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
import random
from user.models import PlayHistory
from django.contrib.auth.models import User
from itertools import chain, combinations

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

# def generate_listening_history():
#     # Fetch all users
#     users = User.objects.all()
#     print("Users", users)

#     # Create a list to store the listening history
#     listening_history = []

#     # Iterate through each user
#     for user in users:
#         # Fetch the listening history entries for the user
#         user_history_entries = PlayHistory.objects.filter(user=user).order_by('date_played')
#         print("listening_history", user_history_entries)

#         # Create a list to represent the user's listening history
#         user_history = [entry.song_title for entry in user_history_entries]

#         # Append the user's history to the listening history list
#         listening_history.append({
#             'user': user.username,
#             'history': user_history,
#         })

#     return listening_history

def generate_listening_history(min_support_threshold):
    # Fetch all users
    users = User.objects.all()
    print("Users", users)

    # Create a list to store the listening history
    listening_history = []

    # Count occurrences of each item (song) in the entire dataset
    item_counts = {}

    # Iterate through each user
    for user in users:
        # Fetch the listening history entries for the user
        user_history_entries = PlayHistory.objects.filter(user=user).order_by('date_played')
        print("listening_history", user_history_entries)

        # Create a list to represent the user's listening history
        user_history = [entry.song_title for entry in user_history_entries]
        print("user history", user_history)

        # Update item counts based on the current user's history
        for itemset in combinations(user_history, 2):
            item_counts[itemset] = item_counts.get(itemset, 0) + 1

        # Append the user's history to the listening history list
        listening_history.append(set(user_history))  # Convert to set to ensure unique items

    # Calculate support for each itemset
    dataset_size = len(listening_history)
    itemset_support = {frozenset(itemset): count / dataset_size for itemset, count in item_counts.items() if count / dataset_size >= min_support_threshold}

    # Filter itemsets based on the minimum support threshold
    frequent_itemsets = {support: [itemset for itemset, support_value in itemset_support.items() if support_value == support] for support in set(itemset_support.values())}

    return frequent_itemsets



def generate_association_rules(frequent_itemsets, min_confidence):
    association_rules = []

    for support, itemsets_list in frequent_itemsets.items():
        for itemset in itemsets_list:
            print("Itemset:", itemset)
            itemset_list = list(itemset)
            print("itemset_list", itemset_list)
            antecedents = generate_antecedents(itemset_list)
            print("Antecedents:", antecedents)
            print("Support:", support)

            if len(antecedents) >= 2:
                print("some...")
                for antecedent in antecedents:
                    antecedent_set = set(antecedent)
                    consequent = set(itemset_list) - antecedent_set
                    antecedent_support = sum(1 for other_itemset in frequent_itemsets[support] if antecedent_set.issubset(other_itemset))
                    confidence = support / antecedent_support if antecedent_support > 0 else 0

                    if confidence >= min_confidence:
                        rule = {
                            'antecedent': antecedent_set,
                            'consequent': consequent,
                            'support': support,
                            'confidence': confidence
                        }
                        association_rules.append(rule)

    return association_rules



def generate_antecedents(itemset_list):
    length = len(itemset_list)

    antecedents = []

    for i in range(2, length + 1):  # Ensure that combinations have at least two items
        antecedents.extend(combinations(itemset_list, i))

    return antecedents


def recommend_song(request, username):
    user_obj = get_object_or_404(User, username=username)
    min_support_threshold = 0.2
    frequent_itemsets = generate_listening_history(min_support_threshold)
    print("Frequent Itemsets:", frequent_itemsets)
    min_confidence = 0.5
    association_rules = generate_association_rules(frequent_itemsets, min_confidence)

    for rule in association_rules:
        print(f"Rule: If user listens to {rule['antecedent']}, then they are likely to listen to {rule['consequent']}. Confidence: {rule['confidence']}")


    context = {
        'frequent_itemsets' : frequent_itemsets,
        # 'association_rules' : association_rules,
        'user_obj' : user_obj,
    }

    return render(request, 'collections.html', context)


