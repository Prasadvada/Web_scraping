import math
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys
import pandas as pd
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("incognito")
driver = webdriver.Chrome(options=options)
input_list = ["Lucy in the sky#movie", "Lucifer#series"]
y=[re.match(r'([^#]+)',i).group(1) for i in input_list if re.match(r'([^#]+)',i)]
z=y[1]

def data_extraction(z):
    url = 'https://www.rottentomatoes.com'
    while True:
        try:
            driver.get(url)
            driver.find_element(By.XPATH, '//input[@data-qa="search-input"]').send_keys(z)
            driver.find_element(By.XPATH, '//input[@data-qa="search-input"]').click()
            driver.find_element(By.XPATH, '//input[@data-qa="search-input"]').send_keys(Keys.ENTER)
            break
        except:
            pass
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, '//li[@data-filter="movie"]//span').click()
    except:
        pass
    total_records = driver.find_element(By.XPATH, '//li[@data-filter="movie"]//span').text
    total = int(re.findall('([\d]+)',total_records)[0])
    pages = math.ceil(total // 10)
    print(pages)
    l = []
    for i in range(1, pages+1):
        print('page:', i)
        total_rows = driver.find_elements(By.XPATH,'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row')
        r = len(total_rows)
        for j in range(1, int(r)+ 1):
            try:
                movie_title = driver.find_element(By.XPATH, f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{j}]/a[2]').text
                cast = driver.find_element(By.XPATH, f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{j}]').get_attribute('cast')
                year = driver.find_element(By.XPATH, f'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[{j}]').get_attribute('releaseyear')
                l.append({"movie": movie_title,'cast':cast,'year':year})
            except Exception as e:
                print(f"An error occurred while processing movie data: {str(e)}")
        print(l)
        try:
            next_button = driver.find_element(By.XPATH, '(//*[@data-qa="paging-btn-next"])[1]')
            next_button.click()
            print('Clicked Next Button')
        except:
            pass
    df =pd.DataFrame(l)
    df.to_csv('prasad.csv',index=False, encoding='utf-8')
if __name__ == '__main__':
    data_extraction(z)
    driver.quit()
