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
    
    # Using a different API structure that handles short links better
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Get the actual video URL from the service
            api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
            response = await client.get(api_url, timeout=20.0)
            data = response.json()
            
            if data.get("status") == "success":
                video_url = data['video']['noWatermark']
                author = data['author']['name']
                subs = data['author']['stats']['followerCount']
                
                await update.message.reply_video(video=video_url, caption=f"Author: {author}\nFollowers: {subs}")
            else:
                await update.message.reply_text("Failed to download. Please try another link.")
            
            await msg.delete()
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
        await msg.delete()

if __name__ == '__main__':
    Thread(target=run_web).start()
    application = ApplicationBuilder().token(TOKEN).build()
    application.bot.delete_webhook(drop_pending_updates=True)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    application.run_polling(drop_pending_updates=True)
