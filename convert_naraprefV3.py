#!/usr/bin/env python3
####
#   奈良県オープンデータのEXCELからJSONを生成するスクリプト
#       データ元； http://www.pref.nara.jp/55168.htm
####
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

# For Google Spread Sheet
#SRC_SHEETID = "1C07ojkwER8BiAjLBxlzJkfvgM5jxUCLrdtI7wtctTIY"
#SHEET1_NAME = '01.陽性患者の属性'
##SHEET2_NAME = '入院患者の状況'
#SHEET2_NAME = '03.陽性者状況'

# For Opendata by Nara Prefecture.
URL_EXCEL1="http://www.pref.nara.jp/secure/227193/%E5%A5%88%E8%89%AF%E7%9C%8C_01%E6%96%B0%E5%9E%8B%E3%82%B3%E3%83%AD%E3%83%8A%E3%82%A6%E3%82%A4%E3%83%AB%E3%82%B9%E6%84%9F%E6%9F%93%E8%80%85_%E6%82%A3%E8%80%85%E3%83%AA%E3%82%B9%E3%83%88.xlsx"
URL_EXCEL2="http://www.pref.nara.jp/secure/227221/%E5%A5%88%E8%89%AF%E7%9C%8C_02%E6%96%B0%E5%9E%8B%E3%82%B3%E3%83%AD%E3%83%8A%E3%82%A6%E3%82%A4%E3%83%AB%E3%82%B9%E6%84%9F%E6%9F%93%E8%80%85_%E6%82%A3%E8%80%85%E9%9B%86%E8%A8%88%E8%A1%A8.xlsx"
SHEET1_NAME = '奈良県_01新型コロナウイルス感染者_患者リスト'
SHEET2_NAME = '奈良県_02新型コロナウイルス感染者_患者集計表'

DEST_FILE   = 'data.json'

TAB = ['', '  ', '    ', '      ', '        ', '          ', '            ',
       '              ', '                ', '                    ', '                     ']

# 患者リストの読み込み
def load_patient_list( dataUri, sheetName ):
    # ファイルリード／ダウンロード
    df_list = pd.read_excel( dataUri, sheet_name=sheetName, header=None)
    
    # 必要なデータのみに加工
    df_list.columns = df_list.iloc[1]
    df_list = df_list.drop(range(0,2))
    df_list = df_list.drop(['全国地方公共団体コード', '都道府県名'], axis=1)
    # NaNの置換
    df_list['備考'] = df_list['備考'].fillna('')
    df_list['公表_年月日'] = df_list['公表_年月日'].fillna('')
    df_list['発症_年月日'] = df_list['発症_年月日'].fillna('')
    df_list['患者_居住地'] = df_list['患者_居住地'].fillna('')
    #df_list['患者_年代'] = df_list['患者_年代'].fillna('')
    #df_list['患者_性別'] = df_list['患者_性別'].fillna('')
    #df_list['患者_職業'] = df_list['患者_職業'].fillna('')
    #df_list['患者_状態'] = df_list['患者_状態'].fillna('')
    #df_list['患者_症状'] = df_list['患者_症状'].fillna('')

    # 最終更新日時 
    last_data = df_list.iloc[len(df_list.index)-1]
    last_update = last_data['公表_年月日']
    
    return last_update, df_list

# 日々更新データの読み込み
def load_patient_summary( dataUri, sheetName ):
    # ファイルリード／ダウンロード
    df_summary = pd.read_excel( dataUri, sheet_name=sheetName, header=None)

    # 必要なデータのみに加工
    df_summary.columns = df_summary.iloc[1]
    df_summary = df_summary.drop(range(0,2))
    
    df_summary['公表_年月日'] = df_summary['公表_年月日'].fillna('')
    df_summary = df_summary[df_summary['公表_年月日'] != '' ]

    # 最終更新日時設定
    last_data = df_summary.iloc[len(df_summary.index)-1]
    last_update = last_data['公表_年月日']

    # NaNの置換
    df_summary['重症'] = df_summary['重症'].fillna( 0 )
    df_summary['宿泊療養者数'] = df_summary['宿泊療養者数'].fillna( 0 )
    df_summary['自宅療養数'] = df_summary['自宅療養数'].fillna( 0 )
    
    #df_summary['県内PCR検査数'] = df_summary['県内PCR検査数'].fillna( '' )
    #df_summary['県内PCR検査数_陽性確認'] = df_summary['県内PCR検査数_陽性確認'].fillna( '' )

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
        #f.write(TAB[4] + '"職業": "{}",\n'.format(patient['患者_職業']))
        #f.write(TAB[4] + '"状態": "{}",\n'.format(patient['患者_状態']))
        #f.write(TAB[4] + '"症状": "{}",\n'.format(patient['患者_症状']))
        f.write(TAB[4] + '"発症日": "{}",\n'.format(patient['発症_年月日']))
        f.write(TAB[4] + '"備考": "{}"\n'.format(patient['備考']))
        if i == (len(patients.index) - 1):
            f.write(TAB[3] + '}\n')
        else:
            f.write(TAB[3] + '},\n')
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')

