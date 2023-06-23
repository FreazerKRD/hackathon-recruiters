from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import re
import pickle
import os

#Логин
USER_LOGIN = 'aiyumrin@gmail.com'
#файл с паролем
with open('C:\doc.txt') as f:
    USER_PASSWORD = f.readline()
COOKIES_PATH = 'lincookies'

if __name__ == '__main__':
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'eager'
    driver = webdriver.Chrome()

    if os.path.exists(COOKIES_PATH):
        driver.get('https://linkedin.com')
        #Загрузка куки
        for cookie in pickle.load(open('D:\lincookies', 'rb')):
            driver.add_cookie(cookie)
        time.sleep(5)
        driver.refresh()
        time.sleep(10)
    else:
        driver.get('https://linkedin.com/uas/login')
        #Авторизация
        time.sleep(3.5)
        username = driver.find_element(By.ID, "username")
        username.send_keys(USER_LOGIN)
        pword = driver.find_element(By.ID, "password")
        pword.send_keys(USER_PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(30) #время на ввод кода подтверждения
        #Сохранение куки
        pickle.dump(driver.get_cookies(), open('D:\lincookies', 'wb'))

    driver.get('https://www.linkedin.com/search/results/people/?keywords=data%20scientist&origin=CLUSTER_EXPANSION&sid=1gy')

    time.sleep(10)
""""
    profile_urls = []

    NUM_PAGES_TO_PARSE = 12

    for i in range(NUM_PAGES_TO_PARSE):
        search_result_links = driver.find_elements(By.CSS_SELECTOR, "div.entity-result__item a.app-aware-link")

        for link in search_result_links:
            href = link.get_attribute("href")
            if 'linkedin.com/in' in href:
                profile_urls.append(href)

        next_button = driver.find_element(By.CLASS_NAME,'artdeco-pagination__button--next')
        next_button.click()
        time.sleep(2)


    profile_urls = list(set(profile_urls))

    print(profile_urls)

    for profile_url in profile_urls:
        get_and_print_profile_info(driver, profile_url)
        time.sleep(2)

    driver.quit()
"""