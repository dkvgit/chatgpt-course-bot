from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from lessons_data import LESSONS

PAID_USERS = set()  # пока временно, потом передадим из main.py

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in PAID_USERS:
        await update.message.reply_text("🔒 Доступно только после оплаты.")
        return
    await show_lessons_menu(context, update.message.chat.id)

async def open_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in PAID_USERS:
        await query.edit_message_text("🔒 Уроки доступны только после оплаты.")
        return

    key = query.data.replace("menu_", "")
    lesson = LESSONS.get(key)
    if lesson:
        await context.bot.send_video(chat_id=query.message.chat.id, video=lesson["file_id"], caption=lesson['title'])
        context.user_data["current_lesson"] = key
        await show_next_lesson_options(context, query.message.chat.id, key)

async def back_to_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in PAID_USERS:
        await query.edit_message_text("🔒 Уроки доступны только после оплаты.")
        return

    await show_lessons_menu(context, query.message.chat.id)

async def show_lessons_menu(context, chat_id):
    buttons = []
    for key, lesson in LESSONS.items():
        if key.startswith("lesson_"):
            buttons.append([InlineKeyboardButton(lesson["title"], callback_data=f"menu_{key}")])

    await context.bot.send_message(chat_id=chat_id, text="📚 Выбери урок:", reply_markup=InlineKeyboardMarkup(buttons))

async def show_next_lesson_options(context, chat_id, current_lesson_key):
    current_num = int(current_lesson_key.split('_')[1])
    next_num = current_num + 1
    next_key = f"lesson_{next_num}"

    buttons = []
    if next_key in LESSONS:
        next_title = LESSONS[next_key]["title"]
        buttons.append([InlineKeyboardButton(f"▶️ {next_title}", callback_data=f"menu_{next_key}")])

    buttons.append([
        InlineKeyboardButton("📚 Все уроки", callback_data="back_to_menu"),
        InlineKeyboardButton("🏠 В начало", callback_data="go_home")
    ])

    await context.bot.send_message(chat_id=chat_id, text="Перейти к следующему?", reply_markup=InlineKeyboardMarkup(buttons))

# ⬇️ новая функция
async def show_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "📚 Вот программа курса:\n\n"
    for lesson in LESSONS.values():
        text += f"• {lesson['title']}\n"

    await query.message.reply_text(text)
