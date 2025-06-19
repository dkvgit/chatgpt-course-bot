import json
import os

PAID_USERS_FILE = "paid_users.json"

# Загружаем пользователей при старте
def load_paid_users():
    if not os.path.exists(PAID_USERS_FILE):
        return set()
    try:
        with open(PAID_USERS_FILE, "r") as f:
            return set(json.load(f))
    except Exception as e:
        print("⚠️ Ошибка при загрузке paid_users.json:", e)
        return set()

# Сохраняем в файл
def save_paid_users(user_ids: set):
    try:
        with open(PAID_USERS_FILE, "w") as f:
            json.dump(list(user_ids), f)
    except Exception as e:
        print("⚠️ Ошибка при сохранении paid_users.json:", e)
