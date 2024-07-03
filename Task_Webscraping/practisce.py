from pprint import pprint
import pytesseract
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance
from urllib3 import disable_warnings
from urllib3 import disable_warnings

disable_warnings()

pytesseract.pytesseract.tesseract_cmd = (
    "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

session = requests.Session()
res = session.get(
    "https://bbmptax.karnataka.gov.in/Forms/PrintForms.aspx?rptype=3", verify=False
)
cookies = res.cookies.get_dict()
with open("page1.html", "wb") as file:
    file.write(res.content)
soup = BeautifulSoup(res.content, "lxml")
form_data_1 = {}
for i in soup.find_all("input", {"type": "hidden"}):
    form_data_1[i["name"]] = i.get("value") if i.get("value") else ""
form_data_1.update(
    {
        "__EVENTTARGET": "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtApp",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__SCROLLPOSITIONX": "0",
        "__SCROLLPOSITIONY": "0",
        "ctl00$ctl00$ContentPlaceHolder1$ddlLanguages": "en-us",
        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtApp": "1600000057",
        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtCaptcha": "",
    }
)


form_data_2 = dict(sorted(form_data_1.items()))

params = (("rptype", "3"),)
response = session.post(
    "https://bbmptax.karnataka.gov.in/Forms/PrintForms.aspx?rptype=3",
    # headers=headers,
    data=form_data_2,
    verify=False,
    cookies=cookies,
)
soup = BeautifulSoup(response.content, "lxml")
# print(soup.select_one("#ContentPlaceHolder1_ContentPlaceHolder1_ddlAsses"))
# with open("page2.html", "wb") as file:
#     file.write(response.content)
form_data_2 = {}
for i in soup.find_all("input", {"type": "hidden"}):
    form_data_2[i["name"]] = i.get("value") if i.get("value") else ""


captcha_link = f'https://bbmptax.karnataka.gov.in/Forms/{soup.select_one("#ContentPlaceHolder1_ContentPlaceHolder1_panel1 table img").get("src")}'
print(captcha_link)

captcha_res = session.get(captcha_link, cookies=cookies, verify=False)
with open("captcha.png", "wb") as file:
    file.write(captcha_res.content)

img = Image.open("captcha.png")
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(2.5)
captcha_text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
captcha_text = captcha_text.replace(".", "").strip().replace(" ", "")
captcha_text


form_data_2.update(
    {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__SCROLLPOSITIONX": "0",
        "__SCROLLPOSITIONY": "0",
        "__VIEWSTATEENCRYPTED": "",
        "ctl00$ctl00$ContentPlaceHolder1$ddlLanguages": "en-us",
        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtApp": "1600000057",
        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$ddlAsses": "2021-2022",
        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtCaptcha": captcha_text,
        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$Button1": "submit",
        "ctl00$ctl00$ContentPlaceHolder1$lblIp": "",
    }
)
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Origin": "https://bbmptax.karnataka.gov.in",
    "Referer": "https://bbmptax.karnataka.gov.in/Forms/PrintForms.aspx?rptype=3",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}
print(captcha_text, "\n\n")
print(list(form_data_2.keys()))
print(cookies)
response = requests.post(
    "https://bbmptax.karnataka.gov.in/Forms/PrintForms.aspx?rptype=3",
    cookies=cookies,
    data=form_data_2,
    verify=False,
    headers=headers,
)

with open("page2.html", "wb") as file:
    file.write(response.content)


response.headers
