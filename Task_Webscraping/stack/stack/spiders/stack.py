import json
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
class StackItem(scrapy.Spider):
    name = "parker"
    body = "{'count':'1','Latitude':0,'Longitude':'0','cityID':'10','location':''}"
    headers = {'Content-Type': 'application/json'}
    url_1 = "https://www.vijaysales.com/Store-Locator.aspx/getStoreStruct_Web"
    def start_requests(self):
        yield Request(url='https://www.vijaysales.com/Store-Locator.aspx/getStoreStruct_Web', body=self.body,
                      method='POST',
                      headers=self.headers,callback=self.parse_page)

    def parse_page(self,response):
        open_in_browser(response)
        json_data = json.loads(response.body)
        html_string = json_data['d'].encode().decode('unicode_escape')
