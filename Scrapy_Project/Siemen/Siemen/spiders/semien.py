import time

import scrapy
from scrapy.http import  FormRequest
from scrapy.utils.response import open_in_browser

class SiemenItem(scrapy.Spider):
    name = "Siemenitem1"
    headers = {
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.wikipedia.org/',
        'Connection': 'keep-alive',
    }

    # headers = {
    #     'authority': 'www.cdiscount.com',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    #     'cache-control': 'no-cache',
    #     # 'cookie': 's_ecid=MCMID%7C54514361572758946496794985570109274631; tcId=af6e9396-4512-414c-877a-21f9e163ee14; CookieId=CookieId=230216142125SWUKPGOM&IsA=0; TCPID=123241851271322862960; UniqueVisitContext=UniqueVisitId__230216142128IISXLNEJ__; _cs_c=3; TC_PRIVACY=1@078%7C2%7C2%7C183@@@1676553804369%2C1676553804369%2C1692105804369@; TC_PRIVACY_CENTER=; _$cst=0; _cs_id=6ecbb97e-5708-ad42-b175-3ed3e9fd2ad0.1676553689.5.1678119423.1678119317.1590586488.1710717689726; app_vi=34214400%7C; prio7j=prio4; prio30j=prio4; TC_AB=B; SitePersoCookie=PersoCountryKey____PersoLatitudeKey____PersoLongitudeKey____PersoTownKey____GeolocPriorityKey__0__PersoPostalCodeKey____PersoUrlGeoSCKey____ExpressSellerId____ExpressShopName____ExpressGlobalSellerId____ShowroomVendorId____RetailStoreName____VehicleId__0__AddressId____; chcook7=direct; AMCV_6A63EE6A54FA13E60A4C98A7%40AdobeOrg=1585540135%7CMCIDTS%7C19533%7CMCMID%7C54514361572758946496794985570109274631%7CMCAID%7CNONE%7CMCOPTOUT-1676560875s%7CNONE%7CvVersion%7C4.4.0; mssctse=W2dNXeEyrPI7vQSipcj0oZee3Bk6auOe_sRo7F4cs1YUHxgFjM-oF-vi3v4ry8jL3f4h3h_8iRw3RDVGjaO08Q; svisit=1; s_cc=true; _$dtype=t:d; msswt=; visit_baleen_ACM-655d44=9S4sww_skopGmQhr-I8Hqwm8IipCMttgAgdxOemJ5tvWe6m9dYR90n8I56YN7XGT4dDGtJA-cA3G8PKRjmcNb1Dx1oBcflNDZMIg-It8VNBynyNHo8C9rIj6Cn6MFrqcfHVk_W0kJ2NbRGy1Xz5miBZRHVwHrJsY569h0V6XT0572TNU9KSxHoBll9CGGPgs-VPaZxEdUZvUN-aC2hd3iTawzY1DxOKJlH4EC_81fWNgiyZSJrmeKQ27lDjcrdXOw8g3AQNb5E5RCkZBUwQzHRhznlactiu2rQj5j3QdmHHxA5mM7poitRtl0bwgCSex; cache_cdn=; _$3custinf=AUT=0&XV1=0; el2=0; s_pv=L-242935%3ACuisini%C3%A8re%20%C3%A9lectrique; tp=14798; msstvt=apEBX8keq086HQEjTe9RGvNYxLB_-1O1x4A2TBG919ovEPgd72jRgddCbF-Vxjc12XVGhYtUsvLkYd7Zl0WXvWqUpR0VNKYKJlx7_IiPZDeJA7t1l3h_OGO5BJrvDN0Blh5eiy8tNWR16qLbeHlfjA; visit_baleen_ACM-655d43=XZwNzxbyzReZG0Zgt7wgXkxwynG6aB51PUhT0h1ybfxj5_b-XVrsdF-cUQ2HLE6m_n4OlUvAe7zPg8G1xlPJXCjlTWC7AqpqmXnAm34Es-sRtN0nbFpW6kEi5gQrP2dWEvXbwjCFzeHTwZZunVCJKMFyTQFEF8PoviXPNP3xroehc81G_azaPMztgb89cIpEqu8ycIlFpy-vp1RRW6jsKz4h5_4I0BID1z-mFWAD9I13fGd_2gK-I_u41y7JCN0jTkptdvJTst_MTcJ2jle96Q; VisitContextCookie=R5-gHDaGc_ZuxFVSkPNVHVOaB6iqvvcp-OvGQFeTaGdisv8AlTn_tw; s_nr=1687636136314-Repeat; s_ppv=L-242935%253ACuisini%25C3%25A8re%2520%25C3%25A9lectrique%2C2%2C2%2C350',
    #     'pragma': 'no-cache',
    #     'referer': 'https://www.cdiscount.com/electromenager/four-cuisson/cuisinieres/cuisinieres-table-electrique/l-110230211.html',
    #     'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'document',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-site': 'same-origin',
    #     'sec-fetch-user': '?1',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    # }

    cookies = {
        's_ecid': 'MCMID%7C54514361572758946496794985570109274631',
        'tcId': 'af6e9396-4512-414c-877a-21f9e163ee14',
        'CookieId': 'CookieId=230216142125SWUKPGOM&IsA=0',
        'TCPID': '123241851271322862960',
        'UniqueVisitContext': 'UniqueVisitId__230216142128IISXLNEJ__',
        '_cs_c': '3',
        'TC_PRIVACY': '1@078%7C2%7C2%7C183@@@1676553804369%2C1676553804369%2C1692105804369@',
        'TC_PRIVACY_CENTER': '',
        '_$cst': '0',
        '_cs_id': '6ecbb97e-5708-ad42-b175-3ed3e9fd2ad0.1676553689.5.1678119423.1678119317.1590586488.1710717689726',
        'app_vi': '34214400%7C',
        'prio7j': 'prio4',
        'prio30j': 'prio4',
        'TC_AB': 'B',
        'SitePersoCookie': 'PersoCountryKey____PersoLatitudeKey____PersoLongitudeKey____PersoTownKey____GeolocPriorityKey__0__PersoPostalCodeKey____PersoUrlGeoSCKey____ExpressSellerId____ExpressShopName____ExpressGlobalSellerId____ShowroomVendorId____RetailStoreName____VehicleId__0__AddressId____',
        'chcook7': 'direct',
        'AMCV_6A63EE6A54FA13E60A4C98A7%40AdobeOrg': '1585540135%7CMCIDTS%7C19533%7CMCMID%7C54514361572758946496794985570109274631%7CMCAID%7CNONE%7CMCOPTOUT-1676560875s%7CNONE%7CvVersion%7C4.4.0',
        'mssctse': 'W2dNXeEyrPI7vQSipcj0oZee3Bk6auOe_sRo7F4cs1YUHxgFjM-oF-vi3v4ry8jL3f4h3h_8iRw3RDVGjaO08Q',
        'svisit': '1',
        's_cc': 'true',
        '_$dtype': 't:d',
        'msswt': '',
        'visit_baleen_ACM-655d44': '9S4sww_skopGmQhr-I8Hqwm8IipCMttgAgdxOemJ5tvWe6m9dYR90n8I56YN7XGT4dDGtJA-cA3G8PKRjmcNb1Dx1oBcflNDZMIg-It8VNBynyNHo8C9rIj6Cn6MFrqcfHVk_W0kJ2NbRGy1Xz5miBZRHVwHrJsY569h0V6XT0572TNU9KSxHoBll9CGGPgs-VPaZxEdUZvUN-aC2hd3iTawzY1DxOKJlH4EC_81fWNgiyZSJrmeKQ27lDjcrdXOw8g3AQNb5E5RCkZBUwQzHRhznlactiu2rQj5j3QdmHHxA5mM7poitRtl0bwgCSex',
        'cache_cdn': '',
        '_$3custinf': 'AUT=0&XV1=0',
        'el2': '0',
        's_pv': 'L-242935%3ACuisini%C3%A8re%20%C3%A9lectrique',
        'tp': '14798',
        'msstvt': 'apEBX8keq086HQEjTe9RGvNYxLB_-1O1x4A2TBG919ovEPgd72jRgddCbF-Vxjc12XVGhYtUsvLkYd7Zl0WXvWqUpR0VNKYKJlx7_IiPZDeJA7t1l3h_OGO5BJrvDN0Blh5eiy8tNWR16qLbeHlfjA',
        'visit_baleen_ACM-655d43': 'XZwNzxbyzReZG0Zgt7wgXkxwynG6aB51PUhT0h1ybfxj5_b-XVrsdF-cUQ2HLE6m_n4OlUvAe7zPg8G1xlPJXCjlTWC7AqpqmXnAm34Es-sRtN0nbFpW6kEi5gQrP2dWEvXbwjCFzeHTwZZunVCJKMFyTQFEF8PoviXPNP3xroehc81G_azaPMztgb89cIpEqu8ycIlFpy-vp1RRW6jsKz4h5_4I0BID1z-mFWAD9I13fGd_2gK-I_u41y7JCN0jTkptdvJTst_MTcJ2jle96Q',
        'VisitContextCookie': 'R5-gHDaGc_ZuxFVSkPNVHVOaB6iqvvcp-OvGQFeTaGdisv8AlTn_tw',
        's_nr': '1687636136314-Repeat',
        's_ppv': 'L-242935%253ACuisini%25C3%25A8re%2520%25C3%25A9lectrique%2C2%2C2%2C350',
    }
    all_domain=['www.cdiscount.com']
    url_1 = "https://www.cdiscount.com/electromenager/four-cuisson/cuisinieres/cuisinieres-table-electrique/l-110230211.html"
    # url_1 = "https://www.cdiscount.com/electromenager/four-cuisson/cuisinieres/cuisinieres-table-electrique/l-110230211.html#_his_"
    def start_requests(self):
        yield FormRequest(url=self.url_1,headers=self.headers,callback=self.parse_page)
    def parse_page(self, response):
        open_in_browser(response)
        time.sleep(5)
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
from scrapy.cmdline import execute
execute('scrapy crawl Siemenitem1 -O Siemen1.csv'.split())

