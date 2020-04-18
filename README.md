# covid19-nara-tools

奈良県版 xlsx-json 変換ツール

## 準備

```bash
git clone https://github.com/code4nara/covid19-nara-tools.git
cd covid19-nara-tools
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

for CentOS8
```
sudo yum install python3
sudo yum install python3-pip
sudo pip3 install -r requirements.txt
sudo yum install epel-release
sudo yum install jq
```

jq は出力を見やすく整形するときに利用

## 使い方

### 奈良県/奈良市のニュースjsonの作成
# 奈良県：http://www.pref.nara.jpから取得
# 奈良市：https://www.city.nara.lg.jp

python3 scraping_naraNews.py [-h] [-pref json file] [-city json file]<br>
- pref json file : default ./data/news.json
- city json file : default ./data/news_naracity.json

### 奈良県内市町村jsonの作成

python3 convert_municipalities.py [-h] [-i excel file] [-o json file]<br>
- excel file : default ./data/municipalities.xlsx<br>
- json file : default ./data/municipalities-data.json

### 奈良県版感染情報jsonの作成

奈良市版をベースに修正予定

### 奈良市版感染情報jsonの作成

python3 convert_naracity.py  > data_naracity.json

### バッチ実行スクリプト

bash ./execupdate.sh

記載時点で奈良市版のみ実行。奈良県内市町村jsonおよびニュースnews.jsonの更新追加予定。
参照ファイルの更新を判定し、更新されていれば再作成する。

## ファイル

dataディレクトリにxlsxファイルを配置します。

- 奈良県内市町村リンク： municipalities.xlsx
- 奈良県全体要：準備中
- 奈良市用： opendata_covid19_NaraCity.xlsx

テスト実行は、sample以下にあるexcelのサンプルが使えます。

https://docs.google.com/presentation/u/3/d/1wJH_STk3kKA-VGeI2czkrvbvg-0blcfGSzQrD4wSxq4/edit#slide=id.g7348cc6224_0_0