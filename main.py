from time import sleep
import requests
from api_links import API_LINKS
from dictionary import DICT

BOT_TOKEN = API_LINKS.get('bot_token')
CRYPTONATOR_API = API_LINKS.get('cryptonator_api')

def get_last_update(offset):
    params = {'allowed_updates': {'message': 'text'}, 'timeout': 100, 'offset': offset}
    response = requests.get(BOT_TOKEN + 'getUpdates', data=params)
    return response.json()['result']

def send_message(chat_id, message_text):
    body = {'chat_id': chat_id, 'text': message_text}
    requests.post(BOT_TOKEN + 'sendMessage', data=body)

def get_coin_rate(coin):
    rate = requests.get(CRYPTONATOR_API + coin + '-usd/')
    try:
        return rate.json()
    except:
        return {'success': False}

def handle_message(message_text, chat_id, first_name):
    print('message: ' + message_text + ', user: ' + first_name)
    if message_text == '/start':
        send_message(chat_id, first_name + DICT.get('start'))
    elif message_text == '/help':
        send_message(chat_id, DICT.get('help'))
    else:
        success = get_coin_rate(message_text)['success']
        if success:
            print(message_text)
            coin_base = get_coin_rate(message_text)['ticker']['base']
            coin_price = get_coin_rate(message_text)['ticker']['price']
            send_message(chat_id, '{} rate is: ${}'.format(coin_base, coin_price))
        else:
            send_message(chat_id, DICT.get('error'))

def main():
    offset = 0
    while True:
        updates = get_last_update(offset)
        for update in updates:
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                first_name = update['message']['from']['first_name']
                message_text = update['message']['text']
                handle_message(message_text, chat_id, first_name)
            else:
                send_message(chat_id, DICT.get('error'))
            offset = updates[-1]['update_id'] + 1
        sleep(1)

if __name__ == '__main__':
    main()
