import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import sys

app = Flask(__name__)

##  Set Environment variables
MONGO_URL = os.environ.get('MONGODB_URI')
PORT = os.environ.get('PORT')

if not PORT:
  PORT = 5000

if not MONGO_URL:
    MONGO_URL = "mongodb://db:27017";


## Connect to Mongodb
client = MongoClient(MONGO_URL)
db = client.tododb


@app.route('/')
def todo():
    _items = db.tododb.find()
    print("----------------------------items---------------------------", file=sys.stdout)
    print(_items, file=sys.stdout)

    items = [item for item in _items]

    return render_template('todo.html', items=items)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)