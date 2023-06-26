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

import pandas as pd

driver = auth()
driver.get('https://www.linkedin.com/search/results/people/?keywords=data%20scientist&origin=CLUSTER_EXPANSION&sid=1gy')
time.sleep(20)
urls = pd.read_csv('profile_urls.csv')
print(urls)

for url in urls['profile_url']:
    driver.get(url)
    time.sleep(random.uniform(20, 30))

'''
from bs4 import BeautifulSoup
import time

def get_and_print_profile_info(driver, profile_url):
    driver.get(profile_url)

    src = driver.page_source

    soup = BeautifulSoup(src, 'lxml')

    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})

    name_loc = intro.find("h1")

    name = name_loc.get_text().strip()

    works_at_loc = intro.find("div", {'class': 'text-body-medium'})

    works_at = works_at_loc.get_text().strip()

    print("Name -->",  name,
          "\nWorks At -->", works_at)

    POSTS_URL_SUFFIX = 'recent-activity/all/'

    time.sleep(0.5)

    cur_profile_url = driver.current_url
    print(cur_profile_url)
'''