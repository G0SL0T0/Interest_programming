import json
import os

if not os.path.exists("data/economy.json"):
    with open("data/economy.json", "w") as f:
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