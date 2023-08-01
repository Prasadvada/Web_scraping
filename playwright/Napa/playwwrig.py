import csv
import re, math
import time
from scrapy.http import HtmlResponse
from  DataExtraction import *
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from playwright.sync_api import sync_playwright, expect
jobid = '1'
outname = f"{jobid}_OUTPUT.csv"
def butler_extractor():

    def data_extractor(afn_no):
        with sync_playwright() as sync_playwright_instance:
            browser = sync_playwright_instance.firefox.launch(headless=True,
                                                               channel='firefox'

                                                               )
            context = browser.new_context(
                # storage_state='trumbull_state.json',
                viewport={'width': 1280, 'height': 1024},
                accept_downloads=True,
                java_script_enabled=True,
                ignore_https_errors=True,
            )
            context.storage_state(path='../state.json')
            page1 = context.new_page()
            page1.goto(afn_no)
            try:
                page1.wait_for_load_state('networkidle', timeout=20000)
                page1.wait_for_load_state('load', timeout=10000)
            except:
                pass
            while True:
                try:
                    expect(page1.locator('//div[2]/div/div/div[3]/geo-utilities-nav/div/div[1]/geo-proservices-link/div/a')).to_contain_text(
                        'Pro Services', timeout=80000)
                    break
                except Exception as e:
                    page1.wait_for_timeout(2000)
            page1.wait_for_timeout(2000)
            time.sleep(2)
            try:
                page1.wait_for_load_state('networkidle',timeout=20000)
                page1.wait_for_load_state('load', timeout=10000)
            except:
                pass
            total_row = page1.query_selector_all('//div[@class="geo-search-results-collections"]//geo-product-list-item')
            total_rows = (len(total_row))
            print(total_rows)
            page1.wait_for_timeout(3000)
            page1.wait_for_timeout(3000)
            for r in range(1,total_rows + 1):
                response2 = HtmlResponse(url='https://www.example.com',
                                         body=page1.content().encode('utf-8'))
                DataExtractor(response2,r)
            time.sleep(3)
            page1.close()
    def download_data():
        try:
            with sync_playwright() as sync_playwright_instance:
                browser = sync_playwright_instance.firefox.launch(headless=True,
                                                                   channel='firefox'
                                                                   )
                context = browser.new_context(viewport={'width': 1280, 'height': 1024},
                                              accept_downloads=True,ignore_https_errors=True)
                context.storage_state(path='../state.json')
                page = context.new_page()
                url = 'https://www.napaonline.com/en/search?text=grote&referer=v2'
                page.goto(url)
                page.wait_for_load_state()
                page.wait_for_load_state('load', timeout=10000)
                while True:
                    try:
                        expect(page.locator('//div[2]/div/div/div[3]/geo-utilities-nav/div/div[1]/geo-proservices-link/div/a')).to_contain_text(
                            'Pro Services', timeout=80000)
                        break
                    except Exception as e:
                        page.wait_for_timeout(2000)
                page.wait_for_timeout(1000)
                time.sleep(2)
                page.wait_for_load_state('load', timeout=80000)
                tot_rec_str = page.locator('//*[@id="geo-heading"]/b[1]').inner_text(timeout=20000)
                tot_rec = int(re.findall(r"[\d]+", tot_rec_str)[0])
                m= math.ceil(tot_rec/24)
                try:
                    page.locator('//div/div[2]/div[6]/geo-search-results/div/geo-pagination-links/div/nav/div[1]/div[3]/div[1]/a/div').click()
                except:
                    pass
                l=[]
                for i in range(1):
                    try:
                        pages = page.locator(f'//div[@class="geo-page-numbers"]//a[1]').get_attribute('href')
                        print(pages)
                        l.append(pages)
                    except:
                        pass
                for j in range(2,m+1):
                # for j in range(2,3):
                    y=(f'https://www.napaonline.com/en/search?text=grote&referer=v2&page={j}')
                    l.append(y)
                print(len(l))
                page.close()
                process_doc_list = []
                for doc_val in l:
                    print(doc_val)
                    process_doc_list.append(doc_val)
                with ThreadPoolExecutor(max_workers=5) as exe:
                    exe.map(data_extractor, process_doc_list)
        except:
            pass
    download_data()
if __name__ == "__main__":
    butler_extractor()


