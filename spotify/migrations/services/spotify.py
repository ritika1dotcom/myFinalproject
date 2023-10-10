import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from django.conf import settings

SPOTIPY_CLIENT_ID = settings.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = settings.SPOTIPY_CLIENT_SECRET
