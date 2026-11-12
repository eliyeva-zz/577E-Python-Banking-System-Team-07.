def input_validation(accounts, amount_str):
    """
    girilen pulun valid olub olmadığını yoxlamaq üçün yazılan bir programdır.
    """
    try:
        amount = float(amount_str)
    except ValueError:
        print("Error: Please enter a numeric value.")
        return None
    if "." in amount_str:
        parts = amount_str.split(".")
        if len(parts[1]) > 2:
            print("Error: Maximum 2 decimal places allowed.")
            return None
    if amount <= 0:
        print("Error: Amount must be positive.")
        return None

    return amount

def withdraw_money(accounts, atm_cash):
    if accounts.get('blocked', False):
        print("Error: Your account is blocked, you cannot withdraw money.")
        return atm_cash

    print("\n--- CASH WITHDRAWAL ---")
    amount_str = input("Enter amount to withdraw (AZN): ")
    amount = input_validation(accounts, amount_str)

    current_daily_withdrawn = accounts.get('daily_withdrawn', 0.00)
    daily_max_withdrawn = 1000.00

    if amount + current_daily_withdrawn > daily_max_withdrawn:
        remaining_wd_amount = daily_max_withdrawn - current_daily_withdrawn
        print(f"\nWithdrawal declined: Daily limit would be exceeded.")
        print(f"Already withdrawn today: {current_daily_withdrawn:.2f} AZN")
        print(f"Requested withdrawal: {amount:.2f} AZN")
        print(f"Daily maximum: {daily_max_withdrawn:.2f} AZN")
        print(f"Remaining cash withdrawal allowance: {remaining_wd_amount:.2f} AZN")
        print("Account balance, ATM reserve and daily counters remain unchanged.")
        return atm_cash

    free_allowance = 500.00
    remaining_free_allowance = free_allowance - current_daily_withdrawn
    if amount > remaining_free_allowance:
            withdrawal_commission = (amount - remaining_free_allowance) * 0.02
    else:
        withdrawal_commission = 0.00

    total_withdrawal = amount + withdrawal_commission

    current_balance = accounts.get('balance', 0.00)
    if total_withdrawal > current_balance:
        print(f"\nWithdrawal declined: Insufficient funds.")
        print(f"Account balance: {current_balance:.2f} AZN")
        print(f"Total required (including commission): {total_withdrawal:.2f} AZN")
        print("Account balance, ATM reserve and daily counters remain unchanged.")
        return atm_cash

    if atm_cash < amount:
        print(f"\nWithdrawal declined: Insufficient ATM cash reserve.")
        print(f"Requested withdrawal: {amount:.2f} AZN")
        print(f"Available ATM cash: {atm_cash:.2f} AZN")
        print("Account balance, ATM reserve and daily counters remain unchanged.")
        return atm_cash

    accounts['balance'] = current_balance - total_withdrawal
    accounts['daily_withdrawn'] = current_daily_withdrawn + amount
    atm_cash -= amount #PDF'de gosterilib ki atm kasasindan sadece amount cixmalidi, komissiya + amount cixmamalidi!!

    print(f"\nSuccessfully withdrawn {amount:.2f} AZN.")
    print(f"Withdrawal commission: {withdrawal_commission:.2f} AZN")
    print(f"Total withdrawn from account: {total_withdrawal:.2f} AZN")
    print(f"New account balance: {accounts.get('balance', 0.00):.2f} AZN")
    print(f"Remaining daily withdrawal allowance: {daily_max_withdrawn - accounts.get('daily_withdrawn', 0.00):.2f} AZN")

    return atm_cash




