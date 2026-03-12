import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is Live"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is online and working!")

if __name__ == '__main__':
    t = Thread(target=run)
    t.start()
    
    token = os.environ.get('BOT_TOKEN')
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
