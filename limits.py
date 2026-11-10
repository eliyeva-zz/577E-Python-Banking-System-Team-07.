from datetime import datetime

def check_reset_daily_limits(accounts):
    current_date = datetime.now().date().isoformat()
    stored_data = accounts.get('last_reset_data', current_date)

    if stored_data != current_date:
        accounts['daily_deposited'] = 0.00
        accounts['daily_withdrawal'] = 0.00
        accounts['daily_transfers'] = 0
        accounts['last_reset_data'] = current_date
    return accounts

def display_daily_limits(accounts):

    check_reset_daily_limits(accounts)

    deposit_used = accounts.get('daily_deposited', 0.00)
    deposit_max = 2000.00
    deposit_remaining = deposit_max - deposit_used

    withdraw_used = accounts.get('daily_withdrawal', 0.00)
    withdraw_max = 1000.00
    withdraw_remaining = withdraw_max - withdraw_used

    fee_free_limit = 500.00
    fee_free_remaining = fee_free_limit - withdraw_remaining

    transfers_used = accounts.get('daily_transfers', 0.00)
    transfers_max = 5

    print("\n================ DAILY LIMITS ================")
    print(f"Deposit used:               {deposit_used:.2f} / {deposit_max:.2f} AZN")
    print(f"Deposit remaining:          {deposit_remaining:.2f} AZN")
    print(f"Cash withdrawn:             {withdraw_used:.2f} / {withdraw_max:.2f} AZN")
    print(f"Cash withdrawal remaining:  {withdraw_remaining:.2f} AZN")
    print(f"Fee-free cash remaining:    {fee_free_remaining:.2f} AZN")
    print(f"Outgoing transfers:         {transfers_used} / {transfers_max}")
    print("==============================================")


