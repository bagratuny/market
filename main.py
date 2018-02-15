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
    params = {'timeout': 100, 'offset': [-1]}
    parsed_data = requests.get(api_link + 'getUpdates', data = params)
    response = parsed_data.json()
    return response['result'][-1]

def send_message(chat_id, message_text):
    body = {'chat_id': chat_id, 'text': message_text}
    response = requests.post(bot_token + 'sendMessage', data=body)
    return response

def get_coin_price(coin):
    parsed_data = requests.get(crypto_api + coin + '-usd/')
    response = parsed_data.json()
    return response['ticker']['price']

def main():
    last_update = get_last_update(bot_token)
    update_id = last_update['update_id']
    while True:
        last_update = get_last_update(bot_token)
        message_text = last_update['message']['text']
        chat_id = last_update['message']['chat']['id']
        first_name = last_update['message']['from']['first_name']
        if update_id == last_update['update_id']:
            if message_text == '/start':
                send_message(chat_id, first_name + dictionary['start'])
            elif message_text == '/help':
                send_message(chat_id, dictionary['help'])
            elif message_text == '/btc':
                send_message(chat_id, dictionary['btc'] +str(get_coin_price(btc)))
            elif message_text == '/eth':
                send_message(chat_id, dictionary['eth'] +str(get_coin_price(eth)))
            else:
                send_message(chat_id, dictionary['error'])
            print('message: ' + message_text + ', user: ' + first_name)
            update_id += 1
            print(update_id)
        sleep(1)
if __name__ == '__main__':
    main()
