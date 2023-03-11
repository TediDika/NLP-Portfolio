import pathlib
import requests
import re
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
import os
from nltk.corpus import stopwords
import string
import math
from nltk.stem import WordNetLemmatizer
import pickle
from pathlib import Path

'''
Starts with a starter page and extracts all links from that page and puts them in a queue. 
Then goes to each link in the queue and scrapes all links and adds them to the queue
'''
def web_crawl():
    starter_url = 'https://en.wikipedia.org/wiki/Attack_on_Titan_(TV_series)'
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    # write urls to a file
    url_list = []
    for link in soup.find_all('a'):
        if len(url_list) > 14:
            break

        link_str = str(link.get('href'))
        if 'Titan' in link_str or 'titan' in link_str and 'manga' not in link_str and 'archive' not in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if 'wikipedia' in link_str and 'en' not in link_str:
                pass
            elif link_str.startswith('http') and 'google' not in link_str:
                url_list.append(link_str)
                print(link_str)
    # end of program
    print("end of crawler")
    return url_list


def scrape_page(urls):

    counter = 1
    for url in urls:
        current_page = requests.get(url)
        current_file = open(('text' + str(counter) + '.txt'), 'w', encoding="utf-8")

        current_soup = BeautifulSoup(current_page.content, 'html.parser')
        for p in current_soup.select('p'):
            current_file.write(p.get_text() + '\n')

        counter += 1

if __name__ == '__main__':
    url_list = web_crawl()
    scrape_page(url_list)
