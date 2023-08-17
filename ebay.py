""" BS4 crawler """
# from sqlite3 import Cursor

import requests
import yaml
import bs4
import re
import sqlite3
# import os.path

# # pip install pyyaml - cuz yam package is pyyaml

HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept-Language': 'en-US'})


# if not os.path.isfile('config.yaml'):
#     con = sqlite3.connect("ebay.sqlite")
#     cur = con.cursor()
#     cur.execute("CREATE TABLE storage(url, title, price, availability)")


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def get_content(url, headers):
    """
    :param url:
    :param headers:
    :return:
    """
    return requests.get(url, headers=headers).content


def get_pages(url, headers, parser_type):
    total_items =  bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one('.srp-controls__count-heading > span:nth-child(1)').string.strip()
    item_per_page = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one('#srp-ipp-menu > button:nth-child(1) > span:nth-child(1) > span:nth-child(1)').string.strip()
    total_items = total_items.replace(",", "")
    total_pages = int(total_items) / int(item_per_page)
    ### LIMIT is 42
    if total_pages > 42:
        total_pages = 42
    page_list = []
    for page in range(1, total_pages + 1):
        each_url = config['URL']+"&_pgn=" + str(page)
        page_list.append(each_url)
    return page_list

print(get_pages(config['URL'], HEADERS, config['ParserType']))


for url in get_pages(config['URL'], HEADERS, config['ParserType']):

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
        except AttributeError:
            item_dic['title'] = "No data"
        try:
            item_dic['price'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(
                config['PRICE']).string.strip()
        except AttributeError:
            item_dic['price'] = "No data"
        try:
            item_dic['availability'] = bs4.BeautifulSoup(get_content(url, headers), config['ParserType']).select_one(
                config['AVAILABILITY']).string.strip()
        except AttributeError:
            item_dic['availability'] = "No data"
        if db_storage:
            if cur.execute("SELECT 1 FROM storage WHERE url = ?", [url]).fetchone():
                if not cur.execute("SELECT 1 FROM storage WHERE title = ? AND price = ? AND availability = ?", (item_dic['title'], item_dic['price'], item_dic['availability'])).fetchone():
                    print("Need update")
                    cur.execute("UPDATE storage SET title = ?, price = ?, availability = ? WHERE url = ?",
                                (item_dic['title'], item_dic['price'], item_dic['availability'], url))
            else:
                cur.execute("INSERT INTO storage (url, title, price, availability) VALUES (?, ?, ?, ?)", (url, item_dic['title'], item_dic['price'], item_dic['availability']))
                con.commit()
        print(item_dic)
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
        del links_list[::2]
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
                get_info(link, headers, parser_type, title, price, availability, db_storage)
            else:
                result_list_data.append(get_info(link, headers, parser_type, title, price, availability))
        return result_list_data


    all_elements_from_page = get_each_items_data(url, HEADERS, config['ParserType'], config['TITLE'],
                                                 config['PRICE'], config['AVAILABILITY'], True)

    print(all_elements_from_page)
    print(len(all_elements_from_page))
