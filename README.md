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

## 使い方

### 奈良県版

準備中

### 奈良市版

python convert_naracity.py | jq . > data_naracity.json

（注）jq で成型すること

## ファイル

dataディレクトリにxlsxファイルを配置します。

- 奈良県全体要：準備中
- 奈良市用： opendata_covid19_NaraCity.xlsx
