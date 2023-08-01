import scrapy
from scrapy.http import Request, FormRequest
import json
from scrapy.utils.response import open_in_browser


class walleniu(scrapy.Spider):
    name = "wallet"
    headers = {
        'authority': 'careers.walleniuswilhelmsen.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    cookies = {
        'searchSource': 'external',
        'jrasession': '2acf0545-d98f-4f70-b500-7cdbe85a1041',
        'pixel_consent': '%7B%22cookie%22%3A%22pixel_consent%22%2C%22type%22%3A%22cookie_notice%22%2C%22value%22%3Atrue%2C%22timestamp%22%3A%222023-03-09T14%3A45%3A45.761Z%22%7D',
        'i18n': 'en-US',
        'session_id': 'da244099-826d-4ecc-b792-42094cbf21ac',
        '__atuvc': '5%7C10',
        'jasession': 's%3AL8KgOmCKkzfnPSLZnGIAqv2bjP3YKWH-.iXnYiycFKx%2BZm6khKcMX4w6fy8Tu%2BSCaPRDVeBkp7sM',
        '_janalytics_ses.269d': '*',
        '_janalytics_id.269d': '0e5860b9-11f8-4476-a08a-615f75df74ae.1678372995.8.1678634812.1678564601.880f6a96-d37f-46bd-a492-ff89d24835c7',
        '_jibe_sticky_params': 'eyJxdWVyeUlkIjoiNDc3OTliZGYtNmUzYy00Y2M5LTk4NWMtYzc1MTQ2ZTVlYmIxIiwiZ29vZ2xlUmVxdWVzdElkIjpudWxsLCJpc0tleXdvcmRUeXBlYWhlYWQiOmZhbHNlLCJpc0xvY2F0aW9uVHlwZWFoZWFkIjpmYWxzZSwiZXZlbnRUcmlnZ2VyIjoic2VhcmNoLWhvbWUtc3VibWl0LWJ1dHRvbiJ9',
    }

    params = {
        'keywords': 'operation',
        'page': '1',
        'sortBy': 'relevance',
        'descending': 'false',
        'internal': 'false',
    }
    url_1 = "https://careers.walleniuswilhelmsen.com/careers-home/"

    def start_requests(self):
        yield FormRequest(url=self.url_1,callback=self.parse_page)

    def parse_page(self, response):
        for i in range(1,12):
            url_2 = f"https://careers.walleniuswilhelmsen.com/api/jobs?page={i}&sortBy=relevance&descending=false&internal=false&deviceId=2643272707&domain=2wglobal.jibeapply.com"
            yield FormRequest(url=url_2,headers=self.headers,cookies=self.cookies,callback=self.parse_page1)

    def parse_page1(self, response):
        open_in_browser(response)
        data = json.loads(response.text)
        y=data.get('jobs')
        for i in y:
            title = i['data'].get('title')
            print(title)
            Requid_ID = i['data'].get('req_id')
            print(Requid_ID)

            yield {
                'Title':title,
                "REQUID_ID":Requid_ID
            }