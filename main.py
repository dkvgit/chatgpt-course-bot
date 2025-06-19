from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os
from aiohttp import web
from handlers.start import start
from lessons_data import LESSONS
from handlers.lessons import handle_step
from handlers.payment import handle_payment_buttons
from handlers.menu import menu, open_lesson, back_to_menu_handler
from utils.access import load_paid_users, save_paid_users





# === Переменные окружения ===
BOT_TOKEN="7927577300:AAGM-KTDK3eAx8sS59fWaEKCF4ZZYtNgI18"
OWNER_ID=5425101564
RAILWAY_STATIC_URL="web-production-c31c.up.railway.app"

PORT = int(os.getenv("PORT", 8080))
PAID_USERS = load_paid_users()


# === КНОПКИ ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()


# === Получение file_id (только для админа) ===
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("⛔️ Только администратор может загружать видео.")
        return
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"`{file_id}`", parse_mode='Markdown')


# === Обработчик для кнопки "В начало" ===
async def go_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Создаем новое сообщение вместо попытки подмены update
    await context.bot.send_message(chat_id=query.message.chat.id,
        text="👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"
             "Ты можешь сразу начать бесплатно или купить полный доступ ко всем урокам.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")]]))


# === Узнать свой user_id ===
async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👤 Твой user_id: {update.message.from_user.id}")


# === Выдача доступа (только для админа) ===
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ Укажите ID пользователя: /grant 12345678")
        return

    try:
        target_id = int(context.args[0])
        PAID_USERS.add(target_id)

        # Логируем выдачу доступа
        print(f"💰 Админ выдал доступ пользователю {target_id}")

        await update.message.reply_text(f"✅ Доступ выдан пользователю {target_id}")
        await context.bot.send_message(chat_id=target_id,
            text="✅ Спасибо! Доступ к полному курсу открыт. Напиши /menu чтобы продолжить.")
    except (ValueError, IndexError):
        await update.message.reply_text("⚠️ Неверный ID или ошибка.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при отправке уведомления пользователю: {e}")
        

# === ЗАПУСК ===
async def handle_webhook(request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return web.Response(text="OK")

async def on_startup(app):
    await application.initialize()
    await application.start()
    webhook_url = f"https://{RAILWAY_STATIC_URL}/{BOT_TOKEN}"
    print("📡 Установка webhook:", webhook_url)
    await application.bot.set_webhook(webhook_url)

async def root(request):
    return web.Response(text="🤖 Бот работает")

# === Инициализация Telegram бота ===
application = ApplicationBuilder().token(BOT_TOKEN).build()

# === Добавь свои handlers сюда ===
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("menu", menu))
application.add_handler(CommandHandler("myid", my_id))
application.add_handler(CommandHandler("grant", grant))
application.add_handler(MessageHandler(filters.VIDEO, get_file_id))
application.add_handler(CallbackQueryHandler(handle_step, pattern="^step_.*$"))  # step_0, step_1, step_2
application.add_handler(CallbackQueryHandler(handle_payment_buttons, pattern="^(buy|paid|not_ready)$"))
application.add_handler(CallbackQueryHandler(go_home, pattern="^go_home$"))
application.add_handler(CallbackQueryHandler(open_lesson, pattern="^menu_lesson_.*"))
application.add_handler(CallbackQueryHandler(back_to_menu_handler, pattern="^back_to_menu$"))

# === aiohttp сервер Railway ===
web_app = web.Application()
web_app.router.add_post(f"/{BOT_TOKEN}", handle_webhook)
web_app.router.add_get("/", root)
web_app.on_startup.append(on_startup)

if __name__ == "__main__":
    print("🚀 Запуск на Railway...")
    web.run_app(web_app, port=PORT)
