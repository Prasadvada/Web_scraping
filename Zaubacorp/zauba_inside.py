import time
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
from lxml.html import fromstring
import pymongo
sample_data = []
client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client["mydatabase"]
mycol = mydb["customers"]
def data_extraction(doc_list):
    doc_num, doc_index = doc_list
    url_2 = f'{doc_num}'
    response = requests.get(url_2)
    time.sleep(2)
    resp = fromstring(response.text)
    try:
        CIN =resp.xpath("//p[.='CIN']/../following-sibling::td/p/a/text()")[0]
        print(CIN)
        Company_Name = resp.xpath("//p[.='Company Name']/../following-sibling::td/p/text()")[0]
        Company_Status =resp.xpath("//p[.='Company Status']/../following-sibling::td/p/span/text()")[0]
        RoC =resp.xpath("//p[.='RoC']/../following-sibling::td/p/text()")[0]
        Registration_Number =resp.xpath("//p[.='Registration Number']/../following-sibling::td/p/text()")[0]
        Company_Category =resp.xpath("//p[.='Company Category']/../following-sibling::td/p/text()")[0]
        Company_Sub_Category =resp.xpath("//p[.='Company Sub Category']/../following-sibling::td/p/text()")[0]
        Class_of_Company =resp.xpath("//p[.='Class of Company']/../following-sibling::td/p/text()")[0]
        Date_of_Incorporation =resp.xpath("//p[.='Date of Incorporation']/../following-sibling::td/p/text()")[0]
        Age_of_Company =resp.xpath("//p[.='Age of Company']/../following-sibling::td/p/text()")[0]
        Activity =resp.xpath("//p[.='Activity']/../following-sibling::td/p/text()")[0]
        Authorised_Capital = resp.xpath("//p[.='Authorised Capital']/../following-sibling::td/p/text()")[0]
        Paid_up_capital = resp.xpath("//p[.='Paid up capital']/../following-sibling::td/p/text()")[0]
        email = resp.xpath("//b[.=' Email ID: ']/../text()")[0]
        Address = resp.xpath("//b[.='Address: ']/../following-sibling::p/text()")[0]
        document = {
            'CIN': CIN,
            'Company_Name': Company_Name,
            'Company_Status': Company_Status,
            'RoC': RoC,
            'Registration_Number': Registration_Number,
            'Company_Category': Company_Category,
            'Company_Sub_Category': Company_Sub_Category,
            'Class_of_Company': Class_of_Company,
            'Date_of_Incorporation': Date_of_Incorporation,
            'Age_of_Company': Age_of_Company,
            'Activity': Activity,
            'Authorised_Capital': Authorised_Capital,
            'Paid_up_capital': Paid_up_capital,
            'email': email,
            'Address': Address,
        }
        x = mycol.insert_one(document)
        print(x.inserted_id)
    except:
        pass
# Connect to MongoDB
url_1 = 'https://www.zaubacorp.com/company-list/p-1-company.html'
response1 = requests.get(url_1)
soup = BeautifulSoup(response1.text, 'html.parser')
pagination_info = soup.find('section', {'id': 'block-system-main'})
rows = pagination_info.find_all('span')
pages = rows[0].text.strip()
count=pages.split()[-1].replace(',','').strip()
doc_list = []
doc_index = 0
for page in range(1,int(count)+1):
# for page in range(1,11):
    while True:
        url = "https://www.zaubacorp.com/company-list/" + "p-" +str(page)+"-company.html"
        response = requests.get(url)
        break
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'table'})
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 4:
            href = cells[1].find('a')['href']
            doc_index += 1
            doc_list.append([href,doc_index])
with ThreadPoolExecutor(max_workers=10) as exe:
    exe.map(data_extraction,doc_list)
