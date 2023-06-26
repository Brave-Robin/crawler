''' BS4 crawler'''


import bs4
import urllib.request


the_site = urllib.request.urlopen('https://www.ebay.com/b/Apple-Cell-Phone-Cases-and-Covers/20349/bn_319677').read()
just_start = bs4.BeautifulSoup(the_site, 'html.parser')

# print(just_start.find_all('p'))

for paragraph in just_start.find_all('a'):
    print(paragraph)


# Just demo about bs4


# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
