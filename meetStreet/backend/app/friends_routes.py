from flask import Blueprint, Flask, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv, find_dotenv
from flask_socketio import join_room, leave_room, send, SocketIO
import os
import pprint
from pymongo import MongoClient
import uuid
from bson import Binary
from string import ascii_uppercase
from routes import person_profile

friend_routes_blueprint = Blueprint('friend_routes', __name__)

load_dotenv(find_dotenv())

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return "Hello Flask"


person_profile = person_profile()

# Register 
def register_user(data):
    try:
        doc = {
            "_id": str(uuid.uuid4()),
            "name": data['name'],
            "age": data['age'],
            "gender": data['gender'],
            "email": data['email'],
            "password": data['password'],
            "profile_picture": data['profile_picture'],
            "radius": data['radius'], #integer
            "interests": data['interests'], #array of strings
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

@friend_routes_blueprint.route('/deleteAll', methods=["DELETE"])
def delete():
    try:
        result = person_profile.delete_many({})
        return jsonify({"message": f"Successfully deleted {result.deleted_count} documents."}), 200
    except Exception as error:
        return jsonify({"error": "Error"}), 500

# login & signup
@friend_routes_blueprint.route('/profile', methods=["GET", "POST"])
def testing():
    if request.method == "POST":
        data = request.get_json()
        # data = {
        #     "name": "Tatsuya",
        #     "age": 10,
        #     "password": "jfdsaofsf",
        #     "gender": "M",
        #     "email": "education@gmail.com",
        #     "profile_picture": "img01.png",
        #     "radius": 100,
        #     "interests": [
        #         "Eating", "Jogging", "Dancing", "Drinking"
        #     ],
        #     "friends": [
        #         ""
        #     ],
        #     "friendRequestID": "",
        #     "isFriendRequest": False,
        # }
        if data:
            res = register_user(data)
            return res, 200
        else:
            return jsonify({"error": "No data provided"}), 400
    
    else:
        try:
            data = person_profile.find()
            doc = []
            for document in data:
                printer.pprint(document)
                doc.append(document)
            print(f"Success")
            return jsonify(doc[0])
        except Exception as error:
            print(f"Error: {error}")
            return {}

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
@friend_routes_blueprint.route('/friend-request', methods=["POST"])
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
@friend_routes_blueprint.route("/friend-request-accept", methods=["PUT"])
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
@friend_routes_blueprint.route("/friend-request-reject", methods=["PUT"])
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
@friend_routes_blueprint.route("/setting/<id>", methods=["PUT"])
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

# if __name__ == "__main__":
#     app.run(debug=True)
