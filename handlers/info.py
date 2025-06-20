from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from lessons_data import LESSONS

# 👇 Добавлено — используется в go_paid_menu_handler
async def show_lessons_menu(context, chat_id):
    buttons = []
    for key, lesson in LESSONS.items():
        if key.startswith("lesson_"):
            buttons.append([InlineKeyboardButton(lesson["title"], callback_data=f"menu_{key}")])

    await context.bot.send_message(
        chat_id=chat_id,
        text="📚 Выбери урок:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Уже было
async def show_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "📚 Вот программа курса:\n\n"
    for lesson in LESSONS.values():
        text += f"• {lesson['title']}\n"

    await query.message.reply_text(text)
