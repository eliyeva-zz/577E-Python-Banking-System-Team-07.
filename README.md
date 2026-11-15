# 577E-Python-Banking-System

Console-based multi-user banking and ATM simulation in Python
(Fundamentals of Programming, Group 577E 07).

## Team
| Member | Responsibility |

| [Zuleyxa] (Member A, team lead) |

Authentication, failed-attempt tracking, 60-second countdown, card blocking, password change (`banksystem.py`) |

| [Murad] (Member B) |

Deposits, withdrawals, commission, ATM reserve, daily limits (`deposit.py`, `withdrawal2.py`, `limits2.py`) |

| [Ekber] (Member C) | 

Transfers, transaction history, storage (`transfers.py`, `history.py`, `storage.py`) |


## How to run
Python 3.10+ required (standard library only).

    python main.py

## Demo accounts
| Username | Password | Opening balance | Account number |
|---|---|---|---|
| user01 | Test@123 | 2500.00 AZN | 10010001 |
| user02 | Test@456 | 1500.00 AZN | 10010002 |
| user03 | Test@789 | 3000.00 AZN | 10010003 |

Created automatically on first run. Passwords are stored as SHA-256 hashes.

## Features and exact limits
- Login: 3 wrong passwords -> 60-second countdown (survives restart);
  6 wrong passwords -> card blocked permanently.
- Deposit: max 2000.00 AZN per day, no commission. A deposit that would
  exceed the limit is rejected entirely.
- Withdrawal: max 1000.00 AZN per day. The first 500.00 AZN per day is
  free; 2% fee on the part above 500.00 AZN.
- ATM reserve: shared, starts at 5000.00 AZN, never negative.
- Transfer: by account number, with Y/N confirmation, max 5 outgoing
  transfers per day. ATM reserve is not changed.
- Transaction history: last 10 operations per user.
- Change password: min 8 chars, upper, lower and digit; entered twice.
- Daily counters reset on a new calendar day, not on restart.
- Money is stored in qepik (100 = 1 AZN) to avoid float errors.

## Files
- `main.py` - login screen and 10-option menu
- `banksystem.py` - login, lockout, password change
- `deposit.py` - account info, balance, deposit, amount validation
- `withdrawal2.py` - withdrawal and commission
- `limits2.py` - daily limits, reset, `format_azn`
- `transfers.py` - transfers
- `history.py` - transaction records and display
- `storage.py` - JSON storage (`data.json`, created at runtime)

## Branch / PR workflow
`feature/*` and `bugfix/*` -> Pull Request -> `develop` -> `main`.

## Tests performed
Correct login; 3 wrong passwords (timer); 6 wrong passwords (block);
deposit limit (1800 + 300 rejected); commission (400 then 250 = 3.00 fee);
1000 daily maximum (950 + 100 rejected); transfer and 6th-transfer
rejection; unknown account; cancelled transfer; restart persistence;
password change.

## Known limitations
- Failed login attempts are counted per account.
- No administrator console (optional feature not implemented).
- Passwords are hashed with SHA-256 without salt.