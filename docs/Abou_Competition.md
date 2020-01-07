# About Competition

## Overview
### 主催
- [Booz Allen Hamilton](https://www.boozallen.com/)

### 問題設定
- 学習ゲームのアプリから得られたデータを扱う。
- ユーザーは、課題の回答率から 0~4 の５段階で評価される。
- 今回得問題は、ゲームプレイデータを用いて特定の評価に合格するためには、いくつの試行回数が必要なのかを予測する。    
  - 不正解の回答回数を試行回数として扱う
- 予測する値は、施行回数によってクラスタリングされたもの。
  - 3: 評価は最初の試行で解決されました
  - 2: 2回目の試行で評価が解決された
  - 1: 3回以上の試行の後に評価が解決された 
  - 0: 回答できなかった


## About Submission
- kernelで最終ファイルを提出
  - `submission.csv` というファイル名でのみ提出できる。
- 最終的に、２つのファイルを提出できる。
  - ２つ選んでいなくても、自動的にスコアが高いものから選ばれる。
  - private/public でスコアは異なる。


## Metric
- The quadratic weighted kappa

## Data Description

### train.csv & test.csv
These are the main data files which contain the gameplay events.

- event_id - Randomly generated unique identifier for the event type. Maps to event_id column in specs table.
- game_session - Randomly generated unique identifier grouping events within a single game or video play session.
- timestamp - Client-generated datetime
- event_data - Semi-structured JSON formatted string containing the events parameters. Default fields are: event_count, event_code, and game_time; otherwise fields are determined by the event type.
- installation_id - Randomly generated unique identifier grouping game sessions within a single installed application instance.
- event_count - Incremental counter of events within a game session (offset at 1). Extracted from event_data.
- event_code - Identifier of the event 'class'. Unique per game, but may be duplicated across games. E.g. event code '2000' always identifies the 'Start Game' event for all games. Extracted from event_data.
- game_time - Time in milliseconds since the start of the game session. Extracted from event_data.
- title - Title of the game or video.
- type - Media type of the game or video. Possible values are: 'Game', 'Assessment', 'Activity', 'Clip'.
- world - The section of the application the game or video belongs to. Helpful to identify the educational curriculum goals of the media. Possible values are: 'NONE' (at the app's start screen), TREETOPCITY' (Length/Height), 'MAGMAPEAK' (Capacity/Displacement), 'CRYSTALCAVES' (Weight).

### specs.csv
This file gives the specification of the various event types.

- event_id - Global unique identifier for the event type. Joins to event_id column in events table.
- info - Description of the event.
- args - JSON formatted string of event arguments. Each argument contains:
- name - Argument name.
- type - Type of the argument (string, int, number, object, array).
- info - Description of the argument.
 
### train_labels.csv
This file demonstrates how to compute the ground truth for the assessments in the training set.

