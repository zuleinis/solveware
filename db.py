from flask import Flask
from flask_pymongo import pymongo
from app import app

CONNECTION_STRING = "mongodb+srv://bryanotero:elbryan@cluster0.zjrsb0m.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('example_db')
user_collection = pymongo.collection.Collection(db, 'user_collection')