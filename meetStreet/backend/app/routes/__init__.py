import pymongo
from pymongo import MongoClient
import os

def person_profile():
    # change the password for our database
    password = os.environ.get("MONGODB_PWD")

    # Change this string to the actual one
    connection_string = f"mongodb+srv://tatsuNakaKun:{password}@test.0lcnvy3.mongodb.net/ourDatabase?retryWrites=true&w=majority&appName=test"
    client = MongoClient(connection_string)

    dbs = client.list_database_names()
    test_db = client.ourDetabase
    collections = test_db.list_collection_names()
    # print(collections)

    # profile
    # ---------------------------------------------------------

    profile = client.profile
    person_profile = profile.person_profile

    return person_profile