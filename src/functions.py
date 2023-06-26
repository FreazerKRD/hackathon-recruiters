def auth():
      import os
      from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
      from selenium import webdriver
      import pickle
      import time
      import random
      from selenium.webdriver.common.by import By


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
      return driver