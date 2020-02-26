# 1st Solution

[https://www.kaggle.com/c/data-science-bowl-2019/discussion/127469](https://www.kaggle.com/c/data-science-bowl-2019/discussion/127469)

### Summary

- LGBM の multi-seeds 5 fold.
- バリデーションスコア
    - Weighted QWK：0.591
    - Weighted RMSE：1.009
The model score :
private qwk 0.568, public qwk 0.563
cv weighted qwk 0.591, cv weighted rmse 1.009

### Validation

- ローカルCVだけを信じてスコアを改善した。
- バリデーションは２種類
    - GroupK CV
        - 5-fold GroupK を５回
        - group は installation_id
        - バリデーションにだけ重みを付けた。
            - ' the weight is the sample prob for each sample '
                - 各サンプルのサンプル確率
                - サンプル、installationごとのサンプルされる確率
                - 期待値 ＝ 確率で重み付けされた平均値
                - 重み ＝ 期待される assessment の観測数の逆数
                    - truncated と同じ意味を持たせたい。
                        - １installation_id ごとに １サンプル
                        - asessment数が多いinstallation_idのほうがサンプリングされやすくなる。
                        - weight = `1/number of assessment we obserbed in data by installation_id`
                        - 同じユーザーIDのデータを複数回評価するため、プレイ数が多いユーザーの方が重要度が高く評価されてしまう。
            - 観測されたassessmentの期待値
                - weight = `1 / 2*number of assessment we observed in test - 1`
                - ＊これは違うっぽい
    - Nested CV
      - GroupK CV は機能したが、信頼性に欠けた。
      - 全体からランダムに選択された1,400ユーザーをの全過去データで学習を行い、truncatedされた2,200ユーザーで検証を行った。
        - 検証回数は、50 ~ 100回の計算の平均を検証用スコアとした。



## Feature Enginnering
- 特徴量を作るのに一番時間を使った。
- 20,000くらい特徴量を作った。
- null importance で上位500に削った。
  - [null importance](https://www.kaggle.com/ogrellier/feature-selection-with-null-importances)
- Lots of stats
  - mean, sum, last, std, max, slope
  - correct true ratio, correct feedback ratio
  - 似ているゲーム間のacuuracyにはちゃんと相関があった。
- データセットから異なる特徴量を作った
  - 全部で、５種類のデータセットを作りjoinした
    - 全過去のデータ
    - 直前の5, 12, 48時間のデータ
    - 最後のAssessmentから現在のAsessmentまでのデータ
- Event interval feature (next event timestamps - current event timestamps)
  - `df.groupby(by=[event_id, event_code]).agg([mean, last])`
  - いくつかの特徴量は効いた。
  - timestampでdiffをとって、event_codeでpivotしたらできそう。
- Video skip prop ratio 
  - clipをスキップした割合
  - clip event interval / clip length provided by organizer.
    - clipの長さ / 実際のclipの長さ
- Event data Feature
  - event_dataにおける全ての連続値の mean, sum, last
    - 例 ）event_code2030_misses_mean
      - `f'event_code{event_code}_{key}_{STATS}'` でJSONを展開すれば良さそう。


## Feature Selection
- drop duplicate cols
- Truncated adversarial validationを行った。
  - AUCはだいたい0.5くらいになった。
- null importance を使って上位500個まで削った。

## model
- データのかさ増し
  - train, 使えるtestを使った
- Loss
  - trainingでは、RMSE
  - validationには、weighted RMSEを使った。
- Threshold
  - Optimizer Rounder を使った。
- Ensemble
  - `0.8 * lightgbm + 0.2 * catboost` でブレンドしたが、local CVが改善しなかったので使わなかった。


## Comments
- Advaersarial AUC to 0.5 ってどうやったの？
  - truncated Train と 1,000 testデータを使った。
  - 5-fold val AUC で大体0.49 ~ 0.51
  - feature importanceをみてリークについて考えた。


## What I can do 
- Feature Enginnering
  - Lots of stats
    - type ごとのevent_code count 系の特徴量は作った。
    - [x] titleごとの event_code count 統計量
  - [ ] Video skip prop ratio
    - 前回のセッションの最後のtimestampをとっておいて、現在のtimestampと引き算をする。
    - その長さをclipを見た時間とし、実際のclipの長さで割る。
    - 実際のclipの長さは、秒で格納されている。
  - Event interval feature
    - [x] event_idごとのインターバル時間を保持。リストを更新。calc_dict_statsで変換。
  - Event data Feature
    - [ ] つくる
- Validation Strategy
  - [x] GroupK CVを使う
  - [ ] Nested CVの実装
    - https://twitter.com/Maxwell_110/status/1227586019865722881
- Feature Selection
  - [ ] drop duplicate cols の実装
  - [ ] null importance の実装
  - [ ] adversarial validation の実装
- Model
  - [x] validation だけ weighted RMSE を使う。
    - 学習データは前過去、テストデータはtruncated後、という構図を再現するため。
