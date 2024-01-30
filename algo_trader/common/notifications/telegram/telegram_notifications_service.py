import requests
import os

def get_all_chat_ids(bot_token):
    base_url = 'https://api.telegram.org/bot{}'.format(bot_token)
    get_updates_url = '{}/getUpdates'.format(base_url)

    response = requests.get(get_updates_url)
    updates = response.json().get('result', [])

    chat_ids = set()

    for update in updates:
        chat_id = update.get('message', {}).get('chat', {}).get('id')
        if chat_id:
            chat_ids.add(chat_id)

    return list(chat_ids)

def notify_telegram_users(message):
    bot_token = os.environ.get('BOT_TOKEN')
    all_chat_ids = get_all_chat_ids(bot_token)

    for chat_id in all_chat_ids:
        send_telegram_message(bot_token, chat_id, message)

def send_telegram_message(bot_token, chat_id, message):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_token)
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    print(response.json())