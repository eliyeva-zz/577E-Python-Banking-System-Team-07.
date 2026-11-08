import time
def handle_login(username, password, user_db, save_callback):
    if username not in user_db:
        return false, 'username does not exist'

        # olub olmadigini yoxlayir
    
    user=users_db[username]
    current_time = time.time()
    
        # qisaldir

    if user.get('is_blocked ', false ):
        print('\Maximum login attemp exceeded.\Your card has been blocked. \nPlease contact the bank administrator.')
        return false, 'CARD_BLOCKED'

        # blakda olub olmadigini yoxlayir get=tehlukesizlik

    lockout_time = user.get('lockout_time', 0.0)

    if current_time < lockout_until:
        print('\Too many failed login attemps.')
        remaining = int(lockout_until - current_time)

        while remaining > 0:
            mins, secs = divmod(remaining, 60)

        # divmod vaxti 60 la goturur 

            print(f'\rPlease wait {mins:02d}:{secs:02d} ', end='', flush=true)
            time.sleep(1)
            remaining -=1

        # \r evvele qaytarir flush birbasa gosterir time.sleep 1 san gozle deyir

        print('\nPlease wait : 00:00\nYou may try agan.\n')
        user['lockout_time'] = 0.0
        save_callback()
    
    if password == user.get('password'):
        user['failed_attempts'] = 0
        user.update({'lockout_until' : 0.0, 'is_blocked' :false})
        save_callback()
        return true, 'login successful'
    
    user['failed_attempts'] = user.get('failed_attempts', 0) + 1
    attemps = user['failed_attemps']

    print(f"Incorrect password. Attempt: {attempts}/6")

    # f formated string di yeni tenzimleyir

    if attempts >= 6:
        user['is_blocked'] = true
        print('Maximum login attemps exceeded.\nYour card has been blocked.\nPlease contact the bank administratior.')

    elif attemps == 3:
        user['lockout_until'] =time.time() + 60
        print("Too many failed login attempts.")

    save_callback()
    return false, 'INCORRECT_PASSWORD'

    # CALLBACK SAXLAYIR




# bax a buralar helem doldurulmalidir
def show_main_menu(username):
    
    while True:
        print("\n" + "=" * 36)
        print("PYTHON BANKING SYSTEM")
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
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            print("\n View Account Information seçildi (Hələ yazılmayıb).")
        elif choice == '2':
            print("\n Check Balance seçildi (Hələ yazılmayıb).")
        elif choice == '3':
            print("\n Deposit Money seçildi (Hələ yazılmayıb).")
        elif choice == '4':
            print("\n Withdraw Money seçildi (Hələ yazılmayıb).")
        elif choice == '5':
            print("\n Transfer Money seçildi (Hələ yazılmayıb).")
        elif choice == '6':
            print("\n Transaction History seçildi (Hələ yazılmayıb).")
        elif choice == '7':
            print("\n Daily Limits seçildi (Hələ yazılmayıb).")
        elif choice == '8':
            print("\n Change Password seçildi (Hələ yazılmayıb).")
        elif choice == '9':
            print("\n Hesabdan çıxış edilir (Logout)...")
            return "LOGOUT"  # Giriş ekranına qayıtmaq üçün
        elif choice == '0':
            print("\n Proqramdan çixilir. Sağ olun!")
            exit() 
        else:
            print("\n Yanliş seçim! Zəhmət olmasa 0-9 arasi rəqəm daxil edin.") 