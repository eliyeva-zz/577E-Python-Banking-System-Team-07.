from deposit import input_validation
from limits2 import (DAILY_WITHDRAW_MAX, FEE_FREE_LIMIT, FEE_PERCENT,
                    check_reset_daily_limits, format_azn)


def calculate_commission(amount, withdrawn_today):
    """Sadece gunluk 500 AZN'yi asan hisse ucun %2 komisyon (hamisi qepik).
    Meselen: bugun 40000 cekildi, 25000 istendi -> 10000 ucretsiz, 15000 komisyonlu -> 300"""
    free_left = max(0, FEE_FREE_LIMIT - withdrawn_today)  # kalan ucretsiz hak
    fee_amount = max(0, amount - free_left)  # komisyonlu kisim
    return (fee_amount * FEE_PERCENT + 50) // 100  # +50: yarim kurus yukari yuvarlama


def withdraw_money(user, atm_cash):
    """Cagiran taraf: data["atm_cash"] = withdraw_money(user, data["atm_cash"]); save_data(data)"""
    if user['blocked']:
        print("Error: Your account is blocked, you cannot withdraw money.")
        return atm_cash

    check_reset_daily_limits(user)
    daily = user["daily"]

    print("\n--- CASH WITHDRAWAL ---")
    amount = input_validation(input("Enter amount to withdraw (AZN): "))
    if amount is None:
        return atm_cash

    withdrawn_today = daily["withdrawn"]
    balance = user["balance"]

    # 1) Gunluk 1000 AZN siniri
    if withdrawn_today + amount > DAILY_WITHDRAW_MAX:
        print("\nWithdrawal declined: Daily limit would be exceeded.")
        print(f"Already withdrawn today: {format_azn(withdrawn_today)} AZN")
        print(f"Requested withdrawal: {format_azn(amount)} AZN")
        print(f"Daily maximum: {format_azn(DAILY_WITHDRAW_MAX)} AZN")
        print(f"Remaining cash withdrawal allowance: {format_azn(DAILY_WITHDRAW_MAX - withdrawn_today)} AZN")
        print("Account balance, ATM reserve and daily counters remain unchanged.")
        return atm_cash

    # 2) Balans (komissiya daxil) besdir mi?
    commission = calculate_commission(amount, withdrawn_today)
    total = amount + commission

    if total > balance:
        print("\nWithdrawal declined: Insufficient funds.")
        print(f"Account balance: {format_azn(balance)} AZN")
        print(f"Total required (including commission): {format_azn(total)} AZN")
        print("Account balance, ATM reserve and daily counters remain unchanged.")
        return atm_cash

    # 3) ATM'de yeteri qeder pul var mi? (sadece amount, komissiya ATM'den cixmir)
    if atm_cash < amount:
        print("\nWithdrawal declined: Insufficient ATM cash reserve.")
        print(f"Requested withdrawal: {format_azn(amount)} AZN")
        print(f"Available ATM cash: {format_azn(atm_cash)} AZN")
        print("Account balance, ATM reserve and daily counters remain unchanged.")
        return atm_cash

    user["balance"] = balance - total
    daily["withdrawn"] = withdrawn_today + amount
    atm_cash = atm_cash - amount


    print(f"\nSuccessfully withdrawn {format_azn(amount)} AZN.")
    print(f"Withdrawal commission: {format_azn(commission)} AZN")
    print(f"Total withdrawn from account: {format_azn(total)} AZN")
    print(f"New account balance: {format_azn(user['balance'])} AZN")
    print(f"Remaining daily withdrawal allowance: {format_azn(DAILY_WITHDRAW_MAX - daily['withdrawn'])} AZN")

    return atm_cash