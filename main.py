from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os
from aiohttp import web

# === Переменные окружения ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID_ENV = os.getenv("OWNER_ID")
RAILWAY_STATIC_URL = os.getenv("RAILWAY_STATIC_URL")
PORT = int(os.getenv("PORT", 8080))

# === Проверка и логирование переменных ===
print("✅ ENV BOT_TOKEN:", BOT_TOKEN[:10] + "..." if BOT_TOKEN else "❌ НЕ УСТАНОВЛЕН")
print("✅ ENV OWNER_ID:", OWNER_ID_ENV or "❌ НЕ УСТАНОВЛЕН")
print("✅ ENV RAILWAY_STATIC_URL:", RAILWAY_STATIC_URL or "❌ НЕ УСТАНОВЛЕН")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN переменная окружения не установлена")

if not OWNER_ID_ENV:
    print("⚠️ OWNER_ID не установлен — бот не сможет отправлять уведомления админу")
    OWNER_ID = 0
else:
    OWNER_ID = int(OWNER_ID_ENV)

PAID_USERS = set()


# Все уроки
LESSONS = {"lesson_0": {"title": "Введение в курс Нейросети без паники: простой старт с ChatGPT", "file_id": "BAACAgQAAxkBAAMDaEhKiH81kqU7n6gwyZrPvfHUxxkAAm4YAAIbBkFSitZ_6O09L_82BA"}, "lesson_1": {"title": "Урок 1: Знакомство с ChatGPT", "file_id": "BAACAgQAAxkBAAMFaEhLK6c1vLL79Q5g_mvoFAABWJAhAAJwGAACGwZBUioldIP1mCYkNgQ"}, "lesson_2": {"title": "Урок 2: Первый запуск и настройка", "file_id": "BAACAgQAAxkBAAMHaEhMcN2U21N1G4YapPigdwa3bo0AAnMYAAIbBkFSSue7-aHqqaU2BA"}, "lesson_3": {"title": "Урок 3: Повседневное использование ChatGPT", "file_id": "BAACAgQAAxkBAAMPaEhQ744iIguAsHpdWxgBfxSyazcAAncYAAIbBkFSnLB9razsga82BA"}, "lesson_4": {"title": "Урок 4: Программирование и наставничество", "file_id": "BAACAgQAAxkBAAMRaEhRm8VMDLUZNpFMrdT4mq_kLtsAAngYAAIbBkFSR9leUkrI6A02BA"}, "lesson_5": {"title": "Урок 5: Как правильно задавать запросы", "file_id": "BAACAgQAAxkBAAMTaEhSDiQPbKQGs_yrJHwwms0BwK8AAnkYAAIbBkFScwGvzfAicJw2BA"}, "lesson_6": {"title": "Урок 6: Работа с данными", "file_id": "BAACAgQAAxkBAAMVaEhUXy7zNyxd86eMLXgjhygot6QAAnwYAAIbBkFSMQWn8c-tXZk2BA"}, "lesson_7": {"title": "Урок 7: Ограничение и безопасность", "file_id": "BAACAgQAAxkBAAMXaEhUqD-bmcNx8EpG29hWYth3OKAAAn0YAAIbBkFS5SweQtSDfYQ2BA"}, "lesson_8": {"title": "Урок 8: Обратная связь", "file_id": "BAACAgQAAxkBAAIBIWhJTFeHwFR1TnuUYDdLrrk-chDkAAIWGQACGwZJUhFc-hqK-hf8NgQ"}}


# === START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем параметр запуска
    args = context.args
    source = args[0] if args else "direct"
    user_id = update.message.from_user.id

    # Отслеживаем источники переходов (можно логировать или сохранять в БД)
    if source == "landing":
        print(f"👤 Пользователь {user_id} пришел с лендинга")
        welcome_text = "👋 Добро пожаловать с нашего сайта в мини-курс «Нейросети без паники»!\n\n"
    elif source == "program":
        print(f"👤 Пользователь {user_id} пришел из программы курса")
        welcome_text = "👋 Отлично! Вы изучили программу и готовы начать мини-курс «Нейросети без паники»!\n\n"
    elif source == "webapp":
        print(f"👤 Пользователь {user_id} пришел из WebApp")
        welcome_text = "👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"
    else:
        print(f"👤 Пользователь {user_id} запустил бота напрямую")
        welcome_text = "👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"

    context.user_data["step"] = 0
    context.user_data["source"] = source  # Сохраняем источник для аналитики

    await update.message.reply_text(
        welcome_text + "Ты можешь сразу начать бесплатно или купить полный доступ ко всем урокам.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")]]))

