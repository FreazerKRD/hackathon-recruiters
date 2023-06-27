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
#Ссылка на поиск
SEARCH_URL = 'https://www.linkedin.com/search/results/people/?keywords=data%20scientist&origin=CLUSTER_EXPANSION&sid=1gy'

#Вызов функции авторизации
auth(driver)
time.sleep(random.uniform(.5, 1))
#Вызов функции сбора url
#profile_urls(driver, SEARCH_URL)
time.sleep(random.uniform(.5, 1))

urls = pd.read_csv('profile_urls.csv')['profile_url']

#Создаем файл для записи постов
header = ['url', 'text', 'likes_cnt', 'reposts_cnt', 'comments_cnt']
with open('posts.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)

for url in urls:
    get_and_print_users_posts(driver, url)

driver.quit()