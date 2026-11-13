from datetime import datetime
from storage import save_data

def record_transaction(data, username, transaction_type, amount,
                       balance_before, balance_after, fee=0,
                       other_account=None, save=True):

    transaction_id = f"TXN{data['next_txn_number']:04d}"

    transaction = {
        "id": transaction_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": transaction_type,
        "amount": amount,
        "balance_before": balance_before,
        "balance_after": balance_after,
        "fee": fee,
        "other_account": other_account
    }

    data["users"][username]["history"].append(transaction)
    data["next_txn_number"] += 1

    if save:
        save_data(data)


def show_transaction_history(data, username):

    history = data["users"][username]["history"]

    if not history:
        print("Transaction history is empty.")
        return

    print("\n========== Transaction History ==========")

    for transaction in history[-10:]:
        print("-----------------------------------------")
        print("ID:", transaction["id"])
        print("Date:", transaction["date"])
        print("Type:", transaction["type"])
        print("Amount:", transaction["amount"])
        print("Balance Before:", transaction["balance_before"])
        print("Balance After:", transaction["balance_after"])
        print("Fee:", transaction["fee"])

        if transaction["other_account"] is not None:
            print("Other Account:", transaction["other_account"])

    print("-----------------------------------------")