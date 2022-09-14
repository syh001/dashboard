from django.http import HttpResponse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
from django.shortcuts import render, redirect
import json
from .charts import *
try:
    import six
except ImportError:
    from django.utils import six
import time

root_path = './'
sourth_path = 'C:/Users/sas053/Desktop/dataset'
target_path = 'C:/Users/sas053/Desktop/dataset'
file_name = 'test.csv'
file_name_save = 'return_test.xlsx'

since = time.time()
global DF
DF = pd.read_csv('./1024.csv')
print('it costs: ', time.time() - since, 's to load the file')
print(DF.memory_usage().sum()/(1024**2), 'MB')
since = time.time()
df_col = DF.iloc[:,7]
print('it costs: ', time.time() - since, 's to load the column')

def read_data(source_path, target_path, file_name, file_name_save):

    source_file = source_path + file_name
    target_file = target_path + file_name_save

    if source_file.endswith('.sas7bdat'):
        df = pd.read_sas(source_file)
    # elif source_file.endswith('.jmp'):
    #     jmp = Dispatch("JMP.Application")
    #     doc = jmp.OpenDocument(source_file)
    #     # temporarily add csv file
    #     doc.SaveAs(target_file)
    #     df = pd.read_csv(target_file)
    #     # Delete the extraly generated csv file 
    #     # to ensure that the data warehouse has not changed
    #     os.remove(target_path + file_name_save)
    else:
        df = pd.read_csv(source_file)

    return df


def get_kpi(df, column, axis = 0):

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

def columns2dictionary(df):
    """
    该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
    从DataFrame里读取生成, key即是value, 所见即所得
    """
    dictionary = {col: col for col in df.columns}

    return dictionary

def get_distinct_list(df, column):
    """
    获取一个feature下的不同的值，通过unique()函数
    改list返回可作为画图中的legend
    """
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


def choose_file(request):
    file_list_dict = dict(six.iterlists(request.GET))
    file_list = os.path()
    return file_list

def showdata(request, df=DF):
    data = dict(six.iterlists(request.GET))
    con = {
        'alldata': df.to_html(),
    }
    return HttpResponse(json.dumps(con, ensure_ascii=False),
                        content_type="application/json charset=utf-8")

def query(request, data=DF):
    form_dict = dict(six.iterlists(request.GET))
    df = data.iloc[0:30]
    box = []
    if form_dict:
        global x_feature, y_feature
        x_feature = form_dict['Feature1'][0]
        y_feature = form_dict['Feature2'][0]
        box = [x_feature, y_feature]
        multi_con = form_dict['Feature_opt[]']
        for i in multi_con:
            box.append(i)
        kpi = get_kpi(df, x_feature)
        df = df.loc[:, [x_feature]]
    box_df = pd.DataFrame(box)
    context = {
        "df_mean": kpi["df_mean"],
        "df_std": kpi["df_std"],
        "df_median": kpi["df_median"],
        'data': df.to_html(),
        'data_': box_df.to_html(),
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式

def plot(request):
    type = list(dict(six.iterlists(request.GET)).keys())[0]
    if type == 'Bar':
        chart = echarts_mybar(DF, x_feature, y_feature)
    elif type == 'Scatter':
        chart = echarts_myscatter(DF, x_feature, y_feature)
    elif type == 'Line':
        chart = echarts_myline(DF, x_feature, y_feature)
    chart = chart.dump_options()
    total_trend = json.loads(chart)
    context = {
        'total_trend': total_trend,
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")

def index(request):
    mselect_dict = {}
    form_dict = dict(six.iterlists(request.GET))
    # df = read_data(source_path, target_path, file_name, file_name_save)
    df = DF.iloc[0:50]
    dct = columns2dictionary(df)
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value) # 以后可以后端通过列表为每个多选控件传递备选项
    context = {
        'mselect_dict': mselect_dict,
    }
    return render(request, 'visual/display.html', context)

def blog(request):
    mselect_dict = {}
    form_dict = dict(six.iterlists(request.GET))
    df = DF.iloc[0:50]
    dct = columns2dictionary(df)
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value) # 以后可以后端通过列表为每个多选控件传递备选项
    context = {
        'mselect_dict': mselect_dict,
    }
    return render(request, 'visual/blog_main_display.html', context)
