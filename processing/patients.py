"""
opendata_covid19_NaraCity.xlsx
"""

from openpyxl import load_workbook
import os
import glob
from pathlib import Path
import sys
sys.path.append(str(Path('__file__').resolve().parent))
from common import excel_date

def parse_nara_patients_list():
    FILENAME = "opendata_covid19_NaraCity.xlsx"
    paths = [os.path.abspath(os.path.dirname(__file__)), '..', 'data', FILENAME]

    patients_count = 0 # 陽性患者数
    discharge_count = 0 # 退院
    stayed_count = 0 # 入院
    tiny_injury_count = 0 # 軽症
    severe_injury_count = 0 # 重症
    death_count = 0 # 死亡数
    patients_list = [] # 患者の表の表示用
    
    f = os.path.join(*paths)
    wb = load_workbook(f)
    ws = wb['1.陽性患者リスト']
    inloop = False
    target = None

    # 患者
    for row in ws.values:
        if 'No' in str(row[0]):
            continue;
        if row[0] == None :
            break;

        patient_no = row[0] # No
        pub_date   = row[4] # 発表_年月日
        where_lived= row[6] # 患者_居住地
        age        = row[7] # 患者_年代
        sex        = row[8] # 患者_年代
        discharge  = row[13] # 患者_退院済フラグ
        last_update= row[14] # データ最終更新日
        note       = row[15] # 備考

        # 陽性患者属性
        patients_data = {
            "No": patient_no, 
            "発表日": pub_date.isoformat(timespec='milliseconds')+'Z',
            "居住地": where_lived,
            "年代": age,
            "性別": sex,
            "退院": discharge,
            "更新日": last_update.isoformat(timespec='milliseconds')+'Z',
            "備考": note,
        }
        patients_list.append(patients_data)

        patients_count += 1 # 陽性患者数
        if discharge == 0 : 
            stayed_count += 1 # 入院数
        elif discharge == 1 :
            discharged_count += 1 # 退院数
        elif discharge == 2 :
            death_count += 1 # 死亡数
        #print(patients_data)

    return last_update, patients_list, patients_count, stayed_count, discharge_count, death_count

#   return patients_count, discharge_count, stayed_count, tiny_injury_count, severe_injury_count, data, patients_list
