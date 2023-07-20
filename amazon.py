""" BS4 crawler """

import bs4
import requests
from PIL import Image
import urllib.request
# import re
# import yaml

# pip install pyyaml - cuz yam package is pyyaml


def get_title(soup):
    try:
        title_string = soup.find("span", attrs={"id": 'productTitle'}).string.strip()
    except AttributeError:
        title_string = ""
    return title_string


# print(get_title(soup))


def get_price(soup):
    try:
        price = soup.select_one('span.a-price:nth-child(2) > span:nth-child(1)').string
    except AttributeError:
        price = ""
    return price


# print(get_price(soup))
# print(type(get_price(soup)))


def get_availability(soup):
    try:
        available = soup.select_one('#availability > span:nth-child(1)').string.strip()
    except AttributeError:
        available = ""
    return available



def get_image(soup):
    try:
        pictures = soup.find_all("img", attrs={"id": 'landingImage'})
    except AttributeError:
        pictures = ""

    for picture in pictures:
        link = picture['src']
        urllib.request.urlretrieve(link, "amazon.jpg")
        i = Image.open('amazon.jpg')
        return i.show()








# print(get_availability(soup))


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US, en;q=0.5'})

URL = "https://www.amazon.com/s?k=saitek+x52&rh=n%3A402045011&ref=nb_sb_noss"
# URL = "https://www.amazon.com/s?k=Facial+Treatments+%26+Masks&rh=n%3A11062031&ref=nb_sb_noss"
webpage = requests.get(URL, headers=HEADERS)

soup = bs4.BeautifulSoup(webpage.content, "lxml")

pages = soup.find_all("a", attrs={'class':"a-link-normal s-no-outline"})

page_list = []


for page in pages:
    page_list.append(page.get('href'))


for page in page_list:
    new_webpage = requests.get("https://www.amazon.com" + page, headers=HEADERS)
    new_soup = bs4.BeautifulSoup(new_webpage.content, "lxml")


    print("Product Title =", get_title(new_soup))
    print("Product Price =", get_price(new_soup))
    print("Availability =", get_availability(new_soup))
    print(get_image(new_soup))
    print("")
