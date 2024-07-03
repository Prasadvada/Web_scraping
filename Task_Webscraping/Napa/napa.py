import time
import requests
from Cd_DataExtraction import DataExtractor
b = 300
for j in range(0,17):
    print('row:',j)
    url=''
    if j==0:
        url = f"https://accio.genpt.com/api/v1/core/?site=us&fl=pid%2Ctitle%2Cbrand%2Csale_price%2Cprimary_image%2Cthumb_image%2Curl%2Cdescription%2Cunit_of_measure%2Cproduct_line%2Cline_abbreviation%2Cpart_number%2Cinterchange_parts%2Cuniversal%2Cfield_sku%2Chq_abbrev%2Cregulatory%2Cpriced_from%2Cpriced_to%2Cretail_redirect%2Cretail_url&_br_uid_2=uid%253D5577431256393%253Av%253D15.0%253Ats%253D1683818565428%253Ahc%253D68&request_type=search&search_type=keyword&domain_key=napaonline&url=https%3A%2F%2Fwww.napaonline.com%2Fen%2Fsearch%3Ftext%3DGrote%26referer%3Dv2&facet.range=price&facet.application_part_type.limit=300&q=Grote&view_id=FRE&efq=dc%3A%22FRE%22&rows=300&start=0&sort=relevance+asc"
        print(url)
    elif j>=1:
        row = b * j
        url = f"https://accio.genpt.com/api/v1/core/?site=us&fl=pid%2Ctitle%2Cbrand%2Csale_price%2Cprimary_image%2Cthumb_image%2Curl%2Cdescription%2Cunit_of_measure%2Cproduct_line%2Cline_abbreviation%2Cpart_number%2Cinterchange_parts%2Cuniversal%2Cfield_sku%2Chq_abbrev%2Cregulatory%2Cpriced_from%2Cpriced_to%2Cretail_redirect%2Cretail_url&_br_uid_2=uid%253D5577431256393%253Av%253D15.0%253Ats%253D1683818565428%253Ahc%253D68&request_type=search&search_type=keyword&domain_key=napaonline&url=https%3A%2F%2Fwww.napaonline.com%2Fen%2Fsearch%3Ftext%3DGrote%26referer%3Dv2&facet.range=price&facet.application_part_type.limit=300&q=Grote&view_id=FRE&efq=dc%3A%22FRE%22&rows=300&start={row}&sort=relevance+asc"
        print(url)
    response = requests.get(url)
    data = response.json()
    time.sleep(2)
    DataExtractor(data)

    # Access the extracted data
    # for item in data['response']['docs']:
    #     pid = item.get('pid')
    #     title = item.get('title')
    #     brand = item.get('brand')
    #     sale_price = item.get('sale_price')
    #     primary_image = item.get('primary_image')
    #     thumb_image = item.get('thumb_image')
    #     url = item.get('url')
    #     description = item.get('description')
