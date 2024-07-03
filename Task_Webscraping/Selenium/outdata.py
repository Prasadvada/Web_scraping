import math
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
import pandas as pd
def function():
    driver.get('https://www.python.org')
    time.sleep(3)
function()
driver.find_element_by_xpath('//*[@id="page"]/div[3]/ul/li[2]/div/a').click()
time.sleep(2)
driver.maximize_window()
date2=driver.find_element_by_xpath('//*[@id="recordedDateRange"]')
date2.send_keys(Keys.CONTROL + "a")
date2.send_keys(Keys.DELETE)
date2=driver.find_element_by_xpath('//*[@id="recordedDateRange"]')
date2.send_keys("11/01/2021")
date2=driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/div[5]/div[3]/div[2]/form/div[5]/div/div[2]/div[3]/div[1]/div/input')
date2.send_keys(Keys.CONTROL + "a")
date2.send_keys(Keys.DELETE)
date2=driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/div[5]/div[3]/div[2]/form/div[5]/div/div[2]/div[3]/div[1]/div/input')
date2.send_keys("11/01/2021")
driver.find_element_by_xpath('//button[@aria-disabled="false"]').click()
time.sleep(2)
records=driver.find_element_by_xpath('//*[@id="page"]/div[3]/header/section[1]/div/p/span[1]').text
print('records',records)
m=records.split()[2]
print(m)
no_pages=math.ceil(int(m)//50)+1
print(int(no_pages))
sample_data=[]
for i in range(1, no_pages+1):
    print("PAGE No.",i)
    total_rows = driver.find_elements_by_xpath('//*[@id="page"]/div[3]/div/div[2]/div[1]/table/tbody/tr')
    print(total_rows)
    for r in range(1, int(len(total_rows))):
        sample_dic = {}
        print("row no.: ",r)
        time.sleep(3)
        sample_dic["data"] = driver.find_element_by_xpath(f'//th[contains(text(),"Recorded Date")]/../../following-sibling::tbody/tr[{r}]/td[7]/span').text
        # time.sleep(3)
        # driver.find_element_by_xpath('//*[@id="content"]/main/div[2]/div[1]/div/div/div/header/div/ul/li[2]/button').click()
        time.sleep(2)
        sample_dic["date"] = driver.find_element_by_xpath(f'//th[contains(text(),"Doc Number")]/../../following-sibling::tbody/tr[{r}]/td[8]/span').text
        # print(doc/_no)
        sample_dic["grantor"] = driver.find_element_by_xpath(f'//th[contains(text(),"Grantor")]/../../following-sibling::tbody/tr[{r}]/td[4]/span').text
        # print(rec_date)
        sample_dic["grantee"] = driver.find_element_by_xpath(f'//th[contains(text(),"Grantee")]/../../following-sibling::tbody/tr[{r}]/td[5]/span').text
        # print(book_page)
        sample_data.append(sample_dic)
    print("data", sample_data)
    #driver.find_element_by_xpath('//*[@id="page"]/div[3]/div/div[2]/div[2]/nav/div/button[6]').click()
    #time.sleep(2)
df = pd.DataFrame(sample_data)
print(df)
df.to_dict()
df.to_csv('data.csv', index = False, header=True)

driver.close()
