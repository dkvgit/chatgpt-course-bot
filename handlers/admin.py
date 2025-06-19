from telegram import Update
from telegram.ext import ContextTypes
from utils.access import save_paid_users

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
        print(f"👉 Добавляем ID {target_id} в PAID_USERS")

        PAID_USERS.add(target_id)
        print(f"✅ Теперь PAID_USERS: {PAID_USERS}")

        save_paid_users(PAID_USERS)

        # Проверка содержимого файла:
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
