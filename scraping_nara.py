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

import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))

# 奈良県公式HP URL
NARA_URL = 'http://www.pref.nara.jp/'
JSON_FILE = './data/news.json'
BASE_URL = 'http://www.pref.nara.jp/'

def parse_item(item):
    # 令和 → 西暦
    sep_keys = ['令和', '年', '月', '日）']
    str = item[0].string
    for key in sep_keys:
        str = str.replace(key, ',')
    elem = str.split(',')
    date = '20{}/{}/{}'.format(int(elem[1]) + 18, elem[2], elem[3])
    # タイトル 
    text = elem[4]
    # 相対 → 絶対
    str = item[0].attrs['href']
    str = str.replace('#module', ',')
    elem = str.split(',')
    url = BASE_URL + elem[0]
    print(date, url, text)
    return date, url, text

def make_json_data(items, filename):
    list = []
    for i, item in enumerate(items):
        date, url, text = parse_item(item)
        elem = cl.OrderedDict({"date": date, "url": url, "text": text})
        list.append(elem)
    data = cl.OrderedDict({"newsItems": list})
    jsonFile = codecs.open(filename, 'w', 'utf-8')
    json.dump(data, jsonFile, ensure_ascii=False)

def main(args):
    response = requests.get(NARA_URL)
    page = BeautifulSoup(response.content, 'lxml')
    # 緊急情報さがす
    items = []
    for i in range(0, 9):
        item = page.select('#H7_1356_BlogList_ctl0{}_TitleLink'.format(i+1))
        if len(item) > 0:
            items.append(item)

    # データ作成
    make_json_data(items, args.output)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    help_ = 'Output file'
    parser.add_argument('-o', '--output', help=help_, default=JSON_FILE)
    args = parser.parse_args()
    main(args)
