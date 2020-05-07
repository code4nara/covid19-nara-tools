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

SRC_SHEETID = "1qR8Xs1oZXS0Qt7nGkWtpTu1wNQtngdxUVo6pBl_QP-U"
SHEET1_NAME = '01.陽性患者の属性'
#SHEET2_NAME = '入院患者の状況'
SHEET2_NAME = '03.陽性者状況'

DEST1_FILE = 'data_naracity.json'
DEST2_FILE = 'sickbeds_summary.json'

TAB = ['', '  ', '    ', '      ', '        ', '          ', '            ',
       '              ', '                ', '                    ', '                     ']

# 患者リストの読み込み
def load_patient_list( dataUri, sheetName ):
    # ファイルリード／ダウンロード
    df_list = pd.read_excel( dataUri, sheet_name=sheetName, header=None)
    
    # 必要なデータのみに加工
    df_list.columns = df_list.iloc[0]
    df_list = df_list.drop(range(0,1))
    df_list = df_list.drop(['全国地方公共団体コード', '都道府県名', '患者_渡航歴の有無フラグ','患者_退院済フラグ'], axis=1)
    # NaNの置換
    df_list['備考'] = df_list['備考'].fillna('')
    df_list['発症_年月日'] = df_list['発症_年月日'].fillna('')
    df_list['患者_居住地'] = df_list['患者_居住地'].fillna('')
    df_list['患者_職業'] = df_list['患者_職業'].fillna('')
    df_list['患者_状態'] = df_list['患者_状態'].fillna('')
    df_list['患者_症状'] = df_list['患者_症状'].fillna('')
    # 日付 : object型→datetime型
    #df_list['公表_年月日'] = pd.to_datetime(df_list['公表_年月日'], format='%Y/%m/%d')
    #df_list['発症_年月日'] = pd.to_datetime(df_list['発症_年月日'], format='%Y/%m/%d')

    # 最終更新日時 
    last_data = df_list.iloc[len(df_list.index)-1]
    last_update = last_data['公表_年月日']
    
    return last_update, df_list

# 日々更新データの読み込み
def load_patient_summary( dataUri, sheetName ):
    # ファイルリード／ダウンロード
    df_summary = pd.read_excel( dataUri, sheet_name=sheetName, header=None)

    # 必要なデータのみに加工
    df_summary.columns = df_summary.iloc[0]
    df_summary = df_summary.drop(range(0,1))
    
    df_summary['調査_年月日'] = df_summary['調査_年月日'].fillna('')
    df_summary = df_summary[df_summary['調査_年月日'] != '' ]

    # 最終更新日時設定
    last_data = df_summary.iloc[len(df_summary.index)-1]
    last_update = last_data['調査_年月日']

    # NaNの置換
    df_summary['感染者数_累計'] = df_summary['感染者数_累計'].fillna( -1 )
    df_summary['感染者数_現在'] = df_summary['感染者数_現在'].fillna( -1 )
    df_summary['入院者数_現在'] = df_summary['入院者数_現在'].fillna( -1 )
    df_summary['重症者数_現在'] = df_summary['重症者数_現在'].fillna( -1 )
    df_summary['重症者数_現在'] = df_summary['重症者数_現在'].fillna( -1 )
    df_summary['宿泊療養_現在'] = df_summary['宿泊療養_現在'].fillna( -1 )
    df_summary['自宅療養_現在'] = df_summary['自宅療養_現在'].fillna( -1 )
    df_summary['退院者数_累計'] = df_summary['退院者数_累計'].fillna( -1 )
    df_summary['死亡者数_累計'] = df_summary['死亡者数_累計'].fillna( -1 )
    #print(df_summary)

    # 日付 : object型→datetime型
    #df_summary['発表日'] = pd.to_datetime(df_summary['発表日'])
    #print(df_summary.head())

    return last_update, df_summary

