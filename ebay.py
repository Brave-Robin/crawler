""" BS4 crawler """
from sqlite3 import Cursor

import requests
import yaml
import bs4
import sqlite3

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


def get_info(url, headers, parser_type, title, price, availability, db_storage: bool = False):
    """
    :param db_storage:
    :param url:
    :param headers:
    :param parser_type:
    :param title:
    :param price:
    :param availability:
    :return:
    """
    item_dic = {}
    if db_storage:
        con = sqlite3.connect("ebay.sqlite")
        cur = con.cursor()
    try:
        item_dic['title'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(
            config['TITLE']).string.strip()
        item_dic['price'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(
            config['PRICE']).string.strip()
        item_dic['availability'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(
            config['AVAILABILITY']).string.strip()
        print(item_dic['title'], item_dic['price'], item_dic['availability'])
        if db_storage:
            cur.execute("INSERT INTO storage VALUES (?,?,?)", (item_dic['title'], item_dic['price'], item_dic['availability']))
            con.commit()
    except AttributeError:
        print("Found error in URL: {}".format(url))
    return item_dic


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
    # TODO Need to fix doubles
    # TODO add pagination
    return links_list


def get_each_items_data(url, headers, parser_type, title, price, availability, db_storage: bool = False):
    """
    :param db_storage:
    :param url:
    :param headers:
    :param parser_type:
    :param title:
    :param price:
    :param availability:
    :return:
    """
    result_list_data = []
    for link in get_links(url, headers, parser_type):
        if db_storage:
            get_info(link, headers, parser_type, title, price, availability, True)
        else:
            result_list_data.append(get_info(link, headers, parser_type, title, price, availability))
    return result_list_data


all_elements_from_page = get_each_items_data(config['URL'], HEADERS, config['ParserType'], config['TITLE'],
                                             config['PRICE'], config['AVAILABILITY'])

# print(all_elements_from_page)
# print(len(all_elements_from_page))
