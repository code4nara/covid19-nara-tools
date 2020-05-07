#!/bin/bash -l
####n
#   Stop Covid19nara
#   The Script to make JSON
####
# アップデートフラグ：更新あれば１
UPDATE_FLAG=0

# 公開用のディレクトリ
TGT_JSON_DIR="../html/api/"  

# 奈良県の感染データ
TJSON_datapref="data.json"  
TEMP_datapref="./data/data.json"
TEMP_dataprefSaved=${TEMP_datapref}"_saved"
# 奈良県のニュース
TJSON_newspref="news.json"  
TEMP_newspref="./data/news.json"
TEMP_newsprefSaved=${TEMP_newspref}"_saved"

# 奈良市の感染データ
#TJSON_datacity="data_naracity.json"  
TJSON_datacity="naracity.json"  
TEMP_datacity="./data/data_naracity.json"
TEMP_datacitySaved=${TEMP_datacity}"_saved"
# 奈良市のニュース
TJSON_newscity="news_naracity.json"  
TEMP_newscity="./data/news_naracity.json"
TEMP_newscitySaved=${TEMP_newscity}"_saved"

TEMPFILE1="./updatetmp1.$$"
TEMPFILE2="./updatetmp2.$$"

####
#   ファイル比較：loastUpdate以外
####
function CheckDiff()
{
    if [ ! -e $1 ]; then
	echo 1;
    elif [ ! -e $2 ]; then
	echo 1;
    else
	grep -v lastaUpdate $1 > ${TEMPFILE1}
	grep -v lastaUpdate $2 > ${TEMPFILE2}
	diff ${TEMPFILE1} ${TEMPFILE2} > /dev/null 2>&1
	rm $TEMPFILE1
	rm $TEMPFILE2
    
	if [ $? -ne 0 ] ; then
	    echo 1
	fi
	echo 0
    fi
}

########
#       Main
########
echo "  JSON Update Scrpit"

####
# 奈良県／奈良市のサイトスクレイピング：新着情報の抽出実行
####
echo "--  Scraping news from Nara Pref"
cmd="python3 ./scraping_naraNews.py -p ${TEMP_newspref} -c ${TEMP_newscity} > /dev/null 2>&1"
echo "    cmd: " ${cmd}
eval ${cmd}

# 保存データと比較し変更があれば公開場所にコピー
ret=`CheckDiff ${TEMP_newspref} ${TEMP_newsprefSaved}`
if [ $ret == "1" ] ; then
    echo "II  Found updete : News in Prefecture"
    UPDATE_FLAG=1
    # コピーを保存し公開フォルダにコピー
    cp ${TEMP_newspref} ${TEMP_newsprefSaved}
    cp ${TEMP_newspref} ${TGT_JSON_DIR}${TJSON_newspref}
fi

# 保存データと比較し変更があれば公開場所にコピー
ret=`CheckDiff ${TEMP_newscity}  ${TEMP_newscitySaved}`
if [ $ret == "1" ] ; then
    echo "II  Found updete : News in City"
    UPDATE_FLAG=1
    # コピーを保存し公開フォルダにコピー
    cp ${TEMP_newscity} ${TEMP_newscitySaved}
    cp ${TEMP_newscity} ${TGT_JSON_DIR}${TJSON_newscity}
fi

####
# 奈良県感染データ更新：グーグルスプレッドシート参照
####
echo "--  Making data,json from GoogleSpreadSheet"
cmd="python3 ./convert_narapregfV2.py > /dev/null 2>&1" 
echo "    cmd: " ${cmd}
eval ${cmd}

# 保存データと比較し変更があれば公開場所にコピー
ret=`CheckDiff ${TEMP_datapref}  ${TEMP_dataprefSaved}`
if [ $ret == "1" ] ; then
    echo "II  Found updete : Prefecture Data"
    UPDATE_FLAG=1
    # コピーを保存し公開フォルダにコピー
    cp ${TEMP_datapref} ${TEMP_dataprefSaved}
    cp ${TEMP_datapref} ${TGT_JSON_DIR}${TJSON_datapref}
fi


####
# 奈良市感染データ更新：グーグルスプレッドシート参照
####
echo "--  Making naracity.json from GoogleSpreadSheet"
cmd="python3 ./convert_naracityV2.py > /dev/null 2>&1"
echo "    cmd: " ${cmd}
eval ${cmd}

# 保存データと比較し変更があれば公開場所にコピー
ret=`CheckDiff ${TEMP_datacity}  ${TEMP_datacitySaved}`
if [ $ret == "1" ] ; then
    echo "II  Found updete : Nara City Data"
    UPDATE_FLAG=1
    # コピーを保存し公開フォルダにコピー
    cp ${TEMP_datacity} ${TEMP_datacitySaved}
    cp ${TEMP_datacity} ${TGT_JSON_DIR}${TJSON_datacity}
fi



# 開発サイトへのデプロイ：要環境変数 GITHUB_TOKEN
if [ ${UPDATE_FLAG} == 1 ]; then
   echo "II  Exec Github Action for dta update."

   # 開発サイトへのデプロイ：要環境変数 GITHUB_TOKEN
   cmd="bash ./githubDeployment.sh -b" 
   echo "    cmd: " ${cmd}
   #eval ${cmd}

   # 本番サイトへのデプロイ：要環境変数 GITHUB_TOKEN
   cmd="bash ./githubDeployment.sh -b -r master -e production" 
   echo "    cmd: " ${cmd}
   #eval ${cmd}
fi
