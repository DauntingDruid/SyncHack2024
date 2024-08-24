from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import uuid
from bson import Binary
load_dotenv(find_dotenv())

app = Flask(__name__)
app.config["SECRET_KEY"] = "foieajf fdfsjofsdp"

@app.route('/', methods=["GET"])
def home():
    return "Hello Flask"

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

# Register 
def register_user(data):
    try:
        doc = {
            "_id": str(uuid.uuid4()),
            "name": data['name'],
            "age": data['age'],
            "gender": data['gender'],
            "email": data['email'],
            "profile_picture": data['profile_picture'],
            "preferences": {
                "radius": data['preferences']['radius'],
                "interests": data['preferences']['interests'],
            },
            "friends": data['friends'],
            "friendRequestID": data['friendRequestID'],
            "isFriendRequest": data['isFriendRequest'],
        }
        # print(doc)
        result = person_profile.insert_one(doc)
        print(f"Document inserted with _id: {result.inserted_id}")
        return result.inserted_id
    except Exception as error:
        print(f"Error inserting document: {error}")
        return "Error"

# to get a better format
printer = pprint.PrettyPrinter()

@app.route('/deleteAll', methods=["DELETE"])
def delete():
    try:
        result = person_profile.delete_many({})
        return jsonify({"message": f"Successfully deleted {result.deleted_count} documents."}), 200
    except Exception as error:
        return jsonify({"error": "Error"}), 500

@app.route('/profile', methods=["GET", "POST"])
def testing():
    if request.method == "POST":
        # data = request.get_json()
        data = {
            "name": "Tatsuya",
            "age": 10,
            "gender": "M",
            "email": "education@gmail.com",
            "profile_picture": "img01.png",
            "preferences": {
                "radius": 100,
                "interests": [
                    "Eating", "Jogging", "Dancing", "Drinking"
                ]
            },
            "friends": [
                ""
            ],
            "friendRequestID": "",
            "isFriendRequest": False,
        }
        if data:
            res = register_user(data)
            return res, 200
        else:
            return jsonify({"error": "No data provided"}), 400
    
    else:
        try:
            data = person_profile.find()
            for document in data:
                printer.pprint(document)
            print(f"Success")
        except Exception as error:
            print(f"Error: {error}")
        return "Getting your item"

# ------------------------------------------------

# friends
# -----------------------------------------------
# friends = client.friends
# friends_profile = friends.friends_profile

# Find a friend id
def find_id(id):
    try:
        return person_profile.find({"_id": id})
    except Exception as error:
        return False

def updateFriendRequest(request_id, friend_id):
    try: 
        update = {
            "$set": {"new_field": True, "isFriendRequest": True, "friendRequestID": friend_id},
        }
        result = person_profile.update_one({"_id": request_id}, update)
        # print(result)
        if result.matched_count == 0:
            print(f"None")
            # print("Fuck")
        elif result.modified_count == 0:
            print("Not Modified")
        else:
            updated_user = person_profile.find_one({"_id": request_id})
            print("Updated Document: ", updated_user)
    except Exception as error:
        print(f"Error: {error}")

# send a request (get user_id and friend_id from Front-end)
@app.route('/friend-request', methods=["POST"])
def friend_request():
    user_id = "c1b924ff-7d11-48fb-85d3-d34e7bbde6f0"
    friend_id = "a7b6f24d-916d-4b82-8bb8-ebac11817ca7"
    if find_id(friend_id) and find_id(user_id):
        updateFriendRequest(user_id, friend_id)
        return jsonify({"message": "Friend request sent successfully"}), 200
    else:
        return jsonify({"error": "Friend request did not send successfully"}), 404

def addFriends(id, friend_id):
    try:
        update = {
            "$set": {
                "new_field": True, 
                "isFriendRequest": False,
                "friendRequestID": "",    
            },
            "$push": {
                "friends": friend_id,
            }
        }
        result = person_profile.update_one({"_id": id}, update)
        if result.matched_count == 0:
            print(f"None")
            # print("Fuck")
        elif result.modified_count == 0:
            print("Not Modified")
        else:
            updated_user = person_profile.find_one({"_id": id})
            print("Updated Document: ", updated_user)
    except Exception as error:
        print(f"there are some errors: {error}")
    
# accept
@app.route("/friend-request-accept", methods=["PUT"])
def accept():
    user_id = "a7b6f24d-916d-4b82-8bb8-ebac11817ca7"
    request_id = "c1b924ff-7d11-48fb-85d3-d34e7bbde6f0"
    
    if find_id(user_id) and find_id(request_id):
        updateFriendRequest(user_id, request_id)
        # user_data = person_profile.find_one({"_id": user_id})
        # request_data = person_profile.find_one({"_id": request_id})
        # return jsonify({"message": {user_data}})
        addFriends(user_id, request_id)
        addFriends(request_id, user_id)
        return jsonify({"message": "Success"})
        # if user_data['isFriendRequest'] and request_data['isFriendRequest']:
        #     addFriends(user_id, request_id)
        #     addFriends(request_id, user_id)
        #     return jsonify({"message": "Success"})
        # else:
        #     return jsonify({"message": "Not work"})
        # if user_data['isFriendRequest'] and friend_data['isFriendRequest']:     
        #     addFriends(user_data)
        #     addFriends(friend_data)
        # print(user_data)
        # print(friend_data)
        # print("Success")
        # return jsonify({"message": f"{user_data['_id']}, {request_data}, Success"}), 200
    else:
        return jsonify({"error": "Error"}), 500

