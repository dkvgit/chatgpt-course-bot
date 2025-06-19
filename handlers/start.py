from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
PAID_USERS = set()
from handlers.menu import set_paid_users

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # 🔐 Если пользователь с доступом — показываем отдельную кнопку
    if user_id in PAID_USERS:
        await update.message.reply_text(
            "✅ У тебя уже есть доступ ко всем урокам! 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 Перейти к урокам", callback_data="go_paid_menu")]
            ])
        )
        return

    # Получаем параметр запуска, если был
    args = context.args
    source = args[0] if args else "direct"

    print(f"👤 Пользователь {user_id} запустил бота через: {source}")
    context.user_data["step"] = 0
    context.user_data["source"] = source

    # Сообщение для новичков
    welcome_text = (
        "👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"
        "Ты можешь сразу начать бесплатно, купить доступ или посмотреть программу."
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("📚 Программа курса", callback_data="show_program")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")]
        ])
    )
