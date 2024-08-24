import pymongo
from pymongo import MongoClient
from flask import Blueprint, Flask, request, jsonify
import os
from routes import person_profile

location_routes_blueprint = Blueprint('location_routes', __name__)

app = Flask(__name__)

person_profile = person_profile()

# Update location
@location_routes_blueprint.route('/user/location', methods=['POST'])
def update_user_location():
    # Parse the request JSON data
    data = request.get_json()

    # Extract the user_id and coordinates
    user_id = data.get('user_id')
    coordinates = data.get('coordinates', {})
    lat = coordinates.get('lat')
    lng = coordinates.get('lng')

    # Validate required fields
    if not user_id or lat is None or lng is None:
        return jsonify({'error': 'Missing required fields'}), 400

    # Update or insert user's location in the database
    result = person_profile.update_one(
        {'_id': user_id},
        {'$set': {'latitude': lat, 'longitude': lng}},
        upsert=True  # If user doesn't exist, insert a new document
    )

    if result.matched_count > 0:
        return jsonify({'message': 'Location updated successfully'}), 200
    else:
        return jsonify({'message': 'New location entry created successfully'}), 201
    
if __name__ == '__main__':
    app.run(debug=True)
    

