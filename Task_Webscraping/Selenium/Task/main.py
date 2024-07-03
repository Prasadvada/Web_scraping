from translate import Translator
import math
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
# def nextpage(next):
#     driver = webdriver.Firefox()
#     time.sleep(5)
#     # url =next
#     url ='https://www.dtvp.de/Center/secured/company/welcome.do'
#     driver.get(url)
#     time.sleep(2)
#     accept = driver.find_element(By.XPATH,
#                                  '(//*[contains(text(),"Alles akzeptieren")])[2]')  # Replace with the actual link text
#     accept.click()
#     time.sleep(5)
#     email = driver.find_element(By.XPATH, '//input[@id="login"]')
#     email.send_keys('akanksha.a@dgmarket.com')
#     passowrd = driver.find_element(By.XPATH, '//input[@name="password"]')
#     passowrd.send_keys('mf2vnrZw')
#     time.sleep(1)
#     search_btn = driver.find_element(By.XPATH, '//input[@value="Senden"]')
#     search_btn.click()
#     time.sleep(5)
#     new_window_link = driver.find_element(By.XPATH, '//*[@id="masterForm"]/table/tbody/tr[1]/td[6]/a[1]/img')
#     new_window_link.click()
#     time.sleep(5)
#     driver.switch_to.window(driver.window_handles[1])
#     time.sleep(5)
#     driver.close()
#     driver.switch_to.window(driver.window_handles[0])
#     driver.quit()
#     pass
all_data = []
def extraction():
    driver = webdriver.Firefox()
    url = "https://www.dtvp.de/Center/company/login.do?service=https%3A%2F%2Fwww.dtvp.de%2FCenter%2Fsecured%2Fcompany%2Fwelcome.do"
    driver.get(url)
    time.sleep(5)
    accept = driver.find_element(By.XPATH,'(//*[contains(text(),"Alles akzeptieren")])[2]')
    accept.click()
    time.sleep(2)
    email = driver.find_element(By.XPATH, '//input[@id="login"]')
    email.send_keys('akanksha.a@dgmarket.com')
    passowrd = driver.find_element(By.XPATH, '//input[@name="password"]')
    passowrd.send_keys('mf2vnrZw')
    time.sleep(1)
    search_btn = driver.find_element(By.XPATH, '//input[@value="Senden"]')
    search_btn.click()
    time.sleep(5)
    total_records = driver.find_element(By.XPATH, '//*[@id="masterForm"]/div[1]/h3').text
    tot_rec = int(re.findall(r"[\d]+", total_records)[0])
    no_pages=math.ceil(int(tot_rec)/20)
    for i in range(1,no_pages+1):

        elements = driver.find_elements(By.XPATH, '//*[@id="masterForm"]/table/tbody/tr')
        print(f"No of records found for page : {len(elements)}")
        for j in range(1,int(len(elements))+1):
            pass
            print('processing row:',j)
            end_date = driver.find_element(By.XPATH, f'//*[@id="masterForm"]/table/tbody/tr[{j}]/td[2]').text
            if end_date != 'nv':
                end_dates = end_date.split('.')
                yy = end_dates[-1]
                mm = end_dates[1]
                dd = end_dates[0]
                end_date = yy + '/' + mm + '/' + dd
                print(end_date)
                title = ''
                try:
                    titles = driver.find_element(By.XPATH, f'//*[@id="masterForm"]/table/tbody/tr[{j}]/td[3]').text
                    translator = Translator(to_lang="en")
                    english_translation = translator.translate(titles)
                    title = english_translation
                except:
                    pass
                print(title)
                pub_date =''
                try:
                    pub_date = driver.find_element(By.XPATH, f'//*[@id="masterForm"]/table/tbody/tr[{j}]/td[1]').text
                    if pub_date=='nv':
                        pub_date =''
                    elif pub_date !='nv':
                        from_date = pub_date.split('.')
                        yy=from_date[-1]
                        mm=from_date[1]
                        dd=from_date[0]
                        pub_date =yy + '/' + mm + '/' + dd
                except:
                    pass
                print(pub_date)
                Type =''
                try:
                    Type = driver.find_element(By.XPATH, f'//*[@id="masterForm"]/table/tbody/tr[{j}]/td[4]').text
                except:
                    pass
                print(Type)
                Vergabeplattform_Vergabeplattform =''
                try:
                    Vergabeplattform_Vergabeplattform = driver.find_element(By.XPATH, f'//*[@id="masterForm"]/table/tbody/tr[{j}]/td[5]').text
                except:
                    pass
                print(Vergabeplattform_Vergabeplattform)

            else:
                print("Scipping the Row Contians NV")

        Next_btn =driver.find_element(By.XPATH, f'//*[@id="masterForm"]/table/tbody/tr/td[2]').text


        # next_url = driver.find_element(By.XPATH, f'(//a[@class="noTextDecorationLink"])[2]').get_attribute("href")
        # print(next_url)
        # nextpage(next_url)
        time.sleep(2)
    driver.quit()
    print("process Completed")

if __name__ == '__main__':
    extraction()

