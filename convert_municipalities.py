#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import pandas as pd
import sys
from pathlib import Path
import argparse

sys.path.append(str(Path('__file__').resolve().parent))

# Template, File, Directory
TEMPLATE_JSON = './template/municipalities.json'
DATA_DIR = './data'
SRC_FILE = 'municipalities.xlsx'
DEST_FILE = 'municipalities-data.json'


def main(args):
    data = pd.read_json(TEMPLATE_JSON)
    # print(data.head())
    urldata = pd.read_excel(args.input, sheet_name='対策まとめページ',
                            na_values='', keep_default_na=False)
    # print(urldata.head())
    codes = urldata['コード'].tolist()
    for code in codes:
        url = urldata[urldata['コード']==code]['まとめ・対策ページURL'].values
        print(url)
        data[code].href = url[0]
    # json
    data.to_json(args.output)
                  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    help_ = 'Input file'
    parser.add_argument('-i', '--input', help=help_, default=os.path.join(DATA_DIR, SRC_FILE))
    help_ = 'Output file'
    parser.add_argument('-o', '--output', help=help_, default=os.path.join(DATA_DIR, DEST_FILE))
    args = parser.parse_args()
    main(args)
