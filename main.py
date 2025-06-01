from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Загружаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
print("BOT_TOKEN =", BOT_TOKEN)  # 👈 убедись, что печатает корректно

# Ссылка на канал с курсом
CHANNEL_LINK = "https://t.me/ai_chatgpt_course_bot"

# Инициализация Flask и Telegram Bot API
app = Flask(__name__)
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 О курсе", callback_data="about")],
        [InlineKeyboardButton("🎓 Получить доступ", callback_data="buy")],
        [InlineKeyboardButton("📦 Примеры", callback_data="demo")]
    ]
    await update.message.reply_text("Привет! Это курс ChatGPT для всех 👇", reply_markup=InlineKeyboardMarkup(keyboard))

# Обработка нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.edit_message_text("💡 Этот курс научит тебя использовать ИИ: просто, с юмором и по делу.\nСтоимость: 990₽. Один раз и навсегда.")
    elif query.data == "buy":
        keyboard = [[InlineKeyboardButton("✅ Я оплатил", callback_data="paid")]]
        await query.edit_message_text("Переведи 990₽ на карту 1234 5678 9012 3456\nПосле этого нажми 'Я оплатил'", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "paid":
        await query.edit_message_text(f"Спасибо! Вот ссылка на курс:\n{CHANNEL_LINK}")
    elif query.data == "demo":
        await query.edit_message_text("Открытый урок: https://t.me/neuronica_news/1\nБлок 0 и Блок 1 — бесплатны!")

# Регистрируем обработчики
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    print("🔥 Webhook вызван")
    data = request.get_json(force=True)
    print("📦 Получено:", data)
    bot_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), bot_app.bot))
    return "ok"

# Проверка доступности сервиса
@app.route("/")
def root():
    return "Bot is alive"

# Запуск
if __name__ == "__main__":
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ["PORT"]),
        webhook_url=f"https://chatgpt-course-bot.onrender.com/{BOT_TOKEN}"
    )
