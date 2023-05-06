import requests
import time

token: str = '5603742042:AAGd0_sftQliPysSOxFrA-_bPFwy0vR65nc'
api_url: str = 'https://api.telegram.org/bot'
max_counter: int = 100
answer_url: str = 'https://api.thecatapi.com/v1/images/search'

offset: int = -2
counter: int = 0
chat_id: int

while counter < max_counter:
    print('attemp =', counter)

    updates = requests.get(
        f'{api_url}{token}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            mycat = requests.get(answer_url).json()[0]['url']
            requests.get(
                f'{api_url}{token}/sendPhoto?chat_id={chat_id}&photo={mycat}')
    time.sleep(1)
    counter += 1
