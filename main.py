import json
from time import sleep
import requests
from api_links import API_LINKS, COINS

bot_token = API_LINKS.get('bot_token')
crypto_api = API_LINKS.get('crypto_api')
btc = COINS.get('btc')
eth = COINS.get('eth')

dictionary = json.load(open('dictionary.json'))

def get_last_update(api_link):
    params = {'timeout': 100, 'offset': None}
    parsed_data = requests.get(api_link + 'getUpdates', data = params)
    response = parsed_data.json()
    return response['result'][-1]

def send_message(chat_id, message_text):
    body = {'chat_id': chat_id, 'text': message_text}
    response = requests.post(bot_token + 'sendMessage', data=body)
    return response

def get_coin_price(coin, link):
    parsed_data = requests.get(link + coin + '-usd/')
    response = parsed_data.json()
    return response['ticker']['price']

last_update = get_last_update(bot_token)
chat_id = last_update['message']['chat']['id']
first_name = last_update['message']['from']['first_name']
message_text = last_update['message']['text']
get_btc = get_coin_price(btc, crypto_api)
get_eth = get_coin_price(eth, crypto_api)

def main():
    update_id = last_update['update_id']
    while True:
        if update_id == last_update['update_id']:
            if message_text == '/start':
                send_message(chat_id, first_name + dictionary['start'])
            elif message_text == '/help':
                send_message(chat_id, dictionary['help'])
            elif message_text == '/btc':
                send_message(chat_id, dictionary['btc'] +str(get_btc))
            elif message_text == '/eth':
                send_message(chat_id, dictionary['eth'] +str(get_eth))
            else:
                send_message(chat_id, dictionary['error'])
            print('message: ' + message_text + ', user: ' + first_name)
            update_id += 1
        sleep(1)
if __name__ == '__main__':
    main()
