# -*- coding: utf-8 -*-

import pandas as pd

import requests
import urllib.parse
from bs4 import BeautifulSoup

from multiprocessing.pool import ThreadPool
from itertools import count, repeat


def get_page(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }

    return requests.get(url, headers=header).text


links = set()

# alugar
for i in count(1):
    url_params = {'id': 1, 'pagina': i}
    url_params = urllib.parse.urlencode(url_params)
    html = get_page(f'https://www.lukaimoveis.com.br/imoveis.php?{url_params}')
    soup = BeautifulSoup(html, 'html.parser')

    page_links = {
        x.get('href')
        for x in soup.find_all("a", class_="property-link")
        if x.get('href')
        }

    if page_links:
        links = links.union(page_links)
    else:
        break

# comprar
for i in count(1):
    url_params = {'id': 2, 'pagina': i}
    url_params = urllib.parse.urlencode(url_params)
    html = get_page(f'https://www.lukaimoveis.com.br/imoveis.php?{url_params}')
    soup = BeautifulSoup(html, 'html.parser')

    page_links = {
        x.get('href')
        for x in soup.find_all("a", class_="property-link")
        if x.get('href')
        }

    if page_links:
        links = links.union(page_links)
    else:
        break


with ThreadPool(processes=16) as pool:
    html_list = pool.map(get_page, links)

contents_imovel = []
for html in html_list:
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find('div', class_='property-description')
    if element:
        description = element.text[17:].strip()
        contents_imovel.append(description)

df = pd.DataFrame(zip(contents_imovel, repeat('imovel')),
                  columns=['Text', 'Context'])

df.to_csv('data.csv', mode='a', index=False)
