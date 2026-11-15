import json
import os
import hashlib
from datetime import date

DATA_FILE = "data.json"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def make_user(account_number, balance, password):
    return {
        "password_hash": hash_password(password),
        "account_number": account_number,
        "balance": balance,
        "blocked": False,
        "failed_attempts": 0,
        "lockout_until": 0.0,
        "daily": {
            "date": date.today().isoformat(),
            "deposit": 0,
            "withdrawn": 0,
            "transfer_count": 0,
        },
        "history": [],
    }


def save_data(data):
    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_file, DATA_FILE)


def create_default_data():
    return {
        "atm_cash": 500000,
        "next_txn_number": 1,
        "users": {
            "user01": make_user("10010001", 250000, "Test@123"),
            "user02": make_user("10010002", 150000, "Test@456"),
            "user03": make_user("10010003", 300000, "Test@789"),
        },
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Data file could not be read. Old file was kept and a new one was created.")
        os.replace(DATA_FILE, DATA_FILE + ".broken")
        return None


def get_data():
    data = load_data()
    if data is None:
        data = create_default_data()
        save_data(data)
    return data
