#!/bin/bash
# for NaraPref
#python download.py
#python convert.py | jq . -M > ../covid19/data/data.json
# for NaraCity
python3 convert_naracity.py | jq . -M > ../covid19/data/data_naracity.json
