import csv
import os
class DataExtractor:
    def __init__(self, response1,r):
        self.outname = None
        self.rec_information(response1,r)
    def rec_information(self, response1,r):
        self.outname = f"NAPAN_GENERAL_OUTPUT_1.csv"
        if not os.path.exists(self.outname):
            with open(self.outname, "w", newline="") as wd:
                wr = csv.writer(wd)
                wr.writerow(['Team_Name', 'year', 'wins','losses'])

        Team_Name = response1.xpath(
            f'//*[@id="hockey"]/div/table/tbody/tr[position()>1][{r}]/td[1]/text()').get(default='').strip()

        year = response1.xpath(
            f'//*[@id="hockey"]/div/table/tbody/tr[position()>1][{r}]/td[2]/text()').get(default='').split('-')[0].strip()

        wins = response1.xpath(f'//*[@id="hockey"]/div/table/tbody/tr[position()>1][{r}]/td[3]/text()').get(default='').strip()
        losses = response1.xpath(f'//*[@id="hockey"]/div/table/tbody/tr[position()>1][{r}]/td[4]/text()').get(default='').strip()

        alldata = [i.strip('|') for i in [Team_Name, year, wins,losses]]

        with open(self.outname, "a", newline="") as wd:
            wr = csv.writer(wd)
            print(f'["ALLResponse"]>>>{alldata}')
            wr.writerow(alldata)
            wd.close()
