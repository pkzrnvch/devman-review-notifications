import os
import logging
from textwrap import dedent
from time import sleep

import requests
import telegram
from dotenv import load_dotenv


logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


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
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('Бот запущен!')
    timestamp = None
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {devman_token}'}
    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(
                url,
                headers=headers,
                params=payload,
                timeout=150
            )
            response.raise_for_status()
            review = response.json()
        except requests.HTTPError:
            logger.error('Ошибка HTTP, попытка переподключения через 5 минут')
            sleep(300)
            continue
        except requests.ReadTimeout:
            logger.warning('Нет ответа от сервера, попытка переподключения...')
            continue
        except requests.ConnectionError:
            logger.warning('Потеря связи, попытка переподключения...')
            sleep(60)
            continue
        except Exception:
            logger.exception('Бот cтолкнулся с непредвиденной ошибкой:')
            continue
        if review['status'] == 'found':
            review_details = review['new_attempts'][0]
            message = form_message(review_details)
            bot.send_message(text=message, chat_id=chat_id)
            timestamp = review['last_attempt_timestamp']
        elif review['status'] == 'timeout':
            timestamp = review['timestamp_to_request']


if __name__ == '__main__':
    main()
