#!/bin/bash -l
####n
#   Stop Covid19nara
#   The Script to make JSON
####
# アップデートフラグ：更新あれば１
UPDATE_FLAG=0
BATCH_FLAG=0

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
TJSON_datacity="data_naracity.json" 
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
	grep -v lastUpdate $1 > ${TEMPFILE1}
	grep -v lastUpdate $2 > ${TEMPFILE2}
	diff ${TEMPFILE1} ${TEMPFILE2} > /dev/null 2>&1
	if [ $? -ne 0 ] ; then
	    echo 1
	else
	    echo 0
	fi
	rm -f $TEMPFILE1 $TEMPFILE2
    fi
}
####
#   Yes/no check
####
YN_CHECK()
{
    echo $1
    while true; do
        read -p '  [Y/N] ' Answer
        case $Answer in
            '' | [Yy]* )
                break;
                ;;
            [Nn]* )
                echo "  CANCELed."
                exit;
                ;;
            * )
                echo Please answer YES or NO.
        esac
    done
}
####
#   usage_exit
####
usage_exit()
{
    echo "  JSON Update Scrpit for stopcvoid19.code4nara.org"
    echo "  usage: ${0}  [-b]"
    echo "    -b : Batch-Deploy mode"
    exit;
}


########
#       Main
########
####
#   Option Check
####
while getopts "hb" OPT
do
    case $OPT in
        h) usage_exit ;;
        b) BATCH_FLAG=1 ;;
    esac
done

####
# 奈良県／奈良市のサイトスクレイピング：新着情報の抽出実行
####
echo "--  Scraping news from Nara Pref"
cmd="python3 ./scraping_naraNews.py -p ${TEMP_newspref} -c ${TEMP_newscity} > /dev/null 2>&1"
echo "    exec: " ${cmd}
eval ${cmd}

# 保存データと比較し変更があれば公開場所にコピー
ret=`CheckDiff ${TEMP_newspref} ${TEMP_newsprefSaved}`
if [ $ret == "1" ] ; then
    echo "II  ${TJSON_newspref} Found updete : News in Prefecture"
    UPDATE_FLAG=1
    # コピーを保存し公開フォルダにコピー
    cp ${TEMP_newspref} ${TEMP_newsprefSaved}
    cp ${TEMP_newspref} ${TGT_JSON_DIR}${TJSON_newspref}
fi

# 保存データと比較し変更があれば公開場所にコピー
#ret=`CheckDiff ${TEMP_newscity}  ${TEMP_newscitySaved}`
#if [ $ret == "1" ] ; then
#    echo "II  ${TJSON_newscity} Found updete : News in City"
#    UPDATE_FLAG=1
#    # コピーを保存し公開フォルダにコピー
#    cp ${TEMP_newscity} ${TEMP_newscitySaved}
#    cp ${TEMP_newscity} ${TGT_JSON_DIR}${TJSON_newscity}
#fi

####
# 奈良県感染データ更新
####
echo "--  Making data.json from Excel"
cmd="python3 ./convert_naraprefV3.py > /dev/null 2>&1" 
echo "    exec: " ${cmd}
eval ${cmd}

# 保存データと比較し変更があれば公開場所にコピー
ret=`CheckDiff ${TEMP_datapref}  ${TEMP_dataprefSaved}`
if [ $ret == "1" ] ; then
    echo "II  ${TJSON_datapref} Found updete : Prefecture Data"
    UPDATE_FLAG=1
    # コピーを保存し公開フォルダにコピー
    cp ${TEMP_datapref} ${TEMP_dataprefSaved}
    cp ${TEMP_datapref} ${TGT_JSON_DIR}${TJSON_datapref}
fi


####
# 奈良市感染データ更新：グーグルスプレッドシート参照
####
#echo "--  Making naracity.json from GoogleSpreadSheet"
#cmd="python3 ./convert_naracityV2.py > /dev/null 2>&1"
#echo "    exec: " ${cmd}
#eval ${cmd}

## 保存データと比較し変更があれば公開場所にコピー
#ret=`CheckDiff ${TEMP_datacity}  ${TEMP_datacitySaved}`
#if [ $ret == "1" ] ; then
#    echo "II  ${TJSON_datacity} Found updete : Nara City Data"
#    UPDATE_FLAG=1
#    # コピーを保存し公開フォルダにコピー
#    cp ${TEMP_datacity} ${TEMP_datacitySaved}
#    cp ${TEMP_datacity} ${TGT_JSON_DIR}${TJSON_datacity}
#fi


####
# サイトデプロイ：要環境変数 GITHUB_TOKEN
####
if [ ${UPDATE_FLAG} == 1 ]; then
    echo "II  Exec Github Action for data update."
    date +"    at %Y/%m/%d %H:%m:%S"

    # バッチモードならば自動実行／バッチモード以外は Y/N チェック
    if [ ${BATCH_FLAG} == 1 ]; then
        # 開発サイトへのデプロイ
	cmd="bash ./githubDeployment.sh -b" 
	echo "    exec: " ${cmd}
	eval ${cmd}
	
	# 本番サイトへのデプロイ
	cmd="bash ./githubDeployment.sh -b -r master -e production" 
	echo "    exec: " ${cmd}
	eval ${cmd}
    else
        # 開発サイトのデプロイ
	YN_CHECK "  Run Development Deploy to netlify ?" 
	cmd="bash ./githubDeployment.sh -b" 
	echo "    exec: " ${cmd}
	eval ${cmd}

	# 本番サイトのデプロイ
	YN_CHECK "  Run Master Deploy to stopcovid19.code4nara.org ?" 
	cmd="bash ./githubDeployment.sh -b -r master -e production" 
	echo "    exec: " ${cmd}
	eval ${cmd}
    fi
fi
