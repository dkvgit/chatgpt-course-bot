from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from aiohttp import web
import os

BOT_TOKEN = "7376438241:AAG9hmZKKZJ38le5m6Pk7DjDjwMNWed9l5A"
CHANNEL_LINK = "https://t.me/ai_chatgpt_course_bot"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 О курсе", callback_data="about")],
        [InlineKeyboardButton("🎓 Получить доступ", callback_data="buy")],
        [InlineKeyboardButton("📦 Примеры", callback_data="demo")]
    ]
    await update.message.reply_text("Привет! Это курс ChatGPT для всех 👇", reply_markup=InlineKeyboardMarkup(keyboard))

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "about":
        await query.edit_message_text("💡 Этот курс научит тебя использовать ИИ: просто, с юмором и по делу.\nСтоимость: 990₽.")
    elif query.data == "buy":
        keyboard = [[InlineKeyboardButton("✅ Я оплатил", callback_data="paid")]]
        await query.edit_message_text("Переведи 990₽ на карту 1234 5678 9012 3456\nПосле этого нажми 'Я оплатил'", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "paid":
        await query.edit_message_text(f"Спасибо! Вот ссылка на курс:\n{CHANNEL_LINK}")
    elif query.data == "demo":
        await query.edit_message_text("Открытый урок: https://t.me/neuronica_news/1")

# Инициализация бота
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))

# AIOHTTP app и webhook
app = web.Application()

# Webhook POST
async def handle_webhook(request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.update_queue.put(update)
    return web.Response(text="OK")

# Корневой маршрут GET /
async def root(request):
    return web.Response(text="Bot is alive")

# Роутинг
app.router.add_post(f"/{BOT_TOKEN}", handle_webhook)
app.router.add_get("/", root)

# Запуск сервера
if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT", 10000)))
