import scrapy
from scrapy.http import Request, FormRequest
import json
from scrapy.utils.response import open_in_browser
class napa(scrapy.Spider):
    name = "napa"
    headers = {
        'Origin': 'http://fiddle.jshell.net',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'http://fiddle.jshell.net/_display/',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    # url_1 = "https://www.napaonline.com/en/search?text=grote&referer=v2"
    url_1 = "https://accio.genpt.com/api/v1/core/?site=us&fl=pid%2Ctitle%2Cbrand%2Csale_price%2Cprimary_image%2Cthumb_image%2Curl%2Cdescription%2Cunit_of_measure%2Cproduct_line%2Cline_abbreviation%2Cpart_number%2Cinterchange_parts%2Cuniversal%2Cfield_sku%2Chq_abbrev%2Cregulatory%2Cpriced_from%2Cpriced_to%2Cretail_redirect%2Cretail_url&_br_uid_2=&request_type=search&search_type=keyword&domain_key=napaonline&url=https%3A%2F%2Fwww.napaonline.com%2Fen%2Fsearch%3Ftext%3Dgrote%26referer%3Dv2&facet.range=price&facet.application_part_type.limit=300&q=grote&view_id=FRE&efq=dc%3A%22FRE%22&rows=300&start=0&sort=relevance+asc"
    def start_requests(self):
        yield FormRequest(url=self.url_1,headers=self.headers, method="POST",callback=self.parse_page1)
    # def parse_page(self,response):
    #     start_row = 0
    #     for i in range(1, 17):
    #         start_row += 300
    #         url_1 = f"https://accio.genpt.com/api/v1/core/?site=us&fl=pid%2Ctitle%2Cbrand%2Csale_price%2Cprimary_image%2Cthumb_image%2Curl%2Cdescription%2Cunit_of_measure%2Cproduct_line%2Cline_abbreviation%2Cpart_number%2Cinterchange_parts%2Cuniversal%2Cfield_sku%2Chq_abbrev%2Cregulatory%2Cpriced_from%2Cpriced_to%2Cretail_redirect%2Cretail_url&_br_uid_2=&request_type=search&search_type=keyword&domain_key=napaonline&url=https%3A%2F%2Fwww.napaonline.com%2Fen%2Fsearch%3Ftext%3Dgrote%26referer%3Dv2&facet.range=price&facet.application_part_type.limit=300&q=grote&view_id=FRE&efq=dc%3A%22FRE%22&rows=300&start={start_row}&sort=relevance+asc"
    #         print(url_1)
    #         yield FormRequest(url=url_1, headers=self.headers, method="POST", callback=self.parse_page1)
    def parse_page1(self, response):
        # import pdb;pdb.set_trace()
        # open_in_browser(response)
        # data = json.loads(response)
        data = json.loads(response.text)
        y=data.get('response').get('docs')
        for i in y:
            title = i.get('sale_price')
            print(title)
            Requid_ID = i.get('title')
            url = i.get('url')
            yield {
                'Title': title,
                "REQUID_ID": Requid_ID,
                "url": url
            }