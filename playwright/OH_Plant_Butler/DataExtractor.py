import csv
import os
import re
from common import *
from sqlalchemy import select, insert, update
from models import oh_butler_database_tables

TrumbullRecorder, TrumbullStatus, sessionLocal = oh_butler_database_tables()
local_session = sessionLocal()

class DataExtractor:
    # JOBID = ""

    def __init__(self, response1, afn_num, download_folder, jobid,response2):
        self.outname = None
        self.doc_num = afn_num
        self.jobid = jobid
        self.download_folder = download_folder
        self.rec_information(response1,response2)
    def rec_information(self, response1,response2):
        self.outname = f"{self.jobid}_OUTPUT.csv"

        if not os.path.exists(self.outname):
            with open(self.outname, "w", newline="") as wd:
                wr = csv.writer(wd)
                wr.writerow(["Instrument Status", "Document Type", "Document Number", "Book Type", "Recording Date", "Grantor", "Grantee", "Legal Desciption",
                             "Long Desciption", "Document Pages", "Signature Pages", "Book", "Page",  "Consideration", "Related Doc"])

        instrument_status = response1.xpath(
            '//span[contains(text(),"Instrument Status")]/../following-sibling::td[1]/text()').get(default='').split('-')[0].strip()

        document_type = response1.xpath(
            '//span[contains(text(),"Instrument Type")]/../following-sibling::td[1]/text()').get(default='').split('-')[0].strip()

        document_number = response1.xpath(
            '//span[contains(text(),"Instrument Number")]/../following-sibling::td[1]/text()[1]').get(
            default='').replace('-', '').strip()

        book_type = response1.xpath(
            '//span[contains(text(),"Book Type")]/../following-sibling::td[1]/text()').get(default='').split('-')[
            0].strip()

        recording_date = response1.xpath(
            '//span[contains(text(),"Recorded Date")]/../following-sibling::td[1]/text()').get(
            default='').strip()

        legal_des = ' | '.join([i.strip() for i in response2.xpath(
            '//*[@id="data"]/table[4]/tbody/tr/td[3]/text()').getall() if i.strip() != ""])

        long_desc = response2.xpath(
            '//*[@id="data"]/table[8]/tbody/tr/td[3]/text()|'
            '//*[contains(text(), "Long Description")]/ancestor::table[2]/following-sibling::table/tbody/tr/td[3]/text()').get(
            default='').strip()

        document_pages = response1.xpath(
            '//span[contains(text(),"Document Page")]/../following-sibling::td[1]/text()').get(
            default='').strip()

        signature_pages = response1.xpath(
            '//span[contains(text(),"Signature Page")]/../following-sibling::td[1]/text()').get(
            default='').strip()

        book = response1.xpath(
            '//span[contains(text(),"Book")]/../following-sibling::td[1]/text()').get(
            default='').strip()

        page = response1.xpath('//span[text()="Page:"]/../following-sibling::td[1]/text()').get(
            default='').strip()

        consideration = response1.xpath('//span[contains(text(),"Consideration")]/../following-sibling::td[1]/text()').get(
            default='').strip()

        grantor = ' | '.join([i.strip() for i in response1.xpath(
            '//span[contains(text(),"Grantor")]/../../../../../'
            'following-sibling::table[1]/tbody/tr/td/table/tbody/tr/td/text()').getall() if i.strip() != ""]).replace(
            '\n', '')

        grantee = ' | '.join([i.strip() for i in response1.xpath(
            '//span[contains(text(),"Grantee")]/../../../../../'
            'following-sibling::table[1]/tbody/tr/td/table/tbody/tr/td/text()').getall() if i.strip() != ""]).replace(
            '\n', '')

        related_doc = " | ".join([i.strip() for i in response1.xpath(
            '//html/body/form/div[2]/div/table[11]/tbody/tr/td[1]/a/text()|'
            '//html/body/form/div[2]/div/table[11]/tbody/tr/td[2]/text()|'
            '//html/body/form/div[2]/div/table[11]/tbody/tr/td[3]/text()|'
            '//html/body/form/div[2]/div/table[11]/tbody/tr/td[4]/text()').getall() if i.strip() != ""])

        alldata = [i.strip('|') for i in [instrument_status, document_type, document_number, book_type, recording_date, grantor, grantee,
                                          legal_des, long_desc, document_pages, signature_pages, book, page, consideration, related_doc]]

        with open(self.outname, "a", newline="") as wd:
            wr = csv.writer(wd)
            print(f'["ALLResponse"]>>>{alldata}')
            wr.writerow(alldata)
            wd.close()
