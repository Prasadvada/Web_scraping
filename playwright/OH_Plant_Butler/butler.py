import csv
import os
import random
import re, math
import shutil
import time
from concurrent.futures import ThreadPoolExecutor

from fake_useragent import UserAgent

from common import *
import pandas as pd
from sqlalchemy import select, insert, update
from scrapy.http import HtmlResponse
from sqlalchemy import update
from CustomLogger import LogGen
from models import oh_butler_database_tables
from DataExtractor import *
from playwright.sync_api import sync_playwright, expect
logger = LogGen.log_gen("Logs", "Butler.log")
from database import *
# pass parameters
jobid='12'
date = '01/19/2000'
end_date_str = '01/19/2000'
# doc_type = 'DEEDS'
# doc_type = 'MORTGAGES'
state ="OH"
st_county = "OH_BUTLER"
thread_concurrency = 1
remove_old_folder = False
path_temp = os.path.dirname(os.path.realpath(__file__))
download_folder = os.path.join(path_temp, f'{st_county}', f"{st_county}{date.replace('/', '-')}-{end_date_str.replace('/','-')}")
csv_path = f'{download_folder}_OUTPUT.csv'
ua = UserAgent()

afn_list = []

def find_number(stringdata):
    total = re.findall(r"(\d+)", stringdata)
    if total:
        num = total[0]
    else:
        num = "1"
    return num

