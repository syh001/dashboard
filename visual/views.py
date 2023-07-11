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
import json
from random import randrange

from django.http import HttpResponse
# from rest_framework.views import APIView
root_path = './'
sourth_path = 'C:/Users/sas053/Desktop/dataset'
target_path = 'C:/Users/sas053/Desktop/dataset'
file_name = 'test.csv'
file_name_save = 'return_test.xlsx'

global DF
DF = pd.read_csv('C:/Users/1000300246/Desktop/test_drawpic.csv')

def test_read_speed():
    since = time.time()
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

    # print(df)
    # print(df.mean(axis))
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
    # data = dict(six.iterlists(request.GET))
    con = {
        'alldata': df.to_html(),
    }
    return HttpResponse(json.dumps(con, ensure_ascii=False),
                        content_type="application/json charset=utf-8")

def query(request, data=DF):
    form_dict = dict(six.iterlists(request.GET))
    print('query', form_dict)
    df = data
    # box = []
    if form_dict:
        global x_feature, y_feature, box
        x_feature = form_dict['Feature1'][0]
        y_feature = form_dict['Feature2'][0]
        box = [x_feature, y_feature]
        multi_con = form_dict['Feature_opt[]']
        for i in multi_con:
            box.append(i)
        kpi = get_kpi(df, x_feature)
        # df = df.loc[:, [x_feature]]
        df = df.loc[:, box]
    # print(x_feature, y_feature, multi_con)
    box_df = pd.DataFrame(df)
    context = {
        "df_mean": kpi["df_mean"],
        "df_std": kpi["df_std"],
        "df_median": kpi["df_median"],
        'data': df.to_html(),
        'data_': box_df.to_html(),
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式

def query1(request, data=DF):
    form_dict = dict(six.iterlists(request.GET))
    print('query1', form_dict)
    if form_dict:
        global process_choose, query1_data
        process_choose = str(form_dict['process_choose[]'][0])
        print('process_choose', process_choose)
        query1_data = DF[DF['Process'] == process_choose]
    context = {
        "process_choose": 1,
        "query1_data": query1_data.to_json(),
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式


def plot(request):
    type = list(dict(six.iterlists(request.GET)).keys())[0]
    # item = dict(six.iterlists(request.GET)).keys()
    print('===============', type, '==================')

    if type == 'Combine':
        chart = echarts_barline(DF, x_feature, y_feature, box)
    elif type == 'Line':
        chart = echarts_myline(DF, x_feature, y_feature, box)
    elif type == 'Stack':
        chart = echarts_stackbar(DF, x_feature, y_feature, box)

    elif type == 'Plot':

        chart = echarts_two_test(query1_data, process_choose)

    chart = chart.dump_options()


    total_trend = json.loads(chart)
    # print('total_trend', type(total_trend))
    context = {
        'total_trend': total_trend,

    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")

def index(request):
    mselect_dict = {}
    dic = {}
    form_dict = dict(six.iterlists(request.GET))
    df = DF
    dct = columns2dictionary(df)
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value) # 以后可以后端通过列表为每个多选控件传递备选项
        dic[key] = list(set(get_distinct_list(df, value).tolist()))
    # print('dic', dic)
    # print('Pricess', dic['Process'])
    context = {
        'mselect_dict': mselect_dict,
        'Process': dic['Process'],
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

def choose_path_file():
    import os
    current_address = os.path.dirname(os.path.abspath(__file__))
    for parent, dirnames, filenames in os.walk(current_address):
        # Case1: traversal the directories
        for dirname in dirnames:
            print("Parent folder:", parent)
            print("Dirname:", dirname)
        # Case2: traversal the files
        for filename in filenames:
            print("Parent folder:", parent)
            print("Filename:", filename)

def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
        .dump_options_with_quotes()
    )
    return c


