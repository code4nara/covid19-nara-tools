#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import sys
import datetime
from pathlib import Path
import argparse

sys.path.append(str(Path('__file__').resolve().parent))

# Template, File, Directory
DATA_DIR = './data'
SRC1_FILE = '奈良県_01新型コロナウイルス感染者_患者リスト.xlsx'
SHEET1_NAME = '奈良県_01新型コロナウイルス感染者_患者リスト'
SRC2_FILE = '奈良県_02新型コロナウイルス感染者_患者集計表.xlsx'
SHEET2_NAME = '奈良県_02新型コロナウイルス感染者_患者集計表'

DEST1_FILE = 'data.json'
DEST2_FILE = 'sickbeds_summary.json'

TAB = ['', '  ', '    ', '      ', '        ', '          ', '            ',
       '              ', '                ', '                    ']

def load_patient_list(fname):
    df_list = pd.read_excel(fname, sheet_name=SHEET1_NAME, header=None)
    # 最終更新日時
    last_update = pd.to_datetime(df_list.iloc[0][1], format='%Y/%m/%d %H:%M')
    # 必要なデータのみに加工
    df_list = df_list.drop(0)
    df_list.columns = df_list.iloc[0]
    df_list = df_list.drop(1)
    df_list = df_list.drop(['全国地方公共団体コード', '都道府県名', '発症_年月日'], axis=1)
    # 日付 : object型→datetime型
    df_list['公表_年月日'] = pd.to_datetime(df_list['公表_年月日'], format='%Y/%m/%d')
    # NaNの置換
    df_list['備考'] = df_list['備考'].fillna('')
    return last_update, df_list

def load_patient_summary(fname):
    df_summary = pd.read_excel(fname, sheet_name=SHEET2_NAME, header=None)
    # 最終更新日
    last_update = pd.to_datetime(df_summary.iloc[0][1])
    # 必要なデータのみに加工
    df_summary = df_summary.drop(0)
    df_summary.columns = df_summary.iloc[0]
    df_summary = df_summary.drop(1)
    df_summary = df_summary.drop(['全国地方公共団体コード', '都道府県名', '備考'], axis=1)
    # 日付 : object型→datetime型
    df_summary['公表_年月日'].replace(to_replace=r'(\d{4}).?(\d{2}).?(\d{2})', value=r"\1-\2-\3", regex=True, inplace=True)
    df_summary['公表_年月日'] = pd.to_datetime(df_summary['公表_年月日'])
    # NaNの置換
    df_summary[['陽性確認_件数', '陽性確認_件数_累計', '入院者数_累計', '入院者数', '入院者中の患者数', '入院者中の無症状病原体保有者数', '死亡者_累計', '退院者_累計', '感染症対応病床数']] = df_summary[['陽性確認_件数', '陽性確認_件数_累計', '入院者数_累計', '入院者数', '入院者中の患者数', '入院者中の無症状病原体保有者数', '死亡者_累計', '退院者_累計', '感染症対応病床数']].fillna(0)
    return last_update, df_summary

