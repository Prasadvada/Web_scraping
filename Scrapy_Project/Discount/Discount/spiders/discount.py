import scrapy
from scrapy import FormRequest
class expertSpider(scrapy.Spider):
    name = "expert"
    url_1 = 'https://www.cdiscount.com/'
    def start_requests(self):
        yield FormRequest(url=self.url_1,callback=self.parse_page1)
    def parse_page1(self, response):
        title = response.css('title::text').extract()
        print(title)
        yield {
            "title_name": title
        }