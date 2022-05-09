import os
from textwrap import dedent
from time import sleep

import requests
import telegram
from dotenv import load_dotenv


def devman_long_polling(devman_token, timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {devman_token}'}
    payload = {}
    if timestamp:
        payload = {'timestamp': timestamp}
    response = requests.get(url, headers=headers, params=payload, timeout=150)
    response.raise_for_status()
    return response.json()


def form_message(lesson_review):
    review_successful = not lesson_review['is_negative']
    lesson_title = lesson_review['lesson_title']
    lesson_url = lesson_review['lesson_url']
    if review_successful:
        message = f"""
        Ваша работа "{lesson_title}" вернулась с проверки.
        
        Преподавателю все понравилось, можно приступать к следующему уроку!
        {lesson_url}
        """
    else:
        message = f"""
        Ваша работа "{lesson_title}" вернулась с проверки.
        
        К сожалению, к работе возникли замечания. 
        Перейдите по ссылке, чтобы узнать детали:
        {lesson_url}
        """
    return dedent(message)


def main():
    load_dotenv()
    devman_token = os.environ.get('DEVMAN_TOKEN')
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    bot = telegram.Bot(token=tg_bot_token)
    timestamp = 0
    while True:
        try:
            response = devman_long_polling(devman_token, timestamp)
        except requests.HTTPError:
            sleep(10)
            continue
        except requests.ReadTimeout:
            continue
        except requests.ConnectionError:
            sleep(60)
            continue
        if response['status'] == 'found':
            lesson_review = response['new_attempts'][0]
            message = form_message(lesson_review)
            bot.send_message(text=message, chat_id=chat_id)
            timestamp = response['last_attempt_timestamp']
        elif response['status'] == 'timeout':
            timestamp = response['timestamp_to_request']


if __name__ == '__main__':
    main()
