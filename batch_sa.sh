#!/bin/bash

CYCLE=1000
TRIAL=100
T_INI=1
T_MIN=1e-3

## graph/ ディレクトリ内の全ての .txt ファイルを処理する
for file in graph/*.txt
do
    echo "Processing file: $file"
    /xxx/yyy/python sa.py --cycle $CYCLE  --trial $TRIAL --T_ini $T_INI --T_min $T_MIN --file_path "$file"
done


