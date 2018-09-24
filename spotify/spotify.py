import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging

class Spotify:
  def __init__(self):
    self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

  def get_full_playlists_for_user(self, user_id):
    response = self.sp.user_playlists(user_id)
    playlists = response['items']
    for i, playlist in enumerate(playlists):
      new_playlist = self.sp._get('playlists/' + playlist['id'])
      if new_playlist:
        playlists[i] = { **playlist, **new_playlist }
    return playlists