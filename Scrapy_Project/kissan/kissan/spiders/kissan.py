from scrapy.utils.response import open_in_browser
import scrapy
import json
from datetime import datetime
class DataSpider(scrapy.Spider):
    name = 'data_spider'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://data.gov.in/datasets_webservices/datasets/6622307',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    def start_requests(self):
        num_pages = 20  # Number of pages to scrape
        offset = 0  # Initial offset value
        for i in range(num_pages):
            url = f"https://data.gov.in/backend/dmspublic/v1/resources?offset={offset}&limit=8&filters[external_api_reference]=6622307&query=Gujarat&sort[_score]=desc"
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
            # yield scrapy.Request(url, callback=self.parse)
            offset += 8  # Increase the offset value for the next request
    def parse(self, response):
        # open_in_browser(response)
        data = json.loads(response.body)
        print(data)
        rows = data['data']['rows']
        for row in rows:
            Title=''
            try:
                Title = row['title'][0]
            except:
                pass
            Json_url=''
            try:
                Json_url = row['datafile_url'][0]
            except:
                pass
            published_date=''
            try:
                published_timestamp = row['published_date'][0]
                published_date = datetime.fromtimestamp(published_timestamp).strftime('%d/%m/%Y')
            except:
                pass
            updated_date=''
            try:
                updated_timestamp = row['changed'][0]
                updated_date = datetime.fromtimestamp(updated_timestamp).strftime('%d/%m/%Y')
            except:
                pass
            Download_Number=''
            try:
                Download_Number = row['download_count'][0]
                if Download_Number == '':
                    Download_Number=0
                else:
                    pass
            except:
                pass
            print(f"Title: {Title}")
            print(f"Json_url: {Json_url}")
            print(f"Download_Number: {Download_Number}")
            print(f"published_date: {published_date}")
            print(f"updated_date: {updated_date}")
            yield {
                'Title': Title,
                'JSON URL': Json_url,
                'Download Count': Download_Number,
                'published_date': published_date,
                'updated_date': updated_date,
            }
from scrapy.cmdline import execute
execute('scrapy crawl data_spider -O Kissan_data_spider.csv'.split())


