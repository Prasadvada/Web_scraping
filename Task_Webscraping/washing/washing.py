import time
import undetected_chromedriver as uc
import pandas as pd
from scrapy.http import HtmlResponse
from DataExtraction import DataExtractor
from selenium.webdriver.common.by import By
driver = uc.Chrome()
driver.get('https://www.expert.de/shop/unsere-produkte/haushalt-kuche/waschen-trocknen-bugeln-nahen/waschmaschinen')
time.sleep(20)
url_ret =1
while True:
    try:
        time.sleep(5)
        driver.find_element(By.XPATH, '//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
        break
    except (Exception,) as e:
        if url_ret == 15:
            break
        url_ret += 1
time.sleep(2)
driver.refresh()
time.sleep(10)
pages = driver.find_element(By.XPATH,'//span[@class="widget-ArticleList-pageCount"]').text
print(pages)
sample_data = []
url_retry = 1
for j in range(1,int(pages)+1):
    try:
        print("page",j)
        if j>1:
            while True:
                try:
                    time.sleep(5)
                    driver.get(f'https://www.expert.de/shop/unsere-produkte/haushalt-kuche/waschen-trocknen-bugeln-nahen/waschmaschinen?page={j}')
                    break
                except (Exception,) as e:
                    if url_retry == 5:
                        break
                    url_retry += 1
        time.sleep(4)
        driver.refresh()
        time.sleep(3)
        while True:
            response = HtmlResponse(url='https://www.example.com', body=driver.page_source.encode('utf-8'))
            time.sleep(2)
            break
        DataExtractor(response)
    except:
        pass