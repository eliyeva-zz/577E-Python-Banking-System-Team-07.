
from datetime import date
from decimal import Decimal, InvalidOperation

from storage import save_data
from history import record_transaction


def transfer_money(data, sender_username):

    users = data["users"]

    if sender_username not in users:
        print("Göndərən istifadəçi tapılmadı!")
        return

    sender = users[sender_username]

    recipient_account = input("Alıcının hesab nömrəsini daxil edin: ")

    recipient_username = None

    for username, user in users.items():
        if user["account_number"] == recipient_account:
            recipient_username = username
            break

    if recipient_username is None:
        print("Alıcı hesab tapılmadı!")
        return

    if recipient_username == sender_username:
        print("Öz hesabınıza pul köçürə bilməzsiniz!")
        return

    recipient = users[recipient_username]

    amount_input = input("Köçürüləcək məbləği daxil edin (AZN): ")

    try:
        amount_decimal = Decimal(amount_input)

        if not amount_decimal.is_finite():
            print("Yanlış məbləğ!")
            return

        if amount_decimal <= 0:
            print("Məbləğ sıfırdan böyük olmalıdır!")
            return

        if amount_decimal.as_tuple().exponent < -2:
            print("Maksimum 2 onluq rəqəm daxil edə bilərsiniz!")
            return

    except InvalidOperation:
        print("Zəhmət olmasa düzgün məbləğ daxil edin!")
        return

    amount = int(amount_decimal * 100)

    if sender["balance"] < amount:
        print("Balansınızda kifayət qədər pul yoxdur!")
        return

    daily = sender["daily"]
    today = date.today().isoformat()

    if daily["date"] != today:
        daily["date"] = today
        daily["deposit"] = 0
        daily["withdrawn"] = 0
        daily["transfer_count"] = 0

        save_data(data)

    if daily["transfer_count"] >= 5:
        print("Gündəlik 5 transfer limitiniz bitib!")
        return

    print("\n========== TRANSFER DETAILS ==========")
    print("Sender:", sender_username)
    print("Recipient:", recipient_username)
    print("Amount:", amount_decimal, "AZN")

    confirmation = input("Confirm transfer (Y/N): ").strip().upper()

    if confirmation != "Y":
        print("Transfer cancelled!")
        return

    sender_balance_before = sender["balance"]
    recipient_balance_before = recipient["balance"]

    sender["balance"] -= amount
    recipient["balance"] += amount

    daily["transfer_count"] += 1

    record_transaction(
        data,
        sender_username,
        "Transfer Sent",
        amount,
        sender_balance_before,
        sender["balance"],
        other_account=recipient["account_number"],
        save=False
    )

    record_transaction(
        data,
        recipient_username,
        "Transfer Received",
        amount,
        recipient_balance_before,
        recipient["balance"],
        other_account=sender["account_number"],
        save=False
    )

    save_data(data)

    print("\nTransfer successful!")
    print("Sender new balance:", sender["balance"] / 100, "AZN")
