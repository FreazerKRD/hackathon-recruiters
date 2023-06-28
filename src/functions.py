from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

import time
import re
import pickle
import os
import random
import pandas as pd
import csv


def auth(driver, login, files_path):
      #Название файла cookies
      COOKIES_PATH = '\lincookies' + str(login.split('@')[0])
      #Проверка наличия папки для cookies
      if not os.path.exists(files_path):
            os.mkdir(files_path)

      #Авторизация по cookies
      if os.path.exists(files_path + COOKIES_PATH):
            driver.get('https://linkedin.com')
            #Загрузка куки
            for cookie in pickle.load(open(files_path + COOKIES_PATH, 'rb')):
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
            username.send_keys(login)
            pword = driver.find_element(By.ID, "password")
            pword.send_keys(str(input('Введите пароль: ')))
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(30) #время на ввод кода подтверждения если понадобится
            pickle.dump(driver.get_cookies(), open(files_path + COOKIES_PATH, 'wb'))

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

def get_and_save_users_posts(driver, url, posts_file_name):
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

            with open(posts_file_name, 'a', newline='', encoding='utf-8') as file:
                  writer_obj = writer(file)
                  writer_obj.writerow(post_source)

            time.sleep(random.uniform(2, 5))
    
      # Возврат на страницу профиля
      driver.execute_script("window.history.go(-1)")

def get_and_save_profile_info(driver, profile_url, info_file_name, posts_file_name):
      info_source = []
    
      # This will open the link
      driver.get(profile_url)
    
      # Random sleeping time to load all data
      time.sleep(random.uniform(5, 7))

      # Extracting data from page with BeautifulSoup
      src = driver.page_source

      # Now using beautiful soup    
      soup = BeautifulSoup(src, 'lxml')

      # Extracting the HTML of the complete introduction box
      # that contains the name, status, and the location
      intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
    
      # Extracting the Name
      # In case of an error, try changing the tags used here.
      name_loc = intro.find("h1")
      # strip() is used to remove any extra blank spaces
      name = name_loc.get_text().strip()
      info_source.append(name)

      # This gives us the HTML of the tag in which user status is present
      status_loc = intro.find("div", {'class': 'text-body-medium'})
      # Extracting user status
      status = status_loc.get_text().strip()
      info_source.append(status)
      
      try:
            # Extracting the Company name
            work_space = soup.find('ul', {'class': 'pv-text-details__right-panel'})
            # This gives us the HTML of the tag in which the Company Name is present
            works_at_loc = work_space.find('span', {'class': 'pv-text-details__right-panel-item-text'})
            # Extracting the Company Name
            works_at = works_at_loc.get_text().strip()
            info_source.append(works_at)
      except: 
            info_source.append('n/a')

      # Добавил случайный скроллинг страницы для имитации человека
      last_height = driver.execute_script("return document.body.scrollHeight")
      NUM_SCROLLS = random.randint(4, 10)

      for _ in range(NUM_SCROLLS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.5, 3))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                  break
            last_height = new_height

      time.sleep(random.uniform(2, 5))
    
      # Add user profile URL
      info_source.append(profile_url)
    
      # Сохранение в файл
      with open(info_file_name, 'a', newline='', encoding='utf-8') as file:
            writer_obj = csv.writer(file)
            writer_obj.writerow(info_source)
        
      # Собираем посты текущего пользователя, если они существуют
      by = By.CSS_SELECTOR
      path = 'li.profile-creator-shared-feed-update__mini-container'
      # Проверка существования элемента на странице
      def check_exists_element(by, path):
            try:
                  driver.find_element(by, path)
            except NoSuchElementException:
                  return False
            return True
      
      if check_exists_element(by, path):
            get_and_save_users_posts(driver, profile_url, posts_file_name)
        
      time.sleep(random.uniform(1, 3))
      
      # Возврат на страницу поиска
      driver.execute_script("window.history.go(-1)")

def search_pages(driver, num_pages, info_file_name, posts_file_name):
      for i in range(num_pages):
            # Задержка для полной загрузки страницы
            time.sleep(random.uniform(4, 7))

            last_height = driver.execute_script("return document.body.scrollHeight")
            NUM_SCROLLS = 20

            for _ in range(NUM_SCROLLS):
                  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                  time.sleep(random.uniform(1.5, 3))
                  new_height = driver.execute_script("return document.body.scrollHeight")
                  if new_height == last_height:
                        break
                  last_height = new_height

            search_result_links = driver.find_elements(By.CSS_SELECTOR, "span.entity-result__title-text a.app-aware-link")

            profile_urls = []
            
            for link in search_result_links:
                  href = link.get_attribute("href")
                  if 'linkedin.com/in' in href:
                        profile_urls.append(href)
                  
            profile_urls = pd.Series(profile_urls)
            profile_urls_cut = profile_urls.str.split('?', n=1).str[0]
            
            time.sleep(random.uniform(2, 5))
            
            # Парсинг информации о пользователях и их постах
            # Создаем файл для записи инфо о пользователях если он не существует
            if not os.path.exists(info_file_name):
                  header = ['name', 'status', 'company', 'profile_url']
                  with open(info_file_name, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                  
            #Создаем файл для записи постов если он не существует
            if not os.path.exists(posts_file_name):
                  header = ['url', 'text', 'likes_cnt', 'reposts_cnt', 'comments_cnt']
                  with open(posts_file_name, 'w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)

            # Получение информации из профилей пользователей
            for url in profile_urls_cut:
                  get_and_save_profile_info(driver, url, info_file_name, posts_file_name)
                  time.sleep(random.uniform(55, 75))

            print('Current search page completly parsed:')
            print(driver.current_url)
            print('- ' * 25)

            next_button = driver.find_element(By.CSS_SELECTOR, 'button.artdeco-pagination__button--next')
            next_button.click()