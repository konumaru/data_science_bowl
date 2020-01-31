import os
import pandas as pd


def read_data(files: list):
    if os.path.exists('/kaggle/input/data-science-bowl-2019/'):
        data_dir_path = '/kaggle/input/data-science-bowl-2019/'
    else:
        data_dir_path = '../../data/reduced/'
    
    dst_data = {}
    for file in files:
        print(f'Reading {file} ....')
        dst_data[file] = pd.read_csv(data_dir_path + file)
        print(f'{file} file have {dst_data[file].shape[0]} rows and {dst_data[file].shape[1]} columns.')

    return dst_data.values()
