from limits2 import DAILY_DEPOSIT_MAX, check_reset_daily_limits, format_azn


def show_account_info(username, user):
    """username data["users"] sozlugunun acarindan gelir (user icinde yazmir)."""
    print(f"Account Holder : {username}")
    print(f"Account Number : {user['account_number']}")
    print(f"Available Balance: {format_azn(user['balance'])} AZN")
    print("Account Status:", 'Blocked' if user['blocked'] else 'Active')


def show_balances(user):
    print(f"Available balance: {format_azn(user['balance'])} AZN")


def input_validation(amount_str):
    """Girilen miqdar valid olsa qepik (int) dondurur, degilse None.
    Meselen: "12.5" -> 1250, "100" -> 10000, "0.29" -> 29
    Deposit ve withdraw ikisi de bunu isledir."""
    amount_str = amount_str.strip()

    if amount_str.startswith("-"):
        print("Error: Amount must be positive.")
        return None

    # sadece reqem ve en coxu 1 noqte olabiler(herf, bosluq, bos giris reddedilir)
    if not amount_str.replace(".", "", 1).isdecimal():
        print("Error: Please enter a numeric value.")
        return None

    parts = amount_str.split(".")
    if len(parts) == 2 and len(parts[1]) > 2:
        print("Error: Maximum 2 decimal places allowed.")
        return None

    # Yazidan direkt qepik cevir (float isletmirik)
    qepik = int(parts[0] or "0") * 100
    if len(parts) == 2:
        qepik += int(parts[1].ljust(2, "0"))  # "5" -> "50", "05" -> "05"

    if qepik <= 0:
        print("Error: Amount must be positive.")
        return None

    return qepik


def deposit_money(user, atm_cash):
    """Para yatirilir. Hem user["balance"] hem ATM kasasi artar. Yeni atm_cash return eliyir (qepik)."""
    if user['blocked']:
        print("Error: Your account is blocked, you cannot deposit money.")
        return atm_cash

    check_reset_daily_limits(user)
    daily = user["daily"]

    print("\n--- DEPOSIT MONEY ---")
    amount = input_validation(input("Enter amount to deposit (AZN): "))
    if amount is None:
        return atm_cash

    deposited_today = daily["deposit"]

    # Limit asilirsa butun islem redd olur
    if deposited_today + amount > DAILY_DEPOSIT_MAX:
        remaining = DAILY_DEPOSIT_MAX - deposited_today
        print(f"\nDeposited today: {format_azn(deposited_today)} AZN")
        print(f"Requested deposit: {format_azn(amount)} AZN")
        print(f"Daily deposit maximum: {format_azn(DAILY_DEPOSIT_MAX)} AZN")
        print(f"Remaining deposit allowance: {format_azn(remaining)} AZN")
        print("\nDeposit declined: daily limit would be exceeded.")
        print("Account balance and ATM cash remain unchanged.")
        return atm_cash

    # sucsessfull olsa
    user["balance"] = user["balance"] + amount
    daily["deposit"] = deposited_today + amount
    atm_cash = atm_cash + amount


    print(f"Successfully deposited {format_azn(amount)} AZN.")
    print(f"New balance: {format_azn(user['balance'])} AZN.")
    print(f"Remaining deposit allowance: {format_azn(DAILY_DEPOSIT_MAX - daily['deposit'])} AZN.")

    return atm_cash