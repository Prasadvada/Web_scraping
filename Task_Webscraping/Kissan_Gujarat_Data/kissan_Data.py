import csv
import os
from datetime import datetime
class DataExtractor:
    def __init__(self, data):
        self.outname = None
        self.rec_information(data)
    def rec_information(self, data):
        self.outname = f"kissan Gujarat data.csv"
        if not os.path.exists(self.outname):
            with open(self.outname, "w", newline="") as wd:
                wr = csv.writer(wd)
                wr.writerow(
                    ['Title', 'Json_url', 'Download_Number', 'published_date', 'updated_date']
                )
                wd.close()
        rows = data['data']['rows']
        allsales_data = []
        for row in rows:
            Title=''
            try:
                Title = row['title'][0]
            except:
                pass
            Json_url=''
            try:
                Json_url = row['datafile_url'][0]
            except:
                pass
            published_date=''
            try:
                published_timestamp = row['published_date'][0]
                published_date = datetime.fromtimestamp(published_timestamp).strftime('%d/%m/%Y')
            except:
                pass
            updated_date=''
            try:
                updated_timestamp = row['changed'][0]
                updated_date = datetime.fromtimestamp(updated_timestamp).strftime('%d/%m/%Y')
            except:
                pass
            Download_Number=''
            try:
                Download_Number = row['download_count'][0]
                if Download_Number == '':
                    Download_Number=0
                else:
                    pass
            except:
                pass
            alldata = [Title,Json_url,Download_Number, published_date, updated_date]
            allsales_data.append(alldata)
            with open(self.outname, "a", newline="") as wd:
                wr = csv.writer(wd)
                wr.writerow(alldata)
                wd.close()
