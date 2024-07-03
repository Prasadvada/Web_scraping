import math
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
import re
import random
from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
date_time =df_existing = f'{datetime.now().strftime("%d-%m-%Y__%H-%M-%S")}'
print(date_time)
# MongoDB setup

client = MongoClient('mongodb://localhost:27017/')
db = client[f'your_collection_prasad']
collection = db['your_collection_prasad']

output_data_list = []
all_listings = []

def get_all_pages(doc_details):
    href_tag= doc_details
    host_url = f'https://www.audiologyonline.com{href_tag}'
    cookies = {'__utmb': f'{random.randint(1,9)}127091467.30.9.1710053876546'}
    headers = {
        'authority': 'www.audiologyonline.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en;q=0.9',
        'referer': f'https://www.audiologyonline.com/audiology-jobs/search/term:{country_code}/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    try:
        fresponse = requests.get(url=host_url,cookies=cookies, headers=headers)
        fresponse.raise_for_status()
        if fresponse.status_code == 200:
            soup = BeautifulSoup(fresponse.text, 'html.parser')
            time.sleep(2)
            Job_Title = ''
            if soup.find('h1') is not None:
                Job_Title = soup.find('h1').text.strip()
            Location = ''
            if soup.find('div',class_="col-sm-11").find_next('h4') is not None:
                Location = soup.find('div',class_="col-sm-11").find_next('h4').text.strip()
            company_name = ''
            if soup.find('em',class_="grey") is not None:
                company_name = soup.find('em',class_="grey").text.strip()
            contact = ''
            if soup.find('h4',class_="mb15").find_next('strong') is not None:
                contact = soup.find('h4',class_="mb15").find_next('strong').text.strip()
            telephone = ''
            if soup.find('span',class_="tel") is not None:
                telephone = soup.find('span',class_="tel").text.strip().replace('Phone:','').replace('Pref','').replace('.','').replace('x','').strip()
            job_Posted = ''
            try:
                job_Posted = soup.find('div',class_="grey mb20 mt20").text.replace('Posted:','').strip()
            except:
                pass
            email = ''
            try:
                context_page = soup.find('div',class_="container pt20").get_text(' ')
                email = re.findall('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{1,}\b|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',context_page)[0]
            except:
                email = ''
                pass
            internal_no = ''
            try:
                internal_no = soup.find('div',class_="grey mt40").text.strip().replace('ID:','').strip()
            except:
                pass
            salary =''
            try:
                if country_code == 'Audiologist':
                    context_page = soup.find('div', class_="container pt20").get_text('  ')
                    match = re.search(r'Average weekly sales.*?$', context_page, re.MULTILINE | re.DOTALL)
                    if match:
                        extracted_text = match.group(0)
                        salary = 'NA'

                if salary == '':
                    context_page = soup.find('div', class_="container pt20").get_text('  ')
                    match = re.search(r'Salary/Wage:.*?$', context_page, re.MULTILINE | re.DOTALL)
                    if match:
                        extracted_text = match.group(0)
                        pattern = re.compile(r'\$?([\d,\,?\.?\+?\/?]+hr)\s*?\-?\s*? \$?([\d,\,?\.?\+?\/?]+hr)')
                        match = re.search(pattern, extracted_text)
                        if match:
                            salary = match.group(0)

                if soup.find(string=re.compile("Salary: ", re.IGNORECASE)) is not None:
                    salary = soup.find(string=re.compile("Salary: ", re.IGNORECASE)).text
                    salary = re.sub('[a-zA-Z\:\(\)+]', '', salary).strip()
                    salary = salary

                if salary=='':
                    salary_text = soup.find('div', class_="dynamic description mb20").text.strip()
                    # pattern = re.compile(r'\$([\d,]+)-\$([\d,]+)|\$([\d,]+)-\$([\d,]+)k|(\$([\d,]+)-\s\$([\d,]+)\+)|\$([\d,]+)\s*?-\s*?\$?([\d,]+)|\$([\d,\.\,\+]+)\s*\-\s*\$([\d,\.\,\+]+)|\$([\d,\,?\.?\+?]+)|\$([\d,]+)-\$([\d,]+)K?|(\$([\d,\.\/]+)hr\s\-\s\$([\d,\.\/]+)hr)')
                    pattern = re.compile(r'\$?[\d\-]+\$?[\d]+[Kk]|\$([\d,\,?\.?\+?\|])+hr+|\$([\d,\,?\.?\+?\-]+)\s*\s*?per\s?hour|\$([\d,]+)-\$([\d,]+)k?|\$([\d,]+)-\$([\d,]+)k|(\$([\d,]+)-\s\$([\d,]+)\+)|\$([\d,\,?\.?\+?\/?]+hr)\s\-\s\$([\d,\,?\.?\+?\/?]+hr)|\$([\d,]+)\s*?-\s*?\$?([\d,]+)|\$([\d,\.\,\+]+)\s*\-\s*\$([\d,\.\,\+]+)|\$([\d,\,?\.?\+?]+)[kK]?|\$([\d,]+)-\$([\d,]+)K?')
                    match = re.search(pattern, salary_text)
                    if match:
                        salary = match.group(0)
            except:
                salary = ''

            Vacancy_url = host_url

            benfits_text= ''
            try:
                context_page = soup.find('div', class_="container pt20").text.strip()
                pattern = re.compile(r'Benefits:(.*?)Description:', re.DOTALL)
                match = pattern.search(context_page)
                if match:
                    benfits_text = match.group(1).strip()
                if benfits_text=='':
                    if soup.find(string='Benefits:') is not None:
                        benfits_text = soup.find('div', class_="dynamic description mb20").find_next(string='Benefits:').find_next_siblings(['p', 'ul'])
                        if benfits_text:
                            l = []
                            for paragraph in benfits_text:
                                all_jobs = paragraph.get_text()
                                l.append(all_jobs)
                            benfits_text = ' | '.join(l)
                        else:
                            benfits_text = ''
            except:
                benfits_text = ''
            Description =''
            try:
                context_page = soup.find('div', class_="container pt20").text.strip()
                pattern = re.compile(r'Description:(.*?)Job Description:', re.DOTALL)
                match = pattern.search(context_page)
                if match:
                    Description = match.group(1).strip()
            except:
                Description =''
                pass

            job_Description = ''
            try:
                context_page = soup.find('div', class_="container pt20").text.strip()
                pattern = re.compile(r'Job Description:(.*?)Occupation Classification Requirements:', re.DOTALL)
                match = pattern.search(context_page)
                if match:
                    job_Description = match.group(1).strip()
                if job_Description == '':
                    pattern = re.compile(r'Job Description(.*?)Qualifications:|Job Description(.*?)Additional Information',
                                         re.DOTALL)
                    match = pattern.search(context_page)
                    if match:
                        job_Description = match.group(1).strip()
                if job_Description=='':
                    pattern = re.compile(r'Job Description(.*?)Job Description', re.DOTALL)
                    match = pattern.search(context_page)
                    if match:
                        job_Description = match.group(1).strip()

            except:
                job_Description =''
                pass
            all_listings.append({'Job_Title':Job_Title,'Location':Location,'Company_name':company_name,'Contact':contact,'Telephone':telephone,'Job_Posted':job_Posted,'email':email,'Internal_no':internal_no,
                                 'Salary':salary,'Vacancy_url':Vacancy_url,'Benfits':benfits_text,'Description':Description,'Job_Description':job_Description})
    except Exception as e:
        print('Error', e)
        pass



def Pages_data(country_code,total_pages):
    cookies = {'__utmb': f'{random.randint(1,9)}127091467.6.9.1710053442227'}

    headers = {
        'authority': 'www.audiologyonline.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'referer': 'https://www.audiologyonline.com/audiology-jobs/all/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    response = requests.get(
        f'https://www.audiologyonline.com/audiology-jobs/search/term:{country_code}//page:{total_pages}/',
        cookies=cookies,
        headers=headers,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('h6', class_="mb5 job-title inline-block")
    for i in rows:
        try:
            href_tag = i.find('a').get('href')
            if href_tag not in output_data_list and not collection.find_one({'href': href_tag}):
                output_data_list.append(href_tag)
                # Store data in MongoDB
                data = {
                    'href': href_tag,
                }
                collection.insert_one(data)


        except Exception as e:
            print(e)

def get_places_id(country_code):
    cookies = {'__utmb': f'{random.randint(1,9)}127091467.6.9.1710053442227'}

    headers = {
        'authority': 'www.audiologyonline.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'referer': 'https://www.audiologyonline.com/audiology-jobs/all/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    response = requests.get(
        f'https://www.audiologyonline.com/audiology-jobs/search/term:{country_code}/',
        cookies=cookies,
        headers=headers,)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    total = soup.find('div', class_="col-xs-10 pt10 mb5 small").find_next('span', class_='grey').text
    records = int(re.findall("[\d]+", total)[-1])
    print(f'Fetching total_Records:{records}')
    total_pages = math.ceil(records / 15)
    print(f'Fetching total_pages:{total_pages}')
    total_pages = 3
    for i in range(1,total_pages+1):
        print(f'Processing Page :{i}')
        Pages_data(country_code,i)
    print("print the len of the rows:",len(output_data_list))
    print(output_data_list)

    with ThreadPoolExecutor(max_workers=5) as exe:
        exe.map(get_all_pages, output_data_list)

def scrape(country_code):
    print(f'Fetching places id for provided area name:{country_code}')
    get_places_id(country_code)

if __name__ == '__main__':
    search_countries = {
        'AY': "Audiology",
        'AT': "Audiologist"
    }
    country_code = search_countries['AY']
    scrape(country_code)
    df = pd.DataFrame(all_listings)
    df.to_csv(f'{country_code}_{date_time}.csv', index=False, encoding='Utf=8')
    print("Extracted total lenth of Records", len(all_listings))

