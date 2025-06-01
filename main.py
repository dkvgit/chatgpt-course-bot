from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/ai_chatgpt_course_bot"

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 О курсе", callback_data="about")],
        [InlineKeyboardButton("🎓 Получить доступ", callback_data="buy")],
        [InlineKeyboardButton("📦 Примеры", callback_data="demo")]
    ]
    await update.message.reply_text("Привет! Это курс ChatGPT для всех 👇", reply_markup=InlineKeyboardMarkup(keyboard))

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

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url="https://chatgpt-course-bot.onrender.com/webhook"
    )
