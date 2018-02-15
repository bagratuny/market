import json
from time import sleep
import requests
from api_links import API_LINKS, COINS

bot_token = API_LINKS.get('bot_token')
crypto_api = API_LINKS.get('crypto_api')
eth = COINS.get('eth')
btc = COINS.get('btc')

dictionary = json.load(open('dictionary.json'))

def get_last_update(api_link):
    params = {'timeout': 100, 'offset': None}
    parsed_data = requests.get(api_link + 'getUpdates', data = params)
    response = parsed_data.json()
    return response['result'][-1]

def get_chat_id(chat_id):
    response = chat_id['message']['chat']['id']
    return response

def send_message(chat_id, message_text):
    body = {'chat_id': chat_id, 'text': message_text}
    response = requests.post(bot_token + 'sendMessage', data=body)
    return response

def get_chat_first_name(chat_id):
    response = chat_id['message']['from']['first_name']
    return response

def get_message_text(text):
    response = text['message']['text']
    return response

def get_coin_price(coin, link):
    parsed_data = requests.get(link + coin + '-usd/')
    response = parsed_data.json()
    return response['ticker']['price']

get_chat_id = get_chat_id(get_last_update(bot_token))
get_chat_first_name = get_chat_first_name(get_last_update(bot_token))

def main():
    update_id = get_last_update(bot_token)['update_id']
    while True:
        if update_id == get_last_update(bot_token)['update_id']:
            message_text = get_message_text(get_last_update(bot_token))
            if message_text == '/btc':
                send_message(get_chat_id, dictionary['btc'] +str(get_coin_price(btc, crypto_api)))
            elif message_text == '/eth':
                send_message(get_chat_id, dictionary['eth'] +str(get_coin_price(eth, crypto_api)))
            elif message_text == '/start':
                send_message(get_chat_id, get_chat_first_name + dictionary['start'])
            elif message_text == '/help':
                send_message(get_chat_id, dictionary['help'])
            else:
                send_message(get_chat_id, dictionary['error'])
            print('message: ' + message_text + ', user: ' + get_chat_first_name)
            update_id += 1
        sleep(1)
if __name__ == '__main__':
    main()