# === КНОПКИ ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # === Урок 0 ===
    if query.data == "step_0":
        context.user_data["step"] = 1
        lesson = LESSONS["lesson_0"]
        await context.bot.send_video(chat_id=query.message.chat.id, video=lesson["file_id"], caption=lesson['title'])
        await context.bot.send_message(chat_id=query.message.chat.id, text="Понравилось? Круто! Держите Урок 1.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Дальше", callback_data="step_1")]]))

    # === Урок 1 ===
    elif query.data == "step_1":
        context.user_data["step"] = 2
        lesson = LESSONS["lesson_1"]
        await context.bot.send_video(chat_id=query.message.chat.id, video=lesson["file_id"], caption=lesson['title'])
        await context.bot.send_message(chat_id=query.message.chat.id, text="Посмотрели 1 Урок? Продолжаем.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Продолжить", callback_data="step_2")]]))

    # === Предложение купить курс ===
    elif query.data == "step_2":
        context.user_data["step"] = 3
        await context.bot.send_message(chat_id=query.message.chat.id,
            text="Вижу вам понравилось. Первые два видео были бесплатными, чтобы вы могли прочувствовать ценность моего мини-курса. Приобретайте его полностью по кнопке ниже.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Купить мини курс", callback_data="buy")],
                [InlineKeyboardButton("❌ Не хочу покупать", callback_data="not_ready")]]))

    # === Если не готов покупать ===
    elif query.data == "not_ready":
        await context.bot.send_message(chat_id=query.message.chat.id,
            text="Понимаю! Когда будешь готов, просто напиши /start и пройди к предложению о покупке.\n\nСпасибо за внимание к курсу! 😊")

    elif query.data == "buy":
        await context.bot.send_message(chat_id=query.message.chat.id,
            text="💳 Выберите удобный способ оплаты мини-курса (500₽):", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Revolut", url="https://revolut.me/r/hJG50OBCC4")],
                    [InlineKeyboardButton("🔁 Я оплатил — проверить доступ", callback_data="paid")]]))

    elif query.data == "paid":
        if user_id in PAID_USERS:
            await context.bot.send_message(chat_id=query.message.chat.id,
                text="✅ У тебя уже есть доступ ко всем урокам.")
            # Показываем меню для пользователя с доступом
            await show_lessons_menu(context, query.message.chat.id)
        else:
            await context.bot.send_message(chat_id=query.message.chat.id,
                text="🕐 Заявка на доступ отправлена. Проверка оплаты может занять до 10 минут.\n\n"
                     "Если ты уже оплатил, напиши свой ник или ID в личку: @dekavetel")
            # Уведомление владельцу
            username = query.from_user.username or "не указан"
            await context.bot.send_message(chat_id=OWNER_ID,
                text=f"🔔 Новый запрос на доступ от пользователя @{username} (ID: {user_id})")


# === Функция для показа меню уроков ===
async def show_lessons_menu(context, chat_id):
    buttons = []
    for key, lesson in LESSONS.items():
        if key.startswith("lesson_"):
            buttons.append([InlineKeyboardButton(lesson["title"], callback_data=f"menu_{key}")])

    await context.bot.send_message(chat_id=chat_id, text="📚 Выбери урок:", reply_markup=InlineKeyboardMarkup(buttons))


# === /menu для платных пользователей ===
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in PAID_USERS:
        await update.message.reply_text("🔒 Доступно только после оплаты. Напиши /start, чтобы пройти бесплатные уроки.")
        return

    await show_lessons_menu(context, update.message.chat.id)


# === Открытие любого платного урока ===
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

        # Сохраняем текущий урок в user_data
        context.user_data["current_lesson"] = key

        # Показываем кнопки
        await show_next_lesson_options(context, query.message.chat.id, key)


