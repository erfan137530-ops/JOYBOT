from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# لینک کانال‌های تبلیغاتی رو اینجا بذار
CHANNELS = [
    "@channel1",
    "@channel2",
    "@channel3"
]

# لینک فیلم‌ها رو اینجا بذار
MOVIES = {
    "فیلم ۱": "https://example.com/film1.mp4",
    "فیلم ۲": "https://example.com/film2.mp4",
    "فیلم ۳": "https://example.com/film3.mp4",
}

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    not_joined = []
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_joined.append(channel)
        except:
            not_joined.append(channel)
    
    if not_joined:
        keyboard = []
        for channel in not_joined:
            keyboard.append([InlineKeyboardButton(f"عضویت در {channel}", url=f"https://t.me/{channel.replace('@', '')}")])
        keyboard.append([InlineKeyboardButton("بررسی مجدد ✅", callback_data="check_join")])
        
        await update.message.reply_text(
            "برای دیدن فیلم‌ها باید در کانال‌های تبلیغاتی عضو شوید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await show_movies(update, context)

async def show_movies(update: Update, context: CallbackContext):
    keyboard = []
    for name, link in MOVIES.items():
        keyboard.append([InlineKeyboardButton(name, url=link)])
    
    await update.message.reply_text(
        "فیلم‌های موجود:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def check_join_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await start(update, context)

def main():
    app = Application.builder().token("TOKEN_ETUN").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join_callback))
    
    app.run_polling()

if __name__ == "__main__":
    main()