# 陽性者発生状況の出力 : 患者リストから日々の発生数を計算
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

# 陽性者発生状況の出力 : 日々データに陽性数がある場合はこちら
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
            if num != num : # NaN（未入力）の場合は強制的に０に
                num = 0
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

# 検査状況の出力 : 日々データ参照
def output_inspections_summary(f, last_update, summary):
    f.write(TAB[1] + '"inspections":{\n')
    f.write(TAB[2] + '"data": [\n')
    start = datetime.datetime(2020, 1, 24, 0, 0, 0)
    end = last_update + datetime.timedelta(days=1)
    period = (end - start).days
    stflag = 0
    for i in range(period):
        d = start + datetime.timedelta(days=i)
        idx = list(summary['公表_年月日'][summary['公表_年月日'] == d].index)

        if len(idx) == 1:
            num = summary['県内PCR検査数'][idx[0]]
            if num == num : #NaN（未入力）でない場合
                # 最初でなければ } カンマ付を出力
                if stflag == 0:
                    stflag = 1
                else:
                    f.write(TAB[3] + '},\n')
                    
                f.write(TAB[3] + '{\n')
                f.write(TAB[4] + '"日付": "{}",\n'.format(str(d.date()) + 'T08:00:00.000Z'))
                f.write(TAB[4] + '"小計": {}\n'.format(num))
                last_update=d.date()

    f.write(TAB[3] + '}\n') # 最後の } カンマ無し
    f.write(TAB[2] + '],\n')
    f.write(TAB[2] + '"date": "{}"\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[1] + '},\n')

# 陽性率の出力 : 日々データ参照
def output_inspection_persons_summary(f, last_update, summary):
    f.write(TAB[1] + '"inspection_persons_summary":{\n')
    f.write(TAB[2] + '"data": [\n')
    start = datetime.datetime(2020, 1, 24, 0, 0, 0)
    end = last_update + datetime.timedelta(days=1)
    period = (end - start).days
    stflag = 0
    for i in range(period):
        d = start + datetime.timedelta(days=i)
        idx = list(summary['公表_年月日'][summary['公表_年月日'] == d].index)

        if len(idx) == 1:
            num1 = summary['県内PCR検査数'][idx[0]]
            num2 = summary['県内PCR検査数_陽性確認'][idx[0]]
            num3 = summary['陽性率（7日間移動平均）'][idx[0]]
            if num1 == num1 and num2 == num2 or num3 == num3 : # NaNでない場合
                # 最初でなければ } カンマ付を出力
                if stflag == 0:
                    stflag = 1
                else:
                    f.write(TAB[3] + '},\n')
                    
                f.write(TAB[3] + '{\n')
                f.write(TAB[4] + '"日付": "{}",\n'.format(str(d.date()) + 'T08:00:00.000Z'))
                f.write(TAB[4] + '"検査人数": {},\n'.format(num1))
                f.write(TAB[4] + '"陽性者数": {},\n'.format(num2))
                f.write(TAB[4] + '"陽性率": {}\n'.format(num3))
                last_update=d.date()

    f.write(TAB[3] + '}\n') # 最後の } カンマ無し
    f.write(TAB[2] + '],\n')
    f.write(TAB[2] + '"date": "{}"\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[1] + '},\n')
    
