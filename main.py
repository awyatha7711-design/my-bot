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

# Your specific token
TOKEN = '8571756435:AAF-0RLqh2dNgQOgILdNwvpj5zo3SoimyUU'

async def start(update, context):
    await update.message.reply_text("Hello! Send me a TikTok video link and I will download it for you.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Downloading... please wait.")
    api_url = f"https://tikwm.com/api/?url={url}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, timeout=15.0)
            data = response.json()
            
            video_url = data['data']['play']
            subscribers = data['data']['author']['follower_count']
            author_name = data['data']['author']['nickname']
            
            caption = f"Author: {author_name}\nFollowers: {subscribers}"
            
            await update.message.reply_video(video=video_url, caption=caption)
            await msg.delete()
        except Exception:
            await update.message.reply_text("Failed to download the video. Please try another link.")
            await msg.delete()

if __name__ == '__main__':
    # Start the web server for Render
    Thread(target=run_web).start()
    
    # Initialize the bot application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Critical: Remove webhook to solve Conflict Error
    application.bot.delete_webhook(drop_pending_updates=True)
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    
    # Start polling
    application.run_polling(drop_pending_updates=True)
