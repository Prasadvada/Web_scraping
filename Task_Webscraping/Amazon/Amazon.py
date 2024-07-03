from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})
        # Inner NavigatableString Object
        title_value = title.text
        # Title as a string value
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string
def get_price(soup):
    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price
# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available



if __name__ == '__main__':
    # add your user agent
    HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})
    URL = "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"
    webpage = requests.get(URL, headers=HEADERS)
    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
    # Store the links
    links_list = []
    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))
        print(links_list)
    d = {"title": [], "price": [], "availability": []}
    # Loop for extracting product details from each link
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        print("https://www.amazon.com"+link)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        # soup = BeautifulSoup(response.text, 'html.parser')
        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['availability'].append(get_availability(new_soup))
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)