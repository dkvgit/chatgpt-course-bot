import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# === Загрузка переменных окружения ===
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Webhook настройки для Railway:
PORT = int(os.environ.get('PORT', 8000))
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL')

# === Импорты ===
from handlers.start import start, set_paid_users as set_start_paid_users
from handlers.lessons import handle_step
from handlers.payment import handle_payment_buttons
from handlers.menu import (
    menu,
    open_lesson,
    back_to_menu_handler,
    set_paid_users as set_menu_paid_users,
)
from handlers.admin import grant, revoke, list_paid, set_paid_users as set_admin_paid_users
from handlers.info import show_program, show_lessons_menu
from utils.supabase_db import fetch_all_paid_users

# === Загрузка платных пользователей ===
PAID_USERS = fetch_all_paid_users()
set_menu_paid_users(PAID_USERS)
set_admin_paid_users(PAID_USERS)
set_start_paid_users(PAID_USERS)

# === Обработчики ===

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("⛔️ Только администратор может загружать видео.")
        return
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"`{file_id}`", parse_mode='Markdown')

async def go_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text="👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"
             "Ты можешь сразу начать бесплатно или купить полный доступ ко всем урокам.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")]
        ])
    )

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👤 Твой user_id: {update.message.from_user.id}")

async def go_paid_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in PAID_USERS:
        await query.edit_message_text("🔒 Доступно только после оплаты.")
        return

    await show_lessons_menu(context, query.message.chat.id)

# === Запуск приложения ===
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("myid", my_id))
    application.add_handler(CommandHandler("grant", grant))
    application.add_handler(CommandHandler("revoke", revoke))
    application.add_handler(CommandHandler("list_paid", list_paid))
    application.add_handler(MessageHandler(filters.VIDEO, get_file_id))
    application.add_handler(CallbackQueryHandler(go_paid_menu_handler, pattern="^go_paid_menu$"))
    application.add_handler(CallbackQueryHandler(handle_step, pattern="^step_.*$"))
    application.add_handler(CallbackQueryHandler(handle_payment_buttons, pattern="^(buy|paid|not_ready|sepa_details|binance_details|cards_info|crypto_info|bank_info|additional_info)$"))
    application.add_handler(CallbackQueryHandler(go_home, pattern="^go_home$"))
    application.add_handler(CallbackQueryHandler(open_lesson, pattern="^menu_lesson_.*"))
    application.add_handler(CallbackQueryHandler(back_to_menu_handler, pattern="^back_to_menu$"))
    application.add_handler(CallbackQueryHandler(show_program, pattern="^show_program$"))

    # === Автоматический выбор: webhook на Railway, polling локально ===
    if RAILWAY_STATIC_URL:
        webhook_url = f"https://{RAILWAY_STATIC_URL}/webhook"
        print(f"🚀 Railway: запуск через webhook на {webhook_url}")
        print(f"🔧 PORT: {PORT}")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=webhook_url,
        )
    else:
        print("🚀 Локальный запуск через polling...")
        application.run_polling()



if __name__ == "__main__":
    main()
