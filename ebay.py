""" BS4 crawler """

import requests
import yaml
import bs4

# # pip install pyyaml - cuz yam package is pyyaml

HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept-Language': 'en-US'})

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def get_content(url, headers):
    """
    :param url:
    :param headers:
    :return:
    """
    return requests.get(url, headers=headers).content


def get_info(url, headers, parsertype, title, price, availability):
    """
    :param url:
    :param headers:
    :param parsertype:
    :param title:
    :param price:
    :param availability:
    :return:
    """
    item_dic = {}
    try:
        item_dic['title'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(config['TITLE']).string.strip()
        item_dic['price'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(
            config['PRICE']).string.strip()
        item_dic['availability'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(
            config['AVAILABILITY']).string.strip()
    except AttributeError:
        title_string = "noway"
    return item_dic


# print(get_info(config['URL'], HEADERS, config['ParserType'], config['TITLE'], config['PRICE'], config['AVAILABILITY']))


def get_links(url, headers, parser_type):
    """
    :param url:
    :param headers:
    :param parser_type:
    :return:
    """
    listings = bs4.BeautifulSoup(requests.get(url, headers=headers).content, parser_type).select("li a")
    links_list = []
    for a in listings:
        errors = 0
        try:
            link = a["href"]
        except(LookupError):
            errors += 1
        if errors == 0:
            if link.startswith("https://www.ebay.com/itm/"):
                links_list.append(link)
    return links_list


print(get_links(config['URL'], HEADERS, config['ParserType']))

#     soup = bs4.BeautifulSoup(webpage.content, config['ParserType'])
# title = soup.select_one(config['TITLE'])

# print(title.string.strip())

# def get_title(soup):
#     try:
#         title_string = soup.select_one('.x-item-title__mainTitle > span:nth-child(1)').string.strip()
#     except AttributeError:
#         title_string = ""
#     return title_string
#
# # print(get_title(soup))
#
#
# def get_price(soup):
#     try:
#         price = soup.select_one('.x-price-primary > span:nth-child(1)').string
#     except AttributeError:
#         price = ""
#     return price
#
#
# # print(get_price(soup))
# # print(type(get_price(soup)))
#
#
# def get_availability(soup):
#     try:
#         available = soup.select_one('.d-quantity__availability > div:nth-child(1) > span:nth-child(1)').string.strip()
#     except AttributeError:
#         available = ""
#     return available
#
#
# # print(get_availability(soup))
#
# print("Product Title =", get_title(soup))
# print("Product Price =", get_price(soup))
# print("Availability =", get_availability(soup))
