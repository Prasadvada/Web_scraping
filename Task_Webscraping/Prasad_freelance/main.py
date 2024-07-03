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
    autocompl = response.json()
    return autocompl

# def fetch_vendor_listing(lat, long, size=30, page=1, countryId=3, host_url=''):

def third_extraction(lat,long,countryId,host_url,size=30, page=1):

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

    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'baggage': 'sentry-environment=live,sentry-release=peya-web%402.0.90,sentry-public_key=b015b29cb0524fa6a58705cc439e4075,sentry-trace_id=4bcbcd4bf2054eb8b7a3878944543ab8',
        'content-type': 'application/json;charset=UTF-8',
        'origin': host_url,
        'referer': 'https://www.pedidosya.cl/restaurantes?bt=RESTAURANT&origin=home&lat=-33.450085&lng=-70.519936&areaId=18597&areaName=18597&address=Alvaro%20Casanova&city=Santiago',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
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

    response = requests.post(
        'https://www.pedidosya.cl/v3/shoplist/vendors',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    response.raise_for_status()
    json_respons = response.json()
    vendor_list = json_respons['vendors']
    total_records = json_respons['pagination']['total']
    return vendor_list, total_records


def venderos(vendor_id_list, host_url):
    # cookies = {
    #     '_gcl_au': '1.1.2119548986.1708948044',
    #     'dhhPerseusGuestId': '1708948024144.000000001772890733.0000gt7wsx',
    #     '_fbp': 'fb.2.1708948044641.403507645',
    #     '_pxvid': 'af89a43b-d49c-11ee-b8be-2a032a066d62',
    #     '_hjSessionUser_3527570': 'eyJpZCI6ImY0YmZkMjhiLWZlNTQtNTNmNy04MDMxLTJkZGNmYmFkMjVhOSIsImNyZWF0ZWQiOjE3MDg5NDkwMTA0MDQsImV4aXN0aW5nIjpmYWxzZX0=',
    #     '_ga_X043SN5YW8': 'GS1.1.1708949010.1.1.1708949020.0.0.0',
    #     'dhhPerseusSessionId': '1709125057508.000000002204925883.0000gr83ec',
    #     'pxcts': '97a97534-d6ac-11ee-82a5-930c999a207e',
    #     '_gid': 'GA1.3.1323203548.1709304855',
    #     '__Secure-peya.sid': 's%3A018a0644-cda2-4d06-baff-6590c72776ec.2qXmwcT8PQq1y%2Fp1ZcsK2QekDkXXHDEX%2FYbt%2FYZ4c2c',
    #     '__Secure-peyas.sid': 's%3A7300fd4e-a9f4-494d-bcea-ea192f1fe1a1.n4ZY6c5R0S9OfJpZmds8ouch3pd9n5I%2FoxQ69KzoYBI',
    #     'ab.storage.deviceId.8f8614b7-a682-4b80-af4e-c133abb05875': '%7B%22g%22%3A%22ce28fcf0-d9c5-c602-7a48-fcdbd93b6af5%22%2C%22c%22%3A1708948054261%2C%22l%22%3A1709472918541%7D',
    #     'ab.storage.userId.8f8614b7-a682-4b80-af4e-c133abb05875': '%7B%22g%22%3A%22%5Bobject%20Object%5D%22%2C%22c%22%3A1709098012503%2C%22l%22%3A1709472918541%7D',
    #     'AMP_TOKEN': '%24NOT_FOUND',
    #     '_pxhd': 'sVIVRW5K39nvOAZ-pvmm0bcejI4E06hH1qNDbaclXiBo-bxKa9jdj6QxabU3WEuKSs16eP-BHcnw6hWV7ltOgQ==:8o37lEcXPLZeMJOwihM0h8uGGl1MuyJBu8GX7y-tMTOELa-povxkp9TUePg9eSw4KSjVl9xy2MgO7krymjQRL/xnEiyBCAyd3jpS4yOR8lQckVKk3rl0uOemwkfQ2q0dEFr2CVNyb0Fy06WelbVQDA==',
    #     '__cf_bm': 'ps9ZmSbbp6AcxjI7P7NjkkwiSsLS3Trzyplk0WmS4gY-1709472946-1.0.1.1-LlHOoUbAPZH3_7rh9UUDB3BtncBdIYjbEddwiMxbzkfVlrHjE_KSmfTN08hy6vwjLnyMTyMiSUG.j27mF4XYYA',
    #     '_gat_WD2_Tracker_PeYa_Prod': '1',
    #     '_tq_id.TV-81819090-1.20dc': 'a40b1f42db6ebd8d.1708948048.0.1709473240..',
    #     'dhhPerseusHitId': '1709473252986.000000000732791516.0001chwhn6',
    #     '_px3': '0e4e5361a532473fb937c68e3f67a6db434ad6768f8a20b5e51dde8c26653e8e:HqlprlMQHcygrfrvDppwUJHDVikpKHv4m5zroHP45g0bkk0rfMkVl7djnc+ND0MlU1tCFSPS9/H/wZiplwX8rA==:1000:5szJqXz7ncfCyxNvp1mByFyoGqvg/yCrnQH+U6j+1/Sv4U2jj0DUPylWcNULN8C7OsrY6385KqGo6H9vVcJG5l0voIiLml+tFb+grefGfeYhLCq3TUprcOb8Ba9ScqIV3pALyQWNPpctHxuX0J6Z+tk/YUxHUiG78ONTsgUfdCyDU6QWmVUH5zfp1qfu+ii0dnWbjekN13fETOslqGG+lUPfFQP5unl49X8OVWeTz3w=',
    #     '_ga_LQWR31SY8G': 'GS1.1.1709472918.24.1.1709473273.17.0.0',
    #     '_ga': 'GA1.1.1803347457.1708948047',
    #     '_uetsid': '92c2b9f0d7db11ee97a4cb9956167c3c',
    #     '_uetvid': 'd0a51ce0d49c11ee9826e507d905416b',
    #     'ab.storage.sessionId.8f8614b7-a682-4b80-af4e-c133abb05875': '%7B%22g%22%3A%22a41c8cdf-c4bf-f86e-600c-8e01c8f246d8%22%2C%22e%22%3A1709475073634%2C%22c%22%3A1709472918540%2C%22l%22%3A1709473273634%7D',
    # }

    headers = {
        'authority': host_url,
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6',
        'baggage': 'sentry-environment=live,sentry-release=peya-web%402.0.90,sentry-public_key=b015b29cb0524fa6a58705cc439e4075,sentry-trace_id=6f4c2566aa7f4749924bcc99c5d67fad',
        'content-type': 'application/json;charset=UTF-8',
        'origin': host_url,
        'referer': 'https://www.pedidosya.com.ar/restaurantes?bt=RESTAURANT&origin=home&lat=-24.77554&lng=-65.45031&areaId=20339&areaName=20339&address=Almafuerte%203334&city=Salta',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sentry-trace': '6f4c2566aa7f4749924bcc99c5d67fad-985bd47845a80ab8-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    json_data = {'vendors': vendor_id_list}

    vendor_response = requests.post('https://www.pedidosya.com.ar/v1/food-home/v1/vendors', headers=headers, json=json_data)
    vendor_response.raise_for_status()
    json_response = vendor_response.json()
    return json_response

def extraction(area_name,country_code,host_url):
    global vendor_details
    print(f'Fetching places id for provided area name:{area_name}')
    descri = first_extraction(area_name,country_code,host_url)
    placeId,placeType = descri['place_id'], descri['place_type'],
    if descri:
        print(f'Fetching places lat and long for area:{area_name}')
        place_info = second_extraction(placeId,placeType,host_url)
        all_listings = []
        details, cnt = third_extraction(lat=place_info['latitude'], long=place_info['longitude'],countryId=place_info['countryId'], host_url=host_url)
        all_listings.extend(details)
        if cnt > len(details):
            all_listings = []
            all_details, cnt = third_extraction(lat=place_info['latitude'], long=place_info['longitude'],
                                                    countryId=place_info['countryId'], size=cnt, host_url=host_url)
            all_listings.extend(all_details)

        if all_listings:
            vendor_list = ([ele['id'] for ele in all_listings])
            vendor_details = venderos(vendor_list, host_url=host_url)

        with open(f'vendor_listing_{country_code}.json', 'w+') as _file:
            json.dump(all_listings, _file)
        with open(f'vendor_details_{country_code}.json', 'w+') as _file:
            json.dump(vendor_details, _file)



if __name__ == '__main__':
    host_url="https://www.pedidosya.com.ar"
    area_name = "Almafuerte 3334, Salta, Salta, Argentina"
    country_code = 'ar'
    extraction(area_name,country_code,host_url)

