import os
import csv
import re
import pandas as pd
from scrapy.http import HtmlResponse
class TableData:
    def __init__(self):
        self.output = f"Kissan.csv"
        if not os.path.exists(self.output):
            with open(self.output, "w", newline="") as wd:
                wr = csv.writer(wd)
                wr.writerow(['Title', 'json_url', 'Download_number', 'Published_Date', 'Updated_Date'])
                wd.close()

    def data_extractor(self, response, total_rows, page):
        response = HtmlResponse(url='https://www.example.com', body=page.content().encode('utf-8'))
        for j in range(1, total_rows + 1):
            print("row:",j)
            try:
                Title = response.xpath(f'(//h3/a/text())[{j}]').get(default="").strip()
                print(Title)
                json_url = ''
                try:
                    json_Title = response.xpath(f'(//h3/a/text())[{j}]').get(default="").strip()
                    if re.search("from\s+([\w\s]+)(?:\sdistrict)", json_Title, flags=re.I):
                        Dist = re.search("from\s+([\w\s]+)(?:\sdistrict)", json_Title, flags=re.I).group(1)
                    else:
                        Dist = ""
                    Dist = Dist
                    Mont = json_Title.split("month of")[1].split()[0]
                    year = json_Title.split("month of")[1].split()[1]
                    District = Dist.upper().replace('AHMEDABAD', '0401').replace("AHMADABAD", "0401").replace('AMRELI',
                                                                                                              '0413').replace(
                        'ANAND', '0425').replace('ARAVALLI', '0421').replace('BANASKANTHA', '0402').replace(
                        'BANAS KANTHA', '0402').replace('BHARUCH', '0404').replace('BHAVNAGAR', '0414').replace('BOTAD',
                                                                                                                '0423').replace(
                        'CHHOTA UDAIPUR', '0429').replace('DAHOD', '0424').replace('DOHAD', '0424').replace('DANG',
                                                                                                            '0406').replace(
                        'DEVBHOOMI DWARKA', '0430').replace('GANDHINAGAR', '0407').replace('GIR SOMNATH',
                                                                                           '0433').replace('JAMNAGAR',
                                                                                                           '0415').replace(
                        'JUNAGADH', '0416').replace('KUTCH', '0417').replace('KACHCHH', '0417').replace('KHEDA',
                                                                                                        '0408').replace(
                        'MAHISAGAR', '0431').replace('MEHSANA', '0409').replace('MAHESANA', '0409').replace('MORBI',
                                                                                                            '0432').replace(
                        'NARMADA', '0428').replace('NAVSARI', '0422').replace('PANCHMAHAL', '0410').replace(
                        'PANCH MAHALS', '0410').replace('PATAN', '0427').replace('PORBANDAR', '0426').replace('RAJKOT',
                                                                                                              '0418').replace(
                        'SABARKANTHA', '0411').replace('SURAT', '0412').replace('SURENDRANAGAR', '0419').replace('TAPI',
                                                                                                                 '0420').replace(
                        'VADODARA', '0403').replace('VALSAD', '0405')
                    Month = Mont.upper().replace('JANUARY', '01').replace('FEBRUARY', '02').replace('MARCH',
                                                                                                    '03').replace(
                        'APRIL', '04').replace('MAY', '05').replace('JUNE', '06').replace('JULY', '07').replace(
                        'AUGUST', '08').replace('SEPTEMBER', '09').replace('OCTOBER', '10').replace('NOVEMBER',
                                                                                                    '11').replace(
                        'DECEMBER', '12')
                    year = year
                    json_url = f'http://dackkms.gov.in/Account/API/kKMS_QueryData.aspx?StateCD=04&DistrictCd={District}&Month={Month}&Year={year}'
                except:
                    pass

                Download_number = response.xpath(
                    f'(//span[contains(text(),"Download:")]/following-sibling::strong/text())[{j}]').get(
                    default="").strip()
                Published_Date = response.xpath(
                    f'(//span[1][contains(text(),"Published:")]/following-sibling::strong/text())[{j}]').get(
                    default="").strip()
                Updated_Date = response.xpath(
                    f'(//span[1][contains(text(),"Updated:")]/following-sibling::strong/text())[{j}]').get(
                    default="").strip()

                alldata = [Title, json_url, Download_number, Published_Date, Updated_Date]
                with open(self.output, "a", newline="") as wd:
                    wr = csv.writer(wd)
                    # print(alldata)
                    wr.writerow(alldata)
                    wd.close()
                df = pd.read_csv(self.output, index_col=False)
                df.drop_duplicates(subset=["Title"], keep='first', inplace=True)
                df.to_csv(self.output, index=False)
            except:
                pass
