# covid19-chiba-tools

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
sudo pip3 install openpyxl
sudo yum install epel-release
sudo yum install jq
```

jq は出力を見やすく整形するときに利用

## 使い方

### 奈良県内市町村jsonの作成

python3 convert_municipalities.py > municipalities-data.json


### 奈良県版

準備中

### 奈良市版

python3 convert_naracity.py  > data_naracity.json

## ファイル

dataディレクトリにxlsxファイルを配置します。

- 奈良県内市町村リンク： municipalities.xlsx
- 奈良県全体要：準備中
- 奈良市用： opendata_covid19_NaraCity.xlsx

各excelのサンプルデータは samples 以下にある
