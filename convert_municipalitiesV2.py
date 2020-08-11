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
SRC_SHEETID = "1dQFcgpQqN8JG9V3cLotntp5wKmqaSdWA"

def main(args):
    dataUri = "https://docs.google.com/spreadsheets/d/{0}/export?format=xlsx&id={0}".format( args.gid  )

    data = pd.read_json(TEMPLATE_JSON)
    # print(data.head())
    urldata = pd.read_excel( dataUri, sheet_name='対策まとめページ', na_values='', keep_default_na=False)
    # print(urldata.head())
    codes = urldata['コード'].tolist()
    for code in codes:
        url = urldata[urldata['コード']==code]['まとめ・対策ページURL'].values
        print(url)
        data[code].href = url[0]
    # json
    data.to_json(args.output, force_ascii=False)
    
                  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    help_ = 'GoogleSpreadSheet IDe'
    parser.add_argument('-g', '--gid', help=help_, default=os.path.join(SRC_SHEETID))
    help_ = 'Output file'
    parser.add_argument('-o', '--output', help=help_, default=os.path.join(DATA_DIR, DEST_FILE))
    args = parser.parse_args()
    main(args)
