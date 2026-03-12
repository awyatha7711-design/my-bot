import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a TikTok link to download.")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        return

    msg = await update.message.reply_text("Downloading... please wait.")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        await msg.delete()
        os.remove('video.mp4')
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    t = Thread(target=run)
    t.start()
    
    token = os.environ.get('BOT_TOKEN')
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_tiktok))
    
    application.run_polling()
