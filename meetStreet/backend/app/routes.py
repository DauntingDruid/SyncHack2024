# routes.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_database():
    password = os.environ.get("MONGODB_PWD")
    connection_string = f"mongodb+srv://tatsuNakaKun:{password}@test.0lcnvy3.mongodb.net/ourDatabase?retryWrites=true&w=majority&appName=test"
    client = MongoClient(connection_string)
    return client.ourDatabase

def person_profile():
    db = get_database()
    return db.person_profile
