from unittest.mock import MagicMock
import unittest
import spotipy
from spotify.spotify import Spotify
import json

class SpotifyTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.sp = Spotify()
    with open('spotify/test/spotify_user_playlist_response.json') as f:
      cls.user_playlists_response = json.load(f)

  def test_get_full_playlists_for_user(self):
    self.sp.sp.user_playlists = MagicMock(return_value=self.user_playlists_response)
    self.sp.sp._get = MagicMock(return_value={ 'id': 'myID', 'test': 'test' })
    print('im here')
    full_playlists = self.sp.get_full_playlists_for_user('myID')
    print(full_playlists)