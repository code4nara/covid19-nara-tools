#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import requests
import lxml
from bs4 import BeautifulSoup
import pandas as pd
import collections as cl
import json
import codecs
import argparse
import re

import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))

# 奈良県公式HP URL
NARA_PREF_URL = 'http://www.pref.nara.jp/'
NARA_PREF_JSON_FILE = './data/news.json'
NARA_PREF_BASE_URL = 'http://www.pref.nara.jp/'

# 奈良市公式HP URL
NARA_CITY_URL = 'https://www.city.nara.lg.jp/'
NARA_CITY_JSON_FILE = './data/news_naracity.json'
NARA_CITY_BASE_URL = 'https://www.city.nara.lg.jp'

# 奈良県のトップページのパース
def parse_pref_page(page):
    headerPane = page.find(name='div', attrs={'class': 'LinkList_Standard_em'})
    items = headerPane.select('a[id*="TitleLink"]')
    return items

# 奈良県のニュースのパース
def parse_pref_item(item):
    # 令和 → 西暦
    sep_keys = ['令和', '年', '月', '日）']
    str = item.string
    for key in sep_keys:
        str = str.replace(key, ',')
    elem = str.split(',')
    date = '20{}/{}/{}'.format(int(elem[1]) + 18, elem[2], elem[3])
    # タイトル 
    text = elem[4]
    # 相対 → 絶対
    str = item.attrs['href']
    str = str.replace('#module', ',')
    elem = str.split(',')
    if elem[0].startswith('http'):
        url = elem[0]
    else:
        url = NARA_PREF_BASE_URL + elem[0]
    print(date, url, text)
    return date, url, text

# 奈良県のjsonファイル作成
def make_pref_json(items, filename):
    list = []
    print(len(items))
    for i, item in enumerate(items):
        date, url, text = parse_pref_item(item)
        elem = cl.OrderedDict({"date": date, "url": url, "text": text})
        list.append(elem)
    data = cl.OrderedDict({"newsItems": list})
    jsonFile = codecs.open(filename, 'w', 'utf-8')
    json.dump(data, jsonFile, ensure_ascii=False)

# 奈良市のトップページのパース
def parse_city_page(page):
    important = page.find(name='div', attrs={'id': 'top_important'})
    titles = important.find_all(name='span', attrs={'class': 'article_title'})
    dates = important.find_all(name='span', attrs={'class': 'article_date'})
    # for i in range(len(titles)):
    #    print(dates[i].string, titles[i].find('a').string)
    return dates, titles

# 奈良市のニュースのパース
def parse_city_item(date, title):
    sep_keys = ['年', '月', '日', '更新']
    str = date.string
    for key in sep_keys:
        str = str.replace(key, ',')
    elem = str.split(',')
    date = '{}/{}/{}'.format(elem[0], elem[1], elem[2])
    # タイトル 
    text = title.find('a').string
    # 相対 → 絶対
    url = title.find('a').get('href')
    if not url.startswith('http'):
        url = NARA_CITY_BASE_URL + title.find('a').get('href')
    print(date, url, text)
    return date, url, text

# 奈良市のjsonファイル作成
def make_city_json(dates, titles, filename):
    list = []
    for i in range(len(titles)):
        date, url, text = parse_city_item(dates[i], titles[i])
        elem = cl.OrderedDict({"date": date, "url": url, "text": text})
        list.append(elem)
    data = cl.OrderedDict({"newsItems": list})
    jsonFile = codecs.open(filename, 'w', 'utf-8')
    json.dump(data, jsonFile, ensure_ascii=False)

def main(args):
    # 奈良県
    response = requests.get(NARA_PREF_URL)
    page = BeautifulSoup(response.content, 'lxml')
    items = parse_pref_page(page)
    make_pref_json(items, args.pref)

    # 奈良市
    response = requests.get(NARA_CITY_URL)
    page = BeautifulSoup(response.content, 'lxml')
    dates, titles = parse_city_page(page)
    make_city_json(dates, titles, args.city)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    help_ = 'Nara pref json file'
    parser.add_argument('-p', '--pref', help=help_, default=NARA_PREF_JSON_FILE)
    help_ = 'Nara city json file'
    parser.add_argument('-c', '--city', help=help_, default=NARA_CITY_JSON_FILE)
    args = parser.parse_args()
    main(args)
