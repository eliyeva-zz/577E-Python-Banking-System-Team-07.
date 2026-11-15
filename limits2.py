from datetime import date

DAILY_DEPOSIT_MAX = 200000
DAILY_WITHDRAW_MAX = 100000
FEE_FREE_LIMIT = 50000
FEE_PERCENT = 2
DAILY_TRANSFER_MAX = 5


#ffffffffffffffffffffffffffffffffffffff


def format_azn(qepik):
    
    sign = "-" if qepik < 0 else ""
    qepik = abs(qepik)
    return f"{sign}{qepik // 100}.{qepik % 100:02d}"






def check_reset_daily_limits(user):
    """Gun deyisibse user["daily"] icindeki sayaclari sifirlayir."""
    today = date.today().isoformat()
    daily = user["daily"]

    if daily.get("date") != today:
        daily["deposit"] = 0
        daily["withdrawn"] = 0
        daily["transfer_count"] = 0
        daily["date"] = today


def display_daily_limits(user):
    check_reset_daily_limits(user)
    daily = user["daily"]

    deposit_used = daily["deposit"]
    deposit_remaining = DAILY_DEPOSIT_MAX - deposit_used

    withdrawn_used = daily["withdrawn"]
    withdrawn_remaining = DAILY_WITHDRAW_MAX - withdrawn_used

    # 500'e qeder pulsuz; 500'u kecende 0
    fee_free_remaining = max(0, FEE_FREE_LIMIT - withdrawn_used)

    transfers_used = daily["transfer_count"]

    print("\n=========== DAILY LIMITS ===========")
    print(f"Deposit used:               {format_azn(deposit_used)} / {format_azn(DAILY_DEPOSIT_MAX)} AZN")
    print(f"Deposit remaining:          {format_azn(deposit_remaining)} AZN")
    print(f"Cash withdrawn:             {format_azn(withdrawn_used)} / {format_azn(DAILY_WITHDRAW_MAX)} AZN")
    print(f"Cash withdrawal remaining:  {format_azn(withdrawn_remaining)} AZN")
    print(f"Fee-free cash remaining:    {format_azn(fee_free_remaining)} AZN")
    print(f"Outgoing transfers:         {transfers_used} / {DAILY_TRANSFER_MAX}")
    print("====================================")