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

# Your Token
TOKEN = '8571756435:AAF-0RLqh2dNgQOgILdNwvpj5zo3SoimyUU'

async def start(update, context):
    await update.message.reply_text("I'm ready to help! Please paste the TikTok video link you'd like to download.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Downloading your video, please wait a few seconds.")
    
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Expand the short link first
            resp = await client.get(url)
            final_url = str(resp.url)
            
            # API request
            api_url = "https://tikwm.com/api/"
            response = await client.post(api_url, data={"url": final_url, "hd": 1}, timeout=20.0)
            data = response.json()
            
            if data.get("code") == 0:
                video_url = data['data']['play']
                author = data['data']['author']['nickname']
                subs = data['data']['author']['follower_count']
                
                await update.message.reply_video(video=video_url, caption=f"Author: {author}\nFollowers: {subs}")
            else:
                await update.message.reply_text("Failed to download the video. Please try another link.")
            
            await msg.delete()
    except Exception:
        await update.message.reply_text("An error occurred. Please try again.")
        await msg.delete()

if __name__ == '__main__':
    # Start web server
    Thread(target=run_web).start()
    
    # Initialize bot
    application = ApplicationBuilder().token(TOKEN).build()
    application.bot.delete_webhook(drop_pending_updates=True)
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    
    # Start polling
    application.run_polling(drop_pending_updates=True)
