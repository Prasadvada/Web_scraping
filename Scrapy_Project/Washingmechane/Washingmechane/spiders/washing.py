import time

import scrapy
from scrapy.http import  FormRequest
from scrapy.utils.response import open_in_browser

class SiemenItem(scrapy.Spider):
    name = "Washing"
    headers = {
        'Origin': 'http://fiddle.jshell.net',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'http://fiddle.jshell.net/_display/',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = {
        'msg1': 'wow',
        'msg2': 'such',
        'msg3': 'data',
    }

    cookies = {
        "PHPSESSID": "946hl5lpbcf6jalm271g2450u8",
        "spitogatosHomepageMap": "0",
        "currentCurrency": "EUR",
        "_ga": "GA1.2.1080968683.1626031679",
        "_gid": "GA1.2.1871094347.1627582033",
        "_hjTLDTest": "1",
        "_hjid": "66a31a57-9c80-47f1-8767-9bca91d47b1f",
        "_fbp": "fb.1.1626031679317.910543448",
        "__qca": "P0-1840509725-1625417320200",
        "_hjAbsoluteSessionInProgress": "0",
        "openedTabs": "1",
        "_gat_UA-3455846-10": "1",
        "_gat_UA-3455846-2": "1",
        "_hjIncludedInSessionSample": "1",
        "reese84": "3:5Stu7C2tUWBSIdWSdzMOSQ==:ppmbagk94sf6IvvS66908AApyTMfCE+K7i7PgkeyRs6C9VGkCcqBSz8ZsgbOx56c46ktjL+1iyfp8zL1PuiT7AUsmA9XLdcmMoDQm30MnEPgcbQl/dMQV1PgqtVJgWVwGabZlMhGM+T6D8zf5ENVuGhLJ81U74a+gr+GySA5Xx/CqUPcGa/YG2zNICEMnZN7D4bRwJq6vxEvOU+wbSfAE6OquI4ipeHR3dz8jBwY961ka2PfY7MoLCLeGdzPUu07yOxv41lvdcZbaj9/peyxLnLSFqD9QnV5MXsXy7mKE3eNoT46F/ITB8/GAVpc/zqW792F+7HuUkWJD/pWaNOsr6+rc75kpKw15xtN5oCw9Qh3Fw9SYUtfbFMTRXBrUt0Ow/Lv2C3oOLBQyVex80cr76c4ibxS/niuNvKA87f7XZc=:THUtE26ivNhlKtaznqNuX7swpAf4x5S8pF+xoBg5KwE="
    }
    url_1 = "https://www.expert.de/shop/unsere-produkte/haushalt-kuche/waschen-trocknen-bugeln-nahen/waschmaschinen"
    def start_requests(self):
        yield FormRequest(url=self.url_1,headers=self.headers,method='GET',cookies=self.cookies,callback=self.parse_page)
    def parse_page(self, response):
        time.sleep(5)
        open_in_browser(response)
        total =len(response.xpath('//*[@id="lpBloc"]/li[position()>1]/div/div/form/div[2]/a/h2/text()'))
        print(total)
        for i in range(1,int(total)+1):
            print("row:",i)
            Name = response.xpath(f'(//*[@id="lpBloc"]/li[position()>1]/div/div/form/div[2]/a/h2/text())[{i}]').get()
            price =  response.xpath(f'(//span[@class="hideFromPro priceColor price"]/text())[{i}]|(//span[@class="hideFromPro priceColor price"]/sup/text())[{i}]').get()
            Rating = response.xpath(f'(//div[4]/div[3]/div/ul/li[position()>1]/div/div/form/div[2]/span/span[1]/span[2]/text())[{i}]').get()
            print(Rating)
            yield {
                "Product_Name": Name,
                "price": price,
                "Rating": Rating
            }
