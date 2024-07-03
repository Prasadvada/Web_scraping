import csv
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright, expect

all_data = []
def data_extractor(doc_details):
    time.sleep(2)
    url, doc_list = doc_details
    print('processing page -',{doc_list})
    with sync_playwright() as sync_playwright_instance:
        browser = sync_playwright_instance.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 1024}, accept_downloads=True, java_script_enabled=True,
            ignore_https_errors=True, )
        page = context.new_page()
        url = url[0]
        print(url)
        url_retry = 1
        while True:
            try:
                page.goto(url, wait_until='load', timeout=50000)
                page.wait_for_load_state(timeout=50000)
                break
            except (Exception,) as e:
                if url_retry == 5:
                    print(f"thes url is not opened{doc_list}")
                    break
                url_retry += 1
        page.wait_for_timeout(2000)
        try:
            page.locator('//span[contains(text(),"OK, Got it")]').click(timeout=5000)
        except:
            pass
        page.wait_for_timeout(2000)
        try:
            page.locator('(//span[@data-label="VIEW_MORE"])[1]').click(timeout=5000)
        except:
            pass
        page.wait_for_timeout(5000)
        try:
            Project_id= page.locator('//*[@id="newDesc"]/html/body').inner_text()
        except:
            Project_id= ''
        try:
            Projecetid= page.locator('//*[@id="newDesc"]/html/body').inner_text()
            pattern = r'this project is (.+)'
            result = re.search(pattern, Projecetid)
            if result:
                Projecetid = result.group(1)
            else:
                Projecetid = ''
        except:
            Projecetid=''

        try:
            page.locator('//i[@class="iconS_Common_24 icon_close pageComponent "]').click()
            page.mouse.wheel(0, 100)
            page.mouse.wheel(0, 1000)
        except:
            pass
        Builder_id = ''
        latitude = ''
        longitude = ''
        try:
            project_name = page.locator('//h1[@class="ProjectInfo__imgBox1 title_bold"]').inner_text().replace('\n','').strip()
        except:
            project_name=''
        sub_location,city_name = '', ''
        try:
            sub_location = page.locator('//span[@class="caption_subdued_medium ProjectInfo__imgBox1SubTxt"]//span[1]').inner_text().replace('\n','').strip()
            if sub_location!='':
                city_name = sub_location.split(',')[1].strip()
        except:
            pass
        low_cost_text,high_cost_text='',''
        try:
            page.locator('//div[contains(text(),"Price Trends")]').click(timeout=3000)
            low_cost_text = page.locator('(//p[@class="spacer4 section_header_semiBold"])[1]').inner_text()
            high_cost_text = page.locator('(//p[@class="spacer4 section_header_semiBold"])[2]').inner_text()
        except:
            pass
        project_url = ''
        try:
            l=[]
            proj_url = page.locator('//div[@class="d_cardContent__actionheadWrap"]').count()
            if proj_url>0:
                for i in range(1,proj_url+1):
                    proj =page.locator(f'(//div[@class="d_cardContent__actionheadWrap"][1]/a)[{i}]').get_attribute('@href')
                    l.append(proj)
                try:
                    project_url = ' | '.join(l)
                except:
                    pass
        except:
            pass
        try:
            Status = page.locator('//div[@class="ProjectInfo__imgBox1 title_bold ConstructionStatus__phaseStatus"]').inner_text()
        except:
            Status = ''
        try:
            amenities = page.locator('//div[@class="descHolder__descText ReadMoreLess__prewrap "]').inner_text()
        except:
            amenities=''

        media = ''
        Rera = ''
        try:
            Project_Description = Project_id
        except:
            Project_Description=''
        land_mark =''
        try:
            land_mark = Project_id
            pattern = r"^(.*?)\buto\s+is\s+a\b"
            match = re.match(pattern, land_mark)
            if match:
                land_mark = match.group(1)
            else:
                land_mark=''
        except:
            pass
        try:
            state = Project_id
            pattern = r"real\s+estate\s+market\s+of\s+(.*)"
            match = re.search(pattern, state)
            if match:
                state = match.group(1)
            else:
                state=''
        except:
            state = ''
        try:
            rating = page.locator('//*[@class="display_l_semiBold"]').inner_text()
        except:
            rating = ''
        try:
            Price = page.locator('(//div[@class="section_header_semiBold Ng800"])[2]').inner_text()
        except:
            Price = ''
        try:
            completion_date = page.locator('//span[@class="caption_strong_medium ConstructionStatus__phaseStatusSubtitle"]').inner_text()
        except:
            completion_date=''
        try:
            logo = page.locator('//div[@class="ProjectInfo__imgBox"]//img').get_attribute('@src')
        except:
            logo= ''
        try:
            flaship_image = page.locator('//div[@class="PhotonCard__photonDisp"]//img').get_attribute('@src')
        except:
            flaship_image = ''


        product_data = {"Project_id": Projecetid, "project_name": project_name,'land_mark':land_mark,'Project_Description':Project_Description,'logo':logo,'completion_date':completion_date,'Price':Price,'rating':rating,'state':state,'Builder_id':Builder_id,'flaship_image':flaship_image,'project_url':project_url,'Rera':Rera,'low_cost_text':low_cost_text,'high_cost_text':high_cost_text,
         'media':media,'amenities':amenities, 'Status':Status,'latitude':latitude, 'longitude':longitude,
                        'sub_location':sub_location,'city_name':city_name}

        all_data.append(product_data)
        page.wait_for_load_state(timeout=2000)
    with open('property_data.json', 'w') as json_file:
        json.dump(all_data, json_file, indent=4)
        print('Data saved to product_data.json')

doc_index = 0
doc_list = []
i = 0
with open('C:\\Users\\laksh\\OneDrive\\Desktop\\Selenium\\Acres\\websitelinks.csv', mode='r',
          encoding='utf-8-sig') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        url = lines
        doc_index += 1
        doc_list.append([url, doc_index])
    print((doc_list))
    print(len(doc_list))
    with ThreadPoolExecutor(max_workers=5) as exe:
        exe.map(data_extractor, doc_list)
