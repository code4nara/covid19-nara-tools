#!/bin/bash
####n
#   Stop Covid19nara
#   The Script to make JSON
####

# コピー先のディレクトリとファイル名
TGT_JSON_DIR="../html/api/"

# 奈良県のニュース
TJSON_newspref="news.json"  
TEMP_newspref="./data/news.json"
TEMP_newsprefSaved=${TEMP_newspref}"_saved"

# 奈良市のニュース
TJSON_newscity="news_naracity.json"  
TEMP_newscity="./data/news_naracity.json"
TEMP_newscitySaved=${TEMP_newscity}"_saved"

# 奈良市版エクセルファイルＵＲＬ
DURL_naracity="https://www.city.nara.lg.jp/corona/opendata_covid19_naracity.xlsx"
# 奈良市版ダウンロード保存ファイル
TJSON_naracity="data_naracity.json"
DEXCEL_naracity="./data/opendata_covid19_NaraCity.xlsx"
DEXCEL_naracitySaved="./data/opendata_covid19_NaraCity.xlsx_saved"
TEMP_naracity="./data/data_naracity.json"

# 保存ファイルのチェック
if [ ! -e ${DEXCEL_naracitySaved} ]; then
   touch ${DEXCEL_naracitySaved}
fi

#### 奈良県／奈良市のサイトスクレイピング：新着情報の抽出
# echo "Scraping news from Nara Pref"
python3 ./scraping_naraNews.py -p ${TEMP_newspref} -c ${TEMP_newscity} > /dev/null 2>&1

# 保存データと比較し変更があれば公開場所にコピー
diff ${TEMP_newspref}  ${TEMP_newsprefSaved} > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    echo "Found updete : News in Pref"
    # コピーを保存
    cp ${TEMP_newspref} ${TEMP_newsprefSaved}
    # 公開フォルダにコピー
    cp ${TEMP_newspref} ${TGT_JSON_DIR}${TJSON_newspref}
fi

# 保存データと比較し変更があれば公開場所にコピー
diff ${TEMP_newscity}  ${TEMP_newscitySaved} > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    echo "Found updete : News in City"
    # コピーを保存
    cp ${TEMP_newscity} ${TEMP_newscitySaved}
    # 公開フォルダにコピー
    cp ${TEMP_newscity} ${TGT_JSON_DIR}${TJSON_newscity}
fi


# 奈良市版はまだ正式発表でないため

if 0 ; then 

#### 奈良市版のデータコンバート
# エクセルファイルをダウンロードし保存ファイルと比較
curl -s -L ${DURL_naracity} -o ${DEXCEL_naracity}

diff ${DEXCEL_naracity}  ${DEXCEL_naracitySaved} > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    echo "Found updete : ${DURL_naracity}"
    # コピーを保存
    cp ${DEXCEL_naracity} ${DEXCEL_naracitySaved}

    # JSON に変換
    python3 ./convert_naracity.py > ${TEMP_naracity}

    # 公開フォルダにコピー
    cp ${TEMP_naracity} ${TGT_JSON_DIR}${TJSON_naracity}
fi

fi

# 開発サイトへのデプロイ：要環境変数 GITHUB_TOKEN
./deploy_development.sh

# 本番サイトへのデプロイ：要環境変数 GITHUB_TOKEN
#./deploy_master.sh
