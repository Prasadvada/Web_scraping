import pandas as pd
import time
import os, csv, re, json
from scrapy.http import HtmlResponse

class DetailsData:
    JOBID = ""
    parcel_id = ""
    property_address = ""
    property_use_code = ""
    owner_name = ""
    legal_description = ""
    sales_filepath = ""

    def __init__(self,page,job_id, i, file_name, job_id_output_path):
        self.path = job_id_output_path
        self.file_name = file_name
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.JOBID = job_id
        self.property_data(page,job_id, i, file_name, job_id_output_path)
        time.sleep(2)
    def property_data(self,page,job_id, i, file_name, job_id_output_path):
        try:
            self.outname = self.path + f"\\{self.file_name}_Data.csv"
            if not os.path.exists(self.outname):
                with open(self.outname, "w", newline="") as wd:
                    wr = csv.writer(wd)
                    wr.writerow(['job_title', 'Company_Name', 'Job_Location', 'Job_Description'])
                wd.close()
            job_title, Company_Name, Job_Location = '', '', ''
            try:
                job_title = page.locator(
                    f'(//div[@class="base-search-card__info"]//h3[@class="base-search-card__title"])[{i}]').inner_text()
                Company_Name = page.locator(
                    f'(//div[@class="base-search-card__info"]//h4[@class="base-search-card__subtitle"])[{i}]/a').inner_text()
                Job_Location = page.locator(f'(//span[@class="job-search-card__location"])[{i}]').inner_text()
            except:
                pass
            print(job_title)
            Job_Description = ''
            try:
                page.locator('//button[@aria-label="Show more, visually expands previously read content above"]').click(
                    force=True, timeout=30000)
                page.wait_for_load_state()
                page.wait_for_timeout(1000)
                response = HtmlResponse(url='https://www.example.com', body=page.content().encode('utf-8'))
                Job_Description = ' '.join([j.strip() for j in response.xpath(
                    f'//div[@class="show-more-less-html__markup relative overflow-hidden"]/text()|//div[@class="show-more-less-html__markup relative overflow-hidden"]/strong/text()|//div[@class="show-more-less-html__markup relative overflow-hidden"]/ul/li/text()').getall()
                                            if j.strip() != ''])
            except:
                pass
            alldata = [job_title, Company_Name, Job_Location, Job_Description]
            with open(self.outname, "a", newline="") as wd:
                wr = csv.writer(wd)
                print(f'["ALLDATA"]>>>{alldata}')
                wr.writerow(alldata)
                wd.close()
            df = pd.read_csv(self.outname, index_col=False)
            df.drop_duplicates(subset=["Job_Description"], keep='first', inplace=True)
            df.to_csv(self.outname, index=False)
        except:
            pass