# 患者リストの出力
def output_patients_list(f, last_update, patients):
    last_data = patients.iloc[len(patients.index)-1]
    last_update = last_data['公表_年月日']
    
    f.write(TAB[1] + '"patients":{\n')
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[2] + '"data": [\n')
    for i in range(len(patients.index)):
        patient = patients.iloc[i]
        f.write(TAB[3] + '{\n')
        f.write(TAB[4] + '"No": {},\n'.format(patient['No']))
        f.write(TAB[4] + '"発表日": "{}",\n'.format(str(patient['公表_年月日'].date()) + 'T08:00:00.000Z'))
        f.write(TAB[4] + '"住居地": "{}",\n'.format(patient['患者_居住地']))
        f.write(TAB[4] + '"年代": "{}",\n'.format(patient['患者_年代']))
        f.write(TAB[4] + '"性別": "{}",\n'.format(patient['患者_性別']))
        f.write(TAB[4] + '"職業": "{}",\n'.format(patient['患者_職業']))
        f.write(TAB[4] + '"状態": "{}",\n'.format(patient['患者_状態']))
        f.write(TAB[4] + '"症状": "{}",\n'.format(patient['患者_症状']))
        f.write(TAB[4] + '"発症日": "{}",\n'.format(patient['発症_年月日']))
        f.write(TAB[4] + '"備考": "{}"\n'.format(patient['備考']))
        if i == (len(patients.index) - 1):
            f.write(TAB[3] + '}\n')
        else:
            f.write(TAB[3] + '},\n')
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')

# 陽性者発生状況の出力 : 陽性者リストから日々の発生数を計算
def output_patientslist_summary(f, last_update, patients):
    start = datetime.datetime(2020, 1, 24, 0, 0, 0)
    end = last_update + datetime.timedelta(days=1)
    period = (end - start).days
    
    f.write(TAB[1] + '"patients_summary":{\n')
    #f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[2] + '"data": [\n')

    for i in range(period):
        d = start + datetime.timedelta(days=i)
        df = patients[ patients['公表_年月日'] == d]
        cnt =len(df)
        
        f.write(TAB[3] + '{\n')
        f.write(TAB[4] + '"日付": "{}",\n'.format(str(d.date()) + 'T08:00:00.000Z'))
        f.write(TAB[4] + '"小計": {}\n'.format(cnt))
        if i == (period - 1):
            f.write(TAB[3] + '}\n')
        else:
            f.write(TAB[3] + '},\n')
            
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')

# 陽性者発生状況の出力 : 日々データに養成数がある場合はこちら
def output_patients_summary(f, last_update, summary):
    f.write(TAB[1] + '"patients_summary":{\n')
    #f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
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

# 現在（最新）の陽性者状況の出力
def output_main_summary(f, last_update, summary, patient_total ):
    last_data = summary.iloc[len(summary.index)-1]
    f.write(TAB[1] + '"main_summary":{\n')
    #f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[2] + '"attr": "検査実施人数",\n')
    f.write(TAB[2] + '"value": 0,\n')
    f.write(TAB[2] + '"children": [\n')
    f.write(TAB[3] + '{\n')
    f.write(TAB[4] + '"attr": "感染者数累計",\n')
    f.write(TAB[4] + '"value": {},\n'.format( patient_total))
    f.write(TAB[4] + '"children": [\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "現在感染者数",\n')
    f.write(TAB[6] + '"value": {},\n'.format(last_data['感染者数_現在']))
    f.write(TAB[6] + '"children": [\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "入院中",\n')
    f.write(TAB[8] + '"value": {},\n'.format(last_data['入院者数_現在']))
    f.write(TAB[8] + '"children": [\n')
    f.write(TAB[9] + '{\n')
    f.write(TAB[10] + '"attr": "重症",\n')
    f.write(TAB[10] + '"value": {}\n'.format(last_data['重症者数_現在']))
    f.write(TAB[9] + '}\n')
    f.write(TAB[8] + ']\n')
    f.write(TAB[7] + '},\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "宿泊療養",\n')
    f.write(TAB[8] + '"value": {}\n'.format(last_data['宿泊療養_現在']))
    f.write(TAB[7] + '},\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "自宅療養",\n')
    f.write(TAB[8] + '"value": {}\n'.format(last_data['自宅療養_現在']))
    f.write(TAB[7] + '}\n')
    f.write(TAB[6] + ']\n')
    f.write(TAB[5] + '},\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "退院等累計",\n')
    f.write(TAB[6] + '"value": {}\n'.format(last_data['退院者数_累計']))
    f.write(TAB[5] + '},\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "死亡",\n')
    f.write(TAB[6] + '"value": {}\n'.format(last_data['死亡者数_累計']))
    f.write(TAB[5] + '}\n')
    f.write(TAB[4] + ']\n')
    f.write(TAB[3] + '}\n')
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')