def output_patients_list(f, last_update, patients):
    f.write(TAB[1] + '"patients":{\n')
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"data": [\n')
    for i in range(len(patients.index)):
        patient = patients.iloc[i]
        f.write(TAB[3] + '{\n')
        f.write(TAB[4] + '"No": {},\n'.format(patient['No']))
        f.write(TAB[4] + '"発表日": "{}",\n'.format(str(patient['公表_年月日'].date()) + 'T08:00:00.000Z'))
        f.write(TAB[4] + '"住居地": "{}",\n'.format(patient['患者_居住地']))
        f.write(TAB[4] + '"年代": "{}",\n'.format(patient['患者_年代']))
        f.write(TAB[4] + '"性別": "{}",\n'.format(patient['患者_性別']))
        f.write(TAB[4] + '"備考": "{}"\n'.format(patient['備考']))
        if i == (len(patients.index) - 1):
            f.write(TAB[3] + '}\n')
        else:
            f.write(TAB[3] + '},\n')
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')

def output_patients_summary(f, last_update, summary):
    f.write(TAB[1] + '"patients_summary":{\n')
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"data": [\n')
    start = datetime.datetime(2020, 1, 24, 0, 0, 0)
    end = last_update + datetime.timedelta(days=1)
    period = (end - start).days
    for i in range(period):
        d = start + datetime.timedelta(days=i)
        idx = list(summary['公表_年月日'][summary['公表_年月日'] == d].index)
        if len(idx) == 1:
            num = summary['陽性確認_件数'][idx[0]]
        else:
            num = 0
        f.write(TAB[3] + '{\n')
        f.write(TAB[4] + '"日付": "{}",\n'.format(str(d.date()) + 'T08:00:00.000Z'))
        f.write(TAB[4] + '"小計": {}\n'.format(num))
        if i == (period - 1):
            f.write(TAB[3] + '}\n')
        else:
            f.write(TAB[3] + '},\n')
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')

def output_main_summary(f, last_update, summary):
    last_data = summary.iloc[len(summary.index)-1]
    f.write(TAB[1] + '"main_summary":{\n')
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"attr": "検査実施人数",\n')
    f.write(TAB[2] + '"value": 0,\n')
    f.write(TAB[2] + '"children": [\n')
    f.write(TAB[3] + '{\n')
    f.write(TAB[4] + '"attr": "陽性患者数",\n')
    f.write(TAB[4] + '"value": {},\n'.format(last_data['入院者数_累計']))
    f.write(TAB[4] + '"children": [\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "入院患者数",\n')
    f.write(TAB[6] + '"value": {},\n'.format(last_data['入院者数']))
    f.write(TAB[6] + '"children": [\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "症状のない方",\n')
    f.write(TAB[8] + '"value": {}\n'.format(last_data['入院者中の無症状病原体保有者数']))
    f.write(TAB[7] + '},\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "症状のある方",\n')
    f.write(TAB[8] + '"value": {}\n'.format(last_data['入院者中の患者数']))
    f.write(TAB[7] + '}\n')
    f.write(TAB[6] + ']\n')
    f.write(TAB[5] + '},\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "退院した方",\n')
    f.write(TAB[6] + '"value": {}\n'.format(last_data['退院者_累計']))
    f.write(TAB[5] + '},\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "亡くなられた方",\n')
    f.write(TAB[6] + '"value": {}\n'.format(last_data['死亡者_累計']))
    f.write(TAB[5] + '}\n')
    f.write(TAB[4] + ']\n')
    f.write(TAB[3] + '}\n')
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')
    
def output_data_json(fname, list_last_update, df_list, summary_last_update, df_summary):
    fileobj = open(fname, 'w', encoding = 'utf_8')
    fileobj.write('{\n')
    # 表示用データ
    output_patients_list(fileobj, list_last_update, df_list)
    output_patients_summary(fileobj, summary_last_update, df_summary)
    output_main_summary(fileobj, summary_last_update, df_summary)

    fileobj.write(TAB[1] + '"lastUpdate": "{}"\n'.format(summary_last_update.strftime('%Y/%m/%d %H:%M')))
    fileobj.write('}\n')
    fileobj.close()

def output_sickbeds_json(fname, last_update, summary):
    last_data = summary.iloc[len(summary.index)-1]
    fileobj = open(fname, 'w', encoding = 'utf_8')
    fileobj.write('{\n')
    fileobj.write(TAB[1] + '"data": {\n')
    fileobj.write(TAB[2] + '"入院患者数": {},\n'.format(last_data['入院者数']))
    fileobj.write(TAB[2] + '"残り病床数": {}\n'.format(last_data['感染症対応病床数'] - last_data['入院者数']))
    fileobj.write(TAB[1] + '},\n')
    fileobj.write(TAB[1] + '"last_update": "{}"\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    fileobj.write('}\n')
    fileobj.close()

    
def main(args):
    list_last_update, df_list = load_patient_list(args.list)
    print(list_last_update, len(df_list.index))
    print(df_list.head())
    summary_last_update, df_summary = load_patient_summary(args.summary)
    print(summary_last_update, len(df_summary.index))
    print(df_summary.head())
    # output data.json
    output_data_json(args.data, list_last_update, df_list, summary_last_update, df_summary)
    output_sickbeds_json(args.beds, summary_last_update, df_summary)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    help_ = 'Patient list file'
    parser.add_argument('-l', '--list', help=help_, default=os.path.join(DATA_DIR, SRC1_FILE))
    help_ = 'Patient summary file'
    parser.add_argument('-s', '--summary', help=help_, default=os.path.join(DATA_DIR, SRC2_FILE))
    help_ = 'Data file'
    parser.add_argument('-d', '--data', help=help_, default=os.path.join(DATA_DIR, DEST1_FILE))
    args = parser.parse_args()
    help_ = 'Sickbeds file'
    parser.add_argument('-b', '--beds', help=help_, default=os.path.join(DATA_DIR, DEST2_FILE))
    args = parser.parse_args()
    main(args)
