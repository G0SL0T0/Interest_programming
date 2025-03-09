import sqlite3
from dotenv import load_dotenv
import os
from utils.logging_utils import log_info, log_error

# Загружаем переменные окружения
load_dotenv()

# Подключение к базе данных
DATABASE_PATH = os.getenv('DATABASE_PATH')
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Создание таблицы (если её нет)
def init_db():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS sentiments
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           platform TEXT,
                           text TEXT,
                           sentiment REAL,
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        log_info("Database initialized successfully.")
    except Exception as e:
        log_error(f"Error initializing database: {e}")

# Сохранение данных
def save_to_db(platform, text, sentiment):
    try:
        cursor.execute("INSERT INTO sentiments (platform, text, sentiment) VALUES (?, ?, ?)",
                       (platform, text, sentiment))
        conn.commit()
        log_info(f"Data saved to database: {platform}, {text}, {sentiment}")
    except Exception as e:
        log_error(f"Error saving data to database: {e}")

# Получение данных
def fetch_data():
    try:
        cursor.execute("SELECT * FROM sentiments")
        return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching data from database: {e}")
        return []

# Закрытие соединения
def close_db():
    try:
        conn.close()
        log_info("Database connection closed.")
    except Exception as e:
        log_error(f"Error closing database connection: {e}")