from scrapy.http import HtmlResponse
from translate import Translator
import math
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Firefox()
def nextpage(next):
    driver = webdriver.Firefox()
    time.sleep(5)
    url =next
    driver.get(url)
    time.sleep(2)
    html_source = driver.page_source
    response = HtmlResponse(url="my HTML string", body=html_source, encoding='utf-8')
    Name = response.xpath('//h3[@id="contracting_authority-1"]//following-sibling::p[@class="govuk-body govuk-!-margin-bottom-0"]').getall()
    print(Name)
    CPU = response.xpath('(//ul[@class="govuk-list govuk-list--bullet"]//li)[4]').get()
    print(CPU)
    time.sleep(5)
    driver.close()
    pass
def extraction():
    url = "https://www.find-tender.service.gov.uk/Search/Results?&page=1#dashboard_notices"
    driver.get(url)
    time.sleep(5)
    total_pages = '4'
    for i in range(1,int(total_pages)):
        print("processing_page", {i})

        elements = driver.find_elements(By.XPATH, '//*[@class="search-result-header"]')
        print(f"No of records found for page : {len(elements)}")
        for j in range(1, int(len(elements)) + 1):
            Title = driver.find_element(By.XPATH, f'(//div[@class="search-result-header"]//h2/a)[{j}]').text
            print(Title)
            Date = driver.find_element(By.XPATH,'(//strong[contains(text(),"Publication date")])[1]/../following-sibling::dd').text
            date = Date.split(',')
            dates =(date[0].replace('August', '08'))
            yy =dates.split()[-1]
            mm =dates.split()[1]
            dd =dates.split()[0]
            dat = yy + '/' + mm + '/' + dd
            print(dat)
        try:
            Nxt_btn = driver.find_element(By.XPATH,'//a[@class="standard-paginate-next govuk-link break-word"]')
            Nxt_btn.click()
            time.sleep(5)
        except:
            pass
    nextpage_href = driver.find_element(By.XPATH,'(//div[@class="search-result-header"]//h2/a)[1]').get_attribute('href')
    print(nextpage_href)
    nextpage(nextpage_href)

if __name__ == '__main__':
    extraction()


