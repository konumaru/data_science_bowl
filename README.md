# data_science_bowl

Data Science Bowlコンペのスクリプト


## Overview

### Trees
- data/
  - raw: 元データを格納
  - reduced: メモリ消費を少なくした元データを格納
  - submit: サブミッションデータを格納
- docs: 雑多なメモ
- notebook: コンペ全体で扱うnotebook
- vXXXXX: 
  - features: 加工の特徴量を格納
  - notebook: 試行錯誤中のスクリプトを格納
  - script.py: notebookから吐き出したスクリプトなど。


## Commands
### 次の実験用ディレクトリの作成
```
$ pipenv run invoke new-exp
```
