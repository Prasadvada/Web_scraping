import scrapy
from scrapy.http import Request, FormRequest
import json
from scrapy.utils.response import open_in_browser
class napa(scrapy.Spider):
    name = "zauba"
    start_urls = "https://www.zaubacorp.com/company-list/p-1-company.ht"
    def parse(self, response):
        total = response.css('.quote')
        for i in total:
            title = i.css('.text').extract()
            Author_name = i.css('.author').extract()

            yield {
                "title_name":title,
                "author_name":Author_name
            }
        next_btn = response.css('li.next a::attr(href)').get()
        if next_btn is not None:
            print("clicking Next btn")
            yield response.follow(next_btn,self.parse)

