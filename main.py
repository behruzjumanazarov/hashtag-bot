import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("InstaHashBot")
if not TOKEN:
    raise RuntimeError("8530043545:AAHCIU_SIYsI4-J748vjo3dWTeUHaipXF1E")

BANK = {
    "motivatsiya": ["motivatsiya", "maqsad", "intizom", "harakat", "mehnat", "muvaffaqiyat", "hayot", "ozbekvideo"],
    "kulgili": ["kulgili", "prikol", "hazil", "kulgu", "qiziq", "ozbekprikol", "ozbekvideo"],
    "diniy": ["islom", "quran", "duo", "ramazon", "taqvo", "iman", "ozbekdiniy", "ozbekvideo"],
    "sport": ["sport", "mashq", "trenirovka", "fitnes", "kuch", "soglomturmush", "ozbeksport", "ozbekvideo"],
    "biznes": ["biznes", "tadbirkorlik", "pul", "daromad", "sotuv", "marketing", "ozbekbiznes", "ozbekvideo"],
    "vlog": ["vlog", "kundalik", "hayot", "safar", "toshkent", "ozbekvlog", "ozbekvideo"],
    "sevgi": ["sevgi", "muhabbat", "soginch", "hislar", "yurak", "romantika", "ozbekvideo"],
}

PLATFORM_TAGS = {
    "ig": ["reels", "instagram", "ozbekreels"],
    "tt": ["tiktok", "ozbektiktok", "ozbekvideo"],
}

KEYWORDS = {
    "motivatsiya": ["motivatsiya", "ilhom", "maqsad", "intizom", "harakat", "muvaffaqiyat"],
    "kulgili": ["kulgili", "hazil", "prikol", "kulgu", "qiziq"],
    "diniy": ["islom", "quran", "duo", "ramazon", "namoz", "taqvo", "iman"],
    "sport": ["sport", "mashq", "fitnes", "trenirovka", "kuch", "soglom"],
    "biznes": ["biznes", "tadbirkor", "daromad", "pul", "sotuv", "marketing"],
    "vlog": ["vlog", "kundalik", "hayot", "safar", "sayohat", "toshkent"],
    "sevgi": ["sevgi", "muhabbat", "soginch", "his", "yurak", "romantika"],
}

def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9ʻʼ’\s#-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def pick_topics(text: str):
    t = normalize(text)
    topics = []
    for topic, kws in KEYWORDS.items():
        if any(kw in t for kw in kws):
            topics.append(topic)
    return topics[:2] if topics else ["vlog"]

def build_hashtags(text: str, platform: str) -> str:
    topics = pick_topics(text)
    tags = []

    for tp in topics:
        tags.extend(BANK.get(tp, []))

    tags.extend(PLATFORM_TAGS.get(platform, []))

    words = [w for w in normalize(text).split() if len(w) >= 5 and not w.startswith("#")]
    for w in words[:2]:
        tags.append(w)

    uniq, seen = [], set()
    for x in tags:
        x = x.replace(" ", "")
        if x and x not in seen:
            seen.add(x)
            uniq.append(x)

    uniq = uniq[:15]
    return " ".join(f"#{t}" for t in uniq)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[
        InlineKeyboardButton("Instagram", callback_data="plat:ig"),
        InlineKeyboardButton("TikTok", callback_data="plat:tt")
    ]]
    context.user_data["platform"] = "ig"
    await update.message.reply_text(
        "Platformani tanla (default: Instagram). So‘ng video haqida 1-2 gap yoz.",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def on_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    platform = q.data.split(":")[1]
    context.user_data["platform"] = platform
    await q.edit_message_text(
        f"Tanlandi: {'Instagram' if platform=='ig' else 'TikTok'} ✅\nEndi video haqida yoz."
    )

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "")[:500]
    platform = context.user_data.get("platform", "ig")
    hashtags = build_hashtags(text, platform)
    await update.message.reply_text(hashtags)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_platform, pattern=r"^plat:(ig|tt)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling()

if __name__ == "__main__":
    main()
