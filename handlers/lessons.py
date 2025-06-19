# handlers/lessons.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from lessons_data import LESSONS

async def handle_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat.id

    if data == "step_0":
        context.user_data["step"] = 1
        lesson = LESSONS["lesson_0"]
        await context.bot.send_video(chat_id=chat_id, video=lesson["file_id"], caption=lesson['title'])
        await context.bot.send_message(chat_id=chat_id, text="Понравилось? Круто! Держите Урок 1.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Дальше", callback_data="step_1")]]))

    elif data == "step_1":
        context.user_data["step"] = 2
        lesson = LESSONS["lesson_1"]
        await context.bot.send_video(chat_id=chat_id, video=lesson["file_id"], caption=lesson['title'])
        await context.bot.send_message(chat_id=chat_id, text="Посмотрели 1 Урок? Продолжаем.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Продолжить", callback_data="step_2")]]))

    elif data == "step_2":
        context.user_data["step"] = 3
        await context.bot.send_message(chat_id=chat_id,
            text="Вижу вам понравилось. Первые два видео были бесплатными. Приобретайте полный доступ по кнопке ниже.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Купить мини курс", callback_data="buy")],
                [InlineKeyboardButton("❌ Не хочу покупать", callback_data="not_ready")]
            ]))
