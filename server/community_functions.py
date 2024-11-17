import uuid
from datetime import datetime
from firebase_admin import firestore
from user_functions import get_user_by_id, update_user
from transaction_functions import create_transaction

db = firestore.client()

def contribute_to_community(user_id, amount):
    """Allows a user to contribute to the community fund."""
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    if user["wallet_balance"] < amount:
        raise ValueError("Insufficient balance")

    # Deduct from user balance
    new_balance = user["wallet_balance"] - amount
    update_user(user_id, {"wallet_balance": new_balance})

    # Update community fund
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community:
        community = {"total_balance": 0.0, "contributors": []}

    # Update total balance
    community["total_balance"] += amount

    # Update contributor info
    contributor = next((c for c in community["contributors"] if c["user_id"] == user_id), None)
    if contributor:
        contributor["amount"] += amount
    else:
        community["contributors"].append({"user_id": user_id, "amount": amount})

    # Save to Firestore
    community_ref.set(community)

    # Record transaction
    create_transaction(user_id, "contribution", amount)

    return community

def request_loan(user_id, amount, description, credit_score):
    """Allows a user to request a loan."""
    emi = calculate_emi(amount, credit_score)  # Function to calculate EMI

    loan_request = {
        "loan_id": str(uuid.uuid4()),
        "user_id": user_id,
        "amount": amount,
        "description": description,
        "emi": emi,
        "approval_percentage": 0.0,
        "status": "pending"
    }

    # Add to loan requests
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community:
        raise ValueError("Community fund does not exist")

    if community["total_balance"] < amount:
        raise ValueError("Requested amount exceeds available community funds")

    if "pending_loan_requests" not in community:
        community["pending_loan_requests"] = []
    community["pending_loan_requests"].append(loan_request)

    community_ref.set(community)
    return loan_request

def request_loan(user_id, amount, description, credit_score):
    """
    Allows a user to request a loan. EMI is calculated based on credit score.
    """
    emi = calculate_emi(amount, credit_score)

    loan_request = {
        "loan_id": str(uuid.uuid4()),
        "user_id": user_id,
        "amount": amount,
        "description": description,
        "emi": emi,
        "approval_percentage": 0.0,
        "status": "pending"
    }

    # Add to loan requests
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community:
        raise ValueError("Community fund does not exist")

    if community["total_balance"] < amount:
        raise ValueError("Requested amount exceeds available community funds")

    if "pending_loan_requests" not in community:
        community["pending_loan_requests"] = []
    community["pending_loan_requests"].append(loan_request)

    community_ref.set(community)

    # Add to loans collection
    db.collection("loans").document(loan_request["loan_id"]).set(loan_request)

    return loan_request


def approve_or_deny_loan(user_id, loan_id, approve=True):
    """Handles loan approval or denial."""
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community or "pending_loan_requests" not in community:
        raise ValueError("No pending loans found")

    loan = next((l for l in community["pending_loan_requests"] if l["loan_id"] == loan_id), None)
    if not loan:
        raise ValueError("Loan request not found")

    if loan["user_id"] == user_id:
        raise ValueError("Loan requester cannot approve their own loan")

    contributor = next((c for c in community["contributors"] if c["user_id"] == user_id), None)
    if not contributor:
        raise ValueError("Only contributors can vote on loans")

    total_contributions = sum(c["amount"] for c in community["contributors"])
    user_weight = (contributor["amount"] / total_contributions) * 100

    if approve:
        loan["approval_percentage"] += user_weight
        if loan["approval_percentage"] >= 60.0:
            community["pending_loan_requests"].remove(loan)
            if "active_loans" not in community:
                community["active_loans"] = []
            community["active_loans"].append(loan)
            loan["status"] = "approved"

            if community["total_balance"] >= loan["amount"]:
                community["total_balance"] -= loan["amount"]
            else:
                raise ValueError("Community fund has insufficient balance for this loan")
    else:
        loan["approval_percentage"] -= user_weight

    community_ref.set(community)
    db.collection("loans").document(loan_id).update({
        "approval_percentage": loan["approval_percentage"],
        "status": loan["status"]
    })

    return loan

