from flask import Flask
from flask_pymongo import pymongo
import app
import certifi

CONNECTION_STRING = "mongodb+srv://zuleinisramos:data@cluster0.zjrsb0m.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
db = client.get_database('example_db')
user_collection = pymongo.collection.Collection(db, 'user_collection')