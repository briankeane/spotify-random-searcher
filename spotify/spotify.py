import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging
import random

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

  def get_random_words(self, count):
    file = open('commonWords.txt')
    all_words = file.read().splitlines()
    chosen_words = []
    for i in range(count):
      chosen_words.append(random.choice(all_words))
    file.close()
    return chosen_words

  def get_random_phrase(self):
    word_count = random.randint(1,3)
    phrase = " ".join(self.get_random_words(word_count))
    return phrase

  def get_full_playlists_for_random_search(self):
    random_phrase = self.get_random_phrase()
    response = self.sp.search(random_phrase, type='playlist', limit=50)
    playlists= []
    if response["playlists"] is not None:
      if (response["playlists"]["items"]):
        playlists = response["playlists"]['items']
        for i, playlist in enumerate(playlists):
          new_playlist = self.sp._get('playlists/' + playlist['id'])
          new_playlist["discovered_by_phrase"] = random_phrase
          if new_playlist:
            playlists[i] = { **playlist, **new_playlist }
    print(str(len(playlists)) + " found for phrase: " + random_phrase)
    return playlists


