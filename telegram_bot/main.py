from telegram.ext import Updater, CommandHandler
import os
import requests
import json

from api_client import ApiClient

api = ApiClient()

chat_ids = []

def start(update, context):
    update.message.reply_text('Welcome to SatoshiBot! You were successfully subscribed to the Telegram messages.')
    chat_id = update.message.chat_id
    if str(chat_id) not in chat_ids:
        chat_ids.append(chat_id)
        response_telegram_api = api.post('telegram/chat', json={"chat_id": chat_id})
        if response_telegram_api.status_code // 100 == 2:
            print("Chat ID posted successfully:", chat_id)
        else:
            print("Failed to post chat ID. Status code:", response_telegram_api.status_code)

def fetchChatIds():
    response_algo_api = api.get('telegram/chats')
    if response_algo_api.status_code // 100 == 2:
        print("ChatIds retrieved successfully")
    else:
        print("Failed to retrieve chats from Algo API")

    chat_ids_api = None
    if(response_algo_api):
        chat_ids_api = json.loads(response_algo_api.text)

    if(chat_ids_api != None):
        for chat_id in chat_ids_api:
            chat_ids.append(chat_id)

def main():
    fetchChatIds()

    updater = Updater(os.environ.get('BOT_TOKEN'), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
