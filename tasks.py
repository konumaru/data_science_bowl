import invoke

import os
import re

import numpy as np
import pandas as pd


@invoke.task
def hello(c):
    invoke.run('echo "hello invoke!"')


@invoke.task
def CreateNewExperiment(c):
    def get_version_num(dir_name: str):
        match = re.match(r'v(\d{2})\d{3}', dir_name)
        if match:
            return int(match.groups()[0])
        else:
            return 0

    top_dirs = os.listdir()
    versions = [get_version_num(d) for d in top_dirs]
    next_version = str(max(versions) + 1)
    new_exp_path = 'v' + next_version.zfill(2) + '000'

    try:
        os.mkdir(new_exp_path)
        os.mkdir(os.path.join(new_exp_path, 'version_ref.md'))
        # os.mkdir(os.path.join(new_exp_path, 'notebook'))
        invoke.run(f'echo "Create {new_exp_path} Experiment Directory"')
    except FileExistsError as err:
        invoke.run(f'echo "{err}"')


@invoke.task
def ReduceDataSize(c):
    def reduce_mem_usage(df, verbose=True):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        start_mem = df.memory_usage().sum() / 1024**2
        for col in df.columns:
            col_type = df[col].dtypes
            if col_type in numerics:
                c_min = df[col].min()
                c_max = df[col].max()
                if str(col_type)[:3] == 'int':
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)
                else:
                    if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                        df[col] = df[col].astype(np.float16)
                    elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df[col] = df[col].astype(np.float32)
                    else:
                        df[col] = df[col].astype(np.float64)
        end_mem = df.memory_usage().sum() / 1024**2
        if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)\n'.format(
            end_mem, 100 * (start_mem - end_mem) / start_mem))
        return df

    SRC_FILES = [
        'sample_submission.csv',
        'specs.csv',
        'test.csv',
        'train_labels.csv',
        'train.csv'
    ]

    for src_file in SRC_FILES:
        print(f'Processing {src_file}')
        # Load and Transform
        raw_df = pd.read_csv('./data/raw/' + src_file)
        reduced_df = reduce_mem_usage(raw_df)
        # Export
        filename = src_file.split('.')[0]
        reduced_df.to_pickle('./data/reduced/' + filename + '.pkl')
