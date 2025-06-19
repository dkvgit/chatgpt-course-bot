from telegram import Update
from telegram.ext import ContextTypes
from utils.access import save_paid_users

PAID_USERS = None  # Глобальная переменная, будет передана из main.py
OWNER_ID = 5425101564  # Можно заменить на os.getenv если хочешь

# Функция для передачи PAID_USERS из main.py
def set_paid_users(users_set):
    global PAID_USERS
    PAID_USERS = users_set

# Команда /grant <user_id>
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("⛔️ У тебя нет прав на выполнение этой команды.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Укажите ID пользователя: /grant 12345678")
        return

    try:
        target_id = int(context.args[0])
        PAID_USERS.add(target_id)
        save_paid_users(PAID_USERS)

        await update.message.reply_text(f"✅ Доступ выдан пользователю {target_id}")

        try:
            await context.bot.send_message(chat_id=target_id,
                text="✅ Спасибо! Доступ к полному курсу открыт. Напиши /menu чтобы продолжить.")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Доступ выдан, но не удалось отправить сообщение пользователю: {e}")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
