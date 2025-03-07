import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Отправка сообщения в Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, json=payload)