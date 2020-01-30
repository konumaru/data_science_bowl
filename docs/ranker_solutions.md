# メダル圏内のスコアが取れるnotebookを作る

- メダル圏内の人の特徴量を真似して、自分のpiplineを組み、メダル圏内のスコアを出す。
- また、try and error がうまくいく方法を身につける。
- 一旦、決定木系の解法だけを参考にする。
- rank solutions
  - https://kaggledb.com/solutions



## メダルスコアを取るまでの手順

- もう一度、最も簡単な自分のpiplineを作る。
- メダル圏内カーネルを１つずつ参照していき、特徴量を追加する。
- 途中でコードをリファクタリングしたくなったら積極的に行う。



# 参考カーネル
## アライさんのnotebook

kernel: https://www.kaggle.com/hidehisaarai1213/dsb2019-nn-ovr-reduce-90-val-60-percentile#Functions-and-Classes


### 特徴量
- `past_summary_features`関数がメインで特徴量を作っている部分
- 基本の処理方法は、installation_id, sessionごとに処理するやつで同じ。
- session_typeごとに処理を記述
  - 更に、session_titleで分岐


### 学習方法
- 回帰予測のplossに最適化処理を使う
```
def lgb_regression_qwk(y_pred: np.ndarray, data: lgb.Dataset) -> Tuple[str, float, bool]:
    y_true = (data.get_label() * 3).astype(int)
    y_pred = y_pred.reshape(-1)

    OptR = OptimizedRounder(n_classwise=3, n_overall=3)
    OptR.fit(y_pred, y_true)

    y_pred = OptR.predict(y_pred).astype(int)
    qwk = calc_metric(y_true, y_pred)

    return "qwk", qwk, True
```


-----------------------------------------------------------------------



# MEMO

## 知らない単語
- truncated, truncated train data
  - 学習時に各installation_idのデータを１つに絞ること。
- null importance
  - ラベルデータをシャッフルしたときのfeature importance。
  - shuffle後のfeature importanceと同じくらい、あるいは低いのであればランダム値よりも重要ではない可能性が高い。


## 略語・変数名の処理について
- コンペごとの略語変数名は、処理部分の頭にリストにしてくと良さそう。
  - ex) sess -> game_session, session


## adversarial validationの方法
- あるinstallation_idにつき、１つのAssessmentのデータをランダムサンプリングする。
- それを5-foldで学習する。
  - 1st のAUCは、0.49 ~ 0.51 に落ち着いた。
  - feature importanceがリークしているとAUCが高くなる傾向がある。
