from django.shortcuts import render
from django.http import HttpResponse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
from win32com.client import Dispatch
import json
try:
    import six
except ImportError:
    from django.utils import six
# Create your views here.

# is sql important?
# how WD manage data/dataset?
# which data format is most often used?


sourth_path = 'C:/Users/1000297658/Desktop/dataset/'
target_path = 'C:/Users/1000297658/Desktop/dataset/'
file_name = 'Return_yeah.csv'
file_name_save = 'Return_yeah.csv'

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

def get_kpi(df, axis = 0):
    # print(df)
    df = df.iloc[:, 8:9]
    df_mean = df.mean(axis)[0]
    
    df_std = df.std(axis)[0]
    
    df_median = df.median(axis)[0]
    
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
    return dictionary

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

def index(request, source_path=sourth_path, target_path=target_path, file_name=file_name, file_name_save=file_name_save):
 
    mselect_dict = {}

    df = pd.read_excel('C:/Users/sas053/Desktop/feature_importance.xlsx') #将sql语句结果读取至Pandas Dataframe
    # df = pd.read_csv('C:/Users/1000297658/Desktop/dataset/Return_yeah.csv') #将sql语句结果读取至Pandas Dataframe
    # df = read_data(source_path, target_path, file_name, file_name_save)
    kpi = get_kpi(df)

    dct = columns2dictionary(df)
    # D_MULTI_SELECT
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        # mselect_dict[key]['options'] = option_list 以后可以后端通过列表为每个多选控件传递备选项
    
    df = df.iloc[:, 8:9]
    context = {
        "df_mean": kpi["df_mean"],
        "df_std": kpi["df_std"],
        "df_median": kpi["df_median"],
        'data': df.to_html(),
        'mselect_dict': mselect_dict,
    }
    # return render(request, 'visual/analysis.html', context)
    return render(request, 'visual/display.html', context)
    # return HttpResponse(df.to_html(max_cols=10,show_dimensions=True)) #渲染，这里暂时渲染为最简单的HttpResponse，以后可以扩展




def query(request):
    form_data = request.GET.get('form_data')
    print('===============')
    print(form_data)
    print('===============')

    # form_dict = dict(six.iterlists(request.GET))
    # sql = sqlparse(form_dict)  # sql拼接
    # print(sql)
    # df = pd.read_sql_query(sql)  # 将sql语句结果读取至Pandas Dataframe
    #
    # dimension_selected = form_dict['DIMENSION_select'][0]
    # print(dimension_selected)
    # #  如果字段名有空格为了SQL语句在预设字典中加了中括号的，这里要去除
    # if dimension_selected[0] == '[':
    #
    #     column = dimension_selected[1:][:-1]
    # else:
    #     column = dimension_selected
    # pivoted = pd.pivot_table(df,
    #                          values='AMOUNT',  # 数据透视汇总值为AMOUNT字段，一般保持不变
    #                          index='DATE',  # 数据透视行为DATE字段，一般保持不变
    #                          columns=column,  # 数据透视列为前端选择的分析维度
    #                          aggfunc=np.sum)  # 数据透视汇总方式为求和，一般保持不变
    # if pivoted.empty is False:
    #     pivoted.sort_values(by=pivoted.index[-1], axis=1, ascending=False, inplace=True)  # 结果按照最后一个DATE表现排序
    #
    # # KPI
    # kpi = get_kpi(pivoted)
    #
    # context = {
    #     "market_size": kpi["market_size"],
    #     "market_gr": kpi["market_gr"],
    #     "market_cagr": kpi["market_cagr"],
    #     # 'ptable': ptable(pivoted).to_html()
    # }

    return HttpResponse(json.dumps(form_data, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式