# 現在（最新）の陽性者状況の出力
def output_main_summary(f, last_update, summary):
    last_data = summary.iloc[len(summary.index)-1]
    f.write(TAB[1] + '"main_summary":{\n')
    #f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[2] + '"attr": "検査実施人数",\n')
    # 項目が無いので０とする
    f.write(TAB[2] + '"value": 0,\n')  # WIP ======================== WIP
    f.write(TAB[2] + '"children": [\n')
    f.write(TAB[3] + '{\n')
    f.write(TAB[4] + '"attr": "感染者数累計",\n')
    f.write(TAB[4] + '"value": {},\n'.format(last_data['陽性確認_件数_累計']))
    f.write(TAB[4] + '"children": [\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "現在感染者数",\n')
    f.write(TAB[6] + '"value": {},\n'.format(last_data['現在感染者数']))
    f.write(TAB[6] + '"children": [\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "入院中",\n')
    # 2021/1/12のデータ形式変更により項目がなくなったので０に
    #    f.write(TAB[8] + '"value": {},\n'.format(last_data['入院者数']))
    f.write(TAB[8] + '"value": 0,\n')  # WIP ======================== WIP
    f.write(TAB[8] + '"children": [\n')
    f.write(TAB[9] + '{\n')
    f.write(TAB[10] + '"attr": "重症",\n')
    f.write(TAB[10] + '"value": {}\n'.format(last_data['重症']))
    f.write(TAB[9] + '}\n')
    f.write(TAB[8] + ']\n')
    f.write(TAB[7] + '},\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "入院・療養中数",\n')
    f.write(TAB[8] + '"value": {}\n'.format(last_data['入院・療養中数']))
    f.write(TAB[7] + '},\n')
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "入院・入所準備中数",\n')
    f.write(TAB[8] + '"value": {}\n'.format(last_data['入院・入所準備中数']))
    f.write(TAB[7] + '},\n')
    # 2021/1/12のデータ形式変更により項目無しなので宿泊療養は０とする
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "宿泊療養",\n')
#    f.write(TAB[8] + '"value": {}\n'.format(last_data['宿泊療養者数']))
    f.write(TAB[8] + '"value": 0\n')  # WIP ======================== WIP
    f.write(TAB[7] + '},\n')
    # 2021/1/12のデータ形式変更により項目無しなので自宅療養は０とする
    f.write(TAB[7] + '{\n')
    f.write(TAB[8] + '"attr": "自宅療養",\n')
#    f.write(TAB[8] + '"value": {}\n'.format(last_data['自宅療養数']))
    f.write(TAB[8] + '"value": 0\n')  # WIP ======================== WIP
    f.write(TAB[7] + '}\n')
    f.write(TAB[6] + ']\n')
    f.write(TAB[5] + '},\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "退院等累計",\n')
    f.write(TAB[6] + '"value": {}\n'.format(last_data['退院者_累計']))
    f.write(TAB[5] + '},\n')
    f.write(TAB[5] + '{\n')
    f.write(TAB[6] + '"attr": "死亡",\n')
    f.write(TAB[6] + '"value": {}\n'.format(last_data['死亡者_累計']))
    f.write(TAB[5] + '}\n')
    f.write(TAB[4] + ']\n')
    f.write(TAB[3] + '}\n')
    f.write(TAB[2] + ']\n')
    f.write(TAB[1] + '},\n')

def output_patientsstat_summary(  f, last_update, summary):
    last_data = summary.iloc[len(summary.index)-1]
    f.write(TAB[1] + '"patientstat_summary":{\n')
    #f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[2] + '"total": {\n')
    f.write(TAB[3] + '"総病床数": {},\n'.format(last_data['感染症対応病床数']))
    f.write(TAB[3] + '"宿泊療養室数": {}\n'.format(last_data['宿泊療養室数']))
    f.write(TAB[2] + '},\n')
    f.write(TAB[2] + '"data": {\n')
    f.write(TAB[3] + '"入院・療養中数": {},\n'.format(last_data['入院・療養中数']))
    f.write(TAB[3] + '"残り病床数": {},\n'.format( last_data['感染症対応病床数']+last_data['宿泊療養室数']-last_data['入院・療養中数']))     
    f.write(TAB[3] + '"入院・入所準備中数": {}\n'.format(last_data['入院・入所準備中数']))
    f.write(TAB[2] + '}\n')
    f.write(TAB[1] + '},\n')

