from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "superbot")

flask_app = Flask(__name__)
telegram_app = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

telegram_app.add_handler(CommandHandler("start", start))

# Webhook
@flask_app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

@flask_app.route("/")
def index():
    return "Render бот запущен!"

if __name__ == "__main__":
    async def run():
        await telegram_app.initialize()
        flask_app.run(host="0.0.0.0", port=10000)
    asyncio.run(run())
