import time


def handle_login(username, password, user_db, save_callback):
    if username not in user_db:
        return False, 'Username does not exist'

        # olub olmadigini yoxlayir
    
    user=user_db[username]
    current_time = time.time()
    
        # qisaldir

    if user.get('is_blocked', False ):
        print('\nMaximum login attemp exceeded.\nYour card has been blocked. \nPlease contact the bank administrator.')
        return False, 'CARD_BLOCKED'

        # blakda olub olmadigini yoxlayir get=tehlukesizlik

    lockout_time = user.get('lockout_time', 0.0)
    lockout_until = lockout_time + 60


    if current_time < lockout_until:
        print('\nToo many failed login attemps.')
        remaining = int(lockout_until - current_time)

        while remaining > 0:
            mins, secs = divmod(remaining, 60)

        # divmod vaxti 60 la goturur 

            print(f'\rPlease wait {mins:02d}:{secs:02d} ', end='', flush=True)
            time.sleep(1)
            remaining -=1

        # \r evvele qaytarir flush birbasa gosterir time.sleep 1 san gozle deyir

        print('\nPlease wait : 00:00\nYou may try agan.\n')
        user['lockout_time'] = 0.0
        save_callback()

    hashed_password = hash_password(password)

    
    if hashed_password == user.get('password'):
        user['failed_attempts'] = 0
        user.update({'lockout_until' : 0.0, 'is_blocked' :False})
        save_callback()
        return True, 'login successful'
    
    user['failed_attempts'] = user.get('failed_attempts', 0) + 1
    attempts = user['failed_attempts']

    print(f"Incorrect password.\n Attempt: {attempts}/6")

    # f formated string di yeni tenzimleyir

    if attempts >= 6:
        user['is_blocked'] = True
        print('Maximum login attemps exceeded.\nYour card has been blocked.\nPlease contact the bank administratior.')

    elif attempts == 3:
        user['lockout_time'] =time.time() + 60
        print("Too many failed login attempts.")

    




# bax a buralar helem doldurulmalidir
def show_main_menu(username, user_db=None, save_callback=None):

    # xeta vermesin deye
    
    while True:
        print("\n" + "=" * 36)
        print("PYTHON BANKING SYSTEM")
        print("=" * 36)
        print(f"welcome, {username}!")
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
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            print("\n View Account Information seçildi (Hələ yazilmayib).")
        elif choice == '2':
            print("\n Check Balance seçildi (Hələ yazilmayib).")
        elif choice == '3':
            print("\n Deposit Money seçildi (Hələ yazilmayib).")
        elif choice == '4':
            print("\n Withdraw Money seçildi (Hələ yazilmayib).")
        elif choice == '5':
            print("\n Transfer Money seçildi (Hələ yazilmayib).")
        elif choice == '6':
            print("\n Transaction History seçildi (Hələ yazilmayib).")
        elif choice == '7':
            print("\n Daily Limits seçildi (Hələ yazilmayib).")
        elif choice == '8':
            if user_db and save_callback:
                change_password(username, user_db, save_callback)
            else:
              print("\n Change password hele yoxdur ")
        elif choice == '9':
            print("\n Hesabdan çixiş edilir (Logout)...")
            return 'LOGOUT'  

        # girise qayitmaq ucun

        elif choice == '0':
            print('\n Exit...')
            exit()
        else:
            print('\n Invalid option. Please try again.')

 

    save_callback()
    return False, "INCORRECT_PASSWORD"   




    # password deyismeleri


import json 
import os
import hashlib 

# bu py da var hash lamaq ucundu bururlari inceele..........

def register_user(username, password):
    password_bytes = password.encode('utf-8')
    hashed_password_text = hashlib.sha256(password_bytes).hexdigest()

    # Kompüterlər mətnləri birbaşa başa düşmür, onları baytlara (1 və 0-lara) çevirməlidir. encode('utf-8') istifadəçinin daxil etdiyi mətni (məsələn, "Test@123") kompüterin oxuya biləcəyi bayt ardıcıllığına (bytes) çevirir.
    #SHA-256 — bir tərəfli şifrələmə (hash) alqoritmidir.
    new_user = {
        "username": username,
        "password": hashed_password_text,
        "failed_attempts": 0,
        "is_blocked": False,
        "lockout_time": 0.0}

    users_data = {}
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as file:
            try:
                users_data = json.load(file)
            except json.JSONDecodeError:
                users_data = {}
    

    users_data[username] = new_user
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users_data, file, ensure_ascii=False, indent=4)



    print(f'successful registration: {username}')
    return new_user





def change_password(username, user_db, save_callback):
    print("\nchnage password")
    current_pwd = input("Enter current password: ")

    hashed_current = hashlib.sha256(current_pwd.encode('utf-8')).hexdigest()
    if hashed_current != user_db[username].get('password'):
        print('error: Current password is incorrect.')
        return False

    new_pwd = input("Enter new password(at least 8 symbols, one uppercase, one lowercase, one digit): ") 
    if len(new_pwd) < 8 or not any(c.isupper() for c in new_pwd) or not any(c.islower() for c in new_pwd) or not any(c.isdigit() for c in new_pwd):
        print('error: New password does not meet the criteria.')
        return False



    if new_pwd == current_pwd:
        print('error: New password cannot be the same as the current password.')
        return False


    confirm_pwd = input('please confirm new password again: ')
    if new_pwd != confirm_pwd:
        print('error: Passwords do not match.')
        return False


    hashed_new = hashlib.sha256(new_pwd.encode('utf-8')).hexdigest()
    user_db[username]['password'] = hashed_new



    try:
        save_callback(user_db)
    except TypeError:
        save_callback()

    print('Password changed successfully.')
    return True






























        























