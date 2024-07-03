from CustomLogger import LogGen
from Common import solve_recaptcha
import time
from playwright.sync_api import sync_playwright, expect
from tx_kent_a.DataExtractor import input_fields, details_extractor
import logging
def douglas_a():
    json_data = {"PADD": "", "APN": "", "ON": "ROBERTSON FAMILY TRUST"}
    job_id = "4"
    screenshot_path = f"D:\\Development\\Devlop\\Douglas\\Generaloutput\\Dodglous_a\\{job_id}\\"
    job_id_output_path = screenshot_path
    br_logger = LogGen.log_gen("Logs","Nv_douglas_a")
    br_logger.setLevel(logging.DEBUG)
    username = 'manashB'
    password = 'Oppo@#2021'
    with sync_playwright() as sync_playwright_instance:
        br_logger.info("Setting up Extraction Environment!")
        browser = sync_playwright_instance.chromium.launch(headless=False,
                                                           channel='chrome',
                                                           proxy={
                                                               'server': 'x.botproxy.net:8080',
                                                               'username': 'pxu18829-0+US+Session170622',
                                                               'password': 'z5uglHJthAcKOAqd0MUM'}
                                                           )
        context = browser.new_context(viewport={'width': 1280, 'height': 1024}, accept_downloads=True,
                                      java_script_enabled=True, ignore_https_errors=True,
                                      user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        url = "https://www.cdiscount.com/b-416938-les-ventes-tres-privees.html?"
        # url = "https://www.cdiscount.com/electromenager/four-cuisson/cuisinieres/cuisinieres-table-electrique/l-110230211.html/"
        br_logger.info("Nv_douglas_a County Appraiser Search Initiated!!")
        time.sleep(2)
        br_logger.info(f"Loading Nv_douglas_a Home Page; URL: {url}")
        while True:
            try:
                page.goto(url)
                page.wait_for_load_state(timeout=80000)
                page.wait_for_timeout(timeout=2000)
                break
            except Exception as e:
                page.wait_for_timeout(2000)
        recaptcha = _re(username, password, page)

        br_logger.info(f'Loaded Nv_douglas_a Home Page; URL: {url}')
        br_logger.info('Taking screenshot of Home Page; Filename: Home_Page.png\n')
        page.screenshot(path=f"{screenshot_path}Home_Page.png")
        input_fields(page, json_data, screenshot_path)
        br_logger.info(f'Loaded Nv_douglas_a Result Page; URL: {url}')
        br_logger.info(f'Result Page Title: {page.title()}')
        br_logger.info('Taking screenshot of Result Page, Filename: Result_Page.png\n')
        page.wait_for_timeout(timeout=3000)
        details_extractor(page, job_id, job_id_output_path, screenshot_path)



def _re(username, password, page):

    try:
        # site_key = page.locator("//div[contains(@class,'g-recaptcha center')]").get_attribute('data-sitekey', timeout=20000)
        site_key = page.locator('//div[@class="g-recaptcha"]').get_attribute('data-sitekey', timeout=20000)
        print("Recaptcha appeared on Search!!")
        url = page.url
        recaptcha_response = solve_recaptcha(username, password, site_key, url)
        page.evaluate(f"document.getElementById('g-recaptcha-response').innerHTML = `{recaptcha_response['text']}`")
        page.evaluate(f"onReturnRecaptchaCallback();")
        page.wait_for_timeout(2000)
        count = 1
        while True:
            if count <= 5:
                # page.frame_locator("//div[contains(@class,'g-recaptcha center')]/div/div/iframe").locator("(//div[contains(@class,'recaptcha-checkbox-border')])[1]").click()
                # page.frame_locator("//div[6]/div[4]/iframe").locator("//button[contains(@class,'rc-button-default goog-inline-block')]").click()

                page.locator('id=submitDisclaimerAccept').click(timeout=10000)
                try:
                    expect(
                        page.locator("//li[contains(@class,'ui-li-divider ui-bar-a ui-first-child')]")).to_contain_text(
                        'Home Instructions', timeout=20000)
                    return "Recaptcha Solved Successfully!!"
                except Exception as e:
                    count = count + 1
            else:
                print('Failed to Solve Recaptcha, even with 5 attempts!!')

    except Exception as e:
        print('Recaptcha Not found\n')

if __name__ == "__main__":
    douglas_a()