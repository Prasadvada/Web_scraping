import math
import re

from scrapy.http import HtmlResponse
from playwright.sync_api import sync_playwright, expect
with sync_playwright() as sync_playwright_instance:
    browser = sync_playwright_instance.chromium.launch(headless=False,
                                                      channel='chromium')
    context = browser.new_context(
        viewport={'width': 1280, 'height': 1024})
    page = context.new_page()
    c = 1
    while c <= 5:
        try:
            page.goto("https://www.mediamarkt.de/de/category/monitore-408.html?filter=currentprice:23-130",timeout=10000)
            page.wait_for_timeout(5000)
            break
        except:
            c += 1
    b=1
    while b <= 5:
        try:
            page.locator('(//*[contains(text(),"Alle zulassen")])[2]').click()
            page.wait_for_timeout(5000)
            break
        except:
            b += 1
            pass
    Clicking_button = page.locator('//*[text()="Mehr Produkte anzeigen"]').inner_text().strip()
    if 'Mehr Produkte anzeigen' in Clicking_button:
        y=page.locator('//span[@class="sc-3f2da4f5-0 hlwtYt"]').inner_text()
        tot_rec = int(re.findall(r"[\d]+", y)[0])
        m = math.ceil(tot_rec / 12)
        for i in range(1,m):
            print(i)
            page.locator('//*[text()="Mehr Produkte anzeigen"]').click(force=True,timeout=5000)
            page.wait_for_timeout(timeout=4000)
        response = HtmlResponse(url='https://www.example.com', body=page.content().encode('utf-8'))
        page.wait_for_timeout(5000)
        for j in range(1,tot_rec+1):
            title = response.xpath(f'(//p[@class="sc-3f2da4f5-0 fLePRG"]//text())[{j}]').get()
            print(title)

    else:
        response = HtmlResponse(url='https://www.example.com', body=page.content().encode('utf-8'))
        page.wait_for_timeout(5000)
        title = response.xpath('//p[@class="sc-3f2da4f5-0 fLePRG"]//text()').get()
        print(title)


    # with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
