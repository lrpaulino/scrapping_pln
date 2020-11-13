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
for i in range(1, 21):
    html = get_page(f'https://www.tudogostoso.com.br/receitas?page={i}')
    soup = BeautifulSoup(html, 'html.parser')

    links = links.union({
        'https://www.tudogostoso.com.br' + x.get('href')
        for x in soup.find_all("a", class_="link")
        if x.get('href')
        })

with ThreadPool(processes=32) as pool:
    html_list = pool.map(get_page, links)

contents_culinaria = []
for html in html_list:
    receita = ''
    soup = BeautifulSoup(html, 'html.parser')
    ingredients = [
        x.text
        for x in soup.find_all('span', class_='p-ingredient')
        if x]

    receita += '\n'.join(ingredients)

    instrucoes = soup.find('div', class_='instructions')
    if instrucoes:
        receita += instrucoes.text

    if receita:
        contents_culinaria.append(receita)

df = pd.DataFrame(zip(contents_culinaria, repeat('culinaria')),
                  columns=['Text', 'Context'])

df.to_csv('data.csv', mode='a', index=False)
