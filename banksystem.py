import time

def handle_login(username, password, users_db, save_callback):
    

    if username not in users_db:
        return False, " Belə bir istifadəçi mövcud deyil!"

    user = users_db[username]
    current_time = time.time()

    # 1. bloka dusmenin yoxlanmasi
    if user.get("is_blocked", False):
        print("\nMaximum login attempts exceeded.\nYour card has been blocked.\nPlease contact the bank administrator.")
        return False, "CARD_BLOCKED"

    # 2. 60 saniyəlik vaxtin yoxlaması
    lockout_until = user.get("lockout_until", 0.0)
    if current_time < lockout_until:
        print("\nToo many failed login attempts.")
        remaining = int(lockout_until - current_time)
        
        while remaining > 0:
            mins, secs = divmod(remaining, 60)
            print(f"\rPlease wait: {mins:02d}:{secs:02d}", end="", flush=True)
            time.sleep(1)
            remaining -= 1
        
        print("\nPlease wait: 00:00\nYou may try again.\n")
        user["lockout_until"] = 0.0
        save_callback()

    # 3. parol yoxlaması
    if password == user.get("password"):
        user["failed_attempts"] = 0
        user.update({"lockout_until": 0.0, "is_blocked": False})
        save_callback()
        return True, " Uğurla daxil oldunuz!"

    # 4. Şifrə səhvdirse, cəhdləri artırırıq
    user["failed_attempts"] = user.get("failed_attempts", 0) + 1
    attempts = user["failed_attempts"]
    
    print(f"Incorrect password. Attempt: {attempts}/6")

    # 6 səhv olarsa
    if attempts >= 6:
        user["is_blocked"] = True
        print("Maximum login attempts exceeded.\nYour card has been blocked.\nPlease contact the bank administrator.")
    
    # 3 səhv olarsa
    elif attempts == 3:
        user["lockout_until"] = time.time() + 60
        print("Too many failed login attempts.")

    save_callback()
    return False, "INCORRECT_PASSWORD"   

    # bax a buralar helem doldurulacaq

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