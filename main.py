import numpy as np
import pandas as pd


def load_data(data_dir_path='./data/raw/', filetype='csv'):
    print('Reading train file....')
    train = pd.read_csv(data_dir_path + 'train.csv')
    print('Training.csv file have {} rows and {} columns'.format(train.shape[0], train.shape[1]))

    print('Reading test file....')
    test = pd.read_csv(data_dir_path + 'test.csv')
    print('Test.csv file have {} rows and {} columns'.format(test.shape[0], test.shape[1]))

    print('Reading specs file....')
    specs = pd.read_csv(data_dir_path + 'specs.csv')
    print('Specs.csv file have {} rows and {} columns'.format(specs.shape[0], specs.shape[1]))

    return train, test, specs


''' MEMO
- train, test のデータの期間
   - The date range in train is: 2019-07-23 to 2019-10-22
   - The date range in test is: 2019-07-24 to 2019-10-14
'''


def transform(train, test, specs):
    print('Assessment が含まれていないinstallation_idを除外')
    # test データには、installation_id ごとに Assessment が少なくとも１回は行われている。
    # train, test 間で共通するinstallation_idは存在しない。
    # unique number of train is 4,242. and test is 1,000.
    keep_ids = train.loc[train['type'] == 'Assessment', 'installation_id'].unique()
    train = train[train.installation_id.isin(keep_ids)].reset_index(drop=True)

    print('Bird Measurer (Assessment) の event_code == 4100 のデータを除外')
    # 正しいのは、event_code == 4110 のデータのみであるため。
    # MEMO: 4100のデータを除外するか、4100を別名にし、4110を4100に置換するか、検討する必要がある。
    return None


def predict():
    return None


def export():
    return None


def main():
    print('Load Data...')
    train, test, specs = load_data()

    print('Transform Data ...')
    train, test = transform()

    print('Train Model...')

    print('Prediction ...')

    print('Export Submission File ...')


if __name__ == '__main__':
    main()
