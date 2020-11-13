# -*- coding: utf-8 -*-

import pandas as pd

import requests
from bs4 import BeautifulSoup

from multiprocessing.pool import ThreadPool
from itertools import repeat


def get_page(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }

    return requests.get(url, headers=header).text


links = set()
for i in range(1, 11):
    html = get_page(f'https://olhardigital.com.br/noticias/{i}')
    soup = BeautifulSoup(html, 'html.parser')

    noticias = soup.find('div', class_='blk-items')

    links = links.union({
        'https:' + x.get('href')
        for x in noticias.find_all('a')
        if x.get('href')
        })

with ThreadPool(processes=32) as pool:
    html_list = pool.map(get_page, links)

contents_tecnologia = []
for html in html_list:
    noticia = ''
    soup = BeautifulSoup(html, 'html.parser')

    titulo = soup.find('h1', class_='mat-tit').text
    noticia += titulo

    paragrafos = [
        x.text
        for x in soup.find('article', class_='mat-container').find_all('p')
        if x
        ]

    noticia += '\n'.join(paragrafos)
    contents_tecnologia.append(noticia)

df = pd.DataFrame(zip(contents_tecnologia, repeat('tecnologia')),
                  columns=['Text', 'Context'])

df.to_csv('data.csv', mode='a', index=False)
