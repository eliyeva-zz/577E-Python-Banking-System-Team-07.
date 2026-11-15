from storage import save_data
from history import record_transaction
from deposit import input_validation
from limits2 import format_azn, check_reset_daily_limits, DAILY_TRANSFER_MAX


def transfer_money(data, sender_username):
    users = data["users"]
    sender = users[sender_username]

    check_reset_daily_limits(sender)
    daily = sender["daily"]

    print("\n--- TRANSFER MONEY ---")
    recipient_account = input("Enter recipient account number: ").strip()

    recipient_username = None
    for name, user in users.items():
        if user["account_number"] == recipient_account:
            recipient_username = name
            break

    if recipient_username is None:
        print("Error: Recipient account not found.")
        return

    if recipient_username == sender_username:
        print("Error: You cannot transfer money to your own account.")
        return

    recipient = users[recipient_username]

    amount = input_validation(input("Enter amount to transfer (AZN): "))
    if amount is None:
        return

    if sender["balance"] < amount:
        print("Error: Insufficient funds.")
        return

    if daily["transfer_count"] >= DAILY_TRANSFER_MAX:
        print(f"Error: Daily limit of {DAILY_TRANSFER_MAX} outgoing transfers reached.")
        return

    print("\n========== TRANSFER DETAILS ==========")
    print("Sender:", sender_username)
    print("Recipient account:", recipient_account)
    print("Recipient:", recipient_username)
    print("Amount:", format_azn(amount), "AZN")

    confirmation = input("Confirm transfer (Y/N): ").strip().upper()
    if confirmation != "Y":
        print("Transfer cancelled.")
        return

    sender_before = sender["balance"]
    recipient_before = recipient["balance"]

    sender["balance"] -= amount
    recipient["balance"] += amount
    daily["transfer_count"] += 1

    record_transaction(data, sender_username, "Transfer Sent", -amount,
                       sender_before, sender["balance"],
                       other_account=recipient["account_number"], save=False)
    record_transaction(data, recipient_username, "Transfer Received", amount,
                       recipient_before, recipient["balance"],
                       other_account=sender["account_number"], save=False)

    save_data(data) # both balances saved together

    print("\nTransfer successful.")
    print("Sender new balance:", format_azn(sender["balance"]), "AZN")