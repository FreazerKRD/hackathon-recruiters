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