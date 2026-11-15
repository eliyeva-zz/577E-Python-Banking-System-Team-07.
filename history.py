from datetime import datetime
from storage import save_data

def record_transaction(data, username, transaction_type, amount, balance_before, balance_after, fee=0, other_account=None, save=True):

    transaction_id = f"TXN{data['next_txn_number']:04d}"

# tari=metn edir bu %

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

from limits2 import format_azn


def show_transaction_history(data, username):
    history = data["users"][username]["history"]

    if not history:
        print("No transactions found.")
        return

    print("\n========== TRANSACTION HISTORY ==========")
    for t in history[-10:]:
        print("-----------------------------------------")
        print("ID:", t["id"])
        print("Date:", t["date"])
        print("Type:", t["type"])
        if t["other_account"] is not None:
            label = "Recipient account" if t["type"] == "Transfer Sent" else "Sender account"
            print(f"{label}:", t["other_account"])
        print("Amount:", format_azn(t["amount"]), "AZN")
        if t["fee"]:
            print("Fee:", format_azn(t["fee"]), "AZN")
        print("Balance before:", format_azn(t["balance_before"]), "AZN")
        print("Balance after:", format_azn(t["balance_after"]), "AZN")
    print("-----------------------------------------")












