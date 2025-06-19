from telegram import Update
from telegram.ext import ContextTypes
from utils.access import save_paid_users  # ⬅️ добавь это

# PAID_USERS передадим из main.py
PAID_USERS = set()
OWNER_ID = 5425101564

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ Укажите ID пользователя: /grant 12345678")
        return

    try:
        target_id = int(context.args[0])
        PAID_USERS.add(target_id)
        save_paid_users(PAID_USERS)  # ⬅️ добавь эту строку

        await update.message.reply_text(f"✅ Доступ выдан пользователю {target_id}")
        await context.bot.send_message(chat_id=target_id,
            text="✅ Спасибо! Доступ к полному курсу открыт. Напиши /menu чтобы продолжить.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
