import requests
import os
import json
from datetime import datetime

from api_client import ApiClient

api = ApiClient()

def get_all_chat_ids():
    chat_ids = []
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
    
    return chat_ids

def post_telegram_chat(chat_id):
    response_telegram_api = api.post('telegram/chat', json={"chat_id": chat_id})
    if response_telegram_api.status_code // 100 == 2:
        print("Chat ID posted successfully:", chat_id)
    else:
        print("Failed to post chat ID. Status code:", response_telegram_api.status_code)

def build_message(data):
    if data['buy']['price'] <= data['sell']['price']:
        trade_result = "👍 Positive"
    else: 
        trade_result = "👎 Negative"

    trade_details_message = (
    "Trade Details:\n"
    "Pair: {}\n"
    "Amount: {}\n"
    "Buy Order:\n"
    "  Price: {}\n"
    "  Timestamp: {}\n"
    "Sell Order:\n"
    "  Price: {}\n"
    "  Timestamp: {}\n"
    "Trade Result: {}"
    ).format(
        data['pair'],
        data['amount'],
        data['buy']['price'],
        datetime.fromtimestamp(data['buy']['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
        data['sell']['price'],
        datetime.fromtimestamp(data['sell']['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
        trade_result
    )

    return trade_details_message

def notify_telegram_users(data):

    message = build_message(data)

    bot_token = os.environ.get('BOT_TOKEN')
    all_chat_ids = get_all_chat_ids()

    for chat_id in all_chat_ids:
        send_telegram_message(bot_token, chat_id, message)

def send_telegram_message(bot_token, chat_id, message):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_token)
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    print(response.json())