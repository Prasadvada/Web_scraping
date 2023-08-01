import json
from json import dumps
import scrapy
from scrapy import FormRequest
from scrapy.utils.response import open_in_browser


class Workjobs(scrapy.Spider):
    name = 'workjobs'
    cookies = {
        'PLAY_SESSION': '95969c5b66094c289e7e395181f8c2b18b29635d-ccc_pSessionId=15217at8f3fnq48kfkv135ln83&instance=wd5prvps0002i',
        'wday_vps_cookie': '2904961546.8755.0000',
        'timezoneOffset': '-330',
        'enablePrivacyTracking': 'true',
        'TS014c1515': '018b6354febcb1a8cc1fa4e58ae3c09512503e40b98c56d8f60b19eb9f9f830d16bebfbebeafa4629af319ba3cd023461fb039cb77',
        'wd-browser-id': '5a10e4ce-2575-4a86-8b12-26dcf8de4791',
        'CALYPSO_CSRF_TOKEN': 'baae78ac-3456-453c-8a6a-c21511462d0c',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    json_data = """{
        "appliedFacets": {},
        "limit": 20,
        "offset": %d,
        "searchText": ""
    }"""
    # json_data = '''{
    #     'appliedFacets': {},
    #     'limit': 20,
    #     'offset': 20,
    #     'searchText': '',
    # }'''

    offset = 20
    url = 'https://ccc.wd5.myworkdayjobs.com/wday/cxs/ccc/ccc_External/jobs'

    def start_requests(self):
        yield FormRequest(url=self.url, method='POST', headers=self.headers, cookies=self.cookies,
                          callback=self.parse_page_22)

    def parse_page_22(self, response):
        # print(response.text)
        data = json.loads(response.text)
        full_data = data.get('jobPostings')
        for job in full_data:
            title = job.get('title')
            print(title)
            yield {
                'title': title
            }
        if full_data:
            self.offset += 20
            yield self.make_request(self.offset)
            # yield self.make_request()

    def make_request(self, offset):
        return FormRequest(url=self.url, method="POST", headers=self.headers,
                           # body=dumps({"appliedFacets": {}, "limit": 20, "offset": self.offset, "searchText": ""}),
                           body=(self.json_data % self.offset),

                           cookies=self.cookies, callback=self.parse_page_22)

    # def make_request(self):
    #     return FormRequest(url=self.url, method="POST", headers=self.headers,
    #                        body=self.json_data%str(self.offset),callback=self.parse_page_22,)
