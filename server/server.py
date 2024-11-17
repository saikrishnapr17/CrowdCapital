from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import os
import statistics

app = Flask(__name__)

try:
    firebase_admin.get_app()
except ValueError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(current_dir, "serviceapi.json")
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

from fraudLLM import fraud_detection
from user_functions import create_user, get_user_by_id, deposit_money, get_wallet_balance
from transaction_functions import create_transaction, transfer_money, get_transactions_by_user
from community_functions import (
    contribute_to_community,
    request_loan,
    approve_or_deny_loan,
    make_loan_payment,
    withdraw_from_community,
    get_community_interest
)

from investment_functions import enlist_business, invest_in_business, get_business_investments, get_all_business_ids

# Initialize Flask app
CORS(app)

# User Endpoints
@app.route("/fraud", methods=["POST"])
def fraudcheck():
    data = request.json
    message = data["message"]
    result = fraud_detection(message)
    return jsonify(result)

@app.route("/users/create", methods=["POST"])
def create_user_endpoint():
    data = request.json
    user = create_user(data["name"], data["phone_number"])
    return jsonify({"message": "User created successfully", "user": user}), 201

@app.route("/users/<user_id>/deposit", methods=["POST"])
def deposit_money_endpoint(user_id):
    data = request.json
    amount = int(data["amount"])

    try:
        new_balance = deposit_money(user_id, amount)
        create_transaction(user_id, "deposit", amount)
        return jsonify({"message": "Deposit successful", "new_balance": new_balance}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/<user_id>/wallet_balance", methods=["GET"])
def get_wallet_balance_endpoint(user_id):
    """Endpoint to get the wallet balance of a user."""
    try:
        balance = get_wallet_balance(user_id)
        return jsonify(balance), 200
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

@app.route('/firebase/')
def get_users(user_id):
    user_ref = db.collection('user').document(user_id)  
    doc = user_ref.get()
    return doc.to_dict()

@app.route('/credit/<user_id>')
def get_user_credit(user_id):
    transactions = get_transactions_by_user(user_id)
    user = get_users(user_id)
    transaction_count = len(transactions)
    max_transactions_per_month = 30
    frequency_score = (transaction_count / max_transactions_per_month)
    repayment_score = user['repayment_rate'] * 425 # 50% weights
    amounts = [tx['amount'] for tx in transactions]
    if len(amounts) > 1:
        # Calculate standard deviation of transaction amounts
        transaction_stdev = statistics.stdev(amounts)
        # Inverse of standard deviation (scaled)
        transaction_stability_score = (1 / (1 + transaction_stdev))
    else:
        transaction_stability_score = 100 
    total_transaction_amount = sum(amounts)
    savings_score = (total_transaction_amount * 0.20) / total_transaction_amount
    community_score = user['community_rating'] * 10/100
    total_debt = user['current_debt'] 
    total_income = user['avg_income'] 
    debt_to_income_ratio = total_debt / total_income
    debt_to_income_score = max(0, 1 - (debt_to_income_ratio))

    weights = {
        'frequency': 42.5, # 5% weight
        'stability': 127.5, # 15% weight
        'savings': 85, # 10% weight
        'community': 85, # 10% weight
        'debt_to_income': 85 # 10% weight
    }

    # Calculate final credit score
    final_credit_score = (
        frequency_score * weights['frequency'] +
        repayment_score +
        transaction_stability_score * weights['stability'] +
        savings_score * weights['savings'] +
        community_score * weights['community'] +
        debt_to_income_score * weights['debt_to_income']
    )
    print(frequency_score * weights['frequency'])
    print(repayment_score)
    print(transaction_stability_score * weights['stability'])
    print(savings_score * weights['savings'])
    print(community_score * weights['community'])
    print(debt_to_income_score * weights['debt_to_income'])

    return jsonify({
        'credit_score': final_credit_score
    })


#community endpoints
@app.route("/community/<user_id>/contribute", methods=["POST"])
def contribute_to_community_endpoint(user_id):
    """Endpoint for contributing to the community fund."""
    data = request.json
    amount = data["amount"]

    try:
        community = contribute_to_community(user_id, amount)
        return jsonify({"message": "Contribution successful", "community": community}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/community/<user_id>/request_loan", methods=["POST"])
def request_loan_endpoint(user_id):
    """Endpoint for requesting a loan."""
    data = request.json
    amount = data["amount"]
    description = data["description"]
    credit_score = data["credit_score"]

    try:
        loan_request = request_loan(user_id, amount, description, credit_score)
        return jsonify({"message": "Loan request created", "loan_request": loan_request}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/community/<user_id>/approve_or_deny_loan", methods=["POST"])
def approve_or_deny_loan_endpoint(user_id):
    """Endpoint for approving or denying a loan."""
    data = request.json
    loan_id = data["loan_id"]
    approve = data.get("approve", True)

    try:
        loan = approve_or_deny_loan(user_id, loan_id, approve)
        return jsonify({"message": "Loan decision recorded", "loan": loan}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/community/<user_id>/make_payment", methods=["POST"])
def make_loan_payment_endpoint(user_id):
    """Endpoint for making a loan payment."""
    data = request.json
    loan_id = data["loan_id"]
    payment_amount = data["payment_amount"]

    try:
        loan = make_loan_payment(user_id, loan_id, payment_amount)
        return jsonify({"message": "Payment successful", "loan": loan}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/community/<user_id>/withdraw", methods=["POST"])
def withdraw_from_community_endpoint(user_id):
    """Endpoint for withdrawing contributions from the community fund."""
    data = request.json
    amount = data["amount"]

    try:
        community = withdraw_from_community(user_id, amount)
        return jsonify({"message": "Withdrawal successful", "community": community}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/community/interest", methods=["GET"])
def get_community_interest_endpoint():
    """Endpoint to get the total interest earned for the community."""
    try:
        result = get_community_interest()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Investment Endpoints
@app.route("/businesses", methods=["GET"])
def get_all_business_ids_endpoint():
    """Endpoint to retrieve all business IDs."""
    try:
        business_ids = get_all_business_ids()
        return jsonify(business_ids), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/business/enlist", methods=["POST"])
def enlist_business_endpoint():
    """Endpoint for enlisting a business."""
    data = request.json
    owner_id = data["owner_id"]
    business_name = data["business_name"]
    description = data["description"]
    goal = data["goal"]
    equity = data["equity"]

    try:
        business = enlist_business(owner_id, business_name, description, goal, equity)
        return jsonify({"message": "Business enlisted successfully", "business": business}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/business/<business_id>/invest", methods=["POST"])
def invest_in_business_endpoint(business_id):
    """Endpoint for investing in a business."""
    data = request.json
    user_id = data["user_id"]
    amount_invested = data["amount_invested"]

    try:
        result = invest_in_business(user_id, business_id, amount_invested)
        return jsonify({"message": "Investment successful", "result": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/business/<business_id>/investments", methods=["GET"])
def get_business_investments_endpoint(business_id):
    """Endpoint for viewing all investments for a business."""
    try:
        stakeholders = get_business_investments(business_id)
        return jsonify({"stakeholders": stakeholders}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
