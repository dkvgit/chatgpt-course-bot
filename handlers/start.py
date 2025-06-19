from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 👋 Добро пожаловать в курс!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Начать", callback_data="step_0")]
        ])
    )
