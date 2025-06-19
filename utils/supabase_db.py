python
import os
from supabase import create_client, Client

# Загружаем URL и ключ из переменных окружения
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Создаём клиент
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ➕ Добавляем или обновляем user_id
def add_paid_user(user_id: int):
    response = supabase.table("paid_users").upsert({"user_id": user_id}).execute()
    return response

# 📥 Загружаем всех пользователей
def fetch_all_paid_users() -> set:
    try:
        response = supabase.table("paid_users").select("user_id").execute()
        return set(item["user_id"] for item in response.data or [])
    except Exception as e:
        print("⚠️ Ошибка при получении пользователей из Supabase:", e)
        return set()
