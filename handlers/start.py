from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.access import load_paid_users
from handlers.menu import show_lessons_menu

# Загружаем платных пользователей (если не передаёшь из main.py)
PAID_USERS = load_paid_users()

# === START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # 🔐 Если уже платный — сразу в меню
    if user_id in PAID_USERS:
        await update.message.reply_text(
            "✅ У тебя уже есть доступ ко всем урокам! Открываю меню 👇"
        )
        await show_lessons_menu(context, update.message.chat.id)
        return

    # Получаем параметр запуска
    args = context.args
    source = args[0] if args else "direct"

    # Отслеживаем источники переходов
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

    # Сохраняем в user_data
    context.user_data["step"] = 0
    context.user_data["source"] = source

    await update.message.reply_text(
        welcome_text + "Ты можешь сразу начать бесплатно, купить доступ или посмотреть программу.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("📚 Программа курса", callback_data="show_program")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")]
        ])
    )
