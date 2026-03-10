import os
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is running!")

if __name__ == '__main__':
    token = os.environ.get('BOT_TOKEN')
    if token:
        application = ApplicationBuilder().token(token).build()
        application.add_handler(CommandHandler('start', start))
        application.run_polling()
