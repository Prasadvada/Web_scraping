import scrapy
from scrapy.http import Request, FormRequest
import json
from scrapy.utils.response import open_in_browser


class Workdays(scrapy.Spider):
    name = "workday"
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    json_data = '''{
        'appliedFacets': {},
        'limit': 20,
        'offset': %s,
        'searchText': '',
    }'''
    offset = 20
    url_1 = "https://ccc.wd5.myworkdayjobs.com/wday/cxs/ccc/ccc_External/jobs"

    def start_requests(self):
        yield self.make_request()

    def parse(self, response):

        print(response.text)
        open_in_browser(response)
        data = json.loads(response.text)
        full_data = data.get('jobPostings')
        for job in full_data:
            title = job.get('title')
        if full_data:
            self.offset += 20
            yield self.make_request()
            # yield Request(url=self.url_1, body=json.dumps(self.json_data) % str(self.offset), headers=self.headers,
            #               method="POST", callback=self.parse)

    def make_request(self):
        import pdb;pdb.set_trace()

        return FormRequest(url=self.url_1, formdata=self.json_data % (self.offset), headers=self.headers, method="POST",
                           callback=self.parse)


# import scrapy
# from scrapy.http import Request, FormRequest
# import json
# from scrapy.utils.response import open_in_browser
#
#
# class Workdays(scrapy.Spider):
#     name = "workday_test"
#     headers = {
#         'Accept': 'application/json',
#         'Accept-Language': 'en-US',
#         'Origin': 'https://ccc.wd5.myworkdayjobs.com',
#         'Referer': 'https://ccc.wd5.myworkdayjobs.com/en-US/ccc_External',
#         'Content-Type': 'application/json',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#     }
#
#     json_data = '''{
#         'appliedFacets': {},
#         'limit': 20,
#         'offset': %s,
#         'searchText': '',
#     }'''
#     offset_value = 20
#     url_1 = "https://ccc.wd5.myworkdayjobs.com/wday/cxs/ccc/ccc_External/jobs"
#
#     # def start_requests(self):
#     #     yield self.make_request()
#
#     def parse(self, response):
#         import pdb; pdb.set_trace()
#         yield self.make_request(response)
#     def parse_job(self, response):
#         import pdb; pdb.set_trace()
#         print(response.text)
#         open_in_browser(response)
#         data = json.loads(response.text)
#         full_data = data.get('jobPostings')
#         for job in full_data:
#             title = job.get('title')
#             print(title)
#             print('**********')
#
#         # if full_data:
#         #     self.offset += 20
#         #     import pdb;pdb.set_trace()
#         #     yield self.make_request()
#
#     def make_request(self,response):
#         return Request(url=self.url_1, callback=self.parse_job, method="POST", headers=self.headers,
#                        body=self.json_data % str(self.offset_value))
