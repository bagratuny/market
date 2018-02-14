import json
from time import sleep
import requests
from api_links import url, crypto_api

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
    response = requests.post(url + 'sendMessage', data=body)
    return response

def get_chat_first_name(chat_id):
    response = chat_id['message']['from']['first_name']
    return response

def get_message_text(text):
    response = text['message']['text']
    return response

def get_btc_price(btc):
    parsed_data = requests.get(btc + 'btc-usd/')
    response = parsed_data.json()
    return response['ticker']['price']

def get_eth_price(eth):
    parsed_data = requests.get(eth + 'eth-usd/')
    response = parsed_data.json()
    return response['ticker']['price']

def main():
    update_id = get_last_update(url)['update_id']
    while True:
        if update_id == get_last_update(url)['update_id']:
            message_text = get_message_text(get_last_update(url))
            if message_text == '/btc':
                send_message(get_chat_id(get_last_update(url)), dictionary['btc'] +str(get_btc_price(crypto_api)))
            elif message_text == '/eth':
                send_message(get_chat_id(get_last_update(url)), dictionary['eth'] +str(get_eth_price(crypto_api)))
            elif message_text == '/start':
                send_message(get_chat_id(get_last_update(url)), get_chat_first_name(get_last_update(url)) + dictionary['start'])
            elif message_text == '/help':
                send_message(get_chat_id(get_last_update(url)), dictionary['help'])
            else:
                send_message(get_chat_id(get_last_update(url)), dictionary['error'])
            print('message: ' + message_text + ', user: ' + get_chat_first_name(get_last_update(url)))
            update_id += 1
        sleep(1)
if __name__ == '__main__':
    main()
