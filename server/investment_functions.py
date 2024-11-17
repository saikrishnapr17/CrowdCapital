import uuid
from firebase_admin import firestore
from user_functions import get_user_by_id, update_user

db = firestore.client()

def enlist_business(owner_id, business_name, description, goal, equity):
    """
    Allows a user to enlist their business for community investments.
    """
    business_id = str(uuid.uuid4())
    business_data = {
        "business_id": business_id,
        "business_name": business_name,
        "description": description,
        "goal": goal,
        "equity": equity,
        "remaining_amount": goal,
        "owner_id": owner_id,
        "stakeholders": []
    }

    # Save to Firestore
    db.collection("businesses").document(business_id).set(business_data)
    return business_data


def invest_in_business(user_id, business_id, amount_invested):
    """
    Allows a user to invest in a business and updates their equity.
    """
    business_ref = db.collection("businesses").document(business_id)
    business = business_ref.get().to_dict()

    if not business:
        raise ValueError("Business not found")

    if business["remaining_amount"] < amount_invested:
        raise ValueError("Investment amount exceeds remaining goal")

    # Calculate equity for the investment
    equity_share = (amount_invested / business["goal"]) * business["equity"]

    # Update business details
    business["remaining_amount"] -= amount_invested
    stakeholder = next((s for s in business["stakeholders"] if s["user_id"] == user_id), None)
    if stakeholder:
        stakeholder["amount_invested"] += amount_invested
        stakeholder["equity"] += equity_share
    else:
        business["stakeholders"].append({
            "user_id": user_id,
            "amount_invested": amount_invested,
            "equity": equity_share
        })

    business_ref.set(business)

    # Record the investment in the investments collection
    investment_id = str(uuid.uuid4())
    investment_data = {
        "investment_id": investment_id,
        "user_id": user_id,
        "business_id": business_id,
        "amount_invested": amount_invested,
        "equity": equity_share
    }
    db.collection("investments").document(investment_id).set(investment_data)

    # Update user data
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    user_new_balance = user["wallet_balance"] - amount_invested
    if user_new_balance < 0:
        raise ValueError("Insufficient user balance")

    new_investment_amount = user.get("investment_amount", 0) + amount_invested
    new_equity = user.get("equity_from_investments", 0) + equity_share

    update_user(user_id, {
        "wallet_balance": user_new_balance,
        "investment_amount": new_investment_amount,
        "equity_from_investments": new_equity
    })

    return {"business": business, "investment": investment_data}


def get_business_investments(business_id):
    """
    Returns the list of investors and their investments for a specific business.
    """
    business_ref = db.collection("businesses").document(business_id)
    business = business_ref.get().to_dict()

    if not business:
        raise ValueError("Business not found")

    return business["stakeholders"]

def get_all_business_ids():
    """
    Retrieves all business IDs from the businesses collection.
    """
    businesses_ref = db.collection("businesses")
    business_docs = businesses_ref.stream()
    business_ids = [doc.id for doc in business_docs]
    return {"business_ids": business_ids}
