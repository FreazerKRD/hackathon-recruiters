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

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'
driver = webdriver.Chrome()
SEARCH_URL = 'https://www.linkedin.com/search/results/people/?keywords=data%20scientist&origin=CLUSTER_EXPANSION&sid=1gy'

auth(driver)
profile_urls(driver, SEARCH_URL)











driver.get()
time.sleep(20)
urls = pd.read_csv('profile_urls.csv')
print(urls)

for url in urls['profile_url']:
    driver.get(url)
    time.sleep(random.uniform(20, 30))



    # for profile_url in profile_urls:
    #     #get_and_print_profile_info(driver, profile_url)
    #     time.sleep(2)

    # driver.quit()