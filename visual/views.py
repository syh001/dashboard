from django.shortcuts import render
from django.http import HttpResponse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
from win32com.client import Dispatch

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


def columns2dictionary(df):
    """
    该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
    从DataFrame里读取生成, key即是value, 所见即所得
    
    """
    dictionary = {col: col for col in df.columns}

    # print(dictionary)

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


# def index(request):
    
#     ...

    
#     context = {
#        ...
#        'mselect_dict': mselect_dict
#     }
#     return render(request, 'chpa_data/analysis.html', context) # 注意本句和前一章也有变化，渲染至analysis.html而不是display.html




def index(request, source_path=sourth_path, target_path=target_path, file_name=file_name, file_name_save=file_name_save):
    # 标准sql语句，此处为测试返回数据库data表的数据条目n，之后可以用python处理字符串的方式动态扩展
    # sql = "Select count(*) from data" 
    mselect_dict = {}

    # df = pd.read_excel('C:/Users/sas053/Desktop/jmp_feature_importance.xlsx') #将sql语句结果读取至Pandas Dataframe
    df = pd.read_csv('C:/Users/1000297658/Desktop/dataset/Return_yeah.csv') #将sql语句结果读取至Pandas Dataframe

    df = read_data(source_path, target_path, file_name, file_name_save)
    df = df.iloc[0:3]
    # certain_one.columns = [''] * len(certain_one.columns)
    # certain_one = pd.DataFrame(certain_one.iloc[0:2,1], header = None)
    print(type(pd.DataFrame(df.iloc[0,1:3])), '\n', df)
    # certain_one = np.mean(certain_one)
    # print(type(certain_one.keys()))
    # certain_one = certain_one.columns
    # context = {'data': df}

    dct = columns2dictionary(df)
    # D_MULTI_SELECT
    for key, value in D_MULTI_SELECT.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        # mselect_dict[key]['options'] = option_list 以后可以后端通过列表为每个多选控件传递备选项
    

    context = {
        'data': df,
        'mselect_dict': mselect_dict,
    }
    

    return render(request, 'visual/analysis.html', context)
    # return HttpResponse(df.to_html(max_cols=10,show_dimensions=True)) #渲染，这里暂时渲染为最简单的HttpResponse，以后可以扩展