# === Функция для показа опций после урока ===
async def show_next_lesson_options(context, chat_id, current_lesson_key):
    current_num = int(current_lesson_key.split('_')[1])
    next_num = current_num + 1
    next_lesson_key = f"lesson_{next_num}"

    buttons = []

    if next_lesson_key in LESSONS:
        next_title = LESSONS[next_lesson_key]["title"]
        buttons.append([InlineKeyboardButton(f"▶️ {next_title}", callback_data=f"menu_{next_lesson_key}")])

    buttons.append([InlineKeyboardButton("📚 Все уроки", callback_data="back_to_menu"),
        InlineKeyboardButton("🏠 В начало", callback_data="go_home")])

    await context.bot.send_message(chat_id=chat_id, text="Перейти к следующему?",
        reply_markup=InlineKeyboardMarkup(buttons))


# === Обработчик для кнопки "Все уроки" ===
async def back_to_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in PAID_USERS:
        await query.edit_message_text("🔒 Доступно только после оплаты.")
        return

    buttons = []
    for key, lesson in LESSONS.items():
        if key.startswith("lesson_"):
            buttons.append([InlineKeyboardButton(lesson["title"], callback_data=f"menu_{key}")])

    await query.edit_message_text("📚 Выбери урок:", reply_markup=InlineKeyboardMarkup(buttons))


# === Получение file_id (только для админа) ===
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("⛔️ Только администратор может загружать видео.")
        return
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"`{file_id}`", parse_mode='Markdown')


# === Обработчик для кнопки "В начало" ===
async def go_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Создаем новое сообщение вместо попытки подмены update
    await context.bot.send_message(chat_id=query.message.chat.id,
        text="👋 Добро пожаловать в мини-курс «Нейросети без паники»!\n\n"
             "Ты можешь сразу начать бесплатно или купить полный доступ ко всем урокам.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👉 Начать бесплатно", callback_data="step_0")],
            [InlineKeyboardButton("💳 Сразу оплатить", callback_data="buy")]]))


# === Узнать свой user_id ===
async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👤 Твой user_id: {update.message.from_user.id}")


# === Выдача доступа (только для админа) ===
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ Укажите ID пользователя: /grant 12345678")
        return

    try:
        target_id = int(context.args[0])
        PAID_USERS.add(target_id)

        # Логируем выдачу доступа
        print(f"💰 Админ выдал доступ пользователю {target_id}")

        await update.message.reply_text(f"✅ Доступ выдан пользователю {target_id}")
        await context.bot.send_message(chat_id=target_id,
            text="✅ Спасибо! Доступ к полному курсу открыт. Напиши /menu чтобы продолжить.")
    except (ValueError, IndexError):
        await update.message.reply_text("⚠️ Неверный ID или ошибка.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при отправке уведомления пользователю: {e}")
        

# === ЗАПУСК ===
PORT = int(os.getenv("PORT", 8080))
BASE_URL = os.getenv("RAILWAY_STATIC_URL")

async def handle_webhook(request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return web.Response(text="OK")

async def on_startup(app):
    await application.initialize()
    await application.start()
    webhook_url = f"https://{BASE_URL}/{BOT_TOKEN}"
    await application.bot.set_webhook(webhook_url)

async def root(request):
    return web.Response(text="🤖 Бот работает")

# Telegram bot
application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

# Обработчики (как раньше)
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("menu", menu))
application.add_handler(CommandHandler("myid", my_id))
application.add_handler(CommandHandler("grant", grant))
application.add_handler(MessageHandler(filters.VIDEO, get_file_id))
application.add_handler(CallbackQueryHandler(button_handler, pattern="^(step_.*|buy|paid|not_ready)$"))
application.add_handler(CallbackQueryHandler(go_home, pattern="^go_home$"))
application.add_handler(CallbackQueryHandler(open_lesson, pattern="^menu_lesson_.*"))
application.add_handler(CallbackQueryHandler(back_to_menu_handler, pattern="^back_to_menu$"))

# aiohttp app
web_app = web.Application()
web_app.router.add_post(f"/{os.getenv('BOT_TOKEN')}", handle_webhook)
web_app.router.add_get("/", root)
web_app.on_startup.append(on_startup)

if __name__ == "__main__":
    print("🚀 Бот запускается на Railway...")
    web.run_app(web_app, port=PORT)
