import logging
import math
import re
import sys
import time
import usaddress
import json
from scrapy.http import HtmlResponse
from playwright.sync_api import sync_playwright, expect
from concurrent.futures import ProcessPoolExecutor
from .DetailExtractor import DetailsData

executor = ProcessPoolExecutor(max_workers=2)

br_logger = logging.getLogger()


def input_fields(page, json_data, screenshot_path):
    add_dic = {}
    street_json = json.loads(open('D:\\Development\\Devlop\\Douglas\\direction_json.json',
             "r").read())

    dir_json = json.loads(open('D:\\Development\\Devlop\\Douglas\\street_json.json',
             "r").read())

    if json_data["ON"] != "":
        page.wait_for_timeout(timeout=2000)
        names_1 = json_data["ON"]
        names = json_data["ON"].split()
        name = len(names)
        if name == 3:
            name = names_1.replace(' ',', ', 1)
            page.wait_for_timeout(timeout=2000)
            page.locator('//h3[contains(text(),"Search Parcel Records")]//following-sibling::form/input').fill(name)
            page.wait_for_timeout(timeout=2000)
            page.locator('//*[@id="tab-search-quick"]/h1').click()
            page.wait_for_timeout(timeout=2000)

        elif name == 2:
            name = names_1.replace(" ", ", ", 1)
            page.wait_for_timeout(timeout=2000)
            page.locator('//h3[contains(text(),"Search Parcel Records")]//following-sibling::form/input').fill(name)
            page.wait_for_timeout(timeout=2000)
            page.locator('//*[@id="tab-search-quick"]/h1').click()
            page.wait_for_timeout(timeout=1000)

        elif name == 1:
            page.wait_for_timeout(timeout=2000)
            name = names_1
            page.locator('//h3[contains(text(),"Search Parcel Records")]//following-sibling::form/input').fill(name)
            page.wait_for_timeout(timeout=1000)
            page.locator('//*[@id="tab-search-quick"]/h1').click()
            page.wait_for_timeout(timeout=1000)

        elif name>3:
            name = names_1.replace(' ', ', ', 1)
            page.wait_for_timeout(timeout=2000)
            page.locator('//h3[contains(text(),"Search Parcel Records")]//following-sibling::form/input').fill(name)
            page.wait_for_timeout(timeout=2000)
            page.locator('//*[@id="tab-search-quick"]/h1').click()
            page.wait_for_timeout(timeout=2000)
        page.screenshot(path=f"{screenshot_path}Search_Parameters.png")
        page.wait_for_timeout(4000)
        page.locator('(//*[@stroke-linecap="round"])[3]').click(force=True)
        page.wait_for_timeout(timeout=5000)
        try:
            expect(page.locator('//p[contains(text(),"None")]').nth(0)).to_have_text("None", timeout=2000)
            page.wait_for_timeout(timeout=2000)
            page.locator('//h3[contains(text(),"Search Parcel Records")]//following-sibling::form/input').fill(names_1)
            page.wait_for_timeout(timeout=2000)
            page.locator('//*[@id="tab-search-quick"]/h1').click()
            page.wait_for_timeout(timeout=2000)
            page.screenshot(path=f"{screenshot_path}Search_Parameters.png")
            page.wait_for_timeout(timeout=3000)
            page.locator('(//*[@stroke-linecap="round"])[3]').click(timeout=4000)
            page.wait_for_timeout(timeout=3000)
        except AssertionError:
            pass
        br_logger.info(f"Owner Name Search Initiated with the Owner Name: {json_data['ON']}")

    elif json_data["APN"] != "":
        page.wait_for_timeout(timeout=2000)
        names_1 = json_data["APN"]
        page.wait_for_timeout(timeout=2000)
        page.locator('//h3[contains(text(),"Search Parcel Records")]//following-sibling::form/input').fill(names_1)
        page.wait_for_timeout(timeout=2000)
        page.locator('//*[@id="tab-search-quick"]/h1').click()
        page.screenshot(path=f"{screenshot_path}Search_Parameters.png")
        page.wait_for_timeout(timeout=3000)
        page.locator('(//*[@stroke-linecap="round"])[3]').click(timeout=4000)
        page.wait_for_timeout(timeout=3000)
        br_logger.info(f"APN Search Initiated with the APN: {json_data['APN']}")

    elif json_data["PADD"] != "":
        add_initial = usaddress.parse(json_data["PADD"])
        for value, key in add_initial:
            add_dic[key] = add_dic.get(key, "") + value + " "
        for key, value in street_json.items():
            if value in add_dic.get("StreetNamePostType", ""):
                add_dic["StreetNamePostType"] = key
                break
        for key, value in dir_json.items():
            if value in add_dic.get("StreetNamePreDirectional", ""):
                add_dic["StreetNamePreDirectional"] = key
                break
        address = add_dic.get("AddressNumber", "") + add_dic.get("StreetNamePreDirectional", "") + add_dic.get(
            "StreetName", "") + add_dic.get("StreetNamePostType", "")
        address = address.replace(","," ")
        page.wait_for_timeout(timeout=2000)
        page.locator('//h3[contains(text(),"Search Parcel Records")]//following-sibling::form/input').fill(address)

        page.wait_for_timeout(timeout=2000)
        page.locator('//*[@id="tab-search-quick"]/h1').click()
        page.wait_for_timeout(timeout=3000)
        page.screenshot(path=f"{screenshot_path}Search_Parameters.png")
        page.wait_for_timeout(timeout=3000)
        page.locator('(//*[@stroke-linecap="round"])[3]').click(timeout=4000)
        page.wait_for_timeout(timeout=3000)
        br_logger.info(f"PADD Search Initiated with the ADD: {json_data['PADD']}")

    br_logger.info('Taking screenshot of Search Parameters, Filename: Search_Parameters.png\n')

    try:
        expect(page.locator('//p[contains(text(),"None")]').nth(0)).to_have_text("None", timeout=2000)
        br_logger.info(f"Result not found for the Search Criteria!!")
        page.screenshot(path=f"{screenshot_path}No Result_Page.png")
        sys.exit()
    except AssertionError:
        try:
            expect(page.locator('//h3[contains(text(),"Parcel Search Results")]').nth(0)).to_have_text("Parcel Search Results", timeout=2000)
        except:
            pass

