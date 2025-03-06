import sqlite3
from config import DATABASE_PATH

# Подключение к базе данных
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Создание таблицы (если её нет)
def init_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS sentiments
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       platform TEXT,
                       text TEXT,
                       sentiment REAL,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()

# Сохранение данных
def save_to_db(platform, text, sentiment):
    cursor.execute("INSERT INTO sentiments (platform, text, sentiment) VALUES (?, ?, ?)",
                   (platform, text, sentiment))
    conn.commit()

# Получение данных
def fetch_data():
    cursor.execute("SELECT * FROM sentiments")
    return cursor.fetchall()

# Закрытие соединения
def close_db():
    conn.close()