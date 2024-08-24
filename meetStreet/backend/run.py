from flask import Flask, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv, find_dotenv
from flask_socketio import join_room, leave_room, send, SocketIO
import os
import pprint
from pymongo import MongoClient
import uuid
from bson import Binary
import random
from string import ascii_uppercase
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

# if __name__ == "__main__":
#     app.run(debug=True)

socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/chat_setting", methods=["POST", "GET"])
def chat_setting():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # if not name:
        #     return render_template("home.html", error="Please enter a name.", code=code, name=name)

        # if join != False and not code:
        #     return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            # print("Code is not in a room")
            return "Code is not in a room"
            # return redirect(url_for("chat_setting"))
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))
        # print("Got to room")
        # return "Got to room"

    # print("successfully allocated")
    return redirect(url_for("room"))
    # return "successfully allocated"
    # return redirect(url_for("room"))

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        # return redirect(url_for("chat_setting"))
        return "Wow"
    message = rooms[room]["messages"]
    return f"code={room}, message={message}"
    # return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    f"{session.get('name')} said: {data['data']}"

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)