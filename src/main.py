from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import re
import pickle
import os
import random
import pandas as pd

from functions import auth
from functions import profile_urls
from functions import get_and_print_users_posts
import csv

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'
driver = webdriver.Chrome()
driver.implicitly_wait(30)
#Ссылка на поиск
SEARCH_URL = 'https://www.linkedin.com/search/results/people/?currentCompany=%5B%2210718%22%2C%2277009034%22%2C%22579461%22%2C%22868912%22%2C%22970369%22%5D&geoUrn=%5B%22106686604%22%5D&industry=%5B%221594%22%2C%226%22%2C%221810%22%2C%2296%22%2C%224%22%5D&origin=FACETED_SEARCH&page=3&sid=)q%3B'

#Вызов функции авторизации
auth(driver)
time.sleep(random.uniform(.5, 1))




# #Вызов функции сбора url
# profile_urls(driver, SEARCH_URL)
# time.sleep(random.uniform(.5, 1))

# urls = pd.read_csv('profile_urls.csv')['profile_url']

# #Создаем файл для записи постов
# header = ['url', 'text', 'likes_cnt', 'reposts_cnt', 'comments_cnt']
# with open('posts.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(header)

# for url in urls:
#     get_and_print_users_posts(driver, url)

# driver.quit()