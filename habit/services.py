from config.settings import TG_BOT_TOKEN
import requests


def send_tg_message(chat_id, text):
    params = {
        'text': text,
        'chat_id': chat_id
    }
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print(f"Message sent successfully to chat_id {chat_id}: {text}")


def is_today(now, start, period):
    delta = (now - start).days

    match period:
        case 'day':
            return True
        case '2 days':
            return delta % 2 == 0
        case '3 days':
            return delta % 3 == 0
        case 'week':
            return delta % 7 == 0
    return False
