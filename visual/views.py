from django.shortcuts import render
from django.http import HttpResponse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
from django.shortcuts import render, redirect
from win32com.client import Dispatch
import json
from .charts import *
try:
    import six
except ImportError:
    from django.utils import six

sourth_path = 'C:/Users/sas053/Desktop/dataset'
target_path = 'C:/Users/sas053/Desktop/dataset'
file_name = 'test.csv'
file_name_save = 'return_test.xlsx'

DF = pd.read_csv('./test.csv')

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


def get_kpi(df, column, axis=0):
    df = df.loc[:, [column]]
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
    dictionary = {col: col for col in df.columns}
    return dictionary

def get_distinct_list(df, column):
    l = df[column].unique()
    return l
# from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
# from win32com.client import Dispatch
import json
from .charts import *
import matplotlib.pyplot as plt

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

# # global DF
# DF = pd.read_csv('./Return_yeah.csv') # 读取至Pandas Datafram

D_TRANS = {
            'MAT': '滚动年',
            'QTR': '季度',
            'Value': '金额',
            'Volume': '盒数',
            'Volume (Counting Unit)': '最小制剂单位数',
            '滚动年': 'MAT',
            '季度': 'QTR',
            '金额': 'Value',
            '盒数': 'Volume',
            '最小制剂单位数': 'Volume (Counting Unit)'
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

def prepare_chart(data, #全部dataframe
                  df,  # 输入经过pivoted方法透视过的df，不是原始df
                  chart_type,  # 图表类型字符串，人为设置，根据图表类型不同做不同的Pandas数据处理，及生成不同的Pyechart对象
                  form_dict,  # 前端表单字典，用来获得一些变量作为图表的标签如单位
                  ):
    # label = D_MULTI_SELECT[form_dict['PERIOD_select'][0]] + D_MULTI_SELECT[form_dict['UNIT_select'][0]]
    label = form_dict['Feature1'][0]
    print(label)
    if chart_type == 'bar_total_trend':
        df_abs = df.sum(axis=1)  # Pandas列汇总，返回一个N行1列的series，每行是一个date的市场综合
        print("#" * 30, df_abs)
        # df_abs.index = df_abs.index.strftime("%Y-%m")  # 行索引日期数据变成2020-06的形式
        df_abs = df_abs.to_frame()  # series转换成df
        print("-" * 30, df_abs)
        df_abs.columns = [label]  # 用一些设置变量为系列命名，准备作为图表标签
        df_gr = data.loc[df.index, form_dict['Feature2'][0]]

        # print("%" * 50 + '\n', df_gr.columns)
        # df_gr.columns = [form_dict['Feature2'][0]]

        # df_gr = df_abs.pct_change(periods=4)  # 获取同比增长率
        # df_gr.dropna(how='all', inplace=True)  # 删除没有同比增长率的行，也就是时间序列数据的最前面几行，他们没有同比
        # df_gr.replace([np.inf, -np.inf, np.nan], '-', inplace=True)  # 所有分母为0或其他情况导致的inf和nan都转换为'-'
        chart = echarts_stackbar(df=df_abs, #第一个维度
                                 df_gr=df_gr, #第二个维度
                                 line_name = form_dict['Feature2'][0])#第二维的列名
        return chart.dump_options()  # 用json格式返回Pyecharts图表对象的全局设置
    else:
        return None
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



def query(request, data=DF):
    form_dict = dict(six.iterlists(request.GET))
    # print('\nrequest.GET:\n', request.GET, '\n')
    # print('*' * 50, '\nobtained dictionary:\n', form_dict, '\n')
    df = data.iloc[0:30]
    box = []
    if form_dict:
        column = form_dict['Feature1'][0]
        sec = form_dict['Feature2'][0]
        box = [column, sec]
        multi_con = form_dict['Feature_opt[]']
        for i in multi_con:
            box.append(i)
        kpi = get_kpi(df, column)
        df = df.loc[:, [column]]
    box_df = pd.DataFrame(box)
    print('222222222222222233333333333333', kpi)
    flag=0
    bar_total_trend = ""
    if kpi["df_mean"]!='N/A':
        # Pyecharts交互图表
        bar_total_trend = json.loads(prepare_chart(data, df, 'bar_total_trend', form_dict))
        flag+=1
        # scatter_pic = echarts_scatter(data, form_dict)
        # scatter_pic = json.loads(scatter_pic.dump_options())
        # print('=============scatter pic is:=============', '\n', scatter_pic, '\n')

    context = {
        "df_mean": kpi["df_mean"],
        "df_std": kpi["df_std"],
        "df_median": kpi["df_median"],
        'data': df.to_html(),
        'data_': box_df.to_html(),
        # 'scatter_pic': scatter_pic,
        'bar_total_trend': bar_total_trend,
        'flag':flag
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式

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


def choose_file(request):
    """
    交互式(多)文件选择
    后端遍历路径下的文件名 并传至前端候选
    在前端点击所选的文件通过request返回后端一个list供read_data()读取
    
    """
    file_list_dict = dict(six.iterlists(request.GET))
    file_list = os.path()

    return file_list


# def query(request, df = DF):
#     """
#     query方法要实现以下后续功能:
#
#     a. 解析前端参数到理想格式
#     b. 根据前端参数数据拼接SQL并用Pandas读取
#     c. Pandas读取数据后, 将前端选择的DIMENSION作为pivot_table方法的column参数
#     d. 返回Json格式的结果
#     """
#     form_dict = dict(six.iterlists(request.GET))
#
#     print('\nrequest.GET:\n', request.GET, '\n')
#     print('*'*50, '\nobtained dictionary:\n', form_dict, '\n')
#     print('*'*50)
#
#     # print('\nget some elements:\n', form_dict['Feature1'][0])
#     # df = pd.read_csv('./Crush_yeah.csv') #将sql语句结果读取至Pandas Dataframe
#
#     df = df.iloc[0:30]
#
#     # kpi = get_kpi(df)
#
#     if form_dict:
#         column = form_dict['Feature1'][0]
#         kpi = get_kpi(df, column)
#         df = df.loc[:, [column]]
#
#
#     context = {
#         "df_mean": kpi["df_mean"],
#         "df_std": kpi["df_std"],
#         "df_median": kpi["df_median"],
#         'data': df.to_html(),
#         'data_': box_df.to_html(),
#     }
#     return HttpResponse(json.dumps(context, ensure_ascii=False),
#                         content_type="application/json charset=utf-8")  # 返回结果必须是json格式


def showdata(request, df=DF):
    data = dict(six.iterlists(request.GET))
    print(request.method)
    print('读到了数据', data)
    con = {
        'alldata': df.to_html(),
    }
    return HttpResponse(json.dumps(con, ensure_ascii=False),
                        content_type="application/json charset=utf-8")


def index(request):

    mselect_dict = {}

    form_dict = dict(six.iterlists(request.GET))
    print('2222222222222222222222222222222222222222222222222222222222')
    print('*'*50, '\nobtained dictionary:\n', form_dict, '\n')
    print('*'*50)
    # global df
    # df = pd.read_csv('./Crush_yeah.csv') #将sql语句结果读取至Pandas Dataframe
    # df = read_data(source_path, target_path, file_name, file_name_save)
    df = DF.iloc[0:50]

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

def blog(request):
 
    mselect_dict = {}

    form_dict = dict(six.iterlists(request.GET))
    print('111111111111111111111111111111111111111111111111111111111111')
    print('*'*50, '\nobtained dictionary:\n', form_dict, '\n')
    print('*'*50)
    # global df
    # df = pd.read_csv('./Crush_yeah.csv') #将sql语句结果读取至Pandas Dataframe
    # df = read_data(source_path, target_path, file_name, file_name_save)
    df = DF.iloc[0:50]

    dct = columns2dictionary(df)

    # D_MULTI_SELECT
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value) # 以后可以后端通过列表为每个多选控件传递备选项

    context = {
        'mselect_dict': mselect_dict,
    }
    
    return render(request, 'visual/blog_main_display.html', context)
