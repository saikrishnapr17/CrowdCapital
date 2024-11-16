from flask import Flask, jsonify
from firebase_admin import credentials, firestore
import firebase_admin

app = Flask(__name__)

cred = credentials.Certificate("./serviceapi.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return "Hello, Flask from server.py!"

@app.route('/firebase')
def get_users():
    users_ref = db.collection('user')  
    docs = users_ref.stream()
    users = {doc.id: doc.to_dict() for doc in docs}
    
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
