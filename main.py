from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os
from dotenv import load_dotenv
load_dotenv()
from aiohttp import web

# handlers
from handlers.start import start
from handlers.lessons import handle_step
from handlers.payment import handle_payment_buttons
from handlers.menu import menu, open_lesson, back_to_menu_handler
from handlers.admin import grant  # ⬅️ вот он
from lessons_data import LESSONS
from handlers.info import show_program

    

# utils
from utils.access import load_paid_users, save_paid_users


# === Переменные окружения ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
RAILWAY_STATIC_URL = os.getenv("RAILWAY_STATIC_URL")
PORT = int(os.getenv("PORT", 8080))

PAID_USERS = load_paid_users()





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
application.add_handler(CallbackQueryHandler(show_program, pattern="^show_program$"))


# === aiohttp сервер Railway ===
web_app = web.Application()
web_app.router.add_post(f"/{BOT_TOKEN}", handle_webhook)
web_app.router.add_get("/", root)
web_app.on_startup.append(on_startup)

if __name__ == "__main__":
    print("🚀 Запуск на Railway...")
    web.run_app(web_app, port=PORT)
