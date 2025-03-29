import requests
from dotenv import load_dotenv
import os
from utils.logging_utils import log_info, log_error

load_dotenv()

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{os.getenv('token')}/sendMessage"
        payload = {
            'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
            'text': message
        }
        response = requests.post(url, json=payload)
        log_info(f"Telegram message sent: {message}")
    except Exception as e:
        log_error(f"Error sending Telegram message: {e}")
