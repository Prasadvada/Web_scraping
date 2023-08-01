import math
import pandas as pd
from playwright.sync_api import sync_playwright, expect
with sync_playwright() as sync_playwright_instance:
    browser = sync_playwright_instance.chromium.launch(headless=False,
                                                       channel='chrome',
                                                       proxy={
                                                           'server': 'x.botproxy.net:8080',
                                                           'username': f'pxu18829-0+US',
                                                           'password': 'z5uglHJthAcKOAqd0MUM'}
                                                       )
    context = browser.new_context(
        viewport={'width': 1280, 'height': 1024},
        accept_downloads=True,
        java_script_enabled=True,
        ignore_https_errors=True,
    )
    context.storage_state(path='../state.json')
    page = context.new_page()
    url = 'https://starr.tx.publicsearch.us/'
    page.goto(url)
    page.wait_for_load_state(timeout=30000)
    while True:
        try:
            expect(page.locator('//div[@class="search-masthead__seal-title"]')).to_contain_text('Official Records Search', timeout=80000)
            break
        except Exception as e:
            page.wait_for_timeout(2000)
    page.wait_for_timeout(2000)
    try:
        page.wait_for_load_state('networkidle', timeout=20000)
        page.wait_for_load_state('load', timeout=10000)
    except:
        pass
    page.locator('//input[@data-tip="Starting Recorded Date"]').fill('11/01/2021')
    page.wait_for_timeout(2000)
    page.locator('//input[@data-tip="Ending Recorded Date"]').fill('11/01/2021')
    page.wait_for_timeout(2000)
    page.locator('//button[@data-testid="searchSubmitButton"]').click(force=True,timeout=30000)
    page.wait_for_load_state(timeout=30000)
    page.wait_for_timeout(2000)
    records = page.locator('//p[@data-testid="resultsSummary"]').inner_text()
    print('records', records)
    m = records.split()[2]
    print(m)
    no_pages = math.ceil(int(m) // 50) + 1
    print(int(no_pages))
    sample_data = []
    for i in range(1, no_pages + 1):
        total_rows = page.query_selector_all('//*[@id="main-content"]/div[3]/div/div[2]/div[1]/table/tbody/tr')
        for r in range(1, int(len(total_rows)+1)):
            sample_dic = {}
            sample_dic["data"] = page.locator(
                f'//th[contains(text(),"Recorded Date")]/../../following-sibling::tbody/tr[{r}]/td[7]/span').inner_text()
            sample_dic["date"] = page.locator(
                f'//th[contains(text(),"Doc Number")]/../../following-sibling::tbody/tr[{r}]/td[8]/span').inner_text()
            sample_dic["grantor"] = page.locator(
                f'//th[contains(text(),"Grantor")]/../../following-sibling::tbody/tr[{r}]/td[4]/span').inner_text()
            sample_dic["grantee"] = page.locator(
                f'//th[contains(text(),"Grantee")]/../../following-sibling::tbody/tr[{r}]/td[5]/span').inner_text()
            sample_data.append(sample_dic)
        print("data", sample_data)
    df = pd.DataFrame(sample_data)
    print(df)
    df.to_dict()
    df.to_csv('data.csv', index=False, header=True)
    page.close()

