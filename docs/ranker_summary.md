# Winner solution

## 14th place solution
discussion: https://www.kaggle.com/c/data-science-bowl-2019/discussion/127221#726288
kernel: https://www.kaggle.com/khahuras/bowl-2201-a?scriptVersionId=27403894


- 特徴量・学習データ
  - testデータから学習データを作れた。
  - ラベルが少ないデータをかさ増しするために、重み付きサンプリングを行った
    - 評価値が最小二乗法なので、少ないサンプル数のデータが当てにくくなる。
- モデリング
  - Assessment title でのgroup k fold
  - 回帰予測後の閾値の決定には、最適化アルゴリズムを用いた。
