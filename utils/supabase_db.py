import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ➕ Добавляем пользователя
async def add_paid_user(user_id: int):
    return await supabase.table("paid_users").upsert({"user_id": user_id}).execute()

# 📥 Получаем всех
async def fetch_all_paid_users() -> set:
    try:
        response = await supabase.table("paid_users").select("user_id").execute()
        return set(item["user_id"] for item in response.data or [])
    except Exception as e:
        print("⚠️ Ошибка при получении пользователей:", e)
        return set()

# ❌ Удаляем пользователя
async def remove_paid_user(user_id: int):
    try:
        return await supabase.table("paid_users").delete().eq("user_id", user_id).execute()
    except Exception as e:
        print("⚠️ Ошибка при удалении пользователя:", e)
