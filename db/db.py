import os
from pymongo import MongoClient

from urllib.parse import urlparse

MONGODB_URI = os.environ.get('MONGODB_URI') or "mongodb://db:27017/tododb"
PORT = os.environ.get('PORT') or 5000

## Connect to Mongodb
client = MongoClient(MONGODB_URI)
dbName = urlparse(MONGODB_URI).path[1:]
db = client[dbName]

class Database:
  def __init__(self):
    self.client = MongoClient(MONGODB_URI)
    dbName = urlparse(MONGODB_URI).path[1:]
    self.db = self.client[dbName]
    self.Playlist = self.db['playlists']
    self.User = self.db['users']

  def clear_all(self):
    return self.db[dbName].remove({})

  def upsert_playlist(self, query, record):
    return self.Playlist.update(query, record, upsert=True)

  def upsert_user(self, query, record):
    return self.User.update(query, record, upsert=True)

  def find_one_user(self, query):
    return self.User.find(query)

  def find_max_user_id(self):
    user = self.User.find_one(sort=[("id", -1)])
    if not user:
      return "-1"
    return user["id"]