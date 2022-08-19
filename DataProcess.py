import numpy as np
import pandas as pd
import os
import scipy
from sas7bdat import SAS7BDAT
from win32com.client import Dispatch
import random
import shutil
import argparse

parser = argparse.ArgumentParser(description='Settings')
parser.add_argument('--path', default='C:/Users/1000297658/Desktop/dataset/wafer_0.6.jmp', type=str, help='sourse file path')
parser.add_argument('--sub_sample_n', default=None, type=str, help='number of sub-sampling')
parser.add_argument('--sub_sample_frac', default=None, type=str, help='fraction of sub-sampling')

# ----------------------------------------------------------------------------
parser.add_argument('--train_all', action='store_true', help='use all training data' )
parser.add_argument('--color_jitter', action='store_true', help='use color jitter in training' )
parser.add_argument('--batchsize', default=16, type=int, help='batchsize')
parser.add_argument('--stride', default=2, type=int, help='stride')
parser.add_argument('--erasing_p', default=0, type=float, help='Random Erasing probability, in [0,1]')
parser.add_argument('--use_dense', default=0, help='use densenet161' )
parser.add_argument('--use_NAS', action='store_true', help='use NAS' )
parser.add_argument('--warm_epoch', default=0, type=int, help='the first K epoch that needs warm up')
parser.add_argument('--lr', default=0.5, type=float, help='learning rate')
parser.add_argument('--droprate', default=0.5, type=float, help='drop rate')

opt = parser.parse_args()

fp16 = opt.path
data_dir = opt.lr
name = opt.path


def csv2sas(data):

    return data

# pandas dataframe 为数据处理所用格式，不会出现直接的csv2sas
# 可直接用pd的函数保存sas，如需

def sas2csv(data):

    return data

# we assume currently the sourse file is either sas, jmp or csv format
def read_data(path):

    if path.endswith('.sas7bdat'):
        df = pd.read_sas(path)
    elif path.endswith('.jmp'):
        jmp = Dispatch("JMP.Application")
        doc = jmp.OpenDocument(path)
        # temporarily add csv file
        doc.SaveAs('C:/Users/1000297658/Desktop/dataset/sasjmpfile.csv')
        df = pd.read_csv('C:/Users/1000297658/Desktop/dataset/sasjmpfile.csv')
        # Delete the extraly generated csv file 
        # to ensure that the data warehouse has not changed
        os.remove('C:/Users/1000297658/Desktop/dataset/sasjmpfile.csv')
    else:
        df = pd.read_csv(path)

    return df

"""
随机采样 Random (down)sampling

1. The original dataset may be too large, 
the plotting/computing time is too long and the memory overhead is too large

2. Split train-val/test set for machine learning.

Given a dataframe containing N rows, sampling n random rows from it, 
where n <= N

The input parameter is either the number of sample needed (n) or the ratio/fraction (n/N)

"""

def random_sampling(df, sub_sample_n = None, sub_sample_frac = None):
    if sub_sample_n:
        subset = df.sample(n = sub_sample_n)
    else:
        subset = df.sample(frac = sub_sample_frac)

    remaining = df.drop(labels=subset.index)
    # remaining = df[~df.index.isin(subset.index)]
    return subset, remaining


"""
Outlier detection 异常值检测
3-Sigma, al method (no Machine Learning here)

"""
def three_sigma_outlier_detection(data):


    return data



"""
重复行处理
Duplicated row process
"""

def duplication_process(data):

    return data

"""
数据的标准化和归一化
normalise(data)
standardise(data)

所有被归一化的列都必须是float型数据或者int型数据
字符型与布尔型不参与归一化/标准化

默认按列操作
"""
def normalise(data):
    
    # 获取完整列名
    cols=list(data)
    # cols = df.columns.values.tolist()
    
    # 每列里数据类型为string或bool的跳过
    for item in cols:
        if data[item].dtype in ['string', 'bool']:
            continue
        max_tmp = np.max(np.array(data[item]))
        min_tmp = np.min(np.array(data[item]))
        data[item] = data[item].apply(lambda x: (x - min_tmp) / (max_tmp - min_tmp + 1e-6))
    
    return data


def standardise(data):

    # 获取完整列名
    cols=list(data)

    # 每列里数据类型为string或bool的跳过
    for item in cols:
        print(data[item].dtype in ['string', 'bool'])
        if data[item].dtype in ['string', 'bool']:
            continue
        mean_tmp = np.mean(np.array(data[item]))
        std_tmp = np.std(np.array(data[item]))
        data[item] = data[item].apply(lambda x: (x - mean_tmp) / std_tmp + 1e-6)

    return data


# def normalise(data):
    print("Normalising ......")
    print(np.max(data), np.min(data))
    max_min_range = np.max(data) - np.min(data)

    return (data - np.min(data)) / max_min_range

# def standardise(data):
    print("Standardsing ......")
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)

    return (data - mu) / sigma



"""
数据导出
export_data(format)

"""
def export_data(data, save_process_flag, target_path):
    if save_process_flag == True:
        data.to_csv(target_path)





if __name__ == '__main__':


    path = opt.path
    print(path)
    print(path.endswith('.csv'))

    d = read_data(path)
    print('float64' in ['string', 'bool'])
    print(None, 'string' or 'bool')

    d = normalise(d)

    print(d)

    # save_process_flag = False
    # target_path = None
















