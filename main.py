
from storage import get_data
from history import record_transaction, show_transaction_history
from transfers import transfer_money

def show_menu():
    print("\n========== MENU ==========")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Transaction History")
    print("6. Exit")


def get_choice():
    choice = input("\nEnter your choice (1-6): ")
    return choice


def main():
    data = get_data()

    print("==========")
    print("PYTHON BANKING SYSTEM")
    print("==========")

    print("Bank data loaded successfully!")

    show_menu()

    choice = get_choice()

    if choice == "1":
        print("check balance selected")

    elif choice == "2":
        print("deposit selected")

    elif choice == "3":
        print("withdraw selected")

    elif choice == "4": 
        username = input("Enter sender's username: ")
        transfer_money(data, username)

    elif choice == "5":
        print("transaction history selected")
        username = input("Enter your username: ")
        if username in data["users"]:
            show_transaction_history(data, username)
        else:
            print("Invalid username.")

    elif choice == "6":
        print("exit selected")

    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
