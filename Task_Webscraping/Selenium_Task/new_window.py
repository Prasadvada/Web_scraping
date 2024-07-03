import math
import re
import time
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-images")

service = Service(executable_path='C:\\Users\\laksh\\OneDrive\\Desktop\\Selenium_Task\\chromedriver.exe')
driver = webdriver.Chrome(service=service,options=chrome_options)
# driver = webdriver.Chrome()
url = 'https://www.rottentomatoes.com'
input_list = ["Lucy in the sky#movie", "Lucifer#series"]
y= [re.match(r'([^#]+)',g).group(1) for g in input_list if re.match(r'([^#]+)',g)]
a=y[0].strip()
b=y[1]

def Data():
    while True:
        try:
            driver.get(url)
            driver.maximize_window()
            driver.find_element(By.XPATH,'//input[@class="search-text"]').send_keys('Lucy in the sky')
            driver.find_element(By.XPATH,'//input[@class="search-text"]').click()
            driver.find_element(By.XPATH,'//input[@class="search-text"]').send_keys(Keys.ENTER)
            break
        except:
            pass
    while True:
        try:
            time.sleep(2)
            driver.find_element(By.XPATH,'//li[@data-filter="movie"]//span[@data-qa="search-filter-text"]').click()
            break
        except:
            pass
    time.sleep(2)
    total =driver.find_element(By.XPATH,'//li[@data-filter="movie"]//span[@data-qa="search-filter-text"]').text
    pages = int(re.findall(r'([\d]+)',total)[0])
    page = int(math.ceil(pages/10))
    all_data = []
    for i in range(1,page+1):
        total_rows =driver.find_elements(By.XPATH,'//*[@id="search-results"]/search-page-result[2]/ul/search-page-media-row')
        total_rows = len(total_rows)
        for j in range(1,int(total_rows)+1):
            print("row:",j)
            try:
                href = driver.find_element(By.XPATH,f'//*[@id="search-results"]/search-page-result[2]/ul/search-page-media-row[{j}]//a[2]').get_attribute('href')
                print(href)
                try:
                    driver.execute_script(f"window.open('{href}', '_blank');")
                    time.sleep(4)
                except:
                    pass
                driver.switch_to.window(driver.window_handles[-1])
            except Exception as e:
                print(e)
                pass
            response = HtmlResponse(url='https://www.example.com', body=driver.page_source.encode('utf-8'))
            try:
                cast_crew = '|'.join([i.strip() for i in response.xpath('//*[@id="cast-and-crew"]/div/div[1]/div/div/a/p/text()').getall() if i.strip() != ""]).replace('\n', '')
                print('cast',cast_crew)
            except:
                cast_crew =''
                pass
            all_data.append({'cast_crew':cast_crew})
            driver.close()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(4)

    print(all_data)

def Data_extractor():
    pass

if __name__ ==  '__main__':
    if a=='Lucy in the sky':
        Data()
    elif b=='Lucifer':
        Data_extractor()
