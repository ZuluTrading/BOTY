import os
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

DEADLINE = datetime(2025, 1, 8, 23, 59)

RULES_TEXT = (
    "🎄 Конкурс «Новогодний медведь»\n\n"
    "Что нужно сделать:\n"
    "1) Раскрасить медведя\n"
    "2) Дать ему имя и титул\n"
    "3) Отправить фото и описание сюда\n\n"
    "Работа будет опубликована анонимно.\n"
    "Дедлайн: до 8 января включительно."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RULES_TEXT)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    if now > DEADLINE:
        await update.message.reply_text("❌ Приём работ завершён.")
        return

    # Пересылаем сообщение админу
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    await update.message.reply_text("✅ Медведь принят. Спасибо 🐻")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Bot started...")
    app.run_polling()

if name == "main":
    main()
