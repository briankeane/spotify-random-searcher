import unittest
import os
from db.db import Database
from pymongo import MongoClient
from urllib.parse import urlparse

MONGODB_URI = os.environ.get('MONGODB_URI') or "mongodb://db:27017/tododb"
PORT = os.environ.get('PORT') or 5000

class DatabaseTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    client = MongoClient(MONGODB_URI)
    cls.dbName = urlparse(MONGODB_URI).path[1:]
    cls.db = client[cls.dbName]
    cls.playlists_collection = cls.db['playlists']
    cls.playlists_collection.remove({})
    cls.dbHandler = Database()

  def test_clear_all(self):
    self.playlists_collection.insert_one({ 'test': 'testMessage' })
    self.dbHandler.clear_all()
    items = self.db[self.dbName].find()
    self.assertEqual(items.count(), 0)

  def test_upsert_one_record_exists(self):
    """
    it just updates a record if it already exists
    """

  def test_upsert_one_record_does_not_exist(self):
    """
    it just updates a record if it already exists
    """
    self.playlists_collection.insert_many([{ 
                                        'id': '123',
                                        'title': 'bob' 
                                      },
                                      {
                                        'id': '456',
                                        'title': 'bob2'
                                      }
                                      ])
    self.dbHandler.upsert_playlist({ 'id': '123' }, { 'id': '123', 'otherTitle': 'bobby' })
    record = self.playlists_collection.find_one({ 'id': '123' })
    # self.assertEqual(record['otherTitle'], 'bobby')

  def test_gets_max_id(self):
    self.playlists_collection.insert_many([{ 
                                        'id': '123',
                                        'title': 'bob' 
                                      },
                                      {
                                        'id': '456',
                                        'title': 'bob2'
                                      }
                                      ])
    item = self.playlists_collection.find_one(sort=[("id", -1)])
    self.assertEqual(item["id"], "456")

