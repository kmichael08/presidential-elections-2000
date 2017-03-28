from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from collections import deque
from selenium.common.exceptions import WebDriverException

display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Firefox(executable_path='/home/michal/geckodriver/geckodriver')

init_page = 'file:///home/michal/PycharmProjects/wybory_prezydenckie/pages/kraj/Polska.html'

pages = deque([init_page])

def bfs():
    while len(pages) != 0:
        url = pages.popleft()
        try:
            driver.get(url)
            home_page = driver.find_element_by_tag_name('a')
            present_unit = driver.find_element_by_xpath("//ul[@class='topnav']/li[last()]/a")
            print(present_unit.text + ': ')
            if home_page.get_attribute('href') == init_page:
                print('     ma poprawny link do strony głównej')
            else:
                print('     brak linku do strony głównej!!!')
            if driver.find_elements_by_class_name('votes') == []:
                print('     brak wyników głosowania!!!')
            else:
                print('     poprawne wyniki głosowania')
            sub_pages = driver.find_elements_by_xpath("//div[@class='subunits']/ul/li/a")
            for sub_page in sub_pages:
                pages.append(sub_page.get_attribute('href'))
        except WebDriverException:
            print('We have a broken link!!!')

"""
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME,'subunits'))
    )
    print(url)
    sub_pages = driver.find_elements_by_xpath("//div[@class='subunits']/ul/li/a")
    for sub_page in sub_pages:
        print(sub_page.text)
        sub_page.click()
        dfs(driver.current_url)
    driver.back()
"""
bfs()

driver.quit()
display.stop()