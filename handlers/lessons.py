# handlers/lessons.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from lessons_data import LESSONS
from datetime import datetime

async def log_lesson_access(user_id, lesson_id, username):
    """Логирование просмотра урока"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📊 Урок {lesson_id} просмотрен: ID {user_id} (@{username}) в {timestamp}")

async def send_protected_lesson(context, chat_id, lesson_key, user_id, username):
    """Отправка урока с защитой от копирования"""
    lesson = LESSONS[lesson_key]
    
    # Персонализированный заголовок
    personalized_title = f"{lesson['title']}\n\n👤 Персональный доступ: @{username}\n🆔 ID: {user_id}"
    
    # Отправка с защитой
    await context.bot.send_video(
        chat_id=chat_id, 
        video=lesson["file_id"], 
        caption=personalized_title,
        protect_content=True,  # 🔐 Запрет скриншотов и пересылки
        has_spoiler=False
    )
    
    # Логирование
    await log_lesson_access(user_id, lesson_key, username)

async def handle_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    username = query.from_user.username or "без_username"
    
    if data == "step_0":
        context.user_data["step"] = 1
        await send_protected_lesson(context, chat_id, "lesson_0", user_id, username)
        await context.bot.send_message(
            chat_id=chat_id, 
            text="Понравилось? Круто! Держите Урок 1.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Дальше", callback_data="step_1")]])
        )
    
    elif data == "step_1":
        context.user_data["step"] = 2
        await send_protected_lesson(context, chat_id, "lesson_1", user_id, username)
        await context.bot.send_message(
            chat_id=chat_id, 
            text="Посмотрели 1 Урок? Продолжаем.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Продолжить", callback_data="step_2")]])
        )
    
    elif data == "step_2":
        context.user_data["step"] = 3
        await context.bot.send_message(
            chat_id=chat_id,
            text="Вижу вам понравилось. Первые два видео были бесплатными. Приобретайте полный доступ по кнопке ниже.",
            protect_content=True,  # 🔐 Защита текста
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Купить мини курс", callback_data="buy")],
                [InlineKeyboardButton("❌ Не хочу покупать", callback_data="not_ready")]
            ])
        )
