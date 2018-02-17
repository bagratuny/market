import json
from time import sleep
import requests
from api_links import API_LINKS

BOT_TOKEN = API_LINKS.get('bot_token')
CRYPTONATOR_API = API_LINKS.get('cryptonator_api')
DICT = json.load(open('dictionary.json'))

def get_last_update(offset):
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(BOT_TOKEN + 'getUpdates', data=params)
    return response.json()['result']

def send_message(chat_id, message_text):
    body = {'chat_id': chat_id, 'text': message_text}
    requests.post(BOT_TOKEN + 'sendMessage', data=body)

def get_coin_rate(coin):
    response = requests.get(CRYPTONATOR_API + coin + '-usd/')
    return response.json()

def main():
    offset = 0
    while True:
        len_updates = get_last_update(offset)
        if len(len_updates) > 0:
            for update in len_updates:
                message_text = update['message']['text']
                chat_id = update['message']['chat']['id']
                first_name = update['message']['from']['first_name']
                if not get_coin_rate(message_text)['success']:
                    coit_rate = 'False'
                else:
                    coin_rate = get_coin_rate(message_text)['ticker']['price']
                    coin_name = get_coin_rate(message_text)['ticker']['base']
                if message_text == '/start':
                    send_message(chat_id, first_name + DICT['start'])
                elif message_text == '/help':
                    send_message(chat_id, DICT['help'])
                elif get_coin_rate(message_text) == None:
                    send_message(chat_id, DICT['error'])
                else:
                    send_message(chat_id, coin_name + ' rate is: $' + coin_rate)
                print('message: ' + message_text + ', user: ' + first_name)
            offset = len_updates[-1]['update_id'] + 1
        sleep(1)

if __name__ == '__main__':
    main()
