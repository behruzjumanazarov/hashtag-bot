import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# TOKEN ENV dan olinadi
TOKEN = os.getenv("8530043545:AAHCIU_SIYsI4-J748vjo3dWTeUHaipXF1E")

if not TOKEN:
    raise RuntimeError("8530043545:AAHCIU_SIYsI4-J748vjo3dWTeUHaipXF1E")

def make_hashtags(text):
    words = re.findall(r"\w+", text.lower())
    tags = ["#" + w for w in words[:15]]
    base = ["#ozbekvideo", "#reels", "#uzbek"]
    return " ".join(base + tags)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Matn yubor, men hashtag qilib beraman")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(make_hashtags(update.message.text))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
