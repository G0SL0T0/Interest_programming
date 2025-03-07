import requests
from config import SLACK_WEBHOOK_URL

# Отправка сообщения в Slack
def send_slack_message(message):
    payload = {
        'text': message
    }
    requests.post(SLACK_WEBHOOK_URL, json=payload)