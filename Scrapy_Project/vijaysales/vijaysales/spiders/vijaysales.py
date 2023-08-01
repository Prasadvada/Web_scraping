import json
import re
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
class Arendt(scrapy.Spider):
    name = "vijay"
    body = "{'count':'1','Latitude':0,'Longitude':'0','cityID':'10','location':''}"
    headers = {'Content-Type': 'application/json'}
    url_1 = "https://www.vijaysales.com/Store-Locator.aspx/getStoreStruct_Web"

    def start_requests(self):
        yield Request(url='https://www.vijaysales.com/Store-Locator.aspx/getStoreStruct_Web', body=self.body,
                      method='POST', callback=self.parse,
                      headers=self.headers)

    def parse(self, response):
        open_in_browser(response)
        json_data = json.loads(response.body)
        html_string = json_data['d'].encode().decode('unicode_escape')
        selector = Selector(text=html_string)
        location_elements = selector.css('.dv-location')
        for location_element in location_elements:
            location_name = location_element.css('.location-head::text').get()
            address = location_element.css('.location-text-content > .row::text').get().strip()
            PIN_CODE = ''
            try:
                PIN_CODE = re.findall(r"Delhi-([\d]+)", address, flags=re.I)[0]
            except:
                pass
            contact_number = ''
            try:
                contact_numb = location_element.css("a.lnkStpB4Unload::text").get().strip()
                if contact_numb:
                    contact_number = contact_numb.strip()
                    print("Contact Number:", contact_number)
                else:
                    print("Contact number not found.")
            except:
                pass
            print("Location Name:", location_name)
            print("Address:", address)
            print("PIN_CODE:", PIN_CODE)
            print("Contact_Number:", contact_number)
            print("\n")
            yield {
                "Location Name:": location_name,
                "Address:": address,
                "PIN_CODE": PIN_CODE,
                "Contact_Number:": contact_number
            }
from scrapy.cmdline import execute
execute('scrapy crawl vijay -O vijay_sales.csv'.split())