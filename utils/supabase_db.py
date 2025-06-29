# utils/supabase_db.py
import os
from supabase import create_client
from supabase.lib.client_options import ClientOptions

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY, options=ClientOptions())

def add_paid_user(user_id: int):
    return supabase.table("paid_users").upsert({"user_id": user_id}).execute()

def fetch_all_paid_users() -> set:
    try:
        response = supabase.table("paid_users").select("user_id").execute()
        return set(item["user_id"] for item in response.data or [])
    except Exception as e:
        print("⚠️ Ошибка при получении пользователей:", e)
        return set()

def remove_paid_user(user_id: int):
    try:
        return supabase.table("paid_users").delete().eq("user_id", user_id).execute()
    except Exception as e:
        print("⚠️ Ошибка при удалении пользователя:", e)
