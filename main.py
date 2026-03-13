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

# Your New Token
TOKEN = '8682175031:AAGPk7UK8S7U1XQu3a_6EvPHI365udNSNCM'

async def start(update, context):
    await update.message.reply_text("I'm ready to help! Please paste the TikTok video link you'd like to download.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Downloading your video, please wait a few seconds.")
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            # Using tikwm API
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = await client.get(api_url)
            data = response.json()
            
            if data and data.get("code") == 0:
                video_url = data['data']['play']
                author = data['data']['author'].get('nickname', 'User')
                await update.message.reply_video(video=video_url, caption=f"Author: {author}")
            else:
                await update.message.reply_text("Failed to download. Please try another link.")
            
            await msg.delete()
    except Exception:
        await update.message.reply_text("An error occurred. Please try again.")
        try:
            await msg.delete()
        except:
            pass

if __name__ == '__main__':
    Thread(target=run_web).start()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Critical settings to prevent Conflict Errors
    application.bot.delete_webhook(drop_pending_updates=True)
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    
    application.run_polling(drop_pending_updates=True)
