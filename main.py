from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

TOKEN = '8644018753:AAGN99AOn0zkHd9dFo8OsirwOMpmR4SkDqY'

async def start(update, context):
    await update.message.reply_text("I am ready! Please paste the TikTok link.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Downloading...")
    api_url = f"https://tikwm.com/api/?url={url}"
    
    try:
        response = requests.get(api_url).json()
        video_url = response['data']['play']
        await update.message.reply_video(video=video_url)
        await msg.delete()
    except Exception as e:
        await update.message.reply_text("Failed to download.")
        await msg.delete()

if __name__ == '__main__':
    Thread(target=run_web).start()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    
    application.run_polling(drop_pending_updates=True)
