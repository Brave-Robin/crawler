""" BS4 crawler """

import bs4
import urllib.request
import yaml

# Read config
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

the_site = urllib.request.urlopen(config['URL']).read()
just_start = bs4.BeautifulSoup(the_site, config['ParserType'])

print(just_start.find_all('a', attrs={'class': 's-item__title'}))

# for paragraph in just_start.find_all('a'):
#     print(paragraph.getText)
