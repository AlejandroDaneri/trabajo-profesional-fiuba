from telegram.ext import Updater, CommandHandler
import os

def start(update, context):
    update.message.reply_text('Welcome to SatoshiBot! You were successfully subscribed to the Telegram messages.')

def main():
    updater = Updater(os.environ.get('BOT_TOKEN'), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
