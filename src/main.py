from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random
import functions

#Ссылка на поиск
SEARCH_URL = 'https://www.linkedin.com/search/results/people/?currentCompany=%5B%2210718%22%2C%22579461%22%2C%22970369%22%2C%2219201%22%2C%22868912%22%2C%226132%22%2C%2218326534%22%2C%228979%22%2C%2212611%22%2C%222831%22%2C%2210876016%22%2C%2212650056%22%2C%22134818%22%2C%2219031362%22%2C%2232642%22%2C%223735315%22%2C%2266724050%22%2C%2279365269%22%2C%22918215%22%5D&geoUrn=%5B%22106686604%22%5D&industry=%5B%221594%22%2C%226%22%2C%2296%22%2C%224%22%5D&keywords=senior&origin=GLOBAL_SEARCH_HEADER&sid=~o7'
#Логин для входа на linkedin
USER_LOGIN = 'fedorfedukov79@gmail.com'
#Папка для хранения файлов
FILES_PATH = 'D:\Recruiters'
# Количество страниц результатов поиска для парсинга
NUM_PAGES_TO_PARSE = int(input('Введите количество страниц для парсинга: '))
# Путь к файлу с постами
POSTS_FILE_NAME = FILES_PATH + r"\posts.csv"
# Путь к файлу с инфо пользователей
INFO_FILE_NAME = FILES_PATH + r"\user-info.csv"
# Путь к файлу с постами
POSTS_FILE_NAME = FILES_PATH + r"\posts.csv"

if __name__ == '__main__':
    #Инициализируем веб-драйвер
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'eager'
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    # Установлен широкоформатный размер экрана, чтобы нужные элементы помещались на экране
    driver.set_window_size(1920, 1080)

    #Вызов функции авторизации
    functions.auth(driver, USER_LOGIN, FILES_PATH)
    time.sleep(10)

    # Парсинг страниц поисковой выдачи
    # Переход на стартовую страницу поиска
    driver.get(SEARCH_URL)

    # Вызов функции для парсинга
    functions.search_pages(driver, 100, INFO_FILE_NAME, POSTS_FILE_NAME)

    # Пауза
    time.sleep(random.uniform(5, 12))

    # Выключаем драйвер скрэппинга
    driver.quit()