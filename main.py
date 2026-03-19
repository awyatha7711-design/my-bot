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
TOKEN = '8682175031:AAGPk7UK8S7U1XQu3a_6EvPHI365udNSNCM'

async def start(update, context):
    await update.message.reply_text("I'm ready to help! Please paste the TikTok video link you'd like to download.")

async def get_tiktok_video(update, context):
    url = update.message.text
    if "tiktok.com" not in url:
        return
    
    msg = await update.message.reply_text("Downloading your video, please wait a few seconds.")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient(follow_redirects=True, headers=headers, timeout=30.0) as client:
        # --- API 1: TikWM ---
        try:
            resp = await client.get(f"https://www.tikwm.com/api/?url={url}")
            data = resp.json()
            if data and data.get("code") == 0:
                video_url = data['data']['play']
                author = data['data']['author'].get('nickname', 'User')
                await update.message.reply_video(video=video_url, caption=f"Author: {author}")
                await msg.delete()
                return
        except:
            pass # API 1 မရရင် API 2 ကို ဆက်သွားမယ်

        # --- API 2: TiklyDown (Backup) ---
        try:
            resp = await client.get(f"https://api.tiklydown.eu.org/api/download?url={url}")
            data = resp.json()
            if data.get("status") == "success" or data.get("code") == 0:
                video_url = data['video']['noWatermark']
                author = data['author']['name']
                await update.message.reply_video(video=video_url, caption=f"Author: {author}")
                await msg.delete()
                return
        except:
            pass

    # နှစ်ခုလုံး မရမှသာ error ပြမယ်
    await update.message.reply_text("Failed to download. The link might be broken or restricted.")
    await msg.delete()

if __name__ == '__main__':
    Thread(target=run_web).start()
    application = ApplicationBuilder().token(TOKEN).build()
    application.bot.delete_webhook(drop_pending_updates=True)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), get_tiktok_video))
    application.run_polling(drop_pending_updates=True)
