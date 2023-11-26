from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth, db

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://myapp-a0cd7-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://myapp-a0cd7.appspot.com'
})

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    print(data);
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
        # Use Firebase's built-in email/password authentication method
        ref = db.reference('users/' + user.uid)
        userData =ref.get()
        # print(userData)
        if userData["password"]== password :
            return jsonify({"message": "User logged in successfully", "user": userData})    
        else:
            return jsonify({"message": "User passowrd does'nt match"})
    except Exception as e:
        return jsonify({"message": "Login failed", "error": str(e)}), 400

# Store User Data Endpoint
@app.route('/store_data', methods=['POST'])
def store_user_data():
    data = request.get_json()
    email = data['email']
    user = auth.get_user_by_email(email)
    # Assuming 'users' is a collection in Firebase Realtime Database
    ref = db.reference('users/' + user.uid)
    ref.update(data)  # Store user data
    return jsonify({"message": "User data updated successfully"})


@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        data = request.get_json()
        email = data['email']

        user = auth.get_user_by_email(email)
        ref = db.reference('emergency/' + user.uid)
        ref.set(data)
        return jsonify({"message": "Media uploaded successfully"})

    except Exception as e:
        return jsonify({"message": "Upload failed", "error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
