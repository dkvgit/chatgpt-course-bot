from telegram import Update
from telegram.ext import ContextTypes
from utils.access import save_paid_users
from utils.supabase_db import add_paid_user, fetch_all_paid_users, remove_paid_user
from handlers.menu import set_paid_users as set_menu_paid_users  # 👈 важно!
from handlers.start import set_paid_users as set_start_paid_users


PAID_USERS = None
OWNER_ID = 5425101564

def set_paid_users(users_set):
    global PAID_USERS
    PAID_USERS = users_set

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🛠 grant() ЗАПУЩЕН")
    print("PAID_USERS =", PAID_USERS)

    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("⛔️ У тебя нет прав на выполнение этой команды.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Укажите ID пользователя: /grant 12345678")
        return

    try:
        target_id = int(context.args[0])
        print(f"👉 Добавляем ID {target_id} в Supabase")

        add_paid_user(target_id)  # ⬅️ синхронно

        updated_users = fetch_all_paid_users()
        set_paid_users(updated_users)          # обновление в admin.py
        set_menu_paid_users(updated_users)     # ⬅️ обновление в menu.py
        set_start_paid_users(updated_users)
        save_paid_users(updated_users)

        print(f"✅ Обновлённый PAID_USERS: {updated_users}")

        try:
            with open("paid_users.json") as f:
                print("📂 paid_users.json =", f.read())
        except Exception as e:
            print("⚠️ Не удалось прочитать файл:", e)

        await update.message.reply_text(f"✅ Доступ выдан пользователю {target_id}")

        try:
            await context.bot.send_message(
                chat_id=target_id,
                text="✅ Спасибо! Доступ к полному курсу открыт. Напиши /menu чтобы продолжить."
            )
        except Exception as e:
            await update.message.reply_text(f"⚠️ Доступ выдан, но не удалось отправить сообщение пользователю: {e}")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🛠 revoke() ЗАПУЩЕН")
    print("PAID_USERS =", PAID_USERS)

    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("⛔️ У тебя нет прав на выполнение этой команды.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Укажите ID пользователя: /revoke 12345678")
        return

    try:
        target_id = int(context.args[0])
        print(f"🧹 Удаляем ID {target_id} из Supabase")

        remove_paid_user(target_id)

        updated_users = fetch_all_paid_users()
        set_paid_users(updated_users)
        set_menu_paid_users(updated_users)  # ⬅️ важно!
        set_start_paid_users(updated_users)  # ⬅️ и здесь тоже
        save_paid_users(updated_users)

        await update.message.reply_text(f"❌ Доступ удалён у пользователя {target_id}")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

async def list_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("⛔️ У тебя нет прав на выполнение этой команды.")
        return

    if not PAID_USERS:
        await update.message.reply_text("🤷 Пока нет ни одного пользователя с доступом.")
        return

    user_list = "\n".join(f"• `{uid}`" for uid in sorted(PAID_USERS))
    await update.message.reply_text(
        f"📋 Список пользователей с доступом:\n\n{user_list}",
        parse_mode="Markdown"
    )
