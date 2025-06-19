from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# === START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем параметр запуска
    args = context.args
    source = args[0] if args else "direct"
    user_id = update.message.from_user.id

    # Отслеживаем источники переходов (можно логировать или сохранять в БД)
    if source == "landing":
        print(f"👤 Пользователь {user_id} пришел с лендинга")
        welcome_text = "👋 Добро пожаловать с нашего сайта в мини-курс «Нейросети без паники»!\n\n"
    elif source == "program":
        print(f"👤 Пользователь {user_id} пришел из программы курса")
        welcome_text = "👋 Отлично! Вы изучили программу и готовы начать мини-курс «Нейросети без паники»!\n\n"
    elif source == "webapp":
        print(f"👤 Пользователь {user_id} пришел из WebApp")
        welcome_text = "👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"
    else:
        print(f"👤 Пользователь {user_id} запустил бота напрямую")
        welcome_text = "👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"

    context.user_data["step"] = 0
    context.user_data["source"] = source  # Сохраняем источник для аналитики

    await update.message.reply_text(
        welcome_text + "Ты можешь сразу начать бесплатно или купить полный доступ ко всем урокам.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")]]))
