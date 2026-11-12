import json
import os
from datetime import date, datetime

DATA_FILE = "data.json"

def make_user(account_number, balance):
    return {
        "password_hash": "",
        "account_number": account_number,
        "balance": balance,
        "blocked": False,
        "failed_attempts": 0,
        "lockout_time": None,
        "daily": {
            "date": date.today().isoformat(),
            "deposit": 0,   
            "withdrawn": 0,
            "transfer_count": 0
        },
        "history": [],
    }

def create_default_data():
    return{
        "atm_cash": 500000,
        "next_txn_number": 1,
        "users":{
            "user01": make_user("10010001",250000),
            "user02": make_user("10010002",150000),
            "user03": make_user("10010003",300000),
        },
    }

def save_data(data):
    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_file, DATA_FILE)

def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Data file is corrupted. Creating a new one.")
        os.replace(DATA_FILE, DATA_FILE + ".broken")
        return None

def get_data():
    data = load_data()
    if data is None:
        data = create_default_data()
        save_data(data)
    return data

if __name__ == "__main__":
    print(get_data())