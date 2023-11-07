from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def discover_associations(data, min_support=0.1, min_threshold=0.7):
    # Create a one-hot encoded DataFrame from your data
    # You may need to customize this based on your data structure
    one_hot = data.groupby(['title', 'artist']).size().unstack().fillna(0)
    one_hot = (one_hot > 0).astype(int)

    # Apply the Apriori algorithm
    frequent_itemsets = apriori(one_hot, min_support=min_support, use_colnames=True)

    # Discover association rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold)
    return rules

# myapp/utils.py

# Import necessary libraries

def preprocess_song_data(songs):
    # Perform data preprocessing on the fetched songs
    # For example, you might extract relevant fields and create a DataFrame

    # Assuming 'songs' is a QuerySet of Song objects
    song_data = []

    for song in songs:
        # Extract relevant fields from the Song model
        unique_identifier = song.title  # Replace with your actual field name
        song_field = song.artist  # Replace with your actual field name

        # Append the data as a tuple or dictionary, depending on your data structure
        song_data.append({'title': unique_identifier, 'artist': song_field})

    # Create a DataFrame or structure the data as needed for the Apriori algorithm
    # This step depends on your specific data format

    return song_data
