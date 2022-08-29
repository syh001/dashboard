from django.shortcuts import render
from django.http import HttpResponse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
from win32com.client import Dispatch
import json

try:
    import six  # for modern Django
except ImportError:
    from django.utils import six  # for legacy Django

# Create your views here.

# is sql important?
# how WD manage data/dataset?
# which data format is most often used?


sourth_path = 'C:/Users/1000297658/Desktop/dataset/'
target_path = 'C:/Users/1000297658/Desktop/dataset/'
file_name = 'Return_yeah.csv'
file_name_save = 'Return_yeah.csv'

# 该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
D_MULTI_SELECT = {
    'Feature 1 | 特征 1': 'feature_1',
    'Feature 2 | 特征 2': 'feature_2',
    'Feature 3 | 特征 3': 'feature_3',
    'Feature 4 | 特征 4': 'feature_4',
    'Feature 5 | 特征 5': 'feature_5',
    'Feature 10 | 特征 10': 'feature_10',
    'Feature 20 | 特征 20': 'feature_20',
    'Feature 30 | 特征 30': 'feature_30',
    'Feature 40 | 特征 40': 'feature_40',
    'Feature 50 | 特征 50': 'feature_50',
}

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

def get_kpi(df, column='ph1_unbalance_hde', axis = 0):

    df = df.loc[:, [column]]

    print(df)
    print(df.mean(axis))
    try:
        df_mean = df.mean(axis)[0]
        df_std = df.std(axis)[0]
        df_median = df.median(axis)[0]
    
    except:
        df_mean = 'N/A'
        df_std = 'N/A'
        df_median = 'N/A'

    return {
        "df_mean": df_mean,
        "df_std": df_std,
        "df_median": df_median,
    }


def columns2dictionary(df):
    """
    该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
    从DataFrame里读取生成, key即是value, 所见即所得
    
    """
    dictionary = {col: col for col in df.columns}

    # print(dictionary)

    return dictionary

def get_distinct_list(df, column):

    # print(df[column].unique())
    l = df[column].unique()

    return l

def search(request, column, kw, df):
    
    try:
        df = df
        l = df.values.flatten().tolist()
        results_list = []
        for element in l:
            option_dict = {'name': element,
                           'value': element,
                           }
            results_list.append(option_dict)
        res = {
            "success": True,
            "results": results_list,
            "code": 200,
        }
    except Exception as e:
        res = {
            "success": False,
            "errMsg": e,
            "code": 0,
        }
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json charset=utf-8") # 返回结果必须是json格式


def query(request, source_path=sourth_path, target_path=target_path, file_name=file_name, file_name_save=file_name_save):
    """
    query方法要实现以下后续功能:

    a. 解析前端参数到理想格式
    b. 根据前端参数数据拼接SQL并用Pandas读取
    c. Pandas读取数据后, 将前端选择的DIMENSION作为pivot_table方法的column参数
    d. 返回Json格式的结果
    """
    form_dict = dict(six.iterlists(request.GET))

    print('request.GET:\n', request.GET)
    print('obtained dictionary:\n', form_dict)

    # print('\nget some elements:\n', form_dict['Feature1'][0])

    # df = pd.read_excel('C:/Users/sas053/Desktop/jmp_feature_importance.xlsx') #将sql语句结果读取至Pandas Dataframe
    df = pd.read_csv('C:/Users/1000297658/Desktop/dataset/Return_yeah.csv') #将sql语句结果读取至Pandas Dataframe

    df = read_data(source_path, target_path, file_name, file_name_save)
    df = df.iloc[0:30]

    kpi = get_kpi(df)
 
    if form_dict:
        column = form_dict['Feature1'][0]
        kpi = get_kpi(df, column)
        df = df.loc[:, [column]]

    print(df)
    
    context = {
        "df_mean": kpi["df_mean"],
        "df_std": kpi["df_std"],
        "df_median": kpi["df_median"],
        'data': df.to_html(),
    }
    
    return HttpResponse(json.dumps(context, ensure_ascii=True), content_type="application/json charset=utf-8") # 返回结果必须是json格式


def index(request, source_path=sourth_path, target_path=target_path, file_name=file_name, file_name_save=file_name_save):
 
    mselect_dict = {}

    form_dict = dict(six.iterlists(request.GET))
    print('request.GET:\n', request.GET)
    print('obtained dictionary:\n', form_dict)

    df = pd.read_csv('C:/Users/1000297658/Desktop/dataset/Return_yeah.csv') #将sql语句结果读取至Pandas Dataframe
    df = read_data(source_path, target_path, file_name, file_name_save)
    df = df.iloc[0:50]

    dct = columns2dictionary(df)

    # D_MULTI_SELECT
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value) # 以后可以后端通过列表为每个多选控件传递备选项

    context = {
        'mselect_dict': mselect_dict,
    }
    
    return render(request, 'visual/display.html', context)
    # return HttpResponse(df.to_html(max_cols=10,show_dimensions=True)) #渲染，这里暂时渲染为最简单的HttpResponse，以后可以扩展
