import re
import math
from playwright.sync_api import sync_playwright, expect
from kissan_ply.Data_extraction import TableData
from scrapy.http import HtmlResponse

def kissan_ply():
    type = "S"
    url_retry = 1
    with sync_playwright() as playwright_instance:
        browser = playwright_instance.chromium.launch(headless=False,
                                                      channel='chrome')
        context = browser.new_context(no_viewport=False, accept_downloads=True, ignore_https_errors=True,
                                      java_script_enabled=True, bypass_csp=True)
        context.storage_state(path='state.json')
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        url = 'https://data.gov.in/datasets_webservices/datasets/6622307'
        while True:
            try:
                page.goto(url, wait_until='load', timeout=50000)
                break
            except (Exception,) as e:
                if url_retry == 5:
                    break
                url_retry += 1
        page.wait_for_timeout(timeout=4000)
        page.wait_for_load_state('load', timeout=30000)
        try:
            page.locator('id=input-valid').fill('Gujarat')
            page.wait_for_timeout(timeout=3000)
            page.wait_for_load_state('load', timeout=30000)
        except Exception as e:
            pass
        page.locator('id=input-valid').press('Enter')
        page.wait_for_timeout(timeout=5000)
        tot_rec_str = page.locator('//div[@class="page-result"]').inner_text().replace(',', '')
        try:
            tot_rec = int(re.findall(r"[\d]+", tot_rec_str)[-1])
        except:
            tot_rec = 1
        total_pages = math.ceil(tot_rec / 8)
        print(total_pages)
        page.wait_for_load_state('load', timeout=10000)
        current_page_number = 1
        for i in range(1, total_pages + 1):
            print("page:",i)
            try:
                page.wait_for_timeout(3000)
                total_rows = page.query_selector_all('//h3/a')
                print(len(total_rows))
                response = HtmlResponse(url='https://www.example.com', body=page.content().encode('utf-8'))
                extract = TableData()
                extract.data_extractor(response, len(total_rows), page)
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(timeout=1000)
                page.wait_for_timeout(timeout=1000)
                try:
                    try:
                        symbol = '›'
                        page.evaluate('''(symbol) => {
                                   const buttons = Array.from(document.querySelectorAll('button'));
                                   const button = buttons.find(btn => btn.innerText.includes(symbol));
                                   button.click();
                               }''', symbol)
                        page.wait_for_timeout(6000)
                    except:
                        print(f"Not clicking Page_{i}")
                    page.wait_for_load_state()
                    page.wait_for_timeout(1000)
                    page.wait_for_load_state()
                    current_page_number += 1
                    while True:
                        try:
                            expect(page.locator('//span[contains(text(),"Filter By")]')).to_have_text("Filter By",timeout=30000)
                            break
                        except:
                            pass
                    page.wait_for_load_state()

                except Exception as e:
                    pass
            except Exception as e:
                pass


if __name__ == "__main__":
    kissan_ply()
