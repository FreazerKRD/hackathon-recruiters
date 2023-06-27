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


def auth(driver):
      #if __name__ == '__main__':

      #Логин
      USER_LOGIN = 'aiyumrin@gmail.com'

      #Название файла cookies
      COOKIES_PATH = '\lincookies'

      #Папка для хранения cookies
      FILES_PATH = 'D:\Recruiters'

      #Проверка наличия папки для cookies
      if not os.path.exists(FILES_PATH):
            os.mkdir(FILES_PATH)

      #Авторизация по cookies
      if os.path.exists(FILES_PATH + COOKIES_PATH):
            driver.get('https://linkedin.com')
            #Загрузка куки
            for cookie in pickle.load(open(FILES_PATH + COOKIES_PATH, 'rb')):
                  driver.add_cookie(cookie)
            time.sleep(random.uniform(.5, 1))
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

def profile_urls(driver, search_url):
      #Загрузка страницы с результатами поиска
      driver.get(search_url)
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
            NUM_SCROLLS = 5

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
            while k == 1 or errors < 10:
                  
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

      urls = pd.DataFrame(profile_urls, columns=['profile_url'])
      urls['profile_url'] = urls['profile_url'].apply(lambda x: x.split('?')[0])
      print(urls)
      urls.to_csv('profile_urls.csv', index=False)

def get_and_print_users_posts(driver, url):
      from csv import writer
      driver.get(url + '/recent-activity/all/')
      time.sleep(random.uniform(.5, 1))
      SCROLL_PAUSE_TIME = random.uniform(1, 2)
      last_height = driver.execute_script("return document.body.scrollHeight")
      # We can adjust this number to get more posts
      NUM_SCROLLS = random.randint(5, 10)
      for i in range(NUM_SCROLLS):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(random.uniform(1, 2))

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                  break

            last_height = new_height

      src = driver.page_source
      #Установил lxml
      soup = BeautifulSoup(src, 'lxml')
      posts = soup.find_all('li', class_='profile-creator-shared-feed-update__container')
      

      print(f'Number of posts: {len(posts)}')
      for post_src in posts:
            post_source = []
            post_source.append(url)
            #Текст статьи репоста
            post_text_div = post_src.find('a', {'class': 'tap-target update-components-mini-update-v2__link-to-details-page text-body-medium ember-view'})
            if post_text_div is not None:
                  post_text = post_text_div.find('span', {'dir': 'ltr'})
            else:
                  post_text = None

            if post_text is not None:
                  post_text = post_text.get_text().strip()
                  print(f'Post text: {post_text}')
                 
            if post_text is None:
                  post_text_div = post_src.find('div', {'class': 'feed-shared-update-v2__description-wrapper mr2'})            
                  if post_text_div is not None:
                        post_text = post_text_div.find('span', {'dir': 'ltr'})
                  else:
                        post_text = None

                  # If post text is found
            
                  if post_text is not None:
                        post_text = post_text.get_text().strip()
                        print(f'Post text: {post_text}')
                  else:
                        post_text = 'No text'
        
            post_source.append(post_text)

            #Подсчет лайков
            likes_cnt = post_src.find('span', {'class': 'social-details-social-counts__reactions-count'})

            # If number of reactions is written as text
            # It has different class name
            if likes_cnt is None:
                  likes_cnt = post_src.find('span', {'class': 'social-details-social-counts__social-proof-text'})

          
            if likes_cnt is not None:
                  likes_cnt = likes_cnt.get_text().strip()
                  print(f'Likes: {likes_cnt}')

            if likes_cnt == None:
                  likes_cnt = 0
                  print(f'Likes: {likes_cnt}')

            post_source.append(likes_cnt)

            #Подсчет репостов
            reposts_cnt = post_src.find('li', {'class': 'social-details-social-counts__item social-details-social-counts__item--with-social-proof'})
            if reposts_cnt is not None:
                  reposts_cnt = reposts_cnt.find('span', {'aria-hidden': 'true'})
            if reposts_cnt is not None:
                  reposts_cnt = reposts_cnt.get_text().strip()
            else:
                 reposts_cnt = 0 
            print(f'Reposts: {reposts_cnt}')
            post_source.append(reposts_cnt)

            #Подсчет комментариев
            comment_cnt = post_src.find('li', {'class': 'social-details-social-counts__item social-details-social-counts__comments social-details-social-counts__item--with-social-proof'})
            if comment_cnt is not None:
                  comment_cnt = comment_cnt.find('span', {'aria-hidden': 'true'})
            if comment_cnt is not None:
                  comment_cnt = comment_cnt.get_text().strip()
            else:
                 comment_cnt = 0 
            print(f'Comments: {comment_cnt}')
            post_source.append(comment_cnt)          
            with open('posts.csv', 'a', newline='', encoding='utf-8') as file:
                  writer_obj = writer(file)
                  writer_obj.writerow(post_source)