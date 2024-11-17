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
from credit_prediction import prediction
from user_functions import create_user, get_user_by_id, deposit_money, get_wallet_balance
from transaction_functions import create_transaction, transfer_money, get_transactions_by_user
from community_functions import (
    contribute_to_community,
    request_loan,
    approve_or_deny_loan,
    make_loan_payment,
    withdraw_from_community,
    get_community_interest,
    calculate_emi,
    get_community_fund_details,
    get_all_pending_loans
)

from investment_functions import enlist_business, invest_in_business, get_business_investments, get_all_business_info

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

#@app.route('/credit/<user_id>')
def get_user_credit(user_id):
    """
    Calculate a user's credit score based on various factors with default values for missing or invalid data.
    """
    transactions = get_transactions_by_user(user_id)
    user = get_user_by_id(user_id)  # Ensure this fetches the correct user
    if not user:
        raise ValueError("User not found")

    # Ensure valid data for calculations
    transaction_count = len(transactions)
    total_income = user.get('avg_income', 1)  # Default to 1 to avoid division by zero
    total_debt = user.get('current_debt', 0)  # Default to 0
    completed_loans = user.get('completed_loans', 0)  # Default to 0
    repayment_rate = user.get('repayment_rate', 0) / 100  # Default to 0 and scale
    community_rating = user.get('community_rating', 0) / 100  # Default to 0 and scale

    # Transaction frequency score (max transactions per month = 30)
    max_transactions_per_month = 30
    frequency_score = min((transaction_count / max_transactions_per_month) * 100, 100)  # Capped at 100
    frequency_score = frequency_score if frequency_score else 50  # Default to 50 if invalid

    # Transaction stability score (inverse of standard deviation)
    amounts = [tx['amount'] for tx in transactions]
    if len(amounts) > 1:
        transaction_stdev = statistics.stdev(amounts)
        transaction_stability_score = max(0, (1 / (1 + transaction_stdev)) * 100)  # Capped at 100
    else:
        transaction_stability_score = 100  # Default for single transaction
    transaction_stability_score = transaction_stability_score if transaction_stability_score else 50

    # Savings score
    total_transaction_amount = sum(amounts)
    savings_score = (
        (total_transaction_amount * 0.20) / max(total_transaction_amount, 1) * 100
    )  # Default to 100 if invalid
    savings_score = savings_score if savings_score else 50

    # Debt-to-income score
    debt_to_income_ratio = total_debt / total_income
    debt_to_income_score = max(0, 100 - (debt_to_income_ratio * 100))  # Higher ratio = lower score
    debt_to_income_score = debt_to_income_score if debt_to_income_score else 50

    # Community engagement score
    community_score = community_rating * 100  # Scaled to 0-100
    community_score = community_score if community_score else 50

    # Repayment score (based on repayment rate)
    repayment_score = repayment_rate * 100  # Scaled to 0-100
    repayment_score = repayment_score if repayment_score else 50

    # Predictive model contribution (example function `prediction`)
    model_credit = prediction(total_income, completed_loans)

    # Define weights for components
    weights = {
        'frequency': 5,  # 5% weight
        'stability': 15,  # 15% weight
        'savings': 10,  # 10% weight
        'community': 10,  # 10% weight
        'debt_to_income': 10,  # 10% weight
        'repayment': 50  # 50% weight
    }

    # Calculate weighted credit score
    final_credit_score = (
        (frequency_score or 50) * weights['frequency'] +
        (transaction_stability_score or 50) * weights['stability'] +
        (savings_score or 50) * weights['savings'] +
        (community_score or 50) * weights['community'] +
        (debt_to_income_score or 50) * weights['debt_to_income'] +
        (repayment_score or 50) * weights['repayment']
    ) / sum(weights.values())  # Normalize by total weight sum

    # Combine with model prediction
    final_credit_score = (final_credit_score + model_credit) / 2

    # Return credit score, capped within a valid range (e.g., 300-850)
    return max(300, min(int(final_credit_score), 850))



#community endpoints

@app.route("/community/fund", methods=["GET"])
def get_community_fund():
    """
    Endpoint to retrieve community fund details.
    """
    try:
        # Retrieve community fund details
        community_details = get_community_fund_details()
        return jsonify({"community_fund": community_details}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


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

@app.route("/community/pending_loans", methods=["GET"])
def get_pending_loans_endpoint():
    """
    Endpoint to retrieve all pending loan requests.
    """
    try:
        pending_loans = get_all_pending_loans()
        return jsonify({
            "message": "Pending loans retrieved successfully",
            "pending_loans": pending_loans
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/community/<user_id>/request_loan", methods=["POST"])
def request_loan_endpoint(user_id):
    """Endpoint for requesting a loan."""
    data = request.json
    amount = data["amount"]
    description = data["description"]

    try:
        # Calculate the user's credit score dynamically
        credit_score = get_user_credit(user_id)

        # Calculate the EMI based on the credit score and loan amount
        emi = calculate_emi(amount, credit_score)

        # Create the loan request using the calculated credit score
        loan_request = request_loan(user_id, amount, description, credit_score)
        return jsonify({
            "message": "Loan request created",
            "loan_request": loan_request,
            "calculated_credit_score": credit_score,
            "emi": emi
        }), 201
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
@app.route("/businesses/info", methods=["GET"])
def get_all_business_info_endpoint():
    """Endpoint to retrieve all business information."""
    try:
        business_info = get_all_business_info()
        return jsonify(business_info), 200
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