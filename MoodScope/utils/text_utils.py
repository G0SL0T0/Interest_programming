import re

# Очистка текста
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Удаляем ссылки
    text = re.sub(r'[^\w\s]', '', text)  # Удаляем спецсимволы
    return text.strip()