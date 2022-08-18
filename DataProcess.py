import numpy as np
import pandas as pd
import os
import scipy
from sas7bdat import SAS7BDAT
from win32com.client import Dispatch
import random
import shutil

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

The original dataset may be too large, 
the plotting/computing time is too long and the memory overhead is too large

Given a dataframe containing N rows, sampling n random rows from it, 
where n <= N

The input parameter is either the number of sample needed (n) or the ratio/fraction (n/N)

"""

def random_sampling(df, n = None, frac = None):
    if n:
        subset = df.sample(n = n)
    else:
        subset = df.sample(frac = frac)

    return subset


"""
Outlier detection 异常值检测
3-Sigma, al method (no Machine Learning here)

"""
def three_sigma_outlier_detection(data):


    return None



"""
重复行处理
Duplicated row process
"""

def duplication_process():

    return None

"""
数据的标准化和归一化
normalise(data)
standardise(data)

所有被归一化的列都必须是float型数据或者int型数据
字符型与布尔型不参与归一化/标准化

默认按列操作
"""
def normalise(df):
    
    # 获取完整列名
    cols=list(df)
    # cols = df.columns.values.tolist()
    
    # 每列里数据类型为string或bool的跳过
    for item in cols:
        if df[item].dtype == 'string' or 'bool':
            continue
        max_tmp = np.max(np.array(df[item]))
        min_tmp = np.min(np.array(df[item]))
        df[item] = df[item].apply(lambda x: (x - min_tmp) / (max_tmp - min_tmp + 1e-6))
    
    return df


def standardise(df):

    cols=list(df)   # 可以改成自己需要的列的名字
    
    for item in cols:
        mean_tmp = np.mean(np.array(df[item]))
        std_tmp = np.std(np.array(df[item]))
        df[item] = df[item].apply(lambda x: (x - mean_tmp) / std_tmp + 1e-6)

    return df


# def normalise(data):
    print("Normalising ......")
    print(np.max(data), np.min(data))
    max_min_range = np.max(data) - np.min(data)

    return (data - np.min(data)) / max_min_range

def standardise(data):
    print("Standardsing ......")
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)

    return (data - mu) / sigma


"""
数据导出
export_data(format)

"""
path = 'C:/Users/1000297658/Desktop/dataset/wafer_0.6.jmp'
print(path.endswith('.csv'))
d = read_data(path)
# d = pd.read_csv(path)

print(d)

normalise(d)

