def output_sickbeds_summary( f, last_update, summary):
    last_data = summary.iloc[len(summary.index)-1]
    f.write(TAB[1] + '"sickbeds_summary":{\n')
    #f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[2] + '"total": {\n')
    f.write(TAB[3] + '"総病床数": {},\n'.format(last_data['総病床数']))
    f.write(TAB[3] + '"宿泊療養室数": {}\n'.format(last_data['宿泊療養室数']))
    f.write(TAB[2] + '},\n')
    f.write(TAB[2] + '"data": {\n')
    f.write(TAB[3] + '"入院患者数": {},\n'.format(last_data['入院中']))
    f.write(TAB[3] + '"残り病床数": {}\n'.format(last_data['残り病床数']))
    f.write(TAB[2] + '}\n')
    f.write(TAB[1] + '},\n')

# data.jsonの出力
def output_data_json(fname, list_last_update, df_list, summary_last_update, df_summary):
    fileobj = open(fname, 'w', encoding = 'utf_8')
    fileobj.write('{\n')
    # 表示用データ(
    output_patients_list(fileobj, list_last_update, df_list)
    output_patientslist_summary(fileobj, summary_last_update, df_list)
    #output_patients_summary(fileobj, summary_last_update, df_summary)
    output_main_summary(fileobj, summary_last_update, df_summary, len(df_list) )
    #output_sickbeds_summary(fileobj, summary_last_update, df_summary)

    fileobj.write(TAB[1] + '"lastUpdate": "{}"\n'.format( datetime.datetime.now().strftime('%Y/%m/%d %H:%M')))

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
    #fileobj.write(TAB[1] + '"last_update": "{}"\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    fileobj.write(TAB[1] + '"last_update": "{}"\n'.format(last_update.strftime('%Y/%m/%d')))
    fileobj.write('}\n')
    fileobj.close()

def main(args):
    pd.set_option('display.max_columns', 20)

    # patient_list
    datauri = "https://docs.google.com/spreadsheets/d/{0}/export?format=xlsx&id={0}".format( args.gid  )
    list_last_update, df_list = load_patient_list( datauri, args.list )
    print("  ",list_last_update, len(df_list.index))
    #print( df_list.head())
    #print( df_list )
    
    # summary
    datauri = "https://docs.google.com/spreadsheets/d/{0}/export?format=xlsx&id={0}".format( args.gid )
    summary_last_update, df_summary = load_patient_summary( datauri, args.summary )
    print("  ",summary_last_update, len(df_summary.index))
    #print(df_summary.head())

    # output data.json
    output_data_json(args.data, list_last_update, df_list, summary_last_update, df_summary)
    # output_sickbeds_json(args.beds, summary_last_update, df_summary)
    
if __name__ == '__main__':
    print( "Nara CITY  Data Convert Srcipt." )
    parser = argparse.ArgumentParser()
    help_ = 'Google Spreadsheet Id'
    parser.add_argument('-i', '--gid', help=help_, default=SRC_SHEETID )
    help_ = 'Patient List Sheet'
    parser.add_argument('-l', '--list', help=help_, default=SHEET1_NAME )
    help_ = 'Patient Summary Sheet'
    parser.add_argument('-s', '--summary', help=help_, default=SHEET2_NAME )
    help_ = 'Data file'
    parser.add_argument('-d', '--data', help=help_, default=os.path.join(DATA_DIR, DEST1_FILE))
    args = parser.parse_args()

    print( "  output JSON: %s."%( args.data ) )
    main( args )
    print( "Finished." )



