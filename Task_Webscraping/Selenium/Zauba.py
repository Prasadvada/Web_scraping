import time
from selenium import webdriver
import csv
from bs4 import BeautifulSoup
import csv

data = []
for j in range(1,3):
    print(j)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    while True:
        try:
            url = f"https://www.zaubacorp.com/company-list/p-{j}-company.html"
            print(url)
            driver.get(url)
            time.sleep(2)
            break
        except:
            pass

    source_code=driver.page_source
    soup = BeautifulSoup(source_code,'lxml')
    row = soup.select('tbody tr')
    for i in row:
        a= i.find_all('td')
        Cin = a[0].text
        company = a[1].text
        Roc = a[2].text
        status = a[3].text
        data.append({'CIN':Cin,'Company':company,'RoC':Roc,'Status':status})
    print('data',data)

csv_filename = "company_data_1.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file,fieldnames =["CIN", "Company", "RoC", "Status"])
    csv_writer.writeheader()
    csv_writer.writerows(data)
