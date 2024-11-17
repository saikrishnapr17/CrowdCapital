from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import os

app = Flask(__name__)

try:
    firebase_admin.get_app()
except ValueError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(current_dir, "serviceapi.json")
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

from user_functions import create_user, get_user_by_id, deposit_money
from transaction_functions import create_transaction, transfer_money, get_transactions_by_user


# Initialize Flask app
CORS(app)

# User Endpoints
@app.route("/users/create", methods=["POST"])
def create_user_endpoint():
    data = request.json
    user = create_user(data["name"], data["phone_number"])
    return jsonify({"message": "User created successfully", "user": user}), 201

@app.route("/users/<user_id>/deposit", methods=["POST"])
def deposit_money_endpoint(user_id):
    data = request.json
    amount = data["amount"]

    try:
        new_balance = deposit_money(user_id, amount)
        create_transaction(user_id, "deposit", amount)
        return jsonify({"message": "Deposit successful", "new_balance": new_balance}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Transaction Endpoints
@app.route("/transactions/transfer", methods=["POST"])
def transfer_money_endpoint():
    data = request.json
    sender_id = data["sender_id"]
    recipient_phone = data["recipient_phone"]
    amount = data["amount"]

    try:
        balances = transfer_money(sender_id, recipient_phone, amount)
        return jsonify({"message": "Transfer successful", "balances": balances}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/transactions/user/<user_id>", methods=["GET"])
def get_transactions_endpoint(user_id):
    transactions = get_transactions_by_user(user_id)
    if not transactions:
        return jsonify({"message": "No transactions found"}), 404
    return jsonify(transactions), 200


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
