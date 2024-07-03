"""
filename: Pedidosya.py

Example

area_name = "Miguel Aráoz, Salta, Argentina" # replace with your actual Area Name
country_code = 'ar'
scrape(area_name,country_code) # Write your business logic on this data
"""

import json
import random

import requests


def get_places_id(area_name, country_code, host_url):
    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': host_url,
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }

    params = {
        'input': area_name,
        'country': country_code,
    }

    response = requests.get(
        host_url + '/api/web-location/location/autocomplete',
        params=params,
        headers=headers,
    )

    response.raise_for_status()

    autocomplete_json = response.json()
    found_result = autocomplete_json.get('predictions', [])
    return found_result[0]


def get_place_latlong(placeId, placeType, host_url):
    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': host_url,
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }
    params = {'placeId': placeId, 'placeType': placeType}

    place_response = requests.get(
        host_url + '/api/web-location/location/place',
        params=params,
        headers=headers
    )
    place_response.raise_for_status()
    place_details = place_response.json()
    return place_details


def fetch_vendor_listing(lat, long, size=30, page=1, countryId=3, host_url=''):
    cookies = {
        '_gcl_au': '1.1.2119548986.1708948044',
        'dhhPerseusGuestId': '1708948024144.000000001772890733.0000gt7wsx',
        '_fbp': 'fb.2.1708948044641.403507645',
        '_pxvid': 'af89a43b-d49c-11ee-b8be-2a032a066d62',
        '_hjSessionUser_3527570': 'eyJpZCI6ImY0YmZkMjhiLWZlNTQtNTNmNy04MDMxLTJkZGNmYmFkMjVhOSIsImNyZWF0ZWQiOjE3MDg5NDkwMTA0MDQsImV4aXN0aW5nIjpmYWxzZX0=',
        '_ga_X043SN5YW8': 'GS1.1.1708949010.1.1.1708949020.0.0.0',
        'dhhPerseusSessionId': f'{random.randint(1, 2)}1709125057508.000000002204925883.0000gr83ec',
        'pxcts': '97a97534-d6ac-11ee-82a5-930c999a207e',
        '_gid': 'GA1.3.1323203548.1709304855',
        '_px3': '46ba05b3b4b22bf98e232a340b01d791442d57b97b91d4fbd9011635aa9d976c:OQYYNj6upogTo1wpis2aZqTdhaQ4N4thwzaFvg7EUZ55PoHLw6+VPiJJaH/etjWgJ0Pvl/2ge957xFsfmEOGLw==:1000:BMHbOm/QrNaVXCIkNKT/7Fsy3P9ivNnMDeWkHIDkcFK6WAjZMPx5WY098+p0UnbKh1BBp4xKi8jHCRdUaTvYOXSvx9noDEJghEXIMX4sEKlCs4ZdOKP3LNQKASBKGLmxOgFoHz4BSHpoS5t4CxRF75dGyfgZqktVYNt3L9Dgf5iH9pleUV9YVS599eXrLM+rZM0YsmyWQ2O9ul91GTThEJ7YoWbY8h8JJaIRfSFkqLg=',
        '__Secure-peya.sid': 's%3A5649cb30-728b-44fd-a6e8-f8783aa027fb.thiNQp%2F%2FR5BTMwvM1gDf2NqdnJv3BL1rjW6AyaJR5QY',
        '__Secure-peyas.sid': 's%3Adcb82ad5-89e3-41ba-b541-d95dea7d5204.XOACASKm16mhuI0dAOyGqBMXzGCZPjuMzLUqN%2FgZBT0',
        '_pxhd': '10kgPOu0xQbwHxkxb6GVpaySmqU7QTjx2B2p3/zqxujcEPIfuXAEcQW5G6e50hzxmMupL7a-XjyJUCUe0idEqA==:fT1GW-RkN6FSq2bg2nv70tJAn7y0JHlwcmv8jZbJD6r/gdltZiOaY14dlwcjO4hwVZTCB8XYbsgONa/6-L51hRPtCJqdl/jzy1m/IBqAsBTn5ulUz4wzKkgF6VbRzLlgKYEQt/KQDMD3tiBiqKR9mg==',
        '__cf_bm': 'VYedssvFaGdeGX771sDWCxdDqUSXMO2kX1cXe1Fisu8-1709461332-1.0.1.1-ZUnZy9nnIBMN4u0xDrccmoUfDUv8DUyt.rVidAwS7IWJCALNxeadoRIMW0ByLVp5.LGn_HaMIqyQD6kcwPYSeg',
        'dhhPerseusHitId': '1709461390977.000000000096927587.0000d000js',
        '_uetsid': '92c2b9f0d7db11ee97a4cb9956167c3c',
        '_uetvid': 'd0a51ce0d49c11ee9826e507d905416b',
        'ab.storage.sessionId.8f8614b7-a682-4b80-af4e-c133abb05875': '%7B%22g%22%3A%226feff4ea-bbb2-c074-f82b-7a58ab34e3d1%22%2C%22e%22%3A1709463211372%2C%22c%22%3A1709461411373%2C%22l%22%3A1709461411373%7D',
        'ab.storage.deviceId.8f8614b7-a682-4b80-af4e-c133abb05875': '%7B%22g%22%3A%22ce28fcf0-d9c5-c602-7a48-fcdbd93b6af5%22%2C%22c%22%3A1708948054261%2C%22l%22%3A1709461411383%7D',
        'ab.storage.userId.8f8614b7-a682-4b80-af4e-c133abb05875': '%7B%22g%22%3A%22%5Bobject%20Object%5D%22%2C%22c%22%3A1709098012503%2C%22l%22%3A1709461411385%7D',
        'AMP_TOKEN': '%24NOT_FOUND',
        '_gat_WD2_Tracker_PeYa_Prod': '1',
        '_ga_LQWR31SY8G': 'GS1.1.1709461388.23.1.1709461411.37.0.0',
        '_ga': 'GA1.1.1803347457.1708948047',
        '_tq_id.TV-81819090-1.20dc': 'a40b1f42db6ebd8d.1708948048.0.1709461412..',
    }

    if host_url == '':
        raise Exception('Please provide valid host url')

    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        'origin': host_url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }
    json_data = {
        'filters': [],
        'businessTypes': [
            'RESTAURANT',
        ],
        'countryId': countryId,
        'point': {
            'latitude': lat,
            'longitude': long,
        },
        'sort': 'RANKING',
        'offer': {
            'occasions': [
                'DELIVERY',
                'PICKUP',
            ],
        },
    }

    fresponse = requests.post(
        host_url + f'/v3/shoplist/vendors?page={page}&size={size}',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    json_respons = fresponse.json()
    vendor_list = json_respons['vendors']
    total_records = json_respons['pagination']['total']
    return vendor_list, total_records


def get_vendor_details(vendor_id_list, host_url):
    json_data = {'vendors': vendor_id_list}
    headers = {

        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': host_url,
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }
    vendor_response = requests.post(host_url + '/v1/food-home/v1/vendors',
                                    headers=headers,
                                    json=json_data)
    vendor_response.raise_for_status()
    json_response = vendor_response.json()
    return json_response


def scrape(sarea_name, country_code, host_url):
    print(f'Fetching places id for provided area name:{area_name}')
    # area_name = "Miguel Aráoz, Salta, Argentina"
    place_ids = get_places_id(area_name=area_name, country_code=country_code, host_url=host_url)

    if place_ids:
        print(f'Fetching places lat and long for area:{area_name}')
        place_info = get_place_latlong(placeId=place_ids['place_id'], placeType=place_ids['place_type'],
                                       host_url=host_url)

        print(f'Fetching vendor Listing:{area_name}')
        all_listings = []
        details, cnt = fetch_vendor_listing(lat=place_info['latitude'], long=place_info['longitude'],
                                            countryId=place_info['countryId'], host_url=host_url)
        all_listings.extend(details)
        if cnt > len(details):
            all_listings = []
            all_details, cnt = fetch_vendor_listing(lat=place_info['latitude'], long=place_info['longitude'],
                                                    countryId=place_info['countryId'], size=cnt, host_url=host_url)
            all_listings.extend(all_details)

        print(f'Fetched vendor Listing total count:{len(all_listings)}')

        print(f'Fetching vendor details :{len(all_listings)}')
        if all_listings:
            vendor_list = ([ele['id'] for ele in all_listings])
            vendor_details = get_vendor_details(vendor_list, host_url=host_url)

        ## Use this section to write data files or write data to any database
        with open(f'vendor_listing_{country_code}.json', 'w+') as _file:
            json.dump(all_listings, _file)
        with open(f'vendor_details_{country_code}.json', 'w+') as _file:
            json.dump(vendor_details, _file)


if __name__ == '__main__':
    supported_countries = {
        'cl':"https://www.pedidosya.cl", # do not add trailing slash
        # 'ar': "https://www.pedidosya.com.ar"
    }

    area_name = "Alvaro Casanova 4964, Chile" # replace with your actual Area Name
    country_code = 'cl'

    # area_name = "Almafuerte 3334, Salta, Salta Province, Argentina"
    # country_code = 'ar'

    host_url = supported_countries[country_code]
    scrape(sarea_name=area_name, country_code=country_code, host_url=host_url)  # Write your business logic on this data