# MeetStreet Project Overview

## P0 Targets:

### Abhishek (Frontend Lead)

**Tasks:**

1. **Login/Signup Page:**
   - Develop the UI for the login and signup pages.
   - Implement form validation and user input handling.
   - Integrate with the backend for user authentication and profile creation.

2. **Interactive Map (Home Screen):**
   - Implement a map UI to show live locations of users.
   - Display nearby users on the map based on the backend response.
   - Ensure smooth real-time updates based on user movement.

3. **Live Location Sender:**
   - Implement functionality to send the user’s live location to the backend every 30 seconds.
   - Ensure the location updates are synchronized with the backend.

4. **ChatBox**

### Tatsu (Backend Lead and DBMS)

**Tasks:**

1. **User Profile Management (Module 1):**
   - Set up the MongoDB database and implement the User profile creation.
   - Create APIs for creating, retrieving, and updating user profiles.
   - Ensure the user profile includes all required fields: UniqueID, Name, Profile Picture, Coordinates, Preferences, Friends.

2. **Friends Module (Module 3):**
   - Implement the friends' management feature where both users send Unique IDs to the database.
   - Create APIs for sending and receiving friend requests and updating friend lists in the database.

### Varrent (Backend & Location Updates)

**Tasks:**

1. **Location Receiver & Updater (Module 2):**
   - Develop the backend logic to receive and update user location coordinates in MongoDB.
   - Ensure the backend can handle frequent location updates efficiently.

2. **Coordinate Algorithm (Module 2):**
   - Develop the algorithm to find and return users within the specified radius based on coordinates.
   - Optimize the algorithm for performance and accuracy.

3. **Collaborate with Tatsu on the Coordinate Algorithm:**
   - Work together to integrate the real-time location updates with the algorithm.

4. **Assist with API Integration:**
   - Support Tatsu in ensuring that all APIs are integrated smoothly with the location and coordinate logic.

### Faiyad (Backend Developer & Real-time Communication)

**Tasks:**

1. **Real-time Chatbox (Module 4):**
   - Set up Flask-SocketIO for real-time communication between users.
   - Implement the chatbox feature with a 2-minute timer.
   - Add functionality for accepting or rejecting friend requests after the timer expires.

2. **Collaborate on Frontend Integration:**
   - Ensure that the chat functionality integrates well with the frontend, working with Abhishek to ensure a seamless user experience.

---------------------------------------------------------------------------------------------------------------------------------------

## Comprehensive API Specification for MeetStreet

### 1. User Authentication (Login/Signup)

**Endpoint:** `/signup` (POST)  
**Description:** Registers a new user and creates their profile in the database.  
**Request Fields:**
- `name` (string, required) - User’s full name.
- `email` (string, required) - User’s email address.
- `password` (string, required) - User’s password.
- `profile_picture` (file, optional) - User’s profile picture (selfie).
- `preferences` (object, optional)
- `radius` (number, optional) - The preferred radius to find people (in kilometers).
- `interests` (array of strings, optional) - User’s interests (e.g., "music", "sports").

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)

**Endpoint:** `/login` (POST)  
**Description:** Authenticates the user and initiates a session.  
**Request Fields:**
- `email` (string, required) - User’s email address.
- `password` (string, required) - User’s password.

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)

### 2. User Profile Management

**Endpoint:** `/user/profile` (GET)  
**Description:** Retrieves the current user's profile details.  
**Request Fields:**
- `UniqueID` (string, required) - Matches ID in the Table and Sends it back to the frontend.

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)

**Endpoint:** `/user/profile` (PUT)  
**Description:** Updates the user’s profile information.  
**Request Fields:**
- `name` (string, optional) - Updated name.
- `profile_picture` (file, optional) - Updated profile picture.
- `preferences` (object, optional)
- `radius` (number, optional) - Updated radius to find people.
- `interests` (array of strings, optional) - Updated list of interests.

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)

### 3. Live Location Updates

**Endpoint:** `/user/location` (POST)  
**Description:** Sends the user’s live location to the backend every 30 seconds.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the user.
- `coordinates` (object, required)
  - `lat` (number, required) - Latitude of the user.
  - `lng` (number, required) - Longitude of the user.

**Handled By:** Varrent (Backend), Abhishek (Frontend integration)

**Endpoint:** `/user/location/update` (PUT)  
**Description:** Updates the user’s location in the database.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the user.
- `coordinates` (object, required)
  - `lat` (number, required) - Latitude of the user.
  - `lng` (number, required) - Longitude of the user.

**Handled By:** Varrent (Backend), Abhishek (Frontend integration)

### 4. User Discovery (Based on Preferences and Location)

**Endpoint:** `/user/discover` (POST)  
**Description:** Retrieves a list of nearby users based on the current user’s location and preferences.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the user.
- `coordinates` (object, required)
  - `lat` (number, required) - Latitude of the user.
  - `lng` (number, required) - Longitude of the user.
- `radius` (number, optional) - Radius to search for nearby users.

**Handled By:** Tatsu (Backend), Varrent (Algorithm)

### 5. Friend Management

**Endpoint:** `/friend/request` (POST)  
**Description:** Sends a friend request to another user.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the user sending the request.
- `friend_id` (string, required) - Unique ID of the user receiving the request.

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)

**Endpoint:** `/friend/accept` (PUT)  
**Description:** Accepts a friend request from another user.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the user accepting the request.
- `friend_id` (string, required) - Unique ID of the user who sent the request.

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)

**Endpoint:** `/friend/reject` (PUT)  
**Description:** Rejects a friend request from another user.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the user rejecting the request.
- `friend_id` (string, required) - Unique ID of the user who sent the request.

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)

### 6. Real-Time Chatbox

**Endpoint:** `/chat/initiate` (POST)  
**Description:** Initiates a chat session between two users.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the initiating user.
- `friend_id` (string, required) - Unique ID of the other user.

**Handled By:** Faiyad (Backend & Real-time communication), Abhishek (Frontend integration)

**Endpoint:** `/chat/send` (POST)  
**Description:** Sends a message in the chat session.  
**Request Fields:**
- `chat_id` (string, required) - Unique ID of the chat session.
- `sender_id` (string, required) - Unique ID of the user sending the message.
- `message` (string, required) - The message content.

**Handled By:** Faiyad (Backend & Real-time communication), Abhishek (Frontend integration)

**Endpoint:** `/chat/end` (PUT)  
**Description:** Ends the chat session after the 2-minute timer, allowing the user to accept or reject the friend request.  
**Request Fields:**
- `chat_id` (string, required) - Unique ID of the chat session.
- `decision` (string, required) - User’s decision: "accept" or "reject".

**Handled By:** Faiyad (Backend & Real-time communication), Abhishek (Frontend integration)

### 7. Miscellaneous

**Endpoint:** `/settings/update` (PUT)  
**Description:** Updates the user’s app settings.  
**Request Fields:**
- `user_id` (string, required) - Unique ID of the user.
- `settings` (object, required) - Various settings fields like notifications, privacy preferences, etc.

**Handled By:** Tatsu (Backend), Abhishek (Frontend integration)
