# handlers/payment.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from lessons_data import LESSONS

# 👤 ID владельца
OWNER_ID = 5425101564

# 💰 Хранилище платных пользователей (пока в памяти)
PAID_USERS = set()

async def handle_payment_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "buy":
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text="💳 Выберите удобный способ оплаты мини-курса (500₽):",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Revolut", url="https://revolut.me/r/hJG50OBCC4")],
                [InlineKeyboardButton("🔁 Я оплатил — проверить доступ", callback_data="paid")]
            ])
        )

    elif query.data == "paid":
        if user_id in PAID_USERS:
            await context.bot.send_message(chat_id=query.message.chat.id,
                text="✅ У тебя уже есть доступ ко всем урокам.")
            await show_lessons_menu(context, query.message.chat.id)
        else:
            await context.bot.send_message(chat_id=query.message.chat.id,
                text="🕐 Заявка на доступ отправлена. Проверка оплаты может занять до 10 минут.\n\n"
                     "Если ты уже оплатил, напиши свой ник или ID в личку: @dekavetel")
            username = query.from_user.username or "не указан"
            await context.bot.send_message(chat_id=OWNER_ID,
                text=f"🔔 Новый запрос на доступ от пользователя @{username} (ID: {user_id})")

    elif query.data == "not_ready":
        await context.bot.send_message(chat_id=query.message.chat.id,
            text="Понимаю! Когда будешь готов — напиши /start.\n\nСпасибо за внимание к курсу! 😊")

# ⬇️ Эту функцию импортируем из main.py, позже вынесем тоже
async def show_lessons_menu(context, chat_id):
    buttons = []
    for key, lesson in LESSONS.items():
        if key.startswith("lesson_"):
            buttons.append([InlineKeyboardButton(lesson["title"], callback_data=f"menu_{key}")])

    await context.bot.send_message(chat_id=chat_id, text="📚 Выбери урок:", reply_markup=InlineKeyboardMarkup(buttons))
