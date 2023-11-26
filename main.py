from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth, db

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://myapp-a0cd7.firebaseio.com'
})

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        ref = db.reference('users/' + user.uid)
        ref.set(data)  # Store user data
        return jsonify({"message": "User registered successfully", "user_id": user.uid})
    except Exception as e:
        return jsonify({"message": "Registration failed", "error": str(e)}), 400

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    try:
        user = auth.get_user_by_email(email)
        # You might want to handle password-based login differently with Firebase
        # This example uses a separate authentication method
        return jsonify({"message": "User logged in successfully", "user_id": user.uid})
    except Exception as e:
        return jsonify({"message": "Login failed", "error": str(e)}), 400

# Store User Data Endpoint
@app.route('/store_data', methods=['POST'])
def store_user_data():
    data = request.get_json()
    user_id = data['user_id']
    # Assuming 'users' is a collection in Firebase Realtime Database
    ref = db.reference('users/' + user_id)
    ref.set(data)  # Store user data
    return jsonify({"message": "User data stored successfully"})

if __name__ == '__main__':
    app.run(debug=True)
