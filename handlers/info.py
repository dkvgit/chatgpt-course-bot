from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from lessons_data import LESSONS

async def show_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "📚 Вот программа курса:\n\n"
    for lesson in LESSONS.values():
        text += f"• {lesson['title']}\n"

    await query.message.reply_text(text)
