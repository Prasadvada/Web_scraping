import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser


class Arendt(scrapy.Spider):
    name = "arendt"
    data = {
        'guest': 'true',
        'submit': 'I Acknowledge',
    }
    data_1 = {
        'RecordingDateIDStart': '01/01/1818',
        'RecordingDateIDEnd': '03/03/2023',
        'BothNamesIDSearchString': 'SMITH',
        'BothNamesIDSearchType': 'Basic Searching',
        'DocumentNumberID': '',
        'BookType': [
            '',
            '',
        ],
        'BookPageIDBook': '',
        'BookPageIDPage': '',
        'GrantorIDSearchString': '',
        'GrantorIDSearchType': 'Basic Searching',
        'GranteeIDSearchString': '',
        'GranteeIDSearchType': 'Basic Searching',
        'AllDocuments': 'ALL',
        'docTypeTotal': '79',
    }


    url_1 = "https://eriecountyoh-web.tylerhost.net/erieohweb/eagleweb/docSearch.jsp"
    url_2 = "https://eriecountyoh-web.tylerhost.net/erieohweb/eagleweb/docSearchPOST.jsp"
    # url_3 = f"https://eriecountyoh-web.tylerhost.net/erieohweb/eagleweb/viewDoc.jsp?{x}"
    url_3 = "https://eriecountyoh-web.tylerhost.net/erieohweb/eagleweb/viewDoc.jsp?node=DOCC240111"

    def start_requests(self):
        yield FormRequest(url=self.url_1, method='POST', formdata=self.data, callback=self.parse_page)

    def parse_page(self, response):
        # open_in_browser(response)
        yield FormRequest(url=self.url_2, method='POST', formdata=self.data_1, callback=self.parse_page_11)


    def parse_page_11(self, response):
        total = response.xpath('//*[@id="searchResultsTable"]/tbody/tr/td[2]/a/@href').get()
        print(total)
        x = total.split('?')[1]
        # url_3 = f"https://eriecountyoh-web.tylerhost.net/erieohweb/eagleweb/viewDoc.jsp?{x}"
        # print(url_3)
        yield FormRequest(url=self.url_3, callback=self.parse_page1)

    def parse_page1(self, response):
        open_in_browser(response)
        # quote = response.xpath('//*[@id="searchResultsTable"]/tbody/tr')
        # print(len(quote))
        # # for i, count in enumerate(quote):
        # for i in quote:
        doc_no = response.xpath(
            '//span[contains(text(),"Document Number")]//following-sibling::span[1]/span[1]/text()').extract_first().strip()
        yield {
            "Name_extract": doc_no
        }
        next_page = response.xpath('(//a[contains(text(),"Next")])[1]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_page1)
