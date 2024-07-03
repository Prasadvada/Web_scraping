import requests
from kissan_Data import DataExtractor
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://data.gov.in/datasets_webservices/datasets/6622307',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
# cookies = {
#     '_ga': 'GA1.1.79258497.1689361152',
#     'fontSize': '67.5',
#     'citrix_ns_id': 'AAI73JuxZDvQuQkAAAAAADuMGtjGAxHPGX4gO65EzR7kDCfEQ03EDOSGi6XZKPc0Ow==NaCxZA==e6YnjT-wOEhe24eCHQB5cuzCcdU=',
#     '_ga_2NLK0N9J6V': 'GS1.1.1689361151.1.1.1689361390.13.0.0',
# }
# response = requests.get('https://data.gov.in/backend/dmspublic/v1/resources?offset=0&limit=8&filters[external_api_reference]=6622307&query=Gujarat&sort[_score]=desc',cookies=cookies,headers=headers,)
b = 8
for j in range(0,603):
    try:
        print('row:',j)
        url=''
        if j==0:
            url = 'https://data.gov.in/backend/dmspublic/v1/resources?offset=0&limit=8&filters[external_api_reference]=6622307&query=Gujarat&sort[_score]=desc'
            print(url)
        elif j>=1:
            row = b * j
            url = f'https://data.gov.in/backend/dmspublic/v1/resources?offset={row}&limit=8&filters[external_api_reference]=6622307&query=Gujarat%20&sort[_score]=desc'
            print(url)
        response = requests.get(url, headers=headers)
        data = response.json()
        DataExtractor(data)
    except Exception as e:
        print(e)

