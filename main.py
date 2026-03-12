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
    await update.message.reply_text("I'm ready to help! Please paste the TikTok video link you'd like to download.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Downloading your video, please wait a few seconds.")
    
    # Use a custom header to look like a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
            # Using a public, more stable API endpoint
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = await client.get(api_url, timeout=20.0)
            
            # Print response for debugging in your Render Logs
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text[:200]}")
            
            data = response.json()
            
            if data.get("code") == 0:
                video_url = data['data']['play']
                author = data['data']['author']['nickname']
                subs = data['data']['author']['follower_count']
                await update.message.reply_video(video=video_url, caption=f"Author: {author}\nFollowers: {subs}")
            else:
                await update.message.reply_text("Failed to process the link. The API returned an error.")
            
            await msg.delete()
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
        await msg.delete()

if __name__ == '__main__':
    Thread(target=run_web).start()
    application = ApplicationBuilder().token(TOKEN).build()
    application.bot.delete_webhook(drop_pending_updates=True)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    application.run_polling(drop_pending_updates=True)
