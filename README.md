# covid19-nara-tools

奈良県版のツール

千葉県版ツール covid19-chiba-tools を参考にさせていただいて準備中

## 使い方

```bash
git clone https://github.com/code4nara/covid19-nara-tools.git
cd covid19-nara-tools
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python download.py
python convert.py | jq . > data.json
```

dockerを使う場合（動作未確認です）

```bash
git clone https://github.com/code4nara/covid19-nara-tools.git
cd covid19-nara-tools
docker build -t nara-covid19-tools .
docker run --rm -it nara-covid19-tools > data.json
```
## ファイル

download.pyはdataディレクトリにダウンロードするファイル。ファイル実態は準備中

- 検査実施サマリ.xlsx
- 検査実績（データセット）千葉県衛生研究所2019-nCoVラインリスト<日付>.xlsx
- 検査実施日別状況.xlsx
- 【<日付>】千葉県_感染者発生状況.xlsx
- 帰国者接触者センター相談件数-RAW.xlsx
- コールセンター相談件数-RAW.xlsx