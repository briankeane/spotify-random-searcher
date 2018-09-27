from flask import Flask, redirect, url_for, request, render_template
import os
from db.db import Database

app = Flask(__name__)
PORT = os.environ.get('PORT') or 5000

dbHandler = Database()

@app.route('/')
def showSummary():
  playlists = dbHandler.get_top_playlists()
  user_count = dbHandler.user_count()
  playlist_count = dbHandler.playlist_count()
  print('user count')
  print(user_count)
  print('playlist_count:')
  print(playlist_count)

  for playlist in playlists:
    print(playlist['name'])
    playlist['image_link'] = ''
    if (playlist['images'] and len(playlist['images']) > 0):
      playlist['image_link'] = playlist['images'][0]['url']
  print('length playlists: ')
  print(playlists.count())
  return render_template('summary.html', playlists=playlists, user_count=user_count, playlist_count=playlist_count)


@app.route('/new', methods=['POST'])
def new():

  return redirect(url_for('todo'))


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT, debug=True)