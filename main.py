import os
import httpx
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

TOKEN = '8571756435:AAF-0RLqh2dNgQOgILdNwvpj5zo3SoimyUU'

async def start(update, context):
    await update.message.reply_text("Hello! Send me a TikTok video link and I will download it for you.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Downloading...")
    api_url = f"https://tikwm.com/api/?url={url}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, timeout=10.0)
            data = response.json()
            
            video_url = data['data']['play']
            subscribers = data['data']['author']['follower_count']
            author_name = data['data']['author']['nickname']
            
            caption = f"Author: {author_name}\nFollowers: {subscribers}"
            
            await update.message.reply_video(video=video_url, caption=caption)
            await msg.delete()
        except Exception:
            await update.message.reply_text("Error: Could not download the video.")
            await msg.delete()

if __name__ == '__main__':
    Thread(target=run_web).start()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    
    application.run_polling(drop_pending_updates=True)
