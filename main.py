import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("8530043545:AAHCIU_SIYsI4-J748vjo3dWTeUHaipXF1E")

def make_hashtags(text: str, limit: int = 20) -> str:
    # faqat so'zlarni ajratib olamiz
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    words = text.split()

    tags, seen = [], set()
    for w in words:
        w = w.strip()
        if len(w) < 2 or len(w) > 30:
            continue
        key = w.lower()
        if key in seen:
            continue
        seen.add(key)
        w2 = re.sub(r"[^\w]", "", w, flags=re.UNICODE)
        if not w2:
            continue
        tags.append("#" + w2)
        if len(tags) >= limit:
            break

    # har doim 3 ta umumiy o'zbek tag qo'shamiz
    base = ["#ozbekvideo", "#reels", "#uzbek"]
    out = base + tags
    # uniq
    uniq = []
    s = set()
    for t in out:
        if t not in s:
            s.add(t)
            uniq.append(t)
    return " ".join(uniq[:25])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Matn yubor — men hashtag qilib beraman.\n"
        "Misol: Motivatsion video, hayot, intizom"
    )

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        return
    await update.message.reply_text(make_hashtags(text) or "Hashtag chiqmadi.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
