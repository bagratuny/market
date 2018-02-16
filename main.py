import json
from time import sleep
import requests
from api_links import API_LINKS, COINS

BOT_TOKEN = API_LINKS.get('bot_token')
COIN_API = API_LINKS.get('crypto_api')
BTC = COINS.get('btc')
ETH = COINS.get('eth')

dictionary = json.load(open('dictionary.json'))

def get_last_update(huy):
    params = {'timeout': 100, 'offset': huy}
    parsed_data = requests.get(BOT_TOKEN + 'getUpdates', data = params)
    response = parsed_data.json()
    return response['result']

def send_message(chat_id, message_text):
    body = {'chat_id': chat_id, 'text': message_text}
    response = requests.post(BOT_TOKEN + 'sendMessage', data=body)
    return response

def get_coin_price(coin):
    parsed_data = requests.get(COIN_API + coin + '-usd/')
    response = parsed_data.json()
    response2 = response['ticker']['price']
    return str(response2)

def main():
    offset = 0
    while True:
        len_updates = get_last_update(offset)
        if len(len_updates) > 0:
            for count in len_updates:
                message_text = count['message']['text']
                chat_id = count['message']['chat']['id']
                first_name = count['message']['from']['first_name']
                if message_text == '/start':
                    send_message(chat_id, first_name + dictionary['start'])
                elif message_text == '/help':
                    send_message(chat_id, dictionary['help'])
                elif message_text == '/btc':
                    send_message(chat_id, dictionary['btc'] +str(get_coin_price(BTC)))
                elif message_text == '/eth':
                    send_message(chat_id, dictionary['eth'] +str(get_coin_price(ETH)))
                else:
                    send_message(chat_id, dictionary['error'])
                print('message: ' + message_text + ', user: ' + first_name)
            offset = len_updates[-1]['update_id'] + 1
        sleep(5)
if __name__ == '__main__':
    main()
