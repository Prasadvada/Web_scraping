from bs4 import BeautifulSoup
import requests
import pandas as pd
sample_data = []
for page in range(1,7):
  url = "https://www.scrapethissite.com/pages/forms/?page_num=" +str(page)+'&per_page=100'

  print(url)
  furl = requests.get(url)
  jsoup = BeautifulSoup(furl.content, 'html.parser')
  # jsoup = BeautifulSoup(furl.content,'html.parser')
  products = jsoup.find_all('tr',{'class' :'team'})
  for product in products:
      try:
          sample_dic = {}
          sample_dic['Name'] = product.find('td' , class_="name").text.replace('\n', '').strip()
          sample_dic['Price'] = product.find('td' , class_= "year").text.replace('\n', '').strip()
          sample_dic['Rating'] = product.find('td', class_='wins').text.replace('\n', '').strip()
          sample_data.append(sample_dic)
      except:
          pass
df = pd.DataFrame(sample_data)
print(df)
df.to_dict()
df.to_csv('data.csv', index=False, header=True)