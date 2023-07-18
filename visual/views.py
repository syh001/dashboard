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
DF = pd.read_csv('C:/Users/1000300246/Desktop/HDDMagnetic.csv')


def test_read_speed():
    since = time.time()
    print('it costs: ', time.time() - since, 's to load the file')
    print(DF.memory_usage().sum() / (1024 ** 2), 'MB')
    since = time.time()
    df_col = DF.iloc[:, 7]
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


# 该字典key为前端准备显示的所有多选字段名, value为数据库对应的字段名
D_MULTI_SELECT = {
    'YC': ['Yield', 'EC'],
    'Magnetic': ['ACC', 'MCW', 'Roller SER'],
    'Reader HI': ['1k-BEM(Rd)NT', '1k-BEM(Rd)HT', 'Bi-state XTI Profile (writer induced HI)', '172c'],
    'PE': ['PE NT (Degauss on)', 'PE HT (Degauss off/on)'],
    'XTI': ['XTI NT', 'XTI HT'],
    'XTI Degradation': ['Delta XTI', 'Delta OWC'],
    'Writer instability': ['1K-BEM (WrRd) HT', 'RV_Range', 'B_Allband'],
    'Writer degradation': ['Delta MCW', 'Delta SER', 'Delta OW'],
    'Write-short': ['UEC (S5W, Func, SRST, Fin & Featuring)'],
}

def index(request):
    mselect_dict = {}
    dic = {}
    form_dict = dict(six.iterlists(request.GET))
    df = DF
    dct = columns2dictionary(df)
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value)  # 以后可以后端通过列表为每个多选控件传递备选项
        dic[key] = list(set(get_distinct_list(df, value).tolist()))
    print('mselect_dict', mselect_dict)
    context = {
        'mselect_dict': mselect_dict,
        'D_MULTI_SELECT': D_MULTI_SELECT,
        'Product': dic['PRODUCT'],
        'Model': dic['HDD_Model'],
    }
    # 下面一定要返回子模板，否则的话是block与endblock失效的原因！！！
    return render(request, 'visual/plot.html', context)

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
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json charset=utf-8")  # 返回结果必须是json格式


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
        df = df.loc[:, box]
    box_df = pd.DataFrame(df)
    print('aaaaaaa', x_feature, y_feature, kpi)
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
        chart = page_simple_layout()
        # chart = echarts_two_test(query1_data, process_choose)

    chart = chart.dump_options()

    total_trend = json.loads(chart)
    # print('total_trend', type(total_trend))
    context = {
        'total_trend': total_trend,

    }
    return HttpResponse(json.dumps(context, ensure_ascii=False),
                        content_type="application/json charset=utf-8")


def blog(request):
    mselect_dict = {}
    form_dict = dict(six.iterlists(request.GET))
    df = DF.iloc[0:50]
    dct = columns2dictionary(df)
    for key, value in dct.items():
        mselect_dict[key] = {}
        mselect_dict[key]['select'] = value
        mselect_dict[key]['options'] = get_distinct_list(df, value)  # 以后可以后端通过列表为每个多选控件传递备选项
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


def get_process_name(request):
    product_choose = request.POST.get("product_choose")
    model_choose = request.POST.get("model_choose")
    df_pho = DF[(DF['PRODUCT'] == product_choose) & (DF['HDD_Model'] == model_choose) & (DF['HEAD_SITE'] == 'PHO')]
    df_pho = df_pho.dropna()
    df_tho = DF[(DF['PRODUCT'] == product_choose) & (DF['HDD_Model'] == model_choose) & (DF['HEAD_SITE'] == 'THO')]
    df_tho = df_tho.dropna()
    pho_qty = [np.array(df_pho['QTY_6400']).tolist(), np.array(df_pho['MCW_MD']).tolist(),
               np.array(df_pho['Resi_pACC']).tolist()]

    pho_line = [np.array(df_pho['Resi_OWP_MD_Post']).tolist(), np.array(df_pho['Resi_FinalSER']).tolist()]

    tho_qty = [np.array(df_tho['QTY_6400']).tolist(), np.array(df_tho['MCW_MD']).tolist(),
               np.array(df_tho['Resi_pACC']).tolist()]
    tho_line = [np.array(df_tho['Resi_OWP_MD_Post']).tolist(), np.array(df_tho['Resi_FinalSER']).tolist()]
    col_name = ['QTY_6400', 'MCW_MD', 'Resi_pACC', 'Resi_OWP_MD_Post', 'Resi_FinalSER']
    lis1 = ['a', 'b', 'c', 'd', 'Fri', 'Sat', 'Sun']
    lis2 = [150, 230, 224, 218, 135, 147, 260]

    # col_name = ['Evaporation', 'Precipitation', 'Temperature', 'temp']
    # x_date = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # bar_1 =[
    #     2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3
    #   ]
    # bar_2 =[
    #     2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3
    #   ]
    # line_1 =[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
    # line_2 =[20.3, 23.4, 23.0, 16.5, 12.0, 6.2, 2.0, 2.2, 3.3, 4.5, 6.3, 10.2]
    return render(request, './visual/plot.html', {
        "pho_qty": pho_qty,
        "pho_line": pho_line,
        "tho_qty": tho_qty,
        "tho_line": tho_line,
        "col_name": col_name,
        "pho_date": np.array(df_pho['Date']).tolist(),
        "tho_date": np.array(df_tho['Date']).tolist(),
        "lis1" : lis1,
        "lis2" : lis2,


        "product_choose": product_choose,
        "model_choose": model_choose
    })
