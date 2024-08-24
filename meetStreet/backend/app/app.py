# app.py
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv, find_dotenv
import os

# Import routes from the different modules
from chat_routes import chat_routes_blueprint
from friends_routes import friend_routes_blueprint
from location_routes import location_routes_blueprint
from user_routes import user_routes_blueprint

# Load environment variables
load_dotenv(find_dotenv())

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_secret_key")
socketio = SocketIO(app)

# Register Blueprints
app.register_blueprint(chat_routes_blueprint, url_prefix='/chat')
app.register_blueprint(friend_routes_blueprint, url_prefix='/friend')
app.register_blueprint(location_routes_blueprint, url_prefix='/location')
app.register_blueprint(user_routes_blueprint, url_prefix='/user')

if __name__ == "__main__":
    socketio.run(app, debug=True)
