import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
response1=requests.get("//www.amazon.in/Lenovo-Calling-Tab-2GB-32GB/dp/B08DD7VT8P/ref=lp_4363894031_1_1?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D", headers={"Content-Type":"text"})
baseurl = "https://www.amazon.in/Lenovo-Calling-Tab-2GB-32GB/dp/B08DD7VT8P/ref=lp_4363894031_1_1?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"
headers = {"cookie": "CONSENT=YES+cb.20230531-04-p0.en+FX+908"}
result = requests.get(url=baseurl, headers=headers)
soup = BeautifulSoup(result.text, 'html.parser')
def get_dat(url):
    response = requests.get(url)
    resp = fromstring(response.text)
    print(resp)
    row =resp.xpath("//h4[.='Company Details']/following-sibling::table//tr")
    details ={}
    for i in row:
        data =[''.join([ele.strip() for ele in e.itertext()]) for e in i.xpath('./td')]
        # print(data)
        details.update({data[0]:data[1]})
    print(details)

        # compa = i.xpath('./td/text')
        # print(compa)

# import requests
# from lxml.html import fromstring
# url ='//www.zaubacorp.com/company/PURO-WELLNESS-PRIVATE-LIMITED/U74999GJ2016PTC092776'
# def get_dat(url):
#     response = requests.get(url)
#     resp = fromstring(response.text)
#     print(resp)
#     row =resp.xpath("//h4[.='Company Details']/following-sibling::table//tr")
#     details ={}
#     for i in row:
#         data =[''.join([ele.strip() for ele in e.itertext()]) for e in i.xpath('./td')]
#         # print(data)
#         details.update({data[0]:data[1]})
#     print(details)
#
#         # compa = i.xpath('./td/text')
#         # print(compa)
#
# get_dat(url)
