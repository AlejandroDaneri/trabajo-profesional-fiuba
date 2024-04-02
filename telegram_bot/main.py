from telegram.ext import Updater, CommandHandler
import os

def error_handler(update, context):
    print("Two or more instances of the telegram-bot are running. This may result in delays in the updates.")

def start(update, context):
    update.message.reply_text('Welcome to SatoshiBot! You were successfully subscribed to the Telegram messages.')

def main():
    updater = Updater(os.environ.get('BOT_TOKEN'), use_context=True)
    updater.dispatcher.add_error_handler(error_handler)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
