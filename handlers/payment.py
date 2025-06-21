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
        await context.bot.send_message(chat_id=query.message.chat.id, text="""🔸 **Поддержать проект / Выберите удобный способ:**

    💰 **Стоимость курса: 500₽ / 6 EUR / 6 USDT**""", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("💳 🔸 Быстрая оплата картой 🔸", callback_data="cards_info")],
                [InlineKeyboardButton("PayPal", url="https://paypal.me/dkvpay"),
                 InlineKeyboardButton("Boosty", url="https://boosty.to/dkvboosty/donate"),
                 InlineKeyboardButton("Ko-fi", url="https://ko-fi.com/dkvkofi")],
                [InlineKeyboardButton("💰 🔸 Криптовалюта (анонимно) 🔸", callback_data="crypto_info")],
                [InlineKeyboardButton("Запросить адрес (BTC/USDT/ETH)", url="https://t.me/dekavetel")],
                 [InlineKeyboardButton("Binance Pay", callback_data="binance_details")],
                [InlineKeyboardButton("💸 🔸 Переводы 🔸", callback_data="bank_info")],
                [InlineKeyboardButton("Wise", url="https://wise.com/pay/me/denissk128"),
                 InlineKeyboardButton("Revolut", url="https://revolut.me/denmailde"),
                 InlineKeyboardButton("SEPA (EUR)", callback_data="sepa_details")],
                [InlineKeyboardButton("⭐ 🔸 Дополнительно 🔸", callback_data="additional_info")],
                [InlineKeyboardButton("DonationAlerts", url="https://www.donationalerts.com/r/najug")],
                [InlineKeyboardButton("🔁 Я оплатил — проверить доступ", callback_data="paid")],
                [InlineKeyboardButton("💬 Поддержка", url="https://t.me/dekavetel")]]), parse_mode="Markdown")

    elif query.data in ["cards_info", "crypto_info", "bank_info", "additional_info"]:
        await query.answer("Выберите способ оплаты ниже ⬇️")

    elif query.data == "sepa_details":
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text="""💸 **SEPA-перевод (EUR)**

⏰ **Внимание:** Обработка платежа может занять до 3 рабочих дней!

**Реквизиты получателя:**
👤 **Имя:** Deniss Kabakovs
🏦 **IBAN:** LT67 3250 0982 5028 7638
🔢 **BIC/SWIFT:** REVOLT21
🏛️ **Банк:** Revolut Bank UAB
📍 **Адрес банка:** Kostitucijos ave. 21B, 08130, Vilnius, Lithuania

💰 **Сумма:** 6 EUR (примерно 500₽)
📝 **Назначение платежа:** AI Course + ваш @username

⚠️ **Важно:**
- Комиссия за перевод на стороне отправителя
- Обработка 1-3 рабочих дня
- После оплаты пришлите скриншот в @dekavetel

После подтверждения получите доступ к курсу!""",
            parse_mode="Markdown"
        )

    elif query.data == "binance_details":
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text="""₿ **Binance Pay**

💰 **Pay ID:** 39933544

📝 **Инструкция:**
1. Откройте приложение Binance
2. Перейдите в раздел "Pay"
3. Выберите "Отправить"
4. Введите Pay ID: **39933544**
5. Укажите сумму: **6 USDT** (примерно 500₽)
6. Добавьте заметку: "AI Course + ваш @username"
7. Подтвердите перевод

После оплаты пришлите скриншот в @dekavetel для подтверждения!""",
            parse_mode="Markdown"
        )

    elif query.data == "paid":
        if user_id in PAID_USERS:
            await context.bot.send_message(chat_id=query.message.chat.id,
                text="✅ У тебя уже есть доступ ко всем урокам.")
            await show_lessons_menu(context, query.message.chat.id)
        else:
            await context.bot.send_message(chat_id=query.message.chat.id,
                text="🕐 Если ты уже оплатил, пришли скриншоты оплаты в поддержку: @dekavetel. Проверка оплаты "
                     "может "
                     "занять до 10 "
                     "минут.\n\n"
                     "",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💬 Написать в поддержку", url="https://t.me/dekavetel")]
                ])
            )
            username = query.from_user.username or "не указан"
            await context.bot.send_message(chat_id=OWNER_ID,
                text=f"🔔 Новый запрос на доступ от пользователя \n@{username} (ID: {user_id})")

    elif query.data == "not_ready":
        await context.bot.send_message(chat_id=query.message.chat.id,
            text="Понимаю! Когда будешь готов — напиши /start.\n\nСпасибо за внимание к курсу! 😊\n\n"
                 "Если есть вопросы — обращайся в поддержку.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Поддержка", url="https://t.me/dekavetelega")]
            ])
        )

# ⬇️ Эту функцию импортируем из main.py, позже вынесем тоже
async def show_lessons_menu(context, chat_id):
    buttons = []
    for key, lesson in LESSONS.items():
        if key.startswith("lesson_"):
            buttons.append([InlineKeyboardButton(lesson["title"], callback_data=f"menu_{key}")])

    await context.bot.send_message(chat_id=chat_id, text="📚 Выбери урок:", reply_markup=InlineKeyboardMarkup(buttons))
