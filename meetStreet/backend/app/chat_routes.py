# from flask_socketio import join_room, leave_room, send, SocketIO
# from flask import Blueprint, Flask, request, jsonify, session, redirect, url_for
# import random
# from string import ascii_uppercase

# chat_routes_blueprint = Blueprint('chat_routes', __name__)

# app = Flask(__name__)

# socketio = SocketIO(app)

# rooms = {}

# def generate_unique_code(length):
#     while True:
#         code = ""
#         for _ in range(length):
#             code += random.choice(ascii_uppercase)
        
#         if code not in rooms:
#             break
    
#     return code

# @chat_routes_blueprint.route("/chat_setting", methods=["POST", "GET"])
# def chat_setting():
#     session.clear()
#     if request.method == "POST":
#         name = request.form.get("name")
#         code = request.form.get("code")
#         join = request.form.get("join", False)
#         create = request.form.get("create", False)

#         # if not name:
#         #     return render_template("home.html", error="Please enter a name.", code=code, name=name)

#         # if join != False and not code:
#         #     return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
#         room = code
#         if create != False:
#             room = generate_unique_code(4)
#             rooms[room] = {"members": 0, "messages": []}
#         elif code not in rooms:
#             # print("Code is not in a room")
#             return "Code is not in a room"
#             # return redirect(url_for("chat_setting"))
        
#         session["room"] = room
#         session["name"] = name
#         return redirect(url_for("room"))
#         # print("Got to room")
#         # return "Got to room"

#     # print("successfully allocated")
#     return redirect(url_for("room"))
#     # return "successfully allocated"
#     # return redirect(url_for("room"))

# @chat_routes_blueprint.route("/room")
# def room():
#     room = session.get("room")
#     if room is None or session.get("name") is None or room not in rooms:
#         # return redirect(url_for("chat_setting"))
#         return "Wow"
#     message = rooms[room]["messages"]
#     return f"code={room}, message={message}"
#     # return render_template("room.html", code=room, messages=rooms[room]["messages"])

# @socketio.on("message")
# def message(data):
#     room = session.get("room")
#     if room not in rooms:
#         return 
    
#     content = {
#         "name": session.get("name"),
#         "message": data["data"]
#     }
#     send(content, to=room)
#     rooms[room]["messages"].append(content)
#     f"{session.get('name')} said: {data['data']}"

# @socketio.on("connect")
# def connect(auth):
#     room = session.get("room")
#     name = session.get("name")
#     if not room or not name:
#         return
#     if room not in rooms:
#         leave_room(room)
#         return
    
#     join_room(room)
#     send({"name": name, "message": "has entered the room"}, to=room)
#     rooms[room]["members"] += 1
#     print(f"{name} joined room {room}")

# @socketio.on("disconnect")
# def disconnect():
#     room = session.get("room")
#     name = session.get("name")
#     leave_room(room)

#     if room in rooms:
#         rooms[room]["members"] -= 1
#         if rooms[room]["members"] <= 0:
#             del rooms[room]
    
#     send({"name": name, "message": "has left the room"}, to=room)
#     print(f"{name} has left the room {room}")

# if __name__ == "__main__":
#     socketio.run(app, debug=True)