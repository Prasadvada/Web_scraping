import random
import requests

class PedidosyaScraper:
    def __init__(self) -> None:
        self.session = requests.Session()
    def final_scrape(self):
        cookies = {
            'JSESSIONID': 'AEC05E76C7B162DF3A9CE09BF83ED32A',
            'AMCVS_30545A0C536B768C0A490D44%40AdobeOrg': '1',
            '_gcl_au': f'1.1.{random.randint(1,9)}555784502.1711393515',
            'ak_bmsc': 'E55D5692075CAF64FE4ABC7D7271549D~000000000000000000000000000000~YAAQBiozatbjmHaOAQAAx6kAdxdMuq3XezGBtyW8iiZ0vtOMgganHGiNNrKjk9xnEN8wn1nojBkBYZ4SmACsZxNZeZ23m++mUJkuqjdidjROMiGqSFhayGHutQQ6kuxVKOPafS31DWDFIC8SRLiMc63V4jRAEbxfPn0fVtIZKEGFCmgNVMiaTsbZE7gVyd2eA+USRqwdGTOznxm3W7g0IWituiRpGbjkQApz1mmvNldyCo4evGICVlO3w9dauQmKrFhDARNuBZ7Qfde2RNgl/V7UtiBAA4GmaP+YhnjuXt+OYnGDJa1Kb89YX7MTwL9VKE/r5rEoIhnPpOoxqA/gWJ2lGCH2ZnnTa4F/I/Xz8EX8NRGsNksZKdgeaHago9k4y+I/GkswuKMMWHPWNnlHYBn73zEpgvORdY2vZmbBVttLe7spu7y5TSizgZ7K+YlTe185+TajaVT/MGZ4GOdgxhCaWpjXFIQzOkQqMjetPw==',
            's_ecid': 'MCMID%7C38070621018886705693686729193344795253',
            'AMCV_30545A0C536B768C0A490D44%40AdobeOrg': '1176715910%7CMCIDTS%7C19808%7CMCMID%7C38070621018886705693686729193344795253%7CMCAAMLH-1711998315%7C12%7CMCAAMB-1711998315%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1711400715s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19815%7CvVersion%7C5.4.0',
            'at_check': 'true',
            '_uetsid': '9e0c1c40eada11ee89148987f0a3660e',
            '_uetvid': '9e0c3d50eada11ee920b6f1cfd0d9c37',
            'SESSION': 'YzdmYTE5NzItZmNiOS00ZTJlLWEwODYtNjFjOTU4ZGM4ZDkw',
            'visid_incap_1271375': 'nYXOFLmPQlaq7eyZ1ioxQ+7KAWYAAAAAQUIPAAAAAAApD5LKBCaV3oR9gr1HNTxo',
            'nlbi_1271375': 'Hk1aO6keFRNwBNMi9V/w9gAAAAAlimE8xTUozb/aPYBpI6EJ',
            'incap_ses_714_1271375': 'M6KlHtJtFQk6umLl1aPoCe7KAWYAAAAAbAGTOZCax6TdcBspEOq2mg==',
            's_cc': 'true',
            '_ga': f'GA1.2.{random.randint(1,9)}522350845.1711393519',
            '_gid': f'GA1.2.{random.randint(1,9)}335461519.1711393521',
            'QuantumMetricSessionID': 'cd6e282ad9313f44ce760c64dd120a51',
            'QuantumMetricUserID': '3975a41f6e06c55cb6544bee2ee179bb',
            '_fbp': 'fb.1.1711393521135.719958473',
            '_pin_unauth': 'dWlkPU5EWTBOelkwTnpJdFpUUXdOQzAwT1RZMUxXRTRZV1V0WkRZMU5XUm1NakF6TUdGag',
            'OptanonAlertBoxClosed': '2024-03-25T19:06:06.224Z',
            'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Mar+26+2024+00%3A36%3A06+GMT%2B0530+(India+Standard+Time)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&consentId=1bfeeec4-fd58-4ba5-9254-3272051312f8&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0007%3A1%2CC0003%3A1%2CC0004%3A1&hosts=H549%3A1%2CH569%3A1%2CH32%3A1%2CH216%3A1%2CH14%3A1%2CH15%3A1%2CH568%3A1%2CH13%3A1%2CH16%3A1%2CH439%3A1%2CH508%3A1%2CH511%3A1%2CH24%3A1%2CH512%3A1%2CH580%3A1%2CH513%3A1%2CH350%3A1%2CH26%3A1%2CH514%3A1%2CH376%3A1%2CH515%3A1%2CH468%3A1%2CH5%3A1%2CH475%3A1%2CH516%3A1%2CH582%3A1%2CH6%3A1%2CH517%3A1%2CH493%3A1%2CH518%3A1%2CH585%3A1%2CH519%3A1%2CH8%3A1%2CH230%3A1%2CH521%3A1%2CH522%3A1%2CH324%3A1%2CH523%3A1%2CH524%3A1%2CH300%3A1%2CH525%3A1%2CH526%3A1%2CH527%3A1%2CH581%3A1%2CH37%3A1%2CH528%3A1%2CH374%3A1%2CH11%3A1%2CH449%3A1%2CH12%3A1%2CH530%3A1%2CH531%3A1%2CH533%3A1%2CH39%3A1%2CH44%3A1%2CH29%3A1%2CH534%3A1%2CH17%3A1&genVendors=V11%3A1%2CV4%3A1%2CV33%3A1%2CV60%3A0%2CV22%3A1%2CV5%3A1%2CV14%3A1%2CV37%3A1%2CV41%3A1%2CV43%3A1%2CV3%3A1%2CV35%3A1%2CV25%3A1%2CV21%3A1%2CV20%3A1%2CV59%3A1%2CV40%3A1%2CV16%3A1%2CV26%3A1%2CV34%3A1%2CV9%3A1%2CV27%3A1%2CV39%3A1%2CV31%3A1%2CV24%3A1%2CV46%3A1%2CV45%3A1%2CV36%3A1%2CV58%3A1%2CV55%3A1%2CV28%3A1%2CV10%3A1%2CV50%3A1%2CV49%3A1%2CV13%3A1%2CV17%3A1%2CV7%3A1%2CV52%3A1%2CV30%3A1%2CV47%3A1%2CV48%3A1%2CV12%3A1%2CV18%3A1%2CV19%3A1%2CV15%3A1%2CV29%3A1%2CV56%3A1%2CV42%3A1%2CV38%3A1%2CV51%3A1%2CV8%3A1%2CV32%3A1%2CV57%3A1%2CV44%3A1%2CV53%3A1%2CV54%3A1%2CV23%3A1%2CV6%3A1%2C',
            's_pers': '%20s_vs%3D1%7C1711395387698%3B%20gpv_v5%3D%252Fen%252Fhome.html%7C1711395387703%3B',
            's_sq': 'ehglobalprod%3D%2526c.%2526a.%2526activitymap.%2526page%253D%25252Fen%25252Fhome.html%2526link%253DBrowse%252520Vehicles%2526region%253Dbook%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253D%25252Fen%25252Fhome.html%2526pidt%253D1%2526oid%253DfunctionJr%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DBUTTON',
            's_sess': '%20s_ppvl%3D%3B%20SC_LINKS%3D%252Fen%252Fhome.html%255E%255EBrowse%2520Vehicles%255E%255Eundefined%255E%255Ebook%255E%255E%3B%20s_ppv%3D%252Fen%252Fhome.html%252C8%252C16%252C801.3999938964844%252C1280%252C375%252C1280%252C720%252C1.25%252CL%3B',
            '_ga_BEMPZFZ04Z': 'GS1.1.1711393519.1.1.1711393592.55.0.0',
            '_ga_3327J5QJ9N': 'GS1.1.1711393520.1.1.1711393592.60.0.0',
            'mbox': 'session#1229c4178a1045a8aa2d52f6f28fa894#1711395455|PC#1229c4178a1045a8aa2d52f6f28fa894.41_0#1774638395',
            'RT': '"z=1&dm=enterprise.com&si=9443e883-9e9e-4fa8-8a62-3852d7157817&ss=lu7bicp2&sl=2&tt=8h8&bcn=%2F%2F684d0d4a.akstat.io%2F"',
        }

        headers = {
            'authority': 'prd-west.webapi.enterprise.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-IN,en;q=0.9',
            'brand': 'ENTERPRISE',
            'channel': 'WEB',
            'domain_country_of_residence': 'US',
            'locale': 'en_US',
            'origin': 'https://www.enterprise.com',
            'referer': 'https://www.enterprise.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'tab_id': '1711268977723_1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        response = requests.get(
            'https://prd-west.webapi.enterprise.com/enterprise-ewt/session/current',
            cookies=cookies,
            headers=headers,
        )
        print(response.raise_for_status())
        y= response.json()
        l = y['gbo']
        print(l)

    def first_extract(self):
        headers = {
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'locale': 'en_US',
            'sec-ch-ua-mobile': '?0',
            'TAB_ID': '1711268977723_3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'domain_country_of_residence': 'US',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.enterprise.com/',
            'BRAND': 'ENTERPRISE',
            'SOFRESH': 'SOCLEAN',
            'CHANNEL': 'WEB',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'pickup_location_id': '1018781',
            'return_location': {
                'locationName': 'New York JFK International Airport',
                'countryCode': 'US',
                'gps': {
                    'latitude': 40.65915,
                    'longitude': -73.801872,
                },
                'groupBranchNumber': '24JZ',
                'name': 'New York JFK International Airport',
                'longitude': -73.801872,
                'peopleSoftId': '1018781',
                'timeZoneId': 'America/New_York',
                'country_code': 'US',
                'type': 'BRANCH',
                'id': '1018781',
                'lat': 40.65915,
                'key': '1018781',
            },
            'renter_age': '25',
            'one_way_rental': False,
            'pickup_time': '2024-03-28T12:00',
            'return_location_id': '1018781',
            'pickup_location': {
                'locationName': 'New York JFK International Airport',
                'countryCode': 'US',
                'gps': {
                    'latitude': 40.65915,
                    'longitude': -73.801872,
                },
                'groupBranchNumber': '24JZ',
                'name': 'New York JFK International Airport',
                'longitude': -73.801872,
                'peopleSoftId': '1018781',
                'timeZoneId': 'America/New_York',
                'country_code': 'US',
                'type': 'BRANCH',
                'id': '1018781',
                'lat': 40.65915,
                'key': '1018781',
            },
            'renter_age_label': '25+',
            'return_time': '2024-03-28T12:00',
            'applied_vehicle_class_filters': [],
            'country_of_residence_code': 'US',
            'enable_north_american_prepay_rates': False,
            'view_currency_code': 'USD',
            'check_if_no_vehicles_available': True,
            'check_if_oneway_allowed': True,
        }

        response = requests.post(
            'https://prd-west.webapi.enterprise.com/enterprise-ewt/reservations/initiate',
            headers=headers,
            json=json_data,
        )
        print(response.raise_for_status())


    def scrape(self):
        headers = {
            'authority': 'prd.location.enterprise.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-IN,en;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.enterprise.com',
            'pragma': 'no-cache',
            'referer': 'https://www.enterprise.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        params = {
            'dto': 'true',
            'includeExotics': 'true',
            'countryCode': 'US',
            'brand': 'ENTERPRISE',
            'locale': 'en_US',
            'cor': 'US',
        }

        response = requests.get(
            'https://prd.location.enterprise.com/enterprise-sls/search/location/enterprise/web/text/New%20York%20JFK%20International%20Airport',
            params=params,
            headers=headers,
        )
        print(response.raise_for_status())


if __name__ == '__main__':
    s1 = PedidosyaScraper()
    s1.scrape()
    s1.first_extract()
    s1.final_scrape()
