from bs4 import BeautifulSoup
import requests
HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})
URL ="https://www.amazon.in/Lenovo-Calling-Tab-2GB-32GB/dp/B08DD7VT8P/ref=lp_4363894031_1_1?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
title =soup.find('span',attrs={'id':"productTitle"}).text.strip()
Price =soup.find('span',attrs={'class':"a-offscreen"}).text.strip()
Tec =soup.find('h1',attrs={'class':"a-size-medium a-spacing-small"}).text.strip()
Brand =soup.find('td',attrs={'class':"a-size-base prodDetAttrValue"}).text.strip()



# from autoscraper import AutoScraper
# amazon_url="https://www.amazon.in/s?k=iphones"
#
# wanted_list=["₹67,999","Apple iPhone 14 (128 GB) - Midnight"]
# scraper=AutoScraper()
# result=scraper.build(amazon_url,wanted_list)
# print(result)
# print(scraper.get_result_similar(amazon_url,grouped=True))
# scraper.set_rule_aliases({'rule_mxzc':'Title','rule_y6o9':'Price'})
# scraper.keep_rules(['rule_mxzc','rule_y6o9'])
# scraper.save('amazon-search.csv')
