import time
from storage import hash_password

LOCKOUT_SECONDS = 60
MAX_ATTEMPTS = 6


def run_countdown(user, save_callback):
    
    print("\nToo many failed login attempts.")
    remaining = int(user["lockout_until"] - time.time())
    while remaining >= 0:
        mins, secs = divmod(remaining, 60)
        print(f"Please wait: {mins:02d}:{secs:02d}")
        if remaining > 0:
            time.sleep(1)
        remaining -= 1
    print("You may try again.\n")
    user["lockout_until"] = 0.0
    save_callback()


def handle_login(username, password, user_db, save_callback):
    if username not in user_db:
        print("Invalid username or password.")
        return False, "NO_USER"

    user = user_db[username]

    if user.get("blocked", False):
        print("\nMaximum login attempts exceeded.")
        print("Your card has been blocked.")
        print("Please contact the bank administrator.")
        return False, "CARD_BLOCKED"

    #  lockout save in the file surviv restart

    if time.time() < user.get("lockout_until", 0.0):
        run_countdown(user, save_callback)

    if hash_password(password) == user["password_hash"]:
        user["failed_attempts"] = 0
        user["lockout_until"] = 0.0
        save_callback()
        return True, "LOGIN_OK"

    user["failed_attempts"] += 1
    attempts = user["failed_attempts"]
    print(f"Incorrect password. Attempt: {attempts}/{MAX_ATTEMPTS}")

    if attempts >= MAX_ATTEMPTS:
        user["blocked"] = True
        save_callback()
        print("\nMaximum login attempts exceeded.")
        print("Your card has been blocked.")
        print("Please contact the bank administrator.")
        return False, "CARD_BLOCKED"

    if attempts == 3:
        user["lockout_until"] = time.time() + LOCKOUT_SECONDS
        save_callback()
        
         # save first
        
        run_countdown(user, save_callback)

    save_callback()
    return False, "INCORRECT_PASSWORD"


def is_strong_password(password):
    return (len(password) >= 8
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password))


def change_password(username, user_db, save_callback):
    user = user_db[username]
    print("\n--- CHANGE PASSWORD ---")

    current_pwd = input("Enter current password: ")
    if hash_password(current_pwd) != user["password_hash"]:
        print("Error: Current password is incorrect.")
        return False

    new_pwd = input("Enter new password (min 8 chars, upper, lower, digit): ")
    if not is_strong_password(new_pwd):
        print("Error: New password does not meet the requirements.")
        return False

    if new_pwd == current_pwd:
        print("Error: New password cannot be the same as the old one.")
        return False

    confirm_pwd = input("Enter new password again: ")
    if new_pwd != confirm_pwd:
        print("Error: Passwords do not match.")
        return False

    user["password_hash"] = hash_password(new_pwd)
    save_callback()
    print("Password changed successfully.")
    return True