def butler_extractor(jobid, state, st_county, date, end_date_str, thread_concurrency, download_folder):
    logger = LogGen.log_gen("Logs", "OH_BUTLER")
    RecorderTable, StatusTable, sessionLocal = oh_butler_database_tables()
    st_county = state + "_" + st_county
    day, weekday = check_weekday(date)
    logger.info(f"The date {date} falls on, {weekday}")
    if day == 6 or day == 7:
        logger.info(f"Data Might Not Be Available On Start Date {date}, {weekday} ")

    def data_extractor(afn_no):
        # logger.info(f'Processing Document Number - {doc_num}')
        local_session1 = sessionLocal()
        session_id = random.random()
        try:
            with sync_playwright() as sync_playwright_instance:
                browser = sync_playwright_instance.chromium.launch(headless=False,
                                                                   channel='chrome',

                                                                   )
                context = browser.new_context(
                    # storage_state='trumbull_state.json',
                    viewport={'width': 1280, 'height': 1024},
                    accept_downloads=True,
                    java_script_enabled=True,
                    ignore_https_errors=True,
                    user_agent=ua.random,
                )
                context.storage_state(path='../state.json')
                page1 = context.new_page()
                url = 'https://countyfusion13.kofiletech.us/countyweb/loginDisplay.action?countyname=ButlerOH'
                page1.goto(url)
                page1.wait_for_load_state(timeout=30000)
                logger.info(f"Loaded URL: {url}")
                time.sleep(2)
                login_as_guest_btn = page1.locator('input[type=button]').nth(1)
                expect(login_as_guest_btn).to_have_value('Login as Guest', timeout=10000)
                login_as_guest_btn.click()
                time.sleep(4)
                logger.info(f"Logged into website as Guest!")
                page1.wait_for_load_state('load', timeout=10000)
                page1.wait_for_load_state('domcontentloaded', timeout=10000)

                while True:
                    try:
                        search_recs_online = page1.frame("bodyframe").locator(
                            "//td/div[contains(normalize-space(.),'Search Public Records')]")
                        expect(search_recs_online).to_have_text('Search Public Records')
                        search_recs_online.click()
                        break
                    except Exception as e:
                        page1.wait_for_timeout(2000)
                page1.wait_for_timeout(1000)
                while True:
                    try:
                        page1.frame('dynSearchFrame').locator('//span[contains(text(),"Instrument Number")]').nth(0).click()
                        page1.wait_for_timeout(timeout=2000)
                        break
                    except:
                        continue
                        pass

                while True:
                    try:
                        expect(page1.frame('criteriaframe').locator(
                            '//div[@id="elemDocNum"]//td[contains(text(),"Instrument")]'))
                        page1.wait_for_load_state()
                        page1.wait_for_timeout(2000)
                        page1.frame('criteriaframe').locator(
                            '//*[@id="elemDocNum"]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/span/input[1]').fill(afn_no)
                        break
                    except:
                        pass
                page1.frame('dynSearchFrame').locator('//*[@id="imgSearch"]').nth(0).dblclick(force=True)
                try:
                    expect(page1.frame('resultFrame').locator('//td[@id="navDisplay"]')).to_contain_text('Displaying ',
                                                                                                        timeout=80000)
                except Exception as e:
                    page1.wait_for_timeout(2000)

                while True:
                    try:
                        page1.wait_for_load_state()
                        page1.wait_for_timeout(timeout=30000)
                        page1.frame('resultListFrame').locator("//div[@id='instList']//tr//tr/td[3]//a").click(
                            timeout=20000)
                        page1.wait_for_timeout(timeout=9000)
                        page1.wait_for_timeout(timeout=9000)
                        expect(page1.frame('tabs').locator("//div[@id='tabs']//span[contains(.,'Instrument Info')]"))
                        break
                    except Exception as e:
                        page1.wait_for_timeout(2000)

                while True:
                    try:
                        expect(page1.frame('tabs').locator("//div[@id='tabs']//span[contains(.,'Instrument Info')]"))
                        break
                    except Exception as e:
                        page1.wait_for_timeout(2000)
                page1.wait_for_load_state()
                try:
                    afn_num = find_number(page1.frame('docInfoFrame').locator(
                        '//span[contains(text(),"Instrument Number")]/../following-sibling::td[1]').nth(0).inner_text(
                        timeout=4000).replace('-', ''))
                    print(afn_num)
                except Exception as e:
                    afn_num = ""
                logger.info(f"Extraction started for AFN - {afn_num}")
                try:
                    response1 = HtmlResponse(url='https://www.example.com',body=page1.frame('docInfoFrame').content().encode('utf-8'))
                except Exception as e:
                    logger.info(f'Error In Data Extractor.... Found With The Document Number - {afn_num}\n')
                while True:
                    try:
                        legal = page1.frame('tabs').locator('//*[@id="tabs"]/div[1]/div[3]/ul/li[2]/a').nth(0)
                        legal.click()
                        page1.wait_for_timeout(2000)
                        expect(page1.frame('docInfoFrame').locator('//span[contains(.,"Instrument Number:")]')) \
                            .to_contain_text('Instrument Number:')
                        break
                    except Exception as e:
                        # print(e)
                        page1.wait_for_timeout(2000)

                page1.wait_for_timeout(2000)
                response2 = HtmlResponse(url='https://www.example.com',
                                         body=page1.frame('docInfoFrame').content().encode('utf-8'))
                try:
                    # DataExtractor(response, response2, jobid=dow_folder)
                    DataExtractor(response1, afn_num, download_folder, jobid,response2)
                    data_extract_status = 1
                except Exception as e:
                    data_extract_status = 0
                    logger.info(f'Error In Data Extractor.... Found With The Document Number - {afn_num}\n')
                path = f'{download_folder}\\{afn_num}.pdf'
                try:
                    with page1.expect_download(timeout=50000) as download_info:
                        view_document = page1.frame('resnavframe').locator('//*[@title="Save Image"]')
                        view_document.nth(0).click(timeout=20000)
                        page1.wait_for_load_state()
                        page1.wait_for_timeout(2000)

                        download_document = page1.frame('dialogframe').locator(
                            '//input[contains(@value,"Download")]')
                        download_document.nth(0).click(timeout=20000)
                        page1.wait_for_timeout(4000)
                        try:
                            page1.wait_for_load_state()
                            accept_button = page1.frame('dialogframe').locator('//input[contains(@value,"Accept")]')
                            accept_button.nth(0).click(timeout=10000)
                            page1.wait_for_load_state()
                            page1.wait_for_timeout(2000)
                            page1.wait_for_load_state()

                        except:
                            pass
                        try:
                            notification_click = page1.frame('bodyframe').locator('//span[text()="Ok"]')
                            notification_click.nth(0).click(timeout=10000)
                        except Exception as e:
                            # print(e)
                            pass
                    download = download_info.value
                    download.save_as(path)
                    pdf_status = 1
                    logger.info(f"Document Download Successful for AFN - {afn_num} ;)\n")
                except:
                    pdf_status = 0
                    logger.info(f'Document Not Found With The Document Number - {afn_num}\n')


                # fixed for every county, don't change
                # TODO Implement below database code to update db for data extraction and pdf download
                #  status
                try:
                    local_session1.execute(
                        update(RecorderTable)
                        .where(RecorderTable.document_number == f"{afn_no}")
                        .values(
                            data_extract_status=data_extract_status,
                            pdf_status=pdf_status,
                        )
                    )
                    local_session1.commit()
                    local_session1.close()
                except Exception as e:
                    logger.info(f'{e}')

        except Exception as e:
            logger.info(f'Restarting Automation For Processing Document Number - {afn_no}')



    def download_data(date, st_county, dow_folder):
        # RecorderTable, StatusTable, sessionLocal = oh_butler_database_tables()
        # local_session1 = sessionLocal()
        # session_id = random.random()
        local_session = sessionLocal()
        local_session.execute(insert(StatusTable),
                              [
                                  {
                                      "jobid": jobid, "state": state, "county": st_county, "status": 1,
                                      "from_date": date, "thru_date": end_date_str
                                  }
                              ]
                              )
        local_session.commit()

        session_id = random.random()

        logger.info(f'{st_county} Automation Initaited!!')
        try:
            with sync_playwright() as sync_playwright_instance:
                browser = sync_playwright_instance.chromium.launch(headless=False,
                                                                   channel='chrome'

                                                                   )
                context = browser.new_context(viewport={'width': 1280, 'height': 1024}, accept_downloads=True)
                context.storage_state(path='../state.json')
                page = context.new_page()
                url = 'https://countyfusion13.kofiletech.us/countyweb/loginDisplay.action?countyname=ButlerOH'
                page.goto(url)
                page.wait_for_load_state()
                logger.info(f"Loaded URL: {url}")
                login_as_guest_btn = page.locator('input[type=button]').nth(1)
                expect(login_as_guest_btn).to_have_value('Login as Guest', timeout=10000)
                login_as_guest_btn.click()

                logger.info(f"Logged into website as Guest!")

                page.wait_for_load_state('load', timeout=10000)
                page.wait_for_load_state('domcontentloaded', timeout=10000)

                while True:
                    try:
                        search_recs_online = page.frame("bodyframe").locator(
                            "//td/div[contains(normalize-space(.),'Search Public Records')]")
                        expect(search_recs_online).to_have_text('Search Public Records')
                        search_recs_online.click()
                        break
                    except Exception as e:
                        page.wait_for_timeout(2000)
                page.wait_for_timeout(1000)
                time.sleep(2)

                while True:
                    try:
                        start_date = page.frame('criteriaframe').locator('//input[contains(@name,"FROMDATE")]/preceding-sibling''::input').nth(0)
                        break
                    except Exception as e:
                        pass
                        page.wait_for_timeout(2000)
                start_date.type(date, timeout=30000)
                logger.info(f"Entered Start Date - {date}")
                page.wait_for_timeout(2000)

                end_date = page.frame('criteriaframe').locator('//input[contains(@name,"TODATE")]/preceding-sibling'
                                                               '::input').nth(0)
                end_date.type(end_date_str, timeout=30000)
                logger.info(f"Entered End Date - {end_date_str}")

                page.wait_for_timeout(1000)

                page.frame('dynSearchFrame').locator('//*[@id="imgSearch"]').nth(0).dblclick(force=True)
                c = 1
                while c <= 10:
                    try:
                        page.frame('dynSearchFrame').locator('//*[@id="imgSearch"]').nth(0).click()
                        c += 1
                    except Exception as e:
                        break
                page.wait_for_load_state('load', timeout=80000)
                expect(page.frame('resultFrame').locator('//td[@id="navDisplay"]')).to_contain_text('Displaying ',timeout=80000)
                logger.info(f'Search successful for Date - {date}!')
                tot_rec_str = page.frame('resultFrame').locator('id=navDisplay').inner_text(timeout=20000)
                tot_rec = int(re.findall(r"[\d]+", tot_rec_str)[-1])
                tot_res = int(re.findall(r"[\d]+", tot_rec_str)[1])
                logger.info(f'Records Displayed on Page - {tot_res}')
                logger.info(f'Total Results Found - {tot_rec}!')
                m= math.ceil(tot_rec/tot_res)
                l=[]
                for j in range(1,m+1):
                    total_rows = page.frame('resultListFrame').query_selector_all(f"//div[@id='instList']//tr//tr/td[3]//a")
                    for i in range(1,len(total_rows)+1):
                        afn_no = page.frame('resultListFrame').locator(f"//div[@id='instList']//tr[{i}]//tr/td[3]//a").inner_text().strip()
                        l.append(afn_no)
                    try:
                        page.frame('subnav').locator('//img[@alt="Go to next result page"]').nth(0).click(timeout=30000)
                        page.wait_for_load_state()
                        page.wait_for_timeout(timeout=9000)
                        expect(page.frame('resultFrame').locator('//td[@id="navDisplay"]')).to_contain_text('Displaying ',timeout=80000)
                    except:
                        pass
                print(len(l))
                page.close()
                process_doc_list = []
                for doc_val in l:
                    print(doc_val)
                    record_to_update = local_session.execute(
                        select(RecorderTable).where(RecorderTable.document_number == doc_val)).scalars().first()
                    if record_to_update is None:
                        process_doc_list.append(doc_val)

                        local_session.execute(insert(RecorderTable),
                                              [
                                                  {
                                                      "jobid": jobid, "document_number": doc_val
                                                  }
                                              ]
                                              )
                    elif record_to_update.data_extract_status == 0 or record_to_update.pdf_status == 0:
                        process_doc_list.append(doc_val)

                local_session.commit()
                local_session.close()

                # starting threadpool executor, optimal concurrency = 5
                with ThreadPoolExecutor(max_workers=thread_concurrency) as exe:
                    exe.map(data_extractor, process_doc_list)


                logger.info(f'Data Extraction completed for Date Range- {start_date} -- {end_date}  !!')

                # fixed for every county, don't change
                local_session = sessionLocal()
                document_not_downloaded = []
                total_pdf_downloaded = local_session.execute(
                    select(RecorderTable)
                    .where(
                        RecorderTable.jobid == f"{jobid}").where(RecorderTable.pdf_status == 1)).scalars().all()
                pdf_not_found = local_session.execute(
                    select(RecorderTable)
                    .where(
                        RecorderTable.jobid == f"{jobid}").where(RecorderTable.pdf_status == 0)).scalars().all()
                if len(pdf_not_found) != 0:
                    for i in range(len(pdf_not_found)):
                        document_not_downloaded.append(pdf_not_found[i].document_number)
                    logger.info(
                        f'For Date Range {start_date} -- {end_date} PDF Not Downloaded For Documents {document_not_downloaded} !!')
                else:
                    logger.info(f'Every Document is Downloaded !!')

                # fixed for every county, don't change
                record_not_extracted = []
                total_record_extracted = local_session.execute(
                    select(RecorderTable)
                    .where(
                        RecorderTable.jobid == f"{jobid}").where(
                        RecorderTable.data_extract_status == 1)).scalars().all()
                record_not_found = local_session.execute(
                    select(RecorderTable)
                    .where(
                        RecorderTable.jobid == f"{jobid}").where(
                        RecorderTable.data_extract_status == 0)).scalars().all()
                if len(record_not_found) != 0:
                    for i in range(len(record_not_found)):
                        record_not_extracted.append(record_not_found[i].document_number)
                    logger.info(
                        f'For Date Range {start_date} -- {end_date} Record Data Not Extracted For Documents {record_not_extracted} !!')
                else:
                    logger.info(f'Every Record is Extracted !!')
                local_session.close()

                outname1 = f'{os.path.dirname(os.path.realpath(download_folder))}\\TOTAL_RECORDS_STATUS_DESCRIPTION.csv'
                outname2 = f'{os.path.dirname(os.path.realpath(download_folder))}\\..\\TOTAL_RECORDS_STATUS_DESCRIPTION.csv'

                # fixed for every county, don't change
                for outname in [outname1, outname2]:
                    with open(outname, "w", newline="") as wd:
                        wr = csv.writer(wd)
                        allresponse = [
                            [
                                "Jobid", "State", "County", "From Date", "Thru Date", "Total Records Found On Website",
                                "Total Data Extracted", "Missing Data Count", "Missing Data",
                                "Total PDFs Downloaded",
                                "Missing PDFs Count",  "Missing PDFs"
                            ],
                            [
                                jobid, state, st_county, start_date, end_date, tot_rec, len(total_record_extracted),
                                len(record_not_extracted), record_not_extracted, len(total_pdf_downloaded), len(pdf_not_found), document_not_downloaded
                            ]
                        ]

                        wr.writerows(allresponse)
                    wd.close()
            # break
        except Exception as e:
            logger.info(f'{e}')
            # continue

        finally:
            # fixed for every county, don't change
            local_session = sessionLocal()
            local_session.execute(
                update(StatusTable),
                [
                    {
                        "jobid": jobid,
                        "total_record_found": tot_rec,
                        "total_record_extracted": len(total_record_extracted),
                        "missing_records": len(record_not_extracted),
                        "total_pdf_downloaded": len(total_pdf_downloaded),
                        "pdf_not_found": len(pdf_not_found)
                     }
                ]
            )
            local_session.commit()
            local_session.close()

    download_data(date, st_county,  download_folder)


if __name__ == "__main__":
    butler_extractor(jobid, state, st_county, date, end_date_str, thread_concurrency, download_folder)
    # download_data(date, st_county,  download_folder)
    destination = os.path.join(path_temp, f"{st_county}-{date.replace('/', '_')}", f"{st_county}{end_date_str.replace('/', '_')}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(f'{download_folder}', destination)
    df = pd.read_csv(csv_path)
    new_df = df.drop_duplicates()
    new_df.to_csv(f"{destination}\\..\\{st_county}-{date.replace('/', '_')}-{end_date_str.replace('/','_')}_OUTPUT.csv")
    shutil.make_archive(root_dir=f"{destination}/..", format='zip', base_name=f"{destination}\\..")


