import math
import re
import time
import sqlite3
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
print("Amazon Website Search Initiated!!")
conn = sqlite3.connect('amazon_products.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        price TEXT
    )
''')
conn.commit()
def amazon():
    while True:
        driver.get('https://www.amazon.in/mobile-phones/b/?ie=UTF8&node=1389401031&ref_=nav_cs_mobiles')
        print(f"loading Amazon Website!!")
        driver.maximize_window()
        break
    print(f"loaded Amazon Website sucessfully!!")
    wait = WebDriverWait(driver, 100)
    wait.until(
        EC.visibility_of_element_located((By.XPATH, '//a[@data-csa-c-content-id="nav_cs_mobiles"]'))).click()
    time.sleep(5)
    elem_clicking = wait.until(
        EC.visibility_of_element_located((By.XPATH, '(//i[@class="a-icon a-icon-checkbox"])[6]')))
    elem_clicking.click()
    time.sleep(5)
    try:
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
            (By.XPATH, '//span[@class="a-size-medium-plus a-color-base a-text-bold"]')))
    except Exception as e:
        print("please try Again the page is not loaded")
    total_records = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="a-section a-spacing-small a-spacing-top-small"]//span'))).text
    tot_rec = int(re.findall(r"[\d]+", total_records)[-1])
    print(f"No of records found for search - {tot_rec}")
    no_pages=math.ceil(int(tot_rec)/24)
    for i in range(1,no_pages+1):
        print(f"processing Page :{i}")
        try:
            elements = WebDriverWait(driver,100).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))
            print(f"No of records found for page : {len(elements)}")
            for j in range(1,int(len(elements))+1):
                html_source = driver.page_source
                response = HtmlResponse(url="my HTML string", body=html_source, encoding='utf-8')

                product_name = response.xpath(f'(//div[@data-component-type="s-search-result"]//span[@class="a-size-base-plus a-color-base a-text-normal"]/text())[{j}]').get(default='').strip()
                product_price = response.xpath(f'(//span[@class="a-price-whole"]/text())[{j}]').get(default='').strip()
                cursor.execute("INSERT OR IGNORE INTO products (name, price) VALUES (?, ?)", (product_name, product_price))
                conn.commit()
        except:
            pass
        try:
            next_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(),"Next")]')))
            next_button.click()
            time.sleep(5)
        except:
            pass
        try:
            WebDriverWait(driver,100).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="a-size-medium-plus a-color-base a-text-bold"]')))
        except:
            pass
    print(f"Data Extraction Completed Successfully:")
    driver.quit()
    data_base()

def data_base():
    print(f"Connect to the database")
    conn = sqlite3.connect('amazon_products.db')
    cursor = conn.cursor()
    print(f"Execute a query to retrieve data from the products table")
    cursor.execute("SELECT * FROM products")
    print(f"Fetch all the rows")
    rows = cursor.fetchall()
    print(f"Print the retrieved data")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}")
    print(f"Close the connection")
    conn.close()
if __name__ == '__main__':
    amazon()


