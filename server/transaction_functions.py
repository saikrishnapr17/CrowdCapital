import uuid
from datetime import datetime
from firebase_admin import firestore
from user_functions import get_user_by_id, update_user, get_user_by_phone

db = firestore.client()

def create_transaction(user_id, transaction_type, amount, target_user=None):
    transaction_id = str(uuid.uuid4())
    transaction_data = {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "type": transaction_type,  # 'deposit', 'transfer'
        "amount": amount,
        "target_user": target_user,  # For transfers
        "timestamp": datetime.utcnow().isoformat(),
    }
    db.collection("transactions").document(transaction_id).set(transaction_data)
    return transaction_data

def get_transactions_by_user(user_id):
    transactions_query = db.collection("transactions").where("user_id", "==", user_id).get()
    return [t.to_dict() for t in transactions_query]

def transfer_money(sender_id, recipient_phone, amount):
    sender = get_user_by_id(sender_id)
    recipient = get_user_by_phone(recipient_phone)

    if not sender:
        raise ValueError("Sender not found")
    if not recipient:
        raise ValueError("Recipient not found")
    if sender["wallet_balance"] < amount:
        raise ValueError("Insufficient balance")

    # Update wallet balances
    sender_new_balance = sender["wallet_balance"] - amount
    recipient_new_balance = recipient["wallet_balance"] + amount
    update_user(sender_id, {"wallet_balance": sender_new_balance})
    update_user(recipient["user_id"], {"wallet_balance": recipient_new_balance})

    # Record transactions
    create_transaction(sender_id, "transfer", amount, target_user=recipient["user_id"])
    create_transaction(recipient["user_id"], "transfer", amount, target_user=sender_id)

    return {"sender_new_balance": sender_new_balance, "recipient_new_balance": recipient_new_balance}