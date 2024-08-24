from flask import Flask, request, jsonify
from pymongo import MongoClient
from geopy.distance import geodesic

app = Flask(__name__)

# Connect to MongoDB
cluster = MongoClient("mongodb+srv://varrentnw:yI08Qp3CU8ihC22V@cluster0.g11mii6.mongodb.net/")
db = cluster["userProfile"]
collection = db["userProfile"]

@app.route('/user/discover', methods=['GET'])
def discover_nearby_users():


    # Parse the request JSON data
    data = request.get_json()

    # Extract the user_id, coordinates, and radius
    user_id = data.get('user_id')
    coordinates = data.get('coordinates', {})
    lat = coordinates.get('lat')
    lng = coordinates.get('lng')
    radius = data.get('radius', 1)  # Default radius is 1 kilometer if not provided

    # Validate required fields
    if not user_id or lat is None or lng is None:
        return jsonify({'error': 'Missing required fields'}), 400

    # Define the user's location
    user_location = (lat, lng)

    # Find nearby users within the specified radius
    nearby_users = []
    for user in collection.find({'_id': {'$ne': user_id}}):
        user_lat = user.get('latitude')
        user_lng = user.get('longitude')
        
        if user_lat is not None and user_lng is not None:
            other_user_location = (user_lat, user_lng)
            distance = geodesic(user_location, other_user_location).kilometers
            
            if distance <= radius:
                nearby_users.append({
                    'user_id': user['_id'],
                    'name' : user['name'],
                    'picture' : user['picture'],
                    'latitude': user_lat,
                    'longitude': user_lng,
                    'friends' : user['friends'],
                    'distance_km': distance
                })

    return jsonify({'nearby_users': nearby_users}), 200

if __name__ == '__main__':
    app.run(debug=True)
