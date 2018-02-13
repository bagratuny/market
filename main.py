import requests
from settings import url

def getLastUpdate(apiLink):
    parsedData = requests.get(apiLink + 'getUpdates')
    response = parsedData.json()
    return response['result'][-1]

def getChatID(chatID):
    response = chatID['message']['chat']['id']
    return response

def sendMessage(chatID, messageText):
    body = {'chat_id': chatID, 'text': messageText}
    response = requests.post(url + 'sendMessage', data=body)
    return response

chatID = getChatID(getLastUpdate(url))
sendMessage(chatID, 'Hi there!')

#test