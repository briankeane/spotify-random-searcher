import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
from db.db import Database
from spotify.spotify import Spotify
import time

DBHandler = Database()
SpotifyHandler = Spotify()

MAX_ID = 10

def run_search():
  while True:
    print('retrieving playlists for random phrase: ')
    playlists = SpotifyHandler.get_full_playlists_for_random_search()
    if len(playlists) > 0:
      for i, playlist in enumerate(playlists):
        print("storing... " + str(i+1) + " of " + str(len(playlists)) + " for phrase: " + playlist["discovered_by_phrase"])
        DBHandler.upsert_playlist({ 'id': playlist['id'] }, playlist)


def display_same_line(message):
  print(message.ljust(50), end="\r")

# @app.route('/')
# def todo():
#   return render_template('todo.html', items=items)



retries = 0
while retries < 1000:
  try:
    run_search()
  except:
    retries += 1
    print("exception experienced. sleeping for 5 secs... " + str(1000-retries) + " retries remaining")
    time.sleep(5)
# bind to port
PORT = os.environ.get('PORT') or 5000
app = Flask(__name__)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)