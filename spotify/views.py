from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
import random
from user.models import PlayHistory
from django.contrib.auth.models import User


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


def generate_listening_history(request, username):
    # Fetch the listening history for a specific user
    user = User.objects.get(username=username)
    listening_history_entries = PlayHistory.objects.filter(user=user).order_by('date_played')

    # Create a list to store sequences of song titles
    listening_history = []

    # Initialize a sequence for the current user
    current_sequence = []

    # Iterate through the listening history entries
    for entry in listening_history_entries:
        song_title = entry.song_title
        current_sequence.append(song_title)

    # Append the current user's sequence to the listening history
    listening_history.append(current_sequence)

    # You can optionally include more history by considering all past songs
    all_songs = [entry.song_title for entry in listening_history_entries]
    listening_history.append(all_songs)

    # You can return or render the listening history as needed
    return listening_history

#Calculate the support count for each song in your dataset. The support count is the number of times a song appears in all listening sequences.

# def get_support_count(listening_history, song):
#     count = 0
#     for sequence in listening_history:
#         if song in sequence:
#             count += 1
#     return count

# #Determine the frequent itemsets, i.e., songs with support counts above a minimum threshold. You need to specify a minimum support count to consider a song frequent.

# def get_frequent_itemsets(listening_history, min_support_count):
#     frequent_itemsets = []
#     min_support_count = 10
#     all_songs = set(song for sequence in listening_history for song in sequence)

#     for song in all_songs:
#         support = get_support_count(listening_history, song)
#         if support >= min_support_count:
#             frequent_itemsets.append(frozenset({song}))
#     return frequent_itemsets

# # Implement the function to generate candidate itemsets from the frequent itemsets.
# def generate_candidates(frequent_itemsets):
#     candidates = set()
#     for i in range(len(frequent_itemsets)):
#         for j in range(i + 1, len(frequent_itemsets)):
#             itemset1, itemset2 = frequent_itemsets[i], frequent_itemsets[j]
#             union = itemset1.union(itemset2)
#             if len(union) == len(itemset1) + 1:
#                 candidates.add(frozenset(union))
#     return candidates

# # Prune the candidate itemsets to eliminate those that contain infrequent subsets. This step helps reduce the number of itemsets to check.
# def prune_candidates(candidates, frequent_itemsets):
#     pruned_candidates = set()
#     for candidate in candidates:
#         is_valid = True
#         subsets = [candidate.difference({item}) for item in candidate]
#         for subset in subsets:
#             if subset not in frequent_itemsets:
#                 is_valid = False
#                 break
#         if is_valid:
#             pruned_candidates.add(candidate)
#     return pruned_candidates

# # Repeatedly generate candidates and prune until no more candidates can be formed. This process will give you frequent itemsets of different sizes.
# def get_all_frequent_itemsets(listening_history, min_support_count):
#     frequent_itemsets = []
#     candidates = set()
#     k = 1

#     while True:
#         if k == 1:
#             candidates = get_frequent_itemsets(listening_history, min_support_count)
#         else:
#             candidates = generate_candidates(frequent_itemsets)
#             candidates = prune_candidates(candidates, frequent_itemsets)

#         if not candidates:
#             break

#         frequent_itemsets.extend(candidates)
#         k += 1

#     return frequent_itemsets

# # Once you have the frequent itemsets, you can generate association rules based on metrics like confidence, lift, etc.

# def generate_association_rules(listening_history, min_support_count, min_confidence):
#     frequent_itemsets = get_all_frequent_itemsets(listening_history, min_support_count)
#     association_rules = []

#     for itemset in frequent_itemsets:
#         if len(itemset) < 2:
#             continue
#         for item in itemset:
#             antecedent = itemset.difference({item})
#             support_itemset = get_support_count(listening_history, itemset)
#             support_antecedent = get_support_count(listening_history, antecedent)
#             confidence = support_itemset / support_antecedent
#             if confidence >= min_confidence:
#                 association_rules.append((antecedent, item, confidence))

#     return association_rules

# # Finally, you can use the association rules to recommend songs to users. You may recommend songs based on the songs they've already listened to. For example, if a user has listened to song A, the association rules can suggest song B.
# def recommend_songs_to_user(user_history, association_rules, min_confidence, max_recommendations=10):
#     recommendations = []

#     for rule in association_rules:
#         antecedent, consequent, confidence = rule
#         if antecedent.issubset(user_history) and confidence >= min_confidence:
#             recommendations.append((consequent, confidence))

#     # Sort recommendations by confidence in descending order
#     recommendations.sort(key=lambda x: x[1], reverse=True)

#     # Take the top 10 recommendations or fewer if there are fewer than 10
#     top_recommendations = [recommendation[0] for recommendation in recommendations[:max_recommendations]]

#     return top_recommendations


# def recommend_songs(request, username):
#     # Fetch the user's listening history and other data
#     user = User.objects.get(username=username)  # Replace 'username' with your actual field name
#     listening_history_entries = PlayHistory.objects.filter(user=user).order_by('date_played')

#     listening_history = [entry.song_title for entry in listening_history_entries]

#     # Generate association rules
#     min_support_count = 10  # Set your desired support count threshold
#     min_confidence = 0.7  # Set your desired confidence threshold
#     association_rules = generate_association_rules(listening_history, min_support_count, min_confidence)

#     # Get song recommendations based on the user's history, limited to 10 recommendations
#     recommendations = recommend_songs_to_user(listening_history, association_rules, min_confidence, max_recommendations=10)

#     context = {
#         'username': username,
#         'recommendations': recommendations,
#     }

#     return render(request, 'collections.html', context)

