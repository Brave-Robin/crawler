import bs4
import requests


def get_title(soup):
    try:
        title_string = soup.find("span", attrs={"id": 'productTitle'}).string.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_price(soup):

    try:
        price = soup.select_one('.reinventPricePriceToPayMargin > span:nth-child(1)').string.strip()

    except AttributeError:
        price = ""
    return price


def get_availability(soup):
    try:
        available = soup.select_one('#availability > span:nth-child(1)').string.strip()

    except AttributeError:
        available = ""

    return available



if __name__ == '__main__':


    HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'})

    # URL = "https://www.amazon.com/CASETiFY-Ultra-Impact-Protective-iPhone/dp/B0B8S92NMS/ref=sr_1_1?crid=4SRFN126NMGY&keywords=iphone+14+pro+max&qid=1689268203&sprefix=iphone+14+pro+max%2Caps%2C221&sr=8-1"
    URL = 'https://www.amazon.com/s?k=iphone+14+pro+max&crid=4SRFN126NMGY&sprefix=iphone+14+pro+max%2Caps%2C221&ref=nb_sb_noss_1'
    webpage = requests.get(URL, headers=HEADERS)

    soup = bs4.BeautifulSoup(webpage.content, "lxml")

    links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = []


    for link in links:
        links_list.append(link.get('href'))


    for link in links_list:

        new_website = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = bs4.BeautifulSoup(new_website.content, "lxml")
        print("Product Title =", get_title(new_soup))
        print("Product Price =", get_price(new_soup))
        print("Availability =", get_availability(new_soup))
        print("")

