import json
import math
import random
import requests

def first_extraction(area_name,country_code,host_url):
    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'referer': host_url,
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    response = requests.get(
        f'https://www.pedidosya.cl/api/web-location/location/autocomplete?input={area_name}&country={country_code}',
        headers=headers)

    response.raise_for_status()
    print(response.text)
    autocomplete_json = response.json()
    found_result = autocomplete_json.get('predictions')
    descriptions = [i for i in found_result if i['description'] == area_name]
    # descriptions = [ i for i in found_result]
    if descriptions:
        return descriptions[0]
    else:
        pass

def second_extraction(placeId,placeType,host_url):

    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'referer': host_url,
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    params = {
        'placeId': placeId,
        'placeType': placeType,
    }

    response = requests.get(
        'https://www.pedidosya.cl/api/web-location/location/place',
        params=params,
        headers=headers,
    )

    response.raise_for_status()
    print(response.text)
    autocompl = response.json()
    return autocompl


def third_extraction(host_url,countryId,latitude,longitude,size=30, page=1):

    cookies = {'dhhPerseusGuestId': f'{random.randint(1, 9)}708966738539.000000002780728554.0002htixmo',}
    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'baggage': 'sentry-environment=live,sentry-release=peya-web%402.0.90,sentry-public_key=b015b29cb0524fa6a58705cc439e4075,sentry-trace_id=4bcbcd4bf2054eb8b7a3878944543ab8',
        'content-type': 'application/json;charset=UTF-8',
        'origin': host_url,
        'referer': 'https://www.pedidosya.cl/restaurantes?bt=RESTAURANT&origin=home&lat=-33.450085&lng=-70.519936&areaId=18597&areaName=18597&address=Alvaro%20Casanova&city=Santiago',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    params = {
        'size': f'{size}',
        'page': f'{page}',
    }

    json_data = {
        'filters': [],
        'businessTypes': [
            'RESTAURANT',
        ],
        'countryId': countryId,
        'point': {
            'latitude': latitude,
            'longitude': longitude,
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
        'https://www.pedidosya.cl/v3/shoplist/vendors',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    json_response = fresponse.json()

    return json_response



def extraction(area_name,country_code,host_url):
    print(f'Fetching places id for provided area name:{area_name}')
    descri = first_extraction(area_name,country_code,host_url)
    print(descri)
    placeId,placeType = descri['place_id'], descri['place_type'],
    if descri:
        print(f'Fetching places lat and long for area:{area_name}')
        place_info = second_extraction(placeId,placeType,host_url)
        print(place_info)
        all_listings =[]
        details = third_extraction(host_url,countryId=place_info['countryId'],latitude=place_info['latitude'],longitude=place_info['longitude'])
        print(details)
        all_listings.extend(details)

        # for i in range(1,pages):
        #     places_info = third_extraction(host_url,countryId, latitude, longitude,i)
        #     vendor_list = places_info['vendors']
        #     total_records = places_info['pagination']['total']
        #
        #     all_listings.extend(total_records)
        #     print(f'Fetched vendor Listing total count:{len(all_listings)}')
        with open(f'vendor_listing.json', 'w+') as _file:
            json.dump(all_listings, _file)
        print("total len",len(all_listings))

if __name__ == '__main__':
    host_url="https://www.pedidosya.com.ar"
    area_name = "Almafuerte 3334, Salta, Salta, Argentina"
    country_code = 'ar'
    extraction(area_name,country_code,host_url)

