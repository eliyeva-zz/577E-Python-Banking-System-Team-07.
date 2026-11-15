import sys

from storage import get_data, save_data
from banksystem import handle_login, change_password
from deposit import show_account_info, show_balances, deposit_money
from withdrawal2 import withdraw_money
from history import record_transaction, show_transaction_history
from transfers import transfer_money
from limits2 import display_daily_limits


def do_deposit(data, username):
    user = data["users"][username]
    before = user["balance"]
    data["atm_cash"] = deposit_money(user, data["atm_cash"])
    after = user["balance"]
    if after != before: # only successful deposits are recorded
        record_transaction(data, username, "Deposit", after - before, before, after)
    else:
        save_data(data)


def do_withdraw(data, username):
    user = data["users"][username]
    before = user["balance"]
    atm_before = data["atm_cash"]
    data["atm_cash"] = withdraw_money(user, data["atm_cash"])
    if user["balance"] != before:
        cash = atm_before - data["atm_cash"] # cash dispensed
        fee = (before - user["balance"]) - cash # commission
        record_transaction(data, username, "Withdrawal", -cash,
                           before, user["balance"], fee=fee)
    else:
        save_data(data)


def login_screen(data):
    """Returns username after successful login, or None to exit."""
    users = data["users"]
    save_callback = lambda: save_data(data)
    while True:
        print("\n" + "=" * 36)
        print(" PYTHON BANKING SYSTEM")
        print("=" * 36)
        username = input("Username (or 'exit'): ").strip()
        if username.lower() == "exit":
            return None
        password = input("Password: ")
        ok, status = handle_login(username, password, users, save_callback)
        if ok:
            return username


def show_menu(username):
    print("\n" + "=" * 36)
    print(" PYTHON BANKING SYSTEM")
    print("=" * 36)
    print(f"Welcome, {username}!")
    print("1. View Account Information")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Transaction History")
    print("7. Daily Limits")
    print("8. Change Password")
    print("9. Logout")
    print("0. Exit")
    print("=" * 36)


def session(data, username):
    """Menu loop. Returns when the user logs out."""
    save_callback = lambda: save_data(data)
    while True:
        user = data["users"][username]
        show_menu(username)
        choice = input("Select an option: ").strip()

        if choice == "1":
            show_account_info(username, user)
        elif choice == "2":
            show_balances(user)
        elif choice == "3":
            do_deposit(data, username)
        elif choice == "4":
            do_withdraw(data, username)
        elif choice == "5":
            transfer_money(data, username)
        elif choice == "6":
            show_transaction_history(data, username)
        elif choice == "7":
            display_daily_limits(user)
            save_data(data)
        elif choice == "8":
            change_password(username, data["users"], save_callback)
        elif choice == "9":
            print("\nLogged out.")
            return
        elif choice == "0":
            print("\nGoodbye!")
            sys.exit()
        else:
            print("\nInvalid option. Please try again.")


def main():
    data = get_data()
    while True:
        username = login_screen(data)
        if username is None:
            print("Goodbye!")
            break
        session(data, username)


if __name__ == "__main__":
    main()