import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

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
