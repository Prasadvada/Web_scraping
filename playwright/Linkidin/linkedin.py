import pandas as pd
from playwright.sync_api import sync_playwright, expect
from scrapy.http import HtmlResponse
from linkidin_data import *

sample_data = []
def Data_extractor():
    job_id ='1'
    job_id_output_path =f"C:/Users/laksh\OneDrive/Desktop/playwright/Playwright/General_output/{job_id}"
    try:
        with sync_playwright() as sync_playwright_instance:
            browser = sync_playwright_instance.firefox.launch(headless=False,
                                                               channel='firefox'
                                                               )
            context = browser.new_context(viewport={'width': 1280, 'height': 1024},
                                          accept_downloads=True,ignore_https_errors=True)
            context.storage_state(path='../state.json')
            page = context.new_page()
            url = 'https://www.linkedin.com/jobs/search/?currentJobId=3625879950&distance=25&f_T=25206&geoId=103644278&keywords=machine%20learning'
            while True:
                try:
                    page.goto(url)
                    expect(page.locator('//a[@class="nav__button-tertiary btn-md btn-tertiary"]')).to_contain_text('Join now')
                    break
                except Exception as e:
                    page.wait_for_timeout(2000)
            page.wait_for_load_state()
            try:
                page.locator('(//button[@data-tracking-control-name="public_jobs_f_PP"])[1]').click(force=True,timeout=30000)
                page.locator('//input[@id="f_PP"]').click(force=True,timeout=30000)
                page.locator('//input[@id="f_PP-0"]').click(force=True,timeout=30000)
                page.locator('//input[@id="f_PP"]/../following-sibling::div/following-sibling::button').dblclick(force=True,timeout=30000)
                page.wait_for_timeout(2000)
            except:
                pass
            try:
                expect(page.locator('//a[@class="nav__button-tertiary btn-md btn-tertiary"]')).to_contain_text('Join now')
            except Exception as e:
                print(e)
            for i in range(1,1000):
                print("Cliking of record:",i)
                page.locator(f'//main/section[2]/ul//li[{i}]').click(force=True,timeout=30000)
                page.wait_for_load_state()
                page.wait_for_timeout(2000)
                try:
                    page.locator('//button[@aria-label="See more jobs"]').click(force=True, timeout=30000)
                    page.wait_for_load_state()
                    page.wait_for_timeout(5000)
                except:
                    pass
                DetailsData(page,job_id, i, "Mechinelearning", job_id_output_path)
    except Exception as e:
        print(e)
        pass
if __name__ == "__main__":
    Data_extractor()
    print('completed')


