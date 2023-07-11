""" BS4 crawler """

import bs4
import requests
import re
# import yaml

# pip install pyyaml - cuz yam package is pyyaml

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept-Language': 'en-US, en;q=0.5'})

URL = "https://www.amazon.com/Saitek-X52-Flight-System-Controller/dp/B000LQ4HTS/ref=sr_1_1?keywords=saitek+x52&qid=1689096103&rnid=2941120011&s=videogames&sprefix=saite%2Caps%2C222&sr=1-1"
# URL = "https://www.amazon.com/CeraVe-Retinol-Smoothing-Brightening-Fragrance/dp/B07XJ7XWLW/?_encoding=UTF8&pd_rd_w=G1ID7&content-id=amzn1.sym.3f4ca281-e55c-46d1-9425-fb252d20366f&pf_rd_p=3f4ca281-e55c-46d1-9425-fb252d20366f&pf_rd_r=01VQ3ZKZN8NV2KCG00DH&pd_rd_wg=nBvkB&pd_rd_r=72324b8d-8801-46ba-acd4-450f0f39d0a0&ref_=pd_gw_exports_top_sellers_unrec"
webpage = requests.get(URL, headers=HEADERS)

soup = bs4.BeautifulSoup(webpage.content, "lxml")

# title = soup.find("span", attrs={"id":'productTitle'})
# print(title.string.strip())


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


# print(get_availability(soup))


print("Product Title =", get_title(soup))
print("Product Price =", get_price(soup))
print("Availability =", get_availability(soup))
