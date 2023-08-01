import scrapy
class flipkartSpider(scrapy.Spider):
    name = "flipkart"
    start_urls = ['https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=RECENT&suggestionId=laptop%7CLaptops&requestId=7ec220e8-4f02-4150-9e0b-9e90cf692f4b&as-searchtext=laptop']

    def parse(self, response):
        total = response.css('._2kHMtA')
        for i in total:
            price = i.css('._1_WHN1::text').get()
            print(price)
            title = i.css('._4rR01T::text').get()
            yield {
                "prices": price,
                "title_name": title
            }
        next_btn = response.xpath('//span[contains(text(),"Next")]/../@href').get()
        print(next_btn)
        if next_btn is not None:
            yield response.follow(next_btn, self.parse)
