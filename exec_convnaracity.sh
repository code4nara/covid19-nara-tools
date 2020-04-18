#!/bin/bash
####n
#   Stop Covid19nara
#   The Script to make NaraCity JSON-data from Excle.
####
# エクセルダウンロードＵＲＬ
Download_URL="https://www.city.nara.lg.jp/corona/opendata_covid19_naracity.xlsx"
# ダウンロード保存ファイル
Download_EXCEL="./data/opendata_covid19_NaraCity.xlsx"
# 中間ファイル
Temp_JSONFILE="./data/data_naracity.json"
# コピー先のディレクトリとファイル名
Target_JSON_DIR="../covid19/data/"
Target_JSONFILE="data_naracity.json"

# エクセルファイルをダウンロード
curl -s -L https://www.city.nara.lg.jp/corona/opendata_covid19_naracity.xlsx -o ${Download_EXCEL}

# JSON に変換
python ./convert_naracity.py > ${Temp_JSONFILE}

# 公開フォルダにコピー
cp ${Temp_JSONFILE} ${Target_JSON_DIR}${Target_JSONFILE}

