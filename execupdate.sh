#!/bin/bash
####n
#   Stop Covid19nara
#   The Script to make JSON
####

# コピー先のディレクトリとファイル名
Target_JSON_DIR="../covid19/data/"

# 奈良市版エクセルファイルＵＲＬ
DURL_naracity="https://www.city.nara.lg.jp/corona/opendata_covid19_naracity.xlsx"
# 奈良市版ダウンロード保存ファイル
DEXCEL_naracity="./data/opendata_covid19_NaraCity.xlsx"
DEXCEL_naracitySaved="./data/opendata_covid19_NaraCity.xlsx_saved"
TJSON_naracity="data_naracity.json"
TEMP_naracity="./data/data_naracity.json"

# 保存ファイルのチェック
if [ ! -e ${DEXCEL_naracitySaved} ]; then
   touch ${DEXCEL_naracitySaved}
fi

# エクセルファイルをダウンロードし保存ファイルと比較
curl -s -L ${DURL_naracity} -o ${DEXCEL_naracity}

ls -la ${DEXCEL_naracity}
ls -la ${DEXCEL_naracitySaved}

diff ${DEXCEL_naracity}  ${DEXCEL_naracitySaved} > /dev/null 2>&1

if [ $? -eq 1 ] ; then
    echo "Found updete : ${DURL_naracity}"
    # JSON に変換
    cp ${DEXCEL_naracity} ${DEXCEL_naracitySaved}

    # JSON に変換
    python3 ./convert_naracity.py > ${TEMP_naracity}

    # 公開フォルダにコピー
    cp ${TEMP_naracity} ${TGT_JSON_DIR}${TJSON_naracity}
fi

