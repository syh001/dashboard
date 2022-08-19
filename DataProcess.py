import numpy as np
import pandas as pd
import os
from sas7bdat import SAS7BDAT
from win32com.client import Dispatch
import random
import shutil
import argparse

parser = argparse.ArgumentParser(description='Settings')

parser.add_argument('--path', 
                    default = 'C:/Users/1000297658/Desktop/dataset/wafer_0.6.jmp', 
                    type=str, 
                    help='sourse file path'
                    )

parser.add_argument('--sub_sample_n',
                    default = None,
                    type = int,
                    help='number of sub-sampling, range 0 ~ N (N sample number of raw data)'
                    )

parser.add_argument('--sub_sample_frac',
                    default = None,
                    type = float,
                    help='fraction of sub-sampling, range 0(.0) ~ 1(.0)'
                    )

parser.add_argument('--sigma',
                    default = 3,
                    type = int,
                    help='n-sigma to remove outliers, default is wellknown 3-sigma'
                    )

parser.add_argument('--remove_duplicates',
                    default= False,
                    type = bool,
                    help='remove duplicated raws' )

# ----------------------------------------------------------------------------
parser.add_argument('--batchsize', default=16, type=int, help='batchsize')
parser.add_argument('--stride', default=2, type=int, help='stride')
parser.add_argument('--erasing_p', default=0, type=float, help='Random Erasing probability, in [0,1]')
parser.add_argument('--use_dense', default=0, help='use densenet161' )
parser.add_argument('--use_NAS', action='store_true', help='use NAS' )
parser.add_argument('--warm_epoch', default=0, type=int, help='the first K epoch that needs warm up')
parser.add_argument('--lr', default=0.5, type=float, help='learning rate')
parser.add_argument('--droprate', default=0.5, type=float, help='drop rate')

opt = parser.parse_args()

path = opt.path
sub_sample_n = opt.sub_sample_n
sub_sample_frac = opt.sub_sample_frac
remove_duplicates = opt.remove_duplicates


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

def three_sigma_index(col, sigma):
    """
    col: 传入DataFrame的某一列。
    """
    rule = (col.mean() - sigma * col.std() > col) | (col.mean() + sigma * col.std() < col)
    index = np.arange(col.shape[0])[rule]

    return index  #返回落在3sigma之外的行索引值

def delete_out3sigma(df, sigma):
    """
	data: 待检测的DataFrame
    """
    out_index = [] #保存要删除的行索引
    for i in range(df.shape[1]): # 对每一列分别用3sigma原则处理
        index = three_sigma_index(df.iloc[:, i], sigma)
        out_index += index.tolist()
    delete_ = list(set(out_index))
    print('所删除的行索引为：', delete_)
    df.drop(delete_, inplace = True)

    return df


"""
重复行处理
Duplicated row process

"""

def remove_duplicates(df):

    # 检查重复行
    print(df.duplicated())
    # remove duplicated
    df = df.drop_duplicates()

    return df

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

    data = read_data(path)

    if remove_duplicates:
        data = remove_duplicates(data)

    print(opt.path)
    print(path.endswith('.csv'))

    print('float64' in ['string', 'bool'])
    print(None, 'string' or 'bool')

    data = normalise(data)

    print(data)

    # save_process_flag = False
    # target_path = None
















