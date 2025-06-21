from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

PAID_USERS = set()
from handlers.menu import set_paid_users


# === /start ===
def set_paid_users(users_set):
    global PAID_USERS
    PAID_USERS = users_set


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Получаем параметр запуска, если был
    args = context.args
    source = args[0] if args else "direct"

    print(f"👤 Пользователь {user_id} запустил бота через: {source}")
    context.user_data["step"] = 0
    context.user_data["source"] = source

    # 🔐 Если пользователь с доступом — показываем расширенное меню
    if user_id in PAID_USERS:
        welcome_text = ("✅ С возвращением! У тебя есть полный доступ к курсу.\n\n"
                        "Выбери, что хочешь сделать:")

        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📚 Перейти к урокам", callback_data="go_paid_menu")],
                [InlineKeyboardButton("👉 Начать с начала", callback_data="step_0")],
                [InlineKeyboardButton("📋 Программа курса", callback_data="show_program")],
                [InlineKeyboardButton("💬 Поддержка", url="https://t.me/dekavetelega")]]))
        return

    # Сообщение для новичков
    welcome_text = ("👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"
                    "Ты можешь сразу начать бесплатно, купить доступ или посмотреть программу.")

    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("📚 Программа курса", callback_data="show_program")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")],
            [InlineKeyboardButton("💬 Поддержка", url="https://t.me/dekavetel")]]))
