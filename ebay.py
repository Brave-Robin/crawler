""" BS4 crawler """

import sqlite3
import requests
import yaml
import bs4


# # pip install pyyaml - cuz yam package is pyyaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept-Language': 'en-US'})
main_url = config['URL']
parser_type = config['ParserType']
title = config['TITLE']
price = config['PRICE']
availability = config['AVAILABILITY']


def get_content(search_url):
    """
    :type search_url: string
    :param search_url: ebay search url
    :return: webpage content
    """
    return requests.get(search_url, headers=headers, timeout=5).content


def get_url_with_max_items(input_url):
    """
    :param input_url: main URL to split pages URLs
    :return: new url with max items per page
    """
    split_url = input_url.split("&")
    new_url = ""
    page_counter = False
    for particle in split_url:
        if particle.find("_ipg") != -1:
            particle = "_ipg=240"
            page_counter = True
        if new_url == "":
            new_url = particle
        else:
            new_url = new_url + "&" + particle
    if page_counter:
        return new_url
    return new_url + "&_ipg=240"


def get_pages(url):
    """
    :param url: main URL for scrape content
    :return: list of URLs for each pages
    """
    total_items = bs4.BeautifulSoup(get_content(get_url_with_max_items(url)),
                                    parser_type).select_one(
        '.srp-controls__count-heading > span:nth-child(1)').string.strip()
    item_per_page = 240
    total_items = total_items.replace(",", "").replace('\xa0', '')
    total_pages = min(int(total_items) / int(item_per_page), 42)
    page_list = []
    global total_elements
    total_elements = min((total_pages * item_per_page), 10_000)
    print(f"Total elements: {total_elements}")
    for page in range(1, int(total_pages) + 1):
        each_url = get_url_with_max_items(url) + "&_pgn=" + str(page)
        page_list.append(each_url)
    return page_list


def get_info(url, db_storage: bool = True):
    """
    :param db_storage: true if DB enable
    :param url: link to page
    :return: dictionary for each item
    """
    item_dic = {}
    if db_storage:
        con = sqlite3.connect("ebay.sqlite")
        cur = con.cursor()

    try:
        item_dic['title'] = bs4.BeautifulSoup(get_content(url), parser_type).select_one(
            title).string.strip()
    except AttributeError:
        item_dic['title'] = "No data"
    try:
        item_dic['price'] = bs4.BeautifulSoup(get_content(url), parser_type).select_one(
            price).string.strip()
    except AttributeError:
        item_dic['price'] = "No data"
    try:
        item_dic['availability'] = bs4.BeautifulSoup(get_content(url), parser_type).select_one(
            availability).string.strip()
    except AttributeError:
        item_dic['availability'] = "No data"
    if db_storage:
        if cur.execute("SELECT 1 FROM storage WHERE url = ?", [url]).fetchone():
            if not cur.execute("SELECT 1 FROM storage WHERE title = ? AND price = ? AND availability = ?",
                               (item_dic['title'],
                                item_dic['price'], item_dic['availability'])).fetchone():
                print("Need update")
                cur.execute("UPDATE storage SET title = ?, price = ?, availability = ? WHERE url = ?",
                            (item_dic['title'], item_dic['price'], item_dic['availability'], url))
        else:
            cur.execute("INSERT INTO storage (url, title, price, availability) VALUES (?, ?, ?, ?)",
                        (url, item_dic['title'], item_dic['price'], item_dic['availability']))
            con.commit()
    return item_dic


def get_links(url):
    """
    :param url: search URL
    :return: list of URLs
    """
    listings = bs4.BeautifulSoup(requests.get(url, headers=headers, timeout=5).content, parser_type).select("li a")
    links_list = []
    for a_tag in listings:
        errors = 0
        try:
            link = a_tag["href"]
        except LookupError:
            errors += 1
        if errors == 0:
            if link.startswith("https://www.ebay.com/itm/"):
                links_list.append(link)
    del links_list[::2]
    return links_list


def get_each_items_data(url, db_storage: bool = True):
    """
    :param db_storage: true if DB enable
    :param url: link to page
    :return: list of links
    """
    result_list_data = []
    counter = 0
    for link in get_links(url):
        print(f"{counter + 1}/{total_elements}")
        counter += 1
        if db_storage:
            get_info(link)
        else:
            result_list_data.append(get_info(link))
    return result_list_data


print(list(map(get_each_items_data, get_pages(main_url))))
