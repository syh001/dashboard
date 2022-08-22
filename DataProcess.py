from multiprocessing.reduction import duplicate
import numpy as np
import pandas as pd
import os
from sas7bdat import SAS7BDAT
from win32com.client import Dispatch
import random
import shutil
import argparse
parser = argparse.ArgumentParser(description='Settings')

parser.add_argument('--file_name', 
                    default = 'Return_yeah.csv', 
                    type=str, 
                    help='sourse file path'
                    )

parser.add_argument('--file_name_save', 
                    default = 'Return_yeah_1.csv', 
                    type=str, 
                    help='sourse file path'
                    )

parser.add_argument('--source_path', 
                    default = 'C:/Users/1000297658/Desktop/dataset/', 
                    type=str, 
                    help='sourse file path'
                    )

parser.add_argument('--target_path', 
                    default = 'C:/Users/1000297658/Desktop/dataset/', 
                    type=str, 
                    help='target file path'
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

parser.add_argument('--remove_duplicates_flag',
                    default = False,
                    type = bool,
                    help='remove duplicated rows' )

parser.add_argument('--remove_outliers_flag',
                    default = False,
                    type = bool,
                    help='remove outliers' )

parser.add_argument('--save_csv',
                    default = True,
                    type = bool,
                    help='whether save DataFrame into a .csv file' )


# ---------------------------------syh-------------------------------------------

parser.add_argument('--threshold',
                    default = 0.8,
                    type = float,
                    help='the percentage of which the missing values should be deleted')

parser.add_argument('--fill_nan_method',
                    default = 'mean',
                    type = str,
                    help='how you would like to fill the missing values(mean median or mode)')

parser.add_argument('--column_to_change',
                    default = ['JOBNUM'],
                    help='how you would like to fill the missing values')

parser.add_argument('--column_to_change',
                    default = [],
                    type = list,
                    help='choose the column name that you want to change')

parser.add_argument('--new_column_name',
                    default = ['jobnum'],
                    type = list,
                    help='the corresponding column name of each changed column')

parser.add_argument('--new_column_type',
                    default = ['float'],
                    type = list,
                    help='the corresponding data type of each changed column')

parser.add_argument('--date_column_name',
                    default = 'date',
                    type = str,
                    help='the column name which represents datetime')

# ----------------------------------------------------------------------------
parser.add_argument('--batchsize', default=16, type=int, help='batchsize')
parser.add_argument('--stride', default=2, type=int, help='stride')

opt = parser.parse_args()

file_name_save = opt.file_name_save
file_name = opt.file_name
source_path = opt.source_path
sub_sample_n = opt.sub_sample_n
sub_sample_frac = opt.sub_sample_frac
remove_duplicates_flag = opt.remove_duplicates_flag
remove_outliers_flag = opt.remove_outliers_flag
save_csv = opt.save_csv
target_path = opt.target_path


sigma = opt.sigma
column_to_change = opt.column_to_change
new_column_type = opt.new_column_type
new_column_name = opt.new_column_name
date_column_name = opt.date_column_name
threshold = opt.threshold
fill_nan_method = opt.fill_nan_method


def csv2sas(data):

    return data

# pandas dataframe 为数据处理所用格式，不会出现直接的csv2sas
# 可直接用pd的函数保存sas，如需

def sas2csv(data):

    return data


# we assume currently the sourse file is either sas, jmp or csv format
def read_data(source_path, target_path, file_name, file_name_save):

    source_file = source_path + file_name
    target_file = target_path + file_name_save

    if source_file.endswith('.sas7bdat'):
        df = pd.read_sas(source_file)
    elif source_file.endswith('.jmp'):
        jmp = Dispatch("JMP.Application")
        doc = jmp.OpenDocument(source_file)
        # temporarily add csv file
        doc.SaveAs(target_file)
        df = pd.read_csv(target_file)
        # Delete the extraly generated csv file 
        # to ensure that the data warehouse has not changed
        os.remove(target_path + file_name_save)
    else:
        df = pd.read_csv(source_file)

    return df

#扫描各特征的数据类型
def data_scan_type(df):
    return pd.DataFrame(df.dtypes)

#改变列的数据类型
def change_data_type(df, column = column_to_change, type = new_column_type):

    for i in range(len(column)):
        df[column[i]].astype(type[i])

    return df

#重新命名列名
def data_rename_column(df, column = column_to_change,new_name = new_column_name):

    for i in range(len(column)):
        df.rename(columns ={ column[i]: new_name[i]})

    return df

#功能是按阈值筛选掉缺失值大于多少的列，并返回剩余的数据
def detect_nan_by_column(df, threshold = threshold):

    feature = []
    row_num = df.shape[0]
    dic = df.isnull().sum().to_dict()

    for i in dic:
        if (dic[i] / row_num) > threshold:
            feature.append(i)

    new_data = df.drop(feature, axis = 1)

    return new_data

#按阈值筛选掉缺失值大于多少的行，并返回剩余的数据
def detect_nan_by_row(df, threshold = threshold):

    new_data = pd.DataFrame()

    if threshold == 0:
        new_data = df.dropna()
    else:
        nan_len=0
        col_name = df.columns.tolist()

        for row_index, row in df.iterrows():
            for col in col_name:
                tmp = df.loc[row_index, col]
                if tmp != tmp:
                    nan_len += 1

            ratio = nan_len / len(col_name)

            if ratio < threshold:
                new_data = pd.concat([new_data, df.iloc[row_index,:]])

    return new_data

def fill_nan_data(df, criteria = fill_nan_method):

    col = df.columns[df.isnull().sum() > 0]

    for i in col:
        if criteria == 'mean':
            val = df[i].mean()
        elif criteria == 'median':
            val = df[i].median()
        elif criteria == 'mode':
            val = df[i].mode()[0]

        df[i].fillna(val, inplace = True)

    return df

def check_data_by_date(df, date_column_name=date_column_name):

    df['new_date'] = ""
    df['new_index'] = 0
    multi_df = []

    for row_index, row in df.iterrows():
        df.loc[row_index, 'new_date'] = parser.parse(str(df.loc[row_index,date_column_name]))
    
    df.index = pd.to_datetime(df.new_date)
    df['new_index'] = df.index.isocalendar().week
    col = df['new_index'].tolist()
    df_ = df.reset_index(drop=True)

    for i in col:
        new = df_[df_['new_index']==i]
        new1 = new.reset_index(drop=True)
        new2 = new1.drop(['new_date', 'new_index'], axis=1)
        multi_df.append(new2)

    return multi_df


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
    elif sub_sample_frac:
        subset = df.sample(frac = sub_sample_frac)
    else:
        subset = df
    remaining = df.drop(labels = subset.index)
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
	df: 待检测的DataFrame

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
    # print(df.duplicated())
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

def normalise(df):
    
    # 获取完整列名
    cols=list(df)
    # cols = df.columns.values.tolist()
    # 每列里数据类型为string或bool的跳过
    for item in cols:
        # print(df[item].dtype)
        if df[item].dtype in ['string', 'bool', 'object']:
            continue
        max_tmp = np.max(np.array(df[item]))
        min_tmp = np.min(np.array(df[item]))
        df[item] = df[item].apply(lambda x: (x - min_tmp) / (max_tmp - min_tmp + 1e-6))
    
    return df

def standardise(df):

    # 获取完整列名
    cols=list(df)

    # 每列里数据类型为string或bool的跳过
    for item in cols:
        if df[item].dtype in ['string', 'bool', 'object']:
            continue
        mean_tmp = np.mean(np.array(df[item]))
        std_tmp = np.std(np.array(df[item]))
        df[item] = df[item].apply(lambda x: (x - mean_tmp) / std_tmp + 1e-6)

    return df

"""
数据导出
export_data(format)

"""
def export_data(df, target_path, target_file):
    df.to_csv(target_path + target_file)


if __name__ == '__main__':

    data = read_data(source_path, target_path, file_name, file_name_save)

    print(data)

    if remove_duplicates_flag:
        data = remove_duplicates(data)
    
    if remove_outliers_flag:
        data = delete_out3sigma(data)

    # data = standa
    data = normalise(data)

    data, remain = random_sampling(data, sub_sample_n = None, sub_sample_frac = None)

    print(data, remain)

    if save_csv:
        export_data(data, target_path, file_name_save)

















