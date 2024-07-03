import requests
import pandas as pd
sample_data = []
a=36
for i in range(0,7):
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    j=a*i
    print(j)
    url =''
    if i==0:
        url = 'https://www2.hm.com/en_in/women/new-arrivals/clothes/_jcr_content/main/productlisting.display.json?sort=stock&image-size=small&image=model&offset=0&page-size=36'
        print(url)
    if i>=1:
        url = f'https://www2.hm.com/en_in/women/new-arrivals/clothes/_jcr_content/main/productlisting.display.json?sort=stock&image-size=small&image=model&offset={j}&page-size=36'
        print(url)
    furl = requests.get(url,headers=HEADERS)
    data = furl.json()
    for item in data['products']:
        sample_dic = {}
        try:
          sample_dic['title'] = item.get('title')
          sample_dic['brand'] = item.get('price')
          sample_data.append(sample_dic)
        except:
            pass

df = pd.DataFrame(sample_data)
print(df)
df.to_dict()
df.to_csv('HM_fashions.csv', index=False, header=True)