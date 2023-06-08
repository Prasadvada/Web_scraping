# TODO insterting data in mongoDB
from bs4 import BeautifulSoup
import requests
import pymongo
from concurrent.futures import ThreadPoolExecutor
sample_data = []
client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client["mydatabase"]
mycol = mydb["Zauba_outside_Data"]
def data_extraction(doc_list):
    doc_num, doc_index = doc_list
    url_2 = f'{doc_num}'
    while True:
        response = requests.get(url_2)
        break
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'table'})
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 4:
            cin = cells[0].text.strip()
            company_name = cells[1].text.strip()
            roc = cells[2].text.strip()
            status = cells[3].text.strip()
            # Create a document to be inserted into MongoDB
            document = {
                'cin': cin,
                'company_name': company_name,
                'roc': roc,
                'status': status,
            }
            x = mycol.insert_one(document)
            print(x.inserted_id)
    print("Data saved to MongoDB.")
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
    url = "https://www.zaubacorp.com/company-list/" + "p-" +str(page)+"-company.html"
    doc_index += 1
    doc_list.append([url, doc_index])
with ThreadPoolExecutor(max_workers=100) as exe:
    exe.map(data_extraction, doc_list)



# TODO inserting data in csv and Mongodb
# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# from pymongo import MongoClient
# import pymongo
# sample_data = []
# # Connect to MongoDB
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# mydb = client["mydatabase"]
# mycol = mydb["customers"]
# url_1 = 'https://www.zaubacorp.com/company-list/p-1-company.html'
# response1 = requests.get(url_1)
# soup = BeautifulSoup(response1.text, 'html.parser')
# pagination_info = soup.find('section', {'id': 'block-system-main'})
# rows = pagination_info.find_all('span')
# pages = rows[0].text.strip()
# count=pages.split()[-1].replace(',','').strip()
# print(count)
# for page in range(1,int(count)+1):
#     print('row:',page)
#     while True:
#         url = "https://www.zaubacorp.com/company-list/" + "p-" +str(page)+"-company.html"
#         print(url)
#         response = requests.get(url)
#         break
#     soup = BeautifulSoup(response.text, 'html.parser')
#     table = soup.find('table', {'id': 'table'})
#     rows = table.find_all('tr')
#     for row in rows:
#         cells = row.find_all('td')
#         if len(cells) >= 4:
#             sample_dic = {}
#             cin = cells[0].text.strip()
#             print(cin)
#             company_name = cells[1].text.strip()
#             roc = cells[2].text.strip()
#             status = cells[3].text.strip()
#             sample_dic['cin'] = cells[0].text.strip()
#             sample_dic['company_name'] = cells[1].text.strip()
#             sample_dic['roc'] = cells[2].text.strip()
#             sample_dic['status'] = cells[3].text.strip()
#             sample_data.append(sample_dic)
#             # Create a document to be inserted into MongoDB
#             document = {
#                 'cin': cin,
#                 'company_name': company_name,
#                 'roc': roc,
#                 'status': status,
#             }
#             x = mycol.insert_one(document)
#             print(x.inserted_id)
#     print("data", sample_data)
#     print("Data saved to MongoDB.")
# df = pd.DataFrame(sample_data)
# print(df)
# df.to_dict()
# df.to_csv('Zauba_data.csv', index=False, header=True)
