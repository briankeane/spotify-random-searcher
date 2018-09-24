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
  starting_user_id = int(DBHandler.find_max_user_id())
  starting_user_id += 1

  MAX_ID = 1000000000

  for i in range(starting_user_id, MAX_ID):
    id_string = str(i).zfill(10)
    print('retrieving playlists for user: ' + id_string)
    playlists = SpotifyHandler.get_full_playlists_for_user(id_string)
    if len(playlists) > 0:
      for i, playlist in enumerate(playlists):
        print("storing... " + str(i+1) + " of " + str(len(playlists)) + " for spotifyUID: " + id_string)
        DBHandler.upsert_playlist({ 'id': playlist['id'] }, playlist)

    print("marking user " + id_string + " completed")
    DBHandler.upsert_user({ 'id': id_string }, { 'id': id_string, 'hasBeenSearched': True })


def display_same_line(message):
  print(message.ljust(50), end="\r")

# @app.route('/')
# def todo():
#   return render_template('todo.html', items=items)


# @app.route('/new', methods=['POST'])
# def new():
#     return redirect(url_for('todo'))
retries = 0
while retries < 1000:
  try:
    run_search()
  except:
    retries += 1
    print("exception experienced. sleeping for 5 secs... " + str(1000-retries) + " retries remaining")
    time.sleep(5)

# bind to port
app = Flask(__name__)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)