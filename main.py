import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a TikTok link to get the video.")

async def get_tiktok_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        return

    api_url = f"https://tikwm.com/api/?url={url}"
    
    try:
        response = requests.get(api_url).json()
        video_url = response['data']['play']
        
        await update.message.reply_video(video=video_url, caption="Here is your video!")
    except Exception as e:
        await update.message.reply_text("Error: Could not retrieve the video.")

if __name__ == '__main__':
    t = Thread(target=run)
    t.start()
    
    token = os.environ.get('BOT_TOKEN')
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    
    application.run_polling()
