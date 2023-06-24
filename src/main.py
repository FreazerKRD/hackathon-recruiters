from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import re
import pickle
import os
import random

#Логин
USER_LOGIN = 'aiyumrin@gmail.com'

#Название файла cookies
COOKIES_PATH = '\lincookies'

#Папка для хранения cookies
FILES_PATH = 'D:\Recruiters'

#Проверка наличия папки для cookies
if not os.path.exists(FILES_PATH):
    os.mkdir(FILES_PATH)



if __name__ == '__main__':
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'eager'
    driver = webdriver.Chrome()


    #Авторизация по cookies
    if os.path.exists(FILES_PATH + COOKIES_PATH):
        driver.get('https://linkedin.com')
        #Загрузка куки
        for cookie in pickle.load(open(FILES_PATH + COOKIES_PATH, 'rb')):
            driver.add_cookie(cookie)
        time.sleep(random.uniform(.5, 2))
        driver.refresh()
        time.sleep(random.uniform(.5, 2))

    #Вход по паролю и сохранение cookies
    else:
        driver.get('https://linkedin.com/uas/login')
        #Авторизация
        time.sleep(random.uniform(2, 4))
        username = driver.find_element(By.ID, "username")
        username.send_keys(USER_LOGIN)
        pword = driver.find_element(By.ID, "password")
        pword.send_keys(str(input('Введите пароль: ')))
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10) #время на ввод кода подтверждения если понадобится
        pickle.dump(driver.get_cookies(), open(FILES_PATH + COOKIES_PATH, 'wb'))

    #Загрузка страницы с результатами поиска
    driver.get('https://www.linkedin.com/search/results/people/?keywords=data%20scientist&origin=CLUSTER_EXPANSION&sid=1gy')
    time.sleep(random.uniform(.5, 3))

    profile_urls = []
    NUM_PAGES_TO_PARSE = 100

    for i in range(NUM_PAGES_TO_PARSE):

        print('Page', i+1)

        search_result_links = driver.find_elements(By.CSS_SELECTOR, "span.entity-result__title-text a.app-aware-link")

        for link in search_result_links:
            href = link.get_attribute("href")
            if 'linkedin.com/in' in href:
                profile_urls.append(href)

        last_height = driver.execute_script("return document.body.scrollHeight")
        NUM_SCROLLS = 10

        for j in range(NUM_SCROLLS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.5, 3))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(random.uniform(1, 2))
                
        print('Sucsess!')
        print('-' * 50)

        k = 1
        errors = 0
        while k == 1 and errors < 10:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'button.artdeco-pagination__button--next')
                next_button.click()
                k = 2
            except: 
                print(f'ERROR on page {i+1}! {errors}')
                errors += 1

        time.sleep(random.uniform(.5, 1))


    profile_urls = list(set(profile_urls))
    print('Done!')

    print(profile_urls)

    # for profile_url in profile_urls:
    #     #get_and_print_profile_info(driver, profile_url)
    #     time.sleep(2)

    # driver.quit()