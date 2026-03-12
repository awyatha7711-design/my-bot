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
    await update.message.reply_text("Hello! Please send me any TikTok video link.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Processing your link, please wait...")
    
    # Use the API with the 'hd' parameter to ensure better success
    api_url = "https://tikwm.com/api/"
    
    async with httpx.AsyncClient() as client:
        try:
            # We must pass the url in a way that handles short links
            response = await client.post(api_url, data={"url": url, "hd": 1}, timeout=20.0)
            data = response.json()
            
            if data.get("code") == 0:
                video_url = data['data']['play']
                author_name = data['data']['author']['nickname']
                subscribers = data['data']['author']['follower_count']
                
                caption = f"Author: {author_name}\nFollowers: {subscribers}"
                await update.message.reply_video(video=video_url, caption=caption)
            else:
                await update.message.reply_text("Could not fetch the video. Please try another link.")
                
            await msg.delete()
        except Exception as e:
            await update.message.reply_text("Error occurred. Please try again later.")
            await msg.delete()

if __name__ == '__main__':
    Thread(target=run_web).start()
    application = ApplicationBuilder().token(TOKEN).build()
    application.bot.delete_webhook(drop_pending_updates=True)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    application.run_polling(drop_pending_updates=True)
