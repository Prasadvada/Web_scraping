import csv
import os
import pandas as pd
class DataExtractor:
    def __init__(self, data):
        self.outname = None
        self.rec_information(data)
    def rec_information(self, data):
        # global title, pid, brand, sale_price, primary_image,thumb_image,url,description
        self.outname = f"NAPAN_GENERAL_OUTPUT.csv"
        if not os.path.exists(self.outname):
            with open(self.outname, "w", newline="") as wd:
                wr = csv.writer(wd)
                wr.writerow(['pid', 'title', 'brand','sale_price','primary_image','thumb_image','url','description'])
                wd.close()

        allsales_data = []
        for item in data['response']['docs']:
            pid = item.get('pid')
            title = item.get('title')
            brand = item.get('brand')
            sale_price = item.get('sale_price')
            primary_image = item.get('primary_image')
            thumb_image = item.get('thumb_image')
            url = item.get('url')
            description = item.get('description')
            alldata = [pid, title, brand,sale_price,primary_image,thumb_image,url,description]
            allsales_data.append(alldata)
            with open(self.outname, "a", newline="") as wd:
                wr = csv.writer(wd)
                # print(f'["ALLResponse"]>>>{alldata}')
                wr.writerow(alldata)
                wd.close()
            # df = pd.read_csv(self.outname, index_col=False,encoding='ISO 8859-1')
            # df.drop_duplicates(subset=["url"], keep='first', inplace=True)
            # df.to_csv(self.outname, index=False)
