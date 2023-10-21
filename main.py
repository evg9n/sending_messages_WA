from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pyperclip import copy
from logging import getLogger, config, DEBUG
from dotenv import load_dotenv

from os.path import abspath, join
from os import environ

load_dotenv(abspath(join('.env')))

LIST_NUMBERS = environ.get('list_number').split(', ')
PATH_WEBDRIVER = environ.get('path_webdriver')
XPATH_BUTTON = environ.get('xpath_button')
MESSAGE = environ.get('message')
XPATH_FIELD_INPUT_WIN = environ.get('xpath_field_input')
PATH_PROFILE_MY = 'profile'

FORMAT = "%(levelname)-8s [%(asctime)s] %(message)s"
datefmt = '%d.%m.%y %H:%M:%S'
log_config = {
    'version': 1,
    'formatters': {
        'for_file': {
            'format': FORMAT,
            'datefmt': datefmt
        }
    },
    'handlers': {
        'for_file': {
            'class': 'logging.FileHandler',
            'filename': 'sending_messages_wa.log',
            'encoding': 'utf-8',
            'formatter': 'for_file',
            'level': DEBUG
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': DEBUG,
            'formatter': 'for_file',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        '': {
            'handlers': ['for_file', 'console'],
            'level': DEBUG
        }
    }
}

config.dictConfig(log_config)
log = getLogger()


def sending_messages_wa(list_number: list, message: str, path_webdriver: str, path_profile: str,
                        xpath_field_input: str, xpath_button: str):
    """
    Функция предназначена для рассылки в WhatsApp WEB

    :param list_number: список с полными номерами, например +79874561230
    :type list_number:list
    :param message: текст рассылаемого сообщения
    :type message:str
    :param path_webdriver: путь к ChromeDriver
    :type path_webdriver:str
    :param path_profile: путь где будет храниться сессия
    :type path_profile:str
    :param xpath_field_input: xpath на поле ввода
    :type xpath_field_input:str
    :param xpath_button: xpath на кнопку "Отправить"
    :type xpath_button:str
    :return: None
    """

    options = webdriver.ChromeOptions()
    options.add_argument(fr'--user-data-dir={path_profile}')
    with webdriver.Chrome(executable_path=join('chromedriver-linux64', 'chromedriver'), options=options) as driver:
        driver.get(r"https://web.whatsapp.com")
        input('GO?(жми ENTER)')
        log.debug('GO')

        score = 0
        all_score = len(list_number)

        for number in list_number:
            score += 1

            log.info(f'поиск {number}')
            log.info(f'{score} / {all_score}')
            driver.get(f"https://web.whatsapp.com/send/?phone={number}")
            sleep(15)
            if 'Неверный номер телефона.' in driver.page_source:
                log.error(f'{number} Неверный номер телефона')
                continue

            attempts = 1
            while attempts < 4:
                try:
                    field = driver.find_element(By.XPATH, xpath_field_input)

                    actions = ActionChains(driver)
                    actions.move_to_element(field)

                    actions.click()

                    actions.perform()

                    copy(message)
                    actions.key_down(Keys.CONTROL).send_keys('v')
                    actions.perform()
                    actions.reset_actions()
                    button = driver.find_element(By.XPATH, xpath_button)

                    button.click()
                    log.debug(f'{number} готово')
                    sleep(5)
                    break

                except Exception as error:
                    attempts += 1
                    log.error(f'{error}')
                    driver.get(f"https://web.whatsapp.com/send/?phone={number}")
                    if attempts == 4:
                        log.error(f'Количество попыток превышено лимита в 3 раза\nномер {number} пропускается, переход'
                                  ' к следующему номеру')
                        break

                    log.info(f'Через 30 секунд будет попытка {attempts}/3 поиска номера {number}')
                    sleep(30)

        log.info('Конец рассылки')


if __name__ == '__main__':
    try:
        sending_messages_wa(list_number=LIST_NUMBERS, message=MESSAGE, path_webdriver=PATH_WEBDRIVER,
                            xpath_button=XPATH_BUTTON, xpath_field_input=XPATH_FIELD_INPUT_WIN,
                            path_profile=PATH_PROFILE_MY)
    except Exception as error_exit:
        input('ERROR')
        log.error(f'Программа принудительно остановилась \n {error_exit}')
