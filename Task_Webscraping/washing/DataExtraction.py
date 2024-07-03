import csv
import os
import pandas as pd
class DataExtractor:
    def __init__(self, data):
        self.outname = None
        self.rec_information(data)
    def rec_information(self, data):
        self.outname = f"Washing_data.csv"
        if not os.path.exists(self.outname):
            with open(self.outname, "w", newline="") as wd:
                wr = csv.writer(wd)
                wr.writerow(['Name', 'Web_Code', 'Review'])
                wd.close()
        allsales_data = []
        total_row = len(data.xpath('//div[@class="widget-ArticleList-article referenced"]'))
        print("Total:",total_row)
        for i in range(1, total_row + 1):
            try:
                Name = data.xpath(
                    f'(//div[@data-subwidget-id="0fd53e6f-c783-4aa7-84bc-877e37cf1f6d"])[{i}]/text()').get(
                    default='').strip()
                Web_Code = data.xpath(
                    f'(//span[contains(text(),"Web-Code:")]/following-sibling::span/text())[{i}]').get(
                    default='').strip()
                print(Web_Code)
                Review = ''
                try:
                    Review_1 = data.xpath(f'(//*[@class="ratings"])[{i}]/text()|(//div[@class="bv_averageRating_component_container"]/div/text())[{i}]').get(default='').strip()
                    Review= Review_1.split()[0]
                except:
                    pass
                alldata = [Name, Web_Code, Review]
                allsales_data.append(alldata)
                with open(self.outname, "a", newline="") as wd:
                    wr = csv.writer(wd)
                    print(f'["ALLResponse"]>>>{alldata}')
                    wr.writerow(alldata)
                    wd.close()
            except:
                pass