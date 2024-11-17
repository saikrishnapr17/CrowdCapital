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
    """
    Allows a user to request a loan, calculates total payable with interest.
    """
    emi = calculate_emi(amount, credit_score)
    
    # Calculate total interest for the loan
    interest_rate = 5.0 if credit_score >= 750 else 10.0 if credit_score >= 600 else 15.0
    total_interest = (amount * interest_rate) / 100
    total_payable = amount + total_interest  # Total owed by the user
    
    # Create loan request
    loan_id = str(uuid.uuid4())
    loan_request = {
        "loan_id": loan_id,
        "user_id": user_id,
        "amount": amount,
        "interest_rate": interest_rate,
        "interest_amount": total_interest,
        "total_payable": total_payable,
        "remaining_principal": amount,
        "remaining_interest": total_interest,
        "description": description,
        "emi": emi,
        "approval_percentage": 0.0,
        "status": "pending"
    }

    # Add the loan request to the community fund
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

    # Save the loan request in the loans collection
    db.collection("loans").document(loan_id).set(loan_request)

    # Add the loan_id to the user's document
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    user_loans = user.get("loan_ids", [])
    user_loans.append(loan_id)
    update_user(user_id, {"loan_ids": user_loans})

    return loan_request

def approve_or_deny_loan(user_id, loan_id, approve=True):
    """Handles loan approval or denial."""
    # Fetch community fund
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community or "pending_loan_requests" not in community:
        raise ValueError("No pending loans found")

    # Find the loan in pending loans
    loan = next((l for l in community["pending_loan_requests"] if l["loan_id"] == loan_id), None)
    if not loan:
        raise ValueError("Loan request not found")

    if loan["user_id"] == user_id:
        raise ValueError("Loan requester cannot approve their own loan")

    # Validate if the user is a contributor
    contributor = next((c for c in community["contributors"] if c["user_id"] == user_id), None)
    if not contributor:
        raise ValueError("Only contributors can vote on loans")

    # Calculate user's voting weight
    total_contributions = sum(c["amount"] for c in community["contributors"])
    user_weight = (contributor["amount"] / total_contributions) * 100

    if approve:
        loan["approval_percentage"] += user_weight
        if loan["approval_percentage"] >= 60.0:
            # Remove the loan from pending loans
            community["pending_loan_requests"].remove(loan)

            # Add the loan to active loans
            if "active_loans" not in community:
                community["active_loans"] = []
            community["active_loans"].append(loan)

            # Update loan status
            loan["status"] = "approved"

            # Deduct the loan amount from the community fund balance
            if community["total_balance"] >= loan["amount"]:
                community["total_balance"] -= loan["amount"]
            else:
                raise ValueError("Community fund has insufficient balance for this loan")

    # Update community fund
    community_ref.set(community)

    # Update the loan document in Firestore
    db.collection("loans").document(loan_id).update({
        "approval_percentage": loan["approval_percentage"],
        "status": loan["status"]
    })

    return loan


def get_all_pending_loans():
    """
    Retrieves all pending loan requests from the community fund, displaying user names instead of user IDs.
    """
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community or "pending_loan_requests" not in community:
        raise ValueError("No pending loans found")

    pending_loans = community["pending_loan_requests"]

    # Replace user_id with user names
    for loan in pending_loans:
        user = get_user_by_id(loan["user_id"])
        if user:
            loan["user_name"] = user.get("name", "Unknown")  # Add the user's name
        else:
            loan["user_name"] = "Unknown"

    return pending_loans


def make_loan_payment(user_id, payment_amount):
    """
    Processes a loan payment, updating interest and principal separately.
    """
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    user_loan_ids = user.get("loan_ids", [])
    if not user_loan_ids:
        raise ValueError("No active loans found for the user")

    total_loan_balance = 0
    loans_to_update = []

    for loan_id in user_loan_ids:
        loan_ref = db.collection("loans").document(loan_id)
        loan = loan_ref.get().to_dict()
        if loan["status"] != "repaid":
            remaining_balance = loan["remaining_principal"] + loan["remaining_interest"]
            total_loan_balance += remaining_balance
            loans_to_update.append(loan)

    if total_loan_balance == 0:
        raise ValueError("All loans are already repaid")

    if payment_amount > total_loan_balance:
        raise ValueError("Payment amount exceeds total loan balance")

    # Distribute payment across loans
    for loan in loans_to_update:
        loan_ref = db.collection("loans").document(loan["loan_id"])
        remaining_interest = loan["remaining_interest"]
        remaining_principal = loan["remaining_principal"]

        if payment_amount <= 0:
            break

        # Apply payment to interest first
        payment_to_interest = min(payment_amount, remaining_interest)
        loan["remaining_interest"] -= payment_to_interest
        payment_amount -= payment_to_interest

        # Apply remaining payment to principal
        payment_to_principal = min(payment_amount, remaining_principal)
        loan["remaining_principal"] -= payment_to_principal
        payment_amount -= payment_to_principal

        # Mark loan as repaid if fully paid
        if loan["remaining_principal"] == 0 and loan["remaining_interest"] == 0:
            loan["status"] = "repaid"

        # Update the loan document in Firestore
        loan_ref.update({
            "remaining_interest": loan["remaining_interest"],
            "remaining_principal": loan["remaining_principal"],
            "status": loan["status"]
        })

    # Update the community fund
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    # Add the payment to total balance (for distribution to contributors)
    community["total_balance"] += payment_to_interest  # Only interest is added to community fund
    distribute_interest(payment_to_interest, community["contributors"])
    community_ref.set(community)

    # Record the payment transaction
    create_transaction(user_id, "loan_payment", payment_amount)

    return {
        "message": "Payment successfully applied to loans",
        "updated_loans": loans_to_update,
        "remaining_balance": total_loan_balance - payment_amount
    }



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



def calculate_emi(amount, credit_score = 700, months=12):
    """
    Calculate EMI (Equated Monthly Installment) for a loan.
    
    Args:
        amount (float): The principal loan amount.
        credit_score (int): The borrower's credit score.
        months (int): The repayment period in months (default is 12 months).

    Returns:
        float: The calculated EMI.
    """
    # Determine interest rate based on credit score (example logic)
    if credit_score >= 750:
        interest_rate = 5.0  # Best interest rate for high credit score
    elif credit_score >= 600:
        interest_rate = 10.0
    else:
        interest_rate = 15.0  # Higher rate for lower credit scores

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

def get_community_fund_details():
    """
    Retrieves community fund details, including contributors (with names), loans, and interest earned.
    """
    community_ref = db.collection("community").document("fund")
    community = community_ref.get().to_dict()

    if not community:
        raise ValueError("Community fund does not exist")

    # Update contributors with names
    updated_contributors = []
    for contributor in community.get("contributors", []):
        user = get_user_by_id(contributor["user_id"])
        if user:
            updated_contributors.append({
                "name": user.get("name"),
                "amount": contributor["amount"]
            })
        else:
            updated_contributors.append({
                "name": "Unknown User",
                "amount": contributor["amount"]
            })

    # Replace IDs with names for contributors
    community["contributors"] = updated_contributors

    # Calculate total interest earned by contributors
    total_interest_earned = 0.0
    for contributor in community.get("contributors", []):
        user = get_user_by_id(contributor.get("user_id"))
        if user:
            total_interest_earned += user.get("interest_earned", 0.0)

    # Add total interest earned to the community data
    community["total_interest_earned"] = round(total_interest_earned, 2)

    return community
