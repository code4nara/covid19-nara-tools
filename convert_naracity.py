#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#
from openpyxl import load_workbook
import glob
from datetime import datetime, date, time, timedelta
import json
from common import excel_date
from pathlib import Path

from processing.patients import parse_nara_patients_list
from processing.dailystatus import parse_nara_dailystatus
#from processing.call_center import parse_call_center
#from processing.inspection_per_date import parse_inspection_per_date
#from processing.querents import parse_querents

#(inspections, inspections_summary_data, inspections_summary_labels), total_count = parse_inspection_per_date()
patients_ldate, patients_list, patients_count, stayed_count, discharge_count, death_count = parse_nara_patients_list()
patients_date, patients_summary, inspections_date, inspections_list, querents_date, querents_list, inspections_total, stayed_count, discharge_count, death_count = parse_nara_dailystatus()

#死亡者を除く
discharge_count-=death_count

# print( patients_date )

# data.json 雛形
data = {
    # 陽性患者
    "patients": {
        "date": patients_ldate,
        "data": patients_list
    },

    "main_summary": {
        "date": patients_date,
        "attr": "検査実施人数",
        "value": inspections_total,
        "children": [
            {
                "attr": "陽性患者数",
                "value": patients_count,
                "children": [
                    {
                        "attr": "入院／入院調整中",
                        "value": stayed_count,
                        "children": [
                            {
                                "attr": "軽症・中等症",
                                "value": "-"
                            },
                            {
                                "attr": "重症",
                                "value": "-"
                            }
                        ]
                    },
                    {
                        "attr": "退院",
                        "value": discharge_count
                    },
                    {
                        "attr": "死亡",
                        "value": death_count
                    }
                ]
            }
        ]
    },
    # 患者数
    "patients_summary": { 
        "date": patients_date,
        "data": patients_summary
    },
    # 検査実施数
    "inspections_summary": {
        "date": inspections_date,
        "data": inspections_list
    },
    # 相談件数
    "querents": { 
        "date": querents_date,
        "data": querents_list
    },
    "lastUpdate": datetime.now().strftime('%Y/%m/%d %H:%M'),
}

print(json.dumps(data, ensure_ascii=False ) )

    
"""
    },
    # 奈良市データ: 患者と非患者のサマリ
    "patients_and_no_symptoms_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": {
            "患者": patients_and_no_symptoms_summary_data_patients,
            "無症状病原体保有者": patients_and_no_symptoms_summary_data_no_symptoms
        },
        "labels": patients_and_no_symptoms_summary_labels
    },
    # 退院者
    "discharges_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": []
    },
    "discharges": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": []
    },
    "inspections_summary": {
        "date": datetime.now().strftime('%Y/%m/%d %H:%M'),
        "data": inspections_summary_data,
        "labels": inspections_summary_labels
    },
}
"""


