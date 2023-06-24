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
        time.sleep(6)
        driver.find_element(By.XPATH, '//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
        break
    except (Exception,) as e:
        if url_ret == 15:
            break
        url_ret += 1
# while True:
#     time.sleep(6)
#     driver.find_element(By.XPATH, '//a[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
#     break
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

#         total_row = len(response.xpath('//div[@class="widget-ArticleList-article referenced"]'))
#         for i in range(1,total_row+1):
#             try:
#                 sample_dic ={}
#                 sample_dic['Name']= response.xpath(f'(//div[@data-subwidget-id="0fd53e6f-c783-4aa7-84bc-877e37cf1f6d"])[{i}]/text()').get(default='').strip()
#                 sample_dic['Web_Code'] = response.xpath(f'(//span[contains(text(),"Web-Code:")]/following-sibling::span/text())[{i}]').get(default='').strip()
#                 try:
#                     sample_dic['Review'] = response.xpath(f'(//*[@class="ratings"])[{i}]/text()').get(default='').strip().split()[0]
#                 except:
#                     pass
#                 sample_data.append(sample_dic)
#             except:
#                 pass
#         print("data", sample_data)
#
#     except Exception as e:
#         print(e)
# df = pd.DataFrame(sample_data)
# print(df)
# df.to_dict()
# df.to_csv('Washing_data.csv', index = False, header=True)
# driver.close()
#
