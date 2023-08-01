import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser


class Keep(scrapy.Spider):
    name = "kepio"
    url_1 = "https://kepio.in/vacancies/"

    def start_requests(self):
        yield FormRequest(url=self.url_1, callback=self.parse_page)

    def parse_page(self, response):
        for i in range(1,11):
            doc_no = response.xpath(f'(//*[@class="awsm-job-post-title"]//a)[{i}]/text()').extract()
            doc_no_1 = response.xpath(f'(//div[@class="awsm-job-specification-item awsm-job-specification-job-category"]/span/text())[{i}]').extract()
            yield {
                "Name_extract": doc_no,
                "Name": doc_no_1
            }