def rejectRequest(id):
    try:
        update = {
            "$set": {
                "new_field": True, 
                "isFriendRequest": False,
                "friendRequestID": "",
            },
        }
        result = person_profile.update_one({"_id": id}, update)
        if result.matched_count == 0:
            print(f"None")
            # print("Fuck")
        elif result.modified_count == 0:
            print("Not Modified")
        else:
            updated_user = person_profile.find_one({"_id": id})
            print("Updated Document: ", updated_user)
    except Exception as error:
        print(f"there are some errors: {error}")
    
# reject
@app.route("/friend-request-reject", methods=["PUT"])
def reject():
    request_id = "c1b924ff-7d11-48fb-85d3-d34e7bbde6f0"
    if (find_id(request_id)):
        rejectRequest(request_id)
        return jsonify({"message": "Successfully reject the friend request"})
    else:
        return jsonify({"error": "Error"})
    
# -----------------------------------------------

# Update a profile
def updateProfile(id, data):
    try:
        update_data = {"$set": data}
        result = person_profile.update_one({"_id": id}, update_data)
        if result.matched_count == 0:
            print(f"None")
            # print("Fuck")
        elif result.modified_count == 0:
            print("Not Modified")
        else:
            updated_user = person_profile.find_one({"_id": id})
            print("Updated Document: ", updated_user)
    except Exception as error:
        print(f"Error: {error}")

# Miscellaneous
@app.route("/setting/<id>", methods=["PUT"])
def setting(id):
    try:
        user_id = id
        # data = request.get_json()
        data = {
            "name": "Sasaki",
            "age": 20,
            "gender": "M",
            "email": "education@gmail.com",
            "profile_picture": "img01.png",
            "preferences": {
                "radius": 500,
                "interests": [
                    "Eating", "Jogging", "Drinking"
                ]
            },
            "friends": [
                ""
            ],
            "friendRequestID": "",
            "isFriendRequest": False,
        }
        updateProfile(user_id, data)
        return jsonify({"id": id, "data": data}), 200
    except Exception as error:
        return jsonify({"error": "No data provided"}), 400

# ------------------------------------------------------------

# def insert_test_doc():
#     collection = test_db.myDatabase
#     test_document = {
#         "name": "Tim",
#         "type": "Test"
#     }
#     inserted_id = collection.insert_one(test_document).inserted_id
#     print(inserted_id)

# # insert_test_doc()

# # automatically created a table
# production = client.production
# # automatically created person_collection if it does not exist
# person_collection = production.person_collection

# def create_docuemnts():
#     first_names = ["Time", "Sarah", "Jannifer", "Jose", "Brad", "Allen"]
#     last_names = ["Ruscica", "Smith", "Bart", "Cater", "Pit", "Geral"]
#     ages = [21, 40, 23, 19, 34, 67]

#     docs = []
#     for first_name, last_name, age in zip(first_names, last_names, ages):
#         doc = {"first_name": first_name, "last_name": last_name, "age": age}
#         docs.append(doc)
#         # person_collection.insert_one(doc)
#     person_collection.insert_many(docs)

# # create_docuemnts()

# def find_all_people():
#     people = person_collection.find()
#     for person in people:
#         printer.pprint(person)

# # find_all_people()

# def find_tim():
#     tim = person_collection.find_one({"first_name": "Time"})
#     printer.pprint(tim)
# # find_tim()

# def count_all_people():
#     # We can write both 
#     count = person_collection.count_documents(filter={})
#     print("Number of people, ", count)
# # count_all_people()

# def get_person_by_id(person_id):
#     from bson.objectid import ObjectId
#     _id = ObjectId(person_id)
#     person = person_collection.find_one({"_id": _id})
#     printer.pprint(person)

# # get_person_by_id("66c9afb734ab4ddcd7193a3a")

# # gte greater than or eeual to 
# def get_age_range(min_age, max_age):
#     query = {"$and": [
#         {"age": {"$gte": min_age}},
#         {"age": {"$lte": max_age}}
#     ]}
#     people = person_collection.find(query).sort("age")
#     for person in people:
#         printer.pprint(person)
        
# # get_age_range(20, 35)

# # _id: 0 do not need to have this id 1 need
# def project_columns():
#     columns = {"_id": 0, "first_name": 1, "last_name": 1}
#     people = person_collection.find({}, columns)
#     for person in people:
#         printer.pprint(person)

# # project_columns()

# def update_person_by_id(person_id):
#     from bson.objectid import ObjectId
#     _id = ObjectId(person_id)
#     # inc: increment by 1
#     # all_updates = {
#     #     "$set": {"new_field": True},
#     #     "$inc": {"age": 1},
#     #     "$rename": {"first_name": "first"}
#     # }
#     # person_collection.update_one({"_id": _id}, all_updates) 
    
#     # remove the person
#     person_collection.update_one({"_id": _id}, {"$unset": {"new_field": ""}})  
    
# # replace a document
# def replace_one(person_id):
#     from bson.objectid import ObjectId
#     _id = ObjectId(person_id)
    
#     new_doc = {
#         "first_name": "new first name",
#         "last_name": "new last name",
#         "age": 100
#     }
#     person_collection.update_one({"_id": _id}, new_doc)
    
# # delete 
# def delete_doc_by_id(person_id):
#     from bson.objectid import ObjectId
#     _id = ObjectId(person_id)
#     person_collection.delete_one({"_id": _id})
    
# @app.route('/get-items', methods=["GET"])
# def items():
#     # project_columns()
#     # update_person_by_id("66c9aeff217629086ae1152d")
#     return "True"



if __name__ == "__main__":
    app.run(debug=True)