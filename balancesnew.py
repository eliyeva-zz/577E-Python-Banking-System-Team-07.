def show_account_info(accounts):
    """
    ekranda userin informasiyalarını göstermek üçün yazılan bir funksiyadır. accounts.get dictionaryden data çağırmaq
    üçün istifade olunan methoddur. accounts.get('balance', 0.00) bunu yazmağımım sebebi ondan ibaretdir ki eger balance
    adında bir data yoxdursa error vermek yerine avtomatik 0.00 output elesin. accounts.get('balance', 0.00):.2f buradaki
    :.2f yazısının mahiyyeti ondan ibaretdir ki meselen biz 1500 daxil etsek onu avtomatik 1500.00'a çevirsin
    """
    print(f"Account Holder: {accounts.get('username')}")
    print(f"Account number: {accounts.get('account_number')}")
    print(f"Available balance: {accounts.get('balance', 0.00):.2f} AZN")
    print("Account status: ", 'Blocked' if accounts.get('blocked', False) else 'Active')

def show_balances(accounts):
    print(f"Available balance: {accounts.get('balance', 0.00):.2f} AZN")


def deposit_money(accounts):
    if accounts.get('blocked', False):
        print("Error: Your account is blocked, you cannot deposit money.")
        return None

    print("\n--- DEPOSIT MONEY ---")

    amount_str = input("Enter amount to deposit (AZN): ")
    amount = input_validation(accounts, amount_str)

    if amount is None:
        return None

    current_daily_deposited = accounts.get('daily_deposited', 0.00)
    daily_limit = 2000.00

    if current_daily_deposited + amount > daily_limit:
        remaining_amount = daily_limit - current_daily_deposited
        print(f"\nDeposited today: {current_daily_deposited:.2f} AZN")
        print(f"Requested deposit: {amount:.2f} AZN")
        print(f"Daily deposit maximum: {daily_limit:.2f} AZN")
        print(f"Remaining deposit allowance: {remaining_amount:.2f} AZN")
        print("\n\nDeposit declined: daily limit would be exceeded.")
        print("Account balance and ATM cash remain unchanged.")
        return None

    current_balance = accounts.get('balance', 0.00)
    accounts['balance'] = current_balance + amount
    accounts['daily_deposited'] = accounts.get('daily_deposited', 0.00) + amount

    print(f"Successfully deposited {amount:.2f} AZN.")
    print(f"New balance: {accounts.get('balance', 0.00):.2f} AZN.")
    