def details_extractor(page, job_id, job_id_output_path,screenshot_path):
    try:
        try:
            record = page.locator('//h3[contains(text(),"Parcel Search Results")]/following-sibling::div').inner_text()
        except:
            record_1 = page.query_selector_all('//*[@class="title"]//h1')
            rec = len(record_1)
            record = str(rec)
        records = int(re.findall(r"[\d]+", record)[0])
        br_logger.info(f'Total Records Found per search - {records}!')
        br_logger.info(f"Search Successful!")
        page.wait_for_timeout(timeout=1000)
        total_pages = math.ceil(records / 60)
        try:
            for each_page in range(1, total_pages + 1):
                total_rows = page.query_selector_all('//*[@id="tab-search-quick"]/div[3]/table/tbody/tr|//*[@class="title"]//h1')
                print(len(total_rows))
                br_logger.info(f'Records Found per page - {len(total_rows)}')
                page.screenshot(path=f"{screenshot_path}\\Result_page_{each_page}.png", full_page=True)
                page.wait_for_timeout(timeout=2000)
                try:
                    for i in range(1,len(total_rows)+1):
                        print("row:", i)
                        try:
                            page.locator(f'//*[@id="tab-search-quick"]/div[3]/table/tbody/tr[{i}]/td/a').click(timeout=5000)
                            page.wait_for_timeout(timeout=6000)
                        except:
                            pass
                        page.wait_for_timeout(timeout=2000)
                        try:
                            expect(page.locator('//div[@class="parcel-detail"]//h3[1]')).to_have_text("Owners",timeout=7000)
                        except:
                            print("There is not Document details for these document")
                        try:
                            expect(page.locator('//div[@class="parcel-detail"]//h3[1]')).to_have_text("Owners",timeout=7000)
                            page.wait_for_timeout(timeout=1000)
                            response = HtmlResponse(url='https://www.example.com',body=page.content().encode('utf-8'))
                            page.wait_for_timeout(timeout=3000)
                            DetailsData(page,response, job_id, i, job_id_output_path)
                            page.wait_for_timeout(timeout=1000)
                            doc = response.xpath('//section/h1/text()').get(default='').split()[-1].strip()

                            page.wait_for_timeout(timeout=1000)
                            page.emulate_media(media="screen")
                            page.pdf(path=f"{job_id_output_path}\\Nv_douglas_a_PropertyDoc{doc}.pdf", display_header_footer=True,print_background=True)
                            page.wait_for_timeout(timeout=2000)
                            tax_pdf = job_id_output_path + f"\\Nv_douglas_a_Tax_PDF_{doc}.pdf"
                            with page.expect_popup() as popup_info:
                                page.locator("text=Tax Collection for this Parcel").click()
                            page1 = popup_info.value
                            try:
                                with page1.expect_download(timeout=80000) as download_info:
                                    page1.locator("a:has-text(\"Tax Bill\")").click(timeout=5000)
                                download = download_info.value
                                download.save_as(tax_pdf)
                                print("Document_downloaded")
                            except:
                                print("Tax_pdf is not available")
                            try:
                                page1.close()
                            except:
                                pass
                            try:
                                page.go_back()
                                page.wait_for_timeout(timeout=5000)
                            except:
                                pass
                        except:
                            page.go_back()
                            page.wait_for_timeout(timeout=5000)
                            pass
                    try:
                        page.locator('//a[contains(text(),"next page")]').click()
                        page.wait_for_timeout(timeout=9000)
                    except:
                        pass
                except:
                    pass
        except:
            pass
        br_logger.info("Full Search Data Extraction Completed Successfully:)")
    except:
        br_logger.info(f"Result not found for the Search Criteria!!")
