import json
import os
from datetime import datetime

if not os.path.exists("data/economy.json"):
    with open("data/economy.json", "w") as f:
        json.dump({}, f)

if not os.path.exists("data/daily.json"):
    with open("data/daily.json", "w") as f:
        json.dump({}, f)

def get_balance(user_id):
    with open("data/economy.json", "r") as f:
        economy = json.load(f)
    return economy.get(user_id, 0)

def update_balance(user_id, amount):
    with open("data/economy.json", "r") as f:
        economy = json.load(f)
    economy[user_id] = economy.get(user_id, 0) + amount
    with open("data/economy.json", "w") as f:
        json.dump(economy, f)

def get_last_daily(user_id):
    with open("data/daily.json", "r") as f:
        daily = json.load(f)
    last_daily = daily.get(user_id)
    return datetime.fromisoformat(last_daily) if last_daily else None

def set_last_daily(user_id, date):
    with open("data/daily.json", "r") as f:
        daily = json.load(f)
    daily[user_id] = date.isoformat()
    with open("data/daily.json", "w") as f:
        json.dump(daily, f)