def make_loan_payment(user_id, loan_id, payment_amount):
    """Allows a borrower to make a loan payment."""
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community or "active_loans" not in community:
        raise ValueError("No active loans found")

    loan = next((l for l in community["active_loans"] if l["loan_id"] == loan_id), None)
    if not loan:
        raise ValueError("Active loan not found")

    remaining_balance = loan["amount"] - loan.get("paid_amount", 0)
    if payment_amount > remaining_balance:
        raise ValueError("Payment amount exceeds remaining balance")

    loan["paid_amount"] = loan.get("paid_amount", 0) + payment_amount
    if loan["paid_amount"] >= loan["amount"]:
        loan["status"] = "repaid"
        community["active_loans"].remove(loan)

    interest = payment_amount - loan["amount"] if loan["paid_amount"] >= loan["amount"] else 0.0
    community["total_balance"] += payment_amount
    distribute_interest(interest, community["contributors"])

    community_ref.set(community)

    db.collection("loans").document(loan_id).update({
        "paid_amount": loan["paid_amount"],
        "status": loan["status"]
    })

    create_transaction(user_id, "loan_payment", payment_amount)
    return loan

def withdraw_from_community(user_id, amount):
    """Allows a user to withdraw their contributions from the community fund."""
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community:
        raise ValueError("Community fund does not exist")

    contributor = next((c for c in community["contributors"] if c["user_id"] == user_id), None)
    if not contributor or contributor["amount"] < amount:
        raise ValueError("Insufficient contribution balance")

    available_balance = community["total_balance"] - sum(l["amount"] for l in community.get("active_loans", []))
    if amount > available_balance:
        raise ValueError("Cannot withdraw more than the available community balance")

    contributor["amount"] -= amount
    community["total_balance"] -= amount
    if contributor["amount"] == 0:
        community["contributors"].remove(contributor)

    community_ref.set(community)

    user = get_user_by_id(user_id)
    new_balance = user["wallet_balance"] + amount
    update_user(user_id, {"wallet_balance": new_balance})

    create_transaction(user_id, "withdrawal", amount)
    return community



def distribute_interest(interest, contributors):
    """
    Distribute the earned interest proportionally among contributors.
    Args:
        interest (float): The total interest earned from a loan repayment.
        contributors (list): List of contributors with their user_id and amount.
    """
    total_contributions = sum(c["amount"] for c in contributors)

    if total_contributions == 0:
        raise ValueError("No contributions in the community fund to distribute interest.")

    # Distribute interest to each contributor proportionally
    for contributor in contributors:
        contribution_percentage = contributor["amount"] / total_contributions
        interest_share = interest * contribution_percentage

        # Update the contributor's interest_earned
        user = get_user_by_id(contributor["user_id"])
        if user:
            new_interest_earned = user.get("interest_earned", 0.0) + interest_share
            update_user(contributor["user_id"], {"interest_earned": new_interest_earned})


def calculate_emi(amount, credit_score, months=12):
    """
    Calculate EMI (Equated Monthly Installment) for a loan.
    
    Args:
        amount (float): The principal loan amount.
        credit_score (int): The borrower's credit score.
        months (int): The repayment period in months (default is 12 months).

    Returns:
        float: The calculated EMI.
    """
    # Define interest rates for ranges
    base_rate = 15.0  # Starting interest rate for lowest scores
    rate_decrease_per_range = 0.5  # Interest decreases by 0.5% per range
    range_interval = 30  # Each range spans 30 points
    min_credit_score = 300  # Minimum credit score (e.g., FICO score scale)
    max_credit_score = 850  # Maximum credit score (e.g., FICO score scale)

    # Calculate interest rate based on credit score range
    if credit_score < min_credit_score:
        interest_rate = base_rate
    elif credit_score >= max_credit_score:
        interest_rate = base_rate - ((max_credit_score - min_credit_score) // range_interval) * rate_decrease_per_range
    else:
        range_index = (credit_score - min_credit_score) // range_interval
        interest_rate = base_rate - (range_index * rate_decrease_per_range)

    # Convert annual interest rate to monthly rate
    monthly_rate = interest_rate / (12 * 100)

    # EMI formula: EMI = [P * r * (1 + r)^n] / [(1 + r)^n - 1]
    emi = (amount * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)

    return round(emi, 2)



def get_community_interest():
    """
    Retrieves the total interest earned by the community.
    """
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community:
        raise ValueError("Community fund does not exist")

    total_interest_earned = 0.0
    for contributor in community.get("contributors", []):
        user = get_user_by_id(contributor["user_id"])
        if user:
            total_interest_earned += user.get("interest_earned", 0.0)

    return {"total_interest_earned": round(total_interest_earned, 2)}