def output_sickbeds_summary( f, last_update, summary):
    last_data = summary.iloc[len(summary.index)-1]
    f.write(TAB[1] + '"sickbeds_summary":{\n')
    #f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d %H:%M')))
    f.write(TAB[2] + '"date": "{}",\n'.format(last_update.strftime('%Y/%m/%d')))
    f.write(TAB[2] + '"total": {\n')
    f.write(TAB[3] + '"総病床数": {},\n'.format(last_data['感染症対応病床数']))
    #f.write(TAB[3] + '"宿泊療養室数": {}\n'.format(last_data['宿泊療養室数']))
    f.write(TAB[3] + '"宿泊療養室数": {}\n'.format(0))
    f.write(TAB[2] + '},\n')
    f.write(TAB[2] + '"data": {\n')
    # 2021/1/12のデータ形式変更により項目がなくなったので０に
    #f.write(TAB[3] + '"入院患者数": {},\n'.format(last_data['入院者数']))
    #f.write(TAB[3] + '"残り病床数": {}\n'.format( last_data['感染症対応病床数']-last_data['入院者数'] ))
    f.write(TAB[3] + '"入院患者数": 0,\n')
    f.write(TAB[3] + '"残り病床数": 0\n')
    f.write(TAB[2] + '}\n')
    f.write(TAB[1] + '},\n')

# data.jsonの出力
def output_data_json(fname, list_last_update, df_list, summary_last_update, df_summary):
    fileobj = open(fname, 'w', encoding = 'utf_8')
    fileobj.write('{\n')
    
    # 陽性者リスト
    output_patients_list(fileobj, list_last_update, df_list)
    # 日々の陽性者数
    #output_patientslist_summary(fileobj, summary_last_update, df_list)
    output_patients_summary(fileobj, summary_last_update, df_summary)
    # 日々の検査数
    output_inspections_summary(fileobj, summary_last_update, df_summary)
    # ７日間平均陽性率
    output_inspection_persons_summary(fileobj, summary_last_update, df_summary)
    # 最新の集計
    output_main_summary(fileobj, summary_last_update, df_summary)
    # ベッド数と入院数
    output_sickbeds_summary(fileobj, summary_last_update, df_summary)
    # 陽性者総数（入院＋療養中）と病床数＋宿泊療養室数
    output_patientsstat_summary(fileobj, summary_last_update, df_summary)
        
    # 全体の更新日付
    fileobj.write(TAB[1] + '"lastUpdate": "{}"\n'.format( datetime.datetime.now().strftime('%Y/%m/%d %H:%M')))

    fileobj.write('}\n')
    fileobj.close()

def main(args):
    # メイン関数

    ## Pandas DataFlame のprint時の表示カラム数設定
    pd.set_option('display.max_columns', 20)
    
    ## 陽性者リストの作成
    list_last_update, df_list = load_patient_list( URL_EXCEL1, args.list )
    print("    Pateient List   : ", list_last_update, len(df_list.index))
    #print( df_list.head())
    
    ## Daily Summary
    summary_last_update, df_summary = load_patient_summary( URL_EXCEL2, args.summary )
    print("    Pateient Summary: ", summary_last_update, len(df_summary.index))
    #print(df_summary.head())

    # output data.json
    output_data_json(args.data, list_last_update, df_list, summary_last_update, df_summary)
    
if __name__ == '__main__':
    print( "Nara PREFCTURE  Data Convert Srcipt." )

    # 引数処理
    parser = argparse.ArgumentParser()
    #help_ = 'Google Spreadsheet Id'
    #parser.add_argument('-i', '--gid', help=help_, default=SRC_SHEETID )
    help_ = 'Patient List Sheet'
    parser.add_argument('-l', '--list', help=help_, default=SHEET1_NAME )
    help_ = 'Patient Summary Sheet'
    parser.add_argument('-s', '--summary', help=help_, default=SHEET2_NAME )
    help_ = 'Data file'
    parser.add_argument('-d', '--data', help=help_, default=os.path.join(DATA_DIR, DEST_FILE))
    args = parser.parse_args()

    # メイン関数
    main( args )
    
    print( "Finished." )

