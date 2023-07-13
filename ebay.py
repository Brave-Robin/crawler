import bs4
import requests


def get_title(soup):
    try:
        title_string = soup.select_one('.x-item-title__mainTitle > span:nth-child(1)').string.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_price(soup):

    try:
        price = soup.select_one('.x-price-primary > span:nth-child(1)').string

    except AttributeError:
        price = ""
    return price


def get_availability(soup):
    try:
        available = soup.select_one('.d-quantity__availability > div:nth-child(1) > span:nth-child(1)').string.strip()

    except AttributeError:
        available = ""

    return available


if __name__ == '__main__':


    HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'})

    # URL = "https://www.ebay.com/itm/125533439255?_trkparms=pageci%3A1e0abdd9-2010-11ee-a22e-26dc0c4565fc%7Cparentrq%3A45fdcf511890ad59ed762527ffffb694%7Ciid%3A1"
    URL = 'https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584'
    webpage = requests.get(URL, headers=HEADERS)

    soup = bs4.BeautifulSoup(webpage.content, "lxml")

    links = soup.find_all("a", attrs={'class':'s-item__link'})
    links_list = []


    for link in links:
        links_list.append(link.get('href'))


    for link in links_list:

        new_website = requests.get(link, headers=HEADERS)

        new_soup = bs4.BeautifulSoup(new_website.content, "lxml")
        print("Product Title =", get_title(new_soup))
        print("Product Price =", get_price(new_soup))
        print("Availability =", get_availability(new_soup))
        print("")

