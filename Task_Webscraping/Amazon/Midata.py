from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np

def data_extraction(list_ref):
    doc_num, doc_index = list_ref
    print(doc_num)
    new_webpage = requests.get(doc_num, headers=HEADERS)
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")
    links = new_soup.find_all("a",class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    links_list = []
    for link in links:
        links_list.append(link.get("href"))
    print(len(links_list))
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        # print("https://www.amazon.in"+link)
        new_page = BeautifulSoup(new_webpage.content, "html.parser")
        Title = new_page.find('span',attrs={'id':"productTitle"}).text.strip()
        print(Title)
        Price = new_page.find('span',class_="a-price-whole").text.strip()
        # print(Price)

HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})
list_ref = []
doc_index = 0
for i in range(1,3):
    doc_index += 1
    if i ==1:
        url =f'https://www.amazon.in/s?i=computers&rh=n%3A4363893031&fs=true&qid=1686592658&ref=sr_pg_{i}'
        print(url)
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        list_ref.append([url, doc_index])
    elif i>1:
        url =f'https://www.amazon.in/s?i=computers&rh=n%3A4363893031&fs=true&page=2&qid=1686597486&ref=sr_pg_{i}'
        print(url)
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        list_ref.append([url, doc_index])
print(len(list_ref))
with ThreadPoolExecutor(max_workers=2) as exe:
    exe.map(data_extraction, list_ref)







