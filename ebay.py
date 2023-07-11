""" BS4 crawler """

import bs4
import requests
# import yaml

# pip install pyyaml - cuz yam package is pyyaml

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US, en;q=0.5'})

URL = "https://www.ebay.com/itm/224954251003?hash=item34605176fb:g:zJQAAOSwXeViZSRD&var=523828589245"
webpage = requests.get(URL, headers=HEADERS)

soup = bs4.BeautifulSoup(webpage.content, "lxml")

# title = soup.select_one('.x-item-title__mainTitle > span:nth-child(1)') # <<= CSS path
# print(title.string.strip())


def get_title(soup):
    try:
        title_string = soup.select_one('.x-item-title__mainTitle > span:nth-child(1)').string.strip()
    except AttributeError:
        title_string = ""
    return title_string

# print(get_title(soup))


def get_price(soup):
    try:
        price = soup.select_one('.x-price-primary > span:nth-child(1)').string
    except AttributeError:
        price = ""
    return price


# print(get_price(soup))
# print(type(get_price(soup)))


def get_availability(soup):
    try:
        available = soup.select_one('.d-quantity__availability > div:nth-child(1) > span:nth-child(1)').string.strip()
    except AttributeError:
        available = ""
    return available


# print(get_availability(soup))

print("Product Title =", get_title(soup))
print("Product Price =", get_price(soup))
print("Availability =", get_availability(soup))
