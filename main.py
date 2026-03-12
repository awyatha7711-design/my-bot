from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# Bot Token
TOKEN = '8644018753:AAE_IH51-l0WjG99Bj357j-uo-tRrS7j8nA'

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I'm ready to help! Please paste the TikTok video link you'd like to download."
    )

# TikTok Link handler
async def get_tiktok_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        return

    # Processing message
    msg = await update.message.reply_text("Downloading your video, please wait a few seconds.")

    api_url = f"https://tikwm.com/api/?url={url}"
    
    try:
        response = requests.get(api_url).json()
        video_url = response['data']['play']
        
        # Send video
        await update.message.reply_video(video=video_url, caption="Here is your video!")
        await msg.delete() # Delete processing message
        
    except Exception as e:
        await update.message.reply_text("Sorry, could not download the video.")
        await msg.delete()

if __name__ == '__main__':
    # Initialize application
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    
    # Run polling
    application.run_polling(drop_pending_updates=